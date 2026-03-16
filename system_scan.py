import psutil
import platform
import datetime
import time
import socket
import subprocess

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

try:
    import GPUtil
except:
    GPUtil = None

try:
    from ping3 import ping
except:
    ping = None


console = Console()


class SystemScanner:

    def __init__(self, speaker=None):
        self.speaker = speaker

    def speak(self, text):
        if self.speaker:
            self.speaker.speak(text)

    def check_internet(self):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except:
            return False

    def check_firewall(self):
        try:
            output = subprocess.check_output(
                "netsh advfirewall show allprofiles",
                shell=True
            ).decode()

            if "ON" in output:
                return "Enabled"
            else:
                return "Disabled"
        except:
            return "Unknown"

    def run_scan(self):

        console.print("\n[bold cyan]⚡ Artery starting...[/bold cyan]")
        self.speak("Artery starting")

        with console.status("[bold green]🔍 Artery scanning the system..."):
            time.sleep(2)

        self.speak("Artery scanning the system")

        now = datetime.datetime.now()

        console.print(
            Panel(
                f"📅 Date: {now.strftime('%d-%m-%Y')}\n"
                f"⏰ Time: {now.strftime('%H:%M:%S')}",
                title="🧠 ARTERY SYSTEM REPORT",
                border_style="cyan",
            )
        )

        # ================= SYSTEM =================

        system_table = Table(box=box.ROUNDED)

        system_table.add_column("Component", style="cyan")
        system_table.add_column("Value", style="magenta")

        system_table.add_row("🖥 OS", f"{platform.system()} {platform.release()}")
        system_table.add_row("🏷 Machine", platform.node())
        system_table.add_row("⚙ Architecture", platform.machine())

        console.print(Panel(system_table, title="💻 SYSTEM INFORMATION"))

        # ================= CPU =================

        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_cores = psutil.cpu_count(logical=False)
        cpu_threads = psutil.cpu_count()

        cpu_text = (
            f"🧮 Cores: {cpu_cores}\n"
            f"🧵 Threads: {cpu_threads}\n"
            f"📊 Usage: {cpu_percent}%"
        )

        try:
            temps = psutil.sensors_temperatures()
            if temps:
                for name, entries in temps.items():
                    cpu_text += f"\n🌡 Temperature: {entries[0].current} °C"
                    break
        except:
            cpu_text += "\n🌡 Temperature: Not available"

        console.print(Panel(cpu_text, title="🧮 CPU STATUS", border_style="green"))

        # ================= GPU =================

        gpu_text = ""

        if GPUtil:
            gpus = GPUtil.getGPUs()

            if gpus:
                for gpu in gpus:
                    gpu_text += (
                        f"🎮 Name: {gpu.name}\n"
                        f"📊 Load: {gpu.load*100:.0f}%\n"
                        f"🌡 Temp: {gpu.temperature} °C\n"
                        f"💾 VRAM: {gpu.memoryUsed}MB / {gpu.memoryTotal}MB\n\n"
                    )
            else:
                gpu_text = "❌ No GPU detected"
        else:
            gpu_text = "⚠ GPU library not installed"

        console.print(Panel(gpu_text, title="🎮 GPU STATUS", border_style="yellow"))

        # ================= RAM =================

        mem = psutil.virtual_memory()

        ram_text = (
            f"🧠 Total RAM: {round(mem.total / (1024**3), 2)} GB\n"
            f"📦 Used RAM: {round(mem.used / (1024**3), 2)} GB\n"
            f"📊 Usage: {mem.percent}%"
        )

        console.print(Panel(ram_text, title="🧠 MEMORY", border_style="blue"))

        # ================= DISK =================

        disk_table = Table(box=box.SIMPLE)

        disk_table.add_column("💽 Drive")
        disk_table.add_column("📦 Total")
        disk_table.add_column("📂 Used")
        disk_table.add_column("📊 Usage")

        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)

                disk_table.add_row(
                    partition.device,
                    f"{round(usage.total / (1024**3),2)} GB",
                    f"{round(usage.used / (1024**3),2)} GB",
                    f"{usage.percent}%",
                )
            except:
                pass

        console.print(Panel(disk_table, title="💽 DISK PARTITIONS"))

        # ================= NETWORK =================

        internet = self.check_internet()

        network_text = ""

        if internet:
            network_text += "🌐 Internet: Connected ✅\n"
        else:
            network_text += "🌐 Internet: Not Connected ❌\n"

        if ping:
            latency = ping("google.com")
            if latency:
                network_text += f"⚡ Latency: {round(latency*1000)} ms\n"

        firewall = self.check_firewall()
        network_text += f"🛡 Firewall: {firewall}"

        console.print(Panel(network_text, title="🌐 NETWORK"))

        # ================= PROCESSES =================

        process_table = Table(box=box.SIMPLE)

        process_table.add_column("⚙ Process")
        process_table.add_column("🔥 CPU %")
        process_table.add_column("🧠 RAM %")

        processes = []

        for proc in psutil.process_iter(["name", "cpu_percent", "memory_percent"]):
            try:
                processes.append(proc.info)
            except:
                pass

        processes = sorted(processes, key=lambda x: x["cpu_percent"], reverse=True)

        for p in processes[:5]:
            process_table.add_row(
                str(p["name"]),
                str(p["cpu_percent"]),
                f"{p['memory_percent']:.2f}",
            )

        console.print(Panel(process_table, title="⚙ TOP PROCESSES"))

        # ================= BATTERY =================

        battery = psutil.sensors_battery()

        if battery:
            battery_text = (
                f"🔋 Battery Level: {battery.percent}%\n"
                f"⚡ Charging: {battery.power_plugged}"
            )
        else:
            battery_text = "🔋 Battery not detected"

        console.print(Panel(battery_text, title="🔋 BATTERY"))

        # ================= HEALTH =================

        issues = []

        if cpu_percent > 85:
            issues.append("High CPU usage")

        if mem.percent > 90:
            issues.append("High RAM usage")

        if not internet:
            issues.append("No internet connection")

        if firewall == "Disabled":
            issues.append("Firewall disabled")

        if issues:

            issue_text = "\n".join([f"⚠ {i}" for i in issues])

            console.print(
                Panel(issue_text, title="⚠ SYSTEM WARNINGS", border_style="red")
            )

        else:

            console.print(
                Panel(
                    "🟢 System healthy\n✅ No issues detected",
                    title="SYSTEM HEALTH",
                    border_style="green",
                )
            )

            self.speak("System report is ready")
            self.speak("No issues found. System is healthy")

        console.print("\n[bold green]🤖 Artery is ready to assist you[/bold green]\n")

        self.speak("Artery is ready to assist you")
import os
import subprocess
import webbrowser
import pyautogui
import time
import sys
import ctypes
import psutil
#whatsapp import
try:
    import pyperclip
except ImportError:
    print("pyperclip module not found - WhatsApp message sending may not work. Install with 'pip install pyperclip'")

                                                                                
# YouTubeTask import
try:
    from modules.app_control.youtube_task import YouTubeTask
    YOUTUBE_AVAILABLE = True
except ImportError:
    YOUTUBE_AVAILABLE = False
    print("YouTubeTask not found - modules/app_control/youtube_task.py banao")

class SystemControl:
    def __init__(self):
        print("[SystemControl] Ready")
        self.awaiting_close_all_confirmation = False
        self.awaiting_power_confirmation = None
        #whatsapp control ready
        print("[SystemControl] WhatsApp Control Ready")
    
        # YouTubeTask instance
        self.youtube = YouTubeTask() if YOUTUBE_AVAILABLE else None

        self.process_map = {
            "chrome": "chrome.exe",
            "edge": "msedge.exe",
            "vscode": "Code.exe",
            "vs code": "Code.exe",
            "notepad": "notepad.exe",
            "calculator": "Calculator.exe",
            "excel": "EXCEL.EXE",
            "word": "WINWORD.EXE",
            "powerpoint": "POWERPNT.EXE",
            "whatsapp": "WhatsApp.exe",
            "explorer": "explorer.exe"
        }

        self.self_process = os.path.basename(sys.argv[0]).lower()

    # ================= MAIN HANDLER =================
    def handle(self, cmd: str):
        cmd = cmd.lower().strip()

        # ---------- POWER CONFIRM ----------
        if self.awaiting_power_confirmation:
            if cmd in ["yes", "haan", "confirm", "ok"]:
                action = self.awaiting_power_confirmation
                self.awaiting_power_confirmation = None
                return action()
            if cmd in ["no", "cancel", "nahi", "stop"]:
                self.awaiting_power_confirmation = None
                return "Action cancel Confirm boss."
            return "Boss only Say Yes ya No."

        # ---------- CLOSE ALL CONFIRM ----------
        if self.awaiting_close_all_confirmation:
            if cmd in ["yes", "haan", "confirm", "ok"]:
                self.awaiting_close_all_confirmation = False
                return self.close_all_apps()
            if cmd in ["no", "cancel", "nahi", "stop"]:
                self.awaiting_close_all_confirmation = False
                return "Close all cancel kar diya boss."
            return "Boss sirf Yes ya No bolo."

        # ---------- YOUTUBE CONTROL (Connected to YouTubeTask) ----------
        if cmd == "play song":
            return "Boss kaunsa song play karu?"

        if cmd.startswith("play ") and self.youtube:
            song = cmd.replace("play ", "").strip()
            return self.youtube.execute("play", song)

        if cmd in ["next", "youtube next"] and self.youtube:
            return self.youtube.execute("next")

        if cmd in ["previous", "youtube previous"] and self.youtube:
            return self.youtube.execute("previous")

        if cmd in ["fullscreen", "youtube fullscreen"] and self.youtube:
            return self.youtube.execute("fullscreen")

        if cmd in ["captions", "youtube captions"] and self.youtube:
            return self.youtube.execute("captions")

        if "close youtube" in cmd and self.youtube:
            self.youtube.stop()
            return "YouTube CLosed Done boss."
        #------------------whatsapp control------------------
        if cmd.startswith("send whatsapp message to "):
            try:
                parts = cmd.replace("send whatsapp message to ", "").split(" saying ")
                contact = parts[0].strip()
                message = parts[1].strip()
                return self.send_whatsapp_message(contact, message)
            except Exception as e:
                return "Command format galat hai boss. Use: send whatsapp message to [contact] saying [message]"

        # ---------- OPEN APPS ----------
        if "open chrome" in cmd:
            return self.open_chrome()

        if "open edge" in cmd:
            return self.open_edge()

        if "open vscode" in cmd or "open vs code" in cmd:
            return self.open_vscode()

        if "open notepad" in cmd:
            subprocess.Popen(["notepad.exe"])
            return "Notepad open kar diya boss."

        if "open calculator" in cmd:
            subprocess.Popen(["calc.exe"])
            return "Calculator open kar diya boss."

        if "open excel" in cmd:
            return self.open_office("excel")

        if "open word" in cmd:
            return self.open_office("word")

        if "open powerpoint" in cmd:
            return self.open_office("powerpoint")

        if "open whatsapp" in cmd:
            return self.open_whatsapp()

        if "open file explorer" in cmd or "open explorer" in cmd:
            subprocess.Popen("explorer")
            return "File Explorer open kar diya boss."

        if "open settings" in cmd:
            subprocess.Popen(["start", "ms-settings:"], shell=True)
            return "Settings open kar diya boss."

        if "open wifi" in cmd:
            subprocess.Popen(["start", "ms-settings:network-wifi"], shell=True)
            return "WiFi settings open kar diya boss."

        if "open bluetooth" in cmd:
            subprocess.Popen(["start", "ms-settings:bluetooth"], shell=True)
            return "Bluetooth settings open kar diya boss."

        if "open youtube" in cmd:
            webbrowser.open("https://www.youtube.com")
            return "YouTube open kar diya boss."

        # ---------- CLOSE ----------
        if cmd.startswith("close "):
            app = cmd.replace("close", "").strip()
            return self.close_app(app)

        if "close all apps" in cmd:
            self.awaiting_close_all_confirmation = True
            return "Boss confirm karo sab band kar du? (Yes/No)"

        # ---------- VOLUME ----------
        if "volume up" in cmd:
            for _ in range(5):
                pyautogui.press("volumeup")
            return "Volume increase boss."

        if "volume down" in cmd:
            for _ in range(5):
                pyautogui.press("volumedown")
            return "Volume down boss."

        if "mute" in cmd:
            pyautogui.press("volumemute")
            return "Mute kar diya boss."

        # ---------- BRIGHTNESS ----------
        if "brightness up" in cmd:
            pyautogui.press("brightnessup")
            return "Brightness badha di boss."

        if "brightness down" in cmd:
            pyautogui.press("brightnessdown")
            return "Brightness kam kar di boss."

        # ---------- POWER ----------
        if "shutdown" in cmd:
            self.awaiting_power_confirmation = self.shutdown_system
            return "Boss confirm karo shutdown karu? (Yes/No)"

        if "restart" in cmd:
            self.awaiting_power_confirmation = self.restart_system
            return "Boss confirm karo restart karu? (Yes/No)"

        if "sleep" in cmd:
            self.awaiting_power_confirmation = self.sleep_system
            return "Boss confirm karo sleep mode me dalu? (Yes/No)"

        if "lock" in cmd:
            ctypes.windll.user32.LockWorkStation()
            return "System lock kar diya boss."

        # ---------- FILE ----------
        if cmd.startswith("create file"):
            name = cmd.replace("create file", "").strip()
            open(name, "w").close()
            return f"{name} file bana di boss."

        if cmd.startswith("create folder"):
            name = cmd.replace("create folder", "").strip()
            os.makedirs(name, exist_ok=True)
            return f"{name} folder bana diya boss."

        if "battery" in cmd:
            return self.battery_status()

        return None

    # ================= HELPERS (ALL SAME) =================
    def close_app(self, app_name):
        exe = self.process_map.get(app_name)
        if exe:
            subprocess.run(
                ["taskkill", "/f", "/t", "/im", exe],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return f"{app_name} close, boss."
        return "App, not, found, boss."

    def close_all_apps(self):
        for exe in self.process_map.values():
            subprocess.run(
                ["taskkill", "/f", "/t", "/im", exe],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        return "All, appliication, Close, Boss."

    def open_chrome(self):
        paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ]
        for p in paths:
            if os.path.exists(p):
                subprocess.Popen([p])
                return "Chrome open kar diya boss."
        webbrowser.open("https://google.com")
        return "Chrome web me open kiya boss."

    def open_edge(self):
        subprocess.Popen(["start", "msedge"], shell=True)
        return "Edge open, boss."

    def open_vscode(self):
        paths = [
            r"C:\Users\shiva\AppData\Local\Programs\Microsoft VS Code\Code.exe",
            r"C:\Program Files\Microsoft VS Code\Code.exe"
        ]
        for p in paths:
            if os.path.exists(p):
                subprocess.Popen([p])
                return "VS Code, Opening, boss."
        return "VS Code, Not found, boss."

    def open_whatsapp(self):
        try:
            subprocess.Popen([
                "explorer.exe",
                "shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App"
            ])
            return "WhatsApp open, boss."
        except Exception:
            webbrowser.open("https://web.whatsapp.com")
            return "WhatsApp Web, open, boss."

    def open_office(self, app):
        office_paths = {
            "excel": [
                r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
                r"C:\Program Files (x86)\Microsoft Office\root\Office16\EXCEL.EXE"
            ],
            "word": [
                r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
                r"C:\Program Files (x86)\Microsoft Office\root\Office16\WINWORD.EXE"
            ],
            "powerpoint": [
                r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
                r"C:\Program Files (x86)\Microsoft Office\root\Office16\POWERPNT.EXE"
            ]
        }
        for p in office_paths.get(app, []):
            if os.path.exists(p):
                subprocess.Popen([p])
                return f"{app} open kar diya boss."
        return f"{app} nahi mila boss."

    def shutdown_system(self):
        os.system("shutdown /s /t 1")
        return "System shutdown ho raha hai boss."

    def restart_system(self):
        os.system("shutdown /r /t 1")
        return "System restart ho raha hai boss."

    def sleep_system(self):
        subprocess.run("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return "System sleep mode me ja raha hai boss."

    def battery_status(self):
        b = psutil.sensors_battery()
        if b:
            return f"Battery {b.percent}% hai boss."
        return "Battery info nahi mil rahi boss."

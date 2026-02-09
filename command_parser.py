# Artery Command Parser
# Converts text commands into structured tasks

class CommandParser:
    def __init__(self):
        print("[CommandParser] Ready")

    def parse(self, text):
        text = text.lower()

        if "open" in text:
            return {
                "task": "open_app",
                "params": text
            }

        elif "shutdown" in text:
            return {
                "task": "shutdown_system",
                "params": None
            }

        elif "learn" in text or "search" in text:
            return {
                "task": "learn_online",
                "params": text.replace("learn", "").replace("search", "").strip()
            }

        else:
            return {
                "task": "unknown",
                "params": text
            }
       
import datetime
import random


class BasicConversation:

    def __init__(self):
        self.small_talk = {
            "how are you": [
                "Main bilkul stable hu boss.",
                "System optimal chal raha hai.",
                "All services running smooth."
            ],
            "who are you": [
                "I am Artery — Your system assistant.",
                "Artery AI — command ready."
            ],
            "what's up": [
                "Just processing your commands, boss.",
                "All systems go, boss."
        ],
        "tell me a joke": [
                "Why did the computer show up at work late? It had a hard drive!",
                "Why do programmers prefer dark mode? Because light attracts bugs!"
            ],
            "what's your name": [
                "I am Artery, your system assistant.",
                "Artery AI at your service."
            ],
            "how's the weather": [
                "I can't check the weather right now, but I hope it's nice outside!",
                "Weather info is not available, but I hope it's sunny!"
            ],
            "do you like music": [
                "yes boss, I love music!.",
                "Music is great for boosting productivity, boss."
            ]
        }

    def handle(self, text: str):
        text = text.lower().strip()

        # Greeting
        if any(greet in text for greet in ["hi", "hello", "hey"]):
            return "Hello boss."
    
        

        # Thanks
        if "thank" in text:
            return "Always ready boss."

        # Bye
        if any(word in text for word in ["bye", "good night"]):
            return "Shutdown nahi ho raha hu 😄, bas standby me hu boss."

        # Time
        if "time" in text:
            now = datetime.datetime.now().strftime("%I:%M %p")
            return f"Abhi time {now} hai boss."

        # Date
        if "date" in text:
            today = datetime.date.today().strftime("%d %B %Y")
            return f"Aaj ki date {today} hai boss."

        # Small talk dictionary
        for key in self.small_talk:
            if key in text:
                return random.choice(self.small_talk[key])

        return None
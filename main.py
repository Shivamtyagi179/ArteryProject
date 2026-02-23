from core.task_engine import TaskEngine
from speech.speaker import Speaker
from core.command_parser import CommandParser
from core.voice_listener import VoiceListener
import threading
import time


def voice_loop(engine, speaker):
    listener = VoiceListener()
    while True:
        text = listener.listen()
        if not text:
            continue
        reply = engine.execute_command(text)
        if reply:
            speaker.speak(reply)
        time.sleep(0.3)

def main():
    print("Artery starting... Har Har Mahadev")

    speaker = Speaker()
    engine = TaskEngine()

    speaker.speak("Hello Boss, I am Artery, I am listening.")

    threading.Thread(
        target=voice_loop,
        args=(engine, speaker),
        daemon=True
    ).start()

    while True:
        user_input = input("🧠 You: ").strip()
        if user_input in ["exit", "quit"]:
            speaker.speak("Shutting down. Har Har Mahadev.")
            
            break

        reply = engine.execute_command(user_input)
        if reply:
            speaker.speak(reply)



if __name__ == "__main__":
    main()

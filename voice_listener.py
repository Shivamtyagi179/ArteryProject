import speech_recognition as sr

class VoiceListener:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        print("[VoiceListener] Ready")

    def listen(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("[VoiceListener] Listening... speak now")
            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio)
            print(f"[VoiceListener] You said: {text}")
            return text.lower()

        except sr.UnknownValueError:
            print("[VoiceListener] Could not understand audio")
            return ""

        except sr.RequestError:
            print("[VoiceListener] Speech service error")
            return ""

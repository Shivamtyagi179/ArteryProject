import tempfile
import os
import winsound
from .tts_engine import TTSEngine


class Speaker:
    def __init__(self):
        self.tts = TTSEngine()
        self.is_speaking = False

    def speak(self, text: str):
        if not text or self.is_speaking:
            return

        self.is_speaking = True
        temp_path = None

        try:
            audio_bytes = self.tts.synthesize(text)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                f.write(audio_bytes)
                temp_path = f.name

            # 🔊 Windows native playback (BLOCKING, SAFE)
            winsound.PlaySound(temp_path, winsound.SND_FILENAME)

        except Exception as e:
            print("[Speaker Error]", e)

        finally:
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except PermissionError:
                    pass

            self.is_speaking = False

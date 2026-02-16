from google.cloud import texttospeech


class TTSEngine:
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()

        # ✅ Hindi Neural2 Female (most natural)
        self.voice = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    name="en-US-Neural2-F",
    ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
)


        # ✅ Neutral audio config (let model breathe)
        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16,
            speaking_rate=0.92,   # natural slow
            pitch=1.0,            # IMPORTANT
            volume_gain_db=1.5,
        )

    def synthesize(self, text: str) -> bytes:
        # ❌ No prosody, no tricks
        # ✅ Plain text = max realism
        response = self.client.synthesize_speech(
            input=texttospeech.SynthesisInput(text=text),
            voice=self.voice,
            audio_config=self.audio_config,
        )

        return response.audio_content

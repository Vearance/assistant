import subprocess
import sounddevice as sd  # For audio playback
import numpy as np
import logging

logger = logging.getLogger("TTS")

class PiperTTS:
    def __init__(self):
        self.piper_path = r"piper/piper.exe"
        self.model_path = r"voices/en_US-kristin-medium.onnx"
        # self.piper_path = str(Path(__file__).parent / "piper" / "piper.exe")
        # self.model_path = str(Path(__file__).parent / "voices" / "en_US-kristin-medium.onnx")
        self.sample_rate = 22050  # Piper's default sample rate

    def speak(self, text):
        try:
            # Run Piper and capture raw audio
            cmd = [
                self.piper_path,
                "--model", self.model_path,
                "--output-raw"
            ]
            
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Send text to Piper and get audio
            audio_data, _ = process.communicate(input=text.encode("utf-8"))
            audio_array = np.frombuffer(audio_data, dtype=np.int16)

            # Play audio
            sd.play(audio_array, samplerate=self.sample_rate, device=3)
            sd.wait()

            logger.info(f"Spoke: {text}")
            
        except Exception as e:
            logger.error(f"TTS failed: {str(e)}")
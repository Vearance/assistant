import vosk
import time
import sounddevice as sd
import queue
import logging

logger = logging.getLogger("STT")

class AudioDeviceError(Exception):
    pass

class SpeechRecognizer:
    def __init__(self, model_path="vosk-model-small-en-us-0.15"):  # updated to match available model folder
        self.model = vosk.Model(model_path)
        self.sample_rate = 16000
        # self.device = self._get_input_device()
        self.device = 1  # FORCE DEVICE 1
        self.audio_queue = queue.Queue()
        
    # def _get_input_device(self):
    #     devices = sd.query_devices()
    #     for i, dev in enumerate(devices):
    #         if dev['max_input_channels'] > 0:
    #             logger.info(f"Selected input device {i}: {dev['name']}")
    #             return i
    #     raise AudioDeviceError("No valid input devices found")

    def _audio_callback(self, indata, frames, time, status):
        if status:
            logger.warning(f"Audio input error: {status}")
        self.audio_queue.put(bytes(indata))

    def listen(self, timeout=5):
        with sd.RawInputStream(
            samplerate=self.sample_rate,
            blocksize=8000,
            device=self.device,
            dtype='int16',
            channels=1,
            callback=self._audio_callback
        ):
            recognizer = vosk.KaldiRecognizer(self.model, self.sample_rate)
            start_time = time.time()
            
            while True:
                try:
                    data = self.audio_queue.get(timeout=1)
                    if recognizer.AcceptWaveform(data):
                        return eval(recognizer.Result())["text"].strip().lower()
                        
                    if time.time() - start_time > timeout:
                        return ""
                        
                except queue.Empty:
                    if time.time() - start_time > timeout:
                        return ""
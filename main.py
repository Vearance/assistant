import time
import logging
from stt import SpeechRecognizer
from tts import PiperTTS

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class MINA:
    def __init__(self):
        self.stt = SpeechRecognizer()
        self.tts = PiperTTS()
        self.wake_word = "mina"
        self.running = True
        
    def _detect_wake_word(self, text):
        return self.wake_word in text.replace(" ", "")

    def _handle_command(self, command):
        if not command:
            return
            
        if "time" in command:
            self.tts.speak(f"Current time is {time.strftime('%H:%M')}")
        elif "hello" in command:
            self.tts.speak("Good day sir, how may I assist?")
        else:
            self.tts.speak("Command not recognized")

    def run(self):
        self.tts.speak("System initialized")
        
        try:
            while self.running:
                # Wake word phase
                self.tts.speak("Waiting for wake word")
                wake_text = self.stt.listen(timeout=10)
                
                if self._detect_wake_word(wake_text):
                    # Command phase
                    self.tts.speak("Listening for command")
                    command = self.stt.listen(timeout=7)
                    self._handle_command(command)
                    
        except KeyboardInterrupt:
            self.tts.speak("Shutting down")
            
        except Exception as e:
            logging.error(f"Critical failure: {str(e)}")
            self.tts.speak("Emergency shutdown activated")

if __name__ == "__main__":
    ai = MINA()
    ai.run()
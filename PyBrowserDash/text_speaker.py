from threading import Thread
from queue import Queue
import pyttsx3


class TextSpeaker:
    """Text to speech implementation."""

    def __init__(self):
        self._q = Queue()
        self._thread = Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        """Speak messages from queue out loud."""
        engine = pyttsx3.init()
        while True:
            engine.say(self._q.get())
            engine.runAndWait()

    def speak(self, text):
        """Enqueue a text message to speak."""
        self._q.put(text)

    def is_speaking(self):
        """Return if speach is playing."""
        return self._engine.isBusy()

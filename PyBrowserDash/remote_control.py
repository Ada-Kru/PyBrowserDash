from threading import Thread
from queue import Queue
from serial import Serial

try:
    from PyBrowserDash.local_config import COM_PORT, COM_BAUD
except ImportError:
    from PyBrowserDash.config import COM_PORT, COM_BAUD


class RemoteControl:
    """Text to speech implementation."""

    def __init__(self):
        self._q = Queue()
        self._thread = Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        """Send strings from queue on serial port."""
        while True:
            command = self._q.get()

            with Serial(COM_PORT, COM_BAUD) as ser:
                ser.open()
                ser.write(command)
                ser.close()

    def send_cmd(self, command, emitters):
        """Create a command string to and add to send queue."""
        command_type = "T"
        emitter_1 = int(0 in emitters)
        emitter_2 = int(1 in emitters)
        self._q.put(f"{command_type}_{emitter_1}_{emitter_2}_{command}")

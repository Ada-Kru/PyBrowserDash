from threading import Thread
from queue import Queue
from serial import Serial, SerialException
from time import sleep

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
            try:
                with Serial(COM_PORT, COM_BAUD, timeout=2) as ser:
                    while True:
                        command = self._q.get() + "\n"
                        ser.write(command.encode())
            except SerialException as e:
                print(f"Error sending to {COM_PORT}: {e}")
                sleep(10)

    def send_cmd(self, command, emitters):
        """Create a command string to and add to send queue."""
        # command_type = "T"
        emitter_1 = int(0 in emitters)
        emitter_2 = int(1 in emitters)
        self._q.put(f"{emitter_1}_{emitter_2}_{command}")

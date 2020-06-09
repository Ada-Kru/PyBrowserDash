from psutil import net_io_counters, cpu_percent, virtual_memory as virtmem
from asyncio import sleep


class SystemMonitor:
    """Retreive system status (CPU usage, RAM, Network usage, etc.)."""

    def __init__(self, bg_tasks):
        self._bg_tasks = bg_tasks
        self._total_memory = int(round((virtmem().total) / 1073741824, 1))
        self._prev_bytes_recv = 0
        self._prev_k_bytes_recv = 0
        self._prev_cpu = 0
        self._prev_ram = 0

    def get_computer_status(self):
        """Get computer status info."""
        info_changed = False

        cpu = int(cpu_percent())
        if cpu != self._prev_cpu:
            info_changed = True
        self._prev_cpu = cpu

        vm = virtmem()
        ram = round((vm.total - vm.available) / 1073741824, 1)
        if ram != self._prev_ram:
            info_changed = True
        self._prev_ram = ram

        bytes_recv = net_io_counters().bytes_recv
        k_bytes = int(round((bytes_recv - self._prev_bytes_recv) / 1024, -1))
        self._prev_bytes_recv = bytes_recv
        if k_bytes != self._prev_k_bytes_recv:
            info_changed = True
        self._prev_k_bytes_recv = k_bytes

        return info_changed

    def make_status_text(self):
        """Generate formatted system status text."""
        return {
            "cpu": self._prev_cpu,
            "ram_used": self._prev_ram,
            "ram_total": self._total_memory,
            "net": self._prev_k_bytes_recv,
        }
        # return (
        #     f"CPU: {self._prev_cpu: >2}% RAM: {self._prev_ram: >2}G  ▬▬  "
        #     f"NET: {self._prev_k_bytes_recv:5d}K"
        # )

    async def run(self):
        """Send system status to clients every second."""
        while True:
            if self.get_computer_status():
                msg = {"sys": self.make_status_text()}
                self._bg_tasks.send_all_websockets(msg)
            await sleep(1)

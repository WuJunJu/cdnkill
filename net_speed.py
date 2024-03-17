import time
import psutil

class NetworkSpeedMonitor:
    def __init__(self, interval=2):
        self.interval = interval
        self.last_io_counters = psutil.net_io_counters(pernic=True)

    def calculate_speed(self):
        while True:
            time.sleep(self.interval)
            new_io_counters = psutil.net_io_counters(pernic=True)

            diff_rx = sum(new_io_counters[n].bytes_recv - self.last_io_counters[n].bytes_recv 
                          for n in new_io_counters if n in self.last_io_counters)
            diff_tx = sum(new_io_counters[n].bytes_sent - self.last_io_counters[n].bytes_sent 
                          for n in new_io_counters if n in self.last_io_counters)

            speed_rx = diff_rx / self.interval / 1024**2  # 转换为MB/s
            speed_tx = diff_tx / self.interval / 1024**2

            print(f"Network Speed: RX: {speed_rx:.2f} MB/s | TX: {speed_tx:.2f} MB/s")

            self.last_io_counters.update(new_io_counters)

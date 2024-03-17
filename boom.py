# -*- coding: utf-8 -*-
import asyncio
import aiohttp
import sys
import os
from threading import Thread

from net_speed import NetworkSpeedMonitor

def restart_program():
    """Restarts the current program, with file objects and descriptors cleanup."""
    python = sys.executable
    os.execl(python, python, *sys.argv)

async def download_file(url):
    try:
        async with aiohttp.ClientSession() as session:
            while True:
                async with session.get(url) as response:
                    # 这里我们并没有保存文件，只是读取了内容
                    await asyncio.sleep(0)  # 稍微延时以控制请求频率
    except Exception as e:
        print(f"An error occurred: {e}")
        restart_program()

async def main():
    url = 'https://carimg.lxybaike.com/upload/202203/1648466749.jpg'  # 替换为你的文件URL
    tasks = [download_file(url) for _ in range(250)]  # 同时发起250个下载任务（按需调整）

    # 创建并启动网络速度监控器
    network_speed_monitor = NetworkSpeedMonitor(interval=2)
    monitor_thread = Thread(target=network_speed_monitor.calculate_speed)
    monitor_thread.start()

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Critical error occurred: {e}. Restarting the program.")
        restart_program()
import asyncio
from bleak import BleakClient, BleakScanner

DEVICE_NAME = "Aurora"
CHARACTERISTIC_UUID_TX = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"
#  核心接口函数
# 作用：接收一个「处理消息的函数」，收到蓝牙消息就调用它
# --------------------------
async def connect_ble(handler):
    # 1. 搜索ESP32
    devices = await BleakScanner.discover()
    addr = None
    for d in devices:
        if d.name and DEVICE_NAME in d.name:
            addr = d.address
            break
    if addr is None:
       print(f"错误：没找到名字包含'{DEVICE_NAME}'的设备！")
       return
    # 2. 连接蓝牙
    async with BleakClient(addr) as client:
        print("蓝牙连接成功！")
        # 3. 收到消息 → 调用传入的函数
        def callback(sender, data):
            msg = data.decode().strip()
            handler(msg)  # 把消息传给主文件
        
        await client.start_notify(CHARACTERISTIC_UUID_TX, callback)
        while True: await asyncio.sleep(1)
# 启动函数
def start(handler):
    asyncio.run(connect_ble(handler))
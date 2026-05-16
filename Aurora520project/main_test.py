# 主文件（测试使用BLE脚本）
# 第一步：导入封装好的蓝牙模块
from BLE import start

# --------------------- 第二步：写你自己的消息处理函数 ---------------------
# 这个函数就是传给蓝牙模块的「接口参数」
# 作用：收到蓝牙消息时，自动调用这里
def handler(msg):
    print(f"\n主文件收到消息：{msg}")
    target = "RELAX:"
    # 2. 判断消息是否以目标前缀开头
    if msg.startswith(target):
        # 3. 提取前缀后面的内容
        value= msg[len(target):]
        print(f"收到 relax指数：{value}")
# --------------------- 第三步：调用蓝牙接口 ---------------------
if __name__ == "__main__":
    print("=== 主程序启动 ===")
    print("正在启动蓝牙监听...")  
    # 调用接口：把你的处理函数传给 start
    start(handler)
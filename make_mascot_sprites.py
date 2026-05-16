"""
吉祥物游戏精灵图 - 去绿底 + 透明背景 + 形变动效
"""
from PIL import Image
import numpy as np

src_path = (
    r"C:\Users\yyz\.kimi\sessions\23ffeb3ab1309266679e50bc65e4abd9"
    r"\15c2d476-914d-4cc1-a291-c181db813d2e\uploads\5fba4d99db2395f9aea38433b047a157_14ed49.jpg"
)
src = Image.open(src_path).convert("RGBA")

# 1. 去绿底 → 透明
data = np.array(src)
r, g, b = data[:, :, 0], data[:, :, 1], data[:, :, 2]

# 背景是纯绿色 [0, 134, 0]，允许一定容差
green_mask = (r < 50) & (g > 100) & (g < 180) & (b < 50)
data[green_mask] = [0, 0, 0, 0]

# 清理边缘残留（浅色绿边）
edge_mask = (r < 100) & (g > 80) & (b < 100)
data[edge_mask] = [0, 0, 0, 0]

# Alpha修正
has_color = (data[:, :, 0] > 10) | (data[:, :, 1] > 10) | (data[:, :, 2] > 10)
data[:, :, 3] = np.where(has_color, 255, 0)

img = Image.fromarray(data)

# 2. 裁剪到核心主体（去掉左右小球和波形线）
img = img.crop((50, 0, 430, 370))
bbox = img.getbbox()
img = img.crop(bbox)

TARGET_W, TARGET_H = 44, 47

def make_frame(base_img, scale_x, scale_y, offset_y=0):
    ratio = min(TARGET_W / base_img.width, TARGET_H / base_img.height) * 0.92
    bw = int(base_img.width * ratio)
    bh = int(base_img.height * ratio)
    base = base_img.resize((bw, bh), Image.LANCZOS)
    
    w = int(base.width * scale_x)
    h = int(base.height * scale_y)
    deformed = base.resize((w, h), Image.LANCZOS)
    
    canvas = Image.new("RGBA", (TARGET_W, TARGET_H), (0, 0, 0, 0))
    x = (TARGET_W - w) // 2
    y = (TARGET_H - h) // 2 + offset_y
    canvas.paste(deformed, (x, y), deformed)
    return canvas

# 三帧动画
frame1 = make_frame(img, 1.0, 1.0, offset_y=2)
frame2 = make_frame(img, 1.08, 0.88, offset_y=5)
frame3 = make_frame(img, 0.92, 1.08, offset_y=0)

frame1.save("images/mascot-run-1.png")
frame2.save("images/mascot-run-2.png")
frame3.save("images/mascot-run-3.png")

# 死亡帧（变灰）
dead = frame1.copy()
data = np.array(dead)
gray = data[:, :, :3].mean(axis=2).astype(np.uint8)
data[:, :, 0] = gray
data[:, :, 1] = gray
data[:, :, 2] = gray
dead = Image.fromarray(data)
dead.save("images/mascot-dead.png")

print("Done! Green background removed, transparent sprites generated.")

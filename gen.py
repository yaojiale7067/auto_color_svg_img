import time
import random

ts = time.time()
local_time = time.localtime(ts)
time_str = time.strftime("%Y-%m-%d_%H-%M-%S", local_time)
rng = random.Random(ts)

GRID_SIZE = 32
CELL_PX = 1

# 工具：0xRRGGBB → (r,g,b)
def hex2rgb(v: int):
    r = (v >> 16) & 0xFF
    g = (v >> 8) & 0xFF
    b = v & 0xFF
    return (r, g, b)

# 工具：(r,g,b) → #RRGGBB
def rgb2hex(r,g,b):
    return f"#{r:02X}{g:02X}{b:02X}"

# 工具：两个rgb之间插值
def lerp(a, b, t):
    return int(a + (b - a) * t)

# 【重点：只生成2个主题色，整张图的基调】
base1 = rng.randint(0, 0xFFFFFF)
base2 = rng.randint(0, 0xFFFFFF)
r1,g1,b1 = hex2rgb(base1)
r2,g2,b2 = hex2rgb(base2)

rects = []
color_list = []

for y in range(GRID_SIZE):
    for x in range(GRID_SIZE):
        # 根据坐标得到插值系数
        t = (x + y) / (GRID_SIZE * 2)
        # 基础插值
        rr = lerp(r1, r2, t)
        gg = lerp(g1, g2, t)
        bb = lerp(b1, b2, t)
        # 微小扰动，防止过于死板（幅度很小，不会跑偏色系）
        noise = 12
        rr = max(0, min(255, rr + rng.randint(-noise, noise)))
        gg = max(0, min(255, gg + rng.randint(-noise, noise)))
        bb = max(0, min(255, bb + rng.randint(-noise, noise)))

        c = rgb2hex(rr, gg, bb)
        color_list.append(c)
        x0 = x * CELL_PX
        y0 = y * CELL_PX
        rects.append(f'<rect x="{x0}" y="{y0}" width="{CELL_PX}" height="{CELL_PX}" fill="{c}"/>')

svg_width = GRID_SIZE * CELL_PX
svg_height = GRID_SIZE * CELL_PX

svg_content = f'''<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">
{"".join(rects)}
</svg>'''

svg_path = "color.svg"
log_path = "color.log"

with open(svg_path, "w", encoding="utf-8") as f:
    f.write(svg_content)

log_content = f"""timestamp: {ts}
time: {time_str}
grid: {GRID_SIZE}x{GRID_SIZE}
theme_color_1: 0x{base1:06X} {rgb2hex(r1,g1,b1)}
theme_color_2: 0x{base2:06X} {rgb2hex(r2,g2,b2)}
colors (row-major):
"""
for i in range(len(color_list)):
    log_content += color_list[i] + " "
    if (i+1) % GRID_SIZE == 0:
        log_content += "\n"

with open(log_path, "w", encoding="utf-8") as f:
    f.write(log_content)

print("Generated theme svg OK")
print(f"Base1: 0x{base1:06X}, Base2:0x{base2:06X}")

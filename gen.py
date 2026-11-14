import time
import random
import os

OUT_DIR = "out"
os.makedirs(OUT_DIR, exist_ok=True)

ts = time.time()
local_time = time.localtime(ts)
time_str = time.strftime("%Y-%m-%d_%H-%M-%S", local_time)
rng = random.Random(ts)

GRID_SIZE = 32
CELL_PX = 1  # 严格32×32像素

def rand_color() -> str:
    v = rng.randint(0, 0xFFFFFF)
    return f"#{v:06X}"

rects = []
color_list = []
for y in range(GRID_SIZE):
    for x in range(GRID_SIZE):
        c = rand_color()
        color_list.append(c)
        x0 = x * CELL_PX
        y0 = y * CELL_PX
        rects.append(f'<rect x="{x0}" y="{y0}" width="{CELL_PX}" height="{CELL_PX}" fill="{c}"/>')

svg_width = GRID_SIZE * CELL_PX
svg_height = GRID_SIZE * CELL_PX

svg = f'''<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">
{"".join(rects)}
</svg>'''

svg_path = os.path.join(OUT_DIR, f"grid32_{time_str}.svg")
with open(svg_path, "w", encoding="utf-8") as f:
    f.write(svg)

log_path = os.path.join(OUT_DIR, f"grid32_{time_str}.log")
log_content = f"""timestamp: {ts}
time: {time_str}
grid: {GRID_SIZE}x{GRID_SIZE}
cell_px: {CELL_PX}
colors (row-major, x from 0, y from 0):
"""
for i in range(len(color_list)):
    log_content += color_list[i] + " "
    if (i+1) % GRID_SIZE == 0:
        log_content += "\n"

with open(log_path, "w", encoding="utf-8") as f:
    f.write(log_content)

print(f"✅ 生成：{svg_path}")
print(f"✅ 日志：{log_path}")

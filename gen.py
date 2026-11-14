import time
import random
import colorsys

ts = time.time()
local_time = time.localtime(ts)
time_str = time.strftime("%Y-%m-%d_%H-%M-%S", local_time)
rng = random.Random(ts)

GRID_SIZE = 32
CELL_PX = 1

# 主色：时间种子生成唯一色相 H，固定饱和度
base_h = rng.random()
base_s = rng.uniform(0.55, 0.85)
base_l = rng.uniform(0.4, 0.65)

# hsl(0~1,0~1,0~1) -> #RRGGBB
def hsl2hex(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return f"#{int(r*255):02X}{int(g*255):02X}{int(b*255):02X}"

# 主色（基准主题色）
main_color_hex = hsl2hex(base_h, base_s, base_l)
# 转0xRRGGBB格式给你UIK用
mr = int(main_color_hex[1:3],16)
mg = int(main_color_hex[3:5],16)
mb = int(main_color_hex[5:7],16)
main_color_uik = (mr << 16) | (mg << 8) | mb

rects = []
color_list = []

for y in range(GRID_SIZE):
    for x in range(GRID_SIZE):
        # 只在【同一个色相】附近小幅扰动，不换色调！
        h = base_h + rng.uniform(-0.025, 0.025)
        h = h % 1.0
        # 亮度大范围变化（亮/暗），形成层次
        l = rng.uniform(0.22, 0.82)
        # 饱和度轻微浮动
        s = base_s + rng.uniform(-0.12, 0.12)
        s = max(0.15, min(0.92, s))

        c = hsl2hex(h, s, l)
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
main_theme_color: 0x{main_color_uik:06X} {main_color_hex}
base_hsl: h={base_h:.4f}, s={base_s:.4f}, l={base_l:.4f}
colors (row-major):
"""
for i in range(len(color_list)):
    log_content += color_list[i] + " "
    if (i+1) % GRID_SIZE == 0:
        log_content += "\n"

with open(log_path, "w", encoding="utf-8") as f:
    f.write(log_content)

print(f"✅ Theme color: 0x{main_color_uik:06X} {main_color_hex}")

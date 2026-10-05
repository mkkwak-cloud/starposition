# 홈 화면 아이콘(out/icon-192.png, icon-512.png)을 만든다: 어두운 밤하늘 + 노란 별.
import math, os
from PIL import Image, ImageDraw
O = os.path.join(os.path.dirname(__file__), '..', 'out')

def make(n):
    k = 4  # 선을 부드럽게 하려고 크게 그린 뒤 줄인다
    im = Image.new('RGB', (n * k, n * k), '#050a18')
    d = ImageDraw.Draw(im)
    c, R, r = n * k / 2, n * k * 0.30, n * k * 0.12
    pts = [(c + (R if i % 2 == 0 else r) * math.sin(i * math.pi / 5), c - (R if i % 2 == 0 else r) * math.cos(i * math.pi / 5)) for i in range(10)]
    d.polygon(pts, fill='#ffe07a')
    for fx, fy, fr in ((0.22, 0.2, 0.018), (0.8, 0.28, 0.014), (0.7, 0.8, 0.02), (0.18, 0.74, 0.012)):
        d.ellipse([n * k * fx - n * k * fr, n * k * fy - n * k * fr, n * k * fx + n * k * fr, n * k * fy + n * k * fr], fill='#bcd2ff')
    im.resize((n, n), Image.LANCZOS).save(os.path.join(O, 'icon-%d.png' % n))

for n in (192, 512):
    make(n)
print('ok')

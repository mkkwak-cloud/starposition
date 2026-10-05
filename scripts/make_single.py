# out/index.html 과 같이 쓰는 두 파일(별 자료·계산 도구)을 안에 넣어 파일 하나(out/star-single.html)로 만든다.
import os, re
O = os.path.join(os.path.dirname(__file__), '..', 'out')
rd = lambda f: open(os.path.join(O, f), encoding='utf8').read()
html = rd('index.html')
for name in ('skydata.js', 'astronomy.browser.min.js'):
    js = rd(name)
    assert '</script' not in js.lower()
    tag = '<script src="%s"></script>' % name
    assert tag in html
    html = html.replace(tag, '<script>' + js + '</script>')
open(os.path.join(O, 'star-single.html'), 'w', encoding='utf8').write(html)
print(len(html) // 1024, 'KB')

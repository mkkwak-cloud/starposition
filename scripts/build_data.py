# data/ 의 공개 별 자료를 앱이 읽기 쉬운 작은 파일(out/skydata.js)로 묶는다.
import json, os
D = os.path.join(os.path.dirname(__file__), '..', 'data')
O = os.path.join(os.path.dirname(__file__), '..', 'out')
ld = lambda f: json.load(open(os.path.join(D, f), encoding='utf8'))

KO = {'Sirius':'시리우스','Canopus':'카노푸스','Arcturus':'아르크투루스','Vega':'직녀성(베가)','Altair':'견우성(알타이르)',
      'Deneb':'데네브','Capella':'카펠라','Rigel':'리겔','Betelgeuse':'베텔게우스','Procyon':'프로키온','Polaris':'북극성',
      'Antares':'안타레스','Spica':'스피카','Aldebaran':'알데바란','Regulus':'레굴루스','Pollux':'폴룩스','Castor':'카스토르',
      'Fomalhaut':'포말하우트','Achernar':'아케르나르','Hadar':'하다르','Acrux':'아크룩스','Mimosa':'미모사','Bellatrix':'벨라트릭스'}

sn = ld('starnames.json')
cons_raw = {f['id']: f['properties'] for f in ld('constellations.json')['features']}
stars, named, bycon = [], [], {}
for f in ld('stars.6.json')['features']:
    ra, dec = f['geometry']['coordinates']
    mag = f['properties']['mag']
    try: bv = float(f['properties']['bv'])
    except: bv = 0.6
    i = len(stars)
    e = sn.get(str(f['id']), {})
    cid = e.get('c') or ''
    bayer = e.get('bayer') or ''
    en = e.get('name') or ''
    ko = KO.get(en) or e.get('ko') or ''
    nm = ko or en
    stars.append([round(ra % 360, 3), round(dec, 3), mag, round(bv, 2), cid, bayer if mag < 4.6 else ''])
    if nm:
        named.append([i, nm, en])
    if cid in cons_raw and (nm or bayer) and mag < 4.6:
        lab = nm or (bayer + ' ' + cons_raw[cid]['gen'])
        bycon.setdefault(cid, []).append([lab, mag])

lines = {f['id']: f['geometry']['coordinates'] for f in ld('constellations.lines.json')['features']}
cons = []
for f in ld('constellations.json')['features']:
    p = f['properties']; c = f['geometry']['coordinates']
    cid = f['id']
    ls = [[[round(a % 360, 3), round(b, 3)] for a, b in seg] for seg in lines.get(cid, [])]
    if not ls: continue
    cons.append({'id': cid, 'ko': p['ko'], 'en': p['en'], 'ra': c[0] % 360, 'dec': c[1], 'lines': ls,
                 'top': sorted(bycon.get(cid, []), key=lambda x: x[1])[:4]})

with open(os.path.join(O, 'skydata.js'), 'w', encoding='utf8') as w:
    w.write('const SKY=' + json.dumps({'stars': stars, 'named': named, 'cons': cons}, ensure_ascii=False, separators=(',', ':')) + ';')
print(len(stars), 'stars,', len(named), 'named,', len(cons), 'constellations')

# -*- coding: utf-8 -*-
import json, re, pathlib, concurrent.futures as cf
from ow import get, getbin
d=json.load(open('cats.json')); pathlib.Path('gal').mkdir(exist_ok=True)
pick={'khustky': range(0,30), 'podarunkovi-nabory': list(range(0,43))+[48], 'tvilli': range(0,39), 'masky-dlia-snu': range(0,15), 'sertyfikaty': range(0,5), 'aksesuary-dlia-snu': range(0,8)}
todo=[(c,i) for c,r in pick.items() for i in r if i < len(d[c])]
def page(ci):
    c,i=ci; it=d[c][i]
    try:
        s=get('https://obiimy.world'+it['href'])
        med=re.findall(r"(/content/images/\d+/)(\d+x600l80mc0)/([a-z0-9-]+\.jpg)", s)
        seen=[]; 
        for a,sz,f in med:
            if f not in [x[2] for x in seen]: seen.append((a,sz,f))
        it['gal']=[dict(med=a+sz+'/'+f, full=a+'1500x1500l80mc0/'+f) for a,sz,f in seen]
        m=re.search(r'itemprop="price"[^>]*content="([\d.]+)"', s); it['p']=m.group(1) if m else ''
    except Exception as e: it['gal']=[]; print('ERR', c, i, e)
    return ci
with cf.ThreadPoolExecutor(5) as ex: list(ex.map(page, todo))
jobs=[]
for c,i in todo:
    for n,g in enumerate(d[c][i].get('gal',[])):
        out=f'gal/{c}-{i:03d}-{n}.jpg'; g['file']=out
        if not pathlib.Path(out).exists() or pathlib.Path(out).stat().st_size<3000: jobs.append(('https://obiimy.world'+g['med'], out))
print('pages', len(todo), 'images', len(jobs))
with cf.ThreadPoolExecutor(6) as ex: list(ex.map(lambda j: getbin(*j), jobs))
json.dump(d, open('cats.json','w'), ensure_ascii=False, indent=0)
print('done', len(list(pathlib.Path('gal').glob('*.jpg'))))

# -*- coding: utf-8 -*-
import json, re, pathlib, concurrent.futures as cf
from ow import getbin
d=json.load(open('cats.json')); DST=pathlib.Path('/Users/ivan/obiimy/photo/site')
pick={'khustky':{27:[1,2],24:[1],12:[1,2,3,4],15:[1,2,3,4],7:[1,2,3],8:[1,2],16:[1,2],19:[1,2,3],20:[1],28:[0,2],4:[1],1:[1,2,4],21:[1,2,3],13:[1],22:[1,3],14:[1]},
      'tvilli':{8:[1,2,3],15:[1,2,3],22:[1,2,3],25:[1,2,4,5],17:[1,3],28:[1,2],16:[2]},
      'podarunkovi-nabory':{36:[0,1],22:[0,1],20:[0],37:[0],48:[0],11:[0],17:[0],18:[0,1],23:[0],9:[1],26:[2],28:[2],40:[2],42:[1],5:[7,8]},
      'sertyfikaty':{0:[0]}}
jobs=[]; idx=[]
for c,pp in pick.items():
    for i,ns in pp.items():
        it=d[c][i]; slug=it['href'].strip('/')
        slug=re.sub(r'^shovkova-khustka-','khustka-',slug); slug=re.sub(r'^khustka-tvilli-shovkova-|^khustka-tvilli-','tvilli-',slug); slug=re.sub(r'^podarunkovyi-nabir-|^podarunkovyi-|^nabir-','set-',slug)
        for n in ns:
            if n>=len(it.get('gal',[])): print('no', c,i,n); continue
            out=DST/f"{slug[:44]}-{n+1:02d}.jpg"; idx.append(dict(cat=c,i=i,n=n,name=it['name'],price=it.get('p',''),href=it['href'],file='photo/site/'+out.name))
            if not out.exists(): jobs.append(('https://obiimy.world'+it['gal'][n]['full'], str(out)))
print('jobs', len(jobs))
with cf.ThreadPoolExecutor(6) as ex: sizes=list(ex.map(lambda j: getbin(*j), jobs))
print('bytes', sum(sizes))
json.dump(idx, open('picked.json','w'), ensure_ascii=False, indent=1)
for x in idx: print(x['file'].split('/')[-1], '|', x['name'][:50], x['price'])

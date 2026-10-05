# -*- coding: utf-8 -*-
import re, json, html, sys
from ow import get
cats=sys.argv[1:] or ['podarunkovi-nabory','khustky','tvilli','rezynky','masky-dlia-snu','prykrasy','aksesuary-dlia-snu','sertyfikaty']
allp={}
for c in cats:
    s=get(f'https://obiimy.world/{c}/filter/page=all/')
    blocks=s.split('catalogCard-box j-product-container')[1:]
    items=[]
    for b in blocks:
        h=re.search(r"<a href='([^']+)'\s+class=\"catalogCard-image", b); n=re.search(r'aria-label="([^"]*)"', b); i=re.search(r"class='catalogCard-img'[^>]*src='([^']+)'", b) or re.search(r"<img[^>]*src='([^']+)'", b)
        p=re.search(r'catalogCard-price[^>]*>\s*([^<]+)<', b)
        if h and i: items.append(dict(href=h.group(1), name=html.unescape(n.group(1)) if n else '', img=i.group(1), price=re.sub(r'\s+',' ',html.unescape(p.group(1))).strip() if p else ''))
    print(c, len(s), len(items))
    allp[c]=items
json.dump(allp, open('cats.json','w'), ensure_ascii=False, indent=0)

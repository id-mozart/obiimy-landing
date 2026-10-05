# -*- coding: utf-8 -*-
import re, subprocess, pathlib
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
CK={'challenge_passed': open('hash.txt').read().strip()}
def raw(url, t=90):
    ck='; '.join(f'{k}={v}' for k,v in CK.items())
    return subprocess.run(['curl','-s','-L','--max-time',str(t),'-A',UA,'-b',ck,url],capture_output=True).stdout
def _chal(b):
    if len(b)>5000: return False
    s=b.decode('utf-8','ignore'); m=re.search(r'defaultHash = "([0-9a-f]{64})"', s); n=re.search(r'document\.cookie = "([a-z_]+)="', s)
    if m and n: CK[n.group(1)]=m.group(1); return True
    return False
def get(url):
    for _ in range(4):
        b=raw(url)
        if _chal(b): continue
        return b.decode('utf-8','ignore')
    return b.decode('utf-8','ignore')
def getbin(url, out):
    for _ in range(4):
        b=raw(url)
        if b[:1]==b'<' or b[:9].strip().startswith(b'<'):
            if _chal(b): continue
        pathlib.Path(out).write_bytes(b); return len(b)
    return 0

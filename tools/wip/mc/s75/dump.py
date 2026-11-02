import sys,os,json,re
sys.path.insert(0,'tools/re')
import fncmp
from fncmp import *
addr=next(a for a,s in SYMBOLS.items() if s=='_mode_client')
size=dict(f for _,fs in units(Image('xeBuild.exe')) for f in fs)[addr]
d=json.load(open('build/xeBuild.lines.json'))
for l,a in zip(d['lines'],d['addr']):
    if a is not None and addr<=a<addr+size: print('%x %s'%(a,l.strip()))

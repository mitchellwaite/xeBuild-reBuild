import sys,re
sys.path.insert(0,'tools/wip/dehint')
import iwlib
t=open('build/iw/a21/na.c',newline='').read().replace('\r\n','\n')
# FS table before the spare loop, keeping its guard
m=re.search(r"\tif \(next != 0xf1f1\) \{\n.*?\n\t\}\n\timgEnd = off \+ len;",t,re.S)
fs=m.group(0)[:-len('\timgEnd = off + len;')]
t2=t.replace(fs,'')
t2=t2.replace('#define BLK (start + b)\n',fs+'#define BLK (start + b)\n')
assert t2!=t
print('fsfirst',iwlib.fmt(iwlib.score_text(t2,[]))[:200])

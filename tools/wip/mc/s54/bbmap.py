"""bbmap.py <bbro_mc.txt>: bb -> called symbols / LC refs (RTL before STC)."""
import re,sys
def bbmap(path):
    t=open(path).read(); t=t[:t.find('STC - round 1')] if 0 else t
    m={}; cur=None
    for line in t.split('\n'):
        mm=re.match(r'\(note \d+ \d+ \d+ (\d+) \[bb \d+\] NOTE_INSN_BASIC_BLOCK',line)
        if mm: cur=int(mm.group(1)); m.setdefault(cur,[]); continue
        for s in re.findall(r'symbol_ref[^"]*"([^"]+)"',line):
            if cur is not None and s not in m[cur]: m[cur].append(s)
    return m
if __name__=='__main__':
    m=bbmap(sys.argv[1])
    for b in sorted(m):
        if len(sys.argv)<3 or b>=int(sys.argv[2]): print(b,' '.join(m[b]))

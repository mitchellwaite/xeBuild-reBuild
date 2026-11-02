"""fq.py SLOTDIR DETAILS_COMPGOTOS: freq + pred edges (prob, edge freq) of mapped case-group blocks."""
import sys,os,re
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','s18')); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))
import analyze
sp,_=analyze.spmap(sys.argv[1])[1],0
d=open(sys.argv[2]).read(); B={}
for m in re.finditer(r';; basic block (\d+), loop depth \d+, count \d+, freq (\d+).*?\n;;  prev.*?\n;;  pred:(.*?)\n;; bb',d,re.S):
    B[int(m.group(1))]=(int(m.group(2)),re.findall(r'(\d+|ENTRY) \[([\d.]+)%\]',m.group(3)))
inv={}
for b,s in sp.items(): inv.setdefault(s,b)
IDS=[int(x) for x in sys.argv[3].split(',')] if len(sys.argv)>3 else [129,109,107,113,110,119,108,120,121,128,116,132,115,112,103,117,130,114,94,49,131,118]
for s in IDS:
    b=inv.get(s)
    if b is None or b not in B: print(s,'?'); continue
    f,pr=B[b]
    print(s,'bb%d'%b,'freq',f,' '.join('%s:%.0f'%(p,(B[int(p)][0] if p!='ENTRY' else 0)*float(q)/100) for p,q in pr))

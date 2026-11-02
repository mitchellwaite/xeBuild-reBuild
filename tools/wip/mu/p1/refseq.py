"""refseq.py [O2]: block-order string sequence of _mode_update in build/obj/mode_update.o; with O2 side-by-side diff."""
import sys,os,re,subprocess,difflib
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import ev
def seq(o):
    rd=ev.rdata(o)
    out=[]
    t=subprocess.run([ev.tool('objdump'),'-dr','-M','intel','--no-show-raw-insn',o],env=ev.ENV,capture_output=True,text=True).stdout
    t=t[t.index('<_mode_update>:'):]
    last=None
    for l in t.split('\n'):
        m=re.match(r'\s+([0-9a-f]+):\s+(\S.*)$',l)
        if m and 'dir32' not in l: last=m.group(2)
        if re.search(r'dir32\s+\.rdata',l):
            mm=re.search(r',0x([0-9a-f]+)\s*$',last) or re.search(r'0x([0-9a-f]+)',last)
            off=int(mm.group(1),16) if mm else 0
            e=rd.find(b'\0',off)
            out.append(rd[off:min(e,off+36)].decode('latin1').replace('\n',' '))
    return out
a=seq(ev.REFO)
if len(sys.argv)>1:
    b=seq(sys.argv[1])
    for l in difflib.unified_diff(a,b,'ref','mine',lineterm='',n=0): print(l)
else:
    print('\n'.join(a))

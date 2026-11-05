"""python tools/wip/dehint/irfeat.py <gen_irN.py> [substring ...]: per variant of a generator, loose lines for getImageSmc and which of its remaining differences are right:
A prologue tail (`mov esi,ecx` ... `add esi,eax`), B `mov edi,ebx` right after `lea eax,[ebx-0x800]`, C `mov edi,0x1000; mov ebx,edi`, O block order (ok forwarder before the zero log's `mov [esp+8],0`), L ok block aligned."""
import importlib.util, itertools, os, re, sys
from concurrent.futures import ThreadPoolExecutor
os.environ['IRLOOSE'] = '1'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import irlib

s = importlib.util.spec_from_file_location('gen', sys.argv[1])
m = importlib.util.module_from_spec(s)
s.loader.exec_module(m)
subs = sys.argv[2:]
base = open(os.path.join(irlib.R, getattr(m, 'BASE', 'src/image_read.c')), newline='').read().replace('\r\n', '\n')
combos = [c for c in itertools.product(*m.AXES) if all(x in '+'.join(y[0] for y in c) for x in subs)]


def one(c):
    t = base
    lab = '+'.join(x[0] for x in c if x[0])
    for l, ed in c:
        for x, y in ed:
            t = t.replace(x, y)
    ok, o, d = irlib.compile_src(t, [])
    if not ok:
        irlib.cleanup(d)
        return lab, None, ''
    idn, tot, per, notes = irlib.report(o)
    fns, _ = irlib.disasm(o)
    irlib.cleanup(d)
    ls = [x.split(': ', 1)[1] for x in fns['_getImageSmc']]
    J = '\n'.join(re.sub(r'\s+', ' ', x) for x in ls)
    f = ''
    f += 'A' if 'mov esi,ecx\nand esi,0xff00\nadd esi,eax' in J else '-'
    f += 'B' if 'lea eax,[ebx-0x800]\nmov edi,ebx' in J else '-'
    f += 'C' if 'mov edi,0x1000\nmov ebx,edi' in J else '-'
    zi, oi = J.find('mov DWORD PTR [esp+0x8],0x0\njmp'), J.find('mov ebx,edi\njmp')
    f += 'O' if 0 <= oi < zi else '-'
    k = J.find('cmp ebx,eax\njae')
    tail = J[k:k + 80]
    f += 'L' if re.search(r'jae [0-9a-f]*\n(mov esi,esi|xchg|lea|nop)', tail) else '-'
    return lab, per.get('_getImageSmc', 0), f


with ThreadPoolExecutor(4) as ex:
    res = list(ex.map(one, combos))
res.sort(key=lambda r: (r[1] is None, r[1] or 0))
for lab, k, f in res:
    print(k, f, lab)

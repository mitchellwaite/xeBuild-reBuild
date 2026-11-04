"""python tools/wip/dehint/iw19irasweep.py <gen_iwN.py> [-t threads]: a generator's states scored by finalizeImage's IRA data as well as lines: (l5 MEM cost of the pseudo holding xb.hdr, of xb.spare in the ECD loop, reference counts). Prints any state where the two costs differ, then the best lines. Base from IWB or the generator's BASE."""
import collections, importlib.util, itertools, os, re, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib
a = sys.argv[1:]; th = 2
if '-t' in a:
    i = a.index('-t'); th = int(a[i + 1]); del a[i:i + 2]
sp = importlib.util.spec_from_file_location('g', a[0]); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
base = os.environ.get('IWB', m.BASE)
text = open(os.path.join(iwlib.R, base), newline='').read().replace('\r\n', '\n')
def costs(ira):
    b = re.search(r'^;; Function finalizeImage \(.*?(?=^;; Function |\Z)', ira, re.S | re.M)
    if not b: return None
    b = b.group(0)
    out = {}
    for name, off in (('spare', 48), ('hdr', 56)):
        best = None
        for p in set(re.findall(r'\(set \(reg[^ ]*:SI (\d+)[^)]*\)\s*\(mem/f/c:SI \(const:SI \(plus:SI \(symbol_ref:SI \("xb"\)[^\n]*\n\s*\(const_int %d ' % off, b)):
            c = re.findall(r'a\d+\(r%s,l5\) costs: GENERAL_REGS:\S+ MEM:(\d+),(\d+)' % p, b)
            l0 = re.findall(r'a\d+\(r%s,l0\) costs: GENERAL_REGS:\S+ MEM:(\d+),(\d+)' % p, b)
            if c:
                best = (p, c[-1][1], l0[-1][1] if l0 else '-')
        out[name] = best
    # which loads first in the preheader: the insn stream's first set of each pseudo
    if out.get('hdr') and out.get('spare'):
        def pos(p):
            m = re.search(r'\(set \(reg[^ ]*:SI %s [^\n]*\n\s*\(mem/f/c:SI' % p, b)
            return m.start() if m else -1
        out['first'] = 'spare' if pos(out['spare'][0]) < pos(out['hdr'][0]) else 'hdr'
    return out
def one(c):
    lab = '+'.join(x[0] for x in c if x[0]); t = text
    for l, ed in c:
        for x, y in ed:
            if x not in t: return lab, None, None, t
            t = t.replace(x, y)
    import tempfile, glob
    d = tempfile.mkdtemp(dir=iwlib.BUILD, prefix='ir')
    ok, o, d = iwlib.compile_src(t, [], workdir=d, extra=['-fdump-rtl-ira-all'])
    if not ok:
        iwlib.cleanup(d); return lab, None, None, t
    idn, tot, per, notes = iwlib.report(o)
    f = glob.glob(os.path.join(d, '*.ira'))
    cs = costs(open(f[0], errors='replace').read()) if f else None
    iwlib.cleanup(d)
    return lab, tot, cs, t
combos = list(itertools.product(*m.AXES))
print(len(combos), 'states', flush=True)
res = [r for r in ThreadPoolExecutor(th).map(one, combos) if r[1] is not None]
res.sort(key=lambda r: r[1])
for lab, tot, cs, t in res:
    if cs and cs.get('hdr') and cs.get('spare') and (cs['hdr'][1] != cs['spare'][1] or cs['hdr'][2] != cs['spare'][2]):
        print('COST', tot, lab, cs)
for lab, tot, cs, t in res:
    if cs and cs.get('first') == 'spare' and cs.get('hdr') and cs.get('spare') and int(cs['hdr'][2].replace('-', '0')) > int(cs['spare'][2].replace('-', '0')):
        print('WANT', tot, lab, cs)
        open(os.path.join(iwlib.BUILD, 'a19', 'want_%s.c' % lab[:50]), 'w', newline='\n').write(t)
for lab, tot, cs, t in res[:6]:
    print(tot, lab, cs)

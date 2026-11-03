"""For a generator's outputs (already swept by casweep.py): sendAvatarData lines and prepSysex lines.

python tools/wip/dehint/caboth.py <gen.py>   lists variants sorted by (prepSysex lines, sendAvatarData lines)
"""
import concurrent.futures as cf, importlib.util, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
FNCMP = os.path.join(ROOT, 'tools', 're', 'fncmp.py')
gen = sys.argv[1]
name = os.path.splitext(os.path.basename(gen))[0]
s = importlib.util.spec_from_file_location(name, gen)
m = importlib.util.module_from_spec(s)
s.loader.exec_module(m)


def n(path, fn):
    r = subprocess.run([sys.executable, FNCMP, path, fn, '-O3', '-I', os.path.join(ROOT, 'src')], capture_output=True, text=True, cwd=ROOT)
    o = r.stdout.strip()
    return 0 if o == 'MATCH' else len([l for l in o.split('\n') if re.match(r'^[-+][^-+]', l)]) or 999


def one(it):
    i, tag = it
    p = os.path.join(ROOT, 'build', 'ca', name, 'v%d.c' % i)
    return n(p, 'prepSysex'), n(p, 'sendAvatarData'), n(p, 'addTitleId'), tag, 'v%d' % i


seen, items = set(), []
for v in m.variants():
    if v[1] not in seen:
        seen.add(v[1])
        items.append((len(items), v[0]))
with cf.ThreadPoolExecutor(4) as ex:
    res = sorted(ex.map(one, items), key=lambda r: r[:2])
for r in res[:int(sys.argv[2]) if len(sys.argv) > 2 else 40]:
    print(*r)

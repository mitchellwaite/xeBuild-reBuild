"""python tools/wip/dehint/nstab.py <file.c | gen.py> ...: one line per source: lines, r, aligns, MEM(buf), B(buf test block freq), U(netSendData block freq), traces.

Env NS_N="50 60 70": also sweep --param builtin-expect-probability (diagnostics, sources using __builtin_expect only).
A gen.py is run through its variants() and written to build/ns/<gen>/ like nssweep.
"""
import concurrent.futures as cf, importlib.util, os, re, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BIN = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin')
FNCMP = os.path.join(ROOT, 'tools', 're', 'fncmp.py')
BASE = open(os.path.join(ROOT, 'src', 'net.c')).read()
START = BASE.index('int netSendFile(')
END = BASE.index('int netFormatSysex(')


def fnsec(t):
    t = t[t.index(';; Function netSendFile ('):]
    j = t.find('\n;; Function ', 10)
    return t[:j] if j > 0 else t


def one(a):
    tag, src, flags = a
    src = os.path.abspath(src)
    os.makedirs(os.path.join(ROOT, 'build', 'ns', 'probe'), exist_ok=True)
    d = tempfile.mkdtemp(dir=os.path.join(ROOT, 'build', 'ns', 'probe'))
    env = dict(os.environ, PATH=BIN + os.pathsep + os.environ['PATH'])
    r = subprocess.run([os.path.join(BIN, 'gcc.exe'), '-S', '-masm=intel', '-fno-asynchronous-unwind-tables', '-O3',
                        '-I', os.path.join(ROOT, 'src'), '-fdump-rtl-ira', '-fdump-rtl-bbro-details'] + flags + [src, '-o', 'a.s'],
                       cwd=d, env=env, capture_output=True, text=True)
    if r.returncode:
        shutil.rmtree(d)
        return (10 ** 6, tag + ' FAIL ' + r.stderr[-300:])
    s = open(os.path.join(d, 'a.s')).read()
    i = s.find('_netSendFile:')
    t = s[i:]
    t = t[:t.find('.def', 10)]
    al = len([l for l in t.split('\n') if l.strip().startswith('.p2align')])
    open(os.path.join(d, 'b.s'), 'w', newline='\n').write(re.sub(r'_netRecvVerbose\.constprop\.\d+', '_netRecv', s))
    r = subprocess.run([sys.executable, FNCMP, src, 'netSendFile'], capture_output=True, text=True, cwd=ROOT,
                       env=dict(os.environ, FNCMP_ASM=os.path.join(d, 'b.s')))
    o = (r.stdout + r.stderr).strip()
    n = 0 if o == 'MATCH' else len([l for l in o.split('\n') if re.match(r'^[-+][^-+]', l)])
    ira = fnsec(open(os.path.join(d, next(x for x in os.listdir(d) if x.endswith('r.ira')))).read())
    bb = fnsec(open(os.path.join(d, next(x for x in os.listdir(d) if x.endswith('r.bbro')))).read())
    mem = ''
    m = re.search(r'\(set \(reg/v/f:SI (\d+) \[ buf \]\)', ira)
    if m:
        c = re.search(r'a\d+\(r%s,l0\) costs:.*?MEM:(-?\d+)' % m.group(1), ira)
        mem = c.group(1) if c else '?'
    else:
        mem = 'nopseudo'
    tr = ' '.join(re.sub(r'Trace \d+ \(round (\d)\):\s*', r'R\1:', l).replace(' [', '[') for l in bb.split('\n') if l.startswith('Trace '))
    shutil.rmtree(d)
    return (n, '%d al=%d mem=%s %s\n    %s' % (n, al, mem, tag, tr))


def main():
    items = []
    Ns = os.environ.get('NS_N', '').split()
    for a in sys.argv[1:]:
        if a.endswith('.py'):
            name = os.path.splitext(os.path.basename(a))[0]
            spec = importlib.util.spec_from_file_location(name, a)
            m = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(m)
            out = os.path.join(ROOT, 'build', 'ns', name)
            os.makedirs(out, exist_ok=True)
            for k, v in enumerate(m.variants()):
                text = BASE[:START] + v[1].strip('\n') + '\n\n' + BASE[END:]
                for old, new in (v[2] if len(v) > 2 else ()):
                    assert old in text, old
                    text = text.replace(old, new)
                p = os.path.join(out, 'v%d.c' % k)
                open(p, 'w', newline='\n').write(text)
                if Ns:
                    for N in Ns:
                        items.append(('%s v%d N=%s' % (v[0], k, N), p, ['--param', 'builtin-expect-probability=' + N]))
                else:
                    items.append(('%s v%d' % (v[0], k), p, []))
        elif Ns:
            for N in Ns:
                items.append(('%s N=%s' % (a, N), a, ['--param', 'builtin-expect-probability=' + N]))
        else:
            items.append((a, a, []))
    with cf.ThreadPoolExecutor(os.cpu_count() or 4) as ex:
        res = list(ex.map(one, items))
    if os.environ.get('NS_SORT'):
        res.sort(key=lambda r: r[0])
    for r in res[:int(os.environ.get('NS_TOP', '1000'))]:
        print(r[1])


if __name__ == '__main__':
    main()

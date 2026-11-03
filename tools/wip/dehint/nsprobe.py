"""python tools/wip/dehint/nsprobe.py <src.c> [gcc flags]: netSendFile line count and alignment, plus bb freqs and traces.

DIAGNOSTIC: flags allowed (e.g. --param), the result isn't a MATCH just because this prints 0.
Clone renamed as wbsweep does.  NS_SHOW=1 prints the diff; NS_TRACE=1 the trace lines; NS_OUT=dir keeps the .s there.
"""
import os, re, subprocess, sys, tempfile, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BIN = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin')
FNCMP = os.path.join(ROOT, 'tools', 're', 'fncmp.py')


def probe(src, flags, show=False, trace=False):
    src = os.path.abspath(src)
    os.makedirs(os.path.join(ROOT, 'build', 'ns', 'probe'), exist_ok=True)
    d = tempfile.mkdtemp(dir=os.path.join(ROOT, 'build', 'ns', 'probe'))
    env = dict(os.environ, PATH=BIN + os.pathsep + os.environ['PATH'])
    r = subprocess.run([os.path.join(BIN, 'gcc.exe'), '-S', '-masm=intel', '-fno-asynchronous-unwind-tables', '-O3',
                        '-I', os.path.join(ROOT, 'src'), '-fdump-rtl-bbro-details'] + flags + [src, '-o', 'a.s'],
                       cwd=d, env=env, capture_output=True, text=True)
    if r.returncode:
        shutil.rmtree(d)
        return 'FAIL ' + r.stderr[:300]
    s = open(os.path.join(d, 'a.s')).read()
    i = s.find('_netSendFile:')
    t = s[i:]
    t = t[:t.find('.def', 10)]
    al = [l.strip() for l in t.split('\n') if l.strip().startswith('.p2align')]
    s2 = re.sub(r'_netRecvVerbose\.constprop\.\d+', '_netRecv', s)
    open(os.path.join(d, 'b.s'), 'w', newline='\n').write(s2)
    r = subprocess.run([sys.executable, FNCMP, src, 'netSendFile'], capture_output=True, text=True, cwd=ROOT,
                       env=dict(os.environ, FNCMP_ASM=os.path.join(d, 'b.s'), FNCMP_CONTEXT='1'))
    o = (r.stdout + r.stderr).strip()
    n = 0 if o == 'MATCH' else len([l for l in o.split('\n') if re.match(r'^[-+][^-+]', l)])
    out = ['lines=%d aligns=%d' % (n, len(al))]
    if show and n:
        out.append(o)
    if trace:
        f = next(x for x in os.listdir(d) if x.endswith('r.bbro'))
        b = open(os.path.join(d, f)).read()
        b = b[b.index(';; Function netSendFile ('):]
        j = b.find('\n;; Function ', 10)
        b = b[:j] if j > 0 else b
        out += [l for l in b.split('\n') if re.match(r'(Trace \d|Connection|Final order|\d+ \d+ )', l)]
    shutil.rmtree(d)
    return '\n'.join(out)


if __name__ == '__main__':
    print(probe(sys.argv[1], sys.argv[2:], bool(os.environ.get('NS_SHOW')), bool(os.environ.get('NS_TRACE'))))

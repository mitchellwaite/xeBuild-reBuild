"""Dump a console_hdd draft and print sendAvatarData's block chain at each pass, RTL included (block numbers only).

python tools/wip/dehint/cachains.py <file.c> [pass...]   dumps go to build/ca/a4/<basename>/
"""
import glob, os, re, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BIN = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin')
env = dict(os.environ, PATH=BIN + os.pathsep + os.environ['PATH'])
TAGS = [('Sending avatar', 'GUARD'), ('sending %03d', 'BODY'), ('sending manifest to', 'MF'), ('failed to send %s\\n", _', 'LOOPFAIL'),
        ('failed to send %s\\n", manifest.e', 'LOOPFAIL'), ('failed to send %s\\n", e', 'LOOPFAIL'), ('failed to send %s\\n", &manifest.path', 'MFFAIL'),
        ('successfully sent', 'OK'), ('netUnmount', 'OUT'), ('createSysexDirs', 'CREATE')]


def main():
    src = sys.argv[1]
    d = os.path.join(ROOT, 'build', 'ca', 'a4', os.path.splitext(os.path.basename(src))[0])
    os.makedirs(d, exist_ok=True)
    for f in glob.glob(os.path.join(d, 'a.*')):
        os.remove(f)
    shutil.copy(src, os.path.join(d, 'a.c'))
    r = subprocess.run([os.path.join(BIN, 'gcc.exe'), '-c', '-O3', '-I', os.path.join(ROOT, 'src'), '-fno-asynchronous-unwind-tables',
                        '-fdump-tree-all-details-blocks', '-fdump-rtl-ce1-details', '-fdump-rtl-expand', 'a.c'], cwd=d, env=env, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[:500])
        return
    for p in sys.argv[2:] or ['vrp1', 'ch2', 'dom2', 'crited1', 'pre', 'ivopts', 'dom3', 'vrp2', 'optimized']:
        fs = glob.glob(os.path.join(d, '*.' + p))
        if not fs:
            print(p, 'missing')
            continue
        t = open(fs[0], errors='replace').read()
        m = re.search(r'^;; Function sendAvatarData \(', t, re.M)
        if not m:
            print(p, 'no function')
            continue
        t = t[m.start():t.find('\n;; Function ', m.end())]
        t = t[t.rfind('\nsendAvatarData ('):]
        parts = re.split(r'^;;   basic block (\d+), loop depth (\d+), count \d+, freq (\d+)', t, flags=re.M)
        out = []
        for j in range(1, len(parts), 4):
            b, ld, f, body = parts[j:j + 4]
            tag = next((n for s, n in TAGS if s in body), '')
            cond = re.search(r'^\s*if \((.*?)\)', body, re.M)
            out.append((b, ld, f, tag, cond.group(1) if cond else ''))
        start = next((k for k, x in enumerate(out) if x[3] == 'GUARD'), 0)
        print(p, ' '.join('%s%s[%s]%s' % (x[0], ':' + x[3] if x[3] else '', x[2], '{' + x[4].replace(' ', '') + '}' if x[4] else '') for x in out[start:]))
    fs = glob.glob(os.path.join(d, '*.ce1'))
    if fs:
        t = open(fs[0], errors='replace').read()
        m = re.search(r'^;; Function sendAvatarData \(', t, re.M)
        t = t[m.start():t.find('\n;; Function ', m.end())]
        for l in re.findall(r'^.*(?:IF-CASE|IF-THEN|Conversion).*$', t, re.M)[:12]:
            print(l)


main()

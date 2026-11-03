"""Frequencies of the prepSysex blocks where inlined in sendAvatarData, for a list of files.

python tools/wip/dehint/cafreq.py <file.c>...   prints format-fail, mount-fail, create, loop-fail, MF, guard frequencies (target 50 10 40 29 10 39 at p=80).
"""
import concurrent.futures as cf, os, re, subprocess, sys, tempfile, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BIN = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin')
env = dict(os.environ, PATH=BIN + os.pathsep + os.environ['PATH'])
TAGS = [('fmt', 'format sysex'), ('mnt', 'mount sysex'), ('create', 'createSysexDirs'), ('guard', 'Sending avatar'), ('body', 'sending %03d'),
        ('lfail', 'failed to send %s\\n", _'), ('mf', 'sending manifest to'), ('ok', 'successfully sent')]


def one(path):
    d = tempfile.mkdtemp(dir=os.path.join(ROOT, 'build', 'ca'))
    try:
        shutil.copy(path, os.path.join(d, 'a.c'))
        r = subprocess.run([os.path.join(BIN, 'gcc.exe'), '-c', '-O3', '-I', os.path.join(ROOT, 'src'), '-fno-asynchronous-unwind-tables',
                            '-fdump-tree-optimized-details-blocks', 'a.c'], cwd=d, env=env, capture_output=True, text=True)
        if r.returncode:
            return path, r.stderr[:200]
        f = next(x for x in os.listdir(d) if x.endswith('.optimized'))
        t = open(os.path.join(d, f)).read()
        m = re.search(r'^;; Function sendAvatarData \(', t, re.M)
        t = t[m.start():t.find('\n;; Function ', m.end())]
        parts = re.split(r'^;;   basic block \d+, loop depth \d+, count \d+, freq (\d+)', t, flags=re.M)
        res = {}
        for i in range(1, len(parts), 2):
            for n, s in TAGS:
                if s in parts[i + 1] and n not in res:
                    res[n] = parts[i]
        return path, ' '.join('%s=%s' % (n, res.get(n, '-')) for n, _ in TAGS)
    finally:
        shutil.rmtree(d, ignore_errors=True)


with cf.ThreadPoolExecutor(4) as ex:
    for p, r in ex.map(one, sys.argv[1:]):
        print(os.path.basename(p), r)

"""python tools/wip/dehint/irrtldiff.py <a.c> <b.c> <fn> [regex] : dump every RTL pass of <fn> for both files, normalise
(addresses, uids, line numbers) and list per pass how many insn lines differ; with regex, print differing lines matching it."""
import difflib, os, re, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import irlib

a, b, fn = sys.argv[1:4]
rx = re.compile(sys.argv[4]) if len(sys.argv) > 4 else None
HEAD = re.compile(r'^;; Function (\S+) ')


def dumps(path):
    text = open(path, newline='').read().replace('\r\n', '\n')
    ok, o, d = irlib.compile_src(text, ['-fdump-rtl-all'])
    if not ok:
        print(o)
        sys.exit(1)
    r = {}
    for n in os.listdir(d):
        m = re.search(r'\.(\d+r\.[^.]+)$', n)
        if not m:
            continue
        keep, on = [], False
        for l in open(os.path.join(d, n), errors='replace'):
            h = HEAD.match(l)
            if h:
                on = h.group(1) == fn
            if on:
                keep.append(l.rstrip('\n'))
        r[m.group(1)] = keep
    irlib.cleanup(d)
    return r


def norm(ls):
    out = []
    for l in ls:
        l = re.sub(r'<[a-z_]+ [0-9a-f]+', '<x', l)
        l = re.sub(r'image_read\.c:\d+', 'L', l)
        l = re.sub(r'\b[0-9a-f]{8}\b', 'A', l)
        l = re.sub(r'^\((insn|jump_insn|call_insn|note|code_label|barrier)(/[a-z])? (\d+) (\d+) (\d+)', lambda m: '(' + m.group(1), l)
        out.append(l)
    return out


da, db = dumps(a), dumps(b)
for k in sorted(da, key=lambda s: int(s.split('r.')[0])):
    if k not in db:
        continue
    x, y = norm(da[k]), norm(db[k])
    if x == y:
        print(k, 'same')
        continue
    d = [l for l in difflib.unified_diff(x, y, lineterm='', n=0) if l[0] in '+-' and not l.startswith(('---', '+++'))]
    print(k, len(d))
    if rx:
        for l in d:
            if rx.search(l):
                print('   ', l[:150])

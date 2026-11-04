"""flpass.py <a.c> <b.c> <fn> [tree|rtl|all]: dump every pass for both files and list,
in pass order, the passes where fn's section differs, with the first differing lines.
Numbers in dump names aren't normalised, so renames show up: that's the point."""
import difflib, glob, os, re, subprocess, sys
import fllib as L


def dump(src, tag, kinds):
    d = os.path.join(L.BD, 'dump', tag)
    os.makedirs(d, exist_ok=True)
    for f in glob.glob(os.path.join(d, '*')):
        os.remove(f)
    inp = ('#line 1 "filelist_ini.c"\n' + open(src, newline='').read()).encode()
    fl = os.environ.get('FLFLAGS')
    fl = fl.split() if fl else L.FLAGS
    subprocess.run([L.GCC, '-c'] + fl + kinds + ['-I' + os.path.join(L.R, 'src'), '-x', 'c', '-', '-o', 'x.o'],
                   input=inp, cwd=d, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    r = {}
    for f in glob.glob(os.path.join(d, '-.*')):
        m = re.search(r'\.(\d+[a-z]\.[\w.+-]+)$', f)
        if m:
            r[m.group(1)] = f
    return r


def sect(f, fn):
    t = open(f, errors='replace').read()
    for q in re.split(r'(?m)^(?=;; Function )', t):
        if q.startswith(';; Function %s ' % fn):
            return q
    return ''


a, b, fn = sys.argv[1:4]
k = sys.argv[4] if len(sys.argv) > 4 else 'tree'
kinds = {'tree': ['-fdump-tree-all'], 'rtl': ['-fdump-rtl-all'], 'all': ['-fdump-tree-all', '-fdump-rtl-all']}[k]
da, db = dump(a, 'pa', kinds), dump(b, 'pb', kinds)
keys = sorted(da, key=lambda x: (int(re.match(r'\d+', x).group()), x))
shown = 0
for n in keys:
    if n not in db:
        continue
    sa, sb = sect(da[n], fn), sect(db[n], fn)
    if sa != sb and sa and sb:
        ls = [l for l in difflib.unified_diff(sa.splitlines(), sb.splitlines(), lineterm='', n=0) if not l.startswith(('---', '+++', '@@'))]
        print('== %s: %d lines' % (n, len(ls)))
        if shown < int(os.environ.get('FLSHOW', '3')):
            print('\n'.join(ls[:int(os.environ.get('FLLINES', '40'))]))
            shown += 1

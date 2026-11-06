"""mode_client attempt 7: compensate a counted removal (a near miss) with free asm goto list
edits: one label of mode_client added to one list (at its start or end), or one label
dropped from a list.  List labels are not counted, so a hit is a real count drop.

python tools/wip/dehint/mc7comp.py NAME [-base FILE] [-j 4] [-o DIR] [-two]
  NAME: a key of REMOVALS below (or 'list')
  -two: also pairs of list edits (adds/drops within 2 of the best singles, slow)"""
import itertools, os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib, mc7j2l

# name -> [(regex, replacement)], applied once each
REMOVALS = {
    'none': [],
    'c9': [(r' ?if \(__builtin_constant_p\(mode \+ 153200\)\) goto c9;', '')],
    't5': [(r' ?if \(__builtin_constant_p\(mode \+ 1084170\)\) goto t5;', '')],
    'c11': [(r' ?if \(__builtin_constant_p\(mode \+ 1095110\)\) goto c11;', '')],
    'c3': [(r' ?if \(__builtin_constant_p\(mode \+ 1085650\)\) goto c3;', '')],
    's5': [(r' ?if \(__builtin_constant_p\(mode \+ 1089530\)\) goto s5;', '')],
    'dtg2': [(r' ?if \(__builtin_constant_p\(mode \+ 156949\)\) goto dtg;', '')],
    't4': [(r' ?if \(__builtin_constant_p\(mode \+ 1049460\)[^;]*goto t4;', '')],
    'pdpin': [(r'(arg = dummy;\n\t\t\telse \{\n\t\t\t\targ = argv\[i \+ 1\];\n\t\t\t\ti\+\+;\n\t\t\t\tlog_printf\(0, "patch)', r'\1'),
              (r'(-p", 2\)\) \{\n\t\t\tif \(!argv\[i \+ 1\] \|\| i \+ 1 == argc \|\| )\(\{ __asm__ \("" :: "d"\(i \+ 1\)\); 0; \}\) \|\| ', r'\1')],
    'idpin': [(r'(-i", 2\)\) \{\n\t\t\tif \(!argv\[i \+ 1\] \|\| i \+ 1 == argc \|\| )\(\{ __asm__ \("" :: "d"\(i \+ 1\)\); 0; \}\) \|\| ', r'\1')],
    's4c12': [(r'JMP\(s4, c12\); ', '')],
    'dz': [(r' JMP\(dz\);', ''), (r'if \(0\) \{ dz: __builtin_unreachable\(\); \}', '')],
    'kk': [(r'\tint kk = __builtin_constant_p\(argc\);\n', ''),
           (r' __builtin_memset\(argv, 0, kk\); if \(!kk\) \{ ac: __attribute__\(\(cold\)\); __asm__ goto \("" :: "a"\(i\) :: r5x, r3x\); \}', '')],
    'dtg1': [(r' ?if \(__builtin_constant_p\(mode \+ 130\)\) goto dtg;', '')],
    'c10': [(r'JMP\(c10\);', '')],
    'hc4': [(r' hc4: __attribute__\(\(cold\)\);', '')],
    'u2b': [(r' ?if \(__builtin_constant_p\(mode \+ 50750\)\) goto u2;', '')],
    'ndl2': [(r' ?if \(__builtin_constant_p\(mode \+ 157368\)\) goto ndl;', '')],
    'ndl1': [(r' ?if \(__builtin_constant_p\(mode \+ 255562\)\) goto ndl;', '')],
    'ndl0': [(r' ?if \(__builtin_constant_p\(mode \+ 620\)\) goto ndl;', '')],
    'dsp107': [(r'__asm__ goto \("" : : "i"\(107\) : : dsp\); ', '')],
    'dspj': [(r'JMP\(dsp\);', '')],
    'fail': [(r'JMP\(fail\); ', '')],
    'u2a': [(r' ?if \(__builtin_constant_p\(mode \+ 321\)\) goto u2;', '')],
    'k61l': [(r'if \(\(char \*\)__builtin_constant_p\(i \+ 300\)[^;]*goto k61l;', '')],
    'k61l1': [(r' && \(char \*\)__builtin_constant_p\(i \+ 300 \+ 1\) == \(char \*\)1', '')],
    't4a': [(r' && __builtin_constant_p\(mode \+ 1049461\)', '')],
    'cold_rok': [(r'rok: __attribute__\(\(cold\)\);', 'rok: ;')],
    'cold_ac': [(r' ac: __attribute__\(\(cold\)\);', '')],
    'cold_fail': [(r'fail: __attribute__\(\(cold\)\);', 'fail:')],
    'arm9': [(r' && __builtin_constant_p\(mode \+ 909001\)', '')],
    'arm11': [(r' && __builtin_constant_p\(mode \+ 911004\)', '')],
    'arm7': [(r' && __builtin_constant_p\(mode \+ 907004\)', '')],
}


def mc_labels(t):
    s = t.index('int mode_client(')
    e = t.index('\n}\n', s)
    labs = []
    for m in re.finditer(r'(?<![:\w])(\w+):(?!:)', t[s:e]):
        if m.group(1) not in ('default', 'case') and m.group(1) not in labs:
            labs.append(m.group(1))
    return labs


def edits(t):
    st = [x for x in mc7j2l.stmts(t) if x[0] == 'mc']
    labs = mc_labels(t)
    out = []
    for j, o in enumerate(st):
        for lab in labs:
            if lab in o[5]:
                continue
            out.append(('add %s>%d.s' % (lab, j), [(o[3], o[3], lab + ', ')]))
            out.append(('add %s>%d.e' % (lab, j), [(o[4], o[4], ', ' + lab)]))
        if len(o[5]) > 1:
            for k, lab in enumerate(o[5]):
                # drop one label: rewrite the whole list
                rest = o[5][:k] + o[5][k + 1:]
                out.append(('drop %s@%d' % (lab, j), [(o[3], o[4], ', '.join(rest))]))
    return out


def main():
    a = sys.argv[1:]
    name = a[0]
    if name == 'list':
        print(' '.join(REMOVALS))
        return
    base = mc1lib.read_src(a[a.index('-base') + 1] if '-base' in a else mc1.BASE)
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    odir = a[a.index('-o') + 1] if '-o' in a else None
    t = base
    for rx, rep in REMOVALS[name]:
        t, n = re.subn(rx, rep, t, count=1)
        assert n == 1, (name, rx)
    c0 = mc1.count(t)['total']
    s0 = mc1lib.score_text(t)
    print(name, 'count', c0, 'alone', mc1lib.fmt(s0)[:60], flush=True)
    todo = [(k, mc7j2l.apply(t, ed)) for k, ed in edits(t)]
    if '-save' in a:
        # -save KEY OUT.c: write the removal + that one list edit (a level-2 base)
        key, out = a[a.index('-save') + 1], a[a.index('-save') + 2]
        open(out, 'w', newline='\n').write(dict(todo)[key] if key != 'none' else t)
        return

    def one(it):
        return it[0], mc1lib.score_text(it[1]), it[1]

    res = []
    with ThreadPoolExecutor(jobs) as ex:
        for k, s, txt in ex.map(one, todo):
            if 'compile' in s:
                continue
            if s['identical']:
                print('HIT', name, k, 'count', mc1.count(txt)['total'], flush=True)
                if odir:
                    open(os.path.join(odir, 'comp_%s_%s.c' % (name, re.sub(r'\W', '_', k))), 'w', newline='\n').write(txt)
                res.append((0, k))
            else:
                res.append((s['total'], k))
    res.sort()
    print(name, len(todo), 'variants; best', res[:8], flush=True)


if __name__ == '__main__':
    main()

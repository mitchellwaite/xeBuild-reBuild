"""mode_client attempt 13: natural (behaviour-preserving) rewrites, one site at a time, with
their block-count shift at vrp1 (mc12vrp target indices) and, with -score, the score.

Looking for a +1 / +2 that leaves the bytes alone (or nearly), to pair with the removals
that cost a block (mc12rm's 204,205,207 group).

python tools/wip/dehint/mc13nat.py BASE.c [-j 4] [-score] [-only RX] [-o DIR]"""
import os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1lib, mc12vrp, mc12filt

# (name, regex, replacement) applied at each match separately, from bpArgs on
RULES = [
    ('swapeq', r'(\bi \+ 1|\bj|\bi) == argc', r'argc == \1'),
    ('notnull', r'!(a|b|argv\[i \+ 1\])(?=[ )])', r'\1 == NULL'),
    ('preinc', r'arg = argv\[i \+ 1\];\n(\t+)i\+\+;', r'arg = argv[++i];\n\1;'),
    ('incfirst', r'arg = argv\[i \+ 1\];\n(\t+)i\+\+;', r'i++;\n\1arg = argv[i];'),
    ('ipinc', r'ip = argv\[i \+ 1\];\n(\t+)i\+\+;', r'ip = argv[++i];\n\1;'),
    ('ipincfirst', r'ip = argv\[i \+ 1\];\n(\t+)i\+\+;', r'i++;\n\1ip = argv[i];'),
    ('s_swap', r'if \(reboot == 2\)\n(\t+)(log_printf\(0, "reboot has already[^;]*;)\n\t+else \{\n(\t+)(log_printf\(0, "setting shutdown[^;]*;)\n\t+reboot = 1;\n\t+\}',
     r'if (reboot != 2) {\n\3\4\n\3reboot = 1;\n\1} else\n\1\2'),
    ('c7tern', r'if \(arg == dummy\)\n\t+clientPatches\(NULL\);\n\t+else\n\t+\{ AT\(p1\) clientPatches\(arg\); \}',
     r'{ AT(p1) clientPatches(arg == dummy ? NULL : arg); }'),
    ('c12tern', r'if \(arg == dummy\)\n\t+clientInfo\(NULL\);\n\t+else\n\t+\{ AT\(i1\) clientInfo\(arg\); \}',
     r'{ AT(i1) clientInfo(arg == dummy ? NULL : arg); }'),
    ('dummy_ne', r'if \(arg == dummy\)\n(\t+)(client\w+)\(NULL\);\n\t+else\n\t+\{ AT\((\w+)\) (client\w+)\(arg\); \}',
     r'if (arg != dummy)\n\1{ AT(\3) \4(arg); }\n\1else\n\1\2(NULL);'),
    ('hw_ne', r'if \(cinfo->hwFlags & 0x20\)', r'if ((cinfo->hwFlags & 0x20) != 0)'),
    ('reboot_ne', r'if \(reboot\)', r'if (reboot != 0)'),
    ('mode_ne', r'if \(mode\)', r'if (mode != 0)'),
    ('noent_brace', r'promptEnter = 0;', r'{ promptEnter = 0; }'),
    ('v_brace', r'else if \(!strnicmp\(argv\[i\], "-v", 2\)\)\n(\t+)log_verbose_flag\(argv\[i\]\[2\]\);\n(\t+)else',
     r'else if (!strnicmp(argv[i], "-v", 2)) {\n\1log_verbose_flag(argv[i][2]);\n\2} else'),
    ('local_a', r'if \(!argv\[i \+ 1\] \|\| i \+ 1 == argc \|\| \*argv\[i \+ 1\] == \'-\'\)',
     r"if (!(a = argv[i + 1]) || i + 1 == argc || *a == '-')"),
    ('strcmp_eq', r'!strnicmp\(argv\[i\], ("[^"]*"), (\d+)\)', r'strnicmp(argv[i], \1, \2) == 0'),
    ('eb_block', r'uint32_t block = myatoh32\(sblock, -1\);', r'uint32_t block;\n\n\tblock = myatoh32(sblock, -1);'),
    ('eb_ne', r'if \(block != -1\)', r'if (block != (uint32_t)-1)'),
    ('eb_succ', r'if \(netEraseBlock\(block, 1\)\)', r'if (netEraseBlock(block, 1) != 0)'),
    ('nc_not', r'if \(netConnect\(ip\)\)', r'if (netConnect(ip) != 0)'),
    ('ge_argc', r'(\bi \+ 1|\bj|\bi) == argc', r'\1 >= argc'),
    ('ret_end', r'\treturn 0;\nfail:', r'\treturn 0;\n\nfail:'),
]


def variants(t, only=None):
    s0 = t.index('static char *bpArgs(')
    out = []
    for name, rx, rep in RULES:
        if only and not re.search(only, name):
            continue
        for n, m in enumerate(re.finditer(rx, t[s0:])):
            a, b = s0 + m.start(), s0 + m.end()
            new = m.expand(rep)
            out.append(('%s#%d@%d' % (name, n, a), t[:a] + new + t[b:]))
    return out


def xs_of(th):
    return sorted(int(x) for _, _, x in th[:3] if x != '?')


def main():
    a = sys.argv[1:]
    t = mc1lib.read_src(a[0])
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    only = a[a.index('-only') + 1] if '-only' in a else None
    odir = a[a.index('-o') + 1] if '-o' in a else None
    base = xs_of(mc12vrp.threads(t))
    vs = variants(t, only)
    print('base', base, len(vs), 'variants', flush=True)

    def one(it):
        k, x = it
        try:
            th = mc12vrp.threads(x)
        except Exception:
            return k, None, None, x
        s = mc1lib.score_text(x, []) if '-score' in a else None
        return k, th, s, x
    with ThreadPoolExecutor(jobs) as ex:
        for k, th, s, x in ex.map(one, vs):
            if not th:
                print('err', k, flush=True)
                continue
            xs = xs_of(th)
            sh = xs[1] - base[1] if len(xs) > 1 else '?'
            sc = '' if s is None else (0 if s.get('identical') else s.get('total'))
            print('%+d' % sh if sh != '?' else '?', 'GOOD' if mc12filt.good(th) else 'bad ', xs, sc, k, flush=True)
            if odir and sh not in (0, '?'):
                os.makedirs(odir, exist_ok=True)
                open(os.path.join(odir, re.sub(r'[^\w@#]', '_', k) + '.c'), 'w', newline='\n').write(x)


if __name__ == '__main__':
    main()

"""mode_client attempt 3: natural same-meaning rewrites, one occurrence at a time (or all
occurrences of one rule), scored on one or more bases.  Aim: shift SSA numbering / block
order without a hint, so a near-miss base (e.g. build/mc/bC.c) becomes IDENTICAL.

python tools/wip/dehint/mc3nat.py BASE.c [BASE2.c ...] [-j N] [-r RULE_REGEX] [-pair]
Prints IDENTICAL hits (with trick count) and the best diffs per base.  -pair also tries
every pair of rewrites whose single diff on the base is <= 40.
Hits -> build/mc/m3nat_hits.json."""
import json, os, re, sys, itertools
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib

HITS = os.path.join(mc1lib.BUILD, 'm3nat_hits.json')

# (name, regex, replacement); each match position gives a variant, plus '*' = all
RULES = [
    ('preinc', r'(\w+) = argv\[\+\+i\];', r'i++; \1 = argv[i];'),
    ('preinc2', r'(\w+) = argv\[\+\+i\];', r'\1 = argv[i + 1]; i++;'),
    ('notcmp', r'!strnicmp\((argv\[i\], "[^"]*", \d)\)', r'strnicmp(\1) == 0'),
    ('argvi1', r"!argv\[i \+ 1\] \|\| i \+ 1 == argc \|\| \*argv\[i \+ 1\] == '-'",
     r"i + 1 == argc || !argv[i + 1] || *argv[i + 1] == '-'"),
    ('argvi1b', r"!argv\[i \+ 1\] \|\| i \+ 1 == argc \|\| \*argv\[i \+ 1\] == '-'",
     r"!argv[i + 1] || i + 1 == argc || argv[i + 1][0] == '-'"),
    ('ifmode', r'if \(mode\)', r'if (mode != 0)'),
    ('ret0', r'\treturn 0;\n', '\treturn mode * 0;\n'),
    ('dummyeq', r'arg == dummy', 'dummy == arg'),
    ('reb2', r'reboot == 2', 'reboot > 1'),
    ('reb1', r'reboot == 1', 'reboot < 2 && reboot'),
    ('logthen', r'log_printf\(0, "setting reboot on completion\\n"\);\n\t\t\treboot = 2;',
     'reboot = 2;\n\t\t\tlog_printf(0, "setting reboot on completion\\\\n");'),
    ('logthen2', r'log_printf\(0, "setting shutdown on completion\\n"\);\n\t\t\t\treboot = 1;',
     'reboot = 1;\n\t\t\t\tlog_printf(0, "setting shutdown on completion\\\\n");'),
    ('pe', r'log_printf\(0, "<enter> key on completion suppressed\\n"\);\n\t\t\tpromptEnter = 0;',
     'promptEnter = 0;\n\t\t\tlog_printf(0, "<enter> key on completion suppressed\\\\n");'),
    ('ival', r'\tint i = 0;\n', '\tint i;\n'),
    ('rbval', r'\tint reboot = 0;\n', '\tint reboot;\n'),
    ('rbinit', r'\tlog_set_name\("client"\);\n', '\tlog_set_name("client");\n\treboot = 0;\n'),
    ('modeinit', r'\tint mode = 0;\n', '\tint mode;\n'),
    ('modeinit2', r'\tlog_set_name\("client"\);\n', '\tlog_set_name("client");\n\tmode = 0;\n'),
    ('argnull', r'\tchar \*arg = NULL;\n', '\tchar *arg = 0;\n'),
    ('ipnull', r'\tchar \*ip = NULL;\n', '\tchar *ip = 0;\n'),
    ('sc', r'char \*start = NULL, \*count = NULL;', 'char *start = NULL;\n\tchar *count = NULL;'),
    ('sc2', r'char \*start = NULL, \*count = NULL;', 'char *count = NULL, *start = NULL;'),
    ('dummy', r'char dummy\[\] = "dummy";', 'char dummy[6] = "dummy";'),
    ('forw', r'for \(i = 0; i < argc; i\+\+\) \{', 'for (i = 0; argc > i; i++) {'),
    ('forw2', r'for \(i = 0; i < argc; i\+\+\) \{', 'for (i = 0; i < argc; ++i) {'),
    ('ipset', r'ip = argv\[\+\+i\];\n\t\t\tlog_printf\(0, "setting forced IP to %s\\n", ip\);',
     'i++;\n\t\t\tip = argv[i];\n\t\t\tlog_printf(0, "setting forced IP to %s\\\\n", ip);'),
    ('vflag', r'log_verbose_flag\(argv\[i\]\[2\]\)', 'log_verbose_flag(*(argv[i] + 2))'),
    ('bstart', r'start = b;', 'start = argv[j];'),
    ('nma', r'if \(NO_MODE_ARG\(mode, arg\)\)', 'if (!mode || !arg)'),
    ('preinc3', r'(\w+) = argv\[i \+ 1\]; i\+\+;', r'\1 = argv[++i];'),
    ('preinc4', r'(\w+) = argv\[i \+ 1\]; i\+\+;', r'i++; \1 = argv[i];'),
    ('ab', r'\tchar \*a, \*b;\n', '\tchar *b, *a;\n'),
    ('ab2', r'\tchar \*a, \*b;\n\tint j;\n', '\tint j;\n\tchar *a, *b;\n'),
    ('ab3', r'\tchar \*a, \*b;\n', '\tchar *a;\n\tchar *b;\n'),
    ('decl_ip', r'\tchar \*ip = NULL;\n\tchar \*arg = NULL;\n', '\tchar *arg = NULL;\n\tchar *ip = NULL;\n'),
    ('decl_reboot', r'\tint reboot = 0;\n\tchar \*ip = NULL;\n', '\tchar *ip = NULL;\n\tint reboot = 0;\n'),
    ('decl_i', r'\tint i = 0;\n\tint reboot = 0;\n', '\tint reboot = 0;\n\tint i = 0;\n'),
    ('wbarg', r'\t\t\ti \+= 2;\n\t\t\targ = argv\[i - 1\];\n', '\t\t\targ = a;\n\t\t\ti += 2;\n'),
    ('wbarg2', r'\t\t\ti \+= 2;\n\t\t\targ = argv\[i - 1\];\n', '\t\t\ti += 2;\n\t\t\targ = a;\n'),
    ('bparg', r'\t\t\ti = j;\n\t\t\targ = argv\[i - 1\];\n', '\t\t\targ = argv[i + 1];\n\t\t\ti = j;\n'),
    ('wbj', r'\t\t\tj = i \+ 1;\n\t\t\ta = argv\[j\];\n\t\t\tif \(j == argc', "\t\t\ta = argv[i + 1];\n\t\t\tif (i + 1 == argc"),
    ('eqarg', r'i \+ 1 == argc', 'argc == i + 1'),
    ('mode5', r'if \(mode\) \{ client_usage\(5, argv\[i\]\); \}', 'if (mode)\n\t\t\t\tclient_usage(5, argv[i]);'),
]



def variants(text, rx):
    out = []
    for nm, pat, rep in RULES:
        if rx and not re.search(rx, nm):
            continue
        ms = list(re.finditer(pat, text))
        for k, m in enumerate(ms):
            new = text[:m.start()] + m.expand(rep) + text[m.end():]
            if new != text:
                out.append(('%s@%d' % (nm, k), new))
        if len(ms) > 1:
            new = re.sub(pat, rep, text)
            if new != text:
                out.append(('%s@*' % nm, new))
    return out


def score(v):
    s = mc1lib.score_text(v[1])
    return v[0], s, mc1.count(v[1])['total']


def main():
    a = sys.argv[1:]
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    rx = a[a.index('-r') + 1] if '-r' in a else None
    skip = set()
    for f in ('-j', '-r'):
        if f in a:
            skip |= {a.index(f), a.index(f) + 1}
    bases = [x for k, x in enumerate(a) if k not in skip and not x.startswith('-')]
    hits = json.load(open(HITS)) if os.path.exists(HITS) else {}
    for b in bases:
        text = mc1lib.read_src(b)
        vs = variants(text, rx)
        print('==', b, len(vs), 'variants', flush=True)
        res = []
        with ThreadPoolExecutor(jobs) as ex:
            for k, s, c in ex.map(score, vs):
                if s.get('identical'):
                    print('HIT', b, k, c, flush=True)
                    hits['%s %s' % (b, k)] = c
                    json.dump(hits, open(HITS, 'w'), indent=1)
                elif 'total' in s:
                    res.append((s['total'], k))
                else:
                    print('ERR', k, mc1lib.fmt(s)[:120])
        res.sort()
        for d, k in res[:15]:
            print('  ', d, k)
        if '-pair' in a:
            near = [k for d, k in res if d <= 40]
            vd = dict(vs)
            todo = []
            for x, y in itertools.combinations(near, 2):
                # apply y's rewrite on x's text: recompute via rule on text of x
                nx, ny = x.split('@'), y.split('@')
                if nx[0] == ny[0]:
                    continue
                tx = vd[x]
                for k2, t2 in variants(tx, '^' + re.escape(ny[0]) + '$'):
                    if k2 == y:
                        todo.append((x + ' + ' + y, t2))
            print('  pairs', len(todo), flush=True)
            with ThreadPoolExecutor(jobs) as ex:
                for k, s, c in ex.map(score, todo):
                    if s.get('identical'):
                        print('HIT', b, k, c, flush=True)
                        hits['%s %s' % (b, k)] = c
                        json.dump(hits, open(HITS, 'w'), indent=1)


if __name__ == '__main__':
    main()

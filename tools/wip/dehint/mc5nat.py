"""mode_client attempt 5: mc3nat's natural rewrites plus rules for attempt 4's shapes (the
arg helpers, the reboot tail, the case bodies), crossed with the near misses of the base
(hint removal x rewrite, like mc3nx).

python tools/wip/dehint/mc5nat.py BASE.c [-m 40] [-j 4] [-r RULE_REGEX] [-only]
  -only  score the rewrites on the base alone (count-neutral IDENTICAL ones are drift bases)
Hits -> build/mc/m5nat_hits.json."""
import json, os, re, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib, mc3nat

HITS = os.path.join(mc1lib.BUILD, 'm5nat_hits.json')
SKIP = re.compile(r'fa([3-9]|1[0-9]|20)$|^G_|^fk_all$|^-np$|^rok_all$|^inline$')

NEW = [
    ('keys', r'mode = 3;\n\t\t\targ = dummy;', 'arg = dummy;\n\t\t\tmode = 3;'),
    ('ipinc', r'ip = argv\[i \+ 1\];\n\t\t\ti\+\+;', 'ip = argv[++i];'),
    ('ipinc2', r'ip = argv\[i \+ 1\];\n\t\t\ti\+\+;', 'i++;\n\t\t\tip = argv[i];'),
    ('tail', r'dtg: if \(reboot\)\n\t\t\{ netReboot\(reboot\); JMP\(fail\); ndl: netDisconnect\(\); \}\n\telse\n\t\tnetDisconnect\(\);',
     'dtg: if (!reboot)\n\t\tnetDisconnect();\n\telse\n\t\t{ netReboot(reboot); JMP(fail); ndl: netDisconnect(); }'),
    ('oa_i', r'static char \*oneArg\(int argc, char \*\*argv, int \*pi, int mode\)\n\{\n\tint i = \*pi;\n',
     'static char *oneArg(int argc, char **argv, int *pi, int mode)\n{\n\tint i = *pi;\n\tchar *a = argv[i + 1];\n'),
    ('oa_ret', r'\t\*pi = i \+ 1;\n\treturn argv\[i \+ 1\];', '\ti++;\n\t*pi = i;\n\treturn argv[i];'),
    ('wb_ret', r'\t\*pi = j;\n\treturn argv\[i \+ 1\];\n\}\n\n/\* -eb', '\t*pi = j;\n\treturn a;\n}\n\n/* -eb'),
    ('wb_arg2', r'\t\*arg2 = b;\n\tif \(mode\)\n\t\tclient_usage\(5, argv\[i\]\);\n\t\*pi = j;\n\treturn argv\[i \+ 1\];\n\}\n\n/\* -eb',
     '\tif (mode)\n\t\tclient_usage(5, argv[i]);\n\t*arg2 = b;\n\t*pi = j;\n\treturn argv[i + 1];\n}\n\n/* -eb'),
    ('usage0', r'client_usage\(0, NULL\)', 'client_usage(0, 0)'),
    ('vflag2', r'log_verbose_flag\(argv\[i\]\[2\]\)', 'log_verbose_flag(argv[i][2]);\n\t\t\t/* */'),
    ('rbt', r'if \(reboot == 1\)\n', 'if (reboot != 0)\n'),
    ('s_else', r'if \(reboot == 2\)\n\t\t\t\tlog_printf\(0, "reboot has already been set on command line, ignoring -s\\n"\);\n\t\t\telse \{\n\t\t\t\tlog_printf\(0, "setting shutdown on completion\\n"\);\n\t\t\t\treboot = 1;\n\t\t\t\}',
     'if (reboot != 2) {\n\t\t\t\tlog_printf(0, "setting shutdown on completion\\\\n");\n\t\t\t\treboot = 1;\n\t\t\t} else\n\t\t\t\tlog_printf(0, "reboot has already been set on command line, ignoring -s\\\\n");'),
    ('nma2', r'if \(NO_MODE_ARG\(mode, arg\)\)', 'if (mode == 0 || arg == NULL)'),
    ('help', r'!strnicmp\(argv\[i\], "help", 2\) \|\| !strnicmp\(argv\[i\], "-\?", 2\) \|\| !strnicmp\(argv\[i\], "/\?", 2\)',
     '!strnicmp(argv[i], "help", 2) || !strnicmp(argv[i], "-?", 2) ||\n\t\t    !strnicmp(argv[i], "/?", 2)'),
    ('cinfo', r'cinfo = netGetInfo\(\);', 'cinfo = (struct consoleinfo *)netGetInfo();'),
    ('i0', r'\tint i = 0;\n', '\tint i;\n'),
]
RULES = mc3nat.RULES + NEW


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


def main():
    a = sys.argv[1:]
    jobs = int(a[a.index('-j') + 1]) if '-j' in a else 4
    md = int(a[a.index('-m') + 1]) if '-m' in a else 40
    rx = a[a.index('-r') + 1] if '-r' in a else None
    basef = a[0]
    base = mc1lib.read_src(basef)
    n0 = mc1.count(base)['total']
    todo = [('base + ' + k, v) for k, v in variants(base, rx)]
    if '-only' not in a:
        sj = json.load(open(os.path.join(mc1lib.BUILD, os.environ.get('MC2SINGLES', 'm5_singles.json'))))
        t = mc1.build_template(base)
        ed = {e[0]: e for e in mc1.edits(t)}
        near = []
        for k, r in sj.items():
            m = re.match(r'(\d+)', r['r'])
            if k in ed and not SKIP.search(k) and not r['ok'] and m and int(m.group(1)) <= md:
                near.append(k)
        print(len(near), 'near misses', flush=True)
        for k in near:
            txt = mc1.render(t, *ed[k][1:])
            for vn, v in variants(txt, rx):
                todo.append(('%s + %s' % (k, vn), v))
    print(len(todo), 'variants', flush=True)
    hits = json.load(open(HITS)) if os.path.exists(HITS) else {}
    res = []
    done = 0
    with ThreadPoolExecutor(jobs) as ex:
        for k, s, c in ex.map(mc3nat.score, todo):
            done += 1
            if s.get('identical'):
                print('HIT', k, c, '(base %d)' % n0, flush=True)
                hits['%s %s' % (basef, k)] = c
                json.dump(hits, open(HITS, 'w'), indent=1)
            elif 'total' in s:
                res.append((s['total'], k))
            if done % 500 == 0:
                print('..', done, flush=True)
    res.sort()
    for d, k in res[:25]:
        print('  ', d, k)


if __name__ == '__main__':
    main()

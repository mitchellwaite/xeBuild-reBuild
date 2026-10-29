"""shapes.py: loop-side source shapes of s9/sp.c screened unprofiled (s12 plain.sh + content.py).
python tools/wip/mc/s15/shapes.py [name ...]  -> per shape: plain fncmp lines, content imbalance, same-as-base flag.
Variants are written to build/s15/<name>.c."""
import os, subprocess, sys
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
SRC = open(ROOT + r'\tools\wip\mc\s9\sp.c').read()
A = 'argv[i]'
U3 = "if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')\n\t\t\t\tclient_usage(3, argv[i]);"
R3 = "a = argv[i + 1];\n\t\t\tif (i + 1 == argc || !a || *a == '-')\n\t\t\t\tclient_usage(3, argv[i]);"
LOOP = 'for (i = 0; i < argc; i++) {'
V = {
 'base': [],
 'neq0': [('!strnicmp(argv[i], "-ip", 3)', 'strnicmp(argv[i], "-ip", 3) == 0'), ('!strnicmp(argv[i], "-r", 2)', 'strnicmp(argv[i], "-r", 2) == 0')],
 'while': [(LOOP, 'i = 0;\n\twhile (i < argc) {'), ('\t\t\tclient_usage(1, argv[i]);\n\t}', '\t\t\tclient_usage(1, argv[i]);\n\t\ti++;\n\t}')],
 'dowhile': [(LOOP, 'i = 0;\n\tif (argc > 0) do {'), ('\t\t\tclient_usage(1, argv[i]);\n\t}', '\t\t\tclient_usage(1, argv[i]);\n\t} while (++i < argc);')],
 'forpre': [(LOOP, 'for (i = 0; i < argc; ++i) {')],
 'forne': [(LOOP, 'for (i = 0; i != argc; i++) {')],
 'ip_r3': [('ip = argv[++i];', 'ip = argv[++i];'), (U3 + '\n\t\t\tip', R3 + '\n\t\t\tip')],
 'r_u3': [(R3 + '\n\t\t\tif (mode)\n\t\t\t\tclient_usage(5, argv[i]);\n\t\t\targ = argv[++i];\n\t\t\tlog_printf(0, "setting read', U3 + '\n\t\t\tif (mode)\n\t\t\t\tclient_usage(5, argv[i]);\n\t\t\targ = argv[++i];\n\t\t\tlog_printf(0, "setting read')],
 'w_u3': [(R3 + '\n\t\t\tif (mode)\n\t\t\t\tclient_usage(5, argv[i]);\n\t\t\targ = argv[++i];\n\t\t\tlog_printf(0, "setting write', U3 + '\n\t\t\tif (mode)\n\t\t\t\tclient_usage(5, argv[i]);\n\t\t\targ = argv[++i];\n\t\t\tlog_printf(0, "setting write')],
 'e_noE': [('E(!strnicmp(argv[i], "-e", 2))', '!strnicmp(argv[i], "-e", 2)')],
 'c_noE': [('E(!strnicmp(argv[i], "-c", 2))', '!strnicmp(argv[i], "-c", 2)')],
 'ip_E': [('!strnicmp(argv[i], "-ip", 3)', 'E(!strnicmp(argv[i], "-ip", 3))')],
 'r_E': [('!strnicmp(argv[i], "-r", 2)', 'E(!strnicmp(argv[i], "-r", 2))')],
 'w_E': [('!strnicmp(argv[i], "-w", 2)', 'E(!strnicmp(argv[i], "-w", 2))')],
 'help_elseif': [('\t\t\tclient_usage(0, NULL);\n\t\tif (!strnicmp(argv[i], "-noenter", 8))', '\t\t\tclient_usage(0, NULL);\n\t\telse if (!strnicmp(argv[i], "-noenter", 8))')],
 'cont_ip': [('\t\t\tlog_printf(0, "setting forced IP to %s\\n", ip);\n', '\t\t\tlog_printf(0, "setting forced IP to %s\\n", ip);\n\t\t\tcontinue;\n')],
 'cont_rw': [('\t\t\tmode = 1;\n', '\t\t\tmode = 1;\n\t\t\tcontinue;\n'), ('\t\t\tmode = 2;\n', '\t\t\tmode = 2;\n\t\t\tcontinue;\n')],
 'ip_inc': [('ip = argv[++i];', 'ip = argv[i + 1];\n\t\t\ti++;')],
 'r_inc': [('arg = argv[++i];\n\t\t\tlog_printf(0, "setting read', 'i++;\n\t\t\targ = argv[i];\n\t\t\tlog_printf(0, "setting read')],
 'e_inc': [('arg = argv[++i];\n\t\t\tlog_printf(0, "setting avatar', 'arg = argv[i + 1];\n\t\t\ti++;\n\t\t\tlog_printf(0, "setting avatar')],
 'e_pin': [('arg = argv[++i];\n\t\t\tlog_printf(0, "setting avatar', 'arg = argv[++i];\n\t\t\t__asm__("" :: "r"(i));\n\t\t\tlog_printf(0, "setting avatar')],
 'c_pin': [('arg = argv[++i];\n\t\t\tlog_printf(0, "setting xbox', 'arg = argv[++i];\n\t\t\t__asm__("" :: "r"(i));\n\t\t\tlog_printf(0, "setting xbox')],
 'ip_mode': [('ip = argv[++i];', 'ip = argv[++i];\n\t\t\t__asm__("");')],
 'opt_helper': [('int mode_client(int argc, char **argv)\n{', 'static __inline__ int opt(char *s, const char *o, int n) { return !strnicmp(s, o, n); }\nint mode_client(int argc, char **argv)\n{'),
                ('!strnicmp(argv[i], "-ip", 3)', 'opt(argv[i], "-ip", 3)'), ('!strnicmp(argv[i], "-r", 2)', 'opt(argv[i], "-r", 2)'), ('!strnicmp(argv[i], "-w", 2)', 'opt(argv[i], "-w", 2)')],
 'shared_u3': [(U3 + '\n\t\t\tip', 'if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == \'-\')\n\t\t\t\tgoto u3;\n\t\t\tip'),
               ('\t\t\tclient_usage(1, argv[i]);\n\t}', '\t\t\tclient_usage(1, argv[i]);\n\t\tcontinue;\n\tu3: client_usage(3, argv[i]);\n\t}')],
 'sloc': [(LOOP, LOOP + '\n\t\tchar *s = argv[i];'), ('strnicmp(argv[i], "-ip"', 'strnicmp(s, "-ip"'), ('strnicmp(argv[i], "-r"', 'strnicmp(s, "-r"'), ('strnicmp(argv[i], "-w"', 'strnicmp(s, "-w"')],
 'ge_argc': [('i + 1 == argc || !a', 'i + 1 >= argc || !a')],
 'r_order': [("if (i + 1 == argc || !a || *a == '-')\n\t\t\t\tclient_usage(3, argv[i]);\n\t\t\tif (mode)\n\t\t\t\tclient_usage(5, argv[i]);\n\t\t\targ = argv[++i];\n\t\t\tlog_printf(0, \"setting read", "if (!a || i + 1 == argc || *a == '-')\n\t\t\t\tclient_usage(3, argv[i]);\n\t\t\tif (mode)\n\t\t\t\tclient_usage(5, argv[i]);\n\t\t\targ = argv[++i];\n\t\t\tlog_printf(0, \"setting read")],
 'usage_ret': [('client_usage(3, argv[i]);', 'return client_usage(3, argv[i]), 0;')],
}


def run(name):
    s = SRC
    for o, n in V[name]:
        if o not in s:
            return name, 'MISSING ' + o[:40]
        s = s.replace(o, n, 1) if name not in ('usage_ret',) else s.replace(o, n)
    os.makedirs(ROOT + r'\build\s15', exist_ok=True)
    p = ROOT + r'\build\s15\%s.c' % name
    open(p, 'w', newline='\n').write(s)
    n = subprocess.run(['sh', 'tools/wip/mc/s12/plain.sh', 'build/s15/%s.c' % name], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    c = subprocess.run([sys.executable, 'tools/wip/mc/s12/content.py', 'build/s12/plain.%s.c.diff' % name, 'x'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    return name, n, c


if __name__ == '__main__':
    base = None
    for k in (sys.argv[1:] or V):
        r = run(k)
        if k == 'base':
            base = r[2]
        print(*r[:2], 'SAME' if base and len(r) > 2 and r[2] == base else '', r[2][:150] if len(r) > 2 else '', flush=True)

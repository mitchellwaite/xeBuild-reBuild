# mode_client -i / -p arms without the "d"(i + 1) pins: test shapes, both arms in product
import itertools
PIN = '!argv[i + 1] || i + 1 == argc || ({ __asm__ ("" :: "d"(i + 1)); 0; }) || *argv[i + 1] == \'-\''


def arm(msg, mode, cond, pre='', take='arg = argv[++i];', pos=False):
    body = '''				%s
				log_printf(0, "%s\\n", arg);''' % (take, msg)
    if pos:
        return '''%sif (%s) {
%s
			} else
				arg = dummy;
			mode = %d;''' % (pre, cond, body, mode)
    return '''%sif (%s)
				arg = dummy;
			else {
%s
			}
			mode = %d;''' % (pre, cond, body, mode)


def old(msg, mode):
    return arm(msg, mode, PIN)


NEG = {
    'A': ('!argv[i + 1] || i + 1 == argc || *argv[i + 1] == \'-\'', ''),
    'B': ('i + 1 == argc || !argv[i + 1] || *argv[i + 1] == \'-\'', ''),
    'C': ('i + 1 == argc || !a || *a == \'-\'', 'a = argv[i + 1];\n\t\t\t'),
    'D': ('!a || i + 1 == argc || *a == \'-\'', 'a = argv[i + 1];\n\t\t\t'),
    'E': ('j == argc || !a || *a == \'-\'', 'j = i + 1;\n\t\t\ta = argv[j];\n\t\t\t'),
    'F': ('!a || j == argc || *a == \'-\'', 'j = i + 1;\n\t\t\ta = argv[j];\n\t\t\t'),
    'G': ('!argv[i + 1] || i + 1 == argc || argv[i + 1][0] == \'-\'', ''),
}
POS = {
    'P': ('argv[i + 1] && i + 1 != argc && *argv[i + 1] != \'-\'', ''),
    'Q': ('i + 1 != argc && argv[i + 1] && *argv[i + 1] != \'-\'', ''),
    'R': ('i + 1 != argc && a && *a != \'-\'', 'a = argv[i + 1];\n\t\t\t'),
}
FORMS = {}
for k, (c, p) in NEG.items():
    FORMS[k] = dict(cond=c, pre=p)
    FORMS[k + 'i'] = dict(cond=c, pre=p, take='i++;\n\t\t\t\targ = argv[i];')
for k, (c, p) in POS.items():
    FORMS[k] = dict(cond=c, pre=p, pos=True)
ARMS = [('info dump path set to %s', 12), ('patch file set to %s', 7)]
V = {}
sel = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'P', 'Q', 'R', 'Ai', 'Ci']
for fi, fp in itertools.product(sel, sel):
    V['i%s_p%s' % (fi, fp)] = [(old(*ARMS[0]), arm(*ARMS[0], **FORMS[fi])), (old(*ARMS[1]), arm(*ARMS[1], **FORMS[fp]))]

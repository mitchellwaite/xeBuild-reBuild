"""Attempt 11: parseOption's vlen tail without the expect, aimed at the .rdata order (unknown,
incomplete, bad).  Forms move the unknown-with-value message inside `if (val)` so the
incomplete block has two preds (val false, vlen false) and isn't a threaded copy.

python tools/wip/dehint/op11tail.py [form ...]   (OUT=file writes the last form)
Each line: score, plus the literal order of the three messages (u, i, b)."""
import os, re, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

UNK = '''log_printf(1, "\\n\\n***** ERROR: unknown option '%s' with value '%s' provided on the command line!\\n", opt, val);'''
INC = '''log_printf(1, "\\n\\n***** ERROR: unknown or incomplete option '%s' provided on the command line!\\n", opt);'''
BADL = '''	log_printf(1, "\\n\\n***** ERROR: parsing option '%s', value '%s' is incorrect!\\n", opt, val);'''
# end of the val block (dvdkey arm) + the current tail
END = '''			xb.bootFlags |= 0x2000000;
			return 1;
		}
	}
	if (__builtin_expect(vlen, 0)) {
		''' + UNK + '''
		return 0;
	}
	''' + INC + '''
	return 0;
bad:
''' + BADL + '''
	return 0;
}
'''
DV = '''			xb.bootFlags |= 0x2000000;
			return 1;
		}
'''
TAILB = '''bad:
''' + BADL + '''
	return 0;
}
'''

F = {
    'E': END,
    # unknown inside the val block
    'IN': DV + '\t\tif (vlen) {\n\t\t\t' + UNK + '\n\t\t\treturn 0;\n\t\t}\n\t}\n\t' + INC + '\n\treturn 0;\n' + TAILB,
    # unknown inside the val block, no vlen test (val implies a value)
    'INv': DV + '\t\t' + UNK + '\n\t\treturn 0;\n\t}\n\t' + INC + '\n\treturn 0;\n' + TAILB,
    'INg': DV + '\t\tif (vlen) {\n\t\t\t' + UNK + '\n\t\t\treturn 0;\n\t\t}\n\t}\n\t' + INC + '\n\treturn 0;\n' + TAILB,
    'INn': DV + '\t\tif (!vlen)\n\t\t\tgoto inc;\n\t\t' + UNK + '\n\t\treturn 0;\n\t}\ninc:\n\t' + INC + '\n\treturn 0;\n' + TAILB,
    'INe': DV + '\t\tif (vlen > 0) {\n\t\t\t' + UNK + '\n\t\t\treturn 0;\n\t\t}\n\t}\n\t' + INC + '\n\treturn 0;\n' + TAILB,
    # unknown returns, then a second (dominated) test in front of incomplete: no join to
    # thread, the test is folded in place by VRP1 (it is still there at profile_estimate)
    'T1': DV + '\t}\n\tif (vlen) {\n\t\t' + UNK + '\n\t\treturn 0;\n\t}\n\tif (!vlen)\n\t\t' + INC + '\n\treturn 0;\n' + TAILB,
    'T2': DV + '\t}\n\tif (vlen) {\n\t\t' + UNK + '\n\t\treturn 0;\n\t}\n\tif (vlen == 0)\n\t\t' + INC + '\n\treturn 0;\n' + TAILB,
    'T4': DV + '\t}\n\tif (vlen) {\n\t\t' + UNK + '\n\t\treturn 0;\n\t}\n\tif (!vlen) {\n\t\t' + INC + '\n\t\treturn 0;\n\t}\n\treturn 0;\n' + TAILB,
    'T5': DV + '\t}\n\tif (vlen)\n\t\t' + UNK + '\n\telse if (!vlen)\n\t\t' + INC + '\n\treturn 0;\n' + TAILB,
    'T6': DV + '\t}\n\tif (vlen) {\n\t\t' + UNK + '\n\t\treturn 0;\n\t}\n\tif (!val)\n\t\t' + INC + '\n\treturn 0;\n' + TAILB,
    'T7': DV + '\t}\n\tif (vlen) {\n\t\t' + UNK + '\n\t\treturn 0;\n\t}\n\tif (vlen <= 0)\n\t\t' + INC + '\n\treturn 0;\n' + TAILB,
    # unknown inside the val block (no return), incomplete after it on its own test: the
    # join gets a third pred (val false) that VRP1 can't thread, so it survives
    'W1': DV + '\t\tif (vlen)\n\t\t\t' + UNK + '\n\t}\n\tif (!vlen)\n\t\t' + INC + '\n\treturn 0;\n' + TAILB,
    'W2': DV + '\t\tif (vlen)\n\t\t\t' + UNK + '\n\t}\n\tif (vlen == 0)\n\t\t' + INC + '\n\treturn 0;\n' + TAILB,
    'W3': DV + '\t\t' + UNK + '\n\t}\n\tif (!vlen)\n\t\t' + INC + '\n\treturn 0;\n' + TAILB,
    'W4': DV + '\t\tif (vlen)\n\t\t\t' + UNK + '\n\t}\n\tif (!val)\n\t\t' + INC + '\n\treturn 0;\n' + TAILB,
    'W5': DV + '\t\tif (vlen) {\n\t\t\t' + UNK + '\n\t\t\treturn 0;\n\t\t}\n\t}\n\tif (!vlen)\n\t\t' + INC + '\n\treturn 0;\n' + TAILB,
    # J25 (attempt 10's near miss) for reference
    'J25': DV + '\t}\n\tif (vlen)\n\t\t' + UNK + '\n\tif (!vlen)\n\t\t' + INC + '\n\treturn 0;\n' + TAILB,
}

KEYS = (('u', "unknown option '"), ('i', 'unknown or incomplete'), ('b', 'parsing option'))


BADMSG = '''"\\n\\n***** ERROR: parsing option '%s', value '%s' is incorrect!\\n"'''
INCMSG = '''"\\n\\n***** ERROR: unknown or incomplete option '%s' provided on the command line!\\n"'''
HEAD = 'uint32_t parseOption(char *opt)\n{\n'
# J25 with one message as a named array: (which, scope)
SA = {'SAb': ('b', 'fn'), 'SAi': ('i', 'fn'), 'SAbg': ('b', 'file'), 'SAig': ('i', 'file'),
      'SPb': ('b', 'ptr'), 'SPi': ('i', 'ptr')}


def make(t, f):
    assert END in t
    if f in SA:
        which, scope = SA[f]
        t = t.replace(END, F['J25'], 1)
        msg, name = (BADMSG, 'badfmt') if which == 'b' else (INCMSG, 'incfmt')
        assert t.count(msg) == 1
        t = t.replace(msg, name, 1)
        if scope == 'fn':
            t = t.replace(HEAD, HEAD + '\tstatic const char %s[] = %s;\n' % (name, msg), 1)
        elif scope == 'file':
            t = t.replace(HEAD, 'static const char %s[] = %s;\n\n' % (name, msg) + HEAD, 1)
        else:
            t = t.replace(HEAD, HEAD + '\tconst char *%s = %s;\n' % (name, msg), 1)
        return t
    return t.replace(END, F[f], 1)


def order(text):
    ok, o, d = optlib.compile_src(text, asm=True)
    if not ok:
        return '?'
    s = open(o).read()
    optlib.cleanup(d)
    pos = []
    for k, sub in KEYS:
        m = re.search(r'^LC(\d+):\n\t\.ascii "[^"]*' + re.escape(sub), s, re.M)
        pos.append((int(m.group(1)) if m else -1, k))
    return ''.join(k for _, k in sorted(pos))


def run(f):
    t = make(optlib.read_src(optlib.SRC), f)
    return f, optlib.score_text(t), order(t)


def main():
    fs = sys.argv[1:] or list(F) + list(SA)
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(run, fs))
    for f, r, o in sorted(res, key=lambda x: x[1].get('total', 99999)):
        print('%-5s %-4s %s' % (f, o, optlib.fmt(r)))
    if os.environ.get('OUT'):
        open(os.environ['OUT'], 'w', newline='\n').write(make(optlib.read_src(optlib.SRC), fs[-1]))


if __name__ == '__main__':
    main()

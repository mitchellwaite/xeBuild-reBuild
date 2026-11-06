"""Attempt 10: parseOption's two expects with the "\\n" success block shared with macid's
success (the reference crossjumps them: macid's tail jumps to setBool's block), so the
setBool edge's destination is no longer dominated by the test (no PRED_CALL), and with
flag joins in front of the return (no early return), x vlen tail forms.

python tools/wip/dehint/op10po.py [S,V ...]     (OUT=file writes the last combination)"""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

SB = '''	if (__builtin_expect(setBoolOption(opt, val) == 1, 0)) {
		log_printf(1, "\\n");
		return 1;
	}
'''
MAC = '''					log_printf(1, "\\n");
					return 1;
				}
				log_printf(1, "\\n\\n***** ERROR: invalid values'''
VL = '''	if (__builtin_expect(vlen, 0)) {
		log_printf(1, "\\n\\n***** ERROR: unknown option '%s' with value '%s' provided on the command line!\\n", opt, val);
		return 0;
	}
	log_printf(1, "\\n\\n***** ERROR: unknown or incomplete option '%s' provided on the command line!\\n", opt);
	return 0;
bad:
	log_printf(1, "\\n\\n***** ERROR: parsing option '%s', value '%s' is incorrect!\\n", opt, val);
	return 0;
}
'''
UNK = '''log_printf(1, "\\n\\n***** ERROR: unknown option '%s' with value '%s' provided on the command line!\\n", opt, val);'''
INC = '''log_printf(1, "\\n\\n***** ERROR: unknown or incomplete option '%s' provided on the command line!\\n", opt);'''
BAD = '''bad:
	log_printf(1, "\\n\\n***** ERROR: parsing option '%s', value '%s' is incorrect!\\n", opt, val);
	return 0;
}
'''
NL = '''nl:
	log_printf(1, "\\n");
	return 1;
'''

# setBool test forms: (replacement for SB, replacement for macid's tail or None, tail extra)
S = {
    'E': (SB, None, ''),
    'P': (SB.replace('__builtin_expect(setBoolOption(opt, val) == 1, 0)', 'setBoolOption(opt, val) == 1'), None, ''),
    # label inside the setBool arm, macid jumps back to it
    'Lin': (SB.replace('__builtin_expect(setBoolOption(opt, val) == 1, 0)) {\n', 'setBoolOption(opt, val) == 1) {\nnl:\n'),
            '\t\t\t\t\tgoto nl;\n\t\t\t\t}\n\t\t\t\tlog_printf(1, "\\n\\n***** ERROR: invalid values', ''),
    # both goto a block at the end (after bad / before bad)
    'Laft': ('\tif (setBoolOption(opt, val) == 1)\n\t\tgoto nl;\n',
             '\t\t\t\t\tgoto nl;\n\t\t\t\t}\n\t\t\t\tlog_printf(1, "\\n\\n***** ERROR: invalid values', 'after'),
    'Lbef': ('\tif (setBoolOption(opt, val) == 1)\n\t\tgoto nl;\n',
             '\t\t\t\t\tgoto nl;\n\t\t\t\t}\n\t\t\t\tlog_printf(1, "\\n\\n***** ERROR: invalid values', 'before'),
    'Ltop': ('\tif (setBoolOption(opt, val) == 1)\n\t\tgoto nl;\n',
             '\t\t\t\t\tgoto nl;\n\t\t\t\t}\n\t\t\t\tlog_printf(1, "\\n\\n***** ERROR: invalid values', 'top'),
    # result join: r flag
    'R': ('\tok = setBoolOption(opt, val) == 1;\n\tif (ok)\n\t\tlog_printf(1, "\\n");\n\tif (ok)\n\t\treturn 1;\n', None, ''),
    # shared nl, plus macid's own via goto and a result join
    'Lin_r': (SB.replace('__builtin_expect(setBoolOption(opt, val) == 1, 0)) {\n', 'setBoolOption(opt, val) == 1) {\nnl:\n'),
              '\t\t\t\t\tgoto nl;\n\t\t\t\t}\n\t\t\t\tlog_printf(1, "\\n\\n***** ERROR: invalid values', ''),
}
V = {
    'E': None,
    'P': VL.replace('__builtin_expect(vlen, 0)', 'vlen'),
    'N': '\tif (!vlen) {\n\t\t' + INC + '\n\t\treturn 0;\n\t}\n\t' + UNK + '\n\treturn 0;\n' + BAD,
    'IE': '\tif (vlen)\n\t\t' + UNK + '\n\telse\n\t\t' + INC + '\n\treturn 0;\n' + BAD,
    'IEn': '\tif (!vlen)\n\t\t' + INC + '\n\telse\n\t\t' + UNK + '\n\treturn 0;\n' + BAD,
    # one arm through a flag join (ok), the other returns
    'J1': '\tok = 0;\n\tif (vlen) {\n\t\t' + UNK + '\n\t\tok = 1;\n\t}\n\tif (!ok) {\n\t\t' + INC + '\n\t}\n\treturn 0;\n' + BAD,
    'J2': '\tif (vlen) {\n\t\t' + UNK + '\n\t\treturn 0;\n\t}\n\tok = 0;\n\t' + INC + '\n\treturn ok;\n' + BAD,
    'J1b': '\tok = 1;\n\tif (vlen) {\n\t\t' + UNK + '\n\t\tok = 0;\n\t}\n\tif (ok)\n\t\t' + INC + '\n\treturn 0;\n' + BAD,
    'J1c': '\tif (vlen) {\n\t\t' + UNK + '\n\t\tok = 1;\n\t} else\n\t\tok = 0;\n\tif (!ok)\n\t\t' + INC + '\n\treturn 0;\n' + BAD,
    'J1d': '\tok = vlen != 0;\n\tif (ok)\n\t\t' + UNK + '\n\tif (!ok)\n\t\t' + INC + '\n\treturn 0;\n' + BAD,
    'J1e': '\tok = 0;\n\tif (vlen) {\n\t\t' + UNK + '\n\t\tok = 1;\n\t}\n\tif (!ok)\n\t\t' + INC + '\n\treturn 0;\n' + BAD.replace('\treturn 0;\n}\n', '\treturn 0;\n}\n'),
    'J1f': '\tok = 0;\n\tif (vlen) {\n\t\t' + UNK + '\n\t\tok = 1;\n\t}\n\tif (ok)\n\t\treturn 0;\n\t' + INC + '\n\treturn 0;\n' + BAD,
    'J1g': '\tok = 0;\n\tif (vlen) {\n\t\t' + UNK + '\n\t\tok = 1;\n\t}\n\tif (!ok) {\n\t\t' + INC + '\n\t\treturn 0;\n\t}\n\treturn 0;\n' + BAD,
    'J1h': '\tok = 0;\n\tif (vlen) {\n\t\t' + UNK + '\n\t\tok = 1;\n\t}\n\tif (!ok)\n\t\t' + INC + '\n\treturn 0;\n' + BAD.replace('val);\n\treturn 0;', 'val);\n\treturn 0;'),
    'J9': '\tok = 1;\n\tif (vlen) {\n\t\t' + UNK + '\n\t\tok = 0;\n\t}\n\tif (ok) {\n\t\t' + INC + '\n\t\tok = 0;\n\t}\n\treturn ok;\n' + BAD,
    'J10': '\tok = 0;\n\tif (vlen) {\n\t\t' + UNK + '\n\t\tgoto out;\n\t}\n\t' + INC + '\nout:\n\treturn ok;\n' + BAD,
    'J11': '\tif (vlen) {\n\t\t' + UNK + '\n\t\tgoto out;\n\t}\n\t' + INC + '\nout:\n\treturn 0;\n' + BAD,
    'J25': '\tif (vlen)\n\t\t' + UNK + '\n\tif (!vlen)\n\t\t' + INC + '\n\treturn 0;\n' + BAD,
    'J26': '\tif (vlen)\n\t\t' + UNK + '\n\telse\n\t\tvlen = -1;\n\tif (vlen < 0)\n\t\t' + INC + '\n\treturn 0;\n' + BAD,
    'J27': '\tok = 0;\n\tif (vlen) {\n\t\t' + UNK + '\n\t\tok = 1;\n\t}\n\tif (!ok)\n\t\t' + INC + '\n\treturn 0;\n' + BAD.replace('bad:\n', 'bad:\n\tok = 0;\n'),
    # val-based
    'Pv': VL.replace('__builtin_expect(vlen, 0)', 'val'),
    'Nv': '\tif (!val) {\n\t\t' + INC + '\n\t\treturn 0;\n\t}\n\t' + UNK + '\n\treturn 0;\n' + BAD,
}


def make(t, s, v):
    sb, mac, where = S[s]
    assert SB in t and MAC in t and VL in t
    t = t.replace(SB, sb, 1)
    if mac is not None:
        t = t.replace(MAC, mac, 1)
    if V[v] is not None:
        t = t.replace(VL, V[v], 1)
    if where == 'after':
        t = t.replace(BAD, BAD[:-2] + NL + '}\n', 1)
    elif where == 'before':
        t = t.replace(BAD, NL + BAD, 1)
    elif where == 'top':
        i = t.find(BAD)
        # just before the vlen test / tail
        k = t.rfind('\t}\n', 0, t.find('vlen', t.find('uint32_t parseOption(')+600) )
    return t


def run(sv):
    s, v = sv
    t = make(optlib.read_src(optlib.SRC), s, v)
    r = optlib.score_text(t)
    return s, v, r


def main():
    args = sys.argv[1:]
    if args:
        combos = [tuple(a.split(',')) for a in args]
    else:
        combos = [(s, v) for s in S if s != 'Ltop' for v in V]
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(run, combos))
    for s, v, r in sorted(res, key=lambda x: x[2].get('total', 99999)):
        print('%-6s %-4s %s' % (s, v, optlib.fmt(r)))
    if os.environ.get('OUT'):
        s, v = combos[-1]
        open(os.environ['OUT'], 'w', newline='\n').write(make(optlib.read_src(optlib.SRC), s, v))


if __name__ == '__main__':
    main()

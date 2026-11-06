"""Attempt 9: cputemp's and gpufan's arms without po_hint, in shapes where the success edge
loses the early-return prediction (DS(opcode 28%, call 71%) = 48.8% bad, which op9end.py's
shared_before shows is enough) because the log block doesn't go straight to the return
block: result variables and repeated tests that are threaded away after profile_estimate.

python tools/wip/dehint/op9rv.py [form...]     (OUT=file writes the last form's source)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib, op9end

ARM = '''			xb.%(f)s = myatou32(val, -1);
			if (xb.%(f)s == -1)
				goto bad;
			log_printf(1, "Using %(n)s option, value %(p)s\\n", xb.%(f)s);
			return 1;
'''
LOG = 'log_printf(1, "Using %(n)s option, value %(p)s\\n", xb.%(f)s);'
FORMS = {
    # ok flag, log under it, then leave on it
    'F1': '\t\t\txb.%(f)s = myatou32(val, -1);\n\t\t\tok = xb.%(f)s != -1;\n\t\t\tif (ok)\n\t\t\t\t%(l)s\n\t\t\tif (!ok)\n\t\t\t\tgoto bad;\n\t\t\treturn 1;\n',
    'F1b': '\t\t\txb.%(f)s = myatou32(val, -1);\n\t\t\tok = xb.%(f)s != -1;\n\t\t\tif (ok)\n\t\t\t\t%(l)s\n\t\t\tif (ok)\n\t\t\t\treturn 1;\n\t\t\tgoto bad;\n',
    'F1c': '\t\t\txb.%(f)s = myatou32(val, -1);\n\t\t\tok = xb.%(f)s != -1;\n\t\t\tif (ok)\n\t\t\t\t%(l)s\n\t\t\telse\n\t\t\t\tgoto bad;\n\t\t\treturn ok;\n',
    'F1d': '\t\t\txb.%(f)s = myatou32(val, -1);\n\t\t\tif (xb.%(f)s == -1)\n\t\t\t\tgoto bad;\n\t\t\t%(l)s\n\t\t\treturn xb.%(f)s != -1;\n',
    'F2': '\t\t\txb.%(f)s = myatou32(val, -1);\n\t\t\tif (xb.%(f)s != -1)\n\t\t\t\t%(l)s\n\t\t\tif (xb.%(f)s != -1)\n\t\t\t\treturn 1;\n\t\t\tgoto bad;\n',
    'F2b': '\t\t\txb.%(f)s = myatou32(val, -1);\n\t\t\tif (xb.%(f)s != -1)\n\t\t\t\t%(l)s\n\t\t\tif (xb.%(f)s == -1)\n\t\t\t\tgoto bad;\n\t\t\treturn 1;\n',
    'F3': '\t\t\tok = (xb.%(f)s = myatou32(val, -1)) != -1;\n\t\t\tif (ok)\n\t\t\t\t%(l)s\n\t\t\telse\n\t\t\t\tgoto bad;\n\t\t\treturn 1;\n',
    'F4': '\t\t\txb.%(f)s = myatou32(val, -1);\n\t\t\tok = 0;\n\t\t\tif (xb.%(f)s != -1) {\n\t\t\t\t%(l)s\n\t\t\t\tok = 1;\n\t\t\t}\n\t\t\tif (!ok)\n\t\t\t\tgoto bad;\n\t\t\treturn 1;\n',
    'F4b': '\t\t\txb.%(f)s = myatou32(val, -1);\n\t\t\tok = 0;\n\t\t\tif (xb.%(f)s != -1) {\n\t\t\t\t%(l)s\n\t\t\t\tok = 1;\n\t\t\t}\n\t\t\tif (ok)\n\t\t\t\treturn 1;\n\t\t\tgoto bad;\n',
    'F4c': '\t\t\txb.%(f)s = myatou32(val, -1);\n\t\t\tok = 0;\n\t\t\tif (xb.%(f)s != -1) {\n\t\t\t\t%(l)s\n\t\t\t\tok = 1;\n\t\t\t}\n\t\t\tif (!ok)\n\t\t\t\tgoto bad;\n\t\t\treturn ok;\n',
}


def form(t, f, arms=(('cpuTemp', 'CPUTEMP'), ('gpuFan', 'GPUFAN'))):
    t = op9end.form(t, 'plain')
    for fld, nm in arms:
        d = {'f': fld, 'n': nm, 'p': '0x%x' if 'Region' in fld else '%d'}
        a = ARM % d
        assert a in t, fld
        d['l'] = LOG % d
        t = t.replace(a, FORMS[f] % d)
    if 'ok' in FORMS[f]:
        t = t.replace('\tint i, len, vlen;\n', '\tint i, len, vlen, ok;\n', 1)
    return t


ALL = [('cpuTemp', 'CPUTEMP'), ('gpuTemp', 'GPUTEMP'), ('edramTemp', 'EDRAMTEMP'),
       ('overCpuTemp', 'OVERCPUTEMP'), ('overGpuTemp', 'OVERGPUTEMP'),
       ('overEdramTemp', 'OVEREDRAMTEMP'), ('cpuFan', 'CPUFAN'), ('gpuFan', 'GPUFAN'),
       ('avRegion', 'AVREGION'), ('gameRegion', 'GAMEREGION'), ('dvdRegion', 'DVDREGION')]
SETS = {'two': ALL[0:1] + ALL[7:8], 'cpu': ALL[0:1], 'gpu': ALL[7:8], 'temps': ALL[:8], 'all': ALL, 'regions': ALL[8:], 'two+regions': [ALL[0], ALL[7]] + ALL[8:],
        'others': ALL[1:7]}
for _i in range(len(ALL)):
    SETS['-' + ALL[_i][0]] = ALL[:_i] + ALL[_i + 1:]
    SETS['+' + ALL[_i][0]] = ALL[_i:_i + 1]
    SETS['t-' + ALL[_i][0]] = [a for a in ALL[:8] if a != ALL[_i]]


def main():
    t = optlib.read_src(optlib.SRC)
    fs = sys.argv[1:] or list(FORMS)
    arms = SETS[os.environ.get('ARMS', 'two')]
    for f in fs:
        v = form(t, f, arms)
        if os.environ.get('OUT'):
            open(os.environ['OUT'], 'w', newline='\n').write(v)
        print(f, optlib.fmt(optlib.score_text(v)))


if __name__ == '__main__':
    main()

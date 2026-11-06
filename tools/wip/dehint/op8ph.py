"""Attempt 8: cputemp's and gpufan's arms without po_hint, in shapes where the success
edge might not get PRED_CALL (see notes: DS(61%, 28%) is po_hint's 37.8%).

python tools/wip/dehint/op8ph.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

ARM = '''			xb.%s = myatou32(val, -1);
			if (xb.%s == -1) {
				po_hint(&dead);
				goto bad;
			}
			log_printf(1, "Using %s option, value %%d\\n", xb.%s);
			return 1;
'''
LOG = 'log_printf(1, "Using %s option, value %%d\\n", xb.%s);'


def form(f, fld, nm):
    lg = LOG % (nm, fld)
    st = '\t\t\txb.%s = myatou32(val, -1);\n' % fld
    if f == 'S1':
        return st + '\t\t\tif (xb.%s != -1) {\n\t\t\t\t%s\n\t\t\t\treturn 1;\n\t\t\t}\n\t\t\tgoto bad;\n' % (fld, lg)
    if f == 'S2':
        return st + '\t\t\tif (xb.%s != -1)\n\t\t\t\t%s\n\t\t\telse\n\t\t\t\tgoto bad;\n\t\t\treturn 1;\n' % (fld, lg)
    if f == 'S3':
        return st + '\t\t\tif (xb.%s == -1)\n\t\t\t\tgoto bad;\n\t\t\t%s\n\t\t\treturn 1;\n' % (fld, lg)
    if f == 'S4':
        return st + '\t\t\tif (xb.%s == -1)\n\t\t\t\tgoto bad;\n\t\t\tif (xb.%s != -1)\n\t\t\t\t%s\n\t\t\treturn 1;\n' % (fld, fld, lg)


def main():
    t = optlib.read_src(optlib.SRC)
    arms = [('cpuTemp', 'CPUTEMP'), ('gpuFan', 'GPUFAN')]
    for fld, nm in arms:
        assert ARM % (fld, fld, nm, fld) in t, fld
    for f in ['S1', 'S2', 'S3', 'S4']:
        v = t
        for fld, nm in arms:
            v = v.replace(ARM % (fld, fld, nm, fld), form(f, fld, nm))
        print(f, optlib.fmt(optlib.score_text(v)))


if __name__ == '__main__':
    main()

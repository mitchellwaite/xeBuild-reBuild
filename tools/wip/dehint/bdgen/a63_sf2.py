"""Attempt 63: target B through the sig-failed arm's own `<= 5` exit (no r test in the tail, so no
exp_pr), crossed with failed-arm forms, tail forms and the setFlashBuild argument.  Score at no param:
python tools/wip/dehint/bdgen/a60lib.py tools/wip/dehint/bdgen/a63_sf2.py -p 0 -o "-" """
import itertools, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import bdlib
T4, T7 = '\t' * 4, '\t' * 7
_src = bdlib.read_src()
_src = _src[_src.index('int loadBlFiles(void)'):]
SIGBLK = _src[_src.index(T4 + 'if (type == 5 || type == 17'):_src.index('\t\t\tcase 6:')]
SIGPART = SIGBLK[:SIGBLK.index(T4 + '/* the expect')]
LOGF = 'log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);\n'
FAILED = T7 + LOGF + T7 + 'r = -1;\n'
assert FAILED in SIGPART
FA = {
    'a': T7 + LOGF + T7 + 'if (xb.type <= BUILD_DEVGL16)\n' + T7 + '\tgoto fail;\n' + T7 + 'r = -1;\n',
    'b': T7 + LOGF + T7 + 'r = -1;\n' + T7 + 'if (xb.type <= BUILD_DEVGL16)\n' + T7 + '\tgoto fail;\n',
    'c': T7 + 'r = -1;\n' + T7 + LOGF + T7 + 'if (xb.type <= BUILD_DEVGL16)\n' + T7 + '\tgoto fail;\n',
    'd': T7 + LOGF + T7 + 'if (xb.type > BUILD_DEVGL16)\n' + T7 + '\tr = -1;\n' + T7 + 'else\n' + T7 + '\tgoto fail;\n',
}
TAILS = {
    'brk': T4 + 'if (xb.type <= BUILD_DEVGL16)\n' + T4 + '\tbreak;\n' + T4 + 'if (type == 14)\n' + T4 + '\tsetFlashBuild(getBeU16(%s + 2));\n' + T4 + 'break;\n',
    'and': T4 + 'if (xb.type > BUILD_DEVGL16 && type == 14)\n' + T4 + '\tsetFlashBuild(getBeU16(%s + 2));\n' + T4 + 'break;\n',
    'and2': T4 + 'if (type == 14 && xb.type > BUILD_DEVGL16)\n' + T4 + '\tsetFlashBuild(getBeU16(%s + 2));\n' + T4 + 'break;\n',
    'kit': T4 + 'if (xb.type > BUILD_DEVGL16) {\n' + T4 + '\tif (type == 14)\n' + T4 + '\t\tsetFlashBuild(getBeU16(%s + 2));\n' + T4 + '}\n' + T4 + 'break;\n',
}
ARGS = {'xi': 'xb.files[i].data', 'e': 'e->data'}
V = {}
for (fk, f), (tk, t), (ak, arg) in itertools.product(FA.items(), TAILS.items(), ARGS.items()):
    V['%s_%s_%s' % (fk, tk, ak)] = [(SIGBLK, SIGPART.replace(FAILED, f) + t % arg)]

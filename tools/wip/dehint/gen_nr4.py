"""Diagnostic, not a candidate: side-effect select + the asm use of got, at a few places, to find what the clone needs."""
import importlib.util, os
spec = importlib.util.spec_from_file_location('g2', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_nr2.py'))
g2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g2)
BASE = g2.src('plain', 'plain', 'side', g2.RECV['plain'], 0)
USE = '__asm__ ("" : : "g"(got));'
SITES = {
    'none': ('', ''),
    'log': ('\tlog_printf(0, "received only', '\t' + USE + '\n\tlog_printf(0, "received only'),
    'okstore': ('\t\t*len = size;', '\t\t' + USE + '\n\t\t*len = size;'),
    'afterloop': ("\tif (got == size) {", '\t' + USE + "\n\tif (got == size) {"),
    'init': ('\tgot = 0;\n', '\tgot = 0;\n\t' + USE + '\n'),
    'body': ('\t\tgot += r;\n', '\t\tgot += r;\n\t\t' + USE + '\n'),
    'free': ('bytes! fail\\n", got, size);\n', 'bytes! fail\\n", got, size);\n\t' + USE + '\n'),
}


def variants():
    for k, (a, b) in SITES.items():
        s = BASE
        if a:
            assert a in s, k
            s = s.replace(a, b)
        yield k, s

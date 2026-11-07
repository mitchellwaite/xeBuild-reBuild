"""Attempt 62: exp_pr kept, no --param (gcc's default 90): at q = 10% the SE copy's P(>5) is 38.1% and needs
< 37.5%, i.e. by the joiner formula P(<=5) = Xc p (1 - q) / (Xc - S) the signature-failed share S / Xc has to
go from 0.275 to 0.28 (S 41 -> 42 at Xc 149).  Diagnostics (d_*: expects, not natural) and natural shapes of
the signature block.
python tools/wip/dehint/bdgen/a62_semeas.py tools/wip/dehint/bdgen/a62_s.py -x -p 90   (cheap)
python tools/wip/dehint/bdgen/a60lib.py tools/wip/dehint/bdgen/a62_s.py -p 0 -o "-"     (score, no param)"""
VER = 'if (!cbVerifySig(e->data, xb.pub1bl)) {'
PUB = '\t\t\t\t\tif (xb.pub1bl) {\n\t\t\t\t\t\tif (!cbVerifySig'
SIG = 'if (type == 5 || type == 17 || type == 11) {'
FAILED = '''							log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);
							r = -1;'''
V = {
    'src': [],
    'd_pf90': [(VER, 'if (__builtin_expect(!cbVerifySig(e->data, xb.pub1bl), 1)) {')],
    'd_pk90': [(PUB, PUB.replace('if (xb.pub1bl)', 'if (__builtin_expect(xb.pub1bl != 0, 1))'))],
    'sig_5_11_17': [(SIG, 'if (type == 5 || type == 11 || type == 17) {')],
    'sig_11_5_17': [(SIG, 'if (type == 11 || type == 5 || type == 17) {')],
    'sig_17_5_11': [(SIG, 'if (type == 17 || type == 5 || type == 11) {')],
    'fail_r_first': [(FAILED, '''							r = -1;
							log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);''')],
    'ver_eq0': [(VER, 'if (cbVerifySig(e->data, xb.pub1bl) == 0) {')],
    'pub_ne': [(PUB, PUB.replace('if (xb.pub1bl)', 'if (xb.pub1bl != NULL)'))],
}
PASSED = '''						} else
							log_printf(1, "loaded %s, signature check passed!'''
V['d_pf71'] = [(PASSED, PASSED.replace('} else\n', '} else if (xb.pub1bl)\n'))]

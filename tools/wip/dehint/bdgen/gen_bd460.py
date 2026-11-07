"""Attempt 34: pin_d by the frequencies IRA sorts the join's thread by.  Within the thread {r535 base, r534 n*0x42c,
r125 n} allocnos pop in ALLOCNO_FREQ order: base 135 (def + use at the join, 50 each, + the size use in the d block, 35),
n 131 (join use 50 + first-path def 50 + fallback defs 31), r534 100.  n popped first would take edx and pull the base
along its copies (the reference).  So: case 27's load chain in forms that give the fallbacks more flow (sequential
`*pr` tests, gotos, nested), and the d test in forms with another probability.  pin_d off.  Runs on src as of 34b3ab10."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdhints, bdrun

FOCUS = ['_loadBlFiles']

HEAD = '''		if (loadBaseFile(e->name, &xb.files[xb.nFlashFiles]) &&
		    loadBaseFile("config.bin", &xb.files[xb.nFlashFiles]) &&
		    (*pr = loadBaseFile("config_raw.bin", &xb.files[xb.nFlashFiles]))) {
'''
F = '&xb.files[xb.nFlashFiles]'
HEADS = {
    'src': HEAD,
    'seq': ('\t\t*pr = loadBaseFile(e->name, %s);\n\t\tif (*pr)\n\t\t\t*pr = loadBaseFile("config.bin", %s);\n'
            '\t\tif (*pr)\n\t\t\t*pr = loadBaseFile("config_raw.bin", %s);\n\t\tif (*pr) {\n') % (F, F, F),
    'seqn': ('\t\t*pr = loadBaseFile(e->name, %s);\n\t\tif (*pr) {\n\t\t\t*pr = loadBaseFile("config.bin", %s);\n'
             '\t\t\tif (*pr)\n\t\t\t\t*pr = loadBaseFile("config_raw.bin", %s);\n\t\t}\n\t\tif (*pr) {\n') % (F, F, F),
    'or': ('\t\tif (!loadBaseFile(e->name, %s) || !loadBaseFile("config.bin", %s) ||\n'
           '\t\t    !(*pr = loadBaseFile("config_raw.bin", %s)))\n\t\t\t;\n\t\telse {\n') % (F, F, F),
    'got': ('\t\tif (!loadBaseFile(e->name, %s))\n\t\t\tgoto smc;\n\t\tif (!loadBaseFile("config.bin", %s))\n\t\t\tgoto smc;\n'
            '\t\tif ((*pr = loadBaseFile("config_raw.bin", %s))) {\n') % (F, F, F),
}
TAILOLD = '''		{
			uint8_t *d = xb.files[xb.nFlashFiles].data;

			__asm__("" : "+a"(d));
			if (d)
				*pr = extractSmcConfig(e, d, xb.files[xb.nFlashFiles].size);
		}
		break;
	case 2:'''
TAILS = {
    'src': '''		{
			uint8_t *d = xb.files[xb.nFlashFiles].data;

			if (d)
				*pr = extractSmcConfig(e, d, xb.files[xb.nFlashFiles].size);
		}
		break;
	case 2:''',
    'brk': '''		{
			uint8_t *d = xb.files[xb.nFlashFiles].data;

			if (!d)
				break;
			*pr = extractSmcConfig(e, d, xb.files[xb.nFlashFiles].size);
		}
		break;
	case 2:''',
    'pin': TAILOLD,
}


def CASES(base):
    out = []
    for hn, h in HEADS.items():
        for tn, t in TAILS.items():
            def f(b, h=h, t=t, hn=hn):
                b = bdrun.sub(b, HEAD, h)
                tt = t
                if hn == 'got':
                    tt = t.replace('\t\t{\n\t\t\tuint8_t', 'smc:\n\t\t{\n\t\t\tuint8_t', 1)
                return bdrun.sub(b, TAILOLD, tt)
            out.append(('%s %s' % (hn, tn), f))
    return out

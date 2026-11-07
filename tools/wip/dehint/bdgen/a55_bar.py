"""Attempt 55: the barrier (vol_fail) against attempt 49's helper boundaries.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a55_bar.py [-k label]
Rows: each helper written back into loadBlFiles only (console keeps calling it), with exp_t10
back or not, each with and without the barrier."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H
BASE = H.BASE

BAR = H.BAR
T10 = ('\t\t\t\t\t} else if (type == 10) {\n\t\t\t\t\t\tif (suGetCG(&e->data, &e->size))\n\t\t\t\t\t\t\tr = 0;\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t\tif (r)\n\t\t\t\t\tbreak;\n\t\t\t\tif (type == 9 &&',
       '\t\t\t\t\t} else if (__builtin_expect(type == 10, 0)) {\n\t\t\t\t\t\tif (suGetCG(&e->data, &e->size))\n\t\t\t\t\t\t\tr = 0;\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t\tif (r)\n\t\t\t\t\tbreak;\n\t\t\t\tif (type == 9 &&')
XELL = ('\t\t\tcase 25:\n\t\t\t\tr = loadXell(e);\n\t\t\t\tbreak;\n\t\t\tcase 3:\n\t\t\t\tif (!loadBaseFile(e->name, &xb.files',
        '\t\t\tcase 25:\n\t\t\t\tif (xb.type == BUILD_RETAIL || xb.type > BUILD_DEVGL16)\n\t\t\t\t\tbreak;\n'
        '\t\t\t\tif (!loadBaseFile(e->name, e))\n\t\t\t\t\tbreak;\n'
        '\t\t\t\tlog_printf(1, "xell not found in perbuild directory, checking firmware /bin folder\\n");\n'
        '\t\t\t\tif (!loadBinFile(e))\n\t\t\t\t\tbreak;\n'
        '\t\t\t\tlog_printf(1, "xell not found in firmware /bin folder, checking base path\\n");\n'
        '\t\t\t\tr = loadLocalFile(e);\n\t\t\t\tbreak;\n\t\t\tcase 3:\n\t\t\t\tif (!loadBaseFile(e->name, &xb.files')
B24 = ('\t\t\t\tif (xb.type == BUILD_JTAG || xb.glitch2mfg)\n\t\t\t\t\tr = loadBl24(e);\n',
       '\t\t\t\tif (xb.type == BUILD_JTAG || xb.glitch2mfg) {\n\t\t\t\t\tif (loadBaseFile(e->name, e))\n\t\t\t\t\t\tr = defaultBl60(e);\n'
       '\t\t\t\t\telse if (e->size != 0x60)\n\t\t\t\t\t\tr = defaultBl60(e);\n\t\t\t\t}\n')

V = {}
for hx in ('', 'x'):
    for hb in ('', 'b'):
        for ht in ('', 't'):
            for bar in ('', 'nb'):
                ed = []
                if hx: ed.append(XELL)
                if hb: ed.append(B24)
                if ht: ed.append(T10)
                if bar: ed.append(BAR)
                V['h_%s%s%s_%s' % (hx or '-', hb or '-', ht or '-', bar or 'b')] = ed

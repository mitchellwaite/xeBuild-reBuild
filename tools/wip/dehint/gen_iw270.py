# attempt 20: forms of partial at P 50 (if (partial), no `> 0`), x where npages/t go. Base nopt.
# `IWB=build/iw/a20/nopt.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw270.py -n 30 -t 2`
import os
BASE = os.environ.get('IWB', 'build/iw/a20/nopt.c')
H = '''		small = type != 0 && type != '0';
		partial = small && len < 0x4000;
		if (partial > 0) {
'''
F = {
 'ifm':  "small = type != 0 && type != '0';\n\t\tpartial = 0;\n\t\tif (small && len < 0x4000)\n\t\t\tpartial = 1;\n",
 'ifm2': "small = type != 0 && type != '0';\n\t\tif (small && len < 0x4000)\n\t\t\tpartial = 1;\n\t\telse\n\t\t\tpartial = 0;\n",
 'ifn':  "partial = 0;\n\t\tif (type != 0 && type != '0' && len < 0x4000)\n\t\t\tpartial = 1;\n",
 'ifs':  "small = type != 0 && type != '0';\n\t\tpartial = 0;\n\t\tif (small)\n\t\t\tpartial = len < 0x4000;\n",
 'ifl':  "small = type != 0 && type != '0';\n\t\tpartial = 0;\n\t\tif (len < 0x4000)\n\t\t\tpartial = small;\n",
 'ifr':  "small = type != 0 && type != '0';\n\t\tpartial = 1;\n\t\tif (!small || len >= 0x4000)\n\t\t\tpartial = 0;\n",
 'ifa':  "small = type != 0 && type != '0';\n\t\tpartial = small;\n\t\tif (len >= 0x4000)\n\t\t\tpartial = 0;\n",
 'ifb':  "partial = type != 0 && type != '0';\n\t\tif (len >= 0x4000)\n\t\t\tpartial = 0;\n",
 'ifc':  "partial = 0;\n\t\tif (type != 0 && type != '0')\n\t\t\tpartial = len < 0x4000;\n",
 'ifd':  "partial = 0;\n\t\tif (type != 0 && type != '0')\n\t\t\tif (len < 0x4000)\n\t\t\t\tpartial = 1;\n",
 'ife':  "small = 0;\n\t\tif (type != 0 && type != '0')\n\t\t\tsmall = 1;\n\t\tpartial = small && len < 0x4000;\n",
 'iff':  "small = 0;\n\t\tif (type != 0 && type != '0')\n\t\t\tsmall = 1;\n\t\tpartial = 0;\n\t\tif (small && len < 0x4000)\n\t\t\tpartial = 1;\n",
}
A = [(k, [(H, '\t\t' + v + '\t\tif (partial) {\n')]) for k, v in F.items()]
T = [('', []), ('tb', [("\t\tp = 0;\n\t\tt = type - '1';\n", "\t\tt = type - '1';\n\t\tp = 0;\n")]),
     ('tt', [("\t\tp = 0;\n\t\tt = type - '1';\n", "\t\tp = 0;\n"), ('\t\tif (partial) {\n', "\t\tt = type - '1';\n\t\tif (partial) {\n")])]
AXES = [A, T]
def FILTER(c):
    return True

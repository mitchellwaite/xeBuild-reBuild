"""Attempt 61 diagnostic (not natural): the checkBl r test's probability set by an expect at the param,
with exp_pr's expect gone (`(int)r < 0` or `r != 0` in the tail).  Only loadBlFiles counts (the param
moves buildFlash's exp_devgl too).
python tools/wip/dehint/bdgen/a60lib.py tools/wip/dehint/bdgen/a61_diag.py -p 52 -o -"""
CB = ('r = checkBl(e->data, e->size, type, e->crc);\n\t\t\t\tif (r)\n',
      'r = checkBl(e->data, e->size, type, e->crc);\n\t\t\t\tif (__builtin_expect(r != 0, 1))\n')
CB0 = ('r = checkBl(e->data, e->size, type, e->crc);\n\t\t\t\tif (r)\n',
      'r = checkBl(e->data, e->size, type, e->crc);\n\t\t\t\tif (__builtin_expect(r != 0, 0))\n')
NEG = ('if (__builtin_expect(r != 0, 0))\n\t\t\t\t\t\tgoto fail;', 'if ((int)r < 0)\n\t\t\t\t\t\tgoto fail;')
NE = ('if (__builtin_expect(r != 0, 0))\n\t\t\t\t\t\tgoto fail;', 'if (r != 0)\n\t\t\t\t\t\tgoto fail;')
V = {'cb1_neg': [CB, NEG], 'cb1_ne': [CB, NE], 'cb0_neg': [CB0, NEG], 'cb0_ne': [CB0, NE]}
V['neg'] = [NEG]
V['ne'] = [NE]

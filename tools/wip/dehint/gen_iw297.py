# attempt 24, pin_t: the page count's test written as direct branches on small and len instead of a flag, so ifcombine's merged probabilities set the split of t's tests (a product of predictors rather than 73 or 50). Base: src minus the pin.
# `IWB=build/iw/a24/nopt.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw297.py -n 30 -t 4`
H = "		small = type != 0 && type != '0';\n		partial = small && len < 0x4000;\n		if (partial > 0) {\n			if (len % 512)\n				npages = (len + 512) / 512;\n			else\n				npages = len / 512;\n		} else\n			npages = 32;\n"
ARM = "			if (len % 512)\n				npages = (len + 512) / 512;\n			else\n				npages = len / 512;\n"
D = '	int partial;\n	_Bool small;\n'
def f(lab, cond, decl=''):
    return (lab, [(H, '		if (' + cond + ') {\n' + ARM + '		} else\n			npages = 32;\n'), (D, decl)])
def g(lab, cond):
    return (lab, [(H, '		if (' + cond + ')\n			npages = 32;\n		else {\n' + ARM + '		}\n'), (D, '')])
def h(lab, pre, cond, decl):
    return (lab, [(H, pre + '		if (' + cond + ') {\n' + ARM + '		} else\n			npages = 32;\n'), (D, decl)])
LL = [('', []),
 f('a1', "type != 0 && type != '0' && len < 0x4000"),
 f('a2', "len < 0x4000 && type != 0 && type != '0'"),
 f('a3', "type && type != '0' && len < 0x4000"),
 f('a4', "type > 0 && type != '0' && len < 0x4000"),
 f('a5', "type != '0' && type != 0 && len < 0x4000"),
 f('a6', "type != '0' && type > 0 && len < 0x4000"),
 f('a7', "type > 0 && len < 0x4000 && type != '0'"),
 f('a8', "len <= 0x3fff && type > 0 && type != '0'"),
 g('b1', "type == 0 || type == '0' || len >= 0x4000"),
 g('b2', "len >= 0x4000 || type == 0 || type == '0'"),
 g('b3', "len > 0x3fff || !type || type == '0'"),
 h('c1', "		small = type != 0 && type != '0';\n", "small && len < 0x4000", '	_Bool small;\n'),
 h('c2', "		small = type != 0 && type != '0';\n", "len < 0x4000 && small", '	_Bool small;\n'),
 h('c3', "		small = type > 0 && type != '0';\n", "small > 0 && len < 0x4000", '	int small;\n'),
 h('c4', "		small = type != 0 && type != '0';\n", "small > 0 && len < 0x4000", '	int small;\n'),
 h('c5', "		small = len < 0x4000;\n", "small > 0 && type != 0 && type != '0'", '	int small;\n'),
 h('c6', "		small = len < 0x4000;\n", "type != 0 && type != '0' && small > 0", '	int small;\n'),
]
AXES = [LL]

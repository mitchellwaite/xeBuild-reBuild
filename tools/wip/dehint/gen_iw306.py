# attempt 24, pin_t: an over-long table inside partial's arm. No global rescale (the arm's far below 10000); the question is whether unrolling leaves the arm's exit edge off 657 by rounding, so that threading splits t's test on the grid.
# `IWB=build/iw/a24/np.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw306.py -n 40 -t 4`
H = "		if (partial > 0) {\n			if (len % 512)\n				npages = (len + 512) / 512;\n			else\n				npages = len / 512;\n		} else\n"
I = '			'
def f(val, n, pre=''):
    return "		if (partial > 0) {\n" + pre + I + 'uint32_t part[%d] = { %s };\n' % (n, val) + I + 'int k;\n\n' + I + 'npages = 0;\n' + I + 'for (k = 0; k < %d; k++)\n' % n + I + '	npages += part[k];\n		} else\n'
FO = [('', [])]
for n in range(2, 12):
    FO.append(('a%d' % n, [(H, f('len % 512 ? (len + 512) / 512 : len / 512', n))]))
    FO.append(('b%d' % n, [(H, "		if (partial > 0) {\n" + I + 'uint32_t part[%d] = { len / 512, len %% 512 != 0 };\n' % n + I + 'int k;\n\n' + I + 'npages = 0;\n' + I + 'for (k = 0; k < %d; k++)\n' % n + I + '	npages += part[k];\n		} else\n')]))
AXES = [FO]

"""calcBlAreaSize without the size pin: a fileSizeOf helper, order of the build-type chain, scoped x, size as a sum in one expression."""
import itertools
A = '''		x = findFile(5);
		size = findFileOffset(5) + xb.files[x].size;
		x = findFile(7);
		size += xb.files[x].size;
		if (xb.seReplacesCf) {
			x = findFile(14);
			size += xb.files[x].size;
		}
'''
B = '''		x = findFile(11);
		size = findFileOffset(11) + xb.files[x].size;
		x = findFile(12);
		size += xb.files[x].size;
		x = findFile(13);
		size += xb.files[x].size;
		x = findFile(14);
		/* the sum so far in ebx (esi up to the 13 lookup), as in the
		   original: IRA otherwise keeps it in esi */
		__asm__("" : "+b"(size));
		size += xb.files[x].size;
		setPatchSlot(size);
		size += 2 * imgCfSize();
'''
C = '''		size = findFileOffset(5) + findFileSize(5);
		size += findFileSize(6);
		size += findFileSize(7);
		size += findFileSize(8);
		if (xb.type != BUILD_RETAIL) {
			x = findFile(25);
			if (xb.files[x].offset > size) {
				xs = xb.files[x].size;
				if (xs > 0x40000)
					log_printf(0, "***** WARNING: xell is unexpectedly larger than 256KiB!!\\n");
				else
					xs = 0x40000;
				size = xb.files[x].offset + xs;
			}
		}
		size = (size + 0xffff) & ~0xffff;
		setPatchSlot(size);
		size += 2 * imgCfSize();
'''
OLD = '	if (xb.type == BUILD_JTAG) {\n' + A + '	} else if (xb.type > BUILD_DEVGL16) {\n' + B + '	} else {\n' + C + '	}\n'
HELP = 'static uint32_t blFileSize(int type)\n{\n	return xb.files[findFile(type)].size;\n}\n\n'
HEAD = 'uint32_t calcBlAreaSize(void)\n'
B0 = B.replace('''		/* the sum so far in ebx (esi up to the 13 lookup), as in the
		   original: IRA otherwise keeps it in esi */
		__asm__("" : "+b"(size));
''', '')
BH = {
    'plain': B0,
    'helper': '		size = findFileOffset(11) + blFileSize(11);\n		size += blFileSize(12);\n		size += blFileSize(13);\n		size += blFileSize(14);\n		setPatchSlot(size);\n		size += 2 * imgCfSize();\n',
    'sum': '		size = findFileOffset(11) + blFileSize(11) + blFileSize(12) + blFileSize(13) + blFileSize(14);\n		setPatchSlot(size);\n		size += 2 * imgCfSize();\n',
    'idx': '		size = findFileOffset(11) + xb.files[findFile(11)].size;\n		size += xb.files[findFile(12)].size;\n		size += xb.files[findFile(13)].size;\n		size += xb.files[findFile(14)].size;\n		setPatchSlot(size);\n		size += 2 * imgCfSize();\n',
    'ptr': '		e = &xb.files[findFile(11)];\n		size = findFileOffset(11) + e->size;\n		e = &xb.files[findFile(12)];\n		size += e->size;\n		e = &xb.files[findFile(13)];\n		size += e->size;\n		e = &xb.files[findFile(14)];\n		size += e->size;\n		setPatchSlot(size);\n		size += 2 * imgCfSize();\n',
    'two': B0.replace('		x = findFile(14);\n		size += xb.files[x].size;\n		setPatchSlot(size);\n		size += 2 * imgCfSize();\n', '		x = findFile(14);\n		xs = size + xb.files[x].size;\n		setPatchSlot(xs);\n		size = xs + 2 * imgCfSize();\n'),
}
AH = {
    'plain': A,
    'helper': '		size = findFileOffset(5) + blFileSize(5);\n		size += blFileSize(7);\n		if (xb.seReplacesCf)\n			size += blFileSize(14);\n',
}
ORD = {
    'orig': '	if (xb.type == BUILD_JTAG) {\n%s	} else if (xb.type > BUILD_DEVGL16) {\n%s	} else {\n%s	}\n',
    'nest': '	if (xb.type == BUILD_JTAG) {\n%s	} else {\n		if (xb.type > BUILD_DEVGL16) {\n%s		} else {\n%s		}\n	}\n',
    'dev1': None,
    'le': '	if (xb.type == BUILD_JTAG) {\n%s	} else if (xb.type <= BUILD_DEVGL16) {\n%s	} else {\n%s	}\n',
    'ne': None,
}


def CASES(base):
    out = []
    for bk, ak, od, sc in itertools.product(BH, AH, ('orig', 'nest', 'dev1', 'le', 'ne'), (0, 1)):
        a, b, c = AH[ak], BH[bk], C
        if od in ('orig', 'nest'):
            new = ORD[od] % (a, b, c)
        elif od == 'le':
            new = ORD[od] % (a, c, b)
        elif od == 'dev1':
            new = '	if (xb.type > BUILD_DEVGL16) {\n%s	} else if (xb.type == BUILD_JTAG) {\n%s	} else {\n%s	}\n' % (b, a, c)
        else:
            new = '	if (xb.type != BUILD_JTAG) {\n		if (xb.type > BUILD_DEVGL16) {\n%s		} else {\n%s		}\n	} else {\n%s	}\n' % (b, c, a)
        t = base.replace(OLD, new)
        if t == base:
            raise ValueError('old')
        pre = HELP if 'blFileSize' in new else ''
        head = HEAD
        if 'e = &xb' in new:
            t = t.replace('uint32_t calcBlAreaSize(void)\n{\n	uint32_t size, xs, x;\n', 'uint32_t calcBlAreaSize(void)\n{\n	uint32_t size, xs, x;\n	struct fileent *e;\n')
        if sc:
            t = t.replace('uint32_t calcBlAreaSize(void)\n{\n	uint32_t size, xs, x;\n', 'uint32_t calcBlAreaSize(void)\n{\n	uint32_t x, xs, size;\n')
        t = t.replace(HEAD, pre + HEAD)
        out.append(('%s %s %s d%d' % (bk, ak, od, sc), t))
    return out

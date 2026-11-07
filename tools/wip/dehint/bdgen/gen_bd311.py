"""Attempt 20, pin_size through the other arms: PRE takes the kit arm's names from the free list (prephitmp_229 <
size_254, so fold puts the load first and IRA ties the sum to it).  The top of the free list at PRE is what reassoc1 and
dce freed of dom2's retail-arm copies (size_243, 237, 229, ...).  So the retail (and JTAG) arm's form decides the kit
arm's names.  Axes: retail arm forms, JTAG arm forms, kit x as uint32_t or int; pin off.  Runs on src as of a0108d6d."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun

FN = 'uint32_t calcBlAreaSize(void)\n'

R_HEAD = {
    'src': '''		size = findFileOffset(5) + findFileSize(5);
		size += findFileSize(6);
		size += findFileSize(7);
		size += findFileSize(8);
''',
    'expr': '''		size = findFileOffset(5) + findFileSize(5) + findFileSize(6) + findFileSize(7) + findFileSize(8);
''',
    'off': '''		size = findFileOffset(5);
		size += findFileSize(5);
		size += findFileSize(6);
		size += findFileSize(7);
		size += findFileSize(8);
''',
    'loop': '''		size = findFileOffset(5);
		for (t = 5; t <= 8; t++)
			size += findFileSize(t);
''',
}
R_XELL = {
    'src': '''		if (xb.type != BUILD_RETAIL) {
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
''',
    'xs0': '''		if (xb.type != BUILD_RETAIL) {
			x = findFile(25);
			if (xb.files[x].offset > size) {
				xs = 0x40000;
				if (xb.files[x].size > xs) {
					log_printf(0, "***** WARNING: xell is unexpectedly larger than 256KiB!!\\n");
					xs = xb.files[x].size;
				}
				size = xb.files[x].offset + xs;
			}
		}
''',
    'ptr': '''		if (xb.type != BUILD_RETAIL) {
			e = &xb.files[findFile(25)];
			if (e->offset > size) {
				xs = e->size;
				if (xs > 0x40000)
					log_printf(0, "***** WARNING: xell is unexpectedly larger than 256KiB!!\\n");
				else
					xs = 0x40000;
				size = e->offset + xs;
			}
		}
''',
    'arms': '''		if (xb.type != BUILD_RETAIL) {
			x = findFile(25);
			if (xb.files[x].offset > size) {
				if (xb.files[x].size > 0x40000) {
					log_printf(0, "***** WARNING: xell is unexpectedly larger than 256KiB!!\\n");
					size = xb.files[x].offset + xb.files[x].size;
				} else
					size = xb.files[x].offset + 0x40000;
			}
		}
''',
    'off': '''		if (xb.type != BUILD_RETAIL) {
			x = findFile(25);
			xo = xb.files[x].offset;
			if (xo > size) {
				xs = xb.files[x].size;
				if (xs > 0x40000)
					log_printf(0, "***** WARNING: xell is unexpectedly larger than 256KiB!!\\n");
				else
					xs = 0x40000;
				size = xo + xs;
			}
		}
''',
}
R_TAIL = '''		size = (size + 0xffff) & ~0xffff;
		setPatchSlot(size);
		size += 2 * imgCfSize();
'''

JT = {
    'src': '''		x = findFile(5);
		size = findFileOffset(5) + xb.files[x].size;
		x = findFile(7);
		size += xb.files[x].size;
		if (xb.seReplacesCf) {
			x = findFile(14);
			size += xb.files[x].size;
		}
''',
    'idx': '''		x = findFile(5);
		size = findFileOffset(5) + xb.files[x].size;
		size += xb.files[findFile(7)].size;
		if (xb.seReplacesCf)
			size += xb.files[findFile(14)].size;
''',
}

KIT = '''		x = findFile(11);
		size = findFileOffset(11) + xb.files[x].size;
		x = findFile(12);
		size += xb.files[x].size;
		x = findFile(13);
		size += xb.files[x].size;
		x = findFile(14);
		size += xb.files[x].size;
		setPatchSlot(size);
		size += 2 * imgCfSize();
'''

ROUND = '''	if (size & 0x3fff)
		size = (size + 0x3fff) & ~0x3fff;
	return size;
'''


def mk(b, rh, rx, jk, xt):
    i, j = bdrun.fnspan(b, FN)
    retail = R_HEAD[rh] + R_XELL[rx] + R_TAIL
    d = '\tuint32_t size, xs;\n\t%s x;\n' % xt
    if 'xo' in retail:
        d += '\tuint32_t xo;\n'
    if 't = ' in retail:
        d += '\tint t;\n'
    if 'e = ' in retail:
        d += '\tstruct fileent *e;\n'
    body = ('\tif (xb.type == BUILD_JTAG) {\n' + JT[jk] + '\t} else if (xb.type > BUILD_DEVGL16) {\n' + KIT +
            '\t} else {\n' + retail + '\t}\n' + ROUND)
    f = FN + '{\n' + d + '\n' + body + '}\n'
    return b[:i] + f + b[j:]


def CASES(base):
    out = []
    for c in itertools.product(R_HEAD, R_XELL, JT, ['uint32_t', 'int']):
        out.append(('%s %s %s %s' % c, lambda b, c=c: mk(b, *c)))
    return out


FOCUS = ['_calcBlAreaSize']

"""Attempt 20, pin_size: whole-function forms of calcBlAreaSize, pin off.  Earlier sweeps (gen_bd105, 110, 176, 283)
varied spellings, helpers, types and scopes of the src statements; this one changes the function's form: the kit (and
JTAG) lookups as a loop over types or over a table, index locals per bootloader with one sum at the end, size locals
summed at the end, the sum as one expression, and each arm returning on its own.  The reference runs the lookups in
the order findFile(11), findFileOffset(11), findFile(12), (13), (14), so every form keeps that order of the loops.
Runs on src as of a0108d6d."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun

FN = 'uint32_t calcBlAreaSize(void)\n'

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

KIT = {
    'src': '''		x = findFile(11);
		size = findFileOffset(11) + xb.files[x].size;
		x = findFile(12);
		size += xb.files[x].size;
		x = findFile(13);
		size += xb.files[x].size;
		x = findFile(14);
		size += xb.files[x].size;
''',
    'loop12': '''		x = findFile(11);
		size = findFileOffset(11) + xb.files[x].size;
		for (t = 12; t <= 14; t++) {
			x = findFile(t);
			size += xb.files[x].size;
		}
''',
    'loop12b': '''		x = findFile(11);
		size = findFileOffset(11) + xb.files[x].size;
		for (t = 12; t <= 14; t++)
			size += xb.files[findFile(t)].size;
''',
    'loop12lt': '''		x = findFile(11);
		size = findFileOffset(11) + xb.files[x].size;
		for (t = 12; t < 15; t++)
			size += xb.files[findFile(t)].size;
''',
    'table': '''		x = findFile(11);
		size = findFileOffset(11) + xb.files[x].size;
		for (t = 0; t < 3; t++)
			size += xb.files[findFile(kitBls[t])].size;
''',
    'idxsum': '''		cb = findFile(11);
		size = findFileOffset(11);
		cd = findFile(12);
		ce = findFile(13);
		cf = findFile(14);
		size += xb.files[cb].size + xb.files[cd].size + xb.files[ce].size + xb.files[cf].size;
''',
    'idxsum2': '''		cb = findFile(11);
		size = findFileOffset(11);
		cd = findFile(12);
		ce = findFile(13);
		cf = findFile(14);
		size = size + xb.files[cb].size + xb.files[cd].size + xb.files[ce].size + xb.files[cf].size;
''',
    'idxsum3': '''		cb = findFile(11);
		size = findFileOffset(11) + xb.files[cb].size;
		cd = findFile(12);
		ce = findFile(13);
		cf = findFile(14);
		size += xb.files[cd].size + xb.files[ce].size + xb.files[cf].size;
''',
    'idxrun': '''		cb = findFile(11);
		size = findFileOffset(11) + xb.files[cb].size;
		cd = findFile(12);
		size += xb.files[cd].size;
		ce = findFile(13);
		size += xb.files[ce].size;
		cf = findFile(14);
		size += xb.files[cf].size;
''',
    'szsum': '''		cb = xb.files[findFile(11)].size;
		size = findFileOffset(11);
		cd = xb.files[findFile(12)].size;
		ce = xb.files[findFile(13)].size;
		cf = xb.files[findFile(14)].size;
		size += cb + cd + ce + cf;
''',
    'szsum2': '''		cb = xb.files[findFile(11)].size;
		size = findFileOffset(11) + cb;
		cd = xb.files[findFile(12)].size;
		ce = xb.files[findFile(13)].size;
		cf = xb.files[findFile(14)].size;
		size += cd + ce + cf;
''',
    'expr': '''		size = xb.files[findFile(11)].size + findFileOffset(11) + xb.files[findFile(12)].size
			+ xb.files[findFile(13)].size + xb.files[findFile(14)].size;
''',
}

TAIL = {
    'src': '''		setPatchSlot(size);
		size += 2 * imgCfSize();
''',
    'ret': None,  # handled in mk: each arm rounds and returns
}

RETAIL = '''		size = findFileOffset(5) + findFileSize(5);
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

ROUND = '''	if (size & 0x3fff)
		size = (size + 0x3fff) & ~0x3fff;
	return size;
'''


def mk(b, jk, kk, struct, decl):
    i, j = bdrun.fnspan(b, FN)
    kit = KIT[kk] + TAIL['src']
    jt = JT[jk]
    vs = ['size', 'xs', 'x']
    if 'cb' in kit:
        vs += ['cb', 'cd', 'ce', 'cf']
    if 't = ' in kit:
        vs.append('t')
    if decl == 'int':
        d = '\tuint32_t %s;\n' % ', '.join(v for v in vs if v not in ('x', 'cb', 'cd', 'ce', 'cf', 't') or 'cb =' in kit and 'xb.files[findFile(11)]' in kit and v in ('cb', 'cd', 'ce', 'cf'))
        iv = [v for v in vs if v in ('x', 't') or (v in ('cb', 'cd', 'ce', 'cf') and 'xb.files[findFile(11)]' not in kit)]
        d += '\tint %s;\n' % ', '.join(iv)
    else:
        d = '\tuint32_t %s;\n' % ', '.join(vs)
    if struct == 'chain':
        body = ('\tif (xb.type == BUILD_JTAG) {\n' + jt + '\t} else if (xb.type > BUILD_DEVGL16) {\n' + kit +
                '\t} else {\n' + RETAIL + '\t}\n' + ROUND)
    elif struct == 'ret':
        r = '\t\treturn alignBlArea(size);\n'
        body = ('\tif (xb.type == BUILD_JTAG) {\n' + jt + r + '\t}\n\tif (xb.type > BUILD_DEVGL16) {\n' + kit + r +
                '\t}\n' + RETAIL.replace('\t\t', '\t', -1) + '\treturn alignBlArea(size);\n')
    elif struct == 'retin':
        r = '\t\treturn size & 0x3fff ? (size + 0x3fff) & ~0x3fff : size;\n'
        body = ('\tif (xb.type == BUILD_JTAG) {\n' + jt + '\t} else if (xb.type > BUILD_DEVGL16) {\n' + kit +
                '\t} else {\n' + RETAIL + '\t}\n' + '\treturn size & 0x3fff ? (size + 0x3fff) & ~0x3fff : size;\n')
    f = FN + '{\n' + d + '\n' + body + '}\n'
    pre = ''
    if struct == 'ret':
        pre = 'static uint32_t alignBlArea(uint32_t size)\n{\n\tif (size & 0x3fff)\n\t\tsize = (size + 0x3fff) & ~0x3fff;\n\treturn size;\n}\n\n'
    if 'kitBls' in kit:
        pre = 'static const int kitBls[] = { 12, 13, 14 };\n\n' + pre
    return b[:i] + pre + f + b[j:]


def CASES(base):
    out = []
    for c in itertools.product(JT, KIT, ['chain', 'ret', 'retin'], ['u32', 'int']):
        out.append(('%s %s %s %s' % c, lambda b, c=c: mk(b, *c)))
    return out


FOCUS = ['_calcBlAreaSize']

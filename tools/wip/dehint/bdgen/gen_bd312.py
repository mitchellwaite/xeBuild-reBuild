"""Attempt 20, pin_size: bigger structural moves.  (a) The setPatchSlot / imgCfSize tail shared by the kit and retail arms
(one call in the source; the reference has two copies, so this only works if gcc duplicates it); (b) each arm's sum as a
static helper called once (inlined at IPA, so its SSA names are made in its own body); (c) the kit arm's sum in a second
variable.  Pin off.  Runs on src as of a0108d6d."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun

FN = 'uint32_t calcBlAreaSize(void)\n'

JT = '''	x = findFile(5);
	size = findFileOffset(5) + xb.files[x].size;
	x = findFile(7);
	size += xb.files[x].size;
	if (xb.seReplacesCf) {
		x = findFile(14);
		size += xb.files[x].size;
	}
'''
KIT = '''	x = findFile(11);
	size = findFileOffset(11) + xb.files[x].size;
	x = findFile(12);
	size += xb.files[x].size;
	x = findFile(13);
	size += xb.files[x].size;
	x = findFile(14);
	size += xb.files[x].size;
'''
RET = '''	size = findFileOffset(5) + findFileSize(5);
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
'''
SLOT = '''	setPatchSlot(size);
	size += 2 * imgCfSize();
'''
ROUND = '''	if (size & 0x3fff)
		size = (size + 0x3fff) & ~0x3fff;
	return size;
'''


def ind(s, n=1):
    return '\n'.join(('\t' * n + l if l.strip() else l) for l in s.split('\n'))


def helper(name, body, decl):
    return 'static uint32_t %s(void)\n{\n%s\n%s\treturn size;\n}\n\n' % (name, decl, body)


def mk(b, shared, hj, hk, hr):
    i, j = bdrun.fnspan(b, FN)
    pre = ''
    if hj:
        pre += helper('jtagBlSize', JT, '\tuint32_t size, x;\n')
        jt = '\t\tsize = jtagBlSize();\n'
    else:
        jt = ind(JT)
    if hk:
        pre += helper('kitBlSize', KIT, '\tuint32_t size, x;\n')
        kit = '\t\tsize = kitBlSize();\n'
    else:
        kit = ind(KIT)
    if hr:
        pre += helper('retailBlSize', RET, '\tuint32_t size, xs, x;\n')
        ret = '\t\tsize = retailBlSize();\n'
    else:
        ret = ind(RET)
    d = '\tuint32_t size, xs, x;\n'
    if shared:
        body = ('\tif (xb.type == BUILD_JTAG) {\n' + jt + '\t} else {\n\t\tif (xb.type > BUILD_DEVGL16) {\n' + ind(kit) +
                '\t\t} else {\n' + ind(ret) + '\t\t}\n' + ind(SLOT) + '\t}\n' + ROUND)
    else:
        body = ('\tif (xb.type == BUILD_JTAG) {\n' + jt + '\t} else if (xb.type > BUILD_DEVGL16) {\n' + kit + ind(SLOT) +
                '\t} else {\n' + ret + ind(SLOT) + '\t}\n' + ROUND)
    f = FN + '{\n' + d + '\n' + body + '}\n'
    return b[:i] + pre + f + b[j:]


def CASES(base):
    out = []
    for c in itertools.product([0, 1], [0, 1], [0, 1], [0, 1]):
        out.append(('shared%d hj%d hk%d hr%d' % c, lambda b, c=c: mk(b, *c)))
    return out


FOCUS = ['_calcBlAreaSize']

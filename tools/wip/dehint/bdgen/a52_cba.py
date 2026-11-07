"""Attempt 52: calcBlAreaSize (pin_size) through helpers it could share.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a52_cba.py
Rows: <helper>_<pin on 'P' / off 'n'>."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H
BASE = H.BASE
HEAD = 'uint32_t calcBlAreaSize(void)\n{\n'
TAILK = '''		size += xb.files[x].size;
		setPatchSlot(size);
		size += 2 * imgCfSize();
	} else {'''
TAILR = '''		size = (size + 0xffff) & ~0xffff;
		setPatchSlot(size);
		size += 2 * imgCfSize();
	}'''
HELP = {}
SUBS = {}
# A: the patch slot and the CF/CG area after the bootloaders
HELP['slot'] = '''/* the patch slot goes after the bootloaders, then room for the CF and CG */
static uint32_t addCfArea(uint32_t size)
{
	setPatchSlot(size);
	return size + 2 * imgCfSize();
}

'''
SUBS['slot'] = [(TAILK, '''		size += xb.files[x].size;
		size = addCfArea(size);
	} else {'''), (TAILR, '''		size = (size + 0xffff) & ~0xffff;
		size = addCfArea(size);
	}''')]
# A2: the same, written as a statement returning in place
SUBS['slot2'] = [(TAILK, '''		size = addCfArea(size + xb.files[x].size);
	} else {'''), (TAILR, '''		size = addCfArea((size + 0xffff) & ~0xffff);
	}''')]
HELP['slot2'] = HELP['slot']
# A3: retail's 64K round inside (kit passes its own)
HELP['slot3'] = '''static uint32_t addCfArea(uint32_t size)
{
	setPatchSlot(size);
	size += 2 * imgCfSize();
	return size;
}

'''
SUBS['slot3'] = SUBS['slot']
# B: whole tail incl. 16K rounding, and jtag too
HELP['tail'] = '''static uint32_t blAreaEnd(uint32_t size)
{
	setPatchSlot(size);
	size += 2 * imgCfSize();
	if (size & 0x3fff)
		size = (size + 0x3fff) & ~0x3fff;
	return size;
}

'''
SUBS['tail'] = [(TAILK, '''		size += xb.files[x].size;
		return blAreaEnd(size);
	} else {'''), (TAILR, '''		size = (size + 0xffff) & ~0xffff;
		return blAreaEnd(size);
	}''')]
# C: files[findFile(t)].size helper for jtag and kit
HELP['fsz'] = '''static uint32_t blSize(int type)
{
	return xb.files[findFile(type)].size;
}

'''
def fsz(t):
    old = t[t.index(HEAD):]
    old = old[:old.index('\n}\n') + 3]
    new = old
    for a, b in [
        ('''		x = findFile(5);
		size = findFileOffset(5) + xb.files[x].size;
		x = findFile(7);
		size += xb.files[x].size;
		if (xb.seReplacesCf) {
			x = findFile(14);
			size += xb.files[x].size;
		}''', '''		size = findFileOffset(5) + blSize(5);
		size += blSize(7);
		if (xb.seReplacesCf)
			size += blSize(14);'''),
        ('''		x = findFile(11);
		size = findFileOffset(11) + xb.files[x].size;
		x = findFile(12);
		size += xb.files[x].size;
		x = findFile(13);
		size += xb.files[x].size;
		x = findFile(14);''', '''		size = findFileOffset(11) + blSize(11);
		size += blSize(12);
		size += blSize(13);'''),
        ('		size += xb.files[x].size;\n		setPatchSlot', '		size += blSize(14);\n		setPatchSlot')]:
        if a not in new:
            raise ValueError(a[:40])
        new = new.replace(a, b, 1)
    return t.replace(old, new)

def mk(h, pin):
    def f(t):
        if not pin:
            t = t.replace(H.PIN[0], '', 1)
        if h == 'fsz':
            if pin:
                raise ValueError('fsz with pin')
            t = fsz(t)
        else:
            for a, b in SUBS[h]:
                if a not in t:
                    raise ValueError(h + ': ' + a[:30])
                t = t.replace(a, b, 1)
        return t.replace(HEAD, HELP[h] + HEAD, 1)
    return f
V = {}
for h in HELP:
    for pin in (1, 0):
        V['%s_%s' % (h, 'P' if pin else 'n')] = mk(h, pin)

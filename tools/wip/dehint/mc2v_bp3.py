# clientBinPatch without the hints: patchNand's loop statement orders (inlined copy's RA)
import itertools, os, runpy
V0 = runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mc2v_bp.py'))['V']
B = V0['none']
L2 = ['len -= 512;', 'data += 512;', 'spare += 528;', 'buf += 528;']
OLD2 = '''		calcPageEcc(buf, spare);
		len -= 512;
		data += 512;
		spare += 528;
		buf += 528;
	}'''
L1 = ['len -= 512 - off;', 'calcPageEcc(buf, spare);', 'data += 512 - off;', 'buf += 528;', 'spare += 528;']
OLD1 = '''		memcpy(buf + off, data, 512 - off);
		len -= 512 - off;
		calcPageEcc(buf, spare);
		data += 512 - off;
		buf += 528;
		spare += 528;
	}'''
L0 = ['buf += 528;', 'spare += 528;', 'off -= 512;']
OLD0 = '''		buf += 528;
		spare += 528;
		off -= 512;
	}'''
V = {}
for p in itertools.permutations(L2):
    if list(p) == L2:
        continue
    V['l2_' + ''.join(s[0] for s in p)] = B + [(OLD2, '		calcPageEcc(buf, spare);\n' + ''.join('\t\t%s\n' % s for s in p) + '\t}')]
for p in itertools.permutations(L1):
    if list(p) == L1 or p.index('data += 512 - off;') < 0:
        continue
    V['l1_' + ''.join(s[0] + s[-4] for s in p)] = B + [(OLD1, '		memcpy(buf + off, data, 512 - off);\n' + ''.join('\t\t%s\n' % s for s in p) + '\t}')]
for p in itertools.permutations(L0):
    if list(p) == L0:
        continue
    V['l0_' + ''.join(s[0] for s in p)] = B + [(OLD0, ''.join('\t\t%s\n' % s for s in p) + '\t}')]

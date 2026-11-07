"""Attempt 50: more code both loaders share, as static helpers (on src after attempt 49).
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a50_share.py [-p 95,99]
Helpers (A50_SET picks the combinations, default every subset):
  su    loadUpdateBl(e, type): loadInputFile + the CF/CG system-update fallback (both loaders' 5..21 arm)
  p23   loadPatchFile(e): case 23's loadBinFile, size check (log, -1) and appendAddonPatches
  nand  useNandData(e, f): free e->data, take f's data and size, clear f (cases 2, 3, 4 of both loaders)
  slot  takeSlot(e): the same from xb.files[xb.nFlashFiles] (loadBlFiles' cases 2, 3, 4)
Each combination is crossed with the hints off one at a time (A50_OFF, default all,pr,bar,lab,none)."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H

BASE = H.BASE
LAB = ('\t\t\t\tdevgl: __attribute__((hot));\n', '')
ANCHOR = '/* load the input files by their type; the arms only set r, which is\n'

SU_FN = '''/* a 5..21 bootloader from its file, or a CF/CG from the system update */
static uint32_t loadUpdateBl(struct fileent *e, int type)
{
	uint32_t r = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);

	if (r) {
		if (type == 9) {
			if (suGetCF(&e->data, &e->size))
				r = 0;
		} else if (type == 10) {
			if (suGetCG(&e->data, &e->size))
				r = 0;
		}
	}
	return r;
}

'''
SU_OLD = '''				r = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);
				if (r) {
					if (type == 9) {
						if (suGetCF(&e->data, &e->size))
							r = 0;
					} else if (type == 10) {
						if (suGetCG(&e->data, &e->size))
							r = 0;
					}
				}
'''
SU_NEW = '\t\t\t\tr = loadUpdateBl(e, type);\n'

P23_FN = '''/* the addon patches: a multiple of 4 bytes */
static int loadPatchFile(struct fileent *e)
{
	int r = loadBinFile(e);

	if (r)
		return r;
	if (e->size & 3) {
		log_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);
		return -1;
	}
	appendAddonPatches(e);
	return 0;
}

'''
P23_OLD_B = '''				r = loadBinFile(e);
				if (r)
					break;
				if (e->size & 3) {
					log_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);
					goto fail;
				}
				appendAddonPatches(e);
				break;
'''
P23_OLD_C = '''				r = loadBinFile(e);
				if (r)
					break;
				if (e->size & 3) {
					log_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);
					r = -1;
					break;
				}
				appendAddonPatches(e);
				break;
'''
P23_NEW = '\t\t\t\tr = loadPatchFile(e);\n\t\t\t\tbreak;\n'

NAND_FN = '''/* take a file's data (from the nand dump or the console) in place of e's */
static void useNandData(struct fileent *e, struct netfile *f)
{
	if (e->data)
		free(e->data);
	e->data = f->data;
	e->size = f->size;
	f->data = NULL;
	f->size = 0;
}

'''
SLOT_FN = '''/* take the data loaded into the spare slot in place of e's */
static void takeSlot(struct fileent *e)
{
	if (e->data)
		free(e->data);
	e->data = xb.files[xb.nFlashFiles].data;
	e->size = xb.files[xb.nFlashFiles].size;
	xb.files[xb.nFlashFiles].data = NULL;
	xb.files[xb.nFlashFiles].size = 0;
}

'''


def nand_old(ind, f):
    t = '\t' * ind
    return (t + 'if (e->data)\n' + t + '\tfree(e->data);\n' + t + 'e->data = xb.%s.data;\n' % f + t +
            'e->size = xb.%s.size;\n' % f + t + 'xb.%s.data = NULL;\n' % f + t + 'xb.%s.size = 0;\n' % f)


def slot_old(ind):
    t = '\t' * ind
    return (t + 'if (e->data)\n' + t + '\tfree(e->data);\n' + t + 'e->data = xb.files[xb.nFlashFiles].data;\n' + t +
            'e->size = xb.files[xb.nFlashFiles].size;\n' + t + 'xb.files[xb.nFlashFiles].data = NULL;\n' + t +
            'xb.files[xb.nFlashFiles].size = 0;\n')


def sub(t, a, b, n=1):
    assert t.count(a) >= n, a[:80]
    return t.replace(a, b, n)


def split(t):
    i = t.index('int loadBlFiles(void)\n')
    j = t.index('int loadConsoleBlFiles(void)\n')
    k = t.index('\n}\n', j) + 3
    return t[:i], t[i:j], t[j:k], t[k:]


def mk(hs, su_fn=SU_FN, p23_fn=P23_FN):
    def f(t):
        fns = ''
        pre, lb, lc, post = split(t)
        if 'su' in hs:
            fns += su_fn
            lb = sub(lb, SU_OLD, SU_NEW)
            lc = sub(lc, SU_OLD, SU_NEW)
        if 'p23' in hs:
            fns += p23_fn
            lb = sub(lb, P23_OLD_B, P23_NEW)
            lc = sub(lc, P23_OLD_C, P23_NEW)
        if 'nand' in hs:
            fns += NAND_FN
            for fld in ('kv', 'kvAlt', 'smc'):
                lb = sub(lb, nand_old(5, fld), '\t\t\t\t\tuseNandData(e, &xb.%s);\n' % fld)
                lc = sub(lc, nand_old(5, fld), '\t\t\t\t\tuseNandData(e, &xb.%s);\n' % fld)
        if 'slot' in hs:
            fns += SLOT_FN
            lb = sub(lb, slot_old(5), '\t\t\t\t\ttakeSlot(e);\n', 3)
        pre = sub(pre, ANCHOR, fns + ANCHOR)
        return pre + lb + lc + post
    return f


OFF = {'all': [], 'pr': [H.PR], 'bar': [H.BAR], 'lab': [LAB], 'none': [H.NONE, H.NONE2], 'dev': [H.DEV]}
HS = ('su', 'p23', 'nand', 'slot')
sets = os.environ.get('A50_SET')
if sets:
    combos = [tuple(s.split('+')) if s != '-' else () for s in sets.split(',')]
else:
    combos = [c for n in range(len(HS) + 1) for c in itertools.combinations(HS, n)]
offs = os.environ.get('A50_OFF', 'all,pr,bar,lab,none').split(',')
V = {}
for c in combos:
    for k in offs:
        def g(t, c=c, p=OFF[k]):
            t = mk(c)(t)
            for a, b in p:
                t = sub(t, a, b)
            return t
        V[('+'.join(c) or 'src') + '_' + k] = g

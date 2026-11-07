"""Attempt 33: the author's nested ifs (memory: author-nested-ifs) in place of `&&` / `||` in loadBl and the loops, one
rewrite at a time, crossed with every loadBl-side hint off alone (and lab_none / pin_d).  Rewrites:
  se1    SE test: if (type == 9) { if (e->data[0] == 'S' && e->data[1] == 'E') {..} }
  se2    SE test fully nested (three ifs)
  c25    case 25's `RETAIL || > DEVGL16` break as two ifs
  c27n   case 27's && chain as nested ifs (attempt 4's gen_bd113 nested them only for pin_d)
  skip   loadBlFiles' `strnicmp || crc` as `if (!strnicmp(..) && !e->crc) continue;`
  skipn  the same with nested ifs: if (!strnicmp(..)) { if (!e->crc) continue; }
  cskip  the console loop the same way (`continue`, r = 0 kept above)
  sig2   the 5/17/11 test as two ifs joined by the signature block as a goto-free switch: switch (type) { case 5: case 11: case 17: .. }
Runs on src as of 5a0bc459."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdhints, bdrun

FOCUS = ['_loadBlFiles', '_loadConsoleBlFiles']

SE_OLD = '''		if (type == 9 && e->data[0] == 'S' && e->data[1] == 'E') {
			/* an SE where the CF goes */
			e->type = type = 14;
			xb.cfLdv = 0;
			xb.seReplacesCf = 1;
		}
'''
SE1 = '''		if (type == 9) {
			if (e->data[0] == 'S' && e->data[1] == 'E') {
				/* an SE where the CF goes */
				e->type = type = 14;
				xb.cfLdv = 0;
				xb.seReplacesCf = 1;
			}
		}
'''
SE2 = '''		if (type == 9) {
			if (e->data[0] == 'S') {
				if (e->data[1] == 'E') {
					/* an SE where the CF goes */
					e->type = type = 14;
					xb.cfLdv = 0;
					xb.seReplacesCf = 1;
				}
			}
		}
'''
C25_OLD = '''		if (xb.type == BUILD_RETAIL || xb.type > BUILD_DEVGL16)
			break;
		if (!loadBaseFile(e->name, e))
			break;
		log_printf(1, "xell not found in perbuild directory, checking firmware /bin folder\\n");
		if (!loadBinFile(e))
			break;
		log_printf(1, "xell not found in firmware /bin folder, checking base path\\n");
		*pr = loadLocalFile(e);'''
C25 = C25_OLD.replace('''		if (xb.type == BUILD_RETAIL || xb.type > BUILD_DEVGL16)
			break;
''', '''		if (xb.type == BUILD_RETAIL)
			break;
		if (xb.type > BUILD_DEVGL16)
			break;
''')
C27_OLD = '''		if (loadBaseFile(e->name, &xb.files[xb.nFlashFiles]) &&
		    loadBaseFile("config.bin", &xb.files[xb.nFlashFiles]) &&
		    (*pr = loadBaseFile("config_raw.bin", &xb.files[xb.nFlashFiles]))) {
			if (!xb.smcConfig.data)
				break;'''
C27N = '''		if (loadBaseFile(e->name, &xb.files[xb.nFlashFiles]))
		    if (loadBaseFile("config.bin", &xb.files[xb.nFlashFiles]))
		    if ((*pr = loadBaseFile("config_raw.bin", &xb.files[xb.nFlashFiles]))) {
			if (!xb.smcConfig.data)
				break;'''
SKIP_OLD = '''		r = 0;
		if (strnicmp(e->name, "none", 4) || e->crc)
			loadBl(e, i, &r);
		if (r) {'''
SKIP = '''		r = 0;
		if (!strnicmp(e->name, "none", 4) && !e->crc)
			continue;
		loadBl(e, i, &r);
		if (r) {'''
SKIPN = '''		r = 0;
		if (!strnicmp(e->name, "none", 4)) {
			if (!e->crc)
				continue;
		}
		loadBl(e, i, &r);
		if (r) {'''
SIG_OLD = '''		if (type == 5 || type == 17 || type == 11) {
			if (xb.pub1bl) {'''


def edit(k):
    def f(t):
        if k == 'src':
            return t
        if k == 'se1':
            return bdrun.sub(t, SE_OLD, SE1)
        if k == 'se2':
            return bdrun.sub(t, SE_OLD, SE2)
        if k == 'c25':
            return bdrun.sub(t, C25_OLD, C25, 1)
        if k == 'c25both':
            return bdrun.sub(t, C25_OLD, C25)
        if k == 'c27n':
            return bdrun.sub(t, C27_OLD, C27N)
        if k == 'skip':
            return bdrun.sub(t, SKIP_OLD, SKIP)
        if k == 'skipn':
            return bdrun.sub(t, SKIP_OLD, SKIPN)
        raise ValueError(k)
    return f


EDITS = ['se1', 'se2', 'c25', 'c27n', 'skip', 'skipn']
OFFS = os.environ.get('BDOFFS', 'none,exp_t10,exp_pr,lab_t5le,pin_d,vol_fail').split(',')
ETYPE = ('\t\t\t\t} else if (type)\n', '\t\t\t\t} else\n')


def off(t, k):
    if k == 'none':
        return t
    if k == 'etype':
        return bdrun.sub(t, *ETYPE)
    return bdhints.off(t, k)


def CASES(base):
    out = []
    for e in EDITS:
        for k in OFFS + ['etype']:
            out.append(('%s|%s' % (e, k), lambda b, e=e, k=k: off(edit(e)(b), k)))
    return out

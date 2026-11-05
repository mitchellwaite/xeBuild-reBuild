"""Quick singles on loadBl and loadConsoleBlFiles: real shared helpers (case 23 and case 25 are the same code in both functions), case 27's test gone or as a function, with
the neighbouring hints off or on."""
import itertools, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdtricks


LOADPATCH = '''/* the patch set */
static int loadPatchFile(struct fileent *e)
{
	int r;

	r = loadBinFile(e);
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
LOADXELL = '''/* xell: perbuild directory, firmware /bin folder, then the base path */
static int loadXell(struct fileent *e)
{
	if (xb.type == BUILD_RETAIL || xb.type > BUILD_DEVGL16)
		return 0;
	if (!loadBaseFile(e->name, e))
		return 0;
	log_printf(1, "xell not found in perbuild directory, checking firmware /bin folder\\n");
	if (!loadBinFile(e))
		return 0;
	log_printf(1, "xell not found in firmware /bin folder, checking base path\\n");
	return loadLocalFile(e);
}

'''
ANCHOR = '/* load the input file e (xb.files[i]) by its type */\n'
BL23 = '''		if (xb.type == BUILD_RETAIL)
			break;
		*pr = loadBinFile(e);
		if (*pr)
			break;
		if (e->size & 3) {
		badsize: __attribute__((hot));
			log_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);
			goto fail;
		}
		appendAddonPatches(e);
		break;
'''
CO23 = '''				r = loadBinFile(e);
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
BL25 = '''		if (xb.type == BUILD_RETAIL || xb.type > BUILD_DEVGL16)
			break;
		if (!loadBaseFile(e->name, e))
			break;
		log_printf(1, "xell not found in perbuild directory, checking firmware /bin folder\\n");
		if (!loadBinFile(e))
			break;
		log_printf(1, "xell not found in firmware /bin folder, checking base path\\n");
		*pr = loadLocalFile(e);
		break;
'''
CO25 = '''				if (xb.type == BUILD_RETAIL || xb.type > BUILD_DEVGL16)
					break;
				if (!loadBaseFile(e->name, e))
					break;
				log_printf(1, "xell not found in perbuild directory, checking firmware /bin folder\\n");
				if (!loadBinFile(e))
					break;
				log_printf(1, "xell not found in firmware /bin folder, checking base path\\n");
				r = loadLocalFile(e);
				break;
'''


def e23(t, which):
    t = t.replace(ANCHOR, LOADPATCH + ANCHOR)
    if 'b' in which:
        t = t.replace(BL23, '		if (xb.type == BUILD_RETAIL)\n			break;\n		*pr = loadPatchFile(e);\n		break;\n')
    if 'c' in which:
        t = t.replace(CO23, '				r = loadPatchFile(e);\n				break;\n')
    return t


def e25(t, which):
    t = t.replace(ANCHOR, LOADXELL + ANCHOR)
    if 'b' in which:
        t = t.replace(BL25, '		*pr = loadXell(e);\n		break;\n')
    if 'c' in which:
        t = t.replace(CO25, '				r = loadXell(e);\n				break;\n')
    return t


def CASES(base):
    out = []
    off = ['', 'lab_badsize', 'lab_t5le', 'exp_pr', 'vol_fail', 'lab_badsize,vol_fail', 'exp_t10', 'lab_none', 'exp_t9', 'exp_27', 'pin_d']
    for o in off:
        b = bdtricks.apply(base, [x for x in o.split(',') if x])[0]
        out.append((('off %s' % o), b))
        for w in ('b', 'c', 'bc'):
            out.append(('off %s p23 %s' % (o, w), e23(b, w)))
            out.append(('off %s x25 %s' % (o, w), e25(b, w)))
            out.append(('off %s p23+x25 %s' % (o, w), e25(e23(b, w), w)))
        out.append(('off %s no27test' % o, b.replace('if (__builtin_expect(type == 27, 1) && loadBaseFile', 'if (loadBaseFile').replace('if (type == 27 && loadBaseFile', 'if (loadBaseFile')))
    return out

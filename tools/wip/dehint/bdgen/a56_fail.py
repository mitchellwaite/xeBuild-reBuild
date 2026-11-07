"""Attempt 56: case 23's patch-size failure shapes on attempt 55's SMC equal bases (`if`: the SMC
failure as `if (!e->offset) { fail: r = -1; } break;`; `end`: `goto fail` with `fail:` after the
default case), barrier off, each with the pr / neg spellings.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a56_fail.py [-p ..] [-k label]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a46_m1hints as H
import a55_smc as S
BASE = H.BASE

C23 = '''				r = loadBinFile(e);
				if (r)
					break;
				if (e->size & 3) {
					log_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);
					goto fail;
				}
				appendAddonPatches(e);
				break;
'''
LOG = 'log_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);'
HELPER_AT = '/* load the input files by their type; the arms only set r, which is\n'


def c23(body, helper=None):
    eds = [(C23, body)]
    if helper:
        eds.append((HELPER_AT, helper + '\n' + HELPER_AT))
    return eds


C = {
 'src': [],
 'own': c23('''				r = loadBinFile(e);
				if (r)
					break;
				if (e->size & 3) {
					%s
					r = -1;
					break;
				}
				appendAddonPatches(e);
				break;
''' % LOG),
 'pre': c23('''				r = loadBinFile(e);
				if (r)
					break;
				if (e->size & 3) {
					r = -1;
					%s
					break;
				}
				appendAddonPatches(e);
				break;
''' % LOG),
 'nest': c23('''				r = loadBinFile(e);
				if (!r) {
					if (e->size & 3) {
						%s
						goto fail;
					}
					appendAddonPatches(e);
				}
				break;
''' % LOG),
 'good': c23('''				r = loadBinFile(e);
				if (r)
					break;
				if (!(e->size & 3)) {
					appendAddonPatches(e);
					break;
				}
				%s
				goto fail;
''' % LOG),
 'else': c23('''				r = loadBinFile(e);
				if (r)
					break;
				if (e->size & 3) {
					%s
					goto fail;
				} else
					appendAddonPatches(e);
				break;
''' % LOG),
 'tern': c23('''				r = loadBinFile(e);
				if (r)
					break;
				r = (e->size & 3) ? -1 : 0;
				if (r) {
					%s
					break;
				}
				appendAddonPatches(e);
				break;
''' % LOG),
 'h_ret': c23('''				r = loadBinFile(e);
				if (r)
					break;
				if (e->size & 3) {
					r = badPatchSize(e);
					break;
				}
				appendAddonPatches(e);
				break;
''', '''/* the patch file's size must be a multiple of 4 */
static int badPatchSize(struct fileent *e)
{
	%s
	return -1;
}
''' % LOG),
 'h_chk': c23('''				r = loadBinFile(e);
				if (r)
					break;
				r = checkPatchSize(e);
				if (r)
					break;
				appendAddonPatches(e);
				break;
''', '''/* the patch file's size must be a multiple of 4 */
static int checkPatchSize(struct fileent *e)
{
	if (e->size & 3) {
		%s
		return -1;
	}
	return 0;
}
''' % LOG),
 'h_chkf': c23('''				r = loadBinFile(e);
				if (r)
					break;
				if (checkPatchSize(e))
					goto fail;
				appendAddonPatches(e);
				break;
''', '''/* the patch file's size must be a multiple of 4 */
static int checkPatchSize(struct fileent *e)
{
	if (e->size & 3) {
		%s
		return 1;
	}
	return 0;
}
''' % LOG),
 'h_okf': c23('''				r = loadBinFile(e);
				if (r)
					break;
				if (!patchSizeOk(e))
					goto fail;
				appendAddonPatches(e);
				break;
''', '''/* the patch file's size must be a multiple of 4 */
static int patchSizeOk(struct fileent *e)
{
	if (!(e->size & 3))
		return 1;
	%s
	return 0;
}
''' % LOG),
 'h_v': c23('''				r = loadBinFile(e);
				if (r)
					break;
				if (e->size & 3) {
					badPatchSize(e);
					goto fail;
				}
				appendAddonPatches(e);
				break;
''', '''/* the patch file's size must be a multiple of 4 */
static void badPatchSize(struct fileent *e)
{
	%s
}
''' % LOG),
 'rep': c23('''				r = loadBinFile(e);
				if (r)
					break;
				if (e->size & 3)
					%s
				if (e->size & 3)
					goto fail;
				appendAddonPatches(e);
				break;
''' % LOG),
}
OFFS = {'': [], 'neg': [('if (__builtin_expect(r != 0, 0))\n', 'if ((int)r < 0)\n')]}
V = {}
for bn, bf in (('if', S.smcif), ('end', S.smcend)):
    for cn, ce in C.items():
        for k, ed in OFFS.items():
            V['%s_%s%s' % (bn, cn, ('_' + k) if k else '')] = bf(0) + ce + ed

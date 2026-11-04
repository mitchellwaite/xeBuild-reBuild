# attempt 21: loop forms whose niter carries an assumption (unsigned <=), so number_of_latch_executions should be unknown and sccp (from memory) leaves the exit unsplit.
# `IWB=build/iw/a21/na.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw277.py -n 30 -t 4`
FS = '''		for (i = 0; i < blocks; i++) {
			if (next != 0 && next != 0xffff) {
				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(next);
			} else {
				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(start + i - xb.fsStart + 1);
			}
		}
'''
PG = '		for (end = p + npages; p < end; p++) {\n'
AF = [
 ('', []),
 ('f1', [('for (i = 0; i < blocks; i++) {\n\t\t\tif (next != 0 &&', 'for (i = 0; i <= blocks - 1; i++) {\n\t\t\tif (next != 0 &&')]),
 ('f1b', [('for (i = 0; i < blocks; i++) {\n\t\t\tif (next != 0 &&', 'for (i = 0; i + 1 <= blocks; i++) {\n\t\t\tif (next != 0 &&')]),
 ('f5', [(FS, FS.replace('i = 0; i < blocks', 'i = 1; i <= blocks').replace('start + i - xb.fsStart]', 'start + i - 1 - xb.fsStart]').replace('start + i - xb.fsStart + 1', 'start + i - xb.fsStart'))]),
 ('f6', [(FS, FS.replace('for (i = 0; i < blocks; i++)', 'for (i = 0; blocks > i; i += 1)'))]),
]
AP = [
 ('', []),
 ('p1', [(PG, '		for (end = p + npages; p <= end - 1; p++) {\n')]),
 ('p2', [(PG, '		end = p + npages - 1;\n\t\tfor (; p <= end; p++) {\n')]),
 ('p3', [(PG, '		for (end = p + npages; p + 1 <= end; p++) {\n')]),
]
AXES = [AF, AP]

# attempt 5: imgFits with an if (survives early inlining as a PHI of constants, threaded later): forms x natural imgAddFile x imgAddMobile x param
import gen_iw68 as G
FITS = '''int imgFits(uint32_t off, uint32_t len)
{
	return (xb.fsEnd - 1) * 0x4000 >= off + len;
}
'''
A = '(xb.fsEnd - 1) * 0x4000'
B = 'off + len'
FORMS = {
 'if1': 'if (%s >= %s)\n		return 1;\n	return 0;\n' % (A, B),
 'if0': 'if (%s < %s)\n		return 0;\n	return 1;\n' % (A, B),
 'if0r': 'if (%s > %s)\n		return 0;\n	return 1;\n' % (B, A),
 'if1r': 'if (%s <= %s)\n		return 1;\n	return 0;\n' % (B, A),
 'else1': 'if (%s >= %s)\n		return 1;\n	else\n		return 0;\n' % (A, B),
 'else0': 'if (%s > %s)\n		return 0;\n	else\n		return 1;\n' % (B, A),
 'r0': 'int r = 0;\n\n	if (%s >= %s)\n		r = 1;\n	return r;\n' % (A, B),
 'r1': 'int r = 1;\n\n	if (%s > %s)\n		r = 0;\n	return r;\n' % (B, A),
 'lim0': 'uint32_t lim = %s;\n\n	if (%s > lim)\n		return 0;\n	return 1;\n' % (A, B),
 'lim1': 'uint32_t lim = %s;\n\n	if (lim >= %s)\n		return 1;\n	return 0;\n' % (A, B),
 'end0': 'uint32_t end = %s;\n\n	if (end > %s)\n		return 0;\n	return 1;\n' % (B, A),
 'tern': 'return %s >= %s ? 1 : 0;\n' % (A, B),
}
AXES = [
 [(k, [(FITS, 'int imgFits(uint32_t off, uint32_t len)\n{\n	' + v + '}\n')]) for k, v in FORMS.items()],
 [('fits', [(G.HEAD, G.F['fits'])]), ('nfits', [(G.HEAD, '''
	if (!imgFits(off, len)) {
		log_printf(0, "\\n******* ERROR: adding %s will exceed available flash space! Skipped!\\n\\n", name);
		return;
	}
	{
'''), (G.ELSE, '	}\n}\n\nvoid imgAddFileAs')])],
 [('', []), ('mob', [('if (__builtin_expect(imgFits(off, len), 1)) {', 'if (imgFits(off, len)) {')])],
]
FLAGS = []

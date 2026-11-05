"""loadDump's mmcbad: PRED_CALL cancelled by a call in both arms (P 50) with the tail in a static helper called from each path, switch or if."""
FOCUS = ['_copyMmcImage', '_loadDump']
BASE = 'src/image_read.c'
src = open(BASE, newline='').read().replace('\r\n', '\n')
i = src.index('		if (xb.dumpMmc) {\n			xb.numBad = 0;')
j = src.index('	} else {\n		log_printf(0, "******* ERROR loading \'%s\', unable to determine')
OLD = src[i:j]
LOG = 'log_printf(0, "\\n\\n***** ERROR: nanddump.bin is a ZEROPAIR/XELL image, discarding\\n");\n'
COPY = 'xb.numBad = 0;\n memcpy(xb.dump, raw, xb.dumpSize);\n'
TAIL = '''getImageKv();
			getImageSmc();
			findSmcConfig();
			getImageLdv();
			if (findFsRoot()) {
				if (!(xb.bootFlags & 0x20000000)) {
					getNetKd();
					getImageMobiles();
				}
				if (!(xb.bootFlags & 0x4000000))
					imgGetSecurityFiles();
			}
			getNonces();
'''
HELP = {
 'st': 'static void readImageParts(void)\n{\n' + TAIL + '}\n\n',
 'si': 'static inline void readImageParts(void)\n{\n' + TAIL + '}\n\n',
}
PARSE = {
 'p1': 'ret = parseDump(raw);\n if (!ret) buildCleanup(); else readImageParts();\n',
 'p2': 'ret = parseDump(raw);\n if (ret) readImageParts(); else buildCleanup();\n',
}
ARM = {
 'sw': f'switch (notZeropair()) {{ case 0: {LOG} ret = 0; buildCleanup(); break; default: ret = 1; readImageParts(); }}\n',
 'sw2': f'switch (notZeropair()) {{ default: ret = 1; readImageParts(); break; case 0: {LOG} ret = 0; buildCleanup(); }}\n',
 'if': f'if (notZeropair()) {{ ret = 1; readImageParts(); }} else {{ {LOG} ret = 0; buildCleanup(); }}\n',
 'ifn': f'if (notZeropair() != (size != 0)) {{ {LOG} ret = 0; buildCleanup(); }} else {{ ret = 1; readImageParts(); }}\n',
 'ife': f'if (notZeropair() != (size == 0)) {{ ret = 1; readImageParts(); }} else {{ {LOG} ret = 0; buildCleanup(); }}\n',
}
AX = []
for kh, h in HELP.items():
    for ka, a in ARM.items():
        for kp, p in PARSE.items():
            AX.append(('.'.join((kh, ka, kp)), [
                ('uint32_t loadDump(const char *path)\n{', h + 'uint32_t loadDump(const char *path)\n{'),
                (OLD, 'if (xb.dumpMmc) {\n' + COPY + a + '} else {\n' + p + '}\n'),
            ]))
AXES = [AX]

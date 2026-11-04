"""flhill.py [dead subset names]: one-off natural edits over parseIni at the natural tail,
with a greedy climb.  Baseline: flash else, sec after, seclen nest, flen nest, raw else; dead
tests removed except those named on the command line (prefix keep:name)."""
import itertools, sys
import fllib as L, flpi as P, flfinal as F

FL = F.FLAGS
EDITS = {
 'noCrcInt': [('	uint32_t noCrc;\n', '	int noCrc;\n')],
 'crcDecl': [('	uint32_t crc;\n', ''), ('	uint32_t noCrc;\n', '	uint32_t noCrc, crc;\n')],
 'ge0ver': [('	if (off != -1) {\n		memset(xb.kernelStr', '	if (off >= 0) {\n		memset(xb.kernelStr')],
 'ne1bl': [('	if (off >= 0) {\n		log_printf(1, "\\nini: label %s found', '	if (off != -1) {\n		log_printf(1, "\\nini: label %s found')],
 'lenlt0': [('		if (len == -1)\n			len = sizeof(xb.kernelStr) - 1;', '		if (len < 0)\n			len = sizeof(xb.kernelStr) - 1;')],
 'bufnot': [('	if (buf == NULL) {', '	if (!buf) {')],
 'nullf': [('	if (f == NULL) {', '	if (!f) {')],
 'plusend': [("		end = off + memFindChar(&buf[off], '[', size - off);\n		/* this and", "		end = memFindChar(&buf[off], '[', size - off) + off;\n		/* this and")],
 'posbl': [("		pos = off;\n		for (i = 0; i < nbl; ) {", "		for (pos = off, i = 0; i < nbl; ) {")],
 'blfor': [("		for (i = 0; i < nbl; ) {", "		for (i = 0; i < nbl; i++) {"), ("			i++;\n			if (pos > end) {", "			if (pos > end) {"), ("i + 1, xb.files[blOrder[i]].name", "i + 1, xb.files[blOrder[i]].name")],
 'posraw': [("		pos = off;\n		for (i = xb.nRawPatches; i < 16; i++) {", "		for (pos = off, i = xb.nRawPatches; i < 16; i++) {")],
 'rawcomma': [('			if (comma == -1 || comma >= nul) {', '			if (comma < 0 || comma >= nul) {')],
 'rawcommarev': [('			if (comma == -1 || comma >= nul) {', '			if (comma >= nul || comma == -1) {')],
 'raworder': [("		end = off + memFindChar(&buf[off], '[', size - off);\n		log_printf(1, \"\\nini: label [rawpatch] found\\n\");", "		log_printf(1, \"\\nini: label [rawpatch] found\\n\");\n		end = off + memFindChar(&buf[off], '[', size - off);")],
 'flcomma': [('		if (comma >= 0 && comma < nul) {', '		if (comma != -1 && comma < nul) {')],
 'flcommarev': [('		if (comma >= 0 && comma < nul) {', '		if (comma < nul && comma >= 0) {')],
 'flnested': [('		if (comma >= 0 && comma < nul) {\n			len = comma;\n			noCrc = 0;\n		}', '		if (comma >= 0) {\n			if (comma < nul) {\n				len = comma;\n				noCrc = 0;\n			}\n		}')],
 'lastchar': [("		if (xb.firmware[i][len - 1] == '1' || xb.firmware[i][len - 1] == '2')\n			xb.firmware[i][len - 1] = 0;", "		if (xb.firmware[i][len - 1] == '1')\n			xb.firmware[i][len - 1] = 0;\n		else if (xb.firmware[i][len - 1] == '2')\n			xb.firmware[i][len - 1] = 0;")],
 'sscope': [('	char *s;\n', ''), ("			s = strrchr(xb.firmware[i], '/');", "			char *s = strrchr(xb.firmware[i], '/');")],
 'sinline': [("			s = s ? s + 1 : xb.firmware[i];\n", "			if (s)\n				s++;\n			else\n				s = xb.firmware[i];\n")],
 'snested': [("			if (s == NULL)\n				s = strrchr(xb.firmware[i], '\\\\');\n", "			if (!s)\n				s = strrchr(xb.firmware[i], '\\\\');\n")],
 'namerev': [("			if (strlen(s) > 21) {", "			if (strlen(s) >= 22) {")],
 'pdecl': [('	unsigned char *buf, *p;\n', '	unsigned char *p, *buf;\n')],
 'crcnoassign': [('			crc = xb.firmwareCrc[i] = 0;\n		log_printf', '			crc = xb.firmwareCrc[i] = 0;\n		log_printf')],
 'crcfw1': [('				crc = xb.firmwareCrc[i] = 0;\n', '				xb.firmwareCrc[i] = crc = 0;\n')],
 'crcfw2': [('			crc = xb.firmwareCrc[i] = 0;\n		log_printf', '			xb.firmwareCrc[i] = crc = 0;\n		log_printf')],
 'crcfw3': [('				crc = xb.firmwareCrc[i] = myatox32(tmp, 0);', '				crc = myatox32(tmp, 0);\n				xb.firmwareCrc[i] = crc;')],
 'efor': [('			e = &xb.files[i];\n', '')] if False else [('		e = &xb.files[i];\n', '		e = xb.files + i;\n')],
 'escope': [('	struct fileent *e;\n', ''), ('		e = &xb.files[i];\n', '		struct fileent *e = &xb.files[i];\n\n')],
 'labelrev': [('	if (xb.blSuffix[0])\n		sprintf(label, "[%sbl%s]", consoleNames[xb.flags & CONSOLE_MASK], xb.blSuffix);\n	else\n		sprintf(label, "[%sbl]", consoleNames[xb.flags & CONSOLE_MASK]);',
               '	if (xb.blSuffix[0] == 0)\n		sprintf(label, "[%sbl]", consoleNames[xb.flags & CONSOLE_MASK]);\n	else\n		sprintf(label, "[%sbl%s]", consoleNames[xb.flags & CONSOLE_MASK], xb.blSuffix);')],
 'tmpscope': [('	char tmp[0x400];\n', '	char tmp[1024];\n')],
 'cbbrev': [('		if (strnicmp(xb.files[4].name, "none", 4) == 0)\n			xb.cbb = 0;\n		else {\n			log_printf(1, "ini dictates dual CB for this model\\n");\n			xb.cbb = 1;\n		}',
             '		if (strnicmp(xb.files[4].name, "none", 4) != 0) {\n			log_printf(1, "ini dictates dual CB for this model\\n");\n			xb.cbb = 1;\n		} else\n			xb.cbb = 0;')],
}


def apply(s, names):
    for n in names:
        for o, w in EDITS[n]:
            if s.count(o) < 1:
                raise ValueError(n + ': ' + o[:50])
            s = s.replace(o, w, 1)
    return s


if __name__ == '__main__':
    keep = [a for a in sys.argv[1:]]
    dead = [d for d in P.ALLDEAD if d not in keep]
    base = F.full(pi=('else', 'after', 'nest', 'nest', 'else'), dead=dead)
    print('base', L.score(L.compile(base, FL, 'h0'))[:3])
    print('noparam', L.score(L.compile(base, ['-O3'], 'h1'))[:3])
    cur = []
    best = L.score(L.compile(base, FL, 'h0'))[0]
    for rnd in range(4):
        V = {}
        for n in EDITS:
            if n in cur:
                continue
            try:
                V[n] = apply(base, cur + [n])
            except ValueError as e:
                print('skip', e)
        rs = L.sweep(V, FL, prefix='hl', show=8 if rnd == 0 else 3)
        n, sc = rs[0][0], rs[0][1][0]
        if sc >= best:
            break
        best, cur = sc, cur + [n]
        print('round', rnd, 'took', n, sc)
    print('final', cur, best)
    open(L.BD + '/hill.c', 'w', newline='\n').write(apply(base, cur))

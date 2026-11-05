"""fsGetFile, pin_v gone: a0 (retval) has to pop before off's thread, or off has to avoid esi.  Forms of off and of the tests / single exit (nested, the author's way)."""
FOCUS = ['_fsGetFile']
BASE = 'tools/wip/dehint/drafts/image_read_attempt6.c'
WHOLE_A = '''	int v = fsValid;

	/* code-free hint: fsValid (reused for return 1) in esi, name in edi */
	__asm__("" : : "S"(v));
	if (v != 1)
		return 0;
	if (!fsFind(name, &block, &len, &t, 1))
		return 0;
	off = fsOffset + (block << 14);
	p = calloc(len, 1);
	left = len;
	done = 0;
	while (left > 0x4000) {
		memcpy(p + done, xb.dump + off, 0x4000);
		left -= 0x4000;
		done += 0x4000;
		block = SWAP16(fs->map[block]) & 0x1fff;
		off = fsOffset + (block << 14);
	}
	if (left)
		memcpy(p + done, xb.dump + off, left);
	*buf = p;
	*size = len;
	*time = t;
	return 1;
'''
OFFS = {
    'a': 'off = fsOffset + (block << 14);\n',
    'b': 'off = (block << 14) + fsOffset;\n',
    'c': 'off = block << 14;\n off += fsOffset;\n',
    'd': 'off = block * 0x4000 + fsOffset;\n',
}
NX = {
    'a': 'block = SWAP16(fs->map[block]) & 0x1fff;\n',
    'b': 'block = fs->map[block];\n block = SWAP16(block) & 0x1fff;\n',
}
def body(o, n):
    return f'''{o} p = calloc(len, 1);
	left = len;
	done = 0;
	while (left > 0x4000) {{
		memcpy(p + done, xb.dump + off, 0x4000);
		left -= 0x4000;
		done += 0x4000;
		{n}
		{o}
	}}
	if (left)
		memcpy(p + done, xb.dump + off, left);
	*buf = p;
	*size = len;
	*time = t;
'''
EX = {
    'r': lambda b: '	if (fsValid != 1)\n return 0;\n if (!fsFind(name, &block, &len, &t, 1))\n return 0;\n' + b + 'return 1;\n',
    'v': lambda b: '	int v = fsValid;\n if (v != 1)\n return 0;\n if (!fsFind(name, &block, &len, &t, 1))\n return 0;\n' + b + 'return 1;\n',
    'vr': lambda b: '	int v = fsValid;\n if (v != 1)\n return 0;\n if (!fsFind(name, &block, &len, &t, 1))\n return 0;\n' + b + 'return v;\n',
    'n': lambda b: '	int ret = 0;\n if (fsValid == 1) {\n if (fsFind(name, &block, &len, &t, 1)) {\n' + b + 'ret = 1;\n }\n }\n return ret;\n',
    'n2': lambda b: '	int ret = 0;\n if (fsValid == 1 && fsFind(name, &block, &len, &t, 1)) {\n' + b + 'ret = 1;\n }\n return ret;\n',
    'n3': lambda b: '	int ret = fsValid == 1;\n if (ret) {\n ret = fsFind(name, &block, &len, &t, 1);\n if (ret) {\n' + b + '}\n }\n return ret;\n',
    'n4': lambda b: '	int ret = fsValid;\n if (ret == 1) {\n if (fsFind(name, &block, &len, &t, 1)) {\n' + b + '}\n else ret = 0;\n }\n else ret = 0;\n return ret;\n',
    'n5': lambda b: '	if (fsValid == 1) {\n if (fsFind(name, &block, &len, &t, 1)) {\n' + b + 'return 1;\n }\n }\n return 0;\n',
    'n6': lambda b: '	int ok = 0;\n if (fsValid == 1)\n ok = fsFind(name, &block, &len, &t, 1);\n if (ok) {\n' + b + '}\n return ok;\n',
}
AX = [(e + o + n, [(WHOLE_A, f(body(OFFS[o], NX[n])))]) for e, f in EX.items() for o in OFFS for n in NX]
AXES = [AX]

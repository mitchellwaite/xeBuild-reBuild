"""ceDecrypt: two tests of buf with real code in the first arm, so threading keeps the second test's block
frequencies but the first test's edge probability (what the hinted build's `if (buf) asm` did).
Axes: where the first arm ends, how the second test's arm ends, key's scope."""
import importlib.util, itertools, os
spec = importlib.util.spec_from_file_location('gen_ce1', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_ce1.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
FN = 'ceDecrypt'
ind = g.ind
L = g.BODY.splitlines(True)
CRYPT = L[:3]
HASHPART = ''.join(L[3:])
TAILS = {
    # good arms return, failure falls out
    'fall_else': lambda body: 'if (buf) {\n' + ind(body) + '} else\n\t' + g.ALLOC + '\n',
    # log after the block, the free arm returning itself
    'ret0': lambda body: 'if (buf) {\n' + ind(body) + '\treturn 0;\n}\n' + g.ALLOC + '\n',
    # the hinted tail: arms join, free sets buf = 0, one return buf
    'join': lambda body: 'if (buf) {\n' + ind(JOIN_REST(body)) + '}\n' + g.ALLOC + '\n',
}
JOINED = '''if (hash) {
	if (blCheckHash(buf, len, hash)) {
		log_printf(1, "%c%c hash check OK! Decryption successful!\\n", buf[0], buf[1]);
		if (outLen)
			*outLen = len;
	} else {
		log_printf(0, "***** ERROR: %c%c hash check invalid, corrupted or decryption failed!\\n", buf[0], buf[1]);
		free(buf);
		buf = 0;
	}
} else {
	log_printf(0, "***** WARNING: could not check %cE signature, 1BL RSA key not loaded!\\n", buf[0]);
	if (outLen)
		*outLen = len;
}
return buf;
'''


def JOIN_REST(body):
    return body.replace(HASHPART, JOINED)


def variants():
    for split, (tn, tail), kscope in itertools.product((1, 2, 3), TAILS.items(), ('magic', 'fn')):
        first = ''.join(CRYPT[:split])
        rest = ''.join(CRYPT[split:]) + HASHPART
        inner = 'len = BL_SIZE(bl);\nbuf = calloc(len, 1);\nif (buf) {\n' + ind(first) + '}\n' + tail(rest)
        decl = 'uint8_t *buf;\nuint32_t len;\n'
        kd = 'uint8_t key[16];\n'
        block = ind((decl + kd if kscope == 'magic' else decl) + '\n' + inner)
        fn = (kd + '\n' if kscope == 'fn' else '') + 'if (bl && hmacKey) {\n' + ind("if (BL_MAGIC(bl, 'E')) {\n" + block + '} else\n\t' + g.MAGICLOG + '\n') + '} else\n\t' + g.NULLLOG + '\nreturn 0;\n'
        yield ('split%d %s key=%s' % (split, tn, kscope), g.HEAD + ind(fn) + '}\n')

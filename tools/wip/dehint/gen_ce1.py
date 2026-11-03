"""ceDecrypt: the alloc-fail edge needs freq > 100 (5041 * 1.9% = 96). Axes: how the alloc arm is spelled, how magic fails."""
FN = 'ceDecrypt'
HEAD = '/* decrypted copy of an SE/CE with hmacKey, hash checked if given */\n' \
       'uint8_t *ceDecrypt(uint8_t *bl, uint32_t *outLen, const uint8_t *hmacKey, const uint8_t *hash)\n{\n'
BODY = '''memcpy(buf, bl, len);
XeCryptHmacSha(hmacKey, 16, buf + 16, 16, 0, 0, 0, 0, key, 16);
XeCryptRc4(key, 16, buf + 32, len - 32);
if (hash) {
	if (blCheckHash(buf, len, hash)) {
		log_printf(1, "%c%c hash check OK! Decryption successful!\\n", buf[0], buf[1]);
		if (outLen)
			*outLen = len;
		return buf;
	}
	log_printf(0, "***** ERROR: %c%c hash check invalid, corrupted or decryption failed!\\n", buf[0], buf[1]);
	free(buf);
} else {
	log_printf(0, "***** WARNING: could not check %cE signature, 1BL RSA key not loaded!\\n", buf[0]);
	if (outLen)
		*outLen = len;
	return buf;
}
'''
ALLOC = 'log_printf(0, "***** WARNING: Unable to allocate 0x%x bytes for %cE!\\n", bl[0]);'
MAGICLOG = 'log_printf(0, "***** WARNING: SE/CE does not have valid magic!\\n");'
NULLLOG = 'log_printf(0, "***** WARNING: SE/CE decrypt not provided with data!\\n");'
DECL = 'uint8_t *buf;\nuint32_t len;\nuint8_t key[16];\n\n'
GET = 'len = BL_SIZE(bl);\nbuf = calloc(len, 1);\n'


def ind(s, n=1):
    return ''.join(('\t' * n + l if l.strip() else l) for l in s.splitlines(True))


ARMS = {
    'base': GET + 'if (buf) {\n' + ind(BODY) + '} else\n\t' + ALLOC + '\n',
    'notfirst': GET + 'if (!buf)\n\t' + ALLOC + '\nelse {\n' + ind(BODY) + '}\n',
    'twotest': GET + 'if (!buf)\n\t' + ALLOC + '\nif (buf) {\n' + ind(BODY) + '}\n',
    'twotest2': GET + 'if (!buf)\n\t' + ALLOC + '\nelse if (buf) {\n' + ind(BODY) + '}\n',
    'ret0': GET + 'if (!buf) {\n\t' + ALLOC + '\n\treturn 0;\n}\n' + BODY,
    'retbuf': GET + 'if (!buf) {\n\t' + ALLOC + '\n\treturn buf;\n}\n' + BODY,
    'gotofall': GET + 'if (buf) {\n' + ind(BODY) + '\treturn 0;\n}\n' + ALLOC + '\n',
    'fallthru': GET + 'if (buf) {\n' + ind(BODY) + '\treturn 0;\n} else\n\t' + ALLOC + '\n',
}


def magic(kind, inner):
    t = ind(DECL + inner)
    if kind == 'one':
        return "if (BL_MAGIC(bl, 'E')) {\n" + t + '} else\n\t' + MAGICLOG + '\n'
    if kind == 'two':
        return "if ((bl[0] & 0x43) == 0x43) {\n\tif (bl[1] == 'E') {\n" + ind(t) + '\t} else\n\t\t' + MAGICLOG + '\n} else\n\t' + MAGICLOG + '\n'
    if kind == 'neg':
        return "if (!BL_MAGIC(bl, 'E'))\n\t" + MAGICLOG + '\nelse {\n' + t + '}\n'
    raise ValueError


def variants():
    for a, inner in ARMS.items():
        for k in ('one', 'two', 'neg'):
            yield ('%s %s' % (a, k), HEAD + ind('if (bl && hmacKey) {\n' + ind(magic(k, inner)) + '} else\n\t' + NULLLOG + '\nreturn 0;\n') + '}\n')

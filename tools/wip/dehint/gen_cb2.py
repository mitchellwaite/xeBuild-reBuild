"""cbDecrypt: return type x buf's type x a separate variable for the result (key at function level).
uncprop only reuses a value that can coalesce with the PHI's result (same type)."""
FN = 'cbDecrypt'


def body(ret, buft, shape):
    proto = '%s cbDecrypt(uint8_t *cb, uint32_t *outLen, uint8_t *outKey)' % ret
    s = '/* decrypted copy of a CB/SB (free it), checked against the 1BL RSA key */\n%s;\n%s\n{\n' % (proto, proto)
    s += '\t%sbuf;\n\tuint32_t len;\n\tuint8_t key[16];\n' % buft
    idx = '' if buft == 'uint8_t *' else '(uint8_t *)'
    U = '((uint8_t *)buf)' if buft != 'uint8_t *' else 'buf'
    if shape == 'ret':
        s = s.replace('\tuint32_t len;', '\t%s ret = 0;\n\tuint32_t len;' % ret.rstrip(), 1) if False else s
    s += '''
	if (cb) {
		if (BL_MAGIC(cb, 'B')) {
			len = BL_SIZE(cb);
			buf = calloc(len, 1);
			if (buf) {
				memcpy(buf, cb, len);
				XeCryptHmacSha(xb.key1bl, 16, U + 16, 16, 0, 0, 0, 0, key, 16);
				XeCryptRc4(key, 16, U + 32, len - 32);
				if (outKey)
					memcpy(outKey, key, 16);
				if (xb.pub1bl) {
					if (cbVerifySig(buf, xb.pub1bl)) {
						log_printf(1, "%cB signature OK! Decryption successful!\\n", U[0]);
						if (outLen)
							*outLen = len;
					} else {
						log_printf(0, "***** ERROR: %cB signature invalid, corrupted or decryption failed!\\n", U[0]);
						free(buf);
						buf = 0;
					}
				} else {
					log_printf(0, "***** WARNING: could not check %cB signature, 1BL RSA key not loaded!\\n", U[0]);
					if (outLen)
						*outLen = len;
				}
				return RET;
			}
			log_printf(0, "***** WARNING: Unable to allocate 0x%x bytes for %c%c!\\n", cb[0], cb[1]);
		} else
			log_printf(0, "***** WARNING: CB/SB does not have valid magic!\\n");
	} else
		log_printf(0, "***** WARNING: CB/SB decrypt not provided with data!\\n");
	return 0;
}
'''.replace('U[0]', U + '[0]').replace('U + ', U + ' + ')
    cast = ''
    if ret == 'int' or ret == 'uint32_t':
        cast = '(%s)' % ret
    return s.replace('RET', cast + 'buf')


def variants():
    for ret in ('uint8_t *', 'void *', 'char *', 'unsigned char *', 'const uint8_t *', 'BYTE *', 'uint32_t', 'int'):
        for buft in ('uint8_t *', 'void *', 'char *', 'unsigned char *'):
            yield ('ret=%s buf=%s' % (ret, buft), body(ret, buft, 'plain'))

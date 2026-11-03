"""cbDecrypt: key/len scope x where the fail arm goes.  First pass: does the brief's description hold?"""
FN = 'cbDecrypt'

HEAD = '''/* decrypted copy of a CB/SB (free it), checked against the 1BL RSA key */
uint8_t *cbDecrypt(uint8_t *cb, uint32_t *outLen, uint8_t *outKey);
uint8_t *cbDecrypt(uint8_t *cb, uint32_t *outLen, uint8_t *outKey)
{
'''


def body(keyat, lenat, bufat):
    k = '\tuint8_t key[16];\n'
    l = '\tuint32_t len;\n'
    b = '\tuint8_t *buf;\n'
    s = HEAD
    if bufat == 'fn': s += b
    if lenat == 'fn': s += l
    if keyat == 'fn': s += k
    s += '\n\tif (cb) {\n'
    if keyat == 'cb': s += '\t' + k
    if lenat == 'cb': s += '\t' + l
    if bufat == 'cb': s += '\t' + b
    s += "\t\tif (BL_MAGIC(cb, 'B')) {\n"
    if keyat == 'magic': s += '\t\t' + k
    if lenat == 'magic': s += '\t\t' + l
    if bufat == 'magic': s += '\t\t' + b
    s += '\t\t\tlen = BL_SIZE(cb);\n\t\t\tbuf = calloc(len, 1);\n\t\t\tif (buf) {\n'
    if keyat == 'buf': s += '\t\t\t' + k
    s += '''				memcpy(buf, cb, len);
				XeCryptHmacSha(xb.key1bl, 16, buf + 16, 16, 0, 0, 0, 0, key, 16);
				XeCryptRc4(key, 16, buf + 32, len - 32);
				if (outKey)
					memcpy(outKey, key, 16);
				if (xb.pub1bl) {
					if (cbVerifySig(buf, xb.pub1bl)) {
						log_printf(1, "%cB signature OK! Decryption successful!\\n", buf[0]);
						if (outLen)
							*outLen = len;
					} else {
						log_printf(0, "***** ERROR: %cB signature invalid, corrupted or decryption failed!\\n", buf[0]);
						free(buf);
						buf = 0;
					}
				} else {
					log_printf(0, "***** WARNING: could not check %cB signature, 1BL RSA key not loaded!\\n", buf[0]);
					if (outLen)
						*outLen = len;
				}
				return buf;
			}
			log_printf(0, "***** WARNING: Unable to allocate 0x%x bytes for %c%c!\\n", cb[0], cb[1]);
		} else
			log_printf(0, "***** WARNING: CB/SB does not have valid magic!\\n");
	} else
		log_printf(0, "***** WARNING: CB/SB decrypt not provided with data!\\n");
	return 0;
}
'''
    return s


def variants():
    for k in ('fn', 'cb', 'magic', 'buf'):
        for l in ('fn', 'cb', 'magic'):
            for b in ('fn', 'cb', 'magic'):
                yield ('key=%s len=%s buf=%s' % (k, l, b), body(k, l, b))

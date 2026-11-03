"""What no-cse-follow-jumps did: the hinted cbDecrypt shape with each half of the attribute.
Run as is for cbDecrypt."""
FN = 'cbDecrypt'

BODY = '''uint8_t *cbDecrypt(uint8_t *cb, uint32_t *outLen, uint8_t *outKey)
{
	uint8_t *buf;
	uint32_t len;
	uint8_t key[16];

	if (cb) {
		if (BL_MAGIC(cb, 'B')) {
			len = BL_SIZE(cb);
			buf = calloc(len, 1);
			if (buf) {
				memcpy(buf, cb, len);
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


def variants():
    for tag, attr in (('both', '"no-tree-dominator-opts", "no-cse-follow-jumps"'), ('dom only', '"no-tree-dominator-opts"'),
                      ('cse only', '"no-cse-follow-jumps"')):
        yield (tag, '__attribute__((optimize(%s)))\n' % attr + BODY)

"""ceDecrypt with cbDecrypt's landed shape, no pin, a look ahead for queue 12 (src/ untouched)."""
FN = 'ceDecrypt'

SRC = '''uint8_t *ceDecrypt(uint8_t *bl, uint32_t *outLen, const uint8_t *hmacKey, const uint8_t *hash)
{
	if (bl && hmacKey) {
		if (BL_MAGIC(bl, 'E')) {
			uint8_t *buf;
			uint32_t len;
			uint8_t key[16];

			len = BL_SIZE(bl);
			buf = calloc(len, 1);
			if (buf) {
				memcpy(buf, bl, len);
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
			} else
				log_printf(0, "***** WARNING: Unable to allocate 0x%x bytes for %cE!\\n", bl[0]);
		} else
			log_printf(0, "***** WARNING: SE/CE does not have valid magic!\\n");
	} else
		log_printf(0, "***** WARNING: SE/CE decrypt not provided with data!\\n");
	return 0;
}
'''


def variants():
    yield ('landed cb shape', '/* decrypted copy of an SE/CE with hmacKey, hash checked if given */\n' + SRC)

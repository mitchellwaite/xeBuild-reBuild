"""cdDecrypt with cbDecrypt's landed shape, a look ahead for queue 11 (src/ untouched)."""
FN = 'cdDecrypt'

SRC = '''uint8_t *cdDecrypt(uint8_t *bl, const void *pubKey, const uint8_t *salt, const uint8_t *hmacKey, uint32_t *outLen, uint8_t *outKey)
{
	if (bl && hmacKey) {
		if ((bl[0] & 0x43) == 0x43 && (bl[1] == 'C' || bl[1] == 'D')) {
			uint8_t *buf;
			uint32_t len;
			uint8_t key[16];

			len = BL_SIZE(bl);
			buf = calloc(len, 1);
			if (buf) {
				memcpy(buf, bl, len);
				XeCryptHmacSha(hmacKey, 16, buf + 16, 16, 0, 0, 0, 0, key, 16);
				XeCryptRc4(key, 16, buf + 32, len - 32);
				if (outKey)
					memcpy(outKey, key, 16);
				if (pubKey && salt) {
					if (blVerifySig(buf, len, pubKey, salt)) {
						log_printf(1, "%c%c signature OK! Decryption successful!\\n", buf[0], buf[1]);
						if (outLen)
							*outLen = len;
						return buf;
					}
					log_printf(0, "***** ERROR: %c%c signature invalid, corrupted or decryption failed!\\n", buf[0], buf[1]);
					free(buf);
				} else {
					log_printf(0, "***** WARNING: could not check %c%c signature, 1BL RSA key not loaded!\\n", buf[0], buf[1]);
					if (outLen)
						*outLen = len;
					return buf;
				}
			} else
				log_printf(0, "***** WARNING: Unable to allocate 0x%x bytes for %c%c!\\n", bl[0], bl[1]);
		} else
			log_printf(0, "***** WARNING: SC/SD/CD does not have valid magic!\\n");
	} else
		log_printf(0, "***** WARNING: SC/SD/CD decrypt not provided with data!\\n");
	return 0;
}
'''


def variants():
    yield ('landed cb shape', '/* decrypted copy of an SC/SD/CD with hmacKey, signature checked if pubKey and salt */\n'
           'uint8_t *cdDecrypt(uint8_t *bl, const void *pubKey, const uint8_t *salt, const uint8_t *hmacKey,\n'
           '\tuint32_t *outLen, uint8_t *outKey);\n' + SRC)

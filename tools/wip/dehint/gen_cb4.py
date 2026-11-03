"""cbDecrypt: the `fall` shape from gen_cb3 (good arms return, sig failure falls out, key in the magic block):
is it stable against buf/len's scope, declaration order, initialisers, and the test's spelling?"""
import itertools

FN = 'cbDecrypt'

TAIL = '''				memcpy(buf, cb, len);
				XeCryptHmacSha(xb.key1bl, 16, buf + 16, 16, 0, 0, 0, 0, key, 16);
				XeCryptRc4(key, 16, buf + 32, len - 32);
				if (outKey)
					memcpy(outKey, key, 16);
				if (xb.pub1bl) {
					if (cbVerifySig(buf, xb.pub1bl)) {
						log_printf(1, "%cB signature OK! Decryption successful!\\n", buf[0]);
						if (outLen)
							*outLen = len;
						return buf;
					}
					log_printf(0, "***** ERROR: %cB signature invalid, corrupted or decryption failed!\\n", buf[0]);
					free(buf);
				} else {
					log_printf(0, "***** WARNING: could not check %cB signature, 1BL RSA key not loaded!\\n", buf[0]);
					if (outLen)
						*outLen = len;
					return buf;
				}
			} else
				log_printf(0, "***** WARNING: Unable to allocate 0x%x bytes for %c%c!\\n", cb[0], cb[1]);
		} else
			log_printf(0, "***** WARNING: CB/SB does not have valid magic!\\n");
	} else
		log_printf(0, "***** WARNING: CB/SB decrypt not provided with data!\\n");
	return 0;
}
'''


def body(place, order, inits):
    d = {'buf': '\t\t\tuint8_t *buf;\n', 'len': '\t\t\tuint32_t len;\n', 'key': '\t\t\tuint8_t key[16];\n'}
    assign = '\t\t\tlen = BL_SIZE(cb);\n\t\t\tbuf = calloc(len, 1);\n'
    if inits:
        d['len'] = '\t\t\tuint32_t len = BL_SIZE(cb);\n'
        d['buf'] = '\t\t\tuint8_t *buf = calloc(len, 1);\n'
        assign = ''
    fn = ''.join(d[n].replace('\t\t\t', '\t') for n in order if place[n] == 'fn')
    block = ''.join(d[n] for n in order if place[n] == 'magic')
    if block:
        block += '\n' if False else ''
    return ('/* decrypted copy of a CB/SB (free it), checked against the 1BL RSA key */\n'
            'uint8_t *cbDecrypt(uint8_t *cb, uint32_t *outLen, uint8_t *outKey);\n'
            'uint8_t *cbDecrypt(uint8_t *cb, uint32_t *outLen, uint8_t *outKey)\n{\n' + fn + ('\n' if fn else '') +
            "\tif (cb) {\n\t\tif (BL_MAGIC(cb, 'B')) {\n" + block + assign + '\t\t\tif (buf) {\n' + TAIL)


def variants():
    for pb, pl in itertools.product(('fn', 'magic'), ('fn', 'magic')):
        for order in itertools.permutations(('buf', 'len', 'key')):
            if order.index('len') > order.index('buf') and pl == pb == 'magic':
                pass
            yield ('buf=%s len=%s %s' % (pb, pl, ','.join(order)), body({'buf': pb, 'len': pl, 'key': 'magic'}, order, False))
    for order in itertools.permutations(('buf', 'len', 'key')):
        if order.index('len') < order.index('buf'):
            yield ('inits %s' % ','.join(order), body({'buf': 'magic', 'len': 'magic', 'key': 'magic'}, order, True))

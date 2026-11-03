"""Baseline: tricks off, one at a time; one source function for both (verifyDae calls it)."""

HEAD = '''int daeVerifySig(uint8_t *seg, uint32_t size, int n)
{
	uint8_t key[16];
	uint8_t hash[20];
	int ok;

	if (!xb.pubPirs)
		return 1;
	if (size < 288)
		return 1;
	memset(key, 0, 16);
	XeCryptHmacSha(key, 16, seg, 32, 0, 0, 0, 0, hash, 20);
	ok = XeKeysPkcs1Verify(hash, seg + 32, (const XECRYPT_RSA *)xb.pubPirs);
'''
TESTS = {
    'ifok': '''	if (ok)
		log_printf(1, "sig %d good! ", n);
	else
		log_printf(1, "\\nsig %d FAIL! ", n);
	return ok;
}
''',
    'ifnot': '''	if (!ok)
		log_printf(1, "\\nsig %d FAIL! ", n);
	else
		log_printf(1, "sig %d good! ", n);
	return ok;
}
''',
}
VD = '''
int verifyDae(uint8_t *buf, uint32_t size)
{
	uint32_t off = 0;
	uint32_t len;
	uint8_t *seg;
	int n = 0;

	while (off < size) {
		seg = buf + off;
		if (buf[off] == 'D' && buf[off + 1] == 'A' && buf[off + 2] == 'E' && buf[off + 3] == 'P') {
			len = (uint16_t)((buf[off + 4] << 8) + buf[off + 5]);
			n++;
			daeVerifySig(seg, len, n);
			daeDecrypt(seg, len, 1);
			if (!shaCheck(seg, len, 12, 20, 336, 0)) {
				log_printf(1, "\\n******* ERROR: dae hash incorrect, could not decrypt!\\n");
				n = 0;
				off = size + 1;
			}
			off += len;
		} else {
			log_printf(1, "\\n******* ERROR: dae segment does not have the expected header!\\n");
			off = size;
		}
	}
	return n == 2;
}
'''


def variants():
    for k, t in TESTS.items():
        yield 'one|' + k, HEAD + t + VD

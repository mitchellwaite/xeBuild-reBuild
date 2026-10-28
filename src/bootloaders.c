/* bootloaders: CB/CF/CD/CE decryption, pairing, FCRT, bootloader signature
   checks.  gcc emits a function's literals in expand-time block order, so
   the original's .rdata order shows its shape: cb/cd/ceDecrypt and
   fcrtVerifySig test for success and log their errors last. */
#include <stdlib.h>
#include <string.h>

#include "crypto/xecrypt.h"
#include "xebuild.h"
#include "bootloaders.h"
#include "fileutil.h"
#include "keys.h"
#include "log.h"
#include "xboxrom.h"

int fcrtVerifySig(uint8_t *fcrt);

#define BL_MAGIC(p, c) (((p)[0] & 0x43) == 0x43 && (p)[1] == (c))
#define BL_SIZE(p) ((getBeU32((p) + 12) + 15) & ~15)

int verifyExtended(uint8_t *buf, uint32_t size)
{
	uint8_t salt[2] = { 7, 0x12 };
	uint8_t key[16];

	XeCryptHmacSha(xb.cpuKey, 16, buf, 16, 0, 0, 0, 0, key, 16);
	XeCryptRc4(key, 16, buf + 16, size - 16);
	XeCryptHmacSha(xb.cpuKey, 16, buf + 16, size - 16, salt, 2, 0, 0, key, 16);
	return memcmp(buf, key, 16) == 0;
}

int unscramble(uint8_t *buf, uint32_t len)
{
	uint8_t s[4] = { 'B', 'u', 'N', 'y' };
	uint32_t i, j = 0;
	int t;

	for (i = 0; i < len; i++) {
		t = buf[i] * 251;
		buf[i] ^= s[j];
		j = (j + 1) & 3;
		s[j] += t;
		s[(j + 1) & 3] += t >> 8;
	}
	return checkZeros(buf + len - 4, 4);
}

uint32_t cbGetPairing(uint8_t *cb)
{
	uint32_t pairing = 0;
	uint32_t len;
	uint8_t *buf;
	uint8_t key[16];

	if (BL_MAGIC(cb, 'B')) {
		len = BL_SIZE(cb);
		buf = malloc(len);
		memcpy(buf, cb, len);
		XeCryptHmacSha(xb.key1bl, 16, cb + 16, 16, 0, 0, 0, 0, key, 16);
		XeCryptRc4(key, 16, buf + 32, len - 32);
		if (checkZeros(buf + 0x270, 0x120)) {
			pairing = getBeU32(buf + 32) & 0xffffff00;
			log_printf(1, "CB decrypted OK, pairing bytes extracted as: 0x%08x\n", pairing);
		} else
			log_printf(0, "***** WARNING: CB decrypt failed! Unable to get pairing data!\n");
		free(buf);
	}
	return pairing;
}

uint32_t cfGetPairing(uint8_t *cf, uint32_t size)
{
	uint32_t len;
	uint8_t key[16];

	if (BL_MAGIC(cf, 'F')) {
		len = BL_SIZE(cf);
		if (size >= len) {
			XeCryptHmacSha(xb.key1bl, 16, cf + 32, 16, 0, 0, 0, 0, key, 16);
			XeCryptRc4(key, 16, cf + 48, len - 48);
			if (checkZeros(cf + 496, 32))
				return getBeU32(cf + 540);
		}
		return 0;
	}
	return 0;
}

uint32_t cfBestPairing(uint8_t *data, uint32_t size)
{
	uint8_t *buf;
	uint32_t p0, p1;
	uint8_t ldv0 = 0, ldv1 = 0;

	if (size > 0x20000)
		return 0;
	buf = malloc(size);
	memcpy(buf, data, size);
	p0 = cfGetPairing(buf, size);
	if (p0) {
		ldv0 = p0;
		log_printf(1, "CF slot 0 decrypted ok LDV 0x%02x Pairing: 0x%06x\n", ldv0, p0 >> 8);
	}
	memcpy(buf, data + size, size);
	p1 = cfGetPairing(buf, size);
	if (p1) {
		ldv1 = p1;
		log_printf(1, "CF slot 1 decrypted ok LDV 0x%02x Pairing: 0x%06x\n", ldv1, p1 >> 8);
	}
	free(buf);
	if (ldv1 >= ldv0)
		p0 = p1;
	return p0;
}

/* decrypt a CF in place with the 1BL key; 1 if it checks out */
/* no DOM/VRP: they fold ok to 0 on the false edge and the result becomes a
   setne; the original keeps `ok` there and if-converts to cmovne */
__attribute__((optimize("no-tree-dominator-opts", "no-tree-vrp")))
int cfDecrypt(uint8_t *cf, uint32_t size)
{
	uint32_t len;
	uint8_t key[16];
	int ok;

	if (BL_MAGIC(cf, 'F')) {
		len = BL_SIZE(cf);
		if (len <= size) {
			XeCryptHmacSha(xb.key1bl, 16, cf + 32, 16, 0, 0, 0, 0, key, 16);
			XeCryptRc4(key, 16, cf + 48, len - 48);
			ok = checkZeros(cf + 496, 32);
			if (ok)
				ok = 1;
			return ok;
		}
	}
	return 0;
}

int cgDecrypt(uint8_t *cg, uint8_t *cfKey, uint32_t size)
{
	uint8_t key[16];

	XeCryptHmacSha(cfKey, 16, cg + 16, 16, 0, 0, 0, 0, key, 16);
	XeCryptRc4(key, 16, cg + 32, size - 32);
	return getBeU32(cg + 32) == 0x120000;
}

int verifySecdata(uint8_t *buf, uint32_t size)
{
	uint8_t key[16];
	uint8_t hash[16];

	memset(hash, 0, 16);
	XeCryptHmacSha(xb.cpuKey, 16, buf, 16, 0, 0, 0, 0, key, 16);
	XeCryptRc4(key, 16, buf + 16, size - 16);
	XeCryptHmacSha(xb.cpuKey, 16, buf + 16, size - 16, 0, 0, 0, 0, hash, 16);
	return memcmp(buf, hash, 16) == 0;
}

int crlVerifySig(uint8_t *crl, uint8_t *hash)
{
	int ok;

	if (!xb.pubPirs)
		return 1;
	if (getBeU32(crl) != 0x43524c50)	/* "CRLP" */
		return 1;
	ok = XeKeysPkcs1Verify(hash, crl + 32, xb.pubPirs);
	if (ok)
		log_printf(1, "sig good! ");
	else
		log_printf(1, "\nsignature check FAILED!\n");
	return ok;
}

int verifyCrl(uint8_t *crl, uint32_t size, int perBox)
{
	uint8_t key[16];
	uint8_t iv[16];
	uint8_t hash[20];
	XECRYPT_AES_STATE aes;

	if (perBox)
		XeCryptAesKey(&aes, xb.cpuKey);
	else
		XeCryptAesKey(&aes, xb.key28c);
	XeCryptAesEcb(&aes, crl + 304, key, 0);
	memcpy(crl + 304, key, 16);
	XeCryptAesKey(&aes, key);
	memcpy(iv, crl + 288, 16);
	XeCryptAesCbc(&aes, crl + 320, 16, crl + 320, iv, 0);
	XeCryptAesCbc(&aes, crl + 336, size - 336, crl + 336, iv, 0);
	if (shaCheck(crl, size, 12, 20, 336, hash)) {
		crlVerifySig(crl, hash);
		return 1;
	}
	return 0;
}

/* not cloned for verifyDae's perBox = 1 call */
__attribute__((noclone)) void daeDecrypt(uint8_t *dae, uint32_t size, int perBox)
{
	uint8_t *buf;
	uint8_t iv[16];
	XECRYPT_AES_STATE aes;

	buf = malloc(size);
	memcpy(buf, dae, size);
	memset(iv, 0, 16);
	if (perBox)
		XeCryptAesKey(&aes, xb.cpuKey);
	else
		XeCryptAesKey(&aes, xb.key28c);
	XeCryptAesCbc(&aes, buf + 304, size - 304, dae + 304, iv, 0);
	free(buf);
}

static void hint(int *p) { *p = 1; }

/* check one DAE segment's signature (1 if no key or too short).  ifcombine
   merges the size test with !xb.pubPirs and the pair keeps the size test's
   probability; the hint call (PRED_CALL; once inlined, its store to a dead
   local goes) lowers it so the FAIL block comes before the !xb.pubPirs return */
__attribute__((optimize("no-early-inlining")))
int daeVerifySig(uint8_t *seg, uint32_t size, int n)
{
	uint8_t key[16];
	uint8_t hash[20];
	int ok, dead;

	if (!xb.pubPirs)
		return 1;
	if (size < 288) {
		hint(&dead);
		return 1;
	}
	memset(key, 0, 16);
	XeCryptHmacSha(key, 16, seg, 32, 0, 0, 0, 0, hash, 20);
	ok = XeKeysPkcs1Verify(hash, seg + 32, xb.pubPirs);
	/* the original's .rdata has "good" before "FAIL" (verifyDae's order) */
	__asm__("" :: "i"("sig %d good! "));
	if (!ok)
		log_printf(1, "\nsig %d FAIL! ", n);
	else
		log_printf(1, "sig %d good! ", n);
	return ok;
}

/* check and decrypt the two DAEP segments of a DAE file */
/* daeVerifySig as verifyDae inlines it: `if (ok)` first, inlined before
   profile estimation (the standalone daeVerifySig tests !ok first) */
static inline __attribute__((always_inline)) int daeSigCheck(uint8_t *seg, uint32_t size, int n)
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
	ok = XeKeysPkcs1Verify(hash, seg + 32, xb.pubPirs);
	if (ok)
		log_printf(1, "sig %d good! ", n);
	else
		log_printf(1, "\nsig %d FAIL! ", n);
	return ok;
}

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
			daeSigCheck(seg, len, n);
			daeDecrypt(seg, len, 1);
			if (!shaCheck(seg, len, 12, 20, 336, 0)) {
				log_printf(1, "\n******* ERROR: dae hash incorrect, could not decrypt!\n");
				n = 0;
				off = size + 1;
			}
			off += len;
		} else {
			log_printf(1, "\n******* ERROR: dae segment does not have the expected header!\n");
			off = size;
		}
	}
	return n == 2;
}

/* inlined into verifyFcrt before profile estimation; the prototype above
   keeps the external definition */
inline __attribute__((always_inline)) int fcrtVerifySig(uint8_t *fcrt)
{
	uint8_t hash[20];
	void *pub;
	int ok;

	pub = (getBeU32(fcrt + 272) & 0x80000000) ? xb.pubPirs : xb.masterPub;
	if (pub) {
		XeCryptHmacSha(xb.cpuKey, 16, fcrt + 256, 64, 0, 0, 0, 0, hash, 20);
		ok = XeKeysPkcs1Verify(hash, fcrt, pub);
		if (ok)
			log_printf(1, "sig good! ");
		else
			log_printf(1, "\nsignature FAILED!\n");
		return ok;
	}
	log_printf(1, "pub key to verify signature is not available, skipping!\n");
	return 1;
}

/* check an FCRT's signature, then decrypt it with the CPU key */
int verifyFcrt(uint8_t *fcrt, uint32_t size)
{
	uint8_t iv[16];
	uint8_t hash[20];
	XECRYPT_AES_STATE aes;
	uint32_t off;

	fcrtVerifySig(fcrt);
	memcpy(iv, fcrt + 256, 16);
	if (size != 0x4000) {
		log_printf(1, "**** ERROR: FCRT decrypt invalid size!\n");
		return 0;
	}
	off = getBeU32(fcrt + 284);
	if (off >= 0x4000) {
		log_printf(1, "**** ERROR: FCRT decrypt invalid offset!\n");
		return 0;
	}
	XeCryptSha(fcrt + off, size - off, 0, 0, 0, 0, hash, 20);
	if (!memcmp(fcrt + 300, hash, 20)) {
		log_printf(1, "FCRT was already decrypted...");
		return 1;
	}
	XeCryptAesKey(&aes, xb.cpuKey);
	XeCryptAesCbc(&aes, fcrt + off, size - off, fcrt + off, iv, 0);
	XeCryptSha(fcrt + off, size - off, 0, 0, 0, 0, hash, 20);
	if (memcmp(fcrt + 300, hash, 20)) {
		log_printf(1, "\n******* ERROR: FCRT hash check failed, could not decrypt!\n");
		return 0;
	}
	return 1;
}

int shaSelfCheck(uint8_t *p)
{
	uint8_t hash[20];

	XeCryptSha(p + 20, 492, 0, 0, 0, 0, hash, 20);
	return memcmp(hash, p, 20) == 0;
}

/* decrypted copy of a CB/SB (free it), checked against the 1BL RSA key */
uint8_t *cbDecrypt(uint8_t *cb, uint32_t *outLen, uint8_t *outKey);
/* stops DOM/uncprop and CSE proving buf == 0 on the calloc-fail path (the
   original keeps its `xor ebx,ebx` there); `if (buf)` first keeps
   postreload from learning it from the jump */
__attribute__((optimize("no-tree-dominator-opts", "no-cse-follow-jumps")))
uint8_t *cbDecrypt(uint8_t *cb, uint32_t *outLen, uint8_t *outKey)
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
						log_printf(1, "%cB signature OK! Decryption successful!\n", buf[0]);
						if (outLen)
							*outLen = len;
					} else {
						log_printf(0, "***** ERROR: %cB signature invalid, corrupted or decryption failed!\n", buf[0]);
						free(buf);
						buf = 0;
					}
				} else {
					log_printf(0, "***** WARNING: could not check %cB signature, 1BL RSA key not loaded!\n", buf[0]);
					if (outLen)
						*outLen = len;
				}
				return buf;
			}
			log_printf(0, "***** WARNING: Unable to allocate 0x%x bytes for %c%c!\n", cb[0], cb[1]);
		} else
			log_printf(0, "***** WARNING: CB/SB does not have valid magic!\n");
	} else
		log_printf(0, "***** WARNING: CB/SB decrypt not provided with data!\n");
	return 0;
}

/* decrypted copy of an SC/SD/CD with hmacKey, signature checked if pubKey and salt */
uint8_t *cdDecrypt(uint8_t *bl, const void *pubKey, const uint8_t *salt, const uint8_t *hmacKey,
	uint32_t *outLen, uint8_t *outKey);
/* as cbDecrypt */
__attribute__((optimize("no-tree-dominator-opts", "no-cse-follow-jumps")))
uint8_t *cdDecrypt(uint8_t *bl, const void *pubKey, const uint8_t *salt, const uint8_t *hmacKey, uint32_t *outLen, uint8_t *outKey)
{
	uint8_t *buf;
	uint32_t len;
	uint8_t key[16];

	if (bl && hmacKey) {
		if ((bl[0] & 0x43) == 0x43 && (bl[1] == 'C' || bl[1] == 'D')) {
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
						log_printf(1, "%c%c signature OK! Decryption successful!\n", buf[0], buf[1]);
						if (outLen)
							*outLen = len;
					} else {
						log_printf(0, "***** ERROR: %c%c signature invalid, corrupted or decryption failed!\n", buf[0], buf[1]);
						free(buf);
						buf = 0;
					}
				} else {
					log_printf(0, "***** WARNING: could not check %c%c signature, 1BL RSA key not loaded!\n", buf[0], buf[1]);
					if (outLen)
						*outLen = len;
				}
				return buf;
			}
			log_printf(0, "***** WARNING: Unable to allocate 0x%x bytes for %c%c!\n", bl[0], bl[1]);
		} else
			log_printf(0, "***** WARNING: SC/SD/CD does not have valid magic!\n");
	} else
		log_printf(0, "***** WARNING: SC/SD/CD decrypt not provided with data!\n");
	return 0;
}

/* decrypted copy of an SE/CE with hmacKey, hash checked if given; as
   cbDecrypt, plus register pins (in a block jump threading removes) that
   keep IRA's original choice: bl ebp, hmacKey edi, len esi */
__attribute__((optimize("no-tree-dominator-opts", "no-cse-follow-jumps")))
uint8_t *ceDecrypt(uint8_t *bl, uint32_t *outLen, const uint8_t *hmacKey, const uint8_t *hash)
{
	uint8_t *buf;
	uint32_t len;
	uint8_t key[16];

	if (bl && hmacKey) {
		if (BL_MAGIC(bl, 'E')) {
			len = BL_SIZE(bl);
			buf = calloc(len, 1);
			if (buf)
				__asm__("" :: "S"(len), "D"(hmacKey));
			if (buf) {
				memcpy(buf, bl, len);
				XeCryptHmacSha(hmacKey, 16, buf + 16, 16, 0, 0, 0, 0, key, 16);
				XeCryptRc4(key, 16, buf + 32, len - 32);
				if (hash) {
					if (blCheckHash(buf, len, hash)) {
						log_printf(1, "%c%c hash check OK! Decryption successful!\n", buf[0], buf[1]);
						if (outLen)
							*outLen = len;
					} else {
						log_printf(0, "***** ERROR: %c%c hash check invalid, corrupted or decryption failed!\n", buf[0], buf[1]);
						free(buf);
						buf = 0;
					}
				} else {
					log_printf(0, "***** WARNING: could not check %cE signature, 1BL RSA key not loaded!\n", buf[0]);
					if (outLen)
						*outLen = len;
				}
				return buf;
			}
			log_printf(0, "***** WARNING: Unable to allocate 0x%x bytes for %cE!\n", bl[0]);
		} else
			log_printf(0, "***** WARNING: SE/CE does not have valid magic!\n");
	} else
		log_printf(0, "***** WARNING: SE/CE decrypt not provided with data!\n");
	return 0;
}

/* the object's strings and unwind info (FDEs for every function) */

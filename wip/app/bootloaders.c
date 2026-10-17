/* bootloaders: CB/CF/CD/CE decryption, pairing, FCRT, bootloader signature checks */
#include <stdlib.h>
#include <string.h>

typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;

/* XeCrypt's XECRYPT_AES_STATE (two Gladman contexts) */
typedef struct {
	u32 ctx[2][61];
} AESSTATE;

void XeCryptHmacSha(const u8 *pbKey, u32 cbKey, const u8 *pbInp1, u32 cbInp1,
	const u8 *pbInp2, u32 cbInp2, const u8 *pbInp3, u32 cbInp3,
	u8 *pbOut, u32 cbOut);
void XeCryptRc4(const u8 *pbKey, u32 cbKey, u8 *pbInpOut, u32 cbInpOut);
void XeCryptSha(const u8 *pbInp1, u32 cbInp1, const u8 *pbInp2, u32 cbInp2,
	const u8 *pbInp3, u32 cbInp3, u8 *pbOut, u32 cbOut);
void XeCryptAesKey(AESSTATE *pAesState, const u8 *pbKey);
void XeCryptAesEcb(AESSTATE *pAesState, const u8 *pbInp, u8 *pbOut, int fEncrypt);
void XeCryptAesCbc(AESSTATE *pAesState, const u8 *pbInp, u32 cbInp, u8 *pbOut,
	u8 *pbFeed, int fEncrypt);
int XeKeysPkcs1Verify(const u8 *pbHash, const u8 *pbSig, const void *pRsaPub);
void log_printf(int level, const char *fmt, ...);
u32 getBeU32(const u8 *p);
int checkZeros(const u8 *p, u32 len);
int cbVerifySig(u8 *bl, const void *pubKey);
int blVerifySig(u8 *bl, unsigned int len, const void *pubKey, const u8 *salt);
int blCheckHash(u8 *bl, unsigned int len, const u8 *expect);
int shaCheck(u8 *buf, u32 size, u32 hashOff, u32 hashLen, u32 dataOff, u8 *hashOut);
int fcrtVerifySig(u8 *fcrt);

extern u8 key1bl[16];
extern u8 cpuKey[16];
extern u8 key28c[16];
extern void *pub1bl;
extern void *masterPub;
extern void *pub2a4;

#define BL_MAGIC(p, c) (((p)[0] & 0x43) == 0x43 && (p)[1] == (c))
#define BL_SIZE(p) ((getBeU32((p) + 12) + 15) & ~15)

int verifyExtended(u8 *buf, u32 size)
{
	u8 salt[2] = { 7, 0x12 };
	u8 key[16];

	XeCryptHmacSha(cpuKey, 16, buf, 16, 0, 0, 0, 0, key, 16);
	XeCryptRc4(key, 16, buf + 16, size - 16);
	XeCryptHmacSha(cpuKey, 16, buf + 16, size - 16, salt, 2, 0, 0, key, 16);
	return memcmp(buf, key, 16) == 0;
}

int unscramble(u8 *buf, u32 len)
{
	u8 s[4] = { 'B', 'u', 'N', 'y' };
	u32 i, j = 0;
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

u32 cbGetPairing(u8 *cb)
{
	u32 pairing = 0;
	u32 len;
	u8 *buf;
	u8 key[16];

	if (BL_MAGIC(cb, 'B')) {
		len = BL_SIZE(cb);
		buf = malloc(len);
		memcpy(buf, cb, len);
		XeCryptHmacSha(key1bl, 16, cb + 16, 16, 0, 0, 0, 0, key, 16);
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

u32 cfGetPairing(u8 *cf, u32 size)
{
	u32 len;
	u8 key[16];

	if (BL_MAGIC(cf, 'F')) {
		len = BL_SIZE(cf);
		if (size >= len) {
			XeCryptHmacSha(key1bl, 16, cf + 32, 16, 0, 0, 0, 0, key, 16);
			XeCryptRc4(key, 16, cf + 48, len - 48);
			if (checkZeros(cf + 496, 32))
				return getBeU32(cf + 540);
		}
		return 0;
	}
	return 0;
}

u32 cfBestPairing(u8 *data, u32 size)
{
	u8 *buf;
	u32 p0, p1;
	u8 ldv0 = 0, ldv1 = 0;

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

/* no DOM/VRP: they fold ok to 0 on the false edge and the result becomes a
   setne; the original keeps `ok` there and if-converts to cmovne */
__attribute__((optimize("no-tree-dominator-opts", "no-tree-vrp")))
int cfDecrypt(u8 *cf, u32 size)
{
	u32 len;
	u8 key[16];
	int ok;

	if (BL_MAGIC(cf, 'F')) {
		len = BL_SIZE(cf);
		if (len <= size) {
			XeCryptHmacSha(key1bl, 16, cf + 32, 16, 0, 0, 0, 0, key, 16);
			XeCryptRc4(key, 16, cf + 48, len - 48);
			ok = checkZeros(cf + 496, 32);
			if (ok)
				ok = 1;
			return ok;
		}
	}
	return 0;
}

int cgDecrypt(u8 *cg, u8 *cfKey, u32 size)
{
	u8 key[16];

	XeCryptHmacSha(cfKey, 16, cg + 16, 16, 0, 0, 0, 0, key, 16);
	XeCryptRc4(key, 16, cg + 32, size - 32);
	return getBeU32(cg + 32) == 0x120000;
}

int verifySecdata(u8 *buf, u32 size)
{
	u8 key[16];
	u8 hash[16];

	memset(hash, 0, 16);
	XeCryptHmacSha(cpuKey, 16, buf, 16, 0, 0, 0, 0, key, 16);
	XeCryptRc4(key, 16, buf + 16, size - 16);
	XeCryptHmacSha(cpuKey, 16, buf + 16, size - 16, 0, 0, 0, 0, hash, 16);
	return memcmp(buf, hash, 16) == 0;
}

int crlVerifySig(u8 *crl, u8 *hash)
{
	int ok;

	if (!pub2a4)
		return 1;
	if (getBeU32(crl) != 0x43524c50)	/* "CRLP" */
		return 1;
	ok = XeKeysPkcs1Verify(hash, crl + 32, pub2a4);
	if (ok)
		log_printf(1, "sig good! ");
	else
		log_printf(1, "\nsignature check FAILED!\n");
	return ok;
}

int verifyCrl(u8 *crl, u32 size, int perBox)
{
	u8 key[16];
	u8 iv[16];
	u8 hash[20];
	AESSTATE aes;

	if (perBox)
		XeCryptAesKey(&aes, cpuKey);
	else
		XeCryptAesKey(&aes, key28c);
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
__attribute__((noclone)) void daeDecrypt(u8 *dae, u32 size, int perBox)
{
	u8 *buf;
	u8 iv[16];
	AESSTATE aes;

	buf = malloc(size);
	memcpy(buf, dae, size);
	memset(iv, 0, 16);
	if (perBox)
		XeCryptAesKey(&aes, cpuKey);
	else
		XeCryptAesKey(&aes, key28c);
	XeCryptAesCbc(&aes, buf + 304, size - 304, dae + 304, iv, 0);
	free(buf);
}

int daeVerifySig(u8 *seg, u32 size, int n)
{
	u8 key[16];
	u8 hash[20];
	int ok;

	if (!pub2a4)
		return 1;
	if (size < 288)
		return 1;
	memset(key, 0, 16);
	XeCryptHmacSha(key, 16, seg, 32, 0, 0, 0, 0, hash, 20);
	ok = XeKeysPkcs1Verify(hash, seg + 32, pub2a4);
	if (!ok)
		log_printf(1, "\nsig %d FAIL! ", n);
	else
		log_printf(1, "sig %d good! ", n);
	return ok;
}

/* daeVerifySig as verifyDae inlines it: `if (ok)` first, inlined before
   profile estimation (the standalone daeVerifySig tests !ok first) */
static inline __attribute__((always_inline)) int daeSigCheck(u8 *seg, u32 size, int n)
{
	u8 key[16];
	u8 hash[20];
	int ok;

	if (!pub2a4)
		return 1;
	if (size < 288)
		return 1;
	memset(key, 0, 16);
	XeCryptHmacSha(key, 16, seg, 32, 0, 0, 0, 0, hash, 20);
	ok = XeKeysPkcs1Verify(hash, seg + 32, pub2a4);
	if (ok)
		log_printf(1, "sig %d good! ", n);
	else
		log_printf(1, "\nsig %d FAIL! ", n);
	return ok;
}

int verifyDae(u8 *buf, u32 size)
{
	u32 off = 0;
	u32 len;
	u8 *seg;
	int n = 0;

	while (off < size) {
		seg = buf + off;
		if (buf[off] == 'D' && buf[off + 1] == 'A' && buf[off + 2] == 'E' && buf[off + 3] == 'P') {
			len = (u16)((buf[off + 4] << 8) + buf[off + 5]);
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
inline __attribute__((always_inline)) int fcrtVerifySig(u8 *fcrt)
{
	u8 hash[20];
	void *pub;
	int ok;

	pub = (getBeU32(fcrt + 272) & 0x80000000) ? pub2a4 : masterPub;
	if (!pub) {
		log_printf(1, "pub key to verify signature is not available, skipping!\n");
		return 1;
	}
	XeCryptHmacSha(cpuKey, 16, fcrt + 256, 64, 0, 0, 0, 0, hash, 20);
	ok = XeKeysPkcs1Verify(hash, fcrt, pub);
	if (ok)
		log_printf(1, "sig good! ");
	else
		log_printf(1, "\nsignature FAILED!\n");
	return ok;
}

int verifyFcrt(u8 *fcrt, u32 size)
{
	u8 iv[16];
	u8 hash[20];
	AESSTATE aes;
	u32 off;

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
	XeCryptAesKey(&aes, cpuKey);
	XeCryptAesCbc(&aes, fcrt + off, size - off, fcrt + off, iv, 0);
	XeCryptSha(fcrt + off, size - off, 0, 0, 0, 0, hash, 20);
	if (memcmp(fcrt + 300, hash, 20)) {
		log_printf(1, "\n******* ERROR: FCRT hash check failed, could not decrypt!\n");
		return 0;
	}
	return 1;
}

int shaSelfCheck(u8 *p)
{
	u8 hash[20];

	XeCryptSha(p + 20, 492, 0, 0, 0, 0, hash, 20);
	return memcmp(hash, p, 20) == 0;
}

/* stops DOM/uncprop and CSE proving buf == 0 on the calloc-fail path (the
   original keeps its `xor ebx,ebx` there); `if (buf)` first keeps
   postreload from learning it from the jump */
__attribute__((optimize("no-tree-dominator-opts", "no-cse-follow-jumps")))
u8 *cbDecrypt(u8 *cb, u32 *outLen, u8 *outKey)
{
	u8 *buf;
	u32 len;
	u8 key[16];

	if (!cb) {
		log_printf(0, "***** WARNING: CB/SB decrypt not provided with data!\n");
		return 0;
	}
	if (!BL_MAGIC(cb, 'B')) {
		log_printf(0, "***** WARNING: CB/SB does not have valid magic!\n");
		return 0;
	}
	len = BL_SIZE(cb);
	buf = calloc(len, 1);
	if (buf) {
		memcpy(buf, cb, len);
		XeCryptHmacSha(key1bl, 16, buf + 16, 16, 0, 0, 0, 0, key, 16);
		XeCryptRc4(key, 16, buf + 32, len - 32);
		if (outKey)
			memcpy(outKey, key, 16);
		if (pub1bl) {
			if (cbVerifySig(buf, pub1bl)) {
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
	return 0;
}

/* as cbDecrypt */
__attribute__((optimize("no-tree-dominator-opts", "no-cse-follow-jumps")))
u8 *cdDecrypt(u8 *bl, const void *pubKey, const u8 *salt, const u8 *hmacKey, u32 *outLen, u8 *outKey)
{
	u8 *buf;
	u32 len;
	u8 key[16];

	if (!bl || !hmacKey) {
		log_printf(0, "***** WARNING: SC/SD/CD decrypt not provided with data!\n");
		return 0;
	}
	if ((bl[0] & 0x43) != 0x43 || (bl[1] != 'C' && bl[1] != 'D')) {
		log_printf(0, "***** WARNING: SC/SD/CD does not have valid magic!\n");
		return 0;
	}
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
	return 0;
}

u8 *ceDecrypt(u8 *bl, u32 *outLen, const u8 *hmacKey, const u8 *hash)
{
	u8 *buf;
	u32 len;
	u8 key[16];

	if (!bl || !hmacKey) {
		log_printf(0, "***** WARNING: SE/CE decrypt not provided with data!\n");
		return 0;
	}
	if (!BL_MAGIC(bl, 'E')) {
		log_printf(0, "***** WARNING: SE/CE does not have valid magic!\n");
		return 0;
	}
	len = BL_SIZE(bl);
	buf = calloc(len, 1);
	if (!buf) {
		log_printf(0, "***** WARNING: Unable to allocate 0x%x bytes for %cE!\n", bl[0]);
		return 0;
	}
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

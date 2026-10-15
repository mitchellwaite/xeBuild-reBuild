/* bootloaders: CB/CF/CD/CE decryption, pairing, FCRT, bootloader signature
   checks.  Mixed object: the functions here are spliced into bootloaders.s
   (re/splice.py), which still holds the rest and the data, so string
   literals are extern names for the .s's strings.  The whole draft, with
   literals, is wip/app/bootloaders.c. */
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
int shaCheck(u8 *buf, u32 size, u32 hashOff, u32 hashLen, u32 dataOff, u8 *hashOut);

extern u8 key1bl[16];
extern u8 cpuKey[16];
extern u8 key28c[16];
extern void *masterPub;
extern void *pub2a4;

/* bootloaders.s strings */
extern const char msg_cbPairOk[];	/* "CB decrypted OK, pairing bytes extracted as: 0x%08x\n" */
extern const char msg_cbPairFail[];	/* "***** WARNING: CB decrypt failed! Unable to get pairing data!\n" */
extern const char msg_cfSlot0[];	/* "CF slot 0 decrypted ok LDV 0x%02x Pairing: 0x%06x\n" */
extern const char msg_cfSlot1[];	/* "CF slot 1 decrypted ok LDV 0x%02x Pairing: 0x%06x\n" */
extern const char msg_sigGood[];	/* "sig good! " */
extern const char msg_sigCheckFail[];	/* "\nsignature check FAILED!\n" */
extern const char msg_sigFail[];	/* "\nsignature FAILED!\n" */
extern const char msg_noPub[];		/* "pub key to verify signature is not available, skipping!\n" */

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
			log_printf(1, msg_cbPairOk, pairing);
		} else
			log_printf(0, msg_cbPairFail);
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
		log_printf(1, msg_cfSlot0, ldv0, p0 >> 8);
	}
	memcpy(buf, data + size, size);
	p1 = cfGetPairing(buf, size);
	if (p1) {
		ldv1 = p1;
		log_printf(1, msg_cfSlot1, ldv1, p1 >> 8);
	}
	free(buf);
	if (ldv1 >= ldv0)
		p0 = p1;
	return p0;
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
		log_printf(1, msg_sigGood);
	else
		log_printf(1, msg_sigCheckFail);
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

void daeDecrypt(u8 *dae, u32 size, int perBox)
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

int fcrtVerifySig(u8 *fcrt)
{
	u8 hash[20];
	void *pub;
	int ok;

	pub = (getBeU32(fcrt + 272) & 0x80000000) ? pub2a4 : masterPub;
	if (!pub) {
		log_printf(1, msg_noPub);
		return 1;
	}
	XeCryptHmacSha(cpuKey, 16, fcrt + 256, 64, 0, 0, 0, 0, hash, 20);
	ok = XeKeysPkcs1Verify(hash, fcrt, pub);
	if (ok)
		log_printf(1, msg_sigGood);
	else
		log_printf(1, msg_sigFail);
	return ok;
}

int shaSelfCheck(u8 *p)
{
	u8 hash[20];

	XeCryptSha(p + 20, 492, 0, 0, 0, 0, hash, 20);
	return memcmp(hash, p, 20) == 0;
}

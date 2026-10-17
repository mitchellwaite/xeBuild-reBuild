/* bootloaders: CB/CF/CD/CE decryption, pairing, FCRT, bootloader signature
   checks.  The functions that don't match in C yet (daeVerifySig,
   ceDecrypt) are top-level __asm__ in place, from the generated asm, and so
   are the object's .rdata strings and .eh_frame; build.sh compiles this
   file with -fno-toplevel-reorder -fno-asynchronous-unwind-tables.  The C
   functions therefore name the strings with extern declarations, not
   literals.  C drafts of the asm functions are in wip/app/bootloaders.c; to
   move one, replace its __asm__ block with the C and keep its trailing
   padding bytes (or drop them where gcc's .p2align gives the same). */
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
int cbVerifySig(u8 *bl, const void *pubKey);
int blVerifySig(u8 *bl, unsigned int len, const void *pubKey, const u8 *salt);
int fcrtVerifySig(u8 *fcrt);

extern u8 key1bl[16];
extern u8 cpuKey[16];
extern u8 key28c[16];
extern void *pub1bl;
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
extern const char msg_daeSigGood[];	/* "sig %d good! " */
extern const char msg_daeSigFail[];	/* "\nsig %d FAIL! " */
extern const char msg_daeHash[];	/* "\n******* ERROR: dae hash incorrect, could not decrypt!\n" */
extern const char msg_daeHeader[];	/* "\n******* ERROR: dae segment does not have the expected header!\n" */
extern const char msg_fcrtSize[];	/* "**** ERROR: FCRT decrypt invalid size!\n" */
extern const char msg_fcrtOffset[];	/* "**** ERROR: FCRT decrypt invalid offset!\n" */
extern const char msg_fcrtDone[];	/* "FCRT was already decrypted..." */
extern const char msg_fcrtHash[];	/* "\n******* ERROR: FCRT hash check failed, could not decrypt!\n" */
extern const char msg_cbSigOk[];	/* "%cB signature OK! Decryption successful!\n" */
extern const char msg_cbSigBad[];	/* "***** ERROR: %cB signature invalid, corrupted or decryption failed!\n" */
extern const char msg_cbNoKey[];	/* "***** WARNING: could not check %cB signature, 1BL RSA key not loaded!\n" */
extern const char msg_allocFail[];	/* "***** WARNING: Unable to allocate 0x%x bytes for %c%c!\n" */
extern const char msg_cbMagic[];	/* "***** WARNING: CB/SB does not have valid magic!\n" */
extern const char msg_cbNoData[];	/* "***** WARNING: CB/SB decrypt not provided with data!\n" */
extern const char msg_cdSigOk[];	/* "%c%c signature OK! Decryption successful!\n" */
extern const char msg_cdSigBad[];	/* "***** ERROR: %c%c signature invalid, corrupted or decryption failed!\n" */
extern const char msg_cdNoKey[];	/* "***** WARNING: could not check %c%c signature, 1BL RSA key not loaded!\n" */
extern const char msg_cdMagic[];	/* "***** WARNING: SC/SD/CD does not have valid magic!\n" */
extern const char msg_cdNoData[];	/* "***** WARNING: SC/SD/CD decrypt not provided with data!\n" */

#define BL_MAGIC(p, c) (((p)[0] & 0x43) == 0x43 && (p)[1] == (c))
#define BL_SIZE(p) ((getBeU32((p) + 12) + 15) & ~15)

__asm__(
	".intel_syntax noprefix\n"
	"	.globl _cbDecrypt\n"
	"	.globl _cdDecrypt\n"
	"	.globl _ceDecrypt\n"
	"	.globl _cfDecrypt\n"
	"	.globl _daeVerifySig\n"
	"	.globl _msg_cbPairFail\n"
	"	.globl _msg_cbPairOk\n"
	"	.globl _msg_cfSlot0\n"
	"	.globl _msg_cfSlot1\n"
	"	.globl _msg_noPub\n"
	"	.globl _msg_sigCheckFail\n"
	"	.globl _msg_sigFail\n"
	"	.globl _msg_sigGood\n"
	"	.globl _verifyDae\n"
	"	.globl _verifyFcrt\n"
	"\n"
	".text\n"
	"	.p2align 4\n"
	".text\n"
	".att_syntax\n");

int verifyExtended(u8 *buf, u32 size)
{
	u8 salt[2] = { 7, 0x12 };
	u8 key[16];

	XeCryptHmacSha(cpuKey, 16, buf, 16, 0, 0, 0, 0, key, 16);
	XeCryptRc4(key, 16, buf + 16, size - 16);
	XeCryptHmacSha(cpuKey, 16, buf + 16, size - 16, salt, 2, 0, 0, key, 16);
	return memcmp(buf, key, 16) == 0;
}

__asm__(
	".intel_syntax noprefix\n"
	"	.byte 0x8d\n"
	"	.byte 0xb6\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x8d\n"
	"	.byte 0xbc\n"
	"	.byte 0x27\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	".text\n"
	".att_syntax\n");

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

__asm__(
	".intel_syntax noprefix\n"
	"	.byte 0x8d\n"
	"	.byte 0x76\n"
	"	.byte 0x0\n"
	"	.byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]\n"
	".text\n"
	".att_syntax\n");

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

__asm__(
	".intel_syntax noprefix\n"
	"	.byte 0x8d\n"
	"	.byte 0xb6\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x8d\n"
	"	.byte 0xbc\n"
	"	.byte 0x27\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	".text\n"
	".att_syntax\n");

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

__asm__(
	".intel_syntax noprefix\n"
	"	.byte 0x8d\n"
	"	.byte 0x74\n"
	"	.byte 0x26\n"
	"	.byte 0x0\n"
	"	.byte 0x8d\n"
	"	.byte 0xbc\n"
	"	.byte 0x27\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	".text\n"
	".att_syntax\n");

/* decrypt a CF in place with the 1BL key; 1 if it checks out */
int cfDecrypt(u8 *cf, u32 size);
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

__asm__(
	".intel_syntax noprefix\n"
	"	.byte 0x8d\n"
	"	.byte 0xb6\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x8d\n"
	"	.byte 0xbc\n"
	"	.byte 0x27\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	".text\n"
	".att_syntax\n");

int cgDecrypt(u8 *cg, u8 *cfKey, u32 size)
{
	u8 key[16];

	XeCryptHmacSha(cfKey, 16, cg + 16, 16, 0, 0, 0, 0, key, 16);
	XeCryptRc4(key, 16, cg + 32, size - 32);
	return getBeU32(cg + 32) == 0x120000;
}

__asm__(
	".intel_syntax noprefix\n"
	"L_401e57:\n"
	"	mov ESI,ESI\n"
	"	.byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]\n"
	".text\n"
	".att_syntax\n");

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

__asm__(
	".intel_syntax noprefix\n"
	"	.byte 0x90\n"
	"	.byte 0x8d\n"
	"	.byte 0x74\n"
	"	.byte 0x26\n"
	"	.byte 0x0\n"
	".text\n"
	".att_syntax\n");

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

__asm__(
	".intel_syntax noprefix\n"
	"	.byte 0x8d\n"
	"	.byte 0x74\n"
	"	.byte 0x26\n"
	"	.byte 0x0\n"
	".text\n"
	".att_syntax\n");

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

__asm__(
	".intel_syntax noprefix\n"
	"	.byte 0x8d\n"
	"	.byte 0x76\n"
	"	.byte 0x0\n"
	"	.byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]\n"
	".text\n"
	".att_syntax\n");

/* check one DAE segment's signature (1 if no key or too short) */
int daeVerifySig(u8 *seg, u32 size, int n);
__asm__(
	".intel_syntax noprefix\n"
	"_daeVerifySig:\n"
	"	mov EAX,DWORD PTR [_pub2a4]\n"
	"	test EAX,EAX\n"
	"	je L_402400\n"
	"	push EBX\n"
	"	mov EAX,1\n"
	"	sub ESP,120\n"
	"	cmp DWORD PTR [ESP+132],287\n"
	"	jbe L_4023d8\n"
	"	mov EDX,DWORD PTR [ESP+128]\n"
	"	lea EAX,DWORD PTR [ESP+76]\n"
	"	lea EBX,DWORD PTR [ESP+92]\n"
	"	mov DWORD PTR [ESP+36],20\n"
	"	mov DWORD PTR [ESP+28],0\n"
	"	mov DWORD PTR [ESP],EAX\n"
	"	mov DWORD PTR [ESP+32],EBX\n"
	"	mov DWORD PTR [ESP+8],EDX\n"
	"	mov DWORD PTR [ESP+24],0\n"
	"	mov DWORD PTR [ESP+20],0\n"
	"	mov DWORD PTR [ESP+16],0\n"
	"	mov DWORD PTR [ESP+12],32\n"
	"	mov DWORD PTR [ESP+4],16\n"
	"	mov DWORD PTR [ESP+76],0\n"
	"	mov DWORD PTR [ESP+80],0\n"
	"	mov DWORD PTR [ESP+84],0\n"
	"	mov DWORD PTR [ESP+88],0\n"
	"	call _XeCryptHmacSha\n"
	"	mov EAX,DWORD PTR [_pub2a4]\n"
	"	mov DWORD PTR [ESP],EBX\n"
	"	mov DWORD PTR [ESP+8],EAX\n"
	"	mov EAX,DWORD PTR [ESP+128]\n"
	"	add EAX,32\n"
	"	mov DWORD PTR [ESP+4],EAX\n"
	"	call _XeKeysPkcs1Verify\n"
	"	mov DWORD PTR [ESP+60],EAX\n"
	"	test EAX,EAX\n"
	"	mov EAX,DWORD PTR [ESP+136]\n"
	"	mov DWORD PTR [ESP+8],EAX\n"
	"	je L_4023e0\n"
	"	mov DWORD PTR [ESP+4],OFFSET L_44c168\n"
	"	mov DWORD PTR [ESP],1\n"
	"	call _log_printf\n"
	"	mov EAX,DWORD PTR [ESP+60]\n"
	"L_4023d8:\n"
	"	add ESP,120\n"
	"	pop EBX\n"
	"	ret\n"
	"	.byte 0x8d\n"
	"	.byte 0x76\n"
	"	.byte 0x0\n"
	"L_4023e0:\n"
	"	mov DWORD PTR [ESP+4],OFFSET L_44c176\n"
	"	mov DWORD PTR [ESP],1\n"
	"	call _log_printf\n"
	"	mov EAX,DWORD PTR [ESP+60]\n"
	"	add ESP,120\n"
	"	pop EBX\n"
	"	ret\n"
	"	.byte 0x8d\n"
	"	.byte 0x76\n"
	"	.byte 0x0\n"
	"L_402400:\n"
	"	mov EAX,1\n"
	"	ret\n"
	"	.byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]\n"
	"	.byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]\n"
	".text\n"
	".att_syntax\n");

/* check and decrypt the two DAEP segments of a DAE file */
int verifyDae(u8 *buf, u32 size);
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
		log_printf(1, msg_daeSigGood, n);
	else
		log_printf(1, msg_daeSigFail, n);
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
				log_printf(1, msg_daeHash);
				n = 0;
				off = size + 1;
			}
			off += len;
		} else {
			log_printf(1, msg_daeHeader);
			off = size;
		}
	}
	return n == 2;
}

__asm__(
	".intel_syntax noprefix\n"
	"	.byte 0x66\n"
	"	.byte 0x90\n"
	".text\n"
	".att_syntax\n");

/* inlined into verifyFcrt before profile estimation; the prototype above
   keeps the external definition */
inline __attribute__((always_inline)) int fcrtVerifySig(u8 *fcrt)
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

__asm__(
	".intel_syntax noprefix\n"
	"	.byte 0x8d\n"
	"	.byte 0xb4\n"
	"	.byte 0x26\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x8d\n"
	"	.byte 0xbc\n"
	"	.byte 0x27\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	".text\n"
	".att_syntax\n");

/* check an FCRT's signature, then decrypt it with the CPU key */
int verifyFcrt(u8 *fcrt, u32 size);
int verifyFcrt(u8 *fcrt, u32 size)
{
	u8 iv[16];
	u8 hash[20];
	AESSTATE aes;
	u32 off;

	fcrtVerifySig(fcrt);
	memcpy(iv, fcrt + 256, 16);
	if (size != 0x4000) {
		log_printf(1, msg_fcrtSize);
		return 0;
	}
	off = getBeU32(fcrt + 284);
	if (off >= 0x4000) {
		log_printf(1, msg_fcrtOffset);
		return 0;
	}
	XeCryptSha(fcrt + off, size - off, 0, 0, 0, 0, hash, 20);
	if (!memcmp(fcrt + 300, hash, 20)) {
		log_printf(1, msg_fcrtDone);
		return 1;
	}
	XeCryptAesKey(&aes, cpuKey);
	XeCryptAesCbc(&aes, fcrt + off, size - off, fcrt + off, iv, 0);
	XeCryptSha(fcrt + off, size - off, 0, 0, 0, 0, hash, 20);
	if (memcmp(fcrt + 300, hash, 20)) {
		log_printf(1, msg_fcrtHash);
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

__asm__(
	".intel_syntax noprefix\n"
	"	.byte 0x66\n"
	"	.byte 0x90\n"
	".text\n"
	".att_syntax\n");

/* decrypted copy of a CB/SB (free it), checked against the 1BL RSA key */
u8 *cbDecrypt(u8 *cb, u32 *outLen, u8 *outKey);
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
		log_printf(0, msg_cbNoData);
		return 0;
	}
	if (!BL_MAGIC(cb, 'B')) {
		log_printf(0, msg_cbMagic);
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
				log_printf(1, msg_cbSigOk, buf[0]);
				if (outLen)
					*outLen = len;
			} else {
				log_printf(0, msg_cbSigBad, buf[0]);
				free(buf);
				buf = 0;
			}
		} else {
			log_printf(0, msg_cbNoKey, buf[0]);
			if (outLen)
				*outLen = len;
		}
		return buf;
	}
	log_printf(0, msg_allocFail, cb[0], cb[1]);
	return 0;
}

__asm__(
	".intel_syntax noprefix\n"
	"	.byte 0x8d\n"
	"	.byte 0xb6\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	".text\n"
	".att_syntax\n");

/* decrypted copy of an SC/SD/CD with hmacKey, signature checked if pubKey and salt */
u8 *cdDecrypt(u8 *bl, const void *pubKey, const u8 *salt, const u8 *hmacKey,
	u32 *outLen, u8 *outKey);
/* as cbDecrypt */
__attribute__((optimize("no-tree-dominator-opts", "no-cse-follow-jumps")))
u8 *cdDecrypt(u8 *bl, const void *pubKey, const u8 *salt, const u8 *hmacKey, u32 *outLen, u8 *outKey)
{
	u8 *buf;
	u32 len;
	u8 key[16];

	if (!bl || !hmacKey) {
		log_printf(0, msg_cdNoData);
		return 0;
	}
	if ((bl[0] & 0x43) != 0x43 || (bl[1] != 'C' && bl[1] != 'D')) {
		log_printf(0, msg_cdMagic);
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
				log_printf(1, msg_cdSigOk, buf[0], buf[1]);
				if (outLen)
					*outLen = len;
			} else {
				log_printf(0, msg_cdSigBad, buf[0], buf[1]);
				free(buf);
				buf = 0;
			}
		} else {
			log_printf(0, msg_cdNoKey, buf[0], buf[1]);
			if (outLen)
				*outLen = len;
		}
		return buf;
	}
	log_printf(0, msg_allocFail, bl[0], bl[1]);
	return 0;
}

__asm__(
	".intel_syntax noprefix\n"
	"	.byte 0x66\n"
	"	.byte 0x90\n"
	".text\n"
	".att_syntax\n");

/* decrypted copy of an SE/CE with hmacKey, hash checked if given */
u8 *ceDecrypt(u8 *bl, u32 *outLen, const u8 *hmacKey, const u8 *hash);
__asm__(
	".intel_syntax noprefix\n"
	"_ceDecrypt:\n"
	"	push EBP\n"
	"	push EDI\n"
	"	push ESI\n"
	"	push EBX\n"
	"	sub ESP,76\n"
	"	mov EBP,DWORD PTR [ESP+96]\n"
	"	mov EDI,DWORD PTR [ESP+104]\n"
	"	test EBP,EBP\n"
	"	je L_403065\n"
	"	test EDI,EDI\n"
	"	je L_403065\n"
	"	movzx EAX,BYTE PTR [EBP]\n"
	"	and EAX,67\n"
	"	cmp AL,67\n"
	"	jne L_403000\n"
	"	cmp BYTE PTR [EBP+1],69\n"
	"	jne L_403000\n"
	"	lea EAX,DWORD PTR [EBP+12]\n"
	"	mov DWORD PTR [ESP],EAX\n"
	"	call _getBeU32\n"
	"	lea ESI,DWORD PTR [EAX+15]\n"
	"	mov DWORD PTR [ESP+4],1\n"
	"	and ESI,4294967280\n"
	"	mov DWORD PTR [ESP],ESI\n"
	"	call _calloc\n"
	"	test EAX,EAX\n"
	"	mov EBX,EAX\n"
	"	je L_403045\n"
	"	mov DWORD PTR [ESP+4],EBP\n"
	"	mov DWORD PTR [ESP+8],ESI\n"
	"	lea EBP,DWORD PTR [ESP+48]\n"
	"	mov DWORD PTR [ESP],EAX\n"
	"	call _memcpy\n"
	"	lea EAX,DWORD PTR [EBX+16]\n"
	"	mov DWORD PTR [ESP+36],16\n"
	"	mov DWORD PTR [ESP+32],EBP\n"
	"	mov DWORD PTR [ESP+28],0\n"
	"	mov DWORD PTR [ESP+24],0\n"
	"	mov DWORD PTR [ESP+8],EAX\n"
	"	mov DWORD PTR [ESP+20],0\n"
	"	mov DWORD PTR [ESP+16],0\n"
	"	mov DWORD PTR [ESP+12],16\n"
	"	mov DWORD PTR [ESP+4],16\n"
	"	mov DWORD PTR [ESP],EDI\n"
	"	call _XeCryptHmacSha\n"
	"	lea EAX,DWORD PTR [ESI-32]\n"
	"	mov DWORD PTR [ESP+4],16\n"
	"	mov DWORD PTR [ESP],EBP\n"
	"	mov DWORD PTR [ESP+12],EAX\n"
	"	lea EAX,DWORD PTR [EBX+32]\n"
	"	mov DWORD PTR [ESP+8],EAX\n"
	"	call _XeCryptRc4\n"
	"	mov ECX,DWORD PTR [ESP+108]\n"
	"	test ECX,ECX\n"
	"	je L_403020\n"
	"	mov EAX,DWORD PTR [ESP+108]\n"
	"	mov DWORD PTR [ESP+4],ESI\n"
	"	mov DWORD PTR [ESP],EBX\n"
	"	mov DWORD PTR [ESP+8],EAX\n"
	"	call _blCheckHash\n"
	"	test EAX,EAX\n"
	"	movzx EAX,BYTE PTR [EBX+1]\n"
	"	mov DWORD PTR [ESP+12],EAX\n"
	"	movzx EAX,BYTE PTR [EBX]\n"
	"	mov DWORD PTR [ESP+8],EAX\n"
	"	je L_403080\n"
	"	mov DWORD PTR [ESP+4],OFFSET L_44c588\n"
	"	mov DWORD PTR [ESP],1\n"
	"	call _log_printf\n"
	"	mov EDX,DWORD PTR [ESP+100]\n"
	"	test EDX,EDX\n"
	"	je L_402ff5\n"
	"L_402fef:\n"
	"	mov EAX,DWORD PTR [ESP+100]\n"
	"	mov DWORD PTR [EAX],ESI\n"
	"L_402ff5:\n"
	"	add ESP,76\n"
	"	mov EAX,EBX\n"
	"	pop EBX\n"
	"	pop ESI\n"
	"	pop EDI\n"
	"	pop EBP\n"
	"	ret\n"
	"	.byte 0x90\n"
	"L_403000:\n"
	"	mov DWORD PTR [ESP+4],OFFSET L_44c67c\n"
	"	mov DWORD PTR [ESP],0\n"
	"	xor EBX,EBX\n"
	"	call _log_printf\n"
	"	add ESP,76\n"
	"	mov EAX,EBX\n"
	"	pop EBX\n"
	"	pop ESI\n"
	"	pop EDI\n"
	"	pop EBP\n"
	"	ret\n"
	"L_403020:\n"
	"	movzx EAX,BYTE PTR [EBX]\n"
	"	mov DWORD PTR [ESP+4],OFFSET L_44c5fc\n"
	"	mov DWORD PTR [ESP],0\n"
	"	mov DWORD PTR [ESP+8],EAX\n"
	"	call _log_printf\n"
	"	mov EAX,DWORD PTR [ESP+100]\n"
	"	test EAX,EAX\n"
	"	jne L_402fef\n"
	"	jmp L_402ff5\n"
	"L_403045:\n"
	"	movzx EAX,BYTE PTR [EBP]\n"
	"	mov DWORD PTR [ESP+4],OFFSET L_44c644\n"
	"	xor EBX,EBX\n"
	"	mov DWORD PTR [ESP],0\n"
	"	mov DWORD PTR [ESP+8],EAX\n"
	"	call _log_printf\n"
	"	jmp L_402ff5\n"
	"L_403065:\n"
	"	mov DWORD PTR [ESP+4],OFFSET L_44c6b0\n"
	"	mov DWORD PTR [ESP],0\n"
	"	xor EBX,EBX\n"
	"	call _log_printf\n"
	"	jmp L_402ff5\n"
	"L_403080:\n"
	"	mov DWORD PTR [ESP+4],OFFSET L_44c5b4\n"
	"	mov DWORD PTR [ESP],0\n"
	"	call _log_printf\n"
	"	mov DWORD PTR [ESP],EBX\n"
	"	xor EBX,EBX\n"
	"	call _free\n"
	"	jmp L_402ff5\n"
	"	.byte 0x90\n"
	"	.byte 0x90\n"
	"	.byte 0x90\n"
	"	.byte 0x90\n"
	"	.byte 0x90\n"
	"	.byte 0x90\n"
	"	.byte 0x90\n"
	"	.byte 0x90\n"
	"	.byte 0x90\n"
	"	.byte 0x90\n"
	"	.byte 0x90\n"
	"	.byte 0x90\n"
	"	.byte 0x90\n"
	"\n"
	".text\n"
	".att_syntax\n");

/* the object's strings and unwind info (FDEs for every function) */
__asm__(
	".intel_syntax noprefix\n"
	".section .rdata,\"dr\"\n"
	"	.p2align 2\n"
	"_msg_cbPairOk:\n"
	"	.string \"CB decrypted OK, pairing bytes extracted as: 0x%08x\\n\"\n"
	"	.zero 3\n"
	"_msg_cbPairFail:\n"
	"	.string \"***** WARNING: CB decrypt failed! Unable to get pairing data!\\n\"\n"
	"	.zero 1\n"
	"_msg_cfSlot0:\n"
	"	.string \"CF slot 0 decrypted ok LDV 0x%02x Pairing: 0x%06x\\n\"\n"
	"	.zero 1\n"
	"_msg_cfSlot1:\n"
	"	.string \"CF slot 1 decrypted ok LDV 0x%02x Pairing: 0x%06x\\n\"\n"
	"_msg_sigGood:\n"
	"	.string \"sig good! \"\n"
	"_msg_sigCheckFail:\n"
	"	.string \"\\nsignature check FAILED!\\n\"\n"
	"_msg_daeSigGood:\n"
	"L_44c168:\n"
	"	.string \"sig %d good! \"\n"
	"_msg_daeSigFail:\n"
	"L_44c176:\n"
	"	.string \"\\nsig %d FAIL! \"\n"
	"	.zero 3\n"
	"_msg_daeHash:\n"
	"L_44c188:\n"
	"	.string \"\\n******* ERROR: dae hash incorrect, could not decrypt!\\n\"\n"
	"_msg_daeHeader:\n"
	"L_44c1c0:\n"
	"	.string \"\\n******* ERROR: dae segment does not have the expected header!\\n\"\n"
	"_msg_sigFail:\n"
	"	.string \"\\nsignature FAILED!\\n\"\n"
	"_msg_noPub:\n"
	"	.string \"pub key to verify signature is not available, skipping!\\n\"\n"
	"	.zero 3\n"
	"_msg_fcrtSize:\n"
	"L_44c250:\n"
	"	.string \"**** ERROR: FCRT decrypt invalid size!\\n\"\n"
	"_msg_fcrtOffset:\n"
	"L_44c278:\n"
	"	.string \"**** ERROR: FCRT decrypt invalid offset!\\n\"\n"
	"_msg_fcrtDone:\n"
	"L_44c2a2:\n"
	"	.string \"FCRT was already decrypted...\"\n"
	"_msg_fcrtHash:\n"
	"L_44c2c0:\n"
	"	.string \"\\n******* ERROR: FCRT hash check failed, could not decrypt!\\n\"\n"
	"_msg_cbSigOk:\n"
	"L_44c2fc:\n"
	"	.string \"%cB signature OK! Decryption successful!\\n\"\n"
	"	.zero 2\n"
	"_msg_cbSigBad:\n"
	"L_44c328:\n"
	"	.string \"***** ERROR: %cB signature invalid, corrupted or decryption failed!\\n\"\n"
	"	.zero 3\n"
	"_msg_cbNoKey:\n"
	"L_44c370:\n"
	"	.string \"***** WARNING: could not check %cB signature, 1BL RSA key not loaded!\\n\"\n"
	"	.zero 1\n"
	"_msg_allocFail:\n"
	"L_44c3b8:\n"
	"	.string \"***** WARNING: Unable to allocate 0x%x bytes for %c%c!\\n\"\n"
	"_msg_cbMagic:\n"
	"L_44c3f0:\n"
	"	.string \"***** WARNING: CB/SB does not have valid magic!\\n\"\n"
	"	.zero 3\n"
	"_msg_cbNoData:\n"
	"L_44c424:\n"
	"	.string \"***** WARNING: CB/SB decrypt not provided with data!\\n\"\n"
	"	.zero 2\n"
	"_msg_cdSigOk:\n"
	"L_44c45c:\n"
	"	.string \"%c%c signature OK! Decryption successful!\\n\"\n"
	"	.zero 1\n"
	"_msg_cdSigBad:\n"
	"L_44c488:\n"
	"	.string \"***** ERROR: %c%c signature invalid, corrupted or decryption failed!\\n\"\n"
	"	.zero 2\n"
	"_msg_cdNoKey:\n"
	"L_44c4d0:\n"
	"	.string \"***** WARNING: could not check %c%c signature, 1BL RSA key not loaded!\\n\"\n"
	"_msg_cdMagic:\n"
	"L_44c518:\n"
	"	.string \"***** WARNING: SC/SD/CD does not have valid magic!\\n\"\n"
	"_msg_cdNoData:\n"
	"L_44c54c:\n"
	"	.string \"***** WARNING: SC/SD/CD decrypt not provided with data!\\n\"\n"
	"	.zero 3\n"
	"L_44c588:\n"
	"	.string \"%c%c hash check OK! Decryption successful!\\n\"\n"
	"L_44c5b4:\n"
	"	.string \"***** ERROR: %c%c hash check invalid, corrupted or decryption failed!\\n\"\n"
	"	.zero 1\n"
	"L_44c5fc:\n"
	"	.string \"***** WARNING: could not check %cE signature, 1BL RSA key not loaded!\\n\"\n"
	"	.zero 1\n"
	"L_44c644:\n"
	"	.string \"***** WARNING: Unable to allocate 0x%x bytes for %cE!\\n\"\n"
	"	.zero 1\n"
	"L_44c67c:\n"
	"	.string \"***** WARNING: SE/CE does not have valid magic!\\n\"\n"
	"	.zero 3\n"
	"L_44c6b0:\n"
	"	.string \"***** WARNING: SE/CE decrypt not provided with data!\\n\"\n"
	"	.zero 2\n"
	"\n"
	".section .eh_frame,\"dr\"\n"
	"	.p2align 2\n"
	"	.byte 0x14\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x1\n"
	"	.byte 0x7a\n"
	"	.byte 0x52\n"
	"	.byte 0x0\n"
	"	.byte 0x1\n"
	"	.byte 0x7c\n"
	"	.byte 0x8\n"
	"	.byte 0x1\n"
	"	.byte 0x1b\n"
	"	.byte 0xc\n"
	"	.byte 0x4\n"
	"	.byte 0x4\n"
	"	.byte 0x88\n"
	"	.byte 0x1\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x38\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x1c\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.long _verifyExtended - .\n"
	"	.byte 0xf3\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x85\n"
	"	.byte 0x2\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x87\n"
	"	.byte 0x3\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x86\n"
	"	.byte 0x4\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x14\n"
	"	.byte 0x83\n"
	"	.byte 0x5\n"
	"	.byte 0x43\n"
	"	.byte 0xe\n"
	"	.byte 0x70\n"
	"	.byte 0x2\n"
	"	.byte 0xe4\n"
	"	.byte 0xe\n"
	"	.byte 0x14\n"
	"	.byte 0x41\n"
	"	.byte 0xc3\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x44\n"
	"	.byte 0xc6\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x41\n"
	"	.byte 0xc7\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x41\n"
	"	.byte 0xc5\n"
	"	.byte 0xe\n"
	"	.byte 0x4\n"
	"	.byte 0x38\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x58\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.long _unscramble - .\n"
	"	.byte 0xa0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x85\n"
	"	.byte 0x2\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x87\n"
	"	.byte 0x3\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x86\n"
	"	.byte 0x4\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x14\n"
	"	.byte 0x83\n"
	"	.byte 0x5\n"
	"	.byte 0x43\n"
	"	.byte 0xe\n"
	"	.byte 0x40\n"
	"	.byte 0x2\n"
	"	.byte 0x90\n"
	"	.byte 0xe\n"
	"	.byte 0x14\n"
	"	.byte 0x41\n"
	"	.byte 0xc3\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x41\n"
	"	.byte 0xc6\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x41\n"
	"	.byte 0xc7\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x41\n"
	"	.byte 0xc5\n"
	"	.byte 0xe\n"
	"	.byte 0x4\n"
	"	.byte 0x3c\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x94\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.long _cbGetPairing - .\n"
	"	.byte 0x36\n"
	"	.byte 0x1\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x85\n"
	"	.byte 0x2\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x87\n"
	"	.byte 0x3\n"
	"	.byte 0x43\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x86\n"
	"	.byte 0x4\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x14\n"
	"	.byte 0x83\n"
	"	.byte 0x5\n"
	"	.byte 0x43\n"
	"	.byte 0xe\n"
	"	.byte 0x70\n"
	"	.byte 0x52\n"
	"	.byte 0xa\n"
	"	.byte 0xe\n"
	"	.byte 0x14\n"
	"	.byte 0x43\n"
	"	.byte 0xc3\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x41\n"
	"	.byte 0xc6\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x41\n"
	"	.byte 0xc7\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x41\n"
	"	.byte 0xc5\n"
	"	.byte 0xe\n"
	"	.byte 0x4\n"
	"	.byte 0x41\n"
	"	.byte 0xb\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x34\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0xd4\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.long _cfGetPairing - .\n"
	"	.byte 0xe3\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x87\n"
	"	.byte 0x2\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x86\n"
	"	.byte 0x3\n"
	"	.byte 0x43\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x83\n"
	"	.byte 0x4\n"
	"	.byte 0x43\n"
	"	.byte 0xe\n"
	"	.byte 0x50\n"
	"	.byte 0x52\n"
	"	.byte 0xa\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x41\n"
	"	.byte 0xc3\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x41\n"
	"	.byte 0xc6\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x41\n"
	"	.byte 0xc7\n"
	"	.byte 0xe\n"
	"	.byte 0x4\n"
	"	.byte 0x43\n"
	"	.byte 0xb\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x6c\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0xc\n"
	"	.byte 0x1\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.long _cfBestPairing - .\n"
	"	.byte 0xd5\n"
	"	.byte 0x2\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x85\n"
	"	.byte 0x2\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x87\n"
	"	.byte 0x3\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x86\n"
	"	.byte 0x4\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x14\n"
	"	.byte 0x83\n"
	"	.byte 0x5\n"
	"	.byte 0x45\n"
	"	.byte 0xe\n"
	"	.byte 0x70\n"
	"	.byte 0x4f\n"
	"	.byte 0xa\n"
	"	.byte 0xe\n"
	"	.byte 0x14\n"
	"	.byte 0x43\n"
	"	.byte 0xc3\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x41\n"
	"	.byte 0xc6\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x41\n"
	"	.byte 0xc7\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x41\n"
	"	.byte 0xc5\n"
	"	.byte 0xe\n"
	"	.byte 0x4\n"
	"	.byte 0x42\n"
	"	.byte 0xb\n"
	"	.byte 0x2\n"
	"	.byte 0x59\n"
	"	.byte 0xa\n"
	"	.byte 0xe\n"
	"	.byte 0x14\n"
	"	.byte 0x43\n"
	"	.byte 0xc3\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x41\n"
	"	.byte 0xc6\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x41\n"
	"	.byte 0xc7\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x41\n"
	"	.byte 0xc5\n"
	"	.byte 0xe\n"
	"	.byte 0x4\n"
	"	.byte 0x41\n"
	"	.byte 0xb\n"
	"	.byte 0x3\n"
	"	.byte 0x5c\n"
	"	.byte 0x1\n"
	"	.byte 0xa\n"
	"	.byte 0xe\n"
	"	.byte 0x14\n"
	"	.byte 0x41\n"
	"	.byte 0xc3\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x43\n"
	"	.byte 0xc6\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x41\n"
	"	.byte 0xc7\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x41\n"
	"	.byte 0xc5\n"
	"	.byte 0xe\n"
	"	.byte 0x4\n"
	"	.byte 0x41\n"
	"	.byte 0xb\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x34\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x7c\n"
	"	.byte 0x1\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.long _cfDecrypt - .\n"
	"	.byte 0xd3\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x87\n"
	"	.byte 0x2\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x86\n"
	"	.byte 0x3\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x83\n"
	"	.byte 0x4\n"
	"	.byte 0x43\n"
	"	.byte 0xe\n"
	"	.byte 0x50\n"
	"	.byte 0x53\n"
	"	.byte 0xa\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x41\n"
	"	.byte 0xc3\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x41\n"
	"	.byte 0xc6\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x41\n"
	"	.byte 0xc7\n"
	"	.byte 0xe\n"
	"	.byte 0x4\n"
	"	.byte 0x44\n"
	"	.byte 0xb\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x28\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0xb4\n"
	"	.byte 0x1\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.long _cgDecrypt - .\n"
	"	.byte 0x97\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x86\n"
	"	.byte 0x2\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x83\n"
	"	.byte 0x3\n"
	"	.byte 0x43\n"
	"	.byte 0xe\n"
	"	.byte 0x50\n"
	"	.byte 0x2\n"
	"	.byte 0x8c\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x44\n"
	"	.byte 0xc3\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x41\n"
	"	.byte 0xc6\n"
	"	.byte 0xe\n"
	"	.byte 0x4\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x3c\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0xe0\n"
	"	.byte 0x1\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.long _verifySecdata - .\n"
	"	.byte 0x1b\n"
	"	.byte 0x1\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x85\n"
	"	.byte 0x2\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x87\n"
	"	.byte 0x3\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x86\n"
	"	.byte 0x4\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x14\n"
	"	.byte 0x83\n"
	"	.byte 0x5\n"
	"	.byte 0x43\n"
	"	.byte 0xe\n"
	"	.byte 0x80\n"
	"	.byte 0x1\n"
	"	.byte 0x3\n"
	"	.byte 0xc\n"
	"	.byte 0x1\n"
	"	.byte 0xe\n"
	"	.byte 0x14\n"
	"	.byte 0x41\n"
	"	.byte 0xc3\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x44\n"
	"	.byte 0xc6\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x41\n"
	"	.byte 0xc7\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x41\n"
	"	.byte 0xc5\n"
	"	.byte 0xe\n"
	"	.byte 0x4\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x18\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x20\n"
	"	.byte 0x2\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.long _crlVerifySig - .\n"
	"	.byte 0x9c\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x4c\n"
	"	.byte 0xe\n"
	"	.byte 0x30\n"
	"	.byte 0x5b\n"
	"	.byte 0xe\n"
	"	.byte 0x4\n"
	"	.byte 0x59\n"
	"	.byte 0xe\n"
	"	.byte 0x30\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x54\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x3c\n"
	"	.byte 0x2\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.long _verifyCrl - .\n"
	"	.byte 0xf0\n"
	"	.byte 0x1\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x85\n"
	"	.byte 0x2\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x87\n"
	"	.byte 0x3\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x86\n"
	"	.byte 0x4\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x14\n"
	"	.byte 0x83\n"
	"	.byte 0x5\n"
	"	.byte 0x46\n"
	"	.byte 0xe\n"
	"	.byte 0xe0\n"
	"	.byte 0x4\n"
	"	.byte 0x3\n"
	"	.byte 0x3f\n"
	"	.byte 0x1\n"
	"	.byte 0xa\n"
	"	.byte 0xe\n"
	"	.byte 0x14\n"
	"	.byte 0x41\n"
	"	.byte 0xc3\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x41\n"
	"	.byte 0xc6\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x41\n"
	"	.byte 0xc7\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x41\n"
	"	.byte 0xc5\n"
	"	.byte 0xe\n"
	"	.byte 0x4\n"
	"	.byte 0x43\n"
	"	.byte 0xb\n"
	"	.byte 0x7e\n"
	"	.byte 0xa\n"
	"	.byte 0xe\n"
	"	.byte 0x14\n"
	"	.byte 0x46\n"
	"	.byte 0xc3\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x41\n"
	"	.byte 0xc6\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x41\n"
	"	.byte 0xc7\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x41\n"
	"	.byte 0xc5\n"
	"	.byte 0xe\n"
	"	.byte 0x4\n"
	"	.byte 0x49\n"
	"	.byte 0xb\n"
	"	.byte 0x0\n"
	"	.byte 0x3c\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x94\n"
	"	.byte 0x2\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.long _daeDecrypt - .\n"
	"	.byte 0xd6\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x85\n"
	"	.byte 0x2\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x87\n"
	"	.byte 0x3\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x86\n"
	"	.byte 0x4\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x14\n"
	"	.byte 0x83\n"
	"	.byte 0x5\n"
	"	.byte 0x46\n"
	"	.byte 0xe\n"
	"	.byte 0xc0\n"
	"	.byte 0x4\n"
	"	.byte 0x2\n"
	"	.byte 0xaa\n"
	"	.byte 0xa\n"
	"	.byte 0xe\n"
	"	.byte 0x14\n"
	"	.byte 0x41\n"
	"	.byte 0xc3\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x41\n"
	"	.byte 0xc6\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x41\n"
	"	.byte 0xc7\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x41\n"
	"	.byte 0xc5\n"
	"	.byte 0xe\n"
	"	.byte 0x4\n"
	"	.byte 0x48\n"
	"	.byte 0xb\n"
	"	.byte 0x28\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0xd4\n"
	"	.byte 0x2\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.long _daeVerifySig - .\n"
	"	.byte 0x16\n"
	"	.byte 0x1\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x4e\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x83\n"
	"	.byte 0x2\n"
	"	.byte 0x48\n"
	"	.byte 0xe\n"
	"	.byte 0x80\n"
	"	.byte 0x1\n"
	"	.byte 0x2\n"
	"	.byte 0xd5\n"
	"	.byte 0xa\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x41\n"
	"	.byte 0xc3\n"
	"	.byte 0xe\n"
	"	.byte 0x4\n"
	"	.byte 0x44\n"
	"	.byte 0xb\n"
	"	.byte 0x5b\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x41\n"
	"	.byte 0xc3\n"
	"	.byte 0xe\n"
	"	.byte 0x4\n"
	"	.byte 0x3c\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x3\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.long _verifyDae - .\n"
	"	.byte 0xfe\n"
	"	.byte 0x1\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x85\n"
	"	.byte 0x2\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x87\n"
	"	.byte 0x3\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x86\n"
	"	.byte 0x4\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x14\n"
	"	.byte 0x83\n"
	"	.byte 0x5\n"
	"	.byte 0x43\n"
	"	.byte 0xe\n"
	"	.byte 0x90\n"
	"	.byte 0x1\n"
	"	.byte 0x2\n"
	"	.byte 0x48\n"
	"	.byte 0xa\n"
	"	.byte 0xe\n"
	"	.byte 0x14\n"
	"	.byte 0x41\n"
	"	.byte 0xc3\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x41\n"
	"	.byte 0xc6\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x41\n"
	"	.byte 0xc7\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x41\n"
	"	.byte 0xc5\n"
	"	.byte 0xe\n"
	"	.byte 0x4\n"
	"	.byte 0x41\n"
	"	.byte 0xb\n"
	"	.byte 0x54\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x40\n"
	"	.byte 0x3\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.long _fcrtVerifySig - .\n"
	"	.byte 0x2\n"
	"	.byte 0x1\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x87\n"
	"	.byte 0x2\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x86\n"
	"	.byte 0x3\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x83\n"
	"	.byte 0x4\n"
	"	.byte 0x43\n"
	"	.byte 0xe\n"
	"	.byte 0x60\n"
	"	.byte 0x2\n"
	"	.byte 0xac\n"
	"	.byte 0xa\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x43\n"
	"	.byte 0xc3\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x41\n"
	"	.byte 0xc6\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x41\n"
	"	.byte 0xc7\n"
	"	.byte 0xe\n"
	"	.byte 0x4\n"
	"	.byte 0x49\n"
	"	.byte 0xb\n"
	"	.byte 0x57\n"
	"	.byte 0xa\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x43\n"
	"	.byte 0xc3\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x41\n"
	"	.byte 0xc6\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x41\n"
	"	.byte 0xc7\n"
	"	.byte 0xe\n"
	"	.byte 0x4\n"
	"	.byte 0x44\n"
	"	.byte 0xb\n"
	"	.byte 0x5c\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x43\n"
	"	.byte 0xc3\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x41\n"
	"	.byte 0xc6\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x41\n"
	"	.byte 0xc7\n"
	"	.byte 0xe\n"
	"	.byte 0x4\n"
	"	.byte 0x0\n"
	"	.byte 0x54\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x98\n"
	"	.byte 0x3\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.long _verifyFcrt - .\n"
	"	.byte 0xd1\n"
	"	.byte 0x2\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x85\n"
	"	.byte 0x2\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x87\n"
	"	.byte 0x3\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x86\n"
	"	.byte 0x4\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x14\n"
	"	.byte 0x83\n"
	"	.byte 0x5\n"
	"	.byte 0x46\n"
	"	.byte 0xe\n"
	"	.byte 0xf0\n"
	"	.byte 0x4\n"
	"	.byte 0x2\n"
	"	.byte 0xfb\n"
	"	.byte 0xa\n"
	"	.byte 0xe\n"
	"	.byte 0x14\n"
	"	.byte 0x41\n"
	"	.byte 0xc3\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x41\n"
	"	.byte 0xc6\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x41\n"
	"	.byte 0xc7\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x41\n"
	"	.byte 0xc5\n"
	"	.byte 0xe\n"
	"	.byte 0x4\n"
	"	.byte 0x47\n"
	"	.byte 0xb\n"
	"	.byte 0x3\n"
	"	.byte 0xba\n"
	"	.byte 0x1\n"
	"	.byte 0xe\n"
	"	.byte 0x14\n"
	"	.byte 0x43\n"
	"	.byte 0xc3\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x41\n"
	"	.byte 0xc6\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x41\n"
	"	.byte 0xc7\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x41\n"
	"	.byte 0xc5\n"
	"	.byte 0xe\n"
	"	.byte 0x4\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x28\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0xf0\n"
	"	.byte 0x3\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.long _shaSelfCheck - .\n"
	"	.byte 0x6e\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x86\n"
	"	.byte 0x2\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x83\n"
	"	.byte 0x3\n"
	"	.byte 0x43\n"
	"	.byte 0xe\n"
	"	.byte 0x50\n"
	"	.byte 0x2\n"
	"	.byte 0x63\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x44\n"
	"	.byte 0xc3\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x41\n"
	"	.byte 0xc6\n"
	"	.byte 0xe\n"
	"	.byte 0x4\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x54\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x1c\n"
	"	.byte 0x4\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.long _cbDecrypt - .\n"
	"	.byte 0xfa\n"
	"	.byte 0x1\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x85\n"
	"	.byte 0x2\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x87\n"
	"	.byte 0x3\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x86\n"
	"	.byte 0x4\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x14\n"
	"	.byte 0x83\n"
	"	.byte 0x5\n"
	"	.byte 0x43\n"
	"	.byte 0xe\n"
	"	.byte 0x60\n"
	"	.byte 0x3\n"
	"	.byte 0x39\n"
	"	.byte 0x1\n"
	"	.byte 0xa\n"
	"	.byte 0xe\n"
	"	.byte 0x14\n"
	"	.byte 0x43\n"
	"	.byte 0xc3\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x41\n"
	"	.byte 0xc6\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x41\n"
	"	.byte 0xc7\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x41\n"
	"	.byte 0xc5\n"
	"	.byte 0xe\n"
	"	.byte 0x4\n"
	"	.byte 0x4a\n"
	"	.byte 0xb\n"
	"	.byte 0x59\n"
	"	.byte 0xa\n"
	"	.byte 0xe\n"
	"	.byte 0x14\n"
	"	.byte 0x43\n"
	"	.byte 0xc3\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x41\n"
	"	.byte 0xc6\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x41\n"
	"	.byte 0xc7\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x41\n"
	"	.byte 0xc5\n"
	"	.byte 0xe\n"
	"	.byte 0x4\n"
	"	.byte 0x41\n"
	"	.byte 0xb\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x54\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x74\n"
	"	.byte 0x4\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.long _cdDecrypt - .\n"
	"	.byte 0x4e\n"
	"	.byte 0x2\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x85\n"
	"	.byte 0x2\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x87\n"
	"	.byte 0x3\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x86\n"
	"	.byte 0x4\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x14\n"
	"	.byte 0x83\n"
	"	.byte 0x5\n"
	"	.byte 0x43\n"
	"	.byte 0xe\n"
	"	.byte 0x60\n"
	"	.byte 0x3\n"
	"	.byte 0x75\n"
	"	.byte 0x1\n"
	"	.byte 0xa\n"
	"	.byte 0xe\n"
	"	.byte 0x14\n"
	"	.byte 0x43\n"
	"	.byte 0xc3\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x41\n"
	"	.byte 0xc6\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x41\n"
	"	.byte 0xc7\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x41\n"
	"	.byte 0xc5\n"
	"	.byte 0xe\n"
	"	.byte 0x4\n"
	"	.byte 0x41\n"
	"	.byte 0xb\n"
	"	.byte 0x59\n"
	"	.byte 0xa\n"
	"	.byte 0xe\n"
	"	.byte 0x14\n"
	"	.byte 0x43\n"
	"	.byte 0xc3\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x41\n"
	"	.byte 0xc6\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x41\n"
	"	.byte 0xc7\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x41\n"
	"	.byte 0xc5\n"
	"	.byte 0xe\n"
	"	.byte 0x4\n"
	"	.byte 0x41\n"
	"	.byte 0xb\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x54\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0xcc\n"
	"	.byte 0x4\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.long _ceDecrypt - .\n"
	"	.byte 0xe3\n"
	"	.byte 0x1\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x85\n"
	"	.byte 0x2\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x87\n"
	"	.byte 0x3\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x86\n"
	"	.byte 0x4\n"
	"	.byte 0x41\n"
	"	.byte 0xe\n"
	"	.byte 0x14\n"
	"	.byte 0x83\n"
	"	.byte 0x5\n"
	"	.byte 0x43\n"
	"	.byte 0xe\n"
	"	.byte 0x60\n"
	"	.byte 0x3\n"
	"	.byte 0x31\n"
	"	.byte 0x1\n"
	"	.byte 0xa\n"
	"	.byte 0xe\n"
	"	.byte 0x14\n"
	"	.byte 0x43\n"
	"	.byte 0xc3\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x41\n"
	"	.byte 0xc6\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x41\n"
	"	.byte 0xc7\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x41\n"
	"	.byte 0xc5\n"
	"	.byte 0xe\n"
	"	.byte 0x4\n"
	"	.byte 0x42\n"
	"	.byte 0xb\n"
	"	.byte 0x59\n"
	"	.byte 0xa\n"
	"	.byte 0xe\n"
	"	.byte 0x14\n"
	"	.byte 0x43\n"
	"	.byte 0xc3\n"
	"	.byte 0xe\n"
	"	.byte 0x10\n"
	"	.byte 0x41\n"
	"	.byte 0xc6\n"
	"	.byte 0xe\n"
	"	.byte 0xc\n"
	"	.byte 0x41\n"
	"	.byte 0xc7\n"
	"	.byte 0xe\n"
	"	.byte 0x8\n"
	"	.byte 0x41\n"
	"	.byte 0xc5\n"
	"	.byte 0xe\n"
	"	.byte 0x4\n"
	"	.byte 0x41\n"
	"	.byte 0xb\n"
	"	.byte 0x0\n"
	"	.byte 0x0\n"
	".text\n"
	".att_syntax\n");


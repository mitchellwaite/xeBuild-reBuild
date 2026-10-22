/* keys: CPU/1BL keys, pairing, the per-image HMAC nonces, and encrypting
   the bootloaders, SMC, keyvault, extended, secdata, CRL, DAE and FCRT
   for the image being built. */
#include <stdlib.h>
#include <string.h>

typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef unsigned long long u64;

/* XeCrypt's XECRYPT_AES_STATE (two Gladman contexts) */
typedef struct {
	u32 ctx[2][61];
} AESSTATE;

/* a file of the image (build.c's table, 0x42c bytes) */
typedef struct {
	char name[0x40c];
	u8 *buf;			/* 40c */
	u32 size;			/* 410 */
	u32 f414[4];			/* 414 */
	u32 f424;			/* 424 */
	u32 f428;			/* 428 */
} part_t;

/* the parts of main.c's struct xebuild used here */
struct xebuild {
	int mode;			/* 000 */
	u32 flags;			/* 004 */
	u32 type;			/* 008 build type */
	u8 pad00c[0x060 - 0x00c];
	u32 bootFlags;			/* 060 */
	u8 pad064[0x074 - 0x064];
	u8 cbLdv;			/* 074 */
	u8 cfLdv;			/* 075 */
	u8 pad076[0x26c - 0x076];
	u8 key1bl[16];			/* 26c */
	u8 cpuKey[16];			/* 27c */
	u8 key28c[16];			/* 28c */
};

void aes_init(void);
void XeCryptRandom(u8 *pb, u32 cb);
int XeCryptHammingWeight(u8 *data, int len);
void XeCryptUidEccEncode(u8 *pbaCpuKey);
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
void log_printf(int level, const char *fmt, ...);
int validateString(char *s);
u8 myatox8(char *dat);
int checkZeros(const u8 *p, u32 len);
void showKey(int level, const u8 *key);
u8 *setBeU64(u64 v, u8 *p);
u16 getBeU16(const u8 *p);
/* getBeU32 and verifyFcrt pure: fcrtEncrypt's block order needs them left
   out of the call heuristic (with its off < 0x4000 hint at
   builtin-expect-probability 60) */
u32 getBeU32(const u8 *p) __attribute__((pure));
u32 sumBytes(const u8 *p, u32 len);
void memcpyrev(u8 *dst, const u8 *src, int len);
int unscramble(u8 *buf, u32 len);
int smcCheck(u8 *smc, int len, int type);
void smcPatch(u8 *smc, int len, u32 flags);
void kvSet(u8 *buf);
int verifyExtended(void *buf, int size);
int verifyCrl(void *buf, int size, int perBox);
void daeDecrypt(u8 *dae, u32 size, int perBox);
int verifyFcrt(u8 *fcrt, u32 size) __attribute__((pure));
/* external copy of the always_inline cfPatchSlots */
short cfPatchSlots(part_t *cf, u32 extra, u16 block, u32 max);

extern struct xebuild xb;

#define SWAP32(x) (((x) << 24) + ((x) >> 24) + (((x) << 8) & 0xff0000) + (((x) >> 8) & 0xff00))
#define SWAP16(x) ((((x) & 0xff) << 8) + (((x) & 0xff00) >> 8))

u8 secdataKey[8] = { 0x5a, 0xa4, 0xd1, 0xd2, 0x7d, 0xe4, 0x45, 0x3e };
u8 daeKey[32];
u8 crlKey[32];
u8 smcKey[4];
u8 kvAltSalt[8];
u8 kvSalt[8];
u8 infoKey5[16];
u8 infoKey4[16];
u8 infoKey3[16];
u8 infoKey2[16];
u8 infoKey1[16];
u8 infoKey0[16];
u8 zeroKey[16];
u8 pairing[3];

void keysInit(int random)
{
	aes_init();
	if (random) {
		log_printf(1, "initializing random nonces\n");
		XeCryptRandom(infoKey0, 16);
		XeCryptRandom(infoKey1, 16);
		XeCryptRandom(infoKey2, 16);
		XeCryptRandom(infoKey3, 16);
		XeCryptRandom(infoKey4, 16);
		XeCryptRandom(infoKey5, 16);
		XeCryptRandom(kvSalt, 8);
		XeCryptRandom(kvAltSalt, 8);
		XeCryptRandom(smcKey, 4);
		XeCryptRandom(crlKey, 32);
		XeCryptRandom(daeKey, 32);
		XeCryptRandom(secdataKey, 8);
	} else if (pairing[0] == 0 && pairing[1] == 0 && pairing[2] == 0) {
		log_printf(1, "initializing static pairing value\n");
		pairing[0] = 0x23;
		pairing[1] = 0x45;
		pairing[2] = 0xf1;
	}
	if (pairing[0] == 0 && pairing[1] == 0 && pairing[2] == 0)
		XeCryptRandom(pairing, 3);
}

void setCrlKey(u8 *key)
{
#if 1 == 1
	memcpy(crlKey, key + 16, 16);
	memcpy(crlKey + 16, key, 16);
#elif 1 == 2
	u32 *k = (u32 *)key, *c = (u32 *)crlKey;
	c[0] = k[4]; c[1] = k[5]; c[2] = k[6]; c[3] = k[7];
	c[4] = k[0]; c[5] = k[1]; c[6] = k[2]; c[7] = k[3];
#elif 1 == 3
	int i;
	for (i = 0; i < 16; i++) {
		crlKey[i] = key[i + 16];
		crlKey[i + 16] = key[i];
	}
#else
	memcpy(crlKey, key + 16, 16);
	memcpy(crlKey + 16, key, 16);
#endif
}

void setDaeKey(u8 *key)
{
	memcpy(daeKey, key, 32);
}

void setSecdataKey(u8 *key)
{
	memcpy(secdataKey, key, 8);
}

void setInfoKey0(u8 *key)
{
	memcpy(infoKey0, key, 16);
}

void setInfoKey1(u8 *key)
{
	memcpy(infoKey1, key, 16);
}

void setInfoKey2(u8 *key)
{
	memcpy(infoKey2, key, 16);
}

void setInfoKey3(u8 *key)
{
	memcpy(infoKey3, key, 16);
}

void setInfoKey4(u8 *key)
{
	memcpy(infoKey4, key, 16);
}

void setInfoKey5(u8 *key)
{
	memcpy(infoKey5, key, 16);
}

void setKvSalt(u8 *key)
{
	memcpy(kvSalt, key, 8);
}

void setKvAltSalt(u8 *key)
{
	memcpy(kvAltSalt, key, 8);
}

void setSmcKey(u8 *key)
{
	memcpy(smcKey, key, 4);
}

int setPairing(u32 pair)
{
	if (pair & 0xffffff) {
		pairing[2] = pair;
		pairing[0] = pair >> 16;
		pairing[1] = pair >> 8;
		log_printf(1, "pairing set to: %02x %02x %02x\n", pairing[0], pairing[1], pairing[2]);
		return 1;
	}
	return 0;
}

int checkCpuKey(int level, u8 *key)
{
	u8 mask[16] = { 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
		0xff, 0xff, 0xff, 0xff, 0xff, 0x03, 0, 0 };
	u8 tmp[16];
	int i, weight, ecd, wok;

	for (i = 0; i < 16; i++)
		tmp[i] = key[i] & mask[i];
	weight = XeCryptHammingWeight(tmp, 16);
	XeCryptUidEccEncode(tmp);
	ecd = memcmp(key, tmp, 16) == 0;
	wok = weight == 53;
	log_printf(level, " (weight:0x%x %s; ecd: %s)", weight,
		wok ? "valid" : "error", ecd ? "valid" : "error");
	return wok && ecd;
}

int setCpuKeyStr(char *str)
{
	int len = strlen(str);
	int i, ret;

	if (len == 32) {
		ret = validateString(str);
		if (ret) {
			for (i = 0; i < 16; i++, str += 2)
				xb.cpuKey[i] = myatox8(str);
			log_printf(1, "CPU Key set to: 0x");
			for (i = 0; i < 16; i++)
				log_printf(1, "%02X", xb.cpuKey[i]);
			ret = 1;
			if (!checkZeros(xb.cpuKey, 16)) {
				if (checkCpuKey(1, xb.cpuKey))
					log_printf(0, "\n");
				else
					log_printf(0, "\n***** WARNING: CPU key check failed, CPU key may not be valid!\n\n");
			}
		} else
			log_printf(0, "\n******* ERROR: invalid or unexpected characters in CPU key!\n");
	} else {
		ret = 0;
		log_printf(0, "\n***** ERROR: unable to set CPU key to '%s', %d is not the correct length, 32 chars required!\n", str, len);
	}
	return ret;
}

int setCpuKey(int level, u8 *key)
{
	memcpy(xb.cpuKey, key, 16);
	log_printf(level, "CPU Key set to  : ");
	showKey(level, key);
	if (!checkZeros(xb.cpuKey, 16) && !checkCpuKey(level, xb.cpuKey))
		log_printf(level, "\n***** WARNING: CPU key check failed, CPU key may not be valid!\n\n");
	log_printf(level, "\n");
	return 1;
}

void setFuseLdv(u8 *fuse, u8 ldv)
{
	u32 i;
	u64 cb, cf;

	if (ldv > 16) {
		if (ldv > 31)
			cf = ~0ULL;
		else
			for (cf = 0, i = 0; i < ldv - 16; i++)
				cf = (cf >> 4) | 0xf000000000000000ULL;
		cb = ~0ULL;
	} else {
		cf = 0;
		if (ldv == 16)
			cb = ~0ULL;
		else
			for (cb = 0, i = 0; i < ldv; i++)
				cb = (cb >> 4) | 0xf000000000000000ULL;
	}
	setBeU64(cb, fuse + 56);
	setBeU64(cf, fuse + 64);
	log_printf(1, "Fuse CF LDV set to : 0x");
	for (i = 0; i < 16; i++)
		log_printf(1, "%02X", fuse[56 + i]);
	log_printf(1, "\n");
}

void setFuseCpuKey(u8 *fuse)
{
	int i;

	if (__builtin_expect(fuse == NULL, 0)) {
		log_printf(0, "\nERROR: YOU SHOULD NOT BE SEEING THIS ERROR!\n");
		return;
	}
	memcpy(fuse + 24, xb.cpuKey, 8);
	memcpy(fuse + 32, xb.cpuKey, 16);
	memcpy(fuse + 48, xb.cpuKey + 8, 8);
	memcpy(xb.cpuKey, fuse + 32, 16);
	setFuseLdv(fuse, xb.cfLdv);
	log_printf(1, "Fuse CPU Key set to: 0x");
	for (i = 32; i < 48; i++)
		log_printf(1, "%02X", fuse[i]);
	log_printf(1, "\n");
}

u32 calcXexKey(void)
{
	u8 key[16] = { 0x95, 0x27, 0x72, 0xbf, 0x47, 0xc0, 0xf6, 0x98,
		0x5c, 0x7d, 0xf2, 0x50, 0x65, 0x4d, 0x55, 0xcd };
	u8 junk[16];
	u8 hash[16];

	memcpy(junk, "thisisjustajunky", 16);
	XeCryptHmacSha(junk, 16, xb.key1bl, 16, NULL, 0, NULL, 0, hash, 16);
	memcpy(xb.key28c, key, 16);
	XeCryptRc4(hash, 16, xb.key28c, 16);
	return sumBytes(xb.key28c, 16);
}

int check1blKey(void)
{
	u32 sum1 = sumBytes(xb.key1bl, 16);
	u32 sum2 = calcXexKey();

	if (sum1 == 0x983 && sum2 == 0x800) {
		log_printf(1, "1BL Key set to  : 0x");
		showKey(1, xb.key1bl);
		log_printf(1, " sum: 0x%x (expects: 0x983)\n", sum1);
		log_printf(1, "xex Key set to  : 0x");
		showKey(1, xb.key28c);
		log_printf(1, " sum: 0x%x (expects: 0x800)\n", sum2);
		return 1;
	}
	return 0;
}

int set1blKey(u8 *key)
{
	memcpy(xb.key1bl, key, 16);
	if (check1blKey())
		return 1;
	log_printf(0, "\n******* ERROR: 1BL key 0x");
	showKey(0, xb.key1bl);
	log_printf(0, " does not appear to be correct!\n");
	return 0;
}

int checkKeys(char *str)
{
	int len = strlen(str);
	char *p;
	int i;

	if (len == 32) {
		if (validateString(str)) {
			for (i = 0, p = str; i < 16; i++, p += 2)
				xb.key1bl[i] = myatox8(p);
			if (check1blKey())
				return 1;
			log_printf(0, "\n******* ERROR: 1BL key 0x%s ", str);
			log_printf(0, "does not appear to be correct!\n");
			return 0;
		}
		log_printf(0, "\n******* ERROR: invalid or unexpected characters in 1BL key!\n");
		return 0;
	}
	log_printf(0, "\n***** ERROR: unable to set 1BL key to '%s', %d is not the correct length, 32 chars required!\n", str, len);
	return 0;
}

/* the sums are copied to a type they can't be coalesced with (signed vs
   unsigned), so the value after the loop is its own pseudo: in registers
   there (xor'd on the count == 0 path) while the loop's sums stay in memory */
__attribute__((always_inline))
static inline void smcSum(u32 *buf, u8 *out, u32 count)
{
	u64 s1 = 0, s2 = 0;
	long long sum1 = 0, sum2 = 0;
	u32 i, v;

	for (i = 0; i < count; i++) {
		v = SWAP32(buf[i]);
		sum1 += v;
		sum2 -= v;
		sum1 = (sum1 << 29) | (u32)((u32)(sum1 >> 32) >> 3);
		sum2 = (sum2 << 31) | (u32)((u32)(sum2 >> 32) >> 1);
		s1 = sum1;
		s2 = sum2;
	}
	setBeU64(s1, out);
	setBeU64(s2, out + 8);
}

/* smcPrepare inlines smcSum with the object's flags; the standalone copy
   skips the late forwprop (it would put the loop bound first in the exit
   cmp) and reassoc (SWAP32's first add) */
__attribute__((optimize("no-tree-forwprop", "no-tree-reassoc")))
void smcChecksum(u32 *buf, u8 *out, u32 count)
{
	smcSum(buf, out, count);
}

void smcEncrypt(u8 *buf, u32 len)
{
	u8 s[4] = { 'B', 'u', 'N', 'y' };
	u32 i, j = 0;
	int t;

	for (i = 0; i < len; i++) {
		buf[i] ^= s[j];
		t = buf[i] * 251;
		j = (j + 1) & 3;
		s[j] += t;
		s[(j + 1) & 3] += t >> 8;
	}
}

int smcPrepare(u8 *smc, u8 *hash, u32 size)
{
	u8 *buf = malloc(size);
	u32 patch;
	int bad;

	memcpy(buf, smc, size);
	if (!checkZeros(buf + size - 4, 4)) {
		log_printf(1, "SMC binary appears to be encrypted, attempting to decrypt...");
		if (unscramble(buf, size)) {
			memcpy(smc, buf, size);
			log_printf(1, "success!");
		} else {
			log_printf(1, "failed!");
			log_printf(0, "\n******* ERROR: please make sure your provided a valid/decryptable SMC binary!\n\n");
			if (!(xb.bootFlags & 0x200000))
				return 1;
			memcpy(buf, smc, size);
		}
	}
	if (checkZeros(buf + size - 4, 4)) {
		bad = smcCheck(smc, size, xb.type);
		if (xb.type == 1) {
			if (bad) {
				log_printf(0, "\n******* ERROR: hacked or unknown SMC binary found? you should use a clean SMC binary for a retail image!\n\n");
				if (!(xb.bootFlags & 0x200000))
					return 1;
			} else
				log_printf(1, "known/clean SMC binary found! type 0x%x\n", 1);
			xb.bootFlags &= 0xf73fffff;
		} else if (xb.type > 5) {
			if (bad)
				log_printf(0, "\n******* WARNING: hacked or unknown SMC binary found? Just a warning, there are a lot of different SMC binaries for devkits!\n\n");
			else
				log_printf(1, "known/clean SMC binary found!\n");
			xb.bootFlags &= 0xf73fffff;
		} else if (bad) {
			if (xb.type == 3) {
				log_printf(1, "glitch hack found in SMC binary!\n");
				xb.bootFlags &= ~0x8000000;
			} else if (xb.type == 4 || xb.type == 5)
				log_printf(1, "\n******* WARNING: hacked or unknown SMC binary found!\n");
			else
				log_printf(1, "jtag hack found in SMC binary!\n");
		} else {
			if (xb.type == 3) {
				if (!(xb.bootFlags & 0x8000000))
					log_printf(0, "\n******* ERROR: clean SMC binary found? you should use a hacked SMC binary for glitch images.\n\n");
			} else if (xb.type == 4 || xb.type == 5)
				log_printf(1, "known/clean SMC binary found!\n");
			else {
				log_printf(0, "\n******* ERROR: clean SMC binary found? you should use a hacked SMC binary for JTAG images.\n\n");
				if (!(xb.bootFlags & 0x200000))
					return 1;
			}
		}
		patch = xb.bootFlags & 0x8c00000;
		if (patch)
			smcPatch(smc, size, patch);
		memcpy(smc, smcKey, 4);
		smcEncrypt(smc, size);
	}
	memcpy(buf, smc, size);
	smcSum((u32 *)buf, hash, size / 4);
	free(buf);
	return 0;
}

void cbaEncrypt(u8 *salt, u8 *cb, u8 *key, u32 size, int zero)
{
	memcpy(cb + 16, infoKey0, 16);
	XeCryptHmacSha(xb.key1bl, 16, cb + 16, 16, NULL, 0, NULL, 0, key, 16);
	if (!zero) {
		log_printf(1, "CBENC pairing set to: %02x %02x %02x\n", pairing[0], pairing[1], pairing[2]);
		memcpy(cb + 32, pairing, 3);
		cb[35] = xb.cbLdv;
		XeCryptHmacSha(xb.cpuKey, 16, key, 16, cb + 32, 16, salt, 16, cb + 48, 16);
	}
	XeCryptRc4(key, 16, cb + 32, size - 32);
}

void cbaEncryptZero(u8 *cb, u8 *key, u32 size)
{
	memset(pairing, 0, 3);
	memcpy(cb + 16, infoKey0, 16);
	memset(cb + 32, 0, 32);
	XeCryptHmacSha(xb.key1bl, 16, cb + 16, 16, NULL, 0, NULL, 0, key, 16);
	XeCryptRc4(key, 16, cb + 32, size - 32);
}

void cbaEncrypt2(u8 *salt, u8 *cb, u8 *key, u32 size, int zero)
{
	memcpy(cb + 16, infoKey0, 16);
	if (zero)
		memset(cb + 32, 0, 32);
	XeCryptHmacSha(xb.key1bl, 16, cb + 16, 16, NULL, 0, NULL, 0, key, 16);
	if (!zero) {
		memcpy(cb + 32, pairing, 3);
		cb[35] = xb.cbLdv;
		XeCryptHmacSha(xb.cpuKey, 16, key, 16, cb + 32, 16, salt, 16, cb + 48, 16);
	}
	XeCryptRc4(key, 16, cb + 32, size - 32);
}

void cbbEncrypt(u8 *salt, u8 *cbb, u8 *cbaKey, u8 *cba, u8 *key, u32 size, int zero)
{
	u16 flags = getBeU16(cba + 6);
	u8 *ck;
	u8 hdr[16];

	memcpy(cbb + 16, infoKey1, 16);
	ck = !(flags & 1) ? xb.cpuKey : zeroKey;
	if (flags & 0x800)
		log_printf(1, "\t**dual CB flag detected!**\n");
	if (flags & 0x1000) {
		log_printf(1, "\t**15572+ CBB crypto method detected!**\n");
		memcpy(hdr, cba, 16);
		hdr[6] = 0;
		hdr[7] = 0;
		XeCryptHmacSha(cbaKey, 16, cbb + 16, 16, ck, 16, hdr, 16, key, 16);
	} else
		XeCryptHmacSha(cbaKey, 16, cbb + 16, 16, ck, 16, NULL, 0, key, 16);
	if (zero) {
		memset(pairing, 0, 3);
		memset(cbb + 32, 0, 32);
	} else {
		memcpy(cbb + 32, pairing, 3);
		cbb[35] = xb.cbLdv;
		if (!(flags & 1))
			XeCryptHmacSha(xb.cpuKey, 16, key, 16, cbb + 32, 16, salt, 16, cbb + 48, 16);
		else
			log_printf(1, "\t** CBB crypto method set to work with mfg CBA!**\n");
	}
	XeCryptRc4(key, 16, cbb + 32, size - 32);
}

void cdEncryptZero(u8 *cd, u8 *key, u32 size)
{
	u8 zero[16];

	memset(zero, 0, 16);
	memcpy(cd + 16, infoKey1, 16);
	XeCryptHmacSha(zero, 16, cd + 16, 16, NULL, 0, NULL, 0, key, 16);
	XeCryptRc4(key, 16, cd + 32, size - 32);
}

void cdEncrypt(u8 *cd, u8 *prevKey, u8 *key, u32 size)
{
	memcpy(cd + 16, infoKey2, 16);
	XeCryptHmacSha(prevKey, 16, cd + 16, 16, NULL, 0, NULL, 0, key, 16);
	XeCryptRc4(key, 16, cd + 32, size - 32);
}

void cdEncryptCpu(u8 *cd, u8 *prevKey, u8 *key, u32 size)
{
	memcpy(cd + 16, infoKey2, 16);
	XeCryptHmacSha(prevKey, 16, cd + 16, 16, NULL, 0, NULL, 0, key, 16);
	XeCryptHmacSha(xb.cpuKey, 16, key, 16, NULL, 0, NULL, 0, key, 16);
	XeCryptRc4(key, 16, cd + 32, size - 32);
}

void ceEncrypt(u8 *ce, u8 *prevKey, u8 *key, u32 size)
{
	memcpy(ce + 16, infoKey3, 16);
	XeCryptHmacSha(prevKey, 16, ce + 16, 16, NULL, 0, NULL, 0, key, 16);
	XeCryptRc4(key, 16, ce + 32, size - 32);
}

/* The slot index i and the count n are separate (the original computes
   the last index as trips + 2 but n as (trips + 1) + 1); n is 16-bit, so
   its add isn't CSE'd with the index's. */
__attribute__((always_inline))
inline short cfPatchSlots(part_t *cf, u32 extra, u16 block, u32 max)
{
	u8 *buf = cf->buf;
	u32 end = cf->size + extra;
	u32 over;
	short n = 0;
	u32 i;
	u16 *tbl = (u16 *)(buf + 48);

	if (__builtin_expect(end > max, 1)) {
		over = end - max;
		cf->f428 = max - cf->size;
		cf->f424 = over;
		for (i = 1; over > 0x4000; i++, over -= 0x4000) {
			tbl[i] = SWAP16(block + i - 1);
			n++;
		}
		if (over) {
			tbl[i] = SWAP16(block + i - 1);
			n++;
		}
	}
	tbl[0] = SWAP16(n);
	return n;
}

u16 cfEncrypt(part_t *cf, u32 extra, u16 block, int keep, u32 max)
{
	u8 key[16];
	u8 salt[16];
	short n;
	u8 *buf;

	memcpy(salt, infoKey4, 16);
	if (!keep) {
		buf = cf->buf;
		memset(buf + 32, 0, 528);
		if (xb.type == 2)
			cf->buf[539] = 1;
		else
			cf->buf[539] = 0;
		memcpy(cf->buf + 540, pairing, 3);
		cf->buf[543] = xb.cfLdv;
	}
	n = cfPatchSlots(cf, extra, block, max);
	XeCryptHmacSha(xb.key1bl, 16, salt, 16, NULL, 0, NULL, 0, key, 16);
	if (!keep) {
		memcpy(cf->buf + 32, key, 16);
		XeCryptHmacSha(xb.cpuKey, 16, cf->buf, 0x220, NULL, 0, NULL, 0, cf->buf + 544, 16);
	}
	buf = cf->buf;
	memcpy(cf->f414, buf + 816, 16);
	memcpy(buf + 32, salt, 16);
	XeCryptRc4(key, 16, cf->buf + 48, cf->size - 48);
	return n;
}

void cgEncrypt(u8 *cg, u8 *prevKey, u8 *key, u32 size)
{
	memcpy(cg + 16, infoKey5, 16);
	XeCryptHmacSha(prevKey, 16, cg + 16, 16, NULL, 0, NULL, 0, key, 16);
	XeCryptRc4(key, 16, cg + 32, size - 32);
}

void kvEncrypt(u8 *kv, u32 size)
{
	u8 ver[2] = { 0x07, 0x12 };
	u8 key[16];

	memcpy(kv + 16, kvSalt, 8);
	XeCryptHmacSha(xb.cpuKey, 16, kv + 16, size - 16, ver, 2, NULL, 0, kv, 16);
	XeCryptHmacSha(xb.cpuKey, 16, kv, 16, NULL, 0, NULL, 0, key, 16);
	XeCryptRc4(key, 16, kv + 16, size - 16);
}

void kvEncryptAlt(u8 *kv, u32 size)
{
	u8 ver[2] = { 0x07, 0x12 };
	u8 key[16];

	memcpy(kv + 16, kvAltSalt, 8);
	XeCryptHmacSha(xb.cpuKey, 16, kv + 16, size - 16, ver, 2, NULL, 0, kv, 16);
	XeCryptHmacSha(xb.cpuKey, 16, kv, 16, NULL, 0, NULL, 0, key, 16);
	XeCryptRc4(key, 16, kv + 16, size - 16);
}

int shaCheck(u8 *buf, u32 size, u32 hashOff, u32 hashLen, u32 dataOff, u8 *hashOut)
{
	u8 hash[20];

	XeCryptSha(buf + dataOff, size - dataOff, NULL, 0, NULL, 0, hash, 20);
	if (memcmp(buf + hashOff, hash, hashLen) == 0) {
		if (hashOut)
			memcpy(hashOut, hash, 20);
		return 1;
	}
	return 0;
}

void shaHeader(u8 *buf)
{
	XeCryptSha(buf + 20, 0x1ec, NULL, 0, NULL, 0, buf, 20);
}

static int kvHashOk(u8 *kv, u32 size)
{
	u8 ver[2] = { 0x07, 0x12 };
	u8 hash[16];

	XeCryptHmacSha(xb.cpuKey, 16, kv + 16, size - 16, ver, 2, NULL, 0, hash, 16);
	return memcmp(kv, hash, 16) == 0;
}

/* The size check comes after the 0x3ff0 fix-up (profile estimated before
   jump threading: a colder main path makes alt a caller-saved ecx).  The
   hints and labels give bb-reorder the original's trace order and LRA
   its spill-slot order (wip/README.md). */
void kvPrepare(part_t *kv, int alt)
{
	const char *file = "kv.bin", *name = "kv";
	u8 *buf, *nbuf;

	if (alt) {
		file = "kv_alt.bin";
		name = "alt kv";
	}
	if (kv->size == 0x3ff0) {
		nbuf = malloc(0x4000);
		memset(nbuf, 0, 16);
		memcpy(nbuf + 16, kv->buf, 0x3ff0);
		free(kv->buf);
		kv->buf = nbuf;
		kv->size = 0x4000;
	}
	if (__builtin_expect(kv->size != 0x4000, 1)) {
		log_printf(0, "\n******* ERROR: %s is not the correct size! Skipping verification and encryption!\n", file);
		return;
	}
	buf = malloc(0x4000);
	memcpy(buf, kv->buf, 0x4000);
	if (__builtin_expect(!checkZeros(buf, 16), 0)) {
		if (!kvHashOk(buf, kv->size)) {
			if (__builtin_expect(checkZeros(buf + 56, 88), 0)) {
				log_printf(1, "%s appears to be decrypted already, but the hash does not match the CPU key...", file);
				log_printf(0, "\n******* WARNING: could not verify pre-decrypted keyvault, please be sure your provided a valid %s!\n", file);
			} else {
				log_printf(1, "%s appears to be encrypted, attempting to decrypt...", file);
				memcpy(buf, kv->buf, kv->size);
				if (!verifyExtended(buf, 0x4000)) {
				failed: __attribute__((hot));
					log_printf(1, "Failed!\n%s could not be decrypted!\n", file);
					log_printf(0, "\n******* ERROR: could not decrypt %s, please be sure your provided a valid %s!\n", name, file);
					memcpy(buf, kv->buf, kv->size);
				} else
					log_printf(1, "Success!\n");
			}
		} else {
		hashOk: __attribute__((hot));
		}
	} else if (!checkZeros(kv->buf + 88, 8))
		log_printf(0, "\n******* ERROR: please be sure your provided a DEcrypted %s!\n", file);
	else {
	zerosOk: __attribute__((hot));
	}
	memcpy(kv->buf, buf, kv->size);
	if (__builtin_expect(!alt, 0)) {
		kvSet(kv->buf);
		kvEncrypt(kv->buf, kv->size);
	} else
		kvEncryptAlt(kv->buf, kv->size);
	free(buf);
}

void extendedPrepare(part_t *ext)
{
	u8 *buf;

	if (ext->size != 0x4000) {
		if (!ext->size)
			log_printf(1, "******* WARNING: extended.bin was not provided or was invalid! Making up an clean/empty extended.bin!\n");
		else
			log_printf(1, "******* WARNING: extended.bin is not the correct size! Making up an clean/empty extended.bin!\n");
		if (ext->buf)
			free(ext->buf);
		ext->size = 0x4000;
		ext->buf = calloc(0x4000, 1);
	}
	buf = malloc(0x4000);
	memcpy(buf, ext->buf, 0x4000);
	if (!checkZeros(buf, 16) && !kvHashOk(buf, ext->size)) {
		log_printf(1, "extended.bin appears to be encrypted, attempting to decrypt...");
		memcpy(buf, ext->buf, ext->size);
		if (verifyExtended(buf, 0x4000))
			log_printf(1, "Success!\n");
		else {
			log_printf(1, "Failed!\nextended.bin could not be decrypted, filling clean/empty data.\n");
			memset(buf, 0, ext->size);
		}
	}
	memcpy(ext->buf, buf, ext->size);
	free(buf);
	kvEncrypt(ext->buf, ext->size);
}

void secdataPrepare(part_t *sd, u8 *date)
{
	u8 key[16];

	if (sd->size != 0x400) {
		if (!sd->size)
			log_printf(1, "******* WARNING: secdata.bin was not provided or was invalid! Making up an clean/empty secdata.bin!\n");
		else
			log_printf(1, "******* WARNING: secdata.bin is not the correct size! Making up an clean/empty secdata.bin!\n");
		free(sd->buf);
		sd->size = 0x400;
		sd->buf = calloc(0x400, 1);
	}
	memcpy(sd->buf + 16, secdataKey, 8);
	memcpyrev(sd->buf + 32, date, 8);
	sd->buf[24] = 1;
	sd->buf[25] = xb.cfLdv;
	XeCryptHmacSha(xb.cpuKey, 16, sd->buf + 16, sd->size - 16, NULL, 0, NULL, 0, sd->buf, 16);
	XeCryptHmacSha(xb.cpuKey, 16, sd->buf, 16, NULL, 0, NULL, 0, key, 16);
	XeCryptRc4(key, 16, sd->buf + 16, sd->size - 16);
}

void crlEncrypt(u8 *crl, u32 size, u8 *date)
{
	u8 *buf = malloc(size);
	u8 key[16];
	u8 iv[16];
	AESSTATE aes;
	int ok;

	memcpy(buf, crl, size);
	if (!shaCheck(crl, size, 12, 20, 336, NULL)) {
		log_printf(1, "crl appears crypted, attempting to decrypt with CPU key...");
		if (verifyCrl(buf, size, 1)) {
			log_printf(1, "success!\n");
			memcpy(crl, buf, size);
		} else {
			log_printf(1, "failed! Trying alternate key...");
			memcpy(buf, crl, size);
			if (verifyCrl(buf, size, 0)) {
				log_printf(1, "success!\n");
				memcpy(crl, buf, size);
			} else
				log_printf(1, "failed!\n");
		}
	}
	if (shaCheck(crl, size, 12, 20, 336, NULL)) {
		memcpyrev(crl + 320, date, 8);
		memcpy(key, crlKey, 16);
		memcpy(iv, crlKey + 16, 16);
		memcpy(crl + 288, crlKey + 16, 16);
		crl[335] = xb.cfLdv;
		memcpy(buf, crl, size);
		XeCryptAesKey(&aes, key);
		XeCryptAesCbc(&aes, buf + 320, 16, crl + 320, iv, 1);
		memcpy(iv, crl + 320, 16);
		XeCryptAesCbc(&aes, buf + 336, size - 336, crl + 336, iv, 1);
		XeCryptAesKey(&aes, xb.cpuKey);
		XeCryptAesEcb(&aes, key, crl + 304, 1);
	} else
		log_printf(0, "\n******* ERROR: crl data appears to be crypted with the wrong key or damaged!\n");
	free(buf);
}

void daeEncryptOne(u8 *dae, u32 size, u8 *date)
{
	u8 *buf = malloc(size);
	u8 hash[16];
	u8 iv[16];
	AESSTATE aes;

	memcpy(dae + 288, daeKey, 32);
	dae[289] |= 1;
	memcpyrev(dae + 304, date, 8);
	dae[319] = xb.cfLdv;
	memcpy(buf, dae, size);
	memset(iv, 0, 16);
	XeCryptHmacSha(xb.cpuKey, 16, buf + 288, 32, NULL, 0, NULL, 0, hash, 16);
	memcpy(dae + 320, hash, 16);
	memcpy(buf, dae, size);
	XeCryptAesKey(&aes, xb.cpuKey);
	XeCryptAesCbc(&aes, buf + 304, size - 304, dae + 304, iv, 1);
	free(buf);
}

void fcrtEncrypt(u8 *fcrt, u32 size)
{
	u8 iv[16];
	u8 hash[20];
	u32 off;
	AESSTATE aes;

	memcpy(iv, fcrt + 256, 16);
	if (size != 0x4000) {
		log_printf(0, "****** ERROR: FCRT encrypt invalid size!\n");
		return;
	}
	off = getBeU32(fcrt + 284);
	if (__builtin_expect(off < 0x4000, 1)) {
		XeCryptSha(fcrt + off, 0x4000 - off, NULL, 0, NULL, 0, hash, 20);
		if (memcmp(fcrt + 300, hash, 20) && verifyFcrt(fcrt, 0x4000) != 1) {
			log_printf(0, "****** WARNING: FCRT data appears to be crypted or damaged!! Skipping encryption.\n");
			return;
		}
		XeCryptAesKey(&aes, xb.cpuKey);
		XeCryptAesCbc(&aes, fcrt + off, 0x4000 - off, fcrt + off, iv, 1);
	} else
		log_printf(1, "**** ERROR: FCRT encrypt invalid offset!\n");
}

void daeEncrypt(u8 *buf, u32 size, u8 *date)
{
	u8 *orig = malloc(size);
	u8 *dae;
	u32 off = 0;
	u32 len;
	int n = 0;
	__asm__("" : "+b"(off));

	memcpy(orig, buf, size);
	if (__builtin_expect(size, 1)) do {
		dae = buf + off;
		__asm__("" :: "d"(off));
		if (__builtin_expect(buf[off] != 'D', 0) || __builtin_expect(buf[off + 1] != 'A', 1) || __builtin_expect(buf[off + 2] != 'E', 1) || __builtin_expect(buf[off + 3] != 'P', 1)) {
			log_printf(0, "\n******* ERROR: dae segment does not have the expected header!\n");
			break;
		}
		len = (u16)((buf[off + 4] << 8) + buf[off + 5]);
		if (!shaCheck(dae, len, 12, 20, 336, NULL)) {
			if (!n)
				log_printf(1, "dae appears encrypted, attempting to decrypt with CPU key...");
			memcpy(dae, orig + off, len);
			daeDecrypt(dae, len, 1);
			if (shaCheck(dae, len, 12, 20, 336, NULL)) {
				ok: __attribute__((cold));
				log_printf(1, "success!\n");
				daeEncryptOne(dae, len, date);
				n++;
				goto next;
			}
			if (!n)
				log_printf(1, "failed! Attempting to decrypt with alternate key...\n");
			memcpy(dae, orig + off, len);
			daeDecrypt(dae, len, 0);
			if (shaCheck(dae, len, 12, 20, 336, NULL)) {
				if (!n)
					log_printf(1, "success!\n");
			} else {
				if (!n)
					log_printf(0, "failed!\n******* ERROR: dae hash incorrect, could not verify decrypted dae!\n");
				n = 0;
				off = size + 1;
				goto next;
			}
		}
		daeEncryptOne(dae, len, date);
		n++;
	next:
		off += len;
	} while (off < size);
	if (n != 2) {
		log_printf(0, "\n******* WARNING: dae data appears to be crypted with a different key or damaged! Skipping encryption.\n");
	}
	free(orig);
}


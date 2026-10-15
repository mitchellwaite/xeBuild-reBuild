/* keys: CPU/1BL keys, pairing, the per-image HMAC nonces, and encrypting
   the bootloaders, SMC, keyvault, extended, secdata, CRL, DAE and FCRT
   for the image being built.  Mixed object: the functions here are
   spliced into keys.s (re/splice.py), which still holds the rest and
   the data, so strings and key buffers are extern names for the
   .s's.  wip/app/keys.c is the whole draft. */
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

typedef struct { u8 b[8]; } q8;
typedef struct { u8 b[16]; } q16;

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
u32 getBeU32(const u8 *p);
u32 sumBytes(const u8 *p, u32 len);
void memcpyrev(u8 *dst, const u8 *src, int len);
int unscramble(u8 *buf, u32 len);
int smcCheck(u8 *smc, int len, int type);
void smcPatch(u8 *smc, int len, u32 flags);
void kvSet(u8 *buf);
int verifyExtended(void *buf, int size);
int verifyCrl(void *buf, int size, int perBox);
void daeDecrypt(u8 *dae, u32 size, int perBox);
int verifyFcrt(u8 *fcrt, u32 size);

extern struct xebuild xb;
extern u8 key1bl[16];
extern u8 cpuKey[16];
extern u8 key28c[16];

extern u8 secdataKey[8];
extern u8 daeKey[32];
extern u8 crlKey[32];
extern u8 smcKey[4];
extern u8 kvAltSalt[8];
extern u8 kvSalt[8];
extern u8 infoKey5[16];
extern u8 infoKey4[16];
extern u8 infoKey3[16];
extern u8 infoKey2[16];
extern u8 infoKey1[16];
extern u8 infoKey0[16];
extern u8 zeroKey[16];
extern u8 pairing[3];

/* strings in keys.s */
extern const char msg_initRandom[];	/* "initializing random nonces\n" */
extern const char msg_initStatic[];	/* "initializing static pairing value\n" */
extern const char msg_pairingSet[];	/* "pairing set to: %02x %02x %02x\n" */
extern const char str_valid[];	/* "valid" */
extern const char str_error[];	/* "error" */
extern const char msg_weight[];	/* " (weight:0x%x %s; ecd: %s)" */
extern const char msg_cpuKeySet[];	/* "CPU Key set to: 0x" */
extern const char str_hexByte[];	/* "%02X" */
extern const char str_newline[];	/* "\n" */
extern const char msg_cpuKeyWarn[];	/* "\n***** WARNING: CPU key check faile..." */
extern const char msg_cpuKeyChars[];	/* "\n******* ERROR: invalid or unexpect..." */
extern const char msg_cpuKeyLen[];	/* "\n***** ERROR: unable to set CPU key..." */
extern const char msg_cpuKeySet2[];	/* "CPU Key set to  : " */
extern const char msg_1blKeySet[];	/* "1BL Key set to  : 0x" */
extern const char msg_1blSum[];	/* " sum: 0x%x (expects: 0x983)\n" */
extern const char msg_xexKeySet[];	/* "xex Key set to  : 0x" */
extern const char msg_xexSum[];	/* " sum: 0x%x (expects: 0x800)\n" */
extern const char msg_1blBad[];	/* "\n******* ERROR: 1BL key 0x" */
extern const char msg_1blBad2[];	/* " does not appear to be correct!\n" */
extern const char msg_1blChars[];	/* "\n******* ERROR: invalid or unexpect..." */
extern const char msg_1blLen[];	/* "\n***** ERROR: unable to set 1BL key..." */
extern const char msg_1blBadStr[];	/* "\n******* ERROR: 1BL key 0x%s " */
extern const char msg_1blBadStr2[];	/* "does not appear to be correct!\n" */
extern const char msg_cbencPairing[];	/* "CBENC pairing set to: %02x %02x %02x..." */
extern const char msg_dualCb[];	/* "\t**dual CB flag detected!**\n" */
extern const char msg_cbb15572[];	/* "\t**15572+ CBB crypto method detecte..." */
extern const char msg_cbbMfg[];	/* "\t** CBB crypto method set to work w..." */
extern const char str_Success[];	/* "Success!\n" */
extern const char msg_extMissing[];	/* "******* WARNING: extended.bin was no..." */
extern const char msg_extSize[];	/* "******* WARNING: extended.bin is not..." */
extern const char msg_extEncrypted[];	/* "extended.bin appears to be encrypted..." */
extern const char msg_extDecryptFail[];	/* "Failed!\nextended.bin could not be d..." */
extern const char msg_sdMissing[];	/* "******* WARNING: secdata.bin was not..." */
extern const char msg_sdSize[];	/* "******* WARNING: secdata.bin is not ..." */
extern const char str_successNl[];	/* "success!\n" */
extern const char msg_crlRetry[];	/* "failed! Trying alternate key..." */
extern const char str_failedNl[];	/* "failed!\n" */
extern const char msg_crlCrypted[];	/* "crl appears crypted, attempting to d..." */
extern const char msg_crlBad[];	/* "\n******* ERROR: crl data appears to..." */

void keysInit(int random)
{
	aes_init();
	if (random) {
		log_printf(1, msg_initRandom);
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
		log_printf(1, msg_initStatic);
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
		log_printf(1, msg_pairingSet, pairing[0], pairing[1], pairing[2]);
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
	log_printf(level, msg_weight, weight,
		wok ? str_valid : str_error, ecd ? str_valid : str_error);
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
				cpuKey[i] = myatox8(str);
			log_printf(1, msg_cpuKeySet);
			for (i = 0; i < 16; i++)
				log_printf(1, str_hexByte, cpuKey[i]);
			ret = 1;
			if (!checkZeros(cpuKey, 16)) {
				if (checkCpuKey(1, cpuKey))
					log_printf(0, str_newline);
				else
					log_printf(0, msg_cpuKeyWarn);
			}
		} else
			log_printf(0, msg_cpuKeyChars);
	} else {
		ret = 0;
		log_printf(0, msg_cpuKeyLen, str, len);
	}
	return ret;
}

int setCpuKey(int level, u8 *key)
{
	memcpy(cpuKey, key, 16);
	log_printf(level, msg_cpuKeySet2);
	showKey(level, key);
	if (!checkZeros(cpuKey, 16) && !checkCpuKey(level, cpuKey))
		log_printf(level, msg_cpuKeyWarn);
	log_printf(level, str_newline);
	return 1;
}

u32 calcXexKey(void)
{
	u8 key[16] = { 0x95, 0x27, 0x72, 0xbf, 0x47, 0xc0, 0xf6, 0x98,
		0x5c, 0x7d, 0xf2, 0x50, 0x65, 0x4d, 0x55, 0xcd };
	u8 junk[16];
	u8 hash[16];

	memcpy(junk, "thisisjustajunky", 16);
	XeCryptHmacSha(junk, 16, key1bl, 16, NULL, 0, NULL, 0, hash, 16);
	memcpy(key28c, key, 16);
	XeCryptRc4(hash, 16, key28c, 16);
	return sumBytes(key28c, 16);
}

int check1blKey(void)
{
	u32 sum1 = sumBytes(key1bl, 16);
	u32 sum2 = calcXexKey();

	if (sum1 == 0x983 && sum2 == 0x800) {
		log_printf(1, msg_1blKeySet);
		showKey(1, key1bl);
		log_printf(1, msg_1blSum, sum1);
		log_printf(1, msg_xexKeySet);
		showKey(1, key28c);
		log_printf(1, msg_xexSum, sum2);
		return 1;
	}
	return 0;
}

int set1blKey(u8 *key)
{
	memcpy(key1bl, key, 16);
	if (check1blKey())
		return 1;
	log_printf(0, msg_1blBad);
	showKey(0, key1bl);
	log_printf(0, msg_1blBad2);
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
				key1bl[i] = myatox8(p);
			if (check1blKey())
				return 1;
			log_printf(0, msg_1blBadStr, str);
			log_printf(0, msg_1blBadStr2);
			return 0;
		}
		log_printf(0, msg_1blChars);
		return 0;
	}
	log_printf(0, msg_1blLen, str, len);
	return 0;
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

void cbaEncrypt(u8 *salt, u8 *cb, u8 *key, u32 size, int zero)
{
	memcpy(cb + 16, infoKey0, 16);
	XeCryptHmacSha(key1bl, 16, cb + 16, 16, NULL, 0, NULL, 0, key, 16);
	if (!zero) {
		log_printf(1, msg_cbencPairing, pairing[0], pairing[1], pairing[2]);
		memcpy(cb + 32, pairing, 3);
		cb[35] = xb.cbLdv;
		XeCryptHmacSha(cpuKey, 16, key, 16, cb + 32, 16, salt, 16, cb + 48, 16);
	}
	XeCryptRc4(key, 16, cb + 32, size - 32);
}

void cbaEncryptZero(u8 *cb, u8 *key, u32 size)
{
	memset(pairing, 0, 3);
	memcpy(cb + 16, infoKey0, 16);
	memset(cb + 32, 0, 32);
	XeCryptHmacSha(key1bl, 16, cb + 16, 16, NULL, 0, NULL, 0, key, 16);
	XeCryptRc4(key, 16, cb + 32, size - 32);
}

void cbaEncrypt2(u8 *salt, u8 *cb, u8 *key, u32 size, int zero)
{
	memcpy(cb + 16, infoKey0, 16);
	if (zero)
		memset(cb + 32, 0, 32);
	XeCryptHmacSha(key1bl, 16, cb + 16, 16, NULL, 0, NULL, 0, key, 16);
	if (!zero) {
		memcpy(cb + 32, pairing, 3);
		cb[35] = xb.cbLdv;
		XeCryptHmacSha(cpuKey, 16, key, 16, cb + 32, 16, salt, 16, cb + 48, 16);
	}
	XeCryptRc4(key, 16, cb + 32, size - 32);
}

void cbbEncrypt(u8 *salt, u8 *cbb, u8 *cbaKey, u8 *cba, u8 *key, u32 size, int zero)
{
	u16 flags = getBeU16(cba + 6);
	u8 *ck;
	u8 hdr[16];

	memcpy(cbb + 16, infoKey1, 16);
	ck = !(flags & 1) ? cpuKey : zeroKey;
	if (flags & 0x800)
		log_printf(1, msg_dualCb);
	if (flags & 0x1000) {
		log_printf(1, msg_cbb15572);
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
			XeCryptHmacSha(cpuKey, 16, key, 16, cbb + 32, 16, salt, 16, cbb + 48, 16);
		else
			log_printf(1, msg_cbbMfg);
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
	XeCryptHmacSha(cpuKey, 16, key, 16, NULL, 0, NULL, 0, key, 16);
	XeCryptRc4(key, 16, cd + 32, size - 32);
}

void ceEncrypt(u8 *ce, u8 *prevKey, u8 *key, u32 size)
{
	memcpy(ce + 16, infoKey3, 16);
	XeCryptHmacSha(prevKey, 16, ce + 16, 16, NULL, 0, NULL, 0, key, 16);
	XeCryptRc4(key, 16, ce + 32, size - 32);
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
	XeCryptHmacSha(cpuKey, 16, kv + 16, size - 16, ver, 2, NULL, 0, kv, 16);
	XeCryptHmacSha(cpuKey, 16, kv, 16, NULL, 0, NULL, 0, key, 16);
	XeCryptRc4(key, 16, kv + 16, size - 16);
}

void kvEncryptAlt(u8 *kv, u32 size)
{
	u8 ver[2] = { 0x07, 0x12 };
	u8 key[16];

	memcpy(kv + 16, kvAltSalt, 8);
	XeCryptHmacSha(cpuKey, 16, kv + 16, size - 16, ver, 2, NULL, 0, kv, 16);
	XeCryptHmacSha(cpuKey, 16, kv, 16, NULL, 0, NULL, 0, key, 16);
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

	XeCryptHmacSha(cpuKey, 16, kv + 16, size - 16, ver, 2, NULL, 0, hash, 16);
	return memcmp(kv, hash, 16) == 0;
}

void extendedPrepare(part_t *ext)
{
	u8 *buf;

	if (ext->size != 0x4000) {
		if (!ext->size)
			log_printf(1, msg_extMissing);
		else
			log_printf(1, msg_extSize);
		if (ext->buf)
			free(ext->buf);
		ext->size = 0x4000;
		ext->buf = calloc(0x4000, 1);
	}
	buf = malloc(0x4000);
	memcpy(buf, ext->buf, 0x4000);
	if (!checkZeros(buf, 16) && !kvHashOk(buf, ext->size)) {
		log_printf(1, msg_extEncrypted);
		memcpy(buf, ext->buf, ext->size);
		if (verifyExtended(buf, 0x4000))
			log_printf(1, str_Success);
		else {
			log_printf(1, msg_extDecryptFail);
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
			log_printf(1, msg_sdMissing);
		else
			log_printf(1, msg_sdSize);
		free(sd->buf);
		sd->size = 0x400;
		sd->buf = calloc(0x400, 1);
	}
	memcpy(sd->buf + 16, secdataKey, 8);
	memcpyrev(sd->buf + 32, date, 8);
	sd->buf[24] = 1;
	sd->buf[25] = xb.cfLdv;
	XeCryptHmacSha(cpuKey, 16, sd->buf + 16, sd->size - 16, NULL, 0, NULL, 0, sd->buf, 16);
	XeCryptHmacSha(cpuKey, 16, sd->buf, 16, NULL, 0, NULL, 0, key, 16);
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
		log_printf(1, msg_crlCrypted);
		if (verifyCrl(buf, size, 1)) {
			log_printf(1, str_successNl);
			memcpy(crl, buf, size);
		} else {
			log_printf(1, msg_crlRetry);
			memcpy(buf, crl, size);
			if (verifyCrl(buf, size, 0)) {
				log_printf(1, str_successNl);
				memcpy(crl, buf, size);
			} else
				log_printf(1, str_failedNl);
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
		XeCryptAesKey(&aes, cpuKey);
		XeCryptAesEcb(&aes, key, crl + 304, 1);
	} else
		log_printf(0, msg_crlBad);
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
	XeCryptHmacSha(cpuKey, 16, buf + 288, 32, NULL, 0, NULL, 0, hash, 16);
	memcpy(dae + 320, hash, 16);
	memcpy(buf, dae, size);
	XeCryptAesKey(&aes, cpuKey);
	XeCryptAesCbc(&aes, buf + 304, size - 304, dae + 304, iv, 1);
	free(buf);
}

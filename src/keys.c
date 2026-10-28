/* keys: CPU/1BL keys, pairing, the per-image HMAC nonces, and encrypting
   the bootloaders, SMC, keyvault, extended, secdata, CRL, DAE and FCRT
   for the image being built. */
#include <stdlib.h>
#include <string.h>

#include "crypto/xecrypt.h"
#include "xebuild.h"
#include "bootloaders.h"
#include "fileutil.h"
#include "keys.h"
#include "keyvault.h"
#include "log.h"
#include "smc.h"

/* getBeU32 and verifyFcrt redeclared pure (only here: in the headers it
   changes other objects' code): fcrtEncrypt's block order needs them left
   out of the call heuristic (with its off < 0x4000 hint at
   builtin-expect-probability 60) */
uint32_t getBeU32(const uint8_t *p) __attribute__((pure));
int verifyFcrt(uint8_t *fcrt, uint32_t size) __attribute__((pure));
/* external copy of the always_inline cfPatchSlots */
short cfPatchSlots(struct fileent *cf, uint32_t extra, uint16_t block, uint32_t max);

#define SWAP32(x) (((x) << 24) + ((x) >> 24) + (((x) << 8) & 0xff0000) + (((x) >> 8) & 0xff00))
#define SWAP16(x) ((((x) & 0xff) << 8) + (((x) & 0xff00) >> 8))

uint8_t secdataKey[8] = { 0x5a, 0xa4, 0xd1, 0xd2, 0x7d, 0xe4, 0x45, 0x3e };
uint8_t daeKey[32] = {
	0xa1, 0xb2, 0x69, 0x50, 0x58, 0xf4, 0xed, 0x05, 0xe5, 0x80, 0xc7, 0xee, 0x18, 0x9a, 0x27, 0xb5,
	0xac, 0x5e, 0xbc, 0x70, 0x89, 0x29, 0x65, 0x90, 0xf4, 0x24, 0xed, 0x2a, 0xd3, 0x62, 0x83, 0x14
};
uint8_t crlKey[32] = {
	0xc7, 0x03, 0xb9, 0x32, 0xd4, 0x07, 0x7d, 0x41, 0x60, 0x52, 0xa8, 0x13, 0x5e, 0xde, 0x68, 0x18,
	0xd9, 0x75, 0x98, 0xa6, 0xf8, 0x5d, 0x9b, 0x86, 0x7b, 0xc4, 0x34, 0x99, 0xe3, 0x3d, 0xa4, 0xaa
};
uint8_t smcKey[4] = { 0x8e, 0x03, 0x75, 0xcc };
uint8_t kvAltSalt[8] = { 0x36, 0xca, 0xb0, 0x87, 0x8b, 0x83, 0xb7, 0xf6 };
uint8_t kvSalt[8] = { 0x36, 0xca, 0xb0, 0x87, 0x8b, 0x83, 0xb7, 0xf6 };
uint8_t infoKey5[16] = {
	0xb9, 0xa2, 0x1e, 0x3b, 0xfc, 0x2e, 0xab, 0xb4,
	0x19, 0x81, 0x2d, 0x8a, 0x85, 0xaa, 0xa8, 0xce
};
uint8_t infoKey4[16] = {
	0xce, 0xe5, 0x04, 0xee, 0x9f, 0x61, 0x2b, 0x9b,
	0xa5, 0x20, 0xf8, 0xeb, 0x0b, 0x64, 0x68, 0x2a
};
uint8_t infoKey3[16] = {
	0x56, 0xa9, 0x81, 0xcd, 0x8c, 0xbc, 0x07, 0x29,
	0xdd, 0x0b, 0x7b, 0xbc, 0x76, 0xe5, 0x79, 0x98
};
uint8_t infoKey2[16] = {
	0xb3, 0x38, 0x64, 0x1c, 0xeb, 0xd0, 0x1e, 0x10,
	0x2c, 0xdd, 0xe0, 0xf3, 0x19, 0xa1, 0x9f, 0x84
};
uint8_t infoKey1[16] = {
	0xfb, 0xe2, 0x70, 0x9a, 0xe7, 0xa1, 0x3f, 0x42,
	0xcf, 0xec, 0x45, 0x92, 0x8e, 0x3f, 0x0e, 0x37
};
uint8_t infoKey0[16] = {
	0x37, 0x10, 0xa2, 0xf2, 0x2e, 0xd5, 0xf0, 0xa8,
	0xe4, 0x9c, 0xb4, 0xc7, 0xa1, 0x39, 0x5d, 0xaa
};
uint8_t zeroKey[16] = { 0 };
uint8_t pairing[3] = { 0 };

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

void setCrlKey(uint8_t *key)
{
#if 1 == 1
	memcpy(crlKey, key + 16, 16);
	memcpy(crlKey + 16, key, 16);
#elif 1 == 2
	uint32_t *k = (uint32_t *)key, *c = (uint32_t *)crlKey;
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

void setDaeKey(uint8_t *key)
{
	memcpy(daeKey, key, 32);
}

void setSecdataKey(uint8_t *key)
{
	memcpy(secdataKey, key, 8);
}

void setInfoKey0(uint8_t *key)
{
	memcpy(infoKey0, key, 16);
}

void setInfoKey1(uint8_t *key)
{
	memcpy(infoKey1, key, 16);
}

void setInfoKey2(uint8_t *key)
{
	memcpy(infoKey2, key, 16);
}

void setInfoKey3(uint8_t *key)
{
	memcpy(infoKey3, key, 16);
}

void setInfoKey4(uint8_t *key)
{
	memcpy(infoKey4, key, 16);
}

void setInfoKey5(uint8_t *key)
{
	memcpy(infoKey5, key, 16);
}

void setKvSalt(uint8_t *key)
{
	memcpy(kvSalt, key, 8);
}

void setKvAltSalt(uint8_t *key)
{
	memcpy(kvAltSalt, key, 8);
}

void setSmcKey(uint8_t *key)
{
	memcpy(smcKey, key, 4);
}

int setPairing(uint32_t pair)
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

int checkCpuKey(int level, uint8_t *key)
{
	uint8_t mask[16] = { 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
		0xff, 0xff, 0xff, 0xff, 0xff, 0x03, 0, 0 };
	uint8_t tmp[16];
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

int setCpuKey(int level, uint8_t *key)
{
	memcpy(xb.cpuKey, key, 16);
	log_printf(level, "CPU Key set to  : ");
	showKey(level, key);
	if (!checkZeros(xb.cpuKey, 16) && !checkCpuKey(level, xb.cpuKey))
		log_printf(level, "\n***** WARNING: CPU key check failed, CPU key may not be valid!\n\n");
	log_printf(level, "\n");
	return 1;
}

void setFuseLdv(uint8_t *fuse, uint8_t ldv)
{
	uint32_t i;
	uint64_t cb, cf;

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

/* setFuseCpuKey, daeEncrypt and fcrtEncrypt expand their error blocks
   first, so their strings are arrays in the original's order
   (-fno-toplevel-reorder emits them here), aligned as literals are (4
   from 31 bytes, else 1) */
static const char msg_fuseCpuKey[] __attribute__((aligned(1))) = "Fuse CPU Key set to: 0x";
static const char msg_fuseNull[] __attribute__((aligned(4))) = "\nERROR: YOU SHOULD NOT BE SEEING THIS ERROR!\n";

void setFuseCpuKey(uint8_t *fuse)
{
	int i;

	if (__builtin_expect(fuse == NULL, 0)) {
		log_printf(0, msg_fuseNull);
		return;
	}
	memcpy(fuse + 24, xb.cpuKey, 8);
	memcpy(fuse + 32, xb.cpuKey, 16);
	memcpy(fuse + 48, xb.cpuKey + 8, 8);
	memcpy(xb.cpuKey, fuse + 32, 16);
	setFuseLdv(fuse, xb.cfLdv);
	log_printf(1, msg_fuseCpuKey);
	for (i = 32; i < 48; i++)
		log_printf(1, "%02X", fuse[i]);
	log_printf(1, "\n");
}

uint32_t calcXexKey(void)
{
	uint8_t key[16] = { 0x95, 0x27, 0x72, 0xbf, 0x47, 0xc0, 0xf6, 0x98,
		0x5c, 0x7d, 0xf2, 0x50, 0x65, 0x4d, 0x55, 0xcd };
	uint8_t junk[16];
	uint8_t hash[16];

	memcpy(junk, "thisisjustajunky", 16);
	XeCryptHmacSha(junk, 16, xb.key1bl, 16, NULL, 0, NULL, 0, hash, 16);
	memcpy(xb.key28c, key, 16);
	XeCryptRc4(hash, 16, xb.key28c, 16);
	return sumBytes(xb.key28c, 16);
}

int check1blKey(void)
{
	uint32_t sum1 = sumBytes(xb.key1bl, 16);
	uint32_t sum2 = calcXexKey();

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

int set1blKey(uint8_t *key)
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
static inline void smcSum(uint32_t *buf, uint8_t *out, uint32_t count)
{
	uint64_t s1 = 0, s2 = 0;
	long long sum1 = 0, sum2 = 0;
	uint32_t i, v;

	for (i = 0; i < count; i++) {
		v = SWAP32(buf[i]);
		sum1 += v;
		sum2 -= v;
		sum1 = (sum1 << 29) | (uint32_t)((uint32_t)(sum1 >> 32) >> 3);
		sum2 = (sum2 << 31) | (uint32_t)((uint32_t)(sum2 >> 32) >> 1);
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
void smcChecksum(uint32_t *buf, uint8_t *out, uint32_t count)
{
	smcSum(buf, out, count);
}

void smcEncrypt(uint8_t *buf, uint32_t len)
{
	uint8_t s[4] = { 'B', 'u', 'N', 'y' };
	uint32_t i, j = 0;
	int t;

	for (i = 0; i < len; i++) {
		buf[i] ^= s[j];
		t = buf[i] * 251;
		j = (j + 1) & 3;
		s[j] += t;
		s[(j + 1) & 3] += t >> 8;
	}
}

int smcPrepare(uint8_t *smc, uint8_t *hash, uint32_t size)
{
	uint8_t *buf = malloc(size);
	uint32_t patch;
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
	smcSum((uint32_t *)buf, hash, size / 4);
	free(buf);
	return 0;
}

void cbaEncrypt(uint8_t *salt, uint8_t *cb, uint8_t *key, uint32_t size, int zero)
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

void cbaEncryptZero(uint8_t *cb, uint8_t *key, uint32_t size)
{
	memset(pairing, 0, 3);
	memcpy(cb + 16, infoKey0, 16);
	memset(cb + 32, 0, 32);
	XeCryptHmacSha(xb.key1bl, 16, cb + 16, 16, NULL, 0, NULL, 0, key, 16);
	XeCryptRc4(key, 16, cb + 32, size - 32);
}

void cbaEncrypt2(uint8_t *salt, uint8_t *cb, uint8_t *key, uint32_t size, int zero)
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

void cbbEncrypt(uint8_t *salt, uint8_t *cbb, uint8_t *cbaKey, uint8_t *cba, uint8_t *key, uint32_t size, int zero)
{
	uint16_t flags = getBeU16(cba + 6);
	uint8_t *ck;
	uint8_t hdr[16];

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

void cdEncryptZero(uint8_t *cd, uint8_t *key, uint32_t size)
{
	uint8_t zero[16];

	memset(zero, 0, 16);
	memcpy(cd + 16, infoKey1, 16);
	XeCryptHmacSha(zero, 16, cd + 16, 16, NULL, 0, NULL, 0, key, 16);
	XeCryptRc4(key, 16, cd + 32, size - 32);
}

void cdEncrypt(uint8_t *cd, uint8_t *prevKey, uint8_t *key, uint32_t size)
{
	memcpy(cd + 16, infoKey2, 16);
	XeCryptHmacSha(prevKey, 16, cd + 16, 16, NULL, 0, NULL, 0, key, 16);
	XeCryptRc4(key, 16, cd + 32, size - 32);
}

void cdEncryptCpu(uint8_t *cd, uint8_t *prevKey, uint8_t *key, uint32_t size)
{
	memcpy(cd + 16, infoKey2, 16);
	XeCryptHmacSha(prevKey, 16, cd + 16, 16, NULL, 0, NULL, 0, key, 16);
	XeCryptHmacSha(xb.cpuKey, 16, key, 16, NULL, 0, NULL, 0, key, 16);
	XeCryptRc4(key, 16, cd + 32, size - 32);
}

void ceEncrypt(uint8_t *ce, uint8_t *prevKey, uint8_t *key, uint32_t size)
{
	memcpy(ce + 16, infoKey3, 16);
	XeCryptHmacSha(prevKey, 16, ce + 16, 16, NULL, 0, NULL, 0, key, 16);
	XeCryptRc4(key, 16, ce + 32, size - 32);
}

/* The slot index i and the count n are separate (the original computes
   the last index as trips + 2 but n as (trips + 1) + 1); n is 16-bit, so
   its add isn't CSE'd with the index's. */
__attribute__((always_inline))
inline short cfPatchSlots(struct fileent *cf, uint32_t extra, uint16_t block, uint32_t max)
{
	uint8_t *buf = cf->data;
	uint32_t end = cf->size + extra;
	uint32_t over;
	short n = 0;
	uint32_t i;
	uint16_t *tbl = (uint16_t *)(buf + 48);

	if (__builtin_expect(end > max, 1)) {
		over = end - max;
		cf->fsOffset = max - cf->size;
		cf->fsSize = over;
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

uint16_t cfEncrypt(struct fileent *cf, uint32_t extra, uint16_t block, int keep, uint32_t max)
{
	uint8_t key[16];
	uint8_t salt[16];
	short n;
	uint8_t *buf;

	memcpy(salt, infoKey4, 16);
	if (!keep) {
		buf = cf->data;
		memset(buf + 32, 0, 528);
		if (xb.type == 2)
			cf->data[539] = 1;
		else
			cf->data[539] = 0;
		memcpy(cf->data + 540, pairing, 3);
		cf->data[543] = xb.cfLdv;
	}
	n = cfPatchSlots(cf, extra, block, max);
	XeCryptHmacSha(xb.key1bl, 16, salt, 16, NULL, 0, NULL, 0, key, 16);
	if (!keep) {
		memcpy(cf->data + 32, key, 16);
		XeCryptHmacSha(xb.cpuKey, 16, cf->data, 0x220, NULL, 0, NULL, 0, cf->data + 544, 16);
	}
	buf = cf->data;
	memcpy(cf->key, buf + 816, 16);
	memcpy(buf + 32, salt, 16);
	XeCryptRc4(key, 16, cf->data + 48, cf->size - 48);
	return n;
}

void cgEncrypt(uint8_t *cg, uint8_t *prevKey, uint8_t *key, uint32_t size)
{
	memcpy(cg + 16, infoKey5, 16);
	XeCryptHmacSha(prevKey, 16, cg + 16, 16, NULL, 0, NULL, 0, key, 16);
	XeCryptRc4(key, 16, cg + 32, size - 32);
}

void kvEncrypt(uint8_t *kv, uint32_t size)
{
	uint8_t ver[2] = { 0x07, 0x12 };
	uint8_t key[16];

	memcpy(kv + 16, kvSalt, 8);
	XeCryptHmacSha(xb.cpuKey, 16, kv + 16, size - 16, ver, 2, NULL, 0, kv, 16);
	XeCryptHmacSha(xb.cpuKey, 16, kv, 16, NULL, 0, NULL, 0, key, 16);
	XeCryptRc4(key, 16, kv + 16, size - 16);
}

void kvEncryptAlt(uint8_t *kv, uint32_t size)
{
	uint8_t ver[2] = { 0x07, 0x12 };
	uint8_t key[16];

	memcpy(kv + 16, kvAltSalt, 8);
	XeCryptHmacSha(xb.cpuKey, 16, kv + 16, size - 16, ver, 2, NULL, 0, kv, 16);
	XeCryptHmacSha(xb.cpuKey, 16, kv, 16, NULL, 0, NULL, 0, key, 16);
	XeCryptRc4(key, 16, kv + 16, size - 16);
}

static int kvHashOk(uint8_t *kv, uint32_t size)
{
	uint8_t ver[2] = { 0x07, 0x12 };
	uint8_t hash[16];

	XeCryptHmacSha(xb.cpuKey, 16, kv + 16, size - 16, ver, 2, NULL, 0, hash, 16);
	return memcmp(kv, hash, 16) == 0;
}

/* The size check comes after the 0x3ff0 fix-up (profile estimated before
   jump threading: a colder main path makes alt a caller-saved ecx).  The
   hints and labels give bb-reorder the original's trace order and LRA
   its spill-slot order (wip/README.md). */
void kvPrepare(struct fileent *kv, int alt)
{
	const char *file = "kv.bin", *name = "kv";
	uint8_t *buf, *nbuf;

	if (alt) {
		file = "kv_alt.bin";
		name = "alt kv";
	}
	if (kv->size == 0x3ff0) {
		nbuf = malloc(0x4000);
		memset(nbuf, 0, 16);
		memcpy(nbuf + 16, kv->data, 0x3ff0);
		free(kv->data);
		kv->data = nbuf;
		kv->size = 0x4000;
	}
	if (__builtin_expect(kv->size != 0x4000, 1)) {
		log_printf(0, "\n******* ERROR: %s is not the correct size! Skipping verification and encryption!\n", file);
		return;
	}
	buf = malloc(0x4000);
	memcpy(buf, kv->data, 0x4000);
	if (__builtin_expect(!checkZeros(buf, 16), 0)) {
		if (!kvHashOk(buf, kv->size)) {
			if (__builtin_expect(checkZeros(buf + 56, 88), 0)) {
				log_printf(1, "%s appears to be decrypted already, but the hash does not match the CPU key...", file);
				log_printf(0, "\n******* WARNING: could not verify pre-decrypted keyvault, please be sure your provided a valid %s!\n", file);
			} else {
				log_printf(1, "%s appears to be encrypted, attempting to decrypt...", file);
				memcpy(buf, kv->data, kv->size);
				if (!verifyExtended(buf, 0x4000)) {
				failed: __attribute__((hot));
					log_printf(1, "Failed!\n%s could not be decrypted!\n", file);
					log_printf(0, "\n******* ERROR: could not decrypt %s, please be sure your provided a valid %s!\n", name, file);
					memcpy(buf, kv->data, kv->size);
				} else
					log_printf(1, "Success!\n");
			}
		} else {
		hashOk: __attribute__((hot));
		}
	} else if (!checkZeros(kv->data + 88, 8))
		log_printf(0, "\n******* ERROR: please be sure your provided a DEcrypted %s!\n", file);
	else {
	zerosOk: __attribute__((hot));
	}
	memcpy(kv->data, buf, kv->size);
	if (__builtin_expect(!alt, 0)) {
		kvSet(kv->data);
		kvEncrypt(kv->data, kv->size);
	} else
		kvEncryptAlt(kv->data, kv->size);
	free(buf);
}

void extendedPrepare(struct fileent *ext)
{
	uint8_t *buf;

	if (ext->size != 0x4000) {
		if (!ext->size)
			log_printf(1, "******* WARNING: extended.bin was not provided or was invalid! Making up an clean/empty extended.bin!\n");
		else
			log_printf(1, "******* WARNING: extended.bin is not the correct size! Making up an clean/empty extended.bin!\n");
		if (ext->data)
			free(ext->data);
		ext->size = 0x4000;
		ext->data = calloc(0x4000, 1);
	}
	buf = malloc(0x4000);
	memcpy(buf, ext->data, 0x4000);
	if (!checkZeros(buf, 16) && !kvHashOk(buf, ext->size)) {
		log_printf(1, "extended.bin appears to be encrypted, attempting to decrypt...");
		memcpy(buf, ext->data, ext->size);
		if (verifyExtended(buf, 0x4000))
			log_printf(1, "Success!\n");
		else {
			log_printf(1, "Failed!\nextended.bin could not be decrypted, filling clean/empty data.\n");
			memset(buf, 0, ext->size);
		}
	}
	memcpy(ext->data, buf, ext->size);
	free(buf);
	kvEncrypt(ext->data, ext->size);
}

void secdataPrepare(struct fileent *sd, uint8_t *date)
{
	uint8_t key[16];

	if (sd->size != 0x400) {
		if (!sd->size)
			log_printf(1, "******* WARNING: secdata.bin was not provided or was invalid! Making up an clean/empty secdata.bin!\n");
		else
			log_printf(1, "******* WARNING: secdata.bin is not the correct size! Making up an clean/empty secdata.bin!\n");
		free(sd->data);
		sd->size = 0x400;
		sd->data = calloc(0x400, 1);
	}
	memcpy(sd->data + 16, secdataKey, 8);
	memcpyrev(sd->data + 32, date, 8);
	sd->data[24] = 1;
	sd->data[25] = xb.cfLdv;
	XeCryptHmacSha(xb.cpuKey, 16, sd->data + 16, sd->size - 16, NULL, 0, NULL, 0, sd->data, 16);
	XeCryptHmacSha(xb.cpuKey, 16, sd->data, 16, NULL, 0, NULL, 0, key, 16);
	XeCryptRc4(key, 16, sd->data + 16, sd->size - 16);
}

int shaCheck(uint8_t *buf, uint32_t size, uint32_t hashOff, uint32_t hashLen, uint32_t dataOff, uint8_t *hashOut)
{
	uint8_t hash[20];

	XeCryptSha(buf + dataOff, size - dataOff, NULL, 0, NULL, 0, hash, 20);
	if (memcmp(buf + hashOff, hash, hashLen) == 0) {
		if (hashOut)
			memcpy(hashOut, hash, 20);
		return 1;
	}
	return 0;
}

void crlEncrypt(uint8_t *crl, uint32_t size, uint8_t *date)
{
	uint8_t *buf = malloc(size);
	uint8_t key[16];
	uint8_t iv[16];
	XECRYPT_AES_STATE aes;
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

void daeEncryptOne(uint8_t *dae, uint32_t size, uint8_t *date)
{
	uint8_t *buf = malloc(size);
	uint8_t hash[16];
	uint8_t iv[16];
	XECRYPT_AES_STATE aes;

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

static const char msg_daeBad[] __attribute__((aligned(4))) = "\n******* WARNING: dae data appears to be crypted with a different key or damaged! Skipping encryption.\n";
static const char msg_daeEncrypted[] __attribute__((aligned(4))) = "dae appears encrypted, attempting to decrypt with CPU key...";
static const char msg_daeHeader[] __attribute__((aligned(4))) = "\n******* ERROR: dae segment does not have the expected header!\n";
static const char msg_daeRetry[] __attribute__((aligned(4))) = "failed! Attempting to decrypt with alternate key...\n";
static const char msg_daeHash[] __attribute__((aligned(4))) = "failed!\n******* ERROR: dae hash incorrect, could not verify decrypted dae!\n";

/* The `!n` tests are threaded apart into one decrypt sequence per n, which
   leaves the first-key success shared by both; its own encrypt copy keeps
   it in one LRA EBB (no reload of off before the encrypt), and crossjumping
   then merges that copy into the main one.  The asm pins put off's zero in
   ebx across malloc/memcpy and off in edx in the loop, as the original. */
void daeEncrypt(uint8_t *buf, uint32_t size, uint8_t *date)
{
	uint8_t *orig = malloc(size);
	uint8_t *dae;
	uint32_t off = 0;
	uint32_t len;
	int n = 0;
	__asm__("" : "+b"(off));

	memcpy(orig, buf, size);
	if (__builtin_expect(size, 1)) do {
		dae = buf + off;
		__asm__("" :: "d"(off));
		if (__builtin_expect(buf[off] != 'D', 0) || __builtin_expect(buf[off + 1] != 'A', 1) || __builtin_expect(buf[off + 2] != 'E', 1) || __builtin_expect(buf[off + 3] != 'P', 1)) {
			log_printf(0, msg_daeHeader);
			break;
		}
		len = (uint16_t)((buf[off + 4] << 8) + buf[off + 5]);
		if (!shaCheck(dae, len, 12, 20, 336, NULL)) {
			if (!n)
				log_printf(1, msg_daeEncrypted);
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
				log_printf(1, msg_daeRetry);
			memcpy(dae, orig + off, len);
			daeDecrypt(dae, len, 0);
			if (shaCheck(dae, len, 12, 20, 336, NULL)) {
				if (!n)
					log_printf(1, "success!\n");
			} else {
				if (!n)
					log_printf(0, msg_daeHash);
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
		log_printf(0, msg_daeBad);
	}
	free(orig);
}

static const char msg_fcrtSize[] __attribute__((aligned(4))) = "****** ERROR: FCRT encrypt invalid size!\n";
static const char msg_fcrtOffset[] __attribute__((aligned(4))) = "**** ERROR: FCRT encrypt invalid offset!\n";
static const char msg_fcrtBad[] __attribute__((aligned(4))) = "****** WARNING: FCRT data appears to be crypted or damaged!! Skipping encryption.\n";

void fcrtEncrypt(uint8_t *fcrt, uint32_t size)
{
	uint8_t iv[16];
	uint8_t hash[20];
	uint32_t off;
	XECRYPT_AES_STATE aes;

	memcpy(iv, fcrt + 256, 16);
	if (size != 0x4000) {
		log_printf(0, msg_fcrtSize);
		return;
	}
	off = getBeU32(fcrt + 284);
	if (__builtin_expect(off < 0x4000, 1)) {
		XeCryptSha(fcrt + off, 0x4000 - off, NULL, 0, NULL, 0, hash, 20);
		if (memcmp(fcrt + 300, hash, 20) && verifyFcrt(fcrt, 0x4000) != 1) {
			log_printf(0, msg_fcrtBad);
			return;
		}
		XeCryptAesKey(&aes, xb.cpuKey);
		XeCryptAesCbc(&aes, fcrt + off, 0x4000 - off, fcrt + off, iv, 1);
	} else
		log_printf(1, msg_fcrtOffset);
}

void shaHeader(uint8_t *buf)
{
	XeCryptSha(buf + 20, 0x1ec, NULL, 0, NULL, 0, buf, 20);
}

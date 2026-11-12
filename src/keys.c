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

uint8_t pairing[3] = { 0 };
uint8_t zeroKey[16] = { 0 };
uint8_t cbaNonce[16] = {
	0x37, 0x10, 0xa2, 0xf2, 0x2e, 0xd5, 0xf0, 0xa8,
	0xe4, 0x9c, 0xb4, 0xc7, 0xa1, 0x39, 0x5d, 0xaa
};
uint8_t cbbNonce[16] = {
	0xfb, 0xe2, 0x70, 0x9a, 0xe7, 0xa1, 0x3f, 0x42,
	0xcf, 0xec, 0x45, 0x92, 0x8e, 0x3f, 0x0e, 0x37
};
uint8_t cdNonce[16] = {
	0xb3, 0x38, 0x64, 0x1c, 0xeb, 0xd0, 0x1e, 0x10,
	0x2c, 0xdd, 0xe0, 0xf3, 0x19, 0xa1, 0x9f, 0x84
};
uint8_t ceNonce[16] = {
	0x56, 0xa9, 0x81, 0xcd, 0x8c, 0xbc, 0x07, 0x29,
	0xdd, 0x0b, 0x7b, 0xbc, 0x76, 0xe5, 0x79, 0x98
};
uint8_t cfNonce[16] = {
	0xce, 0xe5, 0x04, 0xee, 0x9f, 0x61, 0x2b, 0x9b,
	0xa5, 0x20, 0xf8, 0xeb, 0x0b, 0x64, 0x68, 0x2a
};
uint8_t cgNonce[16] = {
	0xb9, 0xa2, 0x1e, 0x3b, 0xfc, 0x2e, 0xab, 0xb4,
	0x19, 0x81, 0x2d, 0x8a, 0x85, 0xaa, 0xa8, 0xce
};
uint8_t kvSalt[8] = { 0x36, 0xca, 0xb0, 0x87, 0x8b, 0x83, 0xb7, 0xf6 };
uint8_t kvAltSalt[8] = { 0x36, 0xca, 0xb0, 0x87, 0x8b, 0x83, 0xb7, 0xf6 };
uint8_t smcKey[4] = { 0x8e, 0x03, 0x75, 0xcc };
uint8_t crlKey[32] = {
	0xc7, 0x03, 0xb9, 0x32, 0xd4, 0x07, 0x7d, 0x41, 0x60, 0x52, 0xa8, 0x13, 0x5e, 0xde, 0x68, 0x18,
	0xd9, 0x75, 0x98, 0xa6, 0xf8, 0x5d, 0x9b, 0x86, 0x7b, 0xc4, 0x34, 0x99, 0xe3, 0x3d, 0xa4, 0xaa
};
uint8_t daeKey[32] = {
	0xa1, 0xb2, 0x69, 0x50, 0x58, 0xf4, 0xed, 0x05, 0xe5, 0x80, 0xc7, 0xee, 0x18, 0x9a, 0x27, 0xb5,
	0xac, 0x5e, 0xbc, 0x70, 0x89, 0x29, 0x65, 0x90, 0xf4, 0x24, 0xed, 0x2a, 0xd3, 0x62, 0x83, 0x14
};
uint8_t secdataKey[8] = { 0x5a, 0xa4, 0xd1, 0xd2, 0x7d, 0xe4, 0x45, 0x3e };

void keysInit(int random)
{
	aes_init();
	if (random)
	{
		log_printf(1, "initializing random nonces\n");
		XeCryptRandom(cbaNonce, 16);
		XeCryptRandom(cbbNonce, 16);
		XeCryptRandom(cdNonce, 16);
		XeCryptRandom(ceNonce, 16);
		XeCryptRandom(cfNonce, 16);
		XeCryptRandom(cgNonce, 16);
		XeCryptRandom(kvSalt, 8);
		XeCryptRandom(kvAltSalt, 8);
		XeCryptRandom(smcKey, 4);
		XeCryptRandom(crlKey, 32);
		XeCryptRandom(daeKey, 32);
		XeCryptRandom(secdataKey, 8);
	}
	else if (pairing[0] == 0 && pairing[1] == 0 && pairing[2] == 0)
	{
		log_printf(1, "initializing static pairing value\n");
		pairing[0] = 0x23;
		pairing[1] = 0x45;
		pairing[2] = 0xf1;
	}
	if (pairing[0] == 0 && pairing[1] == 0 && pairing[2] == 0)
	{
		XeCryptRandom(pairing, 3);
	}
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
	for (i = 0; i < 16; i++)
	{
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

void setCbaNonce(uint8_t *nonce)
{
	memcpy(cbaNonce, nonce, 16);
}

void setCbbNonce(uint8_t *nonce)
{
	memcpy(cbbNonce, nonce, 16);
}

void setCdNonce(uint8_t *nonce)
{
	memcpy(cdNonce, nonce, 16);
}

void setCeNonce(uint8_t *nonce)
{
	memcpy(ceNonce, nonce, 16);
}

void setCfNonce(uint8_t *nonce)
{
	memcpy(cfNonce, nonce, 16);
}

void setCgNonce(uint8_t *nonce)
{
	memcpy(cgNonce, nonce, 16);
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
	if (pair & 0xffffff)
	{
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
	{
		tmp[i] = key[i] & mask[i];
	}
	weight = XeCryptHammingWeight(tmp, 16);
	XeCryptUidEccEncode(tmp);
	ecd = memcmp(key, tmp, 16) == 0;
	wok = weight == 53;
	log_printf(level, " (weight:0x%x %s; ecd: %s)", weight,
		wok ? "valid" : "error", ecd ? "valid" : "error");
	return wok && ecd;
}

uint32_t setCpuKeyStr(char *str)
{
	int len = strlen(str);
	int i;
	uint32_t ret;

	if (len == 32)
	{
		ret = validateString(str);
		if (ret)
		{
			for (i = 0; i < 16; i++, str += 2)
			{
				xb.cpuKey[i] = myatox8(str);
			}
			log_printf(1, "CPU Key set to: 0x");
			for (i = 0; i < 16; i++)
			{
				log_printf(1, "%02X", xb.cpuKey[i]);
			}
			ret = 1;
			if (!checkZeros(xb.cpuKey, 16))
			{
				if (checkCpuKey(1, xb.cpuKey))
				{
					log_printf(0, "\n");
				}
				else
				{
					log_printf(0, "\n***** WARNING: CPU key check failed, CPU key may not be valid!\n\n");
				}
			}
		}
		else
		{
			log_printf(0, "\n******* ERROR: invalid or unexpected characters in CPU key!\n");
		}
	}
	else
	{
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
	{
		log_printf(level, "\n***** WARNING: CPU key check failed, CPU key may not be valid!\n\n");
	}
	log_printf(level, "\n");
	return 1;
}

void setFuseLdv(uint8_t *fuse, uint8_t ldv)
{
	uint32_t i;
	uint64_t cb, cf;

	if (ldv > 16)
	{
		if (ldv > 31)
		{
			cf = ~0ULL;
		}
		else
		{
			for (cf = 0, i = 0; i < ldv - 16; i++)
			{
				cf = (cf >> 4) | 0xf000000000000000ULL;
			}
		}
		cb = ~0ULL;
	}
	else
	{
		cf = 0;
		if (ldv == 16)
		{
			cb = ~0ULL;
		}
		else
		{
			for (cb = 0, i = 0; i < ldv; i++)
			{
				cb = (cb >> 4) | 0xf000000000000000ULL;
			}
		}
	}
	setBeU64(cb, fuse + 56);
	setBeU64(cf, fuse + 64);
	log_printf(1, "Fuse CF LDV set to : 0x");
	for (i = 0; i < 16; i++)
	{
		log_printf(1, "%02X", fuse[56 + i]);
	}
	log_printf(1, "\n");
}

/* gcc emits a function's literals in expand-time block order, so the
   original's .rdata order shows its shape: setFuseCpuKey and daeEncrypt
   log a bad argument or header in an else after the main path, and
   fcrtEncrypt logs each failure in order down an else chain */
void setFuseCpuKey(uint8_t *fuse)
{
	int i;

	if (fuse != NULL)
	{
		memcpy(fuse + 24, xb.cpuKey, 8);
		memcpy(fuse + 32, xb.cpuKey, 16);
		memcpy(fuse + 48, xb.cpuKey + 8, 8);
		memcpy(xb.cpuKey, fuse + 32, 16);
		setFuseLdv(fuse, xb.cfLdv);
		log_printf(1, "Fuse CPU Key set to: 0x");
		for (i = 32; i < 48; i++)
		{
			log_printf(1, "%02X", fuse[i]);
		}
		log_printf(1, "\n");
	}
	else
	{
		log_printf(0, "\nERROR: YOU SHOULD NOT BE SEEING THIS ERROR!\n");
	}
}

uint32_t calcXexKey(void)
{
	uint8_t key[16] = { 0x95, 0x27, 0x72, 0xbf, 0x47, 0xc0, 0xf6, 0x98,
		0x5c, 0x7d, 0xf2, 0x50, 0x65, 0x4d, 0x55, 0xcd };
	uint8_t junk[16];
	uint8_t hash[16];

	memcpy(junk, "thisisjustajunky", 16);
	XeCryptHmacSha(junk, 16, xb.key1bl, 16, NULL, 0, NULL, 0, hash, 16);
	memcpy(xb.xexKey, key, 16);
	XeCryptRc4(hash, 16, xb.xexKey, 16);
	return sumBytes(xb.xexKey, 16);
}

int check1blKey(void)
{
	uint32_t sum1 = sumBytes(xb.key1bl, 16);
	uint32_t sum2 = calcXexKey();

	if (sum1 == KEY1BL_SUM && sum2 == XEXKEY_SUM)
	{
		log_printf(1, "1BL Key set to  : 0x");
		showKey(1, xb.key1bl);
		log_printf(1, " sum: 0x%x (expects: 0x983)\n", sum1);
		log_printf(1, "xex Key set to  : 0x");
		showKey(1, xb.xexKey);
		log_printf(1, " sum: 0x%x (expects: 0x800)\n", sum2);
		return 1;
	}
	return 0;
}

int set1blKey(uint8_t *key)
{
	memcpy(xb.key1bl, key, 16);
	if (check1blKey())
	{
		return 1;
	}
	log_printf(0, "\n******* ERROR: 1BL key 0x");
	showKey(0, xb.key1bl);
	log_printf(0, " does not appear to be correct!\n");
	return 0;
}

uint32_t checkKeys(char *str)
{
	int len = strlen(str);
	char *p;
	int i;

	if (len == 32)
	{
		if (validateString(str))
		{
			for (i = 0, p = str; i < 16; i++, p += 2)
			{
				xb.key1bl[i] = myatox8(p);
			}
			if (check1blKey())
			{
				return 1;
			}
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

void smcChecksum(uint32_t *buf, uint8_t *out, uint32_t count)
{
	long long sum1 = 0, sum2 = 0;
	uint32_t i, v;

	for (i = 0; i < count; i++)
	{
		v = SWAP32_KEYS(buf[i]);
		sum1 += v;
		sum2 -= v;
		sum1 = (sum1 << 29) | (uint32_t)((uint32_t)(sum1 >> 32) >> 3);
		sum2 = (sum2 << 31) | (uint32_t)((uint32_t)(sum2 >> 32) >> 1);
	}
	setBeU64(sum1, out);
	setBeU64(sum2, out + 8);
}

void smcEncrypt(uint8_t *buf, uint32_t len)
{
	uint8_t s[4] = { 'B', 'u', 'N', 'y' };
	uint32_t i, j = 0;
	int t;

	for (i = 0; i < len; i++)
	{
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
	if (!checkZeros(buf + size - 4, 4))
	{
		log_printf(1, "SMC binary appears to be encrypted, attempting to decrypt...");
		if (unscramble(buf, size))
		{
			memcpy(smc, buf, size);
			log_printf(1, "success!");
		}
		else
		{
			log_printf(1, "failed!");
			log_printf(0, "\n******* ERROR: please make sure your provided a valid/decryptable SMC binary!\n\n");
			if (!(xb.optFlags & OPT_SMCNOCHECK))
			{
				return 1;
			}
			memcpy(buf, smc, size);
		}
	}
	if (checkZeros(buf + size - 4, 4))
	{
		bad = smcCheck(smc, size, xb.type);
		if (xb.type == BUILD_RETAIL)
		{
			if (bad)
			{
				log_printf(0, "\n******* ERROR: hacked or unknown SMC binary found? you should use a clean SMC binary for a retail image!\n\n");
				if (!(xb.optFlags & OPT_SMCNOCHECK))
				{
					return 1;
				}
			}
			else
			{
				log_printf(1, "known/clean SMC binary found! type 0x%x\n", 1);
			}
			xb.optFlags &= ~OPT_SMC_PATCHES;
		}
		else if (xb.type > BUILD_DEVGL16)
		{
			if (bad)
			{
				log_printf(0, "\n******* WARNING: hacked or unknown SMC binary found? Just a warning, there are a lot of different SMC binaries for devkits!\n\n");
			}
			else
			{
				log_printf(1, "known/clean SMC binary found!\n");
			}
			xb.optFlags &= ~OPT_SMC_PATCHES;
		}
		else if (bad)
		{
			if (xb.type == BUILD_GLITCH)
			{
				log_printf(1, "glitch hack found in SMC binary!\n");
				xb.optFlags &= ~OPT_PATCHSMC;
			}
			else if (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16)
			{
				log_printf(1, "\n******* WARNING: hacked or unknown SMC binary found!\n");
			}
			else
			{
				log_printf(1, "jtag hack found in SMC binary!\n");
			}
		}
		else
		{
			if (xb.type == BUILD_GLITCH)
			{
				if (!(xb.optFlags & OPT_PATCHSMC))
				{
					log_printf(0, "\n******* ERROR: clean SMC binary found? you should use a hacked SMC binary for glitch images.\n\n");
				}
			}
			else if (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16)
			{
				log_printf(1, "known/clean SMC binary found!\n");
			}
			else
			{
				log_printf(0, "\n******* ERROR: clean SMC binary found? you should use a hacked SMC binary for JTAG images.\n\n");
				if (!(xb.optFlags & OPT_SMCNOCHECK))
				{
					return 1;
				}
			}
		}
		patch = xb.optFlags & OPT_SMC_PATCHES;
		if (patch)
		{
			smcPatch(smc, size, patch);
		}
		memcpy(smc, smcKey, 4);
		smcEncrypt(smc, size);
	}
	memcpy(buf, smc, size);
	smcChecksum((uint32_t *)buf, hash, size / 4);
	free(buf);
	return 0;
}

void cbaEncrypt(uint8_t *salt, uint8_t *cb, uint8_t *key, uint32_t size, int zero)
{
	memcpy(cb + BL_NONCE, cbaNonce, 16);
	XeCryptHmacSha(xb.key1bl, 16, cb + BL_NONCE, 16, NULL, 0, NULL, 0, key, 16);
	if (!zero)
	{
		log_printf(1, "CBENC pairing set to: %02x %02x %02x\n", pairing[0], pairing[1], pairing[2]);
		memcpy(cb + CB_PAIRING, pairing, 3);
		cb[CB_LDV] = xb.cbLdv;
		XeCryptHmacSha(xb.cpuKey, 16, key, 16, cb + 32, 16, salt, 16, cb + 48, 16);
	}
	XeCryptRc4(key, 16, cb + BL_BODY, size - BL_BODY);
}

void cbaEncryptZero(uint8_t *cb, uint8_t *key, uint32_t size)
{
	memset(pairing, 0, 3);
	memcpy(cb + BL_NONCE, cbaNonce, 16);
	memset(cb + 32, 0, 32);
	XeCryptHmacSha(xb.key1bl, 16, cb + BL_NONCE, 16, NULL, 0, NULL, 0, key, 16);
	XeCryptRc4(key, 16, cb + BL_BODY, size - BL_BODY);
}

void cbaEncrypt2(uint8_t *salt, uint8_t *cb, uint8_t *key, uint32_t size, int zero)
{
	memcpy(cb + BL_NONCE, cbaNonce, 16);
	if (zero)
	{
		memset(cb + 32, 0, 32);
	}
	XeCryptHmacSha(xb.key1bl, 16, cb + BL_NONCE, 16, NULL, 0, NULL, 0, key, 16);
	if (!zero)
	{
		memcpy(cb + CB_PAIRING, pairing, 3);
		cb[CB_LDV] = xb.cbLdv;
		XeCryptHmacSha(xb.cpuKey, 16, key, 16, cb + 32, 16, salt, 16, cb + 48, 16);
	}
	XeCryptRc4(key, 16, cb + BL_BODY, size - BL_BODY);
}

void cbbEncrypt(uint8_t *salt, uint8_t *cbb, uint8_t *cbaKey, uint8_t *cba, uint8_t *key, uint32_t size, int zero)
{
	uint16_t flags = getBeU16(cba + 6);
	uint8_t *ck;
	uint8_t hdr[16];

	memcpy(cbb + BL_NONCE, cbbNonce, 16);
	ck = !(flags & 1) ? xb.cpuKey : zeroKey;
	if (flags & BL_FLAG_CB_B)
	{
		log_printf(1, "\t**dual CB flag detected!**\n");
	}
	if (flags & 0x1000)
	{
		log_printf(1, "\t**15572+ CBB crypto method detected!**\n");
		memcpy(hdr, cba, 16);
		hdr[6] = 0;
		hdr[7] = 0;
		XeCryptHmacSha(cbaKey, 16, cbb + BL_NONCE, 16, ck, 16, hdr, 16, key, 16);
	}
	else
	{
		XeCryptHmacSha(cbaKey, 16, cbb + BL_NONCE, 16, ck, 16, NULL, 0, key, 16);
	}
	if (zero)
	{
		memset(pairing, 0, 3);
		memset(cbb + 32, 0, 32);
	}
	else
	{
		memcpy(cbb + CB_PAIRING, pairing, 3);
		cbb[CB_LDV] = xb.cbLdv;
		if (!(flags & 1))
		{
			XeCryptHmacSha(xb.cpuKey, 16, key, 16, cbb + 32, 16, salt, 16, cbb + 48, 16);
		}
		else
		{
			log_printf(1, "\t** CBB crypto method set to work with mfg CBA!**\n");
		}
	}
	XeCryptRc4(key, 16, cbb + BL_BODY, size - BL_BODY);
}

void cdEncryptZero(uint8_t *cd, uint8_t *key, uint32_t size)
{
	uint8_t zero[16];

	memset(zero, 0, 16);
	memcpy(cd + BL_NONCE, cbbNonce, 16);
	XeCryptHmacSha(zero, 16, cd + BL_NONCE, 16, NULL, 0, NULL, 0, key, 16);
	XeCryptRc4(key, 16, cd + BL_BODY, size - BL_BODY);
}

void cdEncrypt(uint8_t *cd, uint8_t *prevKey, uint8_t *key, uint32_t size)
{
	memcpy(cd + BL_NONCE, cdNonce, 16);
	XeCryptHmacSha(prevKey, 16, cd + BL_NONCE, 16, NULL, 0, NULL, 0, key, 16);
	XeCryptRc4(key, 16, cd + BL_BODY, size - BL_BODY);
}

void cdEncryptCpu(uint8_t *cd, uint8_t *prevKey, uint8_t *key, uint32_t size)
{
	memcpy(cd + BL_NONCE, cdNonce, 16);
	XeCryptHmacSha(prevKey, 16, cd + BL_NONCE, 16, NULL, 0, NULL, 0, key, 16);
	XeCryptHmacSha(xb.cpuKey, 16, key, 16, NULL, 0, NULL, 0, key, 16);
	XeCryptRc4(key, 16, cd + BL_BODY, size - BL_BODY);
}

void ceEncrypt(uint8_t *ce, uint8_t *prevKey, uint8_t *key, uint32_t size)
{
	memcpy(ce + BL_NONCE, ceNonce, 16);
	XeCryptHmacSha(prevKey, 16, ce + BL_NONCE, 16, NULL, 0, NULL, 0, key, 16);
	XeCryptRc4(key, 16, ce + BL_BODY, size - BL_BODY);
}

/* The slot index i and the count n are separate (the original computes
   the last index as trips + 2 but n as (trips + 1) + 1); n is 16-bit, so
   its add isn't CSE'd with the index's. */
extern inline short cfPatchSlots(struct fileent *cf, uint32_t extra, uint16_t block, uint32_t max)
{
	uint8_t *buf = cf->data;
	uint32_t end = cf->size + extra;
	uint32_t over;
	short n = 0;
	uint32_t i;
	uint16_t *tbl = (uint16_t *)(buf + BL_CF_BODY);

	if (end > max)
	{
		over = end - max;
		cf->fsOffset = max - cf->size;
		cf->fsSize = over;
		for (i = 1; over > NAND_BLOCK; i++, over -= NAND_BLOCK)
		{
			tbl[i] = SWAP16_KEYS(block + i - 1);
			n++;
		}
		if (over)
		{
			tbl[i] = SWAP16_KEYS(block + i - 1);
			n++;
		}
	}
	tbl[0] = SWAP16_KEYS(n);
	return n;
}

uint16_t cfEncrypt(struct fileent *cf, uint32_t extra, uint16_t block, int keep, uint32_t max)
{
	uint8_t key[16];
	uint8_t salt[16];
	short n;
	uint8_t *buf;

	memcpy(salt, cfNonce, 16);
	if (!keep)
	{
		buf = cf->data;
		memset(buf + BL_CF_NONCE, 0, 528);
		if (xb.type == BUILD_JTAG)
		{
			cf->data[539] = 1;
		}
		else
		{
			cf->data[539] = 0;
		}
		memcpy(cf->data + CF_PAIRING, pairing, 3);
		cf->data[CF_LDV] = xb.cfLdv;
	}
	n = cfPatchSlots(cf, extra, block, max);
	XeCryptHmacSha(xb.key1bl, 16, salt, 16, NULL, 0, NULL, 0, key, 16);
	if (!keep)
	{
		memcpy(cf->data + BL_CF_NONCE, key, 16);
		XeCryptHmacSha(xb.cpuKey, 16, cf->data, 0x220, NULL, 0, NULL, 0, cf->data + 544, 16);
	}
	buf = cf->data;
	memcpy(cf->key, buf + CF_CG_KEY, 16);
	memcpy(buf + BL_CF_NONCE, salt, 16);
	XeCryptRc4(key, 16, cf->data + BL_CF_BODY, cf->size - BL_CF_BODY);
	return n;
}

void cgEncrypt(uint8_t *cg, uint8_t *prevKey, uint8_t *key, uint32_t size)
{
	memcpy(cg + BL_NONCE, cgNonce, 16);
	XeCryptHmacSha(prevKey, 16, cg + BL_NONCE, 16, NULL, 0, NULL, 0, key, 16);
	XeCryptRc4(key, 16, cg + BL_BODY, size - BL_BODY);
}

void kvEncrypt(uint8_t *kv, uint32_t size)
{
	uint8_t ver[2] = { 0x07, 0x12 };	/* FLASH_KV_VERSION */
	uint8_t key[16];

	memcpy(kv + KV_SALT, kvSalt, 8);
	XeCryptHmacSha(xb.cpuKey, 16, kv + KV_SALT, size - KV_SALT, ver, 2, NULL, 0, kv, 16);
	XeCryptHmacSha(xb.cpuKey, 16, kv, 16, NULL, 0, NULL, 0, key, 16);
	XeCryptRc4(key, 16, kv + KV_SALT, size - KV_SALT);
}

void kvEncryptAlt(uint8_t *kv, uint32_t size)
{
	uint8_t ver[2] = { 0x07, 0x12 };	/* FLASH_KV_VERSION */
	uint8_t key[16];

	memcpy(kv + KV_SALT, kvAltSalt, 8);
	XeCryptHmacSha(xb.cpuKey, 16, kv + KV_SALT, size - KV_SALT, ver, 2, NULL, 0, kv, 16);
	XeCryptHmacSha(xb.cpuKey, 16, kv, 16, NULL, 0, NULL, 0, key, 16);
	XeCryptRc4(key, 16, kv + KV_SALT, size - KV_SALT);
}

static int kvHashOk(uint8_t *kv, uint32_t size)
{
	uint8_t ver[2] = { 0x07, 0x12 };	/* FLASH_KV_VERSION */
	uint8_t hash[16];

	XeCryptHmacSha(xb.cpuKey, 16, kv + KV_SALT, size - KV_SALT, ver, 2, NULL, 0, hash, 16);
	return memcmp(kv, hash, 16) == 0;
}

void kvPrepare(struct fileent *kv, int alt)
{
	const char *file = "kv.bin", *name = "kv";
	uint8_t *buf, *nbuf;

	if (alt)
	{
		file = "kv_alt.bin";
		name = "alt kv";
	}
	if (kv->size == KV_SIZE - 0x10)	/* without the HMAC */
	{
		nbuf = malloc(KV_SIZE);
		memset(nbuf, 0, 16);
		memcpy(nbuf + 16, kv->data, KV_SIZE - 0x10);
		free(kv->data);
		kv->data = nbuf;
		kv->size = KV_SIZE;
	}
	if (kv->size != KV_SIZE)
	{
		log_printf(0, "\n******* ERROR: %s is not the correct size! Skipping verification and encryption!\n", file);
		return;
	}
	buf = malloc(KV_SIZE);
	memcpy(buf, kv->data, KV_SIZE);
	if (!checkZeros(buf, 16))
	{
		if (!kvHashOk(buf, kv->size))
		{
			if (checkZeros(buf + 56, 88))
			{
				log_printf(1, "%s appears to be decrypted already, but the hash does not match the CPU key...", file);
				log_printf(0, "\n******* WARNING: could not verify pre-decrypted keyvault, please be sure your provided a valid %s!\n", file);
			}
			else
			{
				log_printf(1, "%s appears to be encrypted, attempting to decrypt...", file);
				memcpy(buf, kv->data, kv->size);
				if (!verifyExtended(buf, KV_SIZE))
				{
					log_printf(1, "Failed!\n%s could not be decrypted!\n", file);
					log_printf(0, "\n******* ERROR: could not decrypt %s, please be sure your provided a valid %s!\n", name, file);
					memcpy(buf, kv->data, kv->size);
				}
				else
				{
					log_printf(1, "Success!\n");
				}
			}
		}
	}
	else if (!checkZeros(kv->data + 88, 8))
	{
		log_printf(0, "\n******* ERROR: please be sure your provided a DEcrypted %s!\n", file);
	}
	memcpy(kv->data, buf, kv->size);
	if (!alt)
	{
		kvSet(kv->data);
	}
	if (alt)
	{
		kvEncryptAlt(kv->data, kv->size);
	}
	else
	{
		kvEncrypt(kv->data, kv->size);
	}
	free(buf);
}

void extendedPrepare(struct fileent *ext)
{
	uint8_t *buf;

	if (ext->size != EXTENDED_SIZE)
	{
		if (!ext->size)
		{
			log_printf(1, "******* WARNING: extended.bin was not provided or was invalid! Making up an clean/empty extended.bin!\n");
		}
		else
		{
			log_printf(1, "******* WARNING: extended.bin is not the correct size! Making up an clean/empty extended.bin!\n");
		}
		if (ext->data)
		{
			free(ext->data);
		}
		ext->size = EXTENDED_SIZE;
		ext->data = calloc(EXTENDED_SIZE, 1);
	}
	buf = malloc(EXTENDED_SIZE);
	memcpy(buf, ext->data, EXTENDED_SIZE);
	if (!checkZeros(buf, 16) && !kvHashOk(buf, ext->size))
	{
		log_printf(1, "extended.bin appears to be encrypted, attempting to decrypt...");
		memcpy(buf, ext->data, ext->size);
		if (verifyExtended(buf, EXTENDED_SIZE))
		{
			log_printf(1, "Success!\n");
		}
		else
		{
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

	if (sd->size != SECDATA_SIZE)
	{
		if (!sd->size)
		{
			log_printf(1, "******* WARNING: secdata.bin was not provided or was invalid! Making up an clean/empty secdata.bin!\n");
		}
		else
		{
			log_printf(1, "******* WARNING: secdata.bin is not the correct size! Making up an clean/empty secdata.bin!\n");
		}
		free(sd->data);
		sd->size = SECDATA_SIZE;
		sd->data = calloc(SECDATA_SIZE, 1);
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
	if (memcmp(buf + hashOff, hash, hashLen) == 0)
	{
		if (hashOut)
		{
			memcpy(hashOut, hash, 20);
		}
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
	if (!shaCheck(crl, size, 12, 20, 336, NULL))
	{
		log_printf(1, "crl appears crypted, attempting to decrypt with CPU key...");
		if (verifyCrl(buf, size, 1))
		{
			log_printf(1, "success!\n");
			memcpy(crl, buf, size);
		}
		else
		{
			log_printf(1, "failed! Trying alternate key...");
			memcpy(buf, crl, size);
			if (verifyCrl(buf, size, 0))
			{
				log_printf(1, "success!\n");
				memcpy(crl, buf, size);
			}
			else
			{
				log_printf(1, "failed!\n");
			}
		}
	}
	if (shaCheck(crl, size, 12, 20, 336, NULL))
	{
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
	}
	else
	{
		log_printf(0, "\n******* ERROR: crl data appears to be crypted with the wrong key or damaged!\n");
	}
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

void daeEncrypt(uint8_t *buf, uint32_t size, uint8_t *date)
{
	uint8_t *orig = malloc(size);
	uint8_t *dae;
	uint32_t off = 0;
	uint32_t len;
	int n = 0;

	memcpy(orig, buf, size);
	for (;; off += len)
	{
		if (off >= size)
		{
			if (n != 2)
			{
				log_printf(0, "\n******* WARNING: dae data appears to be crypted with a different key or damaged! Skipping encryption.\n");
			}
			break;
		}
		dae = buf + off;
		if (buf[off] == 'D' && buf[off + 1] == 'A' && buf[off + 2] == 'E' && buf[off + 3] == 'P')
		{
			len = (uint16_t)((buf[off + 4] << 8) + buf[off + 5]);
			if (!shaCheck(dae, len, 12, 20, 336, NULL))
			{
				if (!n)
				{
					log_printf(1, "dae appears encrypted, attempting to decrypt with CPU key...");
				}
				memcpy(dae, orig + off, len);
				daeDecrypt(dae, len, 1);
				if (shaCheck(dae, len, 12, 20, 336, NULL))
				{
					log_printf(1, "success!\n");
					daeEncryptOne(dae, len, date);
					n++;
					continue;
				}
				if (!n)
				{
					log_printf(1, "failed! Attempting to decrypt with alternate key...\n");
				}
				memcpy(dae, orig + off, len);
				daeDecrypt(dae, len, 0);
				if (shaCheck(dae, len, 12, 20, 336, NULL))
				{
					if (!n)
					{
						log_printf(1, "success!\n");
					}
				}
				else
				{
					if (!n)
					{
						log_printf(0, "failed!\n******* ERROR: dae hash incorrect, could not verify decrypted dae!\n");
					}
					n = 0;
					off = size + 1;
					continue;
				}
			}
			daeEncryptOne(dae, len, date);
			n++;
		}
		else
		{
			log_printf(0, "\n******* ERROR: dae segment does not have the expected header!\n");
			off = size;
			len = 0;
		}
	}
	free(orig);
}

void fcrtEncrypt(uint8_t *fcrt, uint32_t size)
{
	uint8_t iv[16];
	uint8_t hash[20];
	uint32_t off;
	XECRYPT_AES_STATE aes;

	memcpy(iv, fcrt + 256, 16);
	if (size != FCRT_SIZE)
	{
		log_printf(0, "****** ERROR: FCRT encrypt invalid size!\n");
	}
	else
	{
		off = getBeU32(fcrt + 284);
		if (off >= FCRT_SIZE)
		{
			log_printf(1, "**** ERROR: FCRT encrypt invalid offset!\n");
		}
		else
		{
			XeCryptSha(fcrt + off, FCRT_SIZE - off, NULL, 0, NULL, 0, hash, 20);
			if (memcmp(fcrt + 300, hash, 20) == 0)
			{
				XeCryptAesKey(&aes, xb.cpuKey);
				XeCryptAesCbc(&aes, fcrt + off, FCRT_SIZE - off, fcrt + off, iv, 1);
			}
			else if (verifyFcrt(fcrt, FCRT_SIZE) == 1)
			{
				XeCryptAesKey(&aes, xb.cpuKey);
				XeCryptAesCbc(&aes, fcrt + off, FCRT_SIZE - off, fcrt + off, iv, 1);
			}
			else
			{
				log_printf(0, "****** WARNING: FCRT data appears to be crypted or damaged!! Skipping encryption.\n");
			}
		}
	}
}

void shaHeader(uint8_t *buf)
{
	XeCryptSha(buf + 20, 0x1ec, NULL, 0, NULL, 0, buf, 20);
}

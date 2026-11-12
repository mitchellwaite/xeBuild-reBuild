/* xboxrom: hashes, signs and verifies keyvault and bootloader signatures */
#include <string.h>

#include "crypto/xecrypt.h"
#include "xebuild.h"
#include "fileutil.h"
#include "xboxrom.h"

/* a CB's signature (XECRYPT_SIG) and where what it signs starts (with the
   header); an SC's or SD's.  An SE's (CE's) hash is of the header and the
   body after the nonce. */
#define CB_SIG 0x40
#define CB_SIGNED 0x140
#define BL_SIG 0x20
#define BL_SIGNED 0x120

uint8_t romSalts[3][12] = { "XBOX_ROM_4", "XBOX_ROM_3", "XBOX_ROM_B" };

int kvVerifySig(uint8_t *kv, const XECRYPT_RSAPUB_2048 *pubKey, const uint8_t *hmacKey)
{
	uint8_t hash[20];

	XeCryptHmacSha(hmacKey, 16, kv + KV_ODD_FEATURES, 0xf0 - KV_ODD_FEATURES,
		kv + KV_DVD_KEY, KV_SIGNATURE - KV_DVD_KEY, kv + (KV_SIGNATURE + 0x100),
		KV_SIZE - (KV_SIGNATURE + 0x100), hash, 20);
	return XeKeysPkcs1Verify(hash, kv + KV_SIGNATURE, &pubKey->Rsa);
}

int cbVerifySig(uint8_t *bl, XECRYPT_RSAPUB_2048 *pubKey)
{
	uint8_t hash[20];
	unsigned int len = (getBeU32(bl + BL_SIZE_OFFSET) + 15) & ~15;

	XeCryptRotSumSha(bl, 16, bl + CB_SIGNED, len - CB_SIGNED, hash, 20);
	return XeCryptBnQwBeSigVerify((XECRYPT_SIG *)(bl + CB_SIG), hash, romSalts[2], &pubKey->Rsa);
}

int blVerifySig(uint8_t *bl, unsigned int len, XECRYPT_RSAPUB_2048 *pubKey, const uint8_t *salt)
{
	uint8_t hash[20];

	XeCryptRotSumSha(bl, 16, bl + BL_SIGNED, len - BL_SIGNED, hash, 20);
	return XeCryptBnQwBeSigVerify((XECRYPT_SIG *)(bl + BL_SIG), hash, salt, &pubKey->Rsa);
}

uint32_t blSign(uint8_t *bl, unsigned int len, XECRYPT_RSAPUB_2048 *pubKey, const XECRYPT_RSAPRV_2048 *prvKey, const uint8_t *salt)
{
	struct
	{
		char salt[16];
		uint8_t hash[20];
		uint8_t sig[256];
	} s;

	memset(s.salt, 0, sizeof(s.salt));
	memcpy(s.salt, salt, 10);
	XeCryptRotSumSha(bl, 16, bl + BL_SIGNED, len - BL_SIGNED, s.hash, 20);
	if (!XeCryptBnQwBeSigCreate((XECRYPT_SIG *)s.sig, s.hash, salt, &prvKey->Rsa))
	{
		return 0;
	}
	if (!XeCryptBnQwNeRsaPrvCrypt((u64 *)s.sig, (u64 *)s.sig, &prvKey->Rsa))
	{
		return 0;
	}
	if (!XeCryptBnQwBeSigVerify((XECRYPT_SIG *)s.sig, s.hash, salt, &pubKey->Rsa))
	{
		return 0;
	}
	memcpy(bl + BL_SIG, s.sig, sizeof(s.sig));
	return 1;
}

uint32_t blCheckHash(uint8_t *bl, unsigned int len, const uint8_t *expect)
{
	uint8_t hash[20];

	XeCryptRotSumSha(bl, 16, bl + BL_BODY, len - BL_BODY, hash, 20);
	return memcmp(expect, hash, 20) == 0;
}

int blUpdateHash(uint8_t *bl, unsigned int len, uint8_t *stored)
{
	uint8_t hash[20];

	XeCryptRotSumSha(bl, 16, bl + BL_BODY, len - BL_BODY, hash, 20);
	if (memcmp(stored, hash, 20) == 0)
	{
		return 0;
	}
	memcpy(stored, hash, 20);
	return 1;
}

int blHashAndSign(uint8_t *bl, unsigned int len, uint8_t *prev, unsigned int prevLen, uint8_t *hashOut,
	XECRYPT_RSAPUB_2048 *pubKey, const XECRYPT_RSAPRV_2048 *prvKey)
{
	uint8_t hash[20];

	XeCryptRotSumSha(bl, 16, bl + BL_BODY, len - BL_BODY, hash, 20);
	memcpy(hashOut, hash, 20);
	return blSign(prev, prevLen, pubKey, prvKey,
		getBeU16(prev) != (BL_MAGIC_KIT | BL_MAGIC_CD) ? romSalts[1] : romSalts[0]);
}

/* xboxrom: hashes, signs and verifies keyvault and bootloader signatures */
#include <string.h>

#include "crypto/xecrypt.h"
#include "xebuild.h"
#include "fileutil.h"
#include "xboxrom.h"

char romSalts[3][12] = { "XBOX_ROM_4", "XBOX_ROM_3", "XBOX_ROM_B" };

int kvVerifySig(uint8_t *kv, const struct rsapub *pubKey, const uint8_t *hmacKey)
{
	uint8_t hash[20];

	XeCryptHmacSha(hmacKey, 16, kv + 0x1c, 0xd4, kv + 0x100, 0x1cf8, kv + 0x1ef8, 0x2108, hash, 20);
	/* TODO(prototype cast): xecrypt.h types the key as its XECRYPT_RSA header */
	return XeKeysPkcs1Verify(hash, kv + 0x1df8, (const XECRYPT_RSA *)pubKey);
}

int cbVerifySig(uint8_t *bl, const struct rsapub *pubKey)
{
	uint8_t hash[20];
	unsigned int len = (getBeU32(bl + 12) + 15) & ~15;

	XeCryptRotSumSha(bl, 16, bl + 0x140, len - 0x140, hash, 20);
	/* TODO(prototype cast): the bootloaders' signatures and keys are bytes
	   here; xecrypt.h types them (and its keys aren't const) */
	return XeCryptBnQwBeSigVerify((XECRYPT_SIG *)(bl + 0x40), hash, (uint8_t *)romSalts[2],
				      (XECRYPT_RSA *)pubKey);
}

int blVerifySig(uint8_t *bl, unsigned int len, const void *pubKey, const uint8_t *salt)
{
	uint8_t hash[20];

	XeCryptRotSumSha(bl, 16, bl + 0x120, len - 0x120, hash, 20);
	/* TODO(prototype cast): as in cbVerifySig */
	return XeCryptBnQwBeSigVerify((XECRYPT_SIG *)(bl + 0x20), hash, salt, (XECRYPT_RSA *)pubKey);
}

int blSign(uint8_t *bl, unsigned int len, const void *pubKey, const void *prvKey, const uint8_t *salt)
{
	struct {
		char salt[16];
		uint8_t hash[20];
		uint8_t sig[256];
	} s;

	memset(s.salt, 0, sizeof(s.salt));
	memcpy(s.salt, salt, 10);
	XeCryptRotSumSha(bl, 16, bl + 0x120, len - 0x120, s.hash, 20);
	/* TODO(prototype cast): as in cbVerifySig */
	if (!XeCryptBnQwBeSigCreate((XECRYPT_SIG *)s.sig, s.hash, salt, prvKey))
		return 0;
	if (!XeCryptBnQwNeRsaPrvCrypt((uint64_t *)s.sig, (uint64_t *)s.sig, prvKey))
		return 0;
	if (!XeCryptBnQwBeSigVerify((XECRYPT_SIG *)s.sig, s.hash, salt, (XECRYPT_RSA *)pubKey))
		return 0;
	memcpy(bl + 0x20, s.sig, 256);
	return 1;
}

int blCheckHash(uint8_t *bl, unsigned int len, const uint8_t *expect)
{
	uint8_t hash[20];

	XeCryptRotSumSha(bl, 16, bl + 0x20, len - 0x20, hash, 20);
	return memcmp(expect, hash, 20) == 0;
}

int blUpdateHash(uint8_t *bl, unsigned int len, uint8_t *stored)
{
	uint8_t hash[20];

	XeCryptRotSumSha(bl, 16, bl + 0x20, len - 0x20, hash, 20);
	if (memcmp(stored, hash, 20) == 0)
		return 0;
	memcpy(stored, hash, 20);
	return 1;
}

int blHashAndSign(uint8_t *bl, unsigned int len, uint8_t *prev, unsigned int prevLen, uint8_t *hashOut,
	const void *pubKey, const void *prvKey)
{
	uint8_t hash[20];

	XeCryptRotSumSha(bl, 16, bl + 0x20, len - 0x20, hash, 20);
	memcpy(hashOut, hash, 20);
	return blSign(prev, prevLen, pubKey, prvKey,
		(uint8_t *)(getBeU16(prev) != 0x5344 ? romSalts[1] : romSalts[0]));
}

/* xboxrom: hashes, signs and verifies keyvault and bootloader signatures */
#include <string.h>

#include "../crypto/xecrypt.h"
#include "xebuild.h"
#include "fileutil.h"
#include "xboxrom.h"

char romSalts[3][12] = { "XBOX_ROM_4", "XBOX_ROM_3", "XBOX_ROM_B" };

int kvVerifySig(u8 *kv, const void *pubKey, const u8 *hmacKey)
{
	u8 hash[20];

	XeCryptHmacSha(hmacKey, 16, kv + 0x1c, 0xd4, kv + 0x100, 0x1cf8, kv + 0x1ef8, 0x2108, hash, 20);
	return XeKeysPkcs1Verify(hash, kv + 0x1df8, pubKey);
}

int cbVerifySig(u8 *bl, const void *pubKey)
{
	u8 hash[20];
	unsigned int len = (getBeU32(bl + 12) + 15) & ~15;

	XeCryptRotSumSha(bl, 16, bl + 0x140, len - 0x140, hash, 20);
	/* TODO(prototype cast): the bootloaders' signatures and keys are bytes
	   here; xecrypt.h types them (and its keys aren't const) */
	return XeCryptBnQwBeSigVerify((XECRYPT_SIG *)(bl + 0x40), hash, (u8 *)romSalts[2],
				      (XECRYPT_RSA *)pubKey);
}

int blVerifySig(u8 *bl, unsigned int len, const void *pubKey, const u8 *salt)
{
	u8 hash[20];

	XeCryptRotSumSha(bl, 16, bl + 0x120, len - 0x120, hash, 20);
	/* TODO(prototype cast): as in cbVerifySig */
	return XeCryptBnQwBeSigVerify((XECRYPT_SIG *)(bl + 0x20), hash, salt, (XECRYPT_RSA *)pubKey);
}

int blSign(u8 *bl, unsigned int len, const void *pubKey, const void *prvKey, const u8 *salt)
{
	struct {
		char salt[16];
		u8 hash[20];
		u8 sig[256];
	} s;

	memset(s.salt, 0, sizeof(s.salt));
	memcpy(s.salt, salt, 10);
	XeCryptRotSumSha(bl, 16, bl + 0x120, len - 0x120, s.hash, 20);
	/* TODO(prototype cast): as in cbVerifySig */
	if (!XeCryptBnQwBeSigCreate((XECRYPT_SIG *)s.sig, s.hash, salt, prvKey))
		return 0;
	if (!XeCryptBnQwNeRsaPrvCrypt((u64 *)s.sig, (u64 *)s.sig, prvKey))
		return 0;
	if (!XeCryptBnQwBeSigVerify((XECRYPT_SIG *)s.sig, s.hash, salt, (XECRYPT_RSA *)pubKey))
		return 0;
	memcpy(bl + 0x20, s.sig, 256);
	return 1;
}

int blCheckHash(u8 *bl, unsigned int len, const u8 *expect)
{
	u8 hash[20];

	XeCryptRotSumSha(bl, 16, bl + 0x20, len - 0x20, hash, 20);
	return memcmp(expect, hash, 20) == 0;
}

int blUpdateHash(u8 *bl, unsigned int len, u8 *stored)
{
	u8 hash[20];

	XeCryptRotSumSha(bl, 16, bl + 0x20, len - 0x20, hash, 20);
	if (memcmp(stored, hash, 20) == 0)
		return 0;
	memcpy(stored, hash, 20);
	return 1;
}

int blHashAndSign(u8 *bl, unsigned int len, u8 *prev, unsigned int prevLen, u8 *hashOut,
	const void *pubKey, const void *prvKey)
{
	u8 hash[20];

	XeCryptRotSumSha(bl, 16, bl + 0x20, len - 0x20, hash, 20);
	memcpy(hashOut, hash, 20);
	return blSign(prev, prevLen, pubKey, prvKey,
		(u8 *)(getBeU16(prev) != 0x5344 ? romSalts[1] : romSalts[0]));
}

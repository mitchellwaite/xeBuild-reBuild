/* xboxrom.h: xboxrom.c's functions that other objects use */
#ifndef XBOXROM_H
#define XBOXROM_H

#include "xebuild.h"

int kvVerifySig(u8 *kv, const void *pubKey, const u8 *hmacKey);
int cbVerifySig(u8 *bl, const void *pubKey);
int blVerifySig(u8 *bl, unsigned int len, const void *pubKey, const u8 *salt);
int blSign(u8 *bl, unsigned int len, const void *pubKey, const void *prvKey,
	const u8 *salt);
int blCheckHash(u8 *bl, unsigned int len, const u8 *expect);
int blHashAndSign(u8 *bl, unsigned int len, u8 *prev, unsigned int prevLen,
	u8 *hashOut, const void *pubKey, const void *prvKey);

#endif

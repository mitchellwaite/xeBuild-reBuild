/* xboxrom.h: xboxrom.c's functions that other objects use */
#ifndef XBOXROM_H
#define XBOXROM_H

#include "xebuild.h"

int kvVerifySig(uint8_t *kv, const struct rsapub *pubKey, const uint8_t *hmacKey);
int cbVerifySig(uint8_t *bl, const struct rsapub *pubKey);
int blVerifySig(uint8_t *bl, unsigned int len, const void *pubKey, const uint8_t *salt);
int blSign(uint8_t *bl, unsigned int len, const void *pubKey, const void *prvKey,
	const uint8_t *salt);
int blCheckHash(uint8_t *bl, unsigned int len, const uint8_t *expect);
int blHashAndSign(uint8_t *bl, unsigned int len, uint8_t *prev, unsigned int prevLen,
	uint8_t *hashOut, const void *pubKey, const void *prvKey);

#endif

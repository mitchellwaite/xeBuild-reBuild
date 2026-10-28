/* bootloaders.h: bootloaders.c's functions that other objects use */
#ifndef BOOTLOADERS_H
#define BOOTLOADERS_H

#include "xebuild.h"

int verifyExtended(uint8_t *buf, uint32_t size);
int unscramble(uint8_t *buf, uint32_t len);
uint32_t cbGetPairing(uint8_t *cb);
uint32_t cfBestPairing(uint8_t *data, uint32_t size);
int cfDecrypt(uint8_t *cf, uint32_t size);
int cgDecrypt(uint8_t *cg, uint8_t *cfKey, uint32_t size);
int verifySecdata(uint8_t *buf, uint32_t size);
int verifyCrl(uint8_t *crl, uint32_t size, int perBox);
void daeDecrypt(uint8_t *dae, uint32_t size, int perBox);
int verifyDae(uint8_t *buf, uint32_t size);
int verifyFcrt(uint8_t *fcrt, uint32_t size);
int shaSelfCheck(uint8_t *p);

#endif

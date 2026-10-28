/* bootloaders.h: bootloaders.c's functions that other objects use */
#ifndef BOOTLOADERS_H
#define BOOTLOADERS_H

#include "xebuild.h"

int verifyExtended(u8 *buf, u32 size);
int unscramble(u8 *buf, u32 len);
u32 cbGetPairing(u8 *cb);
u32 cfBestPairing(u8 *data, u32 size);
int cfDecrypt(u8 *cf, u32 size);
int cgDecrypt(u8 *cg, u8 *cfKey, u32 size);
int verifySecdata(u8 *buf, u32 size);
int verifyCrl(u8 *crl, u32 size, int perBox);
void daeDecrypt(u8 *dae, u32 size, int perBox);
int verifyDae(u8 *buf, u32 size);
int verifyFcrt(u8 *fcrt, u32 size);
int shaSelfCheck(u8 *p);

#endif

/* keys.h: keys.c's functions that other objects use */
#ifndef KEYS_H
#define KEYS_H

#include "xebuild.h"

void keysInit(int random);
void setCrlKey(u8 *key);
void setDaeKey(u8 *key);
void setSecdataKey(u8 *key);
void setInfoKey0(u8 *key);
void setInfoKey1(u8 *key);
void setInfoKey2(u8 *key);
void setInfoKey3(u8 *key);
void setInfoKey4(u8 *key);
void setInfoKey5(u8 *key);
void setKvSalt(u8 *key);
void setKvAltSalt(u8 *key);
void setSmcKey(u8 *key);
int setPairing(u32 pair);
int checkCpuKey(int level, u8 *key);
int setCpuKeyStr(char *str);
int setCpuKey(int level, u8 *key);
void setFuseCpuKey(u8 *fuse);
int set1blKey(u8 *key);
int checkKeys(char *str);
int smcPrepare(u8 *smc, u8 *hash, u32 size);
void cbaEncrypt(u8 *salt, u8 *cb, u8 *key, u32 size, int zero);
void cbaEncryptZero(u8 *cb, u8 *key, u32 size);
void cbaEncrypt2(u8 *salt, u8 *cb, u8 *key, u32 size, int zero);
void cbbEncrypt(u8 *salt, u8 *cbb, u8 *cbaKey, u8 *cba, u8 *key, u32 size,
	int zero);
void cdEncryptZero(u8 *cd, u8 *key, u32 size);
void cdEncrypt(u8 *cd, u8 *prevKey, u8 *key, u32 size);
void cdEncryptCpu(u8 *cd, u8 *prevKey, u8 *key, u32 size);
void ceEncrypt(u8 *ce, u8 *prevKey, u8 *key, u32 size);
u16 cfEncrypt(struct fileent *cf, u32 extra, u16 block, int keep, u32 max);
void cgEncrypt(u8 *cg, u8 *prevKey, u8 *key, u32 size);
void kvPrepare(struct fileent *kv, int alt);
void extendedPrepare(struct fileent *ext);
void secdataPrepare(struct fileent *sd, u8 *date);
int shaCheck(u8 *buf, u32 size, u32 hashOff, u32 hashLen, u32 dataOff,
	u8 *hashOut);
void crlEncrypt(u8 *crl, u32 size, u8 *date);
void daeEncrypt(u8 *buf, u32 size, u8 *date);
void fcrtEncrypt(u8 *fcrt, u32 size);
void shaHeader(u8 *buf);

#endif

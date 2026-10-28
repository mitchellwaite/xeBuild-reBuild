/* keys.h: keys.c's functions that other objects use */
#ifndef KEYS_H
#define KEYS_H

#include "xebuild.h"

void keysInit(int random);
void setCrlKey(uint8_t *key);
void setDaeKey(uint8_t *key);
void setSecdataKey(uint8_t *key);
void setInfoKey0(uint8_t *key);
void setInfoKey1(uint8_t *key);
void setInfoKey2(uint8_t *key);
void setInfoKey3(uint8_t *key);
void setInfoKey4(uint8_t *key);
void setInfoKey5(uint8_t *key);
void setKvSalt(uint8_t *key);
void setKvAltSalt(uint8_t *key);
void setSmcKey(uint8_t *key);
int setPairing(uint32_t pair);
int checkCpuKey(int level, uint8_t *key);
int setCpuKeyStr(char *str);
int setCpuKey(int level, uint8_t *key);
void setFuseCpuKey(uint8_t *fuse);
int set1blKey(uint8_t *key);
int checkKeys(char *str);
int smcPrepare(uint8_t *smc, uint8_t *hash, uint32_t size);
void cbaEncrypt(uint8_t *salt, uint8_t *cb, uint8_t *key, uint32_t size, int zero);
void cbaEncryptZero(uint8_t *cb, uint8_t *key, uint32_t size);
void cbaEncrypt2(uint8_t *salt, uint8_t *cb, uint8_t *key, uint32_t size, int zero);
void cbbEncrypt(uint8_t *salt, uint8_t *cbb, uint8_t *cbaKey, uint8_t *cba, uint8_t *key, uint32_t size,
	int zero);
void cdEncryptZero(uint8_t *cd, uint8_t *key, uint32_t size);
void cdEncrypt(uint8_t *cd, uint8_t *prevKey, uint8_t *key, uint32_t size);
void cdEncryptCpu(uint8_t *cd, uint8_t *prevKey, uint8_t *key, uint32_t size);
void ceEncrypt(uint8_t *ce, uint8_t *prevKey, uint8_t *key, uint32_t size);
uint16_t cfEncrypt(struct fileent *cf, uint32_t extra, uint16_t block, int keep, uint32_t max);
void cgEncrypt(uint8_t *cg, uint8_t *prevKey, uint8_t *key, uint32_t size);
void kvPrepare(struct fileent *kv, int alt);
void extendedPrepare(struct fileent *ext);
void secdataPrepare(struct fileent *sd, uint8_t *date);
int shaCheck(uint8_t *buf, uint32_t size, uint32_t hashOff, uint32_t hashLen, uint32_t dataOff,
	uint8_t *hashOut);
void crlEncrypt(uint8_t *crl, uint32_t size, uint8_t *date);
void daeEncrypt(uint8_t *buf, uint32_t size, uint8_t *date);
void fcrtEncrypt(uint8_t *fcrt, uint32_t size);
void shaHeader(uint8_t *buf);

#endif

/* keyvault.h: keyvault.c's functions that other objects use */
#ifndef KEYVAULT_H
#define KEYVAULT_H

#include "xebuild.h"

/* kvGetType: a type 1 KV has no signature; a type 2 one's is checked
   against the master public key */
#define KV_TYPE1 0			/* no signature (or none checked yet) */
#define KV_TYPE2_UNCHECKED 1		/* no master public key to check it */
#define KV_TYPE2_BAD 2			/* modified, or another CPU key's */
#define KV_TYPE2_GOOD 3

int kvGetType(void);
int kvIsLoaded(void);
void kvSet(uint8_t *buf);
int kvGetGameRegion(void);
uint8_t *kvGetDvdKey(void);
uint8_t *kvGetConsoleId(void);
int kvGetSerial(char *out);
uint8_t *kvGetConsoleCert(void);
int kvGetMfgDate(char *out);
uint32_t kvSetDvdKey(char *key);

#endif

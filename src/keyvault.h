/* keyvault.h: keyvault.c's functions that other objects use */
#ifndef KEYVAULT_H
#define KEYVAULT_H

#include "xebuild.h"

int kvGetType(void);
int kvIsLoaded(void);
void kvSet(uint8_t *buf);
int kvGetGameRegion(void);
uint8_t *kvGetDvdKey(void);
uint8_t *kvGetConsoleId(void);
int kvGetSerial(char *out);
uint8_t *kvGetConsoleCert(void);
int kvGetMfgDate(char *out);
int kvSetDvdKey(char *key);

#endif

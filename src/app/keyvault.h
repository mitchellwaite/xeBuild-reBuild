/* keyvault.h: keyvault.c's functions that other objects use */
#ifndef KEYVAULT_H
#define KEYVAULT_H

#include "xebuild.h"

int kvGetType(void);
int kvIsLoaded(void);
void kvSet(u8 *buf);
int kvGetGameRegion(void);
u8 *kvGetDvdKey(void);
u8 *kvGetConsoleId(void);
int kvGetSerial(char *out);
u8 *kvGetConsoleCert(void);
int kvGetMfgDate(char *out);
int kvSetDvdKey(char *key);

#endif

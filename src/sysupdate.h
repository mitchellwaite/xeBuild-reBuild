/* sysupdate.h: sysupdate.c's functions that other objects use */
#ifndef SYSUPDATE_H
#define SYSUPDATE_H

#include "xebuild.h"

const char *suGetDir(void);
uint32_t suGetCF(uint8_t **data, uint32_t *len);
uint32_t suGetCG(uint8_t **data, uint32_t *len);
int suGetFile(const char *name, uint8_t **data, uint32_t *len);
int suNextFile(char *name, int *idx);
int suFirstFile(char *name, int *idx);
int suLoadDir(const char *dir);
uint32_t suLoad(const char *path);
void suFree(void);

#endif

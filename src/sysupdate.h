/* sysupdate.h: sysupdate.c's functions that other objects use */
#ifndef SYSUPDATE_H
#define SYSUPDATE_H

#include "xebuild.h"

const char *suGetDir(void);
int suGetCF(uint8_t **data, uint32_t *len);
int suGetCG(uint8_t **data, uint32_t *len);
int suGetFile(const char *name, uint8_t **data, uint32_t *len);
int suNextFile(char *name, int *idx);
int suFirstFile(char *name, int *idx);
int suLoadDir(const char *dir);
int suLoad(const char *path);
void suFree(void);

#endif

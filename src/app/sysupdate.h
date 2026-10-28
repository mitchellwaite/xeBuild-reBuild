/* sysupdate.h: sysupdate.c's functions that other objects use */
#ifndef SYSUPDATE_H
#define SYSUPDATE_H

#include "xebuild.h"

const char *suGetDir(void);
int suGetCF(u8 **data, u32 *len);
int suGetCG(u8 **data, u32 *len);
int suGetFile(const char *name, u8 **data, u32 *len);
int suNextFile(char *name, int *idx);
int suFirstFile(char *name, int *idx);
int suLoadDir(const char *dir);
int suLoad(const char *path);
void suFree(void);

#endif

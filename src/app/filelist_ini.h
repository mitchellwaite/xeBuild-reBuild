/* filelist_ini.h: filelist_ini.c's functions that other objects use */
#ifndef FILELIST_INI_H
#define FILELIST_INI_H

#include "xebuild.h"

u32 parseIni(char *path);
char *getIniValue(const char *key);
long getIniBool(const char *key, int def);
char *iniBoolInvalid(const char *key);
unsigned int getIniU32(const char *key, unsigned int def);
char *iniU32Invalid(const char *key);
int loadUserIni(void);

#endif

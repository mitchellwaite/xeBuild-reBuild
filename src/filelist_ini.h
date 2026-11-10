/* filelist_ini.h: filelist_ini.c's functions that other objects use */
#ifndef FILELIST_INI_H
#define FILELIST_INI_H

#include "xebuild.h"

uint32_t parseIni(char *path);
char *getIniValue(const char *key);
long getIniBool(const char *key, int def);
char *iniBoolInvalid(const char *key);
unsigned int getIniU32(const char *key, unsigned int def);
char *iniU32Invalid(const char *key);
int loadUserIni(void);

/* defined at the end of filelist_ini.c for .rdata order, used before there */
extern const char *const consoleNames[8];
extern const unsigned char validChars[74];

#endif

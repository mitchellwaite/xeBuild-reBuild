/* console_hdd.h: console_hdd.c's functions that other objects use */
#ifndef CONSOLE_HDD_H
#define CONSOLE_HDD_H

#include "xebuild.h"

void freeManifest(void);
int loadManifest(const char *dir, u32 ver);
long sendAvatarData(const char *dir, u32 ver);
u32 sendCompatData(const char *dir);

#endif

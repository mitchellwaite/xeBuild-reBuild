/* console_hdd.h: console_hdd.c's functions that other objects use */
#ifndef CONSOLE_HDD_H
#define CONSOLE_HDD_H

#include "xebuild.h"

void freeManifest(void);
uint32_t loadManifest(const char *dir, uint32_t ver);
long sendAvatarData(const char *dir, uint32_t ver);
long sendCompatData(const char *dir);

#endif

/* build.h: build.c's functions that other objects use */
#ifndef BUILD_H
#define BUILD_H

#include "xebuild.h"

uint32_t findFileOffset(int type);
int findFile(int type);
int buildFlash(void);

#endif

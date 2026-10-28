/* build.h: build.c's functions that other objects use */
#ifndef BUILD_H
#define BUILD_H

#include "xebuild.h"

u32 findFileOffset(int type);
int findFile(int type);
int buildFlash(void);

#endif

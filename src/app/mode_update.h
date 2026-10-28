/* mode_update.h: mode_update.c's functions that other objects use */
#ifndef MODE_UPDATE_H
#define MODE_UPDATE_H

#include "xebuild.h"

int updateGetFile(const char *name, u8 **data, int *size);
int mode_update(int argc, char **argv);

#endif

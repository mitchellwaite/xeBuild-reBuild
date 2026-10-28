/* mode_build.h: mode_build.c's functions that other objects use */
#ifndef MODE_BUILD_H
#define MODE_BUILD_H

#include "xebuild.h"

void build_usage(void);
int loadKeyFile(char *key, const char *dir, const char *name);
int mode_build(int argc, char **argv);

#endif

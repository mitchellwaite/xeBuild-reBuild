/* options.h: options.c's functions that other objects use */
#ifndef OPTIONS_H
#define OPTIONS_H

#include "xebuild.h"

int iniConsoleType(void);
int setConsoleType(const char *name);
int macidSet(void);
int parseCmdOptions(const char *opts);
void applyIniOptions(void);
int parseRawPatches(const char *pats);
int loadAddons(void);

#endif

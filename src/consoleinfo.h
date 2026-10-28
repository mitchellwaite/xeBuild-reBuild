/* consoleinfo.h: consoleinfo.c's functions that other objects use */
#ifndef CONSOLEINFO_H
#define CONSOLEINFO_H

#include "xebuild.h"

int parseConsoleInfo(int level, const char *dir, const char *optDir,
	int *update);

#endif

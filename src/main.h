/* main.h: main.c's functions and data that other objects use */
#ifndef MAIN_H
#define MAIN_H

#include "xebuild.h"

extern int promptEnter;
extern char separator[];

int verifyFlashFile(int i);
void logButton(int level, int code);

#endif

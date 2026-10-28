/* smc.h: smc.c's functions that other objects use */
#ifndef SMC_H
#define SMC_H

#include "xebuild.h"

int smcCheck(u8 *smc, int len, int type);
void smcPatch(u8 *smc, int len, u32 flags);
int smcConfigOk(const u8 *smc);

#endif

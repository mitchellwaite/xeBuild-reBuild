/* smc.h: smc.c's functions that other objects use */
#ifndef SMC_H
#define SMC_H

#include "xebuild.h"

int smcCheck(uint8_t *smc, int len, int type);
void smcPatch(uint8_t *smc, int len, uint32_t flags);
int smcConfigOk(const uint8_t *smc);

#endif

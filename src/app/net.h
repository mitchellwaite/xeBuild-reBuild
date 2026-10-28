/* net.h: net.c's functions that other objects use */
#ifndef NET_H
#define NET_H

#include "xebuild.h"

void netFree(void *p);
void netTimerStart(void);
void netTimerEnd(void);
uint32_t netConnect(const char *ip);
void netDisconnect(void);
uint32_t netMount(const char *drive, const char *device);
uint32_t netUnmount(const char *drive);
uint8_t *netGetFile(const char *name, int *len);
struct consoleinfo *netGetInfo(void);
int netDumpNand(const char *path);
uint8_t *netGetBldrs(int *len);
uint32_t netSendFlash(const uint8_t *buf, uint32_t len);
uint8_t *netReadBlocks(int *len, uint16_t start, uint16_t count);
int netWriteBlocks(const uint8_t *buf, uint32_t len, uint16_t start, uint16_t count);
int netEraseBlock(uint16_t block, uint16_t count);
uint8_t *netGetBadBlocks(int *len);
int netSendFile(const char *name, const void *buf, uint32_t len);
int netFormatSysex(void);
int netFormatCompat(void);
int netMkdir(const char *name);
int netReboot(int how);
int netWritePatches(const uint8_t *buf, uint32_t len);

#endif

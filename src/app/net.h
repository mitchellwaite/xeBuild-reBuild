/* net.h: net.c's functions that other objects use */
#ifndef NET_H
#define NET_H

#include "xebuild.h"

void netFree(void *p);
void netTimerStart(void);
void netTimerEnd(void);
u32 netConnect(const char *ip);
void netDisconnect(void);
u32 netMount(const char *drive, const char *device);
u32 netUnmount(const char *drive);
u8 *netGetFile(const char *name, int *len);
struct consoleinfo *netGetInfo(void);
int netDumpNand(const char *path);
u8 *netGetBldrs(int *len);
u32 netSendFlash(const u8 *buf, u32 len);
u8 *netReadBlocks(int *len, u16 start, u16 count);
int netWriteBlocks(const u8 *buf, u32 len, u16 start, u16 count);
int netEraseBlock(u16 block, u16 count);
u8 *netGetBadBlocks(int *len);
int netSendFile(const char *name, const void *buf, u32 len);
int netFormatSysex(void);
int netFormatCompat(void);
int netMkdir(const char *name);
int netReboot(int how);
int netWritePatches(const u8 *buf, u32 len);

#endif

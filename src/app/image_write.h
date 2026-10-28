/* image_write.h: image_write.c's functions that other objects use */
#ifndef IMAGE_WRITE_H
#define IMAGE_WRITE_H

#include "xebuild.h"

int buildImage(void);
void imageFree(void);
void calcPageEcc(u8 *data, u8 *spare);
int pageEccOk(u8 *datc, u8 *spare);
int blockEccOk(u8 *blk, int bigBlock);
int blockErased(u8 *blk, int bigBlock);
int isErased(const u8 *p, u32 len);
u32 imgSizeAligned(void);
void setFlashBuild(u16 build);
u32 smcSetLoad(u32 size);
u32 setPatchSlot(u32 off);
u32 imgCfOffset(void);
u32 imgCfSize(void);
u32 imgSize(void);
u32 imgSetSize(u32 size);
int imgBigBlock(void);
int imgAdd(u32 off, const void *src, u32 len, u8 type, u16 next, int pad);
void imgAddFile(const char *name, const void *data, const u32 *time, u32 len);
void imgAddFileAs(const char *name, const void *data, const u32 *time, u32 len);
u32 imgAddMobile(const void *data, u32 len, u8 type);
void fixupFsTable(u32 off);
void fixupEmptyFsBlocks(u32 off);
int addSmcConfig(const u8 *cfg, u32 len);
void writeInitialHeader(void);
long checkBootImage(int write);
void writeFsTable(u32 off);
void copyAnchorBlock(int n);
u8 *imageGetBuffer(u32 *size);
int writeImage(char *name);
int finalizeImage(void);
u32 fsStartBlock(void);
u32 statisticsOffset(int bigBlock, int big, int mmc, u32 *page, u32 *sector);
u32 manufacturingOffset(int bigBlock, int big, int mmc, u32 *page, u32 *sector);
int imgAddRaw(const char *name, const void *data, u32 len, u32 off);

#endif

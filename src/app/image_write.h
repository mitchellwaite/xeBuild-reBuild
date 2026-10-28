/* image_write.h: image_write.c's functions that other objects use */
#ifndef IMAGE_WRITE_H
#define IMAGE_WRITE_H

#include "xebuild.h"

int buildImage(void);
void imageFree(void);
void calcPageEcc(uint8_t *data, uint8_t *spare);
int pageEccOk(uint8_t *datc, uint8_t *spare);
int blockEccOk(uint8_t *blk, int bigBlock);
int blockErased(uint8_t *blk, int bigBlock);
int isErased(const uint8_t *p, uint32_t len);
uint32_t imgSizeAligned(void);
void setFlashBuild(uint16_t build);
uint32_t smcSetLoad(uint32_t size);
uint32_t setPatchSlot(uint32_t off);
uint32_t imgCfOffset(void);
uint32_t imgCfSize(void);
uint32_t imgSize(void);
uint32_t imgSetSize(uint32_t size);
int imgBigBlock(void);
int imgAdd(uint32_t off, const void *src, uint32_t len, uint8_t type, uint16_t next, int pad);
void imgAddFile(const char *name, const void *data, const uint32_t *time, uint32_t len);
void imgAddFileAs(const char *name, const void *data, const uint32_t *time, uint32_t len);
uint32_t imgAddMobile(const void *data, uint32_t len, uint8_t type);
void fixupFsTable(uint32_t off);
void fixupEmptyFsBlocks(uint32_t off);
int addSmcConfig(const uint8_t *cfg, uint32_t len);
void writeInitialHeader(void);
long checkBootImage(int write);
void writeFsTable(uint32_t off);
void copyAnchorBlock(int n);
uint8_t *imageGetBuffer(uint32_t *size);
int writeImage(char *name);
int finalizeImage(void);
uint32_t fsStartBlock(void);
uint32_t statisticsOffset(int bigBlock, int big, int mmc, uint32_t *page, uint32_t *sector);
uint32_t manufacturingOffset(int bigBlock, int big, int mmc, uint32_t *page, uint32_t *sector);
int imgAddRaw(const char *name, const void *data, uint32_t len, uint32_t off);

#endif

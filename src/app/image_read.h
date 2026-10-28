/* image_read.h: image_read.c's functions that other objects use */
#ifndef IMAGE_READ_H
#define IMAGE_READ_H

#include "xebuild.h"

void buildCleanup(void);
void listFlashFiles(void);
int fsGetFile(const char *name, uint8_t **buf, uint32_t *size, uint32_t *time);
void remapBadBlocks(int numBlocks);
uint32_t copyMuData(FILE *out, void *sha);
uint32_t loadDump(const char *path);

#endif

/* image_read.h: image_read.c's functions that other objects use */
#ifndef IMAGE_READ_H
#define IMAGE_READ_H

#include "xebuild.h"

void buildCleanup(void);
void listFlashFiles(void);
int fsGetFile(const char *name, u8 **buf, u32 *size, u32 *time);
void remapBadBlocks(int numBlocks);
u32 copyMuData(FILE *out, void *sha);
u32 loadDump(const char *path);

#endif

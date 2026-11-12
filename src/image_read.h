/* image_read.h: image_read.c's functions that other objects use */
#ifndef IMAGE_READ_H
#define IMAGE_READ_H

#include "xebuild.h"

/* checkBlock's results for a dump's block other than its LBA */
#define BLK_BAD (-1)			/* marked bad */
#define BLK_ERASED (-2)
#define BLK_BAD_LBA (-3)
#define BLK_ECC (-4)			/* fails the ECD check: remap it */
#define BLK_MIXED_LBA (-6)		/* the other controller's LBA (jaspersb) */

/* xb.badRemap entries that aren't a block */
#define REMAP_UNSET (-1)
#define REMAP_NONE (-5)			/* in the remap area: none needed */

/* the last blocks of a dump hold the remapped (bad) blocks */
#define REMAP_BLOCKS 32

void buildCleanup(void);
void listFlashFiles(void);
int fsGetFile(const char *name, uint8_t **buf, uint32_t *size, uint32_t *time);
void remapBadBlocks(int numBlocks);
uint32_t copyMuData(FILE *out, void *sha);
uint32_t loadDump(const char *path);

#endif

/* stfs.h: stfs.c's functions that other objects use, and their type */
#ifndef STFS_H
#define STFS_H

#include "xebuild.h"

/* an STFS package being read */
typedef struct {
	u8 *data;
	u32 *blocks;
	size_t size;
	u32 hdrSize;
	u8 *fileTable;
} stfs_t;

int stfsGetFile(stfs_t *c, const char *name, u8 **out, u32 *len);
void stfsInit(stfs_t *c);
void stfsFree(stfs_t *c);
u32 stfsLoad(stfs_t *c, const char *path, int magic, u32 id1, u32 id2,
	u8 *manifestHash, int verbose);

#endif

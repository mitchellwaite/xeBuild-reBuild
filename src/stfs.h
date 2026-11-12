/* stfs.h: stfs.c's functions that other objects use, and their type */
#ifndef STFS_H
#define STFS_H

#include "xebuild.h"

/* fileTable's entries (stfs.c's stfsEnt): the name (STFS_NAME bytes), and
   the size (big endian) at STFS_ENTRY_SIZE_OFF */
#define STFS_ENTRY 64
#define STFS_NAME 40
#define STFS_ENTRY_SIZE_OFF 52

/* stfsLoad's magic: a system update's "SUPD" */
#define SUPD_MAGIC 0x53555044

/* an STFS package being read */
typedef struct
{
	uint8_t *data;
	uint32_t *blocks;
	size_t size;
	uint32_t hdrSize;
	uint8_t *fileTable;
} stfs_t;

int stfsGetFile(stfs_t *c, const char *name, uint8_t **out, uint32_t *len);
void stfsInit(stfs_t *c);
void stfsFree(stfs_t *c);
int stfsLoad(stfs_t *c, const char *path, int magic, uint32_t id1, uint32_t id2,
	uint8_t *manifestHash, int verbose);

#endif

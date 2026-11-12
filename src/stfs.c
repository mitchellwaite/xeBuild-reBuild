/* stfs: container header/content/manifest hash checks, STFS file listing
   and extraction */
#include <stdlib.h>
#include <string.h>

#include "crypto/xecrypt.h"
#include "xebuild.h"
#include "fileutil.h"
#include "log.h"
#include "stfs.h"

#define LE24(p) ((p)[0] + ((p)[1] << 8) + ((p)[2] << 16))

/* the package header: its size (rounded up to a block), the hash of what
   follows from STFS_CONTENT_TYPE, the content type and title id, the top
   hash table's hash; a system update's SUPD_MAGIC and version */
#define STFS_HDR_HASH 0x32c
#define STFS_HDR_SIZE 0x340
#define STFS_CONTENT_TYPE 0x344
#define STFS_TITLE_ID 0x360
#define STFS_TOP_HASH 0x381
#define STFS_SUPD 0x971a
#define STFS_SUPD_VERSION 0x9722

/* data blocks, and the hash tables' entries (a SHA-1 and 4 bytes) */
#define STFS_BLOCK 0x1000
#define STFS_BLOCK_SHIFT 12
#define STFS_HASH_ENTRY 24
#define STFS_HASHES 170			/* entries in a hash table */

typedef struct
{
	char name[STFS_NAME];
	uint8_t namelen:6;
	uint8_t contig:1;
	uint8_t dir:1;
	uint8_t vb[3];
	uint8_t ab[3];
	uint8_t fb[3];
	uint16_t idx;
	uint32_t size;
	uint32_t mtime;
	uint32_t atime;
} stfsEnt;

int stfsCheckHashes(stfs_t *c, uint8_t *hdr, int verbose)
{
	uint8_t hash[20];
	uint8_t *ent;
	uint32_t blk, n = 0;
	uint8_t *l2 = 0;
	uint32_t off = STFS_HASH_ENTRY;
	int i, more = 1;

	XeCryptSha(c->data + STFS_CONTENT_TYPE, c->hdrSize - STFS_CONTENT_TYPE, 0, 0, 0, 0, hash, 20);
	if (memcmp(hdr + STFS_HDR_HASH, hash, 20))
	{
		return 0;
	}
	blk = c->hdrSize + STFS_BLOCK;
	ent = c->data + c->hdrSize;
	c->fileTable = c->data + blk;
	if (verbose)
	{
		log_printf(1, "header hash is OK, checking content hashes...\n");
	}
	while (more)
	{
		for (i = 0; i < STFS_HASHES && more; i++)
		{
			if (checkZeros(ent, STFS_HASH_ENTRY))
			{
				more = 0;
			}
			else
			{
				XeCryptSha(c->data + blk, STFS_BLOCK, 0, 0, 0, 0, hash, 20);
				if (memcmp(hash, ent, 20))
				{
					return 0;
				}
				c->blocks[n] = blk;
				n++;
				blk += STFS_BLOCK;
				ent += STFS_HASH_ENTRY;
			}
		}
		if (blk + 2 * STFS_BLOCK >= c->size)
		{
			more = 0;
		}
		else
		{
			ent = c->data + blk;
			if (*(uint32_t *)(ent + 20) == 0)
			{
				XeCryptSha(ent, STFS_BLOCK, 0, 0, 0, 0, hash, 20);
				if (memcmp(hdr + STFS_TOP_HASH, hash, 20))
				{
					return 0;
				}
				XeCryptSha(c->data + c->hdrSize, STFS_BLOCK, 0, 0, 0, 0, hash, 20);
				if (memcmp(hash, ent, 20))
				{
					return 0;
				}
				l2 = ent;
				blk += STFS_BLOCK;
				ent = c->data + blk;
			}
			if (l2)
			{
				XeCryptSha(ent, STFS_BLOCK, 0, 0, 0, 0, hash, 20);
				if (memcmp(hash, l2 + off, 20))
				{
					return 0;
				}
			}
			blk += STFS_BLOCK;
			off += STFS_HASH_ENTRY;
		}
	}
	if (verbose)
	{
		log_printf(1, "content hashes seem OK, everything looks good!\n");
	}
	return 1;
}

void stfsListFiles(stfs_t *c)
{
	int i = 0, done = 0;
	stfsEnt *e;

	while (!done)
	{
		if (checkZeros(c->fileTable + i * STFS_ENTRY, STFS_ENTRY))
		{
			done = 1;
		}
		else
		{
			e = (stfsEnt *)(c->fileTable + i * STFS_ENTRY);
			log_printf(1, "name: %s vb: 0x%x ab: 0x%x fb: 0x%x (off 0x%x) size 0x%x\n",
				e->name, LE24(e->vb), LE24(e->ab), LE24(e->fb), c->blocks[LE24(e->fb)], SWAP32(e->size));
			e = (stfsEnt *)(c->fileTable + i * STFS_ENTRY);
			log_printf(1, "\tfnamelen: %d cont: %d dir: %d idx: 0x%x\n",
				e->namelen, e->contig, e->dir, SWAP16(e->idx));
			i++;
		}
	}
}

int stfsCheckHeader(stfs_t *c, uint32_t magic, uint32_t id1, uint32_t id2, uint8_t *manifestHash, int verbose)
{
	uint8_t *hdr = c->data;
	uint32_t ver;

	c->hdrSize = (SWAP32(*(uint32_t *)(hdr + STFS_HDR_SIZE)) + (STFS_BLOCK - 1)) & ~(STFS_BLOCK - 1);
	if (id1 && id1 != SWAP32(*(uint32_t *)(hdr + STFS_CONTENT_TYPE)))
	{
		return 0;
	}
	if (id2 && id2 != SWAP32(*(uint32_t *)(hdr + STFS_TITLE_ID)))
	{
		return 0;
	}
	if (magic && magic != SWAP32(*(uint32_t *)(hdr + STFS_SUPD)))
	{
		return 0;
	}
	ver = 0;
	if (SWAP32(*(uint32_t *)(hdr + STFS_SUPD)) == SUPD_MAGIC)
	{
		ver = SWAP32(*(uint32_t *)(hdr + STFS_SUPD_VERSION));
	}
	c->blocks = malloc((c->size >> STFS_BLOCK_SHIFT) * 4 + 4);
	if (!c->blocks)
	{
		return 0;
	}
	if (verbose)
	{
		if (ver)
		{
			log_printf(1, "header seems valid, version %d.%d.%d.%d\n",
				ver >> 28, (ver >> 24) & 0xf, (ver >> 8) & 0xffff, ver & 0xff);
		}
		else
		{
			log_printf(1, "header seems valid\n");
		}
	}
	if (manifestHash && !checkZeros(manifestHash, 20))
	{
		if (memcmp(hdr + STFS_HDR_HASH, manifestHash, 20))
		{
			log_printf(1, "manifest hash does not match container header!\n");
			return 0;
		}
		if (verbose)
		{
			log_printf(1, "manifest hash matches container header!\n");
		}
	}
	if (stfsCheckHashes(c, hdr, verbose))
	{
		return 1;
	}
	return 0;
}

int stfsGetFile(stfs_t *c, const char *name, uint8_t **out, uint32_t *len)
{
	int i = 0, done = 0;
	int j, n, fb;
	stfsEnt *e;
	uint8_t *buf;

	while (!done)
	{
		if (checkZeros(c->fileTable + i * STFS_ENTRY, STFS_ENTRY))
		{
			done = 1;
		}
		else if (!stricmp(name, (char *)(c->fileTable + i * STFS_ENTRY)))
		{
			e = (stfsEnt *)(c->fileTable + i * STFS_ENTRY);
			if (e->contig)
			{
				buf = malloc((SWAP32(e->size) + (STFS_BLOCK - 1)) & ~(STFS_BLOCK - 1));
				if (buf)
				{
					goto found;
				}
			}
			else
			{
				log_printf(0, "\n\n***** WARNING !!! file %s is not contiguous and contents are being skipped!\n\n");
			}
		}
		i++;
	}
	return 0;
found:
	n = LE24(e->ab);
	fb = LE24(e->fb);
	for (j = 0; j < n; j++)
	{
		uint32_t off = c->blocks[j + fb];
		memcpy(buf + j * STFS_BLOCK, c->data + off, STFS_BLOCK);
	}
	*out = buf;
	*len = SWAP32(e->size);
	return 1;
}

void stfsInit(stfs_t *c)
{
	c->size = 0;
	c->hdrSize = 0;
	c->fileTable = 0;
	c->data = 0;
	c->blocks = 0;
}

void stfsFree(stfs_t *c)
{
	c->size = 0;
	c->hdrSize = 0;
	c->fileTable = 0;
	if (c->data)
	{
		free(c->data);
	}
	c->data = 0;
	if (c->blocks)
	{
		free(c->blocks);
	}
	c->blocks = 0;
}

int stfsLoad(stfs_t *c, const char *path, int magic, uint32_t id1, uint32_t id2, uint8_t *manifestHash, int verbose)
{
	int ret;
	uint8_t *p;

	if (FileExists(path))
	{
		if (verbose)
		{
			log_printf(1, "%s found, loading...", path);
		}
		p = FileToBuffer(path, &c->size);
		c->data = p;
		if (p)
		{
			if (verbose)
			{
				log_printf(1, "done!\n\tRead 0x%x bytes to memory\nchecking integrity...\n", c->size);
			}
			ret = stfsCheckHeader(c, magic, id1, id2, manifestHash, verbose);
			if (!ret)
			{
				log_printf(1, "checks failed! Container corrupt!\n");
				stfsFree(c);
			}
			return ret;
		}
		return 0;
	}
	log_printf(1, "container not found at %s, skipping load\n", path);
	return 0;
}

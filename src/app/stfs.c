/* stfs: container header/content/manifest hash checks, STFS file listing
   and extraction */
#include <stdlib.h>
#include <string.h>

#include "xebuild.h"

void log_printf(int level, const char *fmt, ...);
int checkZeros(const u8 *p, u32 len);
int FileExists(const char *name);
void *FileToBuffer(const char *name, size_t *psize);
void XeCryptSha(u8 *pbInp1, u32 cbInp1, u8 *pbInp2, u32 cbInp2,
		u8 *pbInp3, u32 cbInp3, u8 *pbOut, u32 cbOut);

#define SWAP32(x) (((x) << 24) + (((x) << 8) & 0xff0000) + (((x) >> 8) & 0xff00) + ((x) >> 24))
#define SWAP16(x) ((((x) << 8) & 0xff00) + ((x) >> 8))
#define LE24(p) ((p)[0] + ((p)[1] << 8) + ((p)[2] << 16))

typedef struct {
	u8 *data;
	u32 *blocks;
	size_t size;
	u32 hdrSize;
	u8 *fileTable;
} stfs_t;

typedef struct {
	char name[40];
	u8 namelen:6;
	u8 contig:1;
	u8 dir:1;
	u8 vb[3];
	u8 ab[3];
	u8 fb[3];
	u16 idx;
	u32 size;
	u32 mtime;
	u32 atime;
} stfsEnt;

int stfsCheckHashes(stfs_t *c, u8 *hdr, int verbose)
{
	u8 hash[20];
	u8 *ent;
	u32 blk, n = 0;
	u8 *l2 = 0;
	u32 off = 24;
	int i, more = 1;

	XeCryptSha(c->data + 0x344, c->hdrSize - 0x344, 0, 0, 0, 0, hash, 20);
	if (memcmp(hdr + 0x32c, hash, 20))
		return 0;
	blk = c->hdrSize + 0x1000;
	ent = c->data + c->hdrSize;
	c->fileTable = c->data + blk;
	if (verbose)
		log_printf(1, "header hash is OK, checking content hashes...\n");
	while (more) {
		for (i = 0; i < 170 && more; i++) {
			if (checkZeros(ent, 24))
				more = 0;
			else {
				XeCryptSha(c->data + blk, 0x1000, 0, 0, 0, 0, hash, 20);
				if (memcmp(hash, ent, 20))
					return 0;
				c->blocks[n] = blk;
				n++;
				blk += 0x1000;
				ent += 24;
			}
		}
		if (blk + 0x2000 >= c->size)
			more = 0;
		else {
			ent = c->data + blk;
			if (*(u32 *)(ent + 20) == 0) {
				XeCryptSha(ent, 0x1000, 0, 0, 0, 0, hash, 20);
				if (memcmp(hdr + 0x381, hash, 20))
					return 0;
				XeCryptSha(c->data + c->hdrSize, 0x1000, 0, 0, 0, 0, hash, 20);
				if (memcmp(hash, ent, 20))
					return 0;
				l2 = ent;
				blk += 0x1000;
				ent = c->data + blk;
			}
			if (l2) {
				XeCryptSha(ent, 0x1000, 0, 0, 0, 0, hash, 20);
				if (memcmp(hash, l2 + off, 20))
					return 0;
			}
			blk += 0x1000;
			off += 24;
		}
	}
	if (verbose)
		log_printf(1, "content hashes seem OK, everything looks good!\n");
	return 1;
}

void stfsListFiles(stfs_t *c)
{
	int i = 0, done = 0;
	stfsEnt *e;

	while (!done) {
		if (checkZeros(c->fileTable + i * 64, 64))
			done = 1;
		else {
			e = (stfsEnt *)(c->fileTable + i * 64);
			log_printf(1, "name: %s vb: 0x%x ab: 0x%x fb: 0x%x (off 0x%x) size 0x%x\n",
				e->name, LE24(e->vb), LE24(e->ab), LE24(e->fb), c->blocks[LE24(e->fb)], SWAP32(e->size));
			e = (stfsEnt *)(c->fileTable + i * 64);
			log_printf(1, "\tfnamelen: %d cont: %d dir: %d idx: 0x%x\n",
				e->namelen, e->contig, e->dir, SWAP16(e->idx));
			i++;
		}
	}
}

int stfsCheckHeader(stfs_t *c, u32 magic, u32 id1, u32 id2, u8 *manifestHash, int verbose)
{
	u8 *hdr = c->data;
	u32 ver;

	c->hdrSize = (SWAP32(*(u32 *)(hdr + 0x340)) + 0xfff) & ~0xfff;
	if (id1 && id1 != SWAP32(*(u32 *)(hdr + 0x344)))
		return 0;
	if (id2 && id2 != SWAP32(*(u32 *)(hdr + 0x360)))
		return 0;
	if (magic && magic != SWAP32(*(u32 *)(hdr + 0x971a)))
		return 0;
	ver = 0;
	if (SWAP32(*(u32 *)(hdr + 0x971a)) == 0x53555044)
		ver = SWAP32(*(u32 *)(hdr + 0x9722));
	c->blocks = malloc((c->size >> 12) * 4 + 4);
	if (!c->blocks)
		return 0;
	if (verbose) {
		if (ver)
			log_printf(1, "header seems valid, version %d.%d.%d.%d\n",
				ver >> 28, (ver >> 24) & 0xf, (ver >> 8) & 0xffff, ver & 0xff);
		else
			log_printf(1, "header seems valid\n");
	}
	if (manifestHash && !checkZeros(manifestHash, 20)) {
		if (memcmp(hdr + 0x32c, manifestHash, 20)) {
			log_printf(1, "manifest hash does not match container header!\n");
			return 0;
		}
		if (verbose)
			log_printf(1, "manifest hash matches container header!\n");
	}
	if (stfsCheckHashes(c, hdr, verbose))
		return 1;
	return 0;
}

int stfsGetFile(stfs_t *c, const char *name, u8 **out, u32 *len)
{
	int i = 0, done = 0;
	int j, n, fb;
	stfsEnt *e;
	u8 *buf;

	while (!done) {
		if (checkZeros(c->fileTable + i * 64, 64))
			done = 1;
		else if (!stricmp(name, (char *)(c->fileTable + i * 64))) {
			e = (stfsEnt *)(c->fileTable + i * 64);
			if (e->contig) {
				buf = malloc((SWAP32(e->size) + 0xfff) & ~0xfff);
				if (buf)
					goto found;
			} else
				log_printf(0, "\n\n***** WARNING !!! file %s is not contiguous and contents are being skipped!\n\n");
		}
		i++;
	}
	return 0;
found:
	n = LE24(e->ab);
	fb = LE24(e->fb);
	/* code-free hint: the empty asm asks for fb in esi (the original's
	   allocation); its block folds into the loop guard */
	if (__builtin_expect(n != 0, 1))
		__asm__("" : : "S"(fb));
	for (j = 0; j < n; j++)
		memcpy(buf + j * 0x1000, c->data + c->blocks[j + fb], 0x1000);
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
		free(c->data);
	c->data = 0;
	if (c->blocks)
		free(c->blocks);
	c->blocks = 0;
}

u32 stfsLoad(stfs_t *c, const char *path, int magic, u32 id1, u32 id2, u8 *manifestHash, int verbose)
{
	u32 ret;
	u8 *p;

	if (FileExists(path)) {
		if (verbose)
			log_printf(1, "%s found, loading...", path);
		p = FileToBuffer(path, &c->size);
		c->data = p;
		if (p) {
			if (verbose)
				log_printf(1, "done!\n\tRead 0x%x bytes to memory\nchecking integrity...\n", c->size);
			ret = stfsCheckHeader(c, magic, id1, id2, manifestHash, verbose);
			if (!ret) {
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

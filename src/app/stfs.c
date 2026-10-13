/* stfs: container header/content/manifest hash checks, STFS file listing.
   Mixed object: the hash walk, file listing and file extraction are still in
   stfs.s (re/splice.py). */
#include <stdlib.h>
#include <string.h>

typedef unsigned char u8;
typedef unsigned int u32;

void log_printf(int level, const char *fmt, ...);
int checkZeros(const u8 *p, u32 len);
int FileExists(const char *name);
void *FileToBuffer(const char *name, size_t *psize);

/* strings stay in stfs.s while it is a mixed object */
extern const char sValidVer[];
extern const char sValid[];
extern const char sManifestBad[];
extern const char sManifestOk[];
extern const char sFound[];
extern const char sDone[];
extern const char sCorrupt[];
extern const char sNotFound[];

#define SWAP32(x) (((x) << 24) + ((x) >> 24) + (((x) << 8) & 0xff0000) + (((x) >> 8) & 0xff00))

typedef struct {
	u8 *data;
	u32 *blocks;
	size_t size;
	u32 hdrSize;
	u8 *fileTable;
} stfs_t;

/* still in stfs.s */
int stfsCheckHashes(stfs_t *c, u8 *hdr, int verbose);

int stfsCheckHeader(stfs_t *c, int magic, u32 id1, u32 id2, u8 *manifestHash, int verbose)
{
	u8 *hdr = c->data;
	u32 v, ver;

	v = *(u32 *)(hdr + 0x340);
	__asm__("" : "+a"(v));	/* register hint for the copy inlined in stfsLoad */
	c->hdrSize = (SWAP32(v) + 0xfff) & ~0xfff;
	if (id1) {
		v = *(u32 *)(hdr + 0x344);
		if (id1 != SWAP32(v))
			return 0;
	}
	if (id2) {
		v = *(u32 *)(hdr + 0x360);
		if (id2 != SWAP32(v))
			return 0;
	}
	v = *(u32 *)(hdr + 0x971a);
	v = SWAP32(v);
	__asm__("" : : "a"(v));	/* register hint: keeps magic's load after the swap */
	if (magic && magic != v)
		return 0;
	ver = 0;
	if (v == 0x53555044) {
		ver = *(u32 *)(hdr + 0x9722);
		ver = SWAP32(ver);
	}
	c->blocks = malloc((c->size >> 12) * 4 + 4);
	if (!c->blocks)
		return 0;
	if (verbose) {
		if (ver)
			log_printf(1, sValidVer,
				ver >> 28, (ver >> 24) & 0xf, (ver >> 8) & 0xffff, ver & 0xff);
		else
			log_printf(1, sValid);
	}
	if (manifestHash && !checkZeros(manifestHash, 20)) {
		if (memcmp(hdr + 0x32c, manifestHash, 20)) {
			log_printf(1, sManifestBad);
			return 0;
		}
		if (verbose)
			log_printf(1, sManifestOk);
	}
	if (stfsCheckHashes(c, hdr, verbose))
		return 1;
	return 0;
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
			log_printf(1, sFound, path);
		p = FileToBuffer(path, &c->size);
		c->data = p;
		if (p) {
			if (verbose)
				log_printf(1, sDone, c->size);
			ret = stfsCheckHeader(c, magic, id1, id2, manifestHash, verbose);
			if (!ret) {
				log_printf(1, sCorrupt);
				stfsFree(c);
			}
			return ret;
		}
		return 0;
	}
	log_printf(1, sNotFound, path);
	return 0;
}

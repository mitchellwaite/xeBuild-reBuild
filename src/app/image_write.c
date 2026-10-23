/* image_write: flash layout (header, CB/CE, SMC config, Mobile*.dat, the
   FS table), spare (LBA, ECD) bytes, writing the image to disk.
   Mixed object: the functions here are spliced into image_write.s
   (re/splice.py), which still holds the rest and the data, so strings
   name the .s's (splice.py drops gcc's copies; static arrays rather
   than externs so that gcc still folds strlen of them).
   wip/app/image_write.c is the whole draft; wip/mixed.py makes this file
   from it. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;

#define SWAP16(x) ((((x) << 8) & 0xff00) + (((x) >> 8) & 0xff))
#define SWAP32(x) ((((x) & 0xff) << 24) + (((x) << 8) & 0xff0000) + (((x) >> 8) & 0xff00) + ((x) >> 24))

/* an input file of the image */
struct fileent {
	char name[0x400];
	u32 crc;			/* 400 */
	int type;			/* 404 */
	u32 offset;			/* 408 */
	u8 *data;			/* 40c */
	u32 size;			/* 410 */
	u8 key[16];			/* 414 */
	u32 fsSize;			/* 424 */
	u32 fsOffset;			/* 428 */
};

/* the parts of main.c's struct xebuild used here */
struct xebuild {
	int mode;			/* 000 */
	u32 flags;			/* 004 */
	u32 type;			/* 008 */
	u8 pad00c[0x028 - 0x00c];
	u32 muBlocks;			/* 028 end of the MU area (big block) */
	u8 spare9;			/* 02c spare bytes of system blocks */
	u8 spare8;			/* 02d */
	u8 spare7;			/* 02e */
	u8 pad02f;
	u8 *spare;			/* 030 16 spare bytes per 512-byte page */
	u32 spareSize;			/* 034 */
	u8 *hdr;			/* 038 the flash image (user data) */
	u32 userSize;			/* 03c */
	u8 *raw;			/* 040 data and spare interleaved */
	u32 blocks;			/* 044 16K blocks */
	u32 rawSize;			/* 048 */
	u32 smcConfigOffset;		/* 04c */
	int bigBlock;			/* 050 */
	int bbController;		/* 054 big block controller, small block NAND */
	u32 fsEnd;			/* 058 FS area, in 16K blocks */
	u32 fsStart;			/* 05c */
	u32 bootFlags;			/* 060 */
	u8 pad064[0x075 - 0x064];
	u8 cfLdv;			/* 075 */
	u8 pad076[0x0ac - 0x076];
	u8 *dump;			/* 0ac the nand dump's data */
	u8 *dumpSpare;			/* 0b0 its spare */
	u8 pad0b4[0x0c0 - 0x0b4];
	int dumpBigBlock;		/* 0c0 */
	u8 pad0c4[0x0cc - 0x0c4];
	int nandMu;			/* 0cc */
	u8 pad0d0[0x0d4 - 0x0d0];
	u32 nRemap;			/* 0d4 bad blocks of the dump */
	u32 remapFrom[32];		/* 0d8 */
	u32 remapTo[32];		/* 158 */
	u8 pad1d8[0x1e0 - 0x1d8];
	u8 *bl;				/* 1e0 the bootloaders */
	u32 blSize;			/* 1e4 */
	u8 pad1e8[0x264 - 0x1e8];
	u8 *netKd;			/* 264 */
	u32 netKdSize;			/* 268 */
	u8 pad26c[0x27c - 0x26c];
	u8 cpuKey[16];			/* 27c */
	u8 pad28c[0x41eb0 - 0x28c];
	struct fileent files[35];	/* 41eb0 */
	u8 pad4b0b4[0x4f508 - 0x4b0b4];
	char sha1File[0x400];		/* 4f508 */
	int sha1Write;			/* 4f908 */
};

/* the flash header (big endian) */
struct flashhdr {
	u16 magic;			/* 00 */
	u16 build;			/* 02 */
	u16 qfe;			/* 04 */
	u16 flags;			/* 06 */
	u32 cbOffset;			/* 08 */
	u32 cfOffset;			/* 0c */
	char copyright[0x40];		/* 10 */
	u8 reserved[0x10];		/* 50 */
	u32 kvLength;			/* 60 */
	u32 cfOffset2;			/* 64 */
	u32 patchSlots;			/* 68 */
	u32 kvOffset;			/* 6c */
	u32 patchSlotSize;		/* 70 */
	u32 smcConfigOffset;		/* 74 */
	u32 smcLength;			/* 78 */
	u32 smcOffset;			/* 7c */
};

/* a bootloader's header */
struct blhdr {
	u16 magic;
	u16 build;
	u16 qfe;
	u16 flags;
	u32 entry;
	u32 size;
};

/* an entry of the file table */
struct fsent {
	char name[22];
	u16 block;			/* 16 */
	u32 size;			/* 18 */
	u32 time;			/* 1c */
};

struct sp { u8 b0; u8 b1lo:4, b1hi:4; u8 b2lo:4, b2hi:4; u8 b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15; };
struct spare {
	u8 b[16];
};

void log_printf(int level, const char *fmt, ...);
int checkZeros(const u8 *p, u32 len);
u8 *setBeU16(u16 v, u8 *p);
int findFile(int type);
u32 findFileOffset(int type);
int buildFlash(void);
int imgAdd(u32 off, const void *src, u32 len, u8 type, u16 next, int pad);
u32 copyMuData(FILE *out, void *sha);
int isErased(const u8 *p, u32 len);
void writeSha1File(char *out, const char *src, const unsigned char *sha);
typedef struct { u32 state[24]; } XECRYPT_SHA_STATE;	/* SHA_CTX */
void XeCryptShaInit(XECRYPT_SHA_STATE *sha);
void XeCryptShaUpdate(XECRYPT_SHA_STATE *sha, const void *buf, u32 len);
void XeCryptShaFinal(XECRYPT_SHA_STATE *sha, u8 *out, u32 len);
void XeCryptSha(const u8 *pbInp1, u32 cbInp1, const u8 *pbInp2, u32 cbInp2,
	const u8 *pbInp3, u32 cbInp3, u8 *pbOut, u32 cbOut);

extern struct xebuild xb;
extern u32 mmcAnchor[0x80];
extern struct fsent fsFiles[256];
extern u16 fsTable[0x1000];
extern struct flashhdr hdrTemplate;
extern u32 imgEnd;

extern char copyright[0x40];

extern u32 mobileOffset;
static int nFsFiles;
static u8 smcPage[0x1000];

#define ALIGN_BLOCK(x) (((x) & 0x3fff) ? (x) + 0x4000 - ((x) & 0x3fff) : (x))

/* the LBA in the spare bytes of a block's pages */
#define setSpareLba(sp_, block) do { \
	struct sp *s_ = (sp_); \
	memset(s_, 0, 16); \
	if (xb.bigBlock) { \
		s_->b2lo = (block) >> 8; \
		s_->b0 = 0xff; \
		*((u8 *)s_ + 1) = (block); \
	} else { \
		s_->b1lo = (block) >> 8; \
		s_->b5 = 0xff; \
		s_->b0 = (block); \
	} \
} while (0)

/* the FS table entries of blocks start .. start + n: `next` for each
   (0xf1f1: leave them), or a chain (0: open, 0xffff: closed) */
#define setFsTable(start, n, next) do { \
	u32 i_; \
	if ((next) != 0xf1f1) { \
		for (i_ = 0; i_ < (n); i_++) { \
			if ((next) != 0 && (next) != 0xffff) \
				fsTable[(start) - xb.fsStart + i_] = SWAP16(next); \
			else \
				fsTable[(start) - xb.fsStart + i_] = SWAP16((start) - xb.fsStart + i_ + 1); \
		} \
		if ((next) == 0xffff) \
			fsTable[(start) + (n) - 1 - xb.fsStart] = SWAP16(0x1fff); \
	} \
} while (0)

/* the same with the chain test first */
#define setFsTableB(start, n, next) do { \
	u32 i_; \
	if ((next) != 0xf1f1) { \
		for (i_ = 0; i_ < (n); i_++) { \
			if ((next) == 0 || (next) == 0xffff) \
				fsTable[(start) - xb.fsStart + i_] = SWAP16((start) - xb.fsStart + i_ + 1); \
			else \
				fsTable[(start) - xb.fsStart + i_] = SWAP16(next); \
		} \
		if ((next) == 0xffff) \
			fsTable[(start) + (n) - 1 - xb.fsStart] = SWAP16(0x1fff); \
	} \
} while (0)

/* strings in image_write.s */
static const char iw_451760[] = "***** WARNING: cfldv was not set anywhere, setting it to 1\n";
static const char iw_45179c[] = "      please set it in ini or on command line and rebuild!\n";
static const char iw_4517f8[] = "flash header build version set to v.%d\n";
static const char iw_451820[] = "\n***** ERROR: SMC size 0x%x not supported!!!\n\n";
static const char iw_451850[] = "reset smc load address to 0x%x size 0x%x\n";
static const char iw_45187c[] = "patch slot offset reset to: 0x%x\n";
static const char iw_4518e8[] = "\tadding as %s at raw offset 0x%x len 0x%08x (end 0x%08x)\n";
static const char iw_451924[] = "\n******* ERROR: adding Mobile%c.dat will exceed available flash space! Skipped!\n\n";
static const char iw_451978[] = "\tadding Mobile%c.dat as type 0x%x at raw offset 0x%x len 0x%x (end 0x%x)\n";
static const char iw_4519c4[] = "adding smc config to offset 0x%08x, len 0x%x\n";
static const char iw_4519f4[] = "Inserting netKd data from dump into header\n";
static const char iw_451a20[] = "%c%c v%d at 0x%x size 0x%x (CB)\n";
static const char iw_451a44[] = "%c%c v%d at 0x%x size 0x%x (dual CB)\n";
static const char iw_451a6c[] = "%c%c v%d at 0x%x size 0x%x (devkit CC)\n";
static const char iw_451a94[] = "%c%c v%d at 0x%x size 0x%x (CD)\n";
static const char iw_451ab8[] = "%c%c v%d at 0x%x size 0x%x (CE)\n";
static const char iw_451adc[] = "final truncated bootloader size 0x%x\n";
static const char iw_451b2c[] = "copying anchor block %d to offset 0x%x\n";
static const char iw_451b54[] = "\n------ writing image to disk ------\n";
static const char iw_451b7a[] = "wb";
static const char iw_451b7d[] = "writing file '%s' to disk...";
static const char iw_451b9a[] = "failed!\n";
static const char iw_451ba4[] = "\n***** ERROR: was not able to write %d bytes to the file %s!\n";
static const char iw_451be4[] = "done!\ncreating SHA-1 hash from system area data...";
static const char iw_451c18[] = "done!\nwriting SHA-1 to file...";
static const char iw_451c38[] = "done!\nchecking and copying > 64M NAND data from dump file if present and updating SHA-1...\n";
static const char iw_451c94[] = "done!\nchecking and copying > 64M NAND data from dump file if present...\n";
static const char iw_451cdd[] = "done!\n";
static const char iw_451f80[] = "\tadding %s at raw offset 0x%x len 0x%x (end 0x%x)\n";

/* still in image_write.s */
int imgWriteStart(const void *src, u32 len, u16 next) __attribute__((regparm(3)));
int imgWriteAt(u32 off, const void *src, u32 len, u16 next) __attribute__((regparm(3)));
int imgAdd(u32 off, const void *src, u32 len, u8 type, u16 next, int pad);
void imgAddFile(const char *name, const void *data, const u32 *time, u32 len);
void writeFsTable(u32 off);
int finalizeImage(void);

/* imgWriteStart for big-block NAND (no FS table) */
static int imgWriteHdr(const void *src, u32 len)
{
	/* its own function: called once, so it inlines.  imgWriteStart can't
	   for this call: the u16 `next` is passed promoted to int, so the
	   inliner never sees its value.  The two b0 stores are spelt
	   differently, or cselim sinks them after byte 1.  Absolute page
	   numbers in the inner loop: gcc then guesses its trip count instead
	   of knowing 32, which makes the call block's alignment come out */
	u32 off = 0, first, rem, tail, blocks, start, b, p;
	struct sp *s;

	if (off > xb.rawSize || off + len > xb.rawSize)
		return -1;
	start = off >> 14;
	first = (off & 0x3fff) ? 0x4000 - (off & 0x3fff) : 0;
	if (len <= first) {
		blocks = 1;
		tail = len;
	} else {
		rem = len - first;
		tail = rem < 0x4000 ? rem : rem % 0x4000;
		blocks = rem / 0x4000;
		if (tail)
			blocks++;
		if (first)
			blocks++;
	}
	memcpy(xb.hdr + off, src, len);
	if (tail)
		memset(xb.hdr + off + len, 0, ((off + len + 0x3fff) & ~0x3fff) - (off + len));
	for (b = 0; b < blocks; b++)
		for (p = (start + b) * 32; p < (start + b + 1) * 32; p++) {
			s = (struct sp *)(xb.spare + p * 16);
			memset(s, 0, 16);
			if (xb.bigBlock) {
				s->b2lo = (start + b) >> 8;
				s->b0 = 0xff;
				*((u8 *)s + 1) = start + b;
			} else {
				s->b1lo = (start + b) >> 8;
				s->b5 = 0xff;
				*(u8 *)s = start + b;
			}
		}
	imgEnd = off + len;
	return 0;
}

static __attribute__((noclone)) int imgWritePage(u32 off, const void *src, u16 next)
{
	u32 blocks, start, b, p, i, x, first;

	if (xb.rawSize < off || xb.rawSize < off + 0x1000)
		return -1;
	__asm__("" :: "S"(off + 0x1000));
	x = off & 0x3fff;
	__asm__("" : "+c"(x));
	start = off >> 14;
	blocks = 1;
	if (x)
		blocks = (0x4000 - x >= 0x1000) ? 1 : 2;
	memcpy(xb.hdr + off, src, 0x1000);
	__asm__("" :: "S"(start + blocks), "a"(start * 512));
	for (b = 0; b < blocks; b++)
		for (p = 0; p < 8; p++)
			setSpareLba((struct sp *)(xb.spare + ((start + b) * 32 + p) * 16), start + b);
	if (next != 0xf1f1) {
		for (i = 0; i < blocks; i++) {
			if (next != 0 && next != 0xffff)
				fsTable[start - xb.fsStart + i] = SWAP16(next);
			else
				fsTable[start - xb.fsStart + i] = SWAP16(start - xb.fsStart + i + 1);
		}
		if (next == 0xffff) {
			x = ~xb.fsStart;
			__asm__("" : "+a"(x));
			fsTable[(int)(x + start) + (int)blocks] = SWAP16(0x1fff);
		}
	}
	imgEnd = off + 0x1000;
	return 0;
}

int buildImage(void)
{
	u32 rawSize, spareSize, userSize, cf, bb;
	int bigBlock;
	u8 *spare, *hdr;

	if (xb.type == 1)
		xb.files[findFile(9)].offset = xb.files[findFile(25)].offset;
	if (xb.flags & 0x40000000) {
		xb.blocks = 0x1000;
		xb.smcConfigOffset = 0x3be0000;
		xb.bigBlock = 1;
		xb.spare9 = 4;
		xb.spare7 = 0x10;
		if (xb.flags & 0x20000000) {
			xb.fsStart = 0x2e0;
			xb.fsEnd = 0xee0;
			userSize = 0x4000000;
			xb.spare8 = 0x60;
			xb.muBlocks = 0x5c;
		} else {
			xb.fsStart = 0xae0;
			xb.fsEnd = 0xee0;
			userSize = 0x4000000;
			xb.spare8 = 0x20;
			xb.muBlocks = 0x15c;
		}
		spareSize = 0x200000;
		bigBlock = 1;
		rawSize = 0x4200000;
	} else if (xb.type != 6 && xb.type != 8) {
		if (xb.flags & 0x10000000) {
			xb.blocks = 0xc00;
			xb.smcConfigOffset = 0x2ffc000;
			userSize = 0x3000000;
			xb.fsStart = 0;
			xb.fsEnd = 0xbfa;
			spareSize = 0x180000;
			rawSize = 0x3180000;
		} else {
			xb.blocks = 0x400;
			xb.smcConfigOffset = 0xf7c000;
			userSize = 0x1000000;
			xb.fsStart = 0;
			xb.fsEnd = 0x3dc;
			spareSize = 0x80000;
			rawSize = 0x1080000;
		}
		xb.bigBlock = 0;
		bigBlock = 0;
	} else {
		xb.blocks = 0x1000;
		xb.smcConfigOffset = 0x3dfc000;
		userSize = 0x4000000;
		xb.bigBlock = 0;
		xb.fsStart = 0;
		spareSize = 0x200000;
		xb.fsEnd = 0xf7c;
		bigBlock = 0;
		rawSize = 0x4200000;
	}
	xb.rawSize = rawSize;
	xb.spareSize = spareSize;
	xb.spare = spare = malloc(spareSize);
	xb.userSize = userSize;
	xb.hdr = hdr = malloc(userSize);
	if (!hdr)
		return -1;
	if (!spare)
		return -1;
	memset(spare, 0xff, spareSize);
	memset(hdr, 0xff, userSize);
	memset(fsFiles, 0, sizeof(fsFiles));
	memset(fsTable, 0, sizeof(fsTable));
	memset(&hdrTemplate, 0, sizeof(hdrTemplate));
	hdrTemplate.magic = 0x4fff;
	hdrTemplate.build = 0x6007;
	memset(mmcAnchor, 0, sizeof(mmcAnchor));
	if (xb.type == 2) {
		hdrTemplate.cbOffset = 0x800000;
		hdrTemplate.cfOffset = 0x700;
		hdrTemplate.kvLength = 0x400000;
		hdrTemplate.cfOffset2 = 0x700;
		hdrTemplate.patchSlots = 0x12070200;
		hdrTemplate.kvOffset = 0x400000;
		hdrTemplate.smcLength = 0x300000;
		hdrTemplate.smcOffset = 0x100000;
		imgEnd = 0x8000;
		if ((xb.flags & 7) == 4) {
			if (xb.flags & 0x80000000) {
				xb.bbController = 1;
				hdrTemplate.patchSlotSize = 0x100;
			}
			__asm__("" :: "d"(bigBlock));
			if (bigBlock)
				hdrTemplate.patchSlotSize = 0x100;
			copyright[10] = '8';
		} else if ((xb.flags & 7) == 1 || (xb.flags & 7) == 2) {
			copyright[10] = '5';
			hdrTemplate.kvLength = 0;
		} else
			copyright[10] = '7';
	} else {
		hdrTemplate.cbOffset = xb.type - 8 < 2 ? 0xc00000 : 0x800000;
		cf = SWAP32(findFileOffset(9));
		hdrTemplate.patchSlots = 0x12070200;
		hdrTemplate.kvOffset = 0x400000;
		hdrTemplate.smcLength = 0x300000;
		hdrTemplate.smcOffset = 0x100000;
		imgEnd = 0x8000;
		hdrTemplate.kvLength = xb.type - 8 < 2 ? 0x800000 : 0x400000;
		hdrTemplate.cfOffset = cf;
		hdrTemplate.cfOffset2 = cf;
		switch (xb.flags & 7) {
		case 1:
		case 2:
			copyright[10] = '5';
			hdrTemplate.kvLength = 0;
			break;
		case 3:
			copyright[10] = '7';
			break;
		case 4:
			if (xb.flags & 0x80000000) {
				xb.bbController = 1;
				hdrTemplate.patchSlotSize = 0x100;
			}
			bb = xb.bigBlock;
			__asm__("" :: "b"(bb));
			if (bb)
				hdrTemplate.patchSlotSize = 0x200;
			copyright[10] = '9';
			break;
		case 5:
			xb.bbController = 1;
			hdrTemplate.patchSlotSize = 0x100;
			copyright[9] = '1';
			copyright[10] = '0';
			break;
		case 6:
		case 7:
			xb.bbController = 1;
			hdrTemplate.patchSlotSize = 0x100;
			copyright[9] = '1';
			copyright[10] = '0';
			hdrTemplate.smcOffset = 0x800;
			hdrTemplate.smcLength = 0x3800;
			break;
		}
	}
	if (xb.type > 5) {
		copyright[9] = '1';
		hdrTemplate.qfe = 0x80;
		copyright[10] = '0';
		hdrTemplate.patchSlotSize = xb.bigBlock ? 0x200 : 0x100;
	} else if (!checkZeros(xb.cpuKey, 16) && !xb.cfLdv) {
		log_printf(0, iw_451760);
		if (xb.type != 2)
			log_printf(0, iw_45179c);
		xb.cfLdv = 1;
	}
	memcpy(hdrTemplate.copyright, copyright, sizeof(copyright));
	if (xb.type != 1) {
		xb.hdr[0x49] = 0;
		xb.hdr[0x4a] = 0;
	}
	return buildFlash();
}

void imageFree(void)
{
	if (xb.spare)
		free(xb.spare);
	if (xb.hdr)
		free(xb.hdr);
	if (xb.raw)
		free(xb.raw);
	if (xb.bl)
		free(xb.bl);
}

/* the 26-bit ECD of a page: its 512 data bytes and 12 spare bytes */
u32 calcEcd(u8 *datc, u8 *spare)
{
	unsigned int i = 0, val = 0;
	unsigned int v = 0;
	unsigned int *data = (unsigned int *)datc;
	for (i = 0; i < 0x1066; i++) {
		if (!(i & 31)) {
			if (i == 0x1000)
				data = (unsigned int *)spare;
			v = ~*data++;
		}
		val ^= v & 1;
		v >>= 1;
		if (val & 1)
			val ^= 0x6954559;
		val >>= 1;
	}
	return ~val;
}

void calcPageEcc(u8 *data, u8 *spare)
{
	u32 val = calcEcd((u8 *)data, spare);

	spare[12] = (spare[12] & 0x3f) + (val << 6);
	spare[13] = val >> 2;
	spare[14] = val >> 10;
	spare[15] = val >> 18;
}

int pageEccOk(u8 *datc, u8 *spare)
{
	unsigned int i = 0, val = 0;
	unsigned int v = 0;
	unsigned int *data = (unsigned int *)datc;

	for (i = 0; i < 0x1066; i++) {
		if (!(i & 31)) {
			if (i == 0x1000)
				data = (unsigned int *)spare;
			v = ~*data++;
		}
		val ^= v & 1;
		v >>= 1;
		if (val & 1)
			val ^= 0x6954559;
		val >>= 1;
	}
	val = ~val;
	if ((spare[12] & 0xC0) != ((val << 6) & 0xFF))
		return 0;
	if (spare[13] != ((val >> 2) & 0xFF))
		return 0;
	if (spare[14] != ((val >> 10) & 0xFF))
		return 0;
	if (spare[15] != ((val >> 18) & 0xFF))
		return 0;
	return 1;
}

int pageErased(const u8 *data, const u8 *spare)
{
	int i;

	for (i = 0; i < 512; i++)
		if (data[i] != 0xff)
			return 0;
	for (i = 0; i < 16; i++)
		if (spare[i] != 0xff)
			return 0;
	return 1;
}

/* a raw block (data and spare interleaved) */
int blockEccOk(u8 *blk, int bigBlock)
{
	int i, pages = bigBlock ? 256 : 32;

	for (i = 0; i < pages; i++) {
		if (pageErased(blk + i * 528, blk + i * 528 + 512))
			continue;
		if (pageEccOk(blk + i * 528, blk + i * 528 + 512))
			continue;
		return 0;
	}
	return 1;
}

int blockErased(u8 *blk, int bigBlock)
{
	return isErased(blk, (bigBlock ? 256 : 32) * 528);
}

int blockPagesErased(u8 *data, u8 *spare, int bigBlock)
{
	int i, pages = bigBlock ? 256 : 32;

	for (i = 0; i < pages; i++)
		if (!pageErased(data + i * 512, spare + i * 16))
			return 0;
	return 1;
}

int blockIsFF(const u8 *p)
{
	int i;

	for (i = 0; i < 0x4000; i++)
		if (p[i] != 0xff)
			return 0;
	return 1;
}

int isErased(const u8 *p, u32 len)
{
	u32 i;

	for (i = 0; i < len; i++)
		if (p[i] != 0xff)
			return 0;
	return 1;
}

/* LBA and ECD of each page of a raw block */
void setBlockSpare(u8 *blk, u32 lba, int bigBlock)
{
	int i, pages = bigBlock ? 256 : 32;

	for (i = 0; i < pages; i++) {
		struct sp *s = (struct sp *)(blk + i * 528 + 512);

		memset(s, 0, 16);
		if (bigBlock) {
			s->b2lo = lba >> 8;
			s->b0 = 0xff;
			*((u8 *)s + 1) = lba;
		} else if (xb.bbController) {
			s->b2lo = lba >> 8;
			s->b5 = 0xff;
			*((u8 *)s + 1) = lba;
		} else {
			s->b1lo = lba >> 8;
			s->b5 = 0xff;
			s->b0 = lba;
		}
		calcPageEcc(blk + i * 528, (u8 *)s);
	}
}

u32 imgSizeAligned(void)
{
	u32 r = imgEnd % 0x4000;

	return r ? imgEnd + 0x4000 - r : imgEnd;
}

void setFlashBuild(u16 build)
{
	u16 *p = (u16 *)(xb.hdr + 2);

	*p = SWAP16(build);
	log_printf(1, iw_4517f8, SWAP16(*p));
}

u32 smcSetLoad(u32 size)
{
	u32 *h = (u32 *)xb.hdr;

	if (size > 0x3800) {
		log_printf(0, iw_451820, size);
		return 0;
	}
	h[30] = SWAP32(size);
	h[31] = SWAP32(0x4000 - size);
	log_printf(1, iw_451850, SWAP32(h[31]), SWAP32(h[30]));
	return 0x4000 - size;
}

u32 imgSmcOffset(void)
{
	return ((u32 *)xb.hdr)[31];
}

u32 setPatchSlot(u32 off)
{
	u32 *h = (u32 *)xb.hdr;
	u32 v;

	if (!off)
		off = imgEnd;
	if (xb.bigBlock) {
		off = (off + 0x1ffff) & ~0x1ffff;
		if (xb.type == 1) {
			u32 cf = SWAP32(h[28]);

			xb.spare7 = (off + (cf ? cf * 2 : 0x20000)) >> 17;
		}
	} else
		off = (off + 0x3fff) & ~0x3fff;
	v = SWAP32(off);
	h[25] = v;
	h[3] = v;
	log_printf(1, iw_45187c, SWAP32(v));
	return off;
}

u32 imgCfOffset(void)
{
	u32 *h = (u32 *)xb.hdr;

	return SWAP32(h[25]);
}

u32 imgCfSize(void)
{
	u32 *h = (u32 *)xb.hdr;
	u32 v = SWAP32(h[28]);

	return v ? v : 0x10000;
}

u32 imgSize(void)
{
	return imgEnd;
}

u32 imgSetSize(u32 size)
{
	return imgEnd = size;
}

int imgBigBlock(void)
{
	return xb.bigBlock;
}

int imgFits(u32 off, u32 len)
{
	return (xb.fsEnd - 1) * 0x4000 >= off + len;
}

void imgAddFileAs(const char *name, const void *data, const u32 *time, u32 len)
{
	u32 off = imgSizeAligned();

	log_printf(1, iw_4518e8, name, off, len, off + len);
	imgAddFile(name, data, time, len);
}

u32 imgAddMobile(const void *data, u32 len, u8 type)
{
	u32 off, end, ret;

	if (xb.bigBlock) {
		if (!mobileOffset) {
			mobileOffset = imgSizeAligned();
			if (mobileOffset & 0x1ffff)
				mobileOffset = (mobileOffset + 0x20000) & ~0x1ffff;
		} else if ((mobileOffset & ~0x1ffff) + 0x20000 < mobileOffset + len)
			mobileOffset = (mobileOffset + 0x20000) & ~0x1ffff;
		off = mobileOffset;
		if (!imgFits(off, len)) {
			log_printf(0, iw_451924,
				type + 17);
			return 0;
		}
		log_printf(1, iw_451978,
			type + 17, type, off, len, off + len);
		imgAdd(mobileOffset, data, len, type, 0x1ffe, 0);
		ret = mobileOffset >> 17;
		mobileOffset += len;
		if (mobileOffset & 0x7ff)
			mobileOffset = (mobileOffset + 0x800) & ~0x7ff;
		return ret;
	}
	mobileOffset = off = imgSizeAligned();
	if (__builtin_expect(imgFits(off, len), 1)) {
		log_printf(1, iw_451978,
			type + 17, type, off, len, off + len);
		ret = mobileOffset >> 14;
		imgAdd(mobileOffset, data, len, type, 0x1ffe, 0);
		return ret;
	}
	log_printf(0, iw_451924,
		type + 17);
	return 0;
}

void fixupFsTable(u32 off)
{
	u32 i;

	for (i = 0; i < off >> 14; i++)
		if (fsTable[i - xb.fsStart] != SWAP16(0x1ffb))
			fsTable[i - xb.fsStart] = SWAP16(0x1ffb);
}

void fixupEmptyFsBlocks(u32 off)
{
	u32 b, i, n;

	for (b = off >> 14; b < xb.fsEnd; b++)
		fsTable[b - xb.fsStart] = SWAP16(0x1ffe);
	if (!xb.bigBlock) {
		n = (xb.flags & 0x10000000) ? 6 : 4;
		if (xb.type > 5)
			n = xb.blocks - xb.fsEnd;
		for (i = 0; i < n; i++)
			fsTable[xb.fsEnd + i] = SWAP16(0x1ffb);
	}
	if (xb.type == 2) {
		xb.spare[26] = 3;
		xb.spare[27] = 0x50;
	}
}

int addSmcConfig(const u8 *cfg, u32 len)
{
	memset(smcPage, 0xff, sizeof(smcPage));
	memcpy(smcPage, cfg, 0x400);
	log_printf(1, iw_4519c4, xb.smcConfigOffset, len);
	if (xb.bigBlock)
		return imgWritePage(xb.smcConfigOffset, smcPage, 0xf1f1);
	return imgWritePage(xb.smcConfigOffset, smcPage, 0x1ffb);
}

void writeInitialHeader(void)
{
	if (xb.bigBlock)
		imgWriteHdr(&hdrTemplate, sizeof(hdrTemplate));
	else
		imgWriteStart(&hdrTemplate, sizeof(hdrTemplate), 0x1ffb);
	if (xb.netKd && xb.netKdSize) {
		log_printf(1, iw_4519f4);
		if (xb.bigBlock)
			imgWriteAt(0x80, xb.netKd, xb.netKdSize, 0xf1f1);
		else
			imgWriteAt(0x80, xb.netKd, xb.netKdSize, 0x1ffb);
	}
}

long checkBootImage(int write)
{
	struct flashhdr *h = (struct flashhdr *)xb.bl;
	struct blhdr *b;
	u32 off, size;
	u16 magic, build;

	off = (SWAP32(h->kvOffset) + SWAP32(h->kvLength) + 15) & ~15;
	b = (struct blhdr *)(xb.bl + off);
	magic = SWAP16(b->magic);
	build = SWAP16(b->build);
	size = SWAP32(b->size);
	log_printf(1, iw_451a20, magic >> 8, magic & 0xff, build, off, size);
	if ((magic & 0x43ff) != 0x4342)
		return -1;
	off = (off + size + 15) & ~15;
	if (SWAP16(b->flags) & 0x800) {
		b = (struct blhdr *)(xb.bl + off);
		magic = SWAP16(b->magic);
		build = SWAP16(b->build);
	build = SWAP16(b->build);
		size = SWAP32(b->size);
		log_printf(1, iw_451a44, magic >> 8, magic & 0xff, build, off, size);
		if ((magic & 0x43ff) != 0x4342)
			return -1;
		off = (off + size + 15) & ~15;
	} else if (magic & 0x1000) {
		b = (struct blhdr *)(xb.bl + off);
		magic = SWAP16(b->magic);
		build = SWAP16(b->build);
	build = SWAP16(b->build);
		size = SWAP32(b->size);
		log_printf(1, iw_451a6c, magic >> 8, magic & 0xff, build, off, size);
		if ((magic & 0x43ff) != 0x4343)
			return -1;
		off = (off + size + 15) & ~15;
	}
	b = (struct blhdr *)(xb.bl + off);
	magic = SWAP16(b->magic);
	build = SWAP16(b->build);
	size = SWAP32(b->size);
	log_printf(1, iw_451a94, magic >> 8, magic & 0xff, build, off, size);
	if ((magic & 0x43ff) != 0x4344)
		return -1;
	off = (off + size + 15) & ~15;
	b = (struct blhdr *)(xb.bl + off);
	magic = SWAP16(b->magic);
	build = SWAP16(b->build);
	log_printf(1, iw_451ab8, magic >> 8, magic & 0xff, build, off, SWAP32(b->size));
	if ((magic & 0x43ff) != 0x4345)
		return -1;
	xb.blSize = (off + SWAP32(b->size) + 15) & ~15;
	log_printf(1, iw_451adc, xb.blSize);
	if (write) {
		if (xb.bigBlock)
			imgWriteStart(xb.bl, xb.blSize, 0xf1f1);
		else
			imgWriteStart(xb.bl, xb.blSize, 0x1ffb);
	}
	return 0;
}

void copyAnchorBlock(int n)
{
	u32 off = n != 1 ? 0x2fec000 : 0x2fe8000;

	log_printf(1, iw_451b2c, n, off);
	memset(xb.hdr + off, 0, 0x1000);
	memcpy(xb.hdr + off, mmcAnchor, sizeof(mmcAnchor));
}

int spareUsed(const u8 *s)
{
	int i;

	for (i = 0; i < 16; i++)
		if (s[i] != 0xff)
			return 1;
	return 0;
}

u8 *imageGetBuffer(u32 *size)
{
	if (xb.flags & 0x10000000) {
		*size = 0x3000000;
		return xb.hdr;
	}
	*size = xb.blocks * 0x4200;
	return xb.raw;
}

int writeImage(char *name)
{
	FILE *f;

	log_printf(1, iw_451b54);
	f = fopen(name, iw_451b7a);
	if (!f)
		return -2;
	log_printf(1, iw_451b7d, name);
	if (xb.flags & 0x10000000) {
		if (fwrite(xb.hdr, 0x3000000, 1, f) != 1) {
			log_printf(1, iw_451b9a);
			log_printf(0, iw_451ba4, 0x3000000, name);
			fclose(f);
			return 1;
		}
		if (xb.sha1Write) {
			u8 hash[20];

			log_printf(1, iw_451be4);
			XeCryptSha(xb.hdr, 0x3000000, 0, 0, 0, 0, hash, 20);
			log_printf(1, iw_451c18);
			writeSha1File(xb.sha1File, name, hash);
		}
	} else {
		XECRYPT_SHA_STATE sha;
		u8 hash[20];

		if (fwrite(xb.raw, xb.blocks * 0x4200, 1, f) != 1) {
			log_printf(1, iw_451b9a);
			log_printf(0, iw_451ba4, xb.blocks * 0x4200, name);
			fclose(f);
			return 1;
		}
		if (xb.sha1Write) {
			log_printf(1, iw_451be4);
			XeCryptShaInit(&sha);
			XeCryptShaUpdate(&sha, xb.raw, xb.blocks * 0x4200);
		}
		if (xb.nandMu && (xb.bootFlags & 0x10000000)) {
			if (xb.sha1Write) {
				log_printf(1, iw_451c38);
				xb.nandMu = copyMuData(f, &sha);
			} else {
				log_printf(1, iw_451c94);
				xb.nandMu = copyMuData(f, 0);
			}
		}
		if (xb.sha1Write) {
			XeCryptShaFinal(&sha, hash, 20);
			log_printf(1, iw_451c18);
			writeSha1File(xb.sha1File, name, hash);
		}
		free(xb.raw);
		xb.raw = 0;
	}
	log_printf(1, iw_451cdd);
	fclose(f);
	return 0;
}

u32 fsStartBlock(void)
{
	return xb.fsStart;
}

u32 reservedAreaOffset(int bigBlock, int big, int mmc, u32 *page, u32 *sector, int n)
{
	u32 b, off;

	if (mmc) {
		b = n + 0xbff;
		off = b * 0x4000;
		if (page)
			*page = b * 0x200;
		if (sector)
			*sector = b * 0x20;
		return off;
	}
	if (bigBlock) {
		b = n + 0x1df;
		off = b * 0x20000;
		if (page)
			*page = b * 0x1000;
		if (sector)
			*sector = b * 0x800;
		return off;
	}
	if (big) {
		b = n + 0xf7f;
		off = b * 0x4000;
		if (page)
			*page = b * 0x200;
		if (sector)
			*sector = b * 0x20;
		return off;
	}
	b = n + 0x3df;
	off = b * 0x4000;
	if (page)
		*page = b * 0x200;
	if (sector)
		*sector = b * 0x20;
	return off;
}

u32 statisticsOffset(int bigBlock, int big, int mmc, u32 *page, u32 *sector)
{
	if (mmc) {
		if (page)
			*page = 0x17fc00;
		if (sector)
			*sector = 0x17fc0;
		return 0x2ff8000;
	}
	if (bigBlock) {
		if (page)
			*page = 0x1de000;
		if (sector)
			*sector = 0xef000;
		return 0x3bc0000;
	}
	if (big) {
		if (page)
			*page = 0x1efc00;
		if (sector)
			*sector = 0x1efc0;
		return 0x3df8000;
	}
	if (page)
		*page = 0x7bc00;
	if (sector)
		*sector = 0x7bc0;
	return 0xf78000;
}

u32 manufacturingOffset(int bigBlock, int big, int mmc, u32 *page, u32 *sector)
{
	if (mmc) {
		if (page)
			*page = 0x17fa00;
		if (sector)
			*sector = 0x17fa0;
		return 0x2ff4000;
	}
	if (bigBlock) {
		if (page)
			*page = 0x1dd000;
		if (sector)
			*sector = 0xee800;
		return 0x3ba0000;
	}
	if (big) {
		if (page)
			*page = 0x1efa00;
		if (sector)
			*sector = 0x1efa0;
		return 0x3df4000;
	}
	if (page)
		*page = 0x7ba00;
	if (sector)
		*sector = 0x7ba0;
	return 0xf74000;
}

int imgAddRaw(const char *name, const void *data, u32 len, u32 off)
{
	log_printf(1, iw_451f80, name, off, len, off + len);
	if (xb.bigBlock)
		return imgWritePage(off, data, 0xf1f1);
	return imgWritePage(off, data, 0x1ffb);
}

/* image_write: flash layout (header, CB/CE, SMC config, Mobile*.dat, the
   FS table), spare (LBA, ECD) bytes, writing the image to disk.
   Built as one C object (no .s): gcc's default top-level order emits
   the functions as the original (imgAdd's ipa-cp clones first), and the
   string literals and jump table in .rdata in its order */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "xebuild.h"

#define SWAP16(x) ((((x) << 8) & 0xff00) + (((x) >> 8) & 0xff))
#define SWAP32(x) ((((x) & 0xff) << 24) + (((x) << 8) & 0xff0000) + (((x) >> 8) & 0xff00) + ((x) >> 24))

/* a bootloader's header */
struct blhdr {
	u16 magic;
	u16 build;
	u16 qfe;
	u16 flags;
	u32 entry;
	u32 size;
};

struct spb { u8 b0; u8 b1; u8 b2lo:4, b2hi:4; u8 b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15; };
struct sps { u8 b0; u8 b1lo:4, b1hi:4; u8 b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15; };
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
int pageErased(const u8 *data, const u8 *spare);
u32 copyMuData(FILE *out, void *sha);
int isErased(const u8 *p, u32 len);
void writeSha1File(char *out, const char *src, const unsigned char *sha);
typedef struct { u32 state[24]; } XECRYPT_SHA_STATE;	/* SHA_CTX */
void XeCryptShaInit(XECRYPT_SHA_STATE *sha);
void XeCryptShaUpdate(XECRYPT_SHA_STATE *sha, const void *buf, u32 len);
void XeCryptShaFinal(XECRYPT_SHA_STATE *sha, u8 *out, u32 len);
void XeCryptSha(const u8 *pbInp1, u32 cbInp1, const u8 *pbInp2, u32 cbInp2,
	const u8 *pbInp3, u32 cbInp3, u8 *pbOut, u32 cbOut);
/* the malloc call without the builtin: same call, but CCP doesn't assume
   MALLOC_ABI_ALIGNMENT for the result (the ECD memcpy aligns its destination) */
void *xmalloc(size_t) __asm__("_malloc") __attribute__((malloc));

extern struct fsent fsFiles[256];
extern u16 fsTable[0x1000];
extern struct flashhdr hdrTemplate;
extern u32 imgEnd;

/* the year's last digit is a NUL in the image: buildImage sets it per
   console type */
char copyright[0x40] = "\xa9 2004-200\0 Microsoft Corporation. All rights reserved.";

/* initialised, so .bss rather than COMMON; gcc emits them in reverse
   order of definition */
int nFsFiles = 0;
u32 mobileOffset = 0;
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
	memset(xb.mmcAnchor, 0, sizeof(xb.mmcAnchor));
	if (xb.type == 2) {
		hdrTemplate.cbOffset = 0x800000;
		hdrTemplate.cfOffset = 0x700;
		hdrTemplate.kvSize = 0x400000;
		hdrTemplate.sysUpdateAddr = 0x700;
		hdrTemplate.patchSlots = 0x12070200;
		hdrTemplate.kvAddr = 0x400000;
		hdrTemplate.smcBootSize = 0x300000;
		hdrTemplate.smcBootAddr = 0x100000;
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
			hdrTemplate.kvSize = 0;
		} else
			copyright[10] = '7';
	} else {
		hdrTemplate.cbOffset = xb.type - 8 < 2 ? 0xc00000 : 0x800000;
		cf = SWAP32(findFileOffset(9));
		hdrTemplate.patchSlots = 0x12070200;
		hdrTemplate.kvAddr = 0x400000;
		hdrTemplate.smcBootSize = 0x300000;
		hdrTemplate.smcBootAddr = 0x100000;
		imgEnd = 0x8000;
		hdrTemplate.kvSize = xb.type - 8 < 2 ? 0x800000 : 0x400000;
		hdrTemplate.cfOffset = cf;
		hdrTemplate.sysUpdateAddr = cf;
		switch (xb.flags & 7) {
		case 1:
		case 2:
			copyright[10] = '5';
			hdrTemplate.kvSize = 0;
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
			hdrTemplate.smcBootAddr = 0x800;
			hdrTemplate.smcBootSize = 0x3800;
			break;
		}
	}
	if (xb.type > 5) {
		copyright[9] = '1';
		hdrTemplate.qfe = 0x80;
		copyright[10] = '0';
		hdrTemplate.patchSlotSize = xb.bigBlock ? 0x200 : 0x100;
	} else if (!checkZeros(xb.cpuKey, 16) && !xb.cfLdv) {
		log_printf(0, "***** WARNING: cfldv was not set anywhere, setting it to 1\n");
		if (xb.type != 2)
			log_printf(0, "      please set it in ini or on command line and rebuild!\n");
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
	if (xb.bl.data)
		free(xb.bl.data);
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
	log_printf(1, "flash header build version set to v.%d\n", SWAP16(*p));
}

u32 smcSetLoad(u32 size)
{
	u32 *h = (u32 *)xb.hdr;

	if (size > 0x3800) {
		log_printf(0, "\n***** ERROR: SMC size 0x%x not supported!!!\n\n", size);
		return 0;
	}
	h[30] = SWAP32(size);
	h[31] = SWAP32(0x4000 - size);
	log_printf(1, "reset smc load address to 0x%x size 0x%x\n", SWAP32(h[31]), SWAP32(h[30]));
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
	log_printf(1, "patch slot offset reset to: 0x%x\n", SWAP32(v));
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

/* copy len bytes to the image at off and set the spare bytes of its pages
   (LBA; per type the page count, length, ...) and the FS table chain.
   gcc's ipa-cp clones of it are the image's imgWriteStart (off 0, type 0,
   pad 1: imgAdd.constprop.1), imgWritePage (len 0x1000, type 1, pad 0:
   .constprop.2) and imgWriteAt (type 0, pad 1: .constprop.4), emitted
   in that order; imgAddFile's and writeFsTable's calls inline clones */
int imgAdd(u32 off, const void *src, u32 len, u8 type, u16 next, int pad)
{
	u32 x, first, rem, tail, blocks, start, p, end, npages, pages;
	int left;
	u8 t;
	u32 pg;
	u8 sp9, *s;
	int partial;
	u32 b;
	u32 i;

	if (xb.rawSize < off || xb.rawSize < off + len) {
		return -1;
	}
	x = off & 0x3fff;
	start = (off - x) >> 14;
	first = x ? 0x4000 - x : 0;
	if (len <= first) {
		blocks = 1;
		tail = len;
	} else {
		rem = len - first;
		if (rem < 0x4000)
			tail = rem;
		else
			tail = rem % 0x4000;
		blocks = rem / 0x4000;
		if (tail) {
			blocks++;
		}
		if (x) {
			blocks++;
		}
	}
	if (x > first + 0x4000)
		blocks += 2;
	memcpy(xb.hdr + off, src, len);
	if (pad == 1) if (tail)
		memset(xb.hdr + off + len, 0, ((off + len + 0x3fff) & ~0x3fff) - (off + len));
#define BLK (start + b)
	for (b = 0; b < blocks; b++) {
		/* dead (VRP1 removes them): they raise the off-0 ipa-cp value (imgWriteStart
		   clone; `first + ...` is computed in the loop) and set which SSA names get
		   recycled (compare operand orders in the clones and inlined copies); so
		   do the ones before memcpy, in the FS loop and before imgEnd.  None may
		   modify len or off: ipa-cp then can't specialise on them */
		if (x > first + 0x4000)
			__asm__("");
		if (x + 0x4000 < first)
			blocks++;
		if ((len & 0x3fff) > 0x3fff)
			__asm__("");
		t = type - '1';
		partial = type != 0 && type != '0' && len < 0x4000;
		if (len % 512)
			npages = (len + 512) / 512;
		else
			npages = len / 512;
		if (!partial)
			npages = 32;
		else {
			/* imgAddFile's clone: keeps DOM2's threading from zeroing the npages guard edge */
			lnp2: __attribute__((hot));
		}
		p = 0;
		if (t < 15) {
			/* no code: the slot order of t and partial (dead in every clone) */
			__asm__("" :: "g"(t));
			p = xb.bigBlock ? off & 0x1ffff : off & 0x3fff;
			if (p) p /= 512;
		}
		for (end = p + npages; p < end; p++) {
			s = xb.spare + (BLK * 32 + p) * 16;
			/* pages here and left in the big arm: lim2 then hoists left
			   after len >> 8 and the type tests, as in the original */
			pages = len / 512;
			if (len % 512)
				pages++;
			memset(s, 0, 16);
			if (xb.bigBlock) {
				((struct spb *)s)->b2lo = BLK >> 8;
				((struct spb *)s)->b0 = 0xff;
				s[1] = BLK;
				if (type > 1) {
					s[12] = (s[12] & 0xc0) | (type & 0x3f);
					if (type != 0x2a && type != 0x2c) {
						left = pages;
						if (left & 3)
							left = (left + 4) & ~3;
						s[9] = (((off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256) - left) >> 2;
						s[5] = 1;
						s[8] = len >> 8;
						s[7] = len;
					} else {
						if (type == 0x2c)
							s[5] = 1;
						s[9] = xb.spare9;
						s[8] = xb.spare8;
						s[7] = xb.spare7;
					}
				}
			} else {
				((struct sps *)s)->b1lo = BLK >> 8;
				((struct sps *)s)->b5 = 0xff;
				s[0] = BLK;
				if (type > 1) {
					s[12] = (s[12] & 0xc0) | (type & 0x3f);
					s[9] = 32 - pages;
					s[2] = 1;
					if (type != '0') {
						s[8] = len >> 8;
						s[7] = len;
					}
				}
			}
		}
	}
#undef BLK
	if (next != 0xf1f1) {
		
		for (i = 0; i < blocks; i++) {
			if (x > first + 0x4000)
				blocks++;
			if (next != 0 && next != 0xffff) {
				fsTable[start - xb.fsStart + i] = SWAP16(next);
			} else {
				fsTable[start - xb.fsStart + i] = SWAP16(start - xb.fsStart + i + 1);
			}
		}
		if (x + 0x4000 < first)
			start++;
		if (next == 0xffff) {
			fsTable[start + blocks - 1 - xb.fsStart] = SWAP16(0x1fff);
		}
	}
	if ((len & 0x3fff) > 0x3fff)
		blocks += 2;
	imgEnd = off + len;
	return 0;
}

int imgFits(u32 off, u32 len)
{
	return (xb.fsEnd - 1) * 0x4000 >= off + len;
}

void imgAddFile(const char *name, const void *data, const u32 *time, u32 len)
{
	u32 off = imgSizeAligned();
	u32 start, b, p, pages, npages, first, rem, tail, blocks;
	u16 blk;
	u8 *s;
	/* imgFits by hand, its limit and end before the dead len++: VRP1's
	   threading of the two dead tests copies the block after len++ (which
	   gives the original's head registers), so names defined there are
	   renumbered high.  lim (one use, expanded at the test) and end (kept
	   by the code-free asm; DOM2 makes the inlined imgAdd's off + len this
	   one) keep low numbers: `lim < end` and the range test's `end > raw`
	   then come out in the original's operand order */
	u32 lim = (xb.fsEnd - 1) * 0x4000;
	u32 end = off + len;

	__asm__("" :: "g"(end));
	if ((len & 0x3fff) > 0x3fff)
		len++;
	if (__builtin_expect(lim >= off + len, 1)) {
		/* dead; cold, so the threading that removes it doesn't leave the
		   error edge at 75% (the error block is then laid out after the
		   big-block path) */
		if ((len & 0x3fff) > 0x3fff) {
			c1: __attribute__((cold));
			name++;
		}
		fsFiles[nFsFiles].block = SWAP16((u16)(off >> 14) - xb.fsStart);
		fsFiles[nFsFiles].size = SWAP32(len);
		strcpy(fsFiles[nFsFiles].name, name);
		fsFiles[nFsFiles].time = *time;
		if (!xb.bigBlock)
			imgAdd(off, data, len, 0, 0xffff, 1);
		else
			imgAdd(off, data, len, 0x2a, 0xffff, 1);
		nFsFiles++;
	} else {
		log_printf(0, "\n******* ERROR: adding %s will exceed available flash space! Skipped!\n\n", name);
	}
}

void imgAddFileAs(const char *name, const void *data, const u32 *time, u32 len)
{
	u32 off = imgSizeAligned();

	log_printf(1, "\tadding as %s at raw offset 0x%x len 0x%08x (end 0x%08x)\n", name, off, len, off + len);
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
			log_printf(0, "\n******* ERROR: adding Mobile%c.dat will exceed available flash space! Skipped!\n\n",
				type + 17);
			return 0;
		}
		log_printf(1, "\tadding Mobile%c.dat as type 0x%x at raw offset 0x%x len 0x%x (end 0x%x)\n",
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
		log_printf(1, "\tadding Mobile%c.dat as type 0x%x at raw offset 0x%x len 0x%x (end 0x%x)\n",
			type + 17, type, off, len, off + len);
		ret = mobileOffset >> 14;
		imgAdd(mobileOffset, data, len, type, 0x1ffe, 0);
		return ret;
	}
	log_printf(0, "\n******* ERROR: adding Mobile%c.dat will exceed available flash space! Skipped!\n\n",
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
	log_printf(1, "adding smc config to offset 0x%08x, len 0x%x\n", xb.smcConfigOffset, len);
	if (xb.bigBlock)
		return imgAdd(xb.smcConfigOffset, smcPage, 0x1000, 1, 0xf1f1, 0);
	return imgAdd(xb.smcConfigOffset, smcPage, 0x1000, 1, 0x1ffb, 0);
}

void writeInitialHeader(void)
{
	if (xb.bigBlock)
		imgWriteHdr(&hdrTemplate, sizeof(hdrTemplate));
	else
		imgAdd(0, &hdrTemplate, sizeof(hdrTemplate), 0, 0x1ffb, 1);
	if (xb.netKd.data && xb.netKd.size) {
		log_printf(1, "Inserting netKd data from dump into header\n");
		if (xb.bigBlock)
			imgAdd(0x80, xb.netKd.data, xb.netKd.size, 0, 0xf1f1, 1);
		else
			imgAdd(0x80, xb.netKd.data, xb.netKd.size, 0, 0x1ffb, 1);
	}
}

long checkBootImage(int write)
{
	struct flashhdr *h = (struct flashhdr *)xb.bl.data;
	struct blhdr *b;
	u32 off, size;
	u16 magic, build;

	off = (SWAP32(h->kvAddr) + SWAP32(h->kvSize) + 15) & ~15;
	b = (struct blhdr *)(xb.bl.data + off);
	magic = SWAP16(b->magic);
	build = SWAP16(b->build);
	size = SWAP32(b->size);
	log_printf(1, "%c%c v%d at 0x%x size 0x%x (CB)\n", magic >> 8, magic & 0xff, build, off, size);
	if ((magic & 0x43ff) != 0x4342)
		return -1;
	off = (off + size + 15) & ~15;
	if (SWAP16(b->flags) & 0x800) {
		b = (struct blhdr *)(xb.bl.data + off);
		magic = SWAP16(b->magic);
		build = SWAP16(b->build);
	build = SWAP16(b->build);
		size = SWAP32(b->size);
		log_printf(1, "%c%c v%d at 0x%x size 0x%x (dual CB)\n", magic >> 8, magic & 0xff, build, off, size);
		if ((magic & 0x43ff) != 0x4342)
			return -1;
		off = (off + size + 15) & ~15;
	} else if (magic & 0x1000) {
		b = (struct blhdr *)(xb.bl.data + off);
		magic = SWAP16(b->magic);
		build = SWAP16(b->build);
	build = SWAP16(b->build);
		size = SWAP32(b->size);
		log_printf(1, "%c%c v%d at 0x%x size 0x%x (devkit CC)\n", magic >> 8, magic & 0xff, build, off, size);
		if ((magic & 0x43ff) != 0x4343)
			return -1;
		off = (off + size + 15) & ~15;
	}
	b = (struct blhdr *)(xb.bl.data + off);
	magic = SWAP16(b->magic);
	build = SWAP16(b->build);
	size = SWAP32(b->size);
	log_printf(1, "%c%c v%d at 0x%x size 0x%x (CD)\n", magic >> 8, magic & 0xff, build, off, size);
	if ((magic & 0x43ff) != 0x4344)
		return -1;
	off = (off + size + 15) & ~15;
	b = (struct blhdr *)(xb.bl.data + off);
	magic = SWAP16(b->magic);
	build = SWAP16(b->build);
	log_printf(1, "%c%c v%d at 0x%x size 0x%x (CE)\n", magic >> 8, magic & 0xff, build, off, SWAP32(b->size));
	if ((magic & 0x43ff) != 0x4345)
		return -1;
	xb.bl.size = (off + SWAP32(b->size) + 15) & ~15;
	log_printf(1, "final truncated bootloader size 0x%x\n", xb.bl.size);
	if (write) {
		if (xb.bigBlock)
			imgAdd(0, xb.bl.data, xb.bl.size, 0, 0xf1f1, 1);
		else
			imgAdd(0, xb.bl.data, xb.bl.size, 0, 0x1ffb, 1);
	}
	return 0;
}

__attribute__((optimize("no-tree-scev-cprop"))) void writeFsTable(u32 off)
{
	u8 *buf, *p;
	u32 blk;
	int i;

	blk = off >> 14;
	if (xb.bigBlock && (off & 0x1ffff)) {
		off = (off + 0x20000) & ~0x1ffff;
		blk = off >> 14;
	}
	fsTable[blk - xb.fsStart] = SWAP16(0x1ffd);
	buf = malloc(0x4000);
	p = buf;
	for (i = 0; i < 16; i++) {
		memcpy(p, (u8 *)fsTable + i * 0x200, 0x200);
		p += 0x200;
		memcpy(p, (u8 *)fsFiles + i * 0x200, 0x200);
		p += 0x200;
	}
	log_printf(1, "offset 0x%x len 0x4000 (end 0x%x)...", off, off + 0x4000);
	if (!xb.bigBlock)
		goto small;
	imgAdd(off, buf, i * 0x400, 0x2c, 0x1ffe, 0);
	goto done;
small:
	imgAdd(off, buf, i * 0x400, 0x30, 0x1ffd, 0);
done:
	setBeU16(blk, (u8 *)xb.mmcAnchor + 0x1c);
	setBeU16(0, (u8 *)xb.mmcAnchor + 0x1e);
	free(buf);
}

void copyAnchorBlock(int n)
{
	u32 off = n != 1 ? 0x2fec000 : 0x2fe8000;

	log_printf(1, "copying anchor block %d to offset 0x%x\n", n, off);
	memset(xb.hdr + off, 0, 0x1000);
	memcpy(xb.hdr + off, xb.mmcAnchor, sizeof(xb.mmcAnchor));
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

	log_printf(1, "\n------ writing image to disk ------\n");
	f = fopen(name, "wb");
	if (!f)
		return -2;
	log_printf(1, "writing file '%s' to disk...", name);
	if (xb.flags & 0x10000000) {
		if (fwrite(xb.hdr, 0x3000000, 1, f) != 1) {
			log_printf(1, "failed!\n");
			log_printf(0, "\n***** ERROR: was not able to write %d bytes to the file %s!\n", 0x3000000, name);
			fclose(f);
			return 1;
		}
		if (xb.sha1Write) {
			u8 hash[20];

			log_printf(1, "done!\ncreating SHA-1 hash from system area data...");
			XeCryptSha(xb.hdr, 0x3000000, 0, 0, 0, 0, hash, 20);
			log_printf(1, "done!\nwriting SHA-1 to file...");
			writeSha1File(xb.sha1File, name, hash);
		}
	} else {
		XECRYPT_SHA_STATE sha;
		u8 hash[20];

		if (fwrite(xb.raw, xb.blocks * 0x4200, 1, f) != 1) {
			log_printf(1, "failed!\n");
			log_printf(0, "\n***** ERROR: was not able to write %d bytes to the file %s!\n", xb.blocks * 0x4200, name);
			fclose(f);
			return 1;
		}
		if (xb.sha1Write) {
			log_printf(1, "done!\ncreating SHA-1 hash from system area data...");
			XeCryptShaInit(&sha);
			XeCryptShaUpdate(&sha, xb.raw, xb.blocks * 0x4200);
		}
		if (xb.nandMu && (xb.bootFlags & 0x10000000)) {
			if (xb.sha1Write) {
				log_printf(1, "done!\nchecking and copying > 64M NAND data from dump file if present and updating SHA-1...\n");
				xb.nandMu = copyMuData(f, &sha);
			} else {
				log_printf(1, "done!\nchecking and copying > 64M NAND data from dump file if present...\n");
				xb.nandMu = copyMuData(f, 0);
			}
		}
		if (xb.sha1Write) {
			XeCryptShaFinal(&sha, hash, 20);
			log_printf(1, "done!\nwriting SHA-1 to file...");
			writeSha1File(xb.sha1File, name, hash);
		}
		free(xb.raw);
		xb.raw = 0;
	}
	log_printf(1, "done!\n");
	fclose(f);
	return 0;
}

int finalizeImage(void)
{
	u32 b, p, i, n;
	int size;
	int blocks;
	u8 *raw, *s, *spare;
	void *mem;

	if (xb.flags & 0x10000000)
		return 0;
	xb.raw = (u8 *)(mem = xmalloc(xb.rawSize));
	if (!mem)
		return -1;
	if (xb.bigBlock) {
		log_printf(1, "fixing up big block LBA numbers in spare...");
		n = xb.blocks / 8;
		spare = xb.spare;
		for (b = 0; b < n; b++)
			for (p = 0; p < 256; p++) {
				s = spare + b * 0x1000 + p * 16;
				if (((struct sp *)s)->b2lo == 0xf && s[1] == 0xff)
					continue;
				s[1] = b;
				((struct sp *)s)->b2lo = b >> 8;
			}
		log_printf(1, "done!\n");
	} else if (xb.bbController) {
		log_printf(1, "fixing up big block controller on small block NAND LBA numbers...");
		for (i = 0; i < xb.blocks * 32; i++) {
			u8 t;

			if (!spareUsed(xb.spare + i * 16))
				continue;
			t = xb.spare[i * 16];
			xb.spare[i * 16] = xb.spare[i * 16 + 2];
			xb.spare[i * 16 + 2] = xb.spare[i * 16 + 1];
			xb.spare[i * 16 + 1] = t;
		}
		log_printf(1, "done!\n");
	}
	log_printf(1, "calculating ECD bytes and assembling raw image...");
	raw = (u8 *)mem;
	for (b = 0; b < xb.blocks; b++)
		for (p = 0; p < 32; p++) {
			if (!pageErased(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16))
				calcPageEcc(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16);
			__asm__("" :: "a"(xb.hdr));
			memcpy(raw, xb.hdr + (b * 32 + p) * 512, 512);
			memcpy(raw + 512, xb.spare + (b * 32 + p) * 16, 16);
			raw += 528;
		}
	log_printf(1, "done!\n");
	if (xb.nandMu && (xb.bootFlags & 0x10000000)) {
		log_printf(1, "attempting to restore NAND MU data to big block unit from dump...");
		raw = xb.raw + xb.spare7 * 0x21000;
		for (b = xb.spare7; b < xb.muBlocks; b++)
			for (p = 0; p < 256; p++) {
				memcpy(raw, xb.dump + b * 0x20000 + p * 512, 512);
				memcpy(raw + 512, xb.dumpSpare + b * 0x1000 + p * 16, 16);
				raw += 528;
			}
		log_printf(1, "done!\n");
	}
	if (xb.numBad - 1 < 32) {
		/* the arms in this order (and the error last below): gcc emits the
		   string literals in statement order, which is the image's .rdata
		   order; the code is the same either way */
		if (xb.bigBlock == xb.dumpBigBlock || xb.mode == 2) {
			log_printf(1, "remapping %d blocks\n", xb.numBad);
			if (xb.bigBlock) {
				size = 0x21000;
				blocks = 0x200;
			} else {
				size = 0x4200;
				blocks = xb.type == 6 || xb.type == 8 ? 0x1000 : 0x400;
			}
			for (i = 0; i < xb.numBad; i++) {
				u32 from = xb.badBlocks[i];

				if (from < blocks && xb.badRemap[i] < blocks) {
					u32 src = size * from, dst = size * xb.badRemap[i];

					log_printf(1, "    copying 0x%x bytes of LBA 0x%x to block 0x%x...", size, from, xb.badRemap[i]);
					memcpy(xb.raw + dst, xb.raw + src, size);
					log_printf(1, "zero fill origin...");
					memset(xb.raw + src, 0, size);
					if (blockErased(xb.raw + dst, xb.bigBlock)) {
						log_printf(1, "\n        dest block is empty, fixing up LBA and ECD...");
						setBlockSpare(xb.raw + dst, xb.badBlocks[i], xb.bigBlock);
					}
					log_printf(1, "done!\n");
				} else if (xb.badRemap[i] != 0xfffffffb)
					log_printf(1, "\n\n***** ERROR: Remapping block 0x%x to block 0x%x is not sane on a NAND with 0x%x blocks!\n",
						from, xb.badRemap[i], blocks);
				else {
					u32 off = size * from;

					log_printf(1, "    Remapping block 0x%x is not required, zerofilling...", from);
					memset(xb.raw + off, 0, size);
					log_printf(1, "done!\n");
				}
			}
		} else
			log_printf(1, "\n\n***** ERROR: if you had given the same small/big block style NAND donor image I'd be remapping %d bad blocks now...\n",
				xb.numBad);
	}
	log_printf(1, "done remapping!\n");
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
	log_printf(1, "\tadding %s at raw offset 0x%x len 0x%x (end 0x%x)\n", name, off, len, off + len);
	if (xb.bigBlock)
		return imgAdd(off, data, 0x1000, 1, 0xf1f1, 0);
	return imgAdd(off, data, 0x1000, 1, 0x1ffb, 0);
}

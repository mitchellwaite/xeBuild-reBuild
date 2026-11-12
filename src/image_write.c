/* image_write: flash layout (header, CB/CE, SMC config, Mobile*.dat, the
   FS table), spare (LBA, ECD) bytes, writing the image to disk.
   Built as one C object (no .s): gcc's default top-level order emits
   the functions as the original (imgAdd's ipa-cp clones first), and the
   string literals and jump table in .rdata in its order */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "crypto/xecrypt.h"
#include "xebuild.h"
#include "build.h"
#include "fileutil.h"
#include "image_read.h"
#include "image_write.h"
#include "log.h"

/* a bootloader's header */
struct blhdr
{
	uint16_t magic;
	uint16_t build;
	uint16_t qfe;
	uint16_t flags;
	uint32_t entry;
	uint32_t size;
};

struct spb
{ uint8_t b0; uint8_t b1; uint8_t b2lo:4, b2hi:4; uint8_t b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15; };
struct sps
{ uint8_t b0; uint8_t b1lo:4, b1hi:4; uint8_t b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15; };
struct sp
{ uint8_t b0; uint8_t b1lo:4, b1hi:4; uint8_t b2lo:4, b2hi:4; uint8_t b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15; };
struct spt
{ uint8_t b[12]; uint8_t type:6, ecc3:2; };
struct spare
{
	uint8_t b[16];
};

int pageErased(const uint8_t *data, const uint8_t *spare);

/* the year's last digit is a NUL in the image: buildImage sets it per
   console type */
char copyright[0x40] = "\xa9 2004-200\0 Microsoft Corporation. All rights reserved.";

/* initialised, so .bss rather than COMMON; gcc emits them in reverse
   order of definition */
int nFsFiles = 0;
uint32_t mobileOffset = 0;
static uint8_t smcPage[0x1000];

int buildImage(void)
{
	uint32_t rawSize, spareSize, userSize, cf;
	int bigBlock;
	uint8_t *spare, *hdr;

	if (xb.type == BUILD_RETAIL)
	{
		xb.files[findFile(FILE_CF)].offset = xb.files[findFile(FILE_XELL)].offset;
	}
	if (xb.flags & NAND_BIG_BLOCK)
	{
		xb.blocks = NAND_SIZE_64M / NAND_BLOCK;
		xb.smcConfigOffset = SMCCFG_OFFSET_BB;
		xb.bigBlock = 1;
		xb.spare9 = 4;
		xb.spare7 = 0x10;
		if (xb.flags & NAND_BIG_FFS)
		{
			xb.fsStart = 0x2e0;
			xb.fsEnd = 0xee0;
			userSize = NAND_SIZE_64M;
			xb.spare8 = 0x60;
			xb.muBlocks = 0x5c;
		}
		else
		{
			xb.fsStart = 0xae0;
			xb.fsEnd = 0xee0;
			userSize = NAND_SIZE_64M;
			xb.spare8 = 0x20;
			xb.muBlocks = 0x15c;
		}
		spareSize = NAND_RAW_64M - NAND_SIZE_64M;
		bigBlock = 1;
		rawSize = NAND_RAW_64M;
	}
	else if (xb.type != BUILD_DEVKIT && xb.type != BUILD_TESTKIT)
	{
		if (xb.flags & NAND_MMC)
		{
			xb.blocks = NAND_SIZE_MMC / NAND_BLOCK;
			xb.smcConfigOffset = SMCCFG_OFFSET_MMC;
			userSize = NAND_SIZE_MMC;
			xb.fsStart = 0;
			xb.fsEnd = 0xbfa;
			spareSize = 0x180000;	/* as if it had spare bytes */
			rawSize = 0x3180000;
		}
		else
		{
			xb.blocks = NAND_SIZE_16M / NAND_BLOCK;
			xb.smcConfigOffset = SMCCFG_OFFSET_16M;
			userSize = NAND_SIZE_16M;
			xb.fsStart = 0;
			xb.fsEnd = 0x3dc;
			spareSize = NAND_RAW_16M - NAND_SIZE_16M;
			rawSize = NAND_RAW_16M;
		}
		xb.bigBlock = 0;
		bigBlock = 0;
	}
	else
	{
		xb.blocks = NAND_SIZE_64M / NAND_BLOCK;
		xb.smcConfigOffset = SMCCFG_OFFSET_64M;
		userSize = NAND_SIZE_64M;
		xb.bigBlock = 0;
		xb.fsStart = 0;
		spareSize = NAND_RAW_64M - NAND_SIZE_64M;
		xb.fsEnd = 0xf7c;
		bigBlock = 0;
		rawSize = NAND_RAW_64M;
	}
	xb.rawSize = rawSize;
	xb.spareSize = spareSize;
	xb.spare = spare = malloc(spareSize);
	xb.userSize = userSize;
	xb.hdr = hdr = malloc(userSize);
	if (!hdr)
	{
		return -1;
	}
	if (!spare)
	{
		return -1;
	}
	memset(spare, 0xff, spareSize);
	memset(hdr, 0xff, userSize);
	memset(fsFileEnts, 0, sizeof(fsFileEnts));
	memset(fsChain, 0, sizeof(fsChain));
	memset(&flashHdr, 0, sizeof(flashHdr));
	flashHdr.magic = SWAP16_IMAGE_WRITE(FLASH_MAGIC);
	flashHdr.build = SWAP16_IMAGE_WRITE(FLASH_BUILD);
	memset(xb.mmcAnchor, 0, sizeof(xb.mmcAnchor));

	// Stock XeBuild doesn't set the patch slot size for
	// a bunch of image types, which results in issues
	// especially for glitch2m and DevGL. J-Runner sets
	// it to 0x10000 if it's unset in the header as a
	// workaround, so we're setting this as the default
	#ifdef XEBUILD_FIXES
		flashHdr.patchSlotSize = SWAP32_IMAGE_WRITE(FLASH_PATCH_SLOT);
	#endif

	if (xb.type != BUILD_JTAG)
	{
		/* xb.type - BUILD_TESTKIT < 2: BUILD_TESTKIT or BUILD_TESTKIT16 */
		flashHdr.cbOffset = xb.type - BUILD_TESTKIT < 2 ? SWAP32_IMAGE_WRITE(FLASH_CB_OFFSET_TESTKIT)
			: SWAP32_IMAGE_WRITE(FLASH_CB_OFFSET);
		cf = SWAP32_IMAGE_WRITE((uint32_t)findFileOffset(FILE_CF));
		flashHdr.sysUpdateCount = SWAP16_IMAGE_WRITE(FLASH_SU_COUNT);
		flashHdr.kvVersion = SWAP16_IMAGE_WRITE(FLASH_KV_VERSION);
		flashHdr.kvAddr = SWAP32_IMAGE_WRITE(FLASH_KV_ADDR);
		flashHdr.smcBootSize = SWAP32_IMAGE_WRITE(SMC_SIZE);
		flashHdr.smcBootAddr = SWAP32_IMAGE_WRITE(FLASH_SMC_ADDR);
		imgUsed = FLASH_CB_OFFSET;
		flashHdr.kvSize = xb.type - BUILD_TESTKIT < 2 ? SWAP32_IMAGE_WRITE(2 * KV_SIZE)
			: SWAP32_IMAGE_WRITE(KV_SIZE);
		flashHdr.cfOffset = cf;
		flashHdr.sysUpdateAddr = cf;
		switch (xb.flags & CONSOLE_MASK)
		{
		case CONSOLE_XENON:
		case CONSOLE_ZEPHYR:
			copyright[10] = '5';

			// Stock XeBuild resets the KV size to 0 which causes
			// issues with XeLL and other apps. Don't know why it
			// does this other than that retail images might have
			// it unset from the factory. For the fixed build,
			// don't do this reset.
			#ifndef XEBUILD_FIXES
				flashHdr.kvSize = 0;
			#endif

			break;
		case CONSOLE_FALCON:
			copyright[10] = '7';
			break;
		case CONSOLE_JASPER:
			if (xb.flags & NAND_BB_CONTROLLER)
			{
				xb.bbController = 1;
				flashHdr.patchSlotSize = SWAP32_IMAGE_WRITE(FLASH_PATCH_SLOT);
			}
			if (xb.bigBlock)
			{
				flashHdr.patchSlotSize = SWAP32_IMAGE_WRITE(FLASH_PATCH_SLOT_BB);
			}
			copyright[10] = '9';
			break;
		case CONSOLE_TRINITY:
			xb.bbController = 1;
			flashHdr.patchSlotSize = SWAP32_IMAGE_WRITE(FLASH_PATCH_SLOT);
			copyright[9] = '1';
			copyright[10] = '0';
			break;
		case CONSOLE_CORONA:
		case CONSOLE_WINCHESTER:
			xb.bbController = 1;
			flashHdr.patchSlotSize = SWAP32_IMAGE_WRITE(FLASH_PATCH_SLOT);
			copyright[9] = '1';
			copyright[10] = '0';
			/* not byte swapped (0x80000 and 0x380000 as read): the SMC is
			   0x3800 bytes at 0x800, which smcSetLoad sets when it loads it */
			flashHdr.smcBootAddr = 0x800;
			flashHdr.smcBootSize = 0x3800;
			break;
		}
	}
	else
	{
		flashHdr.cbOffset = SWAP32_IMAGE_WRITE(FLASH_CB_OFFSET);
		flashHdr.cfOffset = SWAP32_IMAGE_WRITE(FLASH_JTAG_CF);
		flashHdr.kvSize = SWAP32_IMAGE_WRITE(KV_SIZE);
		flashHdr.sysUpdateAddr = SWAP32_IMAGE_WRITE(FLASH_JTAG_CF);
		flashHdr.sysUpdateCount = SWAP16_IMAGE_WRITE(FLASH_SU_COUNT);
		flashHdr.kvVersion = SWAP16_IMAGE_WRITE(FLASH_KV_VERSION);
		flashHdr.kvAddr = SWAP32_IMAGE_WRITE(FLASH_KV_ADDR);
		flashHdr.smcBootSize = SWAP32_IMAGE_WRITE(SMC_SIZE);
		flashHdr.smcBootAddr = SWAP32_IMAGE_WRITE(FLASH_SMC_ADDR);
		imgUsed = FLASH_CB_OFFSET;
		if ((xb.flags & CONSOLE_MASK) == CONSOLE_JASPER)
		{
			if (xb.flags & NAND_BB_CONTROLLER)
			{
				xb.bbController = 1;
				flashHdr.patchSlotSize = SWAP32_IMAGE_WRITE(FLASH_PATCH_SLOT);
			}
			if (bigBlock)
			{
				flashHdr.patchSlotSize = SWAP32_IMAGE_WRITE(FLASH_PATCH_SLOT);
			}
			copyright[10] = '8';
		}
		else if ((xb.flags & CONSOLE_MASK) == CONSOLE_XENON ||
			   (xb.flags & CONSOLE_MASK) == CONSOLE_ZEPHYR)
		{
			copyright[10] = '5';

			// Stock XeBuild resets the KV size to 0 which causes
			// issues with XeLL and other apps. Don't know why it
			// does this other than that retail images might have
			// it unset from the factory. For the fixed build,
			// don't do this reset.
			#ifndef XEBUILD_FIXES
				flashHdr.kvSize = 0;
			#endif
		}
		else
		{
			copyright[10] = '7';
		}
	}
	if (xb.type > BUILD_DEVGL16)
	{
		copyright[9] = '1';
		flashHdr.qfe = SWAP16_IMAGE_WRITE(0x8000);
		copyright[10] = '0';
		flashHdr.patchSlotSize = xb.bigBlock ? SWAP32_IMAGE_WRITE(FLASH_PATCH_SLOT_BB)
			: SWAP32_IMAGE_WRITE(FLASH_PATCH_SLOT);
	}
	else if (!checkZeros(xb.cpuKey, 16) && !xb.cfLdv)
	{
		log_printf(0, "***** WARNING: cfldv was not set anywhere, setting it to 1\n");
		if (xb.type != BUILD_JTAG)
		{
			log_printf(0, "      please set it in ini or on command line and rebuild!\n");
		}
		xb.cfLdv = 1;
	}
	memcpy(flashHdr.copyright, copyright, sizeof(copyright));
	if (xb.type != BUILD_RETAIL)
	{
		xb.hdr[HDR_BLMOD_SIZE] = 0;
		xb.hdr[HDR_BLMOD_SIZE + 1] = 0;
	}
	return buildFlash();
}

void imageFree(void)
{
	if (xb.spare)
	{
		free(xb.spare);
	}
	if (xb.hdr)
	{
		free(xb.hdr);
	}
	if (xb.raw)
	{
		free(xb.raw);
	}
	if (xb.bl.data)
	{
		free(xb.bl.data);
	}
}

/* the ECD: an LFSR over a page's 0x1000 data bits and the first 0x66 bits of
   its spare bytes */
#define ECD_POLY 0x6954559
#define ECD_DATA_BITS 0x1000
#define ECD_BITS 0x1066

/* the 26-bit ECD of a page: its 512 data bytes and 12 spare bytes */
uint32_t calcEcd(uint8_t *datc, uint8_t *spare)
{
	unsigned int i = 0, val = 0;
	unsigned int v = 0;
	unsigned int *data = (unsigned int *)datc;
	for (i = 0; i < ECD_BITS; i++)
	{
		if (!(i & 31))
		{
			if (i == ECD_DATA_BITS)
			{
				data = (unsigned int *)spare;
			}
			v = ~*data++;
		}
		val ^= v & 1;
		v >>= 1;
		if (val & 1)
		{
			val ^= ECD_POLY;
		}
		val >>= 1;
	}
	return ~val;
}

void calcPageEcc(uint8_t *data, uint8_t *spare)
{
	uint32_t val = calcEcd((uint8_t *)data, spare);

	spare[12] = (spare[12] & 0x3f) + (val << 6);
	spare[13] = val >> 2;
	spare[14] = val >> 10;
	spare[15] = val >> 18;
}

int pageEccOk(uint8_t *datc, uint8_t *spare)
{
	unsigned int i = 0, val = 0;
	unsigned int v = 0;
	unsigned int *data = (unsigned int *)datc;

	for (i = 0; i < ECD_BITS; i++)
	{
		if (!(i & 31))
		{
			if (i == ECD_DATA_BITS)
			{
				data = (unsigned int *)spare;
			}
			v = ~*data++;
		}
		val ^= v & 1;
		v >>= 1;
		if (val & 1)
		{
			val ^= ECD_POLY;
		}
		val >>= 1;
	}
	val = ~val;
	if ((spare[12] & 0xC0) != ((val << 6) & 0xFF))
	{
		return 0;
	}
	if (spare[13] != ((val >> 2) & 0xFF))
	{
		return 0;
	}
	if (spare[14] != ((val >> 10) & 0xFF))
	{
		return 0;
	}
	if (spare[15] != ((val >> 18) & 0xFF))
	{
		return 0;
	}
	return 1;
}

/* a raw block (data and spare interleaved) */
int blockEccOk(uint8_t *blk, int bigBlock)
{
	int i, pages = bigBlock ? NAND_BB_PAGES : NAND_BLOCK_PAGES;

	for (i = 0; i < pages; i++)
	{
		if (pageErased(blk + i * NAND_RAW_PAGE, blk + i * NAND_RAW_PAGE + NAND_PAGE))
		{
			continue;
		}
		if (pageEccOk(blk + i * NAND_RAW_PAGE, blk + i * NAND_RAW_PAGE + NAND_PAGE))
		{
			continue;
		}
		return 0;
	}
	return 1;
}

int pageErased(const uint8_t *data, const uint8_t *spare)
{
	int i;

	for (i = 0; i < NAND_PAGE; i++)
	{
		if (data[i] != 0xff)
		{
			return 0;
		}
	}
	for (i = 0; i < NAND_SPARE; i++)
	{
		if (spare[i] != 0xff)
		{
			return 0;
		}
	}
	return 1;
}

int blockErased(uint8_t *blk, int bigBlock)
{
	return isErased(blk, (bigBlock ? NAND_BB_PAGES : NAND_BLOCK_PAGES) * NAND_RAW_PAGE);
}

int blockPagesErased(uint8_t *data, uint8_t *spare, int bigBlock)
{
	int i, pages = bigBlock ? NAND_BB_PAGES : NAND_BLOCK_PAGES;

	for (i = 0; i < pages; i++)
	{
		if (!pageErased(data + i * NAND_PAGE, spare + i * NAND_SPARE))
		{
			return 0;
		}
	}
	return 1;
}

int blockIsFF(const uint8_t *p)
{
	int i;

	for (i = 0; i < NAND_BLOCK; i++)
	{
		if (p[i] != 0xff)
		{
			return 0;
		}
	}
	return 1;
}

int isErased(const uint8_t *p, uint32_t len)
{
	uint32_t i;

	for (i = 0; i < len; i++)
	{
		if (p[i] != 0xff)
		{
			return 0;
		}
	}
	return 1;
}

/* LBA and ECD of each page of a raw block */
void setBlockSpare(uint8_t *blk, uint32_t lba, int bigBlock)
{
	int i, pages = bigBlock ? NAND_BB_PAGES : NAND_BLOCK_PAGES;

	for (i = 0; i < pages; i++)
	{
		struct sp *s = (struct sp *)(blk + i * NAND_RAW_PAGE + NAND_PAGE);

		memset(s, 0, NAND_SPARE);
		if (bigBlock)
		{
			s->b2lo = lba >> 8;
			s->b0 = 0xff;
			*((uint8_t *)s + 1) = lba;
		}
		else if (xb.bbController)
		{
			s->b2lo = lba >> 8;
			s->b5 = 0xff;
			*((uint8_t *)s + 1) = lba;
		}
		else
		{
			s->b1lo = lba >> 8;
			s->b5 = 0xff;
			s->b0 = lba;
		}
		calcPageEcc(blk + i * NAND_RAW_PAGE, (uint8_t *)s);
	}
}

uint32_t imgSizeAligned(void)
{
	uint32_t r = imgUsed % NAND_BLOCK;

	return r ? imgUsed + NAND_BLOCK - r : imgUsed;
}

void setFlashBuild(uint16_t build)
{
	uint16_t *p = (uint16_t *)(xb.hdr + 2);

	*p = SWAP16_IMAGE_WRITE(build);
	log_printf(1, "flash header build version set to v.%d\n", SWAP16_IMAGE_WRITE(*p));
}

uint32_t smcSetLoad(uint32_t size)
{
	uint32_t *h = (uint32_t *)xb.hdr;

	if (size > SMC_SIZE_CORONA)
	{
		log_printf(0, "\n***** ERROR: SMC size 0x%x not supported!!!\n\n", size);
		return 0;
	}
	h[30] = SWAP32_IMAGE_WRITE(size);
	h[31] = SWAP32_IMAGE_WRITE(FLASH_KV_ADDR - size);
	log_printf(1, "reset smc load address to 0x%x size 0x%x\n", SWAP32_IMAGE_WRITE(h[31]), SWAP32_IMAGE_WRITE(h[30]));
	return FLASH_KV_ADDR - size;
}

uint32_t imgSmcOffset(void)
{
	return ((uint32_t *)xb.hdr)[31];
}

uint32_t setPatchSlot(uint32_t off)
{
	uint32_t *h = (uint32_t *)xb.hdr;
	uint32_t v;

	if (!off)
	{
		off = imgUsed;
	}
	if (xb.bigBlock)
	{
		off = (off + NAND_BB_MASK) & ~NAND_BB_MASK;
		if (xb.type == BUILD_RETAIL)
		{
			uint32_t cf = SWAP32_IMAGE_WRITE(h[28]);

			xb.spare7 = (off + (cf ? cf * 2 : 2 * FLASH_PATCH_SLOT)) >> NAND_BB_SHIFT;
		}
	}
	else
	{
		off = (off + NAND_BLOCK_MASK) & ~NAND_BLOCK_MASK;
	}
	v = SWAP32_IMAGE_WRITE(off);
	h[25] = v;
	h[3] = v;
	log_printf(1, "patch slot offset reset to: 0x%x\n", SWAP32_IMAGE_WRITE(v));
	return off;
}

uint32_t imgCfOffset(void)
{
	uint32_t *h = (uint32_t *)xb.hdr;

	return SWAP32_IMAGE_WRITE(h[25]);
}

uint32_t imgCfSize(void)
{
	uint32_t *h = (uint32_t *)xb.hdr;
	uint32_t v = SWAP32_IMAGE_WRITE(h[28]);

	return v ? v : FLASH_PATCH_SLOT;
}

uint32_t imgSize(void)
{
	return imgUsed;
}

uint32_t imgSetSize(uint32_t size)
{
	return imgUsed = size;
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
int imgAdd(uint32_t off, const void *src, uint32_t len, uint8_t type, uint16_t next, int pad)
{
	uint32_t x, first, rem, tail, blocks, start, p, end, npages, pages;
	int left;
	uint8_t t;
	uint8_t sp9, *s;
	int partial;
	_Bool small;
	uint32_t b;
	uint32_t i;

	if (xb.rawSize < off || xb.rawSize < off + len)
	{
		return -1;
	}
	x = off & NAND_BLOCK_MASK;
	start = (off - x) >> NAND_BLOCK_SHIFT;
	first = x ? NAND_BLOCK - x : 0;
	if (len <= first)
	{
		blocks = 1;
		tail = len;
	}
	else
	{
		rem = len - first;
		if (rem < NAND_BLOCK)
		{
			tail = rem;
		}
		else
		{
			tail = rem % NAND_BLOCK;
		}
		blocks = rem / NAND_BLOCK;
		if (tail)
		{
			blocks++;
		}
		if (x)
		{
			blocks++;
		}
	}
	memcpy(xb.hdr + off, src, len);
	if (pad == 1)
	{
		if (tail)
		{
			memset(xb.hdr + off + len, 0, ((off + len + NAND_BLOCK_MASK) & ~NAND_BLOCK_MASK) - (off + len));
		}
	}
#define BLK (start + b)
	for (b = 0; b < blocks; b++)
	{
		small = type != 0 && type != SPARE_FS_ROOT;
		partial = len < NAND_BLOCK;
		npages = NAND_BLOCK_PAGES;
		if (partial > 0)
		{
			if (small)
			{
				if (len % NAND_PAGE)
				{
					npages = (len + NAND_PAGE) / NAND_PAGE;
				}
				else
				{
					npages = len / NAND_PAGE;
				}
			}
		}
		p = 0;
		t = type - SPARE_MOBILE_B;
		if (t < 15)
		{
			p = xb.bigBlock ? off & NAND_BB_MASK : off & NAND_BLOCK_MASK;
			if (p)
			{
				p /= NAND_PAGE;
			}
		}
		for (end = p + npages; p < end; p++)
		{
			s = xb.spare + (start * NAND_BLOCK_PAGES + p + b * NAND_BLOCK_PAGES) * NAND_SPARE;
			memset(s, 0, NAND_SPARE);
			if (xb.bigBlock)
			{
				((struct spb *)s)->b2lo = (start + b) >> 8;
				((struct spb *)s)->b0 = 0xff;
				s[1] = BLK;
				if (type > 1)
				{
					((struct spt *)s)->type = type;
					if (type != SPARE_FILE_BB && type != SPARE_FS_ROOT_BB)
					{
						pages = len >> NAND_PAGE_SHIFT;
						if (len & (NAND_PAGE - 1))
						{
							pages++;
						}
						if (off & NAND_BB_MASK)
						{
							int used[2] = { (off & NAND_BB_MASK) / NAND_PAGE, 0 };
							int k;

							left = NAND_BB_PAGES;
							for (k = 0; k < 2; k++)
							{
								left -= used[k];
							}
						}
						else
						{
							left = NAND_BB_PAGES;
						}
						if ((int)pages & 3)
						{
							pages = ((int)pages + 4) & ~3;
						}
						s[9] = (left - pages) >> 2;
						s[5] = 1;
						s[8] = len >> 8;
						s[7] = len;
					}
					else
					{
						if (type == SPARE_FS_ROOT_BB)
						{
							s[5] = 1;
						}
						s[9] = xb.spare9;
						s[8] = xb.spare8;
						s[7] = xb.spare7;
					}
				}
			}
			else
			{
				pages = len % NAND_PAGE ? len / NAND_PAGE + 1 : len / NAND_PAGE;
				((struct sps *)s)->b1lo = BLK >> 8;
				((struct sps *)s)->b5 = 0xff;
				s[0] = BLK;
				if (type > 1)
				{
					((struct spt *)s)->type = type;
					s[9] = NAND_BLOCK_PAGES - pages;
					s[2] = 1;
					if (type != SPARE_FS_ROOT)
					{
						s[8] = len >> 8;
						s[7] = len;
					}
				}
			}
		}
	}
#undef BLK
	if (next != IMG_NO_CHAIN)
	{

		for (i = 0; i < blocks; i++)
		{
			if (next != 0 && next != IMG_CHAIN)
			{
				fsChain[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(next);
			}
			else
			{
				fsChain[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(start + i - xb.fsStart + 1);
			}
		}
		if (next == IMG_CHAIN)
		{
			fsChain[start - xb.fsStart + blocks - 1] = SWAP16_IMAGE_WRITE(FS_CHAIN_END);
		}
	}
	imgUsed = off + len;
	return 0;
}

/* an `if`, not `return a >= b`: gcc 6 has no early phiopt, so the PHI of 1 and 0
   survives early inlining, which gives its callers their branch probabilities
   and the threading of the head block */
int imgFits(uint32_t off, uint32_t len)
{
	if ((xb.fsEnd - 1) * NAND_BLOCK >= off + len)
	{
		return 1;
	}
	return 0;
}

void imgAddFile(const char *name, const void *data, const uint32_t *time, uint32_t len)
{
	uint32_t off = imgSizeAligned();

	if (imgFits(off, len))
	{
		fsFileEnts[nFsFiles].block = SWAP16_IMAGE_WRITE((uint16_t)(off >> NAND_BLOCK_SHIFT) - xb.fsStart);
		fsFileEnts[nFsFiles].size = SWAP32_IMAGE_WRITE(len);
		strcpy(fsFileEnts[nFsFiles].name, name);
		fsFileEnts[nFsFiles].time = *time;
		if (!xb.bigBlock)
		{
			imgAdd(off, data, len, 0, IMG_CHAIN, 1);
		}
		else
		{
			imgAdd(off, data, len, SPARE_FILE_BB, IMG_CHAIN, 1);
		}
		nFsFiles++;
	}
	else
	{
		log_printf(0, "\n******* ERROR: adding %s will exceed available flash space! Skipped!\n\n", name);
	}
}

void imgAddFileAs(const char *name, const void *data, const uint32_t *time, uint32_t len)
{
	uint32_t off = imgSizeAligned();

	log_printf(1, "\tadding as %s at raw offset 0x%x len 0x%08x (end 0x%08x)\n", name, off, len, off + len);
	imgAddFile(name, data, time, len);
}

uint32_t imgAddMobile(const void *data, uint32_t len, uint8_t type)
{
	uint32_t off, end, ret;

	if (xb.bigBlock)
	{
		if (!mobileOffset)
		{
			mobileOffset = imgSizeAligned();
			if (mobileOffset & NAND_BB_MASK)
			{
				mobileOffset = (mobileOffset + NAND_BB_BLOCK) & ~NAND_BB_MASK;
			}
		}
		else if ((mobileOffset & ~NAND_BB_MASK) + NAND_BB_BLOCK < mobileOffset + len)
		{
			mobileOffset = (mobileOffset + NAND_BB_BLOCK) & ~NAND_BB_MASK;
		}
		off = mobileOffset;
		if (imgFits(off, len))
		{
			log_printf(1, "\tadding Mobile%c.dat as type 0x%x at raw offset 0x%x len 0x%x (end 0x%x)\n",
				type + 17, type, off, len, off + len);
			imgAdd(mobileOffset, data, len, type, FS_CHAIN_FREE, 0);
			ret = mobileOffset >> NAND_BB_SHIFT;
			mobileOffset += len;
			if (mobileOffset & 0x7ff)
			{
				mobileOffset = (mobileOffset + 0x800) & ~0x7ff;
			}
			return ret;
		}
		log_printf(0, "\n******* ERROR: adding Mobile%c.dat will exceed available flash space! Skipped!\n\n",
			type + 17);
		return 0;
	}
	mobileOffset = off = imgSizeAligned();
	if (imgFits(off, len))
	{
		log_printf(1, "\tadding Mobile%c.dat as type 0x%x at raw offset 0x%x len 0x%x (end 0x%x)\n",
			type + 17, type, off, len, off + len);
		ret = mobileOffset >> NAND_BLOCK_SHIFT;
		imgAdd(mobileOffset, data, len, type, FS_CHAIN_FREE, 0);
		return ret;
	}
	log_printf(0, "\n******* ERROR: adding Mobile%c.dat will exceed available flash space! Skipped!\n\n",
		type + 17);
	return 0;
}

void fixupFsTable(uint32_t off)
{
	uint32_t i;

	for (i = 0; i < off >> NAND_BLOCK_SHIFT; i++)
	{
		if (fsChain[i - xb.fsStart] != SWAP16_IMAGE_WRITE(FS_CHAIN_RESERVED))
		{
			fsChain[i - xb.fsStart] = SWAP16_IMAGE_WRITE(FS_CHAIN_RESERVED);
		}
	}
}

void fixupEmptyFsBlocks(uint32_t off)
{
	uint32_t b, i, n;

	for (b = off >> NAND_BLOCK_SHIFT; b < xb.fsEnd; b++)
	{
		fsChain[b - xb.fsStart] = SWAP16_IMAGE_WRITE(FS_CHAIN_FREE);
	}
	if (!xb.bigBlock)
	{
		n = (xb.flags & NAND_MMC) ? 6 : 4;
		if (xb.type > BUILD_DEVGL16)
		{
			n = xb.blocks - xb.fsEnd;
		}
		for (i = 0; i < n; i++)
		{
			fsChain[xb.fsEnd + i] = SWAP16_IMAGE_WRITE(FS_CHAIN_RESERVED);
		}
	}
	if (xb.type == BUILD_JTAG)
	{
		xb.spare[26] = 3;
		xb.spare[27] = 0x50;
	}
}

int addSmcConfig(const uint8_t *cfg, uint32_t len)
{
	memset(smcPage, 0xff, sizeof(smcPage));
	memcpy(smcPage, cfg, SMCCFG_SIZE);
	log_printf(1, "adding smc config to offset 0x%08x, len 0x%x\n", xb.smcConfigOffset, len);
	if (xb.bigBlock)
	{
		return imgAdd(xb.smcConfigOffset, smcPage, sizeof(smcPage), 1, IMG_NO_CHAIN, 0);
	}
	return imgAdd(xb.smcConfigOffset, smcPage, sizeof(smcPage), 1, FS_CHAIN_RESERVED, 0);
}

void writeInitialHeader(void)
{
	if (xb.bigBlock)
	{
		imgAdd(0, &flashHdr, sizeof(flashHdr), 0, IMG_NO_CHAIN, 1);
	}
	else
	{
		imgAdd(0, &flashHdr, sizeof(flashHdr), 0, FS_CHAIN_RESERVED, 1);
	}
	if (xb.netKd.data && xb.netKd.size)
	{
		log_printf(1, "Inserting netKd data from dump into header\n");
		if (xb.bigBlock)
		{
			imgAdd(FLASH_NETKD, xb.netKd.data, xb.netKd.size, 0, IMG_NO_CHAIN, 1);
		}
		else
		{
			imgAdd(FLASH_NETKD, xb.netKd.data, xb.netKd.size, 0, FS_CHAIN_RESERVED, 1);
		}
	}
}

long checkBootImage(int write)
{
	struct flashhdr *h = (struct flashhdr *)xb.bl.data;
	struct blhdr *b;
	uint32_t off, size;
	uint16_t magic, build;

	off = (SWAP32_IMAGE_WRITE(h->kvAddr) + SWAP32_IMAGE_WRITE(h->kvSize) + 15) & ~15;
	b = (struct blhdr *)(xb.bl.data + off);
	magic = SWAP16_IMAGE_WRITE(b->magic);
	build = SWAP16_IMAGE_WRITE(b->build);
	size = SWAP32_IMAGE_WRITE(b->size);
	log_printf(1, "%c%c v%d at 0x%x size 0x%x (CB)\n", magic >> 8, magic & 0xff, build, off, size);
	if ((magic & BL_MAGIC_MASK) != BL_MAGIC_CB)
	{
		return -1;
	}
	off = (off + size + 15) & ~15;
	if (SWAP16_IMAGE_WRITE(b->flags) & BL_FLAG_CB_B)
	{
		b = (struct blhdr *)(xb.bl.data + off);
		magic = SWAP16_IMAGE_WRITE(b->magic);
		build = SWAP16_IMAGE_WRITE(b->build);
		size = SWAP32_IMAGE_WRITE(b->size);
		log_printf(1, "%c%c v%d at 0x%x size 0x%x (dual CB)\n", magic >> 8, magic & 0xff, build, off, size);
		if ((magic & BL_MAGIC_MASK) != BL_MAGIC_CB)
		{
			return -1;
		}
		off = (off + size + 15) & ~15;
	}
	else if (magic & BL_MAGIC_KIT)
	{
		b = (struct blhdr *)(xb.bl.data + off);
		magic = SWAP16_IMAGE_WRITE(b->magic);
		build = SWAP16_IMAGE_WRITE(b->build);
		size = SWAP32_IMAGE_WRITE(b->size);
		log_printf(1, "%c%c v%d at 0x%x size 0x%x (devkit CC)\n", magic >> 8, magic & 0xff, build, off, size);
		if ((magic & BL_MAGIC_MASK) != BL_MAGIC_CC)
		{
			return -1;
		}
		off = (off + size + 15) & ~15;
	}
	b = (struct blhdr *)(xb.bl.data + off);
	magic = SWAP16_IMAGE_WRITE(b->magic);
	build = SWAP16_IMAGE_WRITE(b->build);
	size = SWAP32_IMAGE_WRITE(b->size);
	log_printf(1, "%c%c v%d at 0x%x size 0x%x (CD)\n", magic >> 8, magic & 0xff, build, off, size);
	if ((magic & BL_MAGIC_MASK) != BL_MAGIC_CD)
	{
		return -1;
	}
	off = (off + size + 15) & ~15;
	b = (struct blhdr *)(xb.bl.data + off);
	magic = SWAP16_IMAGE_WRITE(b->magic);
	build = SWAP16_IMAGE_WRITE(b->build);
	log_printf(1, "%c%c v%d at 0x%x size 0x%x (CE)\n", magic >> 8, magic & 0xff, build, off, SWAP32_IMAGE_WRITE(b->size));
	if ((magic & BL_MAGIC_MASK) != BL_MAGIC_CE)
	{
		return -1;
	}
	xb.bl.size = (off + SWAP32_IMAGE_WRITE(b->size) + 15) & ~15;
	log_printf(1, "final truncated bootloader size 0x%x\n", xb.bl.size);
	if (write)
	{
		if (xb.bigBlock)
		{
			imgAdd(0, xb.bl.data, xb.bl.size, 0, IMG_NO_CHAIN, 1);
		}
		else
		{
			imgAdd(0, xb.bl.data, xb.bl.size, 0, FS_CHAIN_RESERVED, 1);
		}
	}
	return 0;
}

void writeFsTable(uint32_t off)
{
	uint8_t *buf, *p;
	uint32_t blk;
	int i;
	uint32_t len;

	blk = off >> NAND_BLOCK_SHIFT;
	if (xb.bigBlock && (off & NAND_BB_MASK))
	{
		off = (off + NAND_BB_BLOCK) & ~NAND_BB_MASK;
		blk = off >> NAND_BLOCK_SHIFT;
	}
	fsChain[blk - xb.fsStart] = SWAP16_IMAGE_WRITE(FS_CHAIN_ROOT);
	buf = malloc(NAND_BLOCK);
	p = buf;
	for (i = 0; i < 16; i++)
	{
		memcpy(p, (uint8_t *)fsChain + i * 0x200, 0x200);
		p += 0x200;
		memcpy(p, (uint8_t *)fsFileEnts + i * 0x200, 0x200);
		p += 0x200;
	}
	log_printf(1, "offset 0x%x len 0x4000 (end 0x%x)...", off, off + 0x4000);
	len = i * 0x400;
	if (!xb.bigBlock)
	{
		goto small;
	}
	imgAdd(off, buf, len, SPARE_FS_ROOT_BB, FS_CHAIN_FREE, 0);
	goto done;
small:
	imgAdd(off, buf, len, SPARE_FS_ROOT, FS_CHAIN_ROOT, 0);
done:
	setBeU16(blk, (uint8_t *)&xb.fsBlock);
	setBeU16(0, (uint8_t *)&xb.fsReserved);
	free(buf);
}

void copyAnchorBlock(int n)
{
	uint32_t off = n != 1 ? MMC_ANCHOR1 : MMC_ANCHOR0;

	log_printf(1, "copying anchor block %d to offset 0x%x\n", n, off);
	memset(xb.hdr + off, 0, 0x1000);
	memcpy(xb.hdr + off, xb.mmcAnchor, sizeof(xb.mmcAnchor));
}

int spareUsed(const uint8_t *s)
{
	int i;

	for (i = 0; i < NAND_SPARE; i++)
	{
		if (s[i] != 0xff)
		{
			return 1;
		}
	}
	return 0;
}

uint8_t *imageGetBuffer(uint32_t *size)
{
	if (xb.flags & NAND_MMC)
	{
		*size = NAND_SIZE_MMC;
		return xb.hdr;
	}
	*size = xb.blocks * NAND_RAW_BLOCK;
	return xb.raw;
}

int writeImage(char *name)
{
	FILE *f;

	log_printf(1, "\n------ writing image to disk ------\n");
	f = fopen(name, "wb");
	if (!f)
	{
		return -2;
	}
	log_printf(1, "writing file '%s' to disk...", name);
	if (xb.flags & NAND_MMC)
	{
		if (fwrite(xb.hdr, NAND_SIZE_MMC, 1, f) != 1)
		{
			log_printf(1, "failed!\n");
			log_printf(0, "\n***** ERROR: was not able to write %d bytes to the file %s!\n", NAND_SIZE_MMC, name);
			fclose(f);
			return 1;
		}
		if (xb.sha1Write)
		{
			uint8_t hash[20];

			log_printf(1, "done!\ncreating SHA-1 hash from system area data...");
			XeCryptSha(xb.hdr, NAND_SIZE_MMC, 0, 0, 0, 0, hash, 20);
			log_printf(1, "done!\nwriting SHA-1 to file...");
			writeSha1File(xb.sha1File, name, hash);
		}
	}
	else
	{
		XECRYPT_SHA_STATE sha;
		uint8_t hash[20];

		if (fwrite(xb.raw, xb.blocks * NAND_RAW_BLOCK, 1, f) != 1)
		{
			log_printf(1, "failed!\n");
			log_printf(0, "\n***** ERROR: was not able to write %d bytes to the file %s!\n", xb.blocks * NAND_RAW_BLOCK, name);
			fclose(f);
			return 1;
		}
		if (xb.sha1Write)
		{
			log_printf(1, "done!\ncreating SHA-1 hash from system area data...");
			XeCryptShaInit(&sha);
			XeCryptShaUpdate(&sha, xb.raw, xb.blocks * NAND_RAW_BLOCK);
		}
		if (xb.nandMu && (xb.optFlags & OPT_NANDMU))
		{
			if (xb.sha1Write)
			{
				log_printf(1, "done!\nchecking and copying > 64M NAND data from dump file if present and updating SHA-1...\n");
				xb.nandMu = copyMuData(f, &sha);
			}
			else
			{
				log_printf(1, "done!\nchecking and copying > 64M NAND data from dump file if present...\n");
				xb.nandMu = copyMuData(f, 0);
			}
		}
		if (xb.sha1Write)
		{
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
	uint32_t b, p, i, n;
	int size;
	int blocks;
	uint8_t *raw, *s, *spare;
	void *mem;

	if (xb.flags & NAND_MMC)
	{
		return 0;
	}
	xb.raw = (uint8_t *)(mem = malloc(xb.rawSize));
	if (!mem)
	{
		return -1;
	}
	if (xb.bigBlock)
	{
		log_printf(1, "fixing up big block LBA numbers in spare...");
		n = xb.blocks / (NAND_BB_BLOCK / NAND_BLOCK);
		spare = xb.spare;
		for (b = 0; b < n; b++)
		{
			for (p = 0; p < NAND_BB_PAGES; p++)
			{
				s = spare + b * (NAND_BB_PAGES * NAND_SPARE) + p * NAND_SPARE;
				if (((struct sp *)s)->b2lo == 0xf && s[1] == 0xff)
				{
					continue;
				}
				s[1] = b;
				((struct sp *)s)->b2lo = b >> 8;
			}
		}
		log_printf(1, "done!\n");
	}
	else if (xb.bbController)
	{
		log_printf(1, "fixing up big block controller on small block NAND LBA numbers...");
		for (i = 0; i < xb.blocks * NAND_BLOCK_PAGES; i++)
		{
			uint8_t t;

			if (!spareUsed(xb.spare + i * NAND_SPARE))
			{
				continue;
			}
			t = xb.spare[i * NAND_SPARE];
			xb.spare[i * NAND_SPARE] = xb.spare[i * NAND_SPARE + 2];
			xb.spare[i * NAND_SPARE + 2] = xb.spare[i * NAND_SPARE + 1];
			xb.spare[i * NAND_SPARE + 1] = t;
		}
		log_printf(1, "done!\n");
	}
	log_printf(1, "calculating ECD bytes and assembling raw image...");
	raw = (uint8_t *)mem;
	for (b = 0; b < xb.blocks; b++)
	{
		for (p = 0; p < NAND_BLOCK_PAGES; p++)
		{
			const uint8_t *q = xb.spare;
			uint8_t *h = xb.hdr;

			if (pageErased(h + (b * NAND_BLOCK_PAGES + p) * NAND_PAGE, q + (b * NAND_BLOCK_PAGES + p) * NAND_SPARE) <= 0)
			{
				uint32_t val;

				s = xb.spare + (b * NAND_BLOCK_PAGES + p) * NAND_SPARE;
				val = calcEcd(h + (b * NAND_BLOCK_PAGES + p) * NAND_PAGE, s);
				s[12] = (s[12] & 0x3f) + (val << 6);
				s[13] = val >> 2;
				s[14] = val >> 10;
				s[15] = val >> 18;
				q = xb.spare;
				h = xb.hdr;
			}
			/* a loop over the page's parts, not two memcpys: raw's step is unknown
			   to ccp1 and ccp2 until cunrolli unrolls this, and forwprop2 then leaves
			   it as &MEM[raw + 528], so no pass sets ALIGN on raw (tree dumps, checked
			   with iw22align.py) and the 512-byte memcpy gets its alignment prologue */
			{
				static const uint32_t partSize[2] = { NAND_PAGE, NAND_SPARE };
				const uint8_t *from[2] = { h + (b * NAND_BLOCK_PAGES + p) * NAND_PAGE, q + (b * NAND_BLOCK_PAGES + p) * NAND_SPARE };
				int k;

				for (k = 0; k < 2; k++)
				{
					memcpy(raw, from[k], partSize[k]);
					raw += partSize[k];
				}
			}
		}
	}
	log_printf(1, "done!\n");
	if (xb.nandMu && (xb.optFlags & OPT_NANDMU))
	{
		log_printf(1, "attempting to restore NAND MU data to big block unit from dump...");
		raw = xb.raw + xb.spare7 * NAND_RAW_BB_BLOCK;
		for (b = xb.spare7; b < xb.muBlocks; b++)
		{
			for (p = 0; p < NAND_BB_PAGES; p++)
			{
				memcpy(raw, xb.dump + b * NAND_BB_BLOCK + p * NAND_PAGE, NAND_PAGE);
				memcpy(raw + NAND_PAGE, xb.dumpSpare + b * (NAND_BB_PAGES * NAND_SPARE) + p * NAND_SPARE, NAND_SPARE);
				raw += NAND_RAW_PAGE;
			}
		}
		log_printf(1, "done!\n");
	}
	if (xb.numBad - 1 < 32)
	{
		/* the arms in this order (and the error last below): gcc emits the
		   string literals in statement order, which is the image's .rdata
		   order; the code is the same either way */
		if (xb.bigBlock == xb.dumpBigBlock || xb.mode == MODE_UPDATE)
		{
			log_printf(1, "remapping %d blocks\n", xb.numBad);
			if (xb.bigBlock)
			{
				size = NAND_RAW_BB_BLOCK;
				blocks = NAND_SIZE_64M / NAND_BB_BLOCK;
			}
			else
			{
				size = NAND_RAW_BLOCK;
				blocks = xb.type == BUILD_DEVKIT || xb.type == BUILD_TESTKIT ? NAND_SIZE_64M / NAND_BLOCK : NAND_SIZE_16M / NAND_BLOCK;
			}
			for (i = 0; i < xb.numBad; i++)
			{
				uint32_t from = xb.badBlocks[i];

				if (from < blocks && xb.badRemap[i] < blocks)
				{
					uint32_t src = size * from, dst = size * xb.badRemap[i];

					log_printf(1, "    copying 0x%x bytes of LBA 0x%x to block 0x%x...", size, from, xb.badRemap[i]);
					memcpy(xb.raw + dst, xb.raw + src, size);
					log_printf(1, "zero fill origin...");
					memset(xb.raw + src, 0, size);
					if (blockErased(xb.raw + dst, xb.bigBlock))
					{
						log_printf(1, "\n        dest block is empty, fixing up LBA and ECD...");
						setBlockSpare(xb.raw + dst, xb.badBlocks[i], xb.bigBlock);
					}
					log_printf(1, "done!\n");
				}
				else if (xb.badRemap[i] != REMAP_NONE)
				{
					log_printf(1, "\n\n***** ERROR: Remapping block 0x%x to block 0x%x is not sane on a NAND with 0x%x blocks!\n",
						from, xb.badRemap[i], blocks);
				}
				else
				{
					uint32_t off = size * from;

					log_printf(1, "    Remapping block 0x%x is not required, zerofilling...", from);
					memset(xb.raw + off, 0, size);
					log_printf(1, "done!\n");
				}
			}
		}
		else
		{
			log_printf(1, "\n\n***** ERROR: if you had given the same small/big block style NAND donor image I'd be remapping %d bad blocks now...\n",
				xb.numBad);
		}
	}
	log_printf(1, "done remapping!\n");
	return 0;
}

uint32_t fsStartBlock(void)
{
	return xb.fsStart;
}

uint32_t reservedAreaOffset(int bigBlock, int big, int mmc, uint32_t *page, uint32_t *sector, int n)
{
	uint32_t b, off;

	if (mmc)
	{
		b = n + 0xbff;
		off = b * 0x4000;
		if (page)
		{
			*page = b * 0x200;
		}
		if (sector)
		{
			*sector = b * 0x20;
		}
		return off;
	}
	if (bigBlock)
	{
		b = n + 0x1df;
		off = b * 0x20000;
		if (page)
		{
			*page = b * 0x1000;
		}
		if (sector)
		{
			*sector = b * 0x800;
		}
		return off;
	}
	if (big)
	{
		b = n + 0xf7f;
		off = b * 0x4000;
		if (page)
		{
			*page = b * 0x200;
		}
		if (sector)
		{
			*sector = b * 0x20;
		}
		return off;
	}
	b = n + 0x3df;
	off = b * 0x4000;
	if (page)
	{
		*page = b * 0x200;
	}
	if (sector)
	{
		*sector = b * 0x20;
	}
	return off;
}

uint32_t statisticsOffset(int bigBlock, int big, int mmc, uint32_t *page, uint32_t *sector)
{
	if (mmc)
	{
		if (page)
		{
			*page = 0x17fc00;
		}
		if (sector)
		{
			*sector = 0x17fc0;
		}
		return 0x2ff8000;
	}
	if (bigBlock)
	{
		if (page)
		{
			*page = 0x1de000;
		}
		if (sector)
		{
			*sector = 0xef000;
		}
		return 0x3bc0000;
	}
	if (big)
	{
		if (page)
		{
			*page = 0x1efc00;
		}
		if (sector)
		{
			*sector = 0x1efc0;
		}
		return 0x3df8000;
	}
	if (page)
	{
		*page = 0x7bc00;
	}
	if (sector)
	{
		*sector = 0x7bc0;
	}
	return 0xf78000;
}

uint32_t manufacturingOffset(int bigBlock, int big, int mmc, uint32_t *page, uint32_t *sector)
{
	if (mmc)
	{
		if (page)
		{
			*page = 0x17fa00;
		}
		if (sector)
		{
			*sector = 0x17fa0;
		}
		return 0x2ff4000;
	}
	if (bigBlock)
	{
		if (page)
		{
			*page = 0x1dd000;
		}
		if (sector)
		{
			*sector = 0xee800;
		}
		return 0x3ba0000;
	}
	if (big)
	{
		if (page)
		{
			*page = 0x1efa00;
		}
		if (sector)
		{
			*sector = 0x1efa0;
		}
		return 0x3df4000;
	}
	if (page)
	{
		*page = 0x7ba00;
	}
	if (sector)
	{
		*sector = 0x7ba0;
	}
	return 0xf74000;
}

void imgAddRaw(const char *name, const void *data, uint32_t len, uint32_t off)
{
	log_printf(1, "\tadding %s at raw offset 0x%x len 0x%x (end 0x%x)\n", name, off, len, off + len);
	if (xb.bigBlock)
	{
		imgAdd(off, data, RAWFILE_SIZE, 1, IMG_NO_CHAIN, 0);
	}
	else
	{
		imgAdd(off, data, RAWFILE_SIZE, 1, FS_CHAIN_RESERVED, 0);
	}
}

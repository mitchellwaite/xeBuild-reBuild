/* image_read: parsing an existing NAND image (nanddump.bin): sectors, pairing, LDV, smc.bin */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "../crypto/xecrypt.h"
#include "xebuild.h"
#include "bootloaders.h"
#include "fileutil.h"
#include "image_read.h"
#include "image_write.h"
#include "keys.h"
#include "log.h"
#include "main.h"
#include "smc.h"

/* TODO(prototype cast): shaSelfCheck returns int (bootloaders.c);
   findAnchor's code wants a uint32_t */
uint32_t shaSelfCheckU32(uint8_t *p) __asm__("_shaSelfCheck");

#define SWAP16(x) ((((x) << 8) & 0xff00) + ((x) >> 8))
#define ROT16(x) ((uint16_t)(((x) << 8) | ((x) >> 8)))
#define SWAP32(x) (((x) << 24) + (((x) << 8) & 0xff0000) + (((x) >> 8) & 0xff00) + ((x) >> 24))

struct fsroot {
	uint16_t map[0x1000];
	struct fsent ent[256];
};

/* mobile files found by the scan; 0 is the fs root */
struct mobile {
	int found;
	uint32_t version;
	uint32_t page;
	uint32_t len;
	uint32_t offset;
	uint32_t spare;
};

int fseeko64(FILE *f, long long off, int whence);

int fsFindFile(const char *name, uint32_t *block, uint32_t *size, uint32_t *time, int quiet);
/* not inlined into imgGetSecurityFiles in the original (growth 39 is under
   max-inline-insns-auto here; something made it 40+ there) */
int loadFlashFile(int i, uint32_t block) __attribute__((noinline));
int findAnchor(void);
int mmcFindMobiles(void);
uint32_t spareVersion(uint8_t *s);
void showMobilePages(void);
int scanMobiles(void);
void setFsOffset(void);
int findFsRoot(void);
void imgGetSecurityFiles(void);
void findSmcConfig(void);
int checkBlock(uint8_t *blk, int block, int numBlocks);
int addRemap(uint32_t block, int dest, int numBlocks);
int findFreeRemap(int numBlocks);
int notZeropair(void);
unsigned long spareLbaOk(int pages);
uint32_t copyMmcImage(uint8_t *raw);
unsigned long parseDump(uint8_t *raw);
int detectController(uint8_t *raw, int size);
int checkHeader(const char *name, FILE *fp);
void getNonces(void);

/* .bss and .data in the original's order */
static struct mobile mobiles[10];
static uint8_t anchor[0x200];
static uint32_t fsOffset;
static int fsValid;
static struct fsroot fsBuf;
static int dumpSize;
char zeropair[16] = "zeropair image";
char mobileName[] = "MobileA";
struct fsroot *fs = &fsBuf;

static const char ir_4521b8[] __attribute__((aligned(4))) = "%s found in sector 0x%x size 0x%x...";
static int fsFind(const char *name, uint32_t *block, uint32_t *size, uint32_t *time, int quiet)
{
	int i;

	for (i = 0; i < 256; i++) {
		if (fs->ent[i].name[0] && !stricmp(fs->ent[i].name, name)) {
			*size = SWAP32(fs->ent[i].size);
			*block = SWAP16(fs->ent[i].block);
			if (time)
				*time = SWAP32(fs->ent[i].time);
			if (!quiet)
				log_printf(1, ir_4521b8, name, *block, *size);
			return 1;
		}
	}
	return 0;
}

void buildCleanup(void)
{
	int i;

	dumpSize = 0;
	if (xb.dumpSpare)
		free(xb.dumpSpare);
	if (xb.dump)
		free(xb.dump);
	xb.numBad = 0;
	xb.dump = 0;
	xb.dumpSpare = 0;
	xb.nandMu = 0;
	xb.muChecked = 0;
	for (i = 0; i < sizeof(xb.mobile) / sizeof(xb.mobile[0]); i++)
		if (xb.mobile[i].data)
			free(xb.mobile[i].data);
	for (i = 0; i < 4; i++) {
		if ((&xb.smc)[i].data)
			free((&xb.smc)[i].data);
		(&xb.smc)[i].size = 0;
	}
	if (xb.netKd.data)
		free(xb.netKd.data);
}

static const char ir_4521e0[] __attribute__((aligned(4))) = "Did not find a LDV value to use, setting it to 0 for devkit!\n";
static const char ir_452220[] __attribute__((aligned(4))) = "Did not find a LDV value to use, setting it to 0 for testkit!\n";
static const char ir_452260[] __attribute__((aligned(4))) = "***** WARNING: could not find a non-zero CF LDV to use, setting it to 1 but that may be incorrect!\n";
static const char ir_4522c4[] __attribute__((aligned(1))) = "setting LDV from image to %d\n";
static const char ir_4522e4[] __attribute__((aligned(4))) = "setting pairing data from image to 0x%06x\n";
static const char ir_45230f[] __attribute__((aligned(1))) = "LDV was already set to %d\n";
void getImageLdv(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.dump;
	uint32_t size = SWAP32(h->patchSlotSize);
	uint32_t pairing;
	uint32_t ldv;

	if (!size)
		size = 0x10000;
	pairing = cfBestPairing(xb.dump + SWAP32(h->sysUpdateAddr), size);
	if (!pairing)
		pairing = cbGetPairing(xb.dump + SWAP32(h->kvAddr) + SWAP32(h->kvSize));
	if (pairing) {
		if (!xb.cfLdv)
			log_printf(1, ir_4522c4, pairing & 0xff);
		log_printf(1, ir_4522e4, pairing >> 8);
		setPairing(pairing >> 8);
		ldv = pairing;
	} else if (xb.type == 6 || xb.type == 7) {
		log_printf(1, ir_4521e0);
		ldv = 0;
	} else if (xb.type == 8 || xb.type == 9) {
		log_printf(1, ir_452220);
		ldv = 0;
	} else {
		log_printf(0, ir_452260);
		ldv = 1;
	}
	if (xb.cfLdv)
		log_printf(1, ir_45230f, xb.cfLdv);
	else if ((uint8_t)ldv > 32)
		xb.cfLdv = 32;
	else
		xb.cfLdv = ldv;
}

static const char ir_45232c[] __attribute__((aligned(4))) = "smc.bin should not be at 0x%x, trying 0x1000\n";
static const char ir_45235c[] __attribute__((aligned(4))) = "smc.bin should not be 0x%x bytes, using 0x3800\n";
static const char ir_45238c[] __attribute__((aligned(4))) = "smc.bin should not be 0x%x bytes, using 0x3000\n";
static const char ir_4523bc[] __attribute__((aligned(4))) = "decrypting SMC at address 0x%x of size 0x%x\n";
static const char ir_4523ec[] __attribute__((aligned(4))) = "SMC decrypted OK, will use if no external smc.bin is provided\n";
static const char ir_45242c[] __attribute__((aligned(4))) = "SMC did not decrypt, discarding it\n";
static const char ir_452450[] __attribute__((aligned(4))) = "Wasn't able to alloc 0x%x bytes memory for SMC bin, not using...\n";
static const char ir_452494[] __attribute__((aligned(4))) = "SMC at 0x%x of size 0x%x is not sane, skipping smc.bin in NAND image\n";
__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.dump;
	int addr = SWAP32(h->smcBootAddr);
	int size = SWAP32(h->smcBootSize);

	if (!addr)
		goto zero;
	else {
		vhot: __attribute__((hot));
	}
zback:
	if (addr != 0x800 && addr != 0x1000)
		goto bad;
bback:
	if (size != 0x3000 && size != 0x3800) {
		shot: __attribute__((hot));
		if (addr == 0x800) {
			size = 0x3800;
			log_printf(1, ir_45235c, size);
		} else {
			size = 0x3000;
			if (!h)
				__builtin_unreachable();
			log_printf(1, ir_45238c, size);
		}
	} else
		__asm__("" : "+D"(addr));
	if (__builtin_expect(addr < 528 * xb.dumpPages, 0)) {
		xb.smc.data = malloc(size);
		if (xb.smc.data) {
			xb.smc.size = size;
			memcpy(xb.smc.data, xb.dump + addr, size);
			log_printf(1, ir_4523bc, addr, size);
			if (unscramble(xb.smc.data, xb.smc.size)) {
				log_printf(1, ir_4523ec);
				setSmcKey(xb.smc.data);
			} else {
				log_printf(1, ir_45242c);
				free(xb.smc.data);
				xb.smc.data = 0;
				xb.smc.size = 0;
			}
		} else
			log_printf(1, ir_452450, size);
	} else {
		log_printf(1, ir_452494, addr, size);
	}
	if (0) {
zero:
		log_printf(1, ir_45232c, addr);
		addr = 0x1000;
		goto zback;
bad:
		bhot: __attribute__((hot));
		log_printf(1, ir_45232c, addr);
		addr = 0x1000;
		goto bback;
	}
}

static const char ir_4524dc[] __attribute__((aligned(4))) = "KeyVault cannot be at 0x0, trying 0x4000\n";
static const char ir_452508[] __attribute__((aligned(4))) = "KeyVault cannot be 0x%x bytes, using 0x4000\n";
static const char ir_452538[] __attribute__((aligned(4))) = "decrypting KeyVault at address 0x%x of size 0x%x\n";
static const char ir_45256c[] __attribute__((aligned(4))) = "keyvault decrypted OK, will use if no kv.bin is provided\n";
static const char ir_4525a8[] __attribute__((aligned(4))) = "keyvault decrypt failed, discarding\n";
static const char ir_4525d0[] __attribute__((aligned(4))) = "Wasn't able to alloc 0x4000 bytes memory for KeyVault bin, not using...\n";
static const char ir_45261c[] __attribute__((aligned(4))) = "KeyVault at address 0x%x of size 0x4000 is not sane, skipping KeyVault in NAND image\n";
static const char ir_452674[] __attribute__((aligned(4))) = "decrypting alt KeyVault at address 0x%x of size 0x%x\n";
static const char ir_4526ac[] __attribute__((aligned(4))) = "alt KeyVault decrypted OK, will use if no kv_alt.bin is provided\n";
static const char ir_4526f0[] __attribute__((aligned(4))) = "alt KeyVault decrypt failed, discarding\n";
static const char ir_45271c[] __attribute__((aligned(4))) = "Wasn't able to alloc 0x4000 bytes memory for alt KeyVault bin, not using...\n";
void getImageKv(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.dump;
	int addr = SWAP32(h->kvAddr);
	int size = SWAP32(h->kvSize);
	int ok = 0;

	if (!addr) {
		log_printf(1, ir_4524dc, addr);
		addr = 0x4000;
	}
	if (size != 0x4000 && size != 0x8000) {
		log_printf(1, ir_452508, size);
		size = 0x4000;
	}
	if (addr + size < 528 * xb.dumpPages) {
		xb.kv.data = malloc(0x4000);
		if (xb.kv.data) {
			log_printf(1, ir_452538, addr, 0x4000);
			xb.kv.size = 0x4000;
			memcpy(xb.kv.data, xb.dump + addr, 0x4000);
			ok = verifyExtended(xb.kv.data, xb.kv.size);
			if (ok) {
				log_printf(1, ir_45256c);
				setKvSalt(xb.kv.data + 16);
			} else {
				log_printf(1, ir_4525a8);
				free(xb.kv.data);
				xb.kv.data = 0;
				xb.kv.size = 0;
			}
		} else
			log_printf(1, ir_4525d0);
	} else
		log_printf(1, ir_45261c, addr);
	if (ok && size == 0x8000) {
		addr += 0x4000;
		xb.kvAlt.data = malloc(0x4000);
		if (xb.kvAlt.data) {
			log_printf(1, ir_452674, addr, 0x4000);
			xb.kvAlt.size = 0x4000;
			memcpy(xb.kvAlt.data, xb.dump + addr, 0x4000);
			if (verifyExtended(xb.kvAlt.data, xb.kvAlt.size)) {
				log_printf(1, ir_4526ac);
				setKvAltSalt(xb.kvAlt.data + 16);
			} else {
				log_printf(1, ir_4526f0);
				free(xb.kvAlt.data);
				xb.kvAlt.data = 0;
				xb.kvAlt.size = 0;
			}
		} else
			log_printf(1, ir_45271c);
	}
}

static const char ir_45276c[] __attribute__((aligned(4))) = "Unable to allocate memory for %s 0x%x bytes\n";
static const char ir_452799[] __attribute__((aligned(1))) = "%s.dat";
static const char ir_4527a0[] __attribute__((aligned(4))) = "extracting %s from page 0x%x (offset 0x%x), size %d (0x%x) bytes\n";
static const char ir_4527e4[] __attribute__((aligned(4))) = "Statistics.settings found at offset 0x%x, size %d (0x%x) bytes\n";
static const char ir_452824[] __attribute__((aligned(4))) = "Unable to allocate memory for Statistics.settings 0x%x bytes\n";
static const char ir_452864[] __attribute__((aligned(4))) = "Manufacturing.data found at offset 0x%x, size %d (0x%x) bytes\n";
static const char ir_4528a4[] __attribute__((aligned(4))) = "Unable to allocate memory for Manufacturing.data 0x%x bytes\n";
void getImageMobiles(void)
{
	int i;
	char name[30];
	uint32_t off, len;

	for (i = 0; i < 9; i++) {
		struct mobile *m = &mobiles[i + 1];

		if (!m->found)
			continue;
		xb.mobile[i].data = malloc(m->len);
		if (xb.mobile[i].data) {
			mobileName[6] = 'B' + i;
			sprintf(name, ir_452799, mobileName);
			log_printf(1, ir_4527a0,
				   name, m->page, m->offset, m->len, m->len);
			len = m->len;
			memcpy(xb.mobile[i].data, xb.dump + m->offset, len);
			xb.mobile[i].size = len;
		} else
			log_printf(1, ir_45276c, name, m->len);
	}
	off = statisticsOffset(xb.dumpBigBlock, 0, xb.dumpMmc, 0, 0);
	if (!isErased(xb.dump + off, 0x1000)) {
		log_printf(1, ir_4527e4, off, 0x1000, 0x1000);
		xb.mobile[9].data = malloc(0x1000);
		if (xb.mobile[9].data) {
			memcpy(xb.mobile[9].data, xb.dump + off, 0x1000);
			xb.mobile[9].size = 0x1000;
		} else
			log_printf(1, ir_452824, 0x1000);
	}
	off = manufacturingOffset(xb.dumpBigBlock, 0, xb.dumpMmc, 0, 0);
	if (!isErased(xb.dump + off, 0x1000)) {
		log_printf(1, ir_452864, off, 0x1000, 0x1000);
		xb.mobile[10].data = malloc(0x1000);
		if (!xb.mobile[10].data)
			log_printf(1, ir_4528a4, 0x1000);
		else {
			memcpy(xb.mobile[10].data, xb.dump + off, 0x1000);
			xb.mobile[10].size = 0x1000;
		}
	}
}

static const char ir_4528e1[] __attribute__((aligned(1))) = "netKd info found, size 0x%x\n";
static const char ir_4528fe[] __attribute__((aligned(1))) = "    version : 0x%x\n";
static const char ir_452912[] __attribute__((aligned(1))) = "    xbox IP : %d.%d.%d.%d\n";
static const char ir_452930[] __attribute__((aligned(4))) = "    xbox MAC: %02x:%02x:%02x:%02x:%02x\n";
static const char ir_452958[] __attribute__((aligned(1))) = "    port    : %d\n";
static const char ir_45296a[] __attribute__((aligned(1))) = "    host IP : %d.%d.%d.%d\n";
void getNetKd(void)
{
	uint8_t *img, *p;
	uint32_t ver;

	xb.netKd.data = 0;
	if (getBeU16(xb.dump + 0x80) != 0xca4a)
		return;
	img = xb.dump;
	p = img + 0x80;
	ver = getBeU32(img + 0x90);
	xb.netKd.size = getBeU32(xb.dump + 0x8c);
	log_printf(1, ir_4528e1, xb.netKd.size);
	log_printf(1, ir_4528fe, ver);
	if (ver == 1) {
		log_printf(1, ir_452912, img[0x94], img[0x95], img[0x96], img[0x97]);
		log_printf(1, ir_452930, img[0x98], img[0x99], img[0x9a], img[0x9b], img[0x9c], img[0x9d]);
		log_printf(1, ir_452958, getBeU16(img + 0x9e));
		log_printf(1, ir_45296a, img[0xa0], img[0xa1], img[0xa2], img[0xa3]);
	}
	xb.netKd.data = malloc(xb.netKd.size);
	if (xb.netKd.data)
		memcpy(xb.netKd.data, p, xb.netKd.size);
}

int loadFlashFile(int i, uint32_t block)
{
	uint32_t off = fsOffset + (block << 14);
	uint32_t left = xb.flashSize[i];
	uint32_t done = 0;

	xb.flashBuf[i] = calloc(left, 1);
	while (left > 0x4000) {
		memcpy(xb.flashBuf[i] + done, xb.dump + off, 0x4000);
		left -= 0x4000;
		done += 0x4000;
		block = SWAP16(fs->map[block]) & 0x1fff;
		off = fsOffset + (block << 14);
	}
	if (left)
		memcpy(xb.flashBuf[i] + done, xb.dump + off, left);
	return verifyFlashFile(i);
}

int fsFindFile(const char *name, uint32_t *block, uint32_t *size, uint32_t *time, int quiet)
{
	if (fsValid == 1)
		return fsFind(name, block, size, time, quiet);
	return 0;
}

static const char ir_452988[] __attribute__((aligned(4))) = "sector: 0x%04x offset: 0x%08x size: 0x%08x timestamp: 0x%08x name: %s\n";
void listFlashFiles(void)
{
	int i;

	if (fsValid != 1)
		return;
	for (i = 0; i < 256; i++) {
		struct fsent *e = &fs->ent[i];
		uint32_t block, size, time;
		uint16_t b16;

		if (!e->name[0])
			continue;
		/* this load order keeps e in ebp */
		b16 = e->block;
		size = e->size;
		block = SWAP16(b16);
		time = e->time;
		log_printf(1, ir_452988,
			   block, fsOffset + (block << 14), SWAP32(size), SWAP32(time), e->name);
	}
}

int fsGetFile(const char *name, uint8_t **buf, uint32_t *size, uint32_t *time)
{
	uint32_t block, len, t, off, left, done;
	uint8_t *p;
	int v = fsValid;

	/* code-free hint: fsValid (reused for return 1) in esi, name in edi */
	__asm__("" : : "S"(v));
	if (v != 1)
		return 0;
	if (!fsFind(name, &block, &len, &t, 1))
		return 0;
	off = fsOffset + (block << 14);
	p = calloc(len, 1);
	left = len;
	done = 0;
	while (left > 0x4000) {
		memcpy(p + done, xb.dump + off, 0x4000);
		left -= 0x4000;
		done += 0x4000;
		block = SWAP16(fs->map[block]) & 0x1fff;
		off = fsOffset + (block << 14);
	}
	if (left)
		memcpy(p + done, xb.dump + off, left);
	*buf = p;
	*size = len;
	*time = t;
	return 1;
}

static const char ir_4529d0[] __attribute__((aligned(4))) = "attempting to find valid anchor block\n";
static const char ir_4529f8[] __attribute__((aligned(4))) = "anchor block v %d at 0x2fe8000 is valid\n";
static const char ir_452a24[] __attribute__((aligned(4))) = "anchor block at 0x2fe8000 is invalid\n";
static const char ir_452a4c[] __attribute__((aligned(4))) = "anchor block v %d at 0x2fec000 is valid\n";
static const char ir_452a78[] __attribute__((aligned(4))) = "anchor block v %d at 0x2fec000 is selected\n";
static const char ir_452aa4[] __attribute__((aligned(4))) = "anchor block at 0x2fec000 is invalid\n";
static const char ir_452acc[] __attribute__((aligned(4))) = "anchor block v %d at 0x2fe8000 is selected\n";
int findAnchor(void)
{
	uint32_t v0, v1;
	uint32_t ok0, ok1;

	log_printf(1, ir_4529d0);
	v0 = getBeU32(xb.dump + 0x2fe8018);
	v1 = getBeU32(xb.dump + 0x2fec018);
	ok0 = shaSelfCheckU32(xb.dump + 0x2fe8000);
	if (ok0)
		log_printf(1, ir_4529f8, v0);
	else
		log_printf(1, ir_452a24);
	ok1 = shaSelfCheckU32(xb.dump + 0x2fec000);
	if (ok1)
		log_printf(1, ir_452a4c, v1);
	else {
		log_printf(1, ir_452aa4);
		__asm__("");	/* dom3 doesn't thread this copy: one log, ok0 tested after it */
	}
	if (__builtin_expect(ok0, 1) && (__builtin_expect(!ok1, 1) || v0 >= v1)) {
		log_printf(1, ir_452acc, v0);
		memcpy(anchor, xb.dump + 0x2fe8000, 0x200);
		return 1;
	}
	if (__builtin_expect(ok1, 1)) {
		log_printf(1, ir_452a78, v1);
		memcpy(anchor, xb.dump + 0x2fec000, 0x200);
		return 1;
	}
	return 0;
}

int mmcFindMobiles(void)
{
	int i;
	uint16_t block, len;

	if (!findAnchor())
		return 0;
	for (i = 0; i < 10; i++) {
		block = getBeU16(anchor + 0x1c + i * 4);
		if (!block)
			continue;
		len = getBeU16(anchor + 0x1e + i * 4);
		if (!len && !i)
			len = 0x4000;
		if (len) {
			mobiles[i].page = i;
			mobiles[i].found = 1;
			mobiles[i].version = 1;
			mobiles[i].offset = block << 14;
			mobiles[i].spare = 0;
			mobiles[i].len = len;
		}
	}
	return mobiles[0].found;
}

uint32_t spareVersion(uint8_t *s)
{
	uint32_t lo;

	if (xb.dumpBigBlock)
		lo = s[5];
	else if (xb.dumpBbController)
		lo = s[0];
	else
		lo = s[2];
	return (s[3] << 8) | (s[4] << 16) | (s[6] << 24) | lo;
}

static const char ir_452af8[] __attribute__((aligned(4))) = "Showing all pages with mobile info:\n";
static const char ir_452b20[] __attribute__((aligned(4))) = "starting mobile scan at page 0x%x (offset 0x%x) of 0x%x pages (0x%x total)\n";
static const char ir_452b6c[] __attribute__((aligned(4))) = "mobile%c.dat ver %02d offset 0x%08x (dump:0x%08x) count 0x%02x len 0x%04x page 0x%08x ";
static const char ir_452bc3[] __attribute__((aligned(1))) = "%02x ";
static const char ir_452bc9[] __attribute__((aligned(1))) = "(DELETE)\n";
static const char ir_452bd3[] __attribute__((aligned(1))) = "\n";
/* (uint32_t)letter: PRE hoists the cast into both arms, so letter's PHI dies with
   len's and ivopts' names give the inner loop's `cmp ebx,esi` (wip/README.md) */
void showMobilePages(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.dump;
	uint32_t page, end;
	uint32_t off;
	uint8_t fsType;

	if (!xb.dumpBigBlock) {
		end = xb.dumpPages - 1152;
		fsType = 48;
	} else {
		end = xb.dumpPages - 9216;
		fsType = 44;
	}
	log_printf(2, separator);
	log_printf(2, ir_452af8);
	log_printf(2, separator);
	page = SWAP32(h->sysUpdateAddr) >> 9;
	if (page & 0x1f)
		page = (page & ~0x1f) + 32;
	off = page * 512;
	log_printf(2, ir_452b20,
		   page, off, end, xb.dumpPages);
	for (; page < end; page++) {
		uint8_t *s = xb.dumpSpare + page * 16;
		uint8_t t = s[12] & 0x3f;
		int letter, i;
		uint32_t ver;
		uint16_t len;

		if (t == fsType) {
			letter = 'A';
			len = 0x4000;
		} else if (t >= 0x31 && t <= 0x39) {
			letter = t + 17;
			len = s[7] + (s[8] << 8);
		} else
			continue;
		ver = spareVersion(s);
		log_printf(2, ir_452b6c,
			   (uint32_t)letter, ver, page << 9, page * 528, s[9], len, page);
		for (i = 0; i < 16; i++)
			log_printf(2, ir_452bc3, xb.dumpSpare[page * 16 + i]);
		if (len & 0x8000)
			log_printf(2, ir_452bc9);
		else
			log_printf(2, ir_452bd3);
	}
	log_printf(2, separator);
}

int scanMobiles(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.dump;
	uint32_t end, page, off;
	uint8_t fsType;

	if (!xb.dumpBigBlock) {
		end = xb.dumpPages - 1152;
		fsType = 48;
	} else {
		end = xb.dumpPages - 9216;
		fsType = 44;
	}
	if (log_get_verbose() == 2) {
		log_printf(2, ir_452bd3);
		showMobilePages();
	}
	page = SWAP32(h->sysUpdateAddr) >> 9;
	page = (page & 0x1f) ? (page & ~0x1f) + 32 : page;
	while (page < end) {
		uint8_t *s = xb.dumpSpare + page * 16;
		uint8_t t = s[12] & 0x3f;
		int n, i;
		uint16_t len;
		uint32_t ver;

		/* sink moves this into spareVersion's join, after lo */
		off = page << 9;
		if (t == fsType) {
			n = 0;
			len = 0x4000;
		} else if (t >= 0x31 && t <= 0x39) {
			n = t - 48;
			len = s[7] + (s[8] << 8);
		} else
			goto next;
		ver = spareVersion(s);
		if (log_get_verbose() == 2) {
			log_printf(2, ir_452b6c,
				   n + 'A', ver, off, page * 528, s[9], len, page);
			for (i = 0; i < 16; i++)
				log_printf(2, ir_452bc3, xb.dumpSpare[page * 16 + i]);
			if (len & 0x8000)
				log_printf(2, ir_452bc9);
			else
				log_printf(2, ir_452bd3);
		}
		if (ver >= mobiles[n].version || !mobiles[n].found) {
			if (!len)
				goto next;
			if (len & 0x8000) {
				mobiles[n].found = 0;
				page++;
				goto align;
			}
			mobiles[n].found = 1;
			mobiles[n].version = ver;
			mobiles[n].spare = page * 16;
			mobiles[n].page = page;
			mobiles[n].len = len;
			mobiles[n].offset = off;
		} else {
			/* lays the advance block after the found path's stores */
			if (__builtin_expect(len & 0x8000, 1)) {
				page++;
				goto align;
			}
			if (!len)
				goto next;
		}
		page += len >> 9;
		if (len & 0x1ff)
			page++;
align:
		if (xb.dumpBigBlock)
			page = (page + 3) & ~3;
		continue;
next:
		page++;
		page = (page & 0x1f) ? (page & ~0x1f) + 32 : page;
	}
	return mobiles[0].found;
}

static const char ir_452bd8[] __attribute__((aligned(4))) = "bigblock file system offset set to 0x%x fsb: %x meta: %x lbaend: %x\n";
void setFsOffset(void)
{
	uint32_t meta;

	fsOffset = 0;
	if (!xb.dumpBigBlock)
		return;
	meta = xb.dumpSpare[mobiles[0].spare + 8] << 5;
	fsOffset = (3808 - meta) << 14;
	log_printf(1, ir_452bd8,
		   fsOffset, 3808 - meta, meta, 3808);
}

static const char ir_452c20[] __attribute__((aligned(4))) = "Scanning for mobile data and fsroot...";
static const char ir_452c47[] __attribute__((aligned(1))) = "done! fsroot found ok!";
static const char ir_452c5e[] __attribute__((aligned(1))) = "Mobiles found:\n";
static const char ir_452c70[] __attribute__((aligned(4))) = "    fsroot      version %02d found at offset 0x%08x len 0x%04x page 0x%08x\n";
static const char ir_452cbc[] __attribute__((aligned(4))) = "    mobile%c.dat version %02d found at offset 0x%08x len 0x%04x page 0x%08x\n";
static const char ir_452d0c[] __attribute__((aligned(4))) = "\n\n***** ERROR! Could not find fsroot!\n";
int findFsRoot(void)
{
	int found, i;
	uint8_t *src;
	

	log_printf(1, ir_452c20);
	if (xb.dumpMmc)
		found = mmcFindMobiles();
	else
		found = scanMobiles();
	if (!found) {
		log_printf(1, ir_452d0c);
		return 0;
	}
	puts(ir_452c47);
	setFsOffset();
	log_printf(1, ir_452c5e);
	for (i = 0; i < 10; i++) {
		if (mobiles[i].found) {
			if (i)
				log_printf(1, ir_452cbc, 'A' + i, mobiles[i].version, mobiles[i].offset, mobiles[i].len, mobiles[i].page);
			else
				log_printf(1, ir_452c70, mobiles[i].version, mobiles[i].offset, mobiles[i].len, mobiles[i].page);
		}
	}
	src = xb.dump + mobiles[0].offset;
	for (i = 0; i < 16; i++) {
		memcpy((uint8_t *)fsBuf.map + i * 512, src + i * 1024, 512);
		memcpy((uint8_t *)fsBuf.ent + i * 512, src + i * 1024 + 512, 512);
	}
	fsValid = 1;
	return found;
}

static const char ir_452d33[] __attribute__((aligned(1))) = "seeking security files...\n";
static const char ir_452d4e[] __attribute__((aligned(1))) = "done!\n";
inline void imgGetSecurityFiles(void)
{
	uint32_t i, block;

	log_printf(1, ir_452d33);
	for (i = 0; i < xb.nFlashFiles2; i++)
		if (xb.flashFiles[i][0] && fsFindFile(xb.flashFiles[i], &block, &xb.flashSize[i], &xb.flashTime[i], 0))
			loadFlashFile(i, block);
	log_printf(1, ir_452d4e);
}

static const char ir_452d55[] __attribute__((aligned(1))) = "seeking smc config in dump...";
static const char ir_452d74[] __attribute__((aligned(4))) = "found at offset 0x%x! Using if no smc config is provided.\n";
static const char ir_452db0[] __attribute__((aligned(4))) = "found at offset 0x%x! Unable to allocate 0x400 bytes of memory for smc config, skipping\n";
static const char ir_452e09[] __attribute__((aligned(1))) = "not found!\n";
void findSmcConfig(void)
{
	uint32_t off, end;

	if (xb.dumpMmc) {
		off = 0x2ffc000;
		end = 0x3000000;
	} else if (xb.dumpBigBlock) {
		off = 0x3be0000;
		end = 0x4000000;
	} else {
		end = xb.dumpSize;
		if (end == 0x1000000)
			off = 0xf7c000;
		else if (end == 0x4000000)
			off = 0x3dfc000;
		else
			off = 0;
	}
	log_printf(1, ir_452d55);
	for (; off < end; off += 512) {
		if (!smcConfigOk(xb.dump + off))
			continue;
		xb.smcConfig.data = malloc(0x400);
		if (!xb.smcConfig.data) {
			log_printf(1, ir_452db0, off);
			off = end;
			continue;
		}
		log_printf(1, ir_452d74, off);
		memcpy(xb.smcConfig.data, xb.dump + off, 0x400);
		xb.smcConfig.size = 0x400;
		off = end;
	}
	if (!xb.smcConfig.data)
		log_printf(1, ir_452e09, off);
}

static const char ir_452e18[] __attribute__((aligned(4))) = "\n\n****************  WARNING  *************************\n";
static const char ir_452e50[] __attribute__((aligned(4))) = "  nanddump.bin has NAND memory unit data, make\n";
static const char ir_452e80[] __attribute__((aligned(4))) = "  sure you back up any important data off the\n";
static const char ir_452eb0[] __attribute__((aligned(4))) = "  internal MU before flashing a new image!\n";
static const char ir_452edc[] __attribute__((aligned(4))) = "\n  xeBuild will attempt to keep this data, but\n";
static const char ir_452f0c[] __attribute__((aligned(4))) = "  many things could cause it to be invalid/corrupt.\n";
static const char ir_452f44[] __attribute__((aligned(4))) = "****************************************************\n\n";
/* -1 (bad block) is the initial value and the only one that skips the ECC
   check, so the bad-block exits reach the return through `lba != -1` and
   aren't predicted as negative returns (ce1 hoists the -1 above the tests);
   -6 goes through `lba != -6` (VRP then can't fold the small block's lba to
   0 on the `lba > 0` exit, as it does the big block's) */
int checkBlock(uint8_t *b, int block, int numBlocks)
{
	int lba, lba0, lba1;

	if (blockErased(b, xb.dumpBigBlock))
		return -2;
	lba = -1;
	if (xb.dumpBigBlock) {
		if (b[512] == 0xff && b[68096] == 0xff) {
			lba = b[513] + (b[514] & 0xf) * 256;
			if (lba >= numBlocks - 1)
				lba = -3;
			else if (!xb.muChecked) {
				uint8_t m = b[524] & 0x3f;
				int t = m;

				/* opaque int copy: the <= 0x29 test stays an int
				   compare and isn't merged with the zero test */
				__asm__("" : "+d"(t));
				if (t <= 0x29 && m) {
					log_printf(0, ir_452e18);
					log_printf(0, ir_452e50);
					log_printf(0, ir_452e80);
					log_printf(0, ir_452eb0);
					if (xb.bootFlags & 0x10000000) {
						log_printf(0, ir_452edc);
						log_printf(0, ir_452f0c);
					}
					log_printf(0, ir_452f44);
					xb.muChecked = 1;
					xb.nandMu = 1;
				}
			} else {
				if (lba > 0 && block < numBlocks - 34 && lba != block)
					lba = -3;
			}
		}
	} else {
		if (b[517] == 0xff && b[8965] == 0xff) {
			lba1 = b[513] + (b[514] & 0xf) * 256;
			/* volatile: b[513] loaded again, as in the original */
			lba0 = b[512] + (((volatile uint8_t *)b)[513] & 0xf) * 256;
			if (xb.dumpBbController) {
				if (block && block == lba0)
					lba = -6;
				else
					lba = lba1;
			} else {
				if (block && block == lba1)
					lba = -6;
				else
					lba = lba0;
			}
			if (lba != -6) {
				if (lba >= numBlocks - 1)
					lba = -3;
				else if (lba > 0 && block < numBlocks - 34 && block != lba)
					lba = -3;
			}
		}
	}
	if (lba != -1) {
		if (!(xb.bootFlags & 0x80000000) && !blockEccOk(b, xb.dumpBigBlock))
			lba = -4;
	}
	return lba;
}

static const char ir_452f7c[] __attribute__((aligned(4))) = "block 0x%x was remapped to block 0x%x at remap instance %d\n";
static const char ir_452fb8[] __attribute__((aligned(4))) = "block 0x%x was remapped to block 0x%x, entering remap instance %d\n";
static const char ir_452ffc[] __attribute__((aligned(4))) = "MAX REMAPS of 32 exceeded, remapping disabled and image rejected as faulty!\n";
int addRemap(uint32_t block, int dest, int numBlocks)
{
	uint32_t i;
	int found = 0;
	uint32_t b = block;	/* unused; puts block before the loads in compares */

	for (i = 0; i < xb.numBad; i++) {
		if (block == xb.badBlocks[i] && xb.badRemap[i] == -1 && dest < numBlocks) {
			log_printf(1, ir_452f7c, block, dest, i);
			xb.badRemap[i] = dest;
			found = 1;
		}
	}
	if (found)
		return 1;
	if (xb.numBad >= 32) {
		log_printf(1, ir_452ffc);
		return 0;
	}
	if (dest != -1)
			log_printf(1, ir_452fb8, block, dest, xb.numBad + 1);
		xb.badBlocks[xb.numBad] = block;
		xb.badRemap[xb.numBad] = dest;
		xb.numBad++;
	return 1;
}

int findFreeRemap(int numBlocks)
{
	int b, used;
	uint32_t i;

	for (b = numBlocks - 1; b >= numBlocks - 32; b--) {
		used = 0;
		for (i = 0; i < xb.numBad; i++)
			if (xb.badRemap[i] == b || xb.badBlocks[i] == b) {
				used = 1;
				i = xb.numBad;
			}
		if (!used)
			return b;
	}
	return 0;
}

static const char ir_453049[] __attribute__((aligned(1))) = "cleaning up stray remaps\n";
static const char ir_453064[] __attribute__((aligned(4))) = "block 0x%x had no remap, assigning remap block 0x%x\n";
static const char ir_45309c[] __attribute__((aligned(4))) = "block 0x%x had no remap, and I could not assign one!\n";
static const char ir_4530d4[] __attribute__((aligned(4))) = "block 0x%x had no need of remap, it's in the wear area\n";
void remapBadBlocks(int numBlocks)
{
	uint32_t i;
	int b;

	log_printf(1, ir_453049);
	for (i = 0; i < xb.numBad; i++) {
		if (xb.badRemap[i] != -1)
			continue;
		if (xb.badBlocks[i] < numBlocks - 32) {
			if (!xb.numBad)	/* i < numBad: drops the inlined loop's guard */
				__builtin_unreachable();
			b = findFreeRemap(numBlocks);
			if (b) {
				xb.badRemap[i] = b;
				log_printf(1, ir_453064, xb.badBlocks[i], b);
			} else
				log_printf(1, ir_45309c, xb.badBlocks[i]);
		} else {
			log_printf(1, ir_4530d4, xb.badBlocks[i]);
			xb.badRemap[i] = -5;
		}
	}
	log_printf(1, ir_452d4e);
}

int notZeropair(void)
{
	return memcmp(zeropair, xb.dump + 16, 14) != 0;
}

unsigned long spareLbaOk(int pages)
{
	int i;

	for (i = 1; i < pages; i++)
		if (memcmp(xb.dumpSpare, xb.dumpSpare + i * 16, 3))
			return 0;
	return 1;
}

static const char ir_45310c[] __attribute__((aligned(4))) = "\n\n***** ERROR: nanddump.bin is a ZEROPAIR/XELL image, discarding\n";
/* ce1 would hoist ret = 1 above the branch (edge predicted 61%) */
__attribute__((optimize("no-if-conversion"))) uint32_t copyMmcImage(uint8_t *raw)
{
	xb.numBad = 0;
	memcpy(xb.dump, raw, xb.dumpSize);
	if (notZeropair())
		return 1;
	log_printf(0, ir_45310c);
	return 0;
}

static int addRemapP(int block, int ablock, int cb, int dest, int numBlocks)
{
	int i;
	int found = 0;

	i = 0;
	goto test;
tail:
	if (xb.numBad >= 32) {
		log_printf(1, ir_452ffc);
		return 0;
	}
	if (dest != -1)
		log_printf(1, ir_452fb8, ablock, dest, xb.numBad + 1);
	xb.badBlocks[xb.numBad] = ablock;
	xb.badRemap[xb.numBad] = dest;
	xb.numBad++;
	return 1;
body:
	__asm__("" : : "ri"(cb), "ri"(cb), "ri"(cb), "ri"(cb));
	if (xb.badBlocks[i] == block && xb.badRemap[i] == -1 && dest < numBlocks) {
		log_printf(1, ir_452f7c, block, dest, i);
		xb.badRemap[i] = dest;
		found = 1;
	}
	i++;
test:
	if (i < xb.numBad)
		goto body;
	if (found)
		return 1;
	goto tail;
}

static const char ir_453150[] __attribute__((aligned(4))) = "UNEXPECTED DUMP PARSE ERROR: %d pages cannot divide by %d!\n";
static const char ir_45318c[] __attribute__((aligned(4))) = "parsing dump into user and spare...\n";
static const char ir_4531b4[] __attribute__((aligned(4))) = "bad block at 0x%x (raw offset 0x%x), block ignored\n";
static const char ir_4531e8[] __attribute__((aligned(4))) = "***** WARNING: nanddump.bin has a bad LBA at block 0x%x (raw offset 0x%x), block LBA ignored\n";
static const char ir_453248[] __attribute__((aligned(4))) = "***** WARNING: nanddump.bin has a mixed controller LBA at block 0x%x (raw offset 0x%x), block ignored\n";
static const char ir_4532b0[] __attribute__((aligned(4))) = "               this is likely caused by previously using jaspersb on a jasper type console!\n";
static const char ir_453310[] __attribute__((aligned(4))) = "ECD error at block 0x%x (raw offset 0x%x), block will be remapped\n";
static const char ir_453354[] __attribute__((aligned(4))) = "copying nanddump data from block 0x%x to block 0x%x for file extraction integrity\n";
static const char ir_4533a8[] __attribute__((aligned(4))) = "***** WARNING: ignoring possible remap of block 0x%x to block 0x%x\n";
static const char ir_4533ec[] __attribute__((aligned(4))) = "               this dump may have some bad data!\n";
static const char ir_453420[] __attribute__((aligned(4))) = "\n\n***** ERROR: nanddump.bin has mixed LBA in the same block which usually occurs\n";
static const char ir_453474[] __attribute__((aligned(4))) = "             due to an improper nandpro write method, discarding\n";
static const char ir_4534b8[] __attribute__((aligned(4))) = "Discarding remap data as NOREMAP was specified!\n";
static const char ir_4534e9[] __attribute__((aligned(1))) = "--remap summary--\n";
static const char ir_4534fc[] __attribute__((aligned(1))) = "-----------------\n";
static const char ir_453510[] __attribute__((aligned(4))) = "%d: source: 0x%04x dest: (NONE/BAD)\n";
static const char ir_453538[] __attribute__((aligned(4))) = "%d: source: 0x%04x dest: 0x%04x\n";
unsigned long parseDump(uint8_t *raw)
{
	int ppb = xb.dumpBigBlock ? 256 : 32;
	int blocks = xb.dumpPages / ppb;
	int blk, dst, p, b2;
	uint32_t n;
	int i;
	uint8_t *src;

	int rr = xb.dumpPages % ppb;

	if (rr) {
		log_printf(0, ir_453150, xb.dumpPages, ppb);
		return 0;
	}
	log_printf(1, ir_45318c);
	for (n = 0; n < blocks; n++) {
		blk = n;
		src = raw + blk * 528 * ppb;
		dst = checkBlock(src, blk, blocks);
		if (dst == -2)
			continue;
		if (dst == -1) {
			log_printf(1, ir_4531b4, blk, src - raw);
			b2 = blk;
			__asm__("" : "+r"(b2));
			if (!addRemapP(b2, blk, 0, dst, blocks))
				return 0;
			goto next;
		}
		if (dst == -3) {
			log_printf(0, ir_4531e8, blk, src - raw);
			continue;
		}
		if (dst == -6) {
			log_printf(0, ir_453248, blk, src - raw);
			log_printf(0, ir_4532b0, blk, src - raw);
			continue;
		}
		if (dst == -4) {
			if (blk >= blocks)
				__builtin_unreachable();
			if (blk < blocks) {
				log_printf(1, ir_453310, blk, src - raw);
				if (!addRemapP(blk, blk, blk, -1, blocks))
					return 0;
			}
			__asm__("");
			dst = blk;
		} else {
rem: __attribute__((hot));
			if (dst != blk) {
				if (blk >= blocks - 32)
					log_printf(1, ir_453354, blk, dst);
				else {
					log_printf(0, ir_4533a8, blk, dst);
					log_printf(0, ir_4533ec, blk, dst);
					dst = blk;
				}
			}
		}
		if (blk == 0) {
			if (!notZeropair()) {
				log_printf(0, ir_45310c);
				return 0;
			}
			if (!spareLbaOk(ppb)) {
				log_printf(0, ir_453420);
				log_printf(0, ir_453474);
				return 0;
			}
		}
		for (p = 0; p < ppb; p++) {
			memcpy(xb.dump + (dst * ppb + p) * 512, raw + (blk * ppb + p) * 528, 512);
			memcpy(xb.dumpSpare + (dst * ppb + p) * 16, raw + (blk * ppb + p) * 528 + 512, 16);
		}
		if (blk >= blocks)
			__builtin_unreachable();
		if (dst != blk && !addRemapP(dst, dst, 0, blk, blocks))
			return 0;
next:
		;
	}
	log_printf(1, ir_452d4e);
	if (xb.bootFlags & 0x40000000) {
		if (xb.numBad) {
			log_printf(1, ir_4534b8);
			xb.numBad = 0;
		}
	} else if (xb.numBad) {
		remapBadBlocks(blocks);
		log_printf(1, ir_4534e9);
		for (i = 0; i < xb.numBad; i++) {
			if (xb.badRemap[i] == -5)
				log_printf(1, ir_453510, i, xb.badBlocks[i]);
			else
				log_printf(1, ir_453538, i, xb.badBlocks[i], xb.badRemap[i]);
		}
		log_printf(1, ir_4534fc);
	}
	return 1;
}

static const char ir_45355c[] __attribute__((aligned(4))) = "size is not a multiple of %d bytes, not copying data..\n";
static const char ir_453594[] __attribute__((aligned(1))) = "no data to copy..\n";
static const char ir_4535a7[] __attribute__((aligned(1))) = "rb";
static const char ir_4535ac[] __attribute__((aligned(4))) = "could not re-open '%s' for reading, not copying data..\n";
static const char ir_4535e4[] __attribute__((aligned(4))) = "could not seek to 0x%x, not copying data..\n";
static const char ir_453610[] __attribute__((aligned(4))) = "could not allocate 0x%x byte buffer, not copying data..\n";
static const char ir_453649[] __attribute__((aligned(1))) = "reading nanddump.bin...\n";
static const char ir_453664[] __attribute__((aligned(4))) = "writing nanddump.bin MU area to output file...";
uint32_t copyMuData(FILE *out, void *sha)
{
	char name[0x400];
	FILE *fp;
	uint8_t *buf;
	int len;

	if (dumpSize != dumpSize / 0x4200000 * 0x4200000) {
		log_printf(0, ir_45355c, 0x4200000);
		return 0;
	}
	if (dumpSize <= 0x4200000) {
		log_printf(0, ir_453594);
		return 0;
	}
	strcpy(name, xb.baseDir);
	strcat(name, "nanddump.bin");
	fp = fopen(name, ir_4535a7);
	if (!fp) {
		log_printf(0, ir_4535ac, name);
		return 0;
	}
	if (fseek(fp, 0x4200000, SEEK_END)) {
		log_printf(0, ir_4535e4, 0x4200000);
		fclose(fp);
		return 0;
	}
	len = dumpSize - 0x4200000;
	buf = malloc(len);
	if (!buf) {
		log_printf(0, ir_453610, len);
		fclose(fp);
		return 0;
	}
	log_printf(1, ir_453649);
	fread(buf, dumpSize - 0x4200000, 1, fp);
	fclose(fp);
	log_printf(1, ir_453664);
	if (sha)
		XeCryptShaUpdate(sha, buf, dumpSize - 0x4200000);
	fwrite(buf, dumpSize - 0x4200000, 1, out);
	free(buf);
	return 1;
}

static const char ir_453694[] __attribute__((aligned(4))) = "\tNAND dump is from a mmc machine\n";
static const char ir_4536b8[] __attribute__((aligned(4))) = "\tNAND dump uses big block controller\n";
static const char ir_4536e0[] __attribute__((aligned(4))) = "\tNAND dump is from a big block machine\n";
static const char ir_453708[] __attribute__((aligned(4))) = "***** WARNING: NAND dump too small to be from a big block machine, discarding dump!\n";
static const char ir_453760[] __attribute__((aligned(4))) = "\tNAND dump is from a small block machine\n";
static const char ir_45378c[] __attribute__((aligned(4))) = "\tNAND dump uses small block controller\n";
static const char ir_4537b4[] __attribute__((aligned(4))) = "***** WARNING: NAND dump does not appear to have a good block at block 0, discarding dump!\n";
int detectController(uint8_t *raw, int size)
{
	int i, n;
	uint32_t found;

	if (size == 0x3000000) {
		log_printf(1, ir_453694);
		log_printf(1, ir_4536b8);
		xb.dumpBbController = 1;
		xb.dumpBigBlock = 0;
		xb.muChecked = 1;
		xb.dumpMmc = 1;
		return 1;
	}
	if (raw[512] == 0xff) {
		log_printf(1, ir_4536e0);
		log_printf(1, ir_4536b8);
		if (size < 0x4200000) {
			log_printf(0, ir_453708);
			return 0;
		}
		xb.dumpBigBlock = 1;
		xb.dumpBbController = 1;
		return 1;
	}
	if (raw[517] != 0xff) {
		log_printf(0, ir_4537b4);
		return 0;
	}
	n = size / 16896;
	log_printf(1, ir_453760);
	xb.dumpBigBlock = 0;
	xb.muChecked = 1;
	found = 0;
	/* code-free hints: found in eax outside the loop (one head-merged xor
	   for both found = 0 edges), i in ebx */
	if (n > 1)
		__asm__("" : "+a"(found));
	for (i = 1; i < n; i++) {
		uint8_t *b = raw + i * 16896;
		int hi, lo;
		__asm__("" : : "b"(i));

		if (b[517] != 0xff || b[513] == 0xff)
			continue;
		hi = (b[514] & 0xf) * 256;
		lo = b[513];
		if (hi + lo == i) {
			i = n;
			log_printf(1, ir_4536b8);
			xb.dumpBbController = 1;
			found = 1;
		} else {
			int lo2 = b[512];

			/* lo and lo2 kept live past their adds, so each sum takes
			   hi's register (ebp, ecx) */
			__asm__("" : : "a"(lo));
			__asm__("" : : "d"(lo2));
			if (lo2 + (b[513] & 0xf) * 256 == i) {
				__asm__("" : : "d"(lo2));
				i = n;
				log_printf(1, ir_45378c);
				xb.dumpBbController = 0;
				found = 1;
			}
		}
	}
	return found;
}

static const char ir_453810[] __attribute__((aligned(1))) = "%s file size: 0x%llx\n";
static const char ir_453828[] __attribute__((aligned(4))) = "******* ERROR loading '%s', file size 0x%llx is not large enough\n";
static const char ir_45386c[] __attribute__((aligned(4))) = "******* ERROR loading '%s', flash header magic is incorrect\n";
static const char ir_4538ac[] __attribute__((aligned(4))) = "******* ERROR loading '%s', flash header Entry is too large\n";
static const char ir_4538ec[] __attribute__((aligned(4))) = "******* ERROR loading '%s', flash header Size is too large\n";
static const char ir_453928[] __attribute__((aligned(4))) = "******* ERROR loading '%s', flash header KeyVaultSize is too large\n";
static const char ir_45396c[] __attribute__((aligned(4))) = "******* ERROR loading '%s', flash header SysUpdateAddr is malformed\n";
static const char ir_4539b4[] __attribute__((aligned(4))) = "******* ERROR loading '%s', flash header SysUpdateCount is not 2, continuing anyway\n";
static const char ir_453a0c[] __attribute__((aligned(4))) = "******* ERROR loading '%s', flash header KeyVaultVersion is not 0x0712, continuing anyway\n";
static const char ir_453a68[] __attribute__((aligned(4))) = "******* ERROR loading '%s', flash header KeyVaultAddr is too large\n";
static const char ir_453aac[] __attribute__((aligned(4))) = "******* ERROR loading '%s', flash header FileSystemAddr is too large\n";
static const char ir_453af4[] __attribute__((aligned(4))) = "******* ERROR loading '%s', flash header SmcConfigAddr is not 0, continuing anyway\n";
static const char ir_453b48[] __attribute__((aligned(4))) = "******* ERROR loading '%s', flash header SmcBootSize is not 0x3000 or 0x3800\n";
static const char ir_453b98[] __attribute__((aligned(4))) = "******* ERROR loading '%s', flash header SmcBootAddr is too large\n";
static const char ir_453bdc[] __attribute__((aligned(4))) = "FATX magic found, truncating load size to 0x3000000 bytes for mmc consoles\n";
static const char ir_453c28[] __attribute__((aligned(4))) = "First page does not contain a valid ECC, assuming this is an mmc dump and truncating load size to 0x3000000 bytes!\n";
static const char ir_453c9c[] __attribute__((aligned(4))) = "First page contains a valid ECC, assuming this is a big block flash overdump and truncating load size to 0x4200000 bytes\n";
static const char ir_453d18[] __attribute__((aligned(4))) = "nanddump header checks passed OK!\n";
int checkHeader(const char *name, FILE *fp)
{
	struct flashhdr hdr;
	uint8_t page[0x210];
	uint32_t magic;
	long long size;

	size = getFileSize64(fp);
	log_printf(1, ir_453810, name, size);
	if (size < 0x1080000) {
		log_printf(0, ir_453828, name, size);
		return 0;
	}
	fread(&hdr, 0x80, 1, fp);
	rewind(fp);
	if (SWAP16(hdr.magic) != 0xff4f) {
		log_printf(0, ir_45386c, name);
		return 0;
	}
	if (size < SWAP32(hdr.cbOffset)) {
		log_printf(0, ir_4538ac, name);
		return 0;
	}
	if (size < SWAP32(hdr.cfOffset)) {
		log_printf(0, ir_4538ec, name);
		return 0;
	}
	if (SWAP32(hdr.kvSize) > 0x8000) {
		log_printf(0, ir_453928, name);
		return 0;
	}
	/* as `||`, ifcombine makes it `a | b` and forwprop puts the size test
	   last; the asm keeps two jumps in this order */
	if (size < SWAP32(hdr.sysUpdateAddr))
		goto badSysUpdate;
	__asm__("");
	if (SWAP32(hdr.cfOffset) > SWAP32(hdr.sysUpdateAddr)) {
badSysUpdate:
		log_printf(0, ir_45396c, name);
		return 0;
	}
	if (SWAP16(hdr.sysUpdateCount) != 2)
		log_printf(0, ir_4539b4, name);
	if (SWAP16(hdr.kvVersion) != 0x712)
		log_printf(0, ir_453a0c, name);
	if (size < SWAP32(hdr.kvAddr)) {
		log_printf(0, ir_453a68, name);
		return 0;
	}
	if (size < SWAP32(hdr.patchSlotSize)) {
		log_printf(0, ir_453aac, name);
		return 0;
	}
	if (SWAP32(hdr.smcConfigAddr))
		log_printf(0, ir_453af4, name);
	if (SWAP32(hdr.smcBootSize) != 0x3000 && SWAP32(hdr.smcBootSize) != 0x3800) {
		log_printf(0, ir_453b48, name);
		return 0;
	}
	if (size < SWAP32(hdr.smcBootAddr)) {
		log_printf(0, ir_453b98, name);
		return 0;
	}
	if (size > 0x3000000) {
		fseeko64(fp, 0x3000000, SEEK_SET);
		fread(&magic, 4, 1, fp);
		rewind(fp);
		if (getBeU32((uint8_t *)&magic) == 0x58544146) {
			log_printf(1, ir_453bdc);
			size = 0x3000000;
		} else {
			rewind(fp);
			fread(page, 0x210, 1, fp);
			rewind(fp);
			if (!pageEccOk(page, page + 512)) {
				log_printf(1, ir_453c28);
				size = 0x3000000;
			} else if (size > 0x4200000) {
				log_printf(1, ir_453c9c);
				size = 0x4200000;
			}
		}
	}
	log_printf(1, ir_453d18);
	return size;
}

static const char ir_453d3c[] __attribute__((aligned(4))) = "**** Warning: error getting CB/CBA Nonce offset, aborting!\n";
static const char ir_453d78[] __attribute__((aligned(4))) = "**** Warning: error getting CB/CBA Nonce, aborting!\n";
static const char ir_453db0[] __attribute__((aligned(4))) = "**** Warning: error getting CBB Nonce offset, aborting!\n";
static const char ir_453dec[] __attribute__((aligned(4))) = "**** Warning: error getting CBB Nonce, offset 0x%x aborting!\n";
static const char ir_453e2c[] __attribute__((aligned(4))) = "**** Warning: error getting CD Nonce offset, aborting!\n";
static const char ir_453e64[] __attribute__((aligned(4))) = "**** Warning: error getting CD Nonce, offset 0x%x aborting!\n";
static const char ir_453ea4[] __attribute__((aligned(4))) = "**** Warning: error getting CE Nonce offset, aborting!\n";
static const char ir_453edc[] __attribute__((aligned(4))) = "**** Warning: error getting CE Nonce, offset 0x%x aborting!\n";
static const char ir_453f1c[] __attribute__((aligned(4))) = "**** Warning: error getting CF Nonce offset, aborting!\n";
static const char ir_453f54[] __attribute__((aligned(4))) = "**** Warning: error getting CF Nonce, offset 0x%x aborting!\n";
static const char ir_453f94[] __attribute__((aligned(4))) = "**** Warning: error getting CG Nonce offset, aborting!\n";
static const char ir_453fcc[] __attribute__((aligned(4))) = "**** Warning: error getting CG Nonce, offset 0x%x aborting!\n";
void getNonces(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.dump;
	uint32_t off = SWAP32(h->cbOffset);
	uint8_t *p;

	if (off >= xb.dumpSize) {
		log_printf(1, ir_453d3c);
		return;
	}
	p = xb.dump + off;
	if ((ROT16(*(uint16_t *)p) & 0x43ff) != 0x4342) {
		log_printf(1, ir_453d78);
		return;
	}
	setInfoKey0(xb.dump + off + 16);
	off += (SWAP32(*(uint32_t *)(p + 12)) + 15) & ~15;
	if (p[6] & 8) {
		if (off >= xb.dumpSize) {
			log_printf(1, ir_453db0);
			return;
		}
		p = xb.dump + off;
		if ((ROT16(*(uint16_t *)p) & 0x43ff) != 0x4342) {
			log_printf(1, ir_453dec, off);
			return;
		}
		setInfoKey1(xb.dump + off + 16);
		off += (SWAP32(*(uint32_t *)(p + 12)) + 15) & ~15;
	}
	if (off >= xb.dumpSize) {
		log_printf(1, ir_453e2c);
		return;
	}
	p = xb.dump + off;
	if ((ROT16(*(uint16_t *)p) & 0x43ff) != 0x4344) {
		log_printf(1, ir_453e64, off);
		return;
	}
	setInfoKey2(xb.dump + off + 16);
	off += (SWAP32(*(uint32_t *)(p + 12)) + 15) & ~15;
	if (off >= xb.dumpSize) {
		log_printf(1, ir_453ea4);
		return;
	}
	if ((ROT16(*(uint16_t *)(xb.dump + off)) & 0x43ff) != 0x4345) {
		log_printf(1, ir_453edc, off);
		return;
	}
	setInfoKey3(xb.dump + off + 16);
	off = SWAP32(h->sysUpdateAddr);
	if (off >= xb.dumpSize) {
		log_printf(1, ir_453f1c);
		return;
	}
	p = xb.dump + off;
	if ((ROT16(*(uint16_t *)p) & 0x43ff) != 0x4346) {
		log_printf(1, ir_453f54, off);
		return;
	}
	setInfoKey4(xb.dump + off + 32);
	off += (SWAP32(*(uint32_t *)(p + 12)) + 15) & ~15;
	if (off >= xb.dumpSize) {
		log_printf(1, ir_453f94);
		return;
	}
	if ((ROT16(*(uint16_t *)(xb.dump + off)) & 0x43ff) != 0x4347) {
		log_printf(1, ir_453fcc, off);
		return;
	}
	setInfoKey5(xb.dump + off + 16);
	xb.randomKeys = 0;
}

static const char ir_454009[] __attribute__((aligned(1))) = "\n------ Checking %s ------\n";
static const char ir_454025[] __attribute__((aligned(1))) = "NAND dump not found at '%s'\n";
static const char ir_454044[] __attribute__((aligned(4))) = "NAND dump '%s' is not a correct raw (with ecc) dump size (0x%x bytes), ignoring\n";
static const char ir_454098[] __attribute__((aligned(4))) = "NAND dump '%s' is not a correct dump size (0x%x bytes), ignoring\n";
static const char ir_4540dc[] __attribute__((aligned(4))) = "******* ERROR loading '%s', unable to allocate memory\n";
static const char ir_454114[] __attribute__((aligned(4))) = "Loading NAND dump (0x%x bytes)...";
static const char ir_454138[] __attribute__((aligned(4))) = "******* ERROR loading '%s', unable to allocate user/spare memory\n";
static const char ir_45417c[] __attribute__((aligned(4))) = "Detecting NAND controller type from dump data...\n";
static const char ir_4541b0[] __attribute__((aligned(4))) = "******* ERROR loading '%s', unable to determine NAND controller type!\n";
uint32_t loadDump(const char *path)
{
	char name[0x400];
	FILE *fp;
	int size;
	uint32_t ret;
	uint32_t pages, rawSize;
	uint8_t *raw;

	if (path)
		strcpy(name, path);
	else {
		strcpy(name, xb.baseDir);
		strcat(name, "nanddump.bin");
	}
	buildCleanup();
	log_printf(1, ir_454009, name);
	fp = fopen(name, ir_4535a7);
	if (!fp) {
		log_printf(1, ir_454025, name);
		return 0;
	}
	size = checkHeader(name, fp);
	if (!size) {
		buildCleanup();
		return 0;
	}
	dumpSize = size;
	if (size == 0x3000000) {
		xb.dumpPages = 0x18000;
		rawSize = 0x3000000;
	} else if (size % 528) {
		log_printf(1, ir_454098, name, size);
		fclose(fp);
		return 0;
	} else {
		if (size >= 0x4200000) {
			rawSize = 0x4200000;
			pages = 0x20000;
			size = 0x4200000;
		} else {
			rawSize = 0x1080000;
			pages = 0x8000;
			if (size != 0x1080000) {
				log_printf(1, ir_454044, name, size);
				fclose(fp);
				return 0;
			}
		}
		xb.dumpPages = pages;
	}
	raw = malloc(rawSize);
	if (!raw) {
		log_printf(0, ir_4540dc, name);
		fclose(fp);
		return 0;
	}
	log_printf(1, ir_454114, size);
	fread(raw, rawSize, 1, fp);
	fclose(fp);
	log_printf(1, ir_452d4e, name);
	xb.dumpSize = xb.dumpPages << 9;
	xb.dumpSpareSize = xb.dumpPages * 16;
	xb.dump = malloc(xb.dumpPages << 9);
	xb.dumpSpare = malloc(xb.dumpPages * 16);
	if (!xb.dump || !xb.dumpSpare) {
		log_printf(0, ir_454138, name);
		buildCleanup();
		free(raw);
		return 0;
	}
	memset(xb.dump, 0xff, xb.dumpSize);
	memset(xb.dumpSpare, 0xff, xb.dumpSpareSize);
	log_printf(1, ir_45417c);
	if (detectController(raw, size)) {
		/* copyMmcImage's body, written out: its optimize attribute keeps it
		   from being inlined here.  The test must be predicted 50-52.6%
		   (ce1 hoists ret = 1 only above 50%, the mmc trace takes the log
		   block only within 10% of even): call 71% x hot label 15% x opcode
		   nonequal 72% (the != against size == 0, folded by VRP) = 52.6% */
		if (xb.dumpMmc) {
			xb.numBad = 0;
			memcpy(xb.dump, raw, xb.dumpSize);
			if (notZeropair() != (size == 0))
				ret = 1;
			else {
mmcbad: __attribute__((hot));
				log_printf(0, ir_45310c);
				ret = 0;
			}
		} else
			ret = parseDump(raw);
		if (!ret)
			buildCleanup();
		else {
			getImageKv();
			getImageSmc();
			findSmcConfig();
			getImageLdv();
			if (findFsRoot()) {
				if (!(xb.bootFlags & 0x20000000)) {
					getNetKd();
					getImageMobiles();
				}
				if (!(xb.bootFlags & 0x4000000))
					imgGetSecurityFiles();
			}
			getNonces();
		}
	} else {
		log_printf(0, ir_4541b0, name);
		ret = 0;
	}
	free(raw);
	return ret;
}

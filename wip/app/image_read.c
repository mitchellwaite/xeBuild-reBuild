/* image_read: parsing an existing NAND image (nanddump.bin): sectors, pairing, LDV, smc.bin */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;

#define SWAP16(x) ((((x) << 8) & 0xff00) + ((x) >> 8))
#define ROT16(x) ((u16)(((x) << 8) | ((x) >> 8)))
#define SWAP32(x) (((x) << 24) + (((x) << 8) & 0xff0000) + (((x) >> 8) & 0xff00) + ((x) >> 24))

struct netfile {
	u8 *data;
	int size;
};

/* the parts of main.c's struct xebuild used here */
struct xebuild {
	int mode;			/* 000 */
	u32 flags;			/* 004 */
	u32 type;			/* 008 build type */
	u8 pad00c[0x020 - 0x00c];
	int f020;			/* 020 */
	u8 pad024[0x060 - 0x024];
	u32 bootFlags;			/* 060 */
	u8 pad064[0x075 - 0x064];
	u8 cfLdv;			/* 075 */
	u8 pad076[0x0ac - 0x076];
	u8 *image;			/* 0ac user data, ECC stripped */
	u8 *spare;			/* 0b0 spare data, 16 bytes a page */
	u32 imageSize;			/* 0b4 */
	u32 spareSize;			/* 0b8 */
	u32 numPages;			/* 0bc */
	int bigBlock;			/* 0c0 */
	int bbController;		/* 0c4 */
	int mmc;			/* 0c8 */
	int nandMu;			/* 0cc */
	int muChecked;			/* 0d0 */
	u32 numBad;			/* 0d4 */
	u32 badBlocks[32];		/* 0d8 */
	int badRemap[32];		/* 158 */
	u8 pad1d8[0x1ec - 0x1d8];
	struct netfile mobile[11];	/* 1ec MobileB-J, Statistics, Manufacturing */
	struct netfile smc;		/* 244 */
	struct netfile kv;		/* 24c */
	struct netfile kvAlt;		/* 254 */
	struct netfile smcConfig;	/* 25c */
	struct netfile netkd;		/* 264 */
	u8 pad26c[0xeac - 0x26c];
	char baseDir[0x400];		/* eac */
	u8 pad12ac[0x4f144 - 0x12ac];
	char flashFiles[10][22];	/* 4f144 */
	u8 *flashBuf[10];		/* 4f220 */
	u32 flashSize[10];		/* 4f248 */
	u32 flashTime[10];		/* 4f270 */
	u8 pad4f298[0x4f2c0 - 0x4f298];
	u32 numFlashFiles;		/* 4f2c0 */
};

/* the flash header at the start of the image */
struct flashhdr {
	u16 magic;			/* 00 */
	u16 build;			/* 02 */
	u16 qfe;			/* 04 */
	u16 flags;			/* 06 */
	u32 entry;			/* 08 CB */
	u32 size;			/* 0c */
	u8 copyright[0x60 - 0x10];	/* 10 */
	u32 kvSize;			/* 60 */
	u32 sysUpdateAddr;		/* 64 CF */
	u16 sysUpdateCount;		/* 68 */
	u16 kvVersion;			/* 6a */
	u32 kvAddr;			/* 6c */
	u32 fsAddr;			/* 70 */
	u32 smcConfigAddr;		/* 74 */
	u32 smcBootSize;		/* 78 */
	u32 smcBootAddr;		/* 7c */
};

/* a file system root entry */
struct fsent {
	char name[22];
	u16 block;
	u32 size;
	u32 time;
};

struct fsroot {
	u16 map[0x1000];
	struct fsent ent[256];
};

/* mobile files found by the scan; 0 is the fs root */
struct mobile {
	int found;
	u32 version;
	u32 page;
	u32 len;
	u32 offset;
	u32 spare;
};

void log_printf(int level, const char *fmt, ...);
unsigned int log_get_verbose(void);
unsigned short getBeU16(const unsigned char *p);
u32 getBeU32(const u8 *p);
long long getFileSize64(FILE *f);
int fseeko64(FILE *f, long long off, int whence);
u32 cfBestPairing(u8 *data, u32 size);
u32 cbGetPairing(u8 *cb);
int setPairing(u32 pairing);
int unscramble(u8 *buf, u32 len);
void setSmcKey(u8 *key);
int verifyExtended(u8 *buf, u32 size);
void setKvSalt(u8 *key);
void setKvAltSalt(u8 *key);
u32 shaSelfCheck(u8 *p);
int smcConfigOk(const u8 *smc);
int verifyFlashFile(int i);
void setInfoKey0(const u8 *key);
void setInfoKey1(const u8 *key);
void setInfoKey2(const u8 *key);
void setInfoKey3(const u8 *key);
void setInfoKey4(const u8 *key);
void setInfoKey5(const u8 *key);
void XeCryptShaUpdate(void *ctx, const u8 *buf, u32 len);
/* image_write.c */
int pageEccOk(u8 *data, u8 *spare);
int blockEccOk(u8 *blk, int bigBlock);
int blockErased(u8 *blk, int bigBlock);
int isErased(u8 *buf, int len);
u32 statisticsOffset(int bigBlock, int bbController, int mmc, u32 *page, u32 *spare);
u32 manufacturingOffset(int bigBlock, int bbController, int mmc, u32 *page, u32 *spare);

extern struct xebuild xb;
extern char separator[];

void buildCleanup(void);
int fsFindFile(const char *name, u32 *block, u32 *size, u32 *time, int quiet);
/* not inlined into imgGetSecurityFiles in the original (growth 39 is under
   max-inline-insns-auto here; something made it 40+ there) */
int loadFlashFile(int i, u32 block) __attribute__((noinline));
void listFlashFiles(void);
int fsGetFile(const char *name, u8 **buf, u32 *size, u32 *time);
int findAnchor(void);
int mmcFindMobiles(void);
u32 spareVersion(u8 *s);
void showMobilePages(void);
int scanMobiles(void);
void setFsOffset(void);
int findFsRoot(void);
void imgGetSecurityFiles(void);
void findSmcConfig(void);
int checkBlock(u8 *blk, int block, int numBlocks);
int addRemap(u32 block, int dest, int numBlocks);
int findFreeRemap(int numBlocks);
void remapBadBlocks(int numBlocks);
int notZeropair(void);
int spareLbaOk(int pages);
int copyMmcImage(u8 *raw);
int parseDump(u8 *raw);
u32 copyMuData(FILE *out, void *sha);
int detectController(u8 *raw, int size);
int checkHeader(const char *name, FILE *fp);
void getNonces(void);
int loadDump(const char *path);

/* gcc emits these in reverse */
static struct fsroot fsBuf;
struct fsroot *fs = &fsBuf;
char mobileName[] = "MobileA";
char zeropair[16] = "zeropair image";

static int dumpSize;
static int fsValid;
static u32 fsOffset;
static u8 anchor[0x200];
static struct mobile mobiles[10];

static int fsFind(const char *name, u32 *block, u32 *size, u32 *time, int quiet)
{
	int i;

	for (i = 0; i < 256; i++) {
		if (fs->ent[i].name[0] && !stricmp(fs->ent[i].name, name)) {
			*size = SWAP32(fs->ent[i].size);
			*block = SWAP16(fs->ent[i].block);
			if (time)
				*time = SWAP32(fs->ent[i].time);
			if (!quiet)
				log_printf(1, "%s found in sector 0x%x size 0x%x...", name, *block, *size);
			return 1;
		}
	}
	return 0;
}

void buildCleanup(void)
{
	int i;

	dumpSize = 0;
	if (xb.spare)
		free(xb.spare);
	if (xb.image)
		free(xb.image);
	xb.numBad = 0;
	xb.image = 0;
	xb.spare = 0;
	xb.nandMu = 0;
	xb.muChecked = 0;
	{
		struct netfile *m;
		for (m = xb.mobile; m != &xb.smc; m++)
			if (m->data)
				free(m->data);
	}
	for (i = 0; i < 4; i++) {
		if ((&xb.smc)[i].data)
			free((&xb.smc)[i].data);
		(&xb.smc)[i].size = 0;
	}
	if (xb.netkd.data)
		free(xb.netkd.data);
}

void getImageLdv(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.image;
	u32 size = SWAP32(h->fsAddr);
	u32 pairing;
	u32 ldv;

	if (!size)
		size = 0x10000;
	pairing = cfBestPairing(xb.image + SWAP32(h->sysUpdateAddr), size);
	if (!pairing)
		pairing = cbGetPairing(xb.image + SWAP32(h->kvAddr) + SWAP32(h->kvSize));
	if (pairing) {
		if (!xb.cfLdv)
			log_printf(1, "setting LDV from image to %d\n", pairing & 0xff);
		log_printf(1, "setting pairing data from image to 0x%06x\n", pairing >> 8);
		setPairing(pairing >> 8);
		ldv = pairing;
	} else if (xb.type == 6 || xb.type == 7) {
		log_printf(1, "Did not find a LDV value to use, setting it to 0 for devkit!\n");
		ldv = 0;
	} else if (xb.type == 8 || xb.type == 9) {
		log_printf(1, "Did not find a LDV value to use, setting it to 0 for testkit!\n");
		ldv = 0;
	} else {
		log_printf(0, "***** WARNING: could not find a non-zero CF LDV to use, setting it to 1 but that may be incorrect!\n");
		ldv = 1;
	}
	if (xb.cfLdv)
		log_printf(1, "LDV was already set to %d\n", xb.cfLdv);
	else if ((u8)ldv > 32)
		xb.cfLdv = 32;
	else
		xb.cfLdv = ldv;
}

void getImageSmc(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.image;
	u32 addr = SWAP32(h->smcBootAddr);
	u32 size = SWAP32(h->smcBootSize);

	if (addr != 0x800 && addr != 0x1000) {
		log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\n", addr);
		addr = 0x1000;
	}
	if (size != 0x3000 && size != 0x3800) {
		if (addr == 0x800) {
			size = 0x3800;
			log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3800\n", size);
		} else {
			size = 0x3000;
			log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3000\n", size);
		}
	}
	if (addr >= 528 * xb.numPages) {
		log_printf(1, "SMC at 0x%x of size 0x%x is not sane, skipping smc.bin in NAND image\n", addr, size);
		return;
	}
	xb.smc.data = malloc(size);
	if (!xb.smc.data) {
		log_printf(1, "Wasn't able to alloc 0x%x bytes memory for SMC bin, not using...\n", size);
		return;
	}
	xb.smc.size = size;
	memcpy(xb.smc.data, xb.image + addr, size);
	log_printf(1, "decrypting SMC at address 0x%x of size 0x%x\n", addr, size);
	if (unscramble(xb.smc.data, xb.smc.size)) {
		log_printf(1, "SMC decrypted OK, will use if no external smc.bin is provided\n");
		setSmcKey(xb.smc.data);
	} else {
		log_printf(1, "SMC did not decrypt, discarding it\n");
		free(xb.smc.data);
		xb.smc.data = 0;
		xb.smc.size = 0;
	}
}

void getImageKv(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.image;
	int addr = SWAP32(h->kvAddr);
	int size = SWAP32(h->kvSize);

	if (!addr) {
		log_printf(1, "KeyVault cannot be at 0x0, trying 0x4000\n", addr);
		addr = 0x4000;
	}
	if (size != 0x4000 && size != 0x8000) {
		log_printf(1, "KeyVault cannot be 0x%x bytes, using 0x4000\n", size);
		size = 0x4000;
	}
	if (addr + size < 528 * xb.numPages) {
		xb.kv.data = malloc(0x4000);
		if (xb.kv.data) {
			log_printf(1, "decrypting KeyVault at address 0x%x of size 0x%x\n", addr, 0x4000);
			xb.kv.size = 0x4000;
			memcpy(xb.kv.data, xb.image + addr, 0x4000);
			if (verifyExtended(xb.kv.data, xb.kv.size)) {
				log_printf(1, "keyvault decrypted OK, will use if no kv.bin is provided\n");
				setKvSalt(xb.kv.data + 16);
				if (size == 0x8000) {
					addr += 0x4000;
					xb.kvAlt.data = malloc(0x4000);
					if (xb.kvAlt.data) {
						log_printf(1, "decrypting alt KeyVault at address 0x%x of size 0x%x\n", addr, 0x4000);
						xb.kvAlt.size = 0x4000;
						memcpy(xb.kvAlt.data, xb.image + addr, 0x4000);
						if (verifyExtended(xb.kvAlt.data, xb.kvAlt.size)) {
							log_printf(1, "alt KeyVault decrypted OK, will use if no kv_alt.bin is provided\n");
							setKvAltSalt(xb.kvAlt.data + 16);
						} else {
							log_printf(1, "alt KeyVault decrypt failed, discarding\n");
							free(xb.kvAlt.data);
							xb.kvAlt.data = 0;
							xb.kvAlt.size = 0;
						}
					} else
						log_printf(1, "Wasn't able to alloc 0x4000 bytes memory for alt KeyVault bin, not using...\n");
				}
			} else {
				log_printf(1, "keyvault decrypt failed, discarding\n");
				free(xb.kv.data);
				xb.kv.data = 0;
				xb.kv.size = 0;
			}
		} else
			log_printf(1, "Wasn't able to alloc 0x4000 bytes memory for KeyVault bin, not using...\n");
	} else
		log_printf(1, "KeyVault at address 0x%x of size 0x4000 is not sane, skipping KeyVault in NAND image\n", addr);
}

void getImageMobiles(void)
{
	int i;
	char name[30];
	u32 off, len;

	for (i = 0; i < 9; i++) {
		struct mobile *m = &mobiles[i + 1];

		if (!m->found)
			continue;
		xb.mobile[i].data = malloc(m->len);
		if (xb.mobile[i].data) {
			mobileName[6] = 'B' + i;
			sprintf(name, "%s.dat", mobileName);
			log_printf(1, "extracting %s from page 0x%x (offset 0x%x), size %d (0x%x) bytes\n",
				   name, m->page, m->offset, m->len, m->len);
			len = m->len;
			memcpy(xb.mobile[i].data, xb.image + m->offset, len);
			xb.mobile[i].size = len;
		} else
			log_printf(1, "Unable to allocate memory for %s 0x%x bytes\n", name, m->len);
	}
	off = statisticsOffset(xb.bigBlock, 0, xb.mmc, 0, 0);
	if (!isErased(xb.image + off, 0x1000)) {
		log_printf(1, "Statistics.settings found at offset 0x%x, size %d (0x%x) bytes\n", off, 0x1000, 0x1000);
		xb.mobile[9].data = malloc(0x1000);
		if (xb.mobile[9].data) {
			memcpy(xb.mobile[9].data, xb.image + off, 0x1000);
			xb.mobile[9].size = 0x1000;
		} else
			log_printf(1, "Unable to allocate memory for Statistics.settings 0x%x bytes\n", 0x1000);
	}
	off = manufacturingOffset(xb.bigBlock, 0, xb.mmc, 0, 0);
	if (!isErased(xb.image + off, 0x1000)) {
		log_printf(1, "Manufacturing.data found at offset 0x%x, size %d (0x%x) bytes\n", off, 0x1000, 0x1000);
		xb.mobile[10].data = malloc(0x1000);
		if (!xb.mobile[10].data)
			log_printf(1, "Unable to allocate memory for Manufacturing.data 0x%x bytes\n", 0x1000);
		else {
			memcpy(xb.mobile[10].data, xb.image + off, 0x1000);
			xb.mobile[10].size = 0x1000;
		}
	}
}

void getNetKd(void)
{
	u8 *img, *p;
	u32 ver;

	xb.netkd.data = 0;
	if (getBeU16(xb.image + 0x80) != 0xca4a)
		return;
	img = xb.image;
	p = img + 0x80;
	ver = getBeU32(img + 0x90);
	xb.netkd.size = getBeU32(xb.image + 0x8c);
	log_printf(1, "netKd info found, size 0x%x\n", xb.netkd.size);
	log_printf(1, "    version : 0x%x\n", ver);
	if (ver == 1) {
		log_printf(1, "    xbox IP : %d.%d.%d.%d\n", img[0x94], img[0x95], img[0x96], img[0x97]);
		log_printf(1, "    xbox MAC: %02x:%02x:%02x:%02x:%02x\n", img[0x98], img[0x99], img[0x9a], img[0x9b], img[0x9c], img[0x9d]);
		log_printf(1, "    port    : %d\n", getBeU16(img + 0x9e));
		log_printf(1, "    host IP : %d.%d.%d.%d\n", img[0xa0], img[0xa1], img[0xa2], img[0xa3]);
	}
	xb.netkd.data = malloc(xb.netkd.size);
	if (xb.netkd.data)
		memcpy(xb.netkd.data, p, xb.netkd.size);
}

int loadFlashFile(int i, u32 block)
{
	u32 off = fsOffset + (block << 14);
	u32 left = xb.flashSize[i];
	u32 done = 0;

	xb.flashBuf[i] = calloc(left, 1);
	while (left > 0x4000) {
		memcpy(xb.flashBuf[i] + done, xb.image + off, 0x4000);
		left -= 0x4000;
		done += 0x4000;
		block = SWAP16(fs->map[block]) & 0x1fff;
		off = fsOffset + (block << 14);
	}
	if (left)
		memcpy(xb.flashBuf[i] + done, xb.image + off, left);
	return verifyFlashFile(i);
}

int fsFindFile(const char *name, u32 *block, u32 *size, u32 *time, int quiet)
{
	if (fsValid == 1)
		return fsFind(name, block, size, time, quiet);
	return 0;
}

void listFlashFiles(void)
{
	int i;

	if (fsValid != 1)
		return;
	for (i = 0; i < 256; i++) {
		struct fsent *e = &fs->ent[i];
		u32 block;

		if (!e->name[0])
			continue;
		block = SWAP16(e->block);
		log_printf(1, "sector: 0x%04x offset: 0x%08x size: 0x%08x timestamp: 0x%08x name: %s\n",
			   block, fsOffset + (block << 14), SWAP32(e->size), SWAP32(e->time), e->name);
	}
}

int fsGetFile(const char *name, u8 **buf, u32 *size, u32 *time)
{
	u32 block, len, t, off, left, done;
	u8 *p;

	if (fsValid != 1)
		return 0;
	if (!fsFind(name, &block, &len, &t, 1))
		return 0;
	off = fsOffset + (block << 14);
	p = calloc(len, 1);
	left = len;
	done = 0;
	while (left > 0x4000) {
		memcpy(p + done, xb.image + off, 0x4000);
		left -= 0x4000;
		done += 0x4000;
		block = SWAP16(fs->map[block]) & 0x1fff;
		off = fsOffset + (block << 14);
	}
	if (left)
		memcpy(p + done, xb.image + off, left);
	*buf = p;
	*size = len;
	*time = t;
	return 1;
}

int findAnchor(void)
{
	u32 v0, v1;
	int ok0, ok1;

	log_printf(1, "attempting to find valid anchor block\n");
	v0 = getBeU32(xb.image + 0x2fe8018);
	v1 = getBeU32(xb.image + 0x2fec018);
	ok0 = shaSelfCheck(xb.image + 0x2fe8000);
	if (ok0)
		log_printf(1, "anchor block v %d at 0x2fe8000 is valid\n", v0);
	else
		log_printf(1, "anchor block at 0x2fe8000 is invalid\n");
	ok1 = shaSelfCheck(xb.image + 0x2fec000);
	if (ok1)
		log_printf(1, "anchor block v %d at 0x2fec000 is valid\n", v1);
	else
		log_printf(1, "anchor block at 0x2fec000 is invalid\n");
	if (ok0 && (!ok1 || v0 >= v1)) {
		log_printf(1, "anchor block v %d at 0x2fe8000 is selected\n", v0);
		memcpy(anchor, xb.image + 0x2fe8000, 0x200);
		return 1;
	}
	if (ok1) {
		log_printf(1, "anchor block v %d at 0x2fec000 is selected\n", v1);
		memcpy(anchor, xb.image + 0x2fec000, 0x200);
		return 1;
	}
	return 0;
}

int mmcFindMobiles(void)
{
	int i;
	u16 block, len;

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

u32 spareVersion(u8 *s)
{
	u32 lo;

	if (xb.bigBlock)
		lo = s[5];
	else if (xb.bbController)
		lo = s[0];
	else
		lo = s[2];
	return (s[3] << 8) | (s[4] << 16) | (s[6] << 24) | lo;
}

void showMobilePages(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.image;
	u32 end, page;
	u32 off;
	u8 fsType;

	if (!xb.bigBlock) {
		end = xb.numPages - 1152;
		fsType = 48;
	} else {
		end = xb.numPages - 9216;
		fsType = 44;
	}
	log_printf(2, separator);
	log_printf(2, "Showing all pages with mobile info:\n");
	log_printf(2, separator);
	page = SWAP32(h->sysUpdateAddr) >> 9;
	page = (page & 0x1f) ? (page & ~0x1f) + 32 : page;
	off = page << 9;
	log_printf(2, "starting mobile scan at page 0x%x (offset 0x%x) of 0x%x pages (0x%x total)\n",
		   page, off, end, xb.numPages);
	for (; page < end; page++, off += 512) {
		u8 *s = xb.spare + page * 16;
		u8 t = s[12] & 0x3f;
		int letter, i;
		u32 ver;
		short len;

		if (t == fsType) {
			letter = 'A';
		len = 0x4000;
		} else if (t >= 0x31 && t <= 0x39) {
			letter = t + 17;
		len = s[7] + (s[8] << 8);
		} else
			continue;
		ver = spareVersion(s);
		log_printf(2, "mobile%c.dat ver %02d offset 0x%08x (dump:0x%08x) count 0x%02x len 0x%04x page 0x%08x ",
			   letter, ver, off, page * 528, s[9], (u16)len, page);
		for (i = 0; i < 16; i++)
			log_printf(2, "%02x ", xb.spare[page * 16 + i]);
		if (len < 0)
			log_printf(2, "(DELETE)\n");
		else
			log_printf(2, "\n");
	}
	log_printf(2, separator);
}

int scanMobiles(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.image;
	u32 end, page, off;
	u8 fsType;

	if (!xb.bigBlock) {
		end = xb.numPages - 1152;
		fsType = 48;
	} else {
		end = xb.numPages - 9216;
		fsType = 44;
	}
	if (log_get_verbose() == 2) {
		log_printf(2, "\n");
		showMobilePages();
	}
	page = SWAP32(h->sysUpdateAddr) >> 9;
	page = (page & 0x1f) ? (page & ~0x1f) + 32 : page;
	while (page < end) {
		u8 *s = xb.spare + page * 16;
		u8 t = s[12] & 0x3f;
		int n, i;
		u16 len;
		u32 ver, lo;

		if (t == fsType) {
			n = 0;
			len = 0x4000;
		} else if (t >= 0x31 && t <= 0x39) {
			n = t - 48;
			len = s[7] + (s[8] << 8);
		} else
			goto next;
		ver = spareVersion(s);
		off = page << 9;
		if (log_get_verbose() == 2) {
			log_printf(2, "mobile%c.dat ver %02d offset 0x%08x (dump:0x%08x) count 0x%02x len 0x%04x page 0x%08x ",
				   n + 'A', ver, off, page * 528, s[9], len, page);
			for (i = 0; i < 16; i++)
				log_printf(2, "%02x ", xb.spare[page * 16 + i]);
			if (len & 0x8000)
				log_printf(2, "(DELETE)\n");
			else
				log_printf(2, "\n");
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
			if (len & 0x8000) {
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
		if (xb.bigBlock)
			page = (page + 3) & ~3;
		continue;
next:
		page++;
		page = (page & 0x1f) ? (page & ~0x1f) + 32 : page;
	}
	return mobiles[0].found;
}

void setFsOffset(void)
{
	u32 meta;

	fsOffset = 0;
	if (!xb.bigBlock)
		return;
	meta = xb.spare[mobiles[0].spare + 8] << 5;
	fsOffset = (3808 - meta) << 14;
	log_printf(1, "bigblock file system offset set to 0x%x fsb: %x meta: %x lbaend: %x\n",
		   fsOffset, 3808 - meta, meta, 3808);
}

int findFsRoot(void)
{
	int found, i;
	u8 *src;
	

	log_printf(1, "Scanning for mobile data and fsroot...");
	if (xb.mmc)
		found = mmcFindMobiles();
	else
		found = scanMobiles();
	if (!found) {
		log_printf(1, "\n\n***** ERROR! Could not find fsroot!\n");
		return 0;
	}
	puts("done! fsroot found ok!");
	setFsOffset();
	log_printf(1, "Mobiles found:\n");
	for (i = 0; i < 10; i++) {
		if (mobiles[i].found) {
			if (i)
				log_printf(1, "    mobile%c.dat version %02d found at offset 0x%08x len 0x%04x page 0x%08x\n", 'A' + i, mobiles[i].version, mobiles[i].offset, mobiles[i].len, mobiles[i].page);
			else
				log_printf(1, "    fsroot      version %02d found at offset 0x%08x len 0x%04x page 0x%08x\n", mobiles[i].version, mobiles[i].offset, mobiles[i].len, mobiles[i].page);
		}
	}
	src = xb.image + mobiles[0].offset;
	for (i = 0; i < 16; i++) {
		memcpy((u8 *)fsBuf.map + i * 512, src + i * 1024, 512);
		memcpy((u8 *)fsBuf.ent + i * 512, src + i * 1024 + 512, 512);
	}
	fsValid = 1;
	return found;
}

inline void imgGetSecurityFiles(void)
{
	u32 i, block;

	log_printf(1, "seeking security files...\n");
	for (i = 0; i < xb.numFlashFiles; i++)
		if (xb.flashFiles[i][0] && fsFindFile(xb.flashFiles[i], &block, &xb.flashSize[i], &xb.flashTime[i], 0))
			loadFlashFile(i, block);
	log_printf(1, "done!\n");
}

void findSmcConfig(void)
{
	u32 off, end;

	if (xb.mmc) {
		off = 0x2ffc000;
		end = 0x3000000;
	} else if (xb.bigBlock) {
		off = 0x3be0000;
		end = 0x4000000;
	} else {
		end = xb.imageSize;
		if (end == 0x1000000)
			off = 0xf7c000;
		else if (end == 0x4000000)
			off = 0x3dfc000;
		else
			off = 0;
	}
	log_printf(1, "seeking smc config in dump...");
	for (; off < end; off += 512) {
		if (!smcConfigOk(xb.image + off))
			continue;
		xb.smcConfig.data = malloc(0x400);
		if (!xb.smcConfig.data) {
			log_printf(1, "found at offset 0x%x! Unable to allocate 0x400 bytes of memory for smc config, skipping\n", off);
			off = end;
			continue;
		}
		log_printf(1, "found at offset 0x%x! Using if no smc config is provided.\n", off);
		memcpy(xb.smcConfig.data, xb.image + off, 0x400);
		xb.smcConfig.size = 0x400;
		off = end;
	}
	if (!xb.smcConfig.data)
		log_printf(1, "not found!\n", off);
}

int checkBlock(u8 *b, int block, int numBlocks)
{
	int lba;

	if (blockErased(b, xb.bigBlock))
		return -2;
	if (!xb.bigBlock) {
		if (b[517] != 0xff || b[8965] != 0xff)
			return -1;
		if (xb.bbController) {
			if (block && block == b[512] + (b[513] & 0xf) * 256) {
				lba = -6;
				goto out;
			}
			lba = b[513] + (b[514] & 0xf) * 256;
		} else {
			lba = b[512] + (b[513] & 0xf) * 256;
			if (block && block == b[513] + (b[514] & 0xf) * 256) {
				lba = -6;
				goto out;
			}
		}
		if (lba >= numBlocks - 1)
			lba = -3;
		else if (lba > 0 && block < numBlocks - 34 && block != lba)
			lba = -3;
	} else {
		if (b[512] != 0xff || b[68096] != 0xff)
			return -1;
		lba = b[513] + (b[514] & 0xf) * 256;
		if (lba >= numBlocks - 1)
			lba = -3;
		else if (xb.muChecked) {
			if (lba && block < numBlocks - 34 && lba != block)
				lba = -3;
		} else {
			u8 t = b[524] & 0x3f;

			if (t && t <= 0x29) {
				log_printf(0, "\n\n****************  WARNING  *************************\n");
				log_printf(0, "  nanddump.bin has NAND memory unit data, make\n");
				log_printf(0, "  sure you back up any important data off the\n");
				log_printf(0, "  internal MU before flashing a new image!\n");
				if (xb.bootFlags & 0x10000000) {
					log_printf(0, "\n  xeBuild will attempt to keep this data, but\n");
					log_printf(0, "  many things could cause it to be invalid/corrupt.\n");
				}
				log_printf(0, "****************************************************\n\n");
				xb.muChecked = 1;
				xb.nandMu = 1;
			}
		}
	}
out:
	if (!(xb.bootFlags & 0x80000000) && !blockEccOk(b, xb.bigBlock))
		return -4;
	return lba;
}

int addRemap(u32 block, int dest, int numBlocks)
{
	u32 i;
	int found = 0;
	u32 b = block;	/* unused; puts block before the loads in compares */

	for (i = 0; i < xb.numBad; i++) {
		if (block == xb.badBlocks[i] && xb.badRemap[i] == -1 && dest < numBlocks) {
			log_printf(1, "block 0x%x was remapped to block 0x%x at remap instance %d\n", block, dest, i);
			xb.badRemap[i] = dest;
			found = 1;
		}
	}
	if (found)
		return 1;
	if (xb.numBad >= 32) {
		log_printf(1, "MAX REMAPS of 32 exceeded, remapping disabled and image rejected as faulty!\n");
		return 0;
	}
	if (dest != -1)
			log_printf(1, "block 0x%x was remapped to block 0x%x, entering remap instance %d\n", block, dest, xb.numBad + 1);
		xb.badBlocks[xb.numBad] = block;
		xb.badRemap[xb.numBad] = dest;
		xb.numBad++;
	return 1;
}

int findFreeRemap(int numBlocks)
{
	int b, used;
	u32 i;

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

void remapBadBlocks(int numBlocks)
{
	u32 i;
	int b;

	log_printf(1, "cleaning up stray remaps\n");
	for (i = 0; i < xb.numBad; i++) {
		if (xb.badRemap[i] != -1)
			continue;
		if (xb.badBlocks[i] >= numBlocks - 32) {
			log_printf(1, "block 0x%x had no need of remap, it's in the wear area\n", xb.badBlocks[i]);
			xb.badRemap[i] = -5;
			continue;
		}
		b = findFreeRemap(numBlocks);
		if (b) {
			xb.badRemap[i] = b;
			log_printf(1, "block 0x%x had no remap, assigning remap block 0x%x\n", xb.badBlocks[i], b);
		} else
			log_printf(1, "block 0x%x had no remap, and I could not assign one!\n", xb.badBlocks[i]);
	}
	log_printf(1, "done!\n");
}

int notZeropair(void)
{
	return memcmp(zeropair, xb.image + 16, 14) != 0;
}

int spareLbaOk(int pages)
{
	int i;

	for (i = 1; i < pages; i++)
		if (memcmp(xb.spare, xb.spare + i * 16, 3))
			return 0;
	return 1;
}

int copyMmcImage(u8 *raw)
{
	xb.numBad = 0;
	memcpy(xb.image, raw, xb.imageSize);
	if (notZeropair())
		return 1;
	log_printf(0, "\n\n***** ERROR: nanddump.bin is a ZEROPAIR/XELL image, discarding\n");
	return 0;
}

int parseDump(u8 *raw)
{
	int ppb = xb.bigBlock ? 256 : 32;
	int blocks = xb.numPages / ppb;
	int blk, dst, p;
	u32 i;
	u8 *src;

	if (xb.numPages % ppb) {
		log_printf(0, "UNEXPECTED DUMP PARSE ERROR: %d pages cannot divide by %d!\n", xb.numPages, ppb);
		return 0;
	}
	log_printf(1, "parsing dump into user and spare...\n");
	for (blk = 0; blk < blocks; blk++) {
		src = raw + blk * 528 * ppb;
		dst = checkBlock(src, blk, blocks);
		switch (dst) {
		case -2:
			continue;
		case -1:
			log_printf(1, "bad block at 0x%x (raw offset 0x%x), block ignored\n", blk, src - raw);
			if (!addRemap(blk, -1, blocks))
				return 0;
			continue;
		case -3:
			log_printf(0, "***** WARNING: nanddump.bin has a bad LBA at block 0x%x (raw offset 0x%x), block LBA ignored\n", blk, src - raw);
			continue;
		case -6:
			log_printf(0, "***** WARNING: nanddump.bin has a mixed controller LBA at block 0x%x (raw offset 0x%x), block ignored\n", blk, src - raw);
			log_printf(0, "               this is likely caused by previously using jaspersb on a jasper type console!\n", blk, src - raw);
			continue;
		case -4:
			log_printf(1, "ECD error at block 0x%x (raw offset 0x%x), block will be remapped\n", blk, src - raw);
			if (!addRemap(blk, -1, blocks))
				return 0;
			dst = blk;
			break;
		default:
			if (dst != blk) {
				if (blk < blocks - 32) {
					log_printf(0, "***** WARNING: ignoring possible remap of block 0x%x to block 0x%x\n", blk, dst);
					log_printf(0, "               this dump may have some bad data!\n", blk, dst);
					dst = blk;
				} else
					log_printf(1, "copying nanddump data from block 0x%x to block 0x%x for file extraction integrity\n", blk, dst);
			}
		}
		if (blk == 0) {
			if (!notZeropair()) {
				log_printf(0, "\n\n***** ERROR: nanddump.bin is a ZEROPAIR/XELL image, discarding\n");
				return 0;
			}
			if (!spareLbaOk(ppb)) {
				log_printf(0, "\n\n***** ERROR: nanddump.bin has mixed LBA in the same block which usually occurs\n");
				log_printf(0, "             due to an improper nandpro write method, discarding\n");
				return 0;
			}
		}
		for (p = 0; p < ppb; p++) {
			memcpy(xb.image + (dst * ppb + p) * 512, src + p * 528, 512);
			memcpy(xb.spare + (dst * ppb + p) * 16, src + p * 528 + 512, 16);
		}
		if (dst != blk && !addRemap(dst, blk, blocks))
			return 0;
	}
	log_printf(1, "done!\n");
	if (xb.bootFlags & 0x40000000) {
		if (xb.numBad) {
			log_printf(1, "Discarding remap data as NOREMAP was specified!\n");
			xb.numBad = 0;
		}
	} else if (xb.numBad) {
		remapBadBlocks(blocks);
		log_printf(1, "--remap summary--\n");
		for (i = 0; i < xb.numBad; i++) {
			if (xb.badRemap[i] == -5)
				log_printf(1, "%d: source: 0x%04x dest: (NONE/BAD)\n", i, xb.badBlocks[i]);
			else
				log_printf(1, "%d: source: 0x%04x dest: 0x%04x\n", i, xb.badBlocks[i], xb.badRemap[i]);
		}
		log_printf(1, "-----------------\n");
	}
	return 1;
}

u32 copyMuData(FILE *out, void *sha)
{
	char name[0x400];
	FILE *fp;
	u8 *buf;
	int len;

	if (dumpSize != dumpSize / 0x4200000 * 0x4200000) {
		log_printf(0, "size is not a multiple of %d bytes, not copying data..\n", 0x4200000);
		return 0;
	}
	if (dumpSize <= 0x4200000) {
		log_printf(0, "no data to copy..\n");
		return 0;
	}
	strcpy(name, xb.baseDir);
	strcat(name, "nanddump.bin");
	fp = fopen(name, "rb");
	if (!fp) {
		log_printf(0, "could not re-open '%s' for reading, not copying data..\n", name);
		return 0;
	}
	if (fseek(fp, 0x4200000, SEEK_END)) {
		log_printf(0, "could not seek to 0x%x, not copying data..\n", 0x4200000);
		fclose(fp);
		return 0;
	}
	len = dumpSize - 0x4200000;
	buf = malloc(len);
	if (!buf) {
		log_printf(0, "could not allocate 0x%x byte buffer, not copying data..\n", len);
		fclose(fp);
		return 0;
	}
	log_printf(1, "reading nanddump.bin...\n");
	fread(buf, dumpSize - 0x4200000, 1, fp);
	fclose(fp);
	log_printf(1, "writing nanddump.bin MU area to output file...");
	if (sha)
		XeCryptShaUpdate(sha, buf, dumpSize - 0x4200000);
	fwrite(buf, dumpSize - 0x4200000, 1, out);
	free(buf);
	return 1;
}

int detectController(u8 *raw, int size)
{
	int i, n;
	u32 found;

	if (size == 0x3000000) {
		log_printf(1, "\tNAND dump is from a mmc machine\n");
		log_printf(1, "\tNAND dump uses big block controller\n");
		xb.bbController = 1;
		xb.bigBlock = 0;
		xb.muChecked = 1;
		xb.mmc = 1;
		return 1;
	}
	if (raw[512] == 0xff) {
		log_printf(1, "\tNAND dump is from a big block machine\n");
		log_printf(1, "\tNAND dump uses big block controller\n");
		if (size < 0x4200000) {
			log_printf(0, "***** WARNING: NAND dump too small to be from a big block machine, discarding dump!\n");
			return 0;
		}
		xb.bigBlock = 1;
		xb.bbController = 1;
		return 1;
	}
	if (raw[517] != 0xff) {
		log_printf(0, "***** WARNING: NAND dump does not appear to have a good block at block 0, discarding dump!\n");
		return 0;
	}
	n = size / 16896;
	log_printf(1, "\tNAND dump is from a small block machine\n");
	xb.bigBlock = 0;
	xb.muChecked = 1;
	found = 0;
	for (i = 1; i < n; i++) {
		u8 *b = raw + i * 16896;

		if (b[517] != 0xff || b[513] == 0xff)
			continue;
		if (b[513] + (b[514] & 0xf) * 256 == i) {
			i = n;
			log_printf(1, "\tNAND dump uses big block controller\n");
			xb.bbController = 1;
			found = 1;
		} else if (b[512] + (b[513] & 0xf) * 256 == i) {
			i = n;
			log_printf(1, "\tNAND dump uses small block controller\n");
			xb.bbController = 0;
			found = 1;
		}
	}
	return found;
}

int checkHeader(const char *name, FILE *fp)
{
	struct flashhdr hdr;
	u8 page[0x210];
	u32 magic;
	long long size;

	size = getFileSize64(fp);
	log_printf(1, "%s file size: 0x%llx\n", name, size);
	if (size < 0x1080000) {
		log_printf(0, "******* ERROR loading '%s', file size 0x%llx is not large enough\n", name, size);
		return 0;
	}
	fread(&hdr, 0x80, 1, fp);
	rewind(fp);
	if (SWAP16(hdr.magic) != 0xff4f) {
		log_printf(0, "******* ERROR loading '%s', flash header magic is incorrect\n", name);
		return 0;
	}
	if (size < SWAP32(hdr.entry)) {
		log_printf(0, "******* ERROR loading '%s', flash header Entry is too large\n", name);
		return 0;
	}
	if (size < SWAP32(hdr.size)) {
		log_printf(0, "******* ERROR loading '%s', flash header Size is too large\n", name);
		return 0;
	}
	if (SWAP32(hdr.kvSize) > 0x8000) {
		log_printf(0, "******* ERROR loading '%s', flash header KeyVaultSize is too large\n", name);
		return 0;
	}
	/* as `||`, ifcombine makes it `a | b` and forwprop puts the size test
	   last; the asm keeps two jumps in this order */
	if (size < SWAP32(hdr.sysUpdateAddr))
		goto badSysUpdate;
	__asm__("");
	if (SWAP32(hdr.size) > SWAP32(hdr.sysUpdateAddr)) {
badSysUpdate:
		log_printf(0, "******* ERROR loading '%s', flash header SysUpdateAddr is malformed\n", name);
		return 0;
	}
	if (SWAP16(hdr.sysUpdateCount) != 2)
		log_printf(0, "******* ERROR loading '%s', flash header SysUpdateCount is not 2, continuing anyway\n", name);
	if (SWAP16(hdr.kvVersion) != 0x712)
		log_printf(0, "******* ERROR loading '%s', flash header KeyVaultVersion is not 0x0712, continuing anyway\n", name);
	if (size < SWAP32(hdr.kvAddr)) {
		log_printf(0, "******* ERROR loading '%s', flash header KeyVaultAddr is too large\n", name);
		return 0;
	}
	if (size < SWAP32(hdr.fsAddr)) {
		log_printf(0, "******* ERROR loading '%s', flash header FileSystemAddr is too large\n", name);
		return 0;
	}
	if (SWAP32(hdr.smcConfigAddr))
		log_printf(0, "******* ERROR loading '%s', flash header SmcConfigAddr is not 0, continuing anyway\n", name);
	if (SWAP32(hdr.smcBootSize) != 0x3000 && SWAP32(hdr.smcBootSize) != 0x3800) {
		log_printf(0, "******* ERROR loading '%s', flash header SmcBootSize is not 0x3000 or 0x3800\n", name);
		return 0;
	}
	if (size < SWAP32(hdr.smcBootAddr)) {
		log_printf(0, "******* ERROR loading '%s', flash header SmcBootAddr is too large\n", name);
		return 0;
	}
	if (size > 0x3000000) {
		fseeko64(fp, 0x3000000, SEEK_SET);
		fread(&magic, 4, 1, fp);
		rewind(fp);
		if (getBeU32((u8 *)&magic) == 0x58544146) {
			log_printf(1, "FATX magic found, truncating load size to 0x3000000 bytes for mmc consoles\n");
			size = 0x3000000;
		} else {
			rewind(fp);
			fread(page, 0x210, 1, fp);
			rewind(fp);
			if (!pageEccOk(page, page + 512)) {
				log_printf(1, "First page does not contain a valid ECC, assuming this is an mmc dump and truncating load size to 0x3000000 bytes!\n");
				size = 0x3000000;
			} else if (size > 0x4200000) {
				log_printf(1, "First page contains a valid ECC, assuming this is a big block flash overdump and truncating load size to 0x4200000 bytes\n");
				size = 0x4200000;
			}
		}
	}
	log_printf(1, "nanddump header checks passed OK!\n");
	return size;
}

void getNonces(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.image;
	u32 off = SWAP32(h->entry);
	u8 *p;

	if (off >= xb.imageSize) {
		log_printf(1, "**** Warning: error getting CB/CBA Nonce offset, aborting!\n");
		return;
	}
	p = xb.image + off;
	if ((ROT16(*(u16 *)p) & 0x43ff) != 0x4342) {
		log_printf(1, "**** Warning: error getting CB/CBA Nonce, aborting!\n");
		return;
	}
	setInfoKey0(xb.image + off + 16);
	off += (SWAP32(*(u32 *)(p + 12)) + 15) & ~15;
	if (p[6] & 8) {
		if (off >= xb.imageSize) {
			log_printf(1, "**** Warning: error getting CBB Nonce offset, aborting!\n");
			return;
		}
		p = xb.image + off;
		if ((ROT16(*(u16 *)p) & 0x43ff) != 0x4342) {
			log_printf(1, "**** Warning: error getting CBB Nonce, offset 0x%x aborting!\n", off);
			return;
		}
		setInfoKey1(xb.image + off + 16);
		off += (SWAP32(*(u32 *)(p + 12)) + 15) & ~15;
	}
	if (off >= xb.imageSize) {
		log_printf(1, "**** Warning: error getting CD Nonce offset, aborting!\n");
		return;
	}
	p = xb.image + off;
	if ((ROT16(*(u16 *)p) & 0x43ff) != 0x4344) {
		log_printf(1, "**** Warning: error getting CD Nonce, offset 0x%x aborting!\n", off);
		return;
	}
	setInfoKey2(xb.image + off + 16);
	off += (SWAP32(*(u32 *)(p + 12)) + 15) & ~15;
	if (off >= xb.imageSize) {
		log_printf(1, "**** Warning: error getting CE Nonce offset, aborting!\n");
		return;
	}
	if ((ROT16(*(u16 *)(xb.image + off)) & 0x43ff) != 0x4345) {
		log_printf(1, "**** Warning: error getting CE Nonce, offset 0x%x aborting!\n", off);
		return;
	}
	setInfoKey3(xb.image + off + 16);
	off = SWAP32(h->sysUpdateAddr);
	if (off >= xb.imageSize) {
		log_printf(1, "**** Warning: error getting CF Nonce offset, aborting!\n");
		return;
	}
	p = xb.image + off;
	if ((ROT16(*(u16 *)p) & 0x43ff) != 0x4346) {
		log_printf(1, "**** Warning: error getting CF Nonce, offset 0x%x aborting!\n", off);
		return;
	}
	setInfoKey4(xb.image + off + 32);
	off += (SWAP32(*(u32 *)(p + 12)) + 15) & ~15;
	if (off >= xb.imageSize) {
		log_printf(1, "**** Warning: error getting CG Nonce offset, aborting!\n");
		return;
	}
	if ((ROT16(*(u16 *)(xb.image + off)) & 0x43ff) != 0x4347) {
		log_printf(1, "**** Warning: error getting CG Nonce, offset 0x%x aborting!\n", off);
		return;
	}
	setInfoKey5(xb.image + off + 16);
	xb.f020 = 0;
}

int loadDump(const char *path)
{
	char name[0x400];
	FILE *fp;
	int size, ret;
	u32 rawSize, pages;
	u8 *raw;

	if (path)
		strcpy(name, path);
	else {
		strcpy(name, xb.baseDir);
		strcat(name, "nanddump.bin");
	}
	buildCleanup();
	log_printf(1, "\n------ Checking %s ------\n", name);
	fp = fopen(name, "rb");
	if (!fp) {
		log_printf(1, "NAND dump not found at '%s'\n", name);
		return 0;
	}
	size = checkHeader(name, fp);
	if (!size) {
		buildCleanup();
		return 0;
	}
	dumpSize = size;
	if (size == 0x3000000) {
		xb.numPages = 0x18000;
		rawSize = 0x3000000;
	} else if (size != size / 528 * 528) {
		log_printf(1, "NAND dump '%s' is not a correct dump size (0x%x bytes), ignoring\n", name, size);
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
				log_printf(1, "NAND dump '%s' is not a correct raw (with ecc) dump size (0x%x bytes), ignoring\n", name, size);
				fclose(fp);
				return 0;
			}
		}
		xb.numPages = pages;
	}
	raw = malloc(rawSize);
	if (!raw) {
		log_printf(0, "******* ERROR loading '%s', unable to allocate memory\n", name);
		fclose(fp);
		return 0;
	}
	log_printf(1, "Loading NAND dump (0x%x bytes)...", size);
	fread(raw, rawSize, 1, fp);
	fclose(fp);
	log_printf(1, "done!\n", name);
	xb.imageSize = xb.numPages << 9;
	xb.spareSize = xb.numPages * 16;
	xb.image = malloc(xb.numPages << 9);
	xb.spare = malloc(xb.numPages * 16);
	if (!xb.image || !xb.spare) {
		log_printf(0, "******* ERROR loading '%s', unable to allocate user/spare memory\n", name);
		buildCleanup();
		free(raw);
		return 0;
	}
	memset(xb.image, 0xff, xb.imageSize);
	memset(xb.spare, 0xff, xb.spareSize);
	log_printf(1, "Detecting NAND controller type from dump data...\n");
	if (!detectController(raw, size)) {
		log_printf(0, "******* ERROR loading '%s', unable to determine NAND controller type!\n", name);
		ret = 0;
	} else {
		if (xb.mmc)
			ret = copyMmcImage(raw);
		else
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
	}
	free(raw);
	return ret;
}

/* image_read: parsing an existing NAND image (nanddump.bin): sectors, pairing, LDV, smc.bin.
   Mixed object: the functions here are spliced into image_read.s
   (re/splice.py), which still holds the rest and the data, so strings
   and variables are the .s's.  wip/app/image_read.c is the whole
   draft; wip/irmixed.py makes this file from it. */
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
u32 copyMmcImage(u8 *raw);
int parseDump(u8 *raw);
u32 copyMuData(FILE *out, void *sha);
int detectController(u8 *raw, int size);
int checkHeader(const char *name, FILE *fp);
void getNonces(void);
int loadDump(const char *path);

/* image_read.s's data */
static struct fsroot fsBuf;
extern struct fsroot *fs;
extern char mobileName[];
extern char zeropair[16];

extern int dumpSize;
static int fsValid;
static u32 fsOffset;
static u8 anchor[0x200];
static struct mobile mobiles[10];

/* strings in image_read.s */
extern const char ir_4521b8[];	/* "%s found in sector 0x%x size 0x%x..." */
extern const char ir_4521e0[];	/* "Did not find a LDV value to use, set..." */
extern const char ir_452220[];	/* "Did not find a LDV value to use, set..." */
extern const char ir_452260[];	/* "***** WARNING: could not find a non-..." */
extern const char ir_4522c4[];	/* "setting LDV from image to %d\n" */
extern const char ir_4522e4[];	/* "setting pairing data from image to 0..." */
extern const char ir_45230f[];	/* "LDV was already set to %d\n" */
extern const char ir_45276c[];	/* "Unable to allocate memory for %s 0x%..." */
extern const char ir_452799[];	/* "%s.dat" */
extern const char ir_4527a0[];	/* "extracting %s from page 0x%x (offset..." */
extern const char ir_4527e4[];	/* "Statistics.settings found at offset ..." */
extern const char ir_452824[];	/* "Unable to allocate memory for Statis..." */
extern const char ir_452864[];	/* "Manufacturing.data found at offset 0..." */
extern const char ir_4528a4[];	/* "Unable to allocate memory for Manufa..." */
extern const char ir_4528e1[];	/* "netKd info found, size 0x%x\n" */
extern const char ir_4528fe[];	/* "    version : 0x%x\n" */
extern const char ir_452912[];	/* "    xbox IP : %d.%d.%d.%d\n" */
extern const char ir_452930[];	/* "    xbox MAC: %02x:%02x:%02x:%02x:%0..." */
extern const char ir_452958[];	/* "    port    : %d\n" */
extern const char ir_45296a[];	/* "    host IP : %d.%d.%d.%d\n" */
extern const char ir_4529d0[];	/* "attempting to find valid anchor bloc..." */
extern const char ir_4529f8[];	/* "anchor block v %d at 0x2fe8000 is va..." */
extern const char ir_452a24[];	/* "anchor block at 0x2fe8000 is invalid..." */
extern const char ir_452a4c[];	/* "anchor block v %d at 0x2fec000 is va..." */
extern const char ir_452a78[];	/* "anchor block v %d at 0x2fec000 is se..." */
extern const char ir_452aa4[];	/* "anchor block at 0x2fec000 is invalid..." */
extern const char ir_452acc[];	/* "anchor block v %d at 0x2fe8000 is se..." */
extern const char ir_452bd8[];	/* "bigblock file system offset set to 0..." */
extern const char ir_452c20[];	/* "Scanning for mobile data and fsroot...." */
extern const char ir_452c47[];	/* "done! fsroot found ok!" */
extern const char ir_452c5e[];	/* "Mobiles found:\n" */
extern const char ir_452c70[];	/* "    fsroot      version %02d found a..." */
extern const char ir_452cbc[];	/* "    mobile%c.dat version %02d found ..." */
extern const char ir_452d0c[];	/* "\n\n***** ERROR! Could not find fsro..." */
extern const char ir_452d33[];	/* "seeking security files...\n" */
extern const char ir_452d4e[];	/* "done!\n" */
extern const char ir_452d55[];	/* "seeking smc config in dump..." */
extern const char ir_452d74[];	/* "found at offset 0x%x! Using if no sm..." */
extern const char ir_452db0[];	/* "found at offset 0x%x! Unable to allo..." */
extern const char ir_452e09[];	/* "not found!\n" */
extern const char ir_452f7c[];	/* "block 0x%x was remapped to block 0x%..." */
extern const char ir_452fb8[];	/* "block 0x%x was remapped to block 0x%..." */
extern const char ir_452ffc[];	/* "MAX REMAPS of 32 exceeded, remapping..." */
extern const char ir_453049[];	/* "cleaning up stray remaps\n" */
extern const char ir_453064[];	/* "block 0x%x had no remap, assigning r..." */
extern const char ir_45309c[];	/* "block 0x%x had no remap, and I could..." */
extern const char ir_4530d4[];	/* "block 0x%x had no need of remap, it'..." */
extern const char ir_45310c[];	/* "\n\n***** ERROR: nanddump.bin is a Z..." */
extern const char ir_45355c[];	/* "size is not a multiple of %d bytes, ..." */
extern const char ir_453594[];	/* "no data to copy..\n" */
extern const char ir_4535a7[];	/* "rb" */
extern const char ir_4535ac[];	/* "could not re-open '%s' for reading, ..." */
extern const char ir_4535e4[];	/* "could not seek to 0x%x, not copying ..." */
extern const char ir_453610[];	/* "could not allocate 0x%x byte buffer,..." */
extern const char ir_453649[];	/* "reading nanddump.bin...\n" */
extern const char ir_453664[];	/* "writing nanddump.bin MU area to outp..." */
extern const char ir_453810[];	/* "%s file size: 0x%llx\n" */
extern const char ir_453828[];	/* "******* ERROR loading '%s', file siz..." */
extern const char ir_45386c[];	/* "******* ERROR loading '%s', flash he..." */
extern const char ir_4538ac[];	/* "******* ERROR loading '%s', flash he..." */
extern const char ir_4538ec[];	/* "******* ERROR loading '%s', flash he..." */
extern const char ir_453928[];	/* "******* ERROR loading '%s', flash he..." */
extern const char ir_45396c[];	/* "******* ERROR loading '%s', flash he..." */
extern const char ir_4539b4[];	/* "******* ERROR loading '%s', flash he..." */
extern const char ir_453a0c[];	/* "******* ERROR loading '%s', flash he..." */
extern const char ir_453a68[];	/* "******* ERROR loading '%s', flash he..." */
extern const char ir_453aac[];	/* "******* ERROR loading '%s', flash he..." */
extern const char ir_453af4[];	/* "******* ERROR loading '%s', flash he..." */
extern const char ir_453b48[];	/* "******* ERROR loading '%s', flash he..." */
extern const char ir_453b98[];	/* "******* ERROR loading '%s', flash he..." */
extern const char ir_453bdc[];	/* "FATX magic found, truncating load si..." */
extern const char ir_453c28[];	/* "First page does not contain a valid ..." */
extern const char ir_453c9c[];	/* "First page contains a valid ECC, ass..." */
extern const char ir_453d18[];	/* "nanddump header checks passed OK!\n" */
extern const char ir_453d3c[];	/* "**** Warning: error getting CB/CBA N..." */
extern const char ir_453d78[];	/* "**** Warning: error getting CB/CBA N..." */
extern const char ir_453db0[];	/* "**** Warning: error getting CBB Nonc..." */
extern const char ir_453dec[];	/* "**** Warning: error getting CBB Nonc..." */
extern const char ir_453e2c[];	/* "**** Warning: error getting CD Nonce..." */
extern const char ir_453e64[];	/* "**** Warning: error getting CD Nonce..." */
extern const char ir_453ea4[];	/* "**** Warning: error getting CE Nonce..." */
extern const char ir_453edc[];	/* "**** Warning: error getting CE Nonce..." */
extern const char ir_453f1c[];	/* "**** Warning: error getting CF Nonce..." */
extern const char ir_453f54[];	/* "**** Warning: error getting CF Nonce..." */
extern const char ir_453f94[];	/* "**** Warning: error getting CG Nonce..." */
extern const char ir_453fcc[];	/* "**** Warning: error getting CG Nonce..." */

static __attribute__((noinline)) int fsFind(const char *name, u32 *block, u32 *size, u32 *time, int quiet)
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
	else if ((u8)ldv > 32)
		xb.cfLdv = 32;
	else
		xb.cfLdv = ldv;
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
			sprintf(name, ir_452799, mobileName);
			log_printf(1, ir_4527a0,
				   name, m->page, m->offset, m->len, m->len);
			len = m->len;
			memcpy(xb.mobile[i].data, xb.image + m->offset, len);
			xb.mobile[i].size = len;
		} else
			log_printf(1, ir_45276c, name, m->len);
	}
	off = statisticsOffset(xb.bigBlock, 0, xb.mmc, 0, 0);
	if (!isErased(xb.image + off, 0x1000)) {
		log_printf(1, ir_4527e4, off, 0x1000, 0x1000);
		xb.mobile[9].data = malloc(0x1000);
		if (xb.mobile[9].data) {
			memcpy(xb.mobile[9].data, xb.image + off, 0x1000);
			xb.mobile[9].size = 0x1000;
		} else
			log_printf(1, ir_452824, 0x1000);
	}
	off = manufacturingOffset(xb.bigBlock, 0, xb.mmc, 0, 0);
	if (!isErased(xb.image + off, 0x1000)) {
		log_printf(1, ir_452864, off, 0x1000, 0x1000);
		xb.mobile[10].data = malloc(0x1000);
		if (!xb.mobile[10].data)
			log_printf(1, ir_4528a4, 0x1000);
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
	log_printf(1, ir_4528e1, xb.netkd.size);
	log_printf(1, ir_4528fe, ver);
	if (ver == 1) {
		log_printf(1, ir_452912, img[0x94], img[0x95], img[0x96], img[0x97]);
		log_printf(1, ir_452930, img[0x98], img[0x99], img[0x9a], img[0x9b], img[0x9c], img[0x9d]);
		log_printf(1, ir_452958, getBeU16(img + 0x9e));
		log_printf(1, ir_45296a, img[0xa0], img[0xa1], img[0xa2], img[0xa3]);
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

int findAnchor(void)
{
	u32 v0, v1;
	u32 ok0, ok1;

	log_printf(1, ir_4529d0);
	v0 = getBeU32(xb.image + 0x2fe8018);
	v1 = getBeU32(xb.image + 0x2fec018);
	ok0 = shaSelfCheck(xb.image + 0x2fe8000);
	if (ok0)
		log_printf(1, ir_4529f8, v0);
	else
		log_printf(1, ir_452a24);
	ok1 = shaSelfCheck(xb.image + 0x2fec000);
	if (ok1)
		log_printf(1, ir_452a4c, v1);
	else {
		log_printf(1, ir_452aa4);
		__asm__("");	/* dom3 doesn't thread this copy: one log, ok0 tested after it */
	}
	if (__builtin_expect(ok0, 1) && (__builtin_expect(!ok1, 1) || v0 >= v1)) {
		log_printf(1, ir_452acc, v0);
		memcpy(anchor, xb.image + 0x2fe8000, 0x200);
		return 1;
	}
	if (__builtin_expect(ok1, 1)) {
		log_printf(1, ir_452a78, v1);
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

void setFsOffset(void)
{
	u32 meta;

	fsOffset = 0;
	if (!xb.bigBlock)
		return;
	meta = xb.spare[mobiles[0].spare + 8] << 5;
	fsOffset = (3808 - meta) << 14;
	log_printf(1, ir_452bd8,
		   fsOffset, 3808 - meta, meta, 3808);
}

int findFsRoot(void)
{
	int found, i;
	u8 *src;
	

	log_printf(1, ir_452c20);
	if (xb.mmc)
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

	log_printf(1, ir_452d33);
	for (i = 0; i < xb.numFlashFiles; i++)
		if (xb.flashFiles[i][0] && fsFindFile(xb.flashFiles[i], &block, &xb.flashSize[i], &xb.flashTime[i], 0))
			loadFlashFile(i, block);
	log_printf(1, ir_452d4e);
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
	log_printf(1, ir_452d55);
	for (; off < end; off += 512) {
		if (!smcConfigOk(xb.image + off))
			continue;
		xb.smcConfig.data = malloc(0x400);
		if (!xb.smcConfig.data) {
			log_printf(1, ir_452db0, off);
			off = end;
			continue;
		}
		log_printf(1, ir_452d74, off);
		memcpy(xb.smcConfig.data, xb.image + off, 0x400);
		xb.smcConfig.size = 0x400;
		off = end;
	}
	if (!xb.smcConfig.data)
		log_printf(1, ir_452e09, off);
}

int addRemap(u32 block, int dest, int numBlocks)
{
	u32 i;
	int found = 0;
	u32 b = block;	/* unused; puts block before the loads in compares */

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

__attribute__((optimize("no-if-conversion"))) u32 copyMmcImage(u8 *raw)
{
	xb.numBad = 0;
	memcpy(xb.image, raw, xb.imageSize);
	if (notZeropair())
		return 1;
	log_printf(0, ir_45310c);
	return 0;
}

u32 copyMuData(FILE *out, void *sha)
{
	char name[0x400];
	FILE *fp;
	u8 *buf;
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

int checkHeader(const char *name, FILE *fp)
{
	struct flashhdr hdr;
	u8 page[0x210];
	u32 magic;
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
	if (size < SWAP32(hdr.entry)) {
		log_printf(0, ir_4538ac, name);
		return 0;
	}
	if (size < SWAP32(hdr.size)) {
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
	if (SWAP32(hdr.size) > SWAP32(hdr.sysUpdateAddr)) {
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
	if (size < SWAP32(hdr.fsAddr)) {
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
		if (getBeU32((u8 *)&magic) == 0x58544146) {
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

void getNonces(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.image;
	u32 off = SWAP32(h->entry);
	u8 *p;

	if (off >= xb.imageSize) {
		log_printf(1, ir_453d3c);
		return;
	}
	p = xb.image + off;
	if ((ROT16(*(u16 *)p) & 0x43ff) != 0x4342) {
		log_printf(1, ir_453d78);
		return;
	}
	setInfoKey0(xb.image + off + 16);
	off += (SWAP32(*(u32 *)(p + 12)) + 15) & ~15;
	if (p[6] & 8) {
		if (off >= xb.imageSize) {
			log_printf(1, ir_453db0);
			return;
		}
		p = xb.image + off;
		if ((ROT16(*(u16 *)p) & 0x43ff) != 0x4342) {
			log_printf(1, ir_453dec, off);
			return;
		}
		setInfoKey1(xb.image + off + 16);
		off += (SWAP32(*(u32 *)(p + 12)) + 15) & ~15;
	}
	if (off >= xb.imageSize) {
		log_printf(1, ir_453e2c);
		return;
	}
	p = xb.image + off;
	if ((ROT16(*(u16 *)p) & 0x43ff) != 0x4344) {
		log_printf(1, ir_453e64, off);
		return;
	}
	setInfoKey2(xb.image + off + 16);
	off += (SWAP32(*(u32 *)(p + 12)) + 15) & ~15;
	if (off >= xb.imageSize) {
		log_printf(1, ir_453ea4);
		return;
	}
	if ((ROT16(*(u16 *)(xb.image + off)) & 0x43ff) != 0x4345) {
		log_printf(1, ir_453edc, off);
		return;
	}
	setInfoKey3(xb.image + off + 16);
	off = SWAP32(h->sysUpdateAddr);
	if (off >= xb.imageSize) {
		log_printf(1, ir_453f1c);
		return;
	}
	p = xb.image + off;
	if ((ROT16(*(u16 *)p) & 0x43ff) != 0x4346) {
		log_printf(1, ir_453f54, off);
		return;
	}
	setInfoKey4(xb.image + off + 32);
	off += (SWAP32(*(u32 *)(p + 12)) + 15) & ~15;
	if (off >= xb.imageSize) {
		log_printf(1, ir_453f94);
		return;
	}
	if ((ROT16(*(u16 *)(xb.image + off)) & 0x43ff) != 0x4347) {
		log_printf(1, ir_453fcc, off);
		return;
	}
	setInfoKey5(xb.image + off + 16);
	xb.f020 = 0;
}

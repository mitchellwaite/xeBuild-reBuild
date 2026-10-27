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
u32 loadDump(const char *path);

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
extern const char ir_4524dc[];	/* "KeyVault cannot be at 0x0, trying 0x..." */
extern const char ir_452508[];	/* "KeyVault cannot be 0x%x bytes, using..." */
extern const char ir_452538[];	/* "decrypting KeyVault at address 0x%x ..." */
extern const char ir_45256c[];	/* "keyvault decrypted OK, will use if n..." */
extern const char ir_4525a8[];	/* "keyvault decrypt failed, discarding\..." */
extern const char ir_4525d0[];	/* "Wasn't able to alloc 0x4000 bytes me..." */
extern const char ir_45261c[];	/* "KeyVault at address 0x%x of size 0x4..." */
extern const char ir_452674[];	/* "decrypting alt KeyVault at address 0..." */
extern const char ir_4526ac[];	/* "alt KeyVault decrypted OK, will use ..." */
extern const char ir_4526f0[];	/* "alt KeyVault decrypt failed, discard..." */
extern const char ir_45271c[];	/* "Wasn't able to alloc 0x4000 bytes me..." */
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
extern const char ir_452988[];	/* "sector: 0x%04x offset: 0x%08x size: ..." */
extern const char ir_4529d0[];	/* "attempting to find valid anchor bloc..." */
extern const char ir_4529f8[];	/* "anchor block v %d at 0x2fe8000 is va..." */
extern const char ir_452a24[];	/* "anchor block at 0x2fe8000 is invalid..." */
extern const char ir_452a4c[];	/* "anchor block v %d at 0x2fec000 is va..." */
extern const char ir_452a78[];	/* "anchor block v %d at 0x2fec000 is se..." */
extern const char ir_452aa4[];	/* "anchor block at 0x2fec000 is invalid..." */
extern const char ir_452acc[];	/* "anchor block v %d at 0x2fe8000 is se..." */
extern const char ir_452af8[];	/* "Showing all pages with mobile info:\..." */
extern const char ir_452b20[];	/* "starting mobile scan at page 0x%x (o..." */
extern const char ir_452b6c[];	/* "mobile%c.dat ver %02d offset 0x%08x ..." */
extern const char ir_452bc3[];	/* "%02x " */
extern const char ir_452bc9[];	/* "(DELETE)\n" */
extern const char ir_452bd3[];	/* "\n" */
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
extern const char ir_452e18[];	/* "\n\n****************  WARNING  *****..." */
extern const char ir_452e50[];	/* "  nanddump.bin has NAND memory unit ..." */
extern const char ir_452e80[];	/* "  sure you back up any important dat..." */
extern const char ir_452eb0[];	/* "  internal MU before flashing a new ..." */
extern const char ir_452edc[];	/* "\n  xeBuild will attempt to keep thi..." */
extern const char ir_452f0c[];	/* "  many things could cause it to be i..." */
extern const char ir_452f44[];	/* "************************************..." */
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
extern const char ir_453694[];	/* "\tNAND dump is from a mmc machine\n" */
extern const char ir_4536b8[];	/* "\tNAND dump uses big block controlle..." */
extern const char ir_4536e0[];	/* "\tNAND dump is from a big block mach..." */
extern const char ir_453708[];	/* "***** WARNING: NAND dump too small t..." */
extern const char ir_453760[];	/* "\tNAND dump is from a small block ma..." */
extern const char ir_45378c[];	/* "\tNAND dump uses small block control..." */
extern const char ir_4537b4[];	/* "***** WARNING: NAND dump does not ap..." */
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
extern const char ir_454009[];	/* "\n------ Checking %s ------\n" */
extern const char ir_454025[];	/* "NAND dump not found at '%s'\n" */
extern const char ir_454044[];	/* "NAND dump '%s' is not a correct raw ..." */
extern const char ir_454098[];	/* "NAND dump '%s' is not a correct dump..." */
extern const char ir_4540dc[];	/* "******* ERROR loading '%s', unable t..." */
extern const char ir_454114[];	/* "Loading NAND dump (0x%x bytes)..." */
extern const char ir_454138[];	/* "******* ERROR loading '%s', unable t..." */
extern const char ir_45417c[];	/* "Detecting NAND controller type from ..." */
extern const char ir_4541b0[];	/* "******* ERROR loading '%s', unable t..." */

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
	for (i = 0; i < sizeof(xb.mobile) / sizeof(xb.mobile[0]); i++)
		if (xb.mobile[i].data)
			free(xb.mobile[i].data);
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

void getImageKv(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.image;
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
	if (addr + size < 528 * xb.numPages) {
		xb.kv.data = malloc(0x4000);
		if (xb.kv.data) {
			log_printf(1, ir_452538, addr, 0x4000);
			xb.kv.size = 0x4000;
			memcpy(xb.kv.data, xb.image + addr, 0x4000);
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
			memcpy(xb.kvAlt.data, xb.image + addr, 0x4000);
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

void listFlashFiles(void)
{
	int i;

	if (fsValid != 1)
		return;
	for (i = 0; i < 256; i++) {
		struct fsent *e = &fs->ent[i];
		u32 block, size, time;
		u16 b16;

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

int fsGetFile(const char *name, u8 **buf, u32 *size, u32 *time)
{
	u32 block, len, t, off, left, done;
	u8 *p;
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

void showMobilePages(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.image;
	u32 page, end;
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
	log_printf(2, ir_452af8);
	log_printf(2, separator);
	page = SWAP32(h->sysUpdateAddr) >> 9;
	if (page & 0x1f)
		page = (page & ~0x1f) + 32;
	off = page * 512;
	log_printf(2, ir_452b20,
		   page, off, end, xb.numPages);
	for (; page < end; page++) {
		u8 *s = xb.spare + page * 16;
		u8 t = s[12] & 0x3f;
		int letter, i;
		u32 ver;
		u16 len;

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
			   (u32)letter, ver, page << 9, page * 528, s[9], len, page);
		for (i = 0; i < 16; i++)
			log_printf(2, ir_452bc3, xb.spare[page * 16 + i]);
		if (len & 0x8000)
			log_printf(2, ir_452bc9);
		else
			log_printf(2, ir_452bd3);
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
		log_printf(2, ir_452bd3);
		showMobilePages();
	}
	page = SWAP32(h->sysUpdateAddr) >> 9;
	page = (page & 0x1f) ? (page & ~0x1f) + 32 : page;
	while (page < end) {
		u8 *s = xb.spare + page * 16;
		u8 t = s[12] & 0x3f;
		int n, i;
		u16 len;
		u32 ver;

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
				log_printf(2, ir_452bc3, xb.spare[page * 16 + i]);
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

int checkBlock(u8 *b, int block, int numBlocks)
{
	int lba, lba0, lba1;

	if (blockErased(b, xb.bigBlock))
		return -2;
	lba = -1;
	if (xb.bigBlock) {
		if (b[512] == 0xff && b[68096] == 0xff) {
			lba = b[513] + (b[514] & 0xf) * 256;
			if (lba >= numBlocks - 1)
				lba = -3;
			else if (!xb.muChecked) {
				u8 m = b[524] & 0x3f;
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
			lba0 = b[512] + (((volatile u8 *)b)[513] & 0xf) * 256;
			if (xb.bbController) {
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
		if (!(xb.bootFlags & 0x80000000) && !blockEccOk(b, xb.bigBlock))
			lba = -4;
	}
	return lba;
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

int detectController(u8 *raw, int size)
{
	int i, n;
	u32 found;

	if (size == 0x3000000) {
		log_printf(1, ir_453694);
		log_printf(1, ir_4536b8);
		xb.bbController = 1;
		xb.bigBlock = 0;
		xb.muChecked = 1;
		xb.mmc = 1;
		return 1;
	}
	if (raw[512] == 0xff) {
		log_printf(1, ir_4536e0);
		log_printf(1, ir_4536b8);
		if (size < 0x4200000) {
			log_printf(0, ir_453708);
			return 0;
		}
		xb.bigBlock = 1;
		xb.bbController = 1;
		return 1;
	}
	if (raw[517] != 0xff) {
		log_printf(0, ir_4537b4);
		return 0;
	}
	n = size / 16896;
	log_printf(1, ir_453760);
	xb.bigBlock = 0;
	xb.muChecked = 1;
	found = 0;
	/* code-free hints: found in eax outside the loop (one head-merged xor
	   for both found = 0 edges), i in ebx */
	if (n > 1)
		__asm__("" : "+a"(found));
	for (i = 1; i < n; i++) {
		u8 *b = raw + i * 16896;
		int hi, lo;
		__asm__("" : : "b"(i));

		if (b[517] != 0xff || b[513] == 0xff)
			continue;
		hi = (b[514] & 0xf) * 256;
		lo = b[513];
		if (hi + lo == i) {
			i = n;
			log_printf(1, ir_4536b8);
			xb.bbController = 1;
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
				xb.bbController = 0;
				found = 1;
			}
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

u32 loadDump(const char *path)
{
	char name[0x400];
	FILE *fp;
	int size;
	u32 ret;
	u32 pages, rawSize;
	u8 *raw;

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
		xb.numPages = 0x18000;
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
		xb.numPages = pages;
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
	xb.imageSize = xb.numPages << 9;
	xb.spareSize = xb.numPages * 16;
	xb.image = malloc(xb.numPages << 9);
	xb.spare = malloc(xb.numPages * 16);
	if (!xb.image || !xb.spare) {
		log_printf(0, ir_454138, name);
		buildCleanup();
		free(raw);
		return 0;
	}
	memset(xb.image, 0xff, xb.imageSize);
	memset(xb.spare, 0xff, xb.spareSize);
	log_printf(1, ir_45417c);
	if (detectController(raw, size)) {
		/* copyMmcImage's body, written out: its optimize attribute keeps it
		   from being inlined here.  The test must be predicted 50-52.6%
		   (ce1 hoists ret = 1 only above 50%, the mmc trace takes the log
		   block only within 10% of even): call 71% x hot label 15% x opcode
		   nonequal 72% (the != against size == 0, folded by VRP) = 52.6% */
		if (xb.mmc) {
			xb.numBad = 0;
			memcpy(xb.image, raw, xb.imageSize);
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

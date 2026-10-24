/* build: reading the image's input files (with crc32 checks against the
   ini), bootloader checks, patches and payloads, encoding the flash */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;

/* timeutil.c's cdecl ports of the Win32 time functions */
typedef unsigned short WORD;
typedef unsigned int DWORD;
typedef struct {
	DWORD dwLowDateTime;
	DWORD dwHighDateTime;
} FILETIME;
typedef struct {
	WORD wYear, wMonth, wDayOfWeek, wDay;
	WORD wHour, wMinute, wSecond, wMilliseconds;
} SYSTEMTIME;
int SystemTimeToFileTime(const SYSTEMTIME *syst, FILETIME *ft);
int FileTimeToDosDateTime(const FILETIME *ft, WORD *fatdate, WORD *fattime);
int DosDateTimeToFileTime(WORD fatdate, WORD fattime, FILETIME *ft);
void GetSystemTime(SYSTEMTIME *systime);

/* an input file of the image */
struct fileent {
	char name[0x400];
	u32 crc;			/* 400 */
	int type;			/* 404 */
	u32 offset;			/* 408 */
	u8 *data;			/* 40c */
	u32 size;			/* 410 */
	u8 key[16];			/* 414 its RC4 key once encoded */
	u32 fsSize;			/* 424 the part that goes in the filesystem */
	u32 fsOffset;			/* 428 where that part starts */
};

/* the parts of main.c's struct xebuild used here */
struct xebuild {
	int mode;			/* 000 */
	u32 flags;			/* 004 */
	u32 type;			/* 008 */
	u32 kernel;			/* 00c */
	int glitch2;			/* 010 */
	int glitch2mfg;			/* 014 */
	int cbb;			/* 018 build with a CB_B */
	int f01c;			/* 01c set when an SE replaces the CF */
	int randomKeys;			/* 020 keysInit's argument */
	int sysTime;			/* 024 use the system time for timestamps */
	u8 pad028[0x038 - 0x028];
	u8 *hdr;			/* 038 the flash image */
	u32 userSize;			/* 03c its user (non-spare) size */
	u8 pad040[0x050 - 0x040];
	int bigBlock;			/* 050 */
	u8 pad054[0x060 - 0x054];
	u32 bootFlags;			/* 060 */
	u8 pad064[0x068 - 0x064];
	int xellButton;			/* 068 */
	int xellAltButton;		/* 06c */
	int dualButton;			/* 070 */
	u8 pad074;
	u8 cfLdv;			/* 075 */
	u8 pad076[0x078 - 0x076];
	u32 cpuTemp;			/* 078 smc_config overrides from the ini */
	u32 gpuTemp;			/* 07c */
	u32 edramTemp;			/* 080 */
	u32 overCpuTemp;		/* 084 */
	u32 overGpuTemp;		/* 088 */
	u32 overEdramTemp;		/* 08c */
	u32 cpuFan;			/* 090 */
	u32 gpuFan;			/* 094 */
	u32 avRegion;			/* 098 */
	u32 gameRegion;			/* 09c */
	u32 dvdRegion;			/* 0a0 */
	u8 macid[6];			/* 0a4 */
	u8 pad0aa[0x1d8 - 0x0aa];
	u8 *consoleBlmod;		/* 1d8 blmod.bin from the console */
	u32 consoleBlmodSize;		/* 1dc */
	u8 pad1e0[0x1e8 - 0x1e0];
	int fromConsole;		/* 1e8 bootloaders read from the console */
	struct {
		u8 *data;
		u32 size;
	} mobile[11];			/* 1ec Mobile*.dat etc. from a dump */
	u8 *dumpSmc;			/* 244 files from the nand dump */
	u32 dumpSmcSize;		/* 248 */
	u8 *dumpKv;			/* 24c */
	u32 dumpKvSize;			/* 250 */
	u8 *dumpKvAlt;			/* 254 */
	u32 dumpKvAltSize;		/* 258 */
	u8 *dumpConfig;			/* 25c */
	u32 dumpConfigSize;		/* 260 */
	u8 pad264[0x2a8 - 0x264];
	u8 *prvKey;			/* 2a8 the ini's 2BL private key */
	u8 pad2ac[0x6ac - 0x2ac];
	char binDir[0x800];		/* 6ac */
	char baseDir[0x400];		/* eac */
	char dataDir[0x400];		/* 12ac */
	char commonDir[0x400];		/* 16ac */
	char firmware[256][0x400];	/* 1aac the ini's firmware files */
	u32 firmwareCrc[256];		/* 41aac */
	u32 nFirmware;			/* 41eac */
	struct fileent files[19];	/* 41eb0 35 of them, 19..34 addon patches; the */
	u8 padf[(35 - 19) * 0x42c];	/* bound sets the files loops' guessed trip count */
	u8 pad4b0b4[0x4b0f4 - 0x4b0b4];
	int nAddons;			/* 4b0f4 */
	int nFiles;			/* 4b0f8 */
	int nFlashFiles;		/* 4b0fc */
	struct {
		char name[0x400];
		u32 offset;
	} rawPatch[16];			/* 4b100 */
	u32 nRawPatches;		/* 4f140 */
	char flashFiles[10][22];	/* 4f144 security files */
	u8 *flashBuf[10];		/* 4f220 their data from a dump */
	u32 flashSize[10];		/* 4f248 */
	u32 oddTime[10];		/* 4f270 */
	u8 pad4f298[0x4f2c0 - 0x4f298];
	u32 nFlashFiles2;		/* 4f2c0 the security file count */
	u8 *anchor;			/* 4f2c4 MMC anchor block */
	u8 pad4f2c8[0x4f2df - 0x4f2c8];
	u8 anchorNum;			/* 4f2df */
	u8 pad4f2e0[0x4f2e4 - 0x4f2e0];
	struct {
		u16 type, size;
	} mobileTab[9];			/* 4f2e4 */
	u8 pad4f308[0x4f4c4 - 0x4f308];
	char kernelStr[0x40];		/* 4f4c4 the ini's kernel version string */
};

void log_printf(int level, const char *fmt, ...);
long getFileSize(FILE *f);
unsigned int crc32(const unsigned char *buf, unsigned int len);
u16 getBeU16(const u8 *p);
u32 getBeU32(const u8 *p);
u8 *setBeU32(u32 v, u8 *p);
int checkZeros(const u8 *p, u32 len);
int smcConfigOk(const u8 *smc);
void showSmcConfig(const u8 *smc);
void showMac(u32 level, const u8 *mac);
int macidSet(void);
int suGetCF(u8 **data, u32 *len);
int suGetCG(u8 **data, u32 *len);
u32 smcSetLoad(u32 size);
void setFlashBuild(u16 build);
/* image_write's */
int imgBigBlock(void);
u32 imgCfOffset(void);
u32 imgCfSize(void);
u32 imgSize(void);
void setPatchSlot(u32 off);
void imgWriteHeader(void);
int imgFsBlock(void);
void imgFixFsTable(u32 size);
void imgSetSize(u32 size);
u32 imgFsAligned(void);
void imgAddFsFile(const char *name, const u8 *data, const u8 *ts, u32 len);
void imgAddSecFile(const char *name, const u8 *data, const u8 *ts, u32 len);
int imgAddMobile(const u8 *data, u32 len, int n);
void imgAddRaw(const char *name, const u8 *data, u32 len, u32 off);
void imgAddSmcConfig(const u8 *cfg);
void imgFixEmptyFs(u32 x);
void imgWriteFsTable(u32 x);
void imgCopyAnchor(int n);
int imgFinalize(void);
/* keys.c's */
u32 cfEncrypt(struct fileent *cf, u32 extra, u16 block, int keep, u32 max);
void cgEncrypt(u8 *cg, u8 *prevKey, u8 *key, u32 size);
void cbaEncrypt(u8 *salt, u8 *cb, u8 *key, u32 size, int zero);
void cbaEncryptZero(u8 *cb, u8 *key, u32 size);
void cbaEncrypt2(u8 *salt, u8 *cb, u8 *key, u32 size, int zero);
void cbbEncrypt(u8 *salt, u8 *cbb, u8 *cbaKey, u8 *cba, u8 *key, u32 size, int zero);
void cdEncryptZero(u8 *cd, u8 *key, u32 size);
void cdEncrypt(u8 *cd, u8 *prevKey, u8 *key, u32 size);
void cdEncryptCpu(u8 *cd, u8 *prevKey, u8 *key, u32 size);
void ceEncrypt(u8 *ce, u8 *prevKey, u8 *key, u32 size);
int smcPrepare(u8 *smc, u8 *hash, u32 size);
void kvPrepare(struct fileent *kv, int alt);
void setFuseCpuKey(u8 *fuse);
void showExpectedFuses(u32 flags, u16 cb, u8 *fuses, int clear);
void showFuses(int level, const char *title, const u8 *fuses);
int checkBootImage(int arg);
int suLoadDir(const char *dir);
void keysInit(int random);
int kvGetGameRegion(void);
void extendedPrepare(struct fileent *ext);
void secdataPrepare(struct fileent *sd, u8 *date);
void daeEncrypt(u8 *buf, u32 size, u8 *date);
void crlEncrypt(u8 *crl, u32 size, u8 *date);
void fcrtEncrypt(u8 *fcrt, u32 size);
void shaHeader(u8 *buf);
u8 *setBeU16(u16 v, u8 *p);
u32 statisticsOffset(int bigBlock, int bbController, int mmc, u32 *page, u32 *spare);
u32 manufacturingOffset(int bigBlock, int bbController, int mmc, u32 *page, u32 *spare);
extern u8 cpuKey[16];		/* xb+27c */
int imgAdd(u32 off, const u8 *data, u32 len, int f3, int ecc, int f5);
extern const u8 defBl60[0x60], defPayload[0x200], defCore[0xd40];	/* build.s's .data */
int cbVerifySig(u8 *bl, const void *pubKey);
int blVerifySig(u8 *bl, unsigned int len, const void *pubKey, const u8 *salt);
u32 blSign(u8 *bl, unsigned int len, const void *pubKey, const void *prvKey, const u8 *salt);
/* int in xboxrom.c; as u32 here verifyBlSigs' inlined findFile(11) counts
   from its 0 result instead of a new xor (uncprop) */
u32 blCheckHash(u8 *bl, unsigned int len, const u8 *expect);
int blHashAndSign(u8 *bl, unsigned int len, u8 *prev, unsigned int prevLen, u8 *hashOut,
	const void *pubKey, const void *prvKey);
u32 calcConfigSum(const u8 *buf);
u32 patchSmcConfig(u8 *smc);
u8 *findInst(u8 *buf, int len, const u8 *pat, int patlen);
void display_buffer_hex(const u8 *buf, u32 len, u32 level);
typedef struct { u32 state[24]; } XECRYPT_SHA_STATE;	/* SHA_CTX */
void XeCryptShaInit(XECRYPT_SHA_STATE *sha);
void XeCryptShaUpdate(XECRYPT_SHA_STATE *sha, const void *buf, u32 len);
void XeCryptShaFinal(XECRYPT_SHA_STATE *sha, u8 *out, u32 len);
void XeCryptRotSum(u8 *sum, const void *buf, u32 cqw);

#define SWAP32(x) (((x) << 24) + ((x) >> 24) + (((x) << 8) & 0xff0000) + (((x) >> 8) & 0xff00))
/* folds to a rotate (not the bswap pass's __builtin_bswap16 call), so as a
   call argument it is computed at its store */
#define SWAP16(x) ((u16)(((u32)(x) << 8) | ((u32)(x) >> 8)))
/* an SMC config fan byte */
struct fan {
	u8 speed:7, override:1;
};

extern struct xebuild xb;
extern u8 *pub1bl;		/* xb+29c */
#define addons (&xb.files[19])

int suGetFile(const char *name, u8 **data, u32 *len);
int fsGetFile(const char *name, u8 **buf, u32 *size, u32 *time);
int updateGetFile(const char *name, u8 **data, u32 *size);

u32 findFileOffset(int type)
{
	int i;

	for (i = 0; i < xb.nFlashFiles; i++)
		if (xb.files[i].type == type)
			return xb.files[i].offset;
	return 0;
}

u32 findFileSize(int type)
{
	int i;

	for (i = 0; i < xb.nFlashFiles; i++)
		if (xb.files[i].type == type)
			return xb.files[i].size;
	return 0;
}

int findFile(int type)
{
	int i;

	for (i = 0; i < xb.nFiles; i++)
		if (xb.files[i].type == type)
			return i;
	return 0;
}

int loadFileCrc(const char *name, struct fileent *e, int verbose, int pad, u32 crc)
{
	FILE *f;
	size_t size;
	u32 c;

	f = fopen(name, "rb");
	if (!f)
		return -1;
	if (e->data)
		free(e->data);
	size = getFileSize(f);
	if (!size) {
		fclose(f);
		log_printf(0, "\n******WARNING: '%s' is a 0 byte file, loading skipped!\n", name);
		return 1;
	}
	e->size = size;
	if (pad && (size & 15))
		e->size = (size + 15) & ~15;
	/* hints: the "bytes" log must be hot enough for bb-reorder's second round
	   (build.sh's expect probability, 92-99); the pin sets e's register in the
	   out-of-line copy only (callers with pad == 0 drop this block) */
	if (__builtin_expect(verbose, 1)) {
		if (size != e->size) {
			log_printf(1, "reading %s (0x%x b pad 0x%x b)", name, size, (size + 15) & ~15);
			__asm__("" : : "S"(e));
		} else
			log_printf(1, "reading %s (0x%x bytes)", name, size);
	}
	e->data = calloc(e->size + 0x10000, 1);
	if (!e->data)
		return -2;
	fread(e->data, size, 1, f);
	fclose(f);
	if (crc) {
		c = crc32(e->data, size);
		log_printf(1, " (crc32: 0x%08x ini: 0x%08x)\n", c, crc);
		if (crc != c) {
			log_printf(0, "\n******WARNING: '%s' crc32: 0x%08x expected: 0x%08x\n", name, c, crc);
			return 1;
		}
	} else
		log_printf(1, "\n");
	return 0;
}

int readMetaFile(const char *name, u8 *meta)
{
	FILE *f;

	f = fopen(name, "rb");
	if (!f)
		return -1;
	fread(meta, 4, 1, f);
	fclose(f);
	return 0;
}

/* the build time as a big-endian FAT date and time */
void makeTimestamp(u8 *out, FILETIME *ft)
{
	SYSTEMTIME st;
	FILETIME now;
	WORD date, time;

	if (xb.sysTime) {
		GetSystemTime(&st);
		SystemTimeToFileTime(&st, &now);
	} else {
		log_printf(2, "**** using default time!!! ****\n");
		now.dwHighDateTime = 30268127;
		now.dwLowDateTime = 1903825408;
	}
	FileTimeToDosDateTime(&now, &date, &time);
	if (ft)
		DosDateTimeToFileTime(date, time, ft);
	out[0] = date >> 8;
	out[1] = date;
	out[2] = time >> 8;
	out[3] = time;
}

int timestampToFileTime(const u16 *ts, FILETIME *ft)
{
	return DosDateTimeToFileTime(SWAP16(ts[0]), SWAP16(ts[1]), ft);
}

/* read baseDir/name into e */
static __attribute__((noinline, noclone)) int loadBaseFile(const char *name, struct fileent *e)
{
	if (xb.baseDir[0]) {
		char path[0x400];

		strcpy(path, xb.baseDir);
		strcat(path, name);
		return loadFileCrc(path, e, 1, 0, 0);
	}
	return -1;
}

/* the same with its timestamp from name.meta if there is one */
int loadBaseFileMeta(const char *name, struct fileent *e, u8 *meta)
{
	if (xb.baseDir[0]) {
		char path[0x400];
		int r;

		strcpy(path, xb.baseDir);
		strcat(path, name);
		r = loadFileCrc(path, e, 1, 0, 0);
		if (!r && meta) {
			strcat(path, ".meta");
			if (!readMetaFile(path, meta))
				log_printf(1, "**** %s metadata found, not using system time *****\n\n", path);
		}
		return r;
	}
	return -1;
}

int loadCommonFile(const char *name, struct fileent *e, int pad, u32 crc, u8 *meta)
{
	char path[0x400];
	int r;

	strcpy(path, xb.commonDir);
	strcat(path, name);
	r = loadFileCrc(path, e, 1, pad, crc);
	if (!r && meta) {
		strcat(path, ".meta");
		if (!readMetaFile(path, meta))
			log_printf(1, "**** %s metadata found, not using system time *****\n\n", path);
		else
			makeTimestamp(meta, NULL);
	}
	return r;
}

/* name from the data dir, else from the system update (SUPD), the nand
   dump or the console (USVR), else from the common dir */
int loadInputFile(const char *name, struct fileent *e, int pad, u32 crc, u8 *meta,
		  int su, int fs, int common)
{
	char path[0x400];
	const char *base;
	u32 ts, c;
	int r;

	base = strrchr(name, '/');
	if (!base)
		base = strrchr(name, '\\');
	if (base)
		base++;
	else
		base = name;
	if (strrchr(name, ':'))
		strcpy(path, name);
	else {
		strcpy(path, xb.dataDir);
		strcat(path, name);
	}
	r = loadFileCrc(path, e, 1, pad, crc);
	if (meta && !r) {
		strcat(path, ".meta");
		if (!readMetaFile(path, meta))
			log_printf(1, "**** %s metadata found, not using system time *****\n\n", path);
		else
			makeTimestamp(meta, NULL);
	}
	if (su && r) {
		if (suGetFile(base, &e->data, &e->size)) {
			log_printf(1, "extracted SUPD/%s (0x%x bytes)", base, e->size);
			if (crc) {
				c = crc32(e->data, e->size);
				log_printf(1, " (crc32: 0x%08x ini: 0x%08x)\n", c, crc);
				if (crc == c) {
					if (meta)
						makeTimestamp(meta, NULL);
					r = 0;
				} else
					log_printf(0, "\n******WARNING: '%s' crc32: 0x%08x expected: 0x%08x\n", base, c, crc);
			} else
				log_printf(1, "\n");
		}
	}
	if (fs && r) {
		if (fsGetFile(base, &e->data, &e->size, &ts)) {
			log_printf(1, "extracted nanddump/%s (0x%x bytes)", base, e->size);
			if (crc) {
				c = crc32(e->data, e->size);
				log_printf(1, " (crc32: 0x%08x ini: 0x%08x)\n", c, crc);
				if (crc == c) {
					if (meta)
						makeTimestamp(meta, NULL);
					r = 0;
				} else {
					free(e->data);
					e->data = NULL;
					e->size = 0;
					log_printf(0, "\n******WARNING: '%s' crc32: 0x%08x expected: 0x%08x\n", base, c, crc);
				}
			} else
				log_printf(1, "\n");
		} else if (xb.mode == 2 && updateGetFile(base, &e->data, &e->size)) {
			log_printf(1, "extracted USVR/%s (0x%x bytes)", base, e->size);
			if (crc) {
				c = crc32(e->data, e->size);
				log_printf(1, " (crc32: 0x%08x ini: 0x%08x)\n", c, crc);
				if (crc == c) {
					if (meta)
						makeTimestamp(meta, NULL);
					r = 0;
				} else {
					free(e->data);
					e->data = NULL;
					e->size = 0;
					log_printf(0, "\n******WARNING: '%s' crc32: 0x%08x expected: 0x%08x\n", base, c, crc);
				}
			} else {
				log_printf(1, "\n");
				r = 0;
			}
		}
	}
	if (common && r)
		return loadCommonFile(base, e, pad, crc, meta);
	return r;
}

/* an addon patch from the bin dir */
int loadBinFile(struct fileent *e)
{
	char path[0x400];

	strcpy(path, xb.binDir);
	strcat(path, e->name);
	return loadFileCrc(path, e, 1, 0, 0);
}

/* e->name as given, else from ./ */
int loadLocalFile(struct fileent *e)
{
	char path[0x400];

	strcpy(path, e->name);
	if (!loadFileCrc(path, e, 1, 0, 0))
		return 0;
	strcpy(path, "./");
	strcat(path, e->name);
	return loadFileCrc(path, e, 1, 0, 0);
}

int setFileData(struct fileent *e, const void *data, size_t size)
{
	e->data = calloc(size, 1);
	if (!e->data)
		return 1;
	e->size = size;
	memcpy(e->data, data, size);
	return 0;
}

/* an ini value is used if it is in range; 0 and -1 mean unset */
int iniRangeOk(const char *name, u32 v, u32 lo, u32 hi)
{
	int ok = 1;

	if (v < lo || v > hi) {
		ok = 0;
		if (v != 0 && v != 0xffffffff)
			log_printf(0, "Ini value %d for %s is out of range (%d-%d), not using\n", v, name, lo, hi);
	}
	return ok;
}

/* the build's kernel version is the highest of its bootloaders' */
void raiseKernel(u16 magic, u16 build, u16 qfe)
{
	u32 k = 0x20000000 | build << 8;

	if (k > xb.kernel)
		xb.kernel = k;
}

/* hint call for checkBl and patchSmcConfig (PRED_CALL on the arm it sits
   in); inlined after the profile is estimated, its store goes */
static void cb_hint(int *p)
{
	*p = 1;
}

/* check a bootloader's magic and size and (with its header's per-console
   fields cleared) its crc32 against the ini's; -1 skips the crc for the
   SC/SD/SE that are built rather than read */
__attribute__((optimize("no-early-inlining")))
int checkBl(u8 *bl, u32 size, int type, u32 crc)
{
	u32 blsize, c;
	int m, dead;

	/* hints (none emit code): the original copies the epilogue into the
	   size-error block, which needs that edge >= 10% of entry, and not into
	   the crc failure one, which needs it below. The hot label and cb_hint
	   (on the other edge) take the size error from 1.7% to 19%, the crc
	   expects (build.sh's probability 98) keep `bad` under 10%, and the "D"
	   pin loads type before the first call as the original does. The
	   SC/SD `crc == -1` expects send more frequency to `bad` by branch
	   (crc32 path), so it is aligned as a loop head like the original
	   (.p2align 4,,10: branch freq > 4 x the B case's fallthru). */
	__asm__("" : : "D"(type));
	blsize = getBeU32(bl + 12);
	if (blsize > size) {
		size_err: __attribute__((hot));
		log_printf(0, "\n\n***** ERROR: BL size (0x%x) is bigger than the file (0x%x) read in!\n", blsize, size);
		return -3;
	}
	cb_hint(&dead);
	m = bl[0];
	__asm__("" :: "a"(m));
	if ((m & 0x43) != 0x43)
		goto magic;
	switch (type) {
	case 5:
	case 6:
	case 11:
	case 17:
		if (bl[1] != 'B')
			goto magic;
		memset(bl + 0x10, 0, 0x30);
		c = crc32(bl, blsize);
		if (__builtin_expect(crc != c, 0))
			goto bad;
		break;
	case 7:
	case 18:
		if (bl[1] != 'D')
			goto magic;
		memset(bl + 0x10, 0, 0x10);
		c = crc32(bl, blsize);
		if (__builtin_expect(crc != c, 0))
			goto bad;
		break;
	case 8:
	case 19:
		if (bl[1] != 'E')
			goto magic;
		memset(bl + 0x10, 0, 0x10);
		c = crc32(bl, blsize);
		if (__builtin_expect(crc != c, 0))
			goto bad;
		raiseKernel(getBeU16(bl), getBeU16(bl + 2), getBeU16(bl + 4));
		break;
	case 9:
	case 15:
	case 20:
		if (bl[1] != 'F')
			goto magic;
		memset(bl + 0x20, 0, 0x210);
		c = crc32(bl, blsize);
		if (__builtin_expect(crc != c, 0))
			goto bad;
		raiseKernel(getBeU16(bl), getBeU16(bl + 20), getBeU16(bl + 22));
		break;
	case 10:
	case 16:
	case 21:
		if (bl[1] != 'G')
			goto magic;
		memset(bl + 0x10, 0, 0x10);
		c = crc32(bl, blsize);
		if (__builtin_expect(crc != c, 0))
			goto bad;
		break;
	case 12:
		if (bl[1] != 'C')
			goto magic;
		memset(bl + 0x10, 0, 0x10);
		if (__builtin_expect(crc == 0xffffffff, 0))
			break;
		c = crc32(bl, blsize);
		if (__builtin_expect(crc != c, 0))
			goto bad;
		break;
	case 13:
		if (bl[1] != 'D')
			goto magic;
		memset(bl + 0x10, 0, 0x10);
		if (__builtin_expect(crc == 0xffffffff, 0))
			break;
		c = crc32(bl, blsize);
		if (__builtin_expect(crc != c, 0))
			goto bad;
		break;
	case 14:
		if (bl[1] != 'E')
			goto magic;
		memset(bl + 0x10, 0, 0x10);
		c = crc32(bl, blsize);
		raiseKernel(getBeU16(bl), getBeU16(bl + 2), getBeU16(bl + 4));
		if (crc == 0xffffffff)
			break;
		c = crc32(bl, blsize);
		if (__builtin_expect(crc != c, 0))
			goto bad;
		break;
	default:
		c = 0;
		goto bad;
	}
	return 0;
bad:
	log_printf(0, "\n\n***** ERROR: BL crc check failed! calculated: %08x expected: %08x\n", c, crc);
	return -2;
magic:
	log_printf(0, "\n\n***** ERROR: BL magic check %c%c for type %d failed!\n", bl[0], bl[1], type);
	return -1;
}

/* find the SMC config in a nand image (pages with or without their
   0x10-byte spare data) and copy it to e */
int extractSmcConfig(struct fileent *e, u8 *buf, u32 size)
{
	u32 i, j;
	int found;

	/* hints (wip/README.md): &size makes size SSA late (next <= size in
	   both loops); the bound expects make found the rotated exit; the pin
	   puts next/buf in esi/edi; two hot labels on notfound keep the patched
	   block under bb-reorder's duplication threshold */
	(void)&size;
	if (e->data)
		free(e->data);
	e->size = 0x400;
	e->data = malloc(0x400);
	if (!e->data)
		return -2;
	log_printf(1, "-------------------\n");
	log_printf(1, "checking smc_config\n");
	log_printf(1, "-------------------\n");
	found = 0;
	for (i = 0; __builtin_expect(i + 0x200 <= size, 1); i += 0x200) {
		__asm__("" : : "S"(i + 0x200), "D"(buf));
		if ((found = smcConfigOk(buf + i)) == 1)
			break;
	}
	if (!found) {
		for (i = 0; __builtin_expect(i + 0x210 <= size, 1); i += 0x210)
			if ((found = smcConfigOk(buf + i)) == 1)
				break;
		if (!found)
			goto notfound;
	}
	if (checkZeros(buf + i + 0x20c, 4)) {
		log_printf(1, "extracting config\n");
		if (__builtin_expect(size - i >= 0x400, 1)) {
			u8 *src = buf + i;

			/* buf live past src: no IRA copy buf-src, so the raw
			   loop's eax doesn't push dst out of eax (wip/README) */
			__asm__("" : "+r"(src) : "r"(buf));
			memcpy(e->data, src, 0x400);
		}
	} else if (size - i >= 0x4200) {
		log_printf(1, "extracting config raw\n");
		for (j = 0; j < 8; j++)
			memcpy(e->data + j * 0x200, buf + i + j * 0x210, 0x200);
	} else {
		log_printf(1, "******* ERROR: extracting config did not work, not enough data to copy!\n");
		return -2;
	}
	if (i)
		log_printf(1, "valid SMC config data found at offset 0x%x\n", i);
	log_printf(1, "------------------\n");
	log_printf(1, "SMC config info:\n");
	log_printf(1, "------------------\n");
	showSmcConfig(e->data);
	log_printf(1, "---------------------\n");
	if (patchSmcConfig(e->data)) {
		log_printf(1, "SMC patched info:\n");
		log_printf(1, "------------------\n");
		showSmcConfig(e->data);
		log_printf(1, "---------------------\n");
	}
	return 0;
notfound: __attribute__((hot));
notfound2: __attribute__((hot));
	log_printf(0, "******* ERROR: unable to find SMC config data!\n");
	return 2;
}

int blmodMissing(struct fileent *e)
{
	return loadBaseFile("blmod.bin", e) != 0;
}

/* XeCryptRotSumSha, showing the sums */
void rotSumSha(const u8 *a, u32 alen, const u8 *b, u32 blen, u8 *out, u32 outlen)
{
	u8 sum[32];
	XECRYPT_SHA_STATE sha;
	u32 i;

	for (i = 0; i < 32; i++)
		sum[i] = 0;
	XeCryptRotSum(sum, a, alen >> 3);
	log_printf(1, "sum1:");
	display_buffer_hex(sum, 32, 1);
	XeCryptRotSum(sum, b, blen >> 3);
	log_printf(1, "sum2:");
	display_buffer_hex(sum, 32, 1);
	XeCryptShaInit(&sha);
	XeCryptShaUpdate(&sha, sum, 32);
	XeCryptShaUpdate(&sha, sum, 32);
	XeCryptShaUpdate(&sha, a, alen);
	XeCryptShaUpdate(&sha, b, blen);
	for (i = 0; i < 32; i++)
		sum[i] = ~sum[i];
	log_printf(1, "sum3:");
	display_buffer_hex(sum, 32, 1);
	XeCryptShaUpdate(&sha, sum, 32);
	XeCryptShaUpdate(&sha, sum, 32);
	XeCryptShaFinal(&sha, out, outlen);
	log_printf(1, "fin :");
	display_buffer_hex(out, outlen, 1);
}

int countBits(u8 v)
{
	int i, n = 0;

	for (i = 0; i < 8; i++) {
		if (v & 1)
			n++;
		v >>= 1;
	}
	return n;
}

/* the bootloader types an update (xeBuild's -u) replaces */
int isUpdateBl(int type)
{
	return type == 23 || type == 15 || type == 16 || type == 9 || type == 10 || type == 24 || type == 25;
}

/* payload.bin's `li r4, reps` (copy loop count in words) */
void patchPayloadSize(u8 *buf, int len, int size)
{
	int pat = 0xffff8038;	/* li r4, (any) */
	u8 *p;
	u32 reps = (size + 3) >> 2;

	log_printf(1, "patching payload.bin to load size 0x%x (0x%x reps)\n", size, reps);
	p = findInst(buf, len, (u8 *)&pat, 4);
	if (!p)
		return;
	log_printf(2, "org li %r4, %02x%02x\n", p[2], p[3]);
	p[3] = reps;
	p[2] = reps >> 8;
	log_printf(2, "fin li %r4, %02x%02x\n", p[2], p[3]);
}

/* the header bytes freeboot/xell read: UART speed, power-on reasons */
void patchHeaderOpts(void)
{
	u8 opts = 0;

	xb.hdr[0x4b] = 1;
	if (xb.bootFlags & 9) {
		log_printf(1, "\tPatching header for slower demon/cygnos UART speed\n");
		opts = 1;
	}
	if (xb.type == 2) {
		opts |= xb.bootFlags & 7;
		if (xb.bootFlags & 8)
			opts |= 1;
		if (xb.dualButton == xb.xellButton || xb.dualButton == xb.xellAltButton)
			xb.dualButton = 0;
	} else
		xb.dualButton = 0;
	xb.hdr[0x4c] = xb.dualButton;
	xb.hdr[0x4d] = opts;
	log_printf(1, "\tPatching header for xell power reason\n");
	if (xb.xellButton == xb.xellAltButton)
		xb.xellAltButton = 0;
	xb.hdr[0x4f] = xb.xellButton;
	if (xb.xellAltButton)
		log_printf(1, "\tPatching header for xell alt power reason\n");
	xb.hdr[0x4e] = xb.xellAltButton;
}

/* append the ini's addon patch files to the patches (their 0xffffffff
   terminators dropped), then the terminator and the addon byte count */
void appendAddonPatches(struct fileent *e)
{
	u32 size = e->size - 4;
	u8 *buf = malloc(0x4000);
	u32 added = 0;
	struct fileent *a;
	int i;

	memset(buf, 0xff, 0x4000);
	memcpy(buf, e->data, size);
	if (xb.nAddons)
	for (i = 0; i < xb.nAddons; i++) {
		a = &xb.files[19 + i];
		if (!loadBinFile(a)) {
			if (!(a->size & 3)) {
				if (getBeU32(a->data + a->size - 4) == 0xffffffff)
					a->size -= 4;
				if (size + a->size <= 0x4000) {
					memcpy(buf + size, a->data, a->size);
					added += a->size;
					size += a->size;
				} else
					log_printf(0, "\n***** ERROR: could not append %s%s into patches, not enough room!\n\n",
						   xb.binDir, a->name);
			} else
				log_printf(0, "\n***** ERROR: could %s%s size 0x%x is not a multiple of 4, discarding patch data!\n\n",
					   xb.binDir, a->name, a->size);
		} else
			log_printf(0, "\n***** WARNING: could not load addon patch %s%s!\n\n", xb.binDir, a->name);
	}
	*(u32 *)(buf + size) = 0xffffffff;
	setBeU32(added, buf + size + 4);
	size += 8;
	if (e->data)
		free(e->data);
	e->data = buf;
	e->size = size;
	if (xb.nAddons)
		log_printf(1, "added 0x%x bytes to patches via %d external patch files\n    patches now 0x%x bytes total with addon byte count appended\n",
			   added, xb.nAddons, size);
}

/* what a power-on reason code is; 1 for an unknown one.  Console types
   above 4 (slims) have different USB ports */
int logPowerButton(int reason, const char *use)
{
	switch (reason) {
	case 0x11:
		log_printf(1, "    - console power button is being used to %s \n", use);
		break;
	case 0x12:
		log_printf(1, "    - console DVD eject button is being used to %s \n", use);
		break;
	case 0x20:
		log_printf(1, "    - IR remote power button is being used to %s \n", use);
		break;
	case 0x22:
		log_printf(1, "    - IR remote guide/X button is being used to %s \n", use);
		break;
	case 0x24:
		log_printf(1, "    - IR remote windows button is being used to %s \n", use);
		break;
	case 0x41:
		log_printf(1, "    - KIOSK debug pin is being used to %s \n", use);
		break;
	case 0x55:
		log_printf(1, "    - wireless controller powering on console is being used to %s \n", use);
		break;
	case 0x59:
		if ((xb.flags & 7) > 4)
			log_printf(1, "wired controller (rear top usb port) is being used to %s \n", use);
		else
			log_printf(1, "wired controller (INVALID FOR FATS!!) is being used to %s \n", use);
		break;
	case 0x58:
		if ((xb.flags & 7) > 4)
			log_printf(1, "wired controller (rear middle usb port) is being used to %s \n", use);
		else
			log_printf(1, "wired controller (INVALID FOR FATS!!) is being used to %s \n", use);
		break;
	case 0x5a:
		if ((xb.flags & 7) > 4)
			log_printf(1, "wired controller (rear bottom usb port) is being used to %s \n", use);
		else
			log_printf(1, "wired controller (rear usb port) is being used to %s \n", use);
		break;
	case 0x56:
		if ((xb.flags & 7) > 4)
			log_printf(1, "wired controller (front left usb port) is being used to %s \n", use);
		else
			log_printf(1, "wired controller (front top usb port) is being used to %s \n", use);
		break;
	case 0x57:
		if ((xb.flags & 7) > 4)
			log_printf(1, "wired controller (front right usb port) is being used to %s \n", use);
		else
			log_printf(1, "wired controller (front bottom usb port) is being used to %s \n", use);
		break;
	default:
		return 1;
	}
	return 0;
}

/* drop the first two patch sets (each a list of {addr, count, words}
   ended by 0xffffffff) from the patches file. After the shift `off =
   e->size` ends the loop (as in the Linux v1.16 build); gcc threads it
   to the exit. With that latch the profile spills off and keeps n in a
   register as the original does (a `break` + hot label didn't). `t`
   gives off + 4 one name for both arms; the skip adds to the old off. */
void fixupPatchSet(void)
{
	struct fileent *e = &xb.files[findFile(23)];
	u8 *p = e->data;
	u32 off, i, v, t;
	int n = 0;

	log_printf(1, "Fixing up patch set...");
	off = 0;
	while (off < e->size) {
		if (n == 2) {
			for (i = 0; i < e->size - off; i++)
				e->data[i] = e->data[off + i];
			e->size -= off;
			off = e->size;
		} else {
			v = getBeU32(p + off);
			t = off + 4;
			if (v != 0xffffffff)
				off += getBeU32(p + t) * 4 + 8;
			else {
				n++;
				off = t;
			}
		}
	}
	log_printf(1, "Done!\n");
}
/* the SMC config's temperatures, fans and regions (\370 is the degree
   sign in the console's code page) */
void showSmcConfig(const u8 *smc)
{
	u32 av;
	u16 game;
	int i;

	log_printf(1, "Target temps: Cpu: %3d\370C Gpu: %3d\370C Edram: %3d\370C\n", smc[0x29], smc[0x2a], smc[0x2b]);
	log_printf(1, "Max temps   : Cpu: %3d\370C Gpu: %3d\370C Edram: %3d\370C\n", smc[0x2c], smc[0x2d], smc[0x2e]);
	log_printf(1, "Cpu Fan     : ");
	if (((struct fan *)(smc + 0x11))->override)
		log_printf(1, "%d%%%% (overridden)\n", ((struct fan *)(smc + 0x11))->speed);
	else
		log_printf(1, "(auto)\n");
	log_printf(1, "Gpu Fan     : ", smc[0x12] & 0x7f);
	if (((struct fan *)(smc + 0x12))->override)
		log_printf(1, "%d%%%% (overridden)\n", ((struct fan *)(smc + 0x12))->speed);
	else
		log_printf(1, "(auto)\n");
	log_printf(1, "MAC Address : ");
	showMac(1, smc + 0x220);
	av = *(u32 *)(smc + 0x228);
	av = SWAP32(av);
	switch (av) {
	case 0x100:
		log_printf(1, "\nAVRegion    : 0x%08x (NTSC-M)\n", av);
		break;
	case 0x200:
		log_printf(1, "\nAVRegion    : 0x%08x (NTSC-J)\n", av);
		break;
	case 0x300:
		log_printf(1, "\nAVRegion    : 0x%08x (PAL50)\n", av);
		break;
	case 0x400:
		log_printf(1, "\nAVRegion    : 0x%08x (PAL60)\n", av);
		break;
	default:
		log_printf(1, "\nAVRegion    : 0x%08x (Unknown)\n", av);
		break;
	}
	game = __builtin_bswap16(*(u16 *)(smc + 0x22c));
	log_printf(1, "GameRegion  : 0x%04x ", game);
	switch (game) {
	case 0xff:
		log_printf(1, "(NTSC/US)\n");
		break;
	case 0x1fe:
		log_printf(1, "(NTSC/JAP)\n");
		break;
	case 0x1ff:
		log_printf(1, "(NTSC/JAP)\n");
		break;
	case 0x1fc:
		log_printf(1, "(NTSC/KOR)\n");
		break;
	case 0x101:
		log_printf(1, "(NTSC/HK)\n");
		break;
	case 0x2fe:
		log_printf(1, "(PAL/EU)\n");
		break;
	case 0x201:
		log_printf(1, "(PAL/AUS)\n");
		break;
	case 0x7fff:
		log_printf(1, "(DEVKIT)\n");
		break;
	default:
		log_printf(1, "(Unknown)\n");
		break;
	}
	log_printf(1, "DVDRegion   : %d\n", SWAP32(*(u32 *)(smc + 0x234)));
	log_printf(1, "resetKey    : ");
	for (i = 0; i < 4; i++)
		log_printf(1, "%c", smc[0x238 + i]);
	log_printf(1, "\n");
}

/* apply the ini's smc_config overrides; 1 if anything changed (then the
   checksum is redone). u32, not int: extractSmcConfig's return must not
   coalesce with this result (uncprop). Hints: the cb_hint calls (cpu and
   gpu ok arms, 0x7f arms) break bb-reorder's fibheap ties so the gpu
   range-log/warning trace goes before the cpu one and the gpu ok block
   before the cpu one, as in the original; the gpu warning after the
   return puts its string last in .rdata (a threading copy there) */
__attribute__((optimize("no-early-inlining")))
u32 patchSmcConfig(u8 *smc)
{
	u32 patched = 0;
	int i, dead;

	log_printf(1, "Checking for smc config data patches\n");
	if (iniRangeOk("cputemp", xb.cpuTemp, 40, 120)) {
		smc[0x29] = xb.cpuTemp;
		patched = 1;
	}
	if (iniRangeOk("gputemp", xb.gpuTemp, 40, 120)) {
		smc[0x2a] = xb.gpuTemp;
		patched = 1;
	}
	if (iniRangeOk("edramtemp", xb.edramTemp, 40, 120)) {
		smc[0x2b] = xb.edramTemp;
		patched = 1;
	}
	if (iniRangeOk("overcputemp", xb.overCpuTemp, 40, 120)) {
		smc[0x2c] = xb.overCpuTemp;
		patched = 1;
	}
	if (iniRangeOk("overgputemp", xb.overGpuTemp, 40, 120)) {
		smc[0x2d] = xb.overGpuTemp;
		patched = 1;
	}
	if (iniRangeOk("overedramtemp", xb.overEdramTemp, 40, 120)) {
		smc[0x2e] = xb.overEdramTemp;
		patched = 1;
	}
	if (xb.cpuFan != 0xffffffff) {
		if (iniRangeOk("cpufan", xb.cpuFan, 40, 100)) {
			cb_hint(&dead);
			smc[0x11] = xb.cpuFan | 0x80;
			patched = 1;
		} else if (xb.cpuFan)
			log_printf(0, "***** WARNING: cpu fan speed %d override ignored, not between 40 and 100\n", xb.cpuFan);
		else if (smc[0x11] != 0x7f) {
			cb_hint(&dead);
			smc[0x11] = 0x7f;
			patched = 1;
		}
	}
	if (xb.gpuFan != 0xffffffff) {
		if (iniRangeOk("gpufan", xb.gpuFan, 40, 100)) {
			cb_hint(&dead);
			smc[0x12] = xb.gpuFan | 0x80;
			patched = 1;
		} else if (xb.gpuFan)
			goto gpuwarn;
		else {
			cb_hint(&dead);
			smc[0x12] = 0x7f;
		}
	}
gpudone:
	if (xb.avRegion != 0xffffffff) {
		*(u32 *)(smc + 0x228) = SWAP32(xb.avRegion);
		patched = 1;
	}
	if (xb.gameRegion != 0xffffffff && (u16)xb.gameRegion) {
		*(u16 *)(smc + 0x22c) = __builtin_bswap16(xb.gameRegion);
		patched = 1;
	}
	if (xb.dvdRegion != 0xffffffff) {
		*(u32 *)(smc + 0x234) = SWAP32(xb.dvdRegion);
		patched = 1;
	}
	if (!*(u32 *)(smc + 0x234)) {
		log_printf(0, "****** Warning! SMC config has dvd region as 0, xbox will not play DVD videos like this... forcing it to 1 (NTSC/USA)\n");
		log_printf(0, "       Please set it in boxdata ini file if you require a different region, and run the builder again\n\n");
		*(u32 *)(smc + 0x234) = 0x1000000;
		patched = 1;
	}
	if (macidSet())
		for (i = 0; i < 6; i++) {
			if (smc[0x220 + i] != xb.macid[i])
				patched = 1;
			smc[0x220 + i] = xb.macid[i];
		}
	if (patched) {
		u32 sum = calcConfigSum(smc);

		*(u32 *)smc = SWAP32(sum);
		log_printf(1, "smc config patched!\n");
	} else
		log_printf(1, "smc config was not patched\n");
	log_printf(1, "---------------------\n");
	return patched;
gpuwarn:
	log_printf(0, "***** WARNING: gpu fan speed override setting ignored, not between 40 and 100\n");
	goto gpudone;
}

/* check the bootloaders' signatures (CB/SB against the 1BL key, SC/SD
   against SB's key, SE's hash in SD), resigning with the ini's private key
   when it matches; 0 if a resign failed */
int verifyBlSigs(void)
{
	int ok = 1, sb, sd;
	struct fileent *e;
	u32 i;
	const u8 *salt;

	for (i = 1; i < (u32)xb.nFiles; i++) {
		e = &xb.files[i];
		switch (e->type) {
		case 5:
		case 11:
		case 17:
			if (pub1bl) {
				if (!cbVerifySig(e->data, pub1bl))
					log_printf(0, "\n***** ERROR: %s failed signature check!\n", e->name);
				else
					log_printf(1, "%s signature is good\n", e->name);
			} else
				log_printf(1, "could not check signature of %s, 1BL RSA key not present!\n", e->name);
			break;
		case 12:
		case 13:
			sb = findFile(11);
			if (sb) {
				salt = e->type == 12 ? xb.files[sb].data + 904 : xb.files[sb].data + 914;
				if (blVerifySig(e->data, e->size, xb.files[sb].data + 616, salt))
					log_printf(1, "%s signature is good\n", e->name);
				else if (xb.prvKey) {
					if (!memcmp(xb.prvKey, xb.files[sb].data + 616, 0x110)) {
						log_printf(0, "%s failed signature check, attempting to resign\n", e->name);
						if (!blSign(e->data, e->size, xb.files[sb].data + 616, xb.prvKey, salt)) {
							log_printf(0, "\n***** ERROR: failed to resign %s!\n", e->name);
							ok = 0;
						} else
							log_printf(1, "%s resigned successfully!\n", e->name);
					} else
						log_printf(0, "\n***** ERROR: %s failed signature check, RSA key provided does not match the pub key in SB!\n", e->name);
				} else
					log_printf(0, "\n***** ERROR: %s failed signature check, RSA key not available for resigning!\n", e->name);
			} else
				log_printf(1, "could not locate SB data to check %s!\n", e->name);
			break;
		case 14:
			sd = findFile(13);
			if (sd) {
				if (!blCheckHash(e->data, e->size, xb.files[sd].data + 588)) {
					if (xb.prvKey) {
						sb = findFile(11);
						if (!memcmp(xb.prvKey, xb.files[sb].data + 616, 0x110)) {
							log_printf(0, "%s failed hash check, attempting to correct SE and resign\n", e->name);
							if (!blHashAndSign(e->data, e->size, xb.files[sd].data, xb.files[sd].size,
									   xb.files[sd].data + 588, xb.files[sb].data + 616, xb.prvKey))
								log_printf(0, "\n***** ERROR: failed to resign SE to correct %s hash!\n", e->name);
							else
								log_printf(1, "SE resigned successfully to correct %s hash!\n", e->name);
						} else
							log_printf(0, "\n***** ERROR: %s failed hash check, RSA key provided does not match the pub key in SD!\n", e->name);
					} else
						log_printf(0, "\n***** ERROR: %s failed hash check!\n", e->name);
				} else
					log_printf(1, "%s hash from SE is good\n", e->name);
			} else
				log_printf(1, "\n***** ERROR: could not locate SD data to check %s!\n", e->name);
			break;
		}
	}
	return ok;
}

/* the 0x60-byte bootloader (type 24) from the base dir, else the default */
static int loadBl60(struct fileent *e)
{
	if (loadBaseFile(e->name, e) || e->size != 0x60) {
		e->data = malloc(0x60);
		if (!e->data)
			return 1;
		e->size = 0x60;
		memcpy(e->data, defBl60, 0x60);
	}
	return 0;
}

/* load the input file e (xb.files[i]) by its type */
static u32 loadBl(struct fileent *e, u32 i)
{
	u32 r = 0;
	int type;

	type = e->type;
	switch (type) {
	case 5: case 7: case 8: case 9: case 10: case 11: case 12: case 13:
	case 14: case 15: case 16: case 17: case 18: case 19: case 20: case 21:
		r = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);
		if (r && !(type == 9 && suGetCF(&e->data, &e->size)) &&
		    !(type == 10 && suGetCG(&e->data, &e->size)))
			break;
		if (type == 9 && e->data[0] == 'S' && e->data[1] == 'E') {
			/* an SE where the CF goes */
			e->type = type = 14;
			xb.cfLdv = 0;
			xb.f01c = 1;
		}
		r = checkBl(e->data, e->size, type, e->crc);
		if (r)
			break;
		if (type == 5 || type == 17 || type == 11) {
			if (!pub1bl)
				log_printf(1, "loaded %s, could not check signature rsa key not present!\n", e->name);
			else if (cbVerifySig(e->data, pub1bl))
				log_printf(1, "loaded %s, signature check passed!\n", e->name);
			else {
				log_printf(0, "\n***** ERROR: loaded %s, but signature check failed!\n", e->name);
				r = -1;
			}
		}
		if (xb.type > 5 && type == 14)
			setFlashBuild(getBeU16(xb.files[i].data + 2));
		break;
	case 6:
		if (!xb.cbb)
			break;
		r = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);
		if (!r)
			r = checkBl(e->data, e->size, 6, e->crc);
		break;
	case 24:
		if (xb.type == 2 || xb.glitch2mfg)
			r = loadBl60(e);
		if (xb.type == 4 || xb.type == 5)
			r = loadBl60(e);
		break;
	case 1:
		if (!loadBinFile(e))
			break;
		log_printf(1, "could not read %s%s, using built in payload (0x%x bytes)\n", xb.binDir, e->name, 0x200);
		e->data = malloc(0x200);
		if (!e->data) {
			r = 1;
			break;
		}
		e->size = 0x200;
		memcpy(e->data, defPayload, 0x200);
		break;
	case 22:
		if (!loadBinFile(e))
			break;
		log_printf(1, "could not read %s%s, using built in core (0x%x bytes)\n", xb.binDir, e->name, 0xd40);
		e->data = malloc(0xd40);
		if (!e->data) {
			r = 1;
			break;
		}
		e->size = 0xd40;
		memcpy(e->data, defCore, 0xd40);
		break;
	case 25:
		if (xb.type == 1 || xb.type > 5)
			break;
		if (!loadBaseFile(e->name, e))
			break;
		log_printf(1, "xell not found in perbuild directory, checking firmware /bin folder\n");
		if (!loadBinFile(e))
			break;
		log_printf(1, "xell not found in firmware /bin folder, checking base path\n");
		r = loadLocalFile(e);
		break;
	case 3:
		if (!loadBaseFile(e->name, &xb.files[xb.nFlashFiles]) ||
		    !loadBaseFile("keyvault.bin", &xb.files[xb.nFlashFiles]) ||
		    !(r = loadBaseFile("KV_dec.bin", &xb.files[xb.nFlashFiles]))) {
			if (e->data)
				free(e->data);
			e->data = xb.files[xb.nFlashFiles].data;
			e->size = xb.files[xb.nFlashFiles].size;
			xb.files[xb.nFlashFiles].data = NULL;
			xb.files[xb.nFlashFiles].size = 0;
		} else if (xb.dumpKv) {
			log_printf(1, "reading %s%s failed, using %s from nand dump\n", xb.baseDir, e->name, e->name);
			if (e->data)
				free(e->data);
			e->data = xb.dumpKv;
			e->size = xb.dumpKvSize;
			xb.dumpKv = NULL;
			xb.dumpKvSize = 0;
			r = 0;
		}
		break;
	case 4:
		if (!loadBaseFile(e->name, &xb.files[xb.nFlashFiles]) ||
		    !loadBaseFile("keyvault_alt.bin", &xb.files[xb.nFlashFiles]) ||
		    !(r = loadBaseFile("KV_alt_dec.bin", &xb.files[xb.nFlashFiles]))) {
			if (e->data)
				free(e->data);
			e->data = xb.files[xb.nFlashFiles].data;
			e->size = xb.files[xb.nFlashFiles].size;
			xb.files[xb.nFlashFiles].data = NULL;
			xb.files[xb.nFlashFiles].size = 0;
		} else if (xb.dumpKvAlt) {
			log_printf(1, "reading %s%s failed, using %s from nand dump\n", xb.baseDir, e->name, e->name);
			if (e->data)
				free(e->data);
			e->data = xb.dumpKvAlt;
			e->size = xb.dumpKvAltSize;
			xb.dumpKvAlt = NULL;
			xb.dumpKvAltSize = 0;
			r = 0;
		}
		break;
	case 23:
		if (xb.type == 1)
			break;
		r = loadBinFile(e);
		if (r)
			break;
		if (e->size & 3) {
			log_printf(1, "\n\n***** ERROR: patch size 0x%x is not a multiple of 4!\n", e->size);
			r = -1;
			break;
		}
		appendAddonPatches(e);
		break;
	case 27:
		if (loadBaseFile(e->name, &xb.files[xb.nFlashFiles]) &&
		    loadBaseFile("config.bin", &xb.files[xb.nFlashFiles]) &&
		    (r = loadBaseFile("config_raw.bin", &xb.files[xb.nFlashFiles]))) {
			if (!xb.dumpConfig)
				break;
			log_printf(1, "reading %s%s failed, using %s from nand dump\n", xb.baseDir, e->name, e->name);
			if (xb.files[xb.nFlashFiles].data)
				free(xb.files[xb.nFlashFiles].data);
			xb.files[xb.nFlashFiles].data = xb.dumpConfig;
			xb.dumpConfig = NULL;
			xb.files[xb.nFlashFiles].size = xb.dumpConfigSize;
			xb.dumpConfigSize = 0;
			r = 0;
		}
		{
			u8 *d = xb.files[xb.nFlashFiles].data;

			__asm__("" : "+a"(d));
			if (d)
				r = extractSmcConfig(e, d, xb.files[xb.nFlashFiles].size);
		}
		break;
	case 2:
		r = loadBaseFile(e->name, &xb.files[xb.nFlashFiles]);
		if (!r) {
			if (e->data)
				free(e->data);
			e->data = xb.files[xb.nFlashFiles].data;
			e->size = xb.files[xb.nFlashFiles].size;
			xb.files[xb.nFlashFiles].data = NULL;
			xb.files[xb.nFlashFiles].size = 0;
		} else {
			if (!xb.dumpSmc)
				break;
			log_printf(1, "reading %s%s failed, using %s from nand dump\n", xb.baseDir, e->name, e->name);
			if (e->data)
				free(e->data);
			e->data = xb.dumpSmc;
			e->size = xb.dumpSmcSize;
			xb.dumpSmc = NULL;
			xb.dumpSmcSize = 0;
			r = 0;
		}
		e->offset = smcSetLoad(e->size);
		if (!e->offset)
			r = -1;
		break;
	default:
		log_printf(1, "####### unhandled bl load %d %s\n", type, e->name);
		break;
	}
	return r;
}

/* load every input of the image (by type), falling back to the nand
   dump's copies, the system update or built-in defaults */
int loadBlFiles(void)
{
	struct fileent *e;
	u32 i;
	u32 r;

	for (i = 1; i < (u32)xb.nFiles; i++) {
		e = &xb.files[i];
		if (strnicmp(e->name, "none", 4) || e->crc)
			r = loadBl(e, i);
		else
			r = 0;
		if (r) {
			log_printf(0, "\n\n**** could not read %s (%i) ****\n\n", e->name, r);
			return -1;
		}
	}
	return 0;
}

/* loadBlFiles for a build from a connected console: the SMC, keyvaults
   and smc_config come from the console, the CB..SE from the glitch dump */
int loadConsoleBlFiles(void)
{
	struct fileent *e, *tmp;
	u32 i;
	int r, type;

	for (i = 1; i < (u32)xb.nFiles; i++) {
		e = &xb.files[i];
		if (!strnicmp(e->name, "none", 4) && !e->crc)
			continue;
		type = e->type;
		switch (type) {
		case 2:
			if (!xb.dumpSmc) {
				log_printf(0, "\n***** ERROR!: acquiring smc binary data failed!\n");
				r = -1;
				goto fail;
			}
			log_printf(1, "using smc binary from console\n");
			if (e->data)
				free(e->data);
			e->data = xb.dumpSmc;
			e->size = xb.dumpSmcSize;
			xb.dumpSmc = NULL;
			xb.dumpSmcSize = 0;
			e->offset = smcSetLoad(e->size);
			if (!e->offset) {
				r = -1;
				goto fail;
			}
			break;
		case 3:
			if (!xb.dumpKv) {
				log_printf(0, "\n***** ERROR!: acquiring keyvault data failed!\n");
				r = -1;
				goto fail;
			}
			log_printf(1, "using keyvault data from console\n");
			if (e->data)
				free(e->data);
			e->data = xb.dumpKv;
			e->size = xb.dumpKvSize;
			xb.dumpKv = NULL;
			xb.dumpKvSize = 0;
			break;
		case 4:
			if (!xb.dumpKvAlt) {
				log_printf(0, "\n***** ERROR!: acquiring keyvault data failed!\n");
				r = -1;
				goto fail;
			}
			log_printf(1, "using keyvault alt data from console\n");
			if (e->data)
				free(e->data);
			e->data = xb.dumpKvAlt;
			e->size = xb.dumpKvAltSize;
			xb.dumpKvAlt = NULL;
			xb.dumpKvAltSize = 0;
			break;
		case 5: case 6: case 7: case 8: case 11: case 12: case 13: case 14:
		case 17: case 18: case 19:
			log_printf(1, "skipping %s%s as it is in glitch bootloader dump\n", xb.baseDir, e->name);
			break;
		case 9: case 10: case 15: case 16: case 20: case 21:
			r = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);
			if (r) {
				if (type == 9) {
					if (!suGetCF(&e->data, &e->size))
						goto fail;
				} else if (type == 10) {
					if (!suGetCG(&e->data, &e->size))
						goto fail;
				} else
					goto fail;
			}
			r = checkBl(e->data, e->size, type, e->crc);
			if (r)
				goto fail;
			break;
		case 23:
			r = loadBinFile(e);
			if (r)
				goto fail;
			if (e->size & 3) {
				log_printf(1, "\n\n***** ERROR: patch size 0x%x is not a multiple of 4!\n", e->size);
				r = -1;
				goto fail;
			}
			appendAddonPatches(e);
			break;
		case 24:
			if (!xb.glitch2mfg || (!loadBaseFile(e->name, e) && e->size == 0x60))
				break;
			e->data = malloc(0x60);
			if (!e->data) {
				r = 1;
				goto fail;
			}
			e->size = 0x60;
			memcpy(e->data, defBl60, 0x60);
			break;
		case 25:
			if (xb.type == 1 || xb.type > 5)
				break;
			if (!loadBaseFile(e->name, e))
				break;
			log_printf(1, "xell not found in perbuild directory, checking firmware /bin folder\n");
			if (!loadBinFile(e))
				break;
			log_printf(1, "xell not found in firmware /bin folder, checking base path\n");
			r = loadLocalFile(e);
			if (r)
				goto fail;
			break;
		case 27:
			if (!xb.dumpConfig) {
				log_printf(0, "\n***** ERROR!: acquiring smc configuration data failed!\n");
				r = -1;
				goto fail;
			}
			log_printf(1, "using smc configuration from console\n");
			tmp = &xb.files[xb.nFlashFiles];
			if (tmp->data)
				free(tmp->data);
			tmp->data = xb.dumpConfig;
			tmp->size = xb.dumpConfigSize;
			xb.dumpConfig = NULL;
			xb.dumpConfigSize = 0;
			r = extractSmcConfig(e, tmp->data, tmp->size);
			if (r)
				goto fail;
			break;
		default:
			log_printf(1, "####### unhandled bl load %d %s\n", type, e->name);
			break;
		}
	}
	return 0;
fail:
	log_printf(0, "\n\n**** could not read %s (%i) ****\n\n", e->name, r);
	return -1;
}

/* apply the second patch set (the CD's) from the patches to the CD and
   drop the first two sets, then check the CD's signature against SB,
   resigning it with the ini's key if that is SB's */
int patchBlsResign(void)
{
	int sb = findFile(11), cd = findFile(7), pt = findFile(23);
	struct fileent *p = &xb.files[pt];
	u8 *d = p->data;
	u32 off, addr, len, i, t;
	int n = 0, ok = 0;

	log_printf(1, "Patching BLs...");
	off = 0;
	while (off < p->size) {
		if (n != 2) {
			addr = getBeU32(d + off);
			t = off + 4;
			if (addr != 0xffffffff) {
				len = getBeU32(d + t) * 4;
				off += 8;
				if (n) {
					if (addr + len > xb.files[cd].size) {
						xb.files[cd].size = (addr + len + 15) & ~15;
						setBeU32(xb.files[cd].size, xb.files[cd].data + 12);
					}
					for (i = 0; i < len; i++)
						xb.files[cd].data[addr + i] = d[off + i];
				}
				off += len;
			} else {
				n++;
				off = t;
			}
		} else {
			for (i = 0; i < p->size - off; i++)
				p->data[i] = p->data[off + i];
			p->size -= off;
			off = p->size;
		}
	}
	log_printf(1, "Done!\n");
	if (sb) {
		log_printf(1, "Checking patched CD signature...");
		if (!blVerifySig(xb.files[cd].data, xb.files[cd].size, xb.files[sb].data + 616, xb.files[sb].data + 914)) {
			if (xb.prvKey) {
				if (!memcmp(xb.prvKey, xb.files[sb].data + 616, 0x110)) {
					log_printf(0, "%s failed signature check, attempting to resign\n", xb.files[cd].name);
					if (!blSign(xb.files[cd].data, xb.files[cd].size, xb.files[sb].data + 616, xb.prvKey, xb.files[sb].data + 914))
						log_printf(0, "\n***** ERROR: failed to resign %s!\n", xb.files[cd].name);
					else {
						log_printf(1, "%s resigned successfully!\n", xb.files[cd].name);
						ok = 1;
					}
				} else
					log_printf(0, "\n***** ERROR: %s failed signature check, RSA key provided does not match the pub key in SB!\n", xb.files[cd].name);
			} else
				log_printf(0, "\n***** ERROR: %s failed signature check, RSA key not available for resigning!\n", xb.files[cd].name);
		} else {
			log_printf(1, "%s signature is good\n", xb.files[cd].name);
			ok = 1;
		}
		if (ok)
			log_printf(1, "Done!\n");
	} else
		log_printf(1, "could not locate SB data to check %s!\n", xb.files[cd].name);
	return ok;
}

/* apply the first two patch sets to the CB_B and the CD (growing them as
   needed) and drop them from the patches, then append blmod.bin to the
   CB_B (or the CD without one). The walk is patchBlsResign's. int size:
   the clamped size's unsigned copy is its own pseudo (esi) while size
   spills. no-early-inlining: the findFile calls are inlined at IPA time in
   call order, so cd's pseudo comes before pt's (loop-entry store order) */
__attribute__((optimize("no-early-inlining")))
void patchBlsBlmod(const void *blmod, int size)
{
	int cd = findFile(7), cbb = findFile(6), pt = findFile(23);
	struct fileent *p = &xb.files[pt];
	u8 *d = p->data;
	u32 off, addr, len, i, max, end, t;
	int n = 0;

	log_printf(1, "Patching BLs...");
	off = 0;
	while (off < p->size) {
		if (n != 2) {
			addr = getBeU32(d + off);
			t = off + 4;
			if (addr != 0xffffffff) {
				len = getBeU32(d + t) * 4;
				off += 8;
				if (!n) {
					if (addr + len > xb.files[cbb].size) {
						xb.files[cbb].size = (addr + len + 15) & ~15;
						setBeU32(xb.files[cbb].size, xb.files[cbb].data + 12);
					}
					for (i = 0; i < len; i++)
						xb.files[cbb].data[addr + i] = d[off + i];
				} else {
					if (addr + len > xb.files[cd].size) {
						xb.files[cd].size = (addr + len + 15) & ~15;
						setBeU32(xb.files[cd].size, xb.files[cd].data + 12);
					}
					for (i = 0; i < len; i++)
						xb.files[cd].data[addr + i] = d[off + i];
				}
				off += len;
			} else {
				n++;
				off = t;
			}
		} else {
			for (i = 0; i < p->size - off; i++)
				p->data[i] = p->data[off + i];
			p->size -= off;
			off = p->size;
		}
	}
	if (blmod && size) {
		log_printf(1, "Done!\n");
		if (!xb.cbb)
			cbb = cd;
		max = xb.cbb ? 0xc000 : 0x10000;
		off = getBeU32(xb.files[cbb].data + 12);
		end = (off + size + 15) & ~15;
		if (end > max) {
			size -= end - max;
			log_printf(0, "***** WARNING: blmod.bin is 0x%x bytes too large, truncating to 0x%x bytes!\n", end - max, max - off);
		}
		log_printf(1, "Adding 0x%x bytes blmod.bin data to %s...", size, xb.cbb ? "CBB" : "CD");
		memcpy(xb.files[cbb].data + off, blmod, size);
		end = (off + size + 15) & ~15;
		i = end - xb.files[cbb].size;
		xb.hdr[0x49] = i >> 8;
		xb.hdr[0x4a] = i;
		xb.files[cbb].size = end;
		setBeU32(end, xb.files[cbb].data + 12);
	}
	log_printf(1, "Done!\n");
}

/* lay the flash files out in the image (raw offsets; a CG/CF pair's
   tail goes in the filesystem) */
void addBlsToImage(void)
{
	struct fileent *e;
	int ecc = imgBigBlock() ? 0xf1f1 : 0x1ffb;
	u32 i;
	int type, j, off = 0;

	for (i = 1; i < (u32)xb.nFlashFiles; i++) {
		e = &xb.files[i];
		type = e->type;
		if (e->offset != 0xffffffff)
			off = e->offset;
		if (!strnicmp(e->name, "none", 4) && !e->crc)
			continue;
		if (xb.type == 2) {
			if (type == 14) {
				off += e->size;
				continue;
			}
			if (type == 21) {
				j = findFile(20);
				log_printf(1, "adding %s at raw offset 0x%08x len 0x%x (end 0x%x, rest in fs)\n",
					   e->name, off, e->size, off + e->size - xb.files[j].fsSize);
				imgAdd(off, e->data, e->size - xb.files[j].fsSize, 0, ecc, 1);
			} else if (type == 10) {
				j = findFile(9);
				log_printf(1, "adding %s at raw offset 0x%08x len 0x%x (end 0x%x, rest in fs)\n",
					   e->name, off, e->size, off + e->size - xb.files[j].fsSize);
				imgAdd(off, e->data, e->size - xb.files[j].fsSize, 0, ecc, 1);
			} else {
				log_printf(1, "adding %s at raw offset 0x%08x len 0x%x (end 0x%x)\n",
					   e->name, off, e->size, off + e->size);
				imgAdd(off, e->data, e->size, 0, ecc, 1);
			}
			off += e->size;
			continue;
		}
		if (type == 9)
			off = imgCfOffset();
		else if (type == 23) {
			off = imgCfOffset() + imgCfSize();
			if (xb.glitch2mfg)
				off += 0x60;
			else if (xb.type == 4 || xb.type == 5)
				off += 0x60;
			else
				off += 0x10;
		}
		if (xb.type == 1 && (type == 23 || type == 25)) {
			log_printf(1, "retail image, skipping %s\n", e->name);
			continue;
		} else if (xb.type > 5) {
			if (type == 23 || type == 25) {
				log_printf(1, "devkit/testkit image, skipping %s\n", e->name);
				continue;
			}
		} else if (type == 25 && e->offset < imgSize()) {
			log_printf(0, "***** WARNING: skipping xell, there doesn't appear to be enough room!\n");
			continue;
		}
		if (type != 10 && type != 16 && type != 24)
			log_printf(1, "adding %s at raw offset 0x%08x len 0x%x (end 0x%x)\n",
				   e->name, off, e->size, off + e->size);
		if (type == 10) {
			j = findFile(9);
			log_printf(1, "adding %s at raw offset 0x%08x len 0x%x (end 0x%x, rest in fs)\n",
				   e->name, off, e->size, off + e->size - xb.files[j].fsSize);
			imgAdd(off, e->data, e->size - xb.files[j].fsSize, 0, ecc, 1);
		} else if (type == 16) {
			j = findFile(15);
			log_printf(1, "adding %s at raw offset 0x%08x len 0x%x (end 0x%x, rest in fs)\n",
				   e->name, off, e->size, off + e->size - xb.files[j].fsSize);
			imgAdd(off, e->data, e->size - xb.files[j].fsSize, 0, ecc, 1);
		} else if (type == 6) {
			if (xb.cbb)
				imgAdd(off, e->data, e->size, 0, ecc, 1);
		} else if (type == 24) {
			if (xb.glitch2mfg || xb.type == 4 || xb.type == 5) {
				log_printf(1, "adding %s at raw offset 0x%08x len 0x%x (end 0x%x)\n",
					   e->name, off, e->size, off + e->size);
				imgAdd(off, e->data, e->size, 0, ecc, 1);
			}
		} else
			imgAdd(off, e->data, e->size, 0, ecc, 1);
		off += e->size;
	}
	if (xb.f01c) {
		j = findFile(14);
		log_printf(1, "adding %s at raw offset 0x%08x len 0x%x (end 0x%x)\n",
			   xb.files[j].name, off, xb.files[j].size, off + xb.files[j].size);
		imgAdd(off, xb.files[j].data, xb.files[j].size, 0, ecc, 1);
	}
}

/* addBlsToImage for an update image: only the bootloaders an update
   replaces */
void addUpdateBls(void)
{
	struct fileent *e;
	int ecc = imgBigBlock() ? 0xf1f1 : 0x1ffb;
	u32 i, off = 0;
	int type, j;

	for (i = 1; i < (u32)xb.nFlashFiles; i++) {
		e = &xb.files[i];
		type = e->type;
		if (__builtin_expect(!isUpdateBl(type), 1))
			continue;
		if (__builtin_expect(e->offset != 0xffffffff, 0))
			off = e->offset;
		if (!strnicmp(e->name, "none", 4) && !e->crc)
			continue;
		if (type == 9) {
			off = imgCfOffset();
			goto add;
		}
		if (type == 23) {
			off = imgCfOffset() + imgCfSize();
			if (xb.glitch2mfg)
				off += 0x60;
			else
				off += 0x10;
		} else if (type == 25) {
			if (e->offset < imgSize()) {
				log_printf(0, "***** WARNING: skipping xell, there doesn't appear to be enough room!\n");
				continue;
			}
			goto add;
		}
		__asm__("" : "+S"(type));
	add:
		if (__builtin_expect(type != 10 && type != 16 && type != 24, 0))
			log_printf(1, "adding %s at raw offset 0x%08x len 0x%x (end 0x%x)\n",
				   e->name, off, e->size, off + e->size);
		if (type == 10) {
			j = findFile(9);
			goto rest;
		} else if (type == 16) {
			j = findFile(15);
		rest:
			log_printf(1, "adding %s at raw offset 0x%08x len 0x%x (end 0x%x, rest in fs)\n",
				   e->name, off, e->size, off + e->size - xb.files[j].fsSize);
			imgAdd(off, e->data, e->size - xb.files[j].fsSize, 0, ecc, 1);
		} else if (type == 24) {
			if (xb.glitch2mfg || xb.type == 4 || xb.type == 5) {
				log_printf(1, "adding %s at raw offset 0x%08x len 0x%x (end 0x%x)\n",
				   e->name, off, e->size, off + e->size);
				imgAdd(off, e->data, e->size, 0, ecc, 1);
			}
		} else
			imgAdd(off, e->data, e->size, 0, ecc, 1);
		off += e->size;
	}
}

/* freeboot.bin: the kernel version string, boot options and buttons */
void patchFreeboot(u8 *buf, int len)
{
	u32 opts = xb.bootFlags & 0xf;
	char pat[] = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX";
	u32 hold[4];		/* the hold address instructions; [2..3]: 9199's */
	u32 *q;
	char *p;

	hold[0] = 0x80;
	hold[1] = 0x78300001;
	log_printf(1, "patching freeboot.bin with with kernel version string '%s'\n", xb.kernelStr);
	log_printf(1, "Boot options set:\n");
	if (opts & 9) {
		log_printf(1, "    - Set debug UART speed to cygnos/demon compatible\n");
		opts = (opts & 6) | 1;
	}
	if (opts & 4) {
		if (logPowerButton(xb.xellButton, "start xell")) {
			log_printf(1, "    - UKNOWN POWER REASON, using eject button\n");
			xb.xellButton = 0x12;
		}
		if (xb.xellAltButton == xb.xellButton)
			xb.xellAltButton = 0;
		if (logPowerButton(xb.xellAltButton, "alternately start xell")) {
			log_printf(1, "    - alternate xell button disabled\n");
			xb.xellAltButton = 0;
		}
	} else if (opts & 2)
		log_printf(1, "    - Tray has to be fully ejected for Xell to start (old nodvd method)\n");
	else
		log_printf(1, "    - When powered on, if tray is not fully closed Xell starts\n");
	if (xb.dualButton == xb.xellButton || xb.dualButton == xb.xellAltButton ||
	    logPowerButton(xb.dualButton, "dual boot"))
		xb.dualButton = 0;
	p = (char *)findInst(buf, len, (u8 *)pat, 32);
	if (p) {
		log_printf(2, "org version %s\n", p);
		strncpy(p, xb.kernelStr, 32);
		log_printf(2, "fin version %s\n", p);
	} else
		log_printf(0, "**** ERROR PATCHING FREEBOOT.BIN for kernel version string!\n");
	if (!strncmp(xb.kernelStr, "9199", 4)) {
		hold[2] = 0x80;
		hold[3] = 0xf8ff1f00;
		log_printf(1, "9199 ini string detected, patching to old hold address\n");
		q = (u32 *)findInst(buf, len, (u8 *)hold, 8);
		if (q)
			memcpy(q, hold + 2, 8);
	}
}

/* encodeBls for an update image: only the CF and CG */
int encodeUpdateBls(int unused, u16 ldv)
{
	struct fileent *e;
	u32 i;
	int j;

	for (i = 1; i < (u32)xb.nFlashFiles; i++) {
		e = &xb.files[i];
		if (!strnicmp(e->name, "none", 4) && !e->crc)
			continue;
		switch (e->type) {
		case 9:
			log_printf(1, "encoding %s size 0x%x\n", e->name, e->size);
			j = findFile(10);
			cfEncrypt(e, xb.files[j].size, ldv, 0, imgCfSize());
			break;
		case 10:
			log_printf(1, "encoding %s size 0x%x\n", e->name, e->size);
			j = findFile(9);
			cgEncrypt(e->data, xb.files[j].key, e->key, e->size);
			break;
		}
	}
	return 0;
}

/* the size of the bootloader area (where the filesystem can start),
   setting the patch slot offset; a multiple of 0x4000 */
u32 calcBlAreaSize(void)
{
	u32 size, xs, x;

	if (xb.type == 2) {
		x = findFile(5);
		size = findFileOffset(5) + xb.files[x].size;
		x = findFile(7);
		size += xb.files[x].size;
		if (xb.f01c) {
			x = findFile(14);
			size += xb.files[x].size;
		}
	} else if (xb.type > 5) {
		x = findFile(11);
		size = findFileOffset(11) + xb.files[x].size;
		x = findFile(12);
		size += xb.files[x].size;
		x = findFile(13);
		size += xb.files[x].size;
		x = findFile(14);
		/* the sum so far in ebx (esi up to the 13 lookup), as in the
		   original: IRA otherwise keeps it in esi */
		__asm__("" : "+b"(size));
		size += xb.files[x].size;
		setPatchSlot(size);
		size += 2 * imgCfSize();
	} else {
		size = findFileOffset(5) + findFileSize(5);
		size += findFileSize(6);
		size += findFileSize(7);
		size += findFileSize(8);
		if (xb.type != 1) {
			x = findFile(25);
			if (xb.files[x].offset > size) {
				xs = xb.files[x].size;
				if (xs > 0x40000)
					log_printf(0, "***** WARNING: xell is unexpectedly larger than 256KiB!!\n");
				else
					xs = 0x40000;
				size = xb.files[x].offset + xs;
			}
		}
		size = (size + 0xffff) & ~0xffff;
		setPatchSlot(size);
		size += 2 * imgCfSize();
	}
	if (size & 0x3fff)
		size = (size + 0x3fff) & ~0x3fff;
	return size;
}

/* encrypt (and for retail/glitch builds zeropair) each bootloader with
   its predecessor's key, prepare the SMC and keyvaults; 1 if the SMC
   could not be prepared */
int encodeBls(u8 *salt, u16 ldv)
{
	struct fileent *e;
	u32 i;
	int type, zero, j;

	for (i = 1; i < (u32)xb.nFlashFiles; i++) {
		e = &xb.files[i];
		if (!strnicmp(e->name, "none", 4) && !e->crc)
			continue;
		type = e->type;
		if (xb.type == 2) {
			log_printf(1, "encoding %s size 0x%x (JTAG)\n", e->name, e->size);
			switch (type) {
			case 1:
				if (!memcmp(e->data, defPayload, 0x200))
					patchPayloadSize(e->data, e->size, xb.files[findFile(22)].size);
				break;
			case 2:
				if (smcPrepare(e->data, salt, e->size))
					return 1;
				break;
			case 3:
				kvPrepare(e, 0);
				break;
			case 5:
				showExpectedFuses(getBeU32(e->data + 944), getBeU16(e->data + 2),
						  xb.files[findFile(24)].data, xb.f01c);
				cbaEncrypt(salt, e->data, e->key, e->size, 0);
				break;
			case 7:
				cdEncrypt(e->data, xb.files[findFile(5)].key, e->key, e->size);
				break;
			case 9:
				cfEncrypt(e, xb.files[findFile(10)].size, ldv, 0, imgCfSize());
				break;
			case 10:
				cgEncrypt(e->data, xb.files[findFile(9)].key, e->key, e->size);
				break;
			case 17:
				showExpectedFuses(getBeU32(e->data + 944), getBeU16(e->data + 2), NULL, xb.f01c);
				cbaEncrypt2(salt, e->data, e->key, e->size, 1);
				break;
			case 18:
				cdEncrypt(e->data, xb.files[findFile(17)].key, e->key, e->size);
				break;
			case 19:
				ceEncrypt(e->data, xb.files[findFile(18)].key, e->key, e->size);
				break;
			case 20:
				ldv += cfEncrypt(e, xb.files[findFile(21)].size, ldv, 1, imgCfSize());
				break;
			case 21:
				cgEncrypt(e->data, xb.files[findFile(20)].key, e->key, e->size);
				break;
			case 22:
				if (!memcmp(e->data, defCore, 0xd40))
					patchFreeboot(e->data, e->size);
				else if (xb.bootFlags)
					log_printf(0, "\n******* WARNING: CYGNOS, DEMON and NODVD command line options are ignored due to external freeboot.bin!\n\n");
				break;
			}
		} else if (xb.type <= 3) {
			if (type == 24) {
				if (xb.glitch2mfg)
					log_printf(1, "encoding %s size 0x%x\n", e->name, e->size);
				continue;
			}
			log_printf(1, "encoding %s size 0x%x\n", e->name, e->size);
			switch (type) {
			case 2:
				if (smcPrepare(e->data, salt, e->size))
					return 1;
				break;
			case 3:
				kvPrepare(e, 0);
				break;
			case 5:
				if (xb.cbb) {
					cbaEncrypt(salt, e->data, e->key, e->size, 1);
					break;
				}
				showExpectedFuses(getBeU32(e->data + 944), getBeU16(e->data + 2), NULL, xb.f01c);
				if (xb.type != 1)
					cbaEncryptZero(e->data, e->key, e->size);
				else
					cbaEncrypt(salt, e->data, e->key, e->size, 0);
				break;
			case 6:
				if (!xb.cbb)
					break;
				zero = checkZeros(cpuKey, 16);
				j = findFile(24);
				if (xb.glitch2mfg)
					showExpectedFuses(getBeU32(e->data + 944), getBeU16(e->data + 2), xb.files[j].data, xb.f01c);
				else
					showExpectedFuses(getBeU32(e->data + 944), getBeU16(e->data + 2), NULL, xb.f01c);
				if (zero) {
					log_printf(1, "CPU key is all zeros, zeropairing CB_B\n");
					xb.cfLdv = 0;
				}
				j = findFile(5);
				cbbEncrypt(salt, e->data, xb.files[j].key, xb.files[j].data, e->key, e->size, zero);
				break;
			case 7:
				if (xb.cbb)
					cdEncrypt(e->data, xb.files[findFile(6)].key, e->key, e->size);
				else {
					j = findFile(5);
					if (xb.type != 1)
						cdEncrypt(e->data, xb.files[j].key, e->key, e->size);
					else
						cdEncryptCpu(e->data, xb.files[j].key, e->key, e->size);
				}
				break;
			case 8:
				ceEncrypt(e->data, xb.files[findFile(7)].key, e->key, e->size);
				break;
			case 9:
				cfEncrypt(e, xb.files[findFile(10)].size, ldv, 0, imgCfSize());
				break;
			case 10:
				cgEncrypt(e->data, xb.files[findFile(9)].key, e->key, e->size);
				break;
			}
		} else if (type != 24) {
			log_printf(1, "encoding %s size 0x%x\n", e->name, e->size);
			switch (type) {
			case 2:
				if (smcPrepare(e->data, salt, e->size))
					return 1;
				break;
			case 3:
				kvPrepare(e, 0);
				break;
			case 4:
				kvPrepare(e, 1);
				break;
			case 7:
				cdEncrypt(e->data, xb.files[findFile(12)].key, e->key, e->size);
				break;
			case 8:
				ceEncrypt(e->data, xb.files[findFile(7)].key, e->key, e->size);
				break;
			case 9:
				cfEncrypt(e, xb.files[findFile(10)].size, ldv, 0, imgCfSize());
				break;
			case 10:
				cgEncrypt(e->data, xb.files[findFile(9)].key, e->key, e->size);
				break;
			case 11:
				if (xb.type == 4 || xb.type == 5) {
					j = findFile(24);
					if ((xb.flags & 7) <= 4)
						showExpectedFuses(0x1000000, getBeU16(e->data + 2), NULL, xb.f01c);
					else
						showExpectedFuses(0x3000000, getBeU16(e->data + 2), NULL, xb.f01c);
					log_printf(1, "zeropairing SB\n");
					setFuseCpuKey(xb.files[j].data);
					cbaEncryptZero(e->data, e->key, e->size);
					break;
				}
				showExpectedFuses(getBeU32(e->data + 944), getBeU16(e->data + 2), NULL, xb.f01c);
				if (checkZeros(cpuKey, 16)) {
					log_printf(1, "CPU key is all zeros, zeropairing SB\n");
					xb.cfLdv = 0;
					cbaEncryptZero(e->data, e->key, e->size);
				} else
					cbaEncrypt(salt, e->data, e->key, e->size, 0);
				break;
			case 12:
				cdEncryptZero(e->data, e->key, e->size);
				break;
			case 13:
				cdEncrypt(e->data, xb.files[findFile(12)].key, e->key, e->size);
				break;
			case 14:
				ceEncrypt(e->data, xb.files[findFile(13)].key, e->key, e->size);
				break;
			case 15:
				cfEncrypt(e, xb.files[findFile(16)].size, ldv, 0, imgCfSize());
				break;
			case 16:
				cgEncrypt(e->data, xb.files[findFile(15)].key, e->key, e->size);
				break;
			case 23:
			case 25:
				break;
			default:
				log_printf(1, "****** Unhandled BL typ %d ******\n", type);
				break;
			}
		}
	}
	if (xb.f01c) {
		/* the SE that replaced the CF follows the CD */
		i = findFile(14);
		j = findFile(7);
		log_printf(1, "re-encoding %s size 0x%x\n", xb.files[i].name, xb.files[i].size);
		ceEncrypt(xb.files[i].data, xb.files[j].key, xb.files[i].key, xb.files[i].size);
	}
	return 0;
}

/* build the flash image: header, bootloaders (loaded, checked, patched,
   encrypted, laid out), the CG overflow, firmware and security files,
   Mobile*.dat, smc_config, the filesystem, [rawpatch] data */
int buildFlash(void)
{
	struct fileent f;
	struct fileent *tmp;
	u8 salt[16];
	u8 ts[4];
	FILETIME ft;
	const char *name, *base;
	u32 area, off, a, b, raw, save, i, k;
	int fuse, blocks, r, cf, cg, region, t;
	char last;

	memset(salt, 0, sizeof(salt));
	fuse = 1;
	if (xb.type != 2)
		fuse = xb.glitch2mfg || xb.type == 4 || xb.type == 5;
	if (xb.fromConsole) {
		log_printf(1, "\n------ Copying bootloader image to flash image ------ \n");
		r = checkBootImage(1);
		if (r) {
			log_printf(0, "******* ERROR: bootloaders retrieved from console are inconsistent, cannot proceed!\n\n");
			return r;
		}
	} else {
		log_printf(1, "Writing initial header to flash image\n");
		imgWriteHeader();
	}
	suLoadDir(xb.dataDir);
	log_printf(1, "\n------ Loading bootloaders and required security files ------\n");
	if (xb.fromConsole)
		r = loadConsoleBlFiles();
	else
		r = loadBlFiles();
	if (r) {
		log_printf(0, "******* ERROR: critical bootloader files are missing, cannot proceed!\n\n");
		return r;
	}
	if (!xb.fromConsole && !verifyBlSigs())
		return 1;
	log_printf(1, "done!\n");
	blocks = imgFsBlock();
	area = calcBlAreaSize();
	if (blocks)
		area = blocks << 14;
	else
		blocks = area >> 14;
	if (xb.type == 3) {
		log_printf(1, "\n------ Patching BLs and modifying patches ------\n");
		if (xb.fromConsole)
			fixupPatchSet();
		else {
			memset(&f, 0, sizeof(f));
			if (!loadBaseFile("blmod.bin", &f)) {
				patchBlsBlmod(f.data, f.size);
				free(f.data);
			} else if (xb.consoleBlmod && xb.consoleBlmodSize) {
				patchBlsBlmod(xb.consoleBlmod, xb.consoleBlmodSize);
				free(xb.consoleBlmod);
			} else
				patchBlsBlmod(NULL, 0);
		}
	} else if (xb.type == 4 || xb.type == 5) {
		log_printf(1, "\n------ Patching BLs and modifying patches ------\n");
		if (!patchBlsResign())
			return 1;
	}
	if (!xb.fromConsole && xb.type != 1 && xb.type <= 5) {
		log_printf(1, "\n------ Patching boot reasons and options into flash header ------\n");
		patchHeaderOpts();
	}
	log_printf(1, "\n------ Encrypting and finalizing bootloaders ------\n");
	keysInit(xb.randomKeys);
	if (fuse) {
		tmp = &xb.files[findFile(24)];
		setFuseCpuKey(tmp->data);
		if (xb.type != 2)
			tmp->offset = imgCfOffset() + imgCfSize();
	}
	if (!xb.fromConsole) {
		if (encodeBls(salt, blocks))
			return -4;
	} else if (encodeUpdateBls((int)salt, blocks))
		return -4;
	if (fuse)
		showFuses(1, "\nVirtual Fuses set to:", xb.files[findFile(24)].data);
	log_printf(1, "done!\n\n------ Adding bootloaders to flash image ------\n");
	if (!xb.fromConsole)
		addBlsToImage();
	else
		addUpdateBls();
	if (!imgFsBlock()) {
		log_printf(1, "Fixing up FS table...");
		imgFixFsTable(area);
		imgSetSize(area);
		log_printf(1, "done!\n");
	}
	if (imgFsBlock())
		imgSetSize(imgFsBlock() << 14);

	/* the CG's patch slot overflow goes in the filesystem */
	if (xb.type != 2) {
		if (xb.files[findFile(9)].fsSize) {
			off = imgSize();
			cf = findFile(9);
			cg = findFile(10);
			log_printf(1, "Writing zeropair CG patch slot overflow data to sysupdate.xexp1\n");
			log_printf(1, "\tat raw offset 0x%x len 0x%08x (end: 0x%08x)...", off, xb.files[cf].fsSize, off + xb.files[cf].fsSize);
			makeTimestamp(ts, NULL);
			imgAddFsFile("sysupdate.xexp1", xb.files[cg].data + xb.files[cf].fsOffset, ts, xb.files[cf].fsSize);
			log_printf(1, "done!\n");
		}
	} else {
		off = imgSize();
		if (xb.files[findFile(20)].fsSize) {
			cf = findFile(20);
			cg = findFile(21);
			log_printf(1, "Writing CG patch slot overflow data to sysupdate.xexp1\n");
			log_printf(1, "\tat raw offset 0x%x len 0x%08x (end: 0x%08x)...", off, xb.files[cf].fsSize, off + xb.files[cf].fsSize);
			makeTimestamp(ts, NULL);
			imgAddFsFile("sysupdate.xexp1", xb.files[cg].data + xb.files[cf].fsOffset, ts, xb.files[cf].fsSize);
			log_printf(1, "done!\n");
		}
		if (xb.files[findFile(9)].fsSize) {
			cf = findFile(9);
			cg = findFile(10);
			log_printf(1, "Writing target CG patch slot overflow data to sysupdate.xexp2\n");
			log_printf(1, "\tat raw offset 0x%x len 0x%08x (end: 0x%08x)...", off, xb.files[cf].fsSize, off + xb.files[cf].fsSize);
			makeTimestamp(ts, NULL);
			imgAddFsFile("sysupdate.xexp2", xb.files[cg].data + xb.files[cf].fsOffset, ts, xb.files[cf].fsSize);
			log_printf(1, "done!\n");
		}
	}

	tmp = &xb.files[xb.nFlashFiles];
	log_printf(1, "\n------ adding %d firmware files ------\n", xb.nFirmware);
	for (i = 0; i < xb.nFirmware; i++) {
		name = xb.firmware[i];
		strcpy(f.name, name);
		last = f.name[strlen(f.name) - 1];
		if (!strnicmp("sysupdate.xexp", f.name, 14)) {
			log_printf(1, "\n******* WARNING: firmware file %s ignored, 'sysupdate.xexp' is a reserved name!\n\n", f.name);
			continue;
		}
		if (!xb.firmwareCrc[i])
			r = loadInputFile(f.name, tmp, 0, 0, ts, 0, 1, 0);
		else if (last == 'p') {
			/* a patch (.xexp): the target's comes as .xexp1, a JTAG's as .xexp2 */
			strcat(xb.firmware[i], xb.type == 2 ? "2" : "1");
			r = loadInputFile(f.name, tmp, 0, xb.firmwareCrc[i], ts, 1, 1, 1);
			if (r) {
				strcat(f.name, "1");
				r = loadInputFile(f.name, tmp, 0, xb.firmwareCrc[i], ts, 0, 1, 1);
				if (r) {
					f.name[strlen(f.name) - 1] = '2';
					r = loadInputFile(f.name, tmp, 0, xb.firmwareCrc[i], ts, 0, 1, 1);
				}
			}
		} else
			r = loadInputFile(f.name, tmp, 0, xb.firmwareCrc[i], ts, 1, 1, 1);
		if (r) {
			if (xb.firmwareCrc[i]) {
				log_printf(0, "***** could not read file '%s' *****\n", name);
				log_printf(0, "\n******* ERROR: critical firmware file missing, cannot proceed!\n\n");
				return r;
			}
			log_printf(1, "***** could not read file '%s', skipping *****\n", name);
			continue;
		}
		base = strrchr(name, '/');
		if (!base)
			base = strrchr(name, '\\');
		if (base)
			base++;
		else
			base = name;
		off = imgSize();
		log_printf(1, "\tadding as %s at raw offset 0x%x len 0x%08x (end 0x%08x)\n", base, off, tmp->size, off + tmp->size);
		imgAddFsFile(base, tmp->data, ts, tmp->size);
	}

	log_printf(1, "\n------ adding %d security files ------\n", xb.nFlashFiles2);
	if (xb.nFlashFiles2) {
		memset(tmp, 0, sizeof(*tmp));
		setBeU32(0, ts);
		for (k = 0;;) {
			name = xb.flashFiles[k];
			log_printf(1, "<- Processing %s ->\n", name);
			if (!loadBaseFileMeta(name, tmp, ts))
				goto got;
			if (!(xb.bootFlags & 0x1000000)) {
				if (tmp->data)
					free(tmp->data);
				if (suGetFile(name, &tmp->data, &tmp->size)) {
					log_printf(1, "\tcould not read %s, using data from SUPD...\n", name);
					goto got;
				}
			}
			if (xb.flashBuf[k]) {
				if (tmp->data)
					free(tmp->data);
				tmp->data = xb.flashBuf[k];
				tmp->size = xb.flashSize[k];
				log_printf(1, "\tcould not read %s, using data from previous parse...\n", name);
				goto got;
			}
			if (!strcmp(name, "secdata.bin") || !strcmp(name, "extended.bin")) {
				tmp->size = 0;
				goto got;
			}
			if (!strcmp(name, "fcrt.bin")) {
				region = kvGetGameRegion();
				if (region) {
					log_printf(0, "\n\n***** ERROR: %s not found, keyvault has this file flagged as required but it's being skipped *****\n", name);
					if (xb.type != 1 && xb.type <= 5) {
						if (region == 1)
							log_printf(0, "             note - on hacked images a nofcrt patch should allow the drive and machine to function\n");
						else {
							log_printf(0, "             note - on hacked images a nofcrt patch WILL NOT allow the drive to function\n");
							log_printf(0, "             but should allow the machine to boot normally\n");
						}
					}
				} else
					log_printf(1, "\t%s not found and not required by keyvault, skipped\n", name);
			} else
				log_printf(0, "***** WARNING: %s not found, skipping *****\n", name);
			goto next;
got:
			if (getBeU32(ts))
				timestampToFileTime((u16 *)ts, &ft);
			else
				makeTimestamp(ts, &ft);
			if (!strcmp(name, "secdata.bin"))
				secdataPrepare(tmp, (u8 *)&ft);
			else if (!strcmp(name, "extended.bin"))
				extendedPrepare(tmp);
			else if (!strcmp(name, "dae.bin"))
				daeEncrypt(tmp->data, tmp->size, (u8 *)&ft);
			else if (!strcmp(name, "crl.bin"))
				crlEncrypt(tmp->data, tmp->size, (u8 *)&ft);
			else if (!strcmp(name, "fcrt.bin"))
				fcrtEncrypt(tmp->data, tmp->size);
			else if (!strcmp(name, "odd.bin")) {
				if (xb.oddTime[k])
					setBeU32(xb.oddTime[k], ts);
			} else
				log_printf(0, "******* WARNING: writing %s%s as-is to NAND, if .meta was not included it may be invalid!\n", xb.baseDir, name);
			imgAddSecFile(name, tmp->data, ts, tmp->size);
next:
			if (tmp->data) {
				free(tmp->data);
				tmp->data = NULL;
			}
			if (++k >= xb.nFlashFiles2)
				break;
			memset(tmp, 0, sizeof(*tmp));
			setBeU32(0, ts);
			log_printf(1, "\n");
		}
	}

	log_printf(1, "\n------ checking for Mobile*.dat ------\n");
	for (k = 0; k < 11; k++) {
		if (k == 9) {
			strcpy(f.name, "Statistics.settings");
			raw = statisticsOffset(xb.bigBlock, xb.type > 5, (xb.flags & 0x10000000) != 0, NULL, NULL);
		} else if (k == 10) {
			strcpy(f.name, "Manufacturing.data");
			raw = manufacturingOffset(xb.bigBlock, xb.type > 5, (xb.flags & 0x10000000) != 0, NULL, NULL);
		} else {
			strcpy(f.name, "MobileA.dat");
			f.name[6] = 'B' + k;
			raw = 0;
		}
		if (!loadBaseFile(f.name, tmp)) {
			log_printf(1, "%s found, adding from file\n", f.name);
			if (raw) {
				save = imgSize();
				imgAddRaw(f.name, tmp->data, tmp->size, raw);
				imgSetSize(save);
			} else {
				t = imgAddMobile(tmp->data, tmp->size, '1' + k);
				if (t && k <= 8) {
					setBeU16(t, (u8 *)&xb.mobileTab[k].type);
					setBeU16(tmp->size >= 0x4000 ? 0 : tmp->size, (u8 *)&xb.mobileTab[k].size);
				}
			}
		} else if (xb.mobile[k].data && xb.mobile[k].size) {
			log_printf(1, "%s found, adding from previous parse\n", f.name);
			if (raw) {
				save = imgSize();
				imgAddRaw(f.name, xb.mobile[k].data, xb.mobile[k].size, raw);
				imgSetSize(save);
			} else {
				t = imgAddMobile(xb.mobile[k].data, xb.mobile[k].size, '1' + k);
				if (t && k <= 8) {
					setBeU16(t, (u8 *)&xb.mobileTab[k].type);
					setBeU16(xb.mobile[k].size > 0x3fff ? 0 : xb.mobile[k].size, (u8 *)&xb.mobileTab[k].size);
				}
			}
		}
	}
	a = imgFsAligned();
	b = imgFsAligned();
	log_printf(1, "\n------ adding smc_config.bin ------\n");
	imgAddSmcConfig(xb.files[findFile(27)].data);
	log_printf(1, "\n------ cleaning up image ------\n");
	log_printf(1, "Fixing up empty FS block entries...");
	imgFixEmptyFs(a);
	log_printf(1, "done!\nWriting FS table to image ");
	imgWriteFsTable(b);
	log_printf(1, "done!\n");
	if (xb.flags & 0x10000000) {
		/* MMC: two anchor blocks */
		xb.anchorNum = 1;
		shaHeader(xb.anchor);
		imgCopyAnchor(1);
		xb.anchorNum = 2;
		shaHeader(xb.anchor);
		imgCopyAnchor(2);
	}
	for (k = 0; k < 19; k++) {
		if (!xb.files[k].data || !xb.files[k].size)
			xb.files[k].size = 0;
		else {
			free(xb.files[k].data);
			xb.files[k].data = NULL;
		}
	}
	if (xb.nRawPatches) {
		log_printf(1, "\n------ adding [rawpatch] data ------\n");
		f.data = NULL;
		for (k = 0; k < xb.nRawPatches; k++) {
			r = loadInputFile(xb.rawPatch[k].name, &f, 0, 0, ts, 0, 0, 0);
			if (r) {
				log_printf(0, "***** ERROR: could not load [rawpatch] file '%s'!!\n", xb.rawPatch[k].name);
				return r;
			}
			off = xb.rawPatch[k].offset;
			if (off + f.size > xb.userSize) {
				log_printf(1, "[rawpatch] (%d): '%s' copied to offset 0x%x (len: 0x%x) would exceed user size 0x%x!\n\n",
					   k + 1, xb.rawPatch[k].name, off, f.size, xb.userSize);
				free(f.data);
				return -1;
			}
			memcpy(xb.hdr + off, f.data, f.size);
			log_printf(1, "[rawpatch] (%d): '%s' copied to offset 0x%x len: 0x%x (end: 0x%x) successfully!\n\n",
				   k + 1, xb.rawPatch[k].name, off, f.size, off + f.size);
			free(f.data);
			f.data = NULL;
		}
		log_printf(1, "done!\n");
	}
	log_printf(1, "\n------ finalizing image ------\n");
	return imgFinalize();
}

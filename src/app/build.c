/* build: reading the image's input files (with crc32 checks against the
   ini), bootloader checks, patches and payloads, encoding the flash.
   Mixed object: the functions here are spliced into build.s
   (re/splice.py), which still holds the rest and the data, so strings
   name the .s's (splice.py drops gcc's copies; static arrays rather
   than externs so that gcc still folds strlen of them).
   wip/app/build.c is the whole draft; wip/mixed.py makes this file
   from it. */
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
	struct fileent files[35];	/* 41eb0 [19..34]: addon patches */
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
int blSign(u8 *bl, unsigned int len, const void *pubKey, const void *prvKey, const u8 *salt);
int blCheckHash(u8 *bl, unsigned int len, const u8 *expect);
int blHashAndSign(u8 *bl, unsigned int len, u8 *prev, unsigned int prevLen, u8 *hashOut,
	const void *pubKey, const void *prvKey);
u32 calcConfigSum(const u8 *buf);
int patchSmcConfig(u8 *smc);
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

/* strings in build.s */
static const char bd_458ca4[] = "rb";
static const char bd_458ca8[] = "\n******WARNING: '%s' is a 0 byte file, loading skipped!\n";
static const char bd_458ce1[] = "reading %s (0x%x bytes)";
static const char bd_458cf9[] = "\n";
static const char bd_458cfc[] = "reading %s (0x%x b pad 0x%x b)";
static const char bd_458d1b[] = " (crc32: 0x%08x ini: 0x%08x)\n";
static const char bd_458d3c[] = "\n******WARNING: '%s' crc32: 0x%08x expected: 0x%08x\n";
static const char bd_458d74[] = "**** using default time!!! ****\n";
static const char bd_458d98[] = "**** %s metadata found, not using system time *****\n\n";
static const char bd_458f80[] = "Target temps: Cpu: %3d\370C Gpu: %3d\370C Edram: %3d\370C\n";
static const char bd_458fb4[] = "Max temps   : Cpu: %3d\370C Gpu: %3d\370C Edram: %3d\370C\n";
static const char bd_458fe6[] = "Cpu Fan     : ";
static const char bd_458ff5[] = "%d%%%% (overridden)\n";
static const char bd_45900a[] = "(auto)\n";
static const char bd_459012[] = "Gpu Fan     : ";
static const char bd_459021[] = "MAC Address : ";
static const char bd_459030[] = "\nAVRegion    : 0x%08x (NTSC-M)\n";
static const char bd_459050[] = "\nAVRegion    : 0x%08x (NTSC-J)\n";
static const char bd_459070[] = "\nAVRegion    : 0x%08x (PAL50)\n";
static const char bd_459090[] = "\nAVRegion    : 0x%08x (PAL60)\n";
static const char bd_4590b0[] = "\nAVRegion    : 0x%08x (Unknown)\n";
static const char bd_4590d1[] = "GameRegion  : 0x%04x ";
static const char bd_4590e7[] = "(NTSC/US)\n";
static const char bd_4590f2[] = "(NTSC/JAP)\n";
static const char bd_4590fe[] = "(NTSC/KOR)\n";
static const char bd_45910a[] = "(NTSC/HK)\n";
static const char bd_459115[] = "(PAL/EU)\n";
static const char bd_45911f[] = "(PAL/AUS)\n";
static const char bd_45912a[] = "(DEVKIT)\n";
static const char bd_459134[] = "(Unknown)\n";
static const char bd_45913f[] = "DVDRegion   : %d\n";
static const char bd_459151[] = "resetKey    : ";
static const char bd_459160[] = "%c";
static const char bd_459164[] = "Ini value %d for %s is out of range (%d-%d), not using\n";
static const char bd_459955[] = "none";
static const char bd_459e3c[] = "\tPatching header for slower demon/cygnos UART speed\n";
static const char bd_459e74[] = "\tPatching header for xell power reason\n";
static const char bd_459e9c[] = "\tPatching header for xell alt power reason\n";
static const char bd_459ec8[] = "blmod.bin";
static const char bd_459ed2[] = "sum1:";
static const char bd_459ed8[] = "sum2:";
static const char bd_459ede[] = "sum3:";
static const char bd_459ee4[] = "fin :";
static const char bd_45a0bc[] = "    - console power button is being used to %s \n";
static const char bd_45a0f0[] = "    - console DVD eject button is being used to %s \n";
static const char bd_45a128[] = "    - IR remote power button is being used to %s \n";
static const char bd_45a15c[] = "    - IR remote guide/X button is being used to %s \n";
static const char bd_45a194[] = "    - IR remote windows button is being used to %s \n";
static const char bd_45a1cc[] = "    - KIOSK debug pin is being used to %s \n";
static const char bd_45a1f8[] = "    - wireless controller powering on console is being used to %s \n";
static const char bd_45a23c[] = "wired controller (rear top usb port) is being used to %s \n";
static const char bd_45a278[] = "wired controller (INVALID FOR FATS!!) is being used to %s \n";
static const char bd_45a2b4[] = "wired controller (rear middle usb port) is being used to %s \n";
static const char bd_45a2f4[] = "wired controller (rear bottom usb port) is being used to %s \n";
static const char bd_45a334[] = "wired controller (rear usb port) is being used to %s \n";
static const char bd_45a36c[] = "wired controller (front left usb port) is being used to %s \n";
static const char bd_45a3ac[] = "wired controller (front top usb port) is being used to %s \n";
static const char bd_45a3e8[] = "wired controller (front right usb port) is being used to %s \n";
static const char bd_45a428[] = "wired controller (front bottom usb port) is being used to %s \n";
static const char bd_45a590[] = "patching freeboot.bin with with kernel version string '%s'\n";
static const char bd_45a5cc[] = "Boot options set:\n";
static const char bd_45a5e0[] = "    - Set debug UART speed to cygnos/demon compatible\n";
static const char bd_45a618[] = "    - Tray has to be fully ejected for Xell to start (old nodvd method)\n";
static const char bd_45a664[] = "    - When powered on, if tray is not fully closed Xell starts\n";
static const char bd_45a6a4[] = "start xell";
static const char bd_45a6b0[] = "    - UKNOWN POWER REASON, using eject button\n";
static const char bd_45a6df[] = "alternately start xell";
static const char bd_45a6f8[] = "    - alternate xell button disabled\n";
static const char bd_45a71e[] = "dual boot";
static const char bd_45a728[] = "org version %s\n";
static const char bd_45a738[] = "fin version %s\n";
static const char bd_45a748[] = "**** ERROR PATCHING FREEBOOT.BIN for kernel version string!\n";
static const char bd_45a785[] = "9199";
static const char bd_45a78c[] = "9199 ini string detected, patching to old hold address\n";
static const char bd_45a7c4[] = "patching payload.bin to load size 0x%x (0x%x reps)\n";
static const char bd_45a7f8[] = "org li %r4, %02x%02x\n";
static const char bd_45a80e[] = "fin li %r4, %02x%02x\n";
static const char bd_45a8af[] = "encoding %s size 0x%x\n";

/* still in build.s */
int loadInputFile(const char *name, struct fileent *e, int pad, u32 crc, u8 *meta,
		  int su, int fs, int common);
int checkBl(u8 *bl, u32 size, int type, u32 crc);
int extractSmcConfig(struct fileent *e, u8 *buf, u32 size);
void appendAddonPatches(struct fileent *e);
void fixupPatchSet(void);
int patchSmcConfig(u8 *smc);
int verifyBlSigs(void);
int loadBlFiles(void);
int loadConsoleBlFiles(void);
int patchBlsResign(void);
void patchBlsBlmod(const void *blmod, u32 size);
void addBlsToImage(void);
void addUpdateBls(void);
u32 calcBlAreaSize(void);
int encodeBls(u8 *salt, u16 ldv);
int buildFlash(void);

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

	f = fopen(name, bd_458ca4);
	if (!f)
		return -1;
	if (e->data)
		free(e->data);
	size = getFileSize(f);
	if (!size) {
		fclose(f);
		log_printf(0, bd_458ca8, name);
		return 1;
	}
	e->size = size;
	if (pad && (size & 15))
		e->size = (size + 15) & ~15;
	if (verbose) {
		if (size != e->size)
			log_printf(1, bd_458cfc, name, size, (size + 15) & ~15);
		else
			log_printf(1, bd_458ce1, name, size);
	}
	e->data = calloc(e->size + 0x10000, 1);
	if (!e->data)
		return -2;
	fread(e->data, size, 1, f);
	fclose(f);
	if (crc) {
		c = crc32(e->data, size);
		log_printf(1, bd_458d1b, c, crc);
		if (crc != c) {
			log_printf(0, bd_458d3c, name, c, crc);
			return 1;
		}
	} else
		log_printf(1, bd_458cf9);
	return 0;
}

int readMetaFile(const char *name, u8 *meta)
{
	FILE *f;

	f = fopen(name, bd_458ca4);
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
		log_printf(2, bd_458d74);
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
				log_printf(1, bd_458d98, path);
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
			log_printf(1, bd_458d98, path);
		else
			makeTimestamp(meta, NULL);
	}
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
			log_printf(0, bd_459164, v, name, lo, hi);
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

int blmodMissing(struct fileent *e)
{
	return loadBaseFile(bd_459ec8, e) != 0;
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
	log_printf(1, bd_459ed2);
	display_buffer_hex(sum, 32, 1);
	XeCryptRotSum(sum, b, blen >> 3);
	log_printf(1, bd_459ed8);
	display_buffer_hex(sum, 32, 1);
	XeCryptShaInit(&sha);
	XeCryptShaUpdate(&sha, sum, 32);
	XeCryptShaUpdate(&sha, sum, 32);
	XeCryptShaUpdate(&sha, a, alen);
	XeCryptShaUpdate(&sha, b, blen);
	for (i = 0; i < 32; i++)
		sum[i] = ~sum[i];
	log_printf(1, bd_459ede);
	display_buffer_hex(sum, 32, 1);
	XeCryptShaUpdate(&sha, sum, 32);
	XeCryptShaUpdate(&sha, sum, 32);
	XeCryptShaFinal(&sha, out, outlen);
	log_printf(1, bd_459ee4);
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
int isUpdateBl(u32 type)
{
	return type == 9 || type == 10 || type == 15 || type == 16 ||
	       type == 23 || type == 24 || type == 25;
}

/* payload.bin's `li r4, reps` (copy loop count in words) */
void patchPayloadSize(u8 *buf, int len, int size)
{
	int pat = 0xffff8038;	/* li r4, (any) */
	u8 *p;
	u32 reps = (size + 3) >> 2;

	log_printf(1, bd_45a7c4, size, reps);
	p = findInst(buf, len, (u8 *)&pat, 4);
	if (!p)
		return;
	log_printf(2, bd_45a7f8, p[2], p[3]);
	p[3] = reps;
	p[2] = reps >> 8;
	log_printf(2, bd_45a80e, p[2], p[3]);
}

/* the header bytes freeboot/xell read: UART speed, power-on reasons */
void patchHeaderOpts(void)
{
	u8 opts = 0;

	xb.hdr[0x4b] = 1;
	if (xb.bootFlags & 9) {
		log_printf(1, bd_459e3c);
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
	log_printf(1, bd_459e74);
	if (xb.xellButton == xb.xellAltButton)
		xb.xellAltButton = 0;
	xb.hdr[0x4f] = xb.xellButton;
	if (xb.xellAltButton)
		log_printf(1, bd_459e9c);
	xb.hdr[0x4e] = xb.xellAltButton;
}

int logPowerButton(int reason, const char *use)
{
	switch (reason) {
	case 0x11:
		log_printf(1, bd_45a0bc, use);
		break;
	case 0x12:
		log_printf(1, bd_45a0f0, use);
		break;
	case 0x20:
		log_printf(1, bd_45a128, use);
		break;
	case 0x22:
		log_printf(1, bd_45a15c, use);
		break;
	case 0x24:
		log_printf(1, bd_45a194, use);
		break;
	case 0x41:
		log_printf(1, bd_45a1cc, use);
		break;
	case 0x55:
		log_printf(1, bd_45a1f8, use);
		break;
	case 0x59:
		if ((xb.flags & 7) > 4)
			log_printf(1, bd_45a23c, use);
		else
			log_printf(1, bd_45a278, use);
		break;
	case 0x58:
		if ((xb.flags & 7) > 4)
			log_printf(1, bd_45a2b4, use);
		else
			log_printf(1, bd_45a278, use);
		break;
	case 0x5a:
		if ((xb.flags & 7) > 4)
			log_printf(1, bd_45a2f4, use);
		else
			log_printf(1, bd_45a334, use);
		break;
	case 0x56:
		if ((xb.flags & 7) > 4)
			log_printf(1, bd_45a36c, use);
		else
			log_printf(1, bd_45a3ac, use);
		break;
	case 0x57:
		if ((xb.flags & 7) > 4)
			log_printf(1, bd_45a3e8, use);
		else
			log_printf(1, bd_45a428, use);
		break;
	default:
		return 1;
	}
	return 0;
}

void showSmcConfig(const u8 *smc)
{
	u32 av;
	u16 game;
	int i;

	log_printf(1, bd_458f80, smc[0x29], smc[0x2a], smc[0x2b]);
	log_printf(1, bd_458fb4, smc[0x2c], smc[0x2d], smc[0x2e]);
	log_printf(1, bd_458fe6);
	if (((struct fan *)(smc + 0x11))->override)
		log_printf(1, bd_458ff5, ((struct fan *)(smc + 0x11))->speed);
	else
		log_printf(1, bd_45900a);
	log_printf(1, bd_459012, smc[0x12] & 0x7f);
	if (((struct fan *)(smc + 0x12))->override)
		log_printf(1, bd_458ff5, ((struct fan *)(smc + 0x12))->speed);
	else
		log_printf(1, bd_45900a);
	log_printf(1, bd_459021);
	showMac(1, smc + 0x220);
	av = *(u32 *)(smc + 0x228);
	av = SWAP32(av);
	switch (av) {
	case 0x100:
		log_printf(1, bd_459030, av);
		break;
	case 0x200:
		log_printf(1, bd_459050, av);
		break;
	case 0x300:
		log_printf(1, bd_459070, av);
		break;
	case 0x400:
		log_printf(1, bd_459090, av);
		break;
	default:
		log_printf(1, bd_4590b0, av);
		break;
	}
	game = __builtin_bswap16(*(u16 *)(smc + 0x22c));
	log_printf(1, bd_4590d1, game);
	switch (game) {
	case 0xff:
		log_printf(1, bd_4590e7);
		break;
	case 0x1fe:
		log_printf(1, bd_4590f2);
		break;
	case 0x1ff:
		log_printf(1, bd_4590f2);
		break;
	case 0x1fc:
		log_printf(1, bd_4590fe);
		break;
	case 0x101:
		log_printf(1, bd_45910a);
		break;
	case 0x2fe:
		log_printf(1, bd_459115);
		break;
	case 0x201:
		log_printf(1, bd_45911f);
		break;
	case 0x7fff:
		log_printf(1, bd_45912a);
		break;
	default:
		log_printf(1, bd_459134);
		break;
	}
	log_printf(1, bd_45913f, SWAP32(*(u32 *)(smc + 0x234)));
	log_printf(1, bd_459151);
	for (i = 0; i < 4; i++)
		log_printf(1, bd_459160, smc[0x238 + i]);
	log_printf(1, bd_458cf9);
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
	log_printf(1, bd_45a590, xb.kernelStr);
	log_printf(1, bd_45a5cc);
	if (opts & 9) {
		log_printf(1, bd_45a5e0);
		opts = (opts & 6) | 1;
	}
	if (opts & 4) {
		if (logPowerButton(xb.xellButton, bd_45a6a4)) {
			log_printf(1, bd_45a6b0);
			xb.xellButton = 0x12;
		}
		if (xb.xellAltButton == xb.xellButton)
			xb.xellAltButton = 0;
		if (logPowerButton(xb.xellAltButton, bd_45a6df)) {
			log_printf(1, bd_45a6f8);
			xb.xellAltButton = 0;
		}
	} else if (opts & 2)
		log_printf(1, bd_45a618);
	else
		log_printf(1, bd_45a664);
	if (xb.dualButton == xb.xellButton || xb.dualButton == xb.xellAltButton ||
	    logPowerButton(xb.dualButton, bd_45a71e))
		xb.dualButton = 0;
	p = (char *)findInst(buf, len, (u8 *)pat, 32);
	if (p) {
		log_printf(2, bd_45a728, p);
		strncpy(p, xb.kernelStr, 32);
		log_printf(2, bd_45a738, p);
	} else
		log_printf(0, bd_45a748);
	if (!strncmp(xb.kernelStr, bd_45a785, 4)) {
		hold[2] = 0x80;
		hold[3] = 0xf8ff1f00;
		log_printf(1, bd_45a78c);
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
		if (!strnicmp(e->name, bd_459955, 4) && !e->crc)
			continue;
		switch (e->type) {
		case 9:
			log_printf(1, bd_45a8af, e->name, e->size);
			j = findFile(10);
			cfEncrypt(e, xb.files[j].size, ldv, 0, imgCfSize());
			break;
		case 10:
			log_printf(1, bd_45a8af, e->name, e->size);
			j = findFile(9);
			cgEncrypt(e->data, xb.files[j].key, e->key, e->size);
			break;
		}
	}
	return 0;
}

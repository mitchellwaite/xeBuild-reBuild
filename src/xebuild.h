/* xebuild.h: types and structures shared by the app's objects.

   struct xebuild is the program's state, the global xb (defined in
   src/globals.c).  Names follow the files that use each field.  gcc's
   natural alignment gives the original's layout, so there are no padding
   members.  Where a file reads a field as another type than the one here,
   its use carries a cast marked TODO, so that the type can be settled in a
   later pass without breaking the match. */
#ifndef XEBUILD_H
#define XEBUILD_H

#include <stddef.h>
#include <stdint.h>

/* ---- Shared macros ----

   Used by more than one object.  A macro's spelling can change the code
   gcc emits, so where an object's code was matched with its own spelling
   of one, that spelling is here too, suffixed with the object's name
   (SWAP32_KEYS); either of an object's two swap spellings alone still
   changes its code. */

/* byte swaps for the console's big-endian data (gcc's bswap pass folds them) */
#define SWAP16(x) ((((x) << 8) & 0xff00) + ((x) >> 8))
#define SWAP32(x) (((x) << 24) + (((x) << 8) & 0xff0000) + (((x) >> 8) & 0xff00) + ((x) >> 24))
#define SWAP32_BUILD(x) (((x) << 24) + ((x) >> 24) + (((x) << 8) & 0xff0000) + (((x) >> 8) & 0xff00))
/* folds to a rotate (not the bswap pass's __builtin_bswap16 call), so as a
   call argument it is computed at its store */
#define SWAP16_BUILD(x) ((uint16_t)(((uint32_t)(x) << 8) | ((uint32_t)(x) >> 8)))
#define SWAP16_IMAGE_WRITE(x) ((((x) << 8) & 0xff00) + (((x) >> 8) & 0xff))
#define SWAP32_IMAGE_WRITE(x) ((((x) & 0xff) << 24) + (((x) << 8) & 0xff0000) + (((x) >> 8) & 0xff00) + ((x) >> 24))
#define SWAP32_KEYS(x) (((x) << 24) + ((x) >> 24) + (((x) << 8) & 0xff0000) + (((x) >> 8) & 0xff00))
#define SWAP16_KEYS(x) ((((x) & 0xff) << 8) + (((x) & 0xff00) >> 8))

/* ---- xb.flags and xb.type ----

   xb.flags: the console type in the low 3 bits and NAND bits at the top,
   set together from the -c name or perbox file (options.c's
   setConsoleType/iniConsoleType):
     xenon, zephyr, falcon            CONSOLE_x
     jasper, jasperbc, trinity, corona, winchester
                                      NAND_BB_CONTROLLER | CONSOLE_x
     jaspersb                         CONSOLE_JASPER
     <x>bb, jasper256, jasper512      NAND_BIG_BLOCK | CONSOLE_x
     <x>bigffs                        NAND_BIG_BLOCK | NAND_BIG_FFS | CONSOLE_x
     corona4g, winchester4g           NAND_BB_CONTROLLER | NAND_MMC | CONSOLE_x */
#define CONSOLE_MASK 7
#define CONSOLE_XENON 1
#define CONSOLE_ZEPHYR 2
#define CONSOLE_FALCON 3
#define CONSOLE_JASPER 4
#define CONSOLE_TRINITY 5		/* slims from here on */
#define CONSOLE_CORONA 6
#define CONSOLE_WINCHESTER 7
#define NAND_MMC 0x10000000		/* 48MiB eMMC (system only) */
#define NAND_BIG_FFS 0x20000000	/* extended size FFS (with NAND_BIG_BLOCK) */
#define NAND_BIG_BLOCK 0x40000000	/* 64MiB big block NAND */
#define NAND_BB_CONTROLLER 0x80000000	/* 16MiB small block NAND on a big block controller */

/* xb.type: the build type (-t, or from the dump's bootstrap in
   consoleinfo.c).  BUILD_GLITCH covers glitch, glitch2 and glitch2m
   (xb.glitch2, xb.glitch2mfg); devgl and devgl16 share an ini.  Above
   BUILD_DEVGL16 are the kit builds: devkit and testkit for a 64MiB NAND
   (small block unless NAND_BIG_BLOCK), their 16 variants for 16MiB. */
#define BUILD_RETAIL 1
#define BUILD_JTAG 2
#define BUILD_GLITCH 3
#define BUILD_DEVGL 4
#define BUILD_DEVGL16 5
#define BUILD_DEVKIT 6
#define BUILD_DEVKIT16 7
#define BUILD_TESTKIT 8
#define BUILD_TESTKIT16 9

/* a slim console (xb.flags' console type) */
#define IS_SLIM ((xb.flags & CONSOLE_MASK) > CONSOLE_JASPER)

/* in an object compiled with a profile (mode_update.c, mode_client.c), the
   functions that keep gcc's guessed profile, and .text; a file may define
   it empty before including this */
#ifndef NOPROF
#define NOPROF __attribute__((optimize("no-branch-probabilities", "no-reorder-functions")))
#endif

/* ---- Types ---- */

/* a file and its size (netGetFile's, a dump's) */
struct netfile {
	uint8_t *data;
	int size;
};

/* an input file of the image: xb.files */
struct fileent {
	char name[0x400];
	uint32_t crc;
	int type;
	uint32_t offset;
	uint8_t *data;
	uint32_t size;
	uint8_t key[16];		/* its RC4 key once encoded */
	uint32_t fsSize;		/* the part that goes in the filesystem */
	uint32_t fsOffset;		/* where that part starts */
};

/* an entry of the flash filesystem's file table */
struct fsent {
	char name[22];
	uint16_t block;
	uint32_t size;
	uint32_t time;
};

/* the flash image's header (big endian) */
struct flashhdr {
	uint16_t magic;
	uint16_t build;
	uint16_t qfe;
	uint16_t flags;
	uint32_t cbOffset;		/* entry: the CB */
	uint32_t cfOffset;
	char copyright[0x40];
	uint8_t reserved[0x10];
	uint32_t kvSize;
	uint32_t sysUpdateAddr;		/* the CF */
	uint16_t sysUpdateCount;
	uint16_t kvVersion;
	uint32_t kvAddr;
	uint32_t patchSlotSize;
	uint32_t smcConfigAddr;
	uint32_t smcBootSize;
	uint32_t smcBootAddr;
};

/* an RSA public key as the console keeps it */
struct rsapub {
	uint32_t cqw;
	uint32_t exp;
	uint64_t reserved;
	uint8_t mod[256];
};

/* what xeBuild's client (the console side) reports */
struct consoleinfo {
	uint32_t version;		/* updsvr version; low byte: hv patches */
	uint32_t kernel;
	uint32_t usvrFlags;		/* files USVR offers: 2 blmod, 4 addons */
	uint32_t bootstrap;		/* hack type in the top bits */
	uint32_t hwFlags;		/* console type in the top 4 bits; 0x20: has HDD */
	uint32_t nandSize;		/* system area */
	uint32_t blockSize;
	uint32_t pairing;		/* ldv in the low byte */
	uint8_t cpuKey[16];
	uint8_t dvdKey[16];
	uint8_t fuses[96];
	uint8_t vfuses[96];
	uint8_t key1bl[16];
	struct rsapub pub1bl;
	struct rsapub pubPirs;
	struct rsapub pubMaster;
	uint8_t keys[6][16];
};

/* console_hdd's file manifest */
struct mfFile;
struct manifest {
	struct mfFile *data;
	char path[1024];
	size_t size;
	int count;
	struct {
		void *data;
		uint32_t len;
		char path[1024];
	} e[256];
};

/* xb.files has 35 entries, 19..34 the addon patches (-a).  Two switches a
   file may define before including this change how it sees them:
   XB_FILES_BOUND declares fewer files, as the bound sets gcc's trip count
   estimate for loops over them (build.c, filelist_ini.c).  XB_PATCHES adds
   xb.patches, the addons' names as an array over xb.files in a union
   (options.c, mode_build.c, mode_update.c): mode_update's loop over it only
   compiles to the original's code that way, but the union changes alias
   analysis for every xb.files access, which build.c's code shows */
#ifndef XB_FILES_BOUND
#define XB_FILES_BOUND 35
#endif
#define XB_ADDONS 19

struct xebuild {
	int mode;
	uint32_t flags;			/* console type (& 7), NAND flags */
	uint32_t type;			/* build type */
	uint32_t kernel;
	int glitch2;
	int glitch2mfg;
	uint32_t cbb;			/* build with a CB_B */
	uint32_t seReplacesCf;		/* an SE was loaded where the CF goes */
	int randomKeys;			/* keysInit's argument (random nonces) */
	int sysTime;			/* use the system time for timestamps */
	uint32_t muBlocks;		/* end of the MU area (big block) */
	uint8_t spare9;			/* spare bytes of system blocks */
	uint8_t spare8;
	uint8_t spare7;
	uint8_t *spare;			/* 16 spare bytes per 512-byte page */
	uint32_t spareSize;
	uint8_t *hdr;			/* the flash image (user data) */
	uint32_t userSize;
	uint8_t *raw;			/* data and spare interleaved */
	uint32_t blocks;		/* 16K blocks */
	uint32_t rawSize;
	uint32_t smcConfigOffset;
	int bigBlock;
	int bbController;		/* big block controller, small block NAND */
	uint32_t fsEnd;			/* FS area, in 16K blocks */
	uint32_t fsStart;
	uint32_t bootFlags;		/* options turned on */
	uint32_t bootFlagsOff;		/* options turned off */
	int xellButton;
	/* uint32_t (unlike xellButton): options.c's applyIniOptions' tests of them
	   don't get reused for parseButton's 0 */
	uint32_t xellAltButton;
	uint32_t dualButton;
	uint8_t cbLdv;
	uint8_t cfLdv;
	uint32_t cpuTemp;		/* smc_config overrides from the ini */
	uint32_t gpuTemp;
	uint32_t edramTemp;
	uint32_t overCpuTemp;
	uint32_t overGpuTemp;
	uint32_t overEdramTemp;
	uint32_t cpuFan;
	uint32_t gpuFan;
	uint32_t avRegion;
	uint32_t gameRegion;
	uint32_t dvdRegion;
	uint8_t macid[6];
	uint8_t *dump;			/* the nand dump's user data, ECC stripped */
	uint8_t *dumpSpare;		/* its spare data, 16 bytes a page */
	uint32_t dumpSize;
	uint32_t dumpSpareSize;
	uint32_t dumpPages;
	int dumpBigBlock;
	int dumpBbController;
	int dumpMmc;
	int nandMu;
	int muChecked;
	uint32_t numBad;		/* bad blocks of the dump */
	uint32_t badBlocks[32];
	uint32_t badRemap[32];
	struct netfile consoleBlmod;	/* blmod.bin from the console */
	struct netfile bl;		/* the bootloaders (raw, glitch) */
	int fromConsole;		/* bootloaders read from the console */
	struct netfile mobile[11];	/* MobileB-J, Statistics, Manufacturing */
	struct netfile smc;		/* files from the nand dump */
	struct netfile kv;
	struct netfile kvAlt;
	struct netfile smcConfig;
	struct netfile netKd;
	uint8_t key1bl[16];
	uint8_t cpuKey[16];
	uint8_t xexKey[16];		/* calcXexKey's (CRL/DAE key) */
	struct rsapub *pub1bl;
	struct rsapub *masterPub;
	struct rsapub *pubPirs;
	void *prvKey;			/* the ini's 2BL private key (SB) */
	char suffix[0x400];		/* -i */
	char binDir[0x400];
	char outName[0x400];
	char baseDir[0x400];		/* -d */
	char dataDir[0x400];		/* -f */
	char commonDir[0x400];
	char firmware[256][0x400];	/* the ini's firmware files */
	uint32_t firmwareCrc[256];
	uint32_t nFirmware;
#ifdef XB_PATCHES
	union {
		struct fileent files[XB_FILES_BOUND];
		struct {
			uint8_t padPatches[XB_ADDONS * sizeof(struct fileent)];
			char patches[16][sizeof(struct fileent)];	/* the addons' names */
		};
	};
#else
	struct fileent files[XB_FILES_BOUND];
	uint8_t padFiles[(35 - XB_FILES_BOUND) * sizeof(struct fileent)];
#endif
	char blSuffix[0x40];		/* -r */
	int numPatches;			/* addons (files[XB_ADDONS...]) */
	int nFiles;
	int nFlashFiles;
	struct {
		char name[0x400];
		uint32_t offset;
	} rawPatch[16];
	uint32_t nRawPatches;
	char flashFiles[10][22];	/* security files */
	uint8_t *flashBuf[10];		/* their data from a dump */
	uint32_t flashSize[10];
	uint32_t flashTime[10];
	uint32_t flashCrc[10];
	uint32_t nFlashFiles2;		/* the security file count */
	union {
		uint32_t mmcAnchor[0x80];	/* MMC anchor block */
		struct {
			uint8_t anchor[0x1b];
			uint8_t anchorNum;
			uint16_t fsBlock;	/* writeFsTable's block (big endian) */
			uint16_t fsReserved;	/* written as 0 */
			struct {
				uint16_t type, size;
			} mobileTab[9];
		};
	};
	char kernelStr[0x40];		/* the ini's kernel version string */
	uint8_t *iniBuf;		/* the ini file */
	char sha1File[0x400];
	int sha1Write;
	int iniSize;
};

/* ---- Globals (src/globals.c) ---- */
extern int *blOrder;			/* filelist_ini: one of the bl* tables */
extern struct xebuild xb;
extern struct fsent fsFiles[256];	/* image_write */
extern uint16_t fsTable[0x1000];
extern struct flashhdr hdrTemplate;
extern uint32_t imgEnd;
extern struct manifest manifest;	/* console_hdd */

#endif

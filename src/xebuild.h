/* xebuild.h: types and structures shared by the app's objects.

   struct xebuild is the program's state, the global xb (defined in
   src/globals.c).  Names follow the files that use each field; offsets are
   in the comments.  Where a file reads a field as another type than the one
   here, its use carries a cast marked TODO, so that the type can be settled
   in a later pass without breaking the match. */
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
	uint32_t crc;			/* 400 */
	int type;			/* 404 */
	uint32_t offset;		/* 408 */
	uint8_t *data;			/* 40c */
	uint32_t size;			/* 410 */
	uint8_t key[16];		/* 414 its RC4 key once encoded */
	uint32_t fsSize;		/* 424 the part that goes in the filesystem */
	uint32_t fsOffset;		/* 428 where that part starts */
};

/* an entry of the flash filesystem's file table */
struct fsent {
	char name[22];
	uint16_t block;			/* 16 */
	uint32_t size;			/* 18 */
	uint32_t time;			/* 1c */
};

/* the flash image's header (big endian) */
struct flashhdr {
	uint16_t magic;			/* 00 */
	uint16_t build;			/* 02 */
	uint16_t qfe;			/* 04 */
	uint16_t flags;			/* 06 */
	uint32_t cbOffset;		/* 08 entry: the CB */
	uint32_t cfOffset;		/* 0c */
	char copyright[0x40];		/* 10 */
	uint8_t reserved[0x10];		/* 50 */
	uint32_t kvSize;		/* 60 */
	uint32_t sysUpdateAddr;		/* 64 the CF */
	uint16_t sysUpdateCount;	/* 68 */
	uint16_t kvVersion;		/* 6a */
	uint32_t kvAddr;		/* 6c */
	uint32_t patchSlotSize;		/* 70 */
	uint32_t smcConfigAddr;		/* 74 */
	uint32_t smcBootSize;		/* 78 */
	uint32_t smcBootAddr;		/* 7c */
};

/* an RSA public key as the console keeps it */
struct rsapub {
	uint32_t cqw;
	uint32_t exp;
	uint64_t reserved;		/* 08 */
	uint8_t mod[256];		/* 10 */
};

/* what xeBuild's client (the console side) reports */
struct consoleinfo {
	uint32_t version;		/* 000 updsvr version; low byte: hv patches */
	uint32_t kernel;		/* 004 */
	uint32_t f008;			/* 008 2: has blmod, 4: has addons */
	uint32_t bootstrap;		/* 00c hack type in the top bits */
	uint32_t hwFlags;		/* 010 console type in the top 4 bits; 0x20: has HDD */
	uint32_t nandSize;		/* 014 system area */
	uint32_t blockSize;		/* 018 */
	uint32_t pairing;		/* 01c ldv in the low byte */
	uint8_t cpuKey[16];		/* 020 */
	uint8_t dvdKey[16];		/* 030 */
	uint8_t fuses[96];		/* 040 */
	uint8_t vfuses[96];		/* 0a0 */
	uint8_t key1bl[16];		/* 100 */
	struct rsapub pub1bl;		/* 110 */
	struct rsapub pubPirs;		/* 220 */
	struct rsapub pubMaster;	/* 330 */
	uint8_t keys[6][16];		/* 440 */
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
	int mode;			/* 000 */
	uint32_t flags;			/* 004 console type (& 7), NAND flags */
	uint32_t type;			/* 008 build type */
	uint32_t kernel;		/* 00c */
	int glitch2;			/* 010 */
	int glitch2mfg;			/* 014 */
	uint32_t cbb;			/* 018 build with a CB_B */
	uint32_t f01c;			/* 01c set when an SE replaces the CF */
	int randomKeys;			/* 020 keysInit's argument (random nonces) */
	int sysTime;			/* 024 use the system time for timestamps */
	uint32_t muBlocks;		/* 028 end of the MU area (big block) */
	uint8_t spare9;			/* 02c spare bytes of system blocks */
	uint8_t spare8;			/* 02d */
	uint8_t spare7;			/* 02e */
	uint8_t pad02f;
	uint8_t *spare;			/* 030 16 spare bytes per 512-byte page */
	uint32_t spareSize;		/* 034 */
	uint8_t *hdr;			/* 038 the flash image (user data) */
	uint32_t userSize;		/* 03c */
	uint8_t *raw;			/* 040 data and spare interleaved */
	uint32_t blocks;		/* 044 16K blocks */
	uint32_t rawSize;		/* 048 */
	uint32_t smcConfigOffset;	/* 04c */
	int bigBlock;			/* 050 */
	int bbController;		/* 054 big block controller, small block NAND */
	uint32_t fsEnd;			/* 058 FS area, in 16K blocks */
	uint32_t fsStart;		/* 05c */
	uint32_t bootFlags;		/* 060 options turned on */
	uint32_t bootFlagsOff;		/* 064 options turned off */
	int xellButton;			/* 068 */
	/* uint32_t (unlike xellButton): options.c's applyIniOptions' tests of them
	   don't get reused for parseButton's 0 */
	uint32_t xellAltButton;		/* 06c */
	uint32_t dualButton;		/* 070 */
	uint8_t cbLdv;			/* 074 */
	uint8_t cfLdv;			/* 075 */
	uint8_t pad076[2];
	uint32_t cpuTemp;		/* 078 smc_config overrides from the ini */
	uint32_t gpuTemp;		/* 07c */
	uint32_t edramTemp;		/* 080 */
	uint32_t overCpuTemp;		/* 084 */
	uint32_t overGpuTemp;		/* 088 */
	uint32_t overEdramTemp;		/* 08c */
	uint32_t cpuFan;		/* 090 */
	uint32_t gpuFan;		/* 094 */
	uint32_t avRegion;		/* 098 */
	uint32_t gameRegion;		/* 09c */
	uint32_t dvdRegion;		/* 0a0 */
	uint8_t macid[6];		/* 0a4 */
	uint8_t pad0aa[2];
	uint8_t *dump;			/* 0ac the nand dump's user data, ECC stripped */
	uint8_t *dumpSpare;		/* 0b0 its spare data, 16 bytes a page */
	uint32_t dumpSize;		/* 0b4 */
	uint32_t dumpSpareSize;		/* 0b8 */
	uint32_t dumpPages;		/* 0bc */
	int dumpBigBlock;		/* 0c0 */
	int dumpBbController;		/* 0c4 */
	int dumpMmc;			/* 0c8 */
	int nandMu;			/* 0cc */
	int muChecked;			/* 0d0 */
	uint32_t numBad;		/* 0d4 bad blocks of the dump */
	uint32_t badBlocks[32];		/* 0d8 */
	uint32_t badRemap[32];		/* 158 */
	struct netfile consoleBlmod;	/* 1d8 blmod.bin from the console */
	struct netfile bl;		/* 1e0 the bootloaders (raw, glitch) */
	int fromConsole;		/* 1e8 bootloaders read from the console */
	struct netfile mobile[11];	/* 1ec MobileB-J, Statistics, Manufacturing */
	struct netfile smc;		/* 244 files from the nand dump */
	struct netfile kv;		/* 24c */
	struct netfile kvAlt;		/* 254 */
	struct netfile smcConfig;	/* 25c */
	struct netfile netKd;		/* 264 */
	uint8_t key1bl[16];		/* 26c */
	uint8_t cpuKey[16];		/* 27c */
	uint8_t key28c[16];		/* 28c */
	void *pub1bl;			/* 29c */
	void *masterPub;		/* 2a0 */
	void *pubPirs;			/* 2a4 */
	void *prvKey;			/* 2a8 the ini's 2BL private key (SB) */
	char suffix[0x400];		/* 2ac -i */
	char binDir[0x400];		/* 6ac */
	char outName[0x400];		/* aac */
	char baseDir[0x400];		/* eac -d */
	char dataDir[0x400];		/* 12ac -f */
	char commonDir[0x400];		/* 16ac */
	char firmware[256][0x400];	/* 1aac the ini's firmware files */
	uint32_t firmwareCrc[256];	/* 41aac */
	uint32_t nFirmware;		/* 41eac */
#ifdef XB_PATCHES
	union {
		struct fileent files[XB_FILES_BOUND];	/* 41eb0 */
		struct {
			uint8_t pad41eb0[XB_ADDONS * sizeof(struct fileent)];
			char patches[16][sizeof(struct fileent)];	/* 46df4 the addons' names */
		};
	};
#else
	struct fileent files[XB_FILES_BOUND];	/* 41eb0 */
	uint8_t padFiles[(35 - XB_FILES_BOUND) * sizeof(struct fileent)];
#endif
	char blSuffix[0x40];		/* 4b0b4 -r */
	int numPatches;			/* 4b0f4 addons (files[XB_ADDONS...]) */
	int nFiles;			/* 4b0f8 */
	int nFlashFiles;		/* 4b0fc */
	struct {
		char name[0x400];
		uint32_t offset;
	} rawPatch[16];			/* 4b100 */
	uint32_t nRawPatches;		/* 4f140 */
	char flashFiles[10][22];	/* 4f144 security files */
	uint8_t *flashBuf[10];		/* 4f220 their data from a dump */
	uint32_t flashSize[10];		/* 4f248 */
	uint32_t flashTime[10];		/* 4f270 */
	uint32_t flashCrc[10];		/* 4f298 */
	uint32_t nFlashFiles2;		/* 4f2c0 the security file count */
	union {
		uint32_t mmcAnchor[0x80];	/* 4f2c4 MMC anchor block */
		struct {
			uint8_t anchor[0x1b];	/* 4f2c4 */
			uint8_t anchorNum;	/* 4f2df */
			uint8_t pad4f2e0[4];
			struct {
				uint16_t type, size;
			} mobileTab[9];		/* 4f2e4 */
		};
	};
	char kernelStr[0x40];		/* 4f4c4 the ini's kernel version string */
	uint8_t *iniBuf;		/* 4f504 the ini file */
	char sha1File[0x400];		/* 4f508 */
	int sha1Write;			/* 4f908 */
	int iniSize;			/* 4f90c */
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

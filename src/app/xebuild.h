/* xebuild.h: types and structures shared by the app's objects.

   struct xebuild is the program's state, the global xb (defined in
   src/globals.c).  Names follow the files that use each field; offsets are
   in the comments.  Where a file reads a field as another type than the one
   here, its use carries a cast marked TODO, so that the type can be settled
   in a later pass without breaking the match. */
#ifndef XEBUILD_H
#define XEBUILD_H

#include <stddef.h>

typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef unsigned long long u64;

/* a file and its size (netGetFile's, a dump's) */
struct netfile {
	u8 *data;
	int size;
};

/* an input file of the image: xb.files */
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

/* an entry of the flash filesystem's file table */
struct fsent {
	char name[22];
	u16 block;			/* 16 */
	u32 size;			/* 18 */
	u32 time;			/* 1c */
};

/* the flash image's header (big endian) */
struct flashhdr {
	u16 magic;			/* 00 */
	u16 build;			/* 02 */
	u16 qfe;			/* 04 */
	u16 flags;			/* 06 */
	u32 cbOffset;			/* 08 entry: the CB */
	u32 cfOffset;			/* 0c */
	char copyright[0x40];		/* 10 */
	u8 reserved[0x10];		/* 50 */
	u32 kvSize;			/* 60 */
	u32 sysUpdateAddr;		/* 64 the CF */
	union {
		u32 patchSlots;		/* 68 both halves at once */
		struct {
			u16 sysUpdateCount;	/* 68 */
			u16 kvVersion;		/* 6a */
		};
	};
	u32 kvAddr;			/* 6c */
	u32 patchSlotSize;		/* 70 */
	u32 smcConfigAddr;		/* 74 */
	u32 smcBootSize;		/* 78 */
	u32 smcBootAddr;		/* 7c */
};

/* an RSA public key as the console keeps it */
struct rsapub {
	u32 cqw;
	u32 exp;
	u64 reserved;			/* 08 */
	u8 mod[256];			/* 10 */
};

/* what xeBuild's client (the console side) reports */
struct consoleinfo {
	u32 version;			/* 000 updsvr version; low byte: hv patches */
	u32 kernel;			/* 004 */
	u32 f008;			/* 008 2: has blmod, 4: has addons */
	u32 bootstrap;			/* 00c hack type in the top bits */
	u32 hwFlags;			/* 010 console type in the top 4 bits; 0x20: has HDD */
	u32 nandSize;			/* 014 system area */
	u32 blockSize;			/* 018 */
	u32 pairing;			/* 01c ldv in the low byte */
	u8 cpuKey[16];			/* 020 */
	u8 dvdKey[16];			/* 030 */
	u8 fuses[96];			/* 040 */
	u8 vfuses[96];			/* 0a0 */
	u8 key1bl[16];			/* 100 */
	union {
		u8 pub1bl[272];		/* 110 */
		struct rsapub pub1blKey;
	};
	u8 pubPirs[272];		/* 220 */
	u8 pubMaster[272];		/* 330 */
	u8 keys[6][16];			/* 440 */
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
		u32 len;
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
	u32 flags;			/* 004 console type (& 7), NAND flags */
	u32 type;			/* 008 build type */
	u32 kernel;			/* 00c */
	int glitch2;			/* 010 */
	int glitch2mfg;			/* 014 */
	u32 cbb;			/* 018 build with a CB_B */
	u32 f01c;			/* 01c set when an SE replaces the CF */
	int randomKeys;			/* 020 keysInit's argument (random nonces) */
	int sysTime;			/* 024 use the system time for timestamps */
	u32 muBlocks;			/* 028 end of the MU area (big block) */
	u8 spare9;			/* 02c spare bytes of system blocks */
	u8 spare8;			/* 02d */
	u8 spare7;			/* 02e */
	u8 pad02f;
	u8 *spare;			/* 030 16 spare bytes per 512-byte page */
	u32 spareSize;			/* 034 */
	u8 *hdr;			/* 038 the flash image (user data) */
	u32 userSize;			/* 03c */
	u8 *raw;			/* 040 data and spare interleaved */
	u32 blocks;			/* 044 16K blocks */
	u32 rawSize;			/* 048 */
	u32 smcConfigOffset;		/* 04c */
	int bigBlock;			/* 050 */
	int bbController;		/* 054 big block controller, small block NAND */
	u32 fsEnd;			/* 058 FS area, in 16K blocks */
	u32 fsStart;			/* 05c */
	u32 bootFlags;			/* 060 options turned on */
	u32 bootFlagsOff;		/* 064 options turned off */
	int xellButton;			/* 068 */
	/* u32 (unlike xellButton): options.c's applyIniOptions' tests of them
	   don't get reused for parseButton's 0 */
	u32 xellAltButton;		/* 06c */
	u32 dualButton;			/* 070 */
	u8 cbLdv;			/* 074 */
	u8 cfLdv;			/* 075 */
	u8 pad076[2];
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
	u8 pad0aa[2];
	u8 *dump;			/* 0ac the nand dump's user data, ECC stripped */
	u8 *dumpSpare;			/* 0b0 its spare data, 16 bytes a page */
	u32 dumpSize;			/* 0b4 */
	u32 dumpSpareSize;		/* 0b8 */
	u32 dumpPages;			/* 0bc */
	int dumpBigBlock;		/* 0c0 */
	int dumpBbController;		/* 0c4 */
	int dumpMmc;			/* 0c8 */
	int nandMu;			/* 0cc */
	int muChecked;			/* 0d0 */
	u32 numBad;			/* 0d4 bad blocks of the dump */
	u32 badBlocks[32];		/* 0d8 */
	u32 badRemap[32];		/* 158 */
	struct netfile consoleBlmod;	/* 1d8 blmod.bin from the console */
	struct netfile bl;		/* 1e0 the bootloaders (raw, glitch) */
	int fromConsole;		/* 1e8 bootloaders read from the console */
	struct netfile mobile[11];	/* 1ec MobileB-J, Statistics, Manufacturing */
	struct netfile smc;		/* 244 files from the nand dump */
	struct netfile kv;		/* 24c */
	struct netfile kvAlt;		/* 254 */
	struct netfile smcConfig;	/* 25c */
	struct netfile netKd;		/* 264 */
	u8 key1bl[16];			/* 26c */
	u8 cpuKey[16];			/* 27c */
	u8 key28c[16];			/* 28c */
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
	u32 firmwareCrc[256];		/* 41aac */
	u32 nFirmware;			/* 41eac */
#ifdef XB_PATCHES
	union {
		struct fileent files[XB_FILES_BOUND];	/* 41eb0 */
		struct {
			u8 pad41eb0[XB_ADDONS * sizeof(struct fileent)];
			char patches[16][sizeof(struct fileent)];	/* 46df4 the addons' names */
		};
	};
#else
	struct fileent files[XB_FILES_BOUND];	/* 41eb0 */
	u8 padFiles[(35 - XB_FILES_BOUND) * sizeof(struct fileent)];
#endif
	char blSuffix[0x40];		/* 4b0b4 -r */
	int numPatches;			/* 4b0f4 addons (files[XB_ADDONS...]) */
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
	u32 flashTime[10];		/* 4f270 */
	u32 flashCrc[10];		/* 4f298 */
	u32 nFlashFiles2;		/* 4f2c0 the security file count */
	union {
		u32 mmcAnchor[0x80];	/* 4f2c4 MMC anchor block */
		struct {
			u8 anchor[0x1b];	/* 4f2c4 */
			u8 anchorNum;		/* 4f2df */
			u8 pad4f2e0[4];
			struct {
				u16 type, size;
			} mobileTab[9];		/* 4f2e4 */
		};
	};
	char kernelStr[0x40];		/* 4f4c4 the ini's kernel version string */
	u8 *iniBuf;			/* 4f504 the ini file */
	char sha1File[0x400];		/* 4f508 */
	int sha1Write;			/* 4f908 */
	int iniSize;			/* 4f90c */
};

extern struct xebuild xb;

#endif

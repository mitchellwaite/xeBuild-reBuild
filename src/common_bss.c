/* common_bss: the COMMON block, the uninitialized globals at the end of .bss.

   The original objects declared these without initializers, so gcc made them
   COMMON symbols and ld laid them out after every object's .bss, in the order
   of its symbol hash table (which depends on names we don't know), aligning
   the big ones to 32 bytes.  This file defines them in that address order
   instead.  build.sh compiles it with -fno-common (real definitions, which
   net.c's netStartTime and xecrypt.c's XeCryptRandomState, still tentative,
   resolve to), -fno-toplevel-reorder (definition order) and -fno-ident (the
   original link had no such object, so no `GCC:` ident).  Every variable is
   aligned(4) like the block, and the pad arrays stand for ld's alignment
   padding.  The other files declare struct xebuild with just the fields they
   use; this one names the fields they share. */
#include <time.h>
#include "crypto/rc4/rc4.h"

typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;

#define A4 __attribute__((aligned(4)))
/* static, but in place: gcc would emit a plain static as .lcomm, which gas
   puts after all of .bss */
#define PAD __attribute__((used, section(".bss")))

struct xebuild {
	int mode;			/* 000 */
	u32 flags;			/* 004 console type (& 7), NAND flags */
	u32 type;			/* 008 build type */
	u32 kernel;			/* 00c */
	u8 pad010[0x038 - 0x010];
	u8 *hdr;			/* 038 the flash image */
	u32 userSize;			/* 03c its user (non-spare) size */
	u8 pad040[0x0ac - 0x040];
	u8 *dump;			/* 0ac the nand dump's data */
	u8 pad0b0[0x1e0 - 0x0b0];
	u8 *bl;				/* 1e0 the bootloaders */
	u8 pad1e4[0x26c - 0x1e4];
	u8 key1bl[16];			/* 26c */
	u8 cpuKey[16];			/* 27c */
	u8 key28c[16];			/* 28c */
	void *pub1bl;			/* 29c */
	void *masterPub;		/* 2a0 */
	void *pub2a4;			/* 2a4 */
	u8 *prvKey;			/* 2a8 the ini's 2BL private key */
	u8 pad2ac[0x6ac - 0x2ac];
	char binDir[0x800];		/* 6ac */
	char baseDir[0x400];		/* eac */
	char dataDir[0x400];		/* 12ac */
	char commonDir[0x400];		/* 16ac */
	char firmware[256][0x400];	/* 1aac the ini's firmware files */
	u32 firmwareCrc[256];		/* 41aac */
	u32 nFirmware;			/* 41eac */
	u8 files[35][0x42c];		/* 41eb0 struct fileent */
	u8 pad4b0b4[0x4f144 - 0x4b0b4];
	char flashFiles[10][22];	/* 4f144 security files */
	void *flashBuf[10];		/* 4f220 */
	u32 flashSize[10];		/* 4f248 */
	u8 pad4f270[0x4f2c0 - 0x4f270];
	u32 nFlashFiles2;		/* 4f2c0 the security file count */
	u32 mmcAnchor[0x80];		/* 4f2c4 MMC anchor block */
	u8 pad4f4c4[0x4f504 - 0x4f4c4];
	char *iniBuf;			/* 4f504 the ini file */
	char sha1File[0x400];		/* 4f508 */
	int sha1Write;			/* 4f908 */
	int iniSize;			/* 4f90c */
};
_Static_assert(sizeof(struct xebuild) == 0x4f910, "struct xebuild");

/* an entry of the flash file system's file table */
struct fsent {
	char name[22];
	u16 block;			/* 16 */
	u32 size;			/* 18 */
	u32 time;			/* 1c */
};

/* the flash image header */
struct flashhdr {
	u16 magic;			/* 00 */
	u16 build;			/* 02 */
	u16 qfe;			/* 04 */
	u16 flags;			/* 06 */
	u32 cbOffset;			/* 08 */
	u32 cfOffset;			/* 0c */
	char copyright[0x40];		/* 10 */
	u8 reserved[0x10];		/* 50 */
	u32 kvLength;			/* 60 */
	u32 cfOffset2;			/* 64 */
	u32 patchSlots;			/* 68 */
	u32 kvOffset;			/* 6c */
	u32 patchSlotSize;		/* 70 */
	u32 smcConfigOffset;		/* 74 */
	u32 smcLength;			/* 78 */
	u32 smcOffset;			/* 7c */
};

/* console_hdd's file manifest */
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

typedef void (*_PVFV)(void);

int *blOrder A4;			/* 479e84 filelist_ini: one of the bl* tables */
static char pad479e88[24] PAD;
struct xebuild xb A4;			/* 479ea0 */
static char pad4c97b0[16] PAD;
struct fsent fsFiles[256] A4;		/* 4c97c0 image_write */
u16 fsTable[0x1000] A4;			/* 4cb7c0 */
struct flashhdr hdrTemplate A4;		/* 4cd7c0 */
u32 imgEnd A4;				/* 4cd840 */
time_t netStartTime A4;			/* 4cd844 net */
static char pad4cd848[24] PAD;
char unused4cd860[0x400] A4;		/* 4cd860 nothing references it */
struct manifest manifest A4;		/* 4cdc60 console_hdd */
static char pad50e86c[20] PAD;
RC4_KEY XeCryptRandomState A4;		/* 50e880 crypto/xecrypt */
/* mingw-w64's crt (atonexit.c, natstart.c) */
_PVFV *__onexitend A4;			/* 50ec88 */
_PVFV *__onexitbegin A4;		/* 50ec8c */
volatile void *__native_startup_lock A4;	/* 50ec90 */
volatile unsigned int __native_startup_state A4;	/* 50ec94 */
char unused50ec98[16] A4;		/* 50ec98 nothing references it */

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
#include <time.h>

#include "crypto/xecrypt.h"

/* ---- Windows CRT names on other platforms ----

   The code calls the Windows (msvcrt/mingw) names; elsewhere they map to
   POSIX.  The system headers come first, so the macros can't rename their
   prototypes.  Large files: fseeko/ftello take a 64-bit off_t on 32-bit
   Linux only with _FILE_OFFSET_BITS=64, which the Makefile sets. */
#ifndef _WIN32
#include <stdio.h>
#include <strings.h>
#include <sys/stat.h>
#include <sys/types.h>
#define stricmp strcasecmp
#define strnicmp strncasecmp
#define mkdir(path) mkdir((path), 0777)
#define fseeko64 fseeko
#define ftello64 ftello
#endif

/* The app's code spells many 32-bit values int and unsigned int (and some
   short): renaming them int32_t etc. changes gcc 6's code for the matching
   build even where the typedef is the same type, so they stay as spelled.
   Every supported target (win32, and the 64-bit LLP64 and LP64 ones) has a
   32-bit int and a 16-bit short; fail the build on one that doesn't.  long
   is 64-bit on LP64 (linux, macos); the code uses it only for status
   returns, ftell sizes and date arithmetic, where the wider type is
   harmless. */
_Static_assert(sizeof(int) == 4, "xeBuild needs a 32-bit int");
_Static_assert(sizeof(short) == 2, "xeBuild needs a 16-bit short");

/* ---- Shared macros ----

   Used by more than one object.  A macro's spelling can change the code
   gcc emits, so where an object's code was matched with its own spelling
   of one, that spelling is here too, suffixed with the object's name
   (SWAP32_KEYS); either of an object's two swap spellings alone still
   changes its code. */

/* byte swaps for the console's big-endian data.  Spelled with +, they stay
   open-coded shifts and masks as in the original (gcc's bswap pass doesn't
   fold them); __builtin_bswap16/32 in place of any of these changes its
   objects' code (a bswap or rol instruction, and the code around it
   shifts), so they stay macros. */
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

/* system area sizes the console reports (consoleinfo.nandSize) */
#define NAND_SIZE_MMC 0x3000000		/* 48MiB eMMC, no spare data */
#define NAND_SIZE_BIG_BLOCK 0x4200000	/* 64MiB big block NAND with its spare data */

/* ---- NAND geometry ----

   A page is NAND_PAGE bytes of data and NAND_SPARE spare bytes (LBA, block
   type, ECD), which a raw image interleaves.  A small block NAND's block is
   0x20 pages, a big block one's 0x100; xb.blocks and the FS count 16K
   (small) blocks either way.  The eMMC has no spare data. */
#define NAND_PAGE 0x200
#define NAND_PAGE_SHIFT 9
#define NAND_SPARE 0x10
#define NAND_RAW_PAGE 0x210
#define NAND_BLOCK 0x4000
#define NAND_BLOCK_SHIFT 14
#define NAND_BLOCK_MASK 0x3fff
#define NAND_BLOCK_PAGES 0x20
#define NAND_RAW_BLOCK 0x4200
#define NAND_BB_BLOCK 0x20000		/* a big block */
#define NAND_BB_SHIFT 17
#define NAND_BB_MASK 0x1ffff
#define NAND_BB_PAGES 0x100
#define NAND_RAW_BB_BLOCK 0x21000

/* image sizes: user data, and raw (data and spare); NAND_SIZE_MMC */
#define NAND_SIZE_16M 0x1000000
#define NAND_SIZE_64M 0x4000000
#define NAND_RAW_16M 0x1080000
#define NAND_RAW_64M 0x4200000

/* where the SMC config is, per layout (image_write.c's buildImage,
   image_read.c's findSmcConfig) */
#define SMCCFG_OFFSET_16M 0xf7c000
#define SMCCFG_OFFSET_64M 0x3dfc000	/* small block (kits) */
#define SMCCFG_OFFSET_BB 0x3be0000	/* big block */
#define SMCCFG_OFFSET_MMC 0x2ffc000

/* the eMMC's two anchor blocks (xb.mmcAnchor; image_write.c's
   copyAnchorBlock, image_read.c's anchor checks) */
#define MMC_ANCHOR0 0x2fe8000
#define MMC_ANCHOR1 0x2fec000

/* ---- The flash filesystem ----

   fsChain (the FS table's block chain, big endian) entries other than a
   next block, and imgAdd's next argument: one of these, a block for every
   block it writes, IMG_CHAIN (chain the blocks, the last FS_CHAIN_END) or
   IMG_NO_CHAIN (big block's system area: no FS table entry). */
#define FS_CHAIN_RESERVED 0x1ffb	/* the bootloaders, the SMC config */
#define FS_CHAIN_ROOT 0x1ffd		/* the FS table's block (small block) */
#define FS_CHAIN_FREE 0x1ffe		/* also Mobile*.dat, big block's FS table */
#define FS_CHAIN_END 0x1fff
#define IMG_CHAIN 0xffff
#define IMG_NO_CHAIN 0xf1f1

/* the block type in a page's spare (image_write.c's struct spt, image_read.c's
   fsBlockType) for imgAdd's type: Mobile*.dat are '1' (MobileB) to '9'
   (MobileJ) */
#define SPARE_FILE_BB 0x2a		/* an FS file's block (big block) */
#define SPARE_FS_ROOT_BB 0x2c		/* the FS table (big block) */
#define SPARE_FS_ROOT '0'		/* the FS table (small block) */
#define SPARE_MOBILE_B '1'
#define SPARE_MOBILE_J '9'

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

/* ---- xb.optFlags and xb.optFlagsOff ----

   xb.optFlags: the build options turned on (-o, perbox files, options.ini);
   xb.optFlagsOff: the ones the command line turned off (name=false).
   optIniBool skips an ini or perbox option whose bit is set in either.
   The low nibble is freeboot's boot options word (patchFreeboot) and its
   low 3 bits the flash header's byte 0x4d (patchHeaderOpts,
   getFlashHdrOpts), which stores demon as cygnos.  Bits 1-2 are the tray
   mode xell starts on: OPT_XELL_BUTTON (the default), OPT_NODVD (tray
   fully open) or neither (olddvd: tray not closed). */
#define OPT_CYGNOS 0x00000001		/* cygnos: slow (cygnos/demon) debug UART speed */
#define OPT_NODVD 0x00000002		/* nodvd: xell starts if the tray is fully open */
#define OPT_XELL_BUTTON 0x00000004	/* default: xell starts on a power-on button
					   (xellbutton=); nodvd and olddvd clear it */
#define OPT_DEMON 0x00000008		/* demon: slow UART speed */
#define OPT_SMCNOCHECK 0x00200000	/* smcnocheck: carry on after SMC check errors */
#define OPT_SMCNOEJECT 0x00400000	/* smcnoeject: patch out the SMC's eject button */
#define OPT_SMCNOBLINK 0x00800000	/* smcnoblink: patch out the ROL centre blink */
#define OPT_NOSUSECURITY 0x01000000	/* nosusecurity: no flash files from the system update */
#define OPT_DVDKEY 0x02000000		/* not an option: a dvdkey= was set in the KV */
#define OPT_NOSECURITY 0x04000000	/* nosecurity: don't read the image's security files */
#define OPT_PATCHSMC 0x08000000		/* patchsmc: patch the SMC reset limit (glitch) */
#define OPT_NANDMU 0x10000000		/* nandmu: keep the NAND memory unit data from the dump */
#define OPT_NOMOBILE 0x20000000		/* nomobile: don't read the dump's Mobile* files or the KD */
#define OPT_NOREMAP 0x40000000		/* noremap: discard the dump's bad block remap data */
#define OPT_NOECDREMAP 0x80000000	/* noecdremap: don't remap blocks that fail the ECC check */

#define OPT_UART_SLOW (OPT_CYGNOS | OPT_DEMON)
#define OPT_HDR_MASK (OPT_CYGNOS | OPT_NODVD | OPT_XELL_BUTTON)
#define OPT_FREEBOOT_MASK (OPT_HDR_MASK | OPT_DEMON)
#define OPT_SMC_PATCHES (OPT_PATCHSMC | OPT_SMCNOEJECT | OPT_SMCNOBLINK)

/* ---- Power-on reasons ----

   The SMC's power-on reason codes: xb.xellButton, xb.xellAltButton and
   xb.dualButton, and the xellbutton/xellbutton2/dualboot ini names
   (options.c), shown by logButton and optButton.  The wired controller
   ports are named for a slim; on a fat only PWR_WIRED_B3 (rear) and the
   front two exist. */
#define PWR_POWER 0x11			/* power: console power button */
#define PWR_EJECT 0x12			/* eject: console DVD eject button */
#define PWR_IR_POWER 0x20		/* remopower: IR power button */
#define PWR_IR_GUIDE 0x22		/* remox: IR guide/X button */
#define PWR_IR_WINDOWS 0x24		/* winbutton: IR windows button */
#define PWR_KIOSK 0x41			/* kiosk: KIOSK debug pin */
#define PWR_WIRELESS 0x55		/* wirelessx: wireless controller */
#define PWR_WIRED_F1 0x56		/* wiredxf1: front left (fat: front top) */
#define PWR_WIRED_F2 0x57		/* wiredxf2: front right (fat: front bottom) */
#define PWR_WIRED_B2 0x58		/* wiredxb2: rear middle (slim only) */
#define PWR_WIRED_B1 0x59		/* wiredxb1: rear top (slim only) */
#define PWR_WIRED_B3 0x5a		/* wiredxb3: rear bottom (fat: rear) */

/* ---- Flash header option bytes ----

   Bytes in the tail of the flash header's copyright field that freeboot and
   xell read (build.c's patchHeaderOpts writes them, consoleinfo.c's
   getFlashHdrOpts reads them back from a console). */
#define HDR_BLMOD_SIZE 0x49		/* big endian 16 bits: the blmod.bin bytes
					   build.c's patchBlsBlmod added (glitch) */
#define HDR_OPTS_VALID 0x4b		/* 1: the bytes below are set */
#define HDR_DUAL_BUTTON 0x4c		/* dualboot power-on reason (JTAG) */
#define HDR_OPTS 0x4d			/* OPT_HDR_MASK bits */
#define HDR_XELL_ALT_BUTTON 0x4e	/* xellbutton2 power-on reason */
#define HDR_XELL_BUTTON 0x4f		/* xellbutton power-on reason */

/* ---- Key checksums ----

   sumBytes of a good key: what xeBuild checks keys from the console or
   files against. */
#define KEY1BL_SUM 0x983
#define XEXKEY_SUM 0x800		/* keys.c's calcXexKey, from the 1BL key */
#define PUB1BL_SUM 0x79c7
#define PUBPIRS_SUM 0x80d0
#define PUBMASTER_SUM 0x843c
#define PRVKEY_SUM 0x1ca16		/* SB_priv.bin, the SC/SD private key */

/* ---- SMC config ----

   The SMC's config block (smc_config.bin; build.c's showSmcConfig and
   patchSmcConfig).  Its first two bytes are a big endian checksum of the
   bytes from SMCCFG_SUM_START to SMCCFG_SUM_END (fileutil.c's
   calcConfigSum).  A fan byte is its speed in percent, with FAN_OVERRIDE
   set (build.c's struct fan); FAN_AUTO leaves it to the SMC. */
#define SMCCFG_SIZE 0x400
#define SMCCFG_SUM_START 0x10
#define SMCCFG_SUM_END 0x10c
#define SMCCFG_CPU_FAN 0x11
#define SMCCFG_GPU_FAN 0x12
#define SMCCFG_CPU_TEMP 0x29		/* target temperatures, degrees C */
#define SMCCFG_GPU_TEMP 0x2a
#define SMCCFG_EDRAM_TEMP 0x2b
#define SMCCFG_OVER_CPU_TEMP 0x2c	/* maximum temperatures */
#define SMCCFG_OVER_GPU_TEMP 0x2d
#define SMCCFG_OVER_EDRAM_TEMP 0x2e
#define SMCCFG_MAC 0x220		/* 6 bytes */
#define SMCCFG_AV_REGION 0x228		/* big endian 32 bits */
#define SMCCFG_GAME_REGION 0x22c	/* big endian 16 bits */
#define SMCCFG_DVD_REGION 0x234		/* big endian 32 bits */
#define SMCCFG_RESET_KEY 0x238		/* 4 characters */
#define FAN_OVERRIDE 0x80
#define FAN_AUTO 0x7f

/* ---- File ids ----

   xb.files[].type, findFile's ids: filelist_ini.c's tables give each build
   type's files their ids and flash offsets.  The bootloaders come in four
   sets: the retail CB-CG, the kits' SB-SE with their own CF and CG, and
   for JTAG the exploit's own CB-CG, which boot the target's CB, CD, CF and
   CG (the retail ids). */
#define FILE_NONE 0			/* "none": the flash header's slot */
#define FILE_PAYLOAD 1			/* payload.bin (JTAG) */
#define FILE_SMC 2			/* smc.bin */
#define FILE_KV 3			/* kv.bin */
#define FILE_KV_ALT 4			/* kv_alt.bin (testkit) */
#define FILE_CB 5			/* the retail bootloaders: CB (CB_A) */
#define FILE_CB_B 6
#define FILE_CD 7
#define FILE_CE 8
#define FILE_CF 9
#define FILE_CG 10
#define FILE_SB 11			/* the kits' bootloaders */
#define FILE_SC 12
#define FILE_SD 13
#define FILE_SE 14			/* also a retail SE in place of the CF */
#define FILE_KIT_CF 15
#define FILE_KIT_CG 16
#define FILE_JTAG_CB 17			/* the JTAG exploit's bootloaders */
#define FILE_JTAG_CD 18
#define FILE_JTAG_CE 19
#define FILE_JTAG_CF 20
#define FILE_JTAG_CG 21
#define FILE_FREEBOOT 22		/* freeboot.bin (USVR's freeboot_bin) */
#define FILE_PATCHES 23			/* patches_<type>.bin */
#define FILE_FUSES 24			/* fuses.bin: virtual fuses */
#define FILE_XELL 25			/* xell-2f.bin, xell-gggggg.bin */
#define FILE_SCRATCH 26			/* "none": xb.files[xb.nFlashFiles], where
					   files are loaded before they're moved */
#define FILE_SMC_CONFIG 27		/* smc_config.bin */

/* a file's offset (xb.files[].offset) right after the file before it */
#define FILE_FOLLOWS 0xffffffff

/* virtual fuses (FILE_FUSES, consoleinfo.fuses): 12 lines of 8 bytes */
#define FUSES_SIZE 0x60

/* the patches (FILE_PATCHES) are sections of {address, word count, words},
   each ended by PATCHES_END */
#define PATCHES_END 0xffffffff

/* xb.mobile: MobileB-J.dat, then these two */
#define MOBILE_STATISTICS 9		/* Statistics.settings */
#define MOBILE_MANUFACTURING 10		/* Manufacturing.data */

/* ---- xb.mode ----

   The command line's mode (main.c). */
#define MODE_BUILD 1
#define MODE_UPDATE 2
#define MODE_CLIENT 3
#define MODE_INI 4
#define MODE_EXTRACT 5

/* ---- Types ---- */

/* a file and its size (netGetFile's, a dump's) */
struct netfile
{
	uint8_t *data;
	int size;
};

/* an input file of the image: xb.files */
struct fileent
{
	char name[0x400];
	uint32_t crc;
	int type;
	uint32_t offset;
	uint8_t *data;
	uint32_t size;
	uint8_t key[0x10];		/* its RC4 key once encoded */
	uint32_t fsSize;		/* the part that goes in the filesystem */
	uint32_t fsOffset;		/* where that part starts */
};

/* an entry of the flash filesystem's file table; a name is at most
   FS_NAME_SIZE - 1 characters */
#define FS_NAME_SIZE 0x16
struct fsent
{
	char name[FS_NAME_SIZE];
	uint16_t block;
	uint32_t size;
	uint32_t time;
};

/* the flash image's header (big endian), and the values xeBuild writes
   (image_write.c's buildImage) and checks a dump's against (image_read.c) */
#define FLASH_MAGIC 0xff4f
#define FLASH_BUILD 1888
#define FLASH_KV_VERSION 0x712
#define FLASH_SU_COUNT 2		/* sysUpdateCount */
#define FLASH_CB_OFFSET 0x8000
#define FLASH_CB_OFFSET_TESTKIT 0xc000	/* after its two KVs */
#define FLASH_KV_ADDR 0x4000		/* the SMC ends here */
#define FLASH_SMC_ADDR 0x1000
#define FLASH_PATCH_SLOT 0x10000	/* patchSlotSize, the default */
#define FLASH_PATCH_SLOT_BB 0x20000	/* big block */
#define FLASH_JTAG_CF 0x70000		/* JTAG: cfOffset, sysUpdateAddr */
#define FLASH_NETKD 0x80		/* a dump's network KD follows the header */
#define NETKD_MAGIC 0xca4a

struct flashhdr
{
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

/* the SMC's sizes: SMC_SIZE_CORONA (Corona, Winchester) is at
   FLASH_SMC_ADDR_CORONA; both end at FLASH_KV_ADDR */
#define SMC_SIZE 0x3000
#define SMC_SIZE_CORONA 0x3800
#define FLASH_SMC_ADDR_CORONA 0x800

/* ---- Bootloaders ----

   Each starts with image_write.c's struct blhdr (big endian): a magic of two
   letters, the first 'C' or (the kits') 'S', which BL_MAGIC_MASK makes 'C';
   then the RC4 key's nonce, and the encrypted body (a CF has another 0x10
   bytes of header before its nonce). */
#define BL_MAGIC_MASK 0x43ff
#define BL_MAGIC_KIT 0x1000		/* 'S' */
#define BL_MAGIC_CB 0x4342		/* "CB" */
#define BL_MAGIC_CC 0x4343		/* "CC": the kits' SC */
#define BL_MAGIC_CD 0x4344
#define BL_MAGIC_CE 0x4345
#define BL_MAGIC_CF 0x4346
#define BL_MAGIC_CG 0x4347
#define BL_FLAG_CB_B 0x800		/* a CB's flags: a CB_B follows it */
#define BL_SIZE_OFFSET 0xc		/* the header's size field */
#define BL_NONCE 0x10
#define BL_BODY 0x20			/* what the RC4 encrypts */
#define BL_CF_NONCE 0x20
#define BL_CF_BODY 0x30

/* in a decrypted CB (or SB): the pairing data (3 bytes) and the LDV after
   them; the console type and lock down sequences fileutil.c's
   showExpectedFuses reads (big endian: the fuse type, FUSE_TYPE_x, in the
   top byte, the CB's sequence below it, then the sequences it allows) */
#define CB_PAIRING 0x20
#define CB_LDV 0x23
#define CB_FUSE_FLAGS 0x3b0

/* in an SB: the public key the SC and SD are signed with, and their
   signatures' salts; in an SD, the SE's hash */
#define SB_PUBKEY 0x268			/* XECRYPT_RSAPUB_2048 */
#define SB_SC_SALT 0x388
#define SB_SD_SALT 0x392
#define SD_SE_HASH 0x24c

/* in a decrypted CF: the pairing data and LDV (as CB_PAIRING) and the CG's
   HMAC key */
#define CF_PAIRING 0x21c
#define CF_LDV 0x21f
#define CF_CG_KEY 0x330

/* the highest CF lock down value (cfldv) */
#define CF_LDV_MAX 32

/* ---- Keyvault ----

   A decrypted keyvault: 0x10 bytes of HMAC (keyed with the CPU key) of the
   rest, which also make its RC4 key; then 8 bytes of salt (keys.c's kvSalt)
   and the fields.  A type 2 one is signed with the master key over the
   bytes from KV_ODD_FEATURES on, but for the key at 0xf0 and the signature
   itself (xboxrom.c's kvVerifySig). */
#define KV_SIZE 0x4000
#define KV_SALT 0x10			/* 8 bytes */
#define KV_ODD_FEATURES 0x1c		/* big endian 16 bits */
#define KV_CONSOLE_SERIAL 0xb0		/* 12 characters */
#define KV_MOBO_SERIAL 0xc0		/* the 8 bytes main.c shows as MoboSerial */
#define KV_DVD_KEY 0x100		/* 0x10 bytes */
#define KV_CONSOLE_ID 0x9ca		/* the certificate's console id, 5 bytes */
#define KV_MFG_DATE 0x9e4		/* the certificate's "MM-DD-YY" */
#define KV_SIGNATURE 0x1df8		/* 0x100 bytes */

/* the security files' sizes */
#define FCRT_SIZE 0x4000
#define EXTENDED_SIZE 0x4000		/* extended.bin */
#define SECDATA_SIZE 0x400

/* consoleinfo.version: updsvr version above the low byte, the hv patches'
   version in it */
#define USVR_MIN_VERSION 3		/* updsvr version xeBuild needs */
#define PATCHES_UPDATE_VERSION 2	/* hv patches version update mode needs */

/* consoleinfo.bootstrap: the console type (CONSOLE_x - 1) in the low
   nibble, the hack type in the top bits */
#define BOOTSTRAP_CONSOLE_MASK 0xf
#define BOOTSTRAP_JTAG 0x80000000	/* tested as bootstrap < 0 */
#define BOOTSTRAP_GLITCH 0x40000000
#define BOOTSTRAP_GLITCH2 0x20000000
#define BOOTSTRAP_GLITCH2M 0x10000000

/* consoleinfo.hwFlags: the console type (CONSOLE_x - 1) in the top 4 bits */
#define HW_CONSOLE_SHIFT 28
#define HW_HDD 0x20			/* internal HDD present */

/* consoleinfo.usvrFlags: the files USVR offers */
#define USVR_BLMOD 2
#define USVR_ADDONS 4

/* what xeBuild's client (the console side) reports */
struct consoleinfo
{
	uint32_t version;		/* updsvr version; low byte: hv patches */
	uint32_t kernel;
	uint32_t usvrFlags;		/* files USVR offers: USVR_x */
	uint32_t bootstrap;		/* hack type in the top bits */
	uint32_t hwFlags;		/* console type in the top 4 bits; 0x20: has HDD */
	uint32_t nandSize;		/* system area */
	uint32_t blockSize;
	uint32_t pairing;		/* ldv in the low byte */
	uint8_t cpuKey[0x10];
	uint8_t dvdKey[0x10];
	uint8_t fuses[FUSES_SIZE];
	uint8_t vfuses[FUSES_SIZE];
	uint8_t key1bl[0x10];
	XECRYPT_RSAPUB_2048 pub1bl;
	XECRYPT_RSAPUB_2048 pubPirs;
	XECRYPT_RSAPUB_2048 pubMaster;
	uint8_t cbaNonce[0x10];		/* the bootloaders' nonces */
	uint8_t cbbNonce[0x10];
	uint8_t cdNonce[0x10];
	uint8_t ceNonce[0x10];
	uint8_t cfNonce[0x10];
	uint8_t cgNonce[0x10];
};

/* smc_config overrides from the ini; a field the ini didn't set is
   SMC_OPT_UNSET (macid's bytes 0xff) */
#define SMC_OPT_UNSET 0xffffffff
struct smcopts
{
	uint32_t cpuTemp;
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
	uint8_t macid[0x6];
};

/* console_hdd's file manifest */
struct mfFile;
struct manifest
{
	struct mfFile *data;
	char path[0x400];
	size_t size;
	int count;
	struct
	{
		void *data;
		uint32_t len;
		char path[0x400];
	} e[0x100];
};

/* xb.files has 19 entries; the 16 addon patches (-a) follow it in xb.addons.
   The bound sets gcc's trip count estimate for loops over the files (build.c's
   only match with 19 to 21). */
#define XB_ADDONS 19

/* the lists the ini and command line fill: [flashfs] firmware files, the
   addon patches (-a, the ini's), [rawpatch] files and [security] files */
#define XB_FIRMWARE 0x100
#define XB_ADDON_PATCHES 0x10
#define XB_RAWPATCHES 0x10
#define XB_SECURITY 10

struct xebuild
{
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
	uint32_t optFlags;		/* options turned on (OPT_x) */
	uint32_t optFlagsOff;		/* options turned off */
	int xellButton;
	/* uint32_t (unlike xellButton): options.c's applyIniOptions' tests of them
	   don't get reused for parseButton's 0 */
	uint32_t xellAltButton;
	uint32_t dualButton;
	uint8_t cbLdv;
	uint8_t cfLdv;
	struct smcopts smcOpts;		/* all -1 (unset) until the ini sets them */
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
	uint32_t badBlocks[0x20];
	uint32_t badRemap[0x20];
	struct netfile consoleBlmod;	/* blmod.bin from the console */
	struct netfile bl;		/* the bootloaders (raw, glitch) */
	int fromConsole;		/* bootloaders read from the console */
	struct netfile mobile[11];	/* MobileB-J, Statistics, Manufacturing */
	struct netfile smc;		/* files from the nand dump */
	struct netfile kv;
	struct netfile kvAlt;
	struct netfile smcConfig;
	struct netfile netKd;
	uint8_t key1bl[0x10];
	uint8_t cpuKey[0x10];
	uint8_t xexKey[0x10];		/* calcXexKey's (CRL/DAE key) */
	XECRYPT_RSAPUB_2048 *pub1bl;	/* loaded, or the console's */
	XECRYPT_RSAPUB_2048 *masterPub;
	XECRYPT_RSAPUB_2048 *pubPirs;
	XECRYPT_RSAPRV_2048 *prvKey;	/* the ini's 2BL private key (SB) */
	char suffix[0x400];		/* -i */
	char binDir[0x400];
	char outName[0x400];
	char baseDir[0x400];		/* -d */
	char dataDir[0x400];		/* -f */
	char commonDir[0x400];
	char firmware[XB_FIRMWARE][0x400];	/* the ini's firmware files */
	uint32_t firmwareCrc[XB_FIRMWARE];
	uint32_t nFirmware;
	struct fileent files[XB_ADDONS];
	struct fileent addons[XB_ADDON_PATCHES];
	char blSuffix[0x40];		/* -r */
	int numPatches;			/* entries used in addons */
	int nFiles;
	int nFlashFiles;
	struct
	{
		char name[0x400];
		uint32_t offset;
	} rawPatch[XB_RAWPATCHES];
	uint32_t nRawPatches;
	char flashFiles[XB_SECURITY][FS_NAME_SIZE];	/* security files */
	uint8_t *flashBuf[XB_SECURITY];	/* their data from a dump */
	uint32_t flashSize[XB_SECURITY];
	uint32_t flashTime[XB_SECURITY];
	uint32_t flashCrc[XB_SECURITY];
	uint32_t nFlashFiles2;		/* the security file count */
	union
	{
		uint32_t mmcAnchor[0x80];	/* MMC anchor block */
		struct
		{
			uint8_t anchor[0x1b];
			uint8_t anchorNum;
			uint16_t fsBlock;	/* writeFsTable's block (big endian) */
			uint16_t fsReserved;	/* written as 0 */
			struct
			{
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
extern struct fsent fsFileEnts[0x100];	/* image_write */
extern uint16_t fsChain[0x1000];
extern struct flashhdr flashHdr;
extern uint32_t imgUsed;
extern struct manifest consoleManifest;	/* console_hdd */
extern time_t netTimeStart;		/* net */

#endif

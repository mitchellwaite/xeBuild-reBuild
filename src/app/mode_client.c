/* mode_client: `xeBuild client`, single commands against a console over the network */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* build.sh compiles this file twice: plainly (every function but
   mode_client), and with -DBUILD_FDO and a crafted profile
   (src/app/mode_client.prof) for mode_client and the clientEraseBlock it
   inlines; mode_client comes from that compile (re/splice.py --whole).
   Under BUILD_FDO the other functions keep the guessed profile (NOPROF),
   and mode_client's blocks get labels (AT) reached by empty asm gotos
   (JUMP): dead edges whose only effect is bb-reorder's priority keys and
   the frequencies of the blocks they enter (wip/mc/s18/NOTES.md); the
   empty asm in NO_MODE_ARG splits the test the same way.  Without
   BUILD_FDO they expand to the plain source. */
#ifdef BUILD_FDO
#define NOPROF __attribute__((optimize("no-branch-probabilities", "no-reorder-functions")))
#define AT(l) l:
#define JUMP(...) __asm__ goto ("" :::: __VA_ARGS__)
#define NO_MODE_ARG(m, a) (!(m) || ({ __asm__(""); 0; }) || !(a))
#else
#define NOPROF
#define AT(l)
#define JUMP(...)
#define NO_MODE_ARG(m, a) (!((m) && (a)))
#endif

#include "xebuild.h"
#include "console_hdd.h"
#include "consoleinfo.h"
#include "fileutil.h"
#include "image_write.h"
#include "log.h"
#include "main.h"
#include "mode_client.h"
#include "net.h"

/* TODO(prototype cast): net.c takes u16 block numbers; mode_client's calls
   compile to the original's code only with u32 ones */
int netEraseBlockU32(u32 block, int force) __asm__("_netEraseBlock");
u8 *netReadBlocksU32(int *len, u32 start, u32 count) __asm__("_netReadBlocks");
int netWriteBlocksU32(u8 *buf, int len, u32 start, u32 count) __asm__("_netWriteBlocks");

void client_usage(int err, const char *arg) __attribute__((noreturn));
int dumpKey(const char *name, const char *file, const u8 *key, size_t len, u32 sum);
int checkPatches(u8 *buf, size_t *len, u32 type);
void updatePatches(const char *file, u32 type);
void patchNand(u8 *buf, int off, const u8 *data, int len);

/* the original object's .bss is 32 bytes, cinfo at its start */
static struct consoleinfo *cinfo __attribute__((aligned(32)));
static char mc_bsspad[28] __attribute__((used));

static const char mc_44e10c[] __attribute__((aligned(4))) = "\n\n***** ERROR: option flag %s on command line but no argument provided!\n";
static const char mc_44e158[] __attribute__((aligned(4))) = "\n\n***** ERROR: option flag %s on command line not enough arguments provided!\n";
static const char mc_44e1a8[] __attribute__((aligned(4))) = "\n\n***** ERROR: option flag %s on command line but option was already set!\n";
static const char mc_44e1f4[] __attribute__((aligned(4))) = "\n\n***** ERROR: unknown option '%s' provided on command line!\n";
static const char mc_44e234[] __attribute__((aligned(4))) = "\n\n***** ERROR: not enough info provided to carry out command!\n";
static const char mc_44e273[] __attribute__((aligned(1))) = "xeBuild";
static const char mc_44e27c[] __attribute__((aligned(4))) = "Usage   :\n   %s client <switch> [<option>]\n\n";
static const char mc_44e2a9[] __attribute__((aligned(1))) = "Examples:\n";
static const char mc_44e2b4[] __attribute__((aligned(1))) = "   %s client -r nanddump.bin\n";
static const char mc_44e2d4[] __attribute__((aligned(4))) = "   %s client -w nandflash.bin -ip 192.168.2.100\n";
static const char mc_44e305[] __attribute__((aligned(1))) = "\nSwitches:\n";
static const char mc_44e314[] __attribute__((aligned(4))) = "   -i             : connects to console and shows some info about it\n";
static const char mc_44e35c[] __attribute__((aligned(4))) = "*  -i <d>         : collects console information into folder <d>, usually enough for build mode\n";
static const char mc_44e3c0[] __attribute__((aligned(4))) = "   -r <f>         : dumps system area of NAND to <f>\n";
static const char mc_44e3f8[] __attribute__((aligned(4))) = "   -w <f>         : writes system area of NAND from <f>\n";
static const char mc_44e434[] __attribute__((aligned(4))) = "   -e <d>         : format partition and send avatar/kinect data to HDD from <d>, must match running kernel\n";
static const char mc_44e4a4[] __attribute__((aligned(4))) = "   -c <d>         : format partition and send xbox compatibility data to HDD from <d>\n";
static const char mc_44e4fc[] __attribute__((aligned(4))) = "   -p             : will attempt to automatically update patches based on running kernel version\n";
static const char mc_44e560[] __attribute__((aligned(4))) = "   -p <f>         : update patches with <f>\n";
static const char mc_44e590[] __attribute__((aligned(4))) = "   -rb <f> <b> <l>: read series of blocks starting at <b> for <l>\n";
static const char mc_44e5d4[] __attribute__((aligned(4))) = "   -wb <f> <b>    : write series of blocks starting at <b> for the number of blocks in <f>\n";
static const char mc_44e630[] __attribute__((aligned(4))) = "   -eb <b>        : attempt to erase a single block, even if marked bad on console\n";
static const char mc_44e684[] __attribute__((aligned(4))) = "   -bp <f> <o>    : binary patch NAND with contents of <f> to logical offset <o>\n";
static const char mc_44e6d8[] __attribute__((aligned(4))) = "*  -keys          : will attempt to dump RSA and 1BL keys from console\n";
static const char mc_44e720[] __attribute__((aligned(4))) = "   -s             : shutdown console\n";
static const char mc_44e748[] __attribute__((aligned(4))) = "   -ip <add>      : force attempt to connect to addr (ie: -i 192.168.0.100)\n";
static const char mc_44e798[] __attribute__((aligned(4))) = "   -noenter       : suppresses prompt for enter key when finished\n";
static const char mc_44e7dc[] __attribute__((aligned(4))) = "   -reboot        : causes the console to hard reboot\n";
static const char mc_44e814[] __attribute__((aligned(4))) = "   -v             : shows more info during client process\n";
static const char mc_44e850[] __attribute__((aligned(4))) = "   -?             : shows this help\n\n";
static const char mc_44e876[] __attribute__((aligned(1))) = "legend:\n";
static const char mc_44e880[] __attribute__((aligned(4))) = "<add>    = without this option network will be scanned for server broadcast beacon\n";
static const char mc_44e8d4[] __attribute__((aligned(4))) = "           If provided the correct format is an IPv4 address like 192.168.0.100\n";
static const char mc_44e928[] __attribute__((aligned(4))) = "<f>      = path, absolute or relative, to a file\n";
static const char mc_44e95c[] __attribute__((aligned(4))) = "<d>      = path, absolute or relative, to a directory - do not terminate with /\n";
static const char mc_44e9b0[] __attribute__((aligned(4))) = "<b>      = hexadecimal block number\n";
static const char mc_44e9d8[] __attribute__((aligned(4))) = "<l>      = hexadecimal number of blocks\n";
static const char mc_44ea04[] __attribute__((aligned(4))) = "<o>      = hexadecimal logical offset (spare data not considered) in flash\n";
static const char mc_44ea50[] __attribute__((aligned(1))) = "notes:\n";
static const char mc_44ea58[] __attribute__((aligned(4))) = "* functions not fully supported with older patch versions, use with caution.\n";
static const char mc_44eaa8[] __attribute__((aligned(4))) = "- client mode tends to operate on a single command basis, stacking commands.\n";
static const char mc_44eaf8[] __attribute__((aligned(4))) = "  is not possible with the exception of v, noenter, ip, s and reboot.\n";
static const char mc_44eb40[] __attribute__((aligned(4))) = "- patch update (-p) will retain any addon patches already on the console.\n";
static const char mc_44eb8b[] __attribute__((aligned(1))) = "\npress <enter> to quit...\n";
NOPROF
void client_usage(int err, const char *arg)
{
	switch (err) {
	case 3:
		log_printf(0, mc_44e10c, arg);
		break;
	case 4:
		log_printf(0, mc_44e158, arg);
		break;
	case 5:
		log_printf(0, mc_44e1a8, arg);
		break;
	case 1:
		log_printf(0, mc_44e1f4, arg);
		break;
	case 2:
		log_printf(0, mc_44e234);
		break;
	}
	log_printf(0, separator);
	log_printf(0, mc_44e27c, mc_44e273);
	log_printf(0, mc_44e2a9);
	log_printf(0, mc_44e2b4, mc_44e273);
	log_printf(0, mc_44e2d4, mc_44e273);
	log_printf(0, mc_44e305);
	log_printf(0, mc_44e314);
	log_printf(0, mc_44e35c);
	log_printf(0, mc_44e3c0);
	log_printf(0, mc_44e3f8);
	log_printf(0, mc_44e434);
	log_printf(0, mc_44e4a4);
	log_printf(0, mc_44e4fc);
	log_printf(0, mc_44e560);
	log_printf(0, mc_44e590);
	log_printf(0, mc_44e5d4);
	log_printf(0, mc_44e630);
	log_printf(0, mc_44e684);
	log_printf(0, mc_44e6d8);
	log_printf(0, mc_44e720);
	log_printf(0, mc_44e748);
	log_printf(0, mc_44e798);
	log_printf(0, mc_44e7dc);
	log_printf(0, mc_44e814);
	log_printf(0, mc_44e850);
	log_printf(0, mc_44e876);
	log_printf(0, mc_44e880);
	log_printf(0, mc_44e8d4);
	log_printf(0, mc_44e928);
	log_printf(0, mc_44e95c);
	log_printf(0, mc_44e9b0);
	log_printf(0, mc_44e9d8);
	log_printf(0, mc_44ea04);
	log_printf(0, mc_44ea50);
	log_printf(0, mc_44ea58);
	log_printf(0, mc_44eaa8);
	log_printf(0, mc_44eaf8);
	log_printf(0, mc_44eb40);
	log_printf(0, separator);
	log_finish();
	if (promptEnter) {
		log_printf(0, mc_44eb8b);
		fgetc(stdin);
	}
	exit(1);
}

static const char mc_44ebc0[] __attribute__((aligned(4))) = "creating mydata folder output at %s\n";
static const char mc_44ebe8[] __attribute__((aligned(4))) = "unable to dump details to %s, disabling\n";
static const char mc_44ec11[] __attribute__((aligned(1))) = "0x%x";
static const char mc_44ec16[] __attribute__((aligned(1))) = ",";
static const char mc_44ec18[] __attribute__((aligned(1))) = "dumping console flash to %s\n";
static const char mc_44ec35[] __attribute__((aligned(1))) = "success!\n";
static const char mc_44ec3f[] __attribute__((aligned(1))) = "failed!\n";
static const char mc_44ec48[] __attribute__((aligned(1))) = "Bad Block list  : ";
/* -i [<d>]: console info, bad blocks; with <d> also the info files and a NAND dump */
NOPROF
void clientInfo(const char *dir)
{
	char path[1024];
	const char *out = NULL;
	int len;
	u8 *bad;
	int i;

	if (dir) {
		log_printf(0, mc_44ebc0, dir);
		if (createDir(dir))
			out = dir;
		else
			log_printf(0, mc_44ebe8, dir);
	}
	parseConsoleInfo(0, out, out, NULL);
	bad = netGetBadBlocks(&len);
	if (bad && len) {
		log_printf(0, mc_44ec48);
		for (i = len - 2; i >= 0; i -= 2) {
			log_printf(0, mc_44ec11, getBeU16(bad + i));
			if (i)
				log_printf(0, mc_44ec16);
		}
	}
	if (out) {
		strcpy(path, dir);
		strcat(path, "/nanddump.bin");
		log_printf(0, mc_44ec18, path);
		if (!netDumpNand(path))
			log_printf(0, mc_44ec3f);
		else
			log_printf(0, mc_44ec35);
	}
}

static const char mc_44ec5b[] __attribute__((aligned(1))) = "reading file %s...";
static const char mc_44ec6e[] __attribute__((aligned(1))) = "success, read 0x%x bytes\n";
static const char mc_44ec88[] __attribute__((aligned(1))) = "sending data to console...\n";
static const char mc_44eca4[] __attribute__((aligned(4))) = "\n\n***** ERROR: file size should be 0x%x but its 0x%x bytes! Aborted!\n";
static const char mc_44ecec[] __attribute__((aligned(4))) = "\n\n***** ERROR: image magic should be 0xFF4F but its 0x%x! Aborted!\n";
static const char mc_44ed30[] __attribute__((aligned(4))) = "\n\n***** ERROR: unable to read file to send\n";
/* -w <f> */
NOPROF
int clientWrite(const char *file)
{
	size_t len;
	u8 *buf;
	int ret = 0;

	netTimerStart();
	log_printf(0, mc_44ec5b, file);
	buf = FileToBuffer(file, &len);
	if (buf) {
		log_printf(0, mc_44ec6e, len);
		if (getBeU16(buf) == 0xff4f) {
			if (cinfo->nandSize == len) {
				log_printf(0, mc_44ec88);
				ret = netSendFlash(buf, len);
			} else
				log_printf(0, mc_44eca4, cinfo->nandSize, len);
		} else
			log_printf(0, mc_44ecec, getBeU16(buf));
		free(buf);
	} else
		log_printf(0, mc_44ed30);
	return ret;
}

static const char mc_44ed5c[] __attribute__((aligned(1))) = "manifest, %08x %08x %s\n";
static const char mc_44ed74[] __attribute__((aligned(1))) = "item %03d: %08x %08x %s\n";
NOPROF
void clientManifest(const char *dir)
{
	int i;

	if (!loadManifest(dir, cinfo->kernel & ~0xf))
		return;
	for (i = 0; i < manifest.count; i++)
		log_printf(1, mc_44ed74, i + 1, manifest.e[i].len, manifest.e[i].data, manifest.e[i].path);
	log_printf(1, mc_44ed5c, manifest.size, manifest.size, manifest.path);
	freeManifest();
}

static const char mc_44ed8d[] __attribute__((aligned(1))) = "checking %s (file ./%s)\n";
static const char mc_44eda8[] __attribute__((aligned(4))) = "\n\n****** ERROR: unable to dump %s to file ./%s, key is not valid or file is inaccessible!\n";
static const char mc_44ee04[] __attribute__((aligned(4))) = "dumping valid %s to file ./%s\n";
static const char mc_44ee23[] __attribute__((aligned(1))) = "./";
NOPROF
int dumpKey(const char *name, const char *file, const u8 *key, size_t len, u32 sum)
{
	u32 want = sum;
	int ret = 0;

	log_printf(0, mc_44ed8d, name, file);
	if (FileExists(file))
		FileToBuffer(file, &len);
	if (sumBytes(key, len) == want) {
		log_printf(0, mc_44ee04, name, file);
		if (len == 16)
			ret = writeKeyFile(mc_44ee23, file, key);
		else
			ret = writeFileIn(mc_44ee23, file, key, len);
	}
	if (!ret)
		log_printf(0, mc_44eda8, name, file);
	return ret;
}

static const char mc_44ee26[] __attribute__((aligned(1))) = "1blkey.txt";
static const char mc_44ee31[] __attribute__((aligned(1))) = "1BL key";
static const char mc_44ee39[] __attribute__((aligned(1))) = "1BL_pub.bin";
static const char mc_44ee45[] __attribute__((aligned(1))) = "1BL RSA pub key";
static const char mc_44ee55[] __attribute__((aligned(1))) = "PIRS_pub.bin";
static const char mc_44ee62[] __attribute__((aligned(1))) = "PIRS RSA pub key";
static const char mc_44ee73[] __attribute__((aligned(1))) = "MAST_pub.bin";
static const char mc_44ee80[] __attribute__((aligned(1))) = "MASTER RSA pub key";
static const char mc_44ee94[] __attribute__((aligned(4))) = "\n\n****** ERROR: console patches need to be updated to support this operation!\n";
/* -keys */
NOPROF
void clientKeys(void)
{
	if ((u8)cinfo->version > 1) {
		dumpKey(mc_44ee31, mc_44ee26, cinfo->key1bl, 16, 2435);
		dumpKey(mc_44ee45, mc_44ee39, cinfo->pub1bl, 272, 31175);
		dumpKey(mc_44ee62, mc_44ee55, cinfo->pubPirs, 272, 32976);
		dumpKey(mc_44ee80, mc_44ee73, cinfo->pubMaster, 272, 33852);
	} else
		log_printf(0, mc_44ee94);
}

static const char mc_44eee4[] __attribute__((aligned(4))) = "checking patch sections for glitch console\n";
static const char mc_44ef10[] __attribute__((aligned(4))) = "\n\n***** ERROR: patches do not contain all segments, aborting!\n";
static const char mc_44ef50[] __attribute__((aligned(4))) = "checking patch sections for JTAG console\n";
static const char mc_44ef7c[] __attribute__((aligned(4))) = "\n\n***** ERROR: patches do not contain all segments, counted %d - aborting!\n";
/* patches are sections separated by 0xffffffff: JTAG has 4, glitch 3 and
   loses the first (glitch2 keeps 16 bytes of 0xff in its place) */
NOPROF
int checkPatches(u8 *buf, size_t *len, u32 type)
{
	u32 marker = 0xffffffff;
	u8 *p;
	size_t n, i, off;

	if (type > 1) {
		log_printf(0, mc_44eee4);
		if (countInst(buf, *len, &marker, 4) == 3) {
			p = findInst(buf, *len, &marker, 4);
			if (p) {
				p = findInst(p + 4, *len - (p - buf), &marker, 4);
				if (p) {
					p += 4;
					n = *len - (p - buf);
					off = 0;
					if (type == 2)
						off = 16;
					for (i = 0; i < n; i++)
						buf[off + i] = p[i];
					if (off)
						memset(buf, 0xff, off);
					*len = n + off;
					return 1;
				}
			}
		} else
			log_printf(0, mc_44ef10);
		return 0;
	}
	n = countInst(buf, *len, &marker, 4);
	log_printf(0, mc_44ef50);
	if (n == 4)
		return 1;
	log_printf(0, mc_44ef7c, n);
	return 0;
}

static const char mc_44efc8[] __attribute__((aligned(4))) = "loaded %s size 0x%x (%d) bytes\n";
static const char mc_44efe8[] __attribute__((aligned(4))) = "retrieving patches from console...";
static const char mc_44f00b[] __attribute__((aligned(1))) = "patches";
static const char mc_44f014[] __attribute__((aligned(4))) = "success! received 0x%x (%d) bytes\n";
static const char mc_44f037[] __attribute__((aligned(1))) = "patches updated OK!\n";
static const char mc_44f04c[] __attribute__((aligned(4))) = "\n\n***** ERROR: patch update failed!\n";
static const char mc_44f074[] __attribute__((aligned(4))) = "\n\n***** ERROR: failed to retrieve current patches from console!\n";
static const char mc_44f0b8[] __attribute__((aligned(4))) = "\n\n***** ERROR: %s exists but is 0 len, aborting\n";
static const char mc_44f0ec[] __attribute__((aligned(4))) = "\n\n***** ERROR: could not load %s, aborting\n";
static const char mc_44f118[] __attribute__((aligned(4))) = "sending update patches to console...";
static const char mc_44f140[] __attribute__((aligned(4))) = "patches are already up to date!\n";
NOPROF
void updatePatches(const char *file, u32 type)
{
	size_t len, cur;
	u8 *buf, *patches;
	int same;

	buf = FileToBuffer(file, &len);
	if (buf) {
		if (len) {
			log_printf(0, mc_44efc8, file, len, len);
			if (checkPatches(buf, &len, type)) {
				log_printf(0, mc_44efe8);
				patches = netGetFile(mc_44f00b, &cur);
				if (patches) {
					log_printf(1, mc_44f014, cur, cur);
					same = 0;
					if (len == cur && !memcmp(buf, patches, len))
						same = 1;
					if (!same) {
						log_printf(0, mc_44f118);
						if (netWritePatches(buf, len))
							log_printf(0, mc_44f037);
						else
							log_printf(0, mc_44f04c);
					} else
						log_printf(0, mc_44f140);
				} else
					log_printf(0, mc_44f074);
			}
		} else
			log_printf(0, mc_44f0b8, file);
		free(buf);
	} else
		log_printf(0, mc_44f0ec, file);
}

static const char mc_44f164[] __attribute__((aligned(4))) = "Updating patches from file: %s\n";
static const char mc_44f184[] __attribute__((aligned(1))) = "%d/bin/patches_%s.bin";
static const char mc_44f19a[] __attribute__((aligned(1))) = "%d/bin/patches_g2%s.bin";
static const char mc_44f1b2[] __attribute__((aligned(1))) = "%d/bin/patches_g2m%s.bin";
static const char mc_44f1cb[] __attribute__((aligned(1))) = "%d/bin/patches_fat.bin";
static const char mc_44f1e4[] __attribute__((aligned(4))) = "Updating patches in auto mode: %s\n";
static const char mc_44f208[] __attribute__((aligned(4))) = "\n***** ERROR: unable to determine console hack type!\n";
/* -p [<f>] */
NOPROF
void clientPatches(const char *file)
{
	char path[1024];
	u32 type = 0;
	u32 bs = cinfo->bootstrap;

	if (bs & 0x80000000)
		type = 1;
	else if (bs & 0x20000000)
		type = 2;
	else if (bs & 0x10000000)
		type = 3;
	else if (bs & 0x40000000)
		type = 2;
	if (type) {
		if (file) {
			strcpy(path, file);
			log_printf(0, mc_44f164, path);
		} else {
			if (bs & 0x80000000)
				sprintf(path, mc_44f184, *(u16 *)((u8 *)cinfo + 5), getConsoleTypeStr((bs & 0xf) + 1));
			else if (bs & 0x20000000)
				sprintf(path, mc_44f19a, *(u16 *)((u8 *)cinfo + 5), getConsoleTypeStr((bs & 0xf) + 1));
			else if (bs & 0x10000000)
				sprintf(path, mc_44f1b2, *(u16 *)((u8 *)cinfo + 5), getConsoleTypeStr((bs & 0xf) + 1));
			else if (bs & 0x40000000)
				sprintf(path, mc_44f1cb, *(u16 *)((u8 *)cinfo + 5));
			log_printf(0, mc_44f1e4, path);
		}
		updatePatches(path, type);
	} else
		log_printf(0, mc_44f208);
}

static const char mc_44f240[] __attribute__((aligned(4))) = "Reading 0x%x (%d) blocks from console starting at block 0x%x (%d)...\n";
static const char mc_44f288[] __attribute__((aligned(4))) = "Done!\nWriting 0x%x (%d) bytes to %s...\n";
static const char mc_44f2b0[] __attribute__((aligned(1))) = "Done!\n";
static const char mc_44f2b8[] __attribute__((aligned(4))) = "\n\n***** ERROR: Failed to write block data to file %s!\n";
static const char mc_44f2f0[] __attribute__((aligned(4))) = "\n\n***** ERROR: Trying to read blocks from the console failed!\n";
static const char mc_44f330[] __attribute__((aligned(4))) = "\n\n***** ERROR: This read command will exceed the system area size of 0x%x blocks!\n";
static const char mc_44f384[] __attribute__((aligned(4))) = "\n\n***** ERROR: Invalid arguments specified, please provide hex only for start block and number of blocks!\n";
/* -rb <f> <b> <l> */
NOPROF
void clientReadBlocks(const char *file, const char *sstart, const char *scount)
{
	u32 start = myatoh32(sstart, -1);
	u32 count = myatoh32(scount, -1);
	int len;
	u8 *buf;

	if (count != 0 && count != -1 && start != -1) {
		if (start + count <= cinfo->nandSize / cinfo->blockSize) {
			log_printf(0, mc_44f240, count, count, start, start);
			buf = netReadBlocksU32(&len, start, count);
			if (buf && len > 0) {
				log_printf(0, mc_44f288, len, len, file);
				if (writeFile(file, buf, len))
					log_printf(0, mc_44f2b0);
				else
					log_printf(0, mc_44f2b8, file);
				free(buf);
			} else
				log_printf(0, mc_44f2f0);
		} else
			log_printf(0, mc_44f330, cinfo->nandSize / cinfo->blockSize);
	} else
		log_printf(0, mc_44f384);
}

static const char mc_44f3f0[] __attribute__((aligned(4))) = "Writing 0x%x (%d) blocks to console starting at block 0x%x (%d)...\n";
static const char mc_44f434[] __attribute__((aligned(4))) = "Done! Wrote 0x%x (%d) bytes to console flash!\n";
static const char mc_44f464[] __attribute__((aligned(4))) = "\n\n***** ERROR: Writing data to console failed!\n";
static const char mc_44f494[] __attribute__((aligned(4))) = "\n\n***** ERROR: File %s size (0x%x) is not a multiple of console block size (0x%x)!\n";
static const char mc_44f4e8[] __attribute__((aligned(4))) = "\n\n***** ERROR: Unable to read file %s!\n";
/* -wb <f> <b> */
NOPROF
void clientWriteBlocks(const char *file, const char *sstart)
{
	u32 start = myatoh32(sstart, -1);
	u32 n;
	int len;
	u8 *buf;

	if (start == -1) {
		log_printf(0, mc_44f384);
		return;
	}
	buf = FileToBuffer(file, (size_t *)&len);
	if (!buf || len <= 0) {
		log_printf(0, mc_44f4e8, file);
		return;
	}
	n = len / cinfo->blockSize;
	if (!(len % cinfo->blockSize)) {
		if (start + n <= cinfo->nandSize / cinfo->blockSize) {
			log_printf(0, mc_44f3f0, n, n, start, start);
			if (netWriteBlocksU32(buf, len, start, n))
				log_printf(0, mc_44f434, len, len);
			else
				log_printf(0, mc_44f464);
		} else
			log_printf(0, mc_44f330, cinfo->nandSize / cinfo->blockSize);
	} else
		log_printf(0, mc_44f494, file, len, cinfo->blockSize);
	free(buf);
}

/* copy data into raw NAND pages (512 data + 16 spare) at logical offset off */
NOPROF
void patchNand(u8 *buf, int off, const u8 *data, int len)
{
	u8 *spare = buf + 512;

	while (off >= 512) {
		buf += 528;
		spare += 528;
		off -= 512;
	}
	if (off) {
		memcpy(buf + off, data, 512 - off);
		len -= 512 - off;
		calcPageEcc(buf, spare);
		data += 512 - off;
		buf += 528;
		spare += 528;
	}
	while (len >= 512) {
		memcpy(buf, data, 512);
		calcPageEcc(buf, spare);
		len -= 512;
		data += 512;
		spare += 528;
		buf += 528;
	}
	if (len) {
		memcpy(buf, data, len);
		calcPageEcc(buf, spare);
	}
}

static const char mc_44f510[] __attribute__((aligned(1))) = "file: %s start offset 0x%x\n";
static const char mc_44f52c[] __attribute__((aligned(4))) = "Reading 0x%x blocks from console starting at block 0x%x (%d)...\n";
static const char mc_44f570[] __attribute__((aligned(4))) = "Success!\nPatching in binary data...";
static const char mc_44f594[] __attribute__((aligned(4))) = "Writing 0x%x blocks from console starting at block 0x%x...\n";
static const char mc_44f5d0[] __attribute__((aligned(4))) = "Success! Completed patching NAND!\n";
static const char mc_44f5f4[] __attribute__((aligned(4))) = "\n\n***** ERROR: Reading data from console failed!\n";
static const char mc_44f628[] __attribute__((aligned(4))) = "\n\n***** ERROR: File %s size patched into offset 0x%x will exceed NAND system area (0x%x)!\n";
static const char mc_44f684[] __attribute__((aligned(4))) = "\n\n***** ERROR: Invalid arguments specified, please provide hex only for offset!\n";
/* -bp <f> <o> */
NOPROF
void clientBinPatch(const char *file, const char *soff)
{
	u32 size = cinfo->nandSize;
	u32 bs = cinfo->blockSize;
	u32 off, rem, start, count;
	size_t len;
	int rlen;
	const u8 *data;
	u8 *nand;

	off = myatoh32(soff, -1);
	if (cinfo->nandSize != 0x3000000) {
		size = cinfo->nandSize / 0x4200 * 0x4000;
		bs = cinfo->blockSize / 0x4200 * 0x4000;
	}
	if (off != -1) {
		log_printf(0, mc_44f510, file, soff);
		data = FileToBuffer(file, &len);
		if (data && len) {
			if (off + len < size) {
				rem = off % bs;
				start = rem / bs;
				count = (len + rem) / bs;
				if ((len + rem) % bs)
					count++;
				log_printf(0, mc_44f52c, count, start, start);
				nand = netReadBlocksU32(&rlen, start, count);
				if (nand && rlen) {
					log_printf(0, mc_44f570);
					switch (cinfo->nandSize) {
					default:
						patchNand(nand, rem, data, len);
						break;
					case 0x3000000:
						memcpy(nand + rem, data, len);
					}
					/* code-free hints: edi refs raise LRA's edi usage so the
					   post-loop len - 512 reload takes esi; the count use
					   orders its reload thread before start's (count esi) */
					{ int r; __asm__ volatile("" : "=D"(r)); __asm__ volatile("" :: "D"(r)); }
					{ int r; __asm__ volatile("" : "=D"(r)); __asm__ volatile("" :: "D"(r)); }
					log_printf(0, mc_44f2b0);
					log_printf(0, mc_44f594, count, start);
					__asm__("" :: "r"(count));
					if (netWriteBlocksU32(nand, rlen, start, count))
						log_printf(0, mc_44f5d0);
					else
						log_printf(0, mc_44f464);
				} else
					log_printf(0, mc_44f5f4);
			} else
				log_printf(0, mc_44f628, file, off, size);
		} else
			log_printf(0, mc_44f4e8, file);
	} else
		log_printf(0, mc_44f684);
}

static const char mc_44f6d5[] __attribute__((aligned(1))) = "erasing block 0x%x...";
static const char mc_44f6eb[] __attribute__((aligned(1))) = "Success!\n";
static const char mc_44f6f8[] __attribute__((aligned(4))) = "\n\n***** ERROR: Failed to erase block 0x%x!\n";
static const char mc_44f724[] __attribute__((aligned(4))) = "\n\n***** ERROR: Block 0x%x is outside system area!\n";
/* -eb <b> */
void clientEraseBlock(const char *sblock)
{
	u32 block = myatoh32(sblock, -1);

	if (block != -1) {
		if (block < cinfo->nandSize / cinfo->blockSize) {
			log_printf(0, mc_44f6d5, block);
			if (netEraseBlockU32(block, 1))
				log_printf(0, mc_44f6eb);
			else
				{ AT(efail) log_printf(0, mc_44f6f8, block); }
		} else
			{ log_printf(0, mc_44f724, block); JUMP(efail); }
	} else
		log_printf(0, mc_44f684);
}

/* the option's argument(s); dies with usage if one is missing or, with
   check, if a mode was already set */
NOPROF
char *getArgs(int argc, char **argv, int *pi, int mode, int check, char **arg2, char **arg3)
{
	int first = *pi + 1;
	int i = first;
	char *a = argv[i];

	if (i == argc || !a || *a == '-')
		client_usage(3, argv[first - 1]);
	if (arg2) {
		i++;
		a = argv[i];
		if (!a || i == argc || *a == '-')
			client_usage(4, argv[first - 1]);
		*arg2 = a;
	}
	if (arg3) {
		i++;
		a = argv[i];
		if (!a || i == argc || *a == '-')
			client_usage(4, argv[first - 1]);
		*arg3 = a;
	}
	if (mode && check)
		client_usage(5, argv[first - 1]);
	*pi = i;
	return argv[first];
}

static const char mc_44f757[] __attribute__((aligned(1))) = "client";
static const char mc_44f75e[] __attribute__((aligned(1))) = "help";
static const char mc_44f763[] __attribute__((aligned(1))) = "-?";
static const char mc_44f766[] __attribute__((aligned(1))) = "/?";
static const char mc_44f769[] __attribute__((aligned(1))) = "-noenter";
static const char mc_44f774[] __attribute__((aligned(4))) = "<enter> key on completion suppressed\n";
static const char mc_44f79a[] __attribute__((aligned(1))) = "-reboot";
static const char mc_44f7a4[] __attribute__((aligned(4))) = "shutdown superseded by reboot, ignoring -s in favor of -reboot\n";
static const char mc_44f7e4[] __attribute__((aligned(1))) = "setting reboot on completion\n";
static const char mc_44f802[] __attribute__((aligned(1))) = "-bp";
static const char mc_44f808[] __attribute__((aligned(4))) = "setting binary patch file to %s, offset %s\n";
static const char mc_44f834[] __attribute__((aligned(1))) = "-rb";
static const char mc_44f838[] __attribute__((aligned(4))) = "reading %s blocks to %s, starting block %s\n";
static const char mc_44f864[] __attribute__((aligned(1))) = "-wb";
static const char mc_44f868[] __attribute__((aligned(4))) = "writing blocks from %s, starting at block %s\n";
static const char mc_44f896[] __attribute__((aligned(1))) = "-eb";
static const char mc_44f89a[] __attribute__((aligned(1))) = "erase block set to %s\n";
static const char mc_44f8b1[] __attribute__((aligned(1))) = "-s";
static const char mc_44f8b4[] __attribute__((aligned(4))) = "reboot has already been set on command line, ignoring -s\n";
static const char mc_44f8f0[] __attribute__((aligned(4))) = "setting shutdown on completion\n";
static const char mc_44f910[] __attribute__((aligned(1))) = "-keys";
static const char mc_44f916[] __attribute__((aligned(1))) = "-ip";
static const char mc_44f91a[] __attribute__((aligned(1))) = "setting forced IP to %s\n";
static const char mc_44f933[] __attribute__((aligned(1))) = "-r";
static const char mc_44f936[] __attribute__((aligned(1))) = "setting read filename to %s\n";
static const char mc_44f953[] __attribute__((aligned(1))) = "-w";
static const char mc_44f956[] __attribute__((aligned(1))) = "setting write filename to %s\n";
static const char mc_44f974[] __attribute__((aligned(1))) = "-e";
static const char mc_44f978[] __attribute__((aligned(4))) = "setting avatar/kinect files base path to %s\n";
static const char mc_44f9a5[] __attribute__((aligned(1))) = "-c";
static const char mc_44f9a8[] __attribute__((aligned(4))) = "setting xbox compatibility files base path to %s\n";
static const char mc_44f9da[] __attribute__((aligned(1))) = "-i";
static const char mc_44f9dd[] __attribute__((aligned(1))) = "info dump path set to %s\n";
static const char mc_44f9f7[] __attribute__((aligned(1))) = "-p";
static const char mc_44f9fa[] __attribute__((aligned(1))) = "patch file set to %s\n";
static const char mc_44fa10[] __attribute__((aligned(1))) = "-v";
static const char mc_44fa14[] __attribute__((aligned(4))) = "\n\n***** ERROR: cannot send avatar data when a HDD does not exist!\n";
static const char mc_44fa58[] __attribute__((aligned(4))) = "\n\n***** ERROR: cannot send xbox compatibility data when a HDD does not exist!\n";
static const char mc_44faa8[] __attribute__((aligned(4))) = "\n\n***** ERROR: invalid mode specified, please inform author\n";
static const char mc_44fae8[] __attribute__((aligned(4))) = "\n\n***** ERROR: unable to connect to xbox server\n";
#define E(x) __builtin_expect((x), 1)
int mode_client(int argc, char **argv)
{
	char dummy[] = "dummy";
	char *start = NULL, *count = NULL;
	int i = 0;
	int reboot = 0;
	char *ip = NULL;
	char *arg = NULL;
	int mode = 0;
	char *a, *b;
	int j;

	log_set_name(mc_44f757);
	for (i = 0; i < argc; i++) {
		if (!strnicmp(argv[i], mc_44f75e, 2) || !strnicmp(argv[i], mc_44f763, 2) || !strnicmp(argv[i], mc_44f766, 2))
			client_usage(0, NULL);
		if (!strnicmp(argv[i], mc_44f769, 8)) {
			log_printf(0, mc_44f774);
			promptEnter = 0;
		} else if (!strnicmp(argv[i], mc_44f79a, 7)) {
			if (reboot == 1)
				log_printf(0, mc_44f7a4);
			log_printf(0, mc_44f7e4);
			reboot = 2;
		} else if (E(!strnicmp(argv[i], mc_44f802, 3))) {
			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				client_usage(3, argv[i]);
			__asm__("" :: "r"((unsigned)(i + 1) * 4));
			__asm__("" :: "r"((unsigned)(i + 1) * 4));
			b = argv[i + 2];
			j = i + 2;
			if (j == argc || !b || *b == '-')
				client_usage(4, argv[i]);
			start = b;
			if (mode)
				client_usage(5, argv[i]);
			i = j;
			arg = argv[i - 1];
			log_printf(0, mc_44f808, arg, start);
			mode = 11;
		} else if (!strnicmp(argv[i], mc_44f834, 3)) {
			arg = getArgs(argc, argv, &i, mode, 1, &start, &count);
			log_printf(0, mc_44f838, count, arg, start);
			mode = 8;
		} else if (E(!strnicmp(argv[i], mc_44f864, 3))) {
			j = i + 1;
			a = argv[j];
			if (j == argc || !a || *a == '-')
				client_usage(3, argv[i]);
			__asm__("" :: "r"((unsigned)j * 4));
			__asm__("" :: "r"((unsigned)j * 4));
			b = argv[i + 2];
			if (i + 2 == argc || !b || *b == '-')
				client_usage(4, argv[i]);
			start = b;
			if (mode)
				client_usage(5, argv[i]);
			i += 2;
			arg = argv[i - 1];
			log_printf(0, mc_44f868, arg, start);
			mode = 9;
		} else if (E(!strnicmp(argv[i], mc_44f896, 3))) {
			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				client_usage(3, argv[i]);
			if (mode)
				client_usage(5, argv[i]);
			arg = argv[++i];
			log_printf(0, mc_44f89a, arg);
			mode = 10;
		} else if (!strnicmp(argv[i], mc_44f8b1, 2)) {
			if (reboot == 2)
				log_printf(0, mc_44f8b4);
			else {
				log_printf(0, mc_44f8f0);
				reboot = 1;
			}
		} else if (!strnicmp(argv[i], mc_44f910, 5)) {
			mode = 3;
			arg = dummy;
		} else if (!strnicmp(argv[i], mc_44f916, 3)) {
			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				client_usage(3, argv[i]);
			ip = argv[++i];
			log_printf(0, mc_44f91a, ip);
		} else if (!strnicmp(argv[i], mc_44f933, 2)) {
			a = argv[i + 1];
			if (i + 1 == argc || !a || *a == '-')
				client_usage(3, argv[i]);
			if (mode)
				client_usage(5, argv[i]);
			arg = argv[++i];
			log_printf(0, mc_44f936, arg);
			mode = 1;
		} else if (!strnicmp(argv[i], mc_44f953, 2)) {
			a = argv[i + 1];
			if (i + 1 == argc || !a || *a == '-')
				client_usage(3, argv[i]);
			if (mode)
				client_usage(5, argv[i]);
			arg = argv[++i];
			log_printf(0, mc_44f956, arg);
			mode = 2;
		} else if (E(!strnicmp(argv[i], mc_44f974, 2))) {
			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				client_usage(3, argv[i]);
			if (mode)
				client_usage(5, argv[i]);
			arg = argv[++i];
			log_printf(0, mc_44f978, arg);
			mode = 4;
		} else if (E(!strnicmp(argv[i], mc_44f9a5, 2))) {
			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				client_usage(3, argv[i]);
			if (mode)
				client_usage(5, argv[i]);
			arg = argv[++i];
			log_printf(0, mc_44f9a8, arg);
			mode = 5;
		} else if (!strnicmp(argv[i], mc_44f9da, 2)) {
			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				arg = dummy;
			else {
				arg = argv[++i];
				log_printf(0, mc_44f9dd, arg);
			}
			mode = 12;
		} else if (!strnicmp(argv[i], mc_44f9f7, 2)) {
			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				arg = dummy;
			else {
				arg = argv[++i];
				log_printf(0, mc_44f9fa, arg);
			}
			mode = 7;
		} else if (!strnicmp(argv[i], mc_44fa10, 2))
			log_verbose_flag(argv[i][2]);
		else
			client_usage(1, argv[i]);
	}
	if (NO_MODE_ARG(mode, arg)) {
		if (reboot) {
			if (netConnect(ip)) {
			rok: __attribute__((cold));
				cinfo = netGetInfo();
				JUMP(c12, c11, p0, i0, c9, hdd4, hdd5, c2, c1, c10, u2, cdef, c8, c7, c3, s5);
			} else
				goto fail;
		} else
			{ AT(u2) client_usage(2, NULL); }
	} else {
		if (netConnect(ip)) {
			JUMP(i1, p1, hdd5, hdd4, c10, c9, c1, c7, cdef);
			cinfo = netGetInfo();
			switch (mode) {
			case 1:
				AT(c1) netDumpNand(arg);
				break;
			case 2:
				AT(c2) clientWrite(arg);
				break;
			case 3:
				AT(c3) clientKeys();
				break;
			case 4:
				if (cinfo->hwFlags & 0x20)
					sendAvatarData(arg, cinfo->kernel);
				else
					AT(hdd4) log_printf(0, mc_44fa14);
				break;
			case 5:
				if (cinfo->hwFlags & 0x20)
					{ AT(s5) sendCompatData(arg); }
				else
					AT(hdd5) log_printf(0, mc_44fa58);
				break;
			case 6:
				break;
			case 7:
				AT(c7) if (arg == dummy)
					{ AT(p0) clientPatches(NULL); JUMP(i0); }
				else
					{ AT(p1) clientPatches(arg); }
				break;
			case 8:
				AT(c8) clientReadBlocks(arg, start, count);
				break;
			case 9:
				AT(c9) clientWriteBlocks(arg, start);
				break;
			case 10:
				AT(c10) clientEraseBlock(arg);
				break;
			case 11:
				AT(c11) clientBinPatch(arg, start);
				break;
			case 12:
				AT(c12) if (arg == dummy)
					{ AT(i0) clientInfo(NULL); }
				else
					{ AT(i1) clientInfo(arg); }
				break;
			default:
				AT(cdef) log_printf(0, mc_44faa8);
				break;
			}
		} else
			goto fail;
	}
	if (E(reboot))
		netReboot(reboot);
	netDisconnect();
	return 0;
fail: __attribute__((cold));
	log_printf(0, mc_44fae8);
	return 0;
}

/* 16 zero bytes end the original object's .rdata */
static const char mc_rdpad[16] __attribute__((used)) = {0};

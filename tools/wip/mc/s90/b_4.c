/* mode_client: `xeBuild client`, single commands against a console over the network */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* build.sh compiles this file twice: plainly (every function but
   mode_client), and with -DBUILD_FDO and a crafted profile
   (src/mode_client.prof) for mode_client and the clientEraseBlock it
   inlines; mode_client comes from that compile (tools/re/splice.py --whole).
   Under BUILD_FDO the other functions keep the guessed profile (NOPROF,
   from xebuild.h),
   and mode_client's blocks get labels (AT) reached by empty asm gotos
   (JUMP): dead edges whose only effect is bb-reorder's priority keys and
   the frequencies of the blocks they enter (tools/wip/mc/s18/NOTES.md); the
   empty asm in NO_MODE_ARG splits the test the same way.  Without
   BUILD_FDO they expand to the plain source.  String literals land in
   .rdata in function order (-fno-toplevel-reorder) and, within one, in
   block order; two empty asm "i" hints fix that order where the shape
   alone doesn't. */
#define NOPROF
#define AT(l) l:
#define JUMP(...)
#define JMP(...) __asm__ goto ("" :::: __VA_ARGS__)
#define NO_MODE_ARG(m, a) (!((m) && (a)))


#include "xebuild.h"
#include "console_hdd.h"
#include "consoleinfo.h"
#include "fileutil.h"
#include "image_write.h"
#include "log.h"
#include "main.h"
#include "mode_client.h"
#include "net.h"

/* TODO(prototype cast): net.c takes uint16_t block numbers; mode_client's calls
   compile to the original's code only with uint32_t ones */
int netEraseBlockU32(uint32_t block, int force) __asm__("_netEraseBlock");
uint8_t *netReadBlocksU32(int *len, uint32_t start, uint32_t count) __asm__("_netReadBlocks");
int netWriteBlocksU32(uint8_t *buf, int len, uint32_t start, uint32_t count) __asm__("_netWriteBlocks");

void client_usage(int err, const char *arg) __attribute__((noreturn));
int dumpKey(const char *name, const char *file, const uint8_t *key, size_t len, uint32_t sum);
int checkPatches(uint8_t *buf, size_t *len, uint32_t type);
void updatePatches(const char *file, uint32_t type);
void patchNand(uint8_t *buf, int off, const uint8_t *data, int len);

/* the original object's .bss is 32 bytes, cinfo at its start */
static struct consoleinfo *cinfo __attribute__((aligned(32)));
static char mc_bsspad[28] __attribute__((used));

NOPROF
void client_usage(int err, const char *arg)
{
	switch (err) {
	case 3:
		log_printf(0, "\n\n***** ERROR: option flag %s on command line but no argument provided!\n", arg);
		break;
	case 4:
		log_printf(0, "\n\n***** ERROR: option flag %s on command line not enough arguments provided!\n", arg);
		break;
	case 5:
		log_printf(0, "\n\n***** ERROR: option flag %s on command line but option was already set!\n", arg);
		break;
	case 1:
		log_printf(0, "\n\n***** ERROR: unknown option '%s' provided on command line!\n", arg);
		break;
	case 2:
		log_printf(0, "\n\n***** ERROR: not enough info provided to carry out command!\n");
		break;
	}
	log_printf(0, separator);
	log_printf(0, "Usage   :\n   %s client <switch> [<option>]\n\n", "xeBuild");
	log_printf(0, "Examples:\n");
	log_printf(0, "   %s client -r nanddump.bin\n", "xeBuild");
	log_printf(0, "   %s client -w nandflash.bin -ip 192.168.2.100\n", "xeBuild");
	log_printf(0, "\nSwitches:\n");
	log_printf(0, "   -i             : connects to console and shows some info about it\n");
	log_printf(0, "*  -i <d>         : collects console information into folder <d>, usually enough for build mode\n");
	log_printf(0, "   -r <f>         : dumps system area of NAND to <f>\n");
	log_printf(0, "   -w <f>         : writes system area of NAND from <f>\n");
	log_printf(0, "   -e <d>         : format partition and send avatar/kinect data to HDD from <d>, must match running kernel\n");
	log_printf(0, "   -c <d>         : format partition and send xbox compatibility data to HDD from <d>\n");
	log_printf(0, "   -p             : will attempt to automatically update patches based on running kernel version\n");
	log_printf(0, "   -p <f>         : update patches with <f>\n");
	log_printf(0, "   -rb <f> <b> <l>: read series of blocks starting at <b> for <l>\n");
	log_printf(0, "   -wb <f> <b>    : write series of blocks starting at <b> for the number of blocks in <f>\n");
	log_printf(0, "   -eb <b>        : attempt to erase a single block, even if marked bad on console\n");
	log_printf(0, "   -bp <f> <o>    : binary patch NAND with contents of <f> to logical offset <o>\n");
	log_printf(0, "*  -keys          : will attempt to dump RSA and 1BL keys from console\n");
	log_printf(0, "   -s             : shutdown console\n");
	log_printf(0, "   -ip <add>      : force attempt to connect to addr (ie: -i 192.168.0.100)\n");
	log_printf(0, "   -noenter       : suppresses prompt for enter key when finished\n");
	log_printf(0, "   -reboot        : causes the console to hard reboot\n");
	log_printf(0, "   -v             : shows more info during client process\n");
	log_printf(0, "   -?             : shows this help\n\n");
	log_printf(0, "legend:\n");
	log_printf(0, "<add>    = without this option network will be scanned for server broadcast beacon\n");
	log_printf(0, "           If provided the correct format is an IPv4 address like 192.168.0.100\n");
	log_printf(0, "<f>      = path, absolute or relative, to a file\n");
	log_printf(0, "<d>      = path, absolute or relative, to a directory - do not terminate with /\n");
	log_printf(0, "<b>      = hexadecimal block number\n");
	log_printf(0, "<l>      = hexadecimal number of blocks\n");
	log_printf(0, "<o>      = hexadecimal logical offset (spare data not considered) in flash\n");
	log_printf(0, "notes:\n");
	log_printf(0, "* functions not fully supported with older patch versions, use with caution.\n");
	log_printf(0, "- client mode tends to operate on a single command basis, stacking commands.\n");
	log_printf(0, "  is not possible with the exception of v, noenter, ip, s and reboot.\n");
	log_printf(0, "- patch update (-p) will retain any addon patches already on the console.\n");
	log_printf(0, separator);
	log_finish();
	if (promptEnter) {
		log_printf(0, "\npress <enter> to quit...\n");
		fgetc(stdin);
	}
	exit(1);
}

/* -i [<d>]: console info, bad blocks; with <d> also the info files and a NAND dump */
NOPROF
void clientInfo(const char *dir)
{
	char path[1024];
	const char *out = NULL;
	int len;
	uint8_t *bad;
	int i;

	if (dir) {
		log_printf(0, "creating mydata folder output at %s\n", dir);
		if (createDir(dir))
			out = dir;
		else
			log_printf(0, "unable to dump details to %s, disabling\n", dir);
	}
	parseConsoleInfo(0, out, out, NULL);
	bad = netGetBadBlocks(&len);
	if (bad && len) {
		log_printf(0, "Bad Block list  : ");
		for (i = len - 2; i >= 0; i -= 2) {
			log_printf(0, "0x%x", getBeU16(bad + i));
			if (i)
				log_printf(0, ",");
		}
	}
	if (out) {
		strcpy(path, dir);
		strcat(path, "/nanddump.bin");
		log_printf(0, "dumping console flash to %s\n", path);
		/* .rdata order hint (testing success first flips the branch) */
		__asm__("" :: "i"("success!\n"));
		if (!netDumpNand(path))
			log_printf(0, "failed!\n");
		else
			log_printf(0, "success!\n");
	}
}

/* -w <f> */
NOPROF
int clientWrite(const char *file)
{
	size_t len;
	uint8_t *buf;
	int ret = 0;

	netTimerStart();
	log_printf(0, "reading file %s...", file);
	buf = FileToBuffer(file, &len);
	if (buf) {
		log_printf(0, "success, read 0x%x bytes\n", len);
		if (getBeU16(buf) == 0xff4f) {
			if (cinfo->nandSize == len) {
				log_printf(0, "sending data to console...\n");
				ret = netSendFlash(buf, len);
			} else
				log_printf(0, "\n\n***** ERROR: file size should be 0x%x but its 0x%x bytes! Aborted!\n", cinfo->nandSize, len);
		} else
			log_printf(0, "\n\n***** ERROR: image magic should be 0xFF4F but its 0x%x! Aborted!\n", getBeU16(buf));
		free(buf);
	} else
		log_printf(0, "\n\n***** ERROR: unable to read file to send\n");
	return ret;
}

NOPROF
void clientManifest(const char *dir)
{
	int i;

	if (!loadManifest(dir, cinfo->kernel & ~0xf))
		return;
	for (i = 0; i < manifest.count; i++)
		log_printf(1, "item %03d: %08x %08x %s\n", i + 1, manifest.e[i].len, manifest.e[i].data, manifest.e[i].path);
	log_printf(1, "manifest, %08x %08x %s\n", manifest.size, manifest.size, manifest.path);
	freeManifest();
}

NOPROF
int dumpKey(const char *name, const char *file, const uint8_t *key, size_t len, uint32_t sum)
{
	uint32_t want = sum;
	int ret = 0;

	log_printf(0, "checking %s (file ./%s)\n", name, file);
	if (FileExists(file))
		FileToBuffer(file, &len);
	if (sumBytes(key, len) == want) {
		log_printf(0, "dumping valid %s to file ./%s\n", name, file);
		if (len == 16)
			ret = writeKeyFile("./", file, key);
		else
			ret = writeFileIn("./", file, key, len);
	}
	if (!ret)
		log_printf(0, "\n\n****** ERROR: unable to dump %s to file ./%s, key is not valid or file is inaccessible!\n", name, file);
	return ret;
}

/* -keys */
NOPROF
void clientKeys(void)
{
	if ((uint8_t)cinfo->version > 1) {
		dumpKey("1BL key", "1blkey.txt", cinfo->key1bl, 16, 2435);
		dumpKey("1BL RSA pub key", "1BL_pub.bin", (const uint8_t *)&cinfo->pub1bl, 272, 31175);
		dumpKey("PIRS RSA pub key", "PIRS_pub.bin", (const uint8_t *)&cinfo->pubPirs, 272, 32976);
		dumpKey("MASTER RSA pub key", "MAST_pub.bin", (const uint8_t *)&cinfo->pubMaster, 272, 33852);
	} else
		log_printf(0, "\n\n****** ERROR: console patches need to be updated to support this operation!\n");
}

/* patches are sections separated by 0xffffffff: JTAG has 4, glitch 3 and
   loses the first (glitch2 keeps 16 bytes of 0xff in its place) */
NOPROF
int checkPatches(uint8_t *buf, size_t *len, uint32_t type)
{
	uint32_t marker = 0xffffffff;
	uint8_t *p;
	size_t n, i, off;

	if (type > 1) {
		log_printf(0, "checking patch sections for glitch console\n");
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
			log_printf(0, "\n\n***** ERROR: patches do not contain all segments, aborting!\n");
		return 0;
	}
	n = countInst(buf, *len, &marker, 4);
	log_printf(0, "checking patch sections for JTAG console\n");
	if (n == 4)
		return 1;
	log_printf(0, "\n\n***** ERROR: patches do not contain all segments, counted %d - aborting!\n", n);
	return 0;
}

NOPROF
void updatePatches(const char *file, uint32_t type)
{
	size_t len, cur;
	uint8_t *buf, *patches;
	int same;

	buf = FileToBuffer(file, &len);
	if (buf) {
		if (len) {
			log_printf(0, "loaded %s size 0x%x (%d) bytes\n", file, len, len);
			if (checkPatches(buf, &len, type)) {
				log_printf(0, "retrieving patches from console...");
				patches = netGetFile("patches", &cur);
				if (patches) {
					log_printf(1, "success! received 0x%x (%d) bytes\n", cur, cur);
					same = 0;
					if (len == cur && !memcmp(buf, patches, len))
						same = 1;
					if (!same) {
						log_printf(0, "sending update patches to console...");
						if (netWritePatches(buf, len))
							log_printf(0, "patches updated OK!\n");
						else
							log_printf(0, "\n\n***** ERROR: patch update failed!\n");
					} else
						log_printf(0, "patches are already up to date!\n");
				} else
					log_printf(0, "\n\n***** ERROR: failed to retrieve current patches from console!\n");
			}
		} else
			log_printf(0, "\n\n***** ERROR: %s exists but is 0 len, aborting\n", file);
		free(buf);
	} else
		log_printf(0, "\n\n***** ERROR: could not load %s, aborting\n", file);
}

/* -p [<f>] */
NOPROF
void clientPatches(const char *file)
{
	char path[1024];
	uint32_t type = 0;
	uint32_t bs = cinfo->bootstrap;

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
			log_printf(0, "Updating patches from file: %s\n", path);
		} else {
			if (bs & 0x80000000)
				sprintf(path, "%d/bin/patches_%s.bin", *(uint16_t *)((uint8_t *)cinfo + 5), getConsoleTypeStr((bs & 0xf) + 1));
			else if (bs & 0x20000000)
				sprintf(path, "%d/bin/patches_g2%s.bin", *(uint16_t *)((uint8_t *)cinfo + 5), getConsoleTypeStr((bs & 0xf) + 1));
			else if (bs & 0x10000000)
				sprintf(path, "%d/bin/patches_g2m%s.bin", *(uint16_t *)((uint8_t *)cinfo + 5), getConsoleTypeStr((bs & 0xf) + 1));
			else if (bs & 0x40000000)
				sprintf(path, "%d/bin/patches_fat.bin", *(uint16_t *)((uint8_t *)cinfo + 5));
			log_printf(0, "Updating patches in auto mode: %s\n", path);
		}
		updatePatches(path, type);
	} else
		log_printf(0, "\n***** ERROR: unable to determine console hack type!\n");
}

/* -rb <f> <b> <l> */
NOPROF
void clientReadBlocks(const char *file, const char *sstart, const char *scount)
{
	uint32_t start = myatoh32(sstart, -1);
	uint32_t count = myatoh32(scount, -1);
	int len;
	uint8_t *buf;

	if (count != 0 && count != -1 && start != -1) {
		if (start + count <= cinfo->nandSize / cinfo->blockSize) {
			log_printf(0, "Reading 0x%x (%d) blocks from console starting at block 0x%x (%d)...\n", count, count, start, start);
			buf = netReadBlocksU32(&len, start, count);
			if (buf && len > 0) {
				log_printf(0, "Done!\nWriting 0x%x (%d) bytes to %s...\n", len, len, file);
				if (writeFile(file, buf, len))
					log_printf(0, "Done!\n");
				else
					log_printf(0, "\n\n***** ERROR: Failed to write block data to file %s!\n", file);
				free(buf);
			} else
				log_printf(0, "\n\n***** ERROR: Trying to read blocks from the console failed!\n");
		} else
			log_printf(0, "\n\n***** ERROR: This read command will exceed the system area size of 0x%x blocks!\n", cinfo->nandSize / cinfo->blockSize);
	} else
		log_printf(0, "\n\n***** ERROR: Invalid arguments specified, please provide hex only for start block and number of blocks!\n");
}

/* -wb <f> <b> */
NOPROF
void clientWriteBlocks(const char *file, const char *sstart)
{
	uint32_t start = myatoh32(sstart, -1);
	uint32_t n;
	int len;
	uint8_t *buf;

	if (start == -1) {
		log_printf(0, "\n\n***** ERROR: Invalid arguments specified, please provide hex only for start block and number of blocks!\n");
		return;
	}
	/* .rdata order hint: these come before the read error (a nested
	   success-first shape moves the error blocks) */
	__asm__("" :: "i"("Writing 0x%x (%d) blocks to console starting at block 0x%x (%d)...\n"),
		"i"("Done! Wrote 0x%x (%d) bytes to console flash!\n"),
		"i"("\n\n***** ERROR: Writing data to console failed!\n"),
		"i"("\n\n***** ERROR: File %s size (0x%x) is not a multiple of console block size (0x%x)!\n"));
	buf = FileToBuffer(file, (size_t *)&len);
	if (!buf || len <= 0) {
		log_printf(0, "\n\n***** ERROR: Unable to read file %s!\n", file);
		return;
	}
	n = len / cinfo->blockSize;
	if (!(len % cinfo->blockSize)) {
		if (start + n <= cinfo->nandSize / cinfo->blockSize) {
			log_printf(0, "Writing 0x%x (%d) blocks to console starting at block 0x%x (%d)...\n", n, n, start, start);
			if (netWriteBlocksU32(buf, len, start, n))
				log_printf(0, "Done! Wrote 0x%x (%d) bytes to console flash!\n", len, len);
			else
				log_printf(0, "\n\n***** ERROR: Writing data to console failed!\n");
		} else
			log_printf(0, "\n\n***** ERROR: This read command will exceed the system area size of 0x%x blocks!\n", cinfo->nandSize / cinfo->blockSize);
	} else
		log_printf(0, "\n\n***** ERROR: File %s size (0x%x) is not a multiple of console block size (0x%x)!\n", file, len, cinfo->blockSize);
	free(buf);
}

/* copy data into raw NAND pages (512 data + 16 spare) at logical offset off */
NOPROF
void patchNand(uint8_t *buf, int off, const uint8_t *data, int len)
{
	uint8_t *spare = buf + 512;

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

/* -bp <f> <o> */
NOPROF
void clientBinPatch(const char *file, const char *soff)
{
	uint32_t size = cinfo->nandSize;
	uint32_t bs = cinfo->blockSize;
	uint32_t off, rem, start, count;
	size_t len;
	int rlen;
	const uint8_t *data;
	uint8_t *nand;

	off = myatoh32(soff, -1);
	if (cinfo->nandSize != 0x3000000) {
		size = cinfo->nandSize / 0x4200 * 0x4000;
		bs = cinfo->blockSize / 0x4200 * 0x4000;
	}
	if (off != -1) {
		log_printf(0, "file: %s start offset 0x%x\n", file, soff);
		data = FileToBuffer(file, &len);
		if (data && len) {
			if (off + len < size) {
				rem = off % bs;
				start = rem / bs;
				count = (len + rem) / bs;
				if ((len + rem) % bs)
					count++;
				log_printf(0, "Reading 0x%x blocks from console starting at block 0x%x (%d)...\n", count, start, start);
				nand = netReadBlocksU32(&rlen, start, count);
				if (nand && rlen) {
					log_printf(0, "Success!\nPatching in binary data...");
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
					log_printf(0, "Done!\n");
					log_printf(0, "Writing 0x%x blocks from console starting at block 0x%x...\n", count, start);
					__asm__("" :: "r"(count));
					if (netWriteBlocksU32(nand, rlen, start, count))
						log_printf(0, "Success! Completed patching NAND!\n");
					else
						log_printf(0, "\n\n***** ERROR: Writing data to console failed!\n");
				} else
					log_printf(0, "\n\n***** ERROR: Reading data from console failed!\n");
			} else
				log_printf(0, "\n\n***** ERROR: File %s size patched into offset 0x%x will exceed NAND system area (0x%x)!\n", file, off, size);
		} else
			log_printf(0, "\n\n***** ERROR: Unable to read file %s!\n", file);
	} else
		log_printf(0, "\n\n***** ERROR: Invalid arguments specified, please provide hex only for offset!\n");
}

/* -eb <b> */
void clientEraseBlock(const char *sblock)
{
	uint32_t block = myatoh32(sblock, -1);

	if (block != -1) {
		if (block < cinfo->nandSize / cinfo->blockSize) {
			log_printf(0, "erasing block 0x%x...", block);
			if (netEraseBlockU32(block, 1))
				log_printf(0, "Success!\n");
			else
				{ AT(efail) log_printf(0, "\n\n***** ERROR: Failed to erase block 0x%x!\n", block); }
		} else
			{ log_printf(0, "\n\n***** ERROR: Block 0x%x is outside system area!\n", block); JUMP(efail); }
	} else
		log_printf(0, "\n\n***** ERROR: Invalid arguments specified, please provide hex only for offset!\n");
}

static void clientEraseBlockI(const char *sblock)
{
	uint32_t block = myatoh32(sblock, -1);



	if (block != -1) {
		if (block < cinfo->nandSize / cinfo->blockSize) {

			eerase: log_printf(0, "erasing block 0x%x...", block);
			if (netEraseBlockU32(block, 1))
				{ 
esucc:  log_printf(0, "Success!\n"); }
			else
				{ AT(efail) log_printf(0, "\n\n***** ERROR: Failed to erase block 0x%x!\n", block); }
		} else
			{ eout: log_printf(0, "\n\n***** ERROR: Block 0x%x is outside system area!\n", block); JUMP(efail); }
	} else
		{ einv: __attribute__((cold)); log_printf(0, "\n\n***** ERROR: Invalid arguments specified, please provide hex only for offset!\n"); }
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

	log_set_name("client");
	for (i = 0; i < argc; i++) {
 if ((char *)__builtin_constant_p(i + 60) == (char *)1 && (char *)__builtin_constant_p(i + 61) == (char *)1) goto wb3;
if (__builtin_constant_p(i + 320) && __builtin_constant_p(i + 321)) goto u2;
		if (!strnicmp(argv[i], "help", 2) || !strnicmp(argv[i], "-?", 2) || !strnicmp(argv[i], "/?", 2))
			client_usage(0, NULL);
		if (!strnicmp(argv[i], "-noenter", 8)) {
			log_printf(0, "<enter> key on completion suppressed\n");
			promptEnter = 0;
		} else if (!strnicmp(argv[i], "-reboot", 7)) {
			if (reboot == 1)
				log_printf(0, "shutdown superseded by reboot, ignoring -s in favor of -reboot\n");
			log_printf(0, "setting reboot on completion\n");
			reboot = 2;
		} else if (E(!strnicmp(argv[i], "-bp", 3))) {
			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				client_usage(3, argv[i]);
			__asm__("" :: "a"(i + 1));
			__asm__("" :: "r"((unsigned)(i + 1) * 4));
			b = argv[i + 2];
			j = i + 2;
			if (j == argc || !b || *b == '-')
				lu1: client_usage(4, argv[i]);
			start = b;
			if (mode)
				client_usage(5, argv[i]);
			i = j;
			arg = argv[i - 1];
			log_printf(0, "setting binary patch file to %s, offset %s\n", arg, start);
			mode = 11;
		} else if (!strnicmp(argv[i], "-rb", 3)) {
			arg = getArgs(argc, argv, &i, mode, 1, &start, &count);
			log_printf(0, "reading %s blocks to %s, starting block %s\n", count, arg, start);
			mode = 8;
		} else if (E(!strnicmp(argv[i], "-wb", 3))) {
			j = i + 1;
			a = argv[j];
			if (j == argc || !a || *a == '-')
				{ wb3: client_usage(3, argv[i]); }
			__asm__("" :: "r"((unsigned)j * 4));
			__asm__("" :: "r"((unsigned)j * 4));
			{ int k = i + 2; b = argv[k];
			if (!b || k == argc || *b == '-')
				client_usage(4, argv[i]); }
			start = b;
			if (mode)
				client_usage(5, argv[i]);
			i += 2;
			arg = argv[i - 1];
			log_printf(0, "writing blocks from %s, starting at block %s\n", arg, start);
			mode = 9;
		} else if (E(!strnicmp(argv[i], "-eb", 3))) {
			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				client_usage(3, argv[i]);
			if (mode)
				client_usage(5, argv[i]);
			arg = argv[++i];
			log_printf(0, "erase block set to %s\n", arg);
			mode = 10;
		} else if (!strnicmp(argv[i], "-s", 2)) {
			if ((char *)__builtin_constant_p(i + 300) == (char *)1 && (char *)__builtin_constant_p(i + 300 + 1) == (char *)1 && (char *)__builtin_constant_p(i + 300 + 2) == (char *)1) goto k61l;
if (__builtin_constant_p(i + 300)) goto cdef;
if (reboot == 2)
				log_printf(0, "reboot has already been set on command line, ignoring -s\n");
			else {
				log_printf(0, "setting shutdown on completion\n");
				reboot = 1;
			}
		} else if (!strnicmp(argv[i], "-keys", 5)) {
			mode = 3;
			arg = dummy;
		} else if (!strnicmp(argv[i], "-ip", 3)) {
			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				client_usage(3, argv[i]);
			

if ((char *)__builtin_constant_p(i + 30) == (char *)1 && (char *)__builtin_constant_p(i + 31) == (char *)1) goto k55l;  if ((char *)__builtin_constant_p(i + 40) == (char *)1 && (char *)__builtin_constant_p(i + 41) == (char *)1 && (char *)__builtin_constant_p(i + 42) == (char *)1) goto k67l;
ip = argv[++i];
			log_printf(0, "setting forced IP to %s\n", ip);
		} else { k55l: if (!strnicmp(argv[i], "-r", 2)) {
			a = argv[i + 1];
			if (i + 1 == argc || !a || *a == '-')
				client_usage(3, argv[i]);
			if (mode) { r5x: client_usage(5, argv[i]); }
			arg = argv[++i];
			log_printf(0, "setting read filename to %s\n", arg);
			mode = 1;
		} else { k61l: if (!strnicmp(argv[i], "-w", 2)) {
			a = argv[i + 1];
			if (i + 1 == argc || ({__asm__ goto("" :::: w5x); 0;}) || !a || *a == '-')
				client_usage(3, argv[i]);
			if (mode) { w5x: client_usage(5, argv[i]); }
			arg = argv[++i];
			log_printf(0, "setting write filename to %s\n", arg);
			mode = 2;
		} else { k67l: if (E(!strnicmp(argv[i], "-e", 2))) {
			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				client_usage(3, argv[i]);
			if (mode)
				client_usage(5, argv[i]);
			arg = argv[++i];
			log_printf(0, "setting avatar/kinect files base path to %s\n", arg);
			mode = 4;
		} else if (E(!strnicmp(argv[i], "-c", 2))) {
			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				client_usage(3, argv[i]);
			if (mode)
				client_usage(5, argv[i]);
			arg = argv[++i];
			log_printf(0, "setting xbox compatibility files base path to %s\n", arg);
			mode = 5;
		} else if (!strnicmp(argv[i], "-i", 2)) {
			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				arg = dummy;
			else {
				arg = argv[++i];
				log_printf(0, "info dump path set to %s\n", arg);
			}
			mode = 12;
		} else if (!strnicmp(argv[i], "-p", 2)) {
			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				arg = dummy;
			else {
				arg = argv[++i];
				log_printf(0, "patch file set to %s\n", arg);
			}
			mode = 7;
		} else if (!strnicmp(argv[i], "-v", 2))
			log_verbose_flag(argv[i][2]);
		else
			client_usage(1, argv[i]); } } }
	}
	if (NO_MODE_ARG(mode, arg)) {
		if (__builtin_constant_p(mode + 91) && __builtin_constant_p(mode + 92) && __builtin_constant_p(mode + 93) && __builtin_constant_p(mode + 94) && __builtin_constant_p(mode + 50094) && __builtin_constant_p(mode + 100094) && __builtin_constant_p(mode + 150094) && __builtin_constant_p(mode + 200094) && __builtin_constant_p(mode + 250094)) goto fkbo;
		if (__builtin_constant_p(mode + 130)) goto dtg;
		if (reboot) {
			if (netConnect(ip)) {
			rok: __attribute__((cold));
				cinfo = netGetInfo(); if (__builtin_constant_p(mode + 620)) goto ndl;
				{ struct {} rko; { struct {} rkv0; __asm__ ("" :: "m"(rko), "m"(rkv0)); __asm__ goto ("" :::: dsp, c1, c12, s5, c7, c9, c3, c8, c2, c10, cdef, rk0, rk1, rk2, rk3, rk4, rk5, rk6, rk7, rk8, rk9, rk10, rk11, rk12, rk13); goto rkn0; rk0: goto ork0; rk1: goto ork1; rk2: goto ork2; rk3: goto ork3; rk4: goto ork4; rk5: goto ork5; rk6: goto ork6; rk7: goto ork7; rk8: goto ork8; rk9: goto ork9; rk10: goto ork10; rk11: goto ork11; rk12: goto ork12; rk13: goto ork13; } rkn0: ; { struct {} rkv1; __asm__ ("" :: "m"(rko), "m"(rkv1)); __asm__ goto ("" :::: rk14, rk15, rk16, rk17, rk18, rk19, rk20, rk21, rk22, rk23, rk24, rk25, rk26, rk27, rk28, rk29, rk30, rk31, rk32, rk33, rk34, rk35, rk36, rk37, rk38, rk39, rk40, rk41, rk42, rk43); goto rkn1; rk14: goto ork14; rk15: goto ork15; rk16: goto ork16; rk17: goto ork17; rk18: goto ork18; rk19: goto ork19; rk20: goto ork20; rk21: goto ork21; rk22: goto ork22; rk23: goto ork23; rk24: goto ork24; rk25: goto ork25; rk26: goto ork26; rk27: goto ork27; rk28: goto ork28; rk29: goto ork29; rk30: goto ork30; rk31: goto ork31; rk32: goto ork32; rk33: goto ork33; rk34: goto ork34; rk35: goto ork35; rk36: goto ork36; rk37: goto ork37; rk38: goto ork38; rk39: goto ork39; rk40: goto ork40; rk41: goto ork41; rk42: goto ork42; rk43: goto ork43; } rkn1: ; { struct {} rkv2; __asm__ ("" :: "m"(rko), "m"(rkv2)); __asm__ goto ("" :::: rk44, rk45, rk46, rk47, rk48, rk49, rk50, rk51); goto rkn2; rk44: goto ork44; rk45: goto ork45; rk46: goto ork46; rk47: goto ork47; rk48: goto ork48; rk49: goto ork49; rk50: goto ork50; rk51: goto ork51; } rkn2: ; goto rkE; ork0: goto c1; ork1: goto c1; ork2: goto c12; ork3: goto c12; ork4: goto rkE; ork5: goto c12; ork6: goto c12; ork7: goto s5; ork8: goto s5; ork9: goto c3; ork10: goto c3; ork11: goto rkE; ork12: goto rkE; ork13: goto rkE; ork14: goto rkE; ork15: goto rkE; ork16: goto rkE; ork17: goto rkE; ork18: goto rkE; ork19: goto rkE; ork20: goto rkE; ork21: goto rkE; ork22: goto c8; ork23: goto c8; ork24: goto c8; ork25: goto c8; ork26: goto c10; ork27: goto c10; ork28: goto cdef; ork29: goto cdef; ork30: goto cdef; ork31: goto t4; ork32: goto t4; ork33: goto t4; ork34: goto t5; ork35: goto t5; ork36: goto t5; ork37: goto t5; ork38: goto t5; ork39: goto t5; ork40: goto t5; ork41: goto t5; ork42: goto t5; ork43: goto rkE; ork44: goto rkE; ork45: goto rkE; ork46: goto rkE; ork47: goto rkE; ork48: goto rkE; ork49: goto rkE; ork50: goto rkE; ork51: goto rkE; } rkE: ; 
			} else
				goto fail;
		} else
			{ AT(u2) client_usage(2, NULL); }
	} else {
		if (netConnect(ip)) {
			fkbo: { struct {} fko; { struct {} fkv; __asm__ ("" :: "X"(&fko), "X"(&fkv)); __asm__ goto ("" :::: p1, i1, dtg, ndl, c10, c9, c1, c7, cdef, fa0, fa1, fa2, fa3, fa4, fa5, fa6, fa7, fa8, fa9, fa10, fa11, fa12, fa13, fa14, fa15, fa16, fa17, fa18, fa19, fa20); fkA2: goto fkN; fa0: goto ofa0; fa1: goto ofa1; fa2: goto ofa2; fa3: goto ofa3; fa4: goto ofa4; fa5: goto ofa5; fa6: goto ofa6; fa7: goto ofa7; fa8: goto ofa8; fa9: goto ofa9; fa10: goto ofa10; fa11: goto ofa11; fa12: goto ofa12; fa13: goto ofa13; fa14: goto ofa14; fa15: goto ofa15; fa16: goto ofa16; fa17: goto ofa17; fa18: goto ofa18; fa19: goto ofa19; fa20: goto ofa20;  } ofa0: goto fkA2; ofa1: goto fkA2; ofa2: goto fkA2; ofa3: goto fkA2; ofa4: goto fkA2; ofa5: goto fkA2; ofa6: goto fkA2; ofa7: goto fkA2; ofa8: goto fkA2; ofa9: goto fkA2; ofa10: goto fkA2; ofa11: goto fkA2; ofa12: goto fkA2; ofa13: goto fkA2; ofa14: goto fkA2; ofa15: goto fkA2; ofa16: goto fkA2; ofa17: goto fkA2; ofa18: goto fkA2; ofa19: goto fkA2; ofa20: goto fkA2;  fkM: ; } fkN: ;
			dsp: cinfo = netGetInfo();
			 if (__builtin_constant_p(mode + 910) && __builtin_constant_p(mode + 911) && __builtin_constant_p(mode + 912) && __builtin_constant_p(mode + 913) && __builtin_constant_p(mode + 50913)) goto c9;  if (__builtin_constant_p(mode + 930) && __builtin_constant_p(mode + 931) && __builtin_constant_p(mode + 932) && __builtin_constant_p(mode + 933)) goto t4;      
			           if (__builtin_constant_p(mode + 1210) && __builtin_constant_p(mode + 1211) && __builtin_constant_p(mode + 1212) && __builtin_constant_p(mode + 1213) && __builtin_constant_p(mode + 51213) && __builtin_constant_p(mode + 101213)) mode = 7; else if (__builtin_constant_p(mode + 1230) && __builtin_constant_p(mode + 51230) && __builtin_constant_p(mode + 101230) && __builtin_constant_p(mode + 151230) && __builtin_constant_p(mode + 201230) && __builtin_constant_p(mode + 251230)) mode = 11; else if (__builtin_constant_p(mode + 1220) && __builtin_constant_p(mode + 1221) && __builtin_constant_p(mode + 1222) && __builtin_constant_p(mode + 1223) && __builtin_constant_p(mode + 51223) && __builtin_constant_p(mode + 101223)) mode = 9; switch (mode) {
			case 1:
				AT(c1) netDumpNand(arg);
				__asm__ goto ("" :::: dsp); __asm__ goto ("" :::: dsp); __asm__ goto ("" :::: dsp); break;
			case 2:
				AT(c2) clientWrite(arg);
				break;
			case 3:
				AT(c3)  { JMP(hdd4,s5,hdd5); clientKeys(); }
				__asm__ goto ("" :::: dsp); break;
			case 4:
				AT(t4)  if (cinfo->hwFlags & 0x20)
					s4: { JMP(i0); sendAvatarData(arg, cinfo->kernel); }
				else
					{ AT(hdd4) { hc4: __attribute__((cold)); } log_printf(0, "\n\n***** ERROR: cannot send avatar data when a HDD does not exist!\n"); }
				__asm__ goto ("" :::: dsp); break;
			case 5:
				AT(t5)  if (cinfo->hwFlags & 0x20)
					{ AT(s5) { JMP(s4,c12); sendCompatData(arg); } }
				else
					{ AT(hdd5) { hdd5_c: __attribute__((cold)); } log_printf(0, "\n\n***** ERROR: cannot send xbox compatibility data when a HDD does not exist!\n"); }
				break;
			case 6:
				break;
			case 7:
				AT(c7)  if (arg == dummy)
					{ AT(p0) { p0c: __attribute__((cold)); } clientPatches(NULL); JUMP(i0); }
				else
					{ AT(p1) clientPatches(arg); }
				break;
			case 8:
				AT(c8) { clientReadBlocks(arg, start, count); JMP(p1,cdef); }
				break;
			case 9:
				AT(c9) { clientWriteBlocks(arg, start); JMP(hdd4,hdd5); }
				__asm__ goto ("" :::: dsp); __asm__ goto ("" :::: dsp); __asm__ goto ("" :::: dsp); break;
			case 10:
				AT(c10) clientEraseBlockI(arg);
				break;
			case 11:
				AT(c11) clientBinPatch(arg, start);
				break;
			case 12:
				AT(c12) if (arg == dummy || ({JMP(p0); 0;}))
					{ AT(i0) { i0_c: __attribute__((cold)); } clientInfo(NULL); }
				else
					{ AT(i1) clientInfo(arg); }
				break;
			default:
				AT(cdef) if (__builtin_constant_p(mode + 430) && __builtin_constant_p(mode + 431) && __builtin_constant_p(mode + 432) && __builtin_constant_p(mode + 433) && __builtin_constant_p(mode + 434) && __builtin_constant_p(mode + 50434) && __builtin_constant_p(mode + 100434) && __builtin_constant_p(mode + 150434) && __builtin_constant_p(mode + 200434) && __builtin_constant_p(mode + 250434) && __builtin_constant_p(mode + 300434) && __builtin_constant_p(mode + 350434) && __builtin_constant_p(mode + 400434)) goto ndl; log_printf(0, "\n\n***** ERROR: invalid mode specified, please inform author\n");
				__asm__ goto ("" :::: dsp); __asm__ goto ("" :::: dsp); break;
			}
		} else
			goto fail;
	}
	
	dtg: if (E(reboot))
		netReboot(reboot);
	ndl: netDisconnect();
	  if (__builtin_constant_p(mode + 720) && __builtin_constant_p(mode + 721) && __builtin_constant_p(mode + 722) && __builtin_constant_p(mode + 723) && __builtin_constant_p(mode + 724) && __builtin_constant_p(mode + 725) && __builtin_constant_p(mode + 50725) && __builtin_constant_p(mode + 100725) && __builtin_constant_p(mode + 150725)) goto p0; if (__builtin_constant_p(mode + 730) && __builtin_constant_p(mode + 50730) && __builtin_constant_p(mode + 100730) && __builtin_constant_p(mode + 150730)) goto s5;  if (__builtin_constant_p(mode + 750) && __builtin_constant_p(mode + 50750)) goto u2; 
	return 0;
fail: __attribute__((cold));  if (__builtin_constant_p(mode + 2400) && __builtin_constant_p(mode + 52400) && __builtin_constant_p(mode + 102400) && __builtin_constant_p(mode + 152400)) goto c11; if (__builtin_constant_p(mode + 5562) && __builtin_constant_p(mode + 55562) && __builtin_constant_p(mode + 105562) && __builtin_constant_p(mode + 155562) && __builtin_constant_p(mode + 205562) && __builtin_constant_p(mode + 255562) && __builtin_constant_p(mode + 305562)) goto ndl; if (__builtin_constant_p(mode + 4120) && __builtin_constant_p(mode + 54120) && __builtin_constant_p(mode + 104120) && __builtin_constant_p(mode + 154120) && __builtin_constant_p(mode + 204120)) goto s4; if (__builtin_constant_p(mode + 3000) && __builtin_constant_p(mode + 53000) && __builtin_constant_p(mode + 103000) && __builtin_constant_p(mode + 153000)) goto t5; if (__builtin_constant_p(mode + 260)) goto ndl; if (__builtin_constant_p(mode + 6873) && __builtin_constant_p(mode + 56873) && __builtin_constant_p(mode + 106873) && __builtin_constant_p(mode + 156873) && __builtin_constant_p(mode + 206873) && __builtin_constant_p(mode + 256873) && __builtin_constant_p(mode + 306873) && __builtin_constant_p(mode + 356873) && __builtin_constant_p(mode + 406873) && __builtin_constant_p(mode + 456873)) goto ndl; if (__builtin_constant_p(mode + 8182) && __builtin_constant_p(mode + 58182) && __builtin_constant_p(mode + 108182) && __builtin_constant_p(mode + 158182) && __builtin_constant_p(mode + 208182)) goto ndl; if (__builtin_constant_p(mode + 7351) && __builtin_constant_p(mode + 57351) && __builtin_constant_p(mode + 107351) && __builtin_constant_p(mode + 157351) && __builtin_constant_p(mode + 207351) && __builtin_constant_p(mode + 257351)) goto dtg; if (__builtin_constant_p(mode + 205) && __builtin_constant_p(mode + 50205) && __builtin_constant_p(mode + 100205) && __builtin_constant_p(mode + 150205)) goto c3; if (__builtin_constant_p(mode + 5569) && __builtin_constant_p(mode + 55569) && __builtin_constant_p(mode + 105569) && __builtin_constant_p(mode + 155569) && __builtin_constant_p(mode + 205569)) goto dtg; if (__builtin_constant_p(mode + 7368) && __builtin_constant_p(mode + 57368) && __builtin_constant_p(mode + 107368) && __builtin_constant_p(mode + 157368) && __builtin_constant_p(mode + 207368) && __builtin_constant_p(mode + 257368)) goto ndl; if (__builtin_constant_p(mode + 6949) && __builtin_constant_p(mode + 56949) && __builtin_constant_p(mode + 106949) && __builtin_constant_p(mode + 156949)) goto dtg; if (__builtin_constant_p(mode + 3200) && __builtin_constant_p(mode + 53200) && __builtin_constant_p(mode + 103200) && __builtin_constant_p(mode + 153200)) goto c9;
	log_printf(0, "\n\n***** ERROR: unable to connect to xbox server\n");
	return 0;
}

/* 16 zero bytes end the original object's .rdata */
static const char mc_rdpad[16] __attribute__((used)) = {0};

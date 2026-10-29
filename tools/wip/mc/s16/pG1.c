/* mode_client: `xeBuild client`, single commands against a console over the network */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;

/* the console's info response (net.c) */
struct consoleinfo {
	u32 version;			/* 000 updsvr version; low byte: hv patches */
	u32 kernel;			/* 004 */
	u32 f008;			/* 008 */
	u32 bootstrap;			/* 00c hack type in the top bits */
	u32 hwFlags;			/* 010 0x20: has HDD */
	u32 nandSize;			/* 014 system area */
	u32 blockSize;			/* 018 */
	u32 pairing;			/* 01c */
	u8 cpuKey[16];			/* 020 */
	u8 dvdKey[16];			/* 030 */
	u8 fuses[96];			/* 040 */
	u8 vfuses[96];			/* 0a0 */
	u8 key1bl[16];			/* 100 */
	u8 pub1bl[272];			/* 110 */
	u8 pubPirs[272];		/* 220 */
	u8 pubMaster[272];		/* 330 */
};

/* the loaded manifest and the files it lists (console_hdd.c) */
struct manifest {
	void *data;
	char path[1024];
	size_t size;
	int count;
	struct {
		void *data;
		u32 len;
		char path[1024];
	} e[256];
};

void log_printf(int level, const char *fmt, ...);
void log_set_name(const char *name);
void log_verbose_flag(unsigned char c);
void log_finish(void);
u16 getBeU16(const u8 *p);
const char *getConsoleTypeStr(int type);
u32 myatoh32(const char *s, u32 def);
u32 sumBytes(const u8 *p, u32 len);
u8 *findInst(u8 *buf, int len, const void *pat, int patlen);
int countInst(u8 *buf, int len, const void *pat, int patlen);
int FileExists(const char *name);
void *FileToBuffer(const char *name, size_t *psize);
int writeFile(const char *name, const void *buf, size_t size);
int writeFileIn(const char *dir, const char *name, const void *buf, size_t size);
int writeKeyFile(const char *dir, const char *name, const u8 *key);
int createDir(const char *path);
int parseConsoleInfo(int level, const char *dir, const char *optDir, int *update);
void calcPageEcc(u8 *page, u8 *spare);
int loadManifest(const char *dir, u32 ver);
void freeManifest(void);
void sendAvatarData(const char *dir, u32 kernel);
u32 sendCompatData(const char *dir);
int netConnect(const char *ip);
void netDisconnect(void);
struct consoleinfo *netGetInfo(void);
u8 *netGetFile(const char *name, size_t *len);
u8 *netGetBadBlocks(int *len);
int netDumpNand(const char *path);
void netTimerStart(void);
int netSendFlash(u8 *buf, u32 len);
void netReboot(int how);
u8 *netReadBlocks(int *len, u32 start, u32 count);
int netWriteBlocks(u8 *buf, int len, u32 start, u32 count);
int netEraseBlock(u32 block, int force);
int netWritePatches(u8 *buf, size_t len);
void client_usage(int err, const char *arg) __attribute__((noreturn));
int dumpKey(const char *name, const char *file, const u8 *key, size_t len, u32 sum);
int checkPatches(u8 *buf, size_t *len, u32 type);
void updatePatches(const char *file, u32 type);
void patchNand(u8 *buf, int off, const u8 *data, int len);

extern char separator[];
extern int promptEnter;
extern struct manifest manifest;

static struct consoleinfo *cinfo;

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
void clientInfo(const char *dir)
{
	char path[1024];
	const char *out = NULL;
	int len;
	u8 *bad;
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
		if (!netDumpNand(path))
			log_printf(0, "failed!\n");
		else
			log_printf(0, "success!\n");
	}
}

/* -w <f> */
int clientWrite(const char *file)
{
	size_t len;
	u8 *buf;
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

int dumpKey(const char *name, const char *file, const u8 *key, size_t len, u32 sum)
{
	u32 want = sum;
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
void clientKeys(void)
{
	if ((u8)cinfo->version > 1) {
		dumpKey("1BL key", "1blkey.txt", cinfo->key1bl, 16, 2435);
		dumpKey("1BL RSA pub key", "1BL_pub.bin", cinfo->pub1bl, 272, 31175);
		dumpKey("PIRS RSA pub key", "PIRS_pub.bin", cinfo->pubPirs, 272, 32976);
		dumpKey("MASTER RSA pub key", "MAST_pub.bin", cinfo->pubMaster, 272, 33852);
	} else
		log_printf(0, "\n\n****** ERROR: console patches need to be updated to support this operation!\n");
}

/* patches are sections separated by 0xffffffff: JTAG has 4, glitch 3 and
   loses the first (glitch2 keeps 16 bytes of 0xff in its place) */
int checkPatches(u8 *buf, size_t *len, u32 type)
{
	u32 marker = 0xffffffff;
	u8 *p;
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

void updatePatches(const char *file, u32 type)
{
	size_t len, cur;
	u8 *buf, *patches;
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
			log_printf(0, "Updating patches from file: %s\n", path);
		} else {
			if (bs & 0x80000000)
				sprintf(path, "%d/bin/patches_%s.bin", *(u16 *)((u8 *)cinfo + 5), getConsoleTypeStr((bs & 0xf) + 1));
			else if (bs & 0x20000000)
				sprintf(path, "%d/bin/patches_g2%s.bin", *(u16 *)((u8 *)cinfo + 5), getConsoleTypeStr((bs & 0xf) + 1));
			else if (bs & 0x10000000)
				sprintf(path, "%d/bin/patches_g2m%s.bin", *(u16 *)((u8 *)cinfo + 5), getConsoleTypeStr((bs & 0xf) + 1));
			else if (bs & 0x40000000)
				sprintf(path, "%d/bin/patches_fat.bin", *(u16 *)((u8 *)cinfo + 5));
			log_printf(0, "Updating patches in auto mode: %s\n", path);
		}
		updatePatches(path, type);
	} else
		log_printf(0, "\n***** ERROR: unable to determine console hack type!\n");
}

/* -rb <f> <b> <l> */
void clientReadBlocks(const char *file, const char *sstart, const char *scount)
{
	u32 start = myatoh32(sstart, -1);
	u32 count = myatoh32(scount, -1);
	int len;
	u8 *buf;

	if (count != 0 && count != -1 && start != -1) {
		if (start + count <= cinfo->nandSize / cinfo->blockSize) {
			log_printf(0, "Reading 0x%x (%d) blocks from console starting at block 0x%x (%d)...\n", count, count, start, start);
			buf = netReadBlocks(&len, start, count);
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
void clientWriteBlocks(const char *file, const char *sstart)
{
	u32 start = myatoh32(sstart, -1);
	u32 n;
	int len;
	u8 *buf;

	if (start == -1) {
		log_printf(0, "\n\n***** ERROR: Invalid arguments specified, please provide hex only for start block and number of blocks!\n");
		return;
	}
	buf = FileToBuffer(file, (size_t *)&len);
	if (!buf || len <= 0) {
		log_printf(0, "\n\n***** ERROR: Unable to read file %s!\n", file);
		return;
	}
	n = len / cinfo->blockSize;
	if (!(len % cinfo->blockSize)) {
		if (start + n <= cinfo->nandSize / cinfo->blockSize) {
			log_printf(0, "Writing 0x%x (%d) blocks to console starting at block 0x%x (%d)...\n", n, n, start, start);
			if (netWriteBlocks(buf, len, start, n))
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

/* -bp <f> <o> */
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
				nand = netReadBlocks(&rlen, start, count);
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
					if (netWriteBlocks(nand, rlen, start, count))
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
	u32 block = myatoh32(sblock, -1);

	if (block != -1) {
		if (block < cinfo->nandSize / cinfo->blockSize) {
			log_printf(0, "erasing block 0x%x...", block);
			if (netEraseBlock(block, 1))
				log_printf(0, "Success!\n");
			else
				log_printf(0, "\n\n***** ERROR: Failed to erase block 0x%x!\n", block);
		} else
			log_printf(0, "\n\n***** ERROR: Block 0x%x is outside system area!\n", block);
	} else
		log_printf(0, "\n\n***** ERROR: Invalid arguments specified, please provide hex only for offset!\n");
}

/* the option's argument(s); dies with usage if one is missing or, with
   check, if a mode was already set */
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
			__asm__("" :: "a"(i + 1), "d"((unsigned)(i + 1) * 4));
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
			log_printf(0, "setting binary patch file to %s, offset %s\n", arg, start);
			mode = 11;
		} else if (!strnicmp(argv[i], "-rb", 3)) {
			arg = getArgs(argc, argv, &i, mode, 1, &start, &count);
			log_printf(0, "reading %s blocks to %s, starting block %s\n", count, arg, start);
			mode = 8;
		} else if (E(!strnicmp(argv[i], "-wb", 3))) {
			__asm__("" :: "c"(i));
			j = i + 1;
			a = argv[j];
			__asm__("" :: "c"(i));
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
			ip = argv[++i];
			log_printf(0, "setting forced IP to %s\n", ip);
		} else if (!strnicmp(argv[i], "-r", 2)) {
			a = argv[i + 1];
			if (i + 1 == argc || !a || *a == '-')
				client_usage(3, argv[i]);
			if (mode)
				client_usage(5, argv[i]);
			arg = argv[++i];
			log_printf(0, "setting read filename to %s\n", arg);
			mode = 1;
		} else if (!strnicmp(argv[i], "-w", 2)) {
			a = argv[i + 1];
			if (i + 1 == argc || !a || *a == '-')
				client_usage(3, argv[i]);
			if (mode)
				client_usage(5, argv[i]);
			arg = argv[++i];
			log_printf(0, "setting write filename to %s\n", arg);
			mode = 2;
		} else if (E(!strnicmp(argv[i], "-e", 2))) {
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
			client_usage(1, argv[i]);
	}
	if (!mode || ({ __asm__(""); 0; }) || !arg) {
		if (reboot) {
			if (netConnect(ip)) {
			rok: __attribute__((cold));
				cinfo = netGetInfo();
			} else
				goto fail;
		} else
			client_usage(2, NULL);
	} else {
		if (netConnect(ip)) {
			cinfo = netGetInfo();
			switch (mode) {
			case 1:
				netDumpNand(arg);
				break;
			case 2:
				clientWrite(arg);
				break;
			case 3:
				clientKeys();
				break;
			case 4:
				if (cinfo->hwFlags & 0x20)
					sendAvatarData(arg, cinfo->kernel);
				else
					log_printf(0, "\n\n***** ERROR: cannot send avatar data when a HDD does not exist!\n");
				break;
			case 5:
				if (cinfo->hwFlags & 0x20)
					sendCompatData(arg);
				else
					log_printf(0, "\n\n***** ERROR: cannot send xbox compatibility data when a HDD does not exist!\n");
				break;
			case 6:
				break;
			case 7:
				if (arg == dummy)
					clientPatches(NULL);
				else
					clientPatches(arg);
				break;
			case 8:
				clientReadBlocks(arg, start, count);
				break;
			case 9:
				clientWriteBlocks(arg, start);
				break;
			case 10:
				clientEraseBlock(arg);
				break;
			case 11:
				clientBinPatch(arg, start);
				break;
			case 12:
				if (arg == dummy)
					clientInfo(NULL);
				else
					clientInfo(arg);
				break;
			default:
				log_printf(0, "\n\n***** ERROR: invalid mode specified, please inform author\n");
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
	log_printf(0, "\n\n***** ERROR: unable to connect to xbox server\n");
	return 0;
}

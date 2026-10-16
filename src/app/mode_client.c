/* mode_client: `xeBuild client`, single commands against a console over the network.
   Mixed object: the functions here are spliced into mode_client.s
   (re/splice.py), which still holds the rest and the data, so strings
   and variables are extern names for the .s's.  wip/app/mode_client.c
   is the whole draft; wip/mcmixed.py makes this file from it. */
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

/* mode_client.s's data */
extern struct consoleinfo *cinfo;

/* strings in mode_client.s */
extern const char mc_44ebc0[];	/* "creating mydata folder output at %s\..." */
extern const char mc_44ebe8[];	/* "unable to dump details to %s, disabl..." */
extern const char mc_44ec11[];	/* "0x%x" */
extern const char mc_44ec16[];	/* "," */
extern const char mc_44ec18[];	/* "dumping console flash to %s\n" */
extern const char mc_44ec35[];	/* "success!\n" */
extern const char mc_44ec3f[];	/* "failed!\n" */
extern const char mc_44ec48[];	/* "Bad Block list  : " */
extern const char mc_44ec5b[];	/* "reading file %s..." */
extern const char mc_44ec6e[];	/* "success, read 0x%x bytes\n" */
extern const char mc_44ec88[];	/* "sending data to console...\n" */
extern const char mc_44eca4[];	/* "\n\n***** ERROR: file size should be..." */
extern const char mc_44ecec[];	/* "\n\n***** ERROR: image magic should ..." */
extern const char mc_44ed30[];	/* "\n\n***** ERROR: unable to read file..." */
extern const char mc_44ed5c[];	/* "manifest, %08x %08x %s\n" */
extern const char mc_44ed74[];	/* "item %03d: %08x %08x %s\n" */
extern const char mc_44ed8d[];	/* "checking %s (file ./%s)\n" */
extern const char mc_44eda8[];	/* "\n\n****** ERROR: unable to dump %s ..." */
extern const char mc_44ee04[];	/* "dumping valid %s to file ./%s\n" */
extern const char mc_44ee23[];	/* "./" */
extern const char mc_44eee4[];	/* "checking patch sections for glitch c..." */
extern const char mc_44ef10[];	/* "\n\n***** ERROR: patches do not cont..." */
extern const char mc_44ef50[];	/* "checking patch sections for JTAG con..." */
extern const char mc_44ef7c[];	/* "\n\n***** ERROR: patches do not cont..." */
extern const char mc_44efc8[];	/* "loaded %s size 0x%x (%d) bytes\n" */
extern const char mc_44efe8[];	/* "retrieving patches from console..." */
extern const char mc_44f00b[];	/* "patches" */
extern const char mc_44f014[];	/* "success! received 0x%x (%d) bytes\n" */
extern const char mc_44f037[];	/* "patches updated OK!\n" */
extern const char mc_44f04c[];	/* "\n\n***** ERROR: patch update failed..." */
extern const char mc_44f074[];	/* "\n\n***** ERROR: failed to retrieve ..." */
extern const char mc_44f0b8[];	/* "\n\n***** ERROR: %s exists but is 0 ..." */
extern const char mc_44f0ec[];	/* "\n\n***** ERROR: could not load %s, ..." */
extern const char mc_44f118[];	/* "sending update patches to console..." */
extern const char mc_44f140[];	/* "patches are already up to date!\n" */
extern const char mc_44f164[];	/* "Updating patches from file: %s\n" */
extern const char mc_44f184[];	/* "%d/bin/patches_%s.bin" */
extern const char mc_44f19a[];	/* "%d/bin/patches_g2%s.bin" */
extern const char mc_44f1b2[];	/* "%d/bin/patches_g2m%s.bin" */
extern const char mc_44f1cb[];	/* "%d/bin/patches_fat.bin" */
extern const char mc_44f1e4[];	/* "Updating patches in auto mode: %s\n" */
extern const char mc_44f208[];	/* "\n***** ERROR: unable to determine c..." */
extern const char mc_44f240[];	/* "Reading 0x%x (%d) blocks from consol..." */
extern const char mc_44f288[];	/* "Done!\nWriting 0x%x (%d) bytes to %s..." */
extern const char mc_44f2b0[];	/* "Done!\n" */
extern const char mc_44f2b8[];	/* "\n\n***** ERROR: Failed to write blo..." */
extern const char mc_44f2f0[];	/* "\n\n***** ERROR: Trying to read bloc..." */
extern const char mc_44f330[];	/* "\n\n***** ERROR: This read command w..." */
extern const char mc_44f384[];	/* "\n\n***** ERROR: Invalid arguments s..." */
extern const char mc_44f3f0[];	/* "Writing 0x%x (%d) blocks to console ..." */
extern const char mc_44f434[];	/* "Done! Wrote 0x%x (%d) bytes to conso..." */
extern const char mc_44f464[];	/* "\n\n***** ERROR: Writing data to con..." */
extern const char mc_44f494[];	/* "\n\n***** ERROR: File %s size (0x%x)..." */
extern const char mc_44f4e8[];	/* "\n\n***** ERROR: Unable to read file..." */
extern const char mc_44f684[];	/* "\n\n***** ERROR: Invalid arguments s..." */
extern const char mc_44f6d5[];	/* "erasing block 0x%x..." */
extern const char mc_44f6eb[];	/* "Success!\n" */
extern const char mc_44f6f8[];	/* "\n\n***** ERROR: Failed to erase blo..." */
extern const char mc_44f724[];	/* "\n\n***** ERROR: Block 0x%x is outsi..." */

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

void clientReadBlocks(const char *file, const char *sstart, const char *scount)
{
	u32 start = myatoh32(sstart, -1);
	u32 count = myatoh32(scount, -1);
	int len;
	u8 *buf;

	if (count != 0 && count != -1 && start != -1) {
		if (start + count <= cinfo->nandSize / cinfo->blockSize) {
			log_printf(0, mc_44f240, count, count, start, start);
			buf = netReadBlocks(&len, start, count);
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
			if (netWriteBlocks(buf, len, start, n))
				log_printf(0, mc_44f434, len, len);
			else
				log_printf(0, mc_44f464);
		} else
			log_printf(0, mc_44f330, cinfo->nandSize / cinfo->blockSize);
	} else
		log_printf(0, mc_44f494, file, len, cinfo->blockSize);
	free(buf);
}

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

void clientEraseBlock(const char *sblock)
{
	u32 block = myatoh32(sblock, -1);

	if (block != -1) {
		if (block < cinfo->nandSize / cinfo->blockSize) {
			log_printf(0, mc_44f6d5, block);
			if (netEraseBlock(block, 1))
				log_printf(0, mc_44f6eb);
			else
				log_printf(0, mc_44f6f8, block);
		} else
			log_printf(0, mc_44f724, block);
	} else
		log_printf(0, mc_44f684);
}

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

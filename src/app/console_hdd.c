/* console_hdd: manifest + avatar/kinect data to console HDD, remote dirs */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>

#include "../crypto/xecrypt.h"
#include "xebuild.h"
#include "console_hdd.h"
#include "fileutil.h"
#include "log.h"
#include "net.h"
#include "stfs.h"

/* TODO(prototype cast): netMount returns u32 (net.c); sendCompatData's code
   wants an int */
int netMountInt(const char *drive, const char *device) __asm__("_netMount");

#define SWAP32(x) (((x) << 24) + (((x) << 8) & 0xff0000) + (((x) >> 8) & 0xff00) + ((x) >> 24))

#define SYSEX "SSEP"

/* system.manifest, big endian */
struct mfEntry {
	u32 nameOff;		/* 00 from the header */
	u32 f04;
	u32 size;		/* 08 */
	u32 idOff;		/* 0c title id */
	u32 f10, f14;
	u32 type;		/* 18 2: stfs package, 3: file */
	u32 f1c;
	u32 pathOff;		/* 20 file name */
	u8 stfsHash[20];	/* 24 */
	u8 sha[20];		/* 38 */
	u32 contentType;	/* 4c */
	u32 titleId;		/* 50 */
	u32 f54[3];
};

struct mfHeader {
	u32 revision;		/* 00 */
	u32 len;		/* 04 hashed length */
	u32 f08, f0c;
	u32 schema;		/* 10 */
	u32 version;		/* 14 */
	u32 f18[5];
	u32 count;		/* 2c */
	struct mfEntry e[];	/* 30 */
};

struct mfFile {
	u32 magic;		/* 000 */
	u8 pad004[0x24 - 0x04];
	u8 sha[20];		/* 024 */
	u8 pad038[0x138 - 0x38];
	struct mfHeader hdr;	/* 138 */
};

static u32 errCount;
static u32 flashVer;
static u32 titleIds[48];
static u32 numTitleIds;

static const char *const sysexDirs[] = {
	"%s:\\Content",
	"%s:\\Content\\0000000000000000",
	"%s:\\Content\\0000000000000000\\FFFE07DF",
	"%s:\\Content\\0000000000000000\\FFFE07DF\\00008000",
};

int createSysexDirs(void)
{
	char path[260];
	int i;
	u8 j;

	for (i = 0; i < numTitleIds; i++) {
		sprintf(path, "%s:\\%08X", SYSEX, titleIds[i]);
		if (!netMkdir(path)) {
			log_printf(1, "ERROR: could not create dir %s on console!\n", path);
			return 0;
		}
		log_printf(1, "created dir: %s\n", path);
	}
	for (j = 0; j < 4; j++) {
		sprintf(path, sysexDirs[j], SYSEX);
		if (!netMkdir(path)) {
			log_printf(1, "ERROR: could not create dir %s on console!\n", path);
			return 0;
		}
		log_printf(1, "created dir: %s\n", path);
	}
	return 1;
}

void addTitleId(u32 id)
{
	int i;

	for (i = 0; i < numTitleIds; i++)
		if (titleIds[i] == id)
			return;
	titleIds[numTitleIds] = id;
	numTitleIds++;
}

int checkManifestHeader(struct mfFile *m)
{
	u32 v;
	u8 hash[20];
	int ret;

	if (SWAP32(m->hdr.schema) != 3) {
		log_printf(1, "manifest schema != 3!\n");
		return 0;
	}
	v = SWAP32(m->hdr.revision);
	if (v != 0x7873796D && v != 0x786F6E6D) {
		log_printf(1, "manifest revision 0x%08x != 0x786F6E6D|0x7873796D!\n", v);
		return 0;
	}
	v = SWAP32(m->magic);
	if (v != 0x584D4E50) {
		log_printf(1, "manifest magic 0x%08x != 0x584D4E50!\n", v);
		return 0;
	}
	XeCryptSha((u8 *)m + 0x138, SWAP32(m->hdr.len), 0, 0, 0, 0, hash, 20);
	ret = 1;
	if (memcmp(hash, m->sha, 20)) {
		log_printf(1, "manifest checksum failed!\n");
		ret = 0;
	}
	return ret;
}

int readManifestString(const u8 *p, char *out)
{
	int len = 0;
	u16 l = getBeU16(p);

	if (l) {
		len = l;
		memcpy(out, p + 2, len);
		out[len] = 0;
	} else
		log_printf(1, "err len = 0!\n");
	return len;
}

void *loadFileChecked(const char *path, int size, const u8 *sha)
{
	size_t len;
	u8 hash[20];
	u8 *buf, *ret = 0;

	if (size) {
		buf = FileToBuffer(path, &len);
		if (buf) {
			if (len == size) {
				XeCryptSha(buf, len, 0, 0, 0, 0, hash, 20);
				if (!memcmp(hash, sha, 20)) {
					log_printf(1, "- OK\n");
					ret = buf;
					goto out;
				}
				log_printf(1, "file corrupt, hash check FAILED!!\n");
			} else
				log_printf(1, "file size FAIL! 0x%x is not 0x%x!\n", len, size);
			free(buf);
		} else
			log_printf(1, "could not read file!\n");
	} else
		log_printf(1, "FAILED! Input len is 0!\n");
	errCount++;
out:
	return ret;
}

void *loadStfsChecked(const char *path, int size, u8 *hash)
{
	stfs_t s;

	if (size) {
		stfsInit(&s);
		if (stfsLoad(&s, path, 0, 0, 0, hash, 0)) {
			if (s.size == size) {
				log_printf(1, " - OK\n");
				return s.data;
			}
			log_printf(1, " - FAILED!\n");
			stfsFree(&s);
		}
		log_printf(1, " - FAILED!\n");
	} else
		log_printf(1, " - FAILED! input len is 0!\n");
	errCount++;
	return 0;
}

void parseManifestEntries(const char *dir, struct mfHeader *h, u32 len, u32 ver)
{
	char name[512];
	char path[1024];
	struct mfEntry *e;
	u32 i, id, type;

	log_printf(1, "parsing %d entries in system.manifest\n", SWAP32(h->count));
	for (i = 0; i < SWAP32(h->count) && manifest.count < 256; i++) {
		e = &h->e[i];
		id = SWAP32(e->idOff);
		if (id)
			id = getBeU32((u8 *)h + id);
		if (!e->nameOff)
			continue;
		readManifestString((u8 *)h + SWAP32(e->nameOff), name);
		if (strcmp(name, "flash")) {
			strcpy(path, dir);
			strcat(path, name);
			log_printf(1, "%03d: %s ", manifest.count + 1, path);
			readManifestString((u8 *)h + SWAP32(e->pathOff), name);
			switch (SWAP32(e->type)) {
			case 2:
				manifest.e[manifest.count].data = loadStfsChecked(path, SWAP32(e->size), e->stfsHash);
				if (manifest.e[manifest.count].data) {
					manifest.e[manifest.count].len = SWAP32(e->size);
					sprintf(manifest.e[manifest.count].path, "%s:\\%s%08X\\%08X\\%s", SYSEX,
						"Content\\0000000000000000\\", SWAP32(e->titleId),
						SWAP32(e->contentType), name);
					manifest.count++;
				}
				break;
			case 3:
				manifest.e[manifest.count].data = loadFileChecked(path, SWAP32(e->size), e->sha);
				if (manifest.e[manifest.count].data) {
					manifest.e[manifest.count].len = SWAP32(e->size);
					sprintf(manifest.e[manifest.count].path, "%s:\\%08X\\%s", SYSEX, id, name);
					if (id != ver)
						addTitleId(id);
					manifest.count++;
				}
			}
		}
		if (errCount)
			return;
	}
}

u32 parseManifest(const char *dir, struct mfFile *m, u32 len, int ver)
{
	if (len < 0x164 || len > 0x10000) {
		log_printf(1, "manifest size error! len 0x%x\n", len);
		return 0;
	}
	if (checkManifestHeader(m)) {
		flashVer = SWAP32(m->hdr.version);
		log_printf(1, "header ok!\nManifest flash version: %d.%d.%d.%d\n", flashVer >> 28,
			(flashVer >> 24) & 0xf, (u16)(flashVer >> 8), flashVer & 0xf);
		if (flashVer != ver) {
			log_printf(0, "\n\n***** ERROR: this system extended data is not the correct version!\n");
			return 0;
		}
		parseManifestEntries(dir, &m->hdr, len - 0x138, ver);
		if (errCount) {
			log_printf(0, "\n\n***** ERROR: loading manifest content encountered problems!\n");
			return 0;
		}
		log_printf(1, "found %d items to send to xbox!\n", manifest.count);
		return 1;
	}
	log_printf(1, "manifest header check failed!\n");
	return 0;
}

void freeManifest(void)
{
	int i;

	if (manifest.data)
		free(manifest.data);
	for (i = 0; i < manifest.count; i++) {
		if (manifest.e[i].data)
			free(manifest.e[i].data);
		manifest.e[i].data = 0;
		manifest.e[i].len = 0;
	}
}

int loadManifest(const char *dir, u32 ver)
{
	char base[1024];
	char path[1024];
	int ret;

	strcpy(path, dir);
	strcpy(base, path);
	strcat(path, "system.manifest");
	memset(&manifest, 0, sizeof(manifest));
	if (!FileExists(path)) {
		log_printf(1, "manifest not found at %s\n", path);
		strcat(base, "$SystemUpdate/");
		strcpy(path, base);
		strcat(path, "system.manifest");
		if (!FileExists(path)) {
			log_printf(1, "manifest not found at %s\n", path);
			log_printf(0, "***** WARNING: could not find manifest data for sysex!\n");
			return 0;
		}
	}
	log_printf(1, "loading manifest %s\n", path);
	manifest.data = FileToBuffer(path, &manifest.size);
	if (!manifest.data || !manifest.size) {
		log_printf(0, "***** WARNING: could not read manifest data for sysex!\n");
		return 0;
	}
	log_printf(1, "loaded system.manifest, 0x%x bytes\n", manifest.size);
	ret = parseManifest(base, manifest.data, manifest.size, ver);
	sprintf(manifest.path, "%s:\\system.manifest", SYSEX);
	if (!ret)
		freeManifest();
	return ret;
}

int prepSysex(void)
{
	if (netFormatSysex()) {
		/* hint: makes the mount failure cold where sendAvatarData inlines this */
		if (__builtin_expect(netMountInt(SYSEX, "\\SEP"), 1))
			return createSysexDirs();
		log_printf(0, "ERROR: unable to mount sysex partition!\n");
	} else
		log_printf(0, "ERROR: unable to format sysex partition!\n");
	return 0;
}

/* long, not int: uncprop then can't reuse the int netSendFile result for the
   manifest failure's 0 (it does for the loop failure, which assigns ret) */
long sendAvatarData(const char *dir, u32 ver)
{
	int i;
	u32 k;
	long ret;

	netTimerStart();
	log_printf(0, "loading avatar data...\n");
	ver &= ~0xf;
	addTitleId(ver);
	if (loadManifest(dir, ver)) {
		log_printf(0, "success!\nFormatting HDD partition...\n");
		ret = 1;
		if (prepSysex()) {
			log_printf(0, "success!\nSending avatar files to HDD partition...\n");
			log_printf(1, "sending %d items to xbox\n", manifest.count);
			/* hint: expands this literal before the loop's, for its .rdata
			   order (no code) */
			__asm__("" :: "i"("sending manifest to %s\n"));
			if (manifest.count > 0) {
				i = 0;
				do {
					/* hint: hides k from scev, so ivopts keeps the
					   imul instead of a pointer IV (no code) */
					k = (u32)__builtin_assume_aligned((void *)i, 1);
					log_printf(1, "sending %03d: 0x%08x (%d) bytes, %s\n", i + 1, manifest.e[k].len,
						manifest.e[k].len, manifest.e[k].path);
					ret = netSendFile(manifest.e[k].path, manifest.e[k].data, manifest.e[k].len);
					if (__builtin_expect(!ret, 0)) {
						log_printf(0, "aborting sending avatar data, failed to send %s\n", manifest.e[k].path);
						goto out;
					}
				} while (++i < manifest.count);
				/* hint: i live here stops ifcvt hoisting i = 0 above the guard */
				__asm__("" :: "r"(i));
			}
			log_printf(1, "sending manifest to %s\n", manifest.path);
			if (!netSendFile(manifest.path, manifest.data, manifest.size)) {
				ret = 0;
				log_printf(0, "aborting sending avatar data, failed to send %s\n", manifest.path);
			} else {
				log_printf(0, "success! Avatar data is successfully sent to the console!\n");
				netTimerEnd();
				ret = 1;
			}
		}
out:
		netUnmount(SYSEX);
		freeManifest();
	} else {
		log_printf(0, "***** WARNING: avatar data skipped, unable to load data!\n");
		ret = 1;
	}
	return ret;
}

int sendDir(const char *src, const char *dst)
{
	char dstPath[260];
	char pattern[1024];
	char srcPath[1024];
	struct stat st;
	size_t len;
	DIR *d;
	struct dirent *de;
	u8 *buf;

	strcpy(pattern, src);
	strcat(pattern, "//");
	d = opendir(pattern);
	if (!d)
		goto fail;
	while ((de = readdir(d))) {
		strcpy(dstPath, dst);
		strcat(dstPath, "\\");
		strcat(dstPath, de->d_name);
		strcpy(srcPath, src);
		strcat(srcPath, "\\");
		strcat(srcPath, de->d_name);
		if (stat(srcPath, &st) < 0)
			continue;
		if (st.st_mode & S_IFDIR) {
			if (de->d_name[0] == '.')
				continue;
			log_printf(1, "creating directory %s...", dstPath);
			if (!netMkdir(dstPath)) {
				log_printf(1, "FAILED!\n");
				closedir(d);
				goto fail;
			}
			log_printf(1, "success!\n");
			sendDir(srcPath, dstPath);
		} else if (st.st_mode & S_IFREG) {
			log_printf(1, "reading file from %s...", srcPath);
			buf = FileToBuffer(srcPath, &len);
			if (!buf)
				continue;
			log_printf(1, "OK! read 0x%x (%d) bytes!\n", len, len);
			log_printf(1, "    sending file %s...\n", dstPath);
			if (!netSendFile(dstPath, buf, len)) {
				free(buf);
				log_printf(1, "FAILED sending file %s!\n", dstPath);
				closedir(d);
				goto fail;
			}
			log_printf(1, "    sent 0x%x bytes to file %s OK!\n", len, dstPath);
			free(buf);
		}
	}
	closedir(d);
	return 1;
fail:
	/* no code on i686; keeps this a block of its own until RTL, where
	   cross-jumping shares its xor with the failure paths as in the original */
	__builtin_prefetch(0);
	return 0;
}

u32 sendCompatData(const char *dir)
{
	int ret;

	if (FileExistsIn(dir, "index")) {
		log_printf(0, "formatting compatibility partition...");
		if (netFormatCompat()) {
			log_printf(0, "success!\n");
			if (netMountInt("XCOM", "\\Device\\Harddisk0\\SystemPartition")) {
				if (sendDir(dir, "XCOM:")) {
					ret = 1;
					log_printf(0, "sent files to partition OK!\n");
				} else {
					ret = 0;
					log_printf(0, "\n\n***** ERROR: Sending files to compatibility partition failed!\n");
				}
				netUnmount("XCOM");
				return ret;
			}
			log_printf(0, "\n\n***** ERROR: unable to mount compatibility partition!\n");
		} else
			log_printf(0, "\n\n***** ERROR: unable to format compatibility partition!\n");
	} else
		log_printf(0, "\n\n***** WARNING: compatibility data skipped, unable to find index!\n");
	return 0;
}

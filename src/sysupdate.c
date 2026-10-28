/* sysupdate: system update container, xboxupd.bin (CF/CG) extraction */
#include <stdlib.h>
#include <string.h>

#include "xebuild.h"
#include "bootloaders.h"
#include "fileutil.h"
#include "log.h"
#include "stfs.h"
#include "sysupdate.h"

/* TODO(prototype cast): FileExists read as uint32_t, not int: with an int, gcc
   returns FileExists' 0 instead of a fresh xor in suLoad/suLoadDir's failure
   paths (stfs.c's stfsLoad needs the int) */
uint32_t FileExistsU32(const char *name) __asm__("_FileExists");


#define SWAP32(x) (((x) << 24) + (((x) << 8) & 0xff0000) + (((x) >> 8) & 0xff00) + ((x) >> 24))

static char suPath[1024];
static char suDir[1024];
static stfs_t su;
static int suLoaded;
static uint8_t *cf;
static uint8_t *cg;
static uint32_t cfLen;
static uint32_t cgLen;

const char *suGetPath(void)
{
	return suLoaded ? suPath : 0;
}

const char *suGetDir(void)
{
	return suLoaded ? suDir : 0;
}

void suFreeBl(void)
{
	cfLen = 0;
	cgLen = 0;
	if (cf) {
		free(cf);
		cf = 0;
	}
	if (cg) {
		free(cg);
		cg = 0;
	}
}

void suExtractBl(void)
{
	uint8_t *data;
	uint32_t len, size, cgSize;
	uint16_t magic;
	int ver;

	if (suGetFile("xboxupd.bin", &data, &len)) {
		log_printf(1, "extracted SUPD/xboxupd.bin (0x%x bytes)\n", len);
		magic = getBeU16(data);
		ver = getBeU16(data + 2);
		size = getBeU32(data + 12);
		cfLen = (size + 15) & ~15;
		if (magic == 0x4346) {
			cf = calloc(cfLen, 1);
			if (cf) {
				log_printf(1, "decrypting SUPD/xboxupd.bin/%c%c_%d.bin (0x%x bytes)...", data[0], data[1], ver, cfLen);
				memcpy(cf, data, size);
				if (cfDecrypt(cf, size)) {
					log_printf(1, "done!\n");
					magic = getBeU16(data + size);
					ver = getBeU16(data + size + 2);
					cgSize = getBeU32(data + size + 12);
					cgLen = (cgSize + 15) & ~15;
					if (magic == 0x4347) {
						cg = calloc(cgLen, 1);
						if (cg) {
							memcpy(cg, data + size, cgSize);
							log_printf(1, "decrypting SUPD/xboxupd.bin/%c%c_%d.bin (0x%x bytes)...", data[size], data[size + 1], ver, cgSize);
							if (cgDecrypt(cg, cf + 0x330, cgSize)) {
								log_printf(1, "done!\n");
								return;
							}
							log_printf(1, "failed!\n");
						}
					}
				} else
					log_printf(1, "failed!\n");
			}
		}
	} else
		log_printf(0, "***** ERROR: xboxupd.bin not found in SU container!\n");
	suFreeBl();
}

int suGetCF(uint8_t **data, uint32_t *len)
{
	if (!cf || !cfLen)
		return 0;
	log_printf(1, "extracted SUPD/xboxupd.bin/%c%c_%d.bin (0x%x bytes)\n", cf[0], cf[1], getBeU16(cf + 2), getBeU32(cf + 12));
	*data = cf;
	cf = 0;
	*len = cfLen;
	return 1;
}

int suGetCG(uint8_t **data, uint32_t *len)
{
	if (!cg || !cgLen)
		return 0;
	log_printf(1, "extracted SUPD/xboxupd.bin/%c%c_%d.bin (0x%x bytes)\n", cg[0], cg[1], getBeU16(cg + 2), getBeU32(cg + 12));
	*data = cg;
	cg = 0;
	*len = cgLen;
	return 1;
}

int suGetFile(const char *name, uint8_t **data, uint32_t *len)
{
	if (!suLoaded)
		return 0;
	if (!stfsGetFile(&su, name, data, len)) {
		char buf[40] = "$flash_";

		strncat(buf, name, 40);
		return stfsGetFile(&su, buf, data, len);
	}
	return 1;
}

int suNextFile(char *name, int *idx)
{
	if (!suLoaded || *idx == -1)
		return 0;
	if (checkZeros(su.fileTable + *idx * 64, 64)) {
		*idx = -1;
		return 0;
	}
	memcpy(name, su.fileTable + *idx * 64, 40);
	*(uint32_t *)(name + 40) = SWAP32(*(uint32_t *)(su.fileTable + *idx * 64 + 52));
	(*idx)++;
	return 1;
}

int suFirstFile(char *name, int *idx)
{
	if (!suLoaded)
		return 0;
	*idx = 0;
	return suNextFile(name, idx);
}

int suLoadDir(const char *dir)
{
	int found;

	strcpy(suPath, dir);
	strcpy(suDir, dir);
	strcat(suPath, "su20076000_00000000");
	found = FileExistsU32(suPath);
	log_printf(1, "\n------ loading system update container ------\n");
	if (!found) {
		log_printf(1, "system update container not found at %s, trying alt\n", suPath);
		strcpy(suPath, dir);
		strcat(suPath, "$SystemUpdate/");
		strcpy(suDir, suPath);
		strcat(suPath, "su20076000_00000000");
		found = FileExistsU32(suPath);
	}
	if (found) {
		stfsInit(&su);
		if (stfsLoad(&su, suPath, 0x53555044, 0xb0000, 0xfffe07d1, 0, 1)) {
			suLoaded = 1;
			suExtractBl();
			return 1;
		}
	} else
		log_printf(1, "system update container not found at %s, skipping load\n", suPath);
	return 0;
}

int suLoad(const char *path)
{
	char *p;
	int found;

	strcpy(suPath, path);
	strcpy(suDir, suPath);
	found = FileExistsU32(suPath);
	if (!found) {
		if (suPath[strlen(path) - 1] != '\\')
			if (suPath[strlen(path) - 1] != '/')
				strcat(suPath, "/");
		strcpy(suDir, suPath);
		strcat(suPath, "su20076000_00000000");
		found = FileExistsU32(suPath);
		if (!found) {
			strcat(suDir, "$SystemUpdate/");
			strcpy(suPath, suDir);
			strcat(suPath, "su20076000_00000000");
			found = FileExistsU32(suPath);
		}
	} else {
		p = strrchr(suDir, '/');
		if (!p)
			p = strrchr(suDir, '\\');
		if (p)
			p[1] = 0;
	}
	if (found) {
		log_printf(0, "\n------ loading system update container ------\n");
		log_printf(0, "SU container found! Loading '%s'\n", suPath);
		stfsInit(&su);
		if (stfsLoad(&su, suPath, 0x53555044, 0xb0000, 0xfffe07d1, 0, 1)) {
			suLoaded = 1;
			suExtractBl();
			return 1;
		}
		log_printf(0, "\n***** ERROR could not load container '%s'!\n", suPath);
	} else
		log_printf(1, "system update container not found at or near %s!!\n", path);
	return 0;
}

void suFree(void)
{
	suFreeBl();
	suLoaded = 0;
	stfsFree(&su);
}

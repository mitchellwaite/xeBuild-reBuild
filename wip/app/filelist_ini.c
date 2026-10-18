#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <dirent.h>

typedef unsigned char u8;

typedef unsigned int u32;

struct fileent {
	char name[0x400];
	u32 crc;			/* 400 */
	int type;			/* 404 */
	u32 offset;			/* 408 */
	u8 pad40c[0x42c - 0x40c];
};
struct xebuild {
	int mode;			/* 000 */
	u32 flags;			/* 004 */
	u32 type;			/* 008 */
	u32 kernel;			/* 00c */
	int glitch2;			/* 010 */
	int glitch2mfg;			/* 014 */
	int cbb;			/* 018 build with a CB_B */
	u8 pad01c[0x2ac - 0x01c];
	char suffix[0x400];		/* 2ac -i */
	char binDir[0x400];		/* 6ac */
	char outName[0x400];		/* aac */
	char baseDir[0x400];		/* eac */
	char dataDir[0x400];		/* 12ac */
	char commonDir[0x400];		/* 16ac */
	char firmware[256][0x400];	/* 1aac the ini's firmware files */
	u32 firmwareCrc[256];		/* 41aac */
	u32 nFirmware;			/* 41eac */
	struct fileent files[35];	/* 41eb0 */
	char blSuffix[0x40];		/* 4b0b4 -r */
	int nAddons;			/* 4b0f4 */
	int nFiles;			/* 4b0f8 */
	int nFlashFiles;		/* 4b0fc */
	struct {
		char name[0x400];
		u32 offset;
	} rawPatch[16];			/* 4b100 */
	u32 nRawPatches;		/* 4f140 */
	char flashFiles[10][22];	/* 4f144 security files */
	u8 *flashBuf[10];		/* 4f220 */
	u32 flashSize[10];		/* 4f248 */
	u32 oddTime[10];		/* 4f270 */
	u32 flashCrc[10];		/* 4f298 */
	u32 nFlashFiles2;		/* 4f2c0 the security file count */
	u8 pad4f2c4[0x4f4c4 - 0x4f2c4];
	char kernelStr[0x40];		/* 4f4c4 the ini's kernel version string */
};
extern struct xebuild xb;
extern unsigned char *iniBuf;
extern int iniSize;
extern char fnSmc[32], fnKv[32], fnPatches[32];

void log_printf(int level, const char *fmt, ...);
long getFileSize(FILE *f);
char myatol(char c);
int validateString(char *s);
unsigned int myatou32(char *dat, unsigned int def);
u32 myatox32(char *dat, u32 def);
void fixFileCase(void);
int memFindStr(unsigned char *buf, int size, const char *key, int label);
int memFindChar(unsigned char *buf, char c, int size);

/* .data: {offset, type} per file for each build type, the bl section's file
   order, and the file names */
struct fileloc { u32 offset; int type; };
extern struct fileloc locRetail[], locDevgl[], locTestk[], locDevk[], locJtag[];
extern int blJtag[], blDevgl[], blTestk[], blDevk[], blRetail[];
extern char fnNone[32], fnKvAlt[32], fnXellGg[32], fnXell2f[32], fnSmcConfig[32],
	fnFreeboot[32], fnFuses[32], fnPayload[32];
int *blOrder;
static const char *const consoleNames[] = {
	"xenon", "zephyr", "falcon", "jasper", "trinity", "corona", "winchester"
};

const unsigned char validChars[74] = {
	'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
	'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
	'0','1','2','3','4','5','6','7','8','9','.', ',', ';', '[', ']', '_', '\n', '\\', '/', '-', '$', ':'
};

/* fix the case of the file names in the base dir that need it */
__attribute__((optimize("ira-region=one")))
void fixFileCase(void)
{
	char dir[1024], path[1024];
	struct stat st;
	DIR *d;
	struct dirent *de;

	strcpy(dir, xb.baseDir);
	d = opendir(dir);
	if (d == NULL)
		return;
	while ((de = readdir(d)) != NULL) {
		strcpy(path, dir);
		strcat(path, de->d_name);
		if (stat(path, &st) < 0)
			continue;
		if (stricmp(de->d_name, fnSmc) == 0)
			strcpy(fnSmc, de->d_name);
		else if (stricmp(de->d_name, fnKv) == 0)
			strcpy(fnKv, de->d_name);
		else if (stricmp(de->d_name, fnPatches) == 0)
			strcpy(fnPatches, de->d_name);
	}
	closedir(d);
}

/* strip comments and invalid characters; returns the new size */
int iniPreParse(unsigned char *buf, int size)
{
	unsigned char *tmp;
	int i, j, n = size;

	tmp = malloc(size + 1);
	memcpy(tmp, buf, size + 1);
	/* remove comments */
	for (i = 0; i < n; i++) {
		if (buf[i] == ';') {
			i++;
			for (j = 0; buf[i + j] != 0xff && buf[i + j] != '\n' && i + j < n; j++)
				;
			if (n - i - j > 0) {
				memcpy(&buf[i], &tmp[i + j], n - i - j);
				n -= j;
				memcpy(tmp, buf, size + 1);
				i--;
			}
		}
	}
	/* invalid characters to spaces */
	for (i = 0; i < n; i++) {
		for (j = 0; j < (int)sizeof(validChars); j++)
			if ((char)buf[i] == (char)validChars[j])
				break;
		if (j == sizeof(validChars))
			buf[i] = ' ';
	}
	/* a ';' at the start or end of a line */
	for (i = 0; i < n; i++)
		if (buf[i] == ';') {
			if (i == 0)
				buf[i] = ' ';
			else if (buf[i - 1] == '\n' || buf[i + 1] == '\n')
				buf[i] = ' ';
		}
	memcpy(tmp, buf, size + 1);
	/* remove spaces */
	for (i = 0; i < n; i++) {
		if (buf[i] == ' ') {
			memcpy(&buf[i], &tmp[i + 1], n - i - 1);
			n--;
			memcpy(tmp, buf, size + 1);
			i--;
		}
	}
	/* lines to strings */
	for (i = 0; i < n; i++)
		if (buf[i] == '\n' || buf[i] == ';')
			buf[i] = 0;
	memcpy(tmp, buf, size + 1);
	/* remove empty lines */
	for (i = 0; i < n; i++) {
		if (buf[i] == 0 && buf[i + 1] == 0) {
			memcpy(&buf[i], &tmp[i + 1], n - i - 1);
			n--;
			memcpy(tmp, buf, size + 1);
			i--;
		}
	}
	if (n <= size) {
		buf[n] = 0;
		n++;
	}
	return n;
}

void checkFileCase(void);

/* read the file list ini: the files for this build type, the bootloaders'
   names and crcs, [rawpatch], [flashfs] and [security] */
int parseIni(char *path)
{
	FILE *f;
	unsigned char *buf, *p;
	int size, off, end, pos, len, nul, comma, n, i, nbl, noCrc;
	struct fileloc *loc;
	struct fileent *e;
	char *name, *s;
	u32 crc;
	char label[50];
	char tmp[0x400];

	log_printf(1, "\n------ parsing ini at '%s' ------\n", path);
	f = fopen(path, "rb");
	if (f == NULL) {
		log_printf(0, "\n******* ERROR: could not open '%s'\n", path);
		return 0;
	}
	size = getFileSize(f);
	buf = malloc(size + 1);
	if (buf == NULL) {
		log_printf(0, "******* ERROR loading %s, unable to allocate memory\n", path);
		return 0;
	}
	fread(buf, size, 1, f);
	fclose(f);
	if (buf[0] == 0xff || buf[1] == 0xff) {
		log_printf(0, "\n\n***** ERROR: File descriptor ini %s\nappears to be a multi byte file, not an ascii only file!\n", path);
		goto fail;
	}
	buf[size] = 0xff;
	size = iniPreParse(buf, size);
	buf[size] = 0;

	/* [version] */
	off = memFindStr(buf, size, "[version]", 1);
	if (off == -1) {
		log_printf(0, "\n******* ERROR: could not find label [version] in file list ini\n");
		goto fail;
	}
	memset(xb.kernelStr, 0, sizeof(xb.kernelStr));
	len = memFindChar(&buf[off], 0, sizeof(xb.kernelStr));
	if (len == -1)
		len = sizeof(xb.kernelStr) - 1;
	strncpy(xb.kernelStr, (char *)&buf[off], len);
	log_printf(1, "ini version %s\n", xb.kernelStr);
	if (xb.type == 2) {
		xb.nFiles = 19;
		blOrder = blJtag;
		nbl = 9;
		sprintf(tmp, "%s_jtag_%s.bin", xb.kernelStr, xb.outName);
	} else {
		if (xb.type == 6 || xb.type == 7) {
			xb.nFiles = 11;
			blOrder = blDevk;
			s = "%s_devk_%s.bin";
		} else if (xb.type == 8 || xb.type == 9) {
			xb.nFiles = 12;
			blOrder = blTestk;
			s = "%s_testk_%s.bin";
		} else {
			xb.nFiles = 14;
			if (xb.type == 4 || xb.type == 5) {
				blOrder = blDevgl;
				s = "%s_devgl_%s.bin";
			} else {
				blOrder = blRetail;
				if (xb.type == 1)
					s = "%s_retail_%s.bin";
				else if (xb.glitch2mfg)
					s = "%s_g2m_%s.bin";
				else if (xb.glitch2)
					s = "%s_g2_%s.bin";
				else
					s = "%s_gg_%s.bin";
			}
		}
		nbl = 6;
		sprintf(tmp, s, xb.kernelStr, xb.outName);
	}
	xb.nFlashFiles = xb.nFiles - 2;
	strcpy(xb.outName, tmp);
	checkFileCase();

	/* the files this build type uses */
	for (i = 0; i < xb.nFiles; i++) {
		e = &xb.files[i];
		if (xb.type == 2)
			loc = locJtag;
		else if (xb.type == 6 || xb.type == 7)
			loc = locDevk;
		else if (xb.type == 4 || xb.type == 5)
			loc = locDevgl;
		else if (xb.type == 8 || xb.type == 9)
			loc = locTestk;
		else
			loc = locRetail;
		e->type = loc[i].type;
		e->offset = loc[i].offset;
		switch (e->type) {
		case 0:
		case 26:
			strcpy(e->name, fnNone);
			break;
		case 1:
			strcpy(e->name, fnPayload);
			break;
		case 2:
			strcpy(e->name, fnSmc);
			break;
		case 3:
			strcpy(e->name, fnKv);
			break;
		case 4:
			strcpy(e->name, fnKvAlt);
			break;
		case 22:
			strcpy(e->name, fnFreeboot);
			break;
		case 23:
			strcpy(e->name, fnPatches);
			if (xb.type == 2)
				strcat(e->name, consoleNames[xb.flags & 7]);
			else if (xb.glitch2) {
				if (xb.glitch2mfg)
					strcat(e->name, "g2m");
				else
					strcat(e->name, "g2");
				strcat(e->name, consoleNames[xb.flags & 7]);
			} else if (xb.type == 4 || xb.type == 5) {
				strcat(e->name, "g2m");
				strcat(e->name, consoleNames[xb.flags & 7]);
			} else {
				switch (xb.flags & 7) {
				case 5:
					strcat(e->name, "trinity");
					break;
				case 6:
					strcat(e->name, "corona");
					break;
				case 7:
					strcat(e->name, "winchester");
					break;
				default:
					strcat(e->name, "fat");
					break;
				}
			}
			strcat(e->name, xb.suffix);
			if (xb.blSuffix[0])
				strcat(e->name, xb.blSuffix);
			strcat(e->name, ".bin");
			break;
		case 24:
			strcpy(e->name, fnFuses);
			break;
		case 25:
			if (xb.type == 2)
				strcpy(e->name, fnXell2f);
			else
				strcpy(e->name, fnXellGg);
			break;
		case 27:
			strcpy(e->name, fnSmcConfig);
			break;
		}
	}

	/* [<console>bl<blSuffix>]: the bootloaders' names and crcs */
	if (xb.blSuffix[0])
		sprintf(label, "[%sbl%s]", consoleNames[xb.flags & 7], xb.blSuffix);
	else
		sprintf(label, "[%sbl]", consoleNames[xb.flags & 7]);
	off = memFindStr(buf, size, label, 1);
	if (off == -1) {
		log_printf(0, "\n******* ERROR: could not find label %s in file list ini\n", label);
		goto fail;
	}
	log_printf(1, "\nini: label %s found\n", label);
	end = off + memFindChar(&buf[off], '[', size - off);
	pos = off;
	for (i = 0; i < nbl; ) {
		p = &buf[pos];
		comma = memFindChar(p, ',', size - pos);
		nul = memFindChar(p, 0, size - pos);
		if (nul == -1 || comma == -1) {
			log_printf(0, "\n******* ERROR: ini problem, error in %s section!\n", label);
			goto fail;
		}
		noCrc = 1;
		if (comma > nul)
			len = nul;
		else {
			len = comma;
			noCrc = 0;
		}
		e = &xb.files[blOrder[i]];
		strncpy(e->name, (char *)p, len);
		e->name[len] = 0;
		pos += len + 1;
		if (noCrc)
			e->crc = 0;
		else {
			n = memFindChar(&buf[pos], 0, size - pos);
			if (n == 0)
				e->crc = 0;
			else if (n != 8) {
				log_printf(0, "\n******* ERROR: crc data for file '%s' in ini is incorrect size!\n", e->name);
				goto fail;
			} else {
				strncpy(tmp, (char *)&buf[pos], 8);
				tmp[8] = 0;
				e->crc = myatox32(tmp, 0);
			}
			pos += n + 1;
		}
		i++;
		log_printf(1, "found (%d) '%s' crc: 0x%08x\n", i, e->name, e->crc);
		if (pos > end) {
			log_printf(0, "\n******* ERROR: ini problem, can't find enough data for %s section!\n", label);
			goto fail;
		}
	}
	if (xb.type != 2 && xb.type <= 5) {
		if (strnicmp(xb.files[4].name, "none", 4) == 0)
			xb.cbb = 0;
		else {
			log_printf(1, "ini dictates dual CB for this model\n");
			xb.cbb = 1;
		}
	}

	/* [rawpatch]: name,offset */
	off = memFindStr(buf, size, "[rawpatch]", 1);
	if (off == -1)
		log_printf(1, "\n[rawpatch] label not found in ini\n");
	else {
		end = off + memFindChar(&buf[off], '[', size - off);
		log_printf(1, "\nini: label [rawpatch] found\n");
		pos = off;
		for (i = xb.nRawPatches; i < 16; i++) {
			p = &buf[pos];
			nul = memFindChar(p, 0, size - pos);
			comma = memFindChar(p, ',', size - pos);
			if (comma == -1 || comma >= nul) {
				log_printf(0, "\n******* ERROR: an entry in [rawpatch] is missing offset info!\n");
				goto fail;
			}
			if (comma > 1023) {
				log_printf(0, "\n******* ERROR: file name in [rawpatch] is too long!\n");
				goto fail;
			}
			name = xb.rawPatch[i].name;
			strncpy(name, (char *)p, comma);
			name[comma] = 0;
			pos += comma + 1;
			n = memFindChar(&buf[pos], 0, size - pos);
			if (n == 0 || n > 10) {
				log_printf(0, "\n******* ERROR: offset data for file '%s' is either too large or too small!\n", name);
				goto fail;
			}
			strncpy(tmp, (char *)&buf[pos], n);
			tmp[n] = 0;
			pos += n + 1;
			xb.rawPatch[i].offset = myatou32(tmp, -1);
			if (xb.rawPatch[i].offset == (u32)-1) {
				log_printf(1, "***** ERROR: [rawpatch] '%s' length is unintelligible!\n", name);
				goto fail;
			}
			log_printf(1, "found (%d) '%s' offset: 0x%08x\n", ++xb.nRawPatches, name, xb.rawPatch[i].offset);
			if (pos >= end)
				break;
		}
		if (pos < end) {
			log_printf(0, "\n******* ERROR: %d of %d [rawpatch] slots are already full!\n", xb.nRawPatches, 16);
			goto fail;
		}
	}

	/* [flashfs]: name[,crc]; a trailing 1 or 2 on the name is dropped */
	off = memFindStr(buf, size, "[flashfs]", 1);
	if (off == -1)
		goto noFlashfs;
	xb.nFirmware = 0;
	log_printf(1, "\nini: label [flashfs] found\n");
	pos = off;
	for (i = 0; i < 256; i++) {
		p = &buf[pos];
		nul = memFindChar(p, 0, size - pos);
		comma = memFindChar(p, ',', size - pos);
		noCrc = 1;
		len = nul;
		if (comma >= 0 && comma < nul) {
			len = comma;
			noCrc = 0;
		}
		if (len > 1023) {
			log_printf(0, "\n******* ERROR: file in [flashfs] has greater than %d chars in it's path!\n", 1023);
			goto fail;
		}
		name = xb.firmware[i];
		strncpy(name, (char *)p, len);
		name[len] = 0;
		if (len > 21) {
			s = strrchr(name, '/');
			if (s == NULL)
				s = strrchr(name, '\\');
			s = s ? s + 1 : name;
			if (strlen(s) > 21) {
				log_printf(0, "\n******* ERROR: file in [flashfs] has greater than %d chars in it's name!\n", 21);
				log_printf(0, "\n        Line: %s\n", name);
				goto fail;
			}
		}
		pos += len + 1;
		if (name[len - 1] == '1' || name[len - 1] == '2')
			name[len - 1] = 0;
		if (noCrc)
			crc = xb.firmwareCrc[i] = 0;
		else {
			n = memFindChar(&buf[pos], 0, size - pos);
			if (n == 0)
				crc = xb.firmwareCrc[i] = 0;
			else if (n != 8) {
				log_printf(0, "\n******* ERROR: crc data for file '%s' in ini is incorrect size!\n", name);
				goto fail;
			} else {
				strncpy(tmp, (char *)&buf[pos], 8);
				tmp[8] = 0;
				crc = xb.firmwareCrc[i] = myatox32(tmp, 0);
			}
			pos += n + 1;
		}
		log_printf(1, "found (%d) '%s' crc: 0x%08x\n", ++xb.nFirmware, name, crc);
		if (pos >= size)
			break;
	}

	/* [security]: name[,crc] */
	off = memFindStr(buf, size, "[security]", 1);
	if (off == -1) {
noFlashfs:
		log_printf(0, "\n******* ERROR: could not find label [flashfs] in file list ini\n");
		goto fail;
	}
	xb.nFlashFiles2 = 0;
	log_printf(1, "\nini: label [security] found\n");
	end = off + memFindChar(&buf[off], '[', size - off);
	pos = off;
	for (i = 0; i < 10; i++) {
		p = &buf[pos];
		comma = memFindChar(p, ',', size - pos);
		nul = memFindChar(p, 0, size - pos);
		noCrc = comma > nul;
		len = noCrc ? nul : comma;
		if (len > 21) {
			log_printf(0, "\n******* ERROR: file in [security] has greater than %d chars in it's name!\n", 21);
			goto fail;
		}
		name = xb.flashFiles[i];
		strncpy(name, (char *)p, len);
		name[len] = 0;
		pos += len + 1;
		if (noCrc)
			crc = xb.flashCrc[i] = 0;
		else {
			n = memFindChar(&buf[pos], 0, size - pos);
			if (n == 0)
				crc = xb.flashCrc[i] = 0;
			else if (n != 8) {
				/* sic: names the [flashfs] file */
				log_printf(0, "\n******* ERROR: crc data for file '%s' in ini is incorrect size!\n", xb.firmware[i]);
				goto fail;
			} else {
				strncpy(tmp, (char *)&buf[pos], 8);
				tmp[8] = 0;
				crc = xb.flashCrc[i] = myatox32(tmp, 0);
			}
			pos += n + 1;
		}
		log_printf(1, "found (%d) '%s' crc: 0x%08x\n", ++xb.nFlashFiles2, name, crc);
		if (pos >= end)
			break;
	}
	free(buf);
	log_printf(1, "------ ini parsing completed ------\n\n");
	return 1;
fail:
	free(buf);
	return 0;
}

int memFindStr(unsigned char *buf, int size, const char *key, int label)
{
	int i, j, len;

	len = strlen(key);
	for (i = 0; i < size - len; i++) {
		if (key[0] == buf[i]) {
			for (j = 0; j < len; j++)
				if (buf[i + j] != key[j])
					j = len + 1;
			if (j == len) {
				if (label) {
					if (buf[i + len] == 0)
						return i + len + 1;
					return i + len;
				}
				if (buf[i + len] != 0)
					return i + len;
			}
		}
	}
	return -1;
}

int memFindChar(unsigned char *buf, char c, int size)
{
	int i;

	for (i = 0; i < size; i++)
		if (buf[i] == c)
			return i;
	return -1;
}

void checkFileCase(void)
{
	if (xb.baseDir[0])
		fixFileCase();
}

int loadUserIni(void)
{
	char path[1024];
	FILE *f;
	int len;

	strcpy(path, xb.baseDir);
	strcat(path, "options.ini");
	log_printf(1, "\n------ parsing user ini at '%s' ------\n", path);
	f = fopen(path, "rb");
	if (f == NULL) {
		log_printf(1, "\n******* WARNING: could not open user ini at '%s', skipping\n", path);
		return 0;
	}
	iniSize = getFileSize(f);
	len = iniSize + 1;
	iniBuf = malloc(len);
	if (iniBuf == NULL) {
		log_printf(0, "******* ERROR loading %s, unable to allocate memory\n", path);
		fclose(f);
		return 0;
	}
	memset(iniBuf, 0xff, len);
	log_printf(1, "loading file...", path);
	fread(iniBuf, iniSize, 1, f);
	fclose(f);
	log_printf(1, "done!\n", path);
	if (iniBuf[0] == 0xff || iniBuf[1] == 0xff) {
		log_printf(0, "***** WARNING: User ini %s\nappears to be a multi byte file, not an ascii only file - ignoring it!\n", path);
		free(iniBuf);
		iniBuf = NULL;
		iniSize = 0;
		return 0;
	}
	iniBuf[iniSize] = 0xff;
	log_printf(1, "pre-parsing and sanitizing\n");
	iniSize = iniPreParse(iniBuf, iniSize);
	log_printf(1, "done!\n");
	iniBuf[iniSize] = 0;
	return 1;
}

/* getters' own helper (not memFindStr); the ebx pins fix the RA ties, a sched2
   tie (asm barrier: lea before the reload) is left */
static int findKey(unsigned char *buf, const char *key)
{
	int i, j, len, l1;
	unsigned char *p;
	len = strlen(key);
	for (i = 0; i < iniSize - len; i++) {
		if (key[0] == buf[i]) {
			p = &buf[i];
			for (j = 0; j < len; j++)
				if (p[j] != key[j])
					j = len + 1;
			if (j == len) {
				unsigned char *q = &buf[i + len];
				__asm__("" :: "b"(q));
				if (*q != 0)
					return i + len;
			}
		}
	}
	return -1;
}
#define FIND findKey(iniBuf, key)
long getIniBool(const char *key, int def)
{
	int off;
	char *val;
	if (iniSize == 0)
		return def;
	off = FIND;
	if (off == -1)
		return def;
	val = (char *)&iniBuf[off];
	__asm__("" :: "b"(val));
	if (strnicmp(val, "true", 4) == 0)
		return 1;
	if (strnicmp(val, "false", 5) == 0)
		return 0;
	return def;
}

char *iniBoolInvalid(const char *key)
{
	int off;
	char *val;
	if (iniSize == 0)
		return NULL;
	off = FIND;
	if (off == -1)
		return NULL;
	val = (char *)&iniBuf[off];
	__asm__("" :: "b"(val));
	if (strnicmp(val, "true", 4) == 0)
		return NULL;
	if (strnicmp(val, "false", 5) != 0)
		return val;
	return NULL;
}
unsigned int getIniU32(const char *key, unsigned int def)
{
	int off;
	if (iniSize == 0)
		return def;
	off = FIND;
	if (off == -1)
		return def;
	return myatou32((char *)&iniBuf[off], def);
}
char *iniU32Invalid(const char *key)
{
	int off;
	char *val;
	if (iniSize == 0)
		return NULL;
	off = FIND;
	if (off == -1)
		return NULL;
	val = (char *)&iniBuf[off];
	if (val[0] == '0' && myatol(val[1]) == 'x') {
		if (validateString(val + 2) == 0)
			return val;
		return NULL;
	}
	if (validateString(val) != 0)
		return NULL;
	return val;
}

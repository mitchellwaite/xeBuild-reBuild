/* filelist_ini: reading the file list ini, and the tables that say which
   files each build type uses */
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
	struct fileent files[19];	/* 41eb0 35 of them; the bound sets the */
	u8 padf[(35 - 19) * 0x42c];	/* files loop's guessed trip count */
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

/* .data, in this order (-fno-toplevel-reorder) */
/* the bl section's file order per build type (blOrder is one of them) */
int blJtag[9] = {4, 5, 6, 7, 8, 15, 16, 9, 10};
int blDevgl[6] = {3, 4, 5, 6, 8, 9};
int blTestk[6] = {4, 5, 6, 7, 8, 9};
int blDevk[6] = {3, 4, 5, 6, 7, 8};
int blRetail[6] = {3, 4, 5, 6, 8, 9};

/* {offset, type} of each file for each build type */
struct fileloc { u32 offset; int type; };
struct fileloc locDevgl[14] = {
	{0, 0}, {0x1000, 2}, {0x4000, 3}, {0x8000, 11}, {-1, 12}, {-1, 7}, {-1, 8},
	{0x70000, 25}, {0xb0000, 9}, {-1, 10}, {0xc0000, 24}, {0xc0060, 23}, {-1, 26},
	{0x3febe00, 27}
};
struct fileloc locTestk[12] = {
	{0, 0}, {0x1000, 2}, {0x4000, 3}, {0x8000, 4}, {0xc000, 11}, {-1, 12}, {-1, 13},
	{-1, 14}, {0xb0000, 15}, {-1, 16}, {-1, 26}, {0x3febe00, 27}
};
struct fileloc locDevk[11] = {
	{0, 0}, {0x1000, 2}, {0x4000, 3}, {0x8000, 11}, {-1, 12}, {-1, 13}, {-1, 14},
	{0xb0000, 15}, {-1, 16}, {-1, 26}, {0x3febe00, 27}
};
struct fileloc locJtag[19] = {
	{0, 0}, {0x200, 1}, {0x1000, 2}, {0x4000, 3}, {0x8000, 17}, {-1, 18}, {-1, 19},
	{0x70000, 20}, {-1, 21}, {0x80000, 9}, {-1, 10}, {0x90000, 22}, {0x91000, 23},
	{0x95000, 24}, {0x95060, 25}, {0xd5060, 5}, {-1, 7}, {-1, 26}, {0x3febe00, 27}
};
struct fileloc locRetail[14] = {
	{0, 0}, {0x1000, 2}, {0x4000, 3}, {0x8000, 5}, {-1, 6}, {-1, 7}, {-1, 8},
	{0x70000, 25}, {0xb0000, 9}, {-1, 10}, {0xc0000, 24}, {0xc0060, 23}, {-1, 26},
	{0x3febe00, 27}
};

char fnNone[32] = "none";
char fnSmc[32] = "smc.bin";
char fnKv[32] = "kv.bin";
char fnKvAlt[32] = "kv_alt.bin";
char fnXellGg[32] = "xell-gggggg.bin";
char fnXell2f[32] = "xell-2f.bin";
char fnPatches[32] = "patches_";
char fnSmcConfig[32] = "smc_config.bin";
char fnFreeboot[32] = "freeboot.bin";
char fnFuses[32] = "fuses.bin";
char fnPayload[32] = "payload.bin";

extern const char *const consoleNames[8];
extern const unsigned char validChars[74];
int iniPreParse(unsigned char *buf, int size);
void log_printf(int level, const char *fmt, ...);
long getFileSize(FILE *f);
char myatol(char c);
int validateString(char *s);
unsigned int myatou32(char *dat, unsigned int def);

/* copy the base dir's casing of the smc, kv and patches file names; IRA's
   regional allocation keeps &st rather than dir in a register (ira-region=one) */
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


/* strip comments and invalid characters; returns the new size.  Needs
   -fno-tree-loop-vectorize (with it, PRE drops the validChars loop's
   PHI <'A', validChars[j+1]>) */
int iniPreParse(unsigned char *buf, int size)
{
	unsigned char *tmp;
	int i, j, n = size;

	tmp = malloc(size + 1);
	memcpy(tmp, buf, size + 1);
	/* remove comments */
	for (i = 0; i < n; i++) {
		/* 35% (builtin-expect-probability=65, build.sh): the comment
		   block's memcpy path is then hot enough for the default
		   align-threshold to align it after the ret */
		if (__builtin_expect(buf[i] == ';', 0)) {
			i++;
			for (j = 0; buf[i + j] != '\n' && buf[i + j] != 0xff && i + j < n; j++)
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
	/* dead (VRP drops it): its freed SSA name puts the comment loop's
	   header copy in 0xff-first order */
	if (i < 0)
		buf[0] = 1;
	memcpy(tmp, buf, size + 1);
	/* remove empty lines */
	for (i = 0; i < n; i++) {
		/* dead (VRP drops it, then the empty loop), but the profile is
		   estimated with it as the hottest block: that scales the comment
		   block and its inner loop's preheader to equal REG_FREQs, so LRA
		   assigns the inheritance of i (ebx) before &buf[i] (ecx) */
		for (j = 0; j < 44; j++)
			if (i < 0)
				buf[j] = 1;
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

extern int *blOrder;
u32 myatox32(char *dat, u32 def);
int memFindStr(unsigned char *buf, int size, const char *key, int label);
int memFindChar(unsigned char *buf, char c, int size);
void checkFileCase(void);

/* offset after `str` in buf (past its NUL if skipNul and it ends a line), or -1 */
int memFindStr(unsigned char *buf, int size, const char *str, int skipNul)
{
	int i, j, len;

	len = strlen(str);
	for (i = 0; i < size - len; i++) {
		if (str[0] == buf[i]) {
			for (j = 0; j < len; j++)
				if (buf[i + j] != str[j])
					j = len + 1;
			if (j == len) {
				if (skipNul) {
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

/* parseIni's strings, in the original's .rdata order: gcc emits a
   function's literals in its expand-time block order, which put the
   error messages before the code they follow in the original.  As
   arrays (-fno-toplevel-reorder keeps definition order) they land where
   they did, aligned as literals are (4 from 31 bytes, else 1) */
static const char fi_44fb60[] __attribute__((aligned(4))) = "\n------ parsing ini at '%s' ------\n";
static const char fi_44fb84[] __attribute__((aligned(1))) = "rb";
static const char fi_44fb88[] __attribute__((aligned(4))) = "\n******* ERROR: could not open '%s'\n";
static const char fi_44fbb0[] __attribute__((aligned(4))) = "******* ERROR loading %s, unable to allocate memory\n";
static const char fi_44fbe8[] __attribute__((aligned(4))) = "\n\n***** ERROR: File descriptor ini %s\nappears to be a multi byte file, not an ascii only file!\n";
static const char fi_44fc48[] __attribute__((aligned(1))) = "[version]";
static const char fi_44fc52[] __attribute__((aligned(1))) = "ini version %s\n";
static const char fi_44fc62[] __attribute__((aligned(1))) = "%s_jtag_%s.bin";
static const char fi_44fc71[] __attribute__((aligned(1))) = "%s_devk_%s.bin";
static const char fi_44fc80[] __attribute__((aligned(1))) = "%s_testk_%s.bin";
static const char fi_44fc90[] __attribute__((aligned(1))) = "%s_devgl_%s.bin";
static const char fi_44fca0[] __attribute__((aligned(1))) = "%s_retail_%s.bin";
static const char fi_44fcb1[] __attribute__((aligned(1))) = "%s_g2m_%s.bin";
static const char fi_44fcbf[] __attribute__((aligned(1))) = "%s_g2_%s.bin";
static const char fi_44fccc[] __attribute__((aligned(1))) = "%s_gg_%s.bin";
static const char fi_44fcdc[] __attribute__((aligned(4))) = "\n******* ERROR: could not find label [version] in file list ini\n";
static const char fi_44fd1d[] __attribute__((aligned(1))) = "[%sbl%s]";
static const char fi_44fd26[] __attribute__((aligned(1))) = "[%sbl]";
static const char fi_44fd2d[] __attribute__((aligned(1))) = "\nini: label %s found\n";
static const char fi_44fd44[] __attribute__((aligned(4))) = "\n******* ERROR: ini problem, error in %s section!\n";
static const char fi_44fd78[] __attribute__((aligned(4))) = "\n******* ERROR: crc data for file '%s' in ini is incorrect size!\n";
static const char fi_44fdba[] __attribute__((aligned(1))) = "found (%d) '%s' crc: 0x%08x\n";
static const char fi_44fdd8[] __attribute__((aligned(4))) = "\n******* ERROR: ini problem, can't find enough data for %s section!\n";
static const char fi_44fe20[] __attribute__((aligned(4))) = "\n******* ERROR: could not find label %s in file list ini\n";
static const char fi_44fe5a[] __attribute__((aligned(1))) = "none";
static const char fi_44fe60[] __attribute__((aligned(4))) = "ini dictates dual CB for this model\n";
static const char fi_44fe85[] __attribute__((aligned(1))) = "[rawpatch]";
static const char fi_44fe90[] __attribute__((aligned(1))) = "\nini: label [rawpatch] found\n";
static const char fi_44feb0[] __attribute__((aligned(4))) = "\n******* ERROR: an entry in [rawpatch] is missing offset info!\n";
static const char fi_44fef0[] __attribute__((aligned(4))) = "\n******* ERROR: offset data for file '%s' is either too large or too small!\n";
static const char fi_44ff40[] __attribute__((aligned(4))) = "found (%d) '%s' offset: 0x%08x\n";
static const char fi_44ff60[] __attribute__((aligned(4))) = "***** ERROR: [rawpatch] '%s' length is unintelligible!\n";
static const char fi_44ff98[] __attribute__((aligned(4))) = "\n******* ERROR: file name in [rawpatch] is too long!\n";
static const char fi_44ffd0[] __attribute__((aligned(4))) = "\n******* ERROR: %d of %d [rawpatch] slots are already full!\n";
static const char fi_450010[] __attribute__((aligned(4))) = "\n[rawpatch] label not found in ini\n";
static const char fi_450034[] __attribute__((aligned(1))) = "[flashfs]";
static const char fi_45003e[] __attribute__((aligned(1))) = "\nini: label [flashfs] found\n";
static const char fi_45005c[] __attribute__((aligned(4))) = "\n******* ERROR: file in [flashfs] has greater than %d chars in it's name!\n";
static const char fi_4500a7[] __attribute__((aligned(1))) = "\n        Line: %s\n";
static const char fi_4500bc[] __attribute__((aligned(4))) = "\n******* ERROR: file in [flashfs] has greater than %d chars in it's path!\n";
static const char fi_450108[] __attribute__((aligned(4))) = "\n******* ERROR: could not find label [flashfs] in file list ini\n";
static const char fi_450149[] __attribute__((aligned(1))) = "[security]";
static const char fi_450154[] __attribute__((aligned(1))) = "\nini: label [security] found\n";
static const char fi_450174[] __attribute__((aligned(4))) = "\n******* ERROR: file in [security] has greater than %d chars in it's name!\n";
static const char fi_4501c0[] __attribute__((aligned(4))) = "------ ini parsing completed ------\n\n";

/* read the file list ini: the files for this build type, the bootloaders'
   names and crcs, [rawpatch], [flashfs] and [security] */
u32 parseIni(char *path)
{
	FILE *f;
	unsigned char *buf, *p;
	int size, off, end, pos, len, nul, comma, n, i, nbl;
	u32 noCrc;
	struct fileent *e;
	char *s;
	u32 crc;
	char label[50];
	char tmp[0x400];

	log_printf(1, fi_44fb60, path);
	f = fopen(path, fi_44fb84);
	if (f == NULL) {
		log_printf(0, fi_44fb88, path);
		return 0;
	}
	size = getFileSize(f);
	buf = malloc(size + 1);
	if (buf == NULL) {
		log_printf(0, fi_44fbb0, path);
		return 0;
	}
	fread(buf, size, 1, f);
	fclose(f);
	if (buf[0] == 0xff || buf[1] == 0xff) {
		log_printf(0, fi_44fbe8, path);
		free(buf);
		return 0;
	}
	buf[size] = 0xff;
	size = iniPreParse(buf, size);
	buf[size] = 0;

	/* [version] */
	off = memFindStr(buf, size, fi_44fc48, 1);
	if (off == -1) {
		log_printf(0, fi_44fcdc);
		free(buf);
		return 0;
	}
	memset(xb.kernelStr, 0, sizeof(xb.kernelStr));
	len = memFindChar(&buf[off], 0, sizeof(xb.kernelStr));
	if (len == -1)
		len = sizeof(xb.kernelStr) - 1;
	strncpy(xb.kernelStr, (char *)&buf[off], len);
	log_printf(1, fi_44fc52, xb.kernelStr);
	if (xb.type == 2) {
		xb.nFiles = 19;
		blOrder = blJtag;
		nbl = 9;
		sprintf(tmp, fi_44fc62, xb.kernelStr, xb.outName);
	} else {
		if (xb.type == 6 || xb.type == 7) {
			xb.nFiles = 11;
			blOrder = blDevk;
			sprintf(tmp, fi_44fc71, xb.kernelStr, xb.outName);
			if (off < -1)
				buf[0] = 1;
		} else if (xb.type == 8 || xb.type == 9) {
			xb.nFiles = 12;
			blOrder = blTestk;
			sprintf(tmp, fi_44fc80, xb.kernelStr, xb.outName);
		} else {
			xb.nFiles = 14;
			if (xb.type == 4 || xb.type == 5) {
				blOrder = blDevgl;
				sprintf(tmp, fi_44fc90, xb.kernelStr, xb.outName);
			} else {
				blOrder = blRetail;
				if (xb.type == 1)
					sprintf(tmp, fi_44fca0, xb.kernelStr, xb.outName);
				else if (xb.glitch2mfg)
					sprintf(tmp, fi_44fcb1, xb.kernelStr, xb.outName);
				else if (xb.glitch2)
					sprintf(tmp, fi_44fcbf, xb.kernelStr, xb.outName);
				else
					sprintf(tmp, fi_44fccc, xb.kernelStr, xb.outName);
			}
		}
		nbl = 6;
	}
	xb.nFlashFiles = xb.nFiles - 2;
	strcpy(xb.outName, tmp);
	checkFileCase();

	/* the files this build type uses */
	for (i = 0; i < xb.nFiles; i++) {
		e = &xb.files[i];
		if (xb.type == 2) {
			e->type = locJtag[i].type;
			e->offset = locJtag[i].offset;
		} else if (xb.type == 6 || xb.type == 7) {
			e->type = locDevk[i].type;
			e->offset = locDevk[i].offset;
		} else if (xb.type == 4 || xb.type == 5) {
			e->type = locDevgl[i].type;
			e->offset = locDevgl[i].offset;
		} else if (xb.type == 8 || xb.type == 9) {
			e->type = locTestk[i].type;
			e->offset = locTestk[i].offset;
		} else {
			e->type = locRetail[i].type;
			e->offset = locRetail[i].offset;
		}
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
				if ((xb.flags & 7) == 5)
					strcat(e->name, "trinity");
				else if ((xb.flags & 7) == 6)
					strcat(e->name, "corona");
				else if ((xb.flags & 7) == 7)
					strcat(e->name, "winchester");
				else
					strcat(e->name, "fat");
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
		sprintf(label, fi_44fd1d, consoleNames[xb.flags & 7], xb.blSuffix);
	else
		sprintf(label, fi_44fd26, consoleNames[xb.flags & 7]);
	off = memFindStr(buf, size, label, 1);
	if (off < 0) {
		log_printf(0, fi_44fe20, label);
		free(buf);
		return 0;
	}
	log_printf(1, fi_44fd2d, label);
	end = off + memFindChar(&buf[off], '[', size - off);
	/* this and the other `< -1` stores below are dead (VRP1 drops them);
	   the SSA names they free set the comma/nul compare order in the bl,
	   [flashfs] and [security] loops, and give [rawpatch]'s n a late
	   partition (combine orders the lea's registers by pseudo number) */
	if (comma < -1) {
		buf[0] = 1;
		buf[1] = 1;
	}
	pos = off;
	for (i = 0; i < nbl; ) {
		p = &buf[pos];
		comma = memFindChar(p, ',', size - pos);
		nul = memFindChar(p, 0, size - pos);
		len = comma;
		noCrc = 0;
		if (comma > nul) {
			len = nul;
			noCrc = 1;
		}
		if (len < 0) {
			log_printf(0, fi_44fd44, label);
			free(buf);
			return 0;
		}
		strncpy(xb.files[blOrder[i]].name, (char *)p, len);
		xb.files[blOrder[i]].name[len] = 0;
		pos = pos + len + 1;
		if (!noCrc) {
			n = memFindChar(&buf[pos], 0, size - pos);
			if (n == 0)
				xb.files[blOrder[i]].crc = 0;
			else if (n != 8) {
				log_printf(0, fi_44fd78, xb.files[blOrder[i]].name);
				free(buf);
				return 0;
			} else {
				strncpy(tmp, (char *)&buf[pos], 8);
				tmp[8] = 0;
				xb.files[blOrder[i]].crc = myatox32(tmp, 0);
				if (n < -1)
					n = 0;
			}
			pos = pos + n + 1;
		} else
			xb.files[blOrder[i]].crc = 0;
		log_printf(1, fi_44fdba, i + 1, xb.files[blOrder[i]].name, xb.files[blOrder[i]].crc);
		i++;
		if (pos > end) {
			log_printf(0, fi_44fdd8, label);
			free(buf);
			return 0;
		}
	}
	if (xb.type != 2 && xb.type <= 5) {
		if (strnicmp(xb.files[4].name, fi_44fe5a, 4) == 0)
			xb.cbb = 0;
		else {
			log_printf(1, fi_44fe60);
			xb.cbb = 1;
		}
	}

	/* [rawpatch]: name,offset */
	off = memFindStr(buf, size, fi_44fe85, 1);
	if (i < -1)
		buf[0] = 1;
	if (off == -1)
		log_printf(1, fi_450010);
	else {
		end = off + memFindChar(&buf[off], '[', size - off);
		log_printf(1, fi_44fe90);
		pos = off;
		for (i = xb.nRawPatches; i < 16; i++) {
			p = &buf[pos];
			if (off < -1)
				buf[0] = 1;
			nul = memFindChar(p, 0, size - pos);
			comma = memFindChar(p, ',', size - pos);
			if (comma == -1 || comma >= nul) {
				log_printf(0, fi_44feb0);
				free(buf);
				return 0;
			}
			if (comma > 1023) {
				log_printf(0, fi_44ff98);
				free(buf);
				return 0;
			}
			strncpy(xb.rawPatch[i].name, (char *)p, comma);
			xb.rawPatch[i].name[comma] = 0;
			pos = pos + comma + 1;
			n = memFindChar(&buf[pos], 0, size - pos);
			if (n == 0 || n > 10) {
				log_printf(0, fi_44fef0, xb.rawPatch[i].name);
				free(buf);
				return 0;
			}
			strncpy(tmp, (char *)&buf[pos], n);
			tmp[n] = 0;
			pos = pos + n + 1;
			xb.rawPatch[i].offset = myatou32(tmp, -1);
			if (xb.rawPatch[i].offset == (u32)-1) {
				log_printf(1, fi_44ff60, xb.rawPatch[i].name);
				free(buf);
				return 0;
			}
			log_printf(1, fi_44ff40, ++xb.nRawPatches, xb.rawPatch[i].name, xb.rawPatch[i].offset);
			if (pos >= end)
				i = 16;
		}
		if (pos < end) {
			log_printf(0, fi_44ffd0, xb.nRawPatches, 16);
			free(buf);
			return 0;
		}
	}

	/* [flashfs]: name[,crc]; a trailing 1 or 2 on the name is dropped */
	off = memFindStr(buf, size, fi_450034, 1);
	if (off == -1)
		goto noFlashfs;
	xb.nFirmware = 0;
	log_printf(1, fi_45003e);
	pos = off;
	for (i = 0; i < 256; i++) {
		p = &buf[pos];
		nul = memFindChar(p, 0, size - pos);
		if (nul < -1)
			buf[0] = 1;
		comma = memFindChar(p, ',', size - pos);
		noCrc = 1;
		len = nul;
		if (comma >= 0 && comma < nul) {
			len = comma;
			noCrc = 0;
		}
		if (len > 1023) {
			log_printf(0, fi_4500bc, 1023);
			free(buf);
			return 0;
		}
		strncpy(xb.firmware[i], (char *)p, len);
		xb.firmware[i][len] = 0;
		if (off < -1)
			buf[0] = 1;
		if (len > 21) {
			s = strrchr(xb.firmware[i], '/');
			if (off < -1)
				buf[0] = 1;
			/* dead only from the strlen pass on (after dom3): the names it
			   frees go to vrp2's threading, which then gives the len == 0
			   path's noCrc PHI its copy first */
			{
				char t_[4];
				strcpy(t_, "ab");
				if (strlen(t_) != 2)
					buf[0] = 1;
			}
			if (s == NULL)
				s = strrchr(xb.firmware[i], '\\');
			if (len < -1)
				buf[0] = 1;
			s = s ? s + 1 : xb.firmware[i];
			if (strlen(s) > 21) {
				log_printf(0, fi_45005c, 21);
				log_printf(0, fi_4500a7, xb.firmware[i]);
				free(buf);
				if (off < -1)
					buf[0] = 1;
				return 0;
			}
		}
		pos = pos + len + 1;
		if (xb.firmware[i][len - 1] == '1' || xb.firmware[i][len - 1] == '2')
			xb.firmware[i][len - 1] = 0;
		if (!noCrc) {
			n = memFindChar(&buf[pos], 0, size - pos);
			if (n == 0)
				crc = xb.firmwareCrc[i] = 0;
			else if (n != 8) {
				log_printf(0, fi_44fd78, xb.firmware[i]);
				free(buf);
				return 0;
			} else {
				strncpy(tmp, (char *)&buf[pos], 8);
				tmp[8] = 0;
				crc = xb.firmwareCrc[i] = myatox32(tmp, 0);
			}
			pos = pos + n + 1;
		} else
			crc = xb.firmwareCrc[i] = 0;
		log_printf(1, fi_44fdba, ++xb.nFirmware, xb.firmware[i], crc);
		if (pos >= size)
			i = 256;
	}

	/* [security]: name[,crc] */
	/* the not-found block sits between the search's guard and its preheader:
	   ce2 then speculates the preheader into the guard, and jump2 (once this
	   block is crossjumped into noFlashfs) inverts the guard to fall into
	   IRA's buf reload */
	goto secSearch;
noSecurity:
	/* sic: names [flashfs] */
	log_printf(0, fi_450108);
	free(buf);
	return 0;
secSearch:
	off = memFindStr(buf, size, fi_450149, 1);
	if (off == -1)
		goto noSecurity;
	xb.nFlashFiles2 = 0;
	log_printf(1, fi_450154);
	end = off + memFindChar(&buf[off], '[', size - off);
	pos = off;
	for (i = 0; i < 10; i++) {
		p = &buf[pos];
		comma = memFindChar(p, ',', size - pos);
		nul = memFindChar(p, 0, size - pos);
		if (comma > nul) {
			noCrc = 1;
			len = nul;
		} else {
			noCrc = 0;
			len = comma;
		}
		if (len > 21)
			goto secName;
		strncpy(xb.flashFiles[i], (char *)p, len);
		xb.flashFiles[i][len] = 0;
		pos = pos + len + 1;
		if (!noCrc) {
			n = memFindChar(&buf[pos], 0, size - pos);
			if (n == 0)
				xb.flashCrc[i] = 0;
			else if (n != 8) {
				/* sic: names the [flashfs] file */
				log_printf(0, fi_44fd78, xb.firmware[i]);
				free(buf);
				return 0;
			} else {
				strncpy(tmp, (char *)&buf[pos], 8);
				tmp[8] = 0;
				xb.flashCrc[i] = myatox32(tmp, 0);
			}
			pos = pos + n + 1;
		} else
			xb.flashCrc[i] = 0;
		/* re-read, not a crc variable: FRE's later PHI orders the n == 0
		   path's copies crc first */
		log_printf(1, fi_44fdba, ++xb.nFlashFiles2, xb.flashFiles[i], xb.flashCrc[i]);
		if (pos >= end)
			i = 10;
	}
	free(buf);
	log_printf(1, fi_4501c0);
	return 1;
	/* after the security blocks, so jump2 redirects noSecurity into it */
noFlashfs:
	log_printf(0, fi_450108);
	free(buf);
	return 0;
	/* last in the block chain: jump2 then crossjumps the crc error into the
	   shared tail instead of splitting it */
secName:
	log_printf(0, fi_450174, 21);
	free(buf);
	return 0;
}

/* offset of the value after `key` in buf, or -1 */
static int findIniKey(unsigned char *buf, int size, const char *key)
{
	int i, j, len;

	len = strlen(key);
	for (i = 0; i < size - len; i++) {
		if (key[0] == buf[i]) {
			for (j = 0; j < len; j++)
				if (buf[i + j] != key[j])
					j = len + 1;
			if (j == len && buf[i + len] != 0)
				return i + len;
		}
	}
	return -1;
}

/* the value after `key` in the loaded ini, or NULL */
char *getIniValue(const char *key)
{
	int off;

	if (iniSize == 0)
		return NULL;
	off = findIniKey(iniBuf, iniSize, key);
	if (off == -1)
		return NULL;
	return (char *)&iniBuf[off];
}

/* getters' own helper (not memFindStr).  The ebx pins fix RA ties; findKey's
   has an output (kept by the unreachable) so it is no sched2 barrier */
static int findKey(unsigned char *buf, const char *key)
{
	int i, j, len;
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
				int d;
				__asm__("" : "=r"(d) : "b"(q));
				if (d)
					__builtin_unreachable();
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

/* load and pre-parse options.ini from the base dir; 0 if there is none */
int loadUserIni(void)
{
	char path[1024];
	FILE *f;
	int len;

	strcpy(path, xb.baseDir);
	strcat(path, "options.ini");
	log_printf(1, "\n------ parsing user ini at '%s' ------\n", path);
	f = fopen(path, fi_44fb84);
	if (f == NULL) {
		log_printf(1, "\n******* WARNING: could not open user ini at '%s', skipping\n", path);
		return 0;
	}
	iniSize = getFileSize(f);
	len = iniSize + 1;
	iniBuf = malloc(len);
	if (iniBuf == NULL) {
		log_printf(0, fi_44fbb0, path);
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

/* .rdata after the functions' strings */
/* iniPreParse's; 74 chars, no NUL */
const unsigned char validChars[74] =
	"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,;[]_\n\\/-$:";
const char *const consoleNames[8] = {
	NULL, "xenon", "zephyr", "falcon", "jasper", "trinity", "corona", "winchester"
};

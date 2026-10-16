/* build: reading the image's input files (with crc32 checks against the
   ini), bootloader checks, patches and payloads, encoding the flash.
   Mixed object: the functions here are spliced into build.s
   (re/splice.py), which still holds the rest and the data, so strings
   name the .s's (splice.py drops gcc's copies; static arrays rather
   than externs so that gcc still folds strlen of them).
   wip/app/build.c is the whole draft; wip/mixed.py makes this file
   from it. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;

/* timeutil.c's cdecl ports of the Win32 time functions */
typedef unsigned short WORD;
typedef unsigned int DWORD;
typedef struct {
	DWORD dwLowDateTime;
	DWORD dwHighDateTime;
} FILETIME;
typedef struct {
	WORD wYear, wMonth, wDayOfWeek, wDay;
	WORD wHour, wMinute, wSecond, wMilliseconds;
} SYSTEMTIME;
int SystemTimeToFileTime(const SYSTEMTIME *syst, FILETIME *ft);
int FileTimeToDosDateTime(const FILETIME *ft, WORD *fatdate, WORD *fattime);
int DosDateTimeToFileTime(WORD fatdate, WORD fattime, FILETIME *ft);
void GetSystemTime(SYSTEMTIME *systime);

/* an input file of the image */
struct fileent {
	char name[0x400];
	u32 crc;			/* 400 */
	int type;			/* 404 */
	u32 offset;			/* 408 */
	u8 *data;			/* 40c */
	u32 size;			/* 410 */
	u8 pad414[0x42c - 0x414];
};

/* the parts of main.c's struct xebuild used here */
struct xebuild {
	int mode;			/* 000 */
	u32 flags;			/* 004 */
	u32 type;			/* 008 */
	u32 kernel;			/* 00c */
	u8 pad010[0x024 - 0x010];
	int sysTime;			/* 024 use the system time for timestamps */
	u8 pad028[0x6ac - 0x028];
	char binDir[0x800];		/* 6ac */
	char baseDir[0x400];		/* eac */
	char dataDir[0x400];		/* 12ac */
	char commonDir[0x400];		/* 16ac */
	u8 pad1aac[0x41eb0 - 0x1aac];
	struct fileent files[35];	/* 41eb0 [19..34]: addon patches */
	u8 pad4b0b4[0x4b0f4 - 0x4b0b4];
	int nAddons;			/* 4b0f4 */
	int nFiles;			/* 4b0f8 */
	int nFlashFiles;		/* 4b0fc */
};

void log_printf(int level, const char *fmt, ...);
long getFileSize(FILE *f);
unsigned int crc32(const unsigned char *buf, unsigned int len);

extern struct xebuild xb;
#define addons (&xb.files[19])

int suGetFile(const char *name, u8 **data, u32 *len);
int fsGetFile(const char *name, u8 **buf, u32 *size, u32 *time);
int updateGetFile(const char *name, u8 **data, u32 *size);

/* strings in build.s */
static const char bd_458ca4[] = "rb";
static const char bd_458ca8[] = "\n******WARNING: '%s' is a 0 byte file, loading skipped!\n";
static const char bd_458ce1[] = "reading %s (0x%x bytes)";
static const char bd_458cf9[] = "\n";
static const char bd_458cfc[] = "reading %s (0x%x b pad 0x%x b)";
static const char bd_458d1b[] = " (crc32: 0x%08x ini: 0x%08x)\n";
static const char bd_458d3c[] = "\n******WARNING: '%s' crc32: 0x%08x expected: 0x%08x\n";
static const char bd_458d74[] = "**** using default time!!! ****\n";
static const char bd_458d98[] = "**** %s metadata found, not using system time *****\n\n";

/* still in build.s */
int timestampToFileTime(const u16 *ts, FILETIME *ft);
int loadBaseFile(const char *name, struct fileent *e) __attribute__((regparm(2)));
int loadBaseFileMeta(const char *name, struct fileent *e, u8 *meta);
int loadInputFile(const char *name, struct fileent *e, int pad, u32 crc, u8 *meta,
		  int su, int fs, int common);

u32 findFileOffset(int type)
{
	int i;

	for (i = 0; i < xb.nFlashFiles; i++)
		if (xb.files[i].type == type)
			return xb.files[i].offset;
	return 0;
}

u32 findFileSize(int type)
{
	int i;

	for (i = 0; i < xb.nFlashFiles; i++)
		if (xb.files[i].type == type)
			return xb.files[i].size;
	return 0;
}

int findFile(int type)
{
	int i;

	for (i = 0; i < xb.nFiles; i++)
		if (xb.files[i].type == type)
			return i;
	return 0;
}

int loadFileCrc(const char *name, struct fileent *e, int verbose, int pad, u32 crc)
{
	FILE *f;
	size_t size;
	u32 c;

	f = fopen(name, bd_458ca4);
	if (!f)
		return -1;
	if (e->data)
		free(e->data);
	size = getFileSize(f);
	if (!size) {
		fclose(f);
		log_printf(0, bd_458ca8, name);
		return 1;
	}
	e->size = size;
	if (pad && (size & 15))
		e->size = (size + 15) & ~15;
	if (verbose) {
		if (size != e->size)
			log_printf(1, bd_458cfc, name, size, (size + 15) & ~15);
		else
			log_printf(1, bd_458ce1, name, size);
	}
	e->data = calloc(e->size + 0x10000, 1);
	if (!e->data)
		return -2;
	fread(e->data, size, 1, f);
	fclose(f);
	if (crc) {
		c = crc32(e->data, size);
		log_printf(1, bd_458d1b, c, crc);
		if (crc != c) {
			log_printf(0, bd_458d3c, name, c, crc);
			return 1;
		}
	} else
		log_printf(1, bd_458cf9);
	return 0;
}

int readMetaFile(const char *name, u8 *meta)
{
	FILE *f;

	f = fopen(name, bd_458ca4);
	if (!f)
		return -1;
	fread(meta, 4, 1, f);
	fclose(f);
	return 0;
}

/* the build time as a big-endian FAT date and time */
void makeTimestamp(u8 *out, FILETIME *ft)
{
	SYSTEMTIME st;
	FILETIME now;
	WORD date, time;

	if (xb.sysTime) {
		GetSystemTime(&st);
		SystemTimeToFileTime(&st, &now);
	} else {
		log_printf(2, bd_458d74);
		now.dwHighDateTime = 30268127;
		now.dwLowDateTime = 1903825408;
	}
	FileTimeToDosDateTime(&now, &date, &time);
	if (ft)
		DosDateTimeToFileTime(date, time, ft);
	out[0] = date >> 8;
	out[1] = date;
	out[2] = time >> 8;
	out[3] = time;
}

int loadCommonFile(const char *name, struct fileent *e, int pad, u32 crc, u8 *meta)
{
	char path[0x400];
	int r;

	strcpy(path, xb.commonDir);
	strcat(path, name);
	r = loadFileCrc(path, e, 1, pad, crc);
	if (!r && meta) {
		strcat(path, ".meta");
		if (!readMetaFile(path, meta))
			log_printf(1, bd_458d98, path);
		else
			makeTimestamp(meta, NULL);
	}
	return r;
}

/* an addon patch from the bin dir */
int loadBinFile(struct fileent *e)
{
	char path[0x400];

	strcpy(path, xb.binDir);
	strcat(path, e->name);
	return loadFileCrc(path, e, 1, 0, 0);
}

/* e->name as given, else from ./ */
int loadLocalFile(struct fileent *e)
{
	char path[0x400];

	strcpy(path, e->name);
	if (!loadFileCrc(path, e, 1, 0, 0))
		return 0;
	strcpy(path, "./");
	strcat(path, e->name);
	return loadFileCrc(path, e, 1, 0, 0);
}

int setFileData(struct fileent *e, const void *data, size_t size)
{
	e->data = calloc(size, 1);
	if (!e->data)
		return 1;
	e->size = size;
	memcpy(e->data, data, size);
	return 0;
}

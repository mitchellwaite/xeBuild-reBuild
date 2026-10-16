/* build: reading the image's input files (with crc32 checks against the
   ini), bootloader checks, patches and payloads, encoding the flash */
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

	f = fopen(name, "rb");
	if (!f)
		return -1;
	if (e->data)
		free(e->data);
	size = getFileSize(f);
	if (!size) {
		fclose(f);
		log_printf(0, "\n******WARNING: '%s' is a 0 byte file, loading skipped!\n", name);
		return 1;
	}
	e->size = size;
	if (pad && (size & 15))
		e->size = (size + 15) & ~15;
	if (verbose) {
		if (size != e->size)
			log_printf(1, "reading %s (0x%x b pad 0x%x b)", name, size, (size + 15) & ~15);
		else
			log_printf(1, "reading %s (0x%x bytes)", name, size);
	}
	e->data = calloc(e->size + 0x10000, 1);
	if (!e->data)
		return -2;
	fread(e->data, size, 1, f);
	fclose(f);
	if (crc) {
		c = crc32(e->data, size);
		log_printf(1, " (crc32: 0x%08x ini: 0x%08x)\n", c, crc);
		if (crc != c) {
			log_printf(0, "\n******WARNING: '%s' crc32: 0x%08x expected: 0x%08x\n", name, c, crc);
			return 1;
		}
	} else
		log_printf(1, "\n");
	return 0;
}

int readMetaFile(const char *name, u8 *meta)
{
	FILE *f;

	f = fopen(name, "rb");
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
		log_printf(2, "**** using default time!!! ****\n");
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

int timestampToFileTime(const u16 *ts, FILETIME *ft)
{
	return DosDateTimeToFileTime(__builtin_bswap16(ts[0]), __builtin_bswap16(ts[1]), ft);
}

/* read baseDir/name into e */
static int loadBaseFile(const char *name, struct fileent *e)
{
	char path[0x400];

	if (!xb.baseDir[0])
		return -1;
	strcpy(path, xb.baseDir);
	strcat(path, name);
	return loadFileCrc(path, e, 1, 0, 0);
}

/* the same with its timestamp from name.meta if there is one */
int loadBaseFileMeta(const char *name, struct fileent *e, u8 *meta)
{
	char path[0x400];
	int r;

	if (!xb.baseDir[0])
		return -1;
	strcpy(path, xb.baseDir);
	strcat(path, name);
	r = loadFileCrc(path, e, 1, 0, 0);
	if (!r && meta) {
		strcat(path, ".meta");
		if (!readMetaFile(path, meta))
			log_printf(1, "**** %s metadata found, not using system time *****\n\n", path);
	}
	return r;
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
			log_printf(1, "**** %s metadata found, not using system time *****\n\n", path);
		else
			makeTimestamp(meta, NULL);
	}
	return r;
}

/* name from the data dir, else from the system update (SUPD), the nand
   dump or the console (USVR), else from the common dir */
int loadInputFile(const char *name, struct fileent *e, int pad, u32 crc, u8 *meta,
		  int su, int fs, int common)
{
	char path[0x400];
	const char *base;
	u32 ts, c;
	int r;

	base = strrchr(name, '/');
	if (!base)
		base = strrchr(name, '\\');
	if (base)
		base++;
	else
		base = name;
	if (strrchr(name, ':'))
		strcpy(path, name);
	else {
		strcpy(path, xb.dataDir);
		strcat(path, name);
	}
	r = loadFileCrc(path, e, 1, pad, crc);
	if (meta && !r) {
		strcat(path, ".meta");
		if (!readMetaFile(path, meta))
			log_printf(1, "**** %s metadata found, not using system time *****\n\n", path);
		else
			makeTimestamp(meta, NULL);
	}
	if (su && r) {
		if (suGetFile(base, &e->data, &e->size)) {
			log_printf(1, "extracted SUPD/%s (0x%x bytes)", base, e->size);
			if (crc) {
				c = crc32(e->data, e->size);
				log_printf(1, " (crc32: 0x%08x ini: 0x%08x)\n", c, crc);
				if (crc == c) {
					if (meta)
						makeTimestamp(meta, NULL);
					r = 0;
				} else
					log_printf(0, "\n******WARNING: '%s' crc32: 0x%08x expected: 0x%08x\n", base, c, crc);
			} else
				log_printf(1, "\n");
		}
	}
	if (fs && r) {
		if (fsGetFile(base, &e->data, &e->size, &ts)) {
			log_printf(1, "extracted nanddump/%s (0x%x bytes)", base, e->size);
			if (crc) {
				c = crc32(e->data, e->size);
				log_printf(1, " (crc32: 0x%08x ini: 0x%08x)\n", c, crc);
				if (crc == c) {
					if (meta)
						makeTimestamp(meta, NULL);
					r = 0;
				} else {
					free(e->data);
					e->data = NULL;
					e->size = 0;
					log_printf(0, "\n******WARNING: '%s' crc32: 0x%08x expected: 0x%08x\n", base, c, crc);
				}
			} else
				log_printf(1, "\n");
		} else if (xb.mode == 2 && updateGetFile(base, &e->data, &e->size)) {
			log_printf(1, "extracted USVR/%s (0x%x bytes)", base, e->size);
			if (crc) {
				c = crc32(e->data, e->size);
				log_printf(1, " (crc32: 0x%08x ini: 0x%08x)\n", c, crc);
				if (crc == c) {
					if (meta)
						makeTimestamp(meta, NULL);
					r = 0;
				} else {
					free(e->data);
					e->data = NULL;
					e->size = 0;
					log_printf(0, "\n******WARNING: '%s' crc32: 0x%08x expected: 0x%08x\n", base, c, crc);
				}
			} else {
				log_printf(1, "\n");
				r = 0;
			}
		}
	}
	if (common && r)
		return loadCommonFile(base, e, pad, crc, meta);
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

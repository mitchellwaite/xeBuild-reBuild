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
	u8 pad028[0x038 - 0x028];
	u8 *hdr;			/* 038 the image's header */
	u8 pad03c[0x060 - 0x03c];
	u32 bootFlags;			/* 060 */
	u8 pad064[0x068 - 0x064];
	int xellButton;			/* 068 */
	int xellAltButton;		/* 06c */
	int dualButton;			/* 070 */
	u8 pad074[0x6ac - 0x074];
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
u16 getBeU16(const u8 *p);
u32 getBeU32(const u8 *p);
u8 *setBeU32(u32 v, u8 *p);
int checkZeros(const u8 *p, u32 len);
int smcConfigOk(const u8 *smc);
void showSmcConfig(const u8 *smc);
int patchSmcConfig(u8 *smc);
u8 *findInst(u8 *buf, int len, const u8 *pat, int patlen);
void display_buffer_hex(const u8 *buf, u32 len, u32 level);
typedef struct { u32 state[24]; } XECRYPT_SHA_STATE;	/* SHA_CTX */
void XeCryptShaInit(XECRYPT_SHA_STATE *sha);
void XeCryptShaUpdate(XECRYPT_SHA_STATE *sha, const void *buf, u32 len);
void XeCryptShaFinal(XECRYPT_SHA_STATE *sha, u8 *out, u32 len);
void XeCryptRotSum(u8 *sum, const void *buf, u32 cqw);

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

/* an ini value is used if it is in range; 0 and -1 mean unset */
int iniRangeOk(const char *name, u32 v, u32 lo, u32 hi)
{
	int ok = 1;

	if (v < lo || v > hi) {
		ok = 0;
		if (v != 0 && v != 0xffffffff)
			log_printf(0, "Ini value %d for %s is out of range (%d-%d), not using\n", v, name, lo, hi);
	}
	return ok;
}

/* the build's kernel version is the highest of its bootloaders' */
void raiseKernel(u16 magic, u16 build, u16 qfe)
{
	u32 k = 0x20000000 | build << 8;

	if (k > xb.kernel)
		xb.kernel = k;
}

/* check a bootloader's magic and size and (with its header's per-console
   fields cleared) its crc32 against the ini's; -1 skips the crc for the
   SC/SD/SE that are built rather than read */
int checkBl(u8 *bl, u32 size, int type, u32 crc)
{
	u32 blsize, c;

	blsize = getBeU32(bl + 12);
	if (blsize > size) {
		log_printf(0, "\n\n***** ERROR: BL size (0x%x) is bigger than the file (0x%x) read in!\n", blsize, size);
		return -3;
	}
	if ((bl[0] & 0x43) != 0x43)
		goto magic;
	switch (type) {
	case 5:
	case 6:
	case 11:
	case 17:
		if (bl[1] != 'B')
			goto magic;
		memset(bl + 0x10, 0, 0x30);
		c = crc32(bl, blsize);
		if (crc != c)
			goto bad;
		break;
	case 7:
	case 18:
		if (bl[1] != 'D')
			goto magic;
		memset(bl + 0x10, 0, 0x10);
		c = crc32(bl, blsize);
		if (crc != c)
			goto bad;
		break;
	case 8:
	case 19:
		if (bl[1] != 'E')
			goto magic;
		memset(bl + 0x10, 0, 0x10);
		c = crc32(bl, blsize);
		if (crc != c)
			goto bad;
		raiseKernel(getBeU16(bl), getBeU16(bl + 2), getBeU16(bl + 4));
		break;
	case 9:
	case 15:
	case 20:
		if (bl[1] != 'F')
			goto magic;
		memset(bl + 0x20, 0, 0x210);
		c = crc32(bl, blsize);
		if (crc != c)
			goto bad;
		raiseKernel(getBeU16(bl), getBeU16(bl + 20), getBeU16(bl + 22));
		break;
	case 10:
	case 16:
	case 21:
		if (bl[1] != 'G')
			goto magic;
		memset(bl + 0x10, 0, 0x10);
		c = crc32(bl, blsize);
		if (crc != c)
			goto bad;
		break;
	case 12:
		if (bl[1] != 'C')
			goto magic;
		memset(bl + 0x10, 0, 0x10);
		if (crc == 0xffffffff)
			break;
		c = crc32(bl, blsize);
		if (crc != c)
			goto bad;
		break;
	case 13:
		if (bl[1] != 'D')
			goto magic;
		memset(bl + 0x10, 0, 0x10);
		if (crc == 0xffffffff)
			break;
		c = crc32(bl, blsize);
		if (crc != c)
			goto bad;
		break;
	case 14:
		if (bl[1] != 'E')
			goto magic;
		memset(bl + 0x10, 0, 0x10);
		c = crc32(bl, blsize);
		raiseKernel(getBeU16(bl), getBeU16(bl + 2), getBeU16(bl + 4));
		if (crc == 0xffffffff)
			break;
		c = crc32(bl, blsize);
		if (crc != c)
			goto bad;
		break;
	default:
		c = 0;
		goto bad;
	}
	return 0;
bad:
	log_printf(0, "\n\n***** ERROR: BL crc check failed! calculated: %08x expected: %08x\n", c, crc);
	return -2;
magic:
	log_printf(0, "\n\n***** ERROR: BL magic check %c%c for type %d failed!\n", bl[0], bl[1], type);
	return -1;
}

/* find the SMC config in a nand image (pages with or without their
   0x10-byte spare data) and copy it to e */
int extractSmcConfig(struct fileent *e, u8 *buf, u32 size)
{
	u32 i, j;
	int found;

	if (e->data)
		free(e->data);
	e->size = 0x400;
	e->data = malloc(0x400);
	if (!e->data)
		return -2;
	log_printf(1, "-------------------\n");
	log_printf(1, "checking smc_config\n");
	log_printf(1, "-------------------\n");
	found = 0;
	for (i = 0; i + 0x200 <= size; i += 0x200)
		if ((found = smcConfigOk(buf + i)) == 1)
			break;
	if (!found) {
		for (i = 0; i + 0x210 <= size; i += 0x210)
			if ((found = smcConfigOk(buf + i)) == 1)
				break;
		if (!found) {
			log_printf(0, "******* ERROR: unable to find SMC config data!\n");
			return 2;
		}
	}
	if (checkZeros(buf + i + 0x20c, 4)) {
		log_printf(1, "extracting config\n");
		if (size - i >= 0x400)
			memcpy(e->data, buf + i, 0x400);
	} else {
		if (size - i < 0x4200) {
			log_printf(1, "******* ERROR: extracting config did not work, not enough data to copy!\n");
			return -2;
		}
		log_printf(1, "extracting config raw\n");
		for (j = 0; j < 8; j++)
			memcpy(e->data + j * 0x200, buf + i + j * 0x210, 0x200);
	}
	if (i)
		log_printf(1, "valid SMC config data found at offset 0x%x\n", i);
	log_printf(1, "------------------\n");
	log_printf(1, "SMC config info:\n");
	log_printf(1, "------------------\n");
	showSmcConfig(e->data);
	log_printf(1, "---------------------\n");
	if (patchSmcConfig(e->data)) {
		log_printf(1, "SMC patched info:\n");
		log_printf(1, "------------------\n");
		showSmcConfig(e->data);
		log_printf(1, "---------------------\n");
	}
	return 0;
}

int blmodMissing(struct fileent *e)
{
	return loadBaseFile("blmod.bin", e) != 0;
}

/* XeCryptRotSumSha, showing the sums */
void rotSumSha(const u8 *a, u32 alen, const u8 *b, u32 blen, u8 *out, u32 outlen)
{
	u8 sum[32];
	XECRYPT_SHA_STATE sha;
	u32 i;

	for (i = 0; i < 32; i++)
		sum[i] = 0;
	XeCryptRotSum(sum, a, alen >> 3);
	log_printf(1, "sum1:");
	display_buffer_hex(sum, 32, 1);
	XeCryptRotSum(sum, b, blen >> 3);
	log_printf(1, "sum2:");
	display_buffer_hex(sum, 32, 1);
	XeCryptShaInit(&sha);
	XeCryptShaUpdate(&sha, sum, 32);
	XeCryptShaUpdate(&sha, sum, 32);
	XeCryptShaUpdate(&sha, a, alen);
	XeCryptShaUpdate(&sha, b, blen);
	for (i = 0; i < 32; i++)
		sum[i] = ~sum[i];
	log_printf(1, "sum3:");
	display_buffer_hex(sum, 32, 1);
	XeCryptShaUpdate(&sha, sum, 32);
	XeCryptShaUpdate(&sha, sum, 32);
	XeCryptShaFinal(&sha, out, outlen);
	log_printf(1, "fin :");
	display_buffer_hex(out, outlen, 1);
}

int countBits(u8 v)
{
	int i, n = 0;

	for (i = 0; i < 8; i++) {
		if (v & 1)
			n++;
		v >>= 1;
	}
	return n;
}

/* the bootloader types an update (xeBuild's -u) replaces */
int isUpdateBl(u32 type)
{
	return type == 9 || type == 10 || type == 15 || type == 16 ||
	       type == 23 || type == 24 || type == 25;
}

/* payload.bin's `li r4, reps` (copy loop count in words) */
void patchPayloadSize(u8 *buf, int len, int size)
{
	int pat = 0xffff8038;	/* li r4, (any) */
	u8 *p;
	u32 reps = (size + 3) >> 2;

	log_printf(1, "patching payload.bin to load size 0x%x (0x%x reps)\n", size, reps);
	p = findInst(buf, len, (u8 *)&pat, 4);
	if (!p)
		return;
	log_printf(2, "org li %r4, %02x%02x\n", p[2], p[3]);
	p[3] = reps;
	p[2] = reps >> 8;
	log_printf(2, "fin li %r4, %02x%02x\n", p[2], p[3]);
}

/* the header bytes freeboot/xell read: UART speed, power-on reasons */
void patchHeaderOpts(void)
{
	u8 opts = 0;

	xb.hdr[0x4b] = 1;
	if (xb.bootFlags & 9) {
		log_printf(1, "\tPatching header for slower demon/cygnos UART speed\n");
		opts = 1;
	}
	if (xb.type == 2) {
		opts |= xb.bootFlags & 7;
		if (xb.bootFlags & 8)
			opts |= 1;
		if (xb.dualButton == xb.xellButton || xb.dualButton == xb.xellAltButton)
			xb.dualButton = 0;
	} else
		xb.dualButton = 0;
	xb.hdr[0x4c] = xb.dualButton;
	xb.hdr[0x4d] = opts;
	log_printf(1, "\tPatching header for xell power reason\n");
	if (xb.xellButton == xb.xellAltButton)
		xb.xellAltButton = 0;
	xb.hdr[0x4f] = xb.xellButton;
	if (xb.xellAltButton)
		log_printf(1, "\tPatching header for xell alt power reason\n");
	xb.hdr[0x4e] = xb.xellAltButton;
}

/* append the ini's addon patch files to the patches (their 0xffffffff
   terminators dropped), then the terminator and the addon byte count */
void appendAddonPatches(struct fileent *e)
{
	u32 size = e->size - 4;
	u8 *buf = malloc(0x4000);
	u32 added = 0;
	struct fileent *a;
	int i;

	memset(buf, 0xff, 0x4000);
	memcpy(buf, e->data, size);
	for (i = 0; i < xb.nAddons; i++) {
		a = &addons[i];
		if (!loadBinFile(a)) {
			if (!(a->size & 3)) {
				if (getBeU32(a->data + a->size - 4) == 0xffffffff)
					a->size -= 4;
				if (size + a->size <= 0x4000) {
					memcpy(buf + size, a->data, a->size);
					added += a->size;
					size += a->size;
				} else
					log_printf(0, "\n***** ERROR: could not append %s%s into patches, not enough room!\n\n",
						   xb.binDir, a->name);
			} else
				log_printf(0, "\n***** ERROR: could %s%s size 0x%x is not a multiple of 4, discarding patch data!\n\n",
					   xb.binDir, a->name, a->size);
		} else
			log_printf(0, "\n***** WARNING: could not load addon patch %s%s!\n\n", xb.binDir, a->name);
	}
	*(u32 *)(buf + size) = 0xffffffff;
	setBeU32(added, buf + size + 4);
	size += 8;
	if (e->data)
		free(e->data);
	e->data = buf;
	e->size = size;
	if (xb.nAddons)
		log_printf(1, "added 0x%x bytes to patches via %d external patch files\n"
			   "    patches now 0x%x bytes total with addon byte count appended\n", added, xb.nAddons, size);
}

/* what a power-on reason code is; 1 for an unknown one.  Console types
   above 4 (slims) have different USB ports */
int logPowerButton(int reason, const char *use)
{
	switch (reason) {
	case 0x11:
		log_printf(1, "    - console power button is being used to %s \n", use);
		break;
	case 0x12:
		log_printf(1, "    - console DVD eject button is being used to %s \n", use);
		break;
	case 0x20:
		log_printf(1, "    - IR remote power button is being used to %s \n", use);
		break;
	case 0x22:
		log_printf(1, "    - IR remote guide/X button is being used to %s \n", use);
		break;
	case 0x24:
		log_printf(1, "    - IR remote windows button is being used to %s \n", use);
		break;
	case 0x41:
		log_printf(1, "    - KIOSK debug pin is being used to %s \n", use);
		break;
	case 0x55:
		log_printf(1, "    - wireless controller powering on console is being used to %s \n", use);
		break;
	case 0x56:
		if ((xb.flags & 7) > 4)
			log_printf(1, "wired controller (front left usb port) is being used to %s \n", use);
		else
			log_printf(1, "wired controller (front top usb port) is being used to %s \n", use);
		break;
	case 0x57:
		if ((xb.flags & 7) <= 4)
			log_printf(1, "wired controller (front bottom usb port) is being used to %s \n", use);
		else
			log_printf(1, "wired controller (front right usb port) is being used to %s \n", use);
		break;
	case 0x58:
		if ((xb.flags & 7) > 4)
			log_printf(1, "wired controller (rear middle usb port) is being used to %s \n", use);
		else
			log_printf(1, "wired controller (INVALID FOR FATS!!) is being used to %s \n", use);
		break;
	case 0x59:
		if ((xb.flags & 7) > 4)
			log_printf(1, "wired controller (rear top usb port) is being used to %s \n", use);
		else
			log_printf(1, "wired controller (INVALID FOR FATS!!) is being used to %s \n", use);
		break;
	case 0x5a:
		if ((xb.flags & 7) <= 4)
			log_printf(1, "wired controller (rear usb port) is being used to %s \n", use);
		else
			log_printf(1, "wired controller (rear bottom usb port) is being used to %s \n", use);
		break;
	default:
		return 1;
	}
	return 0;
}

/* drop the first two patch sets (each a list of {addr, count, words}
   ended by 0xffffffff) from the patches file */
void fixupPatchSet(void)
{
	struct fileent *e = &xb.files[findFile(23)];
	u8 *p = e->data;
	u32 off, i;
	int n = 0;

	log_printf(1, "Fixing up patch set...");
	off = 0;
	while (off < e->size) {
		if (n == 2) {
			for (i = 0; i < e->size - off; i++)
				e->data[i] = e->data[off + i];
			e->size -= off;
			break;
		}
		if (getBeU32(p + off) == 0xffffffff) {
			n++;
			off += 4;
		} else
			off += getBeU32(p + off + 4) * 4 + 8;
	}
	log_printf(1, "Done!\n");
}

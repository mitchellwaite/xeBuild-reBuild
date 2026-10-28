/*
 * fileutil.c: byte order, buffer search, hex parsing, file and log helpers
 *
 * Many helpers follow the author's util.c from cOzInABox/XeBuild
 * (tools/opt_idx/opt_idx/util.cpp, tools/su_check/su_check/util.c):
 * MIT License, Copyright (c) 2026 [cOz].
 *
 * readFileIn needs compiler hints to match (see the comment above it).
 */

int _mkdir(const char *path);	/* msvcrt, called through its import stub */
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "xebuild.h"
typedef int BOOL;
#define TRUE 1
#define FALSE 0

void log_printf(unsigned int level, const char *fmt, ...);
BOOL validateString(char* nString);

const char *consoleTypeStr[] = {
	"Unknown", "Xenon", "Zephyr", "Falcon", "Jasper", "Trinity", "Corona",
	"Winchester"
};

const char *getConsoleTypeStr(int type)
{
	if (type <= 6)
		return consoleTypeStr[type];
	return consoleTypeStr[0];
}

unsigned short getBeU16(const unsigned char *p)
{
	return (p[0] << 8) | p[1];
}

unsigned int getBeU32(const unsigned int *p)
{
	return __builtin_bswap32(*p);
}

unsigned long long getBeU64(const unsigned long long *p)
{
	return __builtin_bswap64(*p);
}

unsigned int getLeU32(const unsigned int *p)
{
	return *p;
}

unsigned char *setBeU16(unsigned short v, unsigned char *p)
{
	p[0] = v >> 8;
	p[1] = v;
	return p;
}

unsigned char *setBeU32(unsigned int v, unsigned char *p)
{
	p[0] = v >> 24;
	p[1] = v >> 16;
	p[2] = v >> 8;
	p[3] = v;
	return p;
}

unsigned char *setBeU64(unsigned long long v, unsigned char *p)
{
	int i;
	for(i = 0; i < 8; i++)
	{
		p[7-i] = v&0xFF;
		v = v>>8;
	}
	return p;
}

void display_buffer_hex(const unsigned char *buf, unsigned int len, unsigned int level)
{
	int i;

	for (i = 0; i < len; i++) {
		if (i % 16 == 0)
			log_printf(level, "\n  ");
		log_printf(level, " %02X", buf[i]);
	}
	log_printf(level, "\n");
}

void dump_buffer_hex(const char *name, const void *buf, size_t size)
{
	FILE *f;

	log_printf(1, "dump buffer: n:'%s' b:0x%x s:0x%x\n", name, buf, size);
	if (name && buf && size) {
		f = fopen(name, "wb");
		if (f) {
			fwrite(buf, size, 1, f);
			fclose(f);
		} else
			log_printf(1, "fopen ERROR\n");
	} else
		log_printf(1, "dump buffer arg error\n");
	log_printf(1, "dump OK\n");
}

int writeFile(const char *name, const void *buf, size_t size)
{
	FILE *f;
	int ret = 0;

	if (buf && name && size) {
		f = fopen(name, "wb");
		if (f) {
			ret = fwrite(buf, size, 1, f) == 1;
			fclose(f);
		}
	}
	return ret;
}

int writeFileIn(const char *dir, const char *name, const void *buf, size_t size)
{
	char path[1024];

	if (dir && name && buf) {
		strcpy(path, dir);
		strcat(path, name);
		return writeFile(path, buf, size);
	}
	return 0;
}

int writeKeyFile(const char *dir, const char *name, const unsigned char *key)
{
	char path[1024];
	FILE *f;
	int i;

	if (dir && name && key) {
		strcpy(path, dir);
		strcat(path, name);
		f = fopen(path, "wb");
		if (f) {
			for (i = 0; i < 16; i++)
				fprintf(f, "%02X", key[i]);
			fprintf(f, "\n");
			fclose(f);
			return 1;
		}
	}
	return 0;
}

int writeFuseFile(const char *dir, const char *name, const unsigned char *fuses)
{
	char path[1024];
	FILE *f;
	int i, n = 0;

	if (dir && name && fuses) {
		strcpy(path, dir);
		strcat(path, name);
		f = fopen(path, "wb");
		if (f) {
			for (i = 0; i < 96; i++) {
				if (i % 8 == 0) {
					fprintf(f, "\nfuseset %02d: ", n);
					n++;
				}
				fprintf(f, "%02X", fuses[i]);
			}
			fprintf(f, "\n");
			fclose(f);
			return 1;
		}
	}
	return 0;
}

unsigned char *findInst(unsigned char *buf, int len, const unsigned char *pat, int patlen)
{
	int i, j;

	for (i = 0; i <= len - patlen; i++) {
		if (buf[i] == pat[0]) {
			for (j = 0; j < patlen; j++)
				if (buf[i + j] != pat[j])
					j = patlen + 1;
			if (j == patlen)
				return &buf[i];
		}
	}
	return NULL;
}

int countInst(unsigned char *buf, int len, const unsigned char *pat, int patlen)
{
	int count = 0, off = 0;
	unsigned char* ptr;
	while((off < len) && ((len-off) >= patlen))
	{
		ptr = findInst(&buf[off], len-off, pat, patlen);
		if(ptr == NULL)
			off = len;
		else
		{
			count++;
			off = (ptr-buf)+patlen;
		}
	}
	return count;
}

int findInstExists(unsigned char *buf, int len, const unsigned char *pat, int patlen)
{
	int i, j;

	for (i = 0; i <= len - patlen; i++) {
		if (buf[i] == pat[0]) {
			for (j = 0; j < patlen; j++)
				if (buf[i + j] != pat[j])
					j = patlen + 1;
			if (j == patlen)
				return 1;
		}
	}
	return 0;
}

int replaceInst(unsigned char *buf, int len, const unsigned char *pat, int patlen,
		  const void *rep, size_t replen)
{
	unsigned char *p = findInst(buf, len, pat, patlen);

	if (!p)
		return 0;
	memcpy(p, rep, replen);
	return 1;
}

// converts a ascii hex char to a nibble
unsigned char myatox(char c)
{
	if((c >= 0x61) && (c <= 0x66)) // a thru f
		return (unsigned char)(c-0x57);
	else if((c >= 0x30) && (c <= 0x39)) // 0 thru 9
		return (unsigned char)(c-0x30);
	else if((c >= 0x41) && (c <= 0x46)) // A thru F
		return (unsigned char)(c-0x37);
	return 0xFF;
}

// converts char nibble pair into a uchar
unsigned char myatox8(char* dat)
{
	unsigned char retval;
	retval	= myatox(dat[0]) & 0xF;
	retval = (retval<<4)+(myatox(dat[1]) & 0xF);
	return retval;
}

// converts (up to) 16 uchar nibbles into a u32
u32 myatox32(char* dat, u32 defValue)
{
	u32 retval = 0, i;
	unsigned char res;
	for(i = 0; i < 16; i++)
	{
		if((dat[i]&0xFF) == 0x0)
			i = 16;
		else
		{
			res = (myatox(dat[i]&0xFF));
			if((res&0xFF) == 0xFF) // abort in case of bad value
			{
				i = 16;
				retval = defValue;
			}
			else
				retval = (retval<<4)+(res&0xF);
		}
	}
	return retval;
}

// converts uppercase to lower case
char myatol(char c)
{
	char ret = c;
	if((c>0x40)&&(c<0x5A)) // A thru Z
		ret = c+0x20;
	return ret;
}

// converts a decimal or 0x-prefixed hex string into a u32
// (opt_idx's myatou32; this build also tests for an upper case 'X' after
// myatol, which can never match but changes gcc's branch estimate)
u32 myatou32(char* dat, u32 defValue)
{
	if(((dat[0]&0xFF) == '0')&&((myatol(dat[1]&0xFF) == 'x')||(myatol(dat[1]&0xFF) == 'X')))
	{
		if(validateString(&dat[2]))
			return myatox32(&dat[2], defValue);
	}
	else
	{
		if(validateString(dat))
			return atoi((const char*)dat);
	}
	return defValue;
}

u32 myatoh32(char* dat, u32 defValue)
{
	if((strlen(dat) > 2)&&((dat[0]&0xFF) == '0')&&(myatol(dat[1]&0xFF) == 'x'))
		dat = &dat[2];
	if(validateString(dat))
		return myatox32(dat, defValue);
	return defValue;
}

// checks chars are valid
BOOL validateString(char* nString)
{
	int i, len;
	if(nString == NULL)
		return FALSE;
	len = strlen(nString);
	if((nString[0] != 0x0) && (len != 0))
	{
		for(i = 0; i < len; i++)
		{
			if(myatox(nString[i]) == 0xFF)
				return FALSE;
		}
		return TRUE;
	}
	return FALSE;
}

int checkZeros(const unsigned char *p, unsigned int len)
{
	unsigned int i;

	for (i = 0; i < len; i++)
		if (p[i])
			return 0;
	return 1;
}

void memcpyrev(unsigned char *dst, const unsigned char *src, int len)
{
	int i, j;

	for (i = 0, j = len - 1; i < len; i++, j--)
		dst[i] = src[j];
}

long getFileSize(FILE *f)
{
	long size = 0;

	if (f) {
		fseek(f, 0, SEEK_END);
		size = ftell(f);
		rewind(f);
	}
	return size;
}

long getFileSizeName(const char *name)
{
	long size = 0;
	FILE *f = fopen(name, "rb");

	if (f) {
		fseek(f, 0, SEEK_END);
		size = ftell(f);
		fclose(f);
	}
	return size;
}

long long getFileSize64(FILE *f)
{
	long long size = 0;

	if (f) {
		fseeko64(f, 0, SEEK_END);
		size = ftello64(f);
		rewind(f);
	}
	return size;
}

long long getFileSize64Name(const char *name)
{
	long long size = 0;
	FILE *f = fopen(name, "rb");

	if (f) {
		fseeko64(f, 0, SEEK_END);
		size = ftello64(f);
		fclose(f);
	}
	return size;
}

int FileExists(const char *name)
{
	FILE *f = fopen(name, "rb");

	if (f) {
		fclose(f);
		return 1;
	}
	return 0;
}

int FileExistsIn(const char *dir, const char *name)
{
	char path[1024];

	strcpy(path, dir);
	strcat(path, "/");
	strcat(path, name);
	return FileExists(path);
}

void *FileToBuffer(const char *name, size_t *psize)
{
	FILE *f;
	void *buf = NULL;
	size_t size = 0;

	if (name == NULL)
		return NULL;
	f = fopen(name, "rb");
	if (f) {
		size = getFileSize(f);
		buf = malloc(size);
		if (buf)
			fread(buf, size, 1, f);
		else {
			log_printf(1, "unable to allocate file buffer of 0x%x size!\n", size);
			size = 0;
		}
		fclose(f);
	}
	if (psize)
		*psize = size;
	return buf;
}

size_t readFileTo(const char *name, void *buf, size_t size)
{
	FILE *f;
	int ret = 0;

	if (name && buf && size) {
		f = fopen(name, "rb");
		if (f) {
			if (size <= (size_t)getFileSize(f)) {
				fread(buf, size, 1, f);
				fclose(f);
				ret = size;
			}
		}
	}
	return ret;
}

u32 readFileInTo(const char *dir, const char *name, void *buf, int size)
{
	char path[1024];

	if (dir && name && buf) {
		sprintf(path, "%s%s", dir, name);
		return readFileTo(path, buf, size);
	}
	return 0;
}

/*
 * readFileIn: the plain C (one ok flag, a single return of buf) gives the
 * reference control flow, but gcc's branch estimates and register choices
 * differ.  The hints below only steer those; none of them emits code:
 * - rf_hint() is a guarded call at profile_estimate time (PRED_CALL), which
 *   cancels the call heuristic from log_printf on the alloc-failure edge.
 *   It is inlined later (hence no-early-inlining) and its store to the
 *   write-only rf_sink is deleted with the variable.
 * - __builtin_expect probabilities come from build.sh's
 *   --param builtin-expect-probability for this file.
 * - The empty asm ties size/buf/alloc to edi/ebx/esi as in the reference.
 */
static int rf_sink;
static void rf_hint(void) { rf_sink = 1; }

__attribute__((optimize("no-early-inlining")))
void *readFileIn(const char *dir, const char *name, size_t *psize, size_t align)
{
	char path[1024];
	void *buf = NULL;
	size_t size, alloc;
	int ok = 0;

	if (dir == NULL || name == NULL)
		return NULL;
	sprintf(path, "%s%s", dir, name);
	size = getFileSizeName(path);
	alloc = size;
	if (align) {
		alloc = size + align - 1;
		alloc &= -align;
	}
	buf = calloc(alloc, 1);
	if (buf == NULL)
		log_printf(1, "unable to allocate file buffer of 0x%x size!\n", alloc);
	else {
		__asm__("" : : "D" (size), "b" (buf), "S" (alloc));
		rf_hint();
		if (__builtin_expect(size != 0, 0)) {
			if (readFileTo(path, buf, size) == size)
				ok = 1;
		} else
			ok = 1;
	}
	if (psize) {
		if (ok)
			*psize = alloc;
		else
			*psize = 0;
	}
	if (__builtin_expect(!ok && buf, 0)) {
		free(buf);
		buf = NULL;
	}
	return buf;
}

unsigned int calcConfigSum(const unsigned char *p)
{
	unsigned short sum = 0;
	int i;

	for (i = 16; i < 268; i++)
		sum += p[i];
	sum = ~sum;
	return ((unsigned int)sum << 24) + (((unsigned int)sum << 8) & 0xff0000);
}

unsigned int sumBytes(const unsigned char *p, unsigned int len)
{
	unsigned int i, sum = 0;

	for (i = 0; i < len; i++)
		sum += p[i];
	return sum;
}

void showExpectedFuses(unsigned int flags, unsigned short cb, unsigned char *fuses, int clear)
{
	u32 type = flags >> 24;
	u8 cseq = flags >> 16;
	u16 allow = flags;
	u64 mask, bit;
	int i;

	log_printf(1, "CB %d seq 0x%08x type: 0x%02x cseq: 0x%02x allow: 0x%04x\n",
		   cb, flags, type, cseq, allow);
	log_printf(1, "\texpected fuses:\n");
	log_printf(1, "\tfuseset 00: C0FFFFFFFFFFFFFF\n");
	if (fuses)
		setBeU64(0xC0FFFFFFFFFFFFFFULL, fuses);
	switch (type) {
	case 0:
		log_printf(1, "\tfuseset 01: 0F0F0F0F0F0F0F0F (devkit)\n");
		if (fuses)
			setBeU64(0x0F0F0F0F0F0F0F0FULL, fuses + 8);
		break;
	case 1:
		log_printf(1, "\tfuseset 01: 0F0F0F0F0F0F0FF0 (retail)\n");
		if (fuses)
			setBeU64(0x0F0F0F0F0F0F0FF0ULL, fuses + 8);
		break;
	case 2:
		log_printf(1, "\tfuseset 01: 0F0F0F0F0F0FF00F (testkit)\n");
		if (fuses)
			setBeU64(0x0F0F0F0F0F0FF00FULL, fuses + 8);
		break;
	case 3:
		log_printf(1, "\tfuseset 01: 0F0F0F0F0F0FF0F0 (retail slim)\n");
		if (fuses)
			setBeU64(0x0F0F0F0F0F0FF0F0ULL, fuses + 8);
		break;
	default:
		log_printf(1, "\tfuseset 01: ???????????????? never seen console type 0x%02x\n", type);
		break;
	}
	if (cseq == 0 && allow == 0)
		log_printf(1, "\tfuseset 02: 0000000000000000\n");
	else {
		mask = 0;
		log_printf(1, "\tfuseset 02: %016llX (sequence)\n", 0xFULL << ((16 - cseq) * 4));
		for (i = 0; i < 16; i++) {
			if (allow & (u16)(1 << i)) {
				bit = 0xF000000000000000ULL >> (i * 4);
				log_printf(1, "\tfuseset 02: %016llX (allow cseq %d)\n", bit, i + 1);
				mask |= bit;
			}
		}
		if (fuses)
			setBeU64(mask, fuses + 16);
	}
	if (fuses && clear) {
		setBeU64(0x0F0F0F0F0F0F0F0FULL, fuses + 8);
		setBeU64(0, fuses + 16);
	}
}

void showFuses(unsigned int level, const char *title, const unsigned char *fuses)
{
	int i, n = 0;

	if (title)
		log_printf(level, title);
	for (i = 0; i < 96; i++) {
		if (i % 8 == 0) {
			log_printf(level, "\n\tfuseset %02d: ", n);
			n++;
		}
		log_printf(level, "%02X", fuses[i]);
	}
	log_printf(level, "\n");
}

void showKey(unsigned int level, const unsigned char *key)
{
	int i;

	if (key)
		for (i = 0; i < 16; i++)
			log_printf(level, "%02X", key[i]);
}

void showMac(unsigned int level, const unsigned char *mac)
{
	int i;

	for (i = 0; i < 6; i++) {
		log_printf(level, "%02x", mac[i]);
		if (i != 5)
			log_printf(level, ":");
	}
}

void showHexPairs(unsigned int level, const char *s)
{
	int i, len = strlen(s);

	for (i = 0; i < len; i++) {
		log_printf(level, "%c", s[i]);
		if (i + 1 == len)
			break;
		if ((i + 1) % 2 == 0)
			log_printf(level, ":");
	}
}

void writeSha1File(char *out, const char *src, const unsigned char *sha)
{
	char hex[48];
	char line[1024];
	FILE *f;
	int i;

	if (!out[0]) {
		strcpy(out, src);
		strcat(out, ".sha1");
	}
	f = fopen(out, "wb");
	if (f) {
		line[0] = 0;
		for (i = 0; i < 20; i += 5) {
			sprintf(hex, "%02x%02x%02x%02x%02x", sha[i], sha[i + 1], sha[i + 2],
				sha[i + 3], sha[i + 4]);
			strcat(line, hex);
		}
		fwrite(line, strlen(line), 1, f);
		sprintf(line, " *%s\n", src);
		fwrite(line, strlen(line), 1, f);
		fclose(f);
	} else
		log_printf(0, "\n\n***** ERROR: could not open %s to write SHA-1! Skipping!", out);
}

int createDir(const char *path)
{
	int err;

	if (path == NULL || _mkdir(path) == 0)
		return 1;
	err = errno;
	if (err == EEXIST) {
		log_printf(0, "***** WARNING: reusing folder %s!\n", path);
		return 1;
	}
	log_printf(0, "\n\n***** ERROR: cannot create %s! (error %d)\n", path, err);
	return 0;
}

unsigned int makeBranch(unsigned int from, unsigned int to, int link)
{
	unsigned int insn = 0x48000000 | ((to - from) & 0x03FFFFFC);

	if (link)
		insn |= 1;
	return insn;
}

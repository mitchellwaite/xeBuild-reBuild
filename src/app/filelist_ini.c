/* filelist_ini: reading the file list ini.  Mixed object: the functions here
   are spliced into filelist_ini.s (re/splice.py), which still holds the rest,
   and the data. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <dirent.h>

typedef unsigned char u8;

struct xebuild {
	u8 pad000[0xeac];
	char baseDir[0x400];		/* eac */
};
extern struct xebuild xb;
extern unsigned char *iniBuf;
extern int iniSize;

extern char fnSmc[32], fnKv[32], fnPatches[32];
int iniPreParse(unsigned char *buf, int size);
void log_printf(int level, const char *fmt, ...);
long getFileSize(FILE *f);
char myatol(char c);
int validateString(char *s);
unsigned int myatou32(char *dat, unsigned int def);

/* filelist_ini.s strings */
extern const char fi_44fb84[];	/* "rb" */
extern const char fi_44fbb0[];	/* "******* ERROR loading %s, unable to allocate memory
" */
extern const char fi_450258[];	/* "true" */
extern const char fi_45025d[];	/* "false" */
extern const char fi_450264[];	/* "
------ parsing user ini at '%s' ------
" */
extern const char fi_450290[];	/* "
******* WARNING: could not open user ini at '%s', skipping
" */
extern const char fi_4502cd[];	/* "loading file..." */
extern const char fi_4502dd[];	/* "done!
" */
extern const char fi_4502e4[];	/* "***** WARNING: User ini %s
appears to be a multi byte file, ..." */
extern const char fi_450347[];	/* "pre-parsing and sanitizing
" */

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

/* filelist_ini.s's _validChars; gcc folds [0] to 'A' from this copy, which
   re/splice.py drops (static, so it isn't .globl; a string, so gcc emits it
   as .ascii; 74 chars, no NUL) */
static const unsigned char validChars[74] =
	"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,;[]_\n\\/-$:";

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
		if (buf[i] == ';') {
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
		for (j = 0; j < 18; j++)
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
	if (strnicmp(val, fi_450258, 4) == 0)
		return 1;
	if (strnicmp(val, fi_45025d, 5) == 0)
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
	if (strnicmp(val, fi_450258, 4) == 0)
		return NULL;
	if (strnicmp(val, fi_45025d, 5) != 0)
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
	log_printf(1, fi_450264, path);
	f = fopen(path, fi_44fb84);
	if (f == NULL) {
		log_printf(1, fi_450290, path);
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
	log_printf(1, fi_4502cd, path);
	fread(iniBuf, iniSize, 1, f);
	fclose(f);
	log_printf(1, fi_4502dd, path);
	if (iniBuf[0] == 0xff || iniBuf[1] == 0xff) {
		log_printf(0, fi_4502e4, path);
		free(iniBuf);
		iniBuf = NULL;
		iniSize = 0;
		return 0;
	}
	iniBuf[iniSize] = 0xff;
	log_printf(1, fi_450347);
	iniSize = iniPreParse(iniBuf, iniSize);
	log_printf(1, fi_4502dd);
	iniBuf[iniSize] = 0;
	return 1;
}

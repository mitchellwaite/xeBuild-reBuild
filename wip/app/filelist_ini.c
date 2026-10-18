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

void log_printf(int level, const char *fmt, ...);
long getFileSize(FILE *f);
char myatol(char c);
int validateString(char *s);
unsigned int myatou32(char *dat, unsigned int def);

const unsigned char validChars[74] = {
	'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
	'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
	'0','1','2','3','4','5','6','7','8','9','.', ',', ';', '[', ']', '_', '\n', '\\', '/', '-', '$', ':'
};

/* fix the case of the file names in the base dir that need it */
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

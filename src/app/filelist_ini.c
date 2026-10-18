/* filelist_ini: reading the file list ini.  Mixed object: the functions here
   are spliced into filelist_ini.s (re/splice.py), which still holds the rest,
   and the data. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned char u8;

struct xebuild {
	u8 pad000[0xeac];
	char baseDir[0x400];		/* eac */
};
extern struct xebuild xb;
extern unsigned char *iniBuf;
extern int iniSize;

void fixFileCase(void);
int iniPreParse(unsigned char *buf, int size);
void log_printf(int level, const char *fmt, ...);
long getFileSize(FILE *f);

/* filelist_ini.s strings */
extern const char fi_44fb84[];	/* "rb" */
extern const char fi_44fbb0[];	/* "******* ERROR loading %s, unable to allocate memory
" */
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

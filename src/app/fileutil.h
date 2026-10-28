/* fileutil.h: fileutil.c's functions that other objects use */
#ifndef FILEUTIL_H
#define FILEUTIL_H

#include <stdio.h>
#include "xebuild.h"

const char *getConsoleTypeStr(int type);
unsigned short getBeU16(const unsigned char *p);
unsigned int getBeU32(const u8 *p);
unsigned int getLeU32(const u8 *p);
unsigned char *setBeU16(unsigned short v, unsigned char *p);
unsigned char *setBeU32(unsigned int v, unsigned char *p);
unsigned char *setBeU64(unsigned long long v, unsigned char *p);
void display_buffer_hex(const unsigned char *buf, unsigned int len,
	unsigned int level);
int writeFile(const char *name, const void *buf, size_t size);
int writeFileIn(const char *dir, const char *name, const void *buf,
	size_t size);
int writeKeyFile(const char *dir, const char *name, const unsigned char *key);
int writeFuseFile(const char *dir, const char *name,
	const unsigned char *fuses);
unsigned char *findInst(unsigned char *buf, int len, const void *pat,
	int patlen);
int countInst(unsigned char *buf, int len, const void *pat, int patlen);
int findInstExists(const unsigned char *buf, int len, const void *pat,
	int patlen);
int replaceInst(unsigned char *buf, int len, const void *pat, int patlen,
	const void *rep, size_t replen);
unsigned char myatox8(const char* dat);
u32 myatox32(const char* dat, u32 defValue);
char myatol(char c);
u32 myatou32(const char* dat, u32 defValue);
u32 myatoh32(const char* dat, u32 defValue);
int validateString(const char* nString);
int checkZeros(const unsigned char *p, unsigned int len);
void memcpyrev(unsigned char *dst, const unsigned char *src, int len);
long getFileSize(FILE *f);
long long getFileSize64(FILE *f);
int FileExists(const char *name);
int FileExistsIn(const char *dir, const char *name);
void *FileToBuffer(const char *name, size_t *psize);
unsigned int calcConfigSum(const unsigned char *p);
unsigned int sumBytes(const unsigned char *p, unsigned int len);
void showExpectedFuses(unsigned int flags, unsigned short cb,
	unsigned char *fuses, int clear);
void showFuses(int level, const char *title, const unsigned char *fuses);
void showKey(int level, const unsigned char *key);
void showMac(unsigned int level, const unsigned char *mac);
void showHexPairs(unsigned int level, const char *s);
void writeSha1File(char *out, const char *src, const unsigned char *sha);
int createDir(const char *path);

#endif

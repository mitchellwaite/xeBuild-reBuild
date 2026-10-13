/* mode_ini: `xeBuild ini`, writes an SU's bootloader and flash file hashes to _SU.ini */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>

typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;

void log_set_verbose(int v);
void log_printf(int level, const char *fmt, ...);
u32 crc32(const u8 *buf, int len);
u16 getBeU16(const u8 *p);
u32 getBeU32(const u8 *p);

const char *suGetDir(void);
int suLoad(const char *path);
int suGetCF(u8 **data, u32 *len);
int suGetCG(u8 **data, u32 *len);
u32 suFirstFile(char *name, int *idx);
int suNextFile(char *name, int *idx);
int suGetFile(const char *name, u8 **data, u32 *len);
int loadKeyFile(void *keys, const char *dir, const char *name);
int checkKeys(void *keys);

extern char separator[];
extern int promptEnter;

static char iniFile[1024];
static char iniDir[1024];

void ini_usage(void)
{
	log_printf(0, separator);
	log_printf(0, "Usage   :\n   %s ini [systeUpdateConPath]\n\n", "xeBuild");
	log_printf(0, "Examples:\n");
	log_printf(0, "   %s ini ./16547/\n", "xeBuild");
	log_printf(0, "   %s ini c:\\16547\\$SystemUpdate\n", "xeBuild");
	log_printf(0, "   %s ini z:\\someWeirdPath\\su20076000_00000000\n", "xeBuild");
	log_printf(0, "      when specifying path, either provide relative path or full path\n");
	log_printf(0, "      to either the SU container, a folder with $SystemUpdate folder in it,\n");
	log_printf(0, "      or a folder with flash update named 'su20076000_00000000' in it.\n");
	log_printf(0, "      Hash data will be output to the folder with the SU in it named _SU.ini\n");
	log_printf(0, separator);
	if (promptEnter) {
		log_printf(0, "\npress <enter> to quit...\n");
		fgetc(stdin);
	}
	exit(1);
}

void iniSetFile(const char *path)
{
	if (path) {
		strcpy(iniFile, path);
		remove(iniFile);
		log_printf(0, "output set to file '%s'\n", iniFile);
	}
}

void iniPrintf(const char *fmt, ...)
{
	char buf[512];
	va_list ap;
	FILE *f;

	va_start(ap, fmt);
	vsnprintf(buf, 512, fmt, ap);
	printf(buf);
	f = fopen(iniFile, "a");
	if (f) {
		fprintf(f, buf);
		fclose(f);
	}
}

u32 iniWriteFlashfs(void)
{
	char name[44];
	int idx;
	u8 *data;
	u32 len;
	u32 crc;

	iniPrintf("[flashfs]\n");
	if (!suFirstFile(name, &idx))
		goto unparsed;
	idx = 0;
	while (suNextFile(name, &idx)) {
		if (!suGetFile(name, &data, &len))
			continue;
		if (!strnicmp(name, "$flash_", 7)) {
			crc = crc32(data, len);
			if (!strnicmp(name + 7, "xenonclatin.xttp", 16))
				iniPrintf("xenonclatin.xtt,d5d17ff5; added by xebuild\n");
			else if (!strnicmp(name + 7, "xenonjklatin.xttp", 17))
				iniPrintf("xenonjklatin.xtt,dde4a14c; added by xebuild\n");
			else if (!strnicmp(name + 7, "ximedic.xexp", 16))
				iniPrintf("ximedic.xex,1d992bfb; added by xebuild\n");
			__asm__("" : : "D"(&data));
			if (!strnicmp(name + 7, "systemupdate", 12))
				iniPrintf(";%s,%08x; commented by xebuild\n", name + 7, crc);
			else if (!strnicmp(name + 7, "oddupd", 6))
				iniPrintf(";%s,%08x; commented by xebuild\n", name + 7, crc);
			else
				iniPrintf("%s,%08x\n", name + 7, crc);
		} else
			iniPrintf(";%s,%08x; commented by xebuild\n", name, crc32(data, len));
	}
	__asm__("" : : "r"(&len));
	return 1;
unparsed:
	log_printf(0, "***** ERROR SU seems loaded, but is unparsed!\n");
	return 0;
}

u32 iniWriteBl(void)
{
	u8 *cf = 0, *cg = 0;
	u32 cfLen, cgLen;
	int ver, ret;

	if (suGetCF(&cf, &cfLen)) {
		if (suGetCG(&cg, &cgLen)) {
			ver = getBeU16(cf + 20);
			cfLen = getBeU32(cf + 12);
			cgLen = getBeU32(cg + 12);
			memset(cf + 32, 0, 528);
			memset(cg + 16, 0, 16);
			log_printf(0, "Attempting to output info to file %s\n\n", iniFile);
			iniPrintf("[version]\n%d\n\n[bl]\n", ver);
			iniPrintf("cf_%d.bin,%08x\n", ver, crc32(cf, cfLen));
			iniPrintf("cg_%d.bin,%08x\n\n", ver, crc32(cg, cgLen));
			ret = 1;
		} else {
			log_printf(0, "***** ERROR: could not get CG data from SU!\n");
			ret = 0;
		}
	} else {
		log_printf(0, "***** ERROR: could not get CF data from SU!\n");
		ret = 0;
	}
	if (cf)
		free(cf);
	if (cg)
		free(cg);
	return ret;
}

int mode_ini(int argc, char **argv)
{
	int keys[10];

	log_set_verbose(1);
	memset(keys, 0, sizeof(keys));
	if (loadKeyFile(keys, 0, "1blkey.txt") && !checkKeys(keys)) {
		log_printf(0, "\n***** WARNING: 1blkey.txt not found or invalid, cannot proceed.\n\n");
		return 4;
	}
	if (argc != 1)
		ini_usage();
	if (suLoad(argv[0])) {
		log_printf(0, "SU loaded successfully!\n");
		strcpy(iniDir, suGetDir());
		strcat(iniDir, "_SU.ini");
		iniSetFile(iniDir);
		if (iniWriteBl()) {
			if (iniWriteFlashfs())
				log_printf(0, "\nCompleted output to %s\n", iniFile);
		} else
			log_printf(0, "***** ERROR unable to get CF/CG data from SU!\n");
		return 0;
	}
	log_printf(0, "Error loading SU!\n");
	return 4;
}

/* mode_update: `xeBuild update`, rebuilds and reflashes a console over the network.
   Mixed object: the functions here are spliced into mode_update.s
   (re/splice.py), which still holds the rest and the data, so strings
   and variables are extern names for the .s's.  wip/app/mode_update.c
   is the whole draft. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;

#define SWAP32(x) (((x) << 24) + (((x) << 8) & 0xff0000) + (((x) >> 8) & 0xff00) + ((x) >> 24))

/* a file fetched from the console */
struct netfile {
	u8 *data;
	int size;
};

/* the parts of main.c's struct xebuild used here */
struct xebuild {
	int mode;			/* 000 */
	u32 flags;			/* 004 console type (& 7), NAND flags */
	u32 type;			/* 008 build type */
	u32 kernel;			/* 00c */
	int glitch2;			/* 010 */
	int glitch2mfg;			/* 014 */
	u8 pad018[0x0d4 - 0x018];
	u32 numBad;			/* 0d4 */
	u32 badBlocks[32];		/* 0d8 */
	u32 badRemap[32];		/* 158 */
	struct netfile blmod;		/* 1d8 */
	struct netfile bldrs;		/* 1e0 raw bootloaders (glitch) */
	int haveBldrs;			/* 1e8 */
	struct netfile mobile[11];	/* 1ec MobileB-J, Statistics, Manufacturing */
	struct netfile smc;		/* 244 */
	struct netfile kv;		/* 24c */
	struct netfile f254;		/* 254 */
	struct netfile smcConfig;	/* 25c */
	u8 pad264[0x29c - 0x264];
	void *pub1bl;			/* 29c */
	void *masterPub;		/* 2a0 */
	void *pubPirs;			/* 2a4 */
	void *privSb;			/* 2a8 */
	char suffix[0x400];		/* 2ac -i */
	char binDir[0x400];		/* 6ac */
	char outName[0x400];		/* aac */
	char baseDir[0x400];		/* eac */
	char dataDir[0x400];		/* 12ac -f */
	u8 pad16ac[0x46df4 - 0x16ac];
	char patches[16][0x42c];	/* 46df4 -a */
	char blSuffix[0x40];		/* 4b0b4 -r */
	int numPatches;			/* 4b0f4 */
	u8 pad4b0f8[0x4f144 - 0x4b0f8];
	char flashFiles[10][22];	/* 4f144 */
	u8 *flashBuf[10];		/* 4f220 */
	int flashSize[10];		/* 4f248 */
	u8 pad4f270[0x4f2c0 - 0x4f270];
	u32 numFlashFiles;		/* 4f2c0 */
};

/* the console's info response (net.c) */
struct consoleinfo {
	u32 version;			/* 000 */
	u32 kernel;			/* 004 */
	u32 f008;			/* 008 2: has blmod, 4: has addons */
	u32 bootstrap;			/* 00c */
	u32 hwFlags;			/* 010 */
	u32 nandType;			/* 014 */
	u32 f018;			/* 018 */
};

void log_printf(int level, const char *fmt, ...);
void log_set_name(const char *name);
void log_verbose_flag(unsigned char c);
void log_finish(void);
u16 getBeU16(const u8 *p);
u32 getBeU32(const u8 *p);
int findInstExists(const u8 *buf, int len, const void *inst, int instLen);
void *FileToBuffer(const char *name, size_t *psize);
int writeFileIn(const char *dir, const char *name, const void *buf, size_t size);
int createDir(const char *path);
int smcConfigOk(const u8 *smc);
u32 verifyExtended(void *buf, int size);
int unscramble(u8 *buf, u32 len);
u32 getSecurityFiles(const char *dir);
void setKvSalt(u8 *key);
void setSmcKey(u8 *key);
int verifyFlashFile(int i);
int parseIni(const char *path);
int parseConsoleInfo(int level, const char *dir, const char *optDir, int *update);
int buildImage(void);
int writeImage(const char *name);
u8 *imageGetBuffer(u32 *size);
void remapBadBlocks(u32 numBlocks);
void sendAvatarData(const char *dir, u32 kernel);
int netConnect(const char *ip);
struct consoleinfo *netGetInfo(void);
u8 *netGetFile(const char *name, int *len);
u8 *netGetBadBlocks(int *len);
u8 *netGetBldrs(int *len);
u32 netMount(const char *drive, const char *path);
int netUnmount(const char *drive);
int netDumpNand(const char *path);
void netTimerStart(void);
int netSendFlash(u8 *buf, u32 len);
void netReboot(int how);
void netFree(void *p);

extern struct xebuild xb;
extern char separator[];
extern int promptEnter;

extern int useConsoleAddons;

/* mode_update.s's data */
extern struct consoleinfo *info;
extern int updating;
extern int hasHdd;
extern int clean;
extern int noWrite;
extern int noAvatar;
extern int noReboot;
extern char path[260];

/* strings in mode_update.s */
extern const char mu_44c6e8[];	/* "\n------ getting bad blocks ------\n" */
extern const char mu_44c70c[];	/* "processing %d bad blocks on device\n" */
extern const char mu_44c730[];	/* "marking bad block at 0x%x\n" */
extern const char mu_44c74c[];	/* "no bad blocks found on device\n" */
extern const char mu_44c76c[];	/* "\n\n***** ERROR: unable to retrieve ..." */
extern const char mu_44c7ab[];	/* "xeBuild" */
extern const char mu_44c7b4[];	/* "Usage   :\n   %s update <switch> [<o..." */
extern const char mu_44c7e1[];	/* "Examples:\n" */
extern const char mu_44c7ec[];	/* "   %s update -f 16197 -a nofcrt\n" */
extern const char mu_44c810[];	/* "   %s update -f 16203 -d myflash -ip..." */
extern const char mu_44c844[];	/* "\nSwitches:\n" */
extern const char mu_44c850[];	/* "   -f <dir> : use different data dir..." */
extern const char mu_44c888[];	/* "   -d <dir> : dumps NAND and other d..." */
extern const char mu_44c8ca[];	/* "   -a <name>: append patches\n" */
extern const char mu_44c8e8[];	/* "   -ip <add>: force attempt to conne..." */
extern const char mu_44c918[];	/* "   -i <ext> : adds _<ext> into firmw..." */
extern const char mu_44c95c[];	/* "   -r <ext> : adds _<ext> into ini b..." */
extern const char mu_44c9a8[];	/* "   -nowrite : will not write anythin..." */
extern const char mu_44c9e8[];	/* "              without -d results of ..." */
extern const char mu_44ca2c[];	/* "   -noava   : will not send avatar d..." */
extern const char mu_44ca74[];	/* "   -clean   : secdata, extended and ..." */
extern const char mu_44cac8[];	/* "   -noreeb  : do not automatically r..." */
extern const char mu_44cb18[];	/* "   -noenter : suppresses prompt for ..." */
extern const char mu_44cb58[];	/* "   -v       : shows more info during..." */
extern const char mu_44cb90[];	/* "   -?       : shows this help\n\n" */
extern const char mu_44cbb0[];	/* "legend:\n" */
extern const char mu_44cbbc[];	/* "<name>      = name.bin contents will..." */
extern const char mu_44cc04[];	/* "<dir>       = path, absolute or rela..." */
extern const char mu_44cc58[];	/* "<ext>       = using this option woul..." */
extern const char mu_44ccc8[];	/* "              and patches_jasper_<ex..." */
extern const char mu_44cd14[];	/* "<add>       = without this option ne..." */
extern const char mu_44cd6c[];	/* "              If provided the correc..." */
extern const char mu_44cdc0[];	/* "\npress <enter> to quit...\n" */
extern const char mu_44cddb[];	/* "extended.bin" */
extern const char mu_44cde8[];	/* "secdata.bin" */
extern const char mu_44cdf4[];	/* "Statistics.settings" */
extern const char mu_44ce08[];	/* "skipping %s, -clean flag" */
extern const char mu_44ce21[];	/* "addon patch from console: %s\n" */
extern const char mu_44ce40[];	/* "***** WARNING: exceeded total number..." */
extern const char mu_44ce9c[];	/* "addons" */
extern const char mu_44cea3[];	/* "OK, received 0x%x bytes\n" */
extern const char mu_44cebc[];	/* ".\\%d\\bin\\addon.idx" */
extern const char mu_44ced0[];	/* "\n\n***** WARNING: unable to open %s..." */
extern const char mu_44cf18[];	/* "\n\n***** WARNING: addons.bin from c..." */
extern const char mu_44cf6c[];	/* "\n\n***** WARNING: Unable to retriev..." */
extern const char mu_44cfac[];	/* "\n------ getting mobile settings ---..." */
extern const char mu_44cfd4[];	/* "Mobile%c.dat" */
extern const char mu_44cfe1[];	/* "not available\n" */
extern const char mu_44cff0[];	/* "retrieving USVR\\blmod..." */
extern const char mu_44d009[];	/* "blmod" */
extern const char mu_44d010[];	/* "\n\n***** WARNING: Unable to retriev..." */
extern const char mu_44d054[];	/* "console has no available blmod\n" */
extern const char mu_44d074[];	/* "retrieving USVR\\addons..." */
extern const char mu_44d090[];	/* "skipping USVR\\addons, addons have b..." */
extern const char mu_44d0d4[];	/* "console has no available addons\n" */
extern const char mu_44d0f8[];	/* "retrieving USVR\\Static.settings (sm..." */
extern const char mu_44d12c[];	/* "usv:\\Static.settings" */
extern const char mu_44d144[];	/* "OK, received 0x%x bytes\n        ver..." */
extern const char mu_44d171[];	/* "smc_config is good!\n" */
extern const char mu_44d186[];	/* "smc_config.bin" */
extern const char mu_44d198[];	/* "\n***** ERROR: could not retrieve sm..." */
extern const char mu_44d1d3[];	/* "usv:\\%s" */
extern const char mu_44d1db[];	/* "retrieving USVR\\%s..." */
extern const char mu_44d400[];	/* "\n------ getting bootloaders ------\..." */
extern const char mu_44d424[];	/* "reading bootloader data..." */
extern const char mu_44d440[];	/* "success! Bootloader size with xell i..." */
extern const char mu_44d46e[];	/* "fbldrs.bin" */
extern const char mu_44d479[];	/* "failed!\n" */
extern const char mu_44d484[];	/* "Skipping getting bootloaders on non-..." */
extern const char mu_44d4b9[];	/* "\\SystemRoot" */
extern const char mu_44d4c5[];	/* "usv" */
extern const char mu_44d4cc[];	/* "\n***** ERROR: getting raw boot load..." */
extern const char mu_44d4fc[];	/* "\n***** ERROR: getting mobile files ..." */
extern const char mu_44d528[];	/* "\n***** ERROR: retrieving security f..." */
extern const char mu_44d55c[];	/* "\n***** ERROR: mounting remote Syste..." */
extern const char mu_44d590[];	/* "\n***** ERROR: getting bad blocks fa..." */
extern const char mu_44d5ba[];	/* "failed! received 0 bytes\n" */
extern const char mu_44d5d4[];	/* "failed! file not found on console\n" */

u32 getBadBlocks(void)
{
	u8 *list;
	int len, i;
	u32 blocks;
	u32 block;

	log_printf(1, mu_44c6e8);
	list = netGetBadBlocks(&len);
	if (!list) {
		log_printf(0, mu_44c76c);
		return 0;
	}
	if (len) {
		blocks = info->nandType / info->f018;
		log_printf(1, mu_44c70c, len / 2);
		for (i = len - 2; i >= 0; i -= 2) {
			block = getBeU16(list + i);
			log_printf(1, mu_44c730, block);
			xb.badRemap[xb.numBad] = -1;
			xb.badBlocks[xb.numBad] = block;
			xb.numBad++;
		}
		remapBadBlocks(blocks);
	} else
		log_printf(1, mu_44c74c);
	netFree(list);
	return 1;
}

void update_usage(void)
{
	log_printf(0, separator);
	log_printf(0, mu_44c7b4, mu_44c7ab);
	log_printf(0, mu_44c7e1);
	log_printf(0, mu_44c7ec, mu_44c7ab);
	log_printf(0, mu_44c810, mu_44c7ab);
	log_printf(0, mu_44c844);
	log_printf(0, mu_44c850);
	log_printf(0, mu_44c888);
	log_printf(0, mu_44c8ca);
	log_printf(0, mu_44c8e8);
	log_printf(0, mu_44c918);
	log_printf(0, mu_44c95c);
	log_printf(0, mu_44c9a8);
	log_printf(0, mu_44c9e8);
	log_printf(0, mu_44ca2c);
	log_printf(0, mu_44ca74);
	log_printf(0, mu_44cac8);
	log_printf(0, mu_44cb18);
	log_printf(0, mu_44cb58);
	log_printf(0, mu_44cb90);
	log_printf(0, mu_44cbb0);
	log_printf(0, mu_44cbbc);
	log_printf(0, mu_44cc04);
	log_printf(0, mu_44cc58);
	log_printf(0, mu_44ccc8);
	log_printf(0, mu_44cd14);
	log_printf(0, mu_44cd6c);
	log_printf(0, separator);
	log_finish();
	if (promptEnter) {
		log_printf(0, mu_44cdc0);
		fgetc(stdin);
	}
	exit(1);
}

int wantFile(const char *name)
{
	int ret = 1;

	if (clean) {
		if (!stricmp(name, mu_44cddb) || !stricmp(name, mu_44cde8)
		    || !stricmp(name, mu_44cdf4))
			ret = 0;
		if (!ret)
			log_printf(1, mu_44ce08, name);
	}
	return ret;
}

void parseAddonIdx(const u8 *addons, int len, const u8 *idx, size_t idxLen)
{
	u32 e, i, n;
	u32 off = 4;
	u32 ok;
	char name[1024];

	for (e = 0; e < getBeU32(idx); e++) {
		n = getBeU32(idx + off);
		off += 4;
		ok = 1;
		for (i = 0; i < n; i++) {
			if (!findInstExists(addons, len, idx + off + i * 8, 8)) {
				i = n;
				ok = 0;
			}
		}
		off += n * 8;
		if (ok) {
			if (xb.numPatches > 15) {
				log_printf(0, mu_44ce40, idx + off);
				return;
			}
			strcpy(name, (const char *)idx + off);
			strcat(name, ".bin");
			ok = 1;
			for (i = 0; i < xb.numPatches; i++) {
				if (!stricmp(name, xb.patches[i])) {
					i = xb.numPatches;
					ok = 0;
				}
			}
			if (ok) {
				strcpy(xb.patches[xb.numPatches], name);
				xb.numPatches++;
				log_printf(0, mu_44ce21, idx + off);
			}
		}
		off += 16;
	}
}

void getAddons(void)
{
	u8 *addons, *idx;
	int len;
	size_t size;
	char name[1024];

	addons = netGetFile(mu_44ce9c, &len);
	if (addons) {
		log_printf(1, mu_44cea3, len);
		if (len & 3)
			log_printf(0, mu_44cf18);
		else if (len) {
			sprintf(name, mu_44cebc, *(u16 *)((u8 *)info + 5));
			idx = FileToBuffer(name, &size);
			if (idx) {
				parseAddonIdx(addons, len, idx, size);
				free(idx);
			} else
				log_printf(0, mu_44ced0, name);
		}
		netFree(addons);
	} else
		log_printf(0, mu_44cf6c);
}

u32 getMobileFiles(const char *dir)
{
	u8 i;
	char name[64];
	int ret;

	log_printf(1, mu_44cfac);
	strcpy(path, "usv:\\MobileB.dat");
	for (i = 0; i < 11; i++) {
		if (i == 9)
			strcpy(name, "Statistics.settings");
		else if (i == 10)
			strcpy(name, "Manufacturing.data");
		else
			sprintf(name, mu_44cfd4, 'B' + i);
		if (wantFile(name)) {
			sprintf(path, mu_44d1d3, name);
			log_printf(1, mu_44d1db, name);
			xb.mobile[i].data = netGetFile(path, &xb.mobile[i].size);
			if (xb.mobile[i].data && xb.mobile[i].size) {
				if (i == 9)
					xb.mobile[i].size = 1024;
				else if (i == 10)
					xb.mobile[i].size = 128;
				log_printf(1, mu_44cea3, xb.mobile[i].size);
				if (dir)
					writeFileIn(dir, name, xb.mobile[i].data, xb.mobile[i].size);
			} else
				log_printf(1, mu_44cfe1, path);
		}
	}
	if (info->f008 & 2) {
		log_printf(1, mu_44cff0);
		xb.blmod.data = netGetFile(mu_44d009, &xb.blmod.size);
		if (xb.blmod.data && xb.blmod.size)
			log_printf(1, mu_44cea3, xb.blmod.size);
		else
			log_printf(0, mu_44d010);
		netFree(xb.blmod.data);
		xb.blmod.size = 0;
		xb.blmod.data = NULL;
	} else
		log_printf(1, mu_44d054);
	if (info->f008 & 4) {
		if (useConsoleAddons == 1) {
			log_printf(1, mu_44d074);
			getAddons();
		} else
			log_printf(1, mu_44d090);
	} else
		log_printf(1, mu_44d0d4);
	log_printf(1, mu_44d0f8);
	xb.smcConfig.data = netGetFile(mu_44d12c, &xb.smcConfig.size);
	if (xb.smcConfig.data && xb.smcConfig.size > 1023) {
		log_printf(1, mu_44d144, xb.smcConfig.size);
		if (smcConfigOk(xb.smcConfig.data)) {
			ret = 1;
			log_printf(1, mu_44d171);
			xb.smcConfig.size = 1024;
			if (dir)
				writeFileIn(dir, mu_44d186, xb.smcConfig.data, 1024);
			return ret;
		}
	}
	log_printf(0, mu_44d198);
	return 0;
}

u8 *bldrGetKv(int *size)
{
	u8 *bl = xb.bldrs.data;
	u32 len = SWAP32(*(u32 *)(bl + 96));
	u8 *kv = calloc(len, 1);

	memcpy(kv, bl + SWAP32(*(u32 *)(bl + 108)), len);
	*size = len;
	return kv;
}

u8 *bldrGetSmc(int *size)
{
	u8 *bl = xb.bldrs.data;
	u32 len = SWAP32(*(u32 *)(bl + 120));
	u8 *smc = calloc(len, 1);

	memcpy(smc, bl + SWAP32(*(u32 *)(bl + 124)), len);
	*size = len;
	return smc;
}

u32 checkBadBlocks(void)
{
	if (xb.flags & 0x10000000)
		return 1;
	return getBadBlocks();
}

u32 getBootloaders(const char *dir)
{
	log_printf(1, mu_44d400);
	if (xb.type != 3) {
		log_printf(1, mu_44d484);
		return 1;
	}
	log_printf(1, mu_44d424);
	xb.bldrs.data = netGetBldrs(&xb.bldrs.size);
	if (!xb.bldrs.data || !xb.bldrs.size) {
		log_printf(1, mu_44d479);
		return 0;
	}
	log_printf(1, mu_44d440, xb.bldrs.size);
	if (dir)
		writeFileIn(dir, mu_44d46e, xb.bldrs.data, xb.bldrs.size);
	xb.haveBldrs = 1;
	return 1;
}

int getConsoleFiles(const char *dir)
{
	if (!checkBadBlocks()) {
		log_printf(0, mu_44d590);
		return 0;
	}
	if (!__builtin_expect(netMount(mu_44d4c5, mu_44d4b9), 1)) {
		log_printf(0, mu_44d55c);
		return 0;
	}
	if (!getBootloaders(dir)) {
		log_printf(0, mu_44d4cc);
		return 0;
	}
	if (!getSecurityFiles(dir)) {
		log_printf(0, mu_44d528);
		return 0;
	}
	if (!getMobileFiles(dir)) {
		log_printf(0, mu_44d4fc);
		return 0;
	}
	return 1;
}

int updateGetFile(const char *name, u8 **data, int *size)
{
	char *p;
	u8 *buf;
	u32 len;
	int on = updating;

	*size = 0;
	*data = NULL;
	if (on) {
		char file[260] = "usv:\\";

		p = strrchr(name, '/');
		if (!p)
			p = strrchr(name, '\\');
		if (p)
			strcpy(file + 5, p + 1);
		else
			strcpy(file + 5, name);
		log_printf(1, mu_44d1db, name);
		buf = netGetFile(file, (int *)&len);
		if (!buf) {
			log_printf(1, mu_44d5d4);
			return 0;
		}
		if (!len) {
			log_printf(1, mu_44d5ba);
			free(buf);
			return 0;
		}
		log_printf(1, mu_44cea3, len);
		*data = buf;
		*size = len;
		return 1;
	}
	return on;
}

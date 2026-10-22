/* mode_update: `xeBuild update`, rebuilds and reflashes a console over the network.
   mode_update and updateNand are built with a crafted profile (build.sh). */
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

/* the other functions keep gcc's guessed profile, and .text */
#define NOPROF __attribute__((optimize("no-branch-probabilities", "no-reorder-functions")))
int useConsoleAddons = 1;

/* .bss in the original's order (-fno-toplevel-reorder emits definition
   order); globals, not statics, so that gcc assumes calls can change them */
char path[260] = { 0 };
int noReboot = 0;
int noAvatar = 0;
int noWrite = 0;
int clean = 0;
int hasHdd = 0;
int updating = 0;
struct consoleinfo *info = 0;

/* the strings, in the original .rdata order (-fno-toplevel-reorder emits
   them where they are defined), aligned as literals are (4 from 31
   bytes, else 1) */
static const char mu_44c6e8[] __attribute__((aligned(4))) = "\n------ getting bad blocks ------\n";
static const char mu_44c70c[] __attribute__((aligned(4))) = "processing %d bad blocks on device\n";
static const char mu_44c730[] __attribute__((aligned(1))) = "marking bad block at 0x%x\n";
static const char mu_44c74c[] __attribute__((aligned(4))) = "no bad blocks found on device\n";
static const char mu_44c76c[] __attribute__((aligned(4))) = "\n\n***** ERROR: unable to retrieve bad block list from device!\n";
static const char mu_44c7ab[] __attribute__((aligned(1))) = "xeBuild";
static const char mu_44c7b4[] __attribute__((aligned(4))) = "Usage   :\n   %s update <switch> [<option>]\n\n";
static const char mu_44c7e1[] __attribute__((aligned(1))) = "Examples:\n";
static const char mu_44c7ec[] __attribute__((aligned(4))) = "   %s update -f 16197 -a nofcrt\n";
static const char mu_44c810[] __attribute__((aligned(4))) = "   %s update -f 16203 -d myflash -ip 192.168.2.100\n";
static const char mu_44c844[] __attribute__((aligned(1))) = "\nSwitches:\n";
static const char mu_44c850[] __attribute__((aligned(4))) = "   -f <dir> : use different data dir and file lists\n";
static const char mu_44c888[] __attribute__((aligned(4))) = "   -d <dir> : dumps NAND and other data to <dir> before flashing\n";
static const char mu_44c8ca[] __attribute__((aligned(1))) = "   -a <name>: append patches\n";
static const char mu_44c8e8[] __attribute__((aligned(4))) = "   -ip <add>: force attempt to connect to addr\n";
static const char mu_44c918[] __attribute__((aligned(4))) = "   -i <ext> : adds _<ext> into firmware ini and patches file names\n";
static const char mu_44c95c[] __attribute__((aligned(4))) = "   -r <ext> : adds _<ext> into ini bl section name and patches file names\n";
static const char mu_44c9a8[] __attribute__((aligned(4))) = "   -nowrite : will not write anything to console flash or HDD\n";
static const char mu_44c9e8[] __attribute__((aligned(4))) = "              without -d results of update are not kept anywhere\n";
static const char mu_44ca2c[] __attribute__((aligned(4))) = "   -noava   : will not send avatar data if available and HDD present\n";
static const char mu_44ca74[] __attribute__((aligned(4))) = "   -clean   : secdata, extended and statistics will not be retrieved from console\n";
static const char mu_44cac8[] __attribute__((aligned(4))) = "   -noreeb  : do not automatically reboot console after writes are completed\n";
static const char mu_44cb18[] __attribute__((aligned(4))) = "   -noenter : suppresses prompt for enter key when finished\n";
static const char mu_44cb58[] __attribute__((aligned(4))) = "   -v       : shows more info during update process\n";
static const char mu_44cb90[] __attribute__((aligned(4))) = "   -?       : shows this help\n\n";
static const char mu_44cbb0[] __attribute__((aligned(1))) = "legend:\n";
static const char mu_44cbbc[] __attribute__((aligned(4))) = "<name>      = name.bin contents will be appended to hv/kernel patches\n\n";
static const char mu_44cc04[] __attribute__((aligned(4))) = "<dir>       = path, absolute or relative, to a directory - do not terminate with \\\n";
static const char mu_44cc58[] __attribute__((aligned(4))) = "<ext>       = using this option would cause the builder to look for _glitch_<ext>.ini instead of _glitch.ini\n";
static const char mu_44ccc8[] __attribute__((aligned(4))) = "              and patches_jasper_<ext>.bin instead of patches_jasper.bin\n";
static const char mu_44cd14[] __attribute__((aligned(4))) = "<add>       = without this option network will be scanned for server broadcast beacon\n";
static const char mu_44cd6c[] __attribute__((aligned(4))) = "              If provided the correct format is an IPv4 address like 192.168.0.100\n";
static const char mu_44cdc0[] __attribute__((aligned(1))) = "\npress <enter> to quit...\n";
static const char mu_44cddb[] __attribute__((aligned(1))) = "extended.bin";
static const char mu_44cde8[] __attribute__((aligned(1))) = "secdata.bin";
static const char mu_44cdf4[] __attribute__((aligned(1))) = "Statistics.settings";
static const char mu_44ce08[] __attribute__((aligned(1))) = "skipping %s, -clean flag";
static const char mu_44ce21[] __attribute__((aligned(1))) = "addon patch from console: %s\n";
static const char mu_44ce40[] __attribute__((aligned(4))) = "***** WARNING: exceeded total number of optional patches while processing %s from console!\n";
static const char mu_44ce9c[] __attribute__((aligned(1))) = "addons";
static const char mu_44cea3[] __attribute__((aligned(1))) = "OK, received 0x%x bytes\n";
static const char mu_44cebc[] __attribute__((aligned(1))) = ".\\%d\\bin\\addon.idx";
static const char mu_44ced0[] __attribute__((aligned(4))) = "\n\n***** WARNING: unable to open %s to parse addons.bin from console!\n";
static const char mu_44cf18[] __attribute__((aligned(4))) = "\n\n***** WARNING: addons.bin from console is not a multiple of 4 bytes! Skipping!\n";
static const char mu_44cf6c[] __attribute__((aligned(4))) = "\n\n***** WARNING: Unable to retrieve addons.bin from console!\n";
static const char mu_44cfac[] __attribute__((aligned(4))) = "\n------ getting mobile settings ------\n";
static const char mu_44cfd4[] __attribute__((aligned(1))) = "Mobile%c.dat";
static const char mu_44cfe1[] __attribute__((aligned(1))) = "not available\n";
static const char mu_44cff0[] __attribute__((aligned(1))) = "retrieving USVR\\blmod...";
static const char mu_44d009[] __attribute__((aligned(1))) = "blmod";
static const char mu_44d010[] __attribute__((aligned(4))) = "\n\n***** WARNING: Unable to retrieve blmod.bin data from console!\n";
static const char mu_44d054[] __attribute__((aligned(4))) = "console has no available blmod\n";
static const char mu_44d074[] __attribute__((aligned(1))) = "retrieving USVR\\addons...";
static const char mu_44d090[] __attribute__((aligned(4))) = "skipping USVR\\addons, addons have been specified on command line\n";
static const char mu_44d0d4[] __attribute__((aligned(4))) = "console has no available addons\n";
static const char mu_44d0f8[] __attribute__((aligned(4))) = "retrieving USVR\\Static.settings (smc_config.bin)...";
static const char mu_44d12c[] __attribute__((aligned(1))) = "usv:\\Static.settings";
static const char mu_44d144[] __attribute__((aligned(4))) = "OK, received 0x%x bytes\n        verifying...";
static const char mu_44d171[] __attribute__((aligned(1))) = "smc_config is good!\n";
static const char mu_44d186[] __attribute__((aligned(1))) = "smc_config.bin";
static const char mu_44d198[] __attribute__((aligned(4))) = "\n***** ERROR: could not retrieve smc_config from console!\n";
static const char mu_44d1d3[] __attribute__((aligned(1))) = "usv:\\%s";
static const char mu_44d1db[] __attribute__((aligned(1))) = "retrieving USVR\\%s...";
static const char mu_44d1f4[] __attribute__((aligned(4))) = "\n------ getting security files ------\n";
static const char mu_44d21c[] __attribute__((aligned(4))) = "OK, received 0x%x bytes\n        ";
static const char mu_44d23d[] __attribute__((aligned(1))) = "retrieving USVR\\kv_enc...";
static const char mu_44d257[] __attribute__((aligned(1))) = "kv_enc";
static const char mu_44d25e[] __attribute__((aligned(1))) = "extracting BLDR\\kv_enc...";
static const char mu_44d278[] __attribute__((aligned(4))) = "OK, received 0x%x bytes\n        decrypt and verify...";
static const char mu_44d2ae[] __attribute__((aligned(1))) = "keyvault is good!\n";
static const char mu_44d2c1[] __attribute__((aligned(1))) = "kv.bin";
static const char mu_44d2c8[] __attribute__((aligned(4))) = "\n***** ERROR: could not decrypt keyvault from console!\n";
static const char mu_44d300[] __attribute__((aligned(4))) = "\n***** ERROR: could not retrieve keyvault from console!\n";
static const char mu_44d339[] __attribute__((aligned(1))) = "retrieving USVR\\smc_enc...";
static const char mu_44d354[] __attribute__((aligned(1))) = "smc_enc";
static const char mu_44d35c[] __attribute__((aligned(1))) = "extracting BLDR\\smc_enc...";
static const char mu_44d377[] __attribute__((aligned(1))) = "smc is good!\n";
static const char mu_44d385[] __attribute__((aligned(1))) = "smc.bin";
static const char mu_44d390[] __attribute__((aligned(4))) = "\n***** ERROR: could not decrypt smc.bin from console!\n";
static const char mu_44d3c8[] __attribute__((aligned(4))) = "\n***** ERROR: could not retrieve smc.bin from console!\n";
static const char mu_44d400[] __attribute__((aligned(4))) = "\n------ getting bootloaders ------\n";
static const char mu_44d424[] __attribute__((aligned(1))) = "reading bootloader data...";
static const char mu_44d440[] __attribute__((aligned(4))) = "success! Bootloader size with xell is 0x%08x\n";
static const char mu_44d46e[] __attribute__((aligned(1))) = "fbldrs.bin";
static const char mu_44d479[] __attribute__((aligned(1))) = "failed!\n";
static const char mu_44d484[] __attribute__((aligned(4))) = "Skipping getting bootloaders on non-glitch machine!\n";
static const char mu_44d4b9[] __attribute__((aligned(1))) = "\\SystemRoot";
static const char mu_44d4c5[] __attribute__((aligned(1))) = "usv";
static const char mu_44d4cc[] __attribute__((aligned(4))) = "\n***** ERROR: getting raw boot loaders failed!\n";
static const char mu_44d4fc[] __attribute__((aligned(4))) = "\n***** ERROR: getting mobile files failed!\n";
static const char mu_44d528[] __attribute__((aligned(4))) = "\n***** ERROR: retrieving security files failed!\n";
static const char mu_44d55c[] __attribute__((aligned(4))) = "\n***** ERROR: mounting remote SystemRoot failed!\n";
static const char mu_44d590[] __attribute__((aligned(4))) = "\n***** ERROR: getting bad blocks failed!\n";
static const char mu_44d5ba[] __attribute__((aligned(1))) = "failed! received 0 bytes\n";
static const char mu_44d5d4[] __attribute__((aligned(4))) = "failed! file not found on console\n";
static const char mu_44d5f7[] __attribute__((aligned(1))) = "update";
static const char mu_44d5fe[] __attribute__((aligned(1))) = "help";
static const char mu_44d603[] __attribute__((aligned(1))) = "-?";
static const char mu_44d606[] __attribute__((aligned(1))) = "/?";
static const char mu_44d609[] __attribute__((aligned(1))) = "-noenter";
static const char mu_44d614[] __attribute__((aligned(4))) = "<enter> key on completion suppressed\n";
static const char mu_44d63a[] __attribute__((aligned(1))) = "-ip";
static const char mu_44d640[] __attribute__((aligned(4))) = "\n\n***** ERROR: option flag -ip on command line but no argument provided!\n";
static const char mu_44d68a[] __attribute__((aligned(1))) = "setting forced IP to %s\n";
static const char mu_44d6a3[] __attribute__((aligned(1))) = "-a";
static const char mu_44d6a8[] __attribute__((aligned(4))) = "\n\n***** ERROR: option flag -a on command line but no argument provided!\n";
static const char mu_44d6f4[] __attribute__((aligned(4))) = "***** WARNING: exceeded total number of optional patches with -a %s!\n";
static const char mu_44d73a[] __attribute__((aligned(1))) = "-r";
static const char mu_44d740[] __attribute__((aligned(4))) = "\n\n***** ERROR: option flag -r on command line but no argument provided!\n";
static const char mu_44d78c[] __attribute__((aligned(4))) = "***** WARNING: option flag -r %s on command line replacing previous setting of -r %s!\n";
static const char mu_44d7e3[] __attribute__((aligned(1))) = "_%s";
static const char mu_44d7e7[] __attribute__((aligned(1))) = "-i";
static const char mu_44d7ec[] __attribute__((aligned(4))) = "\n\n***** ERROR: data directory flag -i on command line but no argument provided!\n";
static const char mu_44d840[] __attribute__((aligned(4))) = "suffix '%s' added from command line to ini and patches filenames\n";
static const char mu_44d882[] __attribute__((aligned(1))) = "-nowrite";
static const char mu_44d88c[] __attribute__((aligned(4))) = "-nowrite: flash image and avatars will not be sent to xbox\n";
static const char mu_44d8c8[] __attribute__((aligned(1))) = "-noava";
static const char mu_44d8d0[] __attribute__((aligned(4))) = "-noava: avatar data, if available, will not be sent to console\n";
static const char mu_44d910[] __attribute__((aligned(1))) = "-noreeb";
static const char mu_44d918[] __attribute__((aligned(4))) = "-noreeb: console will not reboot after writes are done\n";
static const char mu_44d950[] __attribute__((aligned(1))) = "-clean";
static const char mu_44d958[] __attribute__((aligned(4))) = "-clean: secdata, extended and statistics will not be retrieved from console, builder will make clean versions\n";
static const char mu_44d9c7[] __attribute__((aligned(1))) = "-v";
static const char mu_44d9ca[] __attribute__((aligned(1))) = "-d";
static const char mu_44d9d0[] __attribute__((aligned(4))) = "\n\n***** ERROR: dump directory flag -d on command line but no argument provided!\n";
static const char mu_44da21[] __attribute__((aligned(1))) = "dump directory set to '%s'\n";
static const char mu_44da3d[] __attribute__((aligned(1))) = "-f";
static const char mu_44da40[] __attribute__((aligned(4))) = "\n\n***** ERROR: data directory flag -f on command line but no argument provided!\n";
static const char mu_44da91[] __attribute__((aligned(1))) = "%s\\";
static const char mu_44da98[] __attribute__((aligned(4))) = "data directory set from command line to '%s'\n";
static const char mu_44dac6[] __attribute__((aligned(1))) = "%s\\bin\\";
static const char mu_44dad0[] __attribute__((aligned(4))) = "\n\n***** ERROR: unknown option '%s' provided on command line!\n";
static const char mu_44db0e[] __attribute__((aligned(1))) = "Dumping disabled!\n";
static const char mu_44db21[] __attribute__((aligned(1))) = "%s%s";
static const char mu_44db26[] __attribute__((aligned(1))) = "%s_update";
static const char mu_44db30[] __attribute__((aligned(4))) = "\n------ dumping console flash ------\n";
static const char mu_44db58[] __attribute__((aligned(4))) = "\n------ flashing console ------\n";
static const char mu_44db7c[] __attribute__((aligned(4))) = "sending flash data to console...\n";
static const char mu_44dba0[] __attribute__((aligned(4))) = "flashing console skipped, -nowrite used\n";
static const char mu_44dbcc[] __attribute__((aligned(4))) = "\n------ loading and sending avatar data ------\n";
static const char mu_44dbfc[] __attribute__((aligned(4))) = "avatar data skipped, -noava or -nowrite used\n";
static const char mu_44dc2c[] __attribute__((aligned(4))) = "avatar data skipped, no HDD detected\n";
static const char mu_44dc54[] __attribute__((aligned(4))) = "\n***** WARNING: due to previous possible errors, console reboot is not being done\n";
static const char mu_44dca8[] __attribute__((aligned(4))) = "               it is not recommended to use update mode on this console again\n";
static const char mu_44dcf8[] __attribute__((aligned(4))) = "               until you have determined it's got a good image on it\n\n";
static const char mu_44dd40[] __attribute__((aligned(4))) = "\n\n***** ERROR: %i writing to file %s\n\n";
static const char mu_44dd67[] __attribute__((aligned(1))) = "%s image built, info:\n";
static const char mu_44dd80[] __attribute__((aligned(4))) = "\n\n***** FATAL UPDATE ERROR: %i unable to complete NAND image\n\n";
static const char mu_44ddc0[] __attribute__((aligned(4))) = "\n\n***** FATAL UPDATE ERROR: unable to get console unique files\n\n";
static const char mu_44de04[] __attribute__((aligned(4))) = "\n\n***** FATAL UPDATE ERROR: unable to parse %s\n\n";
static const char mu_44de38[] __attribute__((aligned(4))) = "\n\n***** FATAL UPDATE ERROR: unable to parse info reply from console!\n\n";
static const char mu_44de80[] __attribute__((aligned(4))) = "\n\n***** FATAL UPDATE ERROR: unable to find console!\n\n";

NOPROF u32 getBadBlocks(void)
{
	u8 *list;
	int len, i;
	u32 blocks;
	u32 block;

	log_printf(1, mu_44c6e8);
	list = netGetBadBlocks(&len);
	if (list) {
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
	log_printf(0, mu_44c76c);
	return 0;
}

NOPROF void update_usage(void)
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

NOPROF int wantFile(const char *name)
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

NOPROF void parseAddonIdx(const u8 *addons, int len, const u8 *idx, size_t idxLen)
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

NOPROF void getAddons(void)
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

NOPROF u32 getMobileFiles(const char *dir)
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

NOPROF u8 *bldrGetKv(int *size)
{
	u8 *bl = xb.bldrs.data;
	u32 len = SWAP32(*(u32 *)(bl + 96));
	u8 *kv = calloc(len, 1);

	memcpy(kv, bl + SWAP32(*(u32 *)(bl + 108)), len);
	*size = len;
	return kv;
}

NOPROF u8 *bldrGetSmc(int *size)
{
	u8 *bl = xb.bldrs.data;
	u32 len = SWAP32(*(u32 *)(bl + 120));
	u8 *smc = calloc(len, 1);

	memcpy(smc, bl + SWAP32(*(u32 *)(bl + 124)), len);
	*size = len;
	return smc;
}

NOPROF static u32 getSmc(const char *dir)
{
	if (!xb.haveBldrs) {
		log_printf(1, mu_44d339);
		xb.smc.data = netGetFile(mu_44d354, &xb.smc.size);
	} else {
		log_printf(1, mu_44d35c);
		xb.smc.data = bldrGetSmc(&xb.smc.size);
	}
	if (xb.smc.data && xb.smc.size > 0x2fff) {
		log_printf(1, mu_44d278, xb.smc.size);
		if (unscramble(xb.smc.data, xb.smc.size)) {
			log_printf(1, mu_44d377);
			setSmcKey(xb.smc.data);
			if (dir)
				writeFileIn(dir, mu_44d385, xb.smc.data, xb.smc.size);
			return 1;
		}
		log_printf(0, mu_44d390);
		return 0;
	}
	log_printf(0, mu_44d3c8);
	return 0;
}

NOPROF static u32 getKv(const char *dir)
{
	u32 ret;

	if (!xb.haveBldrs) {
		log_printf(1, mu_44d23d);
		xb.kv.data = netGetFile(mu_44d257, &xb.kv.size);
	} else {
		log_printf(1, mu_44d25e);
		xb.kv.data = bldrGetKv(&xb.kv.size);
	}
	if (!xb.kv.data || xb.kv.size <= 0x3fff) {
		log_printf(0, mu_44d300);
		return 0;
	}
	log_printf(1, mu_44d278, xb.kv.size);
	ret = verifyExtended(xb.kv.data, xb.kv.size);
	if (ret) {
		log_printf(1, mu_44d2ae);
		setKvSalt(xb.kv.data + 16);
		if (dir)
			writeFileIn(dir, mu_44d2c1, xb.kv.data, xb.kv.size);
	} else
		log_printf(0, mu_44d2c8);
	return ret;
}

NOPROF u32 getSecurityFiles(const char *dir)
{
	u32 i;

	log_printf(1, mu_44d1f4);
	for (i = 0; i < xb.numFlashFiles; i++) {
		if (!xb.flashFiles[i][0])
			continue;
		if (!wantFile(xb.flashFiles[i]))
			continue;
		sprintf(path, mu_44d1d3, xb.flashFiles[i]);
		log_printf(1, mu_44d1db, xb.flashFiles[i]);
		xb.flashBuf[i] = netGetFile(path, &xb.flashSize[i]);
		if (xb.flashBuf[i] && xb.flashSize[i]) {
			log_printf(1, mu_44d21c, xb.flashSize[i]);
			verifyFlashFile(i);
			if (dir)
				writeFileIn(dir, xb.flashFiles[i], xb.flashBuf[i], xb.flashSize[i]);
		} else
			log_printf(1, mu_44cfe1);
	}
	if (!getKv(dir))
		return 0;
	return getSmc(dir);
}

NOPROF u32 checkBadBlocks(void)
{
	if (xb.flags & 0x10000000)
		return 1;
	return getBadBlocks();
}

NOPROF u32 getBootloaders(const char *dir)
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

NOPROF int getConsoleFiles(const char *dir)
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

NOPROF int updateGetFile(const char *name, u8 **data, int *size)
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

static void updateNand(char *dumpDir, int *pret)
{
	int ret, r;

	if (getConsoleFiles(dumpDir)) {
		updating = 1;
		ret = buildImage();
		if (!ret) {
			netUnmount(mu_44d4c5);
			if (dumpDir) {
				char nand[1024];

				strcpy(nand, dumpDir);
				strcat(nand, "nanddump.bin");
				log_printf(1, mu_44db30);
				if (!netDumpNand(nand)) {
					ret = 5;
					log_printf(0, mu_44d479);
				}
			}
			log_printf(1, mu_44db58);
			if (!noWrite) {
				u32 size;
				u8 *buf = imageGetBuffer(&size);

				log_printf(0, mu_44db7c);
				netTimerStart();
				if (!netSendFlash(buf, size))
					ret = 5;
			} else
				log_printf(1, mu_44dba0);
			log_printf(1, mu_44dbcc);
			if (hasHdd) {
				if (noAvatar || noWrite)
					log_printf(1, mu_44dbfc);
				else
					sendAvatarData(xb.dataDir, xb.kernel);
			} else
				log_printf(1, mu_44dc2c);
			if (!noReboot) {
				if (!ret)
					netReboot(2);
				else {
					log_printf(0, mu_44dc54);
					log_printf(0, mu_44dca8);
					log_printf(0, mu_44dcf8);
				}
			}
			if (dumpDir) {
				r = writeImage(xb.outName);
				if (r)
					log_printf(0, mu_44dd40, r, xb.outName);
				log_printf(0, separator);
			}
			log_printf(0, mu_44dd67, xb.outName);
			*pret = ret;
		} else {
			log_printf(0, mu_44dd80, ret);
			*pret = 3;
		}
	} else {
		log_printf(0, mu_44ddc0);
		*pret = 5;
	}
}

int mode_update(int argc, char **argv)
{
	char ini[1024] = ".\\data\\";
	char dumpBuf[1024] = ".\\";
	char tmp[1024];
	char *ip, *dumpDir;
	int i, ret, code;

	xb.baseDir[0] = 0;
	log_set_name(mu_44d5f7);
	ip = NULL;
	dumpDir = NULL;
	for (i = 0; i < argc; i++) {
		if (!strnicmp(argv[i], mu_44d5fe, 2) || !strnicmp(argv[i], mu_44d603, 2)
		    || !strnicmp(argv[i], mu_44d606, 2))
			update_usage();
		if (!strnicmp(argv[i], mu_44d609, 8)) {
			log_printf(1, mu_44d614);
			promptEnter = 0;
		} else if (!strnicmp(argv[i], mu_44d63a, 3)) {
			i++;
			ip = argv[i];
			if (i == argc || !ip || *ip == '-') {
				log_printf(0, mu_44d640);
				update_usage();
			}
			log_printf(0, mu_44d68a, ip);
		} else if (!strnicmp(argv[i], mu_44d6a3, 2)) {
			i++;
			if (!argv[i] || i == argc || *argv[i] == '-') {
				log_printf(0, mu_44d6a8, argv[i]);
				update_usage();
			}
			useConsoleAddons = 0;
			if (xb.numPatches < 16) {
				strcpy(xb.patches[xb.numPatches], argv[i]);
				strcat(xb.patches[xb.numPatches], ".bin");
				xb.numPatches++;
			} else
				log_printf(0, mu_44d6f4, argv[i]);
		} else if (!strnicmp(argv[i], mu_44d73a, 2)) {
			i++;
			char *arg = argv[i];

			if (i == argc || !arg || *arg == '-') {
				log_printf(0, mu_44d740);
				update_usage();
			}
			if (xb.blSuffix[0])
				log_printf(0, mu_44d78c, argv[i], xb.blSuffix + 1);
			sprintf(xb.blSuffix, mu_44d7e3, argv[i]);
		} else if (!strnicmp(argv[i], mu_44d7e7, 2)) {
			i++;
			if (!argv[i] || i == argc || *argv[i] == '-') {
				log_printf(0, mu_44d7ec, argv[i]);
				update_usage();
			}
			strcpy(xb.suffix, "_");
			strcpy(xb.suffix + 1, argv[i]);
			log_printf(1, mu_44d840, xb.suffix);
		} else if (!strnicmp(argv[i], mu_44d882, 8)) {
			i++;
			noWrite = 1;
			noReboot = 1;
			noAvatar = 1;
			log_printf(1, mu_44d88c);
		} else if (!strnicmp(argv[i], mu_44d8c8, 6)) {
			i++;
			noAvatar = 1;
			log_printf(1, mu_44d8d0);
		} else if (!strnicmp(argv[i], mu_44d910, 6)) {
			i++;
			noReboot = 1;
			log_printf(1, mu_44d918);
		} else if (!strnicmp(argv[i], mu_44d950, 6)) {
			i++;
			clean = 1;
			log_printf(1, mu_44d958);
		} else if (!strnicmp(argv[i], mu_44d9c7, 2)) {
			log_verbose_flag(argv[i][2]);
		} else if (!strnicmp(argv[i], mu_44d9ca, 2)) {
			i++;
			if (!argv[i] || i == argc || *argv[i] == '-') {
				log_printf(0, mu_44d9d0, argv[i]);
				update_usage();
			}
			strcpy(dumpBuf, argv[i]);
			strcat(dumpBuf, "\\");
			log_printf(1, mu_44da21, dumpBuf);
			dumpDir = dumpBuf;
		} else if (!strnicmp(argv[i], mu_44da3d, 2)) {
			i++;
			if (!argv[i] || i == argc || *argv[i] == '-') {
				log_printf(0, mu_44da40, argv[i]);
				update_usage();
			}
			sprintf(ini, mu_44da91, argv[i]);
			log_printf(1, mu_44da98, ini);
			sprintf(xb.dataDir, mu_44da91, argv[i]);
			sprintf(xb.binDir, mu_44dac6, argv[i]);
		} else {
			log_printf(0, mu_44dad0, argv[i]);
			update_usage();
		}
	}
	if (dumpDir && !createDir(dumpDir)) {
		log_printf(0, mu_44db0e);
		dumpDir = NULL;
	}
	if (netConnect(ip)) {

		info = netGetInfo();
		if (parseConsoleInfo(1, dumpDir, dumpDir, &hasHdd)) {
			if (xb.type == 1)
				strcat(ini, "_retail");
			else if (xb.type == 2)
				strcat(ini, "_jtag");
			else if (xb.type == 3) {
				if (xb.glitch2mfg)
					strcat(ini, "_glitch2m");
				else if (xb.glitch2)
					strcat(ini, "_glitch2");
				else
					strcat(ini, "_glitch");
			} else if (xb.type == 6 || xb.type == 7)
				strcat(ini, "_devkit");
			else if (xb.type == 8 || xb.type == 9)
				strcat(ini, "_testkit");
			strcat(ini, xb.suffix);
			strcat(ini, ".ini");
			if (parseIni(ini)) {
				if (dumpDir) {
					sprintf(tmp, mu_44db21, dumpDir, xb.outName);
					strcpy(xb.outName, tmp);
					log_set_name(xb.outName);
				} else {
					sprintf(tmp, mu_44db26, xb.outName);
					log_set_name(tmp);
				}
				updateNand(dumpDir, &code);
				ret = code;
			} else {
				log_printf(0, mu_44de04, ini);
				ret = 1;
			}
		} else {
			log_printf(0, mu_44de38);
			ret = 5;
		}
	} else {
		ret = 5;
		log_printf(0, mu_44de80);
	}
	xb.pub1bl = NULL;
	xb.pubPirs = NULL;
	xb.masterPub = NULL;
	return ret;
}

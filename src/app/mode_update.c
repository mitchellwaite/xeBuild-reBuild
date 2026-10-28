/* mode_update: `xeBuild update`, rebuilds and reflashes a console over the network.
   mode_update and updateNand are built with a crafted profile (build.sh). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "xebuild.h"

#define SWAP32(x) (((x) << 24) + (((x) << 8) & 0xff0000) + (((x) >> 8) & 0xff00) + ((x) >> 24))

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

/* Strings are literals where gcc emits them in the original's .rdata order
   (expand-time block order).  Where it doesn't, the first ones of that
   function are static arrays defined right before it (-fno-toplevel-reorder
   emits them there), aligned as gcc aligns literals: 4 from 31 bytes. */

NOPROF u32 getBadBlocks(void)
{
	u8 *list;
	int len, i;
	u32 blocks;
	u32 block;

	log_printf(1, "\n------ getting bad blocks ------\n");
	list = netGetBadBlocks(&len);
	if (list) {
	if (len) {
		blocks = info->nandSize / info->blockSize;
		log_printf(1, "processing %d bad blocks on device\n", len / 2);
		for (i = len - 2; i >= 0; i -= 2) {
			block = getBeU16(list + i);
			log_printf(1, "marking bad block at 0x%x\n", block);
			xb.badRemap[xb.numBad] = -1;
			xb.badBlocks[xb.numBad] = block;
			xb.numBad++;
		}
		remapBadBlocks(blocks);
	} else
		log_printf(1, "no bad blocks found on device\n");
	netFree(list);
		return 1;
	}
	log_printf(0, "\n\n***** ERROR: unable to retrieve bad block list from device!\n");
	return 0;
}

NOPROF void update_usage(void)
{
	log_printf(0, separator);
	log_printf(0, "Usage   :\n   %s update <switch> [<option>]\n\n", "xeBuild");
	log_printf(0, "Examples:\n");
	log_printf(0, "   %s update -f 16197 -a nofcrt\n", "xeBuild");
	log_printf(0, "   %s update -f 16203 -d myflash -ip 192.168.2.100\n", "xeBuild");
	log_printf(0, "\nSwitches:\n");
	log_printf(0, "   -f <dir> : use different data dir and file lists\n");
	log_printf(0, "   -d <dir> : dumps NAND and other data to <dir> before flashing\n");
	log_printf(0, "   -a <name>: append patches\n");
	log_printf(0, "   -ip <add>: force attempt to connect to addr\n");
	log_printf(0, "   -i <ext> : adds _<ext> into firmware ini and patches file names\n");
	log_printf(0, "   -r <ext> : adds _<ext> into ini bl section name and patches file names\n");
	log_printf(0, "   -nowrite : will not write anything to console flash or HDD\n");
	log_printf(0, "              without -d results of update are not kept anywhere\n");
	log_printf(0, "   -noava   : will not send avatar data if available and HDD present\n");
	log_printf(0, "   -clean   : secdata, extended and statistics will not be retrieved from console\n");
	log_printf(0, "   -noreeb  : do not automatically reboot console after writes are completed\n");
	log_printf(0, "   -noenter : suppresses prompt for enter key when finished\n");
	log_printf(0, "   -v       : shows more info during update process\n");
	log_printf(0, "   -?       : shows this help\n\n");
	log_printf(0, "legend:\n");
	log_printf(0, "<name>      = name.bin contents will be appended to hv/kernel patches\n\n");
	log_printf(0, "<dir>       = path, absolute or relative, to a directory - do not terminate with \\\n");
	log_printf(0, "<ext>       = using this option would cause the builder to look for _glitch_<ext>.ini instead of _glitch.ini\n");
	log_printf(0, "              and patches_jasper_<ext>.bin instead of patches_jasper.bin\n");
	log_printf(0, "<add>       = without this option network will be scanned for server broadcast beacon\n");
	log_printf(0, "              If provided the correct format is an IPv4 address like 192.168.0.100\n");
	log_printf(0, separator);
	log_finish();
	if (promptEnter) {
		log_printf(0, "\npress <enter> to quit...\n");
		fgetc(stdin);
	}
	exit(1);
}

NOPROF int wantFile(const char *name)
{
	int ret = 1;

	if (clean) {
		if (!stricmp(name, "extended.bin") || !stricmp(name, "secdata.bin")
		    || !stricmp(name, "Statistics.settings"))
			ret = 0;
		if (!ret)
			log_printf(1, "skipping %s, -clean flag", name);
	}
	return ret;
}

static const char mu_44ce21[] __attribute__((aligned(1))) = "addon patch from console: %s\n";

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
				log_printf(0, "***** WARNING: exceeded total number of optional patches while processing %s from console!\n", idx + off);
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

static const char mu_44ce9c[] __attribute__((aligned(1))) = "addons";
static const char mu_44cea3[] __attribute__((aligned(1))) = "OK, received 0x%x bytes\n";
static const char mu_44cebc[] __attribute__((aligned(1))) = ".\\%d\\bin\\addon.idx";
static const char mu_44ced0[] __attribute__((aligned(4))) = "\n\n***** WARNING: unable to open %s to parse addons.bin from console!\n";

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
			log_printf(0, "\n\n***** WARNING: addons.bin from console is not a multiple of 4 bytes! Skipping!\n");
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
		log_printf(0, "\n\n***** WARNING: Unable to retrieve addons.bin from console!\n");
}

NOPROF u32 getMobileFiles(const char *dir)
{
	u8 i;
	char name[64];
	int ret;

	log_printf(1, "\n------ getting mobile settings ------\n");
	strcpy(path, "usv:\\MobileB.dat");
	for (i = 0; i < 11; i++) {
		if (i == 9)
			strcpy(name, "Statistics.settings");
		else if (i == 10)
			strcpy(name, "Manufacturing.data");
		else
			sprintf(name, "Mobile%c.dat", 'B' + i);
		if (wantFile(name)) {
			sprintf(path, "usv:\\%s", name);
			log_printf(1, "retrieving USVR\\%s...", name);
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
				log_printf(1, "not available\n", path);
		}
	}
	if (info->f008 & 2) {
		log_printf(1, "retrieving USVR\\blmod...");
		xb.consoleBlmod.data = netGetFile("blmod", &xb.consoleBlmod.size);
		if (xb.consoleBlmod.data && xb.consoleBlmod.size)
			log_printf(1, mu_44cea3, xb.consoleBlmod.size);
		else
			log_printf(0, "\n\n***** WARNING: Unable to retrieve blmod.bin data from console!\n");
		netFree(xb.consoleBlmod.data);
		xb.consoleBlmod.size = 0;
		xb.consoleBlmod.data = NULL;
	} else
		log_printf(1, "console has no available blmod\n");
	if (info->f008 & 4) {
		if (useConsoleAddons == 1) {
			log_printf(1, "retrieving USVR\\addons...");
			getAddons();
		} else
			log_printf(1, "skipping USVR\\addons, addons have been specified on command line\n");
	} else
		log_printf(1, "console has no available addons\n");
	log_printf(1, "retrieving USVR\\Static.settings (smc_config.bin)...");
	xb.smcConfig.data = netGetFile("usv:\\Static.settings", &xb.smcConfig.size);
	if (xb.smcConfig.data && xb.smcConfig.size > 1023) {
		log_printf(1, "OK, received 0x%x bytes\n        verifying...", xb.smcConfig.size);
		if (smcConfigOk(xb.smcConfig.data)) {
			ret = 1;
			log_printf(1, "smc_config is good!\n");
			xb.smcConfig.size = 1024;
			if (dir)
				writeFileIn(dir, "smc_config.bin", xb.smcConfig.data, 1024);
			return ret;
		}
	}
	log_printf(0, "\n***** ERROR: could not retrieve smc_config from console!\n");
	return 0;
}

NOPROF u8 *bldrGetKv(int *size)
{
	u8 *bl = xb.bl.data;
	u32 len = SWAP32(*(u32 *)(bl + 96));
	u8 *kv = calloc(len, 1);

	memcpy(kv, bl + SWAP32(*(u32 *)(bl + 108)), len);
	*size = len;
	return kv;
}

NOPROF u8 *bldrGetSmc(int *size)
{
	u8 *bl = xb.bl.data;
	u32 len = SWAP32(*(u32 *)(bl + 120));
	u8 *smc = calloc(len, 1);

	memcpy(smc, bl + SWAP32(*(u32 *)(bl + 124)), len);
	*size = len;
	return smc;
}

static const char mu_44d1f4[] __attribute__((aligned(4))) = "\n------ getting security files ------\n";
static const char mu_44d21c[] __attribute__((aligned(4))) = "OK, received 0x%x bytes\n        ";
static const char mu_44d23d[] __attribute__((aligned(1))) = "retrieving USVR\\kv_enc...";
static const char mu_44d257[] __attribute__((aligned(1))) = "kv_enc";
static const char mu_44d25e[] __attribute__((aligned(1))) = "extracting BLDR\\kv_enc...";
static const char mu_44d278[] __attribute__((aligned(4))) = "OK, received 0x%x bytes\n        decrypt and verify...";

NOPROF static u32 getSmc(const char *dir)
{
	if (!xb.fromConsole) {
		log_printf(1, "retrieving USVR\\smc_enc...");
		xb.smc.data = netGetFile("smc_enc", &xb.smc.size);
	} else {
		log_printf(1, "extracting BLDR\\smc_enc...");
		xb.smc.data = bldrGetSmc(&xb.smc.size);
	}
	if (xb.smc.data && xb.smc.size > 0x2fff) {
		log_printf(1, mu_44d278, xb.smc.size);
		if (unscramble(xb.smc.data, xb.smc.size)) {
			log_printf(1, "smc is good!\n");
			setSmcKey(xb.smc.data);
			if (dir)
				writeFileIn(dir, "smc.bin", xb.smc.data, xb.smc.size);
			return 1;
		}
		log_printf(0, "\n***** ERROR: could not decrypt smc.bin from console!\n");
		return 0;
	}
	log_printf(0, "\n***** ERROR: could not retrieve smc.bin from console!\n");
	return 0;
}

static const char mu_44d2ae[] __attribute__((aligned(1))) = "keyvault is good!\n";
static const char mu_44d2c1[] __attribute__((aligned(1))) = "kv.bin";
static const char mu_44d2c8[] __attribute__((aligned(4))) = "\n***** ERROR: could not decrypt keyvault from console!\n";

NOPROF static u32 getKv(const char *dir)
{
	u32 ret;

	if (!xb.fromConsole) {
		log_printf(1, mu_44d23d);
		xb.kv.data = netGetFile(mu_44d257, &xb.kv.size);
	} else {
		log_printf(1, mu_44d25e);
		xb.kv.data = bldrGetKv(&xb.kv.size);
	}
	if (!xb.kv.data || xb.kv.size <= 0x3fff) {
		log_printf(0, "\n***** ERROR: could not retrieve keyvault from console!\n");
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
	for (i = 0; i < xb.nFlashFiles2; i++) {
		if (!xb.flashFiles[i][0])
			continue;
		if (!wantFile(xb.flashFiles[i]))
			continue;
		sprintf(path, "usv:\\%s", xb.flashFiles[i]);
		log_printf(1, "retrieving USVR\\%s...", xb.flashFiles[i]);
		xb.flashBuf[i] = netGetFile(path, &xb.flashSize[i]);
		if (xb.flashBuf[i] && xb.flashSize[i]) {
			log_printf(1, mu_44d21c, xb.flashSize[i]);
			verifyFlashFile(i);
			if (dir)
				writeFileIn(dir, xb.flashFiles[i], xb.flashBuf[i], xb.flashSize[i]);
		} else
			log_printf(1, "not available\n");
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

static const char mu_44d400[] __attribute__((aligned(4))) = "\n------ getting bootloaders ------\n";
static const char mu_44d424[] __attribute__((aligned(1))) = "reading bootloader data...";
static const char mu_44d440[] __attribute__((aligned(4))) = "success! Bootloader size with xell is 0x%08x\n";
static const char mu_44d46e[] __attribute__((aligned(1))) = "fbldrs.bin";
static const char mu_44d479[] __attribute__((aligned(1))) = "failed!\n";

NOPROF u32 getBootloaders(const char *dir)
{
	log_printf(1, mu_44d400);
	if (xb.type != 3) {
		log_printf(1, "Skipping getting bootloaders on non-glitch machine!\n");
		return 1;
	}
	log_printf(1, mu_44d424);
	xb.bl.data = netGetBldrs(&xb.bl.size);
	if (!xb.bl.data || !xb.bl.size) {
		log_printf(1, mu_44d479);
		return 0;
	}
	log_printf(1, mu_44d440, xb.bl.size);
	if (dir)
		writeFileIn(dir, mu_44d46e, xb.bl.data, xb.bl.size);
	xb.fromConsole = 1;
	return 1;
}

static const char mu_44d4b9[] __attribute__((aligned(1))) = "\\SystemRoot";
static const char mu_44d4c5[] __attribute__((aligned(1))) = "usv";
static const char mu_44d4cc[] __attribute__((aligned(4))) = "\n***** ERROR: getting raw boot loaders failed!\n";
static const char mu_44d4fc[] __attribute__((aligned(4))) = "\n***** ERROR: getting mobile files failed!\n";
static const char mu_44d528[] __attribute__((aligned(4))) = "\n***** ERROR: retrieving security files failed!\n";
static const char mu_44d55c[] __attribute__((aligned(4))) = "\n***** ERROR: mounting remote SystemRoot failed!\n";

NOPROF int getConsoleFiles(const char *dir)
{
	if (!checkBadBlocks()) {
		log_printf(0, "\n***** ERROR: getting bad blocks failed!\n");
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

static const char mu_44d5ba[] __attribute__((aligned(1))) = "failed! received 0 bytes\n";

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
		log_printf(1, "retrieving USVR\\%s...", name);
		buf = netGetFile(file, (int *)&len);
		if (!buf) {
			log_printf(1, "failed! file not found on console\n");
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
				log_printf(1, "\n------ dumping console flash ------\n");
				if (!netDumpNand(nand)) {
					ret = 5;
					log_printf(0, mu_44d479);
				}
			}
			log_printf(1, "\n------ flashing console ------\n");
			if (!noWrite) {
				u32 size;
				u8 *buf = imageGetBuffer(&size);

				log_printf(0, "sending flash data to console...\n");
				netTimerStart();
				if (!netSendFlash(buf, size))
					ret = 5;
			} else
				log_printf(1, "flashing console skipped, -nowrite used\n");
			log_printf(1, "\n------ loading and sending avatar data ------\n");
			if (hasHdd) {
				if (noAvatar || noWrite)
					log_printf(1, "avatar data skipped, -noava or -nowrite used\n");
				else
					sendAvatarData(xb.dataDir, xb.kernel);
			} else
				log_printf(1, "avatar data skipped, no HDD detected\n");
			if (!noReboot) {
				if (!ret)
					netReboot(2);
				else {
					log_printf(0, "\n***** WARNING: due to previous possible errors, console reboot is not being done\n");
					log_printf(0, "               it is not recommended to use update mode on this console again\n");
					log_printf(0, "               until you have determined it's got a good image on it\n\n");
				}
			}
			if (dumpDir) {
				r = writeImage(xb.outName);
				if (r)
					log_printf(0, "\n\n***** ERROR: %i writing to file %s\n\n", r, xb.outName);
				log_printf(0, separator);
			}
			log_printf(0, "%s image built, info:\n", xb.outName);
			*pret = ret;
		} else {
			log_printf(0, "\n\n***** FATAL UPDATE ERROR: %i unable to complete NAND image\n\n", ret);
			*pret = 3;
		}
	} else {
		log_printf(0, "\n\n***** FATAL UPDATE ERROR: unable to get console unique files\n\n");
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
	log_set_name("update");
	ip = NULL;
	dumpDir = NULL;
	for (i = 0; i < argc; i++) {
		if (!strnicmp(argv[i], "help", 2) || !strnicmp(argv[i], "-?", 2)
		    || !strnicmp(argv[i], "/?", 2))
			update_usage();
		if (!strnicmp(argv[i], "-noenter", 8)) {
			log_printf(1, "<enter> key on completion suppressed\n");
			promptEnter = 0;
		} else if (!strnicmp(argv[i], "-ip", 3)) {
			i++;
			ip = argv[i];
			if (i == argc || !ip || *ip == '-') {
				log_printf(0, "\n\n***** ERROR: option flag -ip on command line but no argument provided!\n");
				update_usage();
			}
			log_printf(0, "setting forced IP to %s\n", ip);
		} else if (!strnicmp(argv[i], "-a", 2)) {
			i++;
			if (!argv[i] || i == argc || *argv[i] == '-') {
				log_printf(0, "\n\n***** ERROR: option flag -a on command line but no argument provided!\n", argv[i]);
				update_usage();
			}
			useConsoleAddons = 0;
			if (xb.numPatches < 16) {
				strcpy(xb.patches[xb.numPatches], argv[i]);
				strcat(xb.patches[xb.numPatches], ".bin");
				xb.numPatches++;
			} else
				log_printf(0, "***** WARNING: exceeded total number of optional patches with -a %s!\n", argv[i]);
		} else if (!strnicmp(argv[i], "-r", 2)) {
			i++;
			char *arg = argv[i];

			if (i == argc || !arg || *arg == '-') {
				log_printf(0, "\n\n***** ERROR: option flag -r on command line but no argument provided!\n");
				update_usage();
			}
			if (xb.blSuffix[0])
				log_printf(0, "***** WARNING: option flag -r %s on command line replacing previous setting of -r %s!\n", argv[i], xb.blSuffix + 1);
			sprintf(xb.blSuffix, "_%s", argv[i]);
		} else if (!strnicmp(argv[i], "-i", 2)) {
			i++;
			if (!argv[i] || i == argc || *argv[i] == '-') {
				log_printf(0, "\n\n***** ERROR: data directory flag -i on command line but no argument provided!\n", argv[i]);
				update_usage();
			}
			strcpy(xb.suffix, "_");
			strcpy(xb.suffix + 1, argv[i]);
			log_printf(1, "suffix '%s' added from command line to ini and patches filenames\n", xb.suffix);
		} else if (!strnicmp(argv[i], "-nowrite", 8)) {
			i++;
			noWrite = 1;
			noReboot = 1;
			noAvatar = 1;
			log_printf(1, "-nowrite: flash image and avatars will not be sent to xbox\n");
		} else if (!strnicmp(argv[i], "-noava", 6)) {
			i++;
			noAvatar = 1;
			log_printf(1, "-noava: avatar data, if available, will not be sent to console\n");
		} else if (!strnicmp(argv[i], "-noreeb", 6)) {
			i++;
			noReboot = 1;
			log_printf(1, "-noreeb: console will not reboot after writes are done\n");
		} else if (!strnicmp(argv[i], "-clean", 6)) {
			i++;
			clean = 1;
			log_printf(1, "-clean: secdata, extended and statistics will not be retrieved from console, builder will make clean versions\n");
		} else if (!strnicmp(argv[i], "-v", 2)) {
			log_verbose_flag(argv[i][2]);
		} else if (!strnicmp(argv[i], "-d", 2)) {
			i++;
			if (!argv[i] || i == argc || *argv[i] == '-') {
				log_printf(0, "\n\n***** ERROR: dump directory flag -d on command line but no argument provided!\n", argv[i]);
				update_usage();
			}
			strcpy(dumpBuf, argv[i]);
			strcat(dumpBuf, "\\");
			log_printf(1, "dump directory set to '%s'\n", dumpBuf);
			dumpDir = dumpBuf;
		} else if (!strnicmp(argv[i], "-f", 2)) {
			i++;
			if (!argv[i] || i == argc || *argv[i] == '-') {
				log_printf(0, "\n\n***** ERROR: data directory flag -f on command line but no argument provided!\n", argv[i]);
				update_usage();
			}
			sprintf(ini, "%s\\", argv[i]);
			log_printf(1, "data directory set from command line to '%s'\n", ini);
			sprintf(xb.dataDir, "%s\\", argv[i]);
			sprintf(xb.binDir, "%s\\bin\\", argv[i]);
		} else {
			log_printf(0, "\n\n***** ERROR: unknown option '%s' provided on command line!\n", argv[i]);
			update_usage();
		}
	}
	if (dumpDir && !createDir(dumpDir)) {
		log_printf(0, "Dumping disabled!\n");
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
					sprintf(tmp, "%s%s", dumpDir, xb.outName);
					strcpy(xb.outName, tmp);
					log_set_name(xb.outName);
				} else {
					sprintf(tmp, "%s_update", xb.outName);
					log_set_name(tmp);
				}
				updateNand(dumpDir, &code);
				ret = code;
			} else {
				log_printf(0, "\n\n***** FATAL UPDATE ERROR: unable to parse %s\n\n", ini);
				ret = 1;
			}
		} else {
			log_printf(0, "\n\n***** FATAL UPDATE ERROR: unable to parse info reply from console!\n\n");
			ret = 5;
		}
	} else {
		ret = 5;
		log_printf(0, "\n\n***** FATAL UPDATE ERROR: unable to find console!\n\n");
	}
	xb.pub1bl = NULL;
	xb.pubPirs = NULL;
	xb.masterPub = NULL;
	return ret;
}

/* mode_update: `xeBuild update`, rebuilds and reflashes a console over the network.
   mode_update and updateNand are built with a crafted profile (build.sh). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define XB_PATCHES		/* xb.patches (xebuild.h) */
#include "xebuild.h"
#include "bootloaders.h"
#include "console_hdd.h"
#include "consoleinfo.h"
#include "filelist_ini.h"
#include "fileutil.h"
#include "image_read.h"
#include "image_write.h"
#include "keys.h"
#include "log.h"
#include "main.h"
#include "mode_update.h"
#include "net.h"
#include "smc.h"

/* TODO(prototype cast): verifyExtended returns int (bootloaders.c); getKv's
   code wants a uint32_t */
uint32_t verifyExtendedU32(void *buf, int size) __asm__("_verifyExtended");

uint32_t getSecurityFiles(const char *dir);

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

/* gcc emits a function's literals in expand-time block order, so the
   original's .rdata order shows its shape: parseAddonIdx, getAddons,
   getKv, getBootloaders, getConsoleFiles and updateGetFile test for
   success and log their errors after it. */

NOPROF uint32_t getBadBlocks(void)
{
	uint8_t *list;
	int len, i;
	uint32_t blocks;
	uint32_t block;

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

NOPROF void parseAddonIdx(const uint8_t *addons, int len, const uint8_t *idx, size_t idxLen)
{
	uint32_t e, i, n;
	uint32_t off = 4;
	uint32_t ok;
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
			if (xb.numPatches <= 15) {
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
					log_printf(0, "addon patch from console: %s\n", idx + off);
				}
			} else {
				log_printf(0, "***** WARNING: exceeded total number of optional patches while processing %s from console!\n", idx + off);
				return;
			}
		}
		off += 16;
	}
}

NOPROF void getAddons(void)
{
	uint8_t *addons, *idx;
	int len;
	size_t size;
	char name[1024];

	addons = netGetFile("addons", &len);
	if (addons) {
		log_printf(1, "OK, received 0x%x bytes\n", len);
		if (!(len & 3)) {
			if (len) {
				sprintf(name, ".\\%d\\bin\\addon.idx", *(uint16_t *)((uint8_t *)info + 5));
				idx = FileToBuffer(name, &size);
				if (idx) {
					parseAddonIdx(addons, len, idx, size);
					free(idx);
				} else
					log_printf(0, "\n\n***** WARNING: unable to open %s to parse addons.bin from console!\n", name);
			}
		} else
			log_printf(0, "\n\n***** WARNING: addons.bin from console is not a multiple of 4 bytes! Skipping!\n");
		netFree(addons);
	} else
		log_printf(0, "\n\n***** WARNING: Unable to retrieve addons.bin from console!\n");
}

NOPROF uint32_t getMobileFiles(const char *dir)
{
	uint8_t i;
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
				log_printf(1, "OK, received 0x%x bytes\n", xb.mobile[i].size);
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
			log_printf(1, "OK, received 0x%x bytes\n", xb.consoleBlmod.size);
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

NOPROF uint8_t *bldrGetKv(int *size)
{
	uint8_t *bl = xb.bl.data;
	uint32_t len = SWAP32(*(uint32_t *)(bl + 96));
	uint8_t *kv = calloc(len, 1);

	memcpy(kv, bl + SWAP32(*(uint32_t *)(bl + 108)), len);
	*size = len;
	return kv;
}

NOPROF uint8_t *bldrGetSmc(int *size)
{
	uint8_t *bl = xb.bl.data;
	uint32_t len = SWAP32(*(uint32_t *)(bl + 120));
	uint8_t *smc = calloc(len, 1);

	memcpy(smc, bl + SWAP32(*(uint32_t *)(bl + 124)), len);
	*size = len;
	return smc;
}

NOPROF static uint32_t getSmc(const char *dir)
{
	if (!xb.fromConsole) {
		log_printf(1, "retrieving USVR\\smc_enc...");
		xb.smc.data = netGetFile("smc_enc", &xb.smc.size);
	} else {
		log_printf(1, "extracting BLDR\\smc_enc...");
		xb.smc.data = bldrGetSmc(&xb.smc.size);
	}
	if (xb.smc.data && xb.smc.size > 0x2fff) {
		log_printf(1, "OK, received 0x%x bytes\n        decrypt and verify...", xb.smc.size);
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

NOPROF static uint32_t getKv(const char *dir)
{
	uint32_t ret;

	if (!xb.fromConsole) {
		log_printf(1, "retrieving USVR\\kv_enc...");
		xb.kv.data = netGetFile("kv_enc", &xb.kv.size);
	} else {
		log_printf(1, "extracting BLDR\\kv_enc...");
		xb.kv.data = bldrGetKv(&xb.kv.size);
	}
	if (xb.kv.data && xb.kv.size > 0x3fff) {
		log_printf(1, "OK, received 0x%x bytes\n        decrypt and verify...", xb.kv.size);
		ret = verifyExtendedU32(xb.kv.data, xb.kv.size);
		if (ret) {
			log_printf(1, "keyvault is good!\n");
			setKvSalt(xb.kv.data + 16);
			if (dir)
				writeFileIn(dir, "kv.bin", xb.kv.data, xb.kv.size);
		} else
			log_printf(0, "\n***** ERROR: could not decrypt keyvault from console!\n");
		return ret;
	}
	log_printf(0, "\n***** ERROR: could not retrieve keyvault from console!\n");
	return 0;
}

NOPROF uint32_t getSecurityFiles(const char *dir)
{
	uint32_t i;

	log_printf(1, "\n------ getting security files ------\n");
	for (i = 0; i < xb.nFlashFiles2; i++) {
		if (!xb.flashFiles[i][0])
			continue;
		if (!wantFile(xb.flashFiles[i]))
			continue;
		sprintf(path, "usv:\\%s", xb.flashFiles[i]);
		log_printf(1, "retrieving USVR\\%s...", xb.flashFiles[i]);
		xb.flashBuf[i] = netGetFile(path, &xb.flashSize[i]);
		if (xb.flashBuf[i] && xb.flashSize[i]) {
			log_printf(1, "OK, received 0x%x bytes\n        ", xb.flashSize[i]);
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

NOPROF uint32_t checkBadBlocks(void)
{
	if (xb.flags & NAND_MMC)
		return 1;
	return getBadBlocks();
}

NOPROF uint32_t getBootloaders(const char *dir)
{
	log_printf(1, "\n------ getting bootloaders ------\n");
	if (xb.type == BUILD_GLITCH) {
		log_printf(1, "reading bootloader data...");
		xb.bl.data = netGetBldrs(&xb.bl.size);
		if (xb.bl.data && xb.bl.size) {
			log_printf(1, "success! Bootloader size with xell is 0x%08x\n", xb.bl.size);
			if (dir)
				writeFileIn(dir, "fbldrs.bin", xb.bl.data, xb.bl.size);
			xb.fromConsole = 1;
			return 1;
		}
		log_printf(1, "failed!\n");
		return 0;
	}
	log_printf(1, "Skipping getting bootloaders on non-glitch machine!\n");
	return 1;
}

NOPROF int getConsoleFiles(const char *dir)
{
	if (checkBadBlocks()) {
		if (__builtin_expect(netMount("usv", "\\SystemRoot"), 1)) {
			if (!getBootloaders(dir)) {
				log_printf(0, "\n***** ERROR: getting raw boot loaders failed!\n");
				return 0;
			}
			if (getSecurityFiles(dir)) {
				if (getMobileFiles(dir))
					return 1;
				log_printf(0, "\n***** ERROR: getting mobile files failed!\n");
			} else
				log_printf(0, "\n***** ERROR: retrieving security files failed!\n");
		} else
			log_printf(0, "\n***** ERROR: mounting remote SystemRoot failed!\n");
	} else
		log_printf(0, "\n***** ERROR: getting bad blocks failed!\n");
	return 0;
}

NOPROF int updateGetFile(const char *name, uint8_t **data, int *size)
{
	char *p;
	uint8_t *buf;
	uint32_t len;
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
		if (buf) {
			if (!len) {
				log_printf(1, "failed! received 0 bytes\n");
				free(buf);
				return 0;
			}
			log_printf(1, "OK, received 0x%x bytes\n", len);
			*data = buf;
			*size = len;
			return 1;
		}
		log_printf(1, "failed! file not found on console\n");
		return 0;
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
			netUnmount("usv");
			if (dumpDir) {
				char nand[1024];

				strcpy(nand, dumpDir);
				strcat(nand, "nanddump.bin");
				log_printf(1, "\n------ dumping console flash ------\n");
				if (!netDumpNand(nand)) {
					ret = 5;
					log_printf(0, "failed!\n");
				}
			}
			log_printf(1, "\n------ flashing console ------\n");
			if (!noWrite) {
				uint32_t size;
				uint8_t *buf = imageGetBuffer(&size);

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
			if (xb.type == BUILD_RETAIL)
				strcat(ini, "_retail");
			else if (xb.type == BUILD_JTAG)
				strcat(ini, "_jtag");
			else if (xb.type == BUILD_GLITCH) {
				if (xb.glitch2mfg)
					strcat(ini, "_glitch2m");
				else if (xb.glitch2)
					strcat(ini, "_glitch2");
				else
					strcat(ini, "_glitch");
			} else if (xb.type == BUILD_DEVKIT || xb.type == BUILD_DEVKIT16)
				strcat(ini, "_devkit");
			else if (xb.type == BUILD_TESTKIT || xb.type == BUILD_TESTKIT16)
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

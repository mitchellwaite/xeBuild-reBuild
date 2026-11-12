/* consoleinfo: options.ini writing, parsing the console info response */
#include <stdio.h>
#include <string.h>

#include "xebuild.h"
#include "build.h"
#include "consoleinfo.h"
#include "fileutil.h"
#include "keys.h"
#include "log.h"
#include "main.h"
#include "net.h"
#include "options.h"

/* freeboot 0.08's options block: four big endian words, the boot options
   (OPT_FREEBOOT_MASK) and then the three power-on reasons in the low bytes
   of the other three */
#define FREEBOOT08_OPTS 0x9a0
#define FREEBOOT08_XELL_BUTTON 7
#define FREEBOOT08_DUAL_BUTTON 11
#define FREEBOOT08_XELL_ALT_BUTTON 15

/* gcc emits these in reverse: opts comes first in .bss */
static struct consoleinfo *info;
static FILE *opts;

void optOpen(const char *dir)
{
	char path[260];

	if (dir)
	{
		strcpy(path, dir);
		if (path[strlen(dir)] != '/')
		{
			strcat(path, "/");
		}
		strcat(path, "options.ini");
		opts = fopen(path, "wb");
	}
}

void optClose(void)
{
	if (opts)
	{
		fflush(opts);
		fclose(opts);
	}
}

void optWrite(const char *name, const char *value)
{
	if (opts)
	{
		fprintf(opts, "%s = %s;\n\n", name, value);
	}
}

void optLdv(uint8_t ldv)
{
	if (opts)
	{
		fprintf(opts, "cfldv = %d;\n\n", ldv);
	}
}

void optHex(const char *name, const uint8_t *key)
{
	int i;

	if (opts)
	{
		fprintf(opts, "%s = ", name);
		for (i = 0; i < 16; i++)
		{
			fprintf(opts, "%02X", key[i]);
		}
		fwrite("\n\n", 1, 2, opts);
	}
}

void optButton(const char *name, int code)
{
	if (!opts)
	{
		return;
	}
	switch (code)
	{
	case PWR_POWER:
		fprintf(opts, "%s = power; console power button\n\n", name);
		break;
	case PWR_IR_POWER:
		fprintf(opts, "%s = remopower; IR power button\n\n", name);
		break;
	case PWR_IR_GUIDE:
		fprintf(opts, "%s = remox; IR guide/X button\n\n", name);
		break;
	case PWR_IR_WINDOWS:
		fprintf(opts, "%s = winbutton; IR windows button\n\n", name);
		break;
	case PWR_KIOSK:
		fprintf(opts, "%s = kiosk; KIOSK debug pin\n\n", name);
		break;
	case PWR_WIRELESS:
		fprintf(opts, "%s = wirelessx; wireless controller\n\n", name);
		break;
	case PWR_WIRED_B1:
		if (IS_SLIM)
		{
			fprintf(opts, "%s = wiredxb1; wired controller (rear top usb port)\n\n", name);
		}
		else
		{
			fprintf(opts, "%s = wiredxb1; wired controller (INVALID FOR FATS!!)\n\n", name);
		}
		break;
	case PWR_WIRED_B2:
		if (IS_SLIM)
		{
			fprintf(opts, "%s = wiredxb2; wired controller (rear middle usb port)\n\n", name);
		}
		else
		{
			fprintf(opts, "%s = wiredxb2; wired controller (INVALID FOR FATS!!)\n\n", name);
		}
		break;
	case PWR_WIRED_B3:
		if (IS_SLIM)
		{
			fprintf(opts, "%s = wiredxb3; wired controller (rear bottom usb port)\n\n", name);
		}
		else
		{
			fprintf(opts, "%s = wiredxb3; wired controller (rear usb port)\n\n", name);
		}
		break;
	case PWR_WIRED_F1:
		if (IS_SLIM)
		{
			fprintf(opts, "%s = wiredxf1; wired controller (front left usb port)\n\n", name);
		}
		else
		{
			fprintf(opts, "%s = wiredxf1; wired controller (front top usb port)\n\n", name);
		}
		break;
	case PWR_WIRED_F2:
		if (IS_SLIM)
		{
			fprintf(opts, "%s = wiredxf2; wired controller (front right usb port)\n\n", name);
		}
		else
		{
			fprintf(opts, "%s = wiredxf2; wired controller (front bottom usb port)\n\n", name);
		}
		break;
	default:
		fprintf(opts, "%s = eject; console eject button\n\n", name);
		break;
	}
}

int showImageType(int level, int bootstrap, uint32_t nandType, uint32_t unused)
{
	char type[64];
	uint32_t t = bootstrap & BOOTSTRAP_CONSOLE_MASK;

	strcpy(type, getConsoleTypeStr(t + 1));
	switch (t + 1)
	{
	case CONSOLE_CORONA:
		if (nandType == NAND_SIZE_MMC)
		{
			strcat(type, "4g");
		}
		break;
	case CONSOLE_JASPER:
	case CONSOLE_TRINITY:
		if (nandType == NAND_SIZE_BIG_BLOCK)
		{
			/* bytes 4 and 8 of the response: the low bytes of
			   info->kernel and info->usvrFlags */
			if (((uint8_t *)info)[4] == 8 || (((uint8_t *)info)[8] & 8))
			{
				strcat(type, "bigffs");
			}
			else
			{
				strcat(type, "bb");
			}
		}
		break;
	}
	log_printf(level, "Image Type      : %s (", type);
	if (bootstrap < 0)	/* BOOTSTRAP_JTAG */
	{
		xb.type = BUILD_JTAG;
		log_printf(level, "JTAG");
	}
	else
	{
		xb.type = BUILD_GLITCH;
		if (bootstrap & BOOTSTRAP_GLITCH2)
		{
			xb.glitch2 = 1;
			log_printf(level, "Glitch2");
		}
		else if (bootstrap & BOOTSTRAP_GLITCH)
		{
			log_printf(level, "Glitch");
			if (!t)
			{
				log_printf(level, "-FAT");
			}
		}
		else if (bootstrap & BOOTSTRAP_GLITCH2M)
		{
			xb.glitch2mfg = 1;
			xb.glitch2 = 1;
			log_printf(level, "Glitch2M");
		}
	}
	log_printf(level, ")\n");
	optWrite("type", type);
	return setConsoleType(type);
}

int getFreebootOpts(int level, const char *dir)
{
	int i = findFile(FILE_FREEBOOT);
	uint8_t *p;
	int flags;

	log_printf(1, "retrieving USVR\\freeboot_bin...");
	xb.files[i].data = netGetFile("freeboot_bin", &xb.files[i].size);
	if (xb.files[i].data && xb.files[i].size)
	{
		char sig[] = "[v0.08 - inspired by ikari]";

		if (findInst(xb.files[i].data, xb.files[i].size, (uint8_t *)sig, sizeof sig - 1))
		{
			flags = xb.optFlags;
			log_printf(level, "parsing freeboot 0.08 core for opts\n");
			p = xb.files[i].data + FREEBOOT08_OPTS;
			xb.xellButton = p[FREEBOOT08_XELL_BUTTON];
			xb.dualButton = p[FREEBOOT08_DUAL_BUTTON];
			xb.xellAltButton = p[FREEBOOT08_XELL_ALT_BUTTON];
			flags = (flags & ~OPT_FREEBOOT_MASK) | (getBeU32(p) & OPT_FREEBOOT_MASK);
			log_printf(level, "Xell Reason     : ");
			logButton(level, xb.xellButton);
			optButton("xellbutton", xb.xellButton);
			if (xb.xellAltButton)
			{
				log_printf(level, "Xell Alt Reason : ");
				logButton(level, xb.xellAltButton);
				optButton("xellbutton2", xb.xellAltButton);
			}
			if (flags & OPT_UART_SLOW)
			{
				log_printf(level, "UART speed      : cygnos/demon speed set\n");
				optWrite("cygnos", "true");
			}
			if (xb.dualButton)
			{
				log_printf(level, "DualBoot Reason :");
				logButton(level, xb.dualButton);
				optButton("dualboot", xb.dualButton);
			}
		}
		else
		{
			log_printf(0, "\n*****WARNING: unrecognized freeboot binary on console! Using default options for xell/uart speed!\n");
			xb.xellButton = PWR_EJECT;
		}
		netFree(xb.files[i].data);
		xb.files[i].size = 0;
		return 1;
	}
	return 0;
}

int getFlashHdrOpts(int level, const char *dir)
{
	int len;	/* int, not uint32_t: the empty-header path returns len (0) */
	uint8_t *hdr;
	uint8_t flags;
	int ret;

	hdr = netGetFile("flash_hdr", (uint32_t *)&len);
	if (!hdr)
	{
		return 0;
	}
	if (!len)
	{
		return 0;
	}
	flags = hdr[HDR_OPTS];
	xb.optFlags |= flags & OPT_HDR_MASK;
	if (xb.type == BUILD_JTAG)
	{
		if (hdr[HDR_OPTS_VALID] != 1)
		{
			ret = getFreebootOpts(level, dir);
			netFree(hdr);
			return ret;
		}
		xb.dualButton = hdr[HDR_DUAL_BUTTON];
	}
	xb.xellButton = hdr[HDR_XELL_BUTTON];
	xb.xellAltButton = hdr[HDR_XELL_ALT_BUTTON];
	log_printf(level, "Xell Reason     : ");
	logButton(level, xb.xellButton);
	optButton("xellbutton", xb.xellButton);
	if (xb.xellAltButton)
	{
		log_printf(level, "Xell Alt Reason : ");
		logButton(level, xb.xellAltButton);
		optButton("xellbutton2", xb.xellAltButton);
	}
	if (flags & OPT_CYGNOS)
	{
		log_printf(level, "UART speed      : cygnos/demon speed set\n");
		optWrite("cygnos", "true");
	}
	if (flags & OPT_NODVD)
	{
		optWrite("nodvd", "true");
	}
	if (xb.dualButton)
	{
		optButton("dualboot", xb.dualButton);
	}
	netFree(hdr);
	return 1;
}

int showInfoKeys(int level, const char *dir, int *update)
{
	uint32_t sum;
	int cpuOk;
	int ret, ok;

	if (sumBytes(info->key1bl, sizeof info->key1bl) == KEY1BL_SUM)
	{
		optHex("1blkey", info->key1bl);
	}
	if (!checkZeros(info->cpuKey, sizeof info->cpuKey))
	{
		optHex("cpukey", info->cpuKey);
		log_printf(level, "CPU key         : ");
		showKey(level, info->cpuKey);
		checkCpuKey(level, info->cpuKey);
		log_printf(level, "\n");
	}
	optLdv(info->pairing);
	if (!checkZeros(info->dvdKey, sizeof info->dvdKey))
	{
		optHex("dvdkey", info->dvdKey);
		log_printf(level, "DVD key         : ");
		showKey(level, info->dvdKey);
		log_printf(level, "\n");
	}
	sum = sumBytes(info->key1bl, sizeof info->key1bl);
	log_printf(level, "1BL key         : ");
	showKey(level, info->key1bl);
	log_printf(level, " (%s)\n", sum == KEY1BL_SUM ? "good" : "bad");
	log_printf(level, "Fuses           : ");
	if (!checkZeros(info->fuses, sizeof info->fuses))
	{
		showFuses(level, "present", info->fuses);
	}
	else
	{
		log_printf(level, "not present\n");
	}
	log_printf(level, "Virtual Fuses   : ");
	if (!checkZeros(info->vfuses, sizeof info->vfuses))
	{
		showFuses(level, "present", info->vfuses);
	}
	else
	{
		log_printf(level, "not present\n");
	}
	/* one log call per key; gcc's jump threading splits it into the
	   good/bad calls (and puts their strings after vfuses.txt) */
	ok = sumBytes((const uint8_t *)&info->pub1bl, sizeof info->pub1bl) == PUB1BL_SUM;
	log_printf(level, "1BL RSA pub     : %s\n", ok ? "good" : "bad");
	if (ok)
	{
		if (update)
		{
			xb.pub1bl = &info->pub1bl;
		}
		if (dir)
		{
			writeFileIn(dir, "1BL_pub.bin", &info->pub1bl, sizeof info->pub1bl);
		}
	}
	ok = sumBytes((const uint8_t *)&info->pubPirs, sizeof info->pubPirs) == PUBPIRS_SUM;
	log_printf(level, "PIRS RSA pub    : %s\n", ok ? "good" : "bad");
	if (ok)
	{
		if (update)
		{
			xb.pubPirs = &info->pubPirs;
		}
		if (dir)
		{
			writeFileIn(dir, "PIRS_pub.bin", &info->pubPirs, sizeof info->pubPirs);
		}
	}
	ok = sumBytes((const uint8_t *)&info->pubMaster, sizeof info->pubMaster) == PUBMASTER_SUM;
	log_printf(level, "MASTER RSA pub  : %s\n", ok ? "good" : "bad");
	if (ok)
	{
		if (update)
		{
			xb.masterPub = &info->pubMaster;
		}
		if (dir)
		{
			writeFileIn(dir, "MAST_pub.bin", &info->pubMaster, sizeof info->pubMaster);
		}
	}
	if (dir)
	{
		if (!checkZeros(info->fuses, sizeof info->fuses))
		{
			writeFuseFile(dir, "fuses.txt", info->fuses);
		}
		if (!checkZeros(info->vfuses, sizeof info->vfuses))
		{
			writeFuseFile(dir, "vfuses.txt", info->vfuses);
		}
	}
	/* ret = 0 before the set1blKey test (not `&&`) keeps the result in edx */
	ret = 1;
	if (update)
	{
		log_printf(level, "\n");
		cpuOk = setCpuKey(level, info->cpuKey);
		ret = cpuOk == 1;
		if (set1blKey(info->key1bl) != 1)
		{
			ret = 0;
		}
	}
	return ret;
}

void showCurrentInfo(int level, int *hdd)
{
	uint32_t k;

	log_printf(level, "Console Current Info:\n");
	k = info->kernel;
	log_printf(level, "running kernel  : %d.%d.%d.%d\n", k >> 28, (k >> 24) & 0xf, (uint16_t)(k >> 8), k & 0xf);
	log_printf(level, "bootstrap type  : %s\n", getConsoleTypeStr((info->bootstrap & BOOTSTRAP_CONSOLE_MASK) + 1));
	log_printf(level, "hardware type   : %s\n", getConsoleTypeStr((info->hwFlags >> HW_CONSOLE_SHIFT) + 1));
	log_printf(level, "hardware flags  : 0x%08x\n", info->hwFlags);
	log_printf(level, "internal HDD    : %s\n", (info->hwFlags & HW_HDD) ? "present" : "not present");
	if ((info->hwFlags & HW_HDD) && hdd)
	{
		*hdd = 1;
	}
}

void setInfoKeys(void)
{
	xb.randomKeys = 0;
	if (!checkZeros(info->cbaNonce, sizeof info->cbaNonce))
	{
		setCbaNonce(info->cbaNonce);
	}
	if (!checkZeros(info->cbbNonce, sizeof info->cbbNonce))
	{
		setCbbNonce(info->cbbNonce);
	}
	if (!checkZeros(info->cdNonce, sizeof info->cdNonce))
	{
		setCdNonce(info->cdNonce);
	}
	if (!checkZeros(info->ceNonce, sizeof info->ceNonce))
	{
		setCeNonce(info->ceNonce);
	}
	if (!checkZeros(info->cfNonce, sizeof info->cfNonce))
	{
		setCfNonce(info->cfNonce);
	}
	if (!checkZeros(info->cgNonce, sizeof info->cgNonce))
	{
		setCgNonce(info->cgNonce);
	}
}

int parseConsoleInfo(int level, const char *dir, const char *optDir, int *update)
{
	int ret;

	info = netGetInfo();
	log_printf(level, "\n------ parsing console info response ------\n");
	showCurrentInfo(level, update);
	if (update && (uint8_t)info->version < PATCHES_UPDATE_VERSION)
	{
		log_printf(0, "\n*****ERROR: console hv patches are not recent enough to support update mode!\n");
		log_printf(0, "\n            update console patches and reboot before trying again.\n");
		optClose();
		return 0;
	}
	else if ((info->version & ~0xff) < USVR_MIN_VERSION << 8)
	{
		log_printf(0, "\n*****ERROR: updsvr on console needs to be updated!\n");
		return 0;
	}
	else
	{
		optOpen(optDir);
		if (showImageType(level, info->bootstrap, info->nandSize, info->blockSize)
		    && showInfoKeys(level, dir, update)
		    && getFlashHdrOpts(level, dir))
		{
			xb.cfLdv = info->pairing;
			log_printf(level, "CF LDV          : %d\n", xb.cfLdv);
			log_printf(level, "Pairing Value   : 0x%06x ", info->pairing >> 8);
			if (update)
			{
				setPairing(info->pairing >> 8);
			}
			else
			{
				log_printf(level, "\n");
			}
			setInfoKeys();
			ret = 1;
		}
		else
		{
			ret = 0;
		}
	}
	optClose();
	return ret;
}

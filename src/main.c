/* main: globals, signal handlers, console info, mode dispatch */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>

#include "xebuild.h"
#include "bootloaders.h"
#include "fileutil.h"
#include "image_write.h"
#include "keys.h"
#include "keyvault.h"
#include "log.h"
#include "main.h"
#include "mode_build.h"
#include "mode_client.h"
#include "mode_extract.h"
#include "mode_ini.h"
#include "mode_update.h"
#include "sysupdate.h"

#define XEBUILD_NAME "xeBuild"
#define XEBUILD_MAJOR 1
#define XEBUILD_MINOR 21
#define XEBUILD_BUILD "810"

/* gcc emits these in reverse: separator comes first in .data */
int promptEnter = 1;
char separator[] ="---------------------------------------------------------------\n";

static void sigHandler(int sig)
{
	printf("\n\nAn unhandled exception has occurred:\n\t");
	switch (sig) {
	case SIGABRT:
		puts("SIGABRT: abnormal termination triggered by abort call");
		break;
	case SIGFPE:
		puts("SIGFPE: floating point exception");
		break;
	case SIGILL:
		puts("SIGILL: illegal instruction");
		break;
	case SIGINT:
		puts("SIGINT: interrupt");
		break;
	case SIGSEGV:
		puts("SIGSEGV: segment violation");
		break;
	case SIGTERM:
	default:
		puts("SIGTERM: Software termination signal from kill");
		break;
	}
	puts("exiting...\n");
	exit(4);
}

void installSignals(void)
{
	signal(SIGABRT, sigHandler);
	signal(SIGFPE, sigHandler);
	signal(SIGILL, sigHandler);
	signal(SIGINT, sigHandler);
	signal(SIGSEGV, sigHandler);
	signal(SIGTERM, sigHandler);
}

int verifyFlashFile(int i)
{
	char *name;
	int ok = 0;

	if (xb.flashBuf[i]) {
		if (xb.flashSize[i]) {
			name = xb.flashFiles[i];
			if (!strnicmp(name, "fcrt.bin", 8)) {
				if (verifyFcrt(xb.flashBuf[i], xb.flashSize[i]))
					ok = 1;
			} else if (!strnicmp(name, "extended.bin", 12)) {
				if (verifyExtended(xb.flashBuf[i], xb.flashSize[i]))
					ok = 1;
			} else if (!strnicmp(name, "crl.bin", 7)) {
				if (verifyCrl(xb.flashBuf[i], xb.flashSize[i], 1)) {
					setCrlKey((uint8_t *)xb.flashBuf[i] + 288);
					ok = 1;
				}
			} else if (!strnicmp(name, "dae.bin", 7)) {
				if (verifyDae(xb.flashBuf[i], xb.flashSize[i])) {
					setDaeKey((uint8_t *)xb.flashBuf[i] + 288);
					ok = 1;
				}
			} else if (!strnicmp(name, "secdata.bin", 11)) {
				if (verifySecdata(xb.flashBuf[i], xb.flashSize[i])) {
					setSecdataKey((uint8_t *)xb.flashBuf[i] + 16);
					ok = 1;
				}
			} else if (!strnicmp(name, "odd.bin", 7)) {
				ok = 1;
			}
			if (ok) {
				log_printf(1, "verified! Will use if external file not found.\n");
				return 1;
			}
			log_printf(1, "verify failed! Discarding data.\n");
		}
		if (xb.flashBuf[i])
			free(xb.flashBuf[i]);
	}
	xb.flashBuf[i] = 0;
	xb.flashSize[i] = 0;
	return 0;
}

void logButton(int level, int code)
{
	switch (code) {
	case 0x11:
		log_printf(level, "power button\n");
		break;
	case 0x20:
		log_printf(level, "IR power button\n");
		break;
	case 0x22:
		log_printf(level, "IR guide/X button\n");
		break;
	case 0x24:
		log_printf(level, "IR windows button\n");
		break;
	case 0x41:
		log_printf(level, "KIOSK debug pin\n");
		break;
	case 0x55:
		log_printf(level, "wireless controller\n");
		break;
	case 0x59:
		if (IS_SLIM)
			log_printf(level, "wired controller (rear top usb port)\n");
		else
			log_printf(level, "wired controller (INVALID FOR FATS!!)\n");
		break;
	case 0x58:
		if (IS_SLIM)
			log_printf(level, "wired controller (rear middle usb port)\n");
		else
			log_printf(level, "wired controller (INVALID FOR FATS!!)\n");
		break;
	case 0x5a:
		if (IS_SLIM)
			log_printf(level, "wired controller (rear bottom usb port)\n");
		else
			log_printf(level, "wired controller (rear usb port)\n");
		break;
	case 0x56:
		if (IS_SLIM)
			log_printf(level, "wired controller (front left usb port)\n");
		else
			log_printf(level, "wired controller (front top usb port)\n");
		break;
	case 0x57:
		if (IS_SLIM)
			log_printf(level, "wired controller (front right usb port)\n");
		else
			log_printf(level, "wired controller (front bottom usb port)\n");
		break;
	default:
		log_printf(level, "console eject button\n");
		break;
	}
}

void showConsoleInfo(void)
{
	char buf[64];
	uint8_t *p;
	int i;
	uint32_t k;

	log_printf(0, separator);
	k = xb.kernel;
	if (k)
		log_printf(0, "Kernel    : %d.%d.%d.%d\n", k >> 28, (k >> 24) & 0xf,
			   (uint16_t)(k >> 8), k & 0xf);
	log_printf(0, "Console   : ");
	switch (xb.flags & 0x40000007) {
	case 1:
		log_printf(0, "Xenon\n");
		break;
	case 2:
		log_printf(0, "Zephyr\n");
		break;
	case 3:
		log_printf(0, "Falcon\n");
		break;
	case 4:
		log_printf(0, "Jasper\n");
		break;
	case 5:
		log_printf(0, "Trinity\n");
		break;
	case 0x40000005:
		log_printf(0, "Trinity (big block)\n");
		break;
	case 6:
		log_printf(0, "Corona\n");
		break;
	case 7:
		log_printf(0, "Winchester\n");
		break;
	case 0x40000004:
		log_printf(0, "Jasper (big block)\n");
		break;
	default:
		log_printf(0, "whoops, console type was not caught!\n");
		break;
	}
	log_printf(0, "NAND size : ");
	if (xb.flags & 0x10000000) {
		log_printf(0, "48MiB MMC (system only)");
	} else if (xb.flags & 0x40000000) {
		if (xb.nandMu)
			log_printf(0, "64MiB + NAND MU area");
		else
			log_printf(0, "64MiB (system only)");
		if (xb.flags & 0x20000000)
			log_printf(0, " (extended size FFS)");
	} else if (xb.type == 6 || xb.type == 8) {
		log_printf(0, "64MiB (small block)");
	} else {
		log_printf(0, "16MiB");
	}
	log_printf(0, "\n");
	log_printf(0, "Build     : ");
	switch (xb.type) {
	case 2:
		log_printf(0, "JTAG\n");
		break;
	case 3:
		if (xb.glitch2mfg)
			log_printf(0, "Glitch (v2 mfg)\n");
		else if (xb.glitch2)
			log_printf(0, "Glitch (v2)\n");
		else
			log_printf(0, "Glitch\n");
		break;
	case 1:
		log_printf(0, "Retail\n");
		break;
	case 6:
		log_printf(0, "Devkit\n");
		break;
	case 7:
		log_printf(0, "Devkit16\n");
		break;
	case 4:
		log_printf(0, "Devgl\n");
		break;
	case 5:
		log_printf(0, "Devgl16\n");
		break;
	case 8:
		log_printf(0, "Testkit\n");
		break;
	case 9:
		log_printf(0, "Testkit16\n");
		break;
	}
	if (xb.type >= 3 && xb.type <= 5) {
		log_printf(0, "Xell      : power on console with ");
		logButton(0, xb.xellButton);
		if (xb.xellAltButton) {
			log_printf(0, "XellAlt   : power on console with ");
			logButton(0, xb.xellAltButton);
		}
	} else if (xb.type == 2) {
		if (!(xb.bootFlags & 4)) {
			log_printf(0, "Xell      : starts if tray is ");
			if (!(xb.bootFlags & 2))
				log_printf(0, "fully out at boot time\n");
			else
				log_printf(0, "not closed at boot time\n");
		} else {
			log_printf(0, "Xell      : power on console with ");
			logButton(0, xb.xellButton);
			if (xb.xellAltButton) {
				log_printf(0, "XellAlt   : power on console with ");
				logButton(0, xb.xellAltButton);
			}
		}
		if (xb.dualButton) {
			log_printf(0, "Dualboot  : power on console with ");
			logButton(0, xb.dualButton);
		}
	}
	if ((xb.type == 2 || xb.type == 3) && (xb.bootFlags & 9))
		log_printf(0, "UART      : cygnos/demon speed set\n");
	p = kvGetConsoleId();
	if (p) {
		memcpy(buf, p, 12);
		buf[12] = 0;
		log_printf(0, "Serial    : %s\n", buf);
	}
	if (kvGetSerial(buf))
		log_printf(0, "ConsoleId : %s\n", buf);
	p = kvGetConsoleCert();
	if (p) {
		log_printf(0, "MoboSerial: ");
		for (i = 0; i < 8; i++)
			log_printf(0, "%02X", p[i]);
		log_printf(0, "\n");
	}
	if (kvGetMfgDate(buf))
		log_printf(0, "Mfg Date  : %s\n", buf);
	log_printf(0, "CPU Key   : ");
	showKey(0, xb.cpuKey);
	log_printf(0, "\n1BL Key   : ");
	showKey(0, xb.key1bl);
	log_printf(0, "\n");
	p = kvGetDvdKey();
	if (p) {
		log_printf(0, "DVD Key   : ");
		for (i = 0; i < 16; i++)
			log_printf(0, "%02X", p[i]);
		if (xb.bootFlags & 0x2000000) {
			if (xb.type == 1)
				log_printf(0, " (retail - not patched!)");
			else
				log_printf(0, " (patched)");
		}
		log_printf(0, "\n");
	}
	log_printf(0, "CF LDV    : %d\n", xb.cfLdv);
	if (kvIsLoaded()) {
		log_printf(0, "KV type   : ");
		switch (kvGetType()) {
		case 1:
			log_printf(0, "type2 (hashed - unchecked, master key not available)\n");
			break;
		case 2:
			log_printf(0, "type2 (hashed - Invalid! Keyvault is modified or from a different CPU key)\n");
			break;
		case 3:
			log_printf(0, "type2 (hashed - Good! Signature is valid.)\n");
			break;
		default:
			log_printf(0, "type1 (no hash)\n");
			break;
		}
	}
	if (xb.sha1Write && xb.sha1File[0])
		log_printf(0, "SHA-1 file: %s\n", xb.sha1File);
}

void initGlobals(void)
{
	int i;

	memset(&xb, 0, sizeof(xb));
	xb.bootFlags = 4;
	strcpy(xb.baseDir, "./");
	strcpy(xb.binDir, "./bin/");
	strcpy(xb.dataDir, "./data/");
	strcpy(xb.commonDir, "./common/");
	xb.randomKeys = 1;
	xb.sysTime = 1;
	/* TODO(xebuild.h cast): the 13 ints from cpuTemp to macid's padding,
	   set as one array; xb has named fields there now */
	for (i = 0; i < 13; i++)
		((int *)&xb.cpuTemp)[i] = -1;
}

void setBasePath(const char *argv0)
{
	char path[260];
	char *p;

	if (!argv0)
		return;
	strcpy(path, argv0);
	p = strrchr(path, '/');
	if (!p)
		p = strrchr(path, '\\');
	if (!p)
		return;
	*p = 0;
	if (!chdir(path))
		log_printf(0, "base path changed to %s\n", path);
}

int main(int argc, char **argv)
{
	int ret = 0;

	initGlobals();
	log_set_verbose(0);
	installSignals();
	log_init();
	log_printf(0, separator);
	log_printf(0, "     %s v%d.%02d.%s\n", XEBUILD_NAME, XEBUILD_MAJOR,
		   XEBUILD_MINOR, XEBUILD_BUILD);
	log_printf(0, separator);
	if (argc > 1) {
		setBasePath(argv[0]);
		if (!strnicmp(argv[1], "ini", 3)) {
			xb.mode = 4;
			log_printf(0, "---- { Ini Mode } ----\n");
			ret = mode_ini(argc - 2, argv + 2);
			goto done;
		} else if (!strnicmp(argv[1], "client", 6)) {
			log_printf(0, "---- { Client Mode } ----\n");
			xb.mode = 3;
			ret = mode_client(argc - 2, argv + 2);
			goto done;
		} else if (!strnicmp(argv[1], "update", 6)) {
			xb.mode = 2;
			log_printf(0, "---- { Update Mode } ----\n");
			ret = mode_update(argc - 2, argv + 2);
		} else if (!strnicmp(argv[1], "extract", 7)) {
			xb.mode = 5;
			log_printf(0, "---- { Extract Mode } ----\n");
			ret = mode_extract(argc - 2, argv + 2);
			goto done;
		} else {
			xb.mode = 1;
			log_printf(0, "---- { Image Build Mode } ----\n");
			if (!strnicmp(argv[1], "build", 5))
				ret = mode_build(argc - 2, argv + 2);
			else
				ret = mode_build(argc - 1, argv + 1);
		}
	} else {
		log_printf(0, "ERROR: invalid command line, you need to specify parameters!\n");
		build_usage();
	}
	if (!ret)
		showConsoleInfo();
done:
	suFree();
	imageFree();
	if (xb.iniBuf)
		free(xb.iniBuf);
	if (xb.pub1bl)
		free(xb.pub1bl);
	if (xb.pubPirs)
		free(xb.pubPirs);
	if (xb.masterPub)
		free(xb.masterPub);
	if (xb.prvKey)
		free(xb.prvKey);
	log_printf(0, separator);
	log_printf(0, "    %s Finished. Have a nice day.\n", XEBUILD_NAME);
	log_printf(0, separator);
	log_finish();
	if (promptEnter) {
		log_printf(0, "\npress <enter> to quit...\n");
		fgetc(stdin);
	}
	return ret;
}

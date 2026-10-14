/* consoleinfo: options.ini writing, parsing the console info response */
#include <stdio.h>
#include <string.h>

typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;

/* an input file fetched from the console or disk (build's table) */
struct flashent {
	int f000;
	int id;				/* 004 */
	int f008;
	u8 *data;			/* 00c */
	u32 size;			/* 010 */
	u8 pad014[0x42c - 0x014];
};

/* the parts of main.c's struct xebuild used here */
struct xebuild {
	int mode;			/* 000 */
	u32 flags;			/* 004 console type (& 7), NAND flags */
	u32 type;			/* 008 build type */
	u32 kernel;			/* 00c */
	int glitch2;			/* 010 */
	int glitch2mfg;			/* 014 */
	u8 pad018[0x020 - 0x018];
	int f020, f024;			/* 020 */
	u8 pad028[0x060 - 0x028];
	u32 bootFlags;			/* 060 */
	u8 pad064[0x068 - 0x064];
	int xellButton;			/* 068 */
	int xellAltButton;		/* 06c */
	int dualButton;			/* 070 */
	u8 pad074;
	u8 cfLdv;			/* 075 */
	u8 pad076[0x29c - 0x076];
	void *p29c;			/* 29c */
	void *masterPub;		/* 2a0 */
	void *p2a4;			/* 2a4 */
	u8 pad2a8[0x422b0 - 0x2a8];
	struct flashent files[34];	/* 422b0 */
};

/* the console's info response (net.c) */
struct consoleinfo {
	u32 version;			/* 000 updsvr version; low byte: hv patches */
	u32 kernel;			/* 004 */
	u32 f008;			/* 008 */
	u32 bootstrap;			/* 00c */
	u32 hwFlags;			/* 010 */
	u32 nandType;			/* 014 */
	u32 f018;			/* 018 */
	u32 pairing;			/* 01c ldv in the low byte */
	u8 cpuKey[16];			/* 020 */
	u8 dvdKey[16];			/* 030 */
	u8 fuses[96];			/* 040 */
	u8 vfuses[96];			/* 0a0 */
	u8 key1bl[16];			/* 100 */
	u8 pub1bl[272];			/* 110 */
	u8 pubPirs[272];		/* 220 */
	u8 pubMaster[272];		/* 330 */
	u8 keys[6][16];			/* 440 */
};

void log_printf(int level, const char *fmt, ...);
const char *getConsoleTypeStr(int type);
u32 getBeU32(const u8 *p);
int writeFileIn(const char *dir, const char *name, const void *buf, size_t size);
int writeFuseFile(const char *dir, const char *name, const u8 *fuses);
u8 *findInst(u8 *buf, int len, const u8 *pat, int patlen);
int checkZeros(const u8 *p, u32 len);
u32 sumBytes(const u8 *p, u32 len);
void showFuses(int level, const char *title, const u8 *fuses);
void showKey(int level, const u8 *key);
void logButton(int level, int code);
int setConsoleType(const char *name);
int findFile(int id);
u8 *netGetFile(const char *name, u32 *len);
struct consoleinfo *netGetInfo(void);
void netFree(void *p);
int checkCpuKey(int level, const u8 *key);
int setCpuKey(int level, const u8 *key);
int set1blKey(const u8 *key);
int setPairing(u32 pairing);
void setInfoKey0(const u8 *key);
void setInfoKey1(const u8 *key);
void setInfoKey2(const u8 *key);
void setInfoKey3(const u8 *key);
void setInfoKey4(const u8 *key);
void setInfoKey5(const u8 *key);

extern struct xebuild xb;

#define IS_SLIM ((xb.flags & 7) > 4)

/* gcc emits these in reverse: opts comes first in .bss */
static struct consoleinfo *info;
static FILE *opts;

void optOpen(const char *dir)
{
	char path[260];

	if (dir) {
		strcpy(path, dir);
		if (path[strlen(dir)] != '/')
			strcat(path, "/");
		strcat(path, "options.ini");
		opts = fopen(path, "wb");
	}
}

void optClose(void)
{
	if (opts) {
		fflush(opts);
		fclose(opts);
	}
}

void optWrite(const char *name, const char *value)
{
	if (opts)
		fprintf(opts, "%s = %s;\n\n", name, value);
}

void optLdv(u8 ldv)
{
	if (opts)
		fprintf(opts, "cfldv = %d;\n\n", ldv);
}

void optHex(const char *name, const u8 *key)
{
	int i;

	if (opts) {
		fprintf(opts, "%s = ", name);
		for (i = 0; i < 16; i++)
			fprintf(opts, "%02X", key[i]);
		fwrite("\n\n", 1, 2, opts);
	}
}

void optButton(const char *name, int code)
{
	if (!opts)
		return;
	switch (code) {
	case 0x11:
		fprintf(opts, "%s = power; console power button\n\n", name);
		break;
	case 0x20:
		fprintf(opts, "%s = remopower; IR power button\n\n", name);
		break;
	case 0x22:
		fprintf(opts, "%s = remox; IR guide/X button\n\n", name);
		break;
	case 0x24:
		fprintf(opts, "%s = winbutton; IR windows button\n\n", name);
		break;
	case 0x41:
		fprintf(opts, "%s = kiosk; KIOSK debug pin\n\n", name);
		break;
	case 0x55:
		fprintf(opts, "%s = wirelessx; wireless controller\n\n", name);
		break;
	case 0x59:
		if (IS_SLIM)
			fprintf(opts, "%s = wiredxb1; wired controller (rear top usb port)\n\n", name);
		else
			fprintf(opts, "%s = wiredxb1; wired controller (INVALID FOR FATS!!)\n\n", name);
		break;
	case 0x58:
		if (IS_SLIM)
			fprintf(opts, "%s = wiredxb2; wired controller (rear middle usb port)\n\n", name);
		else
			fprintf(opts, "%s = wiredxb2; wired controller (INVALID FOR FATS!!)\n\n", name);
		break;
	case 0x5a:
		if (IS_SLIM)
			fprintf(opts, "%s = wiredxb3; wired controller (rear bottom usb port)\n\n", name);
		else
			fprintf(opts, "%s = wiredxb3; wired controller (rear usb port)\n\n", name);
		break;
	case 0x56:
		if (IS_SLIM)
			fprintf(opts, "%s = wiredxf1; wired controller (front left usb port)\n\n", name);
		else
			fprintf(opts, "%s = wiredxf1; wired controller (front top usb port)\n\n", name);
		break;
	case 0x57:
		if (IS_SLIM)
			fprintf(opts, "%s = wiredxf2; wired controller (front right usb port)\n\n", name);
		else
			fprintf(opts, "%s = wiredxf2; wired controller (front bottom usb port)\n\n", name);
		break;
	default:
		fprintf(opts, "%s = eject; console eject button\n\n", name);
		break;
	}
}

int showImageType(int level, int bootstrap, u32 nandType, u32 unused)
{
	char type[64];
	u32 t = bootstrap & 0xf;

	strcpy(type, getConsoleTypeStr(t + 1));
	switch (t + 1) {
	case 6:
		if (nandType == 0x3000000)
			strcat(type, "4g");
		break;
	case 4:
	case 5:
		if (nandType == 0x4200000) {
			if (((u8 *)info)[4] == 8 || (((u8 *)info)[8] & 8))
				strcat(type, "bigffs");
			else
				strcat(type, "bb");
		}
		break;
	}
	log_printf(level, "Image Type      : %s (", type);
	if (bootstrap < 0) {
		xb.type = 2;
		log_printf(level, "JTAG");
	} else {
		xb.type = 3;
		if (bootstrap & 0x20000000) {
			xb.glitch2 = 1;
			log_printf(level, "Glitch2");
		} else if (bootstrap & 0x40000000) {
			log_printf(level, "Glitch");
			if (!t)
				log_printf(level, "-FAT");
		} else if (bootstrap & 0x10000000) {
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
	int i = findFile(22);
	u8 *p;
	int flags;

	log_printf(1, "retrieving USVR\\freeboot_bin...");
	xb.files[i].data = netGetFile("freeboot_bin", &xb.files[i].size);
	if (xb.files[i].data && xb.files[i].size) {
		char sig[] = "[v0.08 - inspired by ikari]";

		if (findInst(xb.files[i].data, xb.files[i].size, (u8 *)sig, 27)) {
			flags = xb.bootFlags;
			log_printf(level, "parsing freeboot 0.08 core for opts\n");
			p = xb.files[i].data + 2464;
			xb.xellButton = p[7];
			xb.dualButton = p[11];
			xb.xellAltButton = p[15];
			flags = (flags & ~0xf) | (getBeU32(p) & 0xf);
			log_printf(level, "Xell Reason     : ");
			logButton(level, xb.xellButton);
			optButton("xellbutton", xb.xellButton);
			if (xb.xellAltButton) {
				log_printf(level, "Xell Alt Reason : ");
				logButton(level, xb.xellAltButton);
				optButton("xellbutton2", xb.xellAltButton);
			}
			if (flags & 9) {
				log_printf(level, "UART speed      : cygnos/demon speed set\n");
				optWrite("cygnos", "true");
			}
			if (xb.dualButton) {
				log_printf(level, "DualBoot Reason :");
				logButton(level, xb.dualButton);
				optButton("dualboot", xb.dualButton);
			}
		} else {
			log_printf(0, "\n*****WARNING: unrecognized freeboot binary on console! Using default options for xell/uart speed!\n");
			xb.xellButton = 18;
		}
		netFree(xb.files[i].data);
		xb.files[i].size = 0;
		return 1;
	}
	return 0;
}

int getFlashHdrOpts(int level, const char *dir)
{
	int len;	/* int, not u32: the empty-header path returns len (0) */
	u8 *hdr;
	u8 flags;
	int ret;

	hdr = netGetFile("flash_hdr", (u32 *)&len);
	if (!hdr)
		return 0;
	if (!len)
		return 0;
	flags = hdr[77];
	xb.bootFlags |= flags & 7;
	if (xb.type == 2) {
		if (hdr[75] != 1) {
			ret = getFreebootOpts(level, dir);
			netFree(hdr);
			return ret;
		}
		xb.dualButton = hdr[76];
	}
	xb.xellButton = hdr[79];
	xb.xellAltButton = hdr[78];
	log_printf(level, "Xell Reason     : ");
	logButton(level, xb.xellButton);
	optButton("xellbutton", xb.xellButton);
	if (xb.xellAltButton) {
		log_printf(level, "Xell Alt Reason : ");
		logButton(level, xb.xellAltButton);
		optButton("xellbutton2", xb.xellAltButton);
	}
	if (flags & 1) {
		log_printf(level, "UART speed      : cygnos/demon speed set\n");
		optWrite("cygnos", "true");
	}
	if (flags & 2)
		optWrite("nodvd", "true");
	if (xb.dualButton)
		optButton("dualboot", xb.dualButton);
	netFree(hdr);
	return 1;
}

int showInfoKeys(int level, const char *dir, int *update)
{
	u32 sum;
	int cpuOk;
	int ret, ok;

	if (sumBytes(info->key1bl, 16) == 0x983)
		optHex("1blkey", info->key1bl);
	/* code-free hint: the blocks this adds (until fab drops them) shift
	   dom2's block numbers, so it duplicates the MASTER key check for the
	   dir != 0 path first, as the original did; that block order decides
	   which register peephole2 picks to test `update` in each copy */
	if (level < 0)
		__builtin_unreachable();
	if (!checkZeros(info->cpuKey, 16)) {
		optHex("cpukey", info->cpuKey);
		log_printf(level, "CPU key         : ");
		showKey(level, info->cpuKey);
		checkCpuKey(level, info->cpuKey);
		log_printf(level, "\n");
	}
	optLdv(info->pairing);
	if (!checkZeros(info->dvdKey, 16)) {
		optHex("dvdkey", info->dvdKey);
		log_printf(level, "DVD key         : ");
		showKey(level, info->dvdKey);
		log_printf(level, "\n");
	}
	sum = sumBytes(info->key1bl, 16);
	log_printf(level, "1BL key         : ");
	showKey(level, info->key1bl);
	log_printf(level, " (%s)\n", sum == 0x983 ? "good" : "bad");
	log_printf(level, "Fuses           : ");
	if (!checkZeros(info->fuses, 96))
		showFuses(level, "present", info->fuses);
	else
		log_printf(level, "not present\n");
	log_printf(level, "Virtual Fuses   : ");
	if (!checkZeros(info->vfuses, 96))
		showFuses(level, "present", info->vfuses);
	else
		log_printf(level, "not present\n");
	/* one log call per key; gcc's jump threading splits it into the
	   good/bad calls (and puts their strings after vfuses.txt) */
	ok = sumBytes(info->pub1bl, 272) == 0x79c7;
	log_printf(level, "1BL RSA pub     : %s\n", ok ? "good" : "bad");
	if (ok) {
		if (update)
			xb.p29c = info->pub1bl;
		if (dir)
			writeFileIn(dir, "1BL_pub.bin", info->pub1bl, 272);
	}
	ok = sumBytes(info->pubPirs, 272) == 0x80d0;
	log_printf(level, "PIRS RSA pub    : %s\n", ok ? "good" : "bad");
	if (ok) {
		if (update)
			xb.p2a4 = info->pubPirs;
		if (dir)
			writeFileIn(dir, "PIRS_pub.bin", info->pubPirs, 272);
	}
	ok = sumBytes(info->pubMaster, 272) == 0x843c;
	log_printf(level, "MASTER RSA pub  : %s\n", ok ? "good" : "bad");
	if (ok) {
		if (update)
			xb.masterPub = info->pubMaster;
		if (dir)
			writeFileIn(dir, "MAST_pub.bin", info->pubMaster, 272);
	}
	if (dir) {
		if (!checkZeros(info->fuses, 96))
			writeFuseFile(dir, "fuses.txt", info->fuses);
		if (!checkZeros(info->vfuses, 96))
			writeFuseFile(dir, "vfuses.txt", info->vfuses);
	}
	/* ret = 0 before the set1blKey test (not `&&`) keeps the result in edx */
	ret = 1;
	if (update) {
		log_printf(level, "\n");
		cpuOk = setCpuKey(level, info->cpuKey);
		ret = cpuOk == 1;
		if (set1blKey(info->key1bl) != 1)
			ret = 0;
	}
	return ret;
}

void showCurrentInfo(int level, int *hdd)
{
	u32 k;

	log_printf(level, "Console Current Info:\n");
	k = info->kernel;
	log_printf(level, "running kernel  : %d.%d.%d.%d\n", k >> 28, (k >> 24) & 0xf, (u16)(k >> 8), k & 0xf);
	log_printf(level, "bootstrap type  : %s\n", getConsoleTypeStr((info->bootstrap & 0xf) + 1));
	log_printf(level, "hardware type   : %s\n", getConsoleTypeStr((info->hwFlags >> 28) + 1));
	log_printf(level, "hardware flags  : 0x%08x\n", info->hwFlags);
	log_printf(level, "internal HDD    : %s\n", (info->hwFlags & 0x20) ? "present" : "not present");
	if ((info->hwFlags & 0x20) && hdd)
		*hdd = 1;
}

void setInfoKeys(void)
{
	xb.f020 = 0;
	if (!checkZeros(info->keys[0], 16))
		setInfoKey0(info->keys[0]);
	if (!checkZeros(info->keys[1], 16))
		setInfoKey1(info->keys[1]);
	if (!checkZeros(info->keys[2], 16))
		setInfoKey2(info->keys[2]);
	if (!checkZeros(info->keys[3], 16))
		setInfoKey3(info->keys[3]);
	if (!checkZeros(info->keys[4], 16))
		setInfoKey4(info->keys[4]);
	if (!checkZeros(info->keys[5], 16))
		setInfoKey5(info->keys[5]);
}

int parseConsoleInfo(int level, const char *dir, const char *optDir, int *update)
{
	int ret;

	info = netGetInfo();
	log_printf(level, "\n------ parsing console info response ------\n");
	showCurrentInfo(level, update);
	if (update && (u8)info->version <= 1) {
		log_printf(0, "\n*****ERROR: console hv patches are not recent enough to support update mode!\n");
		log_printf(0, "\n            update console patches and reboot before trying again.\n");
		optClose();
		return 0;
	} else if ((info->version & ~0xff) <= 0x2ff) {
		log_printf(0, "\n*****ERROR: updsvr on console needs to be updated!\n");
		return 0;
	} else {
		optOpen(optDir);
		if (showImageType(level, info->bootstrap, info->nandType, info->f018)
		    && showInfoKeys(level, dir, update)
		    && getFlashHdrOpts(level, dir)) {
			xb.cfLdv = info->pairing;
			log_printf(level, "CF LDV          : %d\n", xb.cfLdv);
			log_printf(level, "Pairing Value   : 0x%06x ", info->pairing >> 8);
			if (update)
				setPairing(info->pairing >> 8);
			else
				log_printf(level, "\n");
			setInfoKeys();
			ret = 1;
		} else
			ret = 0;
	}
	optClose();
	return ret;
}

/* options: console types (xenon...corona), boot options from the command
   line, options.ini and perbox files, optional patches */
#include <stdio.h>
#include <string.h>

typedef unsigned char u8;
typedef unsigned int u32;

/* the parts of main.c's struct xebuild used here */
struct xebuild {
	int mode;			/* 000 */
	u32 flags;			/* 004 console type (& 7), NAND flags */
	u32 type;			/* 008 build type */
	u8 pad00c[0x060 - 0x00c];
	u32 bootFlags;			/* 060 options turned on */
	u32 bootFlagsOff;		/* 064 options turned off */
	int xellButton;			/* 068 */
	int xellAltButton;		/* 06c */
	int dualButton;			/* 070 */
	u8 pad074;
	u8 cfLdv;			/* 075 */
	u8 pad076[0x078 - 0x076];
	u32 cpuTemp;			/* 078 */
	u32 gpuTemp;			/* 07c */
	u32 edramTemp;			/* 080 */
	u32 overCpuTemp;		/* 084 */
	u32 overGpuTemp;		/* 088 */
	u32 overEdramTemp;		/* 08c */
	u32 cpuFan;			/* 090 */
	u32 gpuFan;			/* 094 */
	u32 avRegion;			/* 098 */
	u32 gameRegion;			/* 09c */
	u32 dvdRegion;			/* 0a0 */
	u8 macid[6];			/* 0a4 */
	u8 pad0aa[0xaac - 0x0aa];
	char outName[0x400];		/* aac */
	char baseDir[0x400];		/* eac */
	u8 pad12ac[0x46df4 - 0x12ac];
	char patches[16][0x42c];	/* 46df4 */
	char blSuffix[0x40];		/* 4b0b4 */
	int numPatches;			/* 4b0f4 */
	u8 pad4b0f8[0x4b100 - 0x4b0f8];
	struct {
		char name[0x400];
		u32 offset;
	} rawPatches[16];		/* 4b100 */
	int numRawPatches;		/* 4f140 */
};

void log_printf(int level, const char *fmt, ...);
int FileExists(const char *name);
char *getIniValue(const char *key);
int getIniBool(const char *key, int def);
char *iniBoolInvalid(const char *key);
u32 getIniU32(const char *key, u32 def);
char *iniU32Invalid(const char *key);
u32 myatou32(char *dat, u32 defValue);
unsigned char myatox8(char *dat);
u32 validateString(char *nString);
void showHexPairs(unsigned int level, const char *s);
int kvSetDvdKey(char *key);
void applyIniOptions(void);

extern struct xebuild xb;

int baseFileExists(const char *name)
{
	char path[1024];

	if (!xb.baseDir[0])
		return 0;
	strcpy(path, xb.baseDir);
	strcat(path, name);
	return FileExists(path);
}

/* name or name.txt in the per box directory */
int perboxExists(const char *name)
{
	char txt[1024];

	strcpy(txt, name);
	strcat(txt, ".txt");
	return baseFileExists(name) | baseFileExists(txt);
}

int iniConsoleType(void)
{
	if (perboxExists("xenon")) {
		log_printf(1, "Using xenon ctype (perbox file)\n");
		xb.flags |= 1;
		strcat(xb.outName, "xenon");
	} else if (perboxExists("zephyr")) {
		log_printf(1, "Using zephyr ctype (perbox file)\n");
		xb.flags |= 2;
		strcat(xb.outName, "zephyr");
	} else if (perboxExists("falcon")) {
		log_printf(1, "Using falcon ctype (perbox file)\n");
		xb.flags |= 3;
		strcat(xb.outName, "falcon");
	} else if (perboxExists("jasper") | perboxExists("jasperbc")) {
		log_printf(1, "Using jasper ctype (perbox file)\n");
		xb.flags |= 0x80000004;
		strcat(xb.outName, "jasper");
	} else if (perboxExists("jaspersb")) {
		log_printf(1, "Using jasper smallblock ctype (perbox file)\n");
		xb.flags |= 4;
		strcat(xb.outName, "jasper");
	} else if (perboxExists("jasperbb")) {
		log_printf(1, "Using jasper big block ctype (perbox file)\n");
		xb.flags |= 0x40000004;
		strcat(xb.outName, "jasperbb");
	} else if (perboxExists("jasper256")) {
		log_printf(1, "Using jasper big block ctype (perbox file)\n");
		xb.flags |= 0x40000004;
		strcat(xb.outName, "jasper256");
	} else if (perboxExists("jasper512")) {
		log_printf(1, "Using jasper big block ctype (perbox file)\n");
		xb.flags |= 0x40000004;
		strcat(xb.outName, "jasper512");
	} else if (perboxExists("trinity")) {
		log_printf(1, "Using trinity ctype (perbox file)\n");
		xb.flags |= 0x80000005;
		strcat(xb.outName, "trinity");
	} else if (perboxExists("trinitybb")) {
		log_printf(1, "Using trinity big block ctype (perbox file)\n");
		xb.flags |= 0x40000005;
		strcat(xb.outName, "trinitybb");
	} else if (perboxExists("trinitybigffs")) {
		log_printf(1, "Using trinity big block big file system ctype (perbox file)\n");
		xb.flags |= 0x60000005;
		strcat(xb.outName, "trinitybigffs");
	} else if (perboxExists("corona")) {
		log_printf(1, "Using corona ctype (perbox file)\n");
		xb.flags |= 0x80000006;
		strcat(xb.outName, "corona");
	} else if (perboxExists("coronabb")) {
		log_printf(1, "Using corona big block ctype (perbox file)\n");
		xb.flags |= 0x40000006;
		strcat(xb.outName, "coronabb");
	} else if (perboxExists("coronabigffs")) {
		log_printf(1, "Using corona big block big file system ctype (perbox file)\n");
		xb.flags |= 0x60000006;
		strcat(xb.outName, "coronabigffs");
	} else if (perboxExists("corona4g")) {
		log_printf(1, "Using corona MMC ctype (perbox file)\n");
		xb.flags |= 0x90000006;
		strcat(xb.outName, "corona4g");
	} else if (perboxExists("winchester")) {
		log_printf(1, "Using winchester ctype (perbox file)\n");
		xb.flags |= 0x80000007;
		strcat(xb.outName, "winchester");
	} else if (perboxExists("winchester4g")) {
		log_printf(1, "Using winchester MMC ctype (perbox file)\n");
		xb.flags |= 0x90000007;
		strcat(xb.outName, "winchester4g");
	} else if (perboxExists("winchesterbb")) {
		log_printf(1, "Using winchester big block ctype (perbox file)\n");
		xb.flags |= 0x40000007;
		strcat(xb.outName, "winchesterbb");
	} else if (perboxExists("winchesterbigffs")) {
		log_printf(1, "Using winchester big block big file system ctype (perbox file)\n");
		xb.flags |= 0x60000007;
		strcat(xb.outName, "winchesterbigffs");
	}
	return (xb.flags & 7) != 0;
}

int setConsoleType(const char *name)
{
	if (!name || !*name)
		return 0;
	if (!stricmp(name, "xenon")) {
		xb.flags |= 1;
		strcat(xb.outName, "xenon");
		return 1;
	}
	if (!stricmp(name, "zephyr")) {
		xb.flags |= 2;
		strcat(xb.outName, "zephyr");
		return 1;
	}
	if (!stricmp(name, "falcon")) {
		xb.flags |= 3;
		strcat(xb.outName, "falcon");
		return 1;
	}
	if (!stricmp(name, "jasper") || !stricmp(name, "jasperbc")) {
		xb.flags |= 0x80000004;
		strcat(xb.outName, "jasper");
		return 1;
	}
	if (!stricmp(name, "jaspersb")) {
		xb.flags |= 4;
		strcat(xb.outName, "jasper");
		return 1;
	}
	if (!stricmp(name, "jasperbb")) {
		xb.flags |= 0x40000004;
		strcat(xb.outName, "jasperbb");
		return 1;
	}
	if (!stricmp(name, "jasper256")) {
		xb.flags |= 0x40000004;
		strcat(xb.outName, "jasper256");
		return 1;
	}
	if (!stricmp(name, "jasper512")) {
		xb.flags |= 0x40000004;
		strcat(xb.outName, "jasper512");
		return 1;
	}
	if (!stricmp(name, "jasperbigffs")) {
		xb.flags |= 0x60000004;
		strcat(xb.outName, "jasperbigffs");
		return 1;
	}
	if (!stricmp(name, "trinity")) {
		xb.flags |= 0x80000005;
		strcat(xb.outName, "trinity");
		return 1;
	}
	if (!stricmp(name, "trinitybb")) {
		xb.flags |= 0x40000005;
		strcat(xb.outName, "trinitybb");
		return 1;
	}
	if (!stricmp(name, "trinitybigffs")) {
		xb.flags |= 0x60000005;
		strcat(xb.outName, "trinitybigffs");
		return 1;
	}
	if (!stricmp(name, "corona")) {
		xb.flags |= 0x80000006;
		strcat(xb.outName, "corona");
		return 1;
	}
	if (!stricmp(name, "coronabb")) {
		xb.flags |= 0x40000006;
		strcat(xb.outName, "coronabb");
		return 1;
	}
	if (!stricmp(name, "coronabigffs")) {
		xb.flags |= 0x60000006;
		strcat(xb.outName, "coronabigffs");
		return 1;
	}
	if (!stricmp(name, "corona4g")) {
		xb.flags |= 0x90000006;
		strcat(xb.outName, "corona4g");
		return 1;
	}
	if (!stricmp(name, "winchester")) {
		xb.flags |= 0x80000007;
		strcat(xb.outName, "winchester");
		return 1;
	}
	if (!stricmp(name, "winchester4g")) {
		xb.flags |= 0x90000007;
		strcat(xb.outName, "winchester4g");
		return 1;
	}
	if (!stricmp(name, "winchesterbb")) {
		xb.flags |= 0x40000007;
		strcat(xb.outName, "winchesterbb");
		return 1;
	}
	if (!stricmp(name, "winchesterbigffs")) {
		xb.flags |= 0x60000007;
		strcat(xb.outName, "winchesterbigffs");
		return 1;
	}
	return 0;
}

/* a boolean option from a perbox file or options.ini, unless the command
   line already set it either way */
_Bool optIniBool(const char *name, u32 set, u32 clear, int def)
{
	char *bad;

	if ((xb.bootFlags & set) || (xb.bootFlagsOff & set))
		return 0;
	if (perboxExists(name)) {
		log_printf(1, "Using %s option (perbox file)\n", name);
	} else {
		bad = iniBoolInvalid(name);
		if (bad) {
			log_printf(0, "***** WARNING: options.ini setting '%s' invalid value '%s', discarding!\n", name, bad);
			return 0;
		}
		if (!getIniBool(name, def))
			return 0;
		log_printf(1, "Using %s option (ini file)\n", name);
	}
	xb.bootFlags = (xb.bootFlags & ~clear) | set;
	return 1;
}

int optIniInt(const char *name, int def)
{
	char *bad;

	bad = iniU32Invalid(name);
	if (bad) {
		log_printf(0, "***** WARNING: options.ini setting '%s' invalid value '%s', discarding!\n", name, bad);
		return def;
	}
	return getIniU32(name, def);
}

int parseButton(const char *s)
{
	int b = 0;

	if (!s)
		return 0;
	if (!strnicmp(s, "power", 5))
		b = 0x11;
	else if (!strnicmp(s, "remopower", 9))
		b = 0x20;
	else if (!strnicmp(s, "remox", 5))
		b = 0x22;
	else if (!strnicmp(s, "winbutton", 9))
		b = 0x24;
	else if (!strnicmp(s, "wirelessx", 9))
		b = 0x55;
	else if (!strnicmp(s, "wiredx", 6)) {
		if (!strnicmp(s, "wiredxb1", 8))
			b = 0x59;
		else if (!strnicmp(s, "wiredxb2", 8))
			b = 0x58;
		else if (!strnicmp(s, "wiredxb3", 8))
			b = 0x5a;
		else if (!strnicmp(s, "wiredxf1", 8))
			b = 0x56;
		else if (!strnicmp(s, "wiredxf2", 8))
			b = 0x57;
		else
			b = 0x5a;
	} else if (!strnicmp(s, "eject", 5))
		b = 0x12;
	else if (!strnicmp(s, "kiosk", 5))
		b = 0x41;
	return b;
}

void stripColons(char *s)
{
	int i, j, len;

	len = strlen(s) + 1;
	for (i = 0, j = 0; i < len; i++)
		if (s[i] != ':')
			s[j++] = s[i];
}

int macidSet(void)
{
	int i;

	for (i = 0; i < 6; i++)
		if (xb.macid[i] != 0xff)
			return 1;
	return 0;
}

/* a boolean option given as name, name=true or name=false */
/* a boolean option given as name, name=true or name=false */
int setBoolOption(const char *name, const char *val)
{
	u32 off = 0;

	if (val) {
		if (!stricmp(val, "false"))
			off = 1;
		else if (stricmp(val, "true"))
			return 0;
	}
	if (!stricmp(name, "nodvd")) {
		if (off)
			xb.bootFlagsOff |= 2;
		else {
			xb.bootFlags &= ~4;
			xb.bootFlags |= 2;
			log_printf(1, "Using NODVD (tray status fully open check) option");
		}
		return 1;
	}
	if (!stricmp(name, "olddvd")) {
		if (off)
			xb.bootFlagsOff |= 6;
		else {
			xb.bootFlags &= ~4;
			log_printf(1, "Using OLDDVD (tray status not closed check) option");
		}
		return 1;
	}
	if (!stricmp(name, "cygnos")) {
		if (off)
			xb.bootFlagsOff |= 1;
		else {
			xb.bootFlags |= 1;
			log_printf(1, "Using CYGNOS option");
		}
		return 1;
	}
	if (!stricmp(name, "demon")) {
		if (off)
			xb.bootFlagsOff |= 8;
		else {
			xb.bootFlags |= 8;
			log_printf(1, "Using DEMON option");
		}
		return 1;
	}
	if (!stricmp(name, "nomobile")) {
		if (off)
			xb.bootFlagsOff |= 0x20000000;
		else {
			xb.bootFlags |= 0x20000000;
			log_printf(1, "Using NOMOBILE option");
		}
		return 1;
	}
	if (!stricmp(name, "smcnocheck")) {
		if (off)
			xb.bootFlagsOff |= 0x200000;
		else {
			xb.bootFlags |= 0x200000;
			log_printf(1, "Using SMCNOCHECK option");
		}
		return 1;
	}
	if (!stricmp(name, "noremap")) {
		if (off)
			xb.bootFlagsOff |= 0x40000000;
		else {
			xb.bootFlags |= 0x40000000;
			log_printf(1, "Using NOREMAP option");
		}
		return 1;
	}
	if (!stricmp(name, "noecdremap")) {
		if (off)
			xb.bootFlagsOff |= 0x80000000;
		else {
			xb.bootFlags |= 0x80000000;
			log_printf(1, "Using NOECDREMAP option");
		}
		return 1;
	}
	if (!stricmp(name, "nandmu")) {
		if (off)
			xb.bootFlagsOff |= 0x10000000;
		else {
			xb.bootFlags |= 0x10000000;
			log_printf(1, "Using NANDMU option");
		}
		return 1;
	}
	if (!stricmp(name, "nosecurity")) {
		if (off)
			xb.bootFlagsOff |= 0x4000000;
		else {
			xb.bootFlags |= 0x4000000;
			log_printf(1, "Using NOSECURITY option");
		}
		return 1;
	}
	if (!stricmp(name, "nosusecurity")) {
		if (off)
			xb.bootFlagsOff |= 0x1000000;
		else {
			xb.bootFlags |= 0x1000000;
			log_printf(1, "Using NOSECURITY option");
		}
		return 1;
	}
	if (!stricmp(name, "patchsmc")) {
		if (off)
			xb.bootFlagsOff |= 0x8000000;
		else {
			xb.bootFlags |= 0x8000000;
			log_printf(1, "Using PATCHSMC option");
		}
		return 1;
	}
	if (!stricmp(name, "smcnoeject")) {
		if (off)
			xb.bootFlagsOff |= 0x400000;
		else {
			xb.bootFlags |= 0x400000;
			log_printf(1, "Using SMCNOEJECT option");
		}
		return 1;
	}
	if (!stricmp(name, "smcnoblink")) {
		if (off)
			xb.bootFlagsOff |= 0x800000;
		else {
			xb.bootFlags |= 0x800000;
			log_printf(1, "Using SMCNOBLINK option");
		}
		return 1;
	}
	return 0;
}

/* one name[=value] from the command line option string */
u32 parseOption(char *opt)
{
	char *val = NULL;
	int i, len, vlen;

	len = strlen(opt);
	for (i = 0; i < len; i++) {
		if (opt[i] == '=') {
			val = &opt[i + 1];
			opt[i] = 0;
			if (!*val) {
				log_printf(1, "\n\n***** ERROR: option '%s' provided on command line with = but no value!\n", opt);
				return 0;
			}
			i = len + 1;
		}
	}
	if (len == strlen(opt)) {
		if (setBoolOption(opt, val) == 1)
			goto done;
		if (!val)
			goto incomplete;
		vlen = 0;
	} else {
		vlen = strlen(val);
		if (setBoolOption(opt, val) == 1)
			goto done;
	}
	if (!stricmp(opt, "cputemp")) {
		xb.cpuTemp = myatou32(val, -1);
		if (xb.cpuTemp == -1)
			goto bad;
		log_printf(1, "Using CPUTEMP option, value %d\n", xb.cpuTemp);
		return 1;
	}
	if (!stricmp(opt, "gputemp")) {
		xb.gpuTemp = myatou32(val, -1);
		if (xb.gpuTemp == -1)
			goto bad;
		log_printf(1, "Using GPUTEMP option, value %d\n", xb.gpuTemp);
		return 1;
	}
	if (!stricmp(opt, "edramtemp")) {
		xb.edramTemp = myatou32(val, -1);
		if (xb.edramTemp == -1)
			goto bad;
		log_printf(1, "Using EDRAMTEMP option, value %d\n", xb.edramTemp);
		return 1;
	}
	if (!stricmp(opt, "overcputemp")) {
		xb.overCpuTemp = myatou32(val, -1);
		if (xb.overCpuTemp == -1)
			goto bad;
		log_printf(1, "Using OVERCPUTEMP option, value %d\n", xb.overCpuTemp);
		return 1;
	}
	if (!stricmp(opt, "overgputemp")) {
		xb.overGpuTemp = myatou32(val, -1);
		if (xb.overGpuTemp == -1)
			goto bad;
		log_printf(1, "Using OVERGPUTEMP option, value %d\n", xb.overGpuTemp);
		return 1;
	}
	if (!stricmp(opt, "overedramtemp")) {
		xb.overEdramTemp = myatou32(val, -1);
		if (xb.overEdramTemp == -1)
			goto bad;
		log_printf(1, "Using OVEREDRAMTEMP option, value %d\n", xb.overEdramTemp);
		return 1;
	}
	if (!stricmp(opt, "cpufan")) {
		xb.cpuFan = myatou32(val, -1);
		if (xb.cpuFan == -1)
			goto bad;
		log_printf(1, "Using CPUFAN option, value %d\n", xb.cpuFan);
		return 1;
	}
	if (!stricmp(opt, "gpufan")) {
		xb.gpuFan = myatou32(val, -1);
		if (xb.gpuFan == -1)
			goto bad;
		log_printf(1, "Using GPUFAN option, value %d\n", xb.gpuFan);
		return 1;
	}
	if (!stricmp(opt, "avregion")) {
		xb.avRegion = myatou32(val, -1);
		if (xb.avRegion == -1)
			goto bad;
		log_printf(1, "Using AVREGION option, value 0x%x\n", xb.avRegion);
		return 1;
	}
	if (!stricmp(opt, "gameregion")) {
		xb.gameRegion = myatou32(val, -1);
		if (xb.gameRegion == -1)
			goto bad;
		log_printf(1, "Using GAMEREGION option, value 0x%x\n", xb.gameRegion);
		return 1;
	}
	if (!stricmp(opt, "dvdregion")) {
		xb.dvdRegion = myatou32(val, -1);
		if (xb.dvdRegion == -1)
			goto bad;
		log_printf(1, "Using DVDREGION option, value 0x%x\n", xb.dvdRegion);
		return 1;
	}
	if (!stricmp(opt, "xellbutton")) {
		xb.xellButton = parseButton(val);
		if (!xb.xellButton)
			goto bad;
		log_printf(1, "Using XELLBUTTON option, value %s\n", val);
		return 1;
	}
	if (!stricmp(opt, "xellbutton2")) {
		xb.xellAltButton = parseButton(val);
		if (!xb.xellAltButton)
			goto bad;
		log_printf(1, "Using XELLBUTTON2 option, value %s\n", val);
		return 1;
	}
	if (!stricmp(opt, "dualboot")) {
		xb.dualButton = parseButton(val);
		if (!xb.dualButton)
			goto bad;
		log_printf(1, "Using DUALBOOT option, value %s\n", val);
		return 1;
	}
	if (!stricmp(opt, "cfldv")) {
		xb.cfLdv = myatou32(val, 0);
		if (xb.cfLdv > 32) {
			log_printf(0, "***** WARNING: cfldv value %d on command line is too large, setting to max value of 32\n", xb.cfLdv);
			xb.cfLdv = 32;
		} else if (!xb.cfLdv)
			goto bad;
		log_printf(1, "Using CFLDV option, value %d\n", xb.cfLdv);
		return 1;
	}
	if (!stricmp(opt, "macid")) {
		stripColons(val);
		if (strlen(val) != 12) {
			log_printf(1, "\n\n***** ERROR: invalid length macid %s provided on the command line!\n", opt);
			return 0;
		}
		if (!validateString(val)) {
			log_printf(1, "\n\n***** ERROR: invalid values in macid %s provided on the command line!\n", opt);
			return 0;
		}
		log_printf(1, "Using MACID option address: ");
		xb.macid[0] = myatox8(val);
		val += 2;
		log_printf(1, "%02x", xb.macid[0]);
		for (i = 1; i < 6; i++) {
			log_printf(1, ":");
			xb.macid[i] = myatox8(val);
			val += 2;
			log_printf(1, "%02x", xb.macid[i]);
		}
		goto done;
	}
	if (!stricmp(opt, "dvdkey")) {
		if (!kvSetDvdKey(val))
			goto bad;
		xb.bootFlags |= 0x2000000;
		return 1;
	}
	if (vlen) {
		log_printf(1, "\n\n***** ERROR: unknown option '%s' with value '%s' provided on the command line!\n", opt, val);
		return 0;
	}
incomplete:
	log_printf(1, "\n\n***** ERROR: unknown or incomplete option '%s' provided on the command line!\n", opt);
	return 0;
bad:
	log_printf(1, "\n\n***** ERROR: parsing option '%s', value '%s' is incorrect!\n", opt, val);
	return 0;
done:
	log_printf(1, "\n");
	return 1;
}

/* ;-separated options from the command line */
int parseCmdOptions(const char *opts)
{
	char opt[512];
	int i, j, len;

	len = strlen(opts);
	for (i = 0, j = 0; i <= len; i++) {
		if (opts[i] == ';' || opts[i] == 0) {
			opt[j] = 0;
			if (strlen(opt) > 4) {
				if (!parseOption(opt))
					return 0;
			}
			j = 0;
		} else
			opt[j++] = opts[i];
	}
	return 1;
}

void applyIniOptions(void)
{
	char *s;
	int i;

	if (!(xb.bootFlags & 0x20000000))
		optIniBool("nomobile", 0x20000000, 0, 0);
	if (!(xb.bootFlags & 0x40000000))
		optIniBool("noremap", 0x40000000, 0, 0);
	if (!(xb.bootFlags & 0x80000000))
		optIniBool("noecdremap", 0x80000000, 0, 0);
	if (!(xb.bootFlags & 0x10000000))
		optIniBool("nandmu", 0x10000000, 0, 0);
	if (!(xb.bootFlags & 0x4000000))
		optIniBool("nosecurity", 0x4000000, 0, 0);
	if (!(xb.bootFlags & 0x1000000))
		optIniBool("nosusecurity", 0x1000000, 0, 0);
	if (!(xb.bootFlags & 0x200000))
		optIniBool("smcnocheck", 0x200000, 0, 0);
	if (!xb.cfLdv) {
		xb.cfLdv = optIniInt("cfldv", 0);
		if (xb.cfLdv > 32) {
			log_printf(0, "***** WARNING: cfldv value %d in options.ini is too large, setting to max value of 32\n", xb.cfLdv);
			xb.cfLdv = 32;
		}
	}
	if (xb.cpuFan == -1)
		xb.cpuFan = optIniInt("cpufan", -1);
	if (xb.gpuFan == -1)
		xb.gpuFan = optIniInt("gpufan", -1);
	if (xb.cpuTemp == -1)
		xb.cpuTemp = optIniInt("cputemp", -1);
	if (xb.gpuTemp == -1)
		xb.gpuTemp = optIniInt("gputemp", -1);
	if (xb.edramTemp == -1)
		xb.edramTemp = optIniInt("edramtemp", -1);
	if (xb.overCpuTemp == -1)
		xb.overCpuTemp = optIniInt("overcputemp", -1);
	if (xb.overGpuTemp == -1)
		xb.overGpuTemp = optIniInt("overgputemp", -1);
	if (xb.overEdramTemp == -1)
		xb.overEdramTemp = optIniInt("overedramtemp", -1);
	if (xb.avRegion == -1)
		xb.avRegion = optIniInt("avregion", -1);
	if (xb.gameRegion == -1)
		xb.gameRegion = optIniInt("gameregion", -1);
	if (xb.dvdRegion == -1)
		xb.dvdRegion = optIniInt("dvdregion", -1);
	if (!macidSet()) {
		s = getIniValue("macid");
		if (s) {
			stripColons(s);
			if (strlen(s) != 12) {
				log_printf(0, "***** WARNING: invalid length macid '");
				showHexPairs(0, s);
				log_printf(0, "' provided in ini file! Discarding!\n", s);
			} else if (!validateString(s)) {
				log_printf(0, "***** WARNING: invalid characters in macid '");
				showHexPairs(0, s);
				log_printf(0, "' provided in ini file! Discarding!\n", s);
			} else {
				for (i = 0; i < 6; i++) {
					xb.macid[i] = myatox8(s);
					s += 2;
				}
			}
		}
	}
	if (xb.type - 2 <= 3) {
		if (!(xb.bootFlags & 1))
			optIniBool("cygnos", 1, 0, 0);
		if (!(xb.bootFlags & 8))
			optIniBool("demon", 8, 0, 0);
		if (!(xb.bootFlags & 0x8000000))
			optIniBool("patchsmc", 0x8000000, 0, 0);
		if (!xb.xellButton && (xb.bootFlags & 4)) {
			xb.xellButton = parseButton(getIniValue("xellbutton"));
			if (!xb.xellButton) {
				log_printf(1, "default console DVD eject button is being used to start xell\n");
				xb.xellButton = 0x12;
			}
		}
		if (!xb.xellAltButton && (xb.bootFlags & 4)) {
			xb.xellAltButton = parseButton(getIniValue("xellbutton2"));
			if (!xb.xellButton)
				log_printf(1, "alternate xell button is disabled\n");
		}
		if (!(xb.bootFlags & 0x400000))
			optIniBool("smcnoeject", 0x400000, 0, 0);
		if (!(xb.bootFlags & 0x800000))
			optIniBool("smcnoblink", 0x800000, 0, 0);
		switch (xb.type) {
		case 2:
			if (!(xb.bootFlags & 2))
				optIniBool("nodvd", 2, 4, 0);
			optIniBool("olddvd", 0, 4, 0);
			if (!xb.dualButton) {
				xb.dualButton = parseButton(getIniValue("dualboot"));
				if (xb.xellButton == xb.dualButton) {
					log_printf(1, "dualboot setting ignored!\n");
					xb.dualButton = 0;
				}
			}
			break;
		}
	}
	if (!(xb.bootFlags & 0x2000000)) {
		s = getIniValue("dvdkey");
		if (s && kvSetDvdKey(s))
			xb.bootFlags |= 0x2000000;
	}
	if (!xb.blSuffix[0]) {
		s = getIniValue("rev");
		if (s)
			sprintf(xb.blSuffix, "_%s", s);
	}
}

/* one file,offset raw patch from the command line */
int parseRawPatch(char *pat)
{
	char *val = NULL;
	int i, len, n;

	len = strlen(pat);
	for (i = 0; i < len; i++) {
		if (pat[i] == ',') {
			val = &pat[i + 1];
			pat[i] = 0;
			if (!*val) {
				log_printf(1, "\n\n***** ERROR: option '%s' provided on command line with = but no value!\n", pat);
				return 0;
			}
			i = len + 1;
		}
	}
	if (len != strlen(pat)) {
		if (xb.numRawPatches <= 15) {
			strcpy(xb.rawPatches[xb.numRawPatches].name, pat);
			n = xb.numRawPatches;
			xb.rawPatches[n].offset = myatou32(val, -1);
			if (xb.rawPatches[xb.numRawPatches].offset != -1) {
				log_printf(1, "parsed [rawpatch] (%d) from command line file '%s' offset 0x%x\n", xb.numRawPatches + 1,
					   xb.rawPatches[xb.numRawPatches].name, xb.rawPatches[xb.numRawPatches].offset);
				xb.numRawPatches++;
				return 1;
			}
			log_printf(0, "***** ERROR: [rawpatch] command option '%s' does not appear to have sane offset info!\n", pat);
			return 0;
		}
		log_printf(0, "***** ERROR: %d of %d [rawpatch] slots are already full!\n", xb.numRawPatches, 16, pat);
		return 0;
	}
	log_printf(0, "***** ERROR: parsing optional patch string '%s' failed!\n", pat);
	return 0;
}

/* ;-separated raw patches from the command line */
int parseRawPatches(const char *pats)
{
	char pat[512];
	int i, j, len;

	len = strlen(pats);
	for (i = 0, j = 0; i <= len; i++) {
		if (pats[i] == ';' || pats[i] == 0) {
			pat[j] = 0;
			if (strlen(pat) > 4) {
				if (!parseRawPatch(pat))
					return 0;
			}
			j = 0;
		} else
			pat[j++] = pats[i];
	}
	return 1;
}

/* an optional patch from the ini, skipping ones the command line gave */
void addPatch(const char *name)
{
	char path[1024];
	int i;

	if (xb.numPatches <= 15) {
		sprintf(path, "%s.bin", name);
		for (i = 0; i < xb.numPatches; i++) {
			if (!stricmp(path, xb.patches[i])) {
				log_printf(1, "***** WARNING: %s was provided both on command line and in ini, filtered duplicate!\n", name);
				return;
			}
		}
		strcpy(xb.patches[xb.numPatches], path);
		xb.numPatches++;
	} else
		log_printf(0, "***** WARNING: exceeded total number of optional patches with ini  %s!\n", name);
}

/* the :-separated addon list from the ini */
int loadAddons(void)
{
	char name[512];
	char *s;
	int i, j, len;

	s = getIniValue("addon");
	if (s) {
		len = strlen(s);
		for (i = 0, j = 0; i <= len; i++) {
			if (s[i] == ':' || s[i] == 0) {
				name[j] = 0;
				if (strlen(name) > 4)
					addPatch(name);
				j = 0;
			} else
				name[j++] = s[i];
		}
	}
	return 1;
}

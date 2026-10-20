/* options: console types (xenon...corona), boot options from the command
   line, options.ini and perbox files, optional patches.  Mixed object: the
   functions here are spliced into options.s (re/splice.py), which still
   holds the rest and the data, so string literals are extern names for
   the .s's strings. */
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
u32 parseOption(char *opt);
/* parseCmdOptions matches only when it sees an int return */
int parseOptionInt(char *opt) __asm__("_parseOption");

extern struct xebuild xb;

/* strings in options.s */
extern const char str_xenon[];	/* "xenon" */
extern const char msg_ctype_xenon[];	/* "Using xenon ctype (perbox file)\n" */
extern const char str_zephyr[];	/* "zephyr" */
extern const char msg_ctype_zephyr[];	/* "Using zephyr ctype (perbox file)\n" */
extern const char str_falcon[];	/* "falcon" */
extern const char msg_ctype_falcon[];	/* "Using falcon ctype (perbox file)\n" */
extern const char str_jasper[];	/* "jasper" */
extern const char str_jasperbc[];	/* "jasperbc" */
extern const char msg_ctype_jasper[];	/* "Using jasper ctype (perbox file)\n" */
extern const char str_jaspersb[];	/* "jaspersb" */
extern const char msg_ctype_jaspersb[];	/* "Using jasper smallblock ctype (perbox..." */
extern const char str_jasperbb[];	/* "jasperbb" */
extern const char msg_ctype_jasperbb[];	/* "Using jasper big block ctype (perbox ..." */
extern const char str_jasper256[];	/* "jasper256" */
extern const char str_jasper512[];	/* "jasper512" */
extern const char str_trinity[];	/* "trinity" */
extern const char msg_ctype_trinity[];	/* "Using trinity ctype (perbox file)\n" */
extern const char str_trinitybb[];	/* "trinitybb" */
extern const char msg_ctype_trinitybb[];	/* "Using trinity big block ctype (perbox..." */
extern const char str_trinitybigffs[];	/* "trinitybigffs" */
extern const char msg_ctype_trinitybigffs[];	/* "Using trinity big block big file syst..." */
extern const char str_corona[];	/* "corona" */
extern const char msg_ctype_corona[];	/* "Using corona ctype (perbox file)\n" */
extern const char str_coronabb[];	/* "coronabb" */
extern const char msg_ctype_coronabb[];	/* "Using corona big block ctype (perbox ..." */
extern const char str_coronabigffs[];	/* "coronabigffs" */
extern const char msg_ctype_coronabigffs[];	/* "Using corona big block big file syste..." */
extern const char str_corona4g[];	/* "corona4g" */
extern const char msg_ctype_corona4g[];	/* "Using corona MMC ctype (perbox file)\n" */
extern const char str_winchester[];	/* "winchester" */
extern const char msg_ctype_winchester[];	/* "Using winchester ctype (perbox file)\n" */
extern const char str_winchester4g[];	/* "winchester4g" */
extern const char msg_ctype_winchester4g[];	/* "Using winchester MMC ctype (perbox fi..." */
extern const char str_winchesterbb[];	/* "winchesterbb" */
extern const char msg_ctype_winchesterbb[];	/* "Using winchester big block ctype (per..." */
extern const char str_winchesterbigffs[];	/* "winchesterbigffs" */
extern const char msg_ctype_winchesterbigffs[];	/* "Using winchester big block big file s..." */
extern const char str_jasperbigffs[];	/* "jasperbigffs" */
extern const char msg_iniInvalid[];	/* "***** WARNING: options.ini setting '%..." */
extern const char str_false[];	/* "false" */
extern const char str_true[];	/* "true" */
extern const char msg_optPerbox[];	/* "Using %s option (perbox file)\n" */
extern const char msg_optIni[];	/* "Using %s option (ini file)\n" */
extern const char str_power[];	/* "power" */
extern const char str_remopower[];	/* "remopower" */
extern const char str_remox[];	/* "remox" */
extern const char str_winbutton[];	/* "winbutton" */
extern const char str_wirelessx[];	/* "wirelessx" */
extern const char str_wiredx[];	/* "wiredx" */
extern const char str_wiredxb1[];	/* "wiredxb1" */
extern const char str_wiredxb2[];	/* "wiredxb2" */
extern const char str_wiredxb3[];	/* "wiredxb3" */
extern const char str_wiredxf1[];	/* "wiredxf1" */
extern const char str_wiredxf2[];	/* "wiredxf2" */
extern const char str_eject[];	/* "eject" */
extern const char str_kiosk[];	/* "kiosk" */
extern const char msg_opt_nodvd[];	/* "Using NODVD (tray status fully open c..." */
extern const char msg_opt_olddvd[];	/* "Using OLDDVD (tray status not closed ..." */
extern const char msg_opt_cygnos[];	/* "Using CYGNOS option" */
extern const char msg_opt_demon[];	/* "Using DEMON option" */
extern const char str_nomobile[];	/* "nomobile" */
extern const char msg_opt_nomobile[];	/* "Using NOMOBILE option" */
extern const char str_smcnocheck[];	/* "smcnocheck" */
extern const char msg_opt_smcnocheck[];	/* "Using SMCNOCHECK option" */
extern const char str_noremap[];	/* "noremap" */
extern const char msg_opt_noremap[];	/* "Using NOREMAP option" */
extern const char str_noecdremap[];	/* "noecdremap" */
extern const char msg_opt_noecdremap[];	/* "Using NOECDREMAP option" */
extern const char str_nandmu[];	/* "nandmu" */
extern const char msg_opt_nandmu[];	/* "Using NANDMU option" */
extern const char str_nosecurity[];	/* "nosecurity" */
extern const char msg_opt_nosecurity[];	/* "Using NOSECURITY option" */
extern const char str_nosusecurity[];	/* "nosusecurity" */
extern const char str_patchsmc[];	/* "patchsmc" */
extern const char msg_opt_patchsmc[];	/* "Using PATCHSMC option" */
extern const char str_smcnoeject[];	/* "smcnoeject" */
extern const char msg_opt_smcnoeject[];	/* "Using SMCNOEJECT option" */
extern const char str_smcnoblink[];	/* "smcnoblink" */
extern const char msg_opt_smcnoblink[];	/* "Using SMCNOBLINK option" */
extern const char str_nodvd[];	/* "nodvd" */
extern const char str_olddvd[];	/* "olddvd" */
extern const char str_cygnos[];	/* "cygnos" */
extern const char str_demon[];	/* "demon" */
extern const char msg_optNoValue[];	/* "\n\n***** ERROR: option '%s' provided..." */
extern const char msg_rawPatchParsed[];	/* "parsed [rawpatch] (%d) from command l..." */
extern const char msg_rawPatchBadOffset[];	/* "***** ERROR: [rawpatch] command optio..." */
extern const char msg_rawPatchSlotsFull[];	/* "***** ERROR: %d of %d [rawpatch] slot..." */
extern const char msg_patchParseFailed[];	/* "***** ERROR: parsing optional patch s..." */
extern const char str_binFmt[];	/* "%s.bin" */
extern const char msg_patchDuplicate[];	/* "***** WARNING: %s was provided both o..." */
extern const char str_addon[];	/* "addon" */
extern const char msg_patchTooMany[];	/* "***** WARNING: exceeded total number ..." */
extern const char str_nl[];	/* "\n" */
extern const char str_cputemp[];	/* "cputemp" */
extern const char msg_opt_cputemp[];	/* "Using CPUTEMP option, value %d\n" */
extern const char str_gputemp[];	/* "gputemp" */
extern const char msg_opt_gputemp[];	/* "Using GPUTEMP option, value %d\n" */
extern const char str_edramtemp[];	/* "edramtemp" */
extern const char msg_opt_edramtemp[];	/* "Using EDRAMTEMP option, value %d\n" */
extern const char str_overcputemp[];	/* "overcputemp" */
extern const char msg_opt_overcputemp[];	/* "Using OVERCPUTEMP option, value %d\n" */
extern const char str_overgputemp[];	/* "overgputemp" */
extern const char msg_opt_overgputemp[];	/* "Using OVERGPUTEMP option, value %d\n" */
extern const char str_overedramtemp[];	/* "overedramtemp" */
extern const char msg_opt_overedramtemp[];	/* "Using OVEREDRAMTEMP option, value %d\..." */
extern const char str_cpufan[];	/* "cpufan" */
extern const char msg_opt_cpufan[];	/* "Using CPUFAN option, value %d\n" */
extern const char str_gpufan[];	/* "gpufan" */
extern const char msg_opt_gpufan[];	/* "Using GPUFAN option, value %d\n" */
extern const char str_avregion[];	/* "avregion" */
extern const char msg_opt_avregion[];	/* "Using AVREGION option, value 0x%x\n" */
extern const char str_gameregion[];	/* "gameregion" */
extern const char msg_opt_gameregion[];	/* "Using GAMEREGION option, value 0x%x\n" */
extern const char str_dvdregion[];	/* "dvdregion" */
extern const char msg_opt_dvdregion[];	/* "Using DVDREGION option, value 0x%x\n" */
extern const char str_xellbutton[];	/* "xellbutton" */
extern const char msg_opt_xellbutton[];	/* "Using XELLBUTTON option, value %s\n" */
extern const char str_xellbutton2[];	/* "xellbutton2" */
extern const char msg_opt_xellbutton2[];	/* "Using XELLBUTTON2 option, value %s\n" */
extern const char str_dualboot[];	/* "dualboot" */
extern const char msg_opt_dualboot[];	/* "Using DUALBOOT option, value %s\n" */
extern const char str_cfldv[];	/* "cfldv" */
extern const char msg_cfldvTooLarge[];	/* "***** WARNING: cfldv value %d on comm..." */
extern const char msg_opt_cfldv[];	/* "Using CFLDV option, value %d\n" */
extern const char str_macid[];	/* "macid" */
extern const char msg_opt_macid[];	/* "Using MACID option address: " */
extern const char str_hex02[];	/* "%02x" */
extern const char str_colon[];	/* ":" */
extern const char msg_macidBadValues[];	/* "\n\n***** ERROR: invalid values in ma..." */
extern const char msg_macidBadLength[];	/* "\n\n***** ERROR: invalid length macid..." */
extern const char str_dvdkey[];	/* "dvdkey" */
extern const char msg_optUnknownValue[];	/* "\n\n***** ERROR: unknown option '%s' ..." */
extern const char msg_optIncomplete[];	/* "\n\n***** ERROR: unknown or incomplet..." */
extern const char msg_optBadValue[];	/* "\n\n***** ERROR: parsing option '%s',..." */

/* strcat(xb.outName, "name") as gcc expands it: the short names become
   immediate stores (so they stay literals), the longer ones copy from the
   .s's string, which needs its extern name */
#define OUTCAT(name) memcpy(xb.outName + strlen(xb.outName), str_##name, sizeof #name)

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
	if (perboxExists(str_xenon)) {
		log_printf(1, msg_ctype_xenon);
		xb.flags |= 1;
		strcat(xb.outName, "xenon");
	} else if (perboxExists(str_zephyr)) {
		log_printf(1, msg_ctype_zephyr);
		xb.flags |= 2;
		strcat(xb.outName, "zephyr");
	} else if (perboxExists(str_falcon)) {
		log_printf(1, msg_ctype_falcon);
		xb.flags |= 3;
		strcat(xb.outName, "falcon");
	} else if (perboxExists(str_jasper) | perboxExists(str_jasperbc)) {
		log_printf(1, msg_ctype_jasper);
		xb.flags |= 0x80000004;
		strcat(xb.outName, "jasper");
	} else if (perboxExists(str_jaspersb)) {
		log_printf(1, msg_ctype_jaspersb);
		xb.flags |= 4;
		strcat(xb.outName, "jasper");
	} else if (perboxExists(str_jasperbb)) {
		log_printf(1, msg_ctype_jasperbb);
		xb.flags |= 0x40000004;
		strcat(xb.outName, "jasperbb");
	} else if (perboxExists(str_jasper256)) {
		log_printf(1, msg_ctype_jasperbb);
		xb.flags |= 0x40000004;
		strcat(xb.outName, "jasper256");
	} else if (perboxExists(str_jasper512)) {
		log_printf(1, msg_ctype_jasperbb);
		xb.flags |= 0x40000004;
		strcat(xb.outName, "jasper512");
	} else if (perboxExists(str_trinity)) {
		log_printf(1, msg_ctype_trinity);
		xb.flags |= 0x80000005;
		strcat(xb.outName, "trinity");
	} else if (perboxExists(str_trinitybb)) {
		log_printf(1, msg_ctype_trinitybb);
		xb.flags |= 0x40000005;
		strcat(xb.outName, "trinitybb");
	} else if (perboxExists(str_trinitybigffs)) {
		log_printf(1, msg_ctype_trinitybigffs);
		xb.flags |= 0x60000005;
		strcat(xb.outName, "trinitybigffs");
	} else if (perboxExists(str_corona)) {
		log_printf(1, msg_ctype_corona);
		xb.flags |= 0x80000006;
		strcat(xb.outName, "corona");
	} else if (perboxExists(str_coronabb)) {
		log_printf(1, msg_ctype_coronabb);
		xb.flags |= 0x40000006;
		strcat(xb.outName, "coronabb");
	} else if (perboxExists(str_coronabigffs)) {
		log_printf(1, msg_ctype_coronabigffs);
		xb.flags |= 0x60000006;
		OUTCAT(coronabigffs);
	} else if (perboxExists(str_corona4g)) {
		log_printf(1, msg_ctype_corona4g);
		xb.flags |= 0x90000006;
		OUTCAT(corona4g);
	} else if (perboxExists(str_winchester)) {
		log_printf(1, msg_ctype_winchester);
		xb.flags |= 0x80000007;
		OUTCAT(winchester);
	} else if (perboxExists(str_winchester4g)) {
		log_printf(1, msg_ctype_winchester4g);
		xb.flags |= 0x90000007;
		OUTCAT(winchester4g);
	} else if (perboxExists(str_winchesterbb)) {
		log_printf(1, msg_ctype_winchesterbb);
		xb.flags |= 0x40000007;
		OUTCAT(winchesterbb);
	} else if (perboxExists(str_winchesterbigffs)) {
		log_printf(1, msg_ctype_winchesterbigffs);
		xb.flags |= 0x60000007;
		OUTCAT(winchesterbigffs);
	}
	return (xb.flags & 7) != 0;
}

int setConsoleType(const char *name)
{
	if (!name || !*name)
		return 0;
	if (!stricmp(name, str_xenon)) {
		xb.flags |= 1;
		strcat(xb.outName, "xenon");
		return 1;
	}
	if (!stricmp(name, str_zephyr)) {
		xb.flags |= 2;
		strcat(xb.outName, "zephyr");
		return 1;
	}
	if (!stricmp(name, str_falcon)) {
		xb.flags |= 3;
		strcat(xb.outName, "falcon");
		return 1;
	}
	if (!stricmp(name, str_jasper) || !stricmp(name, str_jasperbc)) {
		xb.flags |= 0x80000004;
		strcat(xb.outName, "jasper");
		return 1;
	}
	if (!stricmp(name, str_jaspersb)) {
		xb.flags |= 4;
		strcat(xb.outName, "jasper");
		return 1;
	}
	if (!stricmp(name, str_jasperbb)) {
		xb.flags |= 0x40000004;
		strcat(xb.outName, "jasperbb");
		return 1;
	}
	if (!stricmp(name, str_jasper256)) {
		xb.flags |= 0x40000004;
		strcat(xb.outName, "jasper256");
		return 1;
	}
	if (!stricmp(name, str_jasper512)) {
		xb.flags |= 0x40000004;
		strcat(xb.outName, "jasper512");
		return 1;
	}
	if (!stricmp(name, str_jasperbigffs)) {
		xb.flags |= 0x60000004;
		strcat(xb.outName, "jasperbigffs");
		return 1;
	}
	if (!stricmp(name, str_trinity)) {
		xb.flags |= 0x80000005;
		strcat(xb.outName, "trinity");
		return 1;
	}
	if (!stricmp(name, str_trinitybb)) {
		xb.flags |= 0x40000005;
		OUTCAT(trinitybb);
		return 1;
	}
	if (!stricmp(name, str_trinitybigffs)) {
		xb.flags |= 0x60000005;
		OUTCAT(trinitybigffs);
		return 1;
	}
	if (!stricmp(name, str_corona)) {
		xb.flags |= 0x80000006;
		OUTCAT(corona);
		return 1;
	}
	if (!stricmp(name, str_coronabb)) {
		xb.flags |= 0x40000006;
		OUTCAT(coronabb);
		return 1;
	}
	if (!stricmp(name, str_coronabigffs)) {
		xb.flags |= 0x60000006;
		OUTCAT(coronabigffs);
		return 1;
	}
	if (!stricmp(name, str_corona4g)) {
		xb.flags |= 0x90000006;
		OUTCAT(corona4g);
		return 1;
	}
	if (!stricmp(name, str_winchester)) {
		xb.flags |= 0x80000007;
		OUTCAT(winchester);
		return 1;
	}
	if (!stricmp(name, str_winchester4g)) {
		xb.flags |= 0x90000007;
		OUTCAT(winchester4g);
		return 1;
	}
	if (!stricmp(name, str_winchesterbb)) {
		xb.flags |= 0x40000007;
		OUTCAT(winchesterbb);
		return 1;
	}
	if (!stricmp(name, str_winchesterbigffs)) {
		xb.flags |= 0x60000007;
		OUTCAT(winchesterbigffs);
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
		log_printf(1, msg_optPerbox, name);
	} else {
		bad = iniBoolInvalid(name);
		if (!bad) {
			if (!getIniBool(name, def))
				return 0;
			log_printf(1, msg_optIni, name);
		} else {
			log_printf(0, msg_iniInvalid, name, bad);
			return 0;
		}
	}
	{
		/* the original ORs into eax (so `return 1` isn't hoisted) */
		u32 f = (xb.bootFlags & ~clear) | set;
		__asm__("" : "+a" (f));
		xb.bootFlags = f;
	}
	return 1;
}

int optIniInt(const char *name, int def)
{
	char *bad;

	bad = iniU32Invalid(name);
	if (bad) {
		log_printf(0, msg_iniInvalid, name, bad);
		return def;
	}
	return getIniU32(name, def);
}

int parseButton(const char *s)
{
	int b = 0;

	if (!s)
		return 0;
	if (!strnicmp(s, str_power, 5))
		b = 0x11;
	else if (!strnicmp(s, str_remopower, 9))
		b = 0x20;
	else if (!strnicmp(s, str_remox, 5))
		b = 0x22;
	else if (!strnicmp(s, str_winbutton, 9))
		b = 0x24;
	else if (!strnicmp(s, str_wirelessx, 9))
		b = 0x55;
	else if (!strnicmp(s, str_wiredx, 6)) {
		if (!strnicmp(s, str_wiredxb1, 8))
			b = 0x59;
		else if (!strnicmp(s, str_wiredxb2, 8))
			b = 0x58;
		else if (!strnicmp(s, str_wiredxb3, 8))
			b = 0x5a;
		else if (!strnicmp(s, str_wiredxf1, 8))
			b = 0x56;
		else if (!strnicmp(s, str_wiredxf2, 8))
			b = 0x57;
		else
			b = 0x5a;
	} else if (!strnicmp(s, str_eject, 5))
		b = 0x12;
	else if (!strnicmp(s, str_kiosk, 5))
		b = 0x41;
	return b;
}

/* applyIniOptions stays asm (splice.py drops this copy); gcc only splits
   parseButton (its .part.0) when the object calls it directly */
void applyIniOptions(void)
{
	xb.xellButton = parseButton(getIniValue(str_power));
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
int setBoolOption(const char *name, const char *val)
{
	u32 off = 0;

	if (val) {
		if (!stricmp(val, str_false))
			off = 1;
		else if (stricmp(val, str_true))
			return 0;
	}
	if (!stricmp(name, str_nodvd)) {
		if (off)
			xb.bootFlagsOff |= 2;
		else {
			xb.bootFlags &= ~4;
			xb.bootFlags |= 2;
			log_printf(1, msg_opt_nodvd);
		}
		return 1;
	}
	if (!stricmp(name, str_olddvd)) {
		if (off)
			xb.bootFlagsOff |= 6;
		else {
			xb.bootFlags &= ~4;
			log_printf(1, msg_opt_olddvd);
		}
		return 1;
	}
	if (!stricmp(name, str_cygnos)) {
		if (off)
			xb.bootFlagsOff |= 1;
		else {
			xb.bootFlags |= 1;
			log_printf(1, msg_opt_cygnos);
		}
		return 1;
	}
	if (!stricmp(name, str_demon)) {
		if (off)
			xb.bootFlagsOff |= 8;
		else {
			xb.bootFlags |= 8;
			log_printf(1, msg_opt_demon);
		}
		return 1;
	}
	if (!stricmp(name, str_nomobile)) {
		if (off)
			xb.bootFlagsOff |= 0x20000000;
		else {
			xb.bootFlags |= 0x20000000;
			log_printf(1, msg_opt_nomobile);
		}
		return 1;
	}
	if (!stricmp(name, str_smcnocheck)) {
		if (off)
			xb.bootFlagsOff |= 0x200000;
		else {
			xb.bootFlags |= 0x200000;
			log_printf(1, msg_opt_smcnocheck);
		}
		return 1;
	}
	if (!stricmp(name, str_noremap)) {
		if (off)
			xb.bootFlagsOff |= 0x40000000;
		else {
			xb.bootFlags |= 0x40000000;
			log_printf(1, msg_opt_noremap);
		}
		return 1;
	}
	if (!stricmp(name, str_noecdremap)) {
		if (off)
			xb.bootFlagsOff |= 0x80000000;
		else {
			xb.bootFlags |= 0x80000000;
			log_printf(1, msg_opt_noecdremap);
		}
		return 1;
	}
	if (!stricmp(name, str_nandmu)) {
		if (off)
			xb.bootFlagsOff |= 0x10000000;
		else {
			xb.bootFlags |= 0x10000000;
			log_printf(1, msg_opt_nandmu);
		}
		return 1;
	}
	if (!stricmp(name, str_nosecurity)) {
		if (off)
			xb.bootFlagsOff |= 0x4000000;
		else {
			xb.bootFlags |= 0x4000000;
			log_printf(1, msg_opt_nosecurity);
		}
		return 1;
	}
	if (!stricmp(name, str_nosusecurity)) {
		if (off)
			xb.bootFlagsOff |= 0x1000000;
		else {
			xb.bootFlags |= 0x1000000;
			log_printf(1, msg_opt_nosecurity);
		}
		return 1;
	}
	if (!stricmp(name, str_patchsmc)) {
		if (off)
			xb.bootFlagsOff |= 0x8000000;
		else {
			xb.bootFlags |= 0x8000000;
			log_printf(1, msg_opt_patchsmc);
		}
		return 1;
	}
	if (!stricmp(name, str_smcnoeject)) {
		if (off)
			xb.bootFlagsOff |= 0x400000;
		else {
			xb.bootFlags |= 0x400000;
			log_printf(1, msg_opt_smcnoeject);
		}
		return 1;
	}
	if (!stricmp(name, str_smcnoblink)) {
		if (off)
			xb.bootFlagsOff |= 0x800000;
		else {
			xb.bootFlags |= 0x800000;
			log_printf(1, msg_opt_smcnoblink);
		}
		return 1;
	}
	return 0;
}

/* one name[=value] from the command line option string.  The `if (val)`
   around the value options is in the Linux build (gcc 4.9 keeps the test);
   gcc 6 threads it away.  The hints only steer block order and alignment:
   - po_hint() on cputemp's and gpufan's bad edges is a guarded call at
     profile_estimate (PRED_CALL, cancelling log_printf's on the success
     edge); inlined later, its store to a dead local goes.  cputemp's success
     then owns an epilogue copy and only edramtemp's -1 test falls into bad;
     gpufan's moves the jump alignment from avregion's test to gameregion's.
   - the two __builtin_expect use build.sh's builtin-expect-probability=83:
     the done edges stay under gputemp's (so its match trace comes first)
     but above the macid loop exit, and the incomplete block reaches the
     epilogue-copy threshold.
   The return is u32 (int keeps it in esi); parseCmdOptions calls it
   through parseOptionInt. */
static void po_hint(int *p) { *p = 1; }

__attribute__((optimize("no-early-inlining")))
u32 parseOption(char *opt)
{
	int dead;
	char *val = NULL;
	int i, len, vlen;

	len = strlen(opt);
	for (i = 0; i < len; i++) {
		if (opt[i] == '=') {
			val = &opt[i + 1];
			opt[i] = 0;
			if (!*val) {
				log_printf(1, msg_optNoValue, opt);
				return 0;
			}
			i = len + 1;
		}
	}
	if (len == strlen(opt))
		vlen = 0;
	else
		vlen = strlen(val);
	if (__builtin_expect(setBoolOption(opt, val) == 1, 0))
		{ log_printf(1, str_nl); return 1; }
	if (val) {
		if (!stricmp(opt, str_cputemp)) {
			xb.cpuTemp = myatou32(val, -1);
			if (xb.cpuTemp == -1) {
				po_hint(&dead);
				goto bad;
			}
			log_printf(1, msg_opt_cputemp, xb.cpuTemp);
			return 1;
		}
		if (!stricmp(opt, str_gputemp)) {
			xb.gpuTemp = myatou32(val, -1);
			if (xb.gpuTemp == -1)
				goto bad;
			log_printf(1, msg_opt_gputemp, xb.gpuTemp);
			return 1;
		}
		if (!stricmp(opt, str_edramtemp)) {
			xb.edramTemp = myatou32(val, -1);
			if (xb.edramTemp == -1)
				goto bad;
			log_printf(1, msg_opt_edramtemp, xb.edramTemp);
			return 1;
		}
		if (!stricmp(opt, str_overcputemp)) {
			xb.overCpuTemp = myatou32(val, -1);
			if (xb.overCpuTemp == -1)
				goto bad;
			log_printf(1, msg_opt_overcputemp, xb.overCpuTemp);
			return 1;
		}
		if (!stricmp(opt, str_overgputemp)) {
			xb.overGpuTemp = myatou32(val, -1);
			if (xb.overGpuTemp == -1)
				goto bad;
			log_printf(1, msg_opt_overgputemp, xb.overGpuTemp);
			return 1;
		}
		if (!stricmp(opt, str_overedramtemp)) {
			xb.overEdramTemp = myatou32(val, -1);
			if (xb.overEdramTemp == -1)
				goto bad;
			log_printf(1, msg_opt_overedramtemp, xb.overEdramTemp);
			return 1;
		}
		if (!stricmp(opt, str_cpufan)) {
			xb.cpuFan = myatou32(val, -1);
			if (xb.cpuFan == -1)
				goto bad;
			log_printf(1, msg_opt_cpufan, xb.cpuFan);
			return 1;
		}
		if (!stricmp(opt, str_gpufan)) {
			xb.gpuFan = myatou32(val, -1);
			if (xb.gpuFan == -1) {
				po_hint(&dead);
				goto bad;
			}
			log_printf(1, msg_opt_gpufan, xb.gpuFan);
			return 1;
		}
		if (!stricmp(opt, str_avregion)) {
			xb.avRegion = myatou32(val, -1);
			if (xb.avRegion == -1)
				goto bad;
			log_printf(1, msg_opt_avregion, xb.avRegion);
			return 1;
		}
		if (!stricmp(opt, str_gameregion)) {
			xb.gameRegion = myatou32(val, -1);
			if (xb.gameRegion == -1)
				goto bad;
			log_printf(1, msg_opt_gameregion, xb.gameRegion);
			return 1;
		}
		if (!stricmp(opt, str_dvdregion)) {
			xb.dvdRegion = myatou32(val, -1);
			if (xb.dvdRegion == -1)
				goto bad;
			log_printf(1, msg_opt_dvdregion, xb.dvdRegion);
			return 1;
		}
		if (!stricmp(opt, str_xellbutton)) {
			xb.xellButton = parseButton(val);
			if (!xb.xellButton)
				goto bad;
			log_printf(1, msg_opt_xellbutton, val);
			return 1;
		}
		if (!stricmp(opt, str_xellbutton2)) {
			xb.xellAltButton = parseButton(val);
			if (!xb.xellAltButton)
				goto bad;
			log_printf(1, msg_opt_xellbutton2, val);
			return 1;
		}
		if (!stricmp(opt, str_dualboot)) {
			xb.dualButton = parseButton(val);
			if (!xb.dualButton)
				goto bad;
			log_printf(1, msg_opt_dualboot, val);
			return 1;
		}
		if (!stricmp(opt, str_cfldv)) {
			xb.cfLdv = myatou32(val, 0);
			if (xb.cfLdv > 32) {
				log_printf(0, msg_cfldvTooLarge, xb.cfLdv);
				xb.cfLdv = 32;
			} else if (!xb.cfLdv)
				goto bad;
			log_printf(1, msg_opt_cfldv, xb.cfLdv);
			return 1;
		}
		if (!stricmp(opt, str_macid)) {
			stripColons(val);
			if (strlen(val) != 12) {
				log_printf(1, msg_macidBadLength, opt);
				return 0;
			}
			if (!validateString(val)) {
				log_printf(1, msg_macidBadValues, opt);
				return 0;
			}
			log_printf(1, msg_opt_macid);
			xb.macid[0] = myatox8(val);
			val += 2;
			log_printf(1, str_hex02, xb.macid[0]);
			for (i = 0; i < 5; i++) {
				log_printf(1, str_colon);
				xb.macid[i + 1] = myatox8(val + i * 2);
				log_printf(1, str_hex02, xb.macid[i + 1]);
			}
			{ log_printf(1, str_nl); return 1; }
		}
		if (!stricmp(opt, str_dvdkey)) {
			if (!kvSetDvdKey(val))
				goto bad;
			xb.bootFlags |= 0x2000000;
			return 1;
		}
	}
	if (__builtin_expect(vlen, 0)) {
		log_printf(1, msg_optUnknownValue, opt, val);
		return 0;
	}
	log_printf(1, msg_optIncomplete, opt);
	return 0;
bad:
	log_printf(1, msg_optBadValue, opt, val);
	return 0;
}

/* the ;-separated command line options */
int parseCmdOptions(const char *opts)
{
	char opt[512];
	int i, j, len;

	len = strlen(opts);
	for (i = 0, j = 0; i <= len; i++) {
		if (opts[i] == ';' || opts[i] == 0) {
			opt[j] = 0;
			if (strlen(opt) > 4) {
				if (!parseOptionInt(opt))
					return 0;
			}
			j = 0;
		} else
			opt[j++] = opts[i];
	}
	return 1;
}

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
				log_printf(1, msg_optNoValue, pat);
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
				log_printf(1, msg_rawPatchParsed, xb.numRawPatches + 1,
					   xb.rawPatches[xb.numRawPatches].name, xb.rawPatches[xb.numRawPatches].offset);
				xb.numRawPatches++;
				return 1;
			}
			log_printf(0, msg_rawPatchBadOffset, pat);
			return 0;
		}
		log_printf(0, msg_rawPatchSlotsFull, xb.numRawPatches, 16, pat);
		return 0;
	}
	log_printf(0, msg_patchParseFailed, pat);
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
	int i;

	if (xb.numPatches <= 15) {
		char path[1024];

		sprintf(path, str_binFmt, name);
		for (i = 0; i < xb.numPatches; i++) {
			if (!stricmp(path, xb.patches[i])) {
				log_printf(1, msg_patchDuplicate, name);
				return;
			}
		}
		strcpy(xb.patches[xb.numPatches], path);
		xb.numPatches++;
	} else
		log_printf(0, msg_patchTooMany, name);
}

/* the :-separated addon list from the ini */
int loadAddons(void)
{
	char name[512];
	char *s;
	int i, j, len;

	s = getIniValue(str_addon);
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

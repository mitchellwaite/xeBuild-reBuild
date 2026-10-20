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
extern const char msg_patchTooMany[];	/* "***** WARNING: exceeded total number ..." */

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

/* parseOption stays asm (splice.py drops this copy); gcc only splits
   parseButton (its .part.0) when the object calls it directly */
u32 parseOption(char *opt)
{
	return parseButton(opt);
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
	char path[1024];
	int i;

	if (xb.numPatches <= 15) {
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

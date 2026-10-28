/* options: console types (xenon...corona), boot options from the command
   line, options.ini and perbox files, optional patches.  The strings are
   static arrays in the original's .rdata order (literals in the original:
   several functions are matched with hints that expand their blocks in
   another order).  applyIniOptions is built with a crafted profile
   (build.sh, src/app/options.prof); everything else keeps gcc's guessed
   one. */
#include <stdio.h>
#include <string.h>

#define XB_PATCHES		/* xb.patches (xebuild.h) */
#include "xebuild.h"

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

/* the strings, in the original's .rdata order: gcc emits static variables
   in reverse definition order, so they are defined last to first.  Arrays
   start 4-aligned where the original pads before them */
static const char str_addon[] __attribute__((aligned(1))) = "addon";
static const char msg_patchTooMany[] __attribute__((aligned(4))) = "***** WARNING: exceeded total number of optional patches with ini  %s!\n";
static const char msg_patchDuplicate[] __attribute__((aligned(1))) = "***** WARNING: %s was provided both on command line and in ini, filtered duplicate!\n";
static const char str_binFmt[] __attribute__((aligned(1))) = "%s.bin";
static const char msg_patchParseFailed[] __attribute__((aligned(4))) = "***** ERROR: parsing optional patch string '%s' failed!\n";
static const char msg_rawPatchSlotsFull[] __attribute__((aligned(4))) = "***** ERROR: %d of %d [rawpatch] slots are already full!\n";
static const char msg_rawPatchBadOffset[] __attribute__((aligned(1))) = "***** ERROR: [rawpatch] command option '%s' does not appear to have sane offset info!\n";
static const char msg_rawPatchParsed[] __attribute__((aligned(4))) = "parsed [rawpatch] (%d) from command line file '%s' offset 0x%x\n";
static const char str_revSuffix[] __attribute__((aligned(1))) = "_%s";
static const char str_rev[] __attribute__((aligned(1))) = "rev";
static const char msg_dualbootIgnored[] __attribute__((aligned(1))) = "dualboot setting ignored!\n";
static const char msg_xellAltDisabled[] __attribute__((aligned(4))) = "alternate xell button is disabled\n";
static const char msg_xellDefault[] __attribute__((aligned(4))) = "default console DVD eject button is being used to start xell\n";
static const char msg_iniMacidBadLength[] __attribute__((aligned(4))) = "***** WARNING: invalid length macid '";
static const char msg_iniMacidDiscard[] __attribute__((aligned(4))) = "' provided in ini file! Discarding!\n";
static const char msg_iniMacidBadChars[] __attribute__((aligned(4))) = "***** WARNING: invalid characters in macid '";
static const char msg_iniCfldvTooLarge[] __attribute__((aligned(4))) = "***** WARNING: cfldv value %d in options.ini is too large, setting to max value of 32\n";
static const char msg_optBadValue[] __attribute__((aligned(1))) = "\n\n***** ERROR: parsing option '%s', value '%s' is incorrect!\n";
static const char msg_optIncomplete[] __attribute__((aligned(4))) = "\n\n***** ERROR: unknown or incomplete option '%s' provided on the command line!\n";
static const char msg_optUnknownValue[] __attribute__((aligned(4))) = "\n\n***** ERROR: unknown option '%s' with value '%s' provided on the command line!\n";
static const char str_dvdkey[] __attribute__((aligned(1))) = "dvdkey";
static const char msg_macidBadLength[] __attribute__((aligned(4))) = "\n\n***** ERROR: invalid length macid %s provided on the command line!\n";
static const char msg_macidBadValues[] __attribute__((aligned(1))) = "\n\n***** ERROR: invalid values in macid %s provided on the command line!\n";
static const char str_colon[] __attribute__((aligned(1))) = ":";
static const char str_hex02[] __attribute__((aligned(1))) = "%02x";
static const char msg_opt_macid[] __attribute__((aligned(1))) = "Using MACID option address: ";
static const char str_macid[] __attribute__((aligned(1))) = "macid";
static const char msg_opt_cfldv[] __attribute__((aligned(1))) = "Using CFLDV option, value %d\n";
static const char msg_cfldvTooLarge[] __attribute__((aligned(4))) = "***** WARNING: cfldv value %d on command line is too large, setting to max value of 32\n";
static const char str_cfldv[] __attribute__((aligned(1))) = "cfldv";
static const char msg_opt_dualboot[] __attribute__((aligned(4))) = "Using DUALBOOT option, value %s\n";
static const char str_dualboot[] __attribute__((aligned(1))) = "dualboot";
static const char msg_opt_xellbutton2[] __attribute__((aligned(4))) = "Using XELLBUTTON2 option, value %s\n";
static const char str_xellbutton2[] __attribute__((aligned(1))) = "xellbutton2";
static const char msg_opt_xellbutton[] __attribute__((aligned(4))) = "Using XELLBUTTON option, value %s\n";
static const char str_xellbutton[] __attribute__((aligned(1))) = "xellbutton";
static const char msg_opt_dvdregion[] __attribute__((aligned(4))) = "Using DVDREGION option, value 0x%x\n";
static const char str_dvdregion[] __attribute__((aligned(1))) = "dvdregion";
static const char msg_opt_gameregion[] __attribute__((aligned(4))) = "Using GAMEREGION option, value 0x%x\n";
static const char str_gameregion[] __attribute__((aligned(1))) = "gameregion";
static const char msg_opt_avregion[] __attribute__((aligned(1))) = "Using AVREGION option, value 0x%x\n";
static const char str_avregion[] __attribute__((aligned(1))) = "avregion";
static const char msg_opt_gpufan[] __attribute__((aligned(4))) = "Using GPUFAN option, value %d\n";
static const char str_gpufan[] __attribute__((aligned(1))) = "gpufan";
static const char msg_opt_cpufan[] __attribute__((aligned(4))) = "Using CPUFAN option, value %d\n";
static const char str_cpufan[] __attribute__((aligned(1))) = "cpufan";
static const char msg_opt_overedramtemp[] __attribute__((aligned(4))) = "Using OVEREDRAMTEMP option, value %d\n";
static const char str_overedramtemp[] __attribute__((aligned(1))) = "overedramtemp";
static const char msg_opt_overgputemp[] __attribute__((aligned(1))) = "Using OVERGPUTEMP option, value %d\n";
static const char str_overgputemp[] __attribute__((aligned(1))) = "overgputemp";
static const char msg_opt_overcputemp[] __attribute__((aligned(4))) = "Using OVERCPUTEMP option, value %d\n";
static const char str_overcputemp[] __attribute__((aligned(1))) = "overcputemp";
static const char msg_opt_edramtemp[] __attribute__((aligned(4))) = "Using EDRAMTEMP option, value %d\n";
static const char str_edramtemp[] __attribute__((aligned(1))) = "edramtemp";
static const char msg_opt_gputemp[] __attribute__((aligned(1))) = "Using GPUTEMP option, value %d\n";
static const char str_gputemp[] __attribute__((aligned(1))) = "gputemp";
static const char msg_opt_cputemp[] __attribute__((aligned(1))) = "Using CPUTEMP option, value %d\n";
static const char str_cputemp[] __attribute__((aligned(1))) = "cputemp";
static const char str_nl[] __attribute__((aligned(1))) = "\n";
static const char msg_optNoValue[] __attribute__((aligned(4))) = "\n\n***** ERROR: option '%s' provided on command line with = but no value!\n";
static const char str_demon[] __attribute__((aligned(1))) = "demon";
static const char str_cygnos[] __attribute__((aligned(1))) = "cygnos";
static const char str_olddvd[] __attribute__((aligned(1))) = "olddvd";
static const char str_nodvd[] __attribute__((aligned(1))) = "nodvd";
static const char msg_opt_smcnoblink[] __attribute__((aligned(1))) = "Using SMCNOBLINK option";
static const char str_smcnoblink[] __attribute__((aligned(1))) = "smcnoblink";
static const char msg_opt_smcnoeject[] __attribute__((aligned(1))) = "Using SMCNOEJECT option";
static const char str_smcnoeject[] __attribute__((aligned(1))) = "smcnoeject";
static const char msg_opt_patchsmc[] __attribute__((aligned(1))) = "Using PATCHSMC option";
static const char str_patchsmc[] __attribute__((aligned(1))) = "patchsmc";
static const char str_nosusecurity[] __attribute__((aligned(1))) = "nosusecurity";
static const char msg_opt_nosecurity[] __attribute__((aligned(1))) = "Using NOSECURITY option";
static const char str_nosecurity[] __attribute__((aligned(1))) = "nosecurity";
static const char msg_opt_nandmu[] __attribute__((aligned(1))) = "Using NANDMU option";
static const char str_nandmu[] __attribute__((aligned(1))) = "nandmu";
static const char msg_opt_noecdremap[] __attribute__((aligned(1))) = "Using NOECDREMAP option";
static const char str_noecdremap[] __attribute__((aligned(1))) = "noecdremap";
static const char msg_opt_noremap[] __attribute__((aligned(1))) = "Using NOREMAP option";
static const char str_noremap[] __attribute__((aligned(1))) = "noremap";
static const char msg_opt_smcnocheck[] __attribute__((aligned(1))) = "Using SMCNOCHECK option";
static const char str_smcnocheck[] __attribute__((aligned(1))) = "smcnocheck";
static const char msg_opt_nomobile[] __attribute__((aligned(1))) = "Using NOMOBILE option";
static const char str_nomobile[] __attribute__((aligned(1))) = "nomobile";
static const char msg_opt_demon[] __attribute__((aligned(1))) = "Using DEMON option";
static const char msg_opt_cygnos[] __attribute__((aligned(1))) = "Using CYGNOS option";
static const char msg_opt_olddvd[] __attribute__((aligned(4))) = "Using OLDDVD (tray status not closed check) option";
static const char msg_opt_nodvd[] __attribute__((aligned(1))) = "Using NODVD (tray status fully open check) option";
static const char str_true[] __attribute__((aligned(1))) = "true";
static const char str_false[] __attribute__((aligned(1))) = "false";
static const char str_winbutton[] __attribute__((aligned(1))) = "winbutton";
static const char str_remox[] __attribute__((aligned(1))) = "remox";
static const char str_remopower[] __attribute__((aligned(1))) = "remopower";
static const char str_power[] __attribute__((aligned(1))) = "power";
static const char msg_iniInvalid[] __attribute__((aligned(4))) = "***** WARNING: options.ini setting '%s' invalid value '%s', discarding!\n";
static const char msg_optIni[] __attribute__((aligned(1))) = "Using %s option (ini file)\n";
static const char msg_optPerbox[] __attribute__((aligned(4))) = "Using %s option (perbox file)\n";
static const char str_jasperbigffs[] __attribute__((aligned(1))) = "jasperbigffs";
static const char msg_ctype_winchesterbigffs[] __attribute__((aligned(4))) = "Using winchester big block big file system ctype (perbox file)\n";
static const char str_winchesterbigffs_[] __attribute__((aligned(1))) = "winchesterbigffs";
extern const char str_winchesterbigffs[1] __attribute__((alias("str_winchesterbigffs_")));
static const char msg_ctype_winchesterbb[] __attribute__((aligned(4))) = "Using winchester big block ctype (perbox file)\n";
static const char str_winchesterbb_[] __attribute__((aligned(1))) = "winchesterbb";
extern const char str_winchesterbb[1] __attribute__((alias("str_winchesterbb_")));
static const char msg_ctype_winchester4g[] __attribute__((aligned(4))) = "Using winchester MMC ctype (perbox file)\n";
static const char str_winchester4g_[] __attribute__((aligned(1))) = "winchester4g";
extern const char str_winchester4g[1] __attribute__((alias("str_winchester4g_")));
static const char msg_ctype_winchester[] __attribute__((aligned(4))) = "Using winchester ctype (perbox file)\n";
static const char str_winchester_[] __attribute__((aligned(1))) = "winchester";
extern const char str_winchester[1] __attribute__((alias("str_winchester_")));
static const char msg_ctype_corona4g[] __attribute__((aligned(4))) = "Using corona MMC ctype (perbox file)\n";
static const char str_corona4g_[] __attribute__((aligned(1))) = "corona4g";
extern const char str_corona4g[1] __attribute__((alias("str_corona4g_")));
static const char msg_ctype_coronabigffs[] __attribute__((aligned(4))) = "Using corona big block big file system ctype (perbox file)\n";
static const char str_coronabigffs_[] __attribute__((aligned(1))) = "coronabigffs";
extern const char str_coronabigffs[1] __attribute__((alias("str_coronabigffs_")));
static const char msg_ctype_coronabb[] __attribute__((aligned(4))) = "Using corona big block ctype (perbox file)\n";
static const char str_coronabb_[] __attribute__((aligned(1))) = "coronabb";
extern const char str_coronabb[1] __attribute__((alias("str_coronabb_")));
static const char msg_ctype_corona[] __attribute__((aligned(1))) = "Using corona ctype (perbox file)\n";
static const char str_corona_[] __attribute__((aligned(1))) = "corona";
extern const char str_corona[1] __attribute__((alias("str_corona_")));
static const char msg_ctype_trinitybigffs[] __attribute__((aligned(4))) = "Using trinity big block big file system ctype (perbox file)\n";
static const char str_trinitybigffs_[] __attribute__((aligned(1))) = "trinitybigffs";
extern const char str_trinitybigffs[1] __attribute__((alias("str_trinitybigffs_")));
static const char msg_ctype_trinitybb[] __attribute__((aligned(4))) = "Using trinity big block ctype (perbox file)\n";
static const char str_trinitybb_[] __attribute__((aligned(1))) = "trinitybb";
extern const char str_trinitybb[1] __attribute__((alias("str_trinitybb_")));
static const char msg_ctype_trinity[] __attribute__((aligned(1))) = "Using trinity ctype (perbox file)\n";
static const char str_trinity[] __attribute__((aligned(1))) = "trinity";
static const char str_jasper512[] __attribute__((aligned(1))) = "jasper512";
static const char str_jasper256[] __attribute__((aligned(1))) = "jasper256";
static const char msg_ctype_jasperbb[] __attribute__((aligned(4))) = "Using jasper big block ctype (perbox file)\n";
static const char str_jasperbb[] __attribute__((aligned(1))) = "jasperbb";
static const char msg_ctype_jaspersb[] __attribute__((aligned(4))) = "Using jasper smallblock ctype (perbox file)\n";
static const char str_jaspersb[] __attribute__((aligned(1))) = "jaspersb";
static const char msg_ctype_jasper[] __attribute__((aligned(4))) = "Using jasper ctype (perbox file)\n";
static const char str_jasperbc[] __attribute__((aligned(1))) = "jasperbc";
static const char str_jasper[] __attribute__((aligned(1))) = "jasper";
static const char msg_ctype_falcon[] __attribute__((aligned(4))) = "Using falcon ctype (perbox file)\n";
static const char str_falcon[] __attribute__((aligned(1))) = "falcon";
static const char msg_ctype_zephyr[] __attribute__((aligned(1))) = "Using zephyr ctype (perbox file)\n";
static const char str_zephyr[] __attribute__((aligned(1))) = "zephyr";
static const char msg_ctype_xenon[] __attribute__((aligned(1))) = "Using xenon ctype (perbox file)\n";
static const char str_xenon[] __attribute__((aligned(1))) = "xenon";
static const char str_kiosk[] __attribute__((aligned(1))) = "kiosk";
static const char str_eject[] __attribute__((aligned(1))) = "eject";
static const char str_wiredxf2[] __attribute__((aligned(1))) = "wiredxf2";
static const char str_wiredxf1[] __attribute__((aligned(1))) = "wiredxf1";
static const char str_wiredxb3[] __attribute__((aligned(1))) = "wiredxb3";
static const char str_wiredxb2[] __attribute__((aligned(1))) = "wiredxb2";
static const char str_wiredxb1[] __attribute__((aligned(1))) = "wiredxb1";
static const char str_wiredx[] __attribute__((aligned(1))) = "wiredx";
static const char str_wirelessx[] __attribute__((aligned(4))) = "wirelessx";

/* strcat(xb.outName, "name") as gcc expands it: the short names become
   immediate stores (so they stay literals), the longer ones copy from the
   string in .rdata.  gcc would fold a visible array's contents into a
   second literal, so OUTCAT's strings are used through 1-element aliases
   (str_x for str_x_), which it can't read 9+ bytes from */
#define OUTCAT(name) memcpy(xb.outName + strlen(xb.outName), str_##name, sizeof #name)

/* the object is compiled with -fbranch-probabilities and a .gcda that has
   counts for applyIniOptions only; the rest keep the guessed profile (a
   function without counts would be compiled as never executed) */
#pragma GCC push_options
#pragma GCC optimize ("no-branch-probabilities", "no-reorder-functions")

/* parseButton after its first four names: gcc's ipa-split part in the
   original, called from applyIniOptions' copies of the first tests.  A
   profile build doesn't split (feedback fnsplit refuses every function),
   so it is written out; cold, and in the original's .text.startup.  Global
   and first: gcc emits split parts (baseFileExists') first, then the
   functions in source order, which puts its FDE second as in the
   original.  regparm(1) is the convention gcc gave the static part */
__attribute__((cold, section(".text.startup"), regparm(1)))
int parseButtonPart(const char *s) __asm__("_parseButton.part.0");
__attribute__((regparm(1))) int parseButtonPart(const char *s)
{
	int b = 0;

	if (!strnicmp(s, str_wirelessx, 9))
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
	/* the part is cold (call predicted never taken), the original's split
	   call was likely: 36 is hoisted above the je only then */
	else if (__builtin_expect(!strnicmp(s, str_winbutton, 9), 1))
		b = 0x24;
	else
		b = parseButtonPart(s);
	return b;
}

#pragma GCC pop_options

/* applyIniOptions' copies of the functions above: a function with other
   optimize options can't be inlined into it (always_inline is, early) */
static inline __attribute__((always_inline)) int optIniIntI(const char *name, int def)
{
	char *bad;

	bad = iniU32Invalid(name);
	if (bad) {
		log_printf(0, msg_iniInvalid, name, bad);
		return def;
	}
	return getIniU32(name, def);
}

/* never written: IPA marks them read-only after the profile is read, and
   the tests on them fold away in ccp2.  The counts the profile gave their
   dead edges stay on the blocks around them (gcc doesn't update counts
   when an edge goes), the stale frequencies the original's alignment
   padding needs (see wip/README.md, app/options.c) */
static int aio_never, aio_never2, aio_never3, aio_never4;

static inline __attribute__((always_inline)) int parseButtonI(const char *s, int skip)
{
	if (!s)
		return 0;
	if (!strnicmp(s, str_power, 5) && !skip)
		return 0x11;
	if (!strnicmp(s, str_remopower, 9))
		return 0x20;
	if (!strnicmp(s, str_remox, 5))
		return 0x22;
	if (!strnicmp(s, str_winbutton, 9))
		return 0x24;
	return parseButtonPart(s);
}

static inline __attribute__((always_inline)) int macidSetI(void)
{
	int i;

	for (i = 0; i < 6; i++)
		if (xb.macid[i] != 0xff)
			return 1;
	return 0;
}

static inline __attribute__((always_inline)) void stripColonsI(char *s)
{
	int i, j, len;

	len = strlen(s) + 1;
	for (i = 0, j = 0; i < len; i++)
		if (s[i] != ':')
			s[j++] = s[i];
}

/* optIniBool's body in the caller (the profile gives each copy its own
   edge counts) */
#define OPT(name, set, clear) do { \
		if (xb.bootFlags & (set)) \
			break; \
		if (xb.bootFlagsOff & (set)) \
			break; \
		if (perboxExists(name)) { \
			log_printf(1, msg_optPerbox, name); \
		} else { \
			s = iniBoolInvalid(name); \
			if (!s) { \
				if (!getIniBool(name, 0)) \
					break; \
				log_printf(1, msg_optIni, name); \
			} else { \
				log_printf(0, msg_iniInvalid, name, s); \
				break; \
			} \
		} \
		xb.bootFlags &= ~(clear); \
		xb.bootFlags |= (set); \
	} while (0)

#pragma GCC push_options
#pragma GCC optimize ("no-branch-probabilities", "no-reorder-functions")

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
   through parseOptionInt.  po_hint gets parseOption's options too, or it
   can't be inlined there (the pragma above gives both an optimize
   attribute). */
__attribute__((optimize("no-early-inlining")))
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

#pragma GCC pop_options

/* options from perbox files and options.ini that the command line didn't
   set.  The block layout comes from the profile: src/app/options.prof sets
   the edges (see wip/README.md for how its frequencies were chosen) */
void applyIniOptions(void)
{
	char *s;
	int i;

	OPT(str_nomobile, 0x20000000, 0);
	OPT(str_noremap, 0x40000000, 0);
	OPT(str_noecdremap, 0x80000000, 0);
	OPT(str_nandmu, 0x10000000, 0);
	OPT(str_nosecurity, 0x4000000, 0);
	OPT(str_nosusecurity, 0x1000000, 0);
	OPT(str_smcnocheck, 0x200000, 0);
	if (!xb.cfLdv) {
		xb.cfLdv = optIniIntI(str_cfldv, 0);
		if (xb.cfLdv > 32) {
			log_printf(0, msg_iniCfldvTooLarge, xb.cfLdv);
			xb.cfLdv = 32;
		}
	}
	if (xb.cpuFan == -1)
		xb.cpuFan = optIniIntI(str_cpufan, -1);
	if (xb.gpuFan == -1)
		xb.gpuFan = optIniIntI(str_gpufan, -1);
	if (xb.cpuTemp == -1)
		xb.cpuTemp = optIniIntI(str_cputemp, -1);
	if (xb.gpuTemp == -1)
		xb.gpuTemp = optIniIntI(str_gputemp, -1);
	if (xb.edramTemp == -1)
		xb.edramTemp = optIniIntI(str_edramtemp, -1);
	if (xb.overCpuTemp == -1)
		xb.overCpuTemp = optIniIntI(str_overcputemp, -1);
	if (xb.overGpuTemp == -1)
		xb.overGpuTemp = optIniIntI(str_overgputemp, -1);
	if (xb.overEdramTemp == -1)
		xb.overEdramTemp = optIniIntI(str_overedramtemp, -1);
	if (xb.avRegion == -1)
		xb.avRegion = optIniIntI(str_avregion, -1);
	if (xb.gameRegion == -1)
		xb.gameRegion = optIniIntI(str_gameregion, -1);
	if (xb.dvdRegion == -1)
		xb.dvdRegion = optIniIntI(str_dvdregion, -1);
	if (!macidSetI()) {
		s = getIniValue(str_macid);
		if (s) {
			stripColonsI(s);
			if (strlen(s) != 12) {
				log_printf(0, msg_iniMacidBadLength);
				showHexPairs(0, s);
				log_printf(0, msg_iniMacidDiscard, s);
			} else if (!validateString(s)) {
				log_printf(0, msg_iniMacidBadChars);
				showHexPairs(0, s);
				log_printf(0, msg_iniMacidDiscard, s);
			} else {
				/* keeps if-conversion from hoisting i = 0 above the test */
				__asm__("");
				for (i = 0; i < 6; i++) {
					xb.macid[i] = myatox8(s);
					s += 2;
				}
			}
		}
	}
	if (xb.type - 2 <= 3) {
		OPT(str_cygnos, 1, 0);
		OPT(str_demon, 8, 0);
		OPT(str_patchsmc, 0x8000000, 0);
		if (!xb.xellButton && (xb.bootFlags & 4)) {
			xb.xellButton = parseButtonI(getIniValue(str_xellbutton), 0);
			if (!xb.xellButton) {
				log_printf(1, msg_xellDefault);
				xb.xellButton = 0x12;
			}
		}
		if (!xb.xellAltButton && (xb.bootFlags & 4)) {
			/* a dead edge into the remopower test: its block keeps a
			   count above its edge's */
			xb.xellAltButton = parseButtonI(getIniValue(str_xellbutton2), aio_never);
			if (!xb.xellButton)
				log_printf(1, msg_xellAltDisabled);
		}
		OPT(str_smcnoeject, 0x400000, 0);
		OPT(str_smcnoblink, 0x800000, 0);
	}
	/* outside the block above: VRP threads its range test past this one
	   (a switch it can't), and smcnoblink's paths reload the type */
	if (xb.type == 2) {
		OPT(str_nodvd, 2, 4);
		/* OPT(str_olddvd, 0, 4) with dead edges: Q (olddvd_q) merges into
		   the iniBoolInvalid block and leaves it its count, olddvd_set
		   merges into the `and ~4` block */
		do {
			if (perboxExists(str_olddvd)) {
				log_printf(1, msg_optPerbox, str_olddvd);
			} else {
olddvd_q:
				if (aio_never)
					break;
				s = iniBoolInvalid(str_olddvd);
				if (!s) {
					if (!getIniBool(str_olddvd, 0))
						break;
					log_printf(1, msg_optIni, str_olddvd);
				} else {
					log_printf(0, msg_iniInvalid, str_olddvd, s);
					break;
				}
			}
olddvd_set:
			if (aio_never)
				break;
			xb.bootFlags &= ~4;
		} while (0);
		if (!xb.dualButton) {
			xb.dualButton = parseButtonI(getIniValue(str_dualboot), 0);
			if (xb.xellButton == xb.dualButton) {
				log_printf(1, msg_dualbootIgnored);
				xb.dualButton = 0;
			}
		}
	} else if (aio_never) {		/* dead flow for the blocks above */
		goto olddvd_set;
	} else if (aio_never2) {
		goto olddvd_q;
	} else if (aio_never4) {
		goto tail;
	}
	if (!(xb.bootFlags & 0x2000000)) {
		s = getIniValue(str_dvdkey);
		if (s && kvSetDvdKey(s))
			xb.bootFlags |= 0x2000000;
	}
blsuffix:
	if (!xb.blSuffix[0]) {
		s = getIniValue(str_rev);
		if (s)
			sprintf(xb.blSuffix, str_revSuffix, s);
	}
	/* a dead cycle through the blSuffix test (irreducible: the goto tail
	   above enters it too) leaves that block the count that sets
	   freq_max, and with it the alignment threshold */
tail:
	if (aio_never3)
		goto blsuffix;
}

#pragma GCC push_options
#pragma GCC optimize ("no-branch-probabilities", "no-reorder-functions")

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
		/* TODO(xebuild.h cast): a signed test here, u32 in filelist_ini */
		if ((int)xb.nRawPatches <= 15) {
			strcpy(xb.rawPatch[xb.nRawPatches].name, pat);
			n = xb.nRawPatches;
			xb.rawPatch[n].offset = myatou32(val, -1);
			if (xb.rawPatch[xb.nRawPatches].offset != -1) {
				log_printf(1, msg_rawPatchParsed, xb.nRawPatches + 1,
					   xb.rawPatch[xb.nRawPatches].name, xb.rawPatch[xb.nRawPatches].offset);
				xb.nRawPatches++;
				return 1;
			}
			log_printf(0, msg_rawPatchBadOffset, pat);
			return 0;
		}
		log_printf(0, msg_rawPatchSlotsFull, xb.nRawPatches, 16, pat);
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

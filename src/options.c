/* options: console types (xenon...corona), boot options from the command
   line, options.ini and perbox files, optional patches.  gcc emits the
   string literals in the order it expands their blocks, which gives the
   original's .rdata order.
   applyIniOptions' cold layout comes from the profiles of the helpers gcc
   inlines into it (optIniBool, optIniInt, parseButton), with no hint and
   no profile file; tools/wip/dehint/notes/options.md says how each shape
   was found (attempts 7 and 30). */
#include <stdio.h>
#include <string.h>

#include "xebuild.h"
#include "filelist_ini.h"
#include "fileutil.h"
#include "keyvault.h"
#include "log.h"
#include "options.h"

int baseFileExists(const char *name)
{
	char path[1024];

	if (!xb.baseDir[0])
	{
		return 0;
	}
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
	if (perboxExists("xenon"))
	{
		log_printf(1, "Using xenon ctype (perbox file)\n");
		xb.flags |= CONSOLE_XENON;
		strcat(xb.outName, "xenon");
	}
	else if (perboxExists("zephyr"))
	{
		log_printf(1, "Using zephyr ctype (perbox file)\n");
		xb.flags |= CONSOLE_ZEPHYR;
		strcat(xb.outName, "zephyr");
	}
	else if (perboxExists("falcon"))
	{
		log_printf(1, "Using falcon ctype (perbox file)\n");
		xb.flags |= CONSOLE_FALCON;
		strcat(xb.outName, "falcon");
	}
	else if (perboxExists("jasper") | perboxExists("jasperbc"))
	{
		log_printf(1, "Using jasper ctype (perbox file)\n");
		xb.flags |= NAND_BB_CONTROLLER | CONSOLE_JASPER;
		strcat(xb.outName, "jasper");
	}
	else if (perboxExists("jaspersb"))
	{
		log_printf(1, "Using jasper smallblock ctype (perbox file)\n");
		xb.flags |= CONSOLE_JASPER;
		strcat(xb.outName, "jasper");
	}
	else if (perboxExists("jasperbb"))
	{
		log_printf(1, "Using jasper big block ctype (perbox file)\n");
		xb.flags |= NAND_BIG_BLOCK | CONSOLE_JASPER;
		strcat(xb.outName, "jasperbb");
	}
	else if (perboxExists("jasper256"))
	{
		log_printf(1, "Using jasper big block ctype (perbox file)\n");
		xb.flags |= NAND_BIG_BLOCK | CONSOLE_JASPER;
		strcat(xb.outName, "jasper256");
	}
	else if (perboxExists("jasper512"))
	{
		log_printf(1, "Using jasper big block ctype (perbox file)\n");
		xb.flags |= NAND_BIG_BLOCK | CONSOLE_JASPER;
		strcat(xb.outName, "jasper512");
	}
	else if (perboxExists("trinity"))
	{
		log_printf(1, "Using trinity ctype (perbox file)\n");
		xb.flags |= NAND_BB_CONTROLLER | CONSOLE_TRINITY;
		strcat(xb.outName, "trinity");
	}
	else if (perboxExists("trinitybb"))
	{
		log_printf(1, "Using trinity big block ctype (perbox file)\n");
		xb.flags |= NAND_BIG_BLOCK | CONSOLE_TRINITY;
		strcat(xb.outName, "trinitybb");
	}
	else if (perboxExists("trinitybigffs"))
	{
		log_printf(1, "Using trinity big block big file system ctype (perbox file)\n");
		xb.flags |= NAND_BIG_BLOCK | NAND_BIG_FFS | CONSOLE_TRINITY;
		strcat(xb.outName, "trinitybigffs");
	}
	else if (perboxExists("corona"))
	{
		log_printf(1, "Using corona ctype (perbox file)\n");
		xb.flags |= NAND_BB_CONTROLLER | CONSOLE_CORONA;
		strcat(xb.outName, "corona");
	}
	else if (perboxExists("coronabb"))
	{
		log_printf(1, "Using corona big block ctype (perbox file)\n");
		xb.flags |= NAND_BIG_BLOCK | CONSOLE_CORONA;
		strcat(xb.outName, "coronabb");
	}
	else if (perboxExists("coronabigffs"))
	{
		log_printf(1, "Using corona big block big file system ctype (perbox file)\n");
		xb.flags |= NAND_BIG_BLOCK | NAND_BIG_FFS | CONSOLE_CORONA;
		strcat(xb.outName, "coronabigffs");
	}
	else if (perboxExists("corona4g"))
	{
		log_printf(1, "Using corona MMC ctype (perbox file)\n");
		xb.flags |= NAND_BB_CONTROLLER | NAND_MMC | CONSOLE_CORONA;
		strcat(xb.outName, "corona4g");
	}
	else if (perboxExists("winchester"))
	{
		log_printf(1, "Using winchester ctype (perbox file)\n");
		xb.flags |= NAND_BB_CONTROLLER | CONSOLE_WINCHESTER;
		strcat(xb.outName, "winchester");
	}
	else if (perboxExists("winchester4g"))
	{
		log_printf(1, "Using winchester MMC ctype (perbox file)\n");
		xb.flags |= NAND_BB_CONTROLLER | NAND_MMC | CONSOLE_WINCHESTER;
		strcat(xb.outName, "winchester4g");
	}
	else if (perboxExists("winchesterbb"))
	{
		log_printf(1, "Using winchester big block ctype (perbox file)\n");
		xb.flags |= NAND_BIG_BLOCK | CONSOLE_WINCHESTER;
		strcat(xb.outName, "winchesterbb");
	}
	else if (perboxExists("winchesterbigffs"))
	{
		log_printf(1, "Using winchester big block big file system ctype (perbox file)\n");
		xb.flags |= NAND_BIG_BLOCK | NAND_BIG_FFS | CONSOLE_WINCHESTER;
		strcat(xb.outName, "winchesterbigffs");
	}
	return (xb.flags & CONSOLE_MASK) != 0;
}

int setConsoleType(const char *name)
{
	if (!name || !*name)
	{
		return 0;
	}
	if (!stricmp(name, "xenon"))
	{
		xb.flags |= CONSOLE_XENON;
		strcat(xb.outName, "xenon");
		return 1;
	}
	if (!stricmp(name, "zephyr"))
	{
		xb.flags |= CONSOLE_ZEPHYR;
		strcat(xb.outName, "zephyr");
		return 1;
	}
	if (!stricmp(name, "falcon"))
	{
		xb.flags |= CONSOLE_FALCON;
		strcat(xb.outName, "falcon");
		return 1;
	}
	if (!stricmp(name, "jasper") || !stricmp(name, "jasperbc"))
	{
		xb.flags |= NAND_BB_CONTROLLER | CONSOLE_JASPER;
		strcat(xb.outName, "jasper");
		return 1;
	}
	if (!stricmp(name, "jaspersb"))
	{
		xb.flags |= CONSOLE_JASPER;
		strcat(xb.outName, "jasper");
		return 1;
	}
	if (!stricmp(name, "jasperbb"))
	{
		xb.flags |= NAND_BIG_BLOCK | CONSOLE_JASPER;
		strcat(xb.outName, "jasperbb");
		return 1;
	}
	if (!stricmp(name, "jasper256"))
	{
		xb.flags |= NAND_BIG_BLOCK | CONSOLE_JASPER;
		strcat(xb.outName, "jasper256");
		return 1;
	}
	if (!stricmp(name, "jasper512"))
	{
		xb.flags |= NAND_BIG_BLOCK | CONSOLE_JASPER;
		strcat(xb.outName, "jasper512");
		return 1;
	}
	if (!stricmp(name, "jasperbigffs"))
	{
		xb.flags |= NAND_BIG_BLOCK | NAND_BIG_FFS | CONSOLE_JASPER;
		strcat(xb.outName, "jasperbigffs");
		return 1;
	}
	if (!stricmp(name, "trinity"))
	{
		xb.flags |= NAND_BB_CONTROLLER | CONSOLE_TRINITY;
		strcat(xb.outName, "trinity");
		return 1;
	}
	if (!stricmp(name, "trinitybb"))
	{
		xb.flags |= NAND_BIG_BLOCK | CONSOLE_TRINITY;
		strcat(xb.outName, "trinitybb");
		return 1;
	}
	if (!stricmp(name, "trinitybigffs"))
	{
		xb.flags |= NAND_BIG_BLOCK | NAND_BIG_FFS | CONSOLE_TRINITY;
		strcat(xb.outName, "trinitybigffs");
		return 1;
	}
	if (!stricmp(name, "corona"))
	{
		xb.flags |= NAND_BB_CONTROLLER | CONSOLE_CORONA;
		strcat(xb.outName, "corona");
		return 1;
	}
	if (!stricmp(name, "coronabb"))
	{
		xb.flags |= NAND_BIG_BLOCK | CONSOLE_CORONA;
		strcat(xb.outName, "coronabb");
		return 1;
	}
	if (!stricmp(name, "coronabigffs"))
	{
		xb.flags |= NAND_BIG_BLOCK | NAND_BIG_FFS | CONSOLE_CORONA;
		strcat(xb.outName, "coronabigffs");
		return 1;
	}
	if (!stricmp(name, "corona4g"))
	{
		xb.flags |= NAND_BB_CONTROLLER | NAND_MMC | CONSOLE_CORONA;
		strcat(xb.outName, "corona4g");
		return 1;
	}
	if (!stricmp(name, "winchester"))
	{
		xb.flags |= NAND_BB_CONTROLLER | CONSOLE_WINCHESTER;
		strcat(xb.outName, "winchester");
		return 1;
	}
	if (!stricmp(name, "winchester4g"))
	{
		xb.flags |= NAND_BB_CONTROLLER | NAND_MMC | CONSOLE_WINCHESTER;
		strcat(xb.outName, "winchester4g");
		return 1;
	}
	if (!stricmp(name, "winchesterbb"))
	{
		xb.flags |= NAND_BIG_BLOCK | CONSOLE_WINCHESTER;
		strcat(xb.outName, "winchesterbb");
		return 1;
	}
	if (!stricmp(name, "winchesterbigffs"))
	{
		xb.flags |= NAND_BIG_BLOCK | NAND_BIG_FFS | CONSOLE_WINCHESTER;
		strcat(xb.outName, "winchesterbigffs");
		return 1;
	}
	return 0;
}

/* a boolean option from a perbox file or options.ini, unless the command
   line already set it either way.  Every arm sets `on` and the one test
   after them applies it: no arm returns, so no test in the inlined copies
   has gcc's early-return prediction (the getIniBool call is 15% of its
   block), and the `on` joins are threaded away after inlining.  The
   profile this leaves is what orders the options' cold blocks in
   applyIniOptions (tools/wip/dehint/notes/options.md, attempts 7 and 30) */
_Bool optIniBool(const char *name, uint32_t set, uint32_t clear, int def)
{
	char *bad;
	_Bool on;

	if ((xb.optFlags & set) || (xb.optFlagsOff & set))
	{
		on = 0;
	}
	else if (perboxExists(name))
	{
		log_printf(1, "Using %s option (perbox file)\n", name);
		on = 1;
	}
	else
	{
		bad = iniBoolInvalid(name);
		if (!bad)
		{
			on = getIniBool(name, def);
			if (on)
			{
				log_printf(1, "Using %s option (ini file)\n", name);
			}
		}
		else
		{
			log_printf(0, "***** WARNING: options.ini setting '%s' invalid value '%s', discarding!\n", name, bad);
			on = 0;
		}
	}
	if (on)
	{
		xb.optFlags &= ~clear;
		xb.optFlags |= set;
	}
	return on;
}

/* an int option from options.ini, def if it is absent or invalid.  The
   good value returns first and the warning is the function's tail: gcc
   predicts an early return unlikely, so in applyIniOptions' inlined copies
   the getIniU32 call is 10% of its block (25 of 249; with the warning arm
   returning first it is 22%, with no return in either arm 15%).  That
   count places the eleven -1 options' calls in applyIniOptions' cold
   layout: after the block for a missing xellbutton value (29) and before
   the JTAG options' invalid-value tests (19)
   (tools/wip/dehint/notes/options.md, attempt 30) */
int optIniInt(const char *name, int def)
{
	char *bad;

	bad = iniU32Invalid(name);
	if (!bad)
	{
		return getIniU32(name, def);
	}
	log_printf(0, "***** WARNING: options.ini setting '%s' invalid value '%s', discarding!\n", name, bad);
	return def;
}

/* the button code for a name, 0 if s is NULL or unknown.  gcc splits the
   names after winbutton off into parseButton.part (unlikely executed, in
   .text.unlikely) and inlines the head at the three sites in
   applyIniOptions; parseOption calls the function */
int parseButton(const char *s)
{
	int b = 0;

	if (!s)
	{
		return 0;
	}
	if (!strnicmp(s, "power", 5))
	{
		b = PWR_POWER;
	}
	else if (!strnicmp(s, "remopower", 9))
	{
		b = PWR_IR_POWER;
	}
	else if (!strnicmp(s, "remox", 5))
	{
		b = PWR_IR_GUIDE;
	}
	else if (!strnicmp(s, "winbutton", 9))
	{
		b = PWR_IR_WINDOWS;
	}
	else if (!strnicmp(s, "wirelessx", 9))
	{
		b = PWR_WIRELESS;
	}
	else if (!strnicmp(s, "wiredx", 6))
	{
		if (!strnicmp(s, "wiredxb1", 8))
		{
			b = PWR_WIRED_B1;
		}
		else if (!strnicmp(s, "wiredxb2", 8))
		{
			b = PWR_WIRED_B2;
		}
		else if (!strnicmp(s, "wiredxb3", 8))
		{
			b = PWR_WIRED_B3;
		}
		else if (!strnicmp(s, "wiredxf1", 8))
		{
			b = PWR_WIRED_F1;
		}
		else if (!strnicmp(s, "wiredxf2", 8))
		{
			b = PWR_WIRED_F2;
		}
		else
		{
			b = PWR_WIRED_B3;
		}
	}
	else if (!strnicmp(s, "eject", 5))
	{
		b = PWR_EJECT;
	}
	else if (!strnicmp(s, "kiosk", 5))
	{
		b = PWR_KIOSK;
	}
	return b;
}

#define OPT(name, set, clear) if (!(xb.optFlags & (set))) optIniBool(name, set, clear, 0)

void stripColons(char *s)
{
	int i, j, len;

	len = strlen(s) + 1;
	for (i = 0, j = 0; i < len; i++)
	{
		if (s[i] != ':')
		{
			s[j++] = s[i];
		}
	}
}

int macidSet(void)
{
	int i;

	for (i = 0; i < 6; i++)
	{
		if (xb.smcOpts.macid[i] != 0xff)
		{
			return 1;
		}
	}
	return 0;
}

/* a boolean option given as name, name=true or name=false */
int setBoolOption(const char *name, const char *val)
{
	uint32_t off = 0;

	if (val)
	{
		if (!stricmp(val, "false"))
		{
			off = 1;
		}
		else if (stricmp(val, "true"))
		{
			return 0;
		}
	}
	if (!stricmp(name, "nodvd"))
	{
		if (off)
		{
			xb.optFlagsOff |= OPT_NODVD;
		}
		else
		{
			xb.optFlags &= ~OPT_XELL_BUTTON;
			xb.optFlags |= OPT_NODVD;
			log_printf(1, "Using NODVD (tray status fully open check) option");
		}
		return 1;
	}
	if (!stricmp(name, "olddvd"))
	{
		if (off)
		{
			xb.optFlagsOff |= (OPT_NODVD | OPT_XELL_BUTTON);
		}
		else
		{
			xb.optFlags &= ~OPT_XELL_BUTTON;
			log_printf(1, "Using OLDDVD (tray status not closed check) option");
		}
		return 1;
	}
	if (!stricmp(name, "cygnos"))
	{
		if (off)
		{
			xb.optFlagsOff |= OPT_CYGNOS;
		}
		else
		{
			xb.optFlags |= OPT_CYGNOS;
			log_printf(1, "Using CYGNOS option");
		}
		return 1;
	}
	if (!stricmp(name, "demon"))
	{
		if (off)
		{
			xb.optFlagsOff |= OPT_DEMON;
		}
		else
		{
			xb.optFlags |= OPT_DEMON;
			log_printf(1, "Using DEMON option");
		}
		return 1;
	}
	if (!stricmp(name, "nomobile"))
	{
		if (off)
		{
			xb.optFlagsOff |= OPT_NOMOBILE;
		}
		else
		{
			xb.optFlags |= OPT_NOMOBILE;
			log_printf(1, "Using NOMOBILE option");
		}
		return 1;
	}
	if (!stricmp(name, "smcnocheck"))
	{
		if (off)
		{
			xb.optFlagsOff |= OPT_SMCNOCHECK;
		}
		else
		{
			xb.optFlags |= OPT_SMCNOCHECK;
			log_printf(1, "Using SMCNOCHECK option");
		}
		return 1;
	}
	if (!stricmp(name, "noremap"))
	{
		if (off)
		{
			xb.optFlagsOff |= OPT_NOREMAP;
		}
		else
		{
			xb.optFlags |= OPT_NOREMAP;
			log_printf(1, "Using NOREMAP option");
		}
		return 1;
	}
	if (!stricmp(name, "noecdremap"))
	{
		if (off)
		{
			xb.optFlagsOff |= OPT_NOECDREMAP;
		}
		else
		{
			xb.optFlags |= OPT_NOECDREMAP;
			log_printf(1, "Using NOECDREMAP option");
		}
		return 1;
	}
	if (!stricmp(name, "nandmu"))
	{
		if (off)
		{
			xb.optFlagsOff |= OPT_NANDMU;
		}
		else
		{
			xb.optFlags |= OPT_NANDMU;
			log_printf(1, "Using NANDMU option");
		}
		return 1;
	}
	if (!stricmp(name, "nosecurity"))
	{
		if (off)
		{
			xb.optFlagsOff |= OPT_NOSECURITY;
		}
		else
		{
			xb.optFlags |= OPT_NOSECURITY;
			log_printf(1, "Using NOSECURITY option");
		}
		return 1;
	}
	if (!stricmp(name, "nosusecurity"))
	{
		if (off)
		{
			xb.optFlagsOff |= OPT_NOSUSECURITY;
		}
		else
		{
			xb.optFlags |= OPT_NOSUSECURITY;
			log_printf(1, "Using NOSECURITY option");
		}
		return 1;
	}
	if (!stricmp(name, "patchsmc"))
	{
		if (off)
		{
			xb.optFlagsOff |= OPT_PATCHSMC;
		}
		else
		{
			xb.optFlags |= OPT_PATCHSMC;
			log_printf(1, "Using PATCHSMC option");
		}
		return 1;
	}
	if (!stricmp(name, "smcnoeject"))
	{
		if (off)
		{
			xb.optFlagsOff |= OPT_SMCNOEJECT;
		}
		else
		{
			xb.optFlags |= OPT_SMCNOEJECT;
			log_printf(1, "Using SMCNOEJECT option");
		}
		return 1;
	}
	if (!stricmp(name, "smcnoblink"))
	{
		if (off)
		{
			xb.optFlagsOff |= OPT_SMCNOBLINK;
		}
		else
		{
			xb.optFlags |= OPT_SMCNOBLINK;
			log_printf(1, "Using SMCNOBLINK option");
		}
		return 1;
	}
	return 0;
}

/* bytes 1 .. n of a macid from the hex pairs at val, logged as ":%02x"
   (parseOption's comment says why it is a helper) */
static void macidRest(uint8_t *mac, const char *val, int n)
{
	int i;

	for (i = 0; i < n; i++)
	{
		log_printf(1, ":");
		mac[i] = myatox8(val + i * 2);
		log_printf(1, "%02x", mac[i]);
	}
}

/* one name[=value] from the command line option string.  The `if (val)`
   around the value options is in the Linux build (gcc 4.9 keeps the test);
   gcc 6 threads it away.  The return is uint32_t, as is parseCmdOptions':
   with int, uncprop returns stricmp's "macid" result for macid's 0s (kept
   in esi), and parseCmdOptions' `return 0` reuses the call's 0 only when
   the types agree. */
uint32_t parseOption(char *opt)
{
	char *val = NULL;
	int i, len, vlen, ok;

	len = strlen(opt);
	for (i = 0; i < len; i++)
	{
		if (opt[i] == '=')
		{
			val = &opt[i + 1];
			opt[i] = 0;
			if (!*val)
			{
				log_printf(1, "\n\n***** ERROR: option '%s' provided on command line with = but no value!\n", opt);
				return 0;
			}
			i = len + 1;
		}
	}
	if (len == strlen(opt))
	{
		vlen = 0;
	}
	else
	{
		vlen = strlen(val);
	}
	ok = 0;
	if (setBoolOption(opt, val) == 1)
	{
		log_printf(1, "\n");
		ok = 1;
	}
	else if (val)
	{
		if (!stricmp(opt, "cputemp"))
		{
			xb.smcOpts.cpuTemp = myatou32(val, -1);
			ok = 0;
			if (xb.smcOpts.cpuTemp != -1)
			{
				log_printf(1, "Using CPUTEMP option, value %d\n", xb.smcOpts.cpuTemp);
				ok = 1;
			}
			if (!ok)
			{
				goto bad;
			}
			return 1;
		}
		if (!stricmp(opt, "gputemp"))
		{
			xb.smcOpts.gpuTemp = myatou32(val, -1);
			if (xb.smcOpts.gpuTemp == -1)
			{
				goto bad;
			}
			log_printf(1, "Using GPUTEMP option, value %d\n", xb.smcOpts.gpuTemp);
			return 1;
		}
		if (!stricmp(opt, "edramtemp"))
		{
			xb.smcOpts.edramTemp = myatou32(val, -1);
			if (xb.smcOpts.edramTemp == -1)
			{
				goto bad;
			}
			log_printf(1, "Using EDRAMTEMP option, value %d\n", xb.smcOpts.edramTemp);
			return 1;
		}
		if (!stricmp(opt, "overcputemp"))
		{
			xb.smcOpts.overCpuTemp = myatou32(val, -1);
			if (xb.smcOpts.overCpuTemp == -1)
			{
				goto bad;
			}
			log_printf(1, "Using OVERCPUTEMP option, value %d\n", xb.smcOpts.overCpuTemp);
			return 1;
		}
		if (!stricmp(opt, "overgputemp"))
		{
			xb.smcOpts.overGpuTemp = myatou32(val, -1);
			if (xb.smcOpts.overGpuTemp == -1)
			{
				goto bad;
			}
			log_printf(1, "Using OVERGPUTEMP option, value %d\n", xb.smcOpts.overGpuTemp);
			return 1;
		}
		if (!stricmp(opt, "overedramtemp"))
		{
			xb.smcOpts.overEdramTemp = myatou32(val, -1);
			if (xb.smcOpts.overEdramTemp == -1)
			{
				goto bad;
			}
			log_printf(1, "Using OVEREDRAMTEMP option, value %d\n", xb.smcOpts.overEdramTemp);
			return 1;
		}
		if (!stricmp(opt, "cpufan"))
		{
			xb.smcOpts.cpuFan = myatou32(val, -1);
			if (xb.smcOpts.cpuFan == -1)
			{
				goto bad;
			}
			log_printf(1, "Using CPUFAN option, value %d\n", xb.smcOpts.cpuFan);
			return 1;
		}
		if (!stricmp(opt, "gpufan"))
		{
			xb.smcOpts.gpuFan = myatou32(val, -1);
			ok = 0;
			if (xb.smcOpts.gpuFan != -1)
			{
				log_printf(1, "Using GPUFAN option, value %d\n", xb.smcOpts.gpuFan);
				ok = 1;
			}
			if (!ok)
			{
				goto bad;
			}
			return 1;
		}
		if (!stricmp(opt, "avregion"))
		{
			xb.smcOpts.avRegion = myatou32(val, -1);
			if (xb.smcOpts.avRegion == -1)
			{
				goto bad;
			}
			log_printf(1, "Using AVREGION option, value 0x%x\n", xb.smcOpts.avRegion);
			return 1;
		}
		if (!stricmp(opt, "gameregion"))
		{
			xb.smcOpts.gameRegion = myatou32(val, -1);
			if (xb.smcOpts.gameRegion == -1)
			{
				goto bad;
			}
			log_printf(1, "Using GAMEREGION option, value 0x%x\n", xb.smcOpts.gameRegion);
			return 1;
		}
		if (!stricmp(opt, "dvdregion"))
		{
			xb.smcOpts.dvdRegion = myatou32(val, -1);
			if (xb.smcOpts.dvdRegion == -1)
			{
				goto bad;
			}
			log_printf(1, "Using DVDREGION option, value 0x%x\n", xb.smcOpts.dvdRegion);
			return 1;
		}
		if (!stricmp(opt, "xellbutton"))
		{
			xb.xellButton = parseButton(val);
			if (!xb.xellButton)
			{
				goto bad;
			}
			log_printf(1, "Using XELLBUTTON option, value %s\n", val);
			return 1;
		}
		if (!stricmp(opt, "xellbutton2"))
		{
			xb.xellAltButton = parseButton(val);
			if (!xb.xellAltButton)
			{
				goto bad;
			}
			log_printf(1, "Using XELLBUTTON2 option, value %s\n", val);
			return 1;
		}
		if (!stricmp(opt, "dualboot"))
		{
			xb.dualButton = parseButton(val);
			if (!xb.dualButton)
			{
				goto bad;
			}
			log_printf(1, "Using DUALBOOT option, value %s\n", val);
			return 1;
		}
		if (!stricmp(opt, "cfldv"))
		{
			xb.cfLdv = myatou32(val, 0);
			if (xb.cfLdv > CF_LDV_MAX)
			{
				log_printf(0, "***** WARNING: cfldv value %d on command line is too large, setting to max value of 32\n", xb.cfLdv);
				xb.cfLdv = CF_LDV_MAX;
			}
			else if (!xb.cfLdv)
			{
				goto bad;
			}
			log_printf(1, "Using CFLDV option, value %d\n", xb.cfLdv);
			return 1;
		}
		if (!stricmp(opt, "macid"))
		{
			stripColons(val);
			if (strlen(val) == 12)
			{
				if (validateString(val))
				{
					log_printf(1, "Using MACID option address: ");
					xb.smcOpts.macid[0] = myatox8(val);
					val += 2;
					log_printf(1, "%02x", xb.smcOpts.macid[0]);
					macidRest(&xb.smcOpts.macid[1], val, 5);
					log_printf(1, "\n");
					return 1;
				}
				log_printf(1, "\n\n***** ERROR: invalid values in macid %s provided on the command line!\n", opt);
				return 0;
			}
			log_printf(1, "\n\n***** ERROR: invalid length macid %s provided on the command line!\n", opt);
			return 0;
		}
		if (!stricmp(opt, "dvdkey"))
		{
			if (!kvSetDvdKey(val))
			{
				goto bad;
			}
			xb.optFlags |= OPT_DVDKEY;
			return 1;
		}
	}
	if (ok)
	{
		return 1;
	}
	if (val && vlen)
	{
		log_printf(1, "\n\n***** ERROR: unknown option '%s' with value '%s' provided on the command line!\n", opt, val);
		return 0;
	}
	log_printf(1, "\n\n***** ERROR: unknown or incomplete option '%s' provided on the command line!\n", opt);
	return 0;
bad:
	log_printf(1, "\n\n***** ERROR: parsing option '%s', value '%s' is incorrect!\n", opt, val);
	return 0;
}

/* the ;-separated command line options. */
uint32_t parseCmdOptions(const char *opts)
{
	char opt[512];
	int i, j, len;

	len = strlen(opts);
	for (i = 0, j = 0; i <= len; i++)
	{
		if (opts[i] == ';' || opts[i] == 0)
		{
			opt[j] = 0;
			if (strlen(opt) > 4)
			{
				if (!parseOption(opt))
				{
					return 0;
				}
			}
			j = 0;
		}
		else
		{
			opt[j++] = opts[i];
		}
	}
	return 1;
}

/* options from perbox files and options.ini that the command line didn't
   set.  optIniBool, optIniInt and parseButton's head are inlined here with
   their own profiles, which give the cold block layout. */
void applyIniOptions(void)
{
	char *s;
	int i;

	OPT("nomobile", OPT_NOMOBILE, 0);
	OPT("noremap", OPT_NOREMAP, 0);
	OPT("noecdremap", OPT_NOECDREMAP, 0);
	OPT("nandmu", OPT_NANDMU, 0);
	OPT("nosecurity", OPT_NOSECURITY, 0);
	OPT("nosusecurity", OPT_NOSUSECURITY, 0);
	OPT("smcnocheck", OPT_SMCNOCHECK, 0);
	if (!xb.cfLdv)
	{
		xb.cfLdv = optIniInt("cfldv", 0);
		if (xb.cfLdv > CF_LDV_MAX)
		{
			log_printf(0, "***** WARNING: cfldv value %d in options.ini is too large, setting to max value of 32\n", xb.cfLdv);
			xb.cfLdv = CF_LDV_MAX;
		}
	}
	if (xb.smcOpts.cpuFan == -1)
	{
		xb.smcOpts.cpuFan = optIniInt("cpufan", -1);
	}
	if (xb.smcOpts.gpuFan == -1)
	{
		xb.smcOpts.gpuFan = optIniInt("gpufan", -1);
	}
	if (xb.smcOpts.cpuTemp == -1)
	{
		xb.smcOpts.cpuTemp = optIniInt("cputemp", -1);
	}
	if (xb.smcOpts.gpuTemp == -1)
	{
		xb.smcOpts.gpuTemp = optIniInt("gputemp", -1);
	}
	if (xb.smcOpts.edramTemp == -1)
	{
		xb.smcOpts.edramTemp = optIniInt("edramtemp", -1);
	}
	if (xb.smcOpts.overCpuTemp == -1)
	{
		xb.smcOpts.overCpuTemp = optIniInt("overcputemp", -1);
	}
	if (xb.smcOpts.overGpuTemp == -1)
	{
		xb.smcOpts.overGpuTemp = optIniInt("overgputemp", -1);
	}
	if (xb.smcOpts.overEdramTemp == -1)
	{
		xb.smcOpts.overEdramTemp = optIniInt("overedramtemp", -1);
	}
	if (xb.smcOpts.avRegion == -1)
	{
		xb.smcOpts.avRegion = optIniInt("avregion", -1);
	}
	if (xb.smcOpts.gameRegion == -1)
	{
		xb.smcOpts.gameRegion = optIniInt("gameregion", -1);
	}
	if (xb.smcOpts.dvdRegion == -1)
	{
		xb.smcOpts.dvdRegion = optIniInt("dvdregion", -1);
	}
	if (!macidSet())
	{
		s = getIniValue("macid");
		if (s)
		{
			stripColons(s);
			if (strlen(s) == 12)
			{
				if (validateString(s))
				{
					for (i = 0; i < 6; i++)
					{
						xb.smcOpts.macid[i] = myatox8(s);
						s += 2;
					}
				}
				else
				{
					log_printf(0, "***** WARNING: invalid characters in macid '");
					showHexPairs(0, s);
					log_printf(0, "' provided in ini file! Discarding!\n", s);
				}
			}
			else
			{
				log_printf(0, "***** WARNING: invalid length macid '");
				showHexPairs(0, s);
				log_printf(0, "' provided in ini file! Discarding!\n", s);
			}
		}
	}
	if (xb.type - BUILD_JTAG <= BUILD_DEVGL16 - BUILD_JTAG)
	{
		OPT("cygnos", OPT_CYGNOS, 0);
		OPT("demon", OPT_DEMON, 0);
		OPT("patchsmc", OPT_PATCHSMC, 0);
		if (!xb.xellButton && (xb.optFlags & OPT_XELL_BUTTON))
		{
			xb.xellButton = parseButton(getIniValue("xellbutton"));
			if (!xb.xellButton)
			{
				log_printf(1, "default console DVD eject button is being used to start xell\n");
				xb.xellButton = PWR_EJECT;
			}
		}
		if (!xb.xellAltButton && (xb.optFlags & OPT_XELL_BUTTON))
		{
			xb.xellAltButton = parseButton(getIniValue("xellbutton2"));
			if (!xb.xellButton)
			{
				log_printf(1, "alternate xell button is disabled\n");
			}
		}
		OPT("smcnoeject", OPT_SMCNOEJECT, 0);
		OPT("smcnoblink", OPT_SMCNOBLINK, 0);
	}
	/* outside the block above: VRP threads its range test past this one
	   (a switch it can't), and smcnoblink's paths reload the type */
	if (xb.type == BUILD_JTAG)
	{
		OPT("nodvd", OPT_NODVD, OPT_XELL_BUTTON);
		/* no bit of its own: it clears OPT_XELL_BUTTON */
		optIniBool("olddvd", 0, OPT_XELL_BUTTON, 0);
		if (!xb.dualButton)
		{
			xb.dualButton = parseButton(getIniValue("dualboot"));
			if (xb.xellButton == xb.dualButton)
			{
				log_printf(1, "dualboot setting ignored!\n");
				xb.dualButton = 0;
			}
		}
	}
	if (!(xb.optFlags & OPT_DVDKEY))
	{
		s = getIniValue("dvdkey");
		if (s && kvSetDvdKey(s))
		{
			xb.optFlags |= OPT_DVDKEY;
		}
	}
	if (!xb.blSuffix[0])
	{
		s = getIniValue("rev");
		if (s)
		{
			sprintf(xb.blSuffix, "_%s", s);
		}
	}
}

int parseRawPatch(char *pat)
{
	char *val = NULL;
	int i, len, n;

	len = strlen(pat);
	for (i = 0; i < len; i++)
	{
		if (pat[i] == ',')
		{
			val = &pat[i + 1];
			pat[i] = 0;
			if (!*val)
			{
				log_printf(1, "\n\n***** ERROR: option '%s' provided on command line with = but no value!\n", pat);
				return 0;
			}
			i = len + 1;
		}
	}
	if (len != strlen(pat))
	{
		n = xb.nRawPatches;
		if (n <= XB_RAWPATCHES - 1)
		{
			strcpy(xb.rawPatch[xb.nRawPatches].name, pat);
			n = xb.nRawPatches;
			xb.rawPatch[n].offset = myatou32(val, -1);
			if (xb.rawPatch[xb.nRawPatches].offset != -1)
			{
				log_printf(1, "parsed [rawpatch] (%d) from command line file '%s' offset 0x%x\n", xb.nRawPatches + 1,
					   xb.rawPatch[xb.nRawPatches].name, xb.rawPatch[xb.nRawPatches].offset);
				xb.nRawPatches++;
				return 1;
			}
			log_printf(0, "***** ERROR: [rawpatch] command option '%s' does not appear to have sane offset info!\n", pat);
			return 0;
		}
		log_printf(0, "***** ERROR: %d of %d [rawpatch] slots are already full!\n", xb.nRawPatches, XB_RAWPATCHES, pat);
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
	for (i = 0, j = 0; i <= len; i++)
	{
		if (pats[i] == ';' || pats[i] == 0)
		{
			pat[j] = 0;
			if (strlen(pat) > 4)
			{
				if (!parseRawPatch(pat))
				{
					return 0;
				}
			}
			j = 0;
		}
		else
		{
			pat[j++] = pats[i];
		}
	}
	return 1;
}

/* an optional patch from the ini, skipping ones the command line gave */
void addPatch(const char *name)
{
	int i;

	if (xb.numPatches <= XB_ADDON_PATCHES - 1)
	{
		char path[1024];

		sprintf(path, "%s.bin", name);
		for (i = 0; i < xb.numPatches; i++)
		{
			if (!stricmp(path, xb.addons[i].name))
			{
				log_printf(1, "***** WARNING: %s was provided both on command line and in ini, filtered duplicate!\n", name);
				return;
			}
		}
		strcpy(xb.addons[xb.numPatches].name, path);
		xb.numPatches++;
	}
	else
	{
		log_printf(0, "***** WARNING: exceeded total number of optional patches with ini  %s!\n", name);
	}
}

/* the :-separated addon list from the ini */
int loadAddons(void)
{
	char name[512];
	char *s;
	int i, j, len;

	s = getIniValue("addon");
	if (s)
	{
		len = strlen(s);
		for (i = 0, j = 0; i <= len; i++)
		{
			if (s[i] == ':' || s[i] == 0)
			{
				name[j] = 0;
				if (strlen(name) > 4)
				{
					addPatch(name);
				}
				j = 0;
			}
			else
			{
				name[j++] = s[i];
			}
		}
	}
	return 1;
}

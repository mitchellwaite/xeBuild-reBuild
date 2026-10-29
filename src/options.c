/* options: console types (xenon...corona), boot options from the command
   line, options.ini and perbox files, optional patches.  gcc emits the
   string literals in the order it expands their blocks, which gives the
   original's .rdata order (one asm hint in applyIniOptions).
   applyIniOptions is built with a crafted profile (build.sh,
   src/options.prof); everything else keeps gcc's guessed one. */
#include <stdio.h>
#include <string.h>

#define XB_PATCHES		/* xb.patches (xebuild.h) */
#include "xebuild.h"
#include "filelist_ini.h"
#include "fileutil.h"
#include "keyvault.h"
#include "log.h"
#include "options.h"

/* TODO(prototype cast): validateString read as uint32_t here */
uint32_t validateStringU32(const char *nString) __asm__("_validateString");

uint32_t parseOption(char *opt);
/* parseCmdOptions matches only when it sees an int return */
int parseOptionInt(char *opt) __asm__("_parseOption");

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

	if (!strnicmp(s, "wirelessx", 9))
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
		xb.flags |= CONSOLE_XENON;
		strcat(xb.outName, "xenon");
	} else if (perboxExists("zephyr")) {
		log_printf(1, "Using zephyr ctype (perbox file)\n");
		xb.flags |= CONSOLE_ZEPHYR;
		strcat(xb.outName, "zephyr");
	} else if (perboxExists("falcon")) {
		log_printf(1, "Using falcon ctype (perbox file)\n");
		xb.flags |= CONSOLE_FALCON;
		strcat(xb.outName, "falcon");
	} else if (perboxExists("jasper") | perboxExists("jasperbc")) {
		log_printf(1, "Using jasper ctype (perbox file)\n");
		xb.flags |= NAND_BB_CONTROLLER | CONSOLE_JASPER;
		strcat(xb.outName, "jasper");
	} else if (perboxExists("jaspersb")) {
		log_printf(1, "Using jasper smallblock ctype (perbox file)\n");
		xb.flags |= CONSOLE_JASPER;
		strcat(xb.outName, "jasper");
	} else if (perboxExists("jasperbb")) {
		log_printf(1, "Using jasper big block ctype (perbox file)\n");
		xb.flags |= NAND_BIG_BLOCK | CONSOLE_JASPER;
		strcat(xb.outName, "jasperbb");
	} else if (perboxExists("jasper256")) {
		log_printf(1, "Using jasper big block ctype (perbox file)\n");
		xb.flags |= NAND_BIG_BLOCK | CONSOLE_JASPER;
		strcat(xb.outName, "jasper256");
	} else if (perboxExists("jasper512")) {
		log_printf(1, "Using jasper big block ctype (perbox file)\n");
		xb.flags |= NAND_BIG_BLOCK | CONSOLE_JASPER;
		strcat(xb.outName, "jasper512");
	} else if (perboxExists("trinity")) {
		log_printf(1, "Using trinity ctype (perbox file)\n");
		xb.flags |= NAND_BB_CONTROLLER | CONSOLE_TRINITY;
		strcat(xb.outName, "trinity");
	} else if (perboxExists("trinitybb")) {
		log_printf(1, "Using trinity big block ctype (perbox file)\n");
		xb.flags |= NAND_BIG_BLOCK | CONSOLE_TRINITY;
		strcat(xb.outName, "trinitybb");
	} else if (perboxExists("trinitybigffs")) {
		log_printf(1, "Using trinity big block big file system ctype (perbox file)\n");
		xb.flags |= NAND_BIG_BLOCK | NAND_BIG_FFS | CONSOLE_TRINITY;
		strcat(xb.outName, "trinitybigffs");
	} else if (perboxExists("corona")) {
		log_printf(1, "Using corona ctype (perbox file)\n");
		xb.flags |= NAND_BB_CONTROLLER | CONSOLE_CORONA;
		strcat(xb.outName, "corona");
	} else if (perboxExists("coronabb")) {
		log_printf(1, "Using corona big block ctype (perbox file)\n");
		xb.flags |= NAND_BIG_BLOCK | CONSOLE_CORONA;
		strcat(xb.outName, "coronabb");
	} else if (perboxExists("coronabigffs")) {
		log_printf(1, "Using corona big block big file system ctype (perbox file)\n");
		xb.flags |= NAND_BIG_BLOCK | NAND_BIG_FFS | CONSOLE_CORONA;
		strcat(xb.outName, "coronabigffs");
	} else if (perboxExists("corona4g")) {
		log_printf(1, "Using corona MMC ctype (perbox file)\n");
		xb.flags |= NAND_BB_CONTROLLER | NAND_MMC | CONSOLE_CORONA;
		strcat(xb.outName, "corona4g");
	} else if (perboxExists("winchester")) {
		log_printf(1, "Using winchester ctype (perbox file)\n");
		xb.flags |= NAND_BB_CONTROLLER | CONSOLE_WINCHESTER;
		strcat(xb.outName, "winchester");
	} else if (perboxExists("winchester4g")) {
		log_printf(1, "Using winchester MMC ctype (perbox file)\n");
		xb.flags |= NAND_BB_CONTROLLER | NAND_MMC | CONSOLE_WINCHESTER;
		strcat(xb.outName, "winchester4g");
	} else if (perboxExists("winchesterbb")) {
		log_printf(1, "Using winchester big block ctype (perbox file)\n");
		xb.flags |= NAND_BIG_BLOCK | CONSOLE_WINCHESTER;
		strcat(xb.outName, "winchesterbb");
	} else if (perboxExists("winchesterbigffs")) {
		log_printf(1, "Using winchester big block big file system ctype (perbox file)\n");
		xb.flags |= NAND_BIG_BLOCK | NAND_BIG_FFS | CONSOLE_WINCHESTER;
		strcat(xb.outName, "winchesterbigffs");
	}
	return (xb.flags & CONSOLE_MASK) != 0;
}

int setConsoleType(const char *name)
{
	if (!name || !*name)
		return 0;
	if (!stricmp(name, "xenon")) {
		xb.flags |= CONSOLE_XENON;
		strcat(xb.outName, "xenon");
		return 1;
	}
	if (!stricmp(name, "zephyr")) {
		xb.flags |= CONSOLE_ZEPHYR;
		strcat(xb.outName, "zephyr");
		return 1;
	}
	if (!stricmp(name, "falcon")) {
		xb.flags |= CONSOLE_FALCON;
		strcat(xb.outName, "falcon");
		return 1;
	}
	if (!stricmp(name, "jasper") || !stricmp(name, "jasperbc")) {
		xb.flags |= NAND_BB_CONTROLLER | CONSOLE_JASPER;
		strcat(xb.outName, "jasper");
		return 1;
	}
	if (!stricmp(name, "jaspersb")) {
		xb.flags |= CONSOLE_JASPER;
		strcat(xb.outName, "jasper");
		return 1;
	}
	if (!stricmp(name, "jasperbb")) {
		xb.flags |= NAND_BIG_BLOCK | CONSOLE_JASPER;
		strcat(xb.outName, "jasperbb");
		return 1;
	}
	if (!stricmp(name, "jasper256")) {
		xb.flags |= NAND_BIG_BLOCK | CONSOLE_JASPER;
		strcat(xb.outName, "jasper256");
		return 1;
	}
	if (!stricmp(name, "jasper512")) {
		xb.flags |= NAND_BIG_BLOCK | CONSOLE_JASPER;
		strcat(xb.outName, "jasper512");
		return 1;
	}
	if (!stricmp(name, "jasperbigffs")) {
		xb.flags |= NAND_BIG_BLOCK | NAND_BIG_FFS | CONSOLE_JASPER;
		strcat(xb.outName, "jasperbigffs");
		return 1;
	}
	if (!stricmp(name, "trinity")) {
		xb.flags |= NAND_BB_CONTROLLER | CONSOLE_TRINITY;
		strcat(xb.outName, "trinity");
		return 1;
	}
	if (!stricmp(name, "trinitybb")) {
		xb.flags |= NAND_BIG_BLOCK | CONSOLE_TRINITY;
		strcat(xb.outName, "trinitybb");
		return 1;
	}
	if (!stricmp(name, "trinitybigffs")) {
		xb.flags |= NAND_BIG_BLOCK | NAND_BIG_FFS | CONSOLE_TRINITY;
		strcat(xb.outName, "trinitybigffs");
		return 1;
	}
	if (!stricmp(name, "corona")) {
		xb.flags |= NAND_BB_CONTROLLER | CONSOLE_CORONA;
		strcat(xb.outName, "corona");
		return 1;
	}
	if (!stricmp(name, "coronabb")) {
		xb.flags |= NAND_BIG_BLOCK | CONSOLE_CORONA;
		strcat(xb.outName, "coronabb");
		return 1;
	}
	if (!stricmp(name, "coronabigffs")) {
		xb.flags |= NAND_BIG_BLOCK | NAND_BIG_FFS | CONSOLE_CORONA;
		strcat(xb.outName, "coronabigffs");
		return 1;
	}
	if (!stricmp(name, "corona4g")) {
		xb.flags |= NAND_BB_CONTROLLER | NAND_MMC | CONSOLE_CORONA;
		strcat(xb.outName, "corona4g");
		return 1;
	}
	if (!stricmp(name, "winchester")) {
		xb.flags |= NAND_BB_CONTROLLER | CONSOLE_WINCHESTER;
		strcat(xb.outName, "winchester");
		return 1;
	}
	if (!stricmp(name, "winchester4g")) {
		xb.flags |= NAND_BB_CONTROLLER | NAND_MMC | CONSOLE_WINCHESTER;
		strcat(xb.outName, "winchester4g");
		return 1;
	}
	if (!stricmp(name, "winchesterbb")) {
		xb.flags |= NAND_BIG_BLOCK | CONSOLE_WINCHESTER;
		strcat(xb.outName, "winchesterbb");
		return 1;
	}
	if (!stricmp(name, "winchesterbigffs")) {
		xb.flags |= NAND_BIG_BLOCK | NAND_BIG_FFS | CONSOLE_WINCHESTER;
		strcat(xb.outName, "winchesterbigffs");
		return 1;
	}
	return 0;
}

/* a boolean option from a perbox file or options.ini, unless the command
   line already set it either way */
_Bool optIniBool(const char *name, uint32_t set, uint32_t clear, int def)
{
	char *bad;

	if ((xb.bootFlags & set) || (xb.bootFlagsOff & set))
		return 0;
	if (perboxExists(name)) {
		log_printf(1, "Using %s option (perbox file)\n", name);
	} else {
		bad = iniBoolInvalid(name);
		if (!bad) {
			if (!getIniBool(name, def))
				return 0;
			log_printf(1, "Using %s option (ini file)\n", name);
		} else {
			log_printf(0, "***** WARNING: options.ini setting '%s' invalid value '%s', discarding!\n", name, bad);
			return 0;
		}
	}
	{
		/* the original ORs into eax (so `return 1` isn't hoisted) */
		uint32_t f = (xb.bootFlags & ~clear) | set;
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
	/* the part is cold (call predicted never taken), the original's split
	   call was likely: 36 is hoisted above the je only then */
	else if (__builtin_expect(!strnicmp(s, "winbutton", 9), 1))
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
		log_printf(0, "***** WARNING: options.ini setting '%s' invalid value '%s', discarding!\n", name, bad);
		return def;
	}
	return getIniU32(name, def);
}

/* never written: IPA marks them read-only after the profile is read, and
   the tests on them fold away in ccp2.  The counts the profile gave their
   dead edges stay on the blocks around them (gcc doesn't update counts
   when an edge goes), the stale frequencies the original's alignment
   padding needs (see tools/wip/README.md, options.c) */
static int aio_never, aio_never2, aio_never3, aio_never4;

static inline __attribute__((always_inline)) int parseButtonI(const char *s, int skip)
{
	if (!s)
		return 0;
	if (!strnicmp(s, "power", 5) && !skip)
		return 0x11;
	if (!strnicmp(s, "remopower", 9))
		return 0x20;
	if (!strnicmp(s, "remox", 5))
		return 0x22;
	if (!strnicmp(s, "winbutton", 9))
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
			log_printf(1, "Using %s option (perbox file)\n", name); \
		} else { \
			s = iniBoolInvalid(name); \
			if (!s) { \
				if (!getIniBool(name, 0)) \
					break; \
				log_printf(1, "Using %s option (ini file)\n", name); \
			} else { \
				log_printf(0, "***** WARNING: options.ini setting '%s' invalid value '%s', discarding!\n", name, s); \
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
	uint32_t off = 0;

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
   The return is uint32_t (int keeps it in esi); parseCmdOptions calls it
   through parseOptionInt.  po_hint gets parseOption's options too, or it
   can't be inlined there (the pragma above gives both an optimize
   attribute). */
__attribute__((optimize("no-early-inlining")))
static void po_hint(int *p) { *p = 1; }

__attribute__((optimize("no-early-inlining")))
uint32_t parseOption(char *opt)
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
				log_printf(1, "\n\n***** ERROR: option '%s' provided on command line with = but no value!\n", opt);
				return 0;
			}
			i = len + 1;
		}
	}
	if (len == strlen(opt))
		vlen = 0;
	else
		vlen = strlen(val);
	if (__builtin_expect(setBoolOption(opt, val) == 1, 0)) {
		log_printf(1, "\n");
		return 1;
	}
	if (val) {
		if (!stricmp(opt, "cputemp")) {
			xb.cpuTemp = myatou32(val, -1);
			if (xb.cpuTemp == -1) {
				po_hint(&dead);
				goto bad;
			}
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
			if (xb.gpuFan == -1) {
				po_hint(&dead);
				goto bad;
			}
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
			if (strlen(val) == 12) {
				if (validateStringU32(val)) {
					log_printf(1, "Using MACID option address: ");
					xb.macid[0] = myatox8(val);
					val += 2;
					log_printf(1, "%02x", xb.macid[0]);
					for (i = 0; i < 5; i++) {
						log_printf(1, ":");
						xb.macid[i + 1] = myatox8(val + i * 2);
						log_printf(1, "%02x", xb.macid[i + 1]);
					}
					log_printf(1, "\n");
					return 1;
				}
				log_printf(1, "\n\n***** ERROR: invalid values in macid %s provided on the command line!\n", opt);
				return 0;
			}
			log_printf(1, "\n\n***** ERROR: invalid length macid %s provided on the command line!\n", opt);
			return 0;
		}
		if (!stricmp(opt, "dvdkey")) {
			if (!kvSetDvdKey(val))
				goto bad;
			xb.bootFlags |= 0x2000000;
			return 1;
		}
	}
	if (__builtin_expect(vlen, 0)) {
		log_printf(1, "\n\n***** ERROR: unknown option '%s' with value '%s' provided on the command line!\n", opt, val);
		return 0;
	}
	log_printf(1, "\n\n***** ERROR: unknown or incomplete option '%s' provided on the command line!\n", opt);
	return 0;
bad:
	log_printf(1, "\n\n***** ERROR: parsing option '%s', value '%s' is incorrect!\n", opt, val);
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
   set.  The block layout comes from the profile: src/options.prof sets
   the edges (see tools/wip/README.md for how its frequencies were chosen) */
void applyIniOptions(void)
{
	char *s;
	int i;

	OPT("nomobile", 0x20000000, 0);
	OPT("noremap", 0x40000000, 0);
	OPT("noecdremap", 0x80000000, 0);
	OPT("nandmu", 0x10000000, 0);
	OPT("nosecurity", 0x4000000, 0);
	OPT("nosusecurity", 0x1000000, 0);
	OPT("smcnocheck", 0x200000, 0);
	if (!xb.cfLdv) {
		xb.cfLdv = optIniIntI("cfldv", 0);
		if (xb.cfLdv > 32) {
			log_printf(0, "***** WARNING: cfldv value %d in options.ini is too large, setting to max value of 32\n", xb.cfLdv);
			xb.cfLdv = 32;
		}
	}
	if (xb.cpuFan == -1)
		xb.cpuFan = optIniIntI("cpufan", -1);
	if (xb.gpuFan == -1)
		xb.gpuFan = optIniIntI("gpufan", -1);
	if (xb.cpuTemp == -1)
		xb.cpuTemp = optIniIntI("cputemp", -1);
	if (xb.gpuTemp == -1)
		xb.gpuTemp = optIniIntI("gputemp", -1);
	if (xb.edramTemp == -1)
		xb.edramTemp = optIniIntI("edramtemp", -1);
	if (xb.overCpuTemp == -1)
		xb.overCpuTemp = optIniIntI("overcputemp", -1);
	if (xb.overGpuTemp == -1)
		xb.overGpuTemp = optIniIntI("overgputemp", -1);
	if (xb.overEdramTemp == -1)
		xb.overEdramTemp = optIniIntI("overedramtemp", -1);
	if (xb.avRegion == -1)
		xb.avRegion = optIniIntI("avregion", -1);
	if (xb.gameRegion == -1)
		xb.gameRegion = optIniIntI("gameregion", -1);
	if (xb.dvdRegion == -1)
		xb.dvdRegion = optIniIntI("dvdregion", -1);
	if (!macidSetI()) {
		s = getIniValue("macid");
		if (s) {
			stripColonsI(s);
			/* the original's .rdata has these before the length error (its
			   tests were likely the other way round, but that reshape would
			   renumber the blocks src/options.prof is keyed by) */
			__asm__("" :: "i"("***** WARNING: invalid characters in macid '"), "i"("' provided in ini file! Discarding!\n"));
			if (strlen(s) != 12) {
				log_printf(0, "***** WARNING: invalid length macid '");
				showHexPairs(0, s);
				log_printf(0, "' provided in ini file! Discarding!\n", s);
			} else if (!validateStringU32(s)) {
				log_printf(0, "***** WARNING: invalid characters in macid '");
				showHexPairs(0, s);
				log_printf(0, "' provided in ini file! Discarding!\n", s);
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
	if (xb.type - BUILD_JTAG <= 3) {
		OPT("cygnos", 1, 0);
		OPT("demon", 8, 0);
		OPT("patchsmc", 0x8000000, 0);
		if (!xb.xellButton && (xb.bootFlags & 4)) {
			xb.xellButton = parseButtonI(getIniValue("xellbutton"), 0);
			if (!xb.xellButton) {
				log_printf(1, "default console DVD eject button is being used to start xell\n");
				xb.xellButton = 0x12;
			}
		}
		if (!xb.xellAltButton && (xb.bootFlags & 4)) {
			/* a dead edge into the remopower test: its block keeps a
			   count above its edge's */
			xb.xellAltButton = parseButtonI(getIniValue("xellbutton2"), aio_never);
			if (!xb.xellButton)
				log_printf(1, "alternate xell button is disabled\n");
		}
		OPT("smcnoeject", 0x400000, 0);
		OPT("smcnoblink", 0x800000, 0);
	}
	/* outside the block above: VRP threads its range test past this one
	   (a switch it can't), and smcnoblink's paths reload the type */
	if (xb.type == BUILD_JTAG) {
		OPT("nodvd", 2, 4);
		/* OPT("olddvd", 0, 4) with dead edges: Q (olddvd_q) merges into
		   the iniBoolInvalid block and leaves it its count, olddvd_set
		   merges into the `and ~4` block */
		do {
			if (perboxExists("olddvd")) {
				log_printf(1, "Using %s option (perbox file)\n", "olddvd");
			} else {
olddvd_q:
				if (aio_never)
					break;
				s = iniBoolInvalid("olddvd");
				if (!s) {
					if (!getIniBool("olddvd", 0))
						break;
					log_printf(1, "Using %s option (ini file)\n", "olddvd");
				} else {
					log_printf(0, "***** WARNING: options.ini setting '%s' invalid value '%s', discarding!\n", "olddvd", s);
					break;
				}
			}
olddvd_set:
			if (aio_never)
				break;
			xb.bootFlags &= ~4;
		} while (0);
		if (!xb.dualButton) {
			xb.dualButton = parseButtonI(getIniValue("dualboot"), 0);
			if (xb.xellButton == xb.dualButton) {
				log_printf(1, "dualboot setting ignored!\n");
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
		s = getIniValue("dvdkey");
		if (s && kvSetDvdKey(s))
			xb.bootFlags |= 0x2000000;
	}
blsuffix:
	if (!xb.blSuffix[0]) {
		s = getIniValue("rev");
		if (s)
			sprintf(xb.blSuffix, "_%s", s);
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
				log_printf(1, "\n\n***** ERROR: option '%s' provided on command line with = but no value!\n", pat);
				return 0;
			}
			i = len + 1;
		}
	}
	if (len != strlen(pat)) {
		/* TODO(xebuild.h cast): a signed test here, uint32_t in filelist_ini */
		if ((int)xb.nRawPatches <= 15) {
			strcpy(xb.rawPatch[xb.nRawPatches].name, pat);
			n = xb.nRawPatches;
			xb.rawPatch[n].offset = myatou32(val, -1);
			if (xb.rawPatch[xb.nRawPatches].offset != -1) {
				log_printf(1, "parsed [rawpatch] (%d) from command line file '%s' offset 0x%x\n", xb.nRawPatches + 1,
					   xb.rawPatch[xb.nRawPatches].name, xb.rawPatch[xb.nRawPatches].offset);
				xb.nRawPatches++;
				return 1;
			}
			log_printf(0, "***** ERROR: [rawpatch] command option '%s' does not appear to have sane offset info!\n", pat);
			return 0;
		}
		log_printf(0, "***** ERROR: %d of %d [rawpatch] slots are already full!\n", xb.nRawPatches, 16, pat);
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
	int i;

	if (xb.numPatches <= 15) {
		char path[1024];

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

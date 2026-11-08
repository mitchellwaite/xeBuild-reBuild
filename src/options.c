/* options: console types (xenon...corona), boot options from the command
   line, options.ini and perbox files, optional patches.  gcc emits the
   string literals in the order it expands their blocks, which gives the
   original's .rdata order.
   applyIniOptions' cold layout is set by optIniBool's and optIniBoolG's own
   profiles and by dead zero-byte hints (dead __builtin_constant_p feeds,
   dummy heap entries), with no profile file; tools/wip/aio/p1/NOTES.md has
   each hint (the helpers' arms and copies are gone:
   tools/wip/dehint/notes/options.md, attempt 7). */
#include <stdio.h>
#include <string.h>

#include "xebuild.h"
#include "filelist_ini.h"
#include "fileutil.h"
#include "keyvault.h"
#include "log.h"
#include "options.h"

/* parseButton after its first four names (gcc's ipa-split part in the
   original), the button for name s or def.
   Borderline, for review: def is always 0, so the helper could return 0
   itself.  The argument steers gcc twice: the bigger call lets fnsplit split
   parseButton at the call alone, so ipa-profile sees only zero-frequency
   calls and makes the helper unlikely executed (size optimised, in
   .text.unlikely, without a cold attribute); and ipa-cp's clone for def = 0
   is made after baseFileExists' split part, so it is emitted (and its FDE
   placed) second, as in the original.  Without it the helper needs
   cold, section, regparm and an asm label, and parseButton a winbutton
   expect (tools/wip/dehint/notes/options.md, attempt 17) */
static int parseButtonPart(const char *s, int def)
{
	int b = def;

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
   line already set it either way.  The `on` joins are threaded away after
   inlining; the profile they leave behind is what the OPT sites' layout
   needs (tools/wip/dehint/notes/options.md, attempt 7) */
_Bool optIniBool(const char *name, uint32_t set, uint32_t clear, int def)
{
	char *bad;
	_Bool on;

	if ((xb.bootFlags & set) || (xb.bootFlagsOff & set))
		on = 0;
	else if (perboxExists(name)) {
		log_printf(1, "Using %s option (perbox file)\n", name);
		on = 1;
	} else {
		bad = iniBoolInvalid(name);
		if (!bad) {
			on = getIniBool(name, def);
			if (on)
				log_printf(1, "Using %s option (ini file)\n", name);
		} else {
			log_printf(0, "***** WARNING: options.ini setting '%s' invalid value '%s', discarding!\n", name, bad);
			return 0;
		}
	}
	if (on) {
		xb.bootFlags &= ~clear;
		xb.bootFlags |= set;
	}
	return on;
}

/* optIniBool for noecdremap, nandmu, nosecurity, cygnos and smcnoeject.
   Borderline, for review: a second copy of optIniBool that exists to match
   (only inlined, so it emits no function of its own).  It differs in one
   statement: the warning arm sets `on` instead of returning, so `!bad`
   loses the early-return prediction (15% instead of 21.6%), which is the
   profile these sites need; the code after inlining is the same.  It
   replaces two hinted copies (optN and optIniBoolG: 6
   __builtin_constant_p, 2 __builtin_expect) */
static _Bool optIniBoolG(const char *name, uint32_t set, uint32_t clear, int def)
{
	char *bad;
	_Bool on;

	if ((xb.bootFlags & set) || (xb.bootFlagsOff & set))
		on = 0;
	else if (perboxExists(name)) {
		log_printf(1, "Using %s option (perbox file)\n", name);
		on = 1;
	} else {
		bad = iniBoolInvalid(name);
		if (!bad) {
			on = getIniBool(name, def);
			if (on)
				log_printf(1, "Using %s option (ini file)\n", name);
		} else {
			log_printf(0, "***** WARNING: options.ini setting '%s' invalid value '%s', discarding!\n", name, bad);
			on = 0;
		}
	}
	if (on) {
		xb.bootFlags &= ~clear;
		xb.bootFlags |= set;
	}
	return on;
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

/* applyIniOptions' copy of parseButton for xellbutton: the expect and the
   dead feed into z set its frequencies (z needs 3/8 of the else arm: 50%
   for the outer test, 75% for `> 0` from the opcode heuristic) */
static int parseButtonX(const char *s)
{
	int b = 0;

	if (!s) {
z:
		return 0;
	}
	if (__builtin_expect(!strnicmp(s, "power", 5), 1)) {
		b = 0x11;
	} else {
		if (__builtin_constant_p(xb.xellButton + 1)) { if (__builtin_constant_p(xb.xellButton + 2) > 0) goto z; }
		if (!strnicmp(s, "remopower", 9))
			b = 0x20;
		else if (!strnicmp(s, "remox", 5))
			b = 0x22;
		else if (!strnicmp(s, "winbutton", 9))
			b = 0x24;
		else
			b = parseButtonPart(s, 0);
	}
	return b;
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
	else
		b = parseButtonPart(s, 0);
	return b;
}

/* optIniInt's body for applyIniOptions' int options, as a macro.
   Borderline, for review: optIniInt itself is never early-inlined (it has
   three calls, so gcc 6's early inliner always refuses it), and the
   original's 15% profile for these blocks needs the code in
   applyIniOptions before profile_estimate; this replaced an always_inline
   copy of optIniInt.  The temporary is the inlined function's return
   value: storing var in both arms gives other code */
#define INI_INT(var, name, def) do { \
	char *bad = iniU32Invalid(name); \
	int v; \
	if (bad) { \
		log_printf(0, "***** WARNING: options.ini setting '%s' invalid value '%s', discarding!\n", name, bad); \
		v = def; \
	} else \
		v = getIniU32(name, def); \
	var = v; \
} while (0)

#define OPT(name, set, clear) if (!(xb.bootFlags & (set))) optIniBool(name, set, clear, 0)

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

/* bytes 1 .. n of a macid from the hex pairs at val, logged as ":%02x"
   (parseOption's comment says why it is a helper) */
static void macidRest(uint8_t *mac, const char *val, int n)
{
	int i;

	for (i = 0; i < n; i++) {
		log_printf(1, ":");
		mac[i] = myatox8(val + i * 2);
		log_printf(1, "%02x", mac[i]);
	}
}

/* one name[=value] from the command line option string.  The `if (val)`
   around the value options is in the Linux build (gcc 4.9 keeps the test);
   gcc 6 threads it away.
   Borderline, for review: cputemp and gpufan set an `ok` flag in the log's
   if and leave on it after, where the other value arms `goto bad` first.
   The log block then doesn't go straight to the return, so their success
   edge gets no early-return prediction (bad 48.8% instead of 59.8%); the
   flag's join is threaded away after profile_estimate.  cputemp's success
   then owns an epilogue copy and only edramtemp's -1 test falls into bad;
   gpufan's moves the jump alignment from avregion's test to gameregion's.
   (Every myatou32 arm but edramtemp in this form also matches.)
   Borderline, for review: a bool option sets `ok` after its "\n" (the
   value options are its else) and `if (ok) return 1;` comes after them,
   where a `return 1` in the arm would do.  The "\n" block then goes to that
   join, not straight to the return, so the setBoolOption edge gets no
   early-return prediction: 13.7% (call, `== 1`) instead of 9.2%.  The
   "\n" block reaches the epilogue-copy threshold (62, 10% of the entry is
   57), cputemp's head stays out of bb-reorder's first trace (271 under
   285), and, with the join after the value options, they get the whole
   false share; VRP1 threads the join away.  The "\n" block must stay ahead
   of cputemp (its literal comes before "cputemp" in .rdata).
   Borderline, for review: macid's last five bytes are a helper with the
   count as an argument (macidRest, called once, with 5).  Its loop's trip
   count isn't known at profile_estimate, so its exit is 9% (loop exit),
   not 1/6 (5 iterations); the len <= 0 setBoolOption copy's "\n" edge
   (13.7%) beats it when bb-reorder connects the "\n" trace.
   Borderline, for review: the unknown-with-value message tests `val &&
   vlen`, where vlen alone decides (vlen is 0 whenever val is NULL).  The
   `val` test lets VRP1 thread the val-null path straight to the
   incomplete message, so after PRE's tail merge that block has the whole
   path's frequency and reaches the epilogue-copy threshold (with `vlen`
   alone it keeps half, one short); it stays in place, so its literal
   stays between the unknown and bad messages.
   The return is uint32_t, as is parseCmdOptions': with int, uncprop
   returns stricmp's "macid" result for macid's 0s (kept in esi), and
   parseCmdOptions' `return 0` reuses the call's 0 only when the types
   agree. */
uint32_t parseOption(char *opt)
{
	char *val = NULL;
	int i, len, vlen, ok;

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
	ok = 0;
	if (setBoolOption(opt, val) == 1) {
		log_printf(1, "\n");
		ok = 1;
	} else if (val) {
		if (!stricmp(opt, "cputemp")) {
			xb.cpuTemp = myatou32(val, -1);
			ok = 0;
			if (xb.cpuTemp != -1) {
				log_printf(1, "Using CPUTEMP option, value %d\n", xb.cpuTemp);
				ok = 1;
			}
			if (!ok)
				goto bad;
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
			ok = 0;
			if (xb.gpuFan != -1) {
				log_printf(1, "Using GPUFAN option, value %d\n", xb.gpuFan);
				ok = 1;
			}
			if (!ok)
				goto bad;
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
				if (validateString(val)) {
					log_printf(1, "Using MACID option address: ");
					xb.macid[0] = myatox8(val);
					val += 2;
					log_printf(1, "%02x", xb.macid[0]);
					macidRest(&xb.macid[1], val, 5);
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
	if (ok)
		return 1;
	if (val && vlen) {
		log_printf(1, "\n\n***** ERROR: unknown option '%s' with value '%s' provided on the command line!\n", opt, val);
		return 0;
	}
	log_printf(1, "\n\n***** ERROR: unknown or incomplete option '%s' provided on the command line!\n", opt);
	return 0;
bad:
	log_printf(1, "\n\n***** ERROR: parsing option '%s', value '%s' is incorrect!\n", opt, val);
	return 0;
}

/* the ;-separated command line options.  Borderline, for review: uint32_t
   like parseOption's, which lets its `return 0` reuse the call's 0 (with
   int it doesn't; parseOption's comment) */
uint32_t parseCmdOptions(const char *opts)
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

/* options from perbox files and options.ini that the command line didn't
   set.  The cold block layout comes from the hints in the head comment. */
void applyIniOptions(void)
{
	char *s;
	int i;

	OPT("nomobile", 0x20000000, 0);
	OPT("noremap", 0x40000000, 0);
	if (!(xb.bootFlags & 0x80000000)) optIniBoolG("noecdremap", 0x80000000, 0, 0);
	if (!(xb.bootFlags & (0x10000000))) optIniBoolG("nandmu", 0x10000000, 0, 0);
	if (!(xb.bootFlags & (0x4000000))) optIniBoolG("nosecurity", 0x4000000, 0, 0);
	OPT("nosusecurity", 0x1000000, 0);
	OPT("smcnocheck", 0x200000, 0);
	if (!xb.cfLdv) {
		INI_INT(xb.cfLdv, "cfldv", 0);
		if (xb.cfLdv > 32) {
			log_printf(0, "***** WARNING: cfldv value %d in options.ini is too large, setting to max value of 32\n", xb.cfLdv);
			xb.cfLdv = 32;
		}
	}
	if (xb.cpuFan == -1)
		INI_INT(xb.cpuFan, "cpufan", -1);
	if (xb.gpuFan == -1)
		INI_INT(xb.gpuFan, "gpufan", -1);
	if (xb.cpuTemp == -1)
		INI_INT(xb.cpuTemp, "cputemp", -1);
	if (xb.gpuTemp == -1)
		INI_INT(xb.gpuTemp, "gputemp", -1);
	if (xb.edramTemp == -1)
		INI_INT(xb.edramTemp, "edramtemp", -1);
	if (xb.overCpuTemp == -1)
		INI_INT(xb.overCpuTemp, "overcputemp", -1);
	if (xb.overGpuTemp == -1)
		INI_INT(xb.overGpuTemp, "overgputemp", -1);
	if (xb.overEdramTemp == -1)
		INI_INT(xb.overEdramTemp, "overedramtemp", -1);
	if (xb.avRegion == -1)
		INI_INT(xb.avRegion, "avregion", -1);
	if (xb.gameRegion == -1)
		INI_INT(xb.gameRegion, "gameregion", -1);
	if (xb.dvdRegion == -1)
		INI_INT(xb.dvdRegion, "dvdregion", -1);
	if (!macidSet()) {
		s = getIniValue("macid");
		if (s) {
			stripColons(s);
			if (strlen(s) == 12) {
				if (validateString(s)) {
					for (i = 0; i < 6; i++) {
						xb.macid[i] = myatox8(s);
						s += 2;
					}
				} else {
					__builtin_memset(s, 0, __builtin_constant_p(xb.macid[1] + 9));
					__asm__ goto ("" :::: dz1);
					log_printf(0, "***** WARNING: invalid characters in macid '");
					showHexPairs(0, s);
					log_printf(0, "' provided in ini file! Discarding!\n", s);
				}
			} else {
				log_printf(0, "***** WARNING: invalid length macid '");
				showHexPairs(0, s);
				log_printf(0, "' provided in ini file! Discarding!\n", s);
			}
		}
	}
	if (xb.type - BUILD_JTAG <= 3) {
		if (!(xb.bootFlags & (1))) optIniBoolG("cygnos", 1, 0, 0);
		OPT("demon", 8, 0);
		OPT("patchsmc", 0x8000000, 0);
		if (!xb.xellButton && (xb.bootFlags & 4)) {
			xb.xellButton = parseButtonX(getIniValue("xellbutton"));
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
		if (!(xb.bootFlags & (0x400000))) optIniBoolG("smcnoeject", 0x400000, 0, 0);
		OPT("smcnoblink", 0x800000, 0);
	}
	/* outside the block above: VRP threads its range test past this one
	   (a switch it can't), and smcnoblink's paths reload the type */
	if (xb.type == BUILD_JTAG) {
		OPT("nodvd", 2, 4);
		/* no bit of its own: it clears nodvd's 4 */
		optIniBool("olddvd", 0, 4, 0);
		if (!xb.dualButton) {
			xb.dualButton = parseButton(getIniValue("dualboot"));
			if (xb.xellButton == xb.dualButton) {
				log_printf(1, "dualboot setting ignored!\n");
				__asm__ goto ("" :::: dz2);
				xb.dualButton = 0;
			}
		}
	}
	if (!(xb.bootFlags & 0x2000000)) {
		s = getIniValue("dvdkey");
		if (s && kvSetDvdKey(s))
			xb.bootFlags |= 0x2000000;
	}
	if (!xb.blSuffix[0]) {
		s = getIniValue("rev");
		if (s) {
			sprintf(xb.blSuffix, "_%s", s);
			/* dead feeds that key the dummies dz1 and dz2; dz1's return
			   takes its flow off dz2's feed, which settles the demon and
			   patchsmc getIniBool tie (no dummy in parseButtonX needed).
			   dz1's own test gets no flow (noreturn, 0%) and keeps that
			   return from being an early return; dz2's inner test sends
			   its other arm to dz1, which gives dz1 its count, so it needs
			   no expect of its own (tools/wip/dehint/notes/options.md,
			   attempt 23) */
			if (__builtin_constant_p(xb.blSuffix[1] + 1)) { if (__builtin_constant_p(xb.blSuffix[1] + 2)) goto dz1; return; }
			if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 15), 0)) { if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 16), 0)) goto dz2; goto dz1; }
		}
	}
	return;
	/* the dummy heap entries: zero-byte, reached only by the asm gotos and
	   the dead feeds above */
dz1:
	__builtin_unreachable();
dz2:
	__builtin_unreachable();
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
			if (!stricmp(path, xb.addons[i].name)) {
				log_printf(1, "***** WARNING: %s was provided both on command line and in ini, filtered duplicate!\n", name);
				return;
			}
		}
		strcpy(xb.addons[xb.numPatches].name, path);
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

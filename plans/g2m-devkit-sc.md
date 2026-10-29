# Glitch2m with a devkit SB/SC/SD/SE chain behind the mfg CB_A

Status: plan only, nothing implemented.

Goal: a glitch2m build whose `[<console>bl]` section has **7 lines**, with
the SC third, builds the whole chain CB_A (mfg) > SB > SC > SD > SE in one
pass:

```
[falconbl]
cba_9188_mfg.bin,e7ff60d0
SB_14352.bin,4712224f
SC_17489.bin,c665b4ec
SD_17489.bin,ba7a0f91
SE_17489.bin,0d896fd1
none,00000000
none,00000000
```

Today this needs a 6-line build (CB_A, SB, SD, SE, none, none) and then a
post-build step that inserts the SC after the SB and re-encrypts the SD and
SE so they chain from the SC's key. This plan moves that step into xeBuild.

Devkit bootloaders always decrypt the SC with the zero key (confirmed),
unlike any retail stage. A retail CB_A > CB_B chain has no SC (hwinit is
built into the CB_B).

## How xeBuild picks a layout

Everything is decided up front, before any file is loaded. `-t` sets
`xb.type` and the glitch flags (src/mode_build.c). `parseIni`
(src/filelist_ini.c) then picks, per build type, the bl line order and
count (`blRetail`, `blDevk`, `blDevgl`, `blTestk`, or `blJtag` with 9
lines), the slots' types and offsets (`locRetail`, `locDevk`, ...), and the
output name. `xb.cbb` also comes from the ini: the CB_B line is `none` or
not. File contents only validate (`checkBl`). The one exception is `f01c`
(`loadBl` retypes an `SE` found in the CF slot after loading), which is why
`encodeBls`, `addBls` and `calcBlAreaSize` each end with an `if (xb.f01c)`
tail.

A new `-t` type would be the most xeBuild-like way to do this, but adding
one isn't wanted for now. A 7-line section is the next best fit: the
parser picks the layout in the same place it picks every other table,
nothing is re-slotted after loading, and file contents only validate, as
for every other type. Detecting a CB_A + SB by magic would mean choosing
the layout after loading (the bootloaders can come from the SUPD, so the
parser can't see them) and moving slots around mid-load, as `f01c` does.

## How the 6-line g2m build works today

The bl section is read into the slots that `blRetail` names, with the
types from `locRetail` (shared by retail and every glitch build):

| ini line | `xb.files[]` index | type | holds today |
|---|---|---|---|
| 1 | 3 | 5 (CB_A) | `cba_9188_mfg.bin` |
| 2 | 4 | 6 (CB_B) | `SB_14352.bin` |
| 3 | 5 | 7 (CD) | `SD_17489.bin` |
| 4 | 6 | 8 (CE) | `SE_17489.bin` |
| 5 | 8 | 9 (CF) | none |
| 6 | 9 | 10 (CG) | none |

`nbl` is 6, so a seventh line is never read. With the 7-line ini above,
today's xeBuild puts the SC in the CD slot, the SD in the CE slot and the
SE in the CF slot (where `f01c` kicks in). That chain is wrong (SC keyed
from the CB_B, SE keyed from the SC), which is why the post-build step
exists.

`checkBl` (src/build.c) only checks the second magic byte for these types
(`?B`, `?C`, `?D`, `?E`), so the devkit SB, SD and SE pass as CB_B, CD and
CE. `xb.cbb` is 1 because slot 4 isn't `none`.

`encodeBls`, glitch branch (`xb.type <= BUILD_GLITCH`):

- type 5, `xb.cbb`: `cbaEncrypt(salt, ..., 1)` (no pairing).
- type 6: `cbbEncrypt`. A mfg CB_A (flags bit 0 at `cba + 6`) makes it use
  the zero key and skip the per-box hash ("CBB crypto method set to work
  with mfg CBA").
- type 7: `cdEncrypt(e, files[CB_B].key, ...)`.
- type 8: `ceEncrypt(e, files[type 7].key, ...)`.
- there is **no case 12**: an SC in a glitch build would not be encrypted.

`addBls` writes every file whose `offset` is -1 right after the previous
one, so the bootloaders are contiguous from 0x8000. `calcBlAreaSize`, glitch
branch, sums the sizes of types 5–8 to place the patch slots.

### The chain to reproduce already exists: DEVGL

`locDevgl` is SB (11), SC (12), CD (7), CE (8), and `encodeBls` encrypts it
as:

- 12: `cdEncryptZero` (key = HMAC(zero key, salt)),
- 7: `cdEncrypt(e, files[type 12].key, ...)`,
- 8: `ceEncrypt(e, files[type 7].key, ...)`.

The new chain is DEVGL's SB > SC > SD > SE with the mfg CB_A in front and
the SB in the CB_B slot. So the plan reuses type 12 for the SC and keeps the
SD/SE in types 7/8.

## Matching

As in plans/cb-ldv-1888.md and plans/header-fixes.md: everything below sits
behind `#ifdef XEBUILD_EXT`, the default build's preprocessed source must
not change, and `sh build.sh` must still end with
`10dac648197fa5cdbb82d975ab9ff11f64075c9686908dfd9a33edc533f1971c`.
`parseIni`, `encodeBls`, `calcBlAreaSize` and `verifyBlSigs` are matched
with code-free hints, so add separate `#ifdef` blocks and `static` helpers
rather than reshaping their code. New .data goes after the existing tables,
inside the `#ifdef` (filelist_ini.c is built with `-fno-toplevel-reorder`).

## Changes

### 1. The SC layout and its flag (filelist_ini.c, filelist_ini.h)

After `locRetail`, under `XEBUILD_EXT`:

```c
/* glitch2m with a devkit chain: locRetail with an SC (type 12) after the
   CB_B, and a 7-line bl section */
int blRetailSc[7] = {3, 4, 5, 6, 7, 9, 10};
struct fileloc locRetailSc[15] = {
	{0, 0}, {0x1000, 2}, {0x4000, 3}, {0x8000, 5}, {-1, 6}, {-1, 12}, {-1, 7},
	{-1, 8}, {0x70000, 25}, {0xb0000, 9}, {-1, 10}, {0xc0000, 24}, {0xc0060, 23},
	{-1, 26}, {0x3febe00, 27}
};
int blSc;
```

and in src/filelist_ini.h:

```c
#ifdef XEBUILD_EXT
/* the bl section has an SC: CB_A > SB (CB_B slot) > SC > SD > SE */
extern int blSc;
#endif
```

Index 4 is still the CB_B, so the `xb.cbb` test (`xb.files[4].name`) keeps
working. 15 files fit `XB_FILES_BOUND` (19); the addons start at 19.
`xb.nFlashFiles` (13) still names the type 26 slot, which `buildFlash`
uses as scratch for the security files (`xb.files[xb.nFlashFiles]`), as
index 12 does in `locRetail`.

### 2. Pick it from the section's line count (filelist_ini.c)

A `static` helper, under `XEBUILD_EXT`:

```c
/* the entries from off to the next label; iniPreParse has made every line
   a string and dropped comments and empty lines */
static int iniCountLines(unsigned char *buf, int off, int size)
{
	int n = 0;

	while (off < size && buf[off] && buf[off] != '[') {
		n++;
		off += strlen((char *)&buf[off]) + 1;
	}
	return n;
}
```

In `parseIni`, under `XEBUILD_EXT`, right after
`xb.nFlashFiles = xb.nFiles - 2;` (before the files loop, which assigns the
slots):

- only when `blOrder == blRetail` (retail and glitch builds; devkit
  sections already have their SC);
- build the bl label as the bl loop does (`[%sbl]` / `[%sbl%s]`) and find
  it with `memFindStr`. If it's missing, do nothing here: the bl loop
  reports it as today;
- 7 lines and `xb.glitch2mfg`: `blSc = 1`, `blOrder = blRetailSc`,
  `nbl = 7`, `xb.nFiles = 15`, `xb.nFlashFiles = 13`, and
  `log_printf(1, "ini: %s has 7 entries, building CB_A > SB > SC > SD > SE\n", label)`;
- 7 lines on any other build type: a warning that the 7th line is ignored
  and that an SC chain needs `-t glitch2m`, then carry on as today;
- any other count: nothing changes.

In the files loop's last `else`, under `XEBUILD_EXT`, take
`locRetailSc[i]` when `blSc`. The bl loop itself needs no change: it
already reads `nbl` lines into `blOrder`'s slots, so the SC lands at index
5, the SD at 6, the SE at 7 and the two `none` lines in the CF/CG slots.

After the `xb.cbb` test, under `XEBUILD_EXT`: if `blSc && !xb.cbb`, error
("the SB goes in the CB_B slot") and return 0.

### 3. Loading (src/build.c)

Nothing to add. `loadBlFiles` walks `xb.nFiles` slots, and `loadBl`
already loads type 12 through `loadInputFile` and `checkBl(..., 12, crc)`.
That check is what catches a wrong third line: a retail CB_A > CB_B ini
with a stray 7th line has a CD there, which fails the `?C` magic check.
The `f01c` path isn't reached: the CF slot holds the 6th line (`none`).

### 4. Encrypting (src/build.c, `encodeBls`)

Glitch branch, under `XEBUILD_EXT`:

- new `case 12:` (only `blSc` builds have a type 12 here). Devkit
  bootloaders decrypt the SC with the zero key:

  ```c
  case 12:
  	cdEncryptZero(e->data, e->key, e->size);
  	break;
  ```

- top of `case 7:`:

  ```c
  if (blSc) {
  	j = findFile(12);
  	cdEncrypt(e->data, xb.files[j].key, e->key, e->size);
  	break;
  }
  ```

- `case 8` stays: the SE is keyed from the type-7 file, now the SD that
  follows the SC.

The loop runs in `xb.files[]` order, so the SC (index 5) is encrypted, and
its key set, before the SD (index 6). `cbbEncrypt` for the SB is unchanged:
that part of today's output already works.

### 5. Image layout (src/build.c)

- `addBls`: nothing to add. The SC's offset is -1, so it lands right after
  the SB and pushes the SD and SE along, as in a devkit image.
- `calcBlAreaSize`, glitch branch: under `XEBUILD_EXT`, add
  `findFileSize(12)` when `blSc`. Without it the patch slots and the xell
  room check are computed as if the SC weren't there, and can overlap the
  SE.

### 6. Virtual fuses: LDV lines zero (src/build.c, `buildFlash`)

With an SE the virtual fuses' LDV lines (fuse lines 7–11, `fuses.bin` bytes
56–95) must be zero. XDKbuild's `fixFuses`, the post-build step this plan
replaces, does exactly that: `memset(vfuses + 56, 0, 40)` and nothing else
(lines 0–6 are left as xeBuild wrote them).

Today, for a g2m build:

- `buildImage` (src/image_write.c) turns `xb.cfLdv == 0` into 1 when there
  is a CPU key ("cfldv was not set anywhere"); otherwise it holds the
  `cfldv` option or the dump's LDV.
- `buildFlash` then, before `encodeBls`, calls `setFuseCpuKey` on the type
  24 file, which calls `setFuseLdv(fuse, xb.cfLdv)`: line 7 (`fuse + 56`)
  and line 8 (`fuse + 64`) get that LDV's nibbles. Lines 9–11 are never
  written: they're zero in `defBl60`, but `loadBl60` takes a 0x60-byte
  `fuses.bin` from the base dir as is.
- So the vfuses carry the console's LDV (or the guessed 1), which an SE
  chain doesn't boot with.

xeBuild's own SE case, `f01c`, sets `xb.cfLdv = 0` in `loadBl`, which
also changes the LDV that secdata, CRL and DAE get later in `buildFlash`.
This plan doesn't: like XDKbuild, it changes only the vfuses, and
`xb.cfLdv` (and every other file that carries it) stays as it is.

In `buildFlash`'s `if (fuse)` block, after `setFuseCpuKey(e->data)`, under
`XEBUILD_EXT`:

```c
#ifdef XEBUILD_EXT
	if (blSc) {
		/* an SE chain boots with no LDV in the vfuses (lines 7-11) */
		memset(e->data + 56, 0, 40);
		log_printf(1, "SE boot chain, fuse LDV lines cleared\n");
	}
#endif
```

`setFuseCpuKey` has already logged the LDV it wrote ("Fuse CF LDV set
to"), so the second line says it was cleared. Clearing all 40 bytes also
covers a user `fuses.bin` with data in lines 9–11.

Lines 0–2 stay as today: `encodeBls` case 6 writes them from the SB's
header through `showExpectedFuses(..., xb.files[24].data, xb.f01c)`, and
XDKbuild doesn't touch them.

XDKbuild also searches for the vfuses (`C0FFFFFFFFFFFFFF`) when they aren't
at the patch slot offset (header 0x0c) plus header 0x70, and rewrites 0x70.
It needs that because it grows the bootloader area after xeBuild has laid
out the image. Here the SC is counted in `calcBlAreaSize` (step 5), and
`buildFlash` places the type 24 file at `imgCfOffset() + imgCfSize()`, the
same two header fields, so nothing to fix up.

### 7. Signature check (src/build.c, `verifyBlSigs`), optional

`case 12` looks up the SB as type 11 and today would log "could not locate
SB data". Under `XEBUILD_EXT`, use `findFile(6)` when `blSc` so the SC is
checked (and resigned with `xb.prvKey`) against the SB's key as in devkit
builds.

### 8. Build the variant (build.sh)

Same `sh build.sh ext` switch as plans/header-fixes.md step 2. If that plan
lands first, nothing to add here; otherwise do that step as part of this
one.

### 9. Document it

- README.md: in the `XEBUILD_EXT` section, the 7-line bl section for
  glitch2m, with the example above, the warning/errors, and that the
  vfuses' LDV lines are zeroed for it (`cfldv` still applies to
  everything else).
- NOTES.md: point to this plan from Status.

## Verification

1. `sh build.sh` (no switch) still ends with the reference SHA256.
2. Ext build, controls that must match the reference `xeBuild.exe` byte for
   byte (same inputs, `-norandom`):
   - the 6-line g2m ini (CB_A, SB, SD, SE, none, none);
   - retail and glitch2 CB_A > CB_B builds with a stray 7th line (the
     warning, then the same output as today);
   - a single-CB retail build and a devkit build.
3. Ext build, the 7-line ini, `-norandom`:
   - the log shows the "has 7 entries" line and
     `adding SC_17489.bin at raw offset ...` between the SB and the SD;
   - compare against the image from the current post-build step, made from
     the same 6-line build. They should match except for whatever that
     tool sets differently (e.g. salts); any other difference names a wrong
     key or offset;
   - a small script in `tools/`: walk the chain from 0x8000 (CB_A with the
     1BL key, SB as `cbbEncrypt` derives it, SC with HMAC(zero key, salt),
     SD with the SC's key, SE with the SD's key), check each decrypted
     magic and size, and the SE hash against the SD (`+588`, as
     `verifyBlSigs` does for devkit builds);
   - the patch slots and xell start after the SE's end;
   - the vfuses sit at header 0x0c + header 0x70 (where XDKbuild looks
     first), lines 7–11 are zero, and lines 0–6 match the 6-line build's.
     Repeat with `cfldv=5` and with a `fuses.bin` whose lines 9–11 aren't
     zero: still zero. Everything outside the vfuses (secdata, CRL, DAE)
     matches the 6-line build's.
4. Errors: a g2m 7-line ini with a CD (not an SC) third (magic error from
   `checkBl`), and with `none` in the SB line.
5. The same ini through `mode_update` (`-u`), which also goes through
   `parseIni` and `loadBlFiles`: same detection, same output for the parts
   an update writes.
6. Hardware, if available: the image boots to the devkit kernel on a
   glitched console.

Needs the user's real inputs (CB_A 9188 mfg, SB 14352, SC/SD/SE 17489,
an image from the current post-build step), which the repo doesn't have.

## Open questions

- **A new `-t` type later.** If one is added (e.g. `glitch2mdev`), step 2's
  count check becomes "this type picks `blRetailSc`/`locRetailSc`", and
  steps 3–7 stay as they are.
- **Lines 1–2 of the vfuses.** `f01c` also passes `clear` to
  `showExpectedFuses`, which sets line 1 to the devkit pattern and zeroes
  line 2 (the CB sequence). XDKbuild leaves both as the g2m build wrote
  them and those images boot, so this plan does too. If an SE chain turns
  out to need them cleared, pass `xb.f01c || blSc` in `encodeBls` case 6.- **The CB_B slot isn't checked for an SB.** A g2m 7-line ini with a retail
  CB_B and an SC would build, and wouldn't boot. Checking it would mean a
  magic test on a loaded file, which this plan avoids; `cbbEncrypt`'s "CBB
  crypto method set to work with mfg CBA" log at least shows the CB_A is a
  mfg one.
- **Reading the image back.** `image_read` and `mode_extract` assume
  CB_A/CB_B/CD/CE in the glitch layout. Using the output as `nanddump.bin`
  (reading the SC back) is out of scope here.
- **Flash header build version.** Devkit builds set it from the SE
  (`setFlashBuild`, type 14). This plan leaves the g2m value as today,
  which the post-build step also keeps.

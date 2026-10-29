# Glitch2m with a devkit SB/SC/SD/SE chain behind the mfg CB_A

Status: plan only, nothing implemented.

Goal: a glitch2m build whose CB_B slot holds a devkit **SB** builds the
whole chain CB_A (mfg) > SB > SC > SD > SE in one pass, with the SC as the
third line of the `[<console>bl]` section:

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

The mode is chosen by **what the files are**, not by how many lines the
section has: a CB_A in the CB slot and an SB in the CB_B slot. A retail
CB_A > CB_B chain has no SC (hwinit is built into the CB_B), so it must
never take this path. Devkit bootloaders always decrypt the SC with the
zero key (confirmed), unlike any retail stage.

## How the 6-line g2m build works today

The bl section is read by `parseIni` (src/filelist_ini.c, the `[%sbl]`
loop) into the slots that `blRetail` names, with the types from
`locRetail` (shared by retail and every glitch build):

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
SE in the CF slot (where `loadBl` turns it into the `f01c` "SE where the CF
goes" case). That chain is wrong (SC keyed from the CB_B, SE keyed from the
SC), which is why the post-build step exists.

`checkBl` (src/build.c) only checks the second magic byte for these types
(`?B`, `?C`, `?D`, `?E`), so the devkit SB, SD and SE pass as CB_B, CD and
CE. `xb.cbb` is 1 because slot 4 isn't `none`.

Order in `buildFlash` (src/build.c): `suLoadDir`, `loadBlFiles` (loads
`xb.files[1..]` in index order through `loadBl`), `verifyBlSigs`,
`calcBlAreaSize`, the glitch blmod patching, `encodeBls`, `addBls`. All of
them look files up by type (`findFile`, `findFileSize`) and none keeps an
index across these calls. Bootloaders can come from the data dir or from
the SUPD (`suGetFile`), so their magic is only known once `loadBl` has run.
`parseIni` can't see it.

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
`parseIni`, `loadBlFiles`, `encodeBls`, `calcBlAreaSize` and `verifyBlSigs`
are matched with code-free hints, so add separate `#ifdef` blocks and
`static`/new functions rather than reshaping their code. New .data goes
after the existing tables, inside the `#ifdef` (filelist_ini.c is built
with `-fno-toplevel-reorder`).

## Changes

### 1. Keep the seventh line (filelist_ini.c)

The section is still read into `blRetail`'s six slots as today. Under
`XEBUILD_EXT`, after the bl loop and only when `blOrder == blRetail`
(retail and glitch builds; devkit sections already have their SC): if
`pos < end`, read one more `name[,crc]` line the same way into an ext-only
`static struct { char name[...]; uint32_t crc; } blLines[7]`, and copy the
six parsed lines into it too. `nBlLines` is 6 or 7. A 7th line on its own
changes nothing: it is only used if step 3 finds an SB. More than 7 lines
are ignored, as today.

`blLines` keeps the ini order, so step 3 can lay the lines out again
without parsing a second time.

### 2. A layout with an SC slot (filelist_ini.c, filelist_ini.h)

After `locRetail`, under `XEBUILD_EXT`:

```c
/* the bl slots of locRetail with an SC (type 12) after the CB_B */
int blRetailSc[7] = {3, 4, 5, 6, 7, 9, 10};
```

and an ext-only global, defined in src/filelist_ini.c and declared in
src/filelist_ini.h:

```c
#ifdef XEBUILD_EXT
/* a CB_A > SB chain: the SC follows the SB, then SD, SE */
extern int blSc;
int blInsertSc(void);
#endif
```

The resulting layout is `locRetail` with `{-1, 12}` at index 5:

| index | 0 | 1 | 2 | 3 | 4 | **5** | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| type | 0 | 2 | 3 | 5 | 6 | **12** | 7 | 8 | 25 | 9 | 10 | 24 | 23 | 26 | 27 |

Index 4 is still the CB_B, so the `xb.cbb` test (`xb.files[4].name`) keeps
working. 15 files fit `XB_FILES_BOUND` (19); the addons start at 19.

### 3. Detect CB_A + SB and insert the slot (filelist_ini.c, build.c)

`blInsertSc` (filelist_ini.c, which owns the tables and `blLines`), called
once the CB_A and the CB_B slot are loaded:

1. Return 0 (nothing to do) unless all of these hold:
   - `blOrder == blRetail` and `xb.cbb` (a CB_A > CB_B build),
   - `xb.files[3].data` starts with `'C','B'` (the CB_A),
   - `xb.files[4].data` starts with `'S','B'` (a devkit SB, not a CB_B).
   Checking both bytes matters: `checkBl` only checks the second one, so a
   `CB` and an `SB` both pass as type 5 or 6.
2. Errors (return -1, with a message naming the problem):
   - `nBlLines < 7`: "%s has an SB in the CB_B slot, the SC must follow
     it". The 6-line SB build of today is still possible, but it's the
     broken chain this replaces, so stop instead of building it;
   - not `xb.glitch2mfg`: "an SB in the CB_B slot needs a glitch2m build";
   - CB_A flags bit 0 (`getBeU16(cba + 6) & 1`) clear: "the CB_A isn't a
     mfg one". Without it `cbbEncrypt` per-box hashes the SB with the CPU
     key.
3. Move `xb.files[5..13]` up one (`memmove` to `[6..14]`). Indices 5 and up
   aren't loaded yet (`data` NULL), and their types, offsets and the fixed
   names (xell, fuses, patches, smc_config) move with them, so they match
   the table above.
4. Clear `xb.files[5]`, set `type = 12`, `offset = -1`.
5. Set the names and crcs of the bl slots from `blLines` through
   `blRetailSc` (line 3 → index 5 the SC, 4 → 6, 5 → 7, 6 → 9, 7 → 10).
6. `xb.nFiles = 15`, `xb.nFlashFiles = 13`, `blSc = 1`, and
   `log_printf(1, "CB_A > SB chain: SC %s inserted after %s\n", ...)`.

In `loadBlFiles` (src/build.c), under `XEBUILD_EXT`, right after the
`r` check in the loop:

```c
#ifdef XEBUILD_EXT
		if (i == 4 && blInsertSc() < 0)
			return -1;
#endif
```

The loop bound reads `xb.nFiles` from the global each time (loadBl calls
out), so it goes on to load indices 5–14 from the new layout. `loadBl`
already loads type 12 through `loadInputFile` and
`checkBl(..., 12, crc)`, which checks the `?C` magic and the crc, so a
wrong file in the SC line fails there. The `f01c` path isn't reached: the
CF slot now holds line 6 (`none`).

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

### 6. Signature check (src/build.c, `verifyBlSigs`), optional

`case 12` looks up the SB as type 11 and today would log "could not locate
SB data". Under `XEBUILD_EXT`, use `findFile(6)` when `blSc` so the SC is
checked (and resigned with `xb.prvKey`) against the SB's key as in devkit
builds.

### 7. Build the variant (build.sh)

Same `sh build.sh ext` switch as plans/header-fixes.md step 2. If that plan
lands first, nothing to add here; otherwise do that step as part of this
one.

### 8. Document it

- README.md: in the `XEBUILD_EXT` section, the CB_A > SB chain for
  glitch2m, with the example above, how it is detected and its errors.
- NOTES.md: point to this plan from Status.

## Verification

1. `sh build.sh` (no switch) still ends with the reference SHA256.
2. Ext build, controls that must match the reference `xeBuild.exe` byte for
   byte (same inputs, random keys off):
   - retail and glitch2 CB_A > CB_B builds, **with a stray 7th line** in
     the section (no SB, so it is ignored as today);
   - a single-CB retail build, a glitch2m build with a retail CB_B, a
     devkit build.
3. Ext build, the 7-line ini, random keys off:
   - the log shows the "SC ... inserted" line and
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
   - the patch slots and xell start after the SE's end.
4. Errors: the 6-line SB ini (no SC), the 7-line ini on a glitch2 build, a
   non-mfg CB_A with an SB, a non-SC file in the SC line (magic error from
   `checkBl`).
5. The same ini through `mode_update` (`-u`), which also goes through
   `buildImage` and `loadBlFiles`: same detection, same output for the
   parts an update writes.
6. Hardware, if available: the image boots to the devkit kernel on a
   glitched console.

Needs the user's real inputs (CB_A 9188 mfg, SB 14352, SC/SD/SE 17489,
an image from the current post-build step), which the repo doesn't have.

## Open questions

- **The 6-line SB build becomes an error.** It's the broken chain that
  needs the post-build step, so stopping seems right. If someone still
  wants it (e.g. to keep their tool working), turn the error into a
  warning and leave the layout alone.
- **Other build types.** Only glitch2m is allowed. Whether a CB_A > SB chain
  makes sense on a non-mfg CB_A is untested, so it errors instead.
- **Reading the image back.** `image_read` and `mode_extract` assume
  CB_A/CB_B/CD/CE in the glitch layout. Using the output as `nanddump.bin`
  (reading the SC back) is out of scope here.
- **Flash header build version.** Devkit builds set it from the SE
  (`setFlashBuild`, type 14). This plan leaves the g2m value as today,
  which the post-build step also keeps.

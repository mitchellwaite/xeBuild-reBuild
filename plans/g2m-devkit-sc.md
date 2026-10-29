# Glitch2m with a devkit SB/SC/SD/SE chain behind the mfg CB_A

Status: plan only, nothing implemented.

Goal: a glitch2m build whose `[<console>bl]` section lists a **seventh**
entry, an SC between the SB and the SD, builds the whole chain
CB_A (mfg) > SB > SC > SD > SE in one pass:

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

Today this needs a 6-entry build (CB_A, SB, SD, SE, none, none) and then a
post-build step that inserts the SC after the SB and re-encrypts the SD and
SE so they chain from the SC's key. This plan moves that step into xeBuild.

## How the 6-entry g2m build works today

The bl section is read by `filelist_ini.c` (the `[%sbl]` loop) into the
slots that `blRetail` names, with the types from `locRetail` (shared by
retail and every glitch build):

| ini line | `xb.files[]` index | type | holds today |
|---|---|---|---|
| 1 | 3 | 5 (CB_A) | `cba_9188_mfg.bin` |
| 2 | 4 | 6 (CB_B) | `SB_14352.bin` |
| 3 | 5 | 7 (CD) | `SD_17489.bin` |
| 4 | 6 | 8 (CE) | `SE_17489.bin` |
| 5 | 8 | 9 (CF) | none |
| 6 | 9 | 10 (CG) | none |

`nbl` is 6, so a seventh line is never read. With the 7-entry ini above,
today's xeBuild therefore puts the SC in the CD slot, the SD in the CE slot
and the SE in the CF slot (where `loadBl` turns it into the `f01c` "SE where
the CF goes" case). That chain is wrong (SC keyed from the CB_B, SE keyed
from the SC), which is why the post-build step exists.

`checkBl` (src/build.c) only checks the second magic byte for these types
(`?B`, `?D`, `?E`), so the devkit SB, SD and SE pass as CB_B, CD and CE.
`xb.cbb` is 1 because slot 4 isn't `none`.

`encodeBls` (src/build.c), glitch branch (`xb.type <= BUILD_GLITCH`):

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

The devkit build (`locDevk`) does the same with types 12, 13, 14. Both say
the SB derives the SC's key from the zero key and each later stage from the
one before. The new chain is DEVGL's SB > SC > SD > SE with the mfg CB_A in
front and the SB in the CB_B slot. So the plan reuses type 12 for the SC
and keeps the SD/SE in types 7/8.

## Matching

As in plans/cb-ldv-1888.md and plans/header-fixes.md: everything below sits
behind `#ifdef XEBUILD_EXT`, the default build's preprocessed source must
not change, and `sh build.sh` must still end with
`10dac648197fa5cdbb82d975ab9ff11f64075c9686908dfd9a33edc533f1971c`. The
bl parser, `encodeBls`, `calcBlAreaSize` and `verifyBlSigs` are matched with
code-free hints, so add separate `#ifdef` blocks and `static` helpers rather
than reshaping their code. New .data (the tables below) goes after the
existing tables, inside the `#ifdef` (filelist_ini.c is built with
`-fno-toplevel-reorder`).

## Changes

### 1. A flag for the mode (filelist_ini.c, filelist_ini.h)

An ext-only global, defined in src/filelist_ini.c and declared in
src/filelist_ini.h:

```c
#ifdef XEBUILD_EXT
/* the bl section has an SC: CB_A > SB (CB_B slot) > SC > SD > SE */
extern int blSc;
#endif
```

### 2. Tables with an SC slot (filelist_ini.c)

After `locRetail`, under `XEBUILD_EXT`:

```c
/* locRetail with an SC (type 12) between the CB_B and the CD */
int blRetailSc[7] = {3, 4, 5, 6, 7, 9, 10};
struct fileloc locRetailSc[15] = {
	{0, 0}, {0x1000, 2}, {0x4000, 3}, {0x8000, 5}, {-1, 6}, {-1, 12}, {-1, 7},
	{-1, 8}, {0x70000, 25}, {0xb0000, 9}, {-1, 10}, {0xc0000, 24}, {0xc0060, 23},
	{-1, 26}, {0x3febe00, 27}
};
```

Index 4 is still the CB_B, so the `xb.cbb` test (`xb.files[4].name`) keeps
working. 15 files fit `XB_FILES_BOUND` (19); the addons start at 19.

### 3. Pick the tables from the section (filelist_ini.c)

The slots have to be chosen before the "files this build type uses" loop,
which runs before the bl section is read. Under `XEBUILD_EXT`, right after
`xb.nFlashFiles = xb.nFiles - 2;`:

- only when `blOrder == blRetail` (retail and glitch builds; devkit
  sections already have their SC);
- build the same label as the bl loop (`[%sbl]` / `[%sbl%s]`), find it,
  and count its entries with a `static` helper: the non-empty
  NUL-terminated strings from the label to the next `[` (bounded by `size`
  when there is no next section; check what `iniPreParse` leaves for blank
  lines and comments);
- 7 entries:
  - not `xb.glitch2mfg`: error ("an SC in %s is only supported for
    glitch2m builds") and return 0;
  - otherwise `blSc = 1`, `blOrder = blRetailSc`, `nbl = 7`,
    `xb.nFiles = 15`, `xb.nFlashFiles = 13`, and
    `log_printf(1, "ini: %s has an SC, building CB_A > SB > SC > SD > SE\n", label)`;
- 6 entries: nothing changes;
- more than 7: error, so a typo doesn't silently drop a file.

In the files loop's last `else`, under `XEBUILD_EXT`, take `locRetailSc[i]`
when `blSc`. The bl loop itself needs no change: it already reads `nbl`
entries into `blOrder`.

After the `xb.cbb` test, under `XEBUILD_EXT`: if `blSc && !xb.cbb`, error
("the SB goes in the CB_B slot"). The CB_A should be a mfg one: warn if
flags bit 0 (`getBeU16(cba + 6) & 1`) is clear once it's loaded (step 5).

### 4. Loading (src/build.c)

Nothing to add. `loadBl` already loads type 12 through `loadInputFile` and
`checkBl(..., 12, crc)`, which checks the `?C` magic and the crc. The
`f01c` path isn't reached because type 9 is `none`.

### 5. Encrypting (src/build.c, `encodeBls`)

Glitch branch, under `XEBUILD_EXT`:

- new `case 12:` (only `blSc` builds have a type 12 here):

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
- in `case 5` (or a `static` helper called before the loop), when `blSc`
  and the CB_A's flags bit 0 is clear, log a warning that the SB/SC chain
  expects a mfg CB_A.

The loop runs in `xb.files[]` order, so the SC (index 5) is encrypted, and
its key set, before the SD (index 6). `cbbEncrypt` for the SB is unchanged:
that part of today's output already works.

### 6. Image layout (src/build.c)

- `addBls`: nothing to add. The SC's offset is -1, so it lands right after
  the SB and pushes the SD and SE along, as in a devkit image.
- `calcBlAreaSize`, glitch branch: under `XEBUILD_EXT`, add
  `findFileSize(12)` when `blSc`. Without it the patch slots and the xell
  room check are computed as if the SC weren't there, and can overlap the
  SE.

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

- README.md: in the `XEBUILD_EXT` section, the 7-entry bl section for
  glitch2m, with the example above, and its errors.
- NOTES.md: point to this plan from Status.

## Verification

1. `sh build.sh` (no switch) still ends with the reference SHA256.
2. Ext build, 6-entry g2m ini (CB_A, SB, SD, SE, none, none): byte for byte
   the same as the reference `xeBuild.exe` with the same inputs and random
   keys off. Also a retail, a glitch2 and a devkit build as controls.
3. Ext build, the 7-entry ini, random keys off:
   - the log shows the new "has an SC" line and
     `adding SC_17489.bin at raw offset ...` between the SB and the SD;
   - compare against the image from the current post-build step, made from
     the same 6-entry build. They should match except for whatever that
     tool sets differently (e.g. salts); any other difference names a wrong
     key or offset;
   - a small script in `tools/`: walk the chain from 0x8000 (CB_A with the
     1BL key, SB as `cbbEncrypt` derives it, SC with HMAC(zero key, salt),
     SD with the SC's key, SE with the SD's key), check each decrypted
     magic and size, and the SE hash against the SD (`+588`, as
     `verifyBlSigs` does for devkit builds);
   - the patch slots and xell start after the SE's end.
4. Errors: the 7-entry section on a glitch2 / retail build, a 7-entry
   section with `none` in the SB line, a non-SC file in the SC line (magic
   error from `checkBl`), an 8-entry section.
5. Hardware, if available: the image boots to the devkit kernel on a
   glitched console.

Needs the user's real inputs (CB_A 9188 mfg, SB 14352, SC/SD/SE 17489,
an image from the current post-build step), which the repo doesn't have.

## Open questions

- **SC key.** The plan takes "SB decrypts the SC with the zero key" from
  xeBuild's own devkit and DEVGL paths (`cdEncryptZero`). The comparison in
  verification step 3 confirms it against the post-build tool.
- **Detection by count.** A seventh line turns the mode on. The
  alternatives are a command-line switch or checking the third file's magic
  for `SC` after loading; both mean choosing slots late or twice. Counting
  keeps the ini as the only input, matching the request.
- **Other build types.** Only glitch2m is allowed. Glitch2 with a non-mfg
  CB_A would per-box hash the SB with the CPU key; whether that chain is
  useful is untested, so it errors instead.
- **Reading the image back.** `image_read`, `mode_update` and
  `mode_extract` assume CB_A/CB_B/CD/CE in the glitch layout. Updating
  (`-u`) only replaces the CF/CG/xell/patches, so it should be fine, but
  reading the SC back (e.g. using the output as `nanddump.bin`) is out of
  scope here. Worth one check in verification step 3.
- **Flash header build version.** Devkit builds set it from the SE
  (`setFlashBuild`, type 14). This plan leaves the g2m value as today,
  which the post-build step also keeps.

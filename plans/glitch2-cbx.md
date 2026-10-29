# Glitch2 / glitch2m with a CB_X between the CB_A and the CB_B

Status: plan only, nothing implemented.

Goal: a new build switch, `-cbx`, makes a glitch2 or glitch2m build put a
CB_X between the CB_A and the CB_B, in one pass. xeBuild carries a built-in
CB_X (1024 bytes); `-cbxfile <file>` uses a custom one instead:

```
xeBuild -t glitch2 -c jasper -d files -cbx out.bin
xeBuild -t glitch2m -c falcon -d files -cbxfile mycbx.bin out.bin
```

gives the chain

```
0x8000  CB_A   the ini's, encrypted as today (1BL key)
        CB_X   encrypted the way a CB_B is (key from the CB_A)
        CB_B   plaintext, its RC4 key at +0x10
        CD     encrypted from the CB_B's key, as today
        CE     as today
```

The same goes for glitch2m images with the devkit chain behind the mfg
CB_A: the CB_X goes between the CB_A and the SB, which takes the CB_B's
place (see "Glitch2m with an SB" below):

```
0x8000  CB_A   mfg, encrypted as today
        CB_X   encrypted the way a CB_B is (zero key: mfg CB_A)
        SB     plaintext, its RC4 key at +0x10
        SC     zero key, as in plans/g2m-devkit-sc.md (7-line ini only)
        SD     from the SC's key (7-line) or the SB's key (6-line), as without -cbx
        SE     from the SD's key
```

Today this needs a normal xeBuild image and then a post-build step (JRunner's
`RGH2to3.ConvertRgh2ToRgh3` with `patchSMC = false`: "we're only injecting
the CB_X"). This plan moves that step into xeBuild.

## What JRunner's post-build step does

`J-Runner/Classes/RGH2to3.cs`, reading the bootloaders from the image's
flash header (0x08) on:

1. Takes the CB_A and the CB_X ("rgh3Payload") from an RGH3 ECC file. The
   CB_X is stored there encrypted as a CB_B with the **zero** CPU key.
   The ECC's CB_A is 10918, a mfg CB_A, and a mfg CB_A derives the next
   stage's key with the zero key, so the ECC's CB_X works on any console.
   (JRunner also patches four words at 0x354 of an older CB_X; current
   CB_X files don't need it, and this plan doesn't do it.)
2. Decrypts the image's CB_A (`DecryptCBA`: key = HMAC(1BL key, +0x10)) and
   then its CB_B with the console's CPU key (`DecryptCBB`: key =
   HMAC(CB_A key, CB_B +0x10, CPU key)). `DecryptCBB` returns the header,
   **the key in place of the nonce at +0x10**, and the RC4-decrypted rest
   from +0x20. It checks the result has `XBOX_ROM` (or zeros) at 0x392.
3. Writes `header..CB_A offset` + the ECC's CB_A + the CB_X + the decrypted
   CB_B + everything after the old CB_B, truncated to the old length, and
   adds the ECC back. So the CD, CE and padding just move along by the size
   difference; the CD and CE themselves are untouched. Xell (0x70000) and
   the patch slots after it don't move.

So:

- the CB_X is encrypted like a CB_B: the CB_A derives its key from its own
  key, the CB_X's nonce and a CPU key (the zero key for a mfg CB_A);
- the real CB_B is stored in plaintext, with its own RC4 key where the nonce
  was (that's how a CB_A leaves a decrypted CB_B in memory, and how the CB_B
  then finds the key it chains the CD from);
- the CD and later stages are encrypted exactly as with an encrypted CB_B:
  the CD's key comes from the CB_B's key, which doesn't change.

What `-cbx` does differently from JRunner:

- **The CB_A stays the ini's.** RGH3 doesn't need a special CB_A; JRunner
  swaps in 10918 only because, being mfg, it lets the post-build step ship
  one pre-encrypted CB_X. xeBuild encrypts the CB_X itself, so it keys it
  against whatever CB_A the build uses.
- **The SMC stays the per-build `smc.bin`.** `patchSMC` isn't part of this.

## Where it fits in xeBuild today

Glitch builds (`xb.type == BUILD_GLITCH`, `xb.glitch2`, and `xb.cbb` from
the ini's CB_B line not being `none`), in `buildFlash` (src/build.c):

- `loadBlFiles` loads the slots `locRetail` names: CB_A (index 3, type 5),
  CB_B (4, type 6), CD (5, type 7), CE (6, type 8), xell (7, type 25, at
  0x70000), CF/CG (8/9). Offsets of -1 mean "right after the previous one".
- `calcBlAreaSize`, glitch branch: CB_A offset + sizes of types 5–8, then
  xell, rounded to 0x10000; that's where the patch slots go.
- `patchBlsBlmod` puts the glitch patches into the CB_B (`xb.cbb`).
- `encodeBls`, glitch branch, in `xb.files[]` order:
  - type 5 with `xb.cbb`: `cbaEncrypt(salt, ..., 1)`;
  - type 6: `cbbEncrypt(salt, cbb, cbaKey, cba, key, size, zero)`, which
    reads the CB_A's flags (+6): bit 0 (mfg CB_A) uses the zero key instead
    of the CPU key and skips the per-box hash; 0x1000 mixes in the CB_A's
    header (15572+ method). It sets the nonce (`infoKey1`), the pairing and
    LDV at +0x20 and the per-box hash at +0x30, then RC4s from +0x20, and
    leaves the key in `e->key`;
  - type 7: `cdEncrypt(e, files[CB_B].key, ...)`.
- `addBlsToImage` writes each file at a running `off` (fixed offsets reset
  it), so the bootloaders are contiguous from 0x8000.

Built-in defaults already exist for other files: `defPayload`, `defCore`
and `defBl60` are byte arrays at the top of src/build.c, used when no file
is found (`loadBl` cases 1, 22, 24). The built-in CB_X follows that
pattern.

The CB_X therefore needs: a source (built-in or file), a key from the CB_A
(as `cbbEncrypt` derives it), room in `calcBlAreaSize`, and a place in
`addBlsToImage` right before the CB_B. The CB_B needs its RC4 undone after
`cbbEncrypt` and its key written to +0x10. Nothing after the CB_B changes.

### Why not a new slot in the layout tables

plans/g2m-devkit-sc.md adds the SC as a new `locRetailSc` layout chosen
in `parseIni`, because the SC comes from the ini. The CB_X comes from the
command line, so it doesn't need a slot in `xb.files[]`: a separate
`struct fileent` in build.c, added at the three places above, keeps
`parseIni` (matched with hints, `-fno-toplevel-reorder`), the `blRetail`
tables, the `xb.files[4]` CB_B test and every `findFile` lookup as they
are. It also leaves the SC plan's `locRetailSc` layout alone, so the two
features combine without either knowing the other's table.

### Glitch2m with an SB (devkit chain)

Two glitch2m layouts put a devkit SB behind the mfg CB_A. In both the SB
sits in the CB_B slot (index 4, type 6), so `xb.cbb` is 1 and every hook
in this plan that keys on type 6 applies to the SB unchanged:

| ini | slots (type) | SD keyed from | today |
|---|---|---|---|
| 6 lines: CB_A, SB, SD, SE, none, none | 5, 6, 7, 8 | the SB (`case 7`, `xb.cbb`) | built by xeBuild |
| 7 lines: CB_A, SB, SC, SD, SE, none, none | 5, 6, 12, 7, 8 (`locRetailSc`) | the SC (plans/g2m-devkit-sc.md step 4) | needs the SC plan |

Going through each step with an SB in the CB_B slot:

- **Loading.** `checkBl(..., 6, ...)` takes the SB (it only checks the `B`).
  `loadCbx` runs after `loadBlFiles`, so it sees the same `xb.cbb`. No
  change.
- **The CB_X's key.** 9188 mfg and the other mfg CB_As have flags bit 0,
  so `cbxEncrypt` uses the zero key, as `cbbEncrypt` already does for the
  SB ("CBB crypto method set to work with mfg CBA").
- **The SB in plaintext.** `cbbStorePlain` runs on whatever `case 6`
  encrypted, so the SB is stored decrypted with its key at +0x10, as
  JRunner's XDKbuild-style path does (its `flashCbb` is the loader after
  the CB_A, here the SB). `e->key` is unchanged, so:
  - 6-line: the SD is keyed from the SB's key exactly as today;
  - 7-line: the SC doesn't use the SB's key at all (`cdEncryptZero`), the
    SD is keyed from the SC and the SE from the SD, as in the SC plan.
- **Order in `encodeBls`.** `case 6` (index 4) runs before the SC (index
  5, `case 12`) and the SD, so the CB_X step in `case 6` is done before
  anything after the SB is encrypted. Nothing after the SB depends on the
  CB_X.
- **Signatures.** `verifyBlSigs` runs before `encodeBls`, while the SB is
  still the plaintext input file; the SC plan's step 7 (SC checked against
  the SB's key at +616) reads the same bytes as without `-cbx`.
- **Layout.** `addBlsToImage` adds the CB_X before type 6, so it lands
  between the CB_A and the SB, and the SC, SD and SE follow at the running
  offset. `calcBlAreaSize` gets both additions: `cbx.size` (step 4 here)
  and the SC's size (the SC plan's step 5).
- **Virtual fuses.** The g2m vfuses (type 24) go at
  `imgCfOffset() + imgCfSize()`, which `calcBlAreaSize` sets after the
  bootloaders, so the CB_X just pushes the patch slots along when it
  crosses a 0x10000 boundary. The SC plan's LDV clearing doesn't look at
  the CB_X.
- **The built-in CB_X.** It only loads the next loader at CB_X + its size
  and jumps to it, so the same `defCbx` works in front of a CB_B or an SB
  (JRunner uses one CB_X for both).

The error when `xb.cbb` is 0 names both: "a CB_X needs a CB_B (or an SB in
the CB_B slot)".

## Matching

As in the other plans: everything sits behind `#ifdef XEBUILD_EXT`, the
default build's preprocessed source must not change, and `sh build.sh` must
still end with
`10dac648197fa5cdbb82d975ab9ff11f64075c9686908dfd9a33edc533f1971c`.
`encodeBls`, `calcBlAreaSize`, `addBlsToImage`, `buildFlash` and
`mode_build` are matched with code-free hints, so add separate `#ifdef`
blocks and `static` helpers rather than reshaping their code. New
functions in src/keys.c go at the end of the file, new data in build.c
after its existing data (after `defCore` and the other tables), all inside
the `#ifdef`. Don't add fields to `xb` (its layout is the original's).

## Changes

### 1. The switches (src/mode_build.c, src/build.h)

In src/build.h:

```c
#ifdef XEBUILD_EXT
/* -cbx: put a CB_X between the CB_A and the CB_B; -cbxfile: a custom one
   instead of the built-in defCbx */
extern int cbxOn;
extern char cbxName[0x400];
#endif
```

In `mode_build`'s argument loop, under `XEBUILD_EXT`, two branches
**before** the `-c` one, `-cbxfile` first (the loop compares prefixes, so
`-c` would take both and `-cbx` would take `-cbxfile`):

```c
		} else if (!strnicmp(argv[i], "-cbxfile", 8)) {
			if (!argv[++i] || i == argc || argv[i][0] == '-') {
				log_printf(0, "\n\n***** ERROR: CB_X file flag -cbxfile on command line but no argument provided!\n");
				build_usage();
			}
			cbxOn = 1;
			strcpy(cbxName, argv[i]);
			log_printf(1, "CB_X from '%s' goes between the CB_A and the CB_B\n", cbxName);
		} else if (!strnicmp(argv[i], "-cbx", 4)) {
			cbxOn = 1;
			log_printf(1, "built-in CB_X goes between the CB_A and the CB_B\n");
```

`-cbx` takes no argument, so it can't swallow the output name. `-cbxfile`
implies `-cbx`; giving both is fine.

After the loop (once `-t` is known), under `XEBUILD_EXT`: if `cbxOn` and
not `xb.type == BUILD_GLITCH && xb.glitch2`, error ("-cbx needs -t glitch2
or glitch2m") and `build_usage()`.

In `build_usage`, under `XEBUILD_EXT`, after the `-8` line:

```
   -cbx     : glitch2/glitch2m: put a CB_X between the CB_A and the CB_B (the CB_B is stored in plaintext)
   -cbxfile <file>: as -cbx, with a custom decrypted CB_X instead of the built-in one
```

Only `mode_build` gets the switches. `mode_update` (`-u`) rewrites only the
CF and CG from the console's own bootloaders (`xb.fromConsole`), so it has
nothing to insert.

### 2. The built-in CB_X and loading (src/build.c)

After the existing build.c data, under `XEBUILD_EXT`:

```c
/* the built-in CB_X, decrypted, nonce zero (-cbx without -cbxfile) */
const uint8_t defCbx[0x400] = {
	...
};

int cbxOn;
char cbxName[0x400];
static struct fileent cbx;
```

`defCbx` is written out like `defCore` (16 bytes a line, hex), from the
decrypted 1024-byte CB_X the user provides; its header size at +12 must be
0x400. A small `tools/bin2c.py <file> <name>` that prints the array keeps
that reproducible; the source file isn't committed unless wanted.

A `static int loadCbx(void)`:

- `!xb.cbb`: error "this console's bl section has no CB_B, a CB_X needs
  a CB_B (or an SB in the CB_B slot)" and fail. (Single-CB glitch2
  sections can't take a CB_X.)
- `cbxName[0]` (`-cbxfile`): load it as given
  (`loadFileCrc(cbxName, &cbx, 1, 1, 0)`: relative to the working
  directory, or absolute), else through
  `loadInputFile(cbxName, &cbx, 1, 0, NULL, 0, 0, 1)` (data dir, then
  common dir, like the bootloaders). Neither found: error. No fallback to
  the built-in: asking for a file that isn't there is a mistake.
- otherwise: `cbx.data = malloc(0x400)`, copy `defCbx`, `cbx.size =
  0x400`, log "using built-in CB_X (0x400 bytes)". It's copied because
  step 3 encrypts in place.
- validate either source as `checkBl` would for a CB_B, without its crc
  (there is no ini crc for it): `(d[0] & 0x43) == 0x43 && d[1] == 'B'`,
  the header size at +12 non-zero, a multiple of 16 and not larger than
  the data. Then set `cbx.size` to the header size (the next loader is
  found at CB_X + header size, so trailing bytes in a file must not be
  written), with a warning if the file was longer.
- zero the nonce, +0x10..+0x20 (step 3 derives the key from it, so the
  output doesn't depend on what a file had there). Leave +0x20 on as
  supplied.
- log `"loaded CB_X %s, version %d (0x%x bytes)\n"` (version at +2;
  "built-in" for the name).

In `buildFlash`, under `XEBUILD_EXT`, after `loadBlFiles`/`verifyBlSigs`
succeed and before `calcBlAreaSize` (which needs the size):

```c
#ifdef XEBUILD_EXT
	if (cbxOn && loadCbx())
		return -1;
#endif
```

### 3. Encrypting (src/keys.c, src/keys.h, src/build.c `encodeBls`)

Two functions at the end of src/keys.c, prototypes in src/keys.h, all under
`XEBUILD_EXT`:

```c
/* a CB_X sits where the CB_B would, so the CB_A derives its key as for a
   CB_B (cbbEncrypt), but it carries no pairing data or per-box hash */
void cbxEncrypt(uint8_t *cbx, uint8_t *cbaKey, uint8_t *cba, uint8_t *key, uint32_t size)
{
	uint16_t flags = getBeU16(cba + 6);
	uint8_t *ck = !(flags & 1) ? xb.cpuKey : zeroKey;
	uint8_t hdr[16];

	if (flags & 0x1000) {
		memcpy(hdr, cba, 16);
		hdr[6] = 0;
		hdr[7] = 0;
		XeCryptHmacSha(cbaKey, 16, cbx + 16, 16, ck, 16, hdr, 16, key, 16);
	} else
		XeCryptHmacSha(cbaKey, 16, cbx + 16, 16, ck, 16, NULL, 0, key, 16);
	XeCryptRc4(key, 16, cbx + 32, size - 32);
}

/* behind a CB_X the CB_B is stored as the CB_A leaves it in memory:
   decrypted, with its key in place of the nonce */
void cbbStorePlain(uint8_t *cbb, uint8_t *key, uint32_t size)
{
	XeCryptRc4(key, 16, cbb + 32, size - 32);
	memcpy(cbb + 16, key, 16);
}
```

`cbxEncrypt` repeats `cbbEncrypt`'s key derivation instead of calling it:
`cbbEncrypt` also writes the pairing, LDV and hash into +0x20..+0x40 and,
when zeropairing, clears the global `pairing` that the CF picks up later.
The CB_X must not change either.

`cbbStorePlain` undoes the RC4 `cbbEncrypt` just did, so the plaintext
keeps everything `cbbEncrypt` wrote (pairing, LDV, per-box hash), as
JRunner's `DecryptCBB` output of an xeBuild image does.

In `encodeBls`, glitch branch, `case 6:`, under `XEBUILD_EXT`, right after
the `cbbEncrypt(...)` call (`j` is the CB_A there):

```c
#ifdef XEBUILD_EXT
			if (cbx.data) {
				log_printf(1, "encoding CB_X size 0x%x\n", cbx.size);
				cbxEncrypt(cbx.data, xb.files[j].key, xb.files[j].data, cbx.key, cbx.size);
				log_printf(1, "storing %s in plaintext behind the CB_X\n", e->name);
				cbbStorePlain(e->data, e->key, e->size);
			}
#endif
```

The CB_A has been encrypted by then (index 3 comes first); its flags at +6
are in the unencrypted header, which is what `cbbEncrypt` already relies
on. `e->key` (the CB_B's key) is unchanged, so `case 7` encrypts the CD
exactly as today, and the CE, CF and CG after it.

Which key the CB_X gets follows from the ini's CB_A: a mfg CB_A
(glitch2m, or 10918 as in the RGH3 ECC) keys it with the zero key; a
retail CB_A (glitch2) keys it with the CPU key, because that's how that
CB_A decrypts whatever follows it. Either way the built-in CB_X is the same
plaintext; only its encryption differs.

### 4. Image layout (src/build.c)

- `calcBlAreaSize`, glitch branch: under `XEBUILD_EXT`, after
  `size += findFileSize(6);`, add `cbx.size`. Without it the patch slot
  position and the xell room check ignore the CB_X.
- `addBlsToImage`: under `XEBUILD_EXT`, after the retail/devkit skip tests
  and before the generic "adding %s" log (so the CB_B's logged offset is
  its real one):

  ```c
  #ifdef XEBUILD_EXT
  		if (type == 6 && xb.cbb && cbx.data) {
  			log_printf(1, "adding CB_X at raw offset 0x%08x len 0x%x (end 0x%x)\n",
  				   off, cbx.size, off + cbx.size);
  			imgAddInt(off, cbx.data, cbx.size, 0, ecc, 1);
  			off += cbx.size;
  		}
  #endif
  ```

  The CB_B, CD and CE then follow at the running offset, as JRunner's
  splice leaves them.
- Overflow check, `buildFlash`, under `XEBUILD_EXT`, right before
  `addBlsToImage()`: a `static uint32_t blChainEnd(void)` that walks
  `xb.files[]` from the CB_A as `addBlsToImage` does (running offset,
  skipping `none` entries and the CB_B slot when `!xb.cbb`, plus
  `cbx.size` before type 6) and stops at the first fixed offset after it
  (xell, type 25, 0x70000). If the end passes that offset: error "CB_X
  doesn't fit before xell". Walking the files, rather than summing types
  5–8, also counts the SC in a 7-line g2m build (type 12), and runs after
  `patchBlsBlmod` has grown the CB_B/SB. The built-in 0x400 bytes won't
  trigger it on any stock layout; a large custom CB_X could.

### 5. Build the variant (build.sh)

Same `sh build.sh ext` switch as plans/header-fixes.md step 2. If that plan
lands first, nothing to add here; otherwise do that step as part of this
one.

### 6. A checker (tools/)

`tools/cbx_check.py <image> <cpukey> <1blkey>`: read the flash header,
remove the ECC, and walk the chain:

- CB_A: key = HMAC(1BL key, +0x10), RC4 from +0x20;
- CB_X: key from the CB_A as above (CB_A flags bit 0 picks the zero key,
  0x1000 adds the header), RC4, magic `?B`; with `--cbx <file>`, compare
  the decrypted CB_X (nonce aside) with that file or with the built-in;
- CB_B or SB: plaintext, `?B` magic, `XBOX_ROM` (or zeros) at 0x392 as
  JRunner checks;
- then by the next loader's magic:
  - `?C` (SC, 7-line g2m): key = HMAC(zero key, SC +0x10), then the SD
    from the SC's key;
  - `?D` (CD, or the SD of a 6-line g2m): key = HMAC(CB_B/SB +0x10,
    +0x10);
  - the CE/SE from the CD/SD's key to `?E`; CF from the 1BL key as today.

The same script with `--inject <cbx.bin>` applies JRunner's transform
*without* replacing the CB_A or the SMC (decrypt the CB_B with the CPU key,
encrypt the CB_X with a zero nonce against the image's CB_A, splice,
re-ECC), for verification step 3.

### 7. Document it

- README.md: in the `XEBUILD_EXT` section, `-cbx` and `-cbxfile`, what the
  image then contains, the errors, and that a custom CB_X is a decrypted
  CB_X taken as is.
- NOTES.md: point to this plan from Status.

## Verification

1. `sh build.sh` (no switch) still ends with the reference SHA256.
2. Ext build without `-cbx`: retail, glitch2, glitch2m and a single-CB
   glitch build match the reference `xeBuild.exe` byte for byte (same
   inputs, `-norandom`).
3. Ext build with `-cbx`, `-norandom`, glitch2 (retail CB_A, real CPU key)
   and glitch2m (mfg CB_A):
   - the log shows "using built-in CB_X", "encoding CB_X", "storing ... in
     plaintext" and `adding CB_X at raw offset 0x...` right after the
     CB_A's end;
   - `tools/cbx_check.py` walks the whole chain and finds the built-in
     CB_X;
   - the same build without `-cbx`, put through `cbx_check.py --inject`
     with the built-in's bytes, matches the `-cbx` image byte for byte;
   - with 10918 as the ini's CB_A and the RGH3 ECC's CB_X decrypted to a
     file: `-cbxfile` against JRunner's real
     `ConvertRgh2ToRgh3(..., patchSMC: false)` on the plain build. They
     should match except the CB_X's nonce, if the ECC's isn't zero.
4. Glitch2m with an SB, `-cbx`, `-norandom`:
   - 6-line ini (CB_A 9188 mfg, SB, SD, SE): the log shows the CB_X added
     right after the CB_A and the SB right after the CB_X; `cbx_check.py`
     walks CB_A > CB_X > SB > SD > SE; the image without `-cbx` through
     `--inject` matches byte for byte (this is JRunner's XDKbuild-style
     path, CB_X before the SB);
   - 7-line ini, once the SC plan is in: `cbx_check.py` walks CB_A > CB_X
     > SB > SC > SD > SE, the SE hash checks against the SD (`+588`), and
     the vfuses' LDV lines are still cleared;
   - in both, everything after the SB matches the build without `-cbx`
     apart from its offset (same keys, same contents).
5. `-cbxfile` with a copy of the built-in gives the same image as `-cbx`.
6. Zeropaired build (CPU key all zeros): the CB_X is keyed with the zero
   key and the CF's pairing is the same as without `-cbx`.
7. Errors: `-cbx` with `-t retail`, `jtag`, `glitch`; a console whose bl
   section has `none` for the CB_B/SB; `-cbxfile` with a missing file, a file
   that isn't `?B`, a header size bigger than the file, a CB_X too large to
   fit before xell.
8. Hardware, if available: the image boots on a glitched console:
   glitch2, glitch2m with a CB_B, and glitch2m with the SB devkit chain
   (to the devkit kernel).

Needs the user's real inputs (the 1024-byte CB_X for `defCbx`, a CPU key,
the bootloaders), which the repo doesn't have.

## Open questions

- **The built-in's bytes.** `defCbx` needs the decrypted CB_X (the user
  has it). Confirm its magic is `?B` (`CB`) and its header size field is
  0x400; if the magic differs, `loadCbx`'s check changes to match.
- **Encrypted input.** `-cbxfile` takes a decrypted CB_X. Accepting an
  encrypted one (or a whole RGH3 ECC, decrypting its CB_A and CB_X as
  JRunner does) would be an extension of `loadCbx`.
- **Pairing data in the CB_X.** The plan leaves +0x20..+0x40 of the CB_X as
  supplied (JRunner does too). If a CB_X ever expects pairing/LDV there,
  as a CB_B does, use `cbbEncrypt`'s writes for it (without touching the
  global `pairing`).
- **Nonce.** The CB_X's nonce is zeroed, so `-norandom` or not, its key
  depends only on the CB_A's key and the CPU key. Using `infoKey1` (the
  CB_B's random nonce) instead would also work but would give the CB_X and
  CB_B the same key.
- **Reading such an image back.** `image_read`, `mode_extract` and
  `buildFlash`'s `checkBootImage` (the `-u` path) expect an encrypted CB_B
  right after the CB_A. Using a CB_X image as `nanddump.bin`, or updating
  it with `-u`, is out of scope here.

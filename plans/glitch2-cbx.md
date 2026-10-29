# Glitch2 / glitch2m with a CB_X between the CB_A and the CB_B

Status: plan only, nothing implemented.

Goal: a new build switch, `-cbx <file>`, makes a glitch2 or glitch2m build
put a CB_X between the CB_A and the CB_B, in one pass:

```
xeBuild -t glitch2 -c jasper -d files -cbx cbx.bin out.bin
```

gives the chain

```
0x8000  CB_A   encrypted as today (1BL key)
        CB_X   encrypted the way a CB_B is (key from the CB_A)
        CB_B   plaintext, its RC4 key at +0x10
        CD     encrypted from the CB_B's key, as today
        CE     as today
```

Today this needs a normal xeBuild image and then a post-build step (JRunner's
`RGH2to3.ConvertRgh2ToRgh3` with `patchSMC = false`: "we're only injecting
the CB_X"). This plan moves that step into xeBuild.

## What JRunner's post-build step does

`J-Runner/Classes/RGH2to3.cs`, reading the bootloaders from the image's
flash header (0x08) on:

1. Takes the CB_A and the CB_X ("rgh3Payload") from an RGH3 ECC file. The
   CB_X is stored there encrypted as a CB_B with the **zero** CPU key.
   If its word at 0x354 is `0x646A0002`, it decrypts it, patches four
   instructions (0x354, 0x368, 0x370, 0x37c), re-encrypts it with the same
   key and zeroes the nonce at +0x10.
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

So, as the request says:

- the CB_X is encrypted like a CB_B: the CB_A derives its key from its own
  key, the CB_X's nonce and a CPU key;
- the real CB_B is stored in plaintext, with its own RC4 key where the nonce
  was (that's how a CB_A leaves a decrypted CB_B in memory, and how the CB_B
  then finds the key it chains the CD from);
- the CD and later stages are encrypted exactly as with an encrypted CB_B:
  the CD's key comes from the CB_B's key, which doesn't change.

Two things JRunner's tool does that this switch should **not** do: it
replaces the image's CB_A with the RGH3 CB_A (here the CB_A stays the one
the ini names, as requested: the CB_X goes *between* the CB_A and the
CB_B), and, with `patchSMC`, the SMC (the SMC stays the per-build
`smc.bin` as usual). See Open questions for both.

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

The CB_X therefore needs: loading, a key from the CB_A (as `cbbEncrypt`
derives it), room in `calcBlAreaSize`, and a place in `addBlsToImage`
right before the CB_B. The CB_B needs its RC4 undone after `cbbEncrypt`
and its key written to +0x10. Nothing after the CB_B changes.

### Why not a new slot in the layout tables

plans/g2m-devkit-sc.md adds the SC as a new `locRetailSc` layout chosen
in `parseIni`, because the SC comes from the ini. The CB_X comes from the
command line, so it doesn't need a slot in `xb.files[]`: a separate
`struct fileent` in build.c, added at the three places above, keeps
`parseIni` (matched with hints, `-fno-toplevel-reorder`), the `blRetail`
tables, the `xb.files[4]` CB_B test and every `findFile` lookup as they
are. It also composes with the SC plan: with the SB in the CB_B slot, the
CB_X goes in front of the SB the same way, which is the XDKbuild-style
chain (CB_A > CB_X > SB > SC > SD > SE) JRunner also handles.

## Matching

As in the other plans: everything sits behind `#ifdef XEBUILD_EXT`, the
default build's preprocessed source must not change, and `sh build.sh` must
still end with
`10dac648197fa5cdbb82d975ab9ff11f64075c9686908dfd9a33edc533f1971c`.
`encodeBls`, `calcBlAreaSize`, `addBlsToImage`, `buildFlash` and
`mode_build` are matched with code-free hints, so add separate `#ifdef`
blocks and `static` helpers rather than reshaping their code. New
functions in src/keys.c go at the end of the file, new state in build.c
after its existing data, all inside the `#ifdef`. Don't add fields to
`xb` (its layout is the original's).

## Changes

### 1. The switch (src/mode_build.c, src/build.h)

In src/build.h:

```c
#ifdef XEBUILD_EXT
/* -cbx: a CB_X to put between the CB_A and the CB_B */
extern char cbxName[0x400];
#endif
```

In `mode_build`'s argument loop, under `XEBUILD_EXT`, a branch **before**
the `-c` one (the loop compares prefixes, so `-c` would take `-cbx`):

```c
		} else if (!strnicmp(argv[i], "-cbx", 4)) {
			if (!argv[++i] || i == argc || argv[i][0] == '-') {
				log_printf(0, "\n\n***** ERROR: CB_X flag -cbx on command line but no argument provided!\n");
				build_usage();
			}
			strcpy(cbxName, argv[i]);
			log_printf(1, "CB_X '%s' goes between the CB_A and the CB_B\n", cbxName);
```

After the loop (once `-t` is known), under `XEBUILD_EXT`: if `cbxName[0]`
and not `xb.type == BUILD_GLITCH && xb.glitch2`, error ("-cbx needs
-t glitch2 or glitch2m") and `build_usage()`.

In `build_usage`, under `XEBUILD_EXT`, after the `-8` line:

```
   -cbx <file>: glitch2/glitch2m: put CB_X <file> between the CB_A and the CB_B (the CB_B is stored in plaintext)
```

Only `mode_build` gets the switch. `mode_update` (`-u`) rewrites only the
CF and CG from the console's own bootloaders (`xb.fromConsole`), so it has
nothing to insert.

### 2. Loading the CB_X (src/build.c)

After the existing build.c data, under `XEBUILD_EXT`:

```c
char cbxName[0x400];
static struct fileent cbx;
```

A `static int loadCbx(void)`:

- `!xb.cbb`: error "this console's bl section has no CB_B, a CB_X needs
  one" and fail. (Single-CB glitch2 sections can't take a CB_X.)
- load `cbxName` as given (`loadFileCrc(cbxName, &cbx, 1, 1, 0)`: relative
  to the working directory, or absolute), else through
  `loadInputFile(cbxName, &cbx, 1, 0, NULL, 0, 0, 1)` (data dir, then
  common dir, like the bootloaders). Neither found: error.
- validate as `checkBl` would for a CB_B, without its crc (there is no ini
  crc for it): `(d[0] & 0x43) == 0x43 && d[1] == 'B'`, the header size at
  +12 non-zero, a multiple of 16 and not larger than the file. Then set
  `cbx.size` to the header size (the next loader is found at CB_X + header
  size, so trailing bytes in the file must not be written), with a warning
  if the file was longer.
- zero the nonce, +0x10..+0x20 (step 3 derives the key from it, so the
  output doesn't depend on what the file had there; JRunner leaves its
  CB_X with a zero nonce). Leave +0x20 on as supplied.
- log `"loaded CB_X %s, version %d (0x%x bytes)\n"` (version at +2).

In `buildFlash`, under `XEBUILD_EXT`, after `loadBlFiles`/`verifyBlSigs`
succeed and before `calcBlAreaSize` (which needs the size):

```c
#ifdef XEBUILD_EXT
	if (cbxName[0] && loadCbx())
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
				log_printf(1, "encoding CB_X %s size 0x%x\n", cbxName, cbx.size);
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

With a mfg CB_A (glitch2m) the CB_X is keyed with the zero key, as
JRunner's RGH3 CB_X is. With a retail CB_A (glitch2) it is keyed with the
CPU key, because that's how that CB_A decrypts whatever follows it.

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
  			log_printf(1, "adding CB_X %s at raw offset 0x%08x len 0x%x (end 0x%x)\n",
  				   cbxName, off, cbx.size, off + cbx.size);
  			imgAddInt(off, cbx.data, cbx.size, 0, ecc, 1);
  			off += cbx.size;
  		}
  #endif
  ```

  The CB_B, CD and CE then follow at the running offset, as JRunner's
  splice leaves them.
- Overflow check, `buildFlash`, under `XEBUILD_EXT`, right before
  `addBlsToImage()`: the bootloaders' end (CB_A offset + CB_X + types 5–8,
  after `patchBlsBlmod` has grown the CB_B) must not pass the xell offset
  (type 25, 0x70000); otherwise error "CB_X doesn't fit before xell".
  xeBuild doesn't check this today because without a CB_X it can't happen;
  a CB_X makes it possible.

### 5. Build the variant (build.sh)

Same `sh build.sh ext` switch as plans/header-fixes.md step 2. If that plan
lands first, nothing to add here; otherwise do that step as part of this
one.

### 6. A checker (tools/)

`tools/cbx_check.py <image> <cpukey> <1blkey>`: read the flash header,
remove the ECC, and walk the chain:

- CB_A: key = HMAC(1BL key, +0x10), RC4 from +0x20;
- CB_X: key from the CB_A as above (CB_A flags bit 0 picks the zero key,
  0x1000 adds the header), RC4, magic `?B`;
- CB_B: plaintext, `?B` magic, `XBOX_ROM` (or zeros) at 0x392 as JRunner
  checks, and its +0x10 equals what `cbbEncrypt` derives (not checkable
  without the nonce, so instead:)
- CD: key = HMAC(CB_B +0x10, CD +0x10) decrypts to `?D`; CE from the CD's
  key to `?E`; CF from the 1BL key as today.

The same script with `--inject <cbx.bin>` applies JRunner's transform
*without* replacing the CB_A or the SMC (decrypt the CB_B with the CPU key,
encrypt the CB_X with a zero nonce, splice, re-ECC), for verification step
3.

### 7. Document it

- README.md: in the `XEBUILD_EXT` section, `-cbx`, what the image then
  contains, the errors, and that the CB_X file is a decrypted CB_X taken as
  is (xeBuild doesn't patch it).
- NOTES.md: point to this plan from Status.

## Verification

1. `sh build.sh` (no switch) still ends with the reference SHA256.
2. Ext build without `-cbx`: retail, glitch2, glitch2m and a single-CB
   glitch build match the reference `xeBuild.exe` byte for byte (same
   inputs, `-norandom`).
3. Ext build with `-cbx`, `-norandom`, glitch2 (retail CB_A, real CPU key)
   and glitch2m (mfg CB_A):
   - the log shows "encoding CB_X", "storing ... in plaintext" and
     `adding CB_X ... at raw offset 0x...` right after the CB_A's end;
   - `tools/cbx_check.py` walks the whole chain;
   - the same build without `-cbx`, put through `cbx_check.py --inject`,
     matches the `-cbx` image byte for byte;
   - if an RGH3 ECC is at hand: build with its CB_A in the ini (`-r`), feed
     the ECC's decrypted CB_X to `-cbx`, and compare against JRunner's real
     `ConvertRgh2ToRgh3(..., patchSMC: false)` on the plain build. They
     should match except the CB_X's nonce, if the ECC's isn't zero.
4. Zeropaired build (CPU key all zeros): the CB_X is keyed with the zero
   key and the CF's pairing is the same as without `-cbx`.
5. Errors: `-cbx` with `-t retail`, `jtag`, `glitch`; a console whose bl
   section has `none` for the CB_B; a missing file; a file that isn't `?B`;
   a header size bigger than the file; a CB_X too large to fit before xell.
6. Hardware, if available: the image boots on a glitched console.

Needs the user's real inputs (a CB_X, a CPU key, the bootloaders), which
the repo doesn't have.

## Open questions

- **Which CB_A.** JRunner swaps the CB_A for the RGH3 ECC's, and the RGH3
  CB_X is encrypted against that CB_A with the zero key. This plan keeps
  the ini's CB_A and encrypts the CB_X against it. If a CB_X only works
  behind a particular CB_A, that's chosen through the ini (`-r`), not by
  the switch. Confirm that's the intended use.
- **CB_X input form.** The plan takes a decrypted CB_X. Accepting an
  encrypted one (or a whole RGH3 ECC, decrypting its CB_A and CB_X as
  JRunner does) would be an extension of `loadCbx`.
- **JRunner's 0x354 fix.** JRunner patches four words of the RGH3 CB_X
  when 0x354 holds `0x646A0002`. This plan doesn't patch the file; it could
  log a warning when it sees that word, if that fix is always wanted.
- **Pairing data in the CB_X.** The plan leaves +0x20..+0x40 of the CB_X as
  supplied (JRunner does too). If a CB_X ever expects pairing/LDV there,
  as a CB_B does, use `cbbEncrypt`'s writes for it (without touching the
  global `pairing`).
- **Nonce.** The CB_X's nonce is zeroed, so `-norandom` or not, its key
  depends only on the CB_A's key and the CPU key. Using `infoKey1` (the
  CB_B's random nonce) instead would also work but would give the CB_X and
  CB_B the same key.
- **The SMC.** `patchSMC` in JRunner swaps in the RGH3 SMC. Not part of
  `-cbx`; the per-build `smc.bin` is used as usual.
- **Reading such an image back.** `image_read`, `mode_extract` and
  `mode_update`'s `checkBootImage` expect an encrypted CB_B right after the
  CB_A. Using a CB_X image as `nanddump.bin`, or updating it with `-u`, is
  out of scope here.

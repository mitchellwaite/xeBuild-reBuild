# CB LDV for retail CE 1888 images without patch slots

Status: plan only, nothing implemented.

Goal: when xeBuild builds a **retail** image with a **CE 1888** and **no
patch slots** (no CF/CG), the CB's LDV byte holds the console's real LDV
(the `cfldv` passed in, or the one found in the input dump). It has to be
in place before the per-box hash is computed and the CB is encrypted. If
xeBuild can't find the real LDV, the build stops: the CB's LDV has to
match the CPU's fuses or the console won't boot, so guessing is no use.

The trigger is the CE alone. Only a CE 1888 with no patch slots needs
this. There are no public CE binaries that boot with a stock CB/CD this
way, and SE dev kernels don't boot with a stock CD. Any CB/CD that comes
with a CE 1888 is covered.

## How the CB is encrypted today

Retail builds go through `encodeBls` (src/build.c), the last branch
(`xb.type <= BUILD_GLITCH`). Retail file types (`locRetail`,
src/filelist_ini.c): 5 CB (CB_A), 6 CB_B, 7 CD, 8 CE, 9 CF, 10 CG.

- type 5: single CB (`!xb.cbb`): `cbaEncrypt(salt, ..., 0)`. With
  `xb.cbb`: `cbaEncrypt(salt, ..., 1)`, which writes no pairing and no LDV.
- type 6 (only with `xb.cbb`): `cbbEncrypt(..., zero)`.
- type 7: `cdEncryptCpu` (single CB) or `cdEncrypt` (CB_B key).
- type 8: `ceEncrypt`.
- types 9/10: skipped, like every entry whose name is `none` with no crc.
  `loadBlFiles` doesn't load them either, so their `data` is NULL.

`cbaEncrypt` (src/keys.c), single CB, does this in order:

1. `cb[0x10..0x1f]` = `infoKey0`; RC4 key = HMAC(1BL key, `cb[0x10..0x1f]`).
2. `cb[0x20..0x22]` = `pairing`, **`cb[0x23]` = `xb.cbLdv`**.
3. Per-box hash: `cb[0x30..0x3f]` = HMAC(CPU key; RC4 key, `cb[0x20..0x2f]`,
   salt). The LDV byte is inside the hashed 16 bytes.
4. RC4 over `cb[0x20..]`.

`cbbEncrypt` does the same for the CB_B: `cbb[0x23] = xb.cbLdv`, then the
per-box hash (unless the CB_A is a mfg one, flag bit 0), then RC4. A zero
CPU key takes its zeropair path and writes no LDV.

So the slot for the LDV already exists. Whatever is in `xb.cbLdv` when
these run ends up in the header and in the hash. But **nothing ever
assigns `xb.cbLdv`** (src/xebuild.h, offset 0x74). It is .bss, so every CB
xeBuild writes has LDV 0. The real value is in `xb.cfLdv` (the next byte).

## Where `xb.cfLdv` comes from, and where it is guessed

| Source | Where | Notes |
|---|---|---|
| `cfldv=` on the command line | `options.c` | 1..32; `cfldv=0` is rejected |
| `cfldv` in options.ini | `options.c`, only if still 0 | capped at 32 |
| input dump's CF | `getImageLdv` (src/image_read.c), only if still 0 | `cfBestPairing` |
| input dump's CB | `getImageLdv`, fallback | **LDV masked off**, see below |
| **guess 1** | `getImageLdv`, when neither decrypts | "could not find a non-zero CF LDV, setting it to 1" |
| **guess 1** | `buildImage` (src/image_write.c), if 0 and the CPU key isn't zero | "cfldv was not set anywhere" |

All of this happens before `buildImage` calls `buildFlash`, which calls
`encodeBls`. That covers `mode_build` and `mode_update`, since both go
through `buildImage`.

For a dump with no patch slots, `getImageLdv` finds no CF and falls back
to `cbGetPairing` (src/bootloaders.c). That decrypts the CB but masks off
the LDV (`getBeU32(buf + 32) & 0xffffff00`). The pairing gets set, but
`xb.cfLdv` stays 0, and `buildImage` turns that into the guessed 1. So
today the dump's real LDV, in its CB's byte 0x23, is thrown away.

`xb.cfLdv == 0` can't tell "not set" apart from "LDV 0". An LDV of 0 is
real: a console whose LDV fuses were never blown. The dump's CB can say 0,
so the plan tracks where the value came from instead of testing for 0.

## Matching

`sh build.sh` must keep producing the reference SHA256. As in
plans/xenon64.md and plans/header-fixes.md, every change sits behind
`#ifdef XEBUILD_EXT`, and the default build doesn't define it. `encodeBls`,
`getImageLdv`, `buildImage` and the option parsers are matched through
code-free hints, so keep the new code in separate `#ifdef` blocks or
`static` helpers and don't reshape the code around them. The default
build's preprocessed source has to stay exactly the same.

## Changes

### 1. Track where the LDV came from (options.c, options.h)

An ext-only global, defined in src/options.c and declared in
src/options.h:

```c
#ifdef XEBUILD_EXT
/* where xb.cfLdv came from; LDV_NONE also covers the guessed 1 */
enum { LDV_NONE, LDV_OPTION, LDV_DUMP };
extern int ldvFrom;
#endif
```

Set `ldvFrom = LDV_OPTION` in the two places options.c stores a value
into `xb.cfLdv`: the command line `cfldv` (after its checks) and the
options.ini read (only if the value it read isn't 0).

### 2. Keep the dump's LDV, including 0 (bootloaders.c, image_read.c)

- `cbGetPairing`: under `XEBUILD_EXT`, return `getBeU32(buf + 32)` without
  the mask, so the low byte is the CB's LDV. Its only caller is
  `getImageLdv`.
- `getImageLdv`, under `XEBUILD_EXT`:
  - When `xb.cfLdv` is still 0 and the CF or the CB decrypted (`pairing`
    nonzero), take its low byte as today (capped at 32) and set
    `ldvFrom = LDV_DUMP`. This now includes a CB with LDV 0, which leaves
    `xb.cfLdv` 0 but known.
  - Log the CB case as its own source, e.g.
    `"setting LDV from image CB to %d\n"`.
  - The "setting it to 1" branch doesn't change `ldvFrom` (still
    `LDV_NONE`).

### 3. Don't turn a known 0 into 1 (image_write.c)

In `buildImage`, the "cfldv was not set anywhere" fallback: under
`XEBUILD_EXT`, skip it when `ldvFrom != LDV_NONE`. That way a dump CB with
LDV 0 stays 0. Builds with no known LDV still get the guessed 1 and the
warning, as today. Step 4 then refuses them in the CE 1888 case.

### 4. Detect the case and set the LDV (src/build.c)

A `static` helper under `XEBUILD_EXT`, next to `findFileN`:

```c
#ifdef XEBUILD_EXT
/* retail CE 1888 with no CF/CG: the CB carries the LDV */
static int cbCarriesLdv(void)
{
	struct fileent *e;
	int i, j;

	if (xb.type != BUILD_RETAIL || xb.seReplacesCf)
		return 0;
	j = findFile(8);
	if (!j || !xb.files[j].data || getBeU16(xb.files[j].data + 2) != 1888)
		return 0;
	for (i = 9; i <= 10; i++) {
		j = findFile(i);
		e = &xb.files[j];
		if (j && e->data && (strnicmp(e->name, "none", 4) || e->crc))
			return 0;
	}
	return 1;
}
#endif
```

At the top of `encodeBls`, before the loop:

```c
#ifdef XEBUILD_EXT
	if (cbCarriesLdv()) {
		if (ldvFrom == LDV_NONE) {
			log_printf(0, "\n******* ERROR: CE 1888 with no patch slots: the CB needs the console's LDV,"
				" set cfldv or use a nanddump.bin, cannot proceed!\n\n");
			return 1;
		}
		xb.cbLdv = xb.cfLdv;
		log_printf(1, "no patch slots, CB LDV set to %d\n", xb.cbLdv);
	}
#endif
```

Notes:

- Setting `xb.cbLdv` once, before the loop, reaches `cbaEncrypt` (single
  CB) and `cbbEncrypt` (the CB_B on `xb.cbb` consoles) whatever order the
  files come in. Both write it before their per-box hash and RC4, which is
  the order asked for. No change to src/keys.c.
- The CE's build number at offset 2 is in the plaintext part of the
  header.
- `findFile` returns 0 when a type is missing, which counts as no CF/CG.
- `xb.seReplacesCf` (an SE loaded where the CF goes) is a dev-kernel setup. It
  also renames type 9 to 14, so without the `seReplacesCf` test it would look like
  "no CF".
- Returning 1 from `encodeBls` makes `buildFlash` return -4 before
  anything is written.
- Optional: show it in `main.c`'s summary next to `CF LDV`, under the same
  `#ifdef`.

### 5. Build the variant (build.sh)

Same switch as plans/header-fixes.md step 2 (`sh build.sh ext`, adds
`-DXEBUILD_EXT`, writes to `build/ext/`, skips the SHA256 check). If that
plan lands first, nothing to add here; otherwise do that step as part of
this one.

### 6. Document it

- README.md: add a line to the `XEBUILD_EXT` section, including the new
  error and that `cfldv` (or a dump) is required for a CE 1888 image
  without patch slots.
- NOTES.md: point to this plan from Status.

## Verification

1. `sh build.sh` (no switch) still ends with
   `10dac648197fa5cdbb82d975ab9ff11f64075c9686908dfd9a33edc533f1971c`.
2. Ext build, retail filelist with a CE 1888 and CF/CG set to `none`, CPU
   key, `cfldv=N`:
   - the log shows `no patch slots, CB LDV set to N`;
   - feed the output back as `nanddump.bin` to `build/ext/xeBuild.exe`:
     "setting LDV from image CB to N";
   - a small script in `tools/`: decrypt the CB (or CB_B) with the 1BL
     key / CB_A key, check byte 0x23 == N, and recompute HMAC(CPU key; RC4
     key, bytes 0x20..0x2f, zero salt) against 0x30..0x3f.
   Do this for a single-CB console and an `xb.cbb` one.
3. Same inputs without `cfldv` and without a dump: the build stops with
   the new error. The guessed 1 never reaches the CB.
4. From a real dump with no patch slots, no `cfldv`: the CB LDV equals the
   dump's CB byte 0x23, including a dump whose byte is 0.
5. Controls that must match the reference `xeBuild.exe` byte for byte
   (same inputs, random keys off): retail with a CF/CG, a CE newer than
   1888, a glitch build, a JTAG build.
6. Hardware, if available: the ext image boots on the console the LDV
   came from.

Needs real inputs (a CE 1888 + bootloaders, a CPU key, ideally a matching
dump), which the repo doesn't have.

## Open questions

- **Steps 2–3 go beyond this case.** Once the dump's CB LDV is kept, a
  dump with no readable CF gives its CB LDV to every build from it,
  including one that adds a CF. A CB LDV of 0 then also skips the guessed
  1 for that CF. That should be closer to the CPU than the guess, but it
  changes output outside the CE 1888 case. To keep it narrow instead,
  store the dump's CB byte in its own ext-only global and use it only in
  step 4, leaving `xb.cfLdv` and the fallback as they are.
- **`cfldv=0` is still rejected** on the command line. A console with LDV 0
  can only be built from its dump. If that should also work from just a
  CPU key, accept `cfldv=0` under `XEBUILD_EXT` (it sets
  `ldvFrom = LDV_OPTION`).
- **Glitch builds** with a CE 1888 use `cbaEncryptZero`, so there's no LDV
  to set. Out of scope.
- **Client mode (`xb.fromConsole`)** uses `encodeUpdateBls` and the
  console's own CB, so step 4 doesn't reach it, by design.

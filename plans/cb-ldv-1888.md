# CB LDV for retail 1888 images without patch slots

Status: plan only, nothing implemented.

Goal: when xeBuild builds a **retail** image whose bootloaders are a single
CB, CD and CE at build **1888** and that has **no patch slots** (no CF/CG),
the CB's LDV byte holds the console's LDV (the `cfldv` passed in, or the
one found in the input dump), and is in place before the per-box hash is
computed and the CB is encrypted.

## How the CB is encrypted today

Retail builds go through `encodeBls` (src/build.c), the last branch
(`xb.type <= BUILD_GLITCH`). For a single-CB console (`!xb.cbb`):

- type 5 (CB): `cbaEncrypt(salt, e->data, e->key, e->size, 0)`
- type 7 (CD): `cdEncryptCpu` (CB key, then the CPU key)
- type 8 (CE): `ceEncrypt` (CD key)
- types 9/10 (CF/CG): skipped, like every entry whose name is `none` with
  no crc (`!strnicmp(e->name, "none", 4) && !e->crc`). `loadBlFiles` never
  loads them either, so their `data` is NULL.

`cbaEncrypt` (src/keys.c) does, in this order:

1. `cb[0x10..0x1f]` = `infoKey0`; RC4 key = HMAC(1BL key, `cb[0x10..0x1f]`).
2. `cb[0x20..0x22]` = `pairing`, **`cb[0x23]` = `xb.cbLdv`**.
3. Per-box hash: `cb[0x30..0x3f]` = HMAC(CPU key; RC4 key, `cb[0x20..0x2f]`,
   salt). The LDV byte is inside the hashed 16 bytes.
4. RC4 over `cb[0x20..]`.

So the right place for the LDV already exists: whatever is in `xb.cbLdv`
when `cbaEncrypt` runs ends up in the header and in the hash. But
**nothing ever assigns `xb.cbLdv`** (src/xebuild.h, offset 0x74). It is
.bss, so every CB xeBuild writes has LDV 0. `cbaEncrypt2` and `cbbEncrypt`
read it the same way. `xb.cfLdv` (the next byte) is the value that the
options, the dump reader and the build fallback all fill.

`xb.cfLdv` is final before `encodeBls` runs:

| Source | Where | Precedence |
|---|---|---|
| `cfldv=` on the command line | `options.c` (capped at 32) | 1 |
| `cfldv` in options.ini | `options.c`, only if still 0 | 2 |
| input dump (`nanddump.bin`) | `getImageLdv` (src/image_read.c), only if still 0 | 3 |
| fallback 1 + warning | `buildImage` (src/image_write.c), if 0 and the CPU key isn't zero | 4 |

`buildImage` then calls `buildFlash`, which calls `encodeBls`. That covers
both `mode_build` and `mode_update`, since both go through `buildImage`.

## Problem with "determined from the input flash image"

For an 1888 dump with no patch slots, `getImageLdv` finds no CF
(`cfBestPairing` returns 0) and falls back to `cbGetPairing`
(src/bootloaders.c). That decrypts the dump's CB but **masks off the LDV**:
`getBeU32(buf + 32) & 0xffffff00`. The pairing gets set, but
`ldv = pairing` has a 0 low byte, so `xb.cfLdv` stays 0 and `buildImage`
then forces it to 1 with the "cfldv was not set anywhere" warning. In that
case the dump's own LDV, which is in the CB's byte 0x23, is lost.

## Matching

`sh build.sh` must keep producing the reference SHA256. As in
plans/xenon64.md and plans/header-fixes.md, every change sits behind
`#ifdef XEBUILD_EXT`, and the default build doesn't define it. Several of
the touched functions are matched through code-free hints (`encodeBls`
lives in build.c; `getImageLdv` in image_read.c). Keep the new code in
separate `#ifdef` blocks or `static` helpers, and don't reshape the
existing code around them, so the preprocessed default source stays
byte-for-byte the same.

## Changes

### 1. Detect the scenario (src/build.c)

A `static` helper under `XEBUILD_EXT`, next to `findFileN`:

```c
#ifdef XEBUILD_EXT
/* retail, single CB, CB/CD/CE 1888 and no CF/CG: the CB carries the LDV */
static int cbCarriesLdv(void)
{
	static const int bl[] = { 5, 7, 8 };
	struct fileent *e;
	int i, j;

	if (xb.type != BUILD_RETAIL || xb.cbb || xb.f01c)
		return 0;
	for (i = 0; i < 3; i++) {
		j = findFile(bl[i]);
		if (!j || !xb.files[j].data || getBeU16(xb.files[j].data + 2) != 1888)
			return 0;
	}
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

Notes:

- The build number at offset 2 is in the plaintext part of the header, so
  it doesn't matter whether CD/CE were already encoded when this runs.
- `findFile` returns 0 when the type is missing. Treat that as absent
  for CF/CG and as "not this scenario" for CB/CD/CE.
- `xb.f01c` (an SE where the CF goes) clears `xb.cfLdv` on purpose; leave
  that path alone.
- `xb.cbb` consoles (CB_A/CB_B) never have an 1888 CB. The check is there
  so `cbbEncrypt`'s use of `xb.cbLdv` can't change by accident.

### 2. Set the LDV before the CB is encrypted (src/build.c)

In `encodeBls`, retail/glitch branch, `case 5`, just before the
`cbaEncrypt(salt, e->data, e->key, e->size, 0)` call (the `xb.type ==
BUILD_RETAIL` arm):

```c
#ifdef XEBUILD_EXT
				if (cbCarriesLdv()) {
					xb.cbLdv = xb.cfLdv;
					log_printf(1, "no patch slots, CB LDV set to %d\n", xb.cbLdv);
				}
#endif
```

`cbaEncrypt` then writes it to `cb[0x23]` before the per-box HMAC and the
RC4, which is the order the request asks for. No change to src/keys.c.

Set `xb.cbLdv` (not `cb[35]` directly) so the value stays in one place and
`main.c`'s summary can show it if wanted (optional: add a
`log_printf(0, "CB LDV    : %d\n", xb.cbLdv)` next to the existing
`CF LDV` line, under the same `#ifdef`).

### 3. Keep the dump's CB LDV (src/bootloaders.c, src/image_read.c)

So that "determined from the input flash image" works for a dump with no
CF:

- `cbGetPairing`: under `XEBUILD_EXT`, return `getBeU32(buf + 32)` without
  the `& 0xffffff00`, so the low byte is the CB's LDV. Its only caller is
  `getImageLdv`, which already treats the low byte as the LDV and the top
  24 bits as the pairing (`setPairing(pairing >> 8)`, `ldv = pairing`,
  cap at 32).
- `getImageLdv`: under `XEBUILD_EXT`, change the log in the CB-fallback
  case so it says the LDV came from the CB, e.g.
  `"setting LDV from image CB to %d\n"`.

Precedence stays the same: command line > options.ini > the dump's CF >
the dump's CB > fallback 1.

### 4. Build the variant (build.sh)

Same switch as plans/header-fixes.md step 2 (`sh build.sh ext`, adds
`-DXEBUILD_EXT`, writes to `build/ext/`, skips the SHA256 check). If that
plan lands first, nothing to add here; otherwise do that step as part of
this one.

### 5. Document it

- README.md: add a line to the `XEBUILD_EXT` section.
- NOTES.md: point to this plan from Status.

## Verification

1. `sh build.sh` (no switch) still ends with
   `10dac648197fa5cdbb82d975ab9ff11f64075c9686908dfd9a33edc533f1971c`.
2. Self-check with the ext build, using an 1888 retail filelist with
   CF/CG set to `none`, a CPU key and `cfldv=N`:
   - the log shows `no patch slots, CB LDV set to N`;
   - feed the output back as `nanddump.bin` to `build/ext/xeBuild.exe`:
     `cbGetPairing`'s "pairing bytes extracted as" log ends in `N` and
     "setting LDV from image CB to N" follows;
   - a small script in `tools/` (or by hand): decrypt the CB with the 1BL
     key, check `cb[0x23] == N`, and recompute HMAC(CPU key; RC4 key,
     `cb[0x20..0x2f]`, zero salt) against `cb[0x30..0x3f]`.
3. Same as 2 but without `cfldv=`, from a real 1888 dump: the CB LDV
   equals the dump's CB byte 0x23, and the "cfldv was not set anywhere"
   warning is gone.
4. Controls that must match the reference `xeBuild.exe` byte for byte
   (same inputs, same `-r`/random keys off): retail with a CF/CG, retail
   with a 1888 CB but a newer CD/CE, a glitch build, a Jasper/Trinity
   (CB_A/CB_B) retail build.
5. Hardware, if available: a fat console that was never updated past 1888
   (or one whose CF LDV fuses match) boots the ext image.

Needs real inputs (an 1888 dump or 1888 bootloaders + a CPU key), which
the repo doesn't have.

## Open questions

- **Fallback 1.** With no `cfldv` and no LDV in the dump, `buildImage`
  sets `xb.cfLdv = 1` with a warning, and the plan copies that into the
  CB. Alternatively, in this scenario, error out and ask for `cfldv`.
  A wrong CB LDV keeps the box from booting just as a wrong CF LDV would.
- **Step 3 reaches further than the scenario.** Once the CB's byte is
  kept, a dump with no readable CF gives its CB LDV to every build from
  it, including one that adds a CF (the CF's LDV, `cf->data[543]`, then
  comes from the CB instead of being forced to 1). That's probably more
  correct than 1, but it is a behaviour change outside the 1888 case. To
  keep it narrow instead, store the dump's CB byte in a new ext-only
  global and use it only in step 2 when `xb.cfLdv` came from the
  fallback.
- **Which builds count.** The plan checks exactly 1888 for CB, CD and CE,
  as asked. If other pre-CF base builds should be covered, widen the
  test in `cbCarriesLdv` (e.g. by CB build only).
- **Glitch builds.** A glitch image with 1888 bootloaders and no patch
  slots uses `cbaEncryptZero`, so there's no LDV to set; out of scope.
- **Client mode (`xb.fromConsole`).** It uses `encodeUpdateBls` and the
  console's own CB, so step 2 doesn't reach it, by design.

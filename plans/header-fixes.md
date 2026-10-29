# Flash header fixes (patch slot size, KV size)

Status: plan only, nothing implemented.

Goal: images come out of xeBuild with the two header fields that JRunner's
`fixBuggyXeBuildImage` repairs afterwards already correct, so that
post-processing step is no longer needed.

## What JRunner does

After xeBuild, JRunner reads page 0 of the image (removing ECC if present),
and in the flash header (`struct flashhdr`, src/xebuild.h, big endian):

- `patchSlotSize` (0x70): if 0, sets it to 0x10000.
- `kvSize` (0x60): if 0, sets it to 0x4000 (a retail KV).

Then it adds the ECC back and writes the image out. Both rules apply to any
image where the field is 0, whatever the console or build type.

Its comment calls the second field the "KV offset". It is the size:
`kvAddr` (0x6c) is already 0x4000 in every template.

## Where the zeros come from

`buildImage` (src/image_write.c) fills `hdrTemplate`. It `memset`s it to
0 first, and the constants are stored byte-swapped (`0x100` is 0x10000 on
disk, `0x400000` is 0x4000). `patchSlotSize` is set only in some cases:

| Build type | Console | `patchSlotSize` | `kvSize` |
|---|---|---|---|
| retail, glitch, devgl, devgl16 | xenon, zephyr | **0** | **0** (set to 0 on purpose) |
| | falcon | **0** | 0x4000 |
| | jaspersb (XSB, no BB controller) | **0** | 0x4000 |
| | jasper, jasperbc (BB controller) | 0x10000 | 0x4000 |
| | jasper big block | 0x20000 | 0x4000 |
| | trinity, corona, winchester | 0x10000 | 0x4000 |
| jtag | xenon, zephyr | **0** | **0** |
| | falcon | **0** | 0x4000 |
| | jaspersb | **0** | 0x4000 |
| | jasper BB controller / big block | 0x10000 | 0x4000 |
| devkit, devkit16, testkit, testkit16 | all | 0x10000 / 0x20000 (big block) | xenon/zephyr **0**, else 0x8000 for testkit types, 0x4000 for the rest |

The bold cells are what JRunner patches.

There's supporting evidence in xeBuild itself. When it reads a dump it
already falls back to the same values: `getImageLdv` (src/image_read.c) uses
0x10000 when `patchSlotSize` is 0, and `getImageKv` uses 0x4000 when `kvSize`
is not 0x4000 or 0x8000. The CF/CG slot size limit in src/build.c
(`max = xb.cbb ? 0xc000 : 0x10000`) also matches a 0x10000 patch slot.

Nothing else reads `hdrTemplate.patchSlotSize` or `kvSize` while building:
they are written to page 0 by `writeInitialHeader` and nothing else. So
changing them changes only those 8 bytes and page 0's ECC.

## Matching

`sh build.sh` must keep producing the reference SHA256, so this follows
plans/xenon64.md: every change sits behind `#ifdef XEBUILD_EXT`, the
default build doesn't define it, and the preprocessor drops the new code.
Use the same switch name, so all behaviour changes build as one variant.

## Changes

### 1. Fill the zero fields in the template (src/image_write.c)

At the end of `buildImage`'s template setup, just before
`memcpy(hdrTemplate.copyright, ...)`, apply JRunner's rule at the source:

```c
#ifdef XEBUILD_EXT
	/* the 2BL/4BL panic on a zero patch slot size (falcon, jaspersb and the
	   fat consoles); XeLL needs the KV size to find the KV (xenon, zephyr) */
	if (!hdrTemplate.patchSlotSize)
		hdrTemplate.patchSlotSize = 0x100;	/* 0x10000 */
	if (!hdrTemplate.kvSize)
		hdrTemplate.kvSize = 0x400000;	/* 0x4000 */
#endif
```

This covers every row in the table at once, JTAG included, which is what
JRunner does. ECC needs no special handling: `calcPageEcc` runs over
`xb.hdr` when the raw image is put together (src/image_write.c, "calculating
ECD bytes"), after the header is in place. MMC images have no spare.

Why here rather than rewriting the finished image the way JRunner does:
one place, no un-ECC/re-ECC, and the log and every later step already see
the corrected header.

### 2. Build the variant (build.sh)

Add a switch, e.g. `sh build.sh ext`, that:

- adds `-DXEBUILD_EXT` to every object's `cflags`,
- writes to its own directory (`build/ext/`, exe `build/ext/xeBuild.exe`)
  so the matching objects in `build/obj/` aren't touched,
- skips `execmp.py`/SHA256 and prints the exe's path instead.

Objects compiled with a profile (`prof=`/`fprof=`) may print
coverage-mismatch warnings in this variant. That's harmless, because only
byte matching depends on the profiles.

### 3. Document it

- README.md: a short section on `XEBUILD_EXT` and what it changes.
- NOTES.md: point to this plan from Status.

## Verification

1. `sh build.sh` (no switch) still ends with
   `10dac648197fa5cdbb82d975ab9ff11f64075c9686908dfd9a33edc533f1971c`.
2. Differential test against JRunner, per console/build pair in the bold
   rows (at least falcon glitch2, jaspersb glitch2, xenon glitch2,
   xenon jtag, plus one control that should not change, e.g. trinity):
   - build with the reference `xeBuild.exe`, then run JRunner's
     `fixBuggyXeBuildImage` (or a small Python port of it in
     `tools/`) on the result;
   - build the same inputs with `build/ext/xeBuild.exe`;
   - the two images must be byte-identical. Compared with the unpatched
     reference output, only 0x60..0x63, 0x70..0x73 and page 0's spare
     bytes may differ.
   This needs real inputs (a dump or CPU key plus the usual xeBuild
   `data/` files), which the repo doesn't have.
3. Hardware, if available: a Falcon or Jasper XSB boots the ext image
   without the 2BL/4BL panic, and XeLL on a Xenon shows the DVD key and
   serial.

## Open questions

- **Kit builds on xenon/zephyr.** JRunner writes 0x4000 into a zero
  `kvSize` regardless of build type. Testkit types use 0x8000 on the other
  consoles. The plan copies JRunner. If testkit Xenons should get 0x8000,
  fill `kvSize` with the template's own value for that build type
  (`xb.type - BUILD_TESTKIT < 2 ? 0x800000 : 0x400000`) instead.
- **Why xenon/zephyr get `kvSize = 0`.** The original sets it on purpose,
  probably to copy factory Xenon headers. The plan treats JRunner's track
  record as evidence that 0x4000 is safe for the bootloaders.
- **Client mode (`xb.fromConsole`).** That path copies the console's own
  bootloader area, header included (`checkBootImage(1)`), not
  `hdrTemplate`, so step 1 doesn't reach it. JRunner would still patch that
  output. `checkBootImage` finds the CB at `kvAddr + kvSize`, though. If it
  is ever fixed for this path, it has to patch the copy written to the image
  after that lookup, not `xb.bl.data` before it.

## Not in scope (seen on the way)

- JTAG big block Jasper gets `patchSlotSize` 0x10000 while the non-JTAG big
  block Jasper gets 0x20000. JRunner doesn't touch it, so it's left alone
  until a big block JTAG dump settles which one is right.

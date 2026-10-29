# 64MiB images for Xenon, Zephyr and Falcon

Status: plan only, nothing implemented.

Goal: new console types `xenon64`, `zephyr64` and `falcon64` that build a
64MiB small block image (0x4200000 raw) instead of the 16MiB one, for any
build type.

## How sizing works today

`buildImage` (src/image_write.c) picks the NAND layout in this order:

1. `NAND_BIG_BLOCK`: 64MiB big block. No Xenon/Zephyr/Falcon name sets it.
2. Not `BUILD_DEVKIT`/`BUILD_TESTKIT`: 48MiB if `NAND_MMC`, else 16MiB
   (0x1080000 raw, 0x400 blocks).
3. Otherwise (devkit, testkit): 64MiB small block: 0x4200000 raw, 0x4000000
   user, 0x1000 blocks, FS 0..0xf7c, SMC config at 0x3dfc000.

So the 64MiB small block layout already exists, but only the devkit and
testkit build types reach it. The plan ties it to a console flag as well.

## Matching

Any behaviour change moves `sh build.sh` off the reference SHA256. Put the
whole feature behind a compile-time switch (e.g. `#ifdef XEBUILD_EXT`) so
the default build stays byte-identical, or keep it on its own branch.

## Changes

### 1. Flag bit and helper (src/xebuild.h)

Bits 3..27 of `xb.flags` are unused.

```c
#define NAND_SMALL_64M 0x08000000	/* 64MiB small block NAND on a non-kit build */
#define IS_64M_SMALL (xb.type == BUILD_DEVKIT || xb.type == BUILD_TESTKIT || \
		      (xb.flags & NAND_SMALL_64M))
```

The low 3 bits stay `CONSOLE_XENON`/`ZEPHYR`/`FALCON`, so console type
tests, `IS_SLIM` and the `consoleNames[]` ini lookups are unaffected
(xenon64 uses xenon's ini sections).

### 2. Names (src/options.c)

Add `xenon64`, `zephyr64`, `falcon64` to `setConsoleType` and to
`iniConsoleType` (perbox files). Each sets `NAND_SMALL_64M | CONSOLE_x` and
appends the name to `xb.outName`.

### 3. Size checks that are spelled as devkit/testkit

Replace with `IS_64M_SMALL`:

- `buildImage` (src/image_write.c): the
  `xb.type != BUILD_DEVKIT && xb.type != BUILD_TESTKIT` branch test.
- Bad block remap range (src/image_write.c, the `blocks = xb.type ==
  BUILD_DEVKIT || ...` line): 0x1000 blocks instead of 0x400.
- `showConsoleInfo` NAND size line (src/main.c): prints
  "64MiB (small block)".
- Mobile file offsets (src/build.c, the `statisticsOffset` /
  `manufacturingOffset` calls): the `big` argument is currently
  `xb.type > BUILD_DEVGL16`.

### 4. Reserved FS blocks (open question)

`fixupEmptyFsBlocks` (src/image_write.c) marks blocks after `fsEnd` as
0x1ffb:

- 16MiB non-kit: 4 blocks (0x3dc..0x3df, ending at the SMC config block),
  leaving 0x3e0..0x3ff for remapping.
- Kits: every block up to `xb.blocks` (0x84 on 64MiB).

The 64MiB analogue of the non-kit rule is 4 blocks (0xf7c..0xf7f, SMC
config at block 0xf7f), leaving 0xf80..0xfff for remapping. Compare the FS
table of a real 64MiB Xenon/Zephyr/Falcon dump to decide.

### 5. Detection from existing data

- Dump reading (src/image_read.c): the `statisticsOffset` /
  `manufacturingOffset` calls pass `big = 0`. Pass "not big block, not
  MMC, `dumpSize == 0x4000000`".
- Client mode: `showImageType` (src/consoleinfo.c) only adds a suffix for
  its cases 4 and 5. Add `"64"` for Xenon/Zephyr/Falcon when `nandSize` is
  0x4200000, so its `setConsoleType(type)` gets `xenon64` etc.
- Update mode: not traced yet. If `mode_update` guesses the console type
  from the dump, it needs the same rule.

## Not expected to change

- Header template: `cbOffset`, `kvSize` (and the Xenon/Zephyr
  `kvSize = 0`) depend on build type and console, not NAND size.
- SMC config position: follows `xb.smcConfigOffset`.
- Bootloaders: the fat consoles are believed to take the NAND geometry from
  the flash controller rather than the image. Only a real 64MiB board can
  confirm this.

## Existing bugs found on the way

These are in the original and worth fixing whether or not this feature
lands (also behind the switch):

- src/build.c passes `xb.type > BUILD_DEVGL16` as the 64MiB flag for the
  Statistics.settings / Manufacturing.data offsets. That includes devkit16
  and testkit16, which are 16MiB, so they get 0x3df8000-range offsets past
  the end of their 0x1000000-byte image.
- src/image_read.c always passes 0 for that flag when reading a dump, so a
  64MiB small block dump (devkits included) is searched at the 16MiB
  offsets.

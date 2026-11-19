# 64MiB small block images for Xenon, Zephyr, Falcon and Jasper

Status: plan only, nothing implemented.

Goal: new console types `xenon64`, `zephyr64`, `falcon64` and `jaspersb64`
that build a 64MiB small block image (`NAND_RAW_64M`, 0x4200000 raw)
instead of the 16MiB one, for any build type. `jaspersb64` is `jaspersb`
(a Jasper with an XSB SMC: small block controller, no
`NAND_BB_CONTROLLER`) on a 64MiB small block NAND.

## How sizing works today

`buildImage` (src/image_write.c) picks the NAND layout in this order:

1. `NAND_BIG_BLOCK`: 64MiB big block. None of the new names sets it.
2. Not `BUILD_DEVKIT`/`BUILD_TESTKIT`: 48MiB if `NAND_MMC`, else 16MiB
   (`NAND_RAW_16M` raw, 0x400 blocks).
3. Otherwise (devkit, testkit): 64MiB small block: `NAND_RAW_64M` raw,
   `NAND_SIZE_64M` user, 0x1000 blocks, FS 0..0xf7c, SMC config at
   `SMCCFG_OFFSET_64M` (0x3dfc000).

So the 64MiB small block layout already exists, but only the devkit and
testkit build types reach it. The plan ties it to a console flag as well.

The console type comes only from `-c`, a perbox file or options.ini's
`type` (src/mode_build.c, through `setConsoleType`/`iniConsoleType`), or in
client and update mode from the console (`showImageType`). A dump never
sets it.

## Matching

Any behaviour change moves `make check` off the reference SHA256. Like
every fix and enhancement, the feature goes under `XEBUILD_FIXES` (every
platform but win32 defines it; `make win32fixes` builds it with the pinned
toolchain): `#ifdef XEBUILD_FIXES` for the new code, with the original in
an `#else` where a test is replaced, so the default build stays
byte-identical. Add a line to README.md's list of fixes.

## Changes

### 1. Flag bit and helper (src/xebuild.h)

Bits 3..27 of `xb.flags` are unused (28..31 are `NAND_MMC`,
`NAND_BIG_FFS`, `NAND_BIG_BLOCK` and `NAND_BB_CONTROLLER`).

```c
#define NAND_SMALL_64M 0x08000000	/* 64MiB small block NAND on a non-kit build */
#define IS_64M_SMALL (xb.type == BUILD_DEVKIT || xb.type == BUILD_TESTKIT || \
		      (xb.flags & NAND_SMALL_64M))
```

plans/nand-1g.md also wants a bit (`NAND_BIG_BLOCK_256K`, "a free top
bit"). The top four are taken, so the next one down is this one: whichever
plan lands second takes another (e.g. 0x04000000).

The low 3 bits stay `CONSOLE_XENON`/`ZEPHYR`/`FALCON`/`JASPER`, so console
type tests, `IS_SLIM` and the `consoleNames[]` ini and patch file lookups
are unaffected (xenon64 uses xenon's ini sections, jaspersb64 jasper's).
Add the new names to the flags table in the comment above `CONSOLE_MASK`.

### 2. Names (src/options.c, src/mode_build.c)

Add to `setConsoleType` and to `iniConsoleType` (perbox files):

| name | `xb.flags` | appended to `xb.outName` |
|---|---|---|
| `xenon64` | `NAND_SMALL_64M \| CONSOLE_XENON` | `xenon64` |
| `zephyr64` | `NAND_SMALL_64M \| CONSOLE_ZEPHYR` | `zephyr64` |
| `falcon64` | `NAND_SMALL_64M \| CONSOLE_FALCON` | `falcon64` |
| `jaspersb64` | `NAND_SMALL_64M \| CONSOLE_JASPER` | `jaspersb64` |

`jaspersb64` has no `NAND_BB_CONTROLLER`, as `jaspersb`. `xb.outName`
becomes the image file name (filelist_ini.c); `jaspersb` appends plain
`jasper`, but `jaspersb64` uses its own name so the file says what it was
built for.

Add the four names to the `XEBUILD_FIXES` `<con>` list in `build_usage`
(src/mode_build.c).

### 3. Size checks that are spelled as devkit/testkit

Replace with `IS_64M_SMALL`:

- `buildImage` (src/image_write.c): the
  `xb.type != BUILD_DEVKIT && xb.type != BUILD_TESTKIT` branch test.
- Bad block remap range (`finalizeImage`, src/image_write.c, the
  `blocks = xb.type == BUILD_DEVKIT || ...` line): 0x1000 blocks instead
  of 0x400.
- `showConsoleInfo` NAND size line (src/main.c): prints
  "64MiB (small block)". The console line needs nothing: its switch masks
  `NAND_BIG_BLOCK | CONSOLE_MASK`, so the new types print Xenon, Zephyr,
  Falcon and Jasper.
- Mobile file offsets (src/build.c, the `statisticsOffset` /
  `manufacturingOffset` calls): the `big` argument is currently
  `xb.type > BUILD_DEVGL16` (see Existing bugs).

### 4. Reserved FS blocks (open question)

`fixupEmptyFsBlocks` (src/image_write.c) marks the blocks after `fsEnd`
`FS_CHAIN_RESERVED`:

- 16MiB non-kit: 4 blocks (0x3dc..0x3df, ending at the SMC config block).
  That reaches the remap area exactly: `findFreeRemap` (src/image_read.c)
  only takes the last `REMAP_BLOCKS` (32) blocks, 0x3e0..0x3ff.
- Kits (`xb.type > BUILD_DEVGL16`): every block up to `xb.blocks` (0x84
  on 64MiB, 0x24 on devkit16/testkit16).

On 64MiB the two rules differ. 4 blocks (0xf7c..0xf7f, SMC config at block
0xf7f) leave 0xf80..0xfff unmarked (0 in `fsChain`), but xeBuild remaps
only into 0xfe0..0xfff, so 0xf80..0xfdf would be 0x60 unmarked blocks that
nothing uses. The kit rule marks all 0x84 and gives the only 64MiB small
block FS table xeBuild writes today: take it (add
`|| (xb.flags & NAND_SMALL_64M)` to the kit test) unless the FS table of a
dump a real 64MiB Xenon/Zephyr/Falcon/Jasper wrote says otherwise.

### 5. Detection from existing data

- Dump reading (src/image_read.c): the `statisticsOffset` /
  `manufacturingOffset` calls pass `big = 0`. Pass "not big block, not
  MMC, `xb.dumpSize == NAND_SIZE_64M`" (`xb.dumpSize` is the dump's user
  bytes; the file-static `dumpSize` is its raw file size). `findSmcConfig`
  already makes that test, so a 64MiB small block dump's SMC config is
  already found; only the Mobile offsets are wrong. The controller
  (`xb.dumpBbController`) comes from the spare data at any size, so a
  jaspersb64 dump reads as small block controller.
- Client and update mode: both reach `showImageType` (src/consoleinfo.c)
  through `parseConsoleInfo` (mode_client.c, mode_update.c), so one change
  covers both. Its switch adds a suffix only for Corona (`4g` at
  `NAND_SIZE_MMC`) and Jasper/Trinity (`bb`/`bigffs` at
  `NAND_SIZE_BIG_BLOCK`, 0x4200000). Add:
  - Xenon, Zephyr, Falcon: `64` when `nandType == NAND_SIZE_BIG_BLOCK`. No
    fat console has a big block NAND, so the size alone says 64MiB small
    block.
  - Jasper: `sb64` when `nandType == NAND_SIZE_BIG_BLOCK` and the block
    size is a small block one (`NAND_RAW_BLOCK`, 0x4200), tested before the
    `bb`/`bigffs` arm, which Trinity keeps as it is. The block size is the
    last argument (`info->blockSize`, named `unused` today; renaming it
    changes no code).

  `showImageType` also saves the name with `optWrite("type", ...)`, so a
  later build from that options.ini gets the new type. Update mode's bad
  block list uses the console's own `nandSize / blockSize`, so it needs
  nothing else.

  That a 64MiB small block NAND reports `nandSize` 0x4200000 and
  `blockSize` 0x4200 is inferred, not seen: both are raw sizes
  (mode_client.c divides them by `NAND_RAW_BLOCK`).

### 6. jaspersb64 and the big block controller

Not planned: a 64MiB small block Jasper on the big block controller (a
`jasper64`). If one exists, client and update mode can't tell it from
jaspersb64. They can't tell jaspersb from jasper at 16MiB today either:
`showImageType` returns plain `Jasper`, which `setConsoleType` makes
`NAND_BB_CONTROLLER`.

## Not expected to change

- Header template: `cbOffset` and `kvSize` depend on build type and
  console, not NAND size. Under `XEBUILD_FIXES` the Xenon/Zephyr
  `kvSize = 0` reset is gone and the patch slot size defaults to
  `FLASH_PATCH_SLOT` (0x10000), so xenon64/zephyr64 keep `KV_SIZE`, and
  jaspersb64, like jaspersb, sets no `bbController` and keeps the 0x10000
  default.
- Spare data: jaspersb64 writes the small block controller's layout
  (`xb.bbController` stays 0), as the fat consoles and the 64MiB kits do.
- SMC config position: follows `xb.smcConfigOffset`.
- Bootloaders: the fat consoles and XSB Jaspers are believed to take the
  NAND geometry from the flash controller rather than the image. Only a
  real 64MiB board can confirm this.

## Existing bugs found on the way

These are in the original and worth fixing whether or not this feature
lands (also under `XEBUILD_FIXES`):

- src/build.c passes `xb.type > BUILD_DEVGL16` as the 64MiB flag for the
  Statistics.settings / Manufacturing.data offsets. That includes devkit16
  and testkit16, which are 16MiB, so they get 0x3df8000 and 0x3df4000,
  past the end of their image. `imgAdd` refuses an offset past
  `xb.rawSize` (it returns -1, which `imgAddRaw` ignores), so both files
  are silently dropped while the log says they are being added.
- src/image_read.c always passes 0 for that flag when reading a dump, so a
  64MiB small block dump (devkits included) is searched at the 16MiB
  offsets.

# 1GB big block NANDs (256KB blocks)

Status: plan only, nothing implemented.

Goal: four new console types, `jasper1g`, `trinity1g`, `corona1g` and
`winchester1g`, for 1GB NANDs with 256KB blocks (0x200 pages of 0x200 data
+ 0x10 spare; raw block 0x42000). xeBuild builds their 64MB system area
(raw 0x4200000), reads their dumps, and remaps their bad blocks, the same
way it does for today's 128KB big block types (`jasperbb`, `jasper256`,
`jasper512`, `<x>bb`, `<x>bigffs`).

All 1GB machines use the big flash filesystem (48MB, like `<x>bigffs`).
There is no small-FS 1GB variant: each `<x>1g` name implies
`NAND_BIG_BLOCK | NAND_BIG_FFS`.

1GB NANDs were never an official console configuration: Microsoft
shipped none, so there is no factory image, no retail dump and no spec to
match. The layout here comes from what the community has built and tested
(J-Runner's converter and images people have booted), not from a known
reference. "Works" in this plan means "people have booted it". Where the
plan picks a value, it is the tested one or our best guess, and better
evidence (a dump a 1GB console's own kernel has written to) should
override it.

Everything goes under `XEBUILD_FIXES`, so `make check` is unaffected, and
gets one line in README.md's list of fixes.

Reference: J-Runner with Extras, `J-Runner/Nand/NandImageConverter.cs` at
commit c04ffedb (`OneGbGeometryConverter`), which converts 128KB big
block images to and from the 1GB layout. Its output is the only oracle we
have (see Testing).

## The 1GB layout vs. 128KB big block

The sectors stay in the same linear order. Only the block grouping, the
spare metadata and a few fixed offsets change.

| | 128KB big block (bigffs) | 1GB, 256KB |
|---|---|---|
| pages per block (`NAND_BB_PAGES`) | 0x100 | 0x200 |
| block data / raw (`NAND_BB_BLOCK`, `NAND_RAW_BB_BLOCK`) | 0x20000 / 0x21000 | 0x40000 / 0x42000 |
| block shift / mask | 17 / 0x1ffff | 18 / 0x3ffff |
| spare bytes 1-2 (block number) | sector / 0x100 | sector / 0x200 |
| patch slot size (`flashHdr.patchSlotSize`) | 0x20000 (`FLASH_PATCH_SLOT_BB`) | **0x40000** |
| FS window (48MB) | 0xB80000-0x3B80000 | 0xB00000-0x3B00000 |
| `xb.fsStart` / `xb.fsEnd` (16KB blocks) | 0x2e0 / 0xee0 | 0x2c0 / 0xec0 |
| spare bytes 7/8/9 of FS pages (`spare7/8/9`) | 0x0A / 0x60 / 0x04 (J-Runner's values) | 0x05 / 0x30 / 0x04 |
| config area (4 blocks) | 0x3B80000, 4 x 128KB | 0x3B00000, 4 x 256KB, data in the first 128KB of each, rest 0xFF |
| manufacturing (`manufacturingOffset`) | 0x3BA0000 | 0x3B40000 |
| statistics (`statisticsOffset`) | 0x3BC0000 | 0x3B80000 |
| SMC config (`SMCCFG_OFFSET_BB`) | 0x3BE0000 | 0x3BC0000 |
| bad-block reserve | block 0x1E0 (60MB) | block 0xF0 (60MB) |
| blocks in the system area | 0x200 | 0x100 |
| ECD (`calcEcd`) | per 0x210 page | unchanged |

The FS window moves down 512KB because the config area doubles to 1MB and
the window has to end below it.

The patch slot size is 0x40000 for 256KB blocks (one block per slot), just
as it is 0x20000 for 128KB. J-Runner's converter keeps the 128KB image's
header unchanged; that is wrong for these machines and we don't follow it.

Spare bytes 7 and 8 are counts in big blocks, so they halve:
- byte 8 (`xb.spare8`) is the FS size: 0x60 x 128KB = 0x30 x 256KB = 48MB.
  `setFsOffset` (image_read.c) reads it back as `meta = s[8] << 5`, the
  size in 16KB blocks; with 256KB blocks that is `<< 6`.
- byte 7 (`xb.spare7`) is the first block after the patch slots (start of
  the MU area), set by `setPatchSlot` as
  `(off + 2 * cf) >> NAND_BB_SHIFT`. With a 0x40000 slot and shift 18 it
  comes out in 256KB units by itself.
- byte 9 (`xb.spare9`) stays 4: every FS table and FS file page of the
  working image (Findings) has 4.

## Where xeBuild hard-codes 128KB

### Geometry as runtime values

`NAND_BB_BLOCK`, `NAND_BB_SHIFT`, `NAND_BB_MASK`, `NAND_BB_PAGES` and
`NAND_RAW_BB_BLOCK` (src/xebuild.h) are compile-time constants used all
through image_write.c and image_read.c. Under `XEBUILD_FIXES`, make them
read fields of `xb` (e.g. `xb.bbShift`, from which the rest follow) that
`buildImage` sets for the image and `detectController` sets for the dump,
with the original constants in the `#else`. The original build then
compiles exactly as before, and the existing 128KB code paths work for
256KB without being touched one by one. Check every use for a constant
context (array sizes, `case` labels) before switching.

The dump and the image can differ (donor dump vs. target type), so the
dump needs its own geometry next to `xb.dumpBigBlock` (e.g.
`xb.dumpBbShift`), and image_read.c's uses of `NAND_BB_*` must take the
dump's.

### Console types: options.c, main.c, mode_build.c, xebuild.h

- A NAND flag for 256KB blocks, e.g. `NAND_BIG_BLOCK_256K` in a free top
  bit of `xb.flags` (src/xebuild.h, next to `NAND_BIG_BLOCK`), always with
  `NAND_BIG_BLOCK | NAND_BIG_FFS`. Update the table in the comment above
  `CONSOLE_MASK`.
- `setConsoleType` (`-c` names) and `iniConsoleType` (perbox files) in
  src/options.c: `jasper1g`, `trinity1g`, `corona1g`, `winchester1g`, each
  setting `NAND_BIG_BLOCK | NAND_BIG_FFS | NAND_BIG_BLOCK_256K | CONSOLE_x`
  and appending its name to `xb.outName`.
- The console type names in src/main.c (`case NAND_BIG_BLOCK | CONSOLE_x`
  lines): the switch masks the flags, so add the new combinations, e.g.
  "Jasper (1GB big block)".
- The `<con>` lists in mode_build.c's usage text.
- mode_build.c's "requires bigffs, forcing" check for devkit/testkit
  Jasper: already satisfied, since 1g implies bigffs.

### Building: image_write.c

- `buildImage`: a 1g branch inside `NAND_BIG_BLOCK`: `fsStart` 0x2c0,
  `fsEnd` 0xec0, `smcConfigOffset` 0x3BC0000, `spare8` 0x30, `spare7`'s
  initial value 0x08 (half of 0x10, the same byte offset 0x200000; only
  retail builds overwrite it in `setPatchSlot`; see Findings for why not
  the working image's 5),
  `muBlocks` 0x2c (0xB00000 >> 18). `xb.blocks`, `userSize`, `rawSize`
  and `spareSize` are unchanged (64MB system area).
- Patch slot size: every place that sets `FLASH_PATCH_SLOT_BB` (the Jasper
  case, and the kit builds' `xb.bigBlock ? FLASH_PATCH_SLOT_BB : ...`)
  sets 0x40000 for 1g. Trinity, Corona and Winchester currently set
  `FLASH_PATCH_SLOT` (0x10000) even for `bb`/`bigffs`; the 1g types set
  0x40000 whatever the console. Same for the JTAG branch's
  `if (bigBlock)` (Jasper only, sets 0x10000 today).
- `setPatchSlot`: rounds the CF offset up with `NAND_BB_MASK`, so 256KB
  alignment follows from the runtime mask. Its `spare7` formula uses
  `h[28]` (patch slot size) and falls back to `FLASH_PATCH_SLOT`; with the
  header set to 0x40000 above, `h[28]` is never 0 for 1g.
- `imgAdd`'s big block branch: the block number written to spare bytes 1-2
  (fixed up later, below), the Mobile/anchor files' pages-left count
  (`left = NAND_BB_PAGES`), and `p = off & NAND_BB_MASK`. The
  `(int)pages & 3` rounding (2KB) and `s[9] = (left - pages) >> 2` stay
  as they are for now: the working image's Mobiles are 2KB apart, and its
  byte 9 counts down from 0x7f, which is `(0x200 - 4) >> 2` (Findings).
  Whether that is right on a 1GB console is an open question (Open
  questions).
- The "fixing up big block LBA numbers in spare" pass in `buildRaw`
  (image_write.c, `n = xb.blocks / (NAND_BB_BLOCK / NAND_BLOCK)`): follows
  from the runtime geometry.
- `setBlockSpare`, `blockEccOk`, `blockErased`, `blockPagesErased`: take
  `int bigBlock` and pick `NAND_BB_PAGES`; follows from the runtime
  geometry.
- Bad-block remap (`buildRaw`): `size = NAND_RAW_BB_BLOCK`,
  `blocks = NAND_SIZE_64M / NAND_BB_BLOCK` (0x100). The condition
  `xb.bigBlock == xb.dumpBigBlock` must also require the same block size,
  or the remap table is in the wrong units; otherwise fall into the
  existing "same small/big block style NAND donor" error.
- NAND MU restore (`OPT_NANDMU`): copies blocks `spare7 .. muBlocks` from
  the dump in `NAND_BB_*` units; needs the same geometry check.
- `reservedAreaOffset`: big block is `b = n + 0x1df`, `off = b * 0x20000`,
  `page = b * 0x1000`, `sector = b * 0x800`. 1g: `b = n + 0xef`,
  `off = b * 0x40000`, `page = b * 0x2000`, `sector = b * 0x1000`.
- `statisticsOffset` / `manufacturingOffset`: big block returns
  0x3BC0000 / 0x3BA0000 (page = off / 0x20, sector = off / 0x40). 1g:
  0x3B80000 / 0x3B40000, same scaling. Both take `int bigBlock`; they need
  the block size too (called from build.c with `xb.bigBlock` and from
  image_read.c with `xb.dumpBigBlock`).
- The config area's four blocks (SMC config, statistics, manufacturing,
  and the first block): each written into the first 128KB of its 256KB
  block, the rest left 0xFF and its spare erased.

### Reading dumps: image_read.c

- `detectController`: `raw[NAND_PAGE] == 0xff` says big block but not
  which size. Tell them apart by the block number in page 0x100's spare
  (bytes 1-2): 1 for 128KB blocks, 0 for 256KB. A dump of 0x42000000 bytes
  (full 1GB) is also 256KB. Set the dump geometry there.
- `scanMobiles` / `showMobilePages`: the scan ends at
  `xb.dumpPages - 9216` (0x3B80000, the 128KB config area). 1g:
  `xb.dumpPages - 10240` (0x3B00000). The `(page + 3) & ~3` alignment
  after a Mobile file stays (2KB, as in `imgAdd`).
- `setFsOffset`: `meta = s[8] << 5` and the end 3808 (0xee0); 1g:
  `s[8] << 6` and 0xec0.
- `findSmcConfig`, statistics and manufacturing reads: through
  `statisticsOffset` / `manufacturingOffset` with the dump's geometry.
- The truncation of a big block overdump to 0x4200000 (`size >
  NAND_RAW_64M`) and `copyNandMu` (the data past the system area of a
  full dump) work as they are: 0x42000000 is a multiple of 0x4200000.

### Network modes: consoleinfo.c, mode_client.c, mode_update.c

- `showImageType` (consoleinfo.c) names the type from the bootstrap and
  `nandSize`, and ignores `blockSize`. Add: a big block system area with a
  raw block size of 0x42000 is `<x>1g`. Today it only names `bb`/`bigffs`
  for Jasper and Trinity; Corona and Winchester big block aren't named at
  all, which the 1g change can fix too.
- mode_client.c and mode_update.c work in `nandSize / blockSize` and the
  console's own block size, so reads, writes, erases and the bad-block
  list should work as they are. Check the raw-to-data conversion in
  mode_client.c (`cinfo->blockSize / NAND_RAW_BLOCK * NAND_BLOCK`) gives
  0x40000 for 0x42000.

## Steps

1. Runtime geometry for `NAND_BB_*` under `XEBUILD_FIXES` (image and
   dump), with 128KB values by default; `make check` still matches and
   `make win32fixes` builds a byte-identical `jasperbigffs` image to before.
2. The four console types and the 256KB flag (options.c, main.c,
   mode_build.c, xebuild.h).
3. `buildImage` layout, patch slot size, the config area, reserved and
   stats/manufacturing offsets.
4. `imgAdd` spare details (pages-left, alignment), checked against the
   oracle.
5. Dump detection and reading (image_read.c), the geometry checks on
   remap and MU restore.
6. `showImageType`.
7. README.md fix line.

## Testing

No 1GB hardware is assumed. Two checks:

- **Build:** build `jasperbigffs` with the fixes build, convert it with
  J-Runner's `ConvertFromLegacyBigBlock`, and compare against our
  `jasper1g` build of the same inputs. Expected differences: the patch
  slot size (0x40000 in ours) and whatever follows from it (CF offset
  alignment, spare byte 7). Everything else (FS, config, spare, ECD)
  should match byte for byte.
- **Read:** take that converted image as a `nanddump.bin` and check
  xeBuild detects 256KB blocks, finds the FS root, Mobiles, SMC config, KV
  and statistics, and that an update (`-u`-style) rebuild round-trips.

## Findings from a working image

A working Corona 1GB image (raw 0x4200000; a 17489 devkit build: SB/SC/
SD/SE, qfe 0x8000, no CF) answers the open questions. It was converted
from a 48MB eMMC devkit image of the same build, not written by a 1GB
console: its FS data, SMC config and statistics are byte-identical to
the eMMC image's (eMMC 0xf4000, 0x2ffc000, 0x2ff8000). So its spare bytes
come from the converter. What it shows is a set of values that boots,
not what a 1GB console's kernel writes itself.

- **Block numbers**: spare bytes 1-2 are `page / 0x200` on every used page
  (0 mismatches; `page / 0x100` mismatches on nearly all).
- **Header**: `patchSlotSize` 0x40000, `sysUpdateAddr` 0x100000. The SE
  ends at 0xd21e2; rounding up to 256KB gives 0x100000 (128KB would give
  0xe0000), so `setPatchSlot`'s rounding with the 256KB mask is right.
  The two slots (0x100000-0x180000) are empty, as for any kit build.
- **FS pages**: types 0x2c (FS table) and 0x2a (file) all have bytes
  7/8/9 = 05/30/04; the FS table pages have byte 5 = a version (1 for the
  one at 0xb00000), file pages 0. Byte 9 is **4**.
- **Mobiles** (in block 0x2d, 0xb40000): every entry starts 4 pages (2KB)
  after the previous; one-page entries leave 3 pages unused. Byte 9 goes
  0x7f, 0x7e, ... down by one per entry: `(0x200 - used - pages) >> 2` with
  pages rounded up to 4. So in this image, padding is **2KB** (`& 3`,
  `>> 2`), with `NAND_BB_PAGES` = 0x200. Bytes 7-8 are the length (0x800
  for a full entry), as today. Whether a 1GB console does the same is in
  Open questions.
- **Layout**: FS table at 0xb00000, Mobiles at 0xb40000, files from
  0xb80000. Config window: statistics at 0x3b80000, SMC config at
  0x3bc0000, each in the first 128KB of its 256KB block with the second
  half erased. 0x3b00000 and 0x3b40000 (manufacturing) are erased; the
  eMMC source had nothing there either. No block from 0xf0 (reserve) is
  used.
- **Spare byte 7 for kits**: this image has 5 (0x140000). That is
  J-Runner's fixed tag (0x0A halved), not anything derived from this
  image: xeBuild's retail formula `(sysUpdateAddr + 2 * patchSlotSize)
  >> 18` gives 6 here (0x180000, the end of the two 0x40000 slots). 5
  boots with both slots empty, but it puts the area after the slots
  inside the second slot, so for 1g:
  - retail: keep `setPatchSlot`'s formula, which with the 0x40000 slot
    gives the end of the slots;
  - kit/JTAG: 0x08 (legacy's 0x10 halved, still 0x200000), clear of
    both slots. 5 is known to boot if 0x08 turns out not to.
- **Other**: 0x300000 holds 128KB of zeros (block number 0x0c, valid ECD)
  with the second half erased. That looks like a 128KB bad-block zero
  fill carried through the conversion. When xeBuild remaps a 1g block it
  zero-fills the whole 256KB.

The eMMC source image has no spare data, so it says nothing more about
these questions.

## How xeBuild lays out Mobiles today

`imgAddMobile` (image_write.c) and `imgAdd`'s spare bytes. Neither pads
the data: `imgAdd` is called with `pad` 0, so it writes the spare of
`ceil(len / 0x200)` pages and leaves the rest of the space erased.

- **Small block (16KB blocks):** every Mobile starts a new 16KB block
  (`imgSizeAligned`) and is alone in it; the next thing written starts at
  the next block. Byte 9 is the block's free pages,
  `NAND_BLOCK_PAGES - pages` (0x20 - pages, in 512-byte pages, no
  rounding).
- **128KB big block:** the first Mobile starts a new 128KB block; the
  rest are packed after it, each on a 2KB boundary (`mobileOffset`
  rounded up with `0x7ff`). A Mobile that would run past the end of the
  block moves to the start of the next one. Byte 9 is the space left in
  the 128KB block after the entry, in 2KB units:
  `(0x100 - pages before it - pages rounded up to 4) >> 2`, 0x3f at most.

For 1g the same code with `NAND_BB_*` at 256KB packs the Mobiles into a
256KB block with byte 9 counting 2KB units of it (0x7f at most).

## Open questions

- **Mobile padding in a 256KB block.** Should a 1GB image pack Mobiles at
  2KB steps through the whole 256KB block, with byte 9 counting what is
  left of the 256KB block? Or should it treat a Mobile as filling (padded
  to) the rest of a smaller unit, such as a 128KB half or the 4KB
  physical page? The working image can't settle it. Its byte 9 values
  (from 0x7f) assume the whole 256KB block, but J-Runner's converter
  computed them, not a 1GB console. All of its 55 entries fit in the
  first 0xdc pages (110KB) of block 0x2d, so nothing shows what happens at
  128KB. To settle it we need a dump from a 1GB console whose kernel has
  rewritten its Mobiles, or a Mobile set larger than 128KB written by
  one.

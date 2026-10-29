# CLAUDE.md

Matching rebuild of `xeBuild.exe`. README.md is the high-level overview for people;
NOTES.md has the findings, layout and the pipeline.

## Rules

- `xeBuild.exe` in the repo root is the reference. Never modify it; analyse copies
  (IDA writes `.i64` next to its input, so point IDA at a copy under `build/`).
- Success is measured by bytes: `sh build.sh` must end with SHA256
  `10dac648197fa5cdbb82d975ab9ff11f64075c9686908dfd9a33edc533f1971c` (it also
  runs `tools/re/execmp.py`, which names any differing header field or byte).
- Every object is C; `build.sh` compiles only `.c` files, in the link order
  of its `$objects` list (the original's; `tools/re/split.py`'s `NAMES` has the
  evidence). `tools/re/split.py` still writes a `.s` from `build/xeBuild.lines.json`
  (`tools/re/ddfix.py`) for any object without a `.c`, but nothing builds it.
- `src/**/*.c` are hand-maintained: XeCrypt's sources under `src/crypto` (see
  NOTES.md) and the app's reconstructed C directly in `src/`. `build.sh`
  compiles each with the per-object flags and original `__FILE__` path set
  there. Keep third-party licence notices intact.
- Shared app types live in `src/xebuild.h` and each object's exported
  prototypes in `src/<obj>.h` (NOTES.md, App headers); don't redeclare them
  in a .c. If a file's code needs another typing to match, use a cast or an
  asm-label declaration (`T fnU32(...) __asm__("_fn")`) marked
  `TODO(xebuild.h cast)` / `TODO(prototype cast)`.
- Keep NOTES.md's Progress section current: after converting an object or
  function (or parking one in `tools/wip/`), run `sh build.sh` then
  `python tools/re/progress.py`, and commit NOTES.md with the change. Functions
  defined in `tools/wip/<obj>.c` that `tools/re/fncmp.py` matches count as C (put a
  draft's non-default gcc flags in the script's `WIP_FLAGS`). The section
  is generated; change `tools/re/progress.py`, not the NOTES.md text between the
  `progress:begin/end` markers. Update the
  "Move functions to C" row in NOTES.md's Status by hand when the totals move.
- To match a function before a full build: `python tools/re/fncmp.py src/<obj>.c
  <name> [flags]` (MATCH or a diff against the original). For a whole file,
  compare its `.text` against `build/obj/<obj>.o` from the last matching
  build (objdump without addresses). Then run the full build.
- File names and boundaries live in `tools/re/split.py` (`NAMES`, with the evidence
  for each). Data boundaries are inferred; keep 4-byte alignment of every
  section piece (gas pads sections to 4).
- Commit without asking whenever a milestone is verified: a coherent step
  (for example a component moved to C, or a pipeline change) is finished and
  `sh build.sh` reproduces the SHA256. Don't commit a build that doesn't match.
  Push to `origin` after each commit.
- Never force push (`--force`, `--force-with-lease`, `+refspec`) or rewrite
  pushed history. If a push is rejected, something went wrong: stop and ask.
- Don't hand-patch the linked exe beyond `tools/re/stamp.py` (timestamp + checksum);
  every other difference must be fixed in the source or build.sh (the link uses
  the gcc driver with the toolchain's own runtime and ld's default script).
- Only use the pinned toolchain in `tools/toolchain-4745/` (gcc 6.2.0, binutils
  2.27, crt 4745 with kernel32/msvcrt import libraries rebuilt from mingw-w64
  e05f3e8 by `tools/fetch_toolchain.sh`). Newer binutils encode differently. gcc needs its `bin/` on
  PATH (cc1 and as load DLLs from there); otherwise it fails silently.
- Don't search the machine for GCC sources or use copies left under `tmp/`.
  Try gcc's dumps (`-fdump-rtl-*`, `-fdump-tree-*`) and the notes first; only
  if a question really needs the source, read that one file from the official
  GCC repository at tag `releases/gcc-6.2.0`, e.g.
  `https://gcc.gnu.org/git/?p=gcc.git;a=blob_plain;f=gcc/bb-reorder.c;hb=refs/tags/releases/gcc-6.2.0`.

## Environment gotchas (Windows 11)

- Bash tool is Git Bash. When calling `wsl` with paths, export
  `MSYS_NO_PATHCONV=1`, and put multi-line WSL work in a script file rather
  than `bash -c "..."` (quoting breaks).
- WSL is Ubuntu 26.04 running as **WSL1** with no passwordless sudo.
  `dpkg-deb -x` fails there ("Function not implemented");
  `tools/ddisasm/install.sh` unpacks with Python instead. ddisasm lives in
  `~/ddisasm-root`; source
  `tools/ddisasm/env.sh` before using it.
- Pass absolute paths to executables from Python `subprocess` on Windows.
- Write generated text with `newline='\n'`; `.gitattributes` enforces LF
  (the `.sh` files must be LF for WSL bash).
- Never `rm -rf` a directory from a variable or glob (a safety check blocks it);
  write to a fresh directory or let the generator overwrite in place.
- In Python edit scripts, string escapes like `'\n'` / `'\0'` get mangled through
  heredocs; use the Edit tool for code changes.
- IDA 9.4 idalib: `python script.py` with the pip-installed `idapro` wheel; don't
  use `python -I` (hides the user site-packages where it lives).

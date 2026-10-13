# CLAUDE.md

Matching rebuild of `xeBuild.exe`; see README.md for findings, layout and the pipeline.

## Rules

- `xeBuild.exe` in the repo root is the reference. Never modify it; analyse copies
  (IDA writes `.i64` next to its input, so point IDA at a copy under `build/`).
- Success is measured by bytes: `sh build.sh` must end with SHA256
  `10dac648197fa5cdbb82d975ab9ff11f64075c9686908dfd9a33edc533f1971c` (it also
  runs `re/execmp.py`, which names any differing header field or byte).
- `src/xeBuild.s` is generated. Change it by changing `re/ddfix.py` or the
  `tools/ddisasm/disasm.sh` options and regenerating, until hand edits begin
  (record in the README when that switch happens).
- Don't hand-patch the linked exe beyond `re/stamp.py` (timestamp + checksum);
  every other difference must be fixed in the source, linker script or ddfix.
- Only use the pinned toolchain in `tools/toolchain-4745/` (gcc 6.2.0, binutils
  2.27, crt 4745). Newer binutils encode differently.

## Environment gotchas (Windows 11)

- Bash tool is Git Bash. When calling `wsl` with paths, export
  `MSYS_NO_PATHCONV=1`, and put multi-line WSL work in a script file rather
  than `bash -c "..."` (quoting breaks).
- WSL is Ubuntu 26.04 running as **WSL1** with no passwordless sudo.
  `dpkg-deb -x` fails there ("Function not implemented"); `install.sh` unpacks
  with Python instead. ddisasm lives in `~/ddisasm-root`; source
  `tools/ddisasm/env.sh` before using it.
- Pass absolute paths to executables from Python `subprocess` on Windows.
- Write generated text with `newline='\n'`; `.gitattributes` enforces LF
  (the `.sh` files must be LF for WSL bash).
- In Python edit scripts, string escapes like `'\n'` / `'\0'` get mangled through
  heredocs; use the Edit tool for code changes.
- IDA 9.4 idalib: `python script.py` with the pip-installed `idapro` wheel; don't
  use `python -I` (hides the user site-packages where it lives).

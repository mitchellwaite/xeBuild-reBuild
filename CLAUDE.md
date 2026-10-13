# CLAUDE.md

Matching rebuild of `xeBuild.exe`; see README.md for findings, layout and the pipeline.

## Rules

- `xeBuild.exe` in the repo root is the reference. Never modify it; analyse copies
  (IDA writes `.i64` next to its input, so point IDA at a copy under `build/`).
- Success is measured by bytes: `re/objcmp.py` must stay at 0 diffs, and the final
  goal is SHA256 `10DAC648197FA5CDBB82D975AB9FF11F64075C9686908DFD9A33EDC533F1971C`.
- `src/xeBuild.s` is generated. Change it by changing `re/ddfix.py` or the
  `tools/ddisasm/disasm.sh` options and regenerating, until hand edits begin
  (record in the README when that switch happens).
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
- IDA 9.4 idalib: `python script.py` with the pip-installed `idapro` wheel; don't
  use `python -I` (hides the user site-packages where it lives).

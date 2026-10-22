# applyIniOptions profile-build tools

For wip/app/options_fdo.c (see wip/README.md, app/options).  Work dirs are
subdirectories here (ignored by git).  Reproduce the parked state:

    mkdir -p wip/aio/t && cp wip/app/options_fdo.c wip/aio/t/a.c
    sh wip/aio/align.sh t ../app/options_fdo.prof   # blk/fncmp counts, then padding diffs
    cd wip/aio && python aldiag.py t                # each label that needs (P) or must not get (N) alignment

- `aiofdo.sh <dir> [overrides]`: instrumented compile (.gcno + profile_estimate
  dump), re/gcda.py, then wip/blk.py and re/fncmp.py on the profile build.
- `run.sh <dir> <overrides file>`: aiofdo.sh, dumps.sh, `lab.txt` (role-labeled
  block order vs the original, `*` = mismatch) and `trl.txt` (STC traces with
  rounds, frequencies and roles).
- `dumps.sh <dir>`: -dA asm (`o.s`), bbro, cprop_hardreg and alignments dumps.
- `align.sh <dir> <overrides file>`: run.sh, assembles `o.s` and diffs the
  instructions including padding against the original (`<dir>/al.txt`).
- `aldiag.py <dir>`: per label, the alignment pass's freq/fall/branch
  numbers vs alignreq.txt (P padded in the original, N must not be requested,
  F free: 16-aligned or 1..5 mod 16, where `.p2align 4,,10` emits nothing).
- `lab.py`, `trl.py`, `discmp.py`, `discmp_lib.py`, `alignreq.py`: helpers.
  They read the original applyIniOptions from src/app/options.s; once that
  function is in C, point them at `git show 56e988e:src/app/options.s`.

`python wip/aiodesign.py <dir>/a.c.042t.profile_estimate` regenerates the
overrides (wip/app/options_fdo.prof).

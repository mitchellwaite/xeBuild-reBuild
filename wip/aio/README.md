# applyIniOptions profile-build tools

For applyIniOptions' crafted profile (src/app/options.c and .prof; see
wip/README.md, app/options).  Work dirs are subdirectories here (ignored by
git).  Check a change to the source or to wip/aiodesign.py:

    mkdir -p wip/aio/t && cp src/app/options.c wip/aio/t/a.c
    sh wip/aio/align.sh t ../../src/app/options.prof   # blk/fncmp counts, then padding diffs
    cd wip/aio && python aldiag.py t                    # each label that needs (P) or must not get (N) alignment

After a source change regenerate the overrides from the new dump first
(`python wip/aiodesign.py wip/aio/t/a.c.042t.profile_estimate`).  `AIOFL`
overrides the compile flags of aiofdo.sh and dumps.sh.

- `aiofdo.sh <dir> [overrides]`: instrumented compile (.gcno + profile_estimate
  dump), re/gcda.py, then wip/blk.py and re/fncmp.py on the profile build.
- `run.sh <dir> <overrides file>`: aiofdo.sh, dumps.sh, `lab.txt` (role-labeled
  block order vs the original, `*` = mismatch) and `trl.txt` (STC traces with
  rounds, frequencies and roles).
- `dumps.sh <dir>`: -dA asm (`o.s`), bbro, cprop_hardreg and alignments dumps.
- `align.sh <dir> <overrides file>`: run.sh, assembles `o.s` and diffs the
  instructions including padding against the original (`<dir>/al.txt`).
- `grun.sh <dir>`: the same outputs for `<dir>/a.c` without a profile
  (gcc's guessed one; GFL overrides the flags); see wip/README.md,
  "applyIniOptions without a profile", and wip/aiog.py.
- `aldiag.py <dir>`: per label, the alignment pass's freq/fall/branch
  numbers vs alignreq.txt (P padded in the original, N must not be requested,
  F free: 16-aligned or 1..5 mod 16, where `.p2align 4,,10` emits nothing).
- `lab.py`, `trl.py`, `discmp.py`, `discmp_lib.py`, `alignreq.py`: helpers.
  They read the original applyIniOptions from `git show 56e988e:src/app/options.s`.

`python wip/aiodesign.py <dir>/a.c.042t.profile_estimate` regenerates the
overrides (src/app/options.prof).

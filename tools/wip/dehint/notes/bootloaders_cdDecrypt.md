# bootloaders cdDecrypt (queue 11)

Removed `__attribute__((optimize("no-tree-dominator-opts", "no-cse-follow-jumps")))`. No investigation was needed: the mechanism is cbDecrypt's, written up in `bootloaders_cbDecrypt.md` (uncprop's 0 on the clobber block's edge, cse1's path, null-return prediction). No new generator; no dumps run for this function.

## What changed

Same shape as cbDecrypt, by hand in src/bootloaders.c:

- `buf`, `len`, `key` declared at the top of the magic block
- the two good arms (signature OK, no key to check with) each `return buf`
- signature failure logs, calls `free(buf)` and falls out, with no `buf = 0`
- `if (buf) {...} else log alloc`
- every failure reaches the final `return 0`

Behaviour is unchanged: on signature failure buf is freed and the function returns 0, as it did with `buf = 0; return buf`.

The attribute's explanation moved from cdDecrypt's comment to ceDecrypt's, which said "as cdDecrypt". ceDecrypt's hints are untouched (queue 12).

## Result

- `python tools/wip/dehint/cbsweep.py tools/wip/dehint/gen_cb6.py`: 0 a=0 o=0 rd=1
- `python tools/re/fncmp.py src/bootloaders.c cdDecrypt`, no flags: MATCH
- Landed src/bootloaders.c's whole .s against the hinted reference (28bd769, build/cb/gen_cb6/ref.s, labels and literals normalised as in cbsweep.py, .p2align included): cdDecrypt equal (178 lines), all 19 functions equal, string list equal (33).
- fncmp MATCH for cfDecrypt, cgDecrypt, daeVerifySig, cbDecrypt, ceDecrypt.
- `sh build.sh`: SHA256 10dac648197fa5cdbb82d975ab9ff11f64075c9686908dfd9a33edc533f1971c, 0 differing bytes in every section, `cmp` with xeBuild.exe identical.

Nothing borderline: no flag, no redundant test, no `goto`. Same judgement call as cbDecrypt: `key` is one block further out than its innermost use, sitting with `buf` and `len`.

drafts/bootloaders_cdDecrypt_best.c is the landed src/bootloaders.c.
Reproduce: python tools/wip/dehint/cbsweep.py tools/wip/dehint/gen_cb6.py ; python tools/re/fncmp.py src/bootloaders.c cdDecrypt ; sh build.sh

## Next

Queue 12, ceDecrypt: see the look-ahead in `bootloaders_cbDecrypt.md` (gen_cb7: fncmp MATCH, a=1, one `.p2align 4,,10` missing).

# d1: mode_update de-hinting, attempt 1: MATCH, plain -O3

`match.c` is the whole object from `gcc -c -O3` with no `--param`, `__builtin_*`, asm, attributes, labels or goto. 14 of the README's 15 tricks are gone. `XB_PATCHES` stays (see below).

## Verification

`sh tools/wip/mu/d1/vlink.sh` (compiles match.c with `-O3`, compares with build/obj/mode_update.o, relinks build.sh's object list):

- `.text .data .bss .rdata .rdata$zzz .eh_frame`, relocs: SAME; `cmp` of the whole `.o`: identical.
- execmp: 0 differing bytes in every section and headers.
- SHA256 `10dac648197fa5cdbb82d975ab9ff11f64075c9686908dfd9a33edc533f1971c`.
- No asm output was removed in a way that leaves an uninitialized read: `code` is now initialized; `-Wall` warns only about the old netGetFile signedness.

p1's cmpo.sh, vlink.sh and ev.py still pass `-fno-toplevel-reorder` and the param, which build.sh no longer uses. Use mu.py and d1/vlink.sh.

## The source changes (`diff src/mode_update.c tools/wip/mu/d1/match.c`)

1. New `static void flashConsole(char *dumpDir, int *pret)` holds updateNand's success path (from `netUnmount` to the "image built" log), with a local `int ret = 0;`. updateNand has `if (!ret) flashConsole(dumpDir, pret); else {...}`.
2. The tail store: `if (ret) *pret = ret;`, with `int code = 0;` in mode_update (was `*pret = ret;`).
3. -ip arm: `i++; ip = argv[i]; if (i == argc || !argv[i] || *argv[i] == '-') {...}` (was `... || !ip || *ip == '-'`).
4. Removed: expect, `wok`, `werr`, `iperr`, `hu`, `dn` block, all cp, `#define cp`. noReboot is plain `if (!noReboot)`, writeImage plain `if (r)`.

Integration, if taken: copy match.c to src/mode_update.c; build.sh's case becomes `cflags="-O3"` and its comment goes; run `sh build.sh`, `python tools/re/progress.py`; README entry 1 shrinks to `XB_PATCHES`.

## Why it works (each line is one key fact)

Plain compile: 42 ev lines, cold order only, as p1 said. p1's "3 keys + a dummy" was the cheapest design under its key-only search, but the real keys are in priority form, and that opens another route.

- **bb_to_key has a priority form**: `-(1000000 + 100*e + f)`, e = edge freq from a trace-end pred, f = bb freq. At round 3's end 105 (`netUnmount`), 43 and 44 are all `-1000909`, 128 (buildImage error) `-1000506`. `pk.py` shows the target order needs 128 to pop no later than 105 (e128 >= e105), and nothing else: no dummy. `dsim.py` with a flat 105 key misled me for a while (see dead ends).
- **50/50 on `if (!ret)`**: 61% came from early return on the error arm only. A block that is one call right before the return block gets the same predictor, so with the success path in a helper both edges have early return and PRED_CALL: DS gives exactly 50%. 105 and 128 both become `-1000707`; they tie, and 128 pops first. All of updateNand's success path scales by .82.
- **-ip error to key 4**: FE folds `i == argc || !ip` to one test, so 2 edges at profile_estimate (0.04% each, freq 3). `!argv[i]` has a load, FE can't fold it, 3 edges, freq 4. The siblings already have that form. `ip = argv[i]` must come first, or the later test order differs (form c: 4 lines; form b, `!argv[i]` first: 6 lines).
- **writeImage error to key 1**: 2500 * .783 * .29 is 1.67, so key 2, and then bbro's triangle rule (`2 * freq(err) >= edge freq(sep)`) pulls the block into the trace (102 lines). `dumpDir`'s 78.3% is pointer 85 + call 29 + early return 61. Early return is there because the false edge goes straight to the return block. Making the tail not end right before return (`if (ret) *pret = ret;`) gives 69.8%: 1.49, key 1, so no `ok` flag is needed.
- **WARNING**: at f = .25 it is key 2 in the match (p1's 3 was only needed for its own heap shape). No expect, no param.

## Levers learned, for other objects

The pass attributions below (rebuild in inline_transform, SCCVN, no early threading, the triangle rule) are from memory of gcc 6 and fit what the dumps showed. I didn't read the sources, so treat the observed effect as the fact and the named pass as the likely cause.

- **Frequencies are recomputed from edge probabilities after inlining** (`TODO_rebuild_frequencies` in inline_transform; verified by a `pret` test whose dump scales but bbro keys don't). A test on a parameter that folds at inlining leaves no stale frequency. Stale needs folding after that: never-written static (ccp2), `*pret` with a local init (FRE).
- `if (!pret) return;` at the top is a fnsplit header: the partial-inlined body is renormalised and the scale cancels.
- **SCCVN in gcc 6 folds a repeated test of the same SSA name early**, so `if (ret)` inside `else` of `if (!ret)` is gone by profile_estimate.
- **No early thread pass in gcc 6**: `y = 0; if (c) y = 1; if (y != 1)` is still two tests at profile_estimate.
- **Opcode spelling lever (not used in the final, worth having)**: `int x = !c; if (x > 0)` gets PRED_TREE_OPCODE_POSITIVE (then-edge 64%, 73% seen with others), `int ok = !c; if (ok <= 0)` lowers it (36%; with PRED_CALL 18.7%). Both fold to the plain test later, in the same bytes. With a boolean `x`, `x != 1` / `x == 1` fold early and do nothing. This replaced `__builtin_expect` + param and the wok/cp hints in intermediate matches, and works as a general plain-C `__builtin_expect`.
- Early return: an edge straight to the return block is 39%; a block whose single succ is the return block (not next_bb) has its pred edges at 39%. A function's final if/else is always 39/61 unless both arms are like that.
- PRED_CALL scans the whole dest block, not only its head.
- Compile time is 0.3 s: 700 variants per minute. Sweep before modelling.

## Sequence of intermediate results

| State | tricks left | ev |
|---|---|---|
| strip all | 0 | 42 |
| drop `memset(argv,0,cp(i+106))`, `hu` (already dead) | 13 | 0 |
| -ip sibling form | 12 | 0 |
| `int reboot = !noReboot; if (reboot > 0)` (no expect, no param; -ip g1) | 10 | 0 |
| `int ok = !r; if (ok <= 0)` | 5 asm/builtin in dn, 2 flags | 0 |
| flashConsole helper: dn gone, reboot flag gone | `ok` flag, -ip goto | 0 |
| -ip c3 spelling | `ok` flag | 0 |
| `if (ret) *pret = ret;` | none of the listed hints | 0 |

## Dead ends (with numbers)

- Helpers for writeImage alone (gen3/gen4): err arm 39% (both arms call, PRED_CALL cancels) or next_bb to return. 36-116.
- Helpers for the reboot block (gen5): one arm always early-returned, trace flips or WARNING 2. 36-42.
- Dead `pret` tests to scale 105 (gen9-12, 42-100): top-of-function splits; after buildImage folds before the rebuild. Static never-written and `*pret` tests do scale (105 to -8) but the order stays wrong: the true requirement is 128 before 105.
- Redundant ret in the error arm (gen13): folded by SCCVN before profile_estimate, no change.
- `lev.py` exhaustive spellings over 6 tests (729 builds) with no helper: floor 42.
- Duplicated tail in the dump arm (gen18 dup_*): 18. `*pret = ret ? ret : 0`: 102 (no split at profile time).
- `updateNand` returning int (gen24): 305 (const return predictors, as tools/wip/README.md says). The out-parameter stays.
- `dsim` overrides replace ins and chg alike, so a flat key on a priority block means "no priority". Use `pk.py`'s P(e, f) form. br.py singles misread 105 this way.

## XB_PATCHES (not removed)

mode_update's own sites match without it with `(xb.files + xb.numPatches + XB_ADDONS)->name`. parseAddonIdx doesn't: floor 7 lines over gen20-23 (about 1180 builds, including `&xb.files[19].name[n*S]`, casts to array types and an overlay struct). The difference is at the copy: reference `xor eax,eax` on the not-entered loop path then adds the base after the join (PRE moves only `n*0x42c`); ours moves the whole address, `mov eax,base`. options.c keeps XB_PATCHES anyway, so the union stays in xebuild.h.

Next attempt, if wanted: find why the union's ARRAY_REF keeps the address together when the overlay's doesn't (`-fdump-tree-pre` on both).

## Tools (run in this dir)

- `python mu.py SRC.c [-f flags] [-t TAG] [-v FUNC] [-d]`: compile as build.sh does, per-function diff, section compare; -d writes dumps to build/v/mu_d1/TAG.
- `sw.py`: parallel runner; `python sw.py subsets`: all subsets of strip.py's removals.
- `diag.py SRC.c [TAG]`: ev + r4 pops with keys vs target order. `fo.py DIR [DIR2]`, `tr.py DIR`: final order, traces.
- `pk.py DUMP`: priority-form key search on the heap model. `br.py DUMP [p]`: flat key search. `ev128.py DUMP B..`: heap events of blocks. `fast.c`/`expev.py`: p1's annealer.
- `axes.py`, `gen*.py`, `gen16.py` FORMS, `lev.py`: sweeps; outputs in build/v/mu_d1/genN. `vlink.sh`: whole check.
- Write generators with the Write tool: Bash heredocs turn `\\n` into `\n`.

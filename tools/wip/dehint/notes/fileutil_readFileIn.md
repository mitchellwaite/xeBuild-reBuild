# fileutil readFileIn (queue 1)

Tools: `tools/wip/dehint/rfsweep.py <gen.py>` (parallel fncmp; prints lines differing, `r=` the
same with registers erased, whether cmp order and size/buf registers are right).
`tools/wip/dehint/iradump.py <file.c> [flags]` prints IRA threads, pop order with names.
Generators `tools/wip/dehint/gen_rf*.py`; outputs in build/rf/<gen>/.

## The reference

Hot path: calloc ok, size == 0, write *psize, return. Cold: align block, dir/name NULL
(own epilogue copy), read path, log path (own epilogue copy, xor-free), free path.
Registers: size=edi alloc=esi buf=ebx align=ebx(neg in place) path=ebp f1=esi f2=ebp;
psize lives in memory (spilled param).
`cmp eax,edi; jae`: the inlined `(size_t)getFileSize >= size`, canonical order from SSA versions.

## Author source (fetched)

cOzInABox/XeBuild tools/opt_idx/opt_idx/util.cpp FileToBuffer has this function's error message:
`FILE *inp; u8 *buf = NULL; u32 bRead = 0;` ...on malloc failure print and `bRead = 0`, else fread;
`if (size != NULL) size[0] = bRead; return buf`. So `u8 *buf`, a size var, nested ifs are likely.

## Findings so far

- Local integer types (size, alloc: size_t/long/int/unsigned), align spelling
  (two-step, one expr, `~(a-1)`, ternary, if/else) never change the output (gen_rf2).
- no-early-inlining alone changes nothing for the chain shape.
- Register problem is IRA (see iradump):
  plain pops size first (highest thread freq, 4759) so size=ebx. buf (r100) has 6 conflicts and
  caller-saved regs still "profitable", so it's trivially colorable, pushed early, popped late,
  then improve_allocation evicts psize for it (buf=edi).
  The reference needs buf non-colorable at the start so it pops before size: then buf=ebx.
  The hint's pin did this by restricting registers. Diagnostic gen_rf6: expects alone can reach the
  right registers but only with the read path hot (s=1 r=1), which breaks the layout:
  caller-saved stops being profitable for buf when (call freq crossing buf) * move cost > buf's mem cost.
- cmp order: `prephitmp_N` from PRE takes a name from the free list. `alloc = size` frees a low one
  in chain shapes (cmp wrong); ok-flag shapes (gen_rf5) get `cmp eax,reg; jae` right.
- Epilogue copies on L590/log path come out right in ok-flag shapes with `*psize = ok ? alloc : 0`.
- Don't retry: subsets of hints, six early-return shapes, gen_rf2 axes.

## Breakthrough: no size test in readFileIn (gen_rf9)

readFileTo already tests `size` and returns 0 for 0, so `readFileTo(path, buf, size) == size` needs no
`if (size)` in the caller. The buf != NULL arm then has a call at profile_estimate (this is what rf_hint
faked, against log_printf's PRED_CALL) and the size test comes in by inlining.
Result: size=edi, buf=ebx, alloc=esi with no pin (gen_rf9 `void|nest|ok_if`, 46 lines).
Remaining at that point: block order, threading of the psize tests, cmp order.

## State at the end of attempt 1: NO MATCH

Best by lines: drafts/fileutil_readFileIn_best.c, 32 lines (gen_rf10 `void|nest|nullfirst|two|nob|fp`).
It frees before writing *psize, which the reference doesn't do, so it isn't the likely shape.
Closest in order: drafts/fileutil_readFileIn_pf37.c, 37 lines (gen_rf14 `nest|bf|sep|int`):
right registers and cmp order, *psize before free. Check: python tools/re/fncmp.py <draft> readFileIn -O3 -Isrc

Two differences remain in the pf37 family, both GIMPLE threading:
1. Read-ok and size==0 each get their own `if (psize)`. vrp1 threads size==0 through the compare (path
   ends `(14,15) nocopy`, on the original join, PHI ok <1,0,0> with the failures), but can't thread read-ok
   because of the cast `(unsigned)(int)size`. dom2 threads read-ok later, so the copies differ.
   `size_t ret` in readFileTo (readFileTo and readFileInTo still MATCH) threads both in vrp1, but dom2 still
   makes two copies and the registers go wrong.
2. Log path keeps `*psize = 0; if (buf)` shared with read failure. Hinted dom3 registers (8,14)(14,16);
   the plain dom3 never tries the true arm of the log block's `if (psize)`. Cause not found. Dom walk order differs
   (hinted visits the log block before the else block, plain after); that link is unproven.
The missing L590 epilogue copy and block order probably follow from the frequencies once these are fixed (unverified).

Sweeps, none matched: gen_rf9 (40), gen_rf10 (1400), gen_rf11 (1680, ret type), gen_rf12 (1536, kept result
then test; `size == 0 || got == size` gets r=11 but wrong registers), gen_rf13 (96, flagless), gen_rf14 (648).
ok type (int/char/size_t) and nest vs or entry made no difference at the top of gen_rf14.
Two separate dir/name tests raise E to .934, the wrong way (gen_rf8). Non-void buf splits buf and return
value into a thread, but breaks uncprop's `mov eax,ebx` on the log path (gen_rf7).

Next: find why dom3 skips the log edge (read that dump, then gcc 6.2 tree-ssa-dom.c from the official repo
if needed); try shapes that make size==0 and read-ok one edge before vrp1.

## Attempt 2

- Dom3 question answered: `potentially_threadable_block` needs 2+ succs and 2+ preds. Hinted: `*psize = 0; if (buf)` is one
  block because dom2 already threaded read-fail + psize==NULL past the `if (buf)`. Plain pf37: `if (buf)` still has a second pred, so
  `*psize = 0` is a single-succ block and dom3 never tries it. So difference 2 is a consequence of the ok-flag threading in dom2.
- Why the ok flag can't get one `if (psize)`: vrp1 threads size==0/read-ok through the empty `ok = 1` arm as `(13,14)(14,16) nocopy`,
  so they bypass the arm's own thread. Flagless shapes (gen_rf13) have the reference's structure directly: r=14.
- `size_t ret` in readFileTo makes it early-split: its `if (size)` head is inlined at einline, so at profile_estimate the buf arm's first block
  has no call, the call heuristic lands only on the log arm and buf==NULL drops from 15% to 6.7% (log f=528, wrong layout). Keep `int ret`.
- Why log path gets `xor` instead of `mov eax,ebx`: DOM const-propagates buf==0 into the return PHI on the `if (psize)` false edge (`if (buf)` test
  directly gives 0B); crited1 splits that edge and dir/name-null's, tail-merge (end of PRE) merges the two empty forwarders into one (bb3), and uncprop
  can't see through it. Hinted source avoids it: `!ok && buf` is compound, so the PHI arg stays buf_23.
- gen_rf15 (no flag, common tail): right structure with `int ret`, wrong forwarder. Next gen_rf16: flag only on the failure tail.
- gen_rf17 (size/alloc types), gen_rf18 (shapes x every readFileTo spelling that still matches, tools rfsig.py): nothing better than 37; signature changes don't help.
  `int size` param breaks readFileTo itself.
- gen_rf19 (`if (ok)` outside `if (psize)`): fixes difference 1 (one psize test, 76 lines, 38 with regs erased, `bf|A`). Difference 2 stays: dom2 must already split read-fail's
  psize==NULL edge past `if (buf)` so dom3 can thread log. That needs read-fail isolated at vrp1, which the hinted source gets because sz0's edge skips the compare.
- Plain: sz0 goes (X,cmp)(cmp,okarm)(okarm,join) nocopy, because the `ok = 1` arm is empty, so it lands in the original join with read-fail. A non-empty true arm stops the
  thread at the arm, where read-ok also arrives. Next gen_rf20: true arm holds the *psize write.
- gen_rf20 (`*psize = alloc` in the true arm, `!ok && buf` free): `nest|c|ob|1`, 58 lines, 26 with registers erased: one `if (psize)`, separate log path, cmp order, `mov eax,ebx` on log all right.
  Left: (a) path/size swapped in ebp/edi (IRA: psize must pop before path, by thread freq), (b) dir-null's `xor ebx,ebx` crossjumps into free's tail. try_crossjump_bb only jumps from the lower-index block:
  when free comes after ret in the block chain (it was merged into a threaded copy of the join) F(dir-null) has the lower index. Hinted: free is the original block, before ret, so no crossjump.
- BREAKTHROUGH gen_rf22 `S|ob|mid`, 11 lines (drafts/fileutil_readFileIn_best.c): `char path[1024]` declared inside `if (dir && name) {`. Its clobber sits between the inner join and the return, so
  the free arm's NULL is an arg of an inner PHI and apply_return_prediction leaves the free test alone (null-return was pulling it to 4.3%).
- S|ob|mid's remaining 11 lines are exactly differences 1 and 2. IRA order and layout are right there. Other bodies fix 1/2 but lose IRA order: psize must outrank path's thread freq, and buf must outrank size's thread (4650).
- dom2 paths can only have a joiner at their first block, so read-fail reaching `if (psize)` through an `if (ok)` block ends the path at the original `if (psize)`. Next gen_rf23: failures jump straight to `if (psize) *psize = 0`, no flag test between.
- gen_rf24 `a|mid` (drafts/fileutil_readFileIn_flagless.c), plain natural source, no flag, scoped path: 46 lines but 12 with registers erased. The inner PHI also stops tail-merge joining log's and dir-null's forwarders.
  Left: (1) path/size swap: a1 psize must push after a6 path (psize freq too low without the threading noise); (2) cmp order (`prephitmp_18` low version; needs a version above `_39`); (3) fread trace before log: fread's block has f=3091 (ghost 39% from the folded
  `name && buf` tests of readFileTo; the cmp block keeps it and fread merges into it), log=1179. Round-3 heap takes the higher first. `ok = (read == size)` leaves fread at f=485 but needs a flag.
- gen_rf25 (flag forms x tails under scoped path): `err|sep` 12 lines, s=6 (build/rf/gen_rf25 v207): only log's `*psize = 0; if (buf)` left (plus a scratch register). dom2 registers for read-fail both (X,if psize)(.., ok test)(.., *psize=0 nocopy) and (X,if psize)(.. join)(join, free); per edge only one survives and the first (true arm of `if (psize)`) wins. If the false-arm path wins, the join loses read-fail's edge and dom3 can thread log. Registration follows EDGE_SUCC order of `if (psize)`: try `if (psize == NULL)` spellings (gen_rf26).
- gen_rf26: `if (psize == NULL)` spellings do flip read-fail's kept thread in dom2 (false arm survives), but then sz0 keeps its true-arm path, so `if (buf)` still has sz0's edge at dom3 start and `*psize = 0` stays a single-succ block.
- Constraints on any natural shape, worked out from the dumps (mem = sum(block freq of refs)/10*4):
  - IRA: buf's own freq must be >= size's a4 (3420, i.e. mem >= 13680), else size pops first (bx) and buf gets si. A psize mem above about 2280 makes psize pop before path, giving path=ebp (psize later spilled, size takes edi).
  - bb-reorder: epilogue copies need edge f>=1000: log's `*psize = 0` (15%*85% of 7861 = 1002, so buf==NULL must be exactly 15%: the call heuristic must cancel, i.e. readFileTo in buf arm's first block) and free->ret (>=12.7% at the free test).
  - log trace before fread trace: fread f<1000 (round 4), or read's second block f<1000. fread merges with the compare block, f=3091 (ghost 39%). `ok = (read == size)` keeps f=485.
- readFileTo spellings (sz, and, and2, and3 still match) give identical readFileIn output (gen_rf27): no use.
- psize refs: mem = sum(block freq)/10*4 - 4011, so psize needs sum >= ~15727. In flagless `a` the read-ok `if (psize)` is f=1871: 28% from PRED_OPCODE_NONEQUAL on `read == size`. Hinted has 3341 there, i.e. 50%, no prediction. A relational compare (`read < size`, `read >= size`) has no opcode prediction. gen_rf28 sweeps the compare operator.
- gen_rf28 `ge|23|h2|1|ob|mid` (drafts/fileutil_readFileIn_h2ge.c, `read >= size`): 50 lines, multiset register-free diff r=0, s=8. Everything is right except: path/size swapped in ebp/edi (psize refs too low to pop before path) and log/fread trace order.
- Trace order: fread (f=3091) beats log (1179) in round 3. The compare block keeps ghost 2606 (edges of the folded name/buf tests). Only readFileTo's own spelling sets it, and only `name && buf && size` matches standalone (all permutations and & forms tried, build/rf/a2/rfto2.py). If read-ok threads too in vrp1 the compare block dies and fread stays 485: needs no cast. `size_t ret` does that but early-splits. Next gen_rf29: `int size` local, so `(size_t)ret == (size_t)size` folds with `int ret` kept.
- gen_rf29 (`int`/`long` size): identical code, the cast doesn't fold. Drop.
- `nf|Dob` with `>=` (drafts/fileutil_readFileIn_dge.c), 35 lines, r=5: registers right, because `if (!ok && psize)` / `if (ok && psize)` are compound (no pointer heuristic), so their writes are f=3930 and psize reaches sum 15721. Threshold: psize sum >= ~15720 (a1 freq = sum/10 + 945, must reach path's 2517). A shape with no threading noise always sums to 14543. Case not yet tried: failures written in the arms, ok write in the tail (gen_rf30).
- gen_rf30 `s12|-|eq` (drafts/fileutil_readFileIn_s12.c): 40 lines but s=0: sequence identical with registers erased. Natural source: `int ok = read == size;` in the read arm, `if (psize) {if (ok) ... else ...}`, `if (!ok) { free }`. Only allocation left.
- gen_rf31 `nf|set|cce3|eq` (drafts/fileutil_readFileIn_best.c): 16 LINES: registers all right, the only difference is the fread block sits before the log block instead of after (8 lines moved). fread f=3091 beats log f=1179 in round 3. `val` form (`int ok = read == size`) keeps fread at 485.
- Two near misses: V1 `set|cce3` (16 lines, fread f too high) and V2 `val|nest` (s=0, psize and buf refs too low: psize mem 764, buf mem 13068). A value flag leaves fread at 485 because vrp1 can't thread through it and dom2 threads all three edges, so the compare block dies; but that takes refs off buf (needs mem>=13680) and needs psize mem>=~2280. `val|cce3` gets psize 2012, buf 13068. gen_rf32: value flag x psize forms x position x free forms.
- gen_rf32: nothing under 16 lines (best 19). `val|cce3` has GIMPLE like the reference with fread 485, but `prephitmp_18` has a low version, so `prephitmp <= _44`: cmp order wrong and a4 isn't colorable when it should be. gen_rf33 sweeps spellings of the size/alloc code on it to move PRE's name.
- gen_rf33: alloc spellings a0-a11, decl order: no change at all. Free-list view: `prephitmp_N` reuses the last released name; `_18 = size + align` is released when reassoc rewrites `size + align - 1`. Shapes with more thread copies before PRE use up the list (prephitmp_64/72 high = right cmp order), `val|cce3` doesn't.
- Why V1's psize passes: its test block is f=5578 (cmp's ghost). With fread=485 (val) the block is 2972, psize mem drops to 2012, threshold is in (2012,2280).
- gen_rf34: `size_t mask = align - 1` spelling fixes prephitmp's version in `val|cce3` (`p2|val|cce3`, drafts/fileutil_readFileIn_valmask.c: s=3, cmp right). Left: IRA. Same conflicts as V1; the difference is alloc's profitable regs: "has 6 avail" vs V1's 4. alloc's mem (9071) must be below its call-crossing cost or caller-saved regs stay profitable: V1 crosses fread at f=3091, valmask at 485. `val|nest` works because its `*psize = alloc` is f=1590, so alloc mem=8571.
- Why natural reference is probably in the value-flag family: log needs f>=1177 for its epilogue copy, and then read's second block is 1.056*log >= 1243, so it can't drop below 1000 as in the hinted source; only fread<1000 (compare block dies) leaves log before fread. So target: fread=485, alloc mem <= ~8571, psize mem >= ~2100-2280, buf popped first.
- gen_rf35: `a0|val|x2|==` (drafts/fileutil_readFileIn_x2.c): 32 lines, every one an ebp/edi swap of path and size. `if (!ok && psize) *psize = 0; else if (ok && psize) *psize = alloc;`. Only psize vs path ordering left; psize sum 11270.

### State at the end of attempt 2: NO MATCH, 16 lines

Best: drafts/fileutil_readFileIn_best.c (gen_rf31 `nf|set|cce3|eq`). Check: python tools/re/fncmp.py tools/wip/dehint/drafts/fileutil_readFileIn_best.c readFileIn -O3 -Isrc
No hints, readFileTo untouched:

    void *buf = NULL; size_t size, alloc;
    if (dir && name) {
        char path[1024];
        sprintf; size = getFileSizeName(path); alloc = size; if (align) {...}
        buf = calloc(alloc, 1);
        if (buf == NULL) { log_printf(...); if (psize) *psize = 0; }
        else {
            int ok = 0;
            if (readFileTo(path, buf, size) == size) ok = 1;
            if (!ok && psize) *psize = 0; else if (psize) *psize = alloc;
            if (!ok) { free(buf); buf = NULL; }
        }
    }
    return buf;

All registers and all instructions right; the only difference is the 8-line fread block placed before the log block instead of after it. Both it and drafts/fileutil_readFileIn_x2.c are hint-free; neither is in src/.

The two remaining failures pull against each other:
- Layout (log before fread) needs fread f<1179. fread merges with the compare block unless the compare is a value (`int ok = read == size`), f=3091 vs 485.
- Registers need psize sum >= ~15720 (pops before path) with alloc mem <= ~8600 (alloc's caller-saved regs unprofitable) and buf popping first. With f=3091 V1 gets psize mem 3244 and alloc avail 4 (fread's calls cross alloc). With f=485: `val|nest` and `val|x2` have layout and alloc right but psize mem 764/500; `val|cce3` psize 2012 but alloc mem 9071.
So what's wanted is a value-flag shape whose read-fail or test blocks carry the 2606 ghost onto psize (as `val|cce3`'s read-fail test 3710) with `*psize = alloc` at f<=~1670. `val|cce3`+`*psize=alloc` lower, or something moving 2-3k block freq onto psize refs.

Don't retry: size/alloc types, readFileTo spellings (only `name && buf && size` matches; sz/and forms match but give identical code), alloc spellings except `size_t mask` (which only moves prephitmp's version), decl order, ok's type, `if (psize == NULL)` spellings.

Findings worth keeping: `char path[1024]` in the `if (dir && name)` block is a real lever (keeps free's NULL in an inner PHI: null-return stops at the free test, and tail-merge can't join log's and dir-null's forwarders). Relational compare removes PRED_OPCODE_NONEQUAL (28% -> 50%). `if (ok)`-free threading rules in the bullets above. Tools: rfshow.py (s= sequence diff), rfcfg.py, rffn.py, rfdump.sh, rfsig.py.

## Attempt 3

- bbro: a block enters the heap only when a neighbour is visited; fread is pushed when compare block is visited (trace 12 13 15 16 18), key = -f. Log key -1179, fread -3091 (ghost: folded name/buf tests of readFileTo left 39% of the arm on the join). So the fix is to remove the ghost, not to change flags.
- gen_rf36: read code written in readFileIn itself (no name/buf tests): log is before fread at once (13 lines, `bf|got0|x9`; `nf|goto|g2` s=11). Remaining there: log's *psize=0 below the 1000 edge threshold (buf==NULL drops to 6.7% since the buf arm's first block has no call). Next gen_rf37: a static helper (call in the first block at profile_estimate, inlined at IPA) with no name/buf tests.
- gen_rf37 (static helper readData, no name/buf tests; a static function called once is never early-split, execute_split_functions skips it, so `size_t ret` works): `szt|nf|d2` (flagless `if (!(readData(path,buf,size) == size)) {...} else if (psize) ...`), 32 lines, r=0, s=16: every instruction and register right, buf==NULL 15%, log before fread, fread f=795. Only left: fopen block f=2605 so it runs in round 2, before dir-null's trace; it must be <2000. That needs P(size)*factor <= .299 of the 6682 arm, i.e. folded tests above the size test (each .78; one gives 2043, two 1589).
- gen_rf38 **fncmp MATCH with -O3 -Isrc** (`name && buf && size|bf|d1`, saved as drafts/fileutil_readFileIn_best.c): static `size_t readData(name, buf, size)` = readFileTo's body with `size_t ret`, called once (never early-split, so call stays in the arm's first block at profile_estimate: 15%), `size_t ret` lets vrp1 thread everything so the compare block dies (fread keeps its real f, ghost off), folded name/buf give fopen f=1589 (round 3). readFileIn: `if (buf) { if (readData(path, buf, size) == size) { if (psize) *psize = alloc; } else { if (psize) *psize = 0; free(buf); buf = NULL; } } else { log; if (psize) *psize = 0; }`, with `char path[1024]` scoped in `if (dir && name)`. Flagless. Concern: helper duplicates readFileTo. Next gen_rf39: get the same from readFileTo itself: `size_t ret` with a non-size_t return type (cast in return block blocks the split).
- gen_rf39 **MATCH without any helper**: `int readFileTo(...)` with `size_t ret` (return type int/long/int32_t x local size_t/uint32_t/unsigned/unsigned long all match; readFileTo and readFileInTo still MATCH, and the fnsplit dump for readFileTo says "Refused"), readFileIn calling it directly in the same flagless shape. The local must be unsigned (no cast on the PHI arg, so vrp1 threads) and the return type must differ from size_t (with size_t it early-splits; the reason it stops splitting wasn't traced further than the dump's "Refused: incoming frequency is too large"). So the gen_rf38 helper isn't needed. This replaced attempt 2's value-flag framing: no flag at all.
- Why it hits every constraint: buf==NULL 15% (call in the arm's first block at profile_estimate), log f=1179 and its write 1002 (epilogue copy), fopen f=1589 (round 3, after dir-null, from the folded name/buf tests), fread f=485 (compare block dies, so the ghost doesn't land on it: log before fread). Attempt 2's thresholds on psize sum and alloc mem weren't wrong but were only measured within flag shapes.

### Result of attempt 3: MATCH, landed in src/fileutil.c, not committed

`sh build.sh` gives 10dac648...971c. build.sh's fileutil case (`--param builtin-expect-probability=65`) is removed: fileutil.o was byte-identical with and without it, and no `__builtin_expect` is left in the file. rf_hint/rf_sink are gone. drafts/fileutil_readFileIn_best.c is a copy of the landed src/fileutil.c. Still in fileutil: the dead `'X'` test in myatou32 (queue 2).

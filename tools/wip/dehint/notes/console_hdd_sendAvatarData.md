# console_hdd sendAvatarData (queue 3)

Tools: `tools/wip/dehint/casweep.py <gen.py> [-v N]` (parallel fncmp plain -O3 -Isrc; outputs in build/ca/<gen>/; source replaces
prepSysex + sendAvatarData), generators `gen_ca*.py`, `caloop.py <file.c>` prints the send loop's assembly.

## Why the imul exists

Plain ivopts dump: pointer cand set costs 21, original-biv only 68, so no cost tweak reaches it (regs_used/pressure can't make up 47). So the index
must not be an IV at ivopts time. `for` with a global count: `do_while_loop_p` says the load+cond header is already do-while so ch doesn't copy it (`jmp` to the test).

## Sweeps

- gen_ca1 plain: 47 lines (r=17), pointer IV.
- gen_ca2 (336: access forms idx/arith/ptr/bytes/off/intaddr x index local types x loop forms): no imul, ever. Don't retry.
- gen_ca3 (189: k = narrow cast, &, %, min/max, abs...): `for` shape keeps the imul with a real movzx/cmov, proves the register plan (ebx/esi/ebp) follows once scev is blind.
  do-while shapes: vrp1 removes & / max / abs (i>=0 known) before ivopts, so no imul. Anything removed must go after ivopts.
- gen_ca4 flag-driven loops (i advances only on success, `i += ret != 0`, `ret && i < count`): threading through the loop header is refused until after the loop passes, so scev sees PHI<i,i+1>: imul kept with no hint.
- gen_ca5 (864): `u|ifelse|and|gd|ifret|p0` 12 lines r=0: `uint32_t k = i` in the loop body (k keeps i dead after `i+1`, so i and i+1 coalesce), `if (ret) i++; else log` and `while ((i < count) & (ret != 0))`.

## State of the 12-line shape (drafts/console_hdd_sendAvatarData_best.c = gen_ca5 v424), two differences
1. `xor ebp,ebp` hoisted above the guard. IF-CASE-2 in ce1 (else block `i=0`, else_prob 73% > 50%). Hinted source has the preheader falling through (case 2/1 refuse). Here the chain is guard, MF, preheader, body because crited1 splits both critical edges into MF (guard skip, `if (ret)` on the loop exit), tail merge in `pre` merges those two forwarders, and "Merging blocks 37 and 18" puts MF at the forwarder right after the guard. Guard expect p=50 stops the hoist but flips the layout (so not prob<=50).
2. Block order mount failure vs loop failure: 25/25 tie create vs mount failure.
prepSysex spelling (gen_ca6 p0..p8) doesn't help: same results or worse.
- gen_ca7 (1008) post-loop tests keeping i live until dom3 (`if ((i >= count) & (ret != 0))`, `if (i >= count && ret)`): hoist gone (gen_ca7 v71 11 lines, v4 12 lines). Only mount-failure order left (+ residual in v71, addTitleId cmp in v4).
- Diagnostic (cadiag.py, expect on netMount): target P(mount success) 79..81% only. DS of early return .61 and call .71 = .793, so look for a prepSysex whose mount failure gets both heuristics and whose success arm has no guarded call.
- CA_DIAG=80 casweep.py: same sweep under the diagnostic.
- gen_ca10 h10a|add|i_ret|wh|and_ge (v85, drafts/console_hdd_sendAvatarData_best.c) fncmp MATCH, plain -O3: prepSysex `uint32_t r = netFormatSysex(); if (!r) log; else { r = netMount(); if (!r) { log; return 0; } } if (r) r = createSysexDirs(); return r;` gives mount fail 10 / create 40 (call + early return, .793, no guarded call on the success edge).
- That prepSysex (uint32_t r) didn't match standalone. `int r` spellings do; gen_ca11 (4320): h9d|add|and|gd1|and_ge|u (v3718): prepSysex + sendAvatarData + everything MATCH. drafts/console_hdd_sendAvatarData_best.c. addTitleId cmp order is SSA numbering (free list); tail `(i >= count) & (ret != 0)` with do-while `(i < count) & (ret != 0)` got it.
- Literal order: the reference's `sending manifest` literal comes before the loop's, so MF is before the body in the expand chain: that's the tail-merged F1 shape (`if (ret)` tail), so the hinted asm "i" was standing in for this. and_ge family (F2) has MF after the loop: .rdata wrong (8 text 16 data lines), although fncmp MATCH (gen_ca11 v3718).
- gen_ca12 v0 (`plain|add|i_ret`, `if (ret)` tail, h9d prepSysex): .rdata identical, only `xor ebp,ebp` hoisted (2 lines). Saved as drafts/console_hdd_sendAvatarData_f1.c.
- ifcvt.c 6.2.0 read for this: find_if_case_2 won't speculate if `cheap_bb_rtx_cost_p` fails; max_cost is COSTS_N_INSNS(BRANCH_COST(.., predictable_edge_p)), and BRANCH_COST is 0 if predictable (prob >= 98%). Diagnostic: f1 draft + expect on the guard: p<=97 2 lines, p>=98 **0 lines**. So target: guard >= 98%. freeManifest's for-loop guard is 99% (copied header of a single-exit loop, PRED_LOOP_ITERATIONS_GUESSED), so the natural source of 99% is a copied loop header. gen_ca13.
- Natural 99% needs guessed iterations: single exit plus an always-executed array access on a scev-visible index at profile_estimate (freeManifest gets it), but a flag-advanced i isn't an IV, so it can't happen in the flag family. gen_ca13: copied-header guards reach 91% only.
- gen_ca14: F2 with the manifest send lexically before the loop (goto), a test of whether chain order is all that's left.
- gen_ca14 (576, manifest send lexically before the loop via goto): 13+ lines, no use. Don't retry.

## State at the end of attempt 1: not landed, src/ and build.sh unchanged

Two drafts, each with exactly one thing wrong, in opposite places. Neither has `__builtin_*`, asm, attributes or `--param`; the align-loop-iterations param isn't needed by either.

**drafts/console_hdd_sendAvatarData_f2.c** (F2, gen_ca11 v3718): `python tools/re/fncmp.py <draft> sendAvatarData -O3 -Isrc` MATCH; prepSysex, addTitleId, freeManifest, sendDir, sendCompatData and the rest also MATCH. Object: .rdata differs (loop literals before the manifest literal), .text only in those literal offsets. Can't land.

**drafts/console_hdd_sendAvatarData_best.c = _f1.c** (F1, gen_ca12 v0): .rdata .data .bss byte-identical; .text differs only by `xor ebp,ebp` hoisted above the guard (fncmp 2 lines). **Diagnostic: f1 + `__builtin_expect(manifest.count > 0, 1)` with --param builtin-expect-probability=98 gives .text .rdata .data .bss byte-identical to build/obj/console_hdd.o.** So in F1 the guard not being speculated is the one thing left, and F1 is the shape to finish.

Shape, as in f1:

    int prepSysex(void) {
        int r = netFormatSysex();
        if (r) { r = netMount(SYSEX, "\SEP"); if (!r) { log mount; return 0; } }
        else log format;
        if (r) return createSysexDirs();
        return 0;
    }
    ...
    if (manifest.count > 0) {
        i = 0;
        do {
            uint32_t k = i;
            log_printf(..., i + 1, manifest.e[k].len, manifest.e[k].len, manifest.e[k].path);
            ret = netSendFile(...e[k]...);
            if (!ret) log fail e[k].path;
            i += ret != 0;
        } while (i < manifest.count && ret);
    }
    if (ret) { manifest send as before }

What each part does, and how far it can be defended:
- `i += ret != 0` (flag-advanced i): i is PHI<i,i+1> until dom3 threads it (threads through the header are refused in vrp1/dom2), so scev can't see it at ivopts: this is what keeps the imul with no hint. It's real logic, odd spelling. `if (ret) i++` also keeps the imul, but in F1 with `&&` gives more lines (gen_ca12 `ifelse|and`, `&` in the loop test: 6 lines).
- `uint32_t k = i`: **borderline.** Reads as an index copy, but its only job is to leave i dead after `i + 1`, so i and i+1 coalesce into ebp. Without it i takes eax or the like (gen_ca5 `i` rows 29+ lines). No purpose other than steering can be given for it.
- `r` flag in prepSysex with the second `if (r)`: **mildly borderline**, reads as ordinary code. It removes the guarded call on the mount-ok edge, so call .71 + early return .61 = .793 (diagnostic window 79..81%).
- F2 only: `(i >= count) & (ret != 0)` is redundant with the loop test and only keeps i live to dom3, the same kind of steering.

Mechanisms worked out:
- Reference chain has MF before the body (literal order): crited1 splits guard->MF and `if (ret)`->MF, tail merge in pre merges the two forwarders, "Merging blocks" puts MF after the guard. The old literal asm stood in for this.
- That needs MF with no PHI, so i can't be live at MF (PHI args would differ and the forwarders wouldn't merge). So the old `__asm__("" :: "r"(i))` can't be how the original did it, and F1 and i-live are mutually exclusive.
- find_if_case_2 (ifcvt.c 6.2.0) speculates else block `i = 0` unless: else prob <= then prob and no postdom (diagnostic p<=50: stops it but flips layout, 41 lines), or not cheap (predictable_edge_p, prob >= 98%: BRANCH_COST 0), or >=3 insns in the block at 73% (max 12*(7300+1250)=102600, each insn 40000), or else block not single pred/succ, or i live at then.

What to try next (F1, stopping the speculation):
- Guard >= 98%. Natural 99% is PRED_LOOP_ITERATIONS_GUESSED on a copied header (freeManifest): needs single exit and an always-executed array access on a scev-visible index at profile_estimate. A flag-advanced i isn't an IV, so look for something that's an IV at profile_estimate (042t) and stops being one before ivopts (154t). gen_ca13 copied headers only reach 91%. Also possible: threading rescaling the guard's edge probabilities if the guard has a second pred (update_bb_profile_for_threading); not tried.
- 3+ insns in the preheader at ce1 that later vanish, or a preheader with a second pred or succ until after ce1. Look at the ce1 dump of the preheader. Not tried beyond reasoning.

Don't retry: access forms and index local types with a plain IV (gen_ca2), cost-based imul (68 vs 21 in ivopts), prepSysex with a guarded call on the ok edge (gen_ca6, gen_ca9), goto lexical order (gen_ca14), copied-header guards (gen_ca13).

Tools added: casweep.py (CA_DIAG=<p>), caloop.py, catrace.py (bbro traces), cachain.py (block chain per pass), cafreq.py, cadiag.py, caobj.py, caboth.py. Generators gen_ca1..gen_ca14.

Verdict: NO MATCH. F2 gets fncmp MATCH with no flags, but its `.rdata` is wrong and both `uint32_t k = i` and the redundant `i >= count` exist only to steer gcc, so it does not meet the README criteria. Best is F1 at 2 lines, which still has `k`. `sh build.sh` was not run: object sections were compared with build/obj/console_hdd.o instead. Earlier bullets naming drafts/console_hdd_sendAvatarData_best.c as gen_ca5 v424 or gen_ca11 v3718 are out of date: _best.c is now F1.

## Attempt 2

Read find_if_header/find_if_case_1/2 (ifcvt.c 6.2.0). The hoist needs then = the block the guard falls through to; case 1 refuses when then falls through to its successor, case 2 refuses when else has 2 preds. Probe of guard probability (expect + param on f1): p<=52 flips the layout (41-43 lines), 53..97 2 lines, >=98 0 lines. Cost route: one insn is 40000 vs 12*(p+1250), so a single insn is never expensive above 50%; two would need p<=54.
**New mechanism (chain, not probability):** expand_gimple_cond makes the FALSE edge the fallthrough when neither successor is next in the chain. So guard `if (count <= 0)` (false = preheader), with some unrelated block Z next in the chain, then MF, then preheader, body: then = preheader, which falls into the body, so case 1 refuses; else = MF with 2 preds, so case 2 refuses. Literals stay right because MF is still before the body. Prototype build/ca/a2/z1 (Z = the cleanup block, MF head lexically before the loop, its arms after): xor ebp right and .rdata identical (fncmp 15 lines; left: `mov edi,1` for createSysexDirs failure hoisted, since crossjump of [edi=1] onto the OK arm's tail no longer fires with OK not falling into OUT).
gen_ca15 (MF inside the loop at its head, `while (ret) { if (i >= count) {MF; break;} ...}`): no header copy (do_while_loop_p: empty latch, load+cond header), 36+ lines. No use.
Z must be multi-pred or it merges into its predecessor (gen_ca17, prep blocks after the guard: merged away). With Z = cleanup block the OK arm no longer falls into it, and crossjump only redirects a whole [edi=1] block when it has the lower index (createSysexDirs is at chain end since vrp1's thread): gen_ca16 (144, prep spellings) 11 lines.
gen_ca18 (MF head in the loop, `for (i = 0;; i += ret != 0) { if (i >= count || !ret) { if (ret) {MF head; goto check;} break; } ...}`, arms after the loop): .rdata right, no `k` needed, 19 lines (hoist, i/i+1 not coalesced: latch i+1 is a dom3 thread copy). Copied header but the old header merges with the thread copy at chain end, so it isn't Z.
gen_ca19 (explicit `if (count <= 0) goto mf` + head-tested loop): e|fora|k2 (v13) 2 lines r=0, .rdata right: same xor hoist as F1. Forwarders guard->MF and test->MF tail-merge in pre, so MF lands right after the guard again.
gen_ca20 (guard goes to a post-loop test that keeps i live, so forwarders don't tail-merge): dom3's thread copy of the test swallows MF at chain end, .rdata wrong. gen_ca21 (guard jumps into the loop past the head test): pointer IV, up to 96 lines. Don't retry either.
**gen_ca22 le|a|forb|k1 (v2, drafts/console_hdd_sendAvatarData_z.c): .rdata .data identical, xor ebp right, 4 fncmp lines: only the latch `cmp [count],ebp; jg` vs reference `cmp ebp,[count]; jl`.** Chain guard, loop test, manifest head, preheader, body. The `goto send` before `mf:` puts a block with no edge to MF (the `if (!ret) break`) right before MF, so crited1 places the guard's forwarder there and not right after the guard (split_edge_bb_loc). `i += ret != 0` before the failure log leaves the latch empty, so the loop test isn't thread-copied. cmp order: gimple `if (_26 <= _31)`: swapped by SSA version (load is numbered before i + 1 because the head test dominates the body). Moving on: gen_ca23, compute i + 1 before the test.
gen_ca23 (i + 1 before the head test), gen_ca24 (432 spellings): cmp order doesn't move. The head test's load is numbered before anything in the body because it dominates it, and `i_new >= _load` gets swapped on copy-prop.
**A read through a small static accessor is inlined with a fresh, higher SSA version. Head test `i >= itemCount()` on the gen_ca22 shape (build/ca/a2/h1.c = drafts/_best.c): fncmp MATCH, caobj text 0 data 0.** Next: remove what can go (gen_ca25), then land.
gen_ca25 (240): the accessor can be `itemCount()`, `itemsDone(i)` or `moreItems(i)`; `i += ret != 0` before the log is the only increment at 0 lines (`after` 2 lines; `if (ret) i++` and the if/else forms 15+); no index local at all: 15+ lines (i isn't threaded the same way).
k replaced: `e = &manifest.e[(uint32_t)i]` or `(size_t)i` 0 lines; no cast 15 lines (lea, i not coalesced); `manifest.e + i` 28; casts inline with no e 41.
gen_ca26 (36, plainer heads): `while (ret)`, `if (ret && more) goto send`, `if (!ret) break` first: 48+. Without `goto send_item` the guard's forwarder lands after the guard (2 lines). `if (0) { mf: ... }` also gives 0 but is a dead test: rejected.

## State at the end of attempt 2: MATCH, landed in src (not committed)

`python tools/re/fncmp.py src/console_hdd.c sendAvatarData` MATCH with no flags, prepSysex MATCH, `sh build.sh` SHA256 10dac648...971c, both --params and the console_hdd case gone from build.sh, no __builtin/asm/attribute left in the file. drafts/console_hdd_sendAvatarData_best.c = landed src/console_hdd.c. src/xebuild.h: the manifest entry struct got a tag (`struct manifestItem`).

Mechanism, in full: see src/console_hdd.c's comment and tools/wip/README.md. Guard >= 98% wasn't the way: no natural source reaches it (goto + call + opcode = 93.9%, guessed iterations needs scev at profile_estimate, 5 exits gets 98%). The chain was.

Borderline, for review:
- Loop control: `if (count <= 0) goto send_manifest;` then `for (;;)` with labels send_manifest and send_item inside it, `goto send_item` right before send_manifest. Live code, but nobody would lay it out this way unprompted. The guard is redundant with the head test.
- `itemsDone(i)` accessor used only in the head test: its one job is the SSA version that decides the cmp operand order.
- `e = &manifest.e[(size_t)i]`: the cast is redundant; it replaces `k`, same job (i dead after i + 1).
- `i += ret != 0` before the failure log, then `if (ret) ... / if (!ret) ...` tests at the loop head: real logic, odd spelling.
- `sent` local with arms after the loop: only so the arms' literals come after the loop's.
- prepSysex's `r` flag and second `if (r)`.

Try next, if the loop control is rejected: gimple chain needs a multi-pred block between guard and manifest send plus the false edge to i = 0; only the loop test qualifies so far. An alternative for the block before send_manifest (now `if (!ret) goto out; goto send_item`) is the place to look.

## Retry later: landed, but not natural yet

The user reviewed the attempt 2 candidate on 2026-11-02 and had it landed as is, with a note to try again.
It has no builtin, asm, attribute or --param and the full build matches, so a retry has to keep all of that.
What it doesn't have is believable source. The goal of a retry is to replace these with what the author likely wrote:

1. `for (;;)` with `send_manifest` and `send_item` labels inside it, entered by `goto`. It sets the block order
   (guard, loop test, manifest head, `i = 0`, body), which stops find_if_case_1 and _2 speculating `i = 0`.
   The manifest's position also puts its literal first in .rdata.
2. `static int itemsDone(int i)`: only changes an SSA version, for `cmp i,count` over `cmp count,i`.
3. `&manifest.e[(size_t)i]`: the cast only leaves `i` dead after `i + 1`, so they coalesce.
4. `i += ret != 0` before the failure log: keeps the imul (scev can't see i until dom3) and an empty latch.
5. `sent` local tested after the loop: the `break` and arm positions only set literal order.
6. `int r` in prepSysex with a second `if (r)`: gives P(mount success) = .793. Same kind as myatou32's approved
   `hex` flag, so this one can probably stay.

Targets a natural source has to hit: the block order in item 1, mount success at about 79-81%, imul kept, manifest
literal before the loop's. Attempt 1's `_f1.c` is the most readable near miss: 2 fncmp lines, only `xor ebp,ebp`
hoisted above the guard, right .rdata. Starting from it is probably better than simplifying the landed shape.

Compare with `python tools/wip/dehint/caobj.py <draft>` as well as fncmp, against a build/obj/console_hdd.o from
the landed source, and finish with `sh build.sh`.

## Attempt 3

No aggregate locals anywhere in sendAvatarData, prepSysex, addTitleId or freeManifest (loadManifest isn't inlined), so no scope clobbers: the scoping lever doesn't apply here unless an aggregate is invented.
gen_ca30 (840; inlined helpers sendItem(i) / sendItem(e, n) / sendManifest x natural loops x increments): imul kept in 252, best 9 lines (pn|dga|add|if), still the hoist plus i/i+1 not coalesced. A late-inlined helper does not change the chain.
gen_ca31 (`while (ret)`, MF at the head): vrp1 threads the ret test away, so header is load+cond with exiting latch pred: no ch copy, 33+.
gen_ca32 (`i >= count` first, MF inside it): same no-copy, 31+.
gen_ca33 (head `if (i >= count || !ret) { if (!ret) goto out; MF; sent = ...; break; }`, `if (!ret) log; i += ret != 0;` at the end): **ch copies the header**, so the guard comes from the natural loop test. 19 lines r=3 (v89): only hoist + no coalesce. Chain at dom2 is guard, H, T, MF, pre, body as wanted; crited1 then moves MF after the guard because T (`if (!ret)`) sits right before MF and has an edge to it (split_edge_bb_loc).
That needs a block with no edge to MF lexically right before it. In C that is either a block with real statements (`if (!ret) { stmts; goto out; }`) or a jump over MF (the landed `goto send_item`).
gen_ca34 (the item failure's log as that block, in the `if (!ret)` at the head): the chain is right and the hoist goes (xor after the guard), but the abort literal then expands before MF (.rdata wrong) and without the join at the body's end the head isn't copied or the latch tests i before ret: 36+. There's no other statement available for that block: anything with a literal breaks .rdata, and the shared `out` code can't be repeated there.
gen_ca35 (copied head plus jumps over MF, no entry goto, no accessor): `if (i < count && ret) goto send_item; if (!ret) goto out; MF; break; send_item:` + cast + `if (!ret) log; i += ret != 0;` (v105, drafts/console_hdd_sendAvatarData_a3label.c): 8 lines, r=2: the hoist plus cmp order in addTitleId and freeManifest (SSA numbering). .rdata right. Two-test head with the block before MF (`A`, v100): 30, because `if (!ret) log; i += ...` makes dom3 thread-copy the loop test to the chain end, so the Z block dies before expand and it hoists anyway.
The conflict in one line: ch copies the head only if the latch's predecessor doesn't exit at ch, which needs the failure arm unthreaded at vrp1 (a statement in the join, `addl`); Z survives to expand only if the join is empty so dom3 doesn't thread-copy the head (`add`), and with `add` vrp1 threads the failure arm and ch sees a do-while.
gen_ca36 (separate `ok = ret != 0` that the head tests, so vrp1 can't thread from a `ret` test; 288): `inl|d|A|brk1` v106 keeps Z (the fail arm still reaches the head's test in gimple, and RTL removes that test) and has no hoist and no cast, 14 lines; but `i += ok` stays setne + add since dom3 can't tell ok from a `ret` test. Testing ok for the log folds it and loses Z again. Not better than the landed text anyway: two labels plus another flag.
gen_ca37 (landed text with one part replaced): accessor -> named local n (function, body or block scope, either compare order), plain test: all 4 lines (`n_25 <= _31`: into-SSA numbers in dominator order and the head dominates i + 1, whether temporary or named). Only an inlined callee gets a later version. Cast -> u32 0 lines (same thing), plain or `+ i` 15+, `num = i + 1` local 9. So no part of the landed text can go on its own.
gen_ca38 (528; `while (ok)` over the MF head, a header of only a condition is never do-while to ch): 31+, setne stays and the ok test stays. Don't retry.

Per part, what attempt 3 learned:
1. for(;;) with labels: the entry goto can go (ch copies the head in gen_ca33/35), but then Z is lost; the `goto send_item` jump-over is needed for split_edge_bb_loc in every shape that keeps Z. Not replaced.
2. itemsDone: not needed in the copied-head family (cmp is right there, drafts a3head and a3label). In the landed explicit-guard family only an inlined callee reorders it. Not replaced in src.
3. (size_t) cast: an item pointer doesn't do its job (`e = &manifest.e[i]`, body local or not: i not coalesced, in F1 12 lines; a pointer or i + 1 passed to an inlined sendItem likewise, 9). Not replaced.
4. `i += ret != 0`: `if (ret) i++` variants all get threaded at vrp1 into a plain IV in the head-tested shapes (imul lost). Not replaced.
5. `sent`: reads fine in the copied-head drafts (`sent = netSendFile(...); break;` then `if (!sent)` after the loop, or with `goto out` for the item failure). Item failure must skip the manifest's arms, and arms in place put the success literal before the loop's. Stays.
6. prepSysex's r: stays, as expected.
Scoping: no aggregate in sendAvatarData or anything inlined into it, and none can be added without changing frame or steering. No clobbers to move. Inlined helpers (gen_ca30): static sendItem and sendManifest inline with the same chain; they renumber SSA but don't move blocks, and don't help the hoist.
Also read: the guard's 95.5% in the E head is first-match PRED_LOOP_EXIT, (100% - 91%) / n_exits. predictable_edge_p (2%) needs n_exits >= 5 at profile_estimate (floor 2%), which is attempt 2's "5 exits gets 98%". Natural sources have 2-3 exits, and the extra tests must fold after 042t. A body failure `goto out` gives a third. Not reached.

## State at the end of attempt 3: no change, landed source stays

src/console_hdd.c and build.sh untouched. drafts/console_hdd_sendAvatarData_a3head.c (gen_ca33 v89) is the most natural text so far: no labels but `out`, no accessor, no entry goto, no cast, the guard comes from ch. 19 fncmp lines, r=3: hoist, and i/i+1 not coalesced. .rdata right. drafts/console_hdd_sendAvatarData_f1.c stays the fewest lines of the readable shapes (2), with `k`.

Try next, only with a new idea: a natural block with no literal and no edge to MF between `if (!ret)` and the manifest send in a3head; or something other than Z that stops find_if_case_2 (guard edge >= 98%, EDGE_LOOP_EXIT on the guard's edge: find_if_header refuses those, and a dirty successor block in ce1). Not tried: anything that puts the guard inside an enclosing loop.
Don't retry: gen_ca31, 32, 34, 36, 38 families.

Evidence: chains, PHIs and the 4.5% are from dumps. split_edge_bb_loc's rule, the do_while_loop_p conditions, the PRED_LOOP_EXIT formula and find_if_header's EDGE_LOOP_EXIT refusal are from memory of gcc's source (none read in this attempt); the first three agree with the dumps, the last is untested.
Full build run at the end of attempt 3: SHA256 10dac648...971c.

## Attempt 4: landed, no labels but `out`, one dead test

Tools: casweep.py now writes every row to build/ca/<gen>/results.txt. cachains.py <file.c> [pass...] dumps a draft and prints the block chain per pass, RTL's ce1 lines at the end. Generators gen_ca40-55.

### The result

src/console_hdd.c: fncmp MATCH with no flags, caobj text 0 data 0, `sh build.sh` SHA256 10dac648...971c. drafts/console_hdd_sendAvatarData_best.c is a copy of it.

    i = 0;
    n = manifest.count;
    ok = 1;
    for (;;) {
        if (i >= n) {
            if (!ret)
                goto out;
            if (ok <= 0) {            /* dead */
                netTimerEnd();
                goto out;
            }
            log manifest; ok = netSendFile(manifest...); break;
        }
        if (!ret)
            goto out;
        e = &manifest.e[(size_t)i];
        log; ret = netSendFile(e...);
        ok = ret != 0;
        n = manifest.count;
        i += ok;
        if (!ret)
            log failure;
    }
    if (!ok) {...} else {...}

Gone from the landed text: `send_manifest` and `send_item` labels, the entry `goto`, `itemsDone`, the `sent` local (ok doubles as it).

### What was new: the count in a local, reloaded before the failure test

Attempt 3's conflict: ch copies the head only if the latch's predecessor doesn't exit at ch (needs an unthreaded failure arm, a statement in the join), and H stays in the chain only with an empty join. Caching the count breaks it, for two separate reasons. Each is from the dumps.
- do_while_loop_p is false for a header of only a condition. With `n` in a local, the head is `if (i >= n)` with the load elsewhere, so ch copies it however vrp1 threaded the failure arm (gen_ca45).
- Where the reload sits decides where H ends up. Reload at the loop bottom (gen_ca45): a block with the load falls into H, they merge at that block's place, and H is gone from the spot after the guard (hoist, 2-4 lines). Reload before `if (!ret)` (gen_ca47): H's only predecessor is the conditional block, nothing merges, and H stays between guard and manifest send. `i += ...` before or after the reload makes no difference. In this shape the cmp orders in sendAvatarData, addTitleId and freeManifest all came right with no accessor.

gen_ca47 `cast|none|Nadd|B|brk0` (`if (i >= n) { if (!ret) goto out; manifest...; break; } if (!ret) goto out; ...`) is fncmp MATCH with no dead test, but .rdata is wrong: dom2 threads the `if (!ret)` on the manifest path, MF is merged into the thread copy at the chain's end, and the manifest literal comes last (caobj text 12, data 32). drafts/console_hdd_sendAvatarData_a4nodead.c. Same class as F2.

### What the dead test does

`ok <= 0` after `if (!ret)` keeps MF in place. Folding timeline for the name, from cachains.py:
- FRE, vrp1: can't. A different PHI from ret, and ok's assert doesn't come from the `ret` test. `failed = !ret` and `ok = !ret` (`bang`) don't work: dom2 folds them (cond `ret == 0` is the same expression), and MF moves as in the no-dead shape.
- dom2: leaves it (ok set before the test, as `(int)(ret != 0)`).
- crited1: its block is in front of MF with no edge to it (split_edge_bb_loc), so the guard's forwarder lands there.
- sink moves ok into the success arm, dom3 folds it to 1 and the test goes. No thread copy of H, so H is still in place at expand.

Frequency: with `if (!ok) goto out;` MF is 5 (H exit 20, ret test .61 from early return, ok test .39 from early return + call against the send). Text is right apart from the arms: bbro round 3's threshold is 10, MF pops in round 4 and extends into the failure arm (gen_ca50, 10 lines, r=2). `<= 0` adds opcode positive: 9, still one short (gen_ca51, 10 lines). A call in the dead arm cancels the call heuristic: 10, MATCH (gen_ca53). The arm can be the abort log, `ret = 0` + log, netTimerEnd() or freeManifest(); all the same bytes (its literal is dead code, so it isn't emitted). `if (sent) goto ok_arm` also fixes the fallthrough (gen_ca52, 4 lines), but addTitleId's `mov eax,1` block is then placed before the failure arm, and only MF >= 10 gets both.

### Dead and redundant tests, exactly

- `if (ok <= 0) { netTimerEnd(); goto out; }`: **dead.** ok is 0 only when ret is 0, and ret was tested just above. Has a comment in src. Steers: chain position of the guard's forwarder, MF's frequency.
- `if (!ret) goto out;` on the manifest path: **redundant, not dead in the source's terms.** i doesn't advance on failure, so i >= n with ret 0 needs the count to shrink. Needed: without it (gen_ca48) the failure arm keeps a real `cmp` on the way out. Reads naturally.
- `ok <= 0` is an unusual spelling for a 0/1 flag.
- `ok = ret != 0` beside ret: only exists for the dead test and `i += ok`. `i += ret != 0` gives the same bytes (`okNr`).

Others left, unchanged in kind: `(size_t)i` (without it 15 lines, r=3, i and i + 1 not coalesced; `uint32_t k = i`, `(uint32_t)i` are the same bytes as the cast), `n` as a local (reads naturally, though nothing can change the count mid-loop), arms after the loop (literal order), prepSysex's r.

### Other things tried

- gen_ca40: the shared cleanup written out in front of MF (`if (!ret) { netUnmount; freeManifest; return 0; }`): freeManifest is inlined, tail merge can't join the return values, 67+. Don't retry.
- gen_ca41: `failed = !ret` for the head and `i += ret != 0` with the plain count: the head's test stays until RTL, but the failure arm threads only after sink, so setne stays (14, r=8). Chain right, MF at the end.
- gen_ca42: `if (i < count) {...} else {manifest}` with no n: 15, r=3. Hoist, since dom2 copies H to the chain's end.
- gen_ca43: `continue` for the dead test: a second back edge, no ch copy. Don't retry.
- gen_ca44: `sent = ret` (nop conversion): FRE sees the same value, same result as `ret`. Don't retry.
- gen_ca46: failure leaving from the body (`if (!ret) { log; goto out; }`): loop exit prediction, so the success arm is 97% and sink (threshold 75%) won't move i + 1 there: setne stays (30+).
- gen_ca48: no ret test on the manifest path: see above.
- gen_ca55: one ret test before H (`tfirst`), the call on the ret test instead (`tm_t2`), `||` of the two tests, `while (ret)`, all 16+. Only `base` matches, `eT` (else form) 2 lines.
- F1's guard >= 98%, the user's first angle: nothing in a folded test can reach it. The guard edge's probability comes from predictors on that edge alone; a test after the guard moves frequencies, not this. Only n_exits >= 5 on a copied head would, so 3 dead exits. Not run: more dead tests than this result has. The lever worked here on MF's frequency instead.

Evidence: chains, frequencies and predictor values are from dumps. do_while_loop_p, split_edge_bb_loc, the sink threshold and bbro's thresholds are from memory of gcc's source (none read this attempt) and fit the dumps; the threshold of 10 is also backed by block 14 [10] popping in round 3. "Sink moves ok, dom3 folds it" is inferred from the test and setne being gone after dom3.

### What to try next

Removing the dead test: something else that keeps MF from merging into dom2's thread copy in the gen_ca47 `B` shape. MF needs another predecessor at dom2, or the `!ret` on the manifest path has to survive dom2 by itself, with a frequency of at least 10 at MF. drafts/console_hdd_sendAvatarData_a4nodead.c is the start. Removing the cast: nothing new, attempt 3's list stands.
Don't retry: the list above; attempt 3's families without n.

Reproduce: python tools/re/fncmp.py src/console_hdd.c sendAvatarData ; python tools/wip/dehint/caobj.py src/console_hdd.c ; sh build.sh ; python tools/wip/dehint/casweep.py tools/wip/dehint/gen_ca53.py (also 45, 47, 54, 55); python tools/wip/dehint/cachains.py <file.c>

## Attempt 5: dead test still landed; two new forms without it

Tools: caobjbest.py <gen> [N] runs caobj on every sweep row with at most N fncmp lines (fncmp alone can't see .rdata). Generators gen_ca56-73. Draft fncmp needs `-O3 -Isrc` from outside src/.

### Landed

`struct manifestItem *e` moved into the loop body, same bytes, SHA256 10dac648...971c. drafts/_best.c is a copy. The dead test, `(size_t)i`, `ok` and `for (;;)` stay.
gen_ca71: with the dead test, `(size_t)i`, `size_t k = i` and `uint32_t k = i`, with or without e, and `i += ok` or `i += ret != 0`, are all text 0 data 0. The arm can be netTimerEnd() or the abort log, with `<= 0`. `!ok` is 10 lines (as in attempt 4) and `i = n` with the dead test is 6+.

### drafts/console_hdd_sendAvatarData_a5while.c: the natural text, 2 fncmp lines

gen_ca72 cast|wh|iN|ifret, tidied. Plain `while (i < n)`, one result variable, no dead test, no labels, no goto, no flag; the manifest handling sits in `if (ret)` after the loop. caobj data 0, text 30: the `xor ebp,ebp` hoist and the addresses it shifts. Declaration order counts: `int i; long ret; int n;` here, while `int i, n; long ret;` also flips freeManifest's cmp (text 34).

    i = 0;
    n = manifest.count;
    while (i < n) {
        struct manifestItem *e = &manifest.e[(size_t)i];
        log; ret = netSendFile(...);
        n = manifest.count;
        i += ret != 0;
        if (!ret) { log failure; i = n; }
    }
    if (ret) { log manifest; if (!send) { ret = 0; log } else { log; netTimerEnd(); ret = 1; } }

What's new is the one loop exit (gen_ca67). A failure ends the loop through `i = n`, so the head is the only exit: PRED_LOOP_EXIT gives it 9%, not 4.5%, and the manifest block is 15-16, past bbro's 10, with no dead arm (attempt 4's 5 -> 10 problem is gone). No cmp is left on the failure path (attempt 4's gen_ca48 problem). `.rdata` is right the F1 way: the forwarders tail-merge in pre and the send lands after the guard, which is also why the hoist happens. `n = 0` in place of `i = n` (z1) is 20 lines, r=8; `if (ret) i++` with `i = n` (z3, z7) is 37+.

Borderline in it: `(size_t)i` (`size_t k = i`, `uint32_t k = i` are the same 2 lines), `n` reloaded and cached (nothing can change the count in the loop), `i += ret != 0` next to `i = n`, prepSysex's r.

### drafts/console_hdd_sendAvatarData_a5labels.c: no dead test, text 0 data 0, not landed

gen_ca64 cast|le|J, tidied (J4 and either caller body also match). Patch from the landed text: drafts/console_hdd_sendAvatarData_candidate_a5.patch. fncmp MATCH for sendAvatarData and prepSysex, caobj text 0 data 0; `sh build.sh` not run on it. Not landed because README names this shape as a candidate: a `for (;;)` entered through a label. It has `if (n <= 0) goto send;`, `send:` and `item:` inside the loop, and a static helper holding everything after addTitleId. **The user's call whether this beats the dead test:** nothing in it is dead, but more of its structure is there to steer.

How each part works, from the dumps:
- Second predecessor (gen_ca57). The entry goto gives the send a real edge from the guard, so dom2's copy doesn't swallow it and it stays in place. .rdata right.
- Positive `if (ret) goto item;` in front of the send (J). The dump has it as `_40 != 0`, the `_40 = ret != 0` that `i += ret != 0` computes, and dom2 doesn't thread it from the body's `ret == 0`. So this block survives to crited1, has no edge to the send, and the guard's forwarder is placed in front of the send (split_edge_bb_loc). It does the dead test's chain job with live code. The `if (!ret)` spelling (X head) is threaded by dom2, and the send lands after the guard (hoist). Worth remembering: **the two senses of a ret test are two values while `ret != 0` is also computed.**
- The helper. vrp1 threads the guard edge past the head (n > 0 and i = 0 mean i < n), and the head's PHIs i_1, ret_2, n_5 are gone by dce2. ch2's copies then have those low versions, and addTitleId's `_2 == ver_14` swaps the cmp (gen_ca58, 2 lines; no spelling in gen_ca59 or gen_ca60 moves it). Inlined from a helper, the PHIs have versions above ver's. The helper must include the else arm and the join: when the send arms (gen_ca61, gen_ca62, 4 lines) or the cleanup (gen_ca63, 34 lines) end the helper, early return (39%) lands on the manifest failure and the arms go from 8/8 to 6/10.

gen_ca66 cast|Q1|add (no entry goto and no helper; `if (i >= n) { if (ret) goto send; goto out; } if (ret) goto item; goto out; send: ...; break; item:`): .rdata right, no hoist, 10 lines, only the arms off because the send's block is 8. gen_ca73 (`ok > 0` for opcode positive, `if (sent)` first): 7 lines at best (`sent1`), 17+ with `ok > 0`. If something brings that block to 10, it's a match with two labels, no entry goto, no helper.

### Literal order idea

a4nodead's text 12 is only literal addresses, so the code is right and only the manifest literal is late. But the literal has to be expanded after `sending %d items` and before `sending %03d`, and only a block in that stretch of the chain can do that. A local `const char *` is propagated to its use, and a static helper expands where it's inlined (gen_ca30 had the same chain). A PHI of literals would expand ahead of the whole function (from memory of expand's order, not tested). None of this was swept. Don't retry without a new way to reach that stretch.

### Other things tried

- gen_ca56 (`!ok` or `ok <= 0` as the manifest path's only test, two exits): 17+.
- gen_ca65, gen_ca66 positive `if (ret)` on the manifest path, or in the body with the head negative: P1, B|elseN, B|cont have data 0 and 12 lines (hoist, arms off, send at 8).
- gen_ca69 (one exit, `!ok` as the head's test): dom2 sends the guard edge straight to the send (the chain shows it), the forwarders merge, hoist. 4 lines at best (`early`, which also flips addTitleId's cmp).
- gen_ca68, gen_ca70 (ok is the result, success arm doesn't assign it, hoping for a PHI at the send that stops tail merge): the PHI's constant is already 1 at crited1, so nothing stops the merge. 2 and 6 lines.

### What's left, for a5while

Only find_if_case_2's speculation of `i = 0` (conditions from attempt 1's read of ifcvt.c and memory):
- A block before the send with no edge to it: can't exist in a `while`. The send is lexically after the body, and only the forwarder right after the guard puts it before the body's literals. It needs the send inside the loop's head, which needs `for (;;)`.
- Guard >= 98%: a loop with one exit could now get PRED_LOOP_ITERATIONS_GUESSED, but that needs an array index scev can read at profile_estimate, and a real IV loses the imul at ivopts. It would need something that's an IV at 042t and stops being one by ivopts. A helper's profile is estimated before inlining, which is the one lever not fully explored; nothing tried.
- A trapping insn in the preheader (dead_or_predicable refuses) or 4+ insns there at ce1, gone by final: no natural source found.
- A PHI at the send whose arguments differ at pre and fold after it: needs a value VRP1 can't see but dom3 can. `ok` fails since its range is 0..1.

Don't retry: gen_ca56, 60, 63, 68, 69, 70 families; n = 0 as the stop.

Evidence: chains, frequencies, predictor values and SSA versions are from dumps. split_edge_bb_loc, find_if_case_2, dead_or_predicable's trap check, the early-return rule and predict_loops' single-exit rule are from memory of gcc's source (none read in this attempt) and fit the dumps. That ch2 reuses the freed PHI versions, and that vrp1 rather than dce2 frees them, are inferred from version numbers. Why dom2 leaves `_40 != 0` alone is inferred from it surviving.

Reproduce: python tools/re/fncmp.py src/console_hdd.c sendAvatarData ; python tools/wip/dehint/caobj.py src/console_hdd.c ; sh build.sh ; python tools/re/fncmp.py tools/wip/dehint/drafts/console_hdd_sendAvatarData_a5while.c sendAvatarData -O3 -Isrc ; python tools/wip/dehint/caobj.py tools/wip/dehint/drafts/console_hdd_sendAvatarData_a5while.c tools/wip/dehint/drafts/console_hdd_sendAvatarData_a5labels.c ; python tools/wip/dehint/casweep.py tools/wip/dehint/gen_ca72.py ; python tools/wip/dehint/caobjbest.py gen_ca72 2

## Attempt 6: natural match, landed

src/console_hdd.c: fncmp MATCH with no flags for sendAvatarData and prepSysex, caobj text 0 data 0, `sh build.sh` SHA256 10dac648...971c. drafts/_best.c is a copy. This supersedes the "Retry later" list and attempts 3-5's what-to-try lists: labels, `ok`, the dead test, `n`, the cast, `i += ret != 0` and `itemsDone` are all gone. The `struct manifestItem` tag from attempt 2 went too.

    long ret = 1;
    ...
    for (i = 0; i < manifest.count; i++) {
        log_printf(1, "sending %03d: ...", i + 1, manifest.e[i].len, manifest.e[i].len, manifest.e[i].path);
        ret = netSendFile(manifest.e[i].path, manifest.e[i].data, manifest.e[i].len);
        if (!ret) {
            log_printf(0, "aborting ...", manifest.e[i].path);
            i = manifest.count;
        }
    }
    if (ret) { log manifest; if (!send) { ret = 0; log } else { log; netTimerEnd(); ret = 1; } }

### How it was found

- gen_ca80 (360; the task's idea, i live after the loop): `i >= n && ret`, `ret && i >= n` and `(i >= n) & (ret != 0)` fold to a5while's bytes, 2 lines, the hoist. Without `ret` in the test (`i >= n`, `i == n`, `i == count`), or with `break`, 19-58 lines. So i-live post-loop tests didn't work. The sweep's useful row was a side effect: `wh|big|ret`, failure `i = n + 1`, had **no hoist**, data 0, 11 lines.
- gen_ca81 (192): the failure arm uses the old n, with the reload only on success, so the load sinks past the ret test: text 4, and `if (ret) i++` works, so `i += ret != 0` isn't needed. Left: the inlined freeManifest's cmp order.
- gen_ca83 (162): `i = n` with i++ in a `for` step is `n + 1` for free. No cast needed. Text 4.
- gen_ca85 (1920) G rows: drop n altogether, `for (i = 0; i < manifest.count; i++)` with `i = manifest.count`: text 0 data 0. The cmp order came right by itself.
- gen_ca86 (432): `long ret = 1` at the top in place of the two `ret = 1` assignments, text 0 data 0.

### Mechanism, from the dumps

Failure path at dom3: `i_34 = manifest.count; _72 = i_34 + 1; if (i_34 > _72)`. No pass can fold that until forwprop4 ("Replaced 'i_34 > _72' with '0'"). That one fact does all three jobs:
- imul: at ivopts the head's i is a PHI of i + 1 and the failure path's value, not an IV. `break` removes that path and gives a pointer IV (39 lines, `-imul`).
- Hoist: at cddce2 the loop has two latch edges (success and failure). The chain goes from `14 guard, 15 MF, 16[35], 17[359], 18 body` at vrp2 to `14 guard, 15[35], 16 MF, 17[359], 18 body` at cddce2, so `i = 0` sits right after the guard. a5while's `i = n` is `n > n`, which folds at dom2, so it has one latch at cddce2, keeps guard, MF, `i = 0`, and gets hoisted.
- .rdata: at `pre` the chain is still guard, MF, body (forwarders merged, the F1 way), so MF stays ahead of the body at expand and the literals are in order.

From memory, not read: cddce's loop_optimizer_init (LOOPS_NORMAL) merging the latches and rebuilding the preheader with split_edge, which would explain why the block moves. That the move is what stops ce1 is inferred: the xor is right, and ce1 still prints "IF-CASE-2 found, start 12, else 15" without hoisting; the refusal itself wasn't traced.

Why dropping n fixed the cmp is not understood beyond the versions: `prephitmp_62 > i_67` (lower version first) where the n forms had `i_71 < prephitmp_99`.

### Left in the source

- `long ret` next to `int netSendFile`: needed, `int ret` is 2 lines (comment in src, from earlier attempts). Reads fine.
- `i = manifest.count` to stop, not `break`: needed. Live, ordinary code.
- prepSysex's `r` with the second `if (r)`, item 6 of the retry list: live, same kind as the approved `hex`. The flag-free spellings (gen_ca86 s1-s6) are at best 10 lines, the mount failure and loop failure arms swapped. Don't retry without a new way to get .793.

Variations with the same bytes: `struct manifestItem *e = &manifest.e[i]` in the body, `if (ret == 0)`, `ret = 1` at both old spots, `long ret; int i;`, prepSysex h5d or h1d.

Reproduce: python tools/re/fncmp.py src/console_hdd.c sendAvatarData ; python tools/wip/dehint/caobj.py src/console_hdd.c ; sh build.sh ; python tools/wip/dehint/casweep.py tools/wip/dehint/gen_ca86.py ; python tools/wip/dehint/cachains.py src/console_hdd.c vrp2 cddce2 forwprop4 optimized

## Review (2026-11-10): both borderline shapes approved, no code change

The user asked for the two console_hdd borderline items to be reviewed and settled. Both stay as they are, with `(approved)` added to their tags. Compared with `python tools/wip/dehint/caobj.py` against build/obj/console_hdd.o; the counts below are caobj text lines (addresses included, so one changed instruction shifts everything after it).

### sendAvatarData's long

- Only the local's type counts. `int sendAvatarData` with `long ret` is text 0. An `int`, `uint32_t`, `unsigned`, `unsigned long` or `_Bool` ret is 314-745.
- **sendCompatData needs long in both places.** An `int` return with `long ret` is 94, `long` return with `int ret` 135, `int` for both 202, `uint32_t` for both 199. These are real code differences (frame 0x18 vs 0x28, registers), not addresses. sendCompatData was never tagged, so this is the author's type for these results, and `long` for both in sendAvatarData is the same form. Recorded in a comment above sendCompatData.

### sendAvatarData's `i = consoleManifest.count`

No new test: attempt 6 swept the stops (`break` 39 lines, pointer IV; `n = 0` 20). It's live, ordinary code, an older idiom for leaving a `for` loop.

### prepSysex's r

New spellings, on top of gen_ca86 s1-s6 (10 lines at best) and gen_ca10's heads:
- Flag-free, `if (!format) {log; return 0;} if (!mount) {log; return 0;} return dirs();`: 1014, data 148. The nested form with `return dirs()` after both tests: 1004.
- Fully chained, the mount failure without its early return (`r = mount; if (!r) log;` then `if (r) r = dirs(); return r;`): 784. The mount failure's early return is needed.
- Same bytes as the landed form: `if (r) r = createSysexDirs(); return r;` (the textbook status chain), `return r ? createSysexDirs() : 0;`, `return r;` in the mount arm, and `int ok = 0; ... ok = 1;` after the mount test. The landed form was kept, since it's the shape of the approved `hex`.
- Why no flag-free form can work, from predict.c's heuristics as the attempts measured them: P(mount success) .793 is the call heuristic (71) and the early-return heuristic (61) together on the mount failure. If `createSysexDirs()` sits in a block guarded by the mount test, its edge gets the call heuristic as well and the two cancel. So the call has to come after a join with the format-failure path, and that path must not call it, which needs a value that carries the format result past the join.

Scratch generator for these (not kept): string replacements on src/console_hdd.c fed to caobj.py.

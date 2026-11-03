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

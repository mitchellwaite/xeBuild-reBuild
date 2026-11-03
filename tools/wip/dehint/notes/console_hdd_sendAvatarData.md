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

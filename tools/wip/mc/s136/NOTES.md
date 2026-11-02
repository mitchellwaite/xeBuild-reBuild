# s136 (attempt 117): NO MATCH. Floor stays 18 (s117/best.c).

s134's gen.py/climb.py ported to best18. base18.c = s117/best.c + `int kk = __builtin_constant_p(argc);`
(mode_client) and `int kk = __builtin_constant_p(block);` (clientEraseBlock): still 18. Levers use `kk`
(best18 has block-local `k`). gen.py reads GBASE (default base18.c); nonin.py N = top-N distinct-asm
non-inert singles -> nonin.json; run_rest.sh = pairs + 4 SA chains per base. Same 28 cold feed targets
filter as s134 (6340 singles per base). ~38.7k real compiles (v/, nma_2/v, rb_ifelse/v *.res).

## best18 (base 18, 7 hunks)
- Singles 6340: floor 18; 1980 at 18, two at 18/5 hunks (dead `if (kk) goto` between the hdd4/hdd5
  error stmts, lines 755<->761); next 19.
- Pairs over 100 distinct non-inert singles (4950): floor 18. SA 4x450 over 4000 singles: all end at base.
## nma_2 on best18 (base 22): singles/pairs/SA floor 22.
## rb_ifelse on best18 (base 26): singles reach 18 via feed from the duplicated reboot log (606) to 597/737,
  but the asm diff is byte-identical to best18's (it just undoes rb_ifelse). Pairs 18/5 (same hdd4/hdd5
  feed); SA chains: one 18/7, three stay 26.
## Remaining diff (best18 and the 18/5 variants)
Common to all: u2 `mov eax,[l]; jmp l` (ref 503) and the usage(5) block (4 insns, ref 542 vs 560) -- the
known stuck u2/usage5 placements. Variable part near ref 421-465: best18 misplaces a
`l(2,0)` call block + `[8+esp]=ebx` store; the 18/5 variant instead misplaces a log_printf+jmp block. No
lever fixes both, or touches the u2/usage5 hunks.
## Semantics
kk = __builtin_constant_p(runtime value) = 0: `t&&!kk`==t, `kk||t`==t; labels/hot/cold no-ops; `if (kk) goto`
dead; empty asm goto falls through. nma_2 (`!arg||!mode`) and rb_ifelse (log duplicated into both arms)
are equivalent (s135). All equivalent to src/mode_client.c.
## Conclusion
The lever family is exhausted on best18 and its two restructurings too: floor 18, residual is the u2/usage5
pair plus one block in the 421-465 region.

# d2: mode_update without XB_PATCHES: MATCH

`match.c` is the whole object from plain `gcc -c -O3`, no `XB_PATCHES`, nothing else added. The spelling is `(&xb.files[n] + XB_ADDONS)->name`, where d1 used `(xb.files + n + XB_ADDONS)->name` (10 lines, 7 without nops).

The same spelling also makes options.c byte-identical without the define (`options_match.c`, flags unchanged), so no object needs the union any more. Nothing outside this directory was edited.

## Verification

`sh tools/wip/mu/d2/vlink.sh tools/wip/mu/d2/match.c`:

- `.text .data .rdata .rdata$zzz .eh_frame`, relocs: SAME. `.bss`: the object has none on either side. `cmp` of the whole `.o`: identical.
- execmp: 0 differing bytes in every section and headers.
- SHA256 `10dac648197fa5cdbb82d975ab9ff11f64075c9686908dfd9a33edc533f1971c`.
- build/obj/mode_update.o is current: `vlink.sh src/mode_update.c` gave identical bytes first.

options_match.c, `#line 1 "options.c"`, `-O3 --param builtin-expect-probability=83`: `cmp` with build/obj/options.o identical (unmodified src/options.c compiled the same way is identical too). Not relinked, as the object bytes are the same.

## The diff (`diff src/mode_update.c tools/wip/mu/d2/match.c`)

- `#define XB_PATCHES` removed.
- `xb.patches[i]` -> `(&xb.files[i] + XB_ADDONS)->name` (1 site).
- `xb.patches[xb.numPatches]` -> `(&xb.files[xb.numPatches] + XB_ADDONS)->name` (3 sites; the 2 -a sites match with either spelling, this one is used everywhere for consistency).

No dead or redundant test. The code is in bounds and means the same as the union view.

## Why (from the dumps)

Tree dumps were compared for the union (`dref`), d1's overlay struct (`dov`) and the match (`dmatch`), with `-fdump-tree-all -fdump-tree-pre-details`.

The difference starts in the front end, and PRE only makes it visible:

1. **Which form the index has.** The union keeps an ARRAY_REF with an **int** index until `laddress`: `_48 = &xb...patches[_84]`. `xb.files + n`, `->name[n]` on a cast pointer, and `(*(T*)p)[n]` all arrive as pointer arithmetic with a `(sizetype)` cast by 006t.omplower (the overlay: `D = (sizetype) n; &xb.files[19] + ...`). So d1's overlay struct was not an ARRAY_REF by then, whatever the source looked like. That is why all of d1's casts tied at 7.
2. **FRE merges that cast with the loop test's.** `i < xb.numPatches` has `_41 = (unsigned int) _40` in the latch. In the pointer form the address's cast value-numbers to `_41`, so ch2's PHI after the loop is over the unsigned: `PHI <_41(12), _72(9)>`.
3. **dom2 knows that value is 0.** The loop guard at dom2 is `if (_66 != 0)`, so on the not-entered edge `_66` is 0 and the PHI becomes `PHI <_41(13), 0(9)>`. In the union form the PHI is over the int, `PHI <_40(13), _34(9)>`, dom2 doesn't substitute `_34`, and the `(sizetype)` cast doesn't exist yet.
4. **PRE then differs.** Overlay/pointer: `{mult_expr,_86,1068}` translates to a constant on the entry edge, so the multiply and the whole address are partially redundant and PHIs go in for them: `PHI <_91(15), &xb.files[19](9)>`, which is the `mov eax,base`. Union: laddress makes `_71 = (sizetype) _84`, only that nop is partially redundant, `PHI <prephitmp_96, _66(9)>`; `_66 * 1068` isn't available, so mult and add stay after the join. `_66` becomes 0 at dom3: the `xor eax,eax`, then `imul`, `add base`.

So what has to hold: the index is a plain int ARRAY_REF index on a real array of `xb`, and the 19 entries are not in that index. `xb.files[n + 19]` keeps the int index but puts the addition in it: 106 lines (`g1.py`'s iplus).

laddress then produces `(sizetype) n * 1068 + constant` on `&xb`, the same constant whichever way the 19 is written. So `&xb.files[n]` followed by a constant offset gives the union's exact tree from `laddress` on. dmatch's PRE log has the same `Replaced (sizetype) _86 with prephitmp_108` as the reference and no created PHI for the multiply.

The reason `&xb.files[n]` isn't turned into pointer addition by the front end while `xb.files + n` is one from the start was seen in the dumps only; I did not read the GCC sources.

## Results (`g1.py`: parseAddonIdx sites only; -a sites keep d1's spelling)

| name | spelling | lines | whole object |
|---|---|---|---|
| idx | `&xb.files[n].name[XB_ADDONS * sizeof(struct fileent)]` | 0 | same |
| plus | `xb.files[n].name + XB_ADDONS * sizeof(struct fileent)` | 0 | same |
| cplus | `(char *)&xb.files[n] + XB_ADDONS * sizeof(struct fileent)` | 0 | same |
| splus | `(&xb.files[n] + XB_ADDONS)->name` | 0 | same (taken: in bounds, shortest) |
| sidx | `(&xb.files[n])[XB_ADDONS].name` | 0 | same |
| cidx | `&((char *)&xb.files[n])[XB_ADDONS * sizeof(struct fileent)]` | 0 | same |
| iplus | `xb.files[XB_ADDONS + n].name` | 106 | no |

For comparison: d1's pointer form 10 lines; d1's overlay struct 7 lines. The first sweep (7 shapes) was enough, once the dumps said what to aim for.

## Levers learned, for other objects

- `&a[n] + K` keeps `n` an int ARRAY_REF index until laddress, while `a + n + K` has `(sizetype) n` from the start. Those are different expressions for FRE, dom and PRE: use the former when a PHI over the index should stay over the int.
- Pointer forms expose the cast to FRE, which merges it with any `(unsigned) n` nearby, such as a `i < n` loop test on an unsigned `i`.
- `->name[n]` through a cast pointer is not an ARRAY_REF at gimple level, so an overlay struct is not the same as a member array of the decl.
- Check 006t.omplower first to see what the front end really produced.
- To find the first pass where two sources differ, normalise SSA numbers (`trace.py` shows one expression per pass) rather than reading diffs: numbering differs from `.original` on.

## Dead ends

None beyond iplus. d1's gen20-23 shapes are explained by the above, not repeated.

## Tools (run in this dir; dumps in build/v/mu_d2)

- `mu.py`, `vlink.sh`: d1's, with paths changed. `python mu.py SRC.c -t TAG -v _parseAddonIdx` (the function name needs its underscore, or -v prints nothing). `sh vlink.sh tools/wip/mu/d2/match.c`: whole check.
- `dump.sh SRC TAG`: all tree and rtl dumps, plus PRE details, in build/v/mu_d2/TAG.
- `fnd.py A B PASS` (run in build/v/mu_d2): cuts parseAddonIdx out of a pass's dump to `A.PASS.fn`, `B.PASS.fn`.
- `trace.py DIR REGEX` (same): matching lines of parseAddonIdx, printed per tree pass when they change.
- `g1.py`: the table above. `ref.c`: src/mode_update.c at 397dad86. `base.c`, `ov.c`: d1's pointer and overlay forms.

## Integration, if taken

- Copy match.c to src/mode_update.c, and options_match.c to src/options.c if wanted; line numbers in the rest of the file shift by the removed define, which doesn't matter to the bytes.
- With both, remove the union and `padPatches`/`patches` from src/xebuild.h and rewrite its comment (it says mode_update's loop only compiles to the original's code that way, which is no longer true). If options.c keeps the define, the comment still needs that fix. Also NOTES.md's line on which files use it.
- README's "Compiler tricks": mode_update reaches 0, so remove its entry, renumber and update the count, per CLAUDE.md. Check whether options' entry mentions XB_PATCHES.
- Run `sh build.sh`, `python tools/re/progress.py`.

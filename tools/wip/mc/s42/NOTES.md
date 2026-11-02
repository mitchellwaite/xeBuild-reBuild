# s42: bcp-goto lever scans for the 53/77/79 insertion events (plain compile, no profile)

Result: NO MATCH. Best content-clean variant is still H5b.c (copy of s41): 5 inv / fncmp 40 / cm (0,8).
Flags: -Isrc -O3 -fno-toplevel-reorder -fno-ipa-profile -fno-reorder-functions --param builtin-expect-probability=50.
About 42k real compiles, all with race-free tags (tt.tid). Tools were copied from s40 (mc40 -> mc42). build/v/mc42 was deleted.

## Tools
- lev.py: one lever = a new label `zqT:` on statement line T of the option loop plus
  `if (bcp(i+N)==1 [&& ...nt]) goto zqT;` inserted before site line S. Sites are the 85 statement starts after a
  `;{}` line (no unbraced if bodies); targets are the 108 statement starts. It records the true inversions (ev.py)
  and the insertion signature of 53/77/79 from the slot history (hsim). It can be resumed.
- lev2.py: multi-lever builder plus a beam (score 10*inv + cm lines). cmc.py: content check (cm.py) for moved
  signatures. anl.py: signature histogram. shp.py: (c) sinking shapes.
- The H5b signature is `2:1038:ins/next/53, 3:53:push, 4:55:ins/this/77, 4:55:ins/this/79`.

## (a) Exhaustive single-lever scan (levA.jsonl: nt=1, all 9095; levB2.jsonl: nt=2,3, targets 642-700, 8256)
- The insertion events DO move. 164 levers put 77/79 at 61 (round 4), 128+ put 53 in round 1 (1037/1038),
  and others put it in round 3, round 4 (at 49) and so on. These are the first real insertion moves found.
- 77/79@61: best 3 inv (e.g. site 599 (-noenter) -> target 676 (`arg = argv[++i]` in -r), also 601/604/606 ->
  672/674/676/677). Order: `... 42 53 79 77 ...`. But every one has cm >= 10: the -r arm's i+1 swaps
  eax/edx registers (5 mov/lea/cmp lines), and fncmp is 58.
- 53 in round 1 (any site -> 643, the -eb usage(3) test): content-clean (0,8) but 6 inv.
- No lever with a moved signature is both content-clean and below 5.

## (b) hsim relocation ranking (rel2.py, rel2_b0.log, rel2_chk.log)
- On H5b, the best single relocation is 79@61 (3), then 77@55 or 77@61 (4). The best double, 79@61 + 77@61,
  gives 2 (`53 77 79`). Lever (a) realises the 77+79@61 move (3, order 79 77).
- On the moved base (chk599676) the only further gain is 77 relocated within 61's group (2). The remaining
  `126 125 55` vs `55 126 125` is not an insertion problem, so relocations cannot fix it.

## (c) Sinking shapes (shp.py, shp.log)
- Sharing usage(3)/(5) of -eb/-ip with -r/-w/-e/-c (goto zu3/zu5 at the loop end, top or middle) changes
  content (31,12+) and gives 11-34 inv.
- Sinking only -r/-w/-e/-c is neutral: (0,8), 5 inv, and the signature is unchanged.
- A switch rewrite was not tried because it necessarily changes the code (switch on a char).

## (d) Beams on the moved bases (lev2.py, 1 round each, about 9.1k compiles each)
- bmB (from [599,676,1], 3 inv / cm 10): best stays 3 inv / cm 10. No second lever restores the -r arm
  register allocation (min cm 10 at inv <= 6).
- bmA (from [606,643,1], clean 6): best (5, cm 2) and (4, cm 10). No clean result below 6.

## Conclusion / next
- The 77/79@61 insertion is reachable, but only by raising the -r arm frequency, which flips its register
  allocation. A content-neutral fix would need a second lever that restores the allocation (for example
  an asm register pin in the -r arm), or a lever that moves 77/79 without heating -r.
- Profile splice remains the only matching build.

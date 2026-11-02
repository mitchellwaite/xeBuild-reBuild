# s75: NO MATCH (fncmp 74 -> 73; item b solved at a cost: 78)

Tools (new): `ours.sh SRC OUT` (mode_client asm, literals resolved), `dump.py`+`dump2.py`
(original asm with strings -> origs.txt), `sig.py origs.txt OUT` (compact diff of the
cold-block / error-block sequence), `gr2.py BASE OUT SECS` (hill climb with sideways moves over
every bcp-goto chain: delete / add conjunct / drop conjunct, plus cold/hot labels on AT() sites;
protects the `mode + 260` lever). `bbmap.py` tags are unreliable (several RTL dumps before Trace 1).

- best73.c = best74 + cold label on hdd4: `AT(hdd4) { hc4: __attribute__((cold)); } log_printf...` (73).
  Greedy over 60 cold/hot-label and efail/eout raise levers (gr.py) found nothing more.
- Item b (epilogue copy after netDisconnect) SOLVED structurally: in `fail:` add
  `if (__builtin_constant_p(mode + 260)) goto ndl;` (one conjunct, ~50%: raises ndl's freq above
  connect_traces' duplication threshold ~10% of entry; 2+ conjuncts = too low, no copy). Any
  predicate shape giving 50% works the same (== 1, != 0, == 3...). Other origins (u2, goto fail
  sites, before dtg, function entry) either don't copy or break much more (entry: 175+).
  fl1 = best73 + that lever: 95; gr2 climb -> best78b.c 78 (epilogue copy + reboot test match,
  rest is the item-a cold order).
- Item a: orig order after the argv traces: -keys CU0 Info Keys Patches invalid | -ip hdd5 hdd4 CU2 |
  -r Block Ferase | -w CU4 CU3 | -e Invalid Patches0 Info0 CU5.. ; ours pulls Keys+hdd5 right after
  the netReboot block (JMP(hdd5,s5) in case 3 is needed: removing it +6..+24) and puts every
  cold group one argv trace too early. Raising efail (bcp goto from clientEraseBlockI entry, 3
  conjuncts) puts Block+Ferase together but before -r, and disturbs -e. Not solved.
- d untouched (follows the cold order).
Next: run gr2.py longer from best78b.c (b fixed) with more lever kinds (rok fan weights, case JMPs).

# s108 (attempt 89): NO MATCH. Best stays s102/best.c (f2 24).

Direction: structural source variants (not dead-goto levers). ~170 compiles; ev.sh = s104/run.sh 4-way + dist.py.
Files: pre.c/post.c (best.c split around clientEraseBlockI), gen.py + vars*.txt (callee bodies),
gm.py (main-region variants), gf.py/gp.py (feeds on the s107 h0/ef inlined family), res in ev.out/res*.txt.

1. clientEraseBlockI restructurings (vars.txt e01-e20): early-return chain, outer/inner/net polarity swaps,
   else-if chain, goto error labels at the end (two label orders), do{}while(0)+break, int return,
   net result in a variable, range test via local. ALL compile to the identical layout (f2 24; only
   block numbers shift). gcc canonicalises these shapes before bbro, so statement structure is not a
   free lever here. Variants that change code: shared msg-variable exit (e05) 51, ternary printf (e09) 48,
   status-code switch (e10) 124, no levers (e11) 64, out-of-range test first (e13) 42, local n (e17) 32,
   einv not cold (e15) 46 (gives 108 139 55), eout cold (e18) 70.
2. Hot/cold labels on each callee label and pairs (vars2/vars3, 24 variants): efail hot = 108 55 139 (target
   order) but 138 drops after 62 and efail becomes the fallthrough of the netErase test (je->jne + sunk
   [8+esp] store), f2 40 - same as s107's efail_i feed. efail hot + esucc hot cancels back to best (24).
   Everything else 34-132.
3. main regions (gm.py, 20): case 12/7 polarity / early break / shared call (m01,m04-m07: 24, same layout),
   arg=NULL + single call (m02/m08) and ternary clientInfo (m03) ~110; switch case text order (m09-m13): 24;
   -r: if(!mode) nesting, i++ split, arg=a: 24; mode=1 before log (m15) 40; extra dsp asm gotos on c10/c11 50/76.
4. efail_i feed (s107 ef.c) + compensating esucc_i feed (gf.py 7 sites x 1-3 conj; gp.py 8x8 site pairs
   from h0): esucc feed restores the je fallthrough but makes 138/139 pop right after 49 (f2 46);
   best pair p_57 (efail from c9, esucc from c11) f2 30. Register pins were not applied: the ef damage is a
   fallthrough choice (efail vs esucc after netEraseBlock), not register allocation, so a pin cannot repair it.
Semantics: every variant keeps the statements/outputs of src/mode_client.c (restructurings are
control-flow equivalent; levers are dead __builtin_constant_p gotos or label attributes). e09 passes an
extra ignored vararg to the "Success!" printf (output identical) - probe only.
Conclusion: source structure in these regions is canonicalised away; only frequency changes move the
order, and those re-enter the known efail/esucc fallthrough trade-off. No variant below 24.

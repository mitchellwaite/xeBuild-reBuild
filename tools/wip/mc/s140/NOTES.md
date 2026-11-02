# s140: case-5 cinfo reload (from s139 best17, f2 17)
b0.c = s139/best17.c (f2 17). Variants of the case-5 empty asm goto input (f2.sh):
- v1 "g"(cinfo) 17, v3 "r"(cinfo) 17, v6 "a" without s4 label 17: reload `mov eax,[cinfo]` stays.
- v2/v7 no input 34; v4 "a"(&cinfo->hwFlags) 32.
- v8 "+a" copy in the if condition 17 (asm goto still re-reads cinfo).
- v9 function-scope local c5 used in test and asm: 116 (frame slots shift by 4).
- v10 block-local c5 = cinfo for case 5: 116 equivalent; c5 spilled across je, case 5 moves after case 6.
Insight: the reload is the input operand itself. cinfo is a static global, and the value the test
loaded is not reused across the je: no CSE over the BB edge. Copying cinfo into a local makes RA
spill it. So the asm needs some input that gcc already holds as a pseudo live in eax over the edge.
None of the tried variants gives one.
Climb (goal 2) not re-run: s139 SA 600x4000 from p17 already floors at 17.
NO MATCH, best 17 (s139/best17.c).

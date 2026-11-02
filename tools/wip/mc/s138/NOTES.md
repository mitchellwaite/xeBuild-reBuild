# s138 (attempt 119): NO MATCH. Floor stays 18 (b18.c = s117/best.c).

Goal: get the case-5 `JMP(s4,c12)` edge's bbro effect without best18's extra edge block
(`L535: mov eax,_cinfo; jmp L532`; L532 = `mov eax,[eax+4]; ...; call _sendAvatarData`, so the edge
needs cinfo in eax).

- Block removed by giving the asm goto `"a"/"r"/"g"(cinfo)` input (vEa/vEr/vEg): f2 35. The edge block is
  gone, but the reload moves into case 5 (`mov eax,[_cinfo]` before sendCompatData, the volatile JMP(dsp)
  stops FRE), and 421-565 relayout (log_printf pair + [8+esp]=ebx block, usage 3/5) -> the edge
  block itself is a bbro trace member best18 relies on, not just the edge.
- "m"(cinfo): 18, same block (vEm). Load cinfo into a local ci5 shared by test and asm: 122 (vFa/vFr).
- Moving s4 after the load (`kv = cinfo->kernel; s4: sendAvatarData(arg,kv)`): 98-102 (vA/vC); s4 after call: 34 (vB).
- Asm with "a"(cinfo) before/merged with JMP(dsp) (vG1-5): 34-44, block stays in G1/G2.
- w/: "a"(cinfo) asm goto with s4 + each other label (e_*, f_*): all 35 (second label inert).
- No RTL mechanism removes an asm-goto edge after bbro (bcp gotos fold in GIMPLE), so a "dies after
  bbro" edge is not available.
Goal 2 (profiled bbro block-by-block, r4sim) not done.

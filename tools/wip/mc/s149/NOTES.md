# s149: CFG-shape levers around case-7 p0 (profile-free mode_client)

Base s146/t6.c (f2 16). Variants a1-a7 (sed on t6, f2 via s101/f2.sh):
- JMP(u2) inside p0 before/after clientPatches(NULL) (a1, a5): 16, edge folds (inert).
- JMP(hdd4) inside p0 (a2) 92; JMP(u2)/JMP(hdd4) before AT(p0) (a3, a4) 76/77.
- JMP(p0c) from u2 (a6, a7) 163/143.
Laundered-value conditions (asm "=r"/"0" copies) were not compiled: they leave a real
test+branch in the output that the reference lacks (no pass after bbro deletes real branches),
so they cannot be byte-exact. Model enumeration to 4-5 changes and climb not run.
## Result
NO MATCH, best f2 16 (s146/t6.c). Semantics: JMP = empty asm goto falling through.

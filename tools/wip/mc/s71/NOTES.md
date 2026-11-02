# s71: natural-loop / rok-strip levers + fncmp-driven SA; NO MATCH (fncmp 158 -> 82)
- m_x.py: strip a case label from rok/fkbo fake edges (ST) + s70 tail loop to dsp. Stripping c10/c9/c2 breaks R2 (35-40);
  c12/c11/c3 keep R2 0-1 but es2 rises (R3 34-38). Tail loop at case 12 alone: fncmp 144 (base best_d 158) though es2 229.
- Conclusion: es2 and fncmp disagree; optimise fncmp directly.
- sa.py = s70 sa + ST lever (toggle a label's rok/fkbo edges), cost = fncmp + 0.1*(es2 + 2*R3), compile with fncmp.
  4 workers x 3000 s. Best: w2 (from s62/best_b, LP {12:1}) -> best_s71w2.json / best82.c:
  **fncmp 82**, es2 196 (R2 0, R3 23), ev 44; LP {4:1,1:3,d:2,9:3,3:1}, ST [c11,i0,p0].
- Next: continue SA from best_s71w2.json with cost on fncmp (longer runs, lower T0); full-object compare.

# s68: inject flow only into the switch dispatch; NO MATCH
Base s64/best_d (es2 156, R1 2 R2 0 R3 18 R4 104, fncmp 158). Probes run with `python ../s64/q.py TAG ../s64/best_d.json m_X.py`.
The mod files are kept (m_*.py; slf.py, slf2.py and lp.py are their generators).
"Dispatch" here means the per-case edge value from the switch block (the 111:N entries in q.py's table); the base value is 4.

| probe | what was added | es2 (R1,R2,R3,R4) | dispatch |
|---|---|---|---|
| lbl | only the `dsp:` label before `switch` | 156 (2,0,18,104) | 4 |
| u2 d1-3 | dead argc-bcp goto dsp before client_usage(2) | 660 (15,61,75,146), same at every depth | - |
| fail d1-3 | dead goto dsp on the netConnect-fail branch | 435 (3,27,70,163) | - |
| rokf d1/2/3 | dead goto dsp after the rok netGetInfo | 243/216/164 (R3 46/28/22) | 4 (rok is cold, so it carries no flow) |
| s1-8 | self loop `dsp: if(bcp(argc..)) goto dsp;` | 160 (2,0,18,108) | 4: a self loop cannot raise the switch's outflow |
| g1 | self loop `dsp: asm goto("" :::: dsp)` | 379 | 3 |
| g3 | self loop with `bcp(mode+777)` | 160 | 4 |
| l1/l2 | `asm goto("" :::: dsp)` at the head of all 12 live cases (a real loop around the switch) | 503/519 (R2 30/24, R3 90/109) | **14** |
| k1-k4 | the same at 1, 3, 6 or 3 cases | 368-399 (R2 19-24, R3 46-66) | 3-5 |
| b1/2/3/5 | dead `bcp(argc+k)` gotos to dsp at every case head | 224/220/208/225 (R2 0, R3 34-45) | 4 |

## Findings
- The only lever that raised the dispatch edges without POST is a real loop: asm-goto back edges from the case heads.
  With all 12 live cases it overshoots (14 per edge against M's 7-10). The case bodies drop to 2-6.
  Any asm-goto loop breaks R2 (19-30).
  The asm diff for k1 shows bb-reorder moving the rok netGetInfo/netReboot block after the switch and the
  dispatch register changing from ecx to edx. The cause is the layout change, not extra bytes.
- Dead bcp back edges to dsp (b*) keep R2 at 0 but do not raise the dispatch edges.
  They only lower the case-body frequencies, so R3 gets worse.
  The table seems to mix frequency snapshots taken at different times; the head frequencies no longer equal the sum of their predecessors.
- Flow into dsp from blocks that look wasted (fail, u2, rok) does nothing useful: those blocks are cold or noreturn, so they carry almost no flow.
- R3 never went below 18, so SA was not started (the gate was R3 < 18). Bests are unchanged: s62/best_b (es2 155) and s64/best_d (R3 18).

## Next ideas (not run)
- Asm-goto loop from a subset of cases, together with an SA that re-tunes rok/TH to repair the bb-reorder layout (R2).
  Target 7-10 per dispatch edge.
- Probability-controlled back edges, e.g. an asm goto with several distinct labels stacked before dsp.

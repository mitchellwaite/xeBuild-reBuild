# s72: longer/cooler SA from s71 best82 on fncmp cost; NO MATCH (fncmp stays 82)
- sa.py = copy of s71 sa.py. 4 workers x 4500 s (~4260 evals each) from best_s71w2.json:
  a T0=1.5 FW=0.1; b FW=0 (pure fncmp) T0=1.5; c T0=3; d FW=0.05 T0=0.8 PLP=0.3.
- No worker beat fncmp 82. Worker a found an es2-only gain (best_s72a.json: es2 189, R3 25, fncmp 82).
  So best82 is a deep local minimum for the existing levers (PD/TH/LP/ST/w/X/E2/order).
- d82.txt = fncmp diff of best82: almost all block placement (log_printf/jmp error blocks
  in a different order, one je/test swap, an epilogue moved, one index-register order).
  Fixing it needs new levers that move individual cold blocks, not more SA on the current ones.

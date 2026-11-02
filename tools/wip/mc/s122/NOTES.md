# s122 (attempt 103): NO MATCH. Floor stays 18.

Forwarder-free realisation of the switch-region asm-goto levers (only moves/merges/drops of
never-taken empty `asm goto` -> semantically equivalent to src/mode_client.c).
- gen.py (10 levers: move block-start JMP into following stmt / merge into existing JMP / drop):
  on b0, m_c9, m_s5c, m_c8, s121 rm1_8. gen3.py (11 more: label-order, p0 operand order, c11 placement).
- ~80 variants measured. New distinct 18s (different asm from b0, same count):
  v/m_c9.c (`AT(c9)JMP(s5); {..JMP(hdd4,hdd5)}` -> single trailing JMP(s5,hdd4,hdd5)),
  v/m_s5c.c (s5 block: JMP(dsp,s4) merged, c12 dropped). Their diff vs ref is still the issue-1
  (fail-log vs usage(2) group) and issue-3 shuffles. Combos, c3 label order, p0mv: 18.
  m_c8 (c11 merged into c8's JMP) 19; dropping cdef/i1 JMP 82-126; c10 JMP move/drop 44-57;
  s5 full merge 28-52; removing AT(t4/t5/u2) labels does not compile (still referenced).
- Not done: per-block wp.py/bbs.py forwarder map and r4sim removal study (task dirs 1-2).
Conclusion: merging block-start JMPs to kill forwarders is neutral at best; the block-start
JMPs on cdef/c10/c12 are load-bearing (removing them costs 30-100).

# s74: NO MATCH (fncmp 76 -> 74)
- best74.c = s73/best76.c with the rk X operands changed to memory operands:
  `"X"(&rko), "X"(&rkvN)` -> `"m"(rko), "m"(rkvN)` (item c: the two rok-path `lea edx/ecx,[56/59+esp]` vanish).
  Same edit on fko/fkv: no change (76). Dropping rko operand, or "X"(rko): 74 too.
- Item b (epilogue copy after netDisconnect): bbro dump shows the netDisconnect block of that
  path (jump-threaded per-mode tail copy, bb 59) at freq 1 vs entry 217, and the return block
  (bb 19) sits inside a longer trace, so connect_traces' 1-block duplication (needs edge freq
  >= ~10% entry for code_may_grow; epilogue is 10 bytes > 2-byte jmp) can't fire. `hot` label on
  ndl: 91, no duplication. Needs that path much hotter or ret as its own trace. gcc source fetch
  from gcc.gnu.org was blocked (Anubis) this session.
- Items a, d untouched.

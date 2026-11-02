# mode_client s24 (profile-free) -- NO MATCH

Profile build stays; no src/ or build.sh change. Base: s21 inv19.json (inv 19).

## Tries
- `scan.py` (uses s23 ext/table): grid over base + a x (58=h4 test, rok,pp) + nb x send-block
  target {38..41} + c x (59=h5, rok,pp) + nb x {42..45}; a,c in 0..3, nb 1..2 (800 builds,
  scan.log; columns inv a b c d nb f110 f111 f112). Best stays 19 (only no-op combos).
  Raising 112 to 4-5 needs (40,rok,pp) and costs inv 26+ (h4/test head reshuffle, as s23 #1).
  f111 is unmapped in table.meas, so exact 111==112 ties could not be read directly.
  => idea (1) via rok injections into test+sibling: no gain.

## Not done (still open from s23)
- Read gcc-6.2 bb-reorder.c better_edge_p / find_traces_1_round tie rules and map 111 in
  analyze so ties can be targeted exactly.
- Entry-level injection source from a non-folding value (global load / function result /
  argv content) for 103 = 2..3.
- Source restructurings (hoist/merge hwFlags test, usage(2) shape) checked against s5/s9.
- Plain compile + s12 asm-goto zero-byte priority edges (s18 X2/RX/T48) combined with bcp.

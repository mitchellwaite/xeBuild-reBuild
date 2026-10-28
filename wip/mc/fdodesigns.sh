#!/bin/sh
# Crafted-profile designs for mode_client (2026-10-27), exactly as run, with their results.
# Run from the repo root in Git Bash.  Each design is one `wip/mc/fdorun.py <slot> <design>
# --over <extra gcda.py args>` call; the slot dir build/mcfdo/slot<slot> keeps the .gcda,
# fdo.diff (fncmp), fdo.s and the bbro/compgotos dumps.  Design values are the draft's RTL
# bb numbers (wip/mc/mcvar.py / bbsum.py numbering, 1cee64878a build) -> wanted frequency;
# fdorun turns them into edge overrides on the instrumented dump's tree bbs.
#
# Prepare once (absolute dir; gcc drops the profile silently if the compile path differs):
#   export EXTRA='--param builtin-expect-probability=50'
#   python wip/mcfdo.py "$(cygpath -w "$PWD")\\build\\mcfdo" wip/app/mode_client.c
#
# Always needed (see wip/README.md, "Crafted profile"):
#   --consistent                               exact integer flows (an edge is zero)
#   --entry=clientEraseBlock:mode_client:126   the inlined erase block keeps the callee's own
#                                              counts, so its entry must equal the call block's
#   clientEraseBlock:5>1=100 ... 8>1=100       every erase leaf leaves by its fake exit arc, so the
#                                              callee's return block (merged into one leaf after
#                                              inlining) carries no count
# Inspect a slot:
#   python wip/mc/bbsum.py build/mcfdo/slotd4/m.c.274r.bbro mode_client build/mcfdo/slotd4/fdo.s build/mcfdo/slotd4/m.c.267r.compgotos
#   awk '/;; Function mode_client /{p=1} p' build/mcfdo/slotd4/m.c.274r.bbro > build/mcfdo/slotd4/mc.bbro
#   python wip/mc/mcgrid.py build/mcfdo/slotd4/mc.bbro        # cold-key grid on that build's heap history
#   python wip/mc/mcsim2.py build/mcfdo/slotd4/mc.bbro 112=4 115=4 ...
#   gcc -S ... -fbranch-probabilities -fprofile-dir=<slot dir, Windows path> -fdump-rtl-compgotos-blocks-details build/mcfdo/m.c -o - >/dev/null
#   python wip/mc/cfgdump.py m.c.267r.compgotos mode_client 97 140     # frequencies, probabilities, counts
#   python wip/mc/gcdadbg.py build/mcfdo/-.gcno build/mcfdo/m.c.042t.profile_estimate build/mcfdo/slotd4/-.gcda clientEraseBlock

set -e
export EXTRA='--param builtin-expect-probability=50'
FAKE="clientEraseBlock:5>1=100 clientEraseBlock:6>1=100 clientEraseBlock:7>1=100 clientEraseBlock:8>1=100"
COMMON="--consistent --entry=clientEraseBlock:mode_client:126"

# The plain build's own frequencies as a design (cases 4, HDD errors 2, usage(2) 4, chain 7/2/1,
# erase 4/1/1/1).  Before --entry this needed --mult=clientEraseBlock:1400 and gave 64 lines /
# inv 22 with the Success leaf carrying the join count (trace split at the erase test).
PLAIN="129=4 107=4 108=4 109=4 110=4 113=4 116=4 119=4 120=4 121=4 128=4 132=4 112=2 115=2 117=1 130=1 49=7 55=2 61=1 126=1 127=1 125=1"
python wip/mc/fdorun.py plain $PLAIN --over $FAKE $COMMON

# D1 (cases 7, HDD 52%): chain overrides above 50% pulled the -r/-w bodies out of their tests'
# traces (fncmp 190, prefix 5: HDD errors before usage(2) for the first time).
# D2 (cases 7, Block 2.6 -> 3, Failed 1.7 -> 2, -w 1.5 -> 1): 156 lines, prefix 7, inv 20; the
# arg test connected to the switch path (its edge to the reboot test came out at 39.6% < 40%,
# and in any case connect_traces decides by probability, see the README).
D2="129=7 107=7 108=7 109=7 110=7 113=7 116=7 119=7 120=7 121=7 128=7 132=7 112=4 115=4 117=1 130=1 49=7 55=3 61=1.5 67=0.75 126=2.6 127=1 125=1.7"
python wip/mc/fdorun.py d2 $D2 --over mode_client:115\>117=52 mode_client:118\>120=52 $FAKE $COMMON

# D3 (five first-popping cases + case 10 at ~7.5, the rest ~5): the case groups pop in two
# batches, so the case layout breaks (228 lines).
# D4 (the two HDD cases and case 10 at 7.27 -> 7, the other nine at 6.8 -> 7, HDD errors 50.5%,
# chain 45/50/50%, Block 2.8 -> 3, Failed 1.7 -> 2): every realized frequency equals the design,
# cold prefix 8 of 40 (through -w), inv 15, but the arg test still falls into the switch path
# (148 lines): the trace ends at the arg test in every mode and connect_traces wants
# P(switch) <= 1/3, which caps the HDD errors at 3 < usage(2) = 4.
D4="110=7.27 113=7.27 121=7.27 129=6.8 107=6.8 109=6.8 108=6.8 119=6.8 120=6.8 128=6.8 116=6.8 132=6.8 112=3.5 115=3.5 117=1 130=1 49=7 55=3.15 61=1.58 67=0.79 126=2.8 127=1 125=1.7"
python wip/mc/fdorun.py d4 $D4 --over mode_client:115\>117=50.5 mode_client:118\>120=50.5 $FAKE $COMMON

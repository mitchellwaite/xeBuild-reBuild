# repro.sh: profiled compile of mode_client that matches the original (fncmp MATCH).
# Source: tools/wip/mc/s18/match/mode_client_fdo.c (= genq.py variant zero1: s12 vY + X2/X1 asm gotos + RX126/RX117),
# profile: tools/re/gcda.py with the overrides in overrides.txt (one per line).
set -e
cd "$(dirname "$0")/../../../../.."
export EXTRA='--param builtin-expect-probability=50'
D="$(cygpath -w "$PWD")\build\mcmatch"
python -c "import sys;sys.path.insert(0,'tools/wip');import mcfdo;mcfdo.prep(r'$D','tools/wip/mc/s18/match/mode_client_fdo.c')"
MCFDO_DIR="$D" python tools/wip/mc/s9/fdorun9.py m --over $(cat tools/wip/mc/s18/match/overrides.txt | tr '\n' ' ') | grep -E '^fncmp|round4'

F='fail: __attribute__((cold)); '
M7='__builtin_constant_p(mode + 51213) && __builtin_constant_p(mode + 101213)) mode = 7'
L9='if (__builtin_constant_p(mode + 1220)'
S=' switch (mode) {'
kk(){ python keys.py d/$1/mc.bbro d/$1/order.txt | sed -n ${2:-6},${3:-13}p | tr '\n' ' '; echo; }
run(){ for f in "$@"; do sh m.sh $f.c; kk $f; done; }

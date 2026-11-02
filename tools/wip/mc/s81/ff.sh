#!/bin/sh
# ff.sh NAME BASE LABEL K [SEED] : add fail-feed bcp goto LABEL with K conjuncts
n=$1; b=$2; lab=$3; k=$4; s=${5:-$(( $(od -An -N2 -tu2 /dev/urandom) + 1000 ))}
c=$(python -c "print(' && '.join('__builtin_constant_p(mode + %d)'%($s+50000*i) for i in range($k)))")
sh t.sh $n $b 'fail: __attribute__((cold)); ' "fail: __attribute__((cold)); if ($c) goto $lab; " && sh ours.sh v_$n.c o_$n.txt && python sig2.py origs.txt o_$n.txt | tr '\n' '|' | cut -c1-${W:-330}; echo

B=$1; P=$2
for n in 3 4 6 7; do sh r.sh ${P}w$n $B '(char *)__builtin_constant_p(i + 60) == (char *)1 && (char *)__builtin_constant_p(i + 61) == (char *)1 && (char *)__builtin_constant_p(i + 62) == (char *)1 && (char *)__builtin_constant_p(i + 63) == (char *)1 && (char *)__builtin_constant_p(i + 64) == (char *)1' "$(python cj.py i 60 $n)"; done

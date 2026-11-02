# mk2.sh BASE PREFIX : wb3/wb4 feed grid
W3a=' if ((char *)__builtin_constant_p(i + 60) == (char *)1 && (char *)__builtin_constant_p(i + 61) == (char *)1 && __builtin_constant_p(i + 777100)) goto wb3;'
cj() { s="__builtin_constant_p(i + $2)"; n=1; while [ $n -lt $1 ]; do s="$s && __builtin_constant_p(i + $(($2 + n * 1000)))"; n=$((n+1)); done; echo "$s"; }
for w in $3; do for f in $4; do
  n=$2w${w}f$f
  W3=" if ($(cj $w 777100)) goto wb3;"; [ $w = 0 ] && W3="$W3a"
  F=""; [ $f != 0 ] && F=" if ($(cj $f 888100)) goto wb4;"
  [ "$5" = r ] && python gen.py $1 $n.c "593|$W3a|$F$W3" '634|client_usage(4, argv[i]);|{ wb4: client_usage(4, argv[i]); }' || python gen.py $1 $n.c "593|$W3a|$W3$F" '634|client_usage(4, argv[i]);|{ wb4: client_usage(4, argv[i]); }'
done; done

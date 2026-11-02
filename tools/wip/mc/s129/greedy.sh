# greedy removal from best18 keeping f2 <= 18
cd $(dirname $0); rem="7"
for k in 32 28 6 9 20 21 25 23 34 5 4 17 11 26 31 29 18 27 30 10 "12 15 16" "13 14" "22 24" 19 33 8 "10 12 15 16" "11 12 15 16"; do
  r=$(sh r.sh g_$(echo $rem $k|tr ' ' _) del $rem $k | cut -d' ' -f2)
  if [ "$r" -le 18 ]; then rem="$rem $k"; echo "KEEP-REMOVED $k -> $r"; fi
done; echo "final removed: $rem"

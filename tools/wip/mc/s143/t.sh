# t.sh NAME : f2 + clientEraseBlockI freqs + r4 order
cd /c/Users/Win11VM/Documents/GitHub/xebuildBugFix/tools/wip/mc/s143
f=$(sh ../s101/f2.sh $1.c); sh dump.sh $1 >/dev/null 2>&1; python ../s101/bbinfo2.py dd/$1/mc.bbro > dd/$1/bb.txt
echo "$1 f2=$f $(grep -E 'LC11[4-8]|LC15[56]' dd/$1/bb.txt | awk '{print $8"/"$6}' | tr '\n' ' ')"
python ../s86/r4sim.py dd/$1/mc.bbro | tail -1 | cut -d' ' -f13-36

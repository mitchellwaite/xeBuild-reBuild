# try target subsets x seeds; print best per subset
for T in 112,115,127 112,115,125,127 112,115,127,117,130 112,115,125,127,117,130 112,115,103,127 112,115,125,127,103 112,115,125,127,117,130,103 127,112,115 115,112,127,125; do
 for s in 1 2 3; do echo "T=$T s=$s $(VC=1 python wip/mc/s12/fake.py build/s12/b.txt 60000 $s $T | grep ^best)"; done
done

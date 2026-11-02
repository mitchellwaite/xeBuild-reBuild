cd /c/Users/Win11VM/Documents/GitHub/xebuildBugFix/tools/wip/mc/s135
for n in sw_r_w sw_e_c nma_2; do (cd cl_$n && python climb.py singles > singles.out 2>&1 && python climb.py pairs 60 > pairs.out 2>&1); done

"""Attempt 54: print one function's profile_estimate dump (whole, blocks with freq) for a variant.
python tools/wip/dehint/bdgen/a54_dump.py <variant.c> <function> [bbfrom bbto]"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a51_fpred as F
t = open(sys.argv[1], newline='').read()
x = F.dump(t, sys.argv[2])
if len(sys.argv) > 3:
    lo, hi = int(sys.argv[3]), int(sys.argv[4])
    on = False
    for l in x.splitlines():
        m = re.match(r'\s*<bb (\d+)>', l) or re.match(r';;\s+basic block (\d+)', l)
        if m:
            on = lo <= int(m.group(1)) <= hi
        if on:
            print(l)
else:
    print(x)

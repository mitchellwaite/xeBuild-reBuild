"""lay.py TAG: compact side-by-side of reference and our block order (role labels) + block-list distance."""
import sys, difflib, lab
o = lab.orig_blocks()
m, ids = lab.our_blocks(sys.argv[1])
print(len(o), len(m), 'lcs-diff', sum(max(b-a,d-c) for t,a,b,c,d in difflib.SequenceMatcher(None,o,m,autojunk=False).get_opcodes() if t!='equal'))

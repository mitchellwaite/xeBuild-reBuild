"""flshow.py <fn> [file [flags..]]: reference listing of fn, or its diff against a variant."""
import difflib, sys
import fllib as L

fn = sys.argv[1]
if len(sys.argv) == 2:
    print('\n'.join(L.dis(L.REF)['_' + fn]))
else:
    o = L.compile(open(sys.argv[2], newline='').read(), sys.argv[3:] or None, 'show')
    a, b = L.dis(L.REF)['_' + fn], L.dis(o)['_' + fn]
    for ln in difflib.unified_diff(a, b, lineterm='', n=3):
        print(ln)

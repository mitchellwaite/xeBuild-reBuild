"""rawref.py SRC OUTDIR: dump original (ref) and gcc (mine) raw mode_client listings with labels."""
import sys, os
R = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
src, out = sys.argv[1], sys.argv[2]
code = open(os.path.join(R, 'tools/re/fncmp.py')).read()
code = code.replace("diff = list(difflib.unified_diff(norm(ref), norm(mine)",
 "open(os.path.join(OUT,'ref.s'),'w').write(chr(10).join(ref)); open(os.path.join(OUT,'mine.s'),'w').write(chr(10).join(mine)); sys.exit(0)\n    diff = list(difflib.unified_diff(norm(ref), norm(mine)")
sys.argv = [os.path.join(R, 'tools/re/fncmp.py'), src, 'mode_client', '-I' + R + r'\src', '-O3', '-fno-toplevel-reorder', '-fno-ipa-profile', '-fno-reorder-functions', '--param', 'builtin-expect-probability=50']
g = {'__name__': '__main__', '__file__': sys.argv[0], 'OUT': out}
os.makedirs(out, exist_ok=True)
exec(compile(code, sys.argv[0], 'exec'), g)

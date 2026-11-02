"""python tools/wip/dehint/rfshow.py <file.c> [gcc flags]: fncmp's result for readFileIn, and the same comparison with
registers erased, as a sequence diff: the lines left are layout or shape differences, not allocation."""
import difflib, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
src = sys.argv[1]
flags = sys.argv[2:] or ['-O3', '-Isrc']
r = subprocess.run([sys.executable, os.path.join(ROOT, 'tools/re/fncmp.py'), src, 'readFileIn'] + flags,
                   capture_output=True, text=True, cwd=ROOT)
o = r.stdout + r.stderr
if o.strip() == 'MATCH':
    print('MATCH')
    sys.exit()
n = len([l for l in o.split('\n') if re.match(r'^[-+][^-+]', l)])
# rebuild both whole sequences by asking fncmp for a full-context diff is not possible, so patch the unified diff
ref, mine = [], []
for l in o.split('\n')[2:]:
    if l.startswith('@@') or not l:
        continue
    if l[0] in ' -':
        ref.append(l[1:])
    if l[0] in ' +':
        mine.append(l[1:])
E = lambda s: re.sub(r'\b(e[abcd]x|e[sd]i|ebp)\b', 'R', s)
a, b = [E(x) for x in ref], [E(x) for x in mine]
d = [l for l in difflib.unified_diff(a, b, lineterm='', n=1)][2:]
print('lines differing: %d; with registers erased: %d' % (n, len([l for l in d if l[0] in '+-'])))
if '-v' in os.environ.get('RFSHOW', '-v'):
    print('\n'.join(d))

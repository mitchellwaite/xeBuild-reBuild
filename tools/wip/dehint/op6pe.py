"""Attempt 6: print applyIniOptions' profile_estimate dump around a pattern.

python tools/wip/dehint/op6pe.py file.c [pattern] [before] [after]
Shows the prediction lines (Predictions for bb N ...) and the block text around the
first block that holds the pattern (default getIniValue ("xellbutton"))."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opfq

src = sys.argv[1]
pat = sys.argv[2] if len(sys.argv) > 2 else 'getIniValue ("xellbutton")'
nb = int(sys.argv[3]) if len(sys.argv) > 3 else 60
na = int(sys.argv[4]) if len(sys.argv) > 4 else 40
text, d = opfq.dump(open(src).read())
body = opfq.fn(text, 'applyIniOptions')
lines = body.split('\n')
for i, l in enumerate(lines):
    if pat in l:
        print('\n'.join(lines[max(0, i - nb):i + na]))
        break
# prediction summary lines for all blocks
print('---- predictions')
pred = text[text.rfind(';; Function applyIniOptions'):]
for l in pred.split('\n'):
    if l.startswith('Predictions for bb') or 'heuristics' in l or l.startswith('  '):
        pass

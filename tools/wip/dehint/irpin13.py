"""python tools/wip/dehint/irpin13.py <file.c> name... : quick single removals of the current pins, by regex edit (attempt 13)."""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import irlib
PINS = {
 'found': ['\t\tif (n > 1)\n\t\t\t__asm__("" : "+a"(found));\n'],
 'lo': ['\t\t\t\t\t__asm__("" : : "a"(lo));\n'],
 'v': ['\t__asm__("" : : "S"(v));\n'],
}
text = open(sys.argv[1], newline='').read().replace('\r\n', '\n')
out = sys.argv[3] if len(sys.argv) > 3 else None
for nm in sys.argv[2].split(','):
    for p in PINS[nm]:
        assert p in text, nm
        text = text.replace(p, '')
if out:
    open(out, 'w', newline='\n').write(text)
print(irlib.fmt(irlib.score_text(text, [])))

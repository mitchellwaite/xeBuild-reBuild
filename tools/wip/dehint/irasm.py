"""python tools/wip/dehint/irasm.py <file.o|ref|file.c> <fn> : function's disassembly (addresses relative
to the function, strings left as relocs).  Reference with `ref`."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import irlib

src, fn = sys.argv[1:3]
if src == 'ref':
    fns = irlib.ref()['fns']
elif src.endswith('.c'):
    text = open(src, newline='').read().replace('\r\n', '\n')
    ok, o, d = irlib.compile_src(text, [])
    if not ok:
        print(o)
        sys.exit(1)
    fns, _ = irlib.disasm(o)
    irlib.cleanup(d)
else:
    fns, _ = irlib.disasm(src)
print('\n'.join(fns[fn]))

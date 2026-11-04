"""python tools/wip/dehint/iw19ft.py <base.c>: probe. Field types of xb.hdr and xb.spare through an overlay of xebuild.h (build/iw/a19/inc); plain -O3. Prints lines per pair; the overlay is a probe, src/xebuild.h isn't touched."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib
base = open(sys.argv[1], newline='').read().replace('\r\n', '\n')
h = open(os.path.join(iwlib.R, 'src', 'xebuild.h'), newline='').read().replace('\r\n', '\n')
inc = os.path.join(iwlib.BUILD, 'a19', 'inc')
T = ['uint8_t *', 'char *', 'void *', 'int8_t *', 'unsigned int *', 'struct nosuch *']
for th in T:
    for ts in T:
        x = h.replace('uint8_t *hdr;', th + 'hdr;').replace('uint8_t *spare;', ts + 'spare;')
        open(os.path.join(inc, 'xebuild.h'), 'w', newline='\n').write(x)
        r = iwlib.score_text(base, [], extra=['-I' + inc])
        print(repr(th), repr(ts), iwlib.fmt(r)[:150].replace('\n', ' '), flush=True)

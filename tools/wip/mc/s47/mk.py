"""mk.py SRC OUT VARIANT: insert a zero-byte asm-goto edge into the -w arm toward its client_usage(5) tail."""
import sys
src, out, v = sys.argv[1:4]; base = open(src).read()
G = '__asm__ goto("" :::: w5x);'
W0 = 'k61l: if (!strnicmp(argv[i], "-w", 2)) {'
i0 = base.index(W0); i1 = base.index('client_usage(5, argv[i]);', i0) + len('client_usage(5, argv[i]);')
W = base[i0:i1]
rep = {'c1': ('if (i + 1 == argc', 'if (({' + G + ' 0;}) || i + 1 == argc'),
       'mid': ('a = argv[i + 1];', 'a = argv[i + 1]; ' + G),
       'pre': ('a = argv[i + 1];', G + ' a = argv[i + 1];'),
       'c2': ('|| !a ||', '|| ({' + G + ' 0;}) || !a ||')}[v]
w = W.replace(*rep).replace('if (mode)\n\t\t\t\tclient_usage(5', 'if (mode) { w5x: client_usage(5') + ' }'
open(out, 'w', newline='\n').write(base.replace(W, w))

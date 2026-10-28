"""mk.py OUT.c BODY.txt : sp.c with clientEraseBlock replaced by BODY.txt"""
import sys
s = open('wip/mc/s9/sp.c').read()
i = s.index('void clientEraseBlock'); j = s.index('/* the option', i)
open(sys.argv[1], 'w', newline='\n').write(s[:i] + open(sys.argv[2]).read() + s[j:])

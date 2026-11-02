# mke.py BASE : c3-style variants (dead ex block inside clientEraseBlockI, JMP(ex) from efail)
import sys
base = sys.argv[1] if len(sys.argv) > 1 else 't6'
s = open(base + '.c').read()
a = 'log_printf(0, "\\n\\n***** ERROR: Failed to erase block 0x%x!\\n", block); }'
end = 'please provide hex only for offset!\\n"); }\n}'
i = s.rindex(a); j = s.rindex(end)
def w(n, ea, body):
    t = s[:i] + ea + s[i+len(a):j] + end[:-1] + '\n\tif (0) { ' + body + ' }}' + s[j+len(end):]
    open(base + n + '.c', 'w', newline='\n').write(t)
A = a[:-1] + 'JMP(ex); }'
w('e1', A, 'ex: __asm__ volatile("");')
w('e2', A, 'ex: __attribute__((cold)); __asm__ volatile("");')
w('e3', 'JMP(ex); ' + a, 'ex: __attribute__((cold)); __asm__ volatile("");')
w('e4', A, 'ex: __attribute__((hot)); __asm__ volatile("");')
w('e5', A, 'ex: __attribute__((cold)); ;')
w('e6', A, 'ex: __attribute__((cold)); goto einv;')
w('e7', A, 'ex: __attribute__((cold)); goto efail;')
w('e8', A, 'ex: __attribute__((cold)); __asm__ volatile(""); return;')

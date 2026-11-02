# dz.py MODE(C|P) : JMP(dz) before each mode_client statement; dz = dead block before return 0
import re, os, sys, subprocess
from multiprocessing.pool import ThreadPool
B = open('t6.c').read().split('\n'); M = sys.argv[1]
mc = B.index('int mode_client(int argc, char **argv)')
ret = [i for i in range(mc, len(B)) if B[i].strip() == 'return 0;'][0]
attr = '__attribute__((cold)); ' if M == 'C' else ';'
L = [i for i in range(mc + 13, ret) if re.match(r'^\s+[A-Za-z{]', B[i]) and B[i].rstrip().endswith(';') and not re.match(r'^\s+(case|default|AT\(\w+\)\s*$)', B[i])]
def one(i):
    S = list(B); S[ret] = '\tif (0) { dz: %s __asm__ volatile(""); }\n' % attr + S[ret]
    m = re.match(r'^(\s*)(.*)$', S[i]); S[i] = m.group(1) + 'JMP(dz); ' + m.group(2)
    n = 'dz/%s_%d' % (M, i + 1); open(n + '.c', 'w', newline='\n').write('\n'.join(S))
    open(n + '.ref', 'w', newline='\n').write(open('c0.ref').read())
    r = subprocess.run(['sh', '../s101/f2.sh', n + '.c'], capture_output=True, text=True).stdout.strip()
    print(r, n, flush=True); return r
ThreadPool(int(os.environ.get('NJ', '1'))).map(one, L)

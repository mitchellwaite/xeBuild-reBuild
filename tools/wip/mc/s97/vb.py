# vb.py FILE : lines "name|base|old|new[|old|new...]" -> r.sh
import sys,subprocess
for l in open(sys.argv[1]):
    l=l.rstrip('\n')
    if not l or l.startswith('#'): continue
    p=l.split('|'); subprocess.run(['sh','r.sh',p[0],p[1]+'.c']+p[2:])

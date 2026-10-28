"""sw.py NAME COND : swap post-loop branches -> if (COND) {switch part} else {reboot part}"""
import sys, subprocess, os
os.chdir(r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix')
s = open('wip/app/mode_client.c').read()
a = s.index('\tif (!(mode && arg)) {\n'); b = s.index('\t} else {\n', a); c = s.index('\n\t}\n\tif (E(reboot))', b)
reb = s[a + len('\tif (!(mode && arg)) {\n'):b]; sw = s[b + len('\t} else {\n'):c + 1]
s = s[:a] + '\tif (%s) {\n' % sys.argv[2] + sw + '\t} else {\n' + reb + s[c + 1:]
out = 'wip/mc/s6/v_%s.c' % sys.argv[1]
open(out, 'w', newline='\n').write(s)
r = subprocess.run([sys.executable, 'wip/mc/mcvar.py', out], env=dict(os.environ, FNCMP='1'), capture_output=True, text=True)
print(sys.argv[1], (r.stdout + r.stderr).strip()[:600])

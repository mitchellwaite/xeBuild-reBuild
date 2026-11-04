"""flxfinal.py: writes attempt 2's draft (src plus the 7-test arm state) and verifies it whole-object and per section."""
import os, re, subprocess
os.environ['START'] = 'comma=3,i=1,len=1,nul=1,off3=2,off4=2,x=4'
import fllib as L, flxp as P

s = P.build(P.START)
# the header comment's last sentence no longer applies
s = L.sub(s, '''success with the error in the else, and so are its length checks.  The
   [flashfs] path check doesn't yet (see its empty asm). */''', '''success with the error in the else, and so are its length checks. */''')
# comma's comment: says what these tests are now
a = s.index('\t\t/* this and the other `< -1` stores')
b = s.index('\t\tif (comma < -1) {')
s = s[:a] + '''\t\t/* this and the other `< -1` tests are dead (this one reads comma
\t\t   uninitialized, and lasts until RTL).  They steer gcc: the SSA names they
\t\t   free, so their stores count too, decide what dom2, dom3 and vrp2 number
\t\t   next, which sets the comma/nul compares, the rawpatch lea and the
\t\t   copy order on flashfs's threaded path */
''' + s[b:]
# reindent the good arm of [flashfs]'s path check
i = s.index('\t\t\tif (len <= 1023) {\n') + len('\t\t\tif (len <= 1023) {\n')
j = s.index('\t\t\t} else {\n\t\t\t\tlog_printf(0, "\\n******* ERROR: file in [flashfs] has greater than %d chars in it\'s path!')
arm = ''.join('\t' + ln if ln.strip() else ln for ln in s[i:j].splitlines(True))
s = s[:i] + arm + s[j:]
open(L.DRAFT, 'w', newline='\n').write(s)

o = L.compile(s, ['-O3'], 'final')
print('whole object identical:', L.same(o))
a, b = L.sections(L.REF), L.sections(o)
for k in sorted(set(a) | set(b)):
    print(' ', k, len(a.get(k, b'')), 'same' if a.get(k) == b.get(k) else 'DIFF')
print('asm:', s.count('__asm__'), 'unreachable:', s.count('__builtin_unreachable'), 'tests:', len(re.findall(r'< -1\)', s)))
p = subprocess.run([L.GCC, '-c', '-O3', '-Wall', '-Wextra', '-I' + os.path.join(L.R, 'src'), '-x', 'c', L.DRAFT, '-o', os.path.join(L.OUT, 'w.o')],
                   stderr=subprocess.PIPE, cwd=L.OUT)
print('\n'.join(l for l in p.stderr.decode(errors='replace').splitlines() if 'uninit' in l))

"""r4.py TAG: real order of trace heads in round 4 (with freq), named; compare with REF4 tail"""
import sys,re,nm
D='../../../../build/v/aio_p1/%s/'%sys.argv[1]
t=open(D+'aio.bbro').read()
tr=[(int(m.group(1)),int(m.group(2)),re.findall(r'(\d+) \[(\d+)\]',m.group(3))) for m in re.finditer(r'^Trace (\d+) \(round (\d+)\):\s+(.*)$',t,re.M)]
r4=[x for x in tr if x[1]==4]
heads=[int(x[2][0][0]) for x in r4]
fr={int(b):int(f) for x in tr for b,f in x[2]}
print('MINE',' '.join('%d[%d]%s'%(h,fr[h],nm.N.get(h,'')) for h in heads))
print('REF ',' '.join('%d[%s]%s'%(h,fr.get(h,'?'),nm.N.get(h,'')) for h in nm.REF4))
# first mismatch
mt=[h for h in heads if h in set(nm.REF4)]
print('sub-order equal' if mt==nm.REF4 else 'sub-order DIFF', len(mt),len(nm.REF4))

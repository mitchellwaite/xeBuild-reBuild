import sys
sys.path.insert(0,'tools/wip/dehint')
import iwlib
from concurrent.futures import ThreadPoolExecutor
t=open('build/iw/a20/nopt.c',newline='').read()
t2=t.replace('if (partial > 0) {','if (__builtin_expect(partial > 0, 1)) {')
assert t2!=t
def one(n):
    return n,iwlib.fmt(iwlib.score_text(t2,['--param','builtin-expect-probability=%d'%n]))[:140]
for r in ThreadPoolExecutor(4).map(one,[55,60,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,80,85,90]):
    print(r)

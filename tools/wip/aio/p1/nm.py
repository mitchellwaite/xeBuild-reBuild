"""block naming for the trace numbering of the guard/inlined base (n8c family)"""
N={}
for base,name in [(2,'nomobile'),(12,'noremap'),(22,'noecd'),(32,'nandmu'),(42,'nosec'),(52,'nosusec'),(62,'smcnoc'),(152,'cygnos'),(162,'demon'),(172,'patch'),(203,'noeject'),(213,'noblink')]:
    for k,r in zip(range(1,10),['O','P','PL','I','G','GL','W','.','S']):
        N[base+k]=name+':'+r
for base,name in [(225,'nodvd')]:
    for k,r in zip(range(1,9),['P','PL','I','G','GL','W','S','?']):
        N[base+k+1]=name+':'+r
    N[226]='nodvd:O'
for k,r in [(234,'P'),(235,'PL'),(236,'I'),(237,'G'),(238,'GL'),(239,'W'),(240,'S')]: N[k]='olddvd:'+r
N[72]='cfldv:U';N[73]='cfldv:W';N[74]='cfldv:GU';N[75]='cfldv:W2'
for i,n in enumerate('cpufan gpufan cputemp gputemp edram overcpu overgpu overedram av game dvd'.split()):
    b=77+5*i
    N[b]=n+':U';N[b+1]=n+':W';N[b+2]=n+':GU';N[b+3]=n+':.'
REF4=[int(x) for x in '74 201 36 16 6 56 66 46 259 94 89 124 119 114 109 84 79 104 99 129 156 166 244 217 176 207 229 27 17 57 7 67 237 47 37 167 177 218 208 157 230'.split()]

import os
XZ=int(os.environ.get('XZ','259'))
REF4=[XZ if x==259 else x for x in REF4]

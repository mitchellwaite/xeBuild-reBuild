import re,sys
src=open('H5b.c').read()
EB='else if (E(!strnicmp(argv[i], "-eb", 3)))'
IP='else if (!strnicmp(argv[i], "-ip", 3))'
KS='else if (!strnicmp(argv[i], "-keys", 5))'
SS='else if (!strnicmp(argv[i], "-s", 2))'
WB='else if (E(!strnicmp(argv[i], "-wb", 3)))'
assert all(x in src for x in [EB,IP,KS,SS,WB])
def w(n,reps):
    s=src
    for a,b in reps: s=s.replace(a,b,1)
    open(n,'w',newline='\n').write(s)
N=lambda t,l: f'else if (__builtin_expect(!strnicmp(argv[i], "{t}", {l}),0))'
Y=lambda t,l: f'else if (E(!strnicmp(argv[i], "{t}", {l})))'
P=lambda t,l: f'else if (!strnicmp(argv[i], "{t}", {l}))'
w('a1.c',[(EB,P('-eb',3))])
w('a2.c',[(EB,N('-eb',3))])
w('a3.c',[(IP,Y('-ip',3))])
w('a4.c',[(IP,N('-ip',3))])
w('a5.c',[(KS,Y('-keys',5))])
w('a6.c',[(SS,Y('-s',2))])
w('a7.c',[(KS,N('-keys',5))])
w('a8.c',[(SS,N('-s',2))])
w('a9.c',[(IP,Y('-ip',3)),(KS,Y('-keys',5)),(SS,Y('-s',2))])
w('a10.c',[(WB,P('-wb',3))])
w('a11.c',[(EB,P('-eb',3)),(IP,N('-ip',3))])

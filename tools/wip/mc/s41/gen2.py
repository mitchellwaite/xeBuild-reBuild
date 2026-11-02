src=open('H5b.c').read()
R='k55l: if (!strnicmp(argv[i], "-r", 2))'; W='k61l: if (!strnicmp(argv[i], "-w", 2))'
E_='k67l: if (E(!strnicmp(argv[i], "-e", 2)))'; C='else if (E(!strnicmp(argv[i], "-c", 2)))'
for x in [R,W,E_,C]: assert x in src,x
def w(n,reps):
    s=src
    for a,b in reps: s=s.replace(a,b,1)
    open(n,'w',newline='\n').write(s)
w('b1.c',[(R,R.replace('if (!strnicmp(argv[i], "-r", 2))','if (E(!strnicmp(argv[i], "-r", 2)))'))])
w('b2.c',[(W,W.replace('if (!strnicmp(argv[i], "-w", 2))','if (E(!strnicmp(argv[i], "-w", 2)))'))])
w('b3.c',[(E_,'k67l: if (!strnicmp(argv[i], "-e", 2))')])
w('b4.c',[(C,'else if (!strnicmp(argv[i], "-c", 2))')])
w('b5.c',[(R,R.replace('if (!strnicmp(argv[i], "-r", 2))','if (E(!strnicmp(argv[i], "-r", 2)))')),(W,W.replace('if (!strnicmp(argv[i], "-w", 2))','if (E(!strnicmp(argv[i], "-w", 2)))'))])
w('b6.c',[(E_,'k67l: if (!strnicmp(argv[i], "-e", 2))'),(C,'else if (!strnicmp(argv[i], "-c", 2))')])

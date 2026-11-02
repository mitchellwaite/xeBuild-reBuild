import glob,os,sys
O='if (({__asm__ goto("" :::: r5x); 0;}) || i + 1 == argc || !a || *a == \'-\')\n\t\t\t\tclient_usage(3, argv[i]);'
N='if (({__asm__ goto("" :::: r5x, r3x); 0;}) || i + 1 == argc || !a || *a == \'-\')\n\t\t\t\t{ r3x: client_usage(3, argv[i]); }'
n=0
for f in sorted(glob.glob('s99/*.c')+glob.glob('s100/*.c')+glob.glob('s101/*.c')):
    s=open(f).read()
    if O in s:
        d=os.path.normpath(f).replace(os.sep,'_')
        open('s102/rr/'+d,'w',newline='\n').write(s.replace(O,N)); n+=1
print(n)

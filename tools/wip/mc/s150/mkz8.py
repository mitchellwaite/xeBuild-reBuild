# memset target must not be &dummy: that CSEs with arg = dummy (r91) and flips the -i/-p tie
s=open('qkak2.c',newline='').read()
M='__builtin_memset(dummy, 0, kk);'; assert s.count(M)==1
for n,T_ in (('r1','argv'),('r2','&j'),('r3','&reboot'),('r4','&mode'),('r5','&cinfo')):
    open(n+'.c','w',newline='\n').write(s.replace(M,'__builtin_memset(%s, 0, kk);'%T_))

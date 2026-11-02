import itertools
T=open('b0.c').read()
anch={
 'ne':'promptEnter = 0;',
 'rb':'reboot = 2;',
 'rd':'mode = 8;',
 'eb':'mode = 10;',
 'ky':'arg = dummy;\n\t\t} else if (!strnicmp(argv[i], "-ip", 3)) {',
 'ipl':'log_printf(0, "setting forced IP to %s\n", ip);',
 'w2':'mode = 2;',
 'm4':'mode = 4;',
 'm5':'mode = 5;',
 'm12':'mode = 12;',
 'm7':'mode = 7;',
 'm11':'mode = 11;',
 'm9':'mode = 9;',
}
out=[]
k=900
for tgt in ['r5x','r3x','u2']:
  for a,s in anch.items():
    for n in (1,2):
      k+=1
      cond=' && '.join('__builtin_constant_p(i + %d)'%(k*10+q) for q in range(n))
      if a=='ky': new=s.replace('arg = dummy;','arg = dummy; if (%s) goto %s;'%(cond,tgt),1)
      else: new=s+' if (%s) goto %s;'%(cond,tgt)
      if T.count(s)!=1: print('BAD',a,T.count(s)); continue
      open('v1/%s_%s_%d.c'%(tgt,a,n),'w',newline='\n').write(T.replace(s,new))

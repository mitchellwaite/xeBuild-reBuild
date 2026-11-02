# raise dy to frequency 3+ so it pops between efail and the -w test: the -w label then isn't aligned (prev freq rule)
s=open('w3fr.c',newline='').read()
a='if (__builtin_constant_p(block + 900)) goto dy; ybk:;'; assert s.count(a)==1
j='JMP(efail); if (block < cinfo'; assert s.count(j)==1
V={'x1':s.replace(a,'if (__builtin_constant_p(block + 900)) goto dy; ybk:; if (__builtin_constant_p(block + 904)) goto dy; ybk2:;'),
   'x2':s.replace(j,'if (__builtin_constant_p(block + 905)) goto dy; ybk3:; '+j),
   'x3':s.replace(j,'if (__builtin_constant_p(block + 905)) goto dy; ybk3:; '+j).replace(a,'ybk:;'),
   'x4':s.replace(j,'if (__builtin_constant_p(block + 905) && __builtin_constant_p(block + 906)) goto dy; ybk3:; '+j),
   }
for n,x in V.items(): open(n+'.c','w',newline='\n').write(x)

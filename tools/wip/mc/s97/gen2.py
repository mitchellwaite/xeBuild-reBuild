import sys
base,pfx=sys.argv[1],sys.argv[2]
s=open(base).read()
o='Failed to erase block 0x%x!\\n", block); }\n\t\t} else\n\t\t\t{ eout'
assert s.count(o)==1
for c in range(1,9):
  g=' && '.join('__builtin_constant_p(block + %d)'%(950+j) for j in range(c))
  for t in ('efail','eout','einv'):
    x='if (%s) goto %s;'%(g,t)
    open('%s_%s_%d.c'%(pfx,t,c),'w',newline='\n').write(s.replace(o,o.replace('block); }','block); %s }'%x)))

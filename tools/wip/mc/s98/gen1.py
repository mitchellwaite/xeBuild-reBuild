import sys
base,pfx=sys.argv[1],sys.argv[2]
s=open(base).read()
FA='{ AT(efail) log_printf(0, "\\n\\n***** ERROR: Failed to erase block 0x%x!\\n", block); }\n\t\t} else\n\t\t\t{ eout'
P={
 'top':('\n\n\n\tif (block != -1) {\n\t\tif (block < cinfo','\n\t{X}\n\n\tif (block != -1) {\n\t\tif (block < cinfo'),
 'er':('eerase: if (__builtin_constant_p(block + 77)) goto einv;','eerase: if (__builtin_constant_p(block + 77)) goto einv; {X}'),
 'su':('esucc:  log_printf(0, "Success!\\n");','esucc:  log_printf(0, "Success!\\n"); {X}'),
 'su0':('esucc:  log_printf(0, "Success!\\n");','esucc: {X} log_printf(0, "Success!\\n");'),
 'ou':('goto einv; JUMP(efail); }','goto einv; {X} }'),
 'fa':(FA,FA.replace('block); }','block); {X} }',1)),
}
only=sys.argv[3].split(',') if len(sys.argv)>3 else None
for p,(o,n) in P.items():
  if only and p not in only: continue
  assert s.count(o)==1,p
  for t in ['efail','esucc','eout','einv','eerase']:
    for c in (1,2):
      g=' && '.join('__builtin_constant_p(block + %d)'%(900+10*c+j) for j in range(c))
      x='if (%s) goto %s;'%(g,t)
      open('%s_%s_%s_%d.c'%(pfx,p,t,c),'w',newline='\n').write(s.replace(o,n.replace('{X}',x)))

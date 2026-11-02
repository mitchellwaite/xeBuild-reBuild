# g2.py BASE PFX : self-loop sweeps (wrap statement S as "Lq: S if(cp) goto Lq;")
import sys
base,pfx=sys.argv[1],sys.argv[2]
s=open(base).read()
V='block'
ST={
 'ers':r'log_printf(0, "erasing block 0x%x...", block);',
 'suc':r'log_printf(0, "Success!\n");',
 'fer':r'log_printf(0, "\n\n***** ERROR: Failed to erase block 0x%x!\n", block);',
 'blk':r'log_printf(0, "\n\n***** ERROR: Block 0x%x is outside system area!\n", block);',
 'inv':r'log_printf(0, "\n\n***** ERROR: Invalid arguments specified, please provide hex only for offset!\n");',
 'rpr':r'log_printf(0, "setting read filename to %s\n", arg);',
 'wpr':r'log_printf(0, "setting write filename to %s\n", arg);',
 'wm2':r'mode = 2;',
 'rm1':r'mode = 1;',
 'epr':r'log_printf(0, "setting avatar/kinect files base path to %s\n", arg);',
 'ipr':r'log_printf(0, "setting forced IP to %s\n", ip);',
}
only=sys.argv[3].split(',') if len(sys.argv)>3 else list(ST)
forms=sys.argv[4].split(',') if len(sys.argv)>4 else ['w','a','b']
for k in only:
  st=ST[k]
  # find occurrence: last occurrence for erase-function strings (clientEraseBlockI is 2nd copy)
  i=s.rfind(st); assert i>=0,k
  v='block' if k in('ers','suc','fer','blk','inv') else 'i'
  for f in forms:
    c='if (__builtin_constant_p(%s + 97%d)) goto Lq%s;'%(v,len(k),k)
    if f=='w': n='Lq%s: %s %s'%(k,st,c)     # loop around stmt
    elif f=='a': n='%s Lq%s: %s'%(st,k,c)   # empty loop after
    elif f=='b': n='Lq%s: %s %s'%(k,c,st)   # empty loop before
    open('%s_%s_%s.c'%(pfx,k,f),'w',newline='\n').write(s[:i]+n+s[i+len(st):])

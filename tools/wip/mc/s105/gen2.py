src=open('base.c').read()
L="if (__builtin_constant_p(i + 777100) && __builtin_constant_p(i + 778100)) goto wb3; if (__builtin_constant_p(i + 888100) && __builtin_constant_p(i + 889100) && __builtin_constant_p(i + 890100)) goto wb4;\n"
U="if (__builtin_constant_p(i + 320) && __builtin_constant_p(i + 321)) goto u2;\n"
assert L in src and U in src
def cp(n,b): return " && ".join("__builtin_constant_p(i + %d)"%(b+k*1000) for k in range(n))
s0=src.replace(L,"")
n=0
for w in (1,2,3):
 for f in (2,3,4,5):
  for pos in ('pre','post'):
   for k in (0,2,3,4,5):
    wb3="if (%s) goto wb3; "%cp(w,777100); wb4="if (%s) goto wb4; "%cp(f,888100)
    kk=("if (%s) goto k55l; "%cp(k,555100)) if k else ""
    if pos=='pre': s=s0.replace(U,wb3+wb4+kk+"\n"+U)
    else: s=s0.replace(U,wb3+"\n"+U+wb4+kk+"\n")
    open('g/w%df%d%sk%d.c'%(w,f,pos,k),'w',newline='\n').write(s); n+=1
print(n)

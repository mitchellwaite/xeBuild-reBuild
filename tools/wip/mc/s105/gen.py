import sys,re
src=open('base.c').read()
F="if (__builtin_constant_p(i + 888100) && __builtin_constant_p(i + 889100) && __builtin_constant_p(i + 890100)) goto wb4;"
def cp(n,base):
    return " && ".join("__builtin_constant_p(i + %d)"%(base+k*1000) for k in range(n))
assert F in src
v={}
nofeed=src.replace(F,"")
anchors={
 'noenter':'\t\t\tpromptEnter = 0;\n',
 'reboot':'\t\t\treboot = 2;\n',
 'bp':'\t\t\tmode = 11;\n',
 'rb':'\t\t\tmode = 8;\n',
 'u2':'if (__builtin_constant_p(i + 320) && __builtin_constant_p(i + 321)) goto u2;\n',
 'help':'\t\t\tclient_usage(0, NULL);\n',
}
for name,a in anchors.items():
    assert nofeed.count(a)>=1,name
    for n in (1,2,3,4,5):
        s=nofeed.replace(a,a+" if (%s) goto wb4;\n"%cp(n,991100),1)
        v['%s_%d'%(name,n)]=s
# split: keep loop feed but weaker and add a second
for n in (1,2):
  for m in (2,3,4):
    s=src.replace(F,"if (%s) goto wb4;"%cp(n,881100)).replace(anchors['rb'],anchors['rb']+" if (%s) goto wb4;\n"%cp(m,991100),1)
    v['spl%d_%d'%(n,m)]=s
for k,s in v.items(): open('v_%s.c'%k,'w',newline='\n').write(s)
print(len(v))

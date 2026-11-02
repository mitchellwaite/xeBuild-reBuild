#!/bin/sh
# dd.sh SRC.c : bbro final order with trace ids (from 40th block on)
R=/c/Users/Win11VM/Documents/GitHub/xebuildBugFix; export PATH=$R/tools/toolchain-4745/mingw32/bin:$R/tools/toolchain-4745/bin:$PATH
n=$(basename $1 .c); mkdir -p d/$n; cp $1 d/$n/x.c; (cd d/$n && gcc -S -I$R/src -O3 -fno-toplevel-reorder -fno-ipa-profile -fno-reorder-functions --param builtin-expect-probability=50 $FX -fdump-rtl-bbro-details x.c -o x.s && awk '/^;; Function mode_client/{p=1} p&&/^;; Function/&&!/mode_client/{exit} p' x.c.*bbro > mc.bbro && rm -f x.c.*bbro)
python bbinfo2.py d/$n/mc.bbro > d/$n/order.txt
python - d/$n/order.txt <<'P'
import sys,re
LC={'LC118':'Block','LC114':'Ferase','LC156':'hdd5','LC155':'hdd4','LC117':'LC117','LC157':'invalid','LC140':'-ip','LC142':'-r','LC144':'-w','LC146':'-e','LC148':'-c','LC150':'-i','LC152':'-p','LC139':'-keys','LC115':'LC115','LC116':'LC116'}
out=[];last=None
for l in open(sys.argv[1]):
    p=l.split(); n=int(p[0]);
    if n<56: continue
    t=p[3]; lab=[]
    for x in p[6:]:
        x=x.lstrip('*_')
        if x in LC: lab.append(LC[x]+':'+p[5])
        elif x.startswith('LC') or x.startswith('L') and x[1:].isdigit() or x in('log_printf','cinfo','strnicmp'): pass
        else: lab.append(x.replace('client_usage','CU').replace('client','')+':'+p[5])
    if t!=last: out.append('['+t+']'); last=t
    out+= lab
print(' '.join(out))
P

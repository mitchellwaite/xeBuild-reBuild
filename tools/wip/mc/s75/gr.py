import subprocess,sys,os,random,json
# gr.py BASE.c : greedy hill-climb over string-replacement levers, fncmp count via f.sh
base=open(sys.argv[1]).read()
B=lambda n,k:' && '.join('__builtin_constant_p(block + %d)'%(n+i) for i in range(k))
C=[]
def cold(anchor,tag,kind='cold'):
    C.append((anchor, anchor.replace('@', ' { %s: __attribute__((%s)); } '%(tag,kind)).replace('@','')))
sites=[('AT(hdd5)@log_printf','h5'),('AT(cdef)@if','cd'),('AT(c7)@if','c7'),('AT(c12)@if','c12'),
 ('AT(i0)@clientInfo(NULL)','i0'),('AT(p0)@clientPatches(NULL)','p0'),('AT(i1)@clientInfo(arg)','i1'),('AT(p1)@clientPatches(arg)','p1'),
 ('eout:@log_printf','eo'),('AT(efail)@log_printf','ef'),('einv:@log_printf','ei'),('esucc:@log_printf','es'),
 ('AT(c1)@netDumpNand','c1'),('AT(c2)@clientWrite','c2'),('AT(c8)@{ clientReadBlocks','c8'),('AT(c9)@{ clientWriteBlocks','c9'),
 ('AT(c10)@clientEraseBlockI','c10'),('AT(c11)@clientBinPatch','c11'),('AT(s5)@{ JMP(s4,c12)','s5'),('AT(hdd4)@','h4x')]
for a,t in sites:
    for kind in ('cold','hot'):
        a2=a.replace('@',' ')
        if a2 in base:
            C.append((a2, a.replace('@',' { %s%s: __attribute__((%s)); } '%(t,kind[0],kind))))
for k in range(1,6):
    for tgt in ('efail','eout','einv','esucc'):
        C.append(('uint32_t block = myatoh32(sblock, -1);if','uint32_t block = myatoh32(sblock, -1);if (%s) goto %s; if'%(B(140+20*k,k),tgt)))
C=[c for c in C if c[0] in base]
print(len(C),'cands',flush=True)
def score(src,tag):
    p='v/gr_%s.c'%tag
    open(p,'w',newline='\n').write(src)
    r=subprocess.run(['sh','f.sh',p],capture_output=True,text=True)
    try: return int(r.stdout.strip())
    except: return 9999
cur=base; cs=score(cur,'base'); print('base',cs,flush=True)
log=open('gr.log','a')
for rnd in range(3):
    improved=False
    for i,(o,n) in enumerate(C):
        if o not in cur: continue
        s=cur.replace(o,n,1); sc=score(s,'t')
        log.write('%d %d %d\n'%(rnd,i,sc)); log.flush()
        if sc<cs:
            cur,cs=s,sc; improved=True; print('accept',rnd,i,n[:80],sc,flush=True)
            open('gr_best.c','w',newline='\n').write(cur)
    if not improved: break
print('final',cs)

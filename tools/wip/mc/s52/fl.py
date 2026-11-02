import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import lp4, es
BC='__builtin_constant_p(mode + %d)'
def fl(s, d, tgt, which=1):
    cond=' && '.join(BC%(61+k) for k in range(d))
    lab={'ret':'fkret','rb':'fkrb'}[tgt]
    if tgt=='ret': s=s.replace('\tnetDisconnect();\n\treturn 0;\nfail:','\tfkret: netDisconnect();\n\treturn 0;\nfail:',1)
    if tgt=='rb': s=s.replace('\tif (E(reboot))\n','\tfkrb: if (E(reboot))\n',1)
    parts=s.split('\t\t\t} else\n\t\t\t\tgoto fail;' if which==1 else '\t\t} else\n\t\t\tgoto fail;')
    assert len(parts)>=2, 'site'
    rep=('\t\t\t} else\n\t\t\t\t{ if (%s) goto %s; goto fail; }' if which==1 else '\t\t} else\n\t\t\t{ if (%s) goto %s; goto fail; }')%(cond,lab)
    return rep.join([parts[0],(('\t\t\t} else\n\t\t\t\tgoto fail;' if which==1 else '\t\t} else\n\t\t\tgoto fail;')).join(parts[1:])])
if __name__=='__main__':
    for a in sys.argv[1:]:
        d,tgt,w=a.split(',')
        tag='s52f_'+a.replace(',','_')
        try: t=fl(lp4.mk(9,21,0,'tail',2,'A'),int(d),tgt,int(w))
        except AssertionError as e: print(a,'nosite'); continue
        r=es.run(t,tag,fncmp=False)
        tr=[l.split(':')[1].strip() for l in open(os.path.join(es.R,'build','v','mc42','slot_'+tag,'bbro_mc.txt')) if l.startswith('Trace') and '(round 2)' in l] if r else []
        print(a,r,tr[:5],flush=True)

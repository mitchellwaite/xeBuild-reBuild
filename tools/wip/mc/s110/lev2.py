import sys,re; sys.path.insert(0,'../s109'); import lev
from cond import conds
COLD={'gi':'netGetInfo','sa':'sendAvatarData','nc':'netConnect'}
LOCC={'bp':('clientBinPatch','void %s(const char *file, const char *soff)'),'ci':('clientInfo','void %s(const char *dir)'),'wb':('clientWriteBlocks','void %s(const char *file, const char *sstart)')}
def apply(cfg):
    s=lev.apply({k:v for k,v in cfg.items() if k not in('x','cold','opt','xt')})
    st=s.index('int mode_client(int argc')
    x=cfg.get('x',-1)
    if x>=0:
        a,b,c=conds(s[st:])[x]; a+=st;b+=st
        parts=re.split(r' (\|\||&&) ',c); t=cfg.get('xt',-1)
        if t<0 or t*2>=len(parts): new='__builtin_expect(!!(%s), 0)'%c
        else: parts[t*2]='__builtin_expect(!!(%s), 0)'%parts[t*2]; new=' '.join(parts)
        if c.startswith('E('): new=c[2:-1]
        s=s[:a]+new+s[b:]
    cd=cfg.get('cold','n'); st=s.index('int mode_client(int argc')
    if cd in COLD: s=s[:st]+'extern __typeof__(%s) %s __attribute__((cold));\n'%(COLD[cd],COLD[cd])+s[st:]
    elif cd in LOCC:
        f,p=LOCC[cd]; body=re.sub(r'\b%s\('%f,f+'A(',s[st:])
        s=s[:st]+p%(f+'A')+' __asm__("_%s") __attribute__((cold)); /* TODO(prototype cast) */\n'%f+body
    o=cfg.get('opt','n')
    if o!='n': s=s.replace('int mode_client(int argc','__attribute__((optimize("%s"))) int mode_client(int argc'%o,1)
    return s
name=lev.name

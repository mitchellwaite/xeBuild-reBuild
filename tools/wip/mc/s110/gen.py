import sys,re
src=open('h0.c').read().split('\n')
MC=557  # index of 'int mode_client' line
ext={'log_printf':'void log_printf(unsigned int level, const char *fmt, ...)',
'netReboot':'int netReboot(int how)','netConnect':None,'netGetInfo':None,'netDisconnect':None,'netDumpNand':None,
'sendAvatarData':None,'sendCompatData':None,'strnicmp':None}
loc={'clientBinPatch':'void %s(const char *file, const char *soff)','clientInfo':'void %s(const char *dir)',
'clientPatches':'void %s(const char *file)','clientWrite':'int %s(const char *file)','clientKeys':'void %s(void)',
'clientReadBlocks':'void %s(const char *file, const char *sstart, const char *scount)',
'clientWriteBlocks':'void %s(const char *file, const char *sstart)',
'client_usage':'void %s(int err, const char *arg) __attribute__((noreturn))'}
def emit(name,pre,repl,fnattr=None):
    s=list(src)
    body='\n'.join(s[MC:])
    for a,b in repl: body=re.sub(r'\b%s\('%a,b+'(',body)
    head=s[:MC]
    if fnattr: body=body.replace('int mode_client(int argc','%s int mode_client(int argc'%fnattr,1)
    open('v/%s.c'%name,'w',newline='\n').write('\n'.join(head)+'\n'+pre+'\n'+body)
import os; os.makedirs('v',exist_ok=True)
for at in ['cold','hot','noinline','noclone']:
  for f,proto in loc.items():
    emit('L_%s_%s'%(at,f),'%s __asm__("_%s") __attribute__((%s)); /* TODO(prototype cast) */'%(proto%(f+'A'),f,at),[(f,f+'A')])
for at in ['cold','hot','leaf','nothrow']:
  for f in ['log_printf','netReboot','netConnect','netGetInfo','netDisconnect','netDumpNand','sendAvatarData','sendCompatData','strnicmp']:
    emit('E_%s_%s'%(at,f),'extern __typeof__(%s) %s __attribute__((%s));'%(f,f,at),[])
emit('E_pure_strnicmp','extern __typeof__(strnicmp) strnicmp __attribute__((pure));',[])
for o in ['no-tree-dominator-opts','no-thread-jumps','no-tree-tail-merge','no-crossjumping','no-tree-ch','no-tree-vrp','no-guess-branch-probability','no-reorder-blocks-and-partition','no-tree-pre','no-ipa-cp','no-tree-switch-conversion','no-if-conversion','no-tree-sink','no-gcse','no-cse-follow-jumps','no-expensive-optimizations','no-tree-loop-optimize','no-peel-loops','no-split-paths','no-hoist-adjacent-loads','no-tree-copy-prop','no-tree-forwprop','no-ssa-phiopt','no-tree-fre','no-code-hoisting','no-tree-coalesce-vars','no-shrink-wrap','no-schedule-insns2','no-optimize-sibling-calls','no-tree-dce','no-ipa-ra','no-tree-cselim','no-tree-bit-ccp','no-tree-ccp','no-ipa-pure-const','no-inline-small-functions','no-inline-functions','no-tree-loop-vectorize','no-unswitch-loops','no-predictive-commoning']:
    emit('O_'+o.replace('-','_'),'',[],'__attribute__((optimize("%s")))'%o)

# mky.py : keyed zero-byte dummy dy: JMP(dy) from the f0 efail log, dy's frequency from a dead constant_p edge
s=open('n0.c',newline='').read().split('\n')
ie=[i for i,x in enumerate(s) if 'AT(efail)' in x][-1]
er=[i for i,x in enumerate(s) if 'eerase:' in x][-1]
iv=[i for i,x in enumerate(s) if 'einv: __attribute__((cold));' in x][-1]
cp=lambda a:'__builtin_constant_p(block + %d)'%a
def mk(n,src,ret):
    x=list(s)
    j=x[ie].rstrip(); assert j.endswith('}'); x[ie]=j[:-1]+'JMP(dy); }'
    x[iv]=x[iv].replace('{ einv:','{ if (0) { dy: asm volatile(""); '+ret+' __builtin_unreachable(); } einv:',1)
    k=x[er].index('log_printf'); x[er]=x[er][:k]+src+' '+x[er][k:]
    open(n+'.c','w',newline='\n').write('\n'.join(x))
back='if (%s) goto ybk;'%cp(901)
mk('y1','if (%s) goto dy; ybk:;'%cp(900),back)
mk('y2','if (%s && %s) goto dy; ybk:;'%(cp(900),cp(902)),back)
mk('y3','if (%s && %s && %s) goto dy; ybk:;'%(cp(900),cp(902),cp(903)),back)
mk('y4','if (%s) goto dy;'%cp(900),'')
mk('y5','if (%s && %s) goto dy;'%(cp(900),cp(902)),'')

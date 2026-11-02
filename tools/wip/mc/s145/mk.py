src=open('fb.c').read()
i=src.index('AT(efail) log_printf'); i=src.index('AT(efail) log_printf',i+1)
j=src.index('}',src.index('block);',i))   # closing brace of efail block
end='{ einv: __attribute__((cold));'
opt='/* the option'
def mk(n,ins,f=None):
    s=src[:j]+ins+' '+src[j:]
    if f: s=f(s)
    open(n+'.c','w',newline='\n').write(s)
mk('c1','JMP(ex);',lambda s:s.replace(end,'{ ex: einv: __attribute__((cold));',1))
mk('c2','JMP(einv);')
k=lambda body:(lambda s:s[:s.index(opt)-3]+body+s[s.index(opt)-3:])
mk('c3','JMP(ex);',k('\n\tif (0) { ex: __asm__ volatile(""); }'))
mk('c4','JMP(ex);',k('\n\treturn; ex: __asm__ volatile("");'))
mk('c5','JMP(ex);',k('\n\treturn; ex: log_printf(0, "Success!\n");'))

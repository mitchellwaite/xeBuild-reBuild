# zero-byte register pin of i+1 in the -i and -p tests (reference keeps it in edx, i-copy in eax)
s=open('r1.c',newline='').read().split('\n')
ii=[n for n,x in enumerate(s) if '"-i", 2' in x and 'strnicmp' in x][-1]
ip=[n for n,x in enumerate(s) if '"-p", 2' in x and 'strnicmp' in x][-1]
t="if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')"
assert t in s[ii+1] and t in s[ip+1]
P='({ __asm__ ("" :: "d"(i + 1)); 0; })'
V={'p1':"if (!argv[i + 1] || "+P+" || i + 1 == argc || *argv[i + 1] == '-')",
   'p2':"if (!argv[i + 1] || i + 1 == argc || "+P+" || *argv[i + 1] == '-')",
   'p3':"if ("+P+" || !argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')",
   'p4':"if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-' || "+P+")"}
for n,v in V.items():
    x=list(s); x[ii+1]=x[ii+1].replace(t,v); x[ip+1]=x[ip+1].replace(t,v)
    open(n+'.c','w',newline='\n').write('\n'.join(x))

import sys; sys.path.insert(0,'../s86'); sys.path.insert(0,r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip'); import fibsim
B=[int(x) for x in sys.argv[1].split(',')]
for d in sys.argv[2:]:
    ev=fibsim.parse('dd/%s/mc.bbro'%d); k={}
    i4=ev.index(('round',4))
    for e in ev[:i4]:
        if e[0]=='push': k[e[1]]=e[2]
        elif e[0]=='ins': k[e[2]]=e[3]
        elif e[0]=='chg': k[e[1]]=e[2]
    print('%-6s'%d, ' '.join('%d:%s'%(b,k.get(b,'-')) for b in B))

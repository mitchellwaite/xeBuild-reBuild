import sys,re
t=open(sys.argv[1]).read(); t=t[t.index(';; Function mode_client'):]
t=t[t.index(';;   basic block '):]
out=[]
for w in ('"-s"','"-keys"','"-ip"'):
    i=t.index('strnicmp (_', t.index(w+', ')-40)
    h=t.rindex(';;   basic block ',0,i); m=re.match(r';;   basic block (\d+), loop depth \d+, count \d+, freq (\d+)',t[h:])
    j=t.index('succ:',i); su=re.findall(r'(\d+) \[([\d.]+)%\]',t[j:j+200])[:2]
    out.append('%s:bb%s f%s %s'%(w.strip('"'),m.group(1),m.group(2),' '.join('%s/%s'%x for x in su)))
print(' | '.join(out))
o2=[]
for w in ('command line, ignoring -s','shutdown on','"-keys"'):
    i=t.index(w); h=t.rindex(';;   basic block ',0,i); m=re.match(r';;   basic block (\d+), loop depth \d+, count \d+, freq (\d+)',t[h:]); o2.append('%s=%s'%(w[:6],m.group(2)))
sys.stdout.write('   ['+' '.join(o2)+']\n')

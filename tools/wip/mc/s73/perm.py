import re,subprocess,itertools,sys,shutil
cur=sys.argv[1]; s=open(cur).read()
def score(t,n='pp'):
    open(n+'.c','w',newline='\n').write(t)
    r=subprocess.run(['sh','f.sh',n+'.c'],capture_output=True,text=True); return int(r.stdout.strip() or 999)
best=score(s); print('base',best,flush=True)
pat=re.compile(r"if \(((?:!?argv\[i \+ 1\]|!?[ab]|[ij]? ?\+? ?\d? ?== argc|i \+ \d == argc|j == argc|k == argc|\*argv\[i \+ 1\] == '-'|\*[ab] == '-'))( \|\| (?:[^()]|\([^()]*\))+?)\)\n")
improved=True
while improved:
    improved=False
    for m in list(pat.finditer(s)):
        full=m.group(0); inner=full[4:-2]
        parts=[p for p in inner.split(' || ')]
        if len(parts)<2 or len(parts)>4: continue
        for pm in itertools.permutations(parts):
            if list(pm)==parts: continue
            t=s.replace(full,'if ('+' || '.join(pm)+')\n',1)
            if t==s: continue
            c=score(t)
            if c<best:
                best=c; s=t; improved=True; print(best,' || '.join(pm),flush=True); open('perm_best.c','w',newline='\n').write(s); break
        if improved: break
print('final',best)

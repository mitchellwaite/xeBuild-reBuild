import sys,importlib.util,itertools
gen,base,lab,out=sys.argv[1:5]
sp=importlib.util.spec_from_file_location('g',gen);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
t=open(base,newline='').read().replace('\r\n','\n')
for c in itertools.product(*m.AXES):
    if '+'.join(x[0] for x in c if x[0])==lab:
        for l,ed in c:
            for x,y in ed:
                assert x in t,x; t=t.replace(x,y)
        open(out,'w',newline='\n').write(t);break
else: raise SystemExit('no state')

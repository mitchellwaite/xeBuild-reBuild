def cond(d,o): return ' && '.join('__builtin_constant_p(mode + %d)'%(o+k) for k in range(d))
def mod(s):
    a='			cinfo = netGetInfo();\n			switch (mode) {'; assert s.count(a)==1
    g=''.join('if (%s) goto %s; '%(cond(d,900+10*i),l) for i,(l,d) in enumerate([('c12',1),('c3',2),('c1',3)]))
    return s.replace(a,'			cinfo = netGetInfo();\n			'+g+'\n			switch (mode) {',1)

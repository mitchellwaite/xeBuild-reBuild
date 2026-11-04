"""fl10n.py [write]: forms of the never-written-static exit (a dead test: candidate at most).  write saves the first match as drafts/filelist_ini_findKey_candidate2.c next to the patch."""
import os, subprocess, sys
import fllib as L, fl10lib as F
T = "if (*q != 0)"
PRE = "static int iniStopOnEmpty;\t/* never set: an empty value keeps the search going */\n\n"
V = {
 'and-1': F.fk(F.KF_NONE.replace(T, "if (iniStopOnEmpty && *q == 0)\n\t\t\t\t\treturn -1;\n\t\t\t\t" + T), PRE),
 'stop-1': F.fk(F.KF_NONE.replace(T, "if (iniStopOnEmpty)\n\t\t\t\t\treturn -1;\n\t\t\t\t" + T), PRE),
}
rs = F.run(V, 'n')
if len(sys.argv) > 1 and rs[0][2]:
    n = rs[0][0]
    o = L.compile(V[n], ['-O3'], 'n10')
    print('sections differing from build/obj:', [k for k in L.sections(o) if L.sections(o)[k] != L.sections(os.path.join(L.R, 'build', 'obj', 'filelist_ini.o')).get(k)], 'same', L.same(o))
    p = os.path.join(F.A10, 'cand2.c')
    open(p, 'w', newline='\n').write(V[n])
    d = subprocess.run(['git', 'diff', '--no-index', '--no-color', os.path.join(L.R, 'src', 'filelist_ini.c'), p], stdout=subprocess.PIPE).stdout.decode()
    open(os.path.join(L.R, 'tools', 'wip', 'dehint', 'drafts', 'filelist_ini_findKey_candidate2.patch'), 'w', newline='\n').write(d)
    print(d)

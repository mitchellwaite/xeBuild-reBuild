"""fl6final.py [write]: attempt 6's draft from current src: findKey's dead key == NULL replaced by the split value test.
Verifies whole-object and per-section against build/obj/filelist_ini.o and the reference.  Change this, not the draft.
Also tries other spellings of the split (`spell`)."""
import os, sys
import fllib as L, fl6lib as F

OLD = ("\t\t\t\tunsigned char *q = &buf[i + len];\n\n" + F.KF +
       "\t\t\t\tif (*q != 0)\n\t\t\t\t\treturn i + len;\n")
assert F.S0.count(OLD) == 1
NEW = ("\t\t\t\t/* one test written as two so that the loop has three exits when gcc estimates branch\n"
       "\t\t\t\t   probabilities (9% / exits), which sets the frequencies the getters' registers follow;\n"
       "\t\t\t\t   ifcombine then merges them into c != 0 (notes/filelist_ini.md) */\n"
       "\t\t\t\tchar c = buf[i + len];\n\n"
       "\t\t\t\tif (c > 0)\n\t\t\t\t\treturn i + len;\n"
       "\t\t\t\tif (c < 0)\n\t\t\t\t\treturn i + len;\n")
SPELL = {
    'or': "\t\t\t\tchar c = buf[i + len];\n\n\t\t\t\tif (c > 0 || c < 0)\n\t\t\t\t\treturn i + len;\n",
    'elif': "\t\t\t\tchar c = buf[i + len];\n\n\t\t\t\tif (c > 0)\n\t\t\t\t\treturn i + len;\n\t\t\t\telse if (c < 0)\n\t\t\t\t\treturn i + len;\n",
    'nochar': "\t\t\t\tif ((char)buf[i + len] > 0)\n\t\t\t\t\treturn i + len;\n\t\t\t\tif ((char)buf[i + len] < 0)\n\t\t\t\t\treturn i + len;\n",
    'eq': "\t\t\t\tint c = (char)buf[i + len];\n\n\t\t\t\tif (c > 0)\n\t\t\t\t\treturn i + len;\n\t\t\t\tif (c < 0)\n\t\t\t\t\treturn i + len;\n",
    'neq': "\t\t\t\tunsigned char c = buf[i + len];\n\n\t\t\t\tif (c > 0)\n\t\t\t\t\treturn i + len;\n\t\t\t\tif (c != 0)\n\t\t\t\t\treturn i + len;\n",
}
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'spell':
        F.run({k: L.sub(F.S0, OLD, v) for k, v in SPELL.items()}, 'spell', 8)
        sys.exit()
    s = L.sub(F.S0, OLD, NEW)
    o = L.compile(s, ['-O3'], 'a6final')
    assert L.same(o), L.score(o)[:4]
    a = L.sections(o)
    for ref in (L.REF, os.path.join(L.R, 'build', 'obj', 'filelist_ini.o')):
        assert a == L.sections(ref)
        assert open(o, 'rb').read() == open(ref, 'rb').read()
    if len(sys.argv) > 1 and sys.argv[1] == 'write':
        with open(L.DRAFT, 'w', newline='\n') as f:
            f.write(s)
    print('MATCH', len(a), 'sections:', sorted(a))

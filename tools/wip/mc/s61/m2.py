def mod(s):
    a='			default:\n				AT(cdef)'; assert s.count(a)==1
    s=s.replace(a,'			case 13: { struct {} q13; __asm__ ("" :: "X"(&q13)); } goto c12;\n'+a,1)
    a='			switch (mode) {\n			case 1:'; assert s.count(a)==1
    return s.replace(a,'			if (mode == 13) __builtin_unreachable();\n'+a,1)

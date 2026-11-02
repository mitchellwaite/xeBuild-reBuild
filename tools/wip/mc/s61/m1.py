def mod(s):
    a='			default:\n				AT(cdef)'; assert s.count(a)==1
    return s.replace(a,'			case 13: { struct {} q13; __asm__ ("" :: "X"(&q13)); } goto c12;\n'+a,1)

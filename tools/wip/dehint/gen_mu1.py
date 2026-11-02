"""First sweep: forms of the 0x test with no dead comparison."""

C0 = ["((dat[0]&0xFF) == '0')", "(dat[0] == '0')"]
CX = ["(myatol(dat[1]&0xFF) == 'x')", "(myatol(dat[1]) == 'x')"]

HEXV = """if(validateString(&dat[2]))
			return myatox32(&dat[2], defValue);"""
DECV = """if(validateString(dat))
			return atoi((const char*)dat);"""

SIG = "uint32_t myatou32(const char* dat, uint32_t defValue)\n"


def bodies(c0, cx):
    both = "%s&&%s" % (c0, cx)
    # plain, for reference
    yield 'plain', "{\n\tif(%s)\n\t{\n\t\t%s\n\t}\n\telse\n\t{\n\t\t%s\n\t}\n\treturn defValue;\n}" % (both, HEXV, DECV)
    # value flags
    for ty in ('int', 'BOOL', 'char', 'unsigned char', 'uint32_t'):
        yield 'val|' + ty, "{\n\t%s hex = %s;\n\tif(hex)\n\t{\n\t\t%s\n\t}\n\telse\n\t{\n\t\t%s\n\t}\n\treturn defValue;\n}" % (ty, both, HEXV, DECV)
        yield 'set|' + ty, "{\n\t%s hex = 0;\n\tif(%s)\n\t\thex = 1;\n\tif(hex)\n\t{\n\t\t%s\n\t}\n\telse\n\t{\n\t\t%s\n\t}\n\treturn defValue;\n}" % (ty, both, HEXV, DECV)
        yield 'nest|' + ty, "{\n\t%s hex = 0;\n\tif(%s)\n\t\tif(%s)\n\t\t\thex = 1;\n\tif(hex)\n\t{\n\t\t%s\n\t}\n\telse\n\t{\n\t\t%s\n\t}\n\treturn defValue;\n}" % (ty, c0, cx, HEXV, DECV)
        yield 'x|' + ty, "{\n\t%s x = %s;\n\tif(%s&&x)\n\t{\n\t\t%s\n\t}\n\telse\n\t{\n\t\t%s\n\t}\n\treturn defValue;\n}" % (ty, cx, c0, HEXV, DECV)
    # temp char
    yield 'tmp', "{\n\tchar c = myatol(dat[1]&0xFF);\n\tif(%s&&(c == 'x'))\n\t{\n\t\t%s\n\t}\n\telse\n\t{\n\t\t%s\n\t}\n\treturn defValue;\n}" % (c0, HEXV, DECV)
    # switch on the prefix
    yield 'sw', "{\n\tif(%s)\n\t{\n\t\tswitch(myatol(dat[1]&0xFF))\n\t\t{\n\t\tcase 'x':\n\t\t\t%s\n\t\t\treturn defValue;\n\t\t}\n\t}\n\t%s\n\treturn defValue;\n}" % (c0, HEXV, DECV)
    yield 'sw2', "{\n\tif(%s)\n\t{\n\t\tswitch(myatol(dat[1]&0xFF))\n\t\t{\n\t\tcase 'x':\n\t\t\t%s\n\t\t\treturn defValue;\n\t\tdefault:\n\t\t\tbreak;\n\t\t}\n\t}\n\t%s\n\treturn defValue;\n}" % (c0, HEXV, DECV)
    yield 'sw0', "{\n\tswitch(dat[0])\n\t{\n\tcase '0':\n\t\tif(%s)\n\t\t{\n\t\t\t%s\n\t\t\treturn defValue;\n\t\t}\n\t}\n\t%s\n\treturn defValue;\n}" % (cx, HEXV, DECV)
    # gotos
    yield 'g1', "{\n\tif(!%s)\n\t\tgoto dec;\n\tif(!%s)\n\t\tgoto dec;\n\t%s\n\treturn defValue;\ndec:\n\t%s\n\treturn defValue;\n}" % (c0, cx, HEXV, DECV)
    yield 'g2', "{\n\tif(%s)\n\t{\n\t\tif(%s)\n\t\t{\n\t\t\t%s\n\t\t\treturn defValue;\n\t\t}\n\t}\n\t%s\n\treturn defValue;\n}" % (c0, cx, HEXV, DECV)
    yield 'g3', "{\n\tif(%s&&%s)\n\t{\n\t\t%s\n\t\treturn defValue;\n\t}\n\t%s\n\treturn defValue;\n}" % (c0, cx, HEXV, DECV)
    yield 'g4', "{\n\tif(%s&&%s)\n\t\tgoto hex;\n\t%s\n\treturn defValue;\nhex:\n\t%s\n\treturn defValue;\n}" % (c0, cx, DECV, HEXV)
    yield 'g5', "{\n\tif(!(%s&&%s))\n\t{\n\t\t%s\n\t\treturn defValue;\n\t}\n\t%s\n\treturn defValue;\n}" % (c0, cx, DECV, HEXV)
    # value kept, one return
    yield 'r1', "{\n\tuint32_t ret = defValue;\n\tif(%s)\n\t{\n\t\tif(validateString(&dat[2]))\n\t\t\tret = myatox32(&dat[2], defValue);\n\t}\n\telse\n\t{\n\t\tif(validateString(dat))\n\t\t\tret = atoi((const char*)dat);\n\t}\n\treturn ret;\n}" % both


def variants():
    for a, c0 in enumerate(C0):
        for b, cx in enumerate(CX):
            for tag, body in bodies(c0, cx):
                yield '%s|c0%d|cx%d' % (tag, a, b), SIG + body
    # helper form: the test in its own small function
    for st in ('static ', 'static inline ', ''):
        for tb, h in (('and', "return ((dat[0]&0xFF) == '0')&&(myatol(dat[1]&0xFF) == 'x');"),
                      ('if', "if(((dat[0]&0xFF) == '0')&&(myatol(dat[1]&0xFF) == 'x'))\n\t\treturn 1;\n\treturn 0;"),
                      ('nest', "if((dat[0]&0xFF) == '0')\n\t\tif(myatol(dat[1]&0xFF) == 'x')\n\t\t\treturn 1;\n\treturn 0;")):
            for ty in ('int', 'uint32_t', 'BOOL'):
                yield 'helper|%s|%s|%s' % (st, tb, ty), "%s%s isHexStr(const char* dat)\n{\n\t%s\n}\n\n%s{\n\tif(isHexStr(dat))\n\t{\n\t\t%s\n\t}\n\telse\n\t{\n\t\t%s\n\t}\n\treturn defValue;\n}" % (st, ty, h, SIG, HEXV, DECV)

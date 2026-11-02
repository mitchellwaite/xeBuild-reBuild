"""Kept x flag with two uses: forwprop won't fold `isx != 0` into the compare when isx has
another use, so the x test stays unpredicted (50%) at profile_estimate, and it's an if, not a
switch, so the true edge comes first."""
import itertools

SIG = "uint32_t myatou32(const char* dat, uint32_t defValue)\n"
C0 = "(dat[0]&0xFF) == '0'"
CX = "myatol(dat[1]&0xFF) == 'x'"
HEX = "if(validateString(&dat[2]))\nreturn myatox32(&dat[2], defValue);\n"
DEC = "if(validateString(dat))\nreturn atoi((const char*)dat);\n"

SHAPES = {
    # the second use is a separate test after the hex attempt
    'a': "if(" + C0 + ")\n{\n%T isx = " + CX + ";\nif(isx&&validateString(&dat[2]))\nreturn myatox32(&dat[2], defValue);\nif(isx)\nreturn defValue;\n}\n" + DEC + "return defValue;\n",
    'b': "if(" + C0 + ")\n{\n%T isx = " + CX + ";\nif(isx)\n{\n" + HEX + "}\nif(isx)\nreturn defValue;\n}\n" + DEC + "return defValue;\n",
    'c': "if(" + C0 + ")\n{\n%T isx = " + CX + ";\nif(isx)\n{\n" + HEX + "}\nif(!isx)\n{\n" + DEC + "}\nreturn defValue;\n}\n" + DEC + "return defValue;\n",
    'd': "%T isx = 0;\nif(" + C0 + ")\n{\nisx = " + CX + ";\nif(isx)\n{\n" + HEX + "}\n}\nif(!isx)\n{\n" + DEC + "}\nreturn defValue;\n",
    'e': "%T isx = 0;\nif(" + C0 + ")\n{\nisx = " + CX + ";\nif(isx&&validateString(&dat[2]))\nreturn myatox32(&dat[2], defValue);\n}\nif(!isx&&validateString(dat))\nreturn atoi((const char*)dat);\nreturn defValue;\n",
    'f': "%T isx = 0;\nif(" + C0 + ")\nif((isx = " + CX + "))\n{\n" + HEX + "}\nif(!isx)\n{\n" + DEC + "}\nreturn defValue;\n",
    'g': "%T isx = 0;\nif((" + C0 + ")&&(isx = " + CX + "))\n{\n" + HEX + "}\nif(isx)\nreturn defValue;\n" + DEC + "return defValue;\n",
    'h': "%T isx = 0;\nif(" + C0 + ")\n{\nisx = " + CX + ";\nif(isx&&validateString(&dat[2]))\nreturn myatox32(&dat[2], defValue);\n}\nif(isx)\nreturn defValue;\n" + DEC + "return defValue;\n",
    # a shared result
    'r': "uint32_t ret = defValue;\n%T isx = 0;\nif(" + C0 + ")\n{\nisx = " + CX + ";\nif(isx&&validateString(&dat[2]))\nret = myatox32(&dat[2], defValue);\n}\nif(!isx&&validateString(dat))\nret = atoi((const char*)dat);\nreturn ret;\n",
    'r2': "uint32_t ret = defValue;\nif(" + C0 + ")\n{\n%T isx = " + CX + ";\nif(isx&&validateString(&dat[2]))\nret = myatox32(&dat[2], defValue);\nif(isx)\nreturn ret;\n}\nif(validateString(dat))\nret = atoi((const char*)dat);\nreturn ret;\n",
    # one validate with a pointer: needs threading across it, expected to fail
    'p': "%T hex = (" + C0 + ")&&(" + CX + ");\nif(hex)\ndat += 2;\nif(validateString(dat))\nreturn hex ? myatox32(dat, defValue) : (uint32_t)atoi((const char*)dat);\nreturn defValue;\n",
}
TY = ['int', 'char', 'unsigned char', 'uint32_t', '_Bool']


def variants():
    for (s, b), ty in itertools.product(SHAPES.items(), TY):
        yield s + '|' + ty, SIG + "{\n" + b.replace('%T', ty) + "}"

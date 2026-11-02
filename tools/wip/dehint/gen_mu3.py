"""Flag family: `if (flag)` has no opcode prediction (compare with 0), so 50% before threading."""
import itertools

SIG = "uint32_t myatou32(const char* dat, uint32_t defValue)\n"
C0 = "(dat[0]&0xFF) == '0'"
CX = "myatol(dat[1]&0xFF) == 'x'"
NCX = "myatol(dat[1]&0xFF) != 'x'"
NC0 = "(dat[0]&0xFF) != '0'"

HEX = "if(validateString(&dat[2]))\nreturn myatox32(&dat[2], defValue);\n"
DEC = "if(validateString(dat))\nreturn atoi((const char*)dat);\n"

SET = {
    'ph0': (0, "%T hex = 0;\nif(" + C0 + ")\nhex = " + CX + ";\n"),
    'ph1': (0, "%T hex;\nif(" + C0 + ")\nhex = " + CX + ";\nelse\nhex = 0;\n"),
    'tern': (0, "%T hex = (" + C0 + ") ? (" + CX + ") : 0;\n"),
    'and': (0, "%T hex = (" + C0 + ")&&(" + CX + ");\n"),
    'not0': (1, "%T dec = 1;\nif(" + C0 + ")\ndec = " + NCX + ";\n"),
    'not1': (1, "%T dec = (" + NC0 + ")||(" + NCX + ");\n"),
    'not2': (1, "%T dec = 1;\nif(" + C0 + ")\nif(" + CX + ")\ndec = 0;\n"),
    'x0': (0, "%T hex = " + C0 + ";\nif(hex)\nhex = " + CX + ";\n"),
    'x1': (0, "%T hex = " + C0 + ";\nif(hex)\nhex = (" + CX + ") ? 1 : 0;\n"),
    'x2': (0, "%T hex = " + C0 + ";\nhex = hex && (" + CX + ");\n"),
    'c0': (0, "char c = 0;\n%T hex;\nif(" + C0 + ")\nc = myatol(dat[1]&0xFF);\nhex = c == 'x';\n"),
    'c1': (0, "char c = dat[0];\n%T hex = 0;\nif(c == '0')\n{\nc = myatol(dat[1]&0xFF);\nhex = c == 'x';\n}\n"),
    'c2': (0, "char c = '\\0';\nif(" + C0 + ")\nc = myatol(dat[1]&0xFF);\nif(c == 'x')\n{\n" + "@HEX@" + "}\nelse\n{\n@DEC@}\nreturn defValue;\n"),
}
TY = ['int', 'char', 'unsigned char', 'uint32_t', '_Bool']
USE = {
    'he': lambda flag, inv: ("if(%s%s)\n{\n@HEX@}\nelse\n{\n@DEC@}\nreturn defValue;\n" % ('!' if inv else '', flag)),
    'de': lambda flag, inv: ("if(%s%s)\n{\n@DEC@}\nelse\n{\n@HEX@}\nreturn defValue;\n" % ('' if inv else '!', flag)),
    'seq': lambda flag, inv: ("if(%s%s)\n{\n@HEX@return defValue;\n}\n@DEC@return defValue;\n" % ('!' if inv else '', flag)),
    'two': lambda flag, inv: ("if(%s%s)\n{\n@HEX@}\nif(%s%s)\n{\n@DEC@}\nreturn defValue;\n" % ('!' if inv else '', flag, '' if inv else '!', flag)),
}


def variants():
    for (s, (inv, st)), ty, (u, use) in itertools.product(SET.items(), TY, USE.items()):
        flag = 'dec' if inv else 'hex'
        if '@HEX@' in st:
            body = st
        else:
            body = st.replace('%T', ty) + use(flag, inv)
        yield '|'.join((s, ty, u)), SIG + "{\n" + body.replace('@HEX@', HEX).replace('@DEC@', DEC) + "}"

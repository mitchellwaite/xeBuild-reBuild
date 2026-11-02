"""`if (flag)` inside the '0' test matched (gen_mu7 ifl, ifb). Find the most natural spelling."""
import itertools

SIG = "uint32_t myatou32(const char* dat, uint32_t defValue)\n"
C0 = "(dat[0]&0xFF) == '0'"
CX = "myatol(dat[1]&0xFF) == 'x'"

SETS = {
    'if2': ("int skip = 0;\nif(" + CX + ")\nskip = 2;\n", 'skip'),
    'q2': ("int skip = (" + CX + ") ? 2 : 0;\n", 'skip'),
    'if1': ("int hex = 0;\nif(" + CX + ")\nhex = 1;\n", 'hex'),
    'q1': ("int hex = (" + CX + ") ? 1 : 0;\n", 'hex'),
    'val': ("int hex = (" + CX + ");\n", 'hex'),
    'b16': ("int base = 0;\nif(" + CX + ")\nbase = 16;\n", 'base'),
    'BOOL': ("BOOL hex = FALSE;\nif(" + CX + ")\nhex = TRUE;\n", 'hex'),
    'BOOLq': ("BOOL hex = (" + CX + ") ? TRUE : FALSE;\n", 'hex'),
    'ifelse': ("int hex;\nif(" + CX + ")\nhex = 1;\nelse\nhex = 0;\n", 'hex'),
}
HEXU = {
    'lit': "if(validateString(&dat[2]))\nreturn myatox32(&dat[2], defValue);\nreturn defValue;\n",
    'var': "if(validateString(&dat[skip]))\nreturn myatox32(&dat[skip], defValue);\nreturn defValue;\n",
    'adv': "dat += skip;\nif(validateString(dat))\nreturn myatox32(dat, defValue);\nreturn defValue;\n",
}
DEC = "if(validateString(dat))\nreturn atoi((const char*)dat);\nreturn defValue;\n"


def variants():
    for (s, (st, fl)), (h, hx) in itertools.product(SETS.items(), HEXU.items()):
        if h != 'lit' and fl != 'skip':
            continue
        yield 'in|%s|%s' % (s, h), SIG + "{\nif(" + C0 + ")\n{\n" + st + "if(" + fl + ")\n{\n" + hx + "}\n}\n" + DEC + "}"
        yield 'decl|%s|%s' % (s, h), SIG + "{\nint " + fl + " = 0;\nif(" + C0 + ")\n{\n" + st.split('\n', 1)[1 if st.startswith('int ' + fl + ' = 0') or st.startswith('BOOL') and 0 else 0].replace('int %s = ' % fl, fl + ' = ').replace('int %s;\n' % fl, '') + "if(" + fl + ")\n{\n" + hx + "}\n}\n" + DEC + "}"

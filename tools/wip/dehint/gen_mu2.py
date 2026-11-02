"""Switch family: single-test switch gets the x test to 50%; sweep for the cmp order (SSA versions)."""
import itertools

SIG = "uint32_t myatou32(const char* dat, uint32_t defValue)\n"

C0 = {'m': "(dat[0]&0xFF) == '0'", 'p': "dat[0] == '0'"}
SW = {
    'm': ("", "myatol(dat[1]&0xFF)"),
    'p': ("", "myatol(dat[1])"),
    'c': ("char c = myatol(dat[1]&0xFF);\n", "c"),
    'i': ("int c = myatol(dat[1]&0xFF);\n", "c"),
    'u': ("unsigned char c = myatol(dat[1]&0xFF);\n", "c"),
    'cm': ("char c = myatol(dat[1]&0xFF);\n", "c&0xFF"),
    'mm': ("", "myatol(dat[1]&0xFF)&0xFF"),
    'uc': ("", "(unsigned char)myatol(dat[1]&0xFF)"),
}
# how the two parse tails read
HEX = {
    'a': ("if(validateString(&dat[2]))\nreturn myatox32(&dat[2], defValue);\nreturn defValue;\n"),
    'b': ("if(!validateString(&dat[2]))\nreturn defValue;\nreturn myatox32(&dat[2], defValue);\n"),
    'c': ("return validateString(&dat[2]) ? myatox32(&dat[2], defValue) : defValue;\n"),
    'd': ("dat += 2;\nif(validateString(dat))\nreturn myatox32(dat, defValue);\nreturn defValue;\n"),
    'e': ("if(validateString(dat+2))\nreturn myatox32(dat+2, defValue);\nreturn defValue;\n"),
}
DEC = {
    'a': ("if(validateString(dat))\nreturn atoi((const char*)dat);\nreturn defValue;\n"),
    'b': ("if(!validateString(dat))\nreturn defValue;\nreturn atoi((const char*)dat);\n"),
    'c': ("return validateString(dat) ? atoi((const char*)dat) : defValue;\n"),
}
# switch layouts
FORM = {
    'if': lambda c0, pre, sw, h, d: "if(%s)\n{\n%sswitch(%s)\n{\ncase 'x':\n%s}\n}\n%s" % (c0, pre, sw, h, d),
    'br': lambda c0, pre, sw, h, d: "if(%s)\n{\n%sswitch(%s)\n{\ncase 'x':\n%sdefault:\nbreak;\n}\n}\n%s" % (c0, pre, sw, h, d),
    'dfl': lambda c0, pre, sw, h, d: "if(%s)\n{\n%sswitch(%s)\n{\ndefault:\nbreak;\ncase 'x':\n%s}\n}\n%s" % (c0, pre, sw, h, d),
    'pre': lambda c0, pre, sw, h, d: "%sif(%s)\n{\nswitch(%s)\n{\ncase 'x':\n%s}\n}\n%s" % (pre, c0, sw, h, d),
}


def variants():
    for (f, form), (a, c0), (b, (pre, sw)), (c, h), (e, d) in itertools.product(FORM.items(), C0.items(), SW.items(), HEX.items(), DEC.items()):
        if f == 'pre' and not pre:
            continue
        yield '|'.join((f, a, b, c, e)), SIG + "{\n" + form(c0, pre, sw, h, d) + "}"

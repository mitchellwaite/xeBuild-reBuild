"""Diagnostic: is default-edge-first really all that's left on the switch shape?
A switch whose DEFAULT arm is the hex arm has its hex edge first, like an if's true edge.
These are odd code (switch on a compare); they test the theory and aren't natural candidates by themselves."""
SIG = "uint32_t myatou32(const char* dat, uint32_t defValue)\n"
C0 = "(dat[0]&0xFF) == '0'"
HEX = "if(validateString(&dat[2]))\nreturn myatox32(&dat[2], defValue);\nreturn defValue;\n"
DEC = "if(validateString(dat))\nreturn atoi((const char*)dat);\nreturn defValue;\n"
EQ = "myatol(dat[1]&0xFF) == 'x'"
NE = "myatol(dat[1]&0xFF) != 'x'"
FORMS = {
    'eq0': "{\nif(" + C0 + ")\n{\nswitch(" + EQ + ")\n{\ncase 0:\nbreak;\ndefault:\n" + HEX + "}\n}\n" + DEC + "}",
    'ne1': "{\nif(" + C0 + ")\n{\nswitch(" + NE + ")\n{\ncase 1:\nbreak;\ndefault:\n" + HEX + "}\n}\n" + DEC + "}",
    'ieq0': "{\nif(" + C0 + ")\n{\nint x = " + EQ + ";\nswitch(x)\n{\ncase 0:\nbreak;\ndefault:\n" + HEX + "}\n}\n" + DEC + "}",
    'sub': "{\nif(" + C0 + ")\n{\nswitch(myatol(dat[1]&0xFF) - 'x')\n{\ncase 0:\n" + HEX + "}\n}\n" + DEC + "}",
}


def variants():
    for k, b in FORMS.items():
        yield k, SIG + b

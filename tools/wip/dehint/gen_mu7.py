"""Looking for a readable member of the switch-with-hex-default family: a number base, a prefix length."""
import itertools

SIG = "uint32_t myatou32(const char* dat, uint32_t defValue)\n"
C0 = "(dat[0]&0xFF) == '0'"
CX = "myatol(dat[1]&0xFF) == 'x'"
HEX = "if(validateString(&dat[2]))\nreturn myatox32(&dat[2], defValue);\nreturn defValue;\n"
DEC = "if(validateString(dat))\nreturn atoi((const char*)dat);\nreturn defValue;\n"

SETS = {
    'phi': "int base = 10;\nif((" + C0 + ")&&(" + CX + "))\nbase = 16;\n",
    'tern': "int base = ((" + C0 + ")&&(" + CX + ")) ? 16 : 10;\n",
    'nest': "int base = 10;\nif(" + C0 + ")\nbase = (" + CX + ") ? 16 : 10;\n",
}
USES = {
    'cD': "switch(base)\n{\ncase 10:\n" + DEC + "default:\n" + HEX + "}\n",
    'cH': "switch(base)\n{\ncase 16:\n" + HEX + "default:\n" + DEC + "}\n",
    'cB': "switch(base)\n{\ncase 16:\n" + HEX + "case 10:\n" + DEC + "}\nreturn defValue;\n",
    'if': "if(base == 16)\n{\n" + HEX + "}\n" + DEC,
}
INNER = {
    # base decided inside the '0' test; only the x test goes through the value
    'i10': "{\nif(" + C0 + ")\n{\nint base = (" + CX + ") ? 16 : 10;\nswitch(base)\n{\ncase 10:\nbreak;\ndefault:\n" + HEX + "}\n}\n" + DEC + "}",
    'i16': "{\nif(" + C0 + ")\n{\nint base = (" + CX + ") ? 16 : 10;\nswitch(base)\n{\ncase 16:\n" + HEX + "}\n}\n" + DEC + "}",
    'ilen': "{\nif(" + C0 + ")\n{\nint skip = (" + CX + ") ? 2 : 0;\nswitch(skip)\n{\ncase 0:\nbreak;\ndefault:\n" + HEX + "}\n}\n" + DEC + "}",
    'ifl': "{\nif(" + C0 + ")\n{\nint skip = (" + CX + ") ? 2 : 0;\nif(skip)\n{\n" + HEX + "}\n}\n" + DEC + "}",
    'ifb': "{\nif(" + C0 + ")\n{\nint skip = 0;\nif(" + CX + ")\nskip = 2;\nif(skip)\n{\n" + HEX + "}\n}\n" + DEC + "}",
}


def variants():
    for (s, st), (u, us) in itertools.product(SETS.items(), USES.items()):
        yield s + '|' + u, SIG + "{\n" + st + us + "}"
    for k, b in INNER.items():
        yield k, SIG + b

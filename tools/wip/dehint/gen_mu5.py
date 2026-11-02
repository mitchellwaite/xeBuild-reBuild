"""Switch shape x spellings of the inlined helpers, looking for a change in ivopts' SSA names (cmp order).
Also single-test `if` x the same helpers, as a control. A hit must be rechecked against myatoh32, myatol,
validateString and the callers in other objects."""
import itertools

SIG = "uint32_t myatou32(const char* dat, uint32_t defValue)\n"
C0 = "(dat[0]&0xFF) == '0'"
HEX = "if(validateString(&dat[2]))\nreturn myatox32(&dat[2], defValue);\nreturn defValue;\n"
DEC = "if(validateString(dat))\nreturn atoi((const char*)dat);\nreturn defValue;\n"
MAIN = {
    'sw': "{\nif(" + C0 + ")\n{\nswitch(myatol(dat[1]&0xFF))\n{\ncase 'x':\n" + HEX + "}\n}\n" + DEC + "}",
    'sw3': "{\nswitch(" + C0 + " ? myatol(dat[1]&0xFF) : 0)\n{\ncase 'x':\n" + HEX + "}\n" + DEC + "}",
    'sw4': "{\nswitch(" + C0 + " ? myatol(dat[1]&0xFF) : 0)\n{\ncase 'x':\n" + HEX + "default:\n" + DEC + "}\n}",
    'if': "{\nif((" + C0 + ")&&(myatol(dat[1]&0xFF) == 'x'))\n{\n" + HEX + "}\n" + DEC + "}",
}
VS_OLD = """	int i, len;
	if(nString == NULL)
		return FALSE;
	len = strlen(nString);
	if((nString[0] != 0x0) && (len != 0))
	{
		for(i = 0; i < len; i++)
		{
			if(myatox(nString[i]) == 0xFF)
				return FALSE;
		}
		return TRUE;
	}
	return FALSE;
"""
VS = {
    'o': None,
    'u': VS_OLD.replace("int i, len;", "unsigned int i, len;"),
    'sz': VS_OLD.replace("int i, len;", "size_t i, len;"),
    'il': VS_OLD.replace("int i, len;", "int i;\n\tint len;"),
    'cast': VS_OLD.replace("len = strlen(nString);", "len = (int)strlen(nString);"),
    'nest': """	int i, len;
	BOOL ret = FALSE;
	if(nString == NULL)
		return FALSE;
	len = strlen(nString);
	if((nString[0] != 0x0) && (len != 0))
	{
		ret = TRUE;
		for(i = 0; i < len; i++)
		{
			if(myatox(nString[i]) == 0xFF)
				return FALSE;
		}
	}
	return ret;
""",
    'wh': VS_OLD.replace("for(i = 0; i < len; i++)\n\t\t{\n\t\t\tif(myatox(nString[i]) == 0xFF)\n\t\t\t\treturn FALSE;\n\t\t}",
                         "i = 0;\n\t\twhile(i < len)\n\t\t{\n\t\t\tif(myatox(nString[i]) == 0xFF)\n\t\t\t\treturn FALSE;\n\t\t\ti++;\n\t\t}"),
}
ML_OLD = """	char ret = c;
	if((c>0x40)&&(c<0x5A)) // A thru Z
		ret = c+0x20;
	return ret;
"""
ML = {
    'o': None,
    'c': "\tif((c>0x40)&&(c<0x5A))\n\t\tc += 0x20;\n\treturn c;\n",
    't': "\treturn ((c>0x40)&&(c<0x5A)) ? c+0x20 : c;\n",
    'r': "\tif((c>0x40)&&(c<0x5A))\n\t\treturn c+0x20;\n\treturn c;\n",
}


def variants():
    for (m, body), (v, vs), (l, ml) in itertools.product(MAIN.items(), VS.items(), ML.items()):
        repl = []
        if vs:
            repl.append((VS_OLD, vs))
        if ml:
            repl.append((ML_OLD, ml))
        yield '|'.join((m, v, l)), SIG + body, repl

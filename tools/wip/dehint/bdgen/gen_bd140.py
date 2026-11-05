"""loadBl from gen_bd139 (pin on d, shared fail with its barrier, nothing else; build/bd/a5/lb3.c): forms of the signature check and flash build test.  Only the type-11 test's position, the copy of the flash test and the CG path's checkBl are still wrong."""
import itertools

BASE = 'build/bd/a5/lb3.c'
OLD = '''if (type == 5 || type == 17 || type == 11) {
if (xb.pub1bl) {
if (!cbVerifySig(e->data, xb.pub1bl)) {
log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);
*pr = -1;
} else if (type)
log_printf(1, "loaded %s, signature check passed!\\n", e->name);
} else
log_printf(1, "loaded %s, could not check signature rsa key not present!\\n", e->name);
}
if (xb.type <= BUILD_DEVGL16)
break;
if (type == 14)
setFlashBuild(getBeU16(xb.files[i].data + 2));
}
break;
'''
NO = 'log_printf(1, "loaded %s, could not check signature rsa key not present!\\n", e->name);\n'
BADS = 'log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);\n*pr = -1;\n'
OK = 'log_printf(1, "loaded %s, signature check passed!\\n", e->name);\n'
V = 'cbVerifySig(e->data, xb.pub1bl)'
SIGS = {
    'cur': 'if (xb.pub1bl) {\nif (!' + V + ') {\n' + BADS + '} else if (type)\n' + OK + '} else\n' + NO,
    'cur0': 'if (xb.pub1bl) {\nif (!' + V + ') {\n' + BADS + '} else\n' + OK + '} else\n' + NO,
    'not': 'if (!xb.pub1bl)\n' + NO + 'else if (!' + V + ') {\n' + BADS + '} else\n' + OK,
    'notel': 'if (!xb.pub1bl)\n' + NO + 'else if (!' + V + ') {\n' + BADS + '} else if (type)\n' + OK,
    'pos': 'if (xb.pub1bl) {\nif (' + V + ')\n' + OK + 'else {\n' + BADS + '}\n} else\n' + NO,
    'not2': 'if (!xb.pub1bl)\n' + NO + 'else if (' + V + ')\n' + OK + 'else {\n' + BADS + '}\n',
}
TY = {
    'or': 'if (type == 5 || type == 17 || type == 11) {\n@@}\n',
    'or2': 'if (type == 5 || type == 11 || type == 17) {\n@@}\n',
    'or3': 'if (type == 11 || type == 5 || type == 17) {\n@@}\n',
    'sw': 'switch (type) {\ncase 5:\ncase 11:\ncase 17:\n@@break;\n}\n',
}
FL = {
    'le': 'if (xb.type <= BUILD_DEVGL16)\nbreak;\nif (type == 14)\nsetFlashBuild(getBeU16(xb.files[i].data + 2));\n',
    'gt': 'if (xb.type > BUILD_DEVGL16 && type == 14)\nsetFlashBuild(getBeU16(xb.files[i].data + 2));\n',
    'lee': 'if (xb.type <= BUILD_DEVGL16)\nbreak;\nif (type == 14)\nsetFlashBuild(getBeU16(e->data + 2));\n',
    'gte': 'if (xb.type > BUILD_DEVGL16 && type == 14)\nsetFlashBuild(getBeU16(e->data + 2));\n',
    'ty': 'if (type == 14 && xb.type > BUILD_DEVGL16)\nsetFlashBuild(getBeU16(xb.files[i].data + 2));\n',
}


def CASES(base):
    out = []
    for s, ty, fl, nest in itertools.product(SIGS, TY, FL, ('in', 'out')):
        body = TY[ty].replace('@@', SIGS[s])
        if nest == 'in':
            new = body + FL[fl] + '}\nbreak;\n'
        else:
            if fl in ('le', 'lee') or ty == 'sw':
                continue
            new = body + '}\n' + FL[fl].replace('if (', 'if (!*pr && ', 1) + 'break;\n'
        out.append(('%s %s %s %s' % (s, ty, fl, nest), base.replace(OLD, new)))
    return out

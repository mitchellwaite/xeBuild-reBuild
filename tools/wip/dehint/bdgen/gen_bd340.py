"""Attempt 23, exp_upd: isUpdateBl bodies with no expect whose first block might get "opcode values nonequal" at
profile_estimate (a GIMPLE_COND against a non-zero constant or a variable) while `type == 23` stays an SSA bool that
addUpdateBls' body can reuse.  Main idea: a result variable holding `type == 23` alone; forwprop turns `if (r)` into
`if (type == 23)` (it always combines comparisons into a cond), so the cond gets nonequal, while the PHI still uses
the SSA bool.  Runs on src as of 604028f1."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun

OLD = '''int isUpdateBl(int type)
{
	return __builtin_expect(type == 23 || type == 15, 0) || type == 16 || type == 9 || type == 10 || type == 24 || type == 25;
}'''
REST = 'type == 15 || type == 16 || type == 9 || type == 10 || type == 24 || type == 25'
F = {
    'none': 'return type == 23 || %s;' % REST,
    'r23': 'int r = type == 23;\n\n\tif (!r)\n\t\tr = %s;\n\treturn r;' % REST,
    'r23if': 'int r = type == 23;\n\n\tif (r)\n\t\treturn r;\n\treturn %s;' % REST,
    'r23ret1': 'int r = type == 23;\n\n\tif (r)\n\t\treturn 1;\n\treturn %s;' % REST,
    'r2315': 'int r = type == 23 || type == 15;\n\n\tif (!r)\n\t\tr = type == 16 || type == 9 || type == 10 || type == 24 || type == 25;\n\treturn r;',
    'r23or': 'int r = type == 23;\n\n\treturn r || %s;' % REST,
    'if23': 'if (type == 23)\n\t\treturn 1;\n\treturn %s;' % REST,
    'tern': 'return type == 23 ? 1 : %s;' % REST,
    'last23': 'if (%s)\n\t\treturn 1;\n\treturn type == 23;' % REST,
    'sw2': 'switch (type) {\n\tcase 23:\n\tcase 15:\n\t\treturn 1;\n\t}\n\treturn type == 16 || type == 9 || type == 10 || type == 24 || type == 25;',
    'ne1': 'return (type == 23 || type == 15) != 0 || type == 16 || type == 9 || type == 10 || type == 24 || type == 25;',
    'cf2v': 'int cf2 = type == 23;\n\n\treturn cf2 || %s;' % REST,
}
FOCUS = ['_addUpdateBls', '_isUpdateBl']


def body(v):
    return 'int isUpdateBl(int type)\n{\n\t%s\n}' % v


def CASES(base):
    return [(k, lambda b, v=v: bdrun.sub(b, OLD, body(v), 1)) for k, v in F.items()]

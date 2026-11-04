"""keysalt.py: try less borderline spellings against drafts/keys_final.c at plain -O3.

Each entry is a list of literal (old, new) edits; every one is checked byte-for-byte."""
import os
import keyslib as K

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drafts', 'keys_final.c')
b = open(D, newline='').read()
BADHDR = "\t\t\toff = size;\n\t\t\tlen = 0;\n"
FREE = "\tif (orig)\n\t\tfree(orig);\n"
ALT2 = "\tif (!alt)\n\t\tkvSet(kv->data);\n\tif (alt)\n\t\tkvEncryptAlt(kv->data, kv->size);\n\telse\n\t\tkvEncrypt(kv->data, kv->size);\n"
V = {
    'base': [],
    'break': [(BADHDR, "\t\t\tbreak;\n")],
    'len_first': [(BADHDR, "\t\t\tlen = 0;\n\t\t\toff = size;\n")],
    'off_over': [(BADHDR, "\t\t\tlen = 0;\n\t\t\toff = size + 1;\n")],
    'next_skip': [(BADHDR, "\t\t\toff = size + 1;\n\t\t\tgoto done;\n"), ("\tif (n != 2)\n", "done:\n\tif (n != 2)\n")],
    'free_plain': [(FREE, "\tfree(orig);\n")],
    'orig_null': [(FREE, "\tif (orig != NULL)\n\t\tfree(orig);\n")],
    'alt8': [(ALT2, "\tif (!alt)\n\t\tkvSet(kv->data);\n\tif (!alt)\n\t\tkvEncrypt(kv->data, kv->size);\n\telse\n\t\tkvEncryptAlt(kv->data, kv->size);\n")],
    'alt_else': [(ALT2, "\tif (alt)\n\t\tkvEncryptAlt(kv->data, kv->size);\n\telse {\n\t\tkvSet(kv->data);\n\t\tkvEncrypt(kv->data, kv->size);\n\t}\n")],
}
for name, edits in V.items():
    s = b
    for old, new in edits:
        assert old in s, old
        s = s.replace(old, new)
    o = K.compile(s, ['-O3'], 'alt')
    print(name, 'MATCH' if K.same(o) else 'differ', K.fndiff(o) if o else 'fail')

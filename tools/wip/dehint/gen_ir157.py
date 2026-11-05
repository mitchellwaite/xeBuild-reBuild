"""getImageSmc from gen_ir155's near miss: the zero and bad arms share `addr = 0x1000` (goto fix), so after threading there is one forwarder per target and tail merge has nothing to merge: B."""
FOCUS = ['_getImageSmc']
BASE = 'tools/wip/dehint/drafts/image_read_attempt9.c'
src = open(BASE, newline='').read().replace('\r\n', '\n')
i = src.index('void getImageSmc(void)')
j = src.index('void getImageKv(void)')
OLD = src[i:j]
LOG0 = 'log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);\n'
k = OLD.index('if (size != 0x3000')
e = OLD.index('return;\nbad:')
MID = OLD[k:e]
HEAD = OLD[:OLD.index('if (!addr)')]
FORMS = {
 'l1': f'if (!addr) {{ {LOG0} fix: addr = 0x1000; }}\n unsigned t = addr;\n if (t != 0x1000) {{ if (t != 0x800) {{ {LOG0} goto fix; }} }}\n{MID}}}\n\n',
 'l2': f'if (!addr) {{ {LOG0} fix: addr = 0x1000; }}\n unsigned t = addr;\n if (t != 0x1000) {{ if (t != 0x800) goto bad; }}\n{MID}return;\nbad:\n{LOG0}goto fix;\n}}\n\n',
 'l3': f'if (!addr) {{ {LOG0} fix: addr = 0x1000; }}\n unsigned t = addr;\n if (t != 0x1000 && t != 0x800) {{ {LOG0} goto fix; }}\n{MID}}}\n\n',
 # X on a copy taken after the join
 'e1': f'if (!addr) {{ {LOG0} goto fix; }}\n{{ unsigned u = addr; if (u != 0x1000) {{ if (u != 0x800) goto bad; }} }}\nbback:\n unsigned t = addr;\n{MID}return;\nbad:\n{LOG0}fix:\n addr = 0x1000;\n goto bback;\n}}\n\n',
 'e2': f'unsigned t;\nif (!addr) {{ {LOG0} goto fix; }}\n t = addr; if (t != 0x1000) {{ if (t != 0x800) goto bad; }}\nbback:\n{MID}return;\nbad:\n{LOG0}fix:\n addr = 0x1000; t = addr;\n goto bback;\n}}\n\n',
 'e3': f'unsigned t;\nif (!addr) {{ {LOG0} goto fix; }}\n t = addr; if (t != 0x1000) {{ if (t != 0x800) {{ {LOG0} fix: addr = 0x1000; t = addr; }} }}\n{MID}}}\n\n',
 'e4': f'unsigned t = addr;\nif (!t) {{ {LOG0} goto fix; }}\n if (t != 0x1000) {{ if (t != 0x800) goto bad; }}\nbback:\n{MID}return;\nbad:\n{LOG0}fix:\n addr = 0x1000; t = addr;\n goto bback;\n}}\n\n',
 'e5': f'unsigned t = addr;\nif (!addr) {{ {LOG0} goto fix; }}\n if (t != 0x1000) {{ if (t != 0x800) goto bad; }}\nbback:\n{MID}return;\nbad:\n{LOG0}fix:\n addr = 0x1000; t = 0x1000;\n goto bback;\n}}\n\n',
 'e6': f'unsigned t = addr;\nif (!addr) {{ {LOG0} t = 0x1000; goto fix; }}\n if (t != 0x1000) {{ if (t != 0x800) goto bad; }}\nbback:\n{MID}return;\nbad:\n{LOG0}fix:\n addr = 0x1000;\n goto bback;\n}}\n\n',
}
AXES = [[(k2, [(OLD, HEAD + v)]) for k2, v in FORMS.items()]]

# attempt 2, on drafts/image_write.c: imgAddFile's c1 cold label replaced by a noreturn call in the dead arm
# (PRED_NORETURN is first-match and very likely, like PRED_COLD_LABEL), and hot label lnp2's forms.
BASE = 'tools/wip/dehint/drafts/image_write.c'
C = '''			c1: __attribute__((cold));
			name++;
'''
LNP = '''		if (!partial)
			npages = 32;
		else {
			/* imgAddFile's clone: keeps DOM2's threading from zeroing the npages guard edge */
			lnp2: __attribute__((hot));
		}
'''
AXES = [
 [('', []),
  ('abort', [(C, '			abort();\n')]),
  ('nabort', [(C, '			name++;\n			abort();\n')]),
  ('abortret', [(C, '			abort();\n			name++;\n')]),
  ('exit', [(C, '			exit(1);\n')]),
  ('nexit', [(C, '			name++;\n			exit(1);\n')]),
 ],
 [('', []),
  ('L1', [(LNP, '		if (!partial)\n			npages = 32;\n')]),
 ],
]

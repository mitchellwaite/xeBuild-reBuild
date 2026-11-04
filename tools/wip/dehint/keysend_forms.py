# keysend.py forms from attempt 2: f1 tails, f2 exit-arm and Z shapes, f3 spellings. Run with KEYSBASE=drafts/keys_final.c.
LW = r'log_printf(0, "\n******* WARNING: dae data appears to be crypted with a different key or damaged! Skipping encryption.\n");'
W = 'while (off < size) {\n'
BAD = '''		} else {
			log_printf(0, "\\n******* ERROR: dae segment does not have the expected header!\\n");
			off = size;
			len = 0;
		}
'''
FORMS = {
 'T1': {'tail': 'free(orig);', 'edits': [(W, 'for (;;) {\nif (off >= size) {\nif (n != 2)\n' + LW + '\nbreak;\n}\n')]},
 'T2': {'tail': 'free(orig);', 'edits': [(W, 'while (1) {\nif (off >= size) {\nif (n != 2)\n' + LW + '\nbreak;\n}\n')]},
 'T3': {'tail': '', 'edits': [(W, 'for (;;) {\nif (off >= size) {\nif (n != 2)\n' + LW + '\nfree(orig);\nreturn;\n}\n')]},
 'T4': {'tail': 'out:\nfree(orig);', 'edits': [(W, 'for (;;) {\nif (off >= size) {\nif (n != 2)\n' + LW + '\ngoto out;\n}\n')]},
 'T5': {'tail': 'free(orig);', 'edits': [(W, 'for (;;) {\nif (off >= size) {\nif (n == 2) break;\n' + LW + '\nbreak;\n}\n')]},
 'Z1': {'tail': 'if (n != 2)\nLW\ngoto out;\nbad:\nlog_printf(0, "\\n******* ERROR: dae segment does not have the expected header!\\n");\noff = size;\nlen = 0;\ngoto next;\nout:\nfree(orig);',
        'edits': [(BAD, '} else goto bad;\n')]},
}
F1 = {
 'E0': {'tail': 'if (n != 2) LW\nfree(orig);'},
 'E1': {'tail': 'if (n == 2) { free(orig); return; }\nLW\nfree(orig);'},
 'E2': {'tail': 'if (n == 2) free(orig);\nelse { LW free(orig); }'},
 'E3': {'tail': 'if (n != 2) { LW free(orig); return; }\nfree(orig);'},
 'E4': {'tail': 'if (n != 2) { LW free(orig); } else free(orig);'},
 'E5': {'tail': 'if (n == 2) { } else LW\nfree(orig);'},
 'E6': {'tail': 'if (n == 2) goto out;\nLW\nout:\nfree(orig);'},
 'E7': {'tail': 'if (n != 2) { LW goto out; }\nout:\nfree(orig);'},
 'E8': {'tail': 'switch (n) { case 2: break; default: LW }\nfree(orig);'},
 'E9': {'tail': 'if (n != 2) goto warn;\nout:\nfree(orig);\nreturn;\nwarn:\nLW\ngoto out;'},
 'Ea': {'tail': 'if (n == 2) {\nout:\nfree(orig);\nreturn;\n}\nLW\ngoto out;'},
 'Eb': {'tail': 'if (n != 2) goto warn;\nfree(orig);\nreturn;\nwarn:\nLW\nfree(orig);'},
 'Ec': {'tail': 'if (n == 2) { free(orig); return; }\nLW\nfree(orig);\nreturn;'},
 'Ed': {'tail': 'if (n != 2) { LW }\nfree(orig);\nreturn;'},
 'Ee': {'tail': 'do { if (n == 2) break; LW } while (0);\nfree(orig);'},
 'Ef': {'tail': 'free(orig);\nif (n != 2) LW'},
 'Eg': {'tail': 'orig = (free(orig), NULL);\nif (n != 2) LW'},
}
HEAD = 'if (off >= size) {\nif (n != 2)\n' + LW + '\nbreak;\n}\n'
T1 = (W, 'for (;;) {\n' + HEAD)
BADOLD = 'off = size;\n\t\t\tlen = 0;\n'
NEXT = '\tnext:\n\t\toff += len;\n'
F3 = {
 'T1': {'tail': 'free(orig);', 'edits': [T1]},
 # for (;; off += len), continue for goto next
 'V1': {'tail': 'free(orig);', 'edits': [(W, 'for (;; off += len) {\n' + HEAD), (NEXT, ''), ('goto next;', 'continue;')]},
 # bad header continues past the add
 'V3': {'tail': 'free(orig);', 'edits': [T1, (BADOLD, 'off = size;\ncontinue;\n')]},
 'V4': {'tail': 'free(orig);', 'edits': [(W, 'for (;; off += len) {\n' + HEAD), (NEXT, ''), ('goto next;', 'continue;'), (BADOLD, 'off = size;\nlen = 0;\ncontinue;\n')]},
 # bad header sets len only
 'V5': {'tail': 'free(orig);', 'edits': [T1, (BADOLD, 'len = 0;\noff = size;\n')]},
 # break out directly from the header arm, warning first
 'V6': {'tail': 'free(orig);', 'edits': [(W, 'for (;;) {\nif (off >= size) {\nif (n != 2) {\n' + LW + '\n}\nbreak;\n}\n')]},
 # off < size spelled the other way
 'V7': {'tail': 'free(orig);', 'edits': [(W, 'for (;;) {\nif (size <= off) {\nif (n != 2)\n' + LW + '\nbreak;\n}\n')]},
 # do-forever
 'V8': {'tail': 'free(orig);', 'edits': [(W, 'do {\n' + HEAD), (NEXT, NEXT + '\t} while (1);\n//')]},
}
FORMS.update(F1)
FORMS.update({"f3" + k: v for k, v in F3.items()})

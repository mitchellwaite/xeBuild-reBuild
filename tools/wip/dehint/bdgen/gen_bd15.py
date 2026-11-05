"""loadConsoleBlFiles: the cold label on the no-files return"""
FOCUS = ['_loadConsoleBlFiles']
H = '''	if ((uint32_t)xb.nFiles <= 1)
		goto none;
	for (i = 1; i < (uint32_t)xb.nFiles; i++) {
'''
T = '''			return -1;
		}
	}
	return 0;
none: __attribute__((cold));
	return 0;
}
'''
TP = '''			return -1;
		}
	}
	return 0;
}
'''
A = [
    ('plain', [(H, '	for (i = 1; i < (uint32_t)xb.nFiles; i++) {\n'), (T, TP)]),
    ('ret', [(H, '	if ((uint32_t)xb.nFiles <= 1)\n		return 0;\n	for (i = 1; i < (uint32_t)xb.nFiles; i++) {\n'), (T, TP)]),
    ('lab', [(T, T.replace('none: __attribute__((cold));', 'none:'))]),
    ('do', [(H, '	if ((uint32_t)xb.nFiles <= 1)\n		return 0;\n	i = 1;\n	do {\n'), (T, '''			return -1;
		}
		i++;
	} while (i < (uint32_t)xb.nFiles);
	return 0;
}
''')]),
    ('do2', [(H, '	i = 1;\n	if ((uint32_t)xb.nFiles > 1) do {\n'), (T, '''			return -1;
		}
		i++;
	} while (i < (uint32_t)xb.nFiles);
	return 0;
}
''')]),
    ('ifn', [(H, '	if ((uint32_t)xb.nFiles > 1)\n	for (i = 1; i < (uint32_t)xb.nFiles; i++) {\n'), (T, TP)]),
    ('int', [(H, '	for (i = 1; (int)i < xb.nFiles; i++) {\n'), (T, TP)]),
    ('while', [(H, '	i = 1;\n	while (i < (uint32_t)xb.nFiles) {\n'), (T, '''			return -1;
		}
		i++;
	}
	return 0;
}
''')]),
    ('retr', [(H, '	r = 0;\n	for (i = 1; i < (uint32_t)xb.nFiles; i++) {\n'), (T, '''			return -1;
		}
	}
	return r;
}
''')]),
]
AXES = [A]

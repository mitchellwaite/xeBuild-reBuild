"""loadBl: t5le's hot label and exp_pr.  A helper with a call on the > 5 side: not early-inlined if big enough, so PRED_CALL lowers
that edge at profile_estimate; ipa-inline brings it back (called once)."""
TAIL = '''		if (xb.type <= BUILD_DEVGL16) {
		t5le: __attribute__((hot));
			if (__builtin_expect(*pr != 0, 0))
				goto fail;
			break;
		}
		if (type == 14)
			setFlashBuild(getBeU16(xb.files[i].data + 2));
		break;
'''
HEAD = '/* load the input file e (xb.files[i]) by its type */\nstatic void loadBl('
H1 = 'static void seFlashBuild(int type, uint32_t i)\n{\n	if (type == 14)\n		setFlashBuild(getBeU16(xb.files[i].data + 2));\n}\n\n'
H2 = 'static void seFlashBuild(uint32_t i)\n{\n	setFlashBuild(getBeU16(xb.files[i].data + 2));\n}\n\n'
ARM = {'k': ('t5le: __attribute__((hot));\n', '__builtin_expect(*pr != 0, 0)'),
       'nl': ('', '__builtin_expect(*pr != 0, 0)'),
       'ne': ('', '*pr != 0'),
       'ke': ('t5le: __attribute__((hot));\n', '*pr != 0')}
A = []
for k, (lab, t) in ARM.items():
    l = ('\t\t' + lab) if lab else ''
    A.append((k + '-orig', [(TAIL, '		if (xb.type <= BUILD_DEVGL16) {\n' + l + '			if (' + t + ')\n				goto fail;\n			break;\n		}\n		if (type == 14)\n			setFlashBuild(getBeU16(xb.files[i].data + 2));\n		break;\n')]))
    A.append((k + '-h1', [(HEAD, H1 + HEAD), (TAIL, '		if (xb.type <= BUILD_DEVGL16) {\n' + l + '			if (' + t + ')\n				goto fail;\n			break;\n		}\n		seFlashBuild(type, i);\n		break;\n')]))
    A.append((k + '-h2', [(HEAD, H2 + HEAD), (TAIL, '		if (xb.type <= BUILD_DEVGL16) {\n' + l + '			if (' + t + ')\n				goto fail;\n			break;\n		}\n		if (type == 14)\n			seFlashBuild(i);\n		break;\n')]))
    A.append((k + '-rv', [(HEAD, H1 + HEAD), (TAIL, '		if (xb.type > BUILD_DEVGL16) {\n			seFlashBuild(type, i);\n			break;\n		}\n' + l + '		if (' + t + ')\n			goto fail;\n		break;\n')]))
AXES = [A]
FOCUS = ['_loadBlFiles']

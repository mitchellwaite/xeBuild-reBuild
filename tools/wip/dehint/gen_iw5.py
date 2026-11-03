# imgAddMobile without its 50/50 expect
BASE = 'tools/wip/dehint/drafts/image_write.c'
FOCUS = ['_imgAddMobile']
FLAGS = ['--param', 'builtin-expect-probability=50']
OLD = '''	mobileOffset = off = imgSizeAligned();
	if (__builtin_expect(imgFits(off, len), 1)) {
		log_printf(1, "\\tadding Mobile%c.dat as type 0x%x at raw offset 0x%x len 0x%x (end 0x%x)\\n",
			type + 17, type, off, len, off + len);
		ret = mobileOffset >> 14;
		imgAdd(mobileOffset, data, len, type, 0x1ffe, 0);
		return ret;
	}
	log_printf(0, "\\n******* ERROR: adding Mobile%c.dat will exceed available flash space! Skipped!\\n\\n",
		type + 17);
	return 0;
}
'''
GOOD = '''		log_printf(1, "\\tadding Mobile%c.dat as type 0x%x at raw offset 0x%x len 0x%x (end 0x%x)\\n",
			type + 17, type, off, len, off + len);
		ret = mobileOffset >> 14;
		imgAdd(mobileOffset, data, len, type, 0x1ffe, 0);
'''
ERR = '''		log_printf(0, "\\n******* ERROR: adding Mobile%c.dat will exceed available flash space! Skipped!\\n\\n",
			type + 17);
'''
HEAD = '	mobileOffset = off = imgSizeAligned();\n'
forms = {
    'if-ret-fall': HEAD + '	if (imgFits(off, len)) {\n' + GOOD + '		return ret;\n	}\n' + ERR + '	return 0;\n}\n',
    'not-ret': HEAD + '	if (!imgFits(off, len)) {\n' + ERR + '		return 0;\n	}\n' + GOOD + '	return ret;\n}\n',
    'ifelse-ret0': HEAD + '	ret = 0;\n	if (imgFits(off, len)) {\n' + GOOD + '	} else {\n' + ERR + '	}\n	return ret;\n}\n',
    'ifelse-rev': HEAD + '	ret = 0;\n	if (!imgFits(off, len)) {\n' + ERR + '	} else {\n' + GOOD + '	}\n	return ret;\n}\n',
    'ifelse-both': HEAD + '	if (imgFits(off, len)) {\n' + GOOD + '	} else {\n' + ERR + '		ret = 0;\n	}\n	return ret;\n}\n',
    'ifelse-both2': HEAD + '	if (!imgFits(off, len)) {\n' + ERR + '		ret = 0;\n	} else {\n' + GOOD + '	}\n	return ret;\n}\n',
    'flag': HEAD + '	int fits = imgFits(off, len);\n	if (fits) {\n' + GOOD + '		return ret;\n	}\n' + ERR + '	return 0;\n}\n',
    'flag2': HEAD + '	int fits = imgFits(off, len);\n	if (!fits) {\n' + ERR + '		return 0;\n	}\n' + GOOD + '	return ret;\n}\n',
    'gt': HEAD + '	if (imgFits(off, len) > 0) {\n' + GOOD + '		return ret;\n	}\n' + ERR + '	return 0;\n}\n',
    'bang': HEAD + '	int nofit = !imgFits(off, len);\n	if (nofit > 0) {\n' + ERR + '		return 0;\n	}\n' + GOOD + '	return ret;\n}\n',
    'bang2': HEAD + '	int nofit = !imgFits(off, len);\n	if (nofit == 0) {\n' + GOOD + '		return ret;\n	}\n' + ERR + '	return 0;\n}\n',
    'lim': HEAD + '	if ((xb.fsEnd - 1) * 0x4000 >= off + len) {\n' + GOOD + '		return ret;\n	}\n' + ERR + '	return 0;\n}\n',
    'lim2': HEAD + '	if ((xb.fsEnd - 1) * 0x4000 < off + len) {\n' + ERR + '		return 0;\n	}\n' + GOOD + '	return ret;\n}\n',
    'goto': HEAD + '	if (!imgFits(off, len))\n		goto toobig;\n' + GOOD + '	return ret;\ntoobig:\n' + ERR + '	return 0;\n}\n',
}
AXES = [[(k, [(OLD, v)]) for k, v in forms.items()]]

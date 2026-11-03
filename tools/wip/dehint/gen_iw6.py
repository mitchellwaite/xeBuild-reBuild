# imgAddMobile: split so the fits test has no early-return predictor (50/50 without expect)
BASE = 'tools/wip/dehint/drafts/image_write.c'
FOCUS = ['_imgAddMobile']
s = open(__file__.replace('gen_iw6.py', 'drafts/image_write.c'), newline='').read().replace('\r\n', '\n')
a = s.index('uint32_t imgAddMobile(const void *data, uint32_t len, uint8_t type)')
b = s.index('void fixupFsTable(uint32_t off)')
OLD = s[a:b]
GOOD = '''		log_printf(1, "\\tadding Mobile%c.dat as type 0x%x at raw offset 0x%x len 0x%x (end 0x%x)\\n",
			type + 17, type, off, len, off + len);
		ret = mobileOffset >> 14;
		imgAdd(mobileOffset, data, len, type, 0x1ffe, 0);
'''
ERR = '''	log_printf(0, "\\n******* ERROR: adding Mobile%c.dat will exceed available flash space! Skipped!\\n\\n",
		type + 17);
'''
i = OLD.index('	if (xb.bigBlock) {\n')
j = OLD.index('	mobileOffset = off = imgSizeAligned();\n')
bigbody = OLD[i:j]
big_inner = bigbody.split('\n', 1)[1].rsplit('	}\n', 1)[0]
smallhead = '	mobileOffset = off = imgSizeAligned();\n'
small1 = smallhead + '	if (imgFits(off, len)) {\n' + GOOD + '		return ret;\n	}\n' + ERR + '	return 0;\n'
small2 = smallhead + '	if (!imgFits(off, len)) {\n' + ERR + '		return 0;\n	}\n' + GOOD + '	return ret;\n'
small3 = smallhead + '	ret = 0;\n	if (imgFits(off, len)) {\n' + GOOD + '	} else {\n' + ERR + '	}\n	return ret;\n'
SIG = '(const void *data, uint32_t len, uint8_t type)\n{\n	uint32_t off%s, ret;\n\n'
SM = {'s1': small1, 's2': small2, 's3': small3}
forms = {}
for k, sm in SM.items():
    hs = 'static uint32_t imgAddMobileSmall' + SIG % '' + sm + '}\n\n'
    hb = 'static uint32_t imgAddMobileBig' + SIG % ', end' + big_inner + '}\n\n'
    forms['helper-small-' + k] = hs + OLD[:OLD.index('	mobileOffset = off = imgSizeAligned();')].replace('uint32_t off, end, ret;', 'uint32_t off, end, ret;') + '	return imgAddMobileSmall(data, len, type);\n}\n\n'
    forms['helper-both-' + k] = hs + hb + 'uint32_t imgAddMobile(const void *data, uint32_t len, uint8_t type)\n{\n	if (xb.bigBlock)\n		return imgAddMobileBig(data, len, type);\n	return imgAddMobileSmall(data, len, type);\n}\n\n'
    forms['helper-both2-' + k] = hs + hb + 'uint32_t imgAddMobile(const void *data, uint32_t len, uint8_t type)\n{\n	if (!xb.bigBlock)\n		return imgAddMobileSmall(data, len, type);\n	return imgAddMobileBig(data, len, type);\n}\n\n'
    forms['helper-both3-' + k] = hs + hb + 'uint32_t imgAddMobile(const void *data, uint32_t len, uint8_t type)\n{\n	return xb.bigBlock ? imgAddMobileBig(data, len, type) : imgAddMobileSmall(data, len, type);\n}\n\n'
    # the small path first in the source
    forms['first-' + k] = 'uint32_t imgAddMobile(const void *data, uint32_t len, uint8_t type)\n{\n	uint32_t off, end, ret;\n\n	if (!xb.bigBlock) {\n' + sm + '	}\n' + big_inner + '}\n\n'
AXES = [[(k, [(OLD, v)]) for k, v in forms.items()]]

# imgAddMobile: as gen_iw7, with the else-if block right before the big tail (split_edge places
# the store block after its source only if the tail's prev block falls into it)
BASE = 'tools/wip/dehint/drafts/image_write.c'
FOCUS = ['_imgAddMobile']
s = open(__file__.replace('gen_iw8.py', 'drafts/image_write.c'), newline='').read().replace('\r\n', '\n')
a = s.index('uint32_t imgAddMobile(const void *data, uint32_t len, uint8_t type)')
b = s.index('void fixupFsTable(uint32_t off)')
OLD = s[a:b]
INIT = '''			mobileOffset = imgSizeAligned();
			if (mobileOffset & 0x1ffff)
				mobileOffset = (mobileOffset + 0x20000) & ~0x1ffff;
'''
GOOD = '''		log_printf(1, "\\tadding Mobile%c.dat as type 0x%x at raw offset 0x%x len 0x%x (end 0x%x)\\n",
			type + 17, type, off, len, off + len);
		ret = mobileOffset >> 14;
		imgAdd(mobileOffset, data, len, type, 0x1ffe, 0);
		return ret;
'''
ERR = '''		log_printf(0, "\\n******* ERROR: adding Mobile%c.dat will exceed available flash space! Skipped!\\n\\n",
			type + 17);
		return 0;
'''
SMALL = {
    'not': '		mobileOffset = off = imgSizeAligned();\n		if (!imgFits(off, len)) {\n' + ERR + '		}\n' + GOOD,
    'fits': '		mobileOffset = off = imgSizeAligned();\n		if (imgFits(off, len)) {\n' + GOOD + '		}\n' + ERR,
    'gofits': '		mobileOffset = off = imgSizeAligned();\n		if (imgFits(off, len))\n			goto fits;\n' + ERR + 'fits:\n' + GOOD,
}
TAIL = '''	off = mobileOffset;
	if (!imgFits(off, len)) {
		log_printf(0, "\\n******* ERROR: adding Mobile%c.dat will exceed available flash space! Skipped!\\n\\n",
			type + 17);
		return 0;
	}
	log_printf(1, "\\tadding Mobile%c.dat as type 0x%x at raw offset 0x%x len 0x%x (end 0x%x)\\n",
		type + 17, type, off, len, off + len);
	imgAdd(mobileOffset, data, len, type, 0x1ffe, 0);
	ret = mobileOffset >> 17;
	mobileOffset += len;
	if (mobileOffset & 0x7ff)
		mobileOffset = (mobileOffset + 0x800) & ~0x7ff;
	return ret;
}

'''
H = '''uint32_t imgAddMobile(const void *data, uint32_t len, uint8_t type)
{
	uint32_t off, end, ret;

'''
ELSEIF = '''(mobileOffset & ~0x1ffff) + 0x20000 < mobileOffset + len)
		mobileOffset = (mobileOffset + 0x20000) & ~0x1ffff;
'''
forms = {}
for k, sm in SMALL.items():
    forms['v1-' + k] = H + '	if (xb.bigBlock && !mobileOffset) {\n' + INIT + '	} else if (!xb.bigBlock) {\n' + sm + '	} else if (' + ELSEIF + TAIL
    forms['v2-' + k] = H + '	if (xb.bigBlock) {\n		if (!mobileOffset) {\n' + INIT + '			goto place;\n		}\n	} else {\n' + sm + '	}\n	if (' + ELSEIF + 'place:\n' + TAIL
    forms['v3-' + k] = H + '	if (!xb.bigBlock) {\n' + sm + '	}\n	if (!mobileOffset) {\n' + INIT + '	} else if (' + ELSEIF + TAIL
AXES = [[(k, [(OLD, v)]) for k, v in forms.items()]]

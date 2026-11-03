# imgAddMobile: small path inside the else, the big path's tail after the if/else, so neither
# small arm is the block before the return block: both fire the early-return predictor -> 50/50
BASE = 'tools/wip/dehint/drafts/image_write.c'
FOCUS = ['_imgAddMobile']
s = open(__file__.replace('gen_iw7.py', 'drafts/image_write.c'), newline='').read().replace('\r\n', '\n')
a = s.index('uint32_t imgAddMobile(const void *data, uint32_t len, uint8_t type)')
b = s.index('void fixupFsTable(uint32_t off)')
OLD = s[a:b]
HEAD = '''uint32_t imgAddMobile(const void *data, uint32_t len, uint8_t type)
{
	uint32_t off, end, ret;

	if (xb.bigBlock) {
		if (!mobileOffset) {
			mobileOffset = imgSizeAligned();
			if (mobileOffset & 0x1ffff)
				mobileOffset = (mobileOffset + 0x20000) & ~0x1ffff;
		} else if ((mobileOffset & ~0x1ffff) + 0x20000 < mobileOffset + len)
			mobileOffset = (mobileOffset + 0x20000) & ~0x1ffff;
	} else {
		mobileOffset = off = imgSizeAligned();
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
TAIL = '''	}
	off = mobileOffset;
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
forms = {
    'not': HEAD + '		if (!imgFits(off, len)) {\n' + ERR + '		}\n' + GOOD + TAIL,
    'fits': HEAD + '		if (imgFits(off, len)) {\n' + GOOD + '		}\n' + ERR + TAIL,
    'else': HEAD + '		if (!imgFits(off, len)) {\n' + ERR + '		} else {\n' + GOOD + '		}\n' + TAIL,
}
AXES = [[(k, [(OLD, v)]) for k, v in forms.items()]]

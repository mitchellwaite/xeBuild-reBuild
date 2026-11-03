# imgAddMobile without its expect: variations on gen_iw8's v2 control flow, to fix esi/edi in the big path
BASE = 'tools/wip/dehint/drafts/image_write.c'
FOCUS = ['_imgAddMobile']
s = open(__file__.replace('gen_iw14.py', 'drafts/image_write.c'), newline='').read().replace('\r\n', '\n')
a = s.index('uint32_t imgAddMobile(const void *data, uint32_t len, uint8_t type)')
b = s.index('void fixupFsTable(uint32_t off)')
OLD = s[a:b]
INIT = '''			mobileOffset = imgSizeAligned();
			if (mobileOffset & 0x1ffff)
				mobileOffset = (mobileOffset + 0x20000) & ~0x1ffff;
'''
GOOD = lambda o, r: f'''		log_printf(1, "\\tadding Mobile%c.dat as type 0x%x at raw offset 0x%x len 0x%x (end 0x%x)\\n",
			type + 17, type, {o}, len, {o} + len);
		{r} = mobileOffset >> 14;
		imgAdd(mobileOffset, data, len, type, 0x1ffe, 0);
		return {r};
'''
ERR = '''		log_printf(0, "\\n******* ERROR: adding Mobile%c.dat will exceed available flash space! Skipped!\\n\\n",
			type + 17);
		return 0;
'''
TAILS = {
    't0': '''	off = mobileOffset;
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

''',
}
TAILS['t1'] = TAILS['t0'].replace('	off = mobileOffset;\n	if (!imgFits(off, len)) {', '	end = mobileOffset;\n	if (!imgFits(end, len)) {').replace('type, off, len, off + len);', 'type, end, len, end + len);')
TAILS['t2'] = TAILS['t0'].replace('	if (!imgFits(off, len)) {', '	if ((xb.fsEnd - 1) * 0x4000 < off + len) {')
TAILS['t3'] = TAILS['t0'].replace('	imgAdd(mobileOffset, data, len, type, 0x1ffe, 0);\n	ret = mobileOffset >> 17;', '	imgAdd(mobileOffset, data, len, type, 0x1ffe, 0);\n	off = mobileOffset;\n	ret = off >> 17;')
TAILS['t4'] = TAILS['t0'].replace('	ret = mobileOffset >> 17;\n	mobileOffset += len;', '	ret = mobileOffset >> 17;\n	mobileOffset = mobileOffset + len;')
SMALL = {
    's0': ('off', 'ret', ''),
    's1': ('o2', 'ret', 'uint32_t o2;\n		'),
    's2': ('off', 'r2', 'uint32_t r2;\n		'),
    's3': ('o2', 'r2', 'uint32_t o2, r2;\n		'),
}
H = '''uint32_t imgAddMobile(const void *data, uint32_t len, uint8_t type)
{
	uint32_t off, end, ret;

'''
ELSEIF = '''(mobileOffset & ~0x1ffff) + 0x20000 < mobileOffset + len)
		mobileOffset = (mobileOffset + 0x20000) & ~0x1ffff;
'''
forms = {}
for sk, (o, r, d) in SMALL.items():
    sm = '		' + d + f'mobileOffset = {o} = imgSizeAligned();\n		if (imgFits({o}, len))\n			goto fits;\n' + ERR + 'fits:\n' + GOOD(o, r)
    for tk, t in TAILS.items():
        forms[sk + tk] = H + '	if (xb.bigBlock) {\n		if (!mobileOffset) {\n' + INIT + '			goto place;\n		}\n	} else {\n' + sm + '	}\n	if (' + ELSEIF + 'place:\n' + t
AXES = [[(k, [(OLD, v)]) for k, v in forms.items()]]

# attempt 3: imgAddMobile without its expect, one error block in the source (the reference has only one).
FOCUS = ['_imgAddMobile']
import os
s = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'src', 'image_write.c'), newline='').read().replace('\r\n', '\n')
a = s.index('uint32_t imgAddMobile(const void *data, uint32_t len, uint8_t type)')
b = s.index('void fixupFsTable(uint32_t off)')
OLD = s[a:b]
H = '''uint32_t imgAddMobile(const void *data, uint32_t len, uint8_t type)
{
	uint32_t off, end, ret;

'''
INIT = '''		if (!mobileOffset) {
			mobileOffset = imgSizeAligned();
			if (mobileOffset & 0x1ffff)
				mobileOffset = (mobileOffset + 0x20000) & ~0x1ffff;
		} else if ((mobileOffset & ~0x1ffff) + 0x20000 < mobileOffset + len)
			mobileOffset = (mobileOffset + 0x20000) & ~0x1ffff;
		off = mobileOffset;
'''
ADD = '''log_printf(1, "\\tadding Mobile%c.dat as type 0x%x at raw offset 0x%x len 0x%x (end 0x%x)\\n",
			type + 17, type, off, len, off + len);
'''
BIGT = '''imgAdd(mobileOffset, data, len, type, 0x1ffe, 0);
			ret = mobileOffset >> 17;
			mobileOffset += len;
			if (mobileOffset & 0x7ff)
				mobileOffset = (mobileOffset + 0x800) & ~0x7ff;
			return ret;
'''
SMT = '''ret = mobileOffset >> 14;
			imgAdd(mobileOffset, data, len, type, 0x1ffe, 0);
			return ret;
'''
ERR = '''log_printf(0, "\\n******* ERROR: adding Mobile%c.dat will exceed available flash space! Skipped!\\n\\n",
		type + 17);
	return 0;
}

'''
SM0 = '		mobileOffset = off = imgSizeAligned();\n'
forms = {}
# both arms try, the error falls out at the end
forms['end'] = H + '	if (xb.bigBlock) {\n' + INIT + '		if (imgFits(off, len)) {\n			' + ADD + '			' + BIGT + '		}\n	} else {\n' + SM0 + '		if (imgFits(off, len)) {\n			' + ADD + '			' + SMT + '		}\n	}\n	' + ERR
# error inside the big arm, small arm jumps to it
forms['errbig'] = H + '	if (xb.bigBlock) {\n' + INIT + '		if (!imgFits(off, len)) {\nerr:\n			' + ERR.replace('	return 0;\n}\n\n', '			return 0;\n		}\n') + '		' + ADD + '		' + BIGT + '	}\n' + SM0 + '	if (!imgFits(off, len))\n		goto err;\n	' + ADD + '	' + SMT + '}\n\n'
# small arm first in the source, the error between
forms['errsm'] = H + '	if (!xb.bigBlock) {\n' + SM0 + '		if (imgFits(off, len)) {\n			' + ADD + '			' + SMT + '		}\n	} else {\n' + INIT + '		if (imgFits(off, len)) {\n			' + ADD + '			' + BIGT + '		}\n	}\n	' + ERR
# common fits test, tail per block size
forms['one'] = H + '	if (xb.bigBlock) {\n' + INIT + '	} else\n' + SM0 + '	off = mobileOffset;\n	if (!imgFits(off, len)) {\n		' + ERR.replace('	return 0;\n}\n\n', '		return 0;\n	}\n') + '	' + ADD + '	if (xb.bigBlock) {\n			' + BIGT + '	}\n	' + SMT + '}\n\n'
forms['one2'] = H + '	if (xb.bigBlock) {\n' + INIT + '	} else\n' + SM0 + '	if (!imgFits(mobileOffset, len)) {\n		' + ERR.replace('	return 0;\n}\n\n', '		return 0;\n	}\n') + '	off = mobileOffset;\n	' + ADD + '	if (xb.bigBlock) {\n			' + BIGT + '	}\n	' + SMT + '}\n\n'
AXES = [[(k, [(OLD, v)]) for k, v in forms.items()], [('p', []), ('np', [('XXXX', 'XXXX')])][:1]]

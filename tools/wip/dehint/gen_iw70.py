# attempt 5: imgAddMobile forms on the if-form imgFits (no expect, no param): only .rdata order was left
import os
BASE = os.environ.get('IWB', 'build/iw/a5/if1.c')
ERRB = '''			log_printf(0, "\\n******* ERROR: adding Mobile%c.dat will exceed available flash space! Skipped!\\n\\n",
				type + 17);
			return 0;
'''
ERRS = '''		log_printf(0, "\\n******* ERROR: adding Mobile%c.dat will exceed available flash space! Skipped!\\n\\n",
			type + 17);
		return 0;
'''
ADDB = '''		log_printf(1, "\\tadding Mobile%c.dat as type 0x%x at raw offset 0x%x len 0x%x (end 0x%x)\\n",
			type + 17, type, off, len, off + len);
		imgAdd(mobileOffset, data, len, type, 0x1ffe, 0);
		ret = mobileOffset >> 17;
		mobileOffset += len;
		if (mobileOffset & 0x7ff)
			mobileOffset = (mobileOffset + 0x800) & ~0x7ff;
		return ret;
'''
ADDS = '''		log_printf(1, "\\tadding Mobile%c.dat as type 0x%x at raw offset 0x%x len 0x%x (end 0x%x)\\n",
			type + 17, type, off, len, off + len);
		ret = mobileOffset >> 14;
		imgAdd(mobileOffset, data, len, type, 0x1ffe, 0);
		return ret;
'''
ind = lambda s: ''.join('\t' + l + '\n' for l in s.split('\n') if l)
ded = lambda s: ''.join(l[1:] + '\n' for l in s.split('\n') if l)
BIGA = '		if (!imgFits(off, len)) {\n' + ERRB + '		}\n' + ADDB
SMALLA = '	if (imgFits(off, len)) {\n' + ADDS + '	}\n' + ded(ERRS)
BIG = {
 'B0': BIGA,
 'Bif': '		if (imgFits(off, len)) {\n' + ind(ADDB) + '		}\n' + ded(ERRB),
 'Belse': '		if (!imgFits(off, len)) {\n' + ERRB + '		} else {\n' + ind(ADDB) + '		}\n',
 'Bifelse': '		if (imgFits(off, len)) {\n' + ind(ADDB) + '		} else {\n' + ERRB + '		}\n',
}
SMALL = {
 'S0': SMALLA,
 'Snot': '	if (!imgFits(off, len)) {\n' + ERRS + '	}\n' + ded(ADDS),
 'Selse': '	if (!imgFits(off, len)) {\n' + ERRS + '	} else {\n' + ADDS + '	}\n',
 'Sifelse': '	if (imgFits(off, len)) {\n' + ADDS + '	} else {\n' + ERRS + '	}\n',
}
AXES = [[(k, [(BIGA, v)]) for k, v in BIG.items()], [(k, [(SMALLA, v)]) for k, v in SMALL.items()]]
FLAGS = []
FOCUS = ['_imgAddMobile']

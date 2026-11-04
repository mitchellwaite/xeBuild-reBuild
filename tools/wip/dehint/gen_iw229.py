# attempt 16: block offset local on the `small` family: place x how s[9] uses it x tail spelling x pages (both arms the a15 form or one ternary). Score with iw16sweep (full signature `<>>><<<<`).
# Facts behind it: place decides imgAdd's lim order (bo above the arms: 6 lines); imgAddFile's 4 lines are one version (`_45 > _53`, 91 v 188), one name more on its stack.
import os
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_a15.c')
USE0 = '						s[9] = (((off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256) - left) >> 2;\n'
FOR = '		for (end = p + npages; p < end; p++) {\n'
IB = '			if (xb.bigBlock) {\n				((struct spb *)s)->b2lo'
TT = '				if (type > 1) {\n					((struct spt *)s)->type = type;\n					if (type != 0x2a'
ARM = '					if (type != 0x2a && type != 0x2c) {\n						pages = len / 512;\n'
DECL = (FOR, FOR + '			uint32_t bo;\n\n')
PL = [('for', [(FOR, FOR + '			uint32_t bo = off & 0x1ffff;\n\n')]),
      ('big', [DECL, (IB, '			if (xb.bigBlock) {\n				bo = off & 0x1ffff;\n				((struct spb *)s)->b2lo')]),
      ('big2', [DECL, ('				s[1] = BLK;\n', '				s[1] = BLK;\n				bo = off & 0x1ffff;\n')]),
      ('bt', [DECL, (TT, '				if (type > 1) {\n					bo = off & 0x1ffff;\n					((struct spt *)s)->type = type;\n					if (type != 0x2a')]),
      ('bt2', [DECL, (TT, '				if (type > 1) {\n					((struct spt *)s)->type = type;\n					bo = off & 0x1ffff;\n					if (type != 0x2a')]),
      ('arm', [DECL, (ARM, '					if (type != 0x2a && type != 0x2c) {\n						bo = off & 0x1ffff;\n						pages = len / 512;\n')]),
      ('arm3', [DECL, ('						s[5] = 1;\n						s[8] = len >> 8;\n', '						bo = off & 0x1ffff;\n						s[5] = 1;\n						s[8] = len >> 8;\n')] ),
      ]
L = '					'
US = [('u0', [(USE0, '						s[9] = ((bo ? 256 - bo / 512 : 256) - left) >> 2;\n')]),
      ('u1', [(USE0, '						s[9] = ((bo ? 256 - (off & 0x1ffff) / 512 : 256) - left) >> 2;\n')]),
      ('u2', [(USE0, '						s[9] = (((off & 0x1ffff) ? 256 - bo / 512 : 256) - left) >> 2;\n')]),
      ('u3', [(USE0, '						bo = bo ? 256 - bo / 512 : 256;\n						s[9] = (bo - left) >> 2;\n')]),
      ('u4', [(USE0, '						if (bo)\n							bo = 256 - bo / 512;\n						else\n							bo = 256;\n						s[9] = (bo - left) >> 2;\n')]),
      ('u5', [(USE0, '						if (bo)\n							s[9] = (256 - bo / 512 - left) >> 2;\n						else\n							s[9] = (256 - left) >> 2;\n')]),
      ('u6', [(USE0, '						bo /= 512;\n						s[9] = ((bo ? 256 - bo : 256) - left) >> 2;\n')] if 0 else [(USE0, '						s[9] = (256 - (bo ? bo / 512 : 0) - left) >> 2;\n')]),
      ('u7', [(USE0, '						s[9] = (256 - bo / 512 - left) >> 2;\n')] ),
      ]
TL = [('', []), ('tb', [('	setBeU16(off >> 14, (uint8_t *)&xb.fsBlock);\n', '	setBeU16(blk, (uint8_t *)&xb.fsBlock);\n')])]
def FILTER(c):
    # u1, u2 and others need bo declared but u3/u4 assign it: keep arm-placed only with a use after it
    return True
AXES = [PL, US, TL]
FLAGS = []

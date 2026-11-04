# attempt 9: near8 with the arms of `if (xb.bigBlock)` in the page loop inverted, so the small arm (and its dead `pages ?:`) is numbered before the big arm.
import os, re
FLAGS = []
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_near8.c')
FOCUS = ['_imgAdd', '_imgAdd.constprop.1', '_imgAdd.constprop.2', '_imgAdd.constprop.4', '_imgAddFile', '_writeInitialHeader']
t = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', BASE), newline='').read().replace('\r\n', '\n')
i = t.index('			memset(s, 0, 16);\n			if (xb.bigBlock) {\n', t.index('int imgAdd(uint32_t off'))
j = t.index('#undef BLK')
whole = t[i:j]
HEAD = '			memset(s, 0, 16);\n			if (xb.bigBlock) {\n'
mid = whole.index('			} else {\n				pages =')
big = whole[len(HEAD):mid]
end = whole.index('			}\n		}\n	}\n', mid)
small = whole[mid + len('			} else {\n'):end]
tail = whole[end:]
SP = {'t': 'pages = len % 512 ? len / 512 + 1 : len / 512;', 'i': 'pages = len / 512;\n				if (len % 512)\n					pages++;', 'e': 'if (len % 512)\n					pages = len / 512 + 1;\n				else\n					pages = len / 512;'}
SP0 = 'pages = len % 512 ? len / 512 + 1 : len / 512;'
BP0 = 'pages = len / 512;\n						if (len % 512)\n							pages++;'
BP = {'i': BP0, 't': SP0, 'e': 'if (len % 512)\n							pages = len / 512 + 1;\n						else\n							pages = len / 512;'}
var = []
for c, cond in (('nb', 'if (!xb.bigBlock) {'), ('z', 'if (xb.bigBlock == 0) {')):
    for sk, sv in SP.items():
        for bk, bv in BP.items():
            var.append((c + sk + bk, [(whole, '			memset(s, 0, 16);\n			' + cond + '\n' + small.replace(SP0, sv) + '			} else {\n' + big.replace(BP0, bv) + tail)]))
AXES = [var]

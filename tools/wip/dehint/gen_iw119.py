# attempt 7: on a7: pin_t and lnp2 together: lnp2 forms set the split of t's test (a multiple of 10 ties with partial), t's position sets regnos.  Sort key ignores writeFsTable, which a local form can fix
import os
PIN = '''			/* no code: the slot order of t and partial (dead in every clone) */
			__asm__("" :: "g"(t));
'''
N = '''		if (!partial)
			npages = 32;
		else {
			/* imgAddFile's clone: keeps DOM2's threading from zeroing the npages guard edge */
			lnp2: __attribute__((hot));
		}
'''
T = "		t = type - '1';\n"
BL = '		blk = start + b;\n'
PA = '		partial = small && len < 0x4000;\n'
SM = "		small = 0;\n		if (type != 0 && type != '0')\n			small = 1;\n" + PA
TE = '		if (t < 15) {\n'
AXES = [
 [('', []), ('nopin', [(PIN, '')])],
 [('', []),
  ('plain', [(N, '		if (!partial)\n			npages = 32;\n')]),
  ('le', [(N, '		if (partial <= 0)\n			npages = 32;\n')]),
  ('lt', [(N, '		if (partial < 1)\n			npages = 32;\n')]),
  ('eq', [(N, '		if (partial == 0)\n			npages = 32;\n')]),
 ],
 [('', []),
  ('tb', [(T, ''), (BL, BL + T)]),
  ('ta', [(T, ''), (PA, PA + T)]),
 ],
 [('', []),
  ('f15', [(TE, '		if (t <= 14) {\n')]),
  ('fr', [(TE, "		if (type >= '1' && type < '@') {\n"), (T, '')]),
 ],
]
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_a7.c')
FLAGS = []
FOCUS = ['_imgAdd', '_imgAdd.constprop.1', '_imgAdd.constprop.2', '_imgAdd.constprop.4', '_imgAddFile', '_imgAddFileAs', '_imgAddMobile', '_addSmcConfig', '_writeInitialHeader', '_checkBootImage', '_finalizeImage', '_imgAddRaw']

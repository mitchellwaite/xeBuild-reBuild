# attempt 8: on n1p1 without pin_t (50/50 split of the t test, so t and partial tie at 180 and regno decides): forms that give t the lower regno.
import os
FLAGS = []
BASE = os.environ.get('IWB', 'build/iw/a8/n1p1t.c')
FOCUS = ['_imgAdd']
P = "		partial = (len < 0x4000) & (type != 0) & (type != '0');\n"
T = "		t = type - '1';\n"
BL = '		blk = start + b;\n'
PF = [
 ('p1', P),
 ('p2', "		partial = type != 0 && type != '0' && len < 0x4000;\n"),
 ('p3', "		small = 0;\n		if (type != 0 && type != '0')\n			small = 1;\n		partial = small && len < 0x4000;\n"),
 ('p4', "		partial = (type != 0) & (type != '0') & (len < 0x4000);\n"),
 ('p5', "		partial = (type != 0) & (type != '0') && len < 0x4000;\n"),
]
TPOS = [
 ('after', None),
 ('tfirst', 'first'),
 ('tbl', 'bl'),
]
EDITS = []
for pn, pt in PF:
    for tn, tp in TPOS:
        if tp is None:
            EDITS.append((pn + tn, [(P + T, pt + T)]))
        elif tp == 'first':
            EDITS.append((pn + tn, [(P + T, T + pt)]))
        else:
            EDITS.append((pn + tn, [(P + T, pt), (BL, T + BL)]))
TT = [
 ('', []),
 ('tint', [('	uint8_t t;\n', '	unsigned t;\n'), ('if (t < 15) {', 'if ((uint8_t)t < 15) {')]),
 ('tcast', [("t = type - '1';", "t = (uint8_t)(type - '1');")]),
]
AXES = [EDITS, TT]

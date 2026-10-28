"""genq.py OUT.c X2LABELS [RX...]   build a vY-based variant with
  * X2: asm goto at the end of the rok path (after cinfo = netGetInfo()) to the given labels
    (sp RTL names: 112 hdd4, 115 hdd5, 103 u2, cases 107 c1 108 c2 109 c3 116 c7 119 c8 120 c9
     121 c10 128 c11 129 c12 132 cdef, 117 p0 = clientPatches(NULL), 130 i0 = clientInfo(NULL))
  * RX sources: '126:125' (asm goto after the outside-range log in clientEraseBlock -> efail),
    '117:130' (asm goto after clientPatches(NULL) -> i0)
X2LABELS: comma list of sp numbers in edge order, e.g. 112,115,103,107"""
import sys
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
LAB = {112: 'hdd4', 115: 'hdd5', 103: 'u2', 107: 'c1', 108: 'c2', 109: 'c3', 116: 'c7', 119: 'c8', 120: 'c9',
       121: 'c10', 128: 'c11', 129: 'c12', 132: 'cdef', 117: 'p0', 130: 'i0'}
out, x2 = sys.argv[1], [int(x) for x in sys.argv[2].split(',') if x]
x1 = [int(x) for x in sys.argv[3].split(',') if x] if len(sys.argv) > 3 and not ':' in sys.argv[3] else None
rx = [a for a in sys.argv[3:] if ':' in a]
s = open(ROOT + r'\wip\mc\s12\vY.c').read()
def rep(a, b):
    global s
    assert s.count(a) == 1, a
    s = s.replace(a, b)
if x2:
    rep("""			rok: __attribute__((cold));
				cinfo = netGetInfo();""", """			rok: __attribute__((cold));
				cinfo = netGetInfo();
				__asm__ goto ("" :::: %s);""" % ', '.join(LAB[t] for t in x2))
if x1 is not None:
    rep('__asm__ goto ("" :::: hdd4, hdd5, c10);', ('__asm__ goto ("" :::: %s);' % ', '.join(LAB[t] for t in x1)) if x1 else '')
rep("""		} else
			client_usage(2, NULL);""", """		} else
			{ u2: client_usage(2, NULL); }""")
rep("case 1:\n\t\t\t\tnetDumpNand(arg);", "case 1:\n\t\t\t\tc1: netDumpNand(arg);")
rep("case 2:\n\t\t\t\tclientWrite(arg);", "case 2:\n\t\t\t\tc2: clientWrite(arg);")
rep("case 3:\n\t\t\t\tclientKeys();", "case 3:\n\t\t\t\tc3: clientKeys();")
rep("case 7:\n\t\t\t\tif (arg == dummy)\n\t\t\t\t\tclientPatches(NULL);",
    "case 7:\n\t\t\t\tc7: if (arg == dummy)\n\t\t\t\t\t{ p0: clientPatches(NULL);%s }" %
    (' __asm__ goto ("" :::: i0);' if '117:130' in rx else ''))
rep("case 8:\n\t\t\t\tclientReadBlocks(", "case 8:\n\t\t\t\tc8: clientReadBlocks(")
rep("case 9:\n\t\t\t\tclientWriteBlocks(", "case 9:\n\t\t\t\tc9: clientWriteBlocks(")
rep("case 11:\n\t\t\t\tclientBinPatch(", "case 11:\n\t\t\t\tc11: clientBinPatch(")
rep("case 12:\n\t\t\t\tif (arg == dummy)\n\t\t\t\t\tclientInfo(NULL);",
    "case 12:\n\t\t\t\tc12: if (arg == dummy)\n\t\t\t\t\t{ i0: clientInfo(NULL); }")
rep("default:\n\t\t\t\tlog_printf(0, \"\\n\\n***** ERROR: invalid mode", "default:\n\t\t\t\tcdef: log_printf(0, \"\\n\\n***** ERROR: invalid mode")
if '126:125' in rx:
    rep("""				log_printf(0, "\\n\\n***** ERROR: Failed to erase block 0x%x!\\n", block);""",
        """				{ efail: log_printf(0, "\\n\\n***** ERROR: Failed to erase block 0x%x!\\n", block); }""")
    rep("""			log_printf(0, "\\n\\n***** ERROR: Block 0x%x is outside system area!\\n", block);""",
        """			{ log_printf(0, "\\n\\n***** ERROR: Block 0x%x is outside system area!\\n", block); __asm__ goto ("" :::: efail); }""")
open(out, 'w', newline='\n').write(s)

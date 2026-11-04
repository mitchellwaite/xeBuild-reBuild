# attempt 11: lnp2 gone with pages kept at src's place, and the writeInitialHeader inline taken out of the picture with a PROBE flag (--param inline-min-speedup=11; never a candidate): imgAddFile's compare, clones.
# If a state here is right everywhere else, the inline can be attacked through the caller's time (imgWriteHdr, gen_iw181).  FOCUS leaves writeInitialHeader and the call-offset functions out.
import os
BASE = os.environ.get('IWB', 'src/image_write.c')
P0 = """		small = 0;
		if (type != 0 && type != '0')
			small = 1;
		partial = small && len < 0x4000;
"""
TT = "		t = type - '1';\n"
N0 = """		if (len % 512)
			npages = (len + 512) / 512;
		else
			npages = len / 512;
		if (!partial)
			npages = 32;
		else {
			/* imgAddFile's clone: keeps DOM2's threading from zeroing the npages guard edge */
			lnp2: __attribute__((hot));
		}
"""
NI = """			if (len % 512)
				npages = (len + 512) / 512;
			else
				npages = len / 512;
"""
PF = {
 'P0': P0,
 'P1': "		partial = (len < 0x4000) & (type != 0) & (type != '0');\n",
 'P2': "		small = 0;\n		if (type != 0 && type != '0')\n			small = 1;\n		partial = small & (len < 0x4000);\n",
 'P3': "		partial = len < 0x4000 && type != 0 && type != '0';\n",
 'P4': "		small = type != 0 && type != '0';\n		partial = small && len < 0x4000;\n",
 'P5': "		partial = 0;\n		if (type != 0 && type != '0' && len < 0x4000)\n			partial = 1;\n",
}
NF = {
 'A': '		if (partial > 0) {\n' + NI + '		} else\n			npages = 32;\n',
 'B': NI.replace('			', '		').replace('	npages', 'npages').replace('		npages', '		npages') if False else '		if (len % 512)\n			npages = (len + 512) / 512;\n		else\n			npages = len / 512;\n		if (partial <= 0)\n			npages = 32;\n',
 'D': '		npages = 32;\n		if (partial > 0) {\n' + NI + '		}\n',
 'E': '		if (partial <= 0)\n			npages = 32;\n		else {\n' + NI + '		}\n',
 'F': '		npages = partial > 0 ? (len % 512 ? (len + 512) / 512 : len / 512) : 32;\n',
 'G': '		if (partial) {\n' + NI + '		} else\n			npages = 32;\n',
}
AXES = [
 [(k, [(P0 + TT, v + TT)]) for k, v in PF.items()],
 [(k, [(N0, v)]) for k, v in NF.items()],
 [('', []), ('nb', [('		blk = start + b;\n', ''), ('b2lo = blk >> 8', 'b2lo = BLK >> 8')])],
]
FLAGS = ['--param', 'inline-min-speedup=11']
FOCUS = ['_imgAdd', '_imgAdd.constprop.1', '_imgAdd.constprop.2', '_imgAdd.constprop.4', '_imgAddFile']

"""findAnchor written as the reference's final CFG (threaded paths spelled out with gotos), no hints at all or
with a few kept: no thread means no update_profile artefacts and the literal order comes from source order."""
FOCUS = ['_findAnchor']
BEG = '	ok0 = shaSelfCheck(xb.dump + 0x2fe8000);\n'
END = '	return 0;\n}\n\nint mmcFindMobiles'
VAL0 = 'log_printf(1, "anchor block v %d at 0x2fe8000 is valid\\n", v0);\n'
INV0 = 'log_printf(1, "anchor block at 0x2fe8000 is invalid\\n");\n'
VAL1 = 'log_printf(1, "anchor block v %d at 0x2fec000 is valid\\n", v1);\n'
INV1 = 'log_printf(1, "anchor block at 0x2fec000 is invalid\\n");\n'
SEL0 = '''log_printf(1, "anchor block v %d at 0x2fe8000 is selected\\n", v0);
	memcpy(anchor, xb.dump + 0x2fe8000, 0x200);
	return 1;
'''
SEL1 = '''log_printf(1, "anchor block v %d at 0x2fec000 is selected\\n", v1);
	memcpy(anchor, xb.dump + 0x2fec000, 0x200);
	return 1;
'''
SHA0 = 'ok0 = shaSelfCheck(xb.dump + 0x2fe8000);\n'
SHA1 = 'ok1 = shaSelfCheck(xb.dump + 0x2fec000);\n'
S = {}
S['g1'] = f'''{SHA0}if (ok0) {{
{VAL0}{SHA1}if (!ok1)
goto inv;
goto both;
}}
{INV0}{SHA1}if (ok1) {{
{VAL1}sel1:
{SEL1}}}
inv:
{INV1}if (ok0) {{
sel0:
{SEL0}}}
return 0;
both:
{VAL1}if (v0 >= v1)
goto sel0;
goto sel1;
'''
S['g2'] = f'''{SHA0}if (ok0) {{
{VAL0}{SHA1}if (ok1)
goto both;
}} else {{
{INV0}{SHA1}if (ok1) {{
{VAL1}goto sel1;
}}
}}
{INV1}if (ok0)
goto sel0;
return 0;
both:
{VAL1}if (v0 >= v1)
goto sel0;
sel1:
{SEL1}sel0:
{SEL0}'''
S['g3'] = f'''{SHA0}if (ok0) {{
{VAL0}{SHA1}if (ok1) {{
{VAL1}if (v0 < v1)
goto sel1;
goto sel0;
}}
}} else {{
{INV0}{SHA1}if (ok1) {{
{VAL1}sel1:
{SEL1}}}
}}
{INV1}if (!ok0)
return 0;
sel0:
{SEL0}'''
S['g4'] = f'''{SHA0}if (!ok0) {{
{INV0}{SHA1}if (ok1) {{
{VAL1}goto sel1;
}}
}} else {{
{VAL0}{SHA1}if (ok1) {{
{VAL1}if (v0 < v1) {{
sel1:
{SEL1}}}
goto sel0;
}}
}}
{INV1}if (!ok0)
return 0;
sel0:
{SEL0}'''
import os
_t = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'src', 'image_read.c'), newline='').read().replace('\r\n', '\n')
_a = _t.index(BEG)
_b = _t.index(END)
OLD = _t[_a:_b + len('	return 0;\n')]
AXES = [[(k, [(OLD, v)]) for k, v in S.items()]]

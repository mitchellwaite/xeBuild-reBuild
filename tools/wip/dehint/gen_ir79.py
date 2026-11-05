"""gen_ir63's copyMmcImage + loadDump forms again, on attempt 4's draft (parseDump's hints are gone, so its costs may have moved), plus forms with the zeropair test nested under a stored result."""
import importlib.util, os
_s = importlib.util.spec_from_file_location('g63', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_ir63.py'))
_m = importlib.util.module_from_spec(_s)
_s.loader.exec_module(_m)
FOCUS = ['_copyMmcImage', '_loadDump']
BASE = 'tools/wip/dehint/drafts/image_read_attempt4.c'
ATTR, USE, LOG, HEAD = _m.ATTR, _m.USE, _m.LOG, _m.HEAD
B = list(_m.AXB)
for k, body in {
    'ok.nest': '	uint32_t ok = notZeropair();\n\n	if (ok) {\n		return ok;\n	}\n	' + LOG + '	return 0;\n}\n',
    'ok.ret': '	uint32_t ok = notZeropair();\n\n	if (!ok)\n		' + LOG + '	return ok;\n}\n',
    'ok.ne': '	uint32_t ok = 0;\n\n	if (notZeropair())\n		ok = 1;\n	else\n		' + LOG + '	return ok;\n}\n',
    'ok.eq': '	uint32_t ok = 1;\n\n	if (!notZeropair()) {\n		' + LOG + '		ok = 0;\n	}\n	return ok;\n}\n',
}.items():
    B.append((k, [(ATTR, HEAD + '	' + body if False else HEAD + body)]))
AXES = [B, _m.AXU]

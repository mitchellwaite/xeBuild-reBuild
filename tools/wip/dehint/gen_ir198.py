"""fsGetFile, no pin: whole-function forms so that P(found fails) lands in [71,74] (window measured with gen_ir197): call 71 alone or an opcode predictor alone (attempt 13)."""
import re, os
FOCUS = ['_fsGetFile']
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')
src = open(os.path.join(R, 'src', 'image_read.c'), newline='').read().replace('\r\n', '\n')
a = src.index('int fsGetFile(const char *name, uint8_t **buf')
b = src.index('int findAnchor(void)\n{')
OLD = src[a:b]
HEAD = 'int fsGetFile(const char *name, uint8_t **buf, uint32_t *size, uint32_t *time)\n{\n	uint32_t block, len, t, off, left, done;\n	uint8_t *p;\n	int v = fsValid;\n	int ret = 0;\n	int f;\n'
COPY = '''off = fsOffset + (block << 14);
p = calloc(len, 1);
left = len;
done = 0;
while (left > 0x4000) {
	memcpy(p + done, xb.dump + off, 0x4000);
	left -= 0x4000;
	done += 0x4000;
	block = SWAP16(fs->map[block]) & 0x1fff;
	off = fsOffset + (block << 14);
}
if (left)
	memcpy(p + done, xb.dump + off, left);
*buf = p;
*size = len;
*time = t;
'''
FIND = 'fsFind(name, &block, &len, &t, 1)'
T = {
 # single exit
 'ret1': f'if (v == 1) {{ if ({FIND}) {{ {COPY} ret = 1; }} }}\n return ret;\n',
 'ret2': f'if (v == 1 && {FIND}) {{ {COPY} ret = 1; }}\n return ret;\n',
 'ret3': f'if (v != 1) return 0;\n if ({FIND}) {{ {COPY} ret = 1; }}\n return ret;\n',
 'ret4': f'if (v != 1) return ret;\n if ({FIND}) {{ {COPY} ret = 1; }}\n return ret;\n',
 'ret5': f'if (v == 1) {{ ret = {FIND}; if (ret) {{ {COPY} }} }}\n return ret;\n',
 'ret6': f'if (v != 1) return 0;\n ret = {FIND}; if (ret) {{ {COPY} }}\n return ret;\n',
 'ret7': f'if (v == 1) {{ ret = {FIND}; if (ret) {{ {COPY} ret = v; }} }}\n return ret;\n',
 'ret8': f'if (v != 1) return 0;\n ret = {FIND}; if (!ret) return 0;\n {COPY} return ret;\n',
 'ret9': f'if (v != 1) return 0;\n f = {FIND}; if (!f) return 0;\n {COPY} return f;\n',
 'reta': f'if (v != 1) return 0;\n f = {FIND}; if (f) {{ {COPY} }} return f;\n',
 'retb': f'if (v == 1) {{ f = {FIND}; if (f) {{ {COPY} return f; }} }} return 0;\n',
 # opcode predictor alone: the failure arm has the call heuristic cancelled
 'gt': f'if (v != 1) return 0;\n f = !{FIND}; if (f > 0) return 0;\n {COPY} return 1;\n',
 'ne': f'if (v != 1) return 0;\n if ({FIND} != 1) return 0;\n {COPY} return 1;\n',
 # a goto to one failure exit
 'g1': f'if (v != 1) goto fail;\n if (!{FIND}) goto fail;\n {COPY} return 1;\n fail: return 0;\n',
 'g2': f'if (v == 1) {{ if ({FIND}) goto copy; }} return 0;\n copy: {COPY} return 1;\n',
 'g3': f'if (v != 1 || !{FIND}) return 0;\n {COPY} return 1;\n',
 'g4': f'if (v == 1 && {FIND}) goto copy; return 0;\n copy: {COPY} return v;\n',
 'g5': f'if (v != 1) return 0;\n if ({FIND}) goto copy; return 0;\n copy: {COPY} return 1;\n',
 'v1': f'if (v != 1) return 0;\n if (!{FIND}) return 0;\n {COPY} return v;\n',
 'v2': f'if (v == 1) {{ if ({FIND}) {{ {COPY} return v; }} }} return 0;\n',
}
AXES = [[(k, [(OLD, HEAD + v + '}\n\n')]) for k, v in T.items()]]

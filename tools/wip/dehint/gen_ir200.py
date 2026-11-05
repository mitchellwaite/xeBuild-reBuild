"""fsGetFile, no pin: block, len, t scoped to the arm that uses them: leaving the scope clobbers them, so the fail path has a real block at profile_estimate (attempt 13)."""
import os
FOCUS = ['_fsGetFile']
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')
src = open(os.path.join(R, 'src', 'image_read.c'), newline='').read().replace('\r\n', '\n')
a = src.index('int fsGetFile(const char *name, uint8_t **buf')
b = src.index('int findAnchor(void)\n{')
OLD = src[a:b]
SIG = 'int fsGetFile(const char *name, uint8_t **buf, uint32_t *size, uint32_t *time)\n{\n'
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
L = 'uint32_t block, len, t;\n'
L2 = 'uint32_t off, left, done;\nuint8_t *p;\n'
V = 'int v = fsValid;\n'
T = {
 'a': SIG + V + f'if (v == 1) {{ {L}{L2} if ({FIND}) {{ {COPY} return 1; }} }}\n return 0;\n}}\n\n',
 'b': SIG + V + f'if (v != 1) return 0;\n {{ {L}{L2} if ({FIND}) {{ {COPY} return 1; }} }}\n return 0;\n}}\n\n',
 'c': SIG + f'if (fsValid == 1) {{ {L}{L2} if ({FIND}) {{ {COPY} return 1; }} }}\n return 0;\n}}\n\n',
 'd': SIG + V + L2 + f'if (v == 1) {{ {L} if ({FIND}) {{ {COPY} return 1; }} }}\n return 0;\n}}\n\n',
 'e': SIG + V + f'if (v == 1) {{ {L}{L2} if ({FIND}) {{ {COPY} return v; }} }}\n return 0;\n}}\n\n',
 'f': SIG + V + f'if (v == 1) {{ {L}{L2} int r = {FIND}; if (r) {{ {COPY} }} return r; }}\n return 0;\n}}\n\n',
 'g': SIG + V + 'int ret = 0;\n' + f'if (v == 1) {{ {L}{L2} if ({FIND}) {{ {COPY} ret = 1; }} }}\n return ret;\n}}\n\n',
 'h': SIG + V + f'if (v == 1) {{ uint32_t block; {L2} {{ uint32_t len, t; if ({FIND}) {{ {COPY} return 1; }} }} }}\n return 0;\n}}\n\n',
}
AXES = [[(k, [(OLD, v)]) for k, v in T.items()]]

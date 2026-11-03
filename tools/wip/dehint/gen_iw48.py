# finalizeImage without the hdr pin: the reload of xb.hdr in the ECC arm through a local of another pointer type, so that
# the PHI's chain has names of two pointer types (out-of-SSA won't coalesce them: a real copy, one ref more for IRA)
FOCUS = ['_finalizeImage']
OLD = '''			if (!pageErased(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16))
				calcPageEcc(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16);
			__asm__("" :: "a"(xb.hdr));
			memcpy(raw, xb.hdr + (b * 32 + p) * 512, 512);
			memcpy(raw + 512, xb.spare + (b * 32 + p) * 16, 16);
			raw += 528;
'''
X = '(b * 32 + p) * 512'
Y = '(b * 32 + p) * 16'
H = 'xb.hdr + ' + X
S = 'xb.spare + ' + Y
CALL = f'calcPageEcc({H}, {S});'
TAIL = f'			memcpy(raw + 512, {S}, 16);\n			raw += 528;\n'
TY = {'cu8': ('const uint8_t *', ''), 'v': ('const void *', '(const uint8_t *)'), 'nv': ('void *', '(uint8_t *)'), 'c': ('const char *', '(const uint8_t *)')}
F = {}
for k, (ty, c) in TY.items():
    F['a' + k] = (f'			{{ {ty}h = xb.hdr;\n			if (!pageErased({c}h + {X}, {S})) {{\n				{CALL}\n				h = xb.hdr;\n			}}\n'
                  f'			memcpy(raw, {c}h + {X}, 512); }}\n' + TAIL)
    F['b' + k] = (f'			{{ {ty}h = xb.hdr;\n			if (!pageErased({H}, {S})) {{\n				{CALL}\n				h = xb.hdr;\n			}}\n'
                  f'			memcpy(raw, {c}h + {X}, 512); }}\n' + TAIL)
    F['c' + k] = (f'			{{ {ty}h;\n			if (!pageErased({H}, {S})) {{\n				{CALL}\n			}}\n			h = xb.hdr;\n'
                  f'			memcpy(raw, {c}h + {X}, 512); }}\n' + TAIL)
    # order: spare's local first
    F['d' + k] = (f'			{{ uint8_t *ss = xb.spare; {ty}h = xb.hdr;\n			if (!pageErased({c}h + {X}, ss + {Y})) {{\n				{CALL}\n				h = xb.hdr;\n			}}\n'
                  f'			memcpy(raw, {c}h + {X}, 512); }}\n' + TAIL)
    F['e' + k] = (f'			{{ uint8_t *ss = {S}; {ty}h = xb.hdr;\n			if (!pageErased({c}h + {X}, ss)) {{\n				{CALL}\n				h = xb.hdr;\n			}}\n'
                  f'			memcpy(raw, {c}h + {X}, 512); }}\n' + TAIL)
    F['f' + k] = (f'			{{ {ty}h = {H};\n			if (!pageErased(h, {S})) {{\n				{CALL}\n				h = {H};\n			}}\n'
                  f'			memcpy(raw, h, 512); }}\n' + TAIL)
    F['g' + k] = (f'			{{ {ty}h;\n			if (!pageErased({H}, {S})) {{\n				{CALL}\n				h = xb.hdr;\n			}} else\n				h = xb.hdr;\n'
                  f'			memcpy(raw, {c}h + {X}, 512); }}\n' + TAIL)
AXES = [[(n, [(OLD, f)]) for n, f in F.items()]]

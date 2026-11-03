# finalizeImage without the hdr pin: split the *spare* PHI chain (reload in the ECC arm through a local of another pointer type):
# its pseudo gets cheaper than hdr's, so hdr pops first and keeps spare's loads first in the preheader.
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
TY = {'v': ('const void *', '(const uint8_t *)'), 'nv': ('void *', '(uint8_t *)'), 'c': ('const char *', '(const uint8_t *)'), 'cu8': ('const uint8_t *', '')}
F = {}
for k, (ty, c) in TY.items():
    F['a' + k] = (f'			{{ {ty}ss = xb.spare;\n			if (!pageErased({H}, {c}ss + {Y})) {{\n				{CALL}\n				ss = xb.spare;\n			}}\n'
                  f'			memcpy(raw, {H}, 512);\n			memcpy(raw + 512, {c}ss + {Y}, 16); }}\n			raw += 528;\n')
    F['b' + k] = (f'			{{ {ty}ss = xb.spare;\n			if (!pageErased({H}, {S})) {{\n				{CALL}\n				ss = xb.spare;\n			}}\n'
                  f'			memcpy(raw, {H}, 512);\n			memcpy(raw + 512, {c}ss + {Y}, 16); }}\n			raw += 528;\n')
AXES = [[(n, [(OLD, f)]) for n, f in F.items()]]

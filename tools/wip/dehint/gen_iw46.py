# finalizeImage without the "a"(xb.hdr) pin: load xb.hdr into a local of another pointer type.
# Out-of-SSA doesn't coalesce names of different pointer types, so the hdr PHI gets a real copy
# (one more ref at the reload block's frequency, the +136 cost the asm gave), which RA then removes.
FOCUS = ['_finalizeImage']
OLD = '''			if (!pageErased(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16))
				calcPageEcc(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16);
			__asm__("" :: "a"(xb.hdr));
			memcpy(raw, xb.hdr + (b * 32 + p) * 512, 512);
			memcpy(raw + 512, xb.spare + (b * 32 + p) * 16, 16);
			raw += 528;
'''
H = 'xb.hdr + (b * 32 + p) * 512'
S = 'xb.spare + (b * 32 + p) * 16'
T0 = f'			if (!pageErased({H}, {S}))\n				calcPageEcc({H}, {S});\n'
TYPES = {'cu8': 'const uint8_t *', 'v': 'void *', 'cv': 'const void *', 'c': 'char *', 'cc': 'const char *', 'u32': 'uint32_t *'}
forms = []
for k, ty in TYPES.items():
    # load after the if, used in the copy
    forms.append(('after_' + k, T0 + f'			{{ {ty}h = xb.hdr; memcpy(raw, (const uint8_t *)h + (b * 32 + p) * 512, 512); }}\n'
                  f'			memcpy(raw + 512, {S}, 16);\n			raw += 528;\n'))
    # load in the arm only
    forms.append(('both_' + k, f'			{{ {ty}h = xb.hdr; if (!pageErased((const uint8_t *)h + (b * 32 + p) * 512, {S}))\n				calcPageEcc({H}, {S});\n'
                  f'			h = xb.hdr; memcpy(raw, (const uint8_t *)h + (b * 32 + p) * 512, 512); }}\n'
                  f'			memcpy(raw + 512, {S}, 16);\n			raw += 528;\n'))
    # the page pointer itself
    forms.append(('first_' + k, f'			{{ {ty}h = xb.hdr; if (!pageErased((const uint8_t *)h + (b * 32 + p) * 512, {S}))\n				calcPageEcc({H}, {S}); }}\n'
                  f'			memcpy(raw, {H}, 512);\n			memcpy(raw + 512, {S}, 16);\n			raw += 528;\n'))
AXES = [[(n, [(OLD, f)]) for n, f in forms]]

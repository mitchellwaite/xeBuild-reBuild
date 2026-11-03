# finalizeImage without the hdr pin: order of the hdr and spare loads with a const hdr local (gen_iw46 first_cu8: only esi/edi and load order left)
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
TAIL0 = f'			memcpy(raw, {H}, 512);\n			memcpy(raw + 512, {S}, 16);\n			raw += 528;\n'
TAILS = {
 'tH': TAIL0,
 'tHh': f'			{{ const uint8_t *h2 = xb.hdr; memcpy(raw, h2 + {X}, 512); }}\n			memcpy(raw + 512, {S}, 16);\n			raw += 528;\n',
 'tSH': f'			memcpy(raw + 512, {S}, 16);\n			memcpy(raw, {H}, 512);\n			raw += 528;\n',
}
TY = {'cu8': 'const uint8_t *', 'v': 'const void *'}
HEADS = {}
for k, ty in TY.items():
    c = '(const uint8_t *)' if k != 'cu8' else ''
    HEADS['h1' + k] = f'			{{ {ty}h = xb.hdr; if (!pageErased({c}h + {X}, {S}))\n				{CALL} }}\n'
    HEADS['h2' + k] = f'			{{ uint8_t *ss = xb.spare; {ty}h = xb.hdr; if (!pageErased({c}h + {X}, ss + {Y}))\n				{CALL} }}\n'
    HEADS['h3' + k] = f'			{{ uint8_t *ss = {S}; {ty}h = xb.hdr; if (!pageErased({c}h + {X}, ss))\n				{CALL} }}\n'
    HEADS['h4' + k] = f'			{{ uint8_t *ss = {S}; {ty}h = xb.hdr; if (!pageErased({c}h + {X}, ss))\n				calcPageEcc({H}, ss); }}\n'
    HEADS['h5' + k] = f'			{{ {ty}h = xb.hdr; uint8_t *ss = xb.spare; if (!pageErased({c}h + {X}, ss + {Y}))\n				{CALL} }}\n'
    HEADS['h6' + k] = f'			{{ uint8_t *ss = xb.spare; {ty}h = xb.hdr; if (!pageErased({c}h + {X}, ss + {Y}))\n				calcPageEcc({H}, ss + {Y}); }}\n'
    HEADS['h7' + k] = f'			{{ uint8_t *ss = {S}; {ty}h = xb.hdr + {X}; if (!pageErased(h, ss))\n				calcPageEcc({H}, ss); }}\n'
    HEADS['h8' + k] = f'			{{ {ty}h = xb.hdr + {X}; if (!pageErased(h, {S}))\n				{CALL} }}\n'
    HEADS['h9' + k] = f'			{{ {ty}h = xb.hdr; if (pageErased({c}h + {X}, {S}))\n				goto copy; }}\n			{CALL}\n			copy:\n'
AXES = [[(n + '+' + t, [(OLD, f + tf)]) for n, f in HEADS.items() for t, tf in TAILS.items()]]

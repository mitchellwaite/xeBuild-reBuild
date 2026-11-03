# finalizeImage: forms of the ECD loop without the "a"(xb.hdr) pin
BASE = 'tools/wip/dehint/drafts/image_write.c'
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
TESTS = {
    't0': f'			if (!pageErased({H}, {S}))\n				calcPageEcc({H}, {S});\n',
    'tS': f'			{{ uint8_t *ss = {S}; if (!pageErased({H}, ss)) calcPageEcc({H}, ss); }}\n',
    'tH': f'			{{ uint8_t *hh = {H}; if (!pageErased(hh, {S})) calcPageEcc(hh, {S}); }}\n',
    'tHS': f'			{{ uint8_t *hh = {H}, *ss = {S}; if (!pageErased(hh, ss)) calcPageEcc(hh, ss); }}\n',
    'tSH': f'			{{ uint8_t *ss = {S}, *hh = {H}; if (!pageErased(hh, ss)) calcPageEcc(hh, ss); }}\n',
}
COPIES = {
    'c0': f'			memcpy(raw, {H}, 512);\n			memcpy(raw + 512, {S}, 16);\n',
    'cHS': f'			{{ uint8_t *h2 = {H}, *s2 = {S}; memcpy(raw, h2, 512); memcpy(raw + 512, s2, 16); }}\n',
    'cSH': f'			{{ uint8_t *s2 = {S}, *h2 = {H}; memcpy(raw, h2, 512); memcpy(raw + 512, s2, 16); }}\n',
    'cS': f'			{{ uint8_t *s2 = {S}; memcpy(raw, {H}, 512); memcpy(raw + 512, s2, 16); }}\n',
    'cH': f'			{{ uint8_t *h2 = {H}; memcpy(raw, h2, 512); memcpy(raw + 512, {S}, 16); }}\n',
    'cOff': f'			{{ uint32_t pg = b * 32 + p; memcpy(raw, xb.hdr + pg * 512, 512); memcpy(raw + 512, xb.spare + pg * 16, 16); }}\n',
    'cR': f'			memcpy(raw + 512, {S}, 16);\n			memcpy(raw, {H}, 512);\n',
}
AXES = []
AXES.append([(t + '+' + c, [(OLD, TESTS[t] + COPIES[c] + '			raw += 528;\n')]) for t in TESTS for c in COPIES])

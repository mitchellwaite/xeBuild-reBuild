# finalizeImage: page index forms x test forms x copy forms without the "a"(xb.hdr) pin
BASE = 'tools/wip/dehint/drafts/image_write.c'
FOCUS = ['_finalizeImage']
OLD = '''		for (p = 0; p < 32; p++) {
			if (!pageErased(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16))
				calcPageEcc(xb.hdr + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16);
			__asm__("" :: "a"(xb.hdr));
			memcpy(raw, xb.hdr + (b * 32 + p) * 512, 512);
			memcpy(raw + 512, xb.spare + (b * 32 + p) * 16, 16);
			raw += 528;
		}
'''
IDX = {
    'ia': ('', '(b * 32 + p) * 512', '(b * 32 + p) * 16', '(b * 32 + p) * 512', '(b * 32 + p) * 16'),
    'ib': ('', 'b * 0x4000 + p * 512', 'b * 0x200 + p * 16', 'b * 0x4000 + p * 512', 'b * 0x200 + p * 16'),
    'ic': ('uint32_t pg = b * 32 + p; ', 'pg * 512', 'pg * 16', 'pg * 512', 'pg * 16'),
    'id': ('uint32_t ho = (b * 32 + p) * 512, so = (b * 32 + p) * 16; ', 'ho', 'so', 'ho', 'so'),
    'ie': ('', '(b * 32 + p) * 512', '(b * 32 + p) * 16', 'b * 0x4000 + p * 512', 'b * 0x200 + p * 16'),
    'if': ('', '(b * 32 + p) << 9', '(b * 32 + p) << 4', '(b * 32 + p) << 9', '(b * 32 + p) << 4'),
    'ig': ('uint32_t so = (b * 32 + p) * 16; ', 'so * 32', 'so', 'so * 32', 'so'),
    'ih': ('uint32_t ho = (b * 32 + p) * 512; ', 'ho', 'ho / 32', 'ho', 'ho / 32'),
}
TST = {
    't0': lambda h, s: f'if (!pageErased({h}, {s})) calcPageEcc({h}, {s}); ',
    'te': lambda h, s: f'int e = pageErased({h}, {s}); if (!e) calcPageEcc({h}, {s}); ',
    'tn': lambda h, s: f'if (pageErased({h}, {s}) == 0) calcPageEcc({h}, {s}); ',
    'tl': lambda h, s: f'uint8_t *hh = {h}, *ss = {s}; if (!pageErased(hh, ss)) calcPageEcc(hh, ss); ',
    'tl2': lambda h, s: f'uint8_t *ss = {s}; if (!pageErased({h}, ss)) calcPageEcc({h}, ss); ',
}
CPY = {
    'c0': lambda h, s: f'memcpy(raw, {h}, 512); memcpy(raw + 512, {s}, 16); raw += 528; ',
    'c1': lambda h, s: f'memcpy(raw, {h}, 512); raw += 512; memcpy(raw, {s}, 16); raw += 16; ',
    'c2': lambda h, s: f'{{ uint8_t *h2 = {h}; memcpy(raw, h2, 512); }} memcpy(raw + 512, {s}, 16); raw += 528; ',
    'c3': lambda h, s: f'{{ uint8_t *s2 = {s}; memcpy(raw, {h}, 512); memcpy(raw + 512, s2, 16); }} raw += 528; ',
}
axis = []
for i, (pre, h1, s1, h2, s2) in IDX.items():
    for t, tf in TST.items():
        for c, cf in CPY.items():
            H1 = 'xb.hdr + ' + h1
            S1 = 'xb.spare + ' + s1
            H2 = 'xb.hdr + ' + h2
            S2 = 'xb.spare + ' + s2
            axis.append((i + '+' + t + '+' + c, [(OLD, '		for (p = 0; p < 32; p++) {\n			' + pre + tf(H1, S1) + cf(H2, S2) + '\n		}\n')]))
AXES = [axis]

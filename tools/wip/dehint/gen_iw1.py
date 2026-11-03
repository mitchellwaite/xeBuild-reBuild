# buildImage: replace the ebx pin by reusing a local (tree-coalesce-vars gives one pseudo)
PIN = '''			bb = xb.bigBlock;
			__asm__("" :: "b"(bb));
			if (bb)
'''
FOCUS = ['_buildImage']
AXES = [[
    ('plain', [(PIN, '			if (xb.bigBlock)\n')]),
    ('bb', [(PIN, '			bb = xb.bigBlock;\n			if (bb)\n')]),
    ('cf', [(PIN, '			cf = xb.bigBlock;\n			if (cf)\n')]),
    ('raw', [(PIN, '			rawSize = xb.bigBlock;\n			if (rawSize)\n')]),
    ('spare', [(PIN, '			spareSize = xb.bigBlock;\n			if (spareSize)\n')]),
    ('user', [(PIN, '			userSize = xb.bigBlock;\n			if (userSize)\n')]),
    ('bigB', [(PIN, '			bigBlock = xb.bigBlock;\n			if (bigBlock)\n')]),
    ('spp', [(PIN, '			spare = (uint8_t *)xb.bigBlock;\n			if (spare)\n')]),
    ('hdr', [(PIN, '			hdr = (uint8_t *)xb.bigBlock;\n			if (hdr)\n')]),
]]

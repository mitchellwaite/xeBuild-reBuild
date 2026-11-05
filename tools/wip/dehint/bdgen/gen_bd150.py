"""Small cleanups in src: dead `else if (type)` in loadBl, the r6 local in case 6, `(uint32_t)` loop casts; console's other always-set forms."""
OPS = {
    'el': ('} else if (type)\n\t\t\t\t\tlog_printf(1, "loaded %s, signature check passed!', '} else\n\t\t\t\t\tlog_printf(1, "loaded %s, signature check passed!'),
    'r6': ('uint32_t r6 = checkBl(e->data, e->size, 6, e->crc);\n\n\t\t\t*pr = r6;\n', '*pr = checkBl(e->data, e->size, 6, e->crc);\n'),
    'r6b': ('if (!*pr) {\n\t\t\tuint32_t r6 = checkBl(e->data, e->size, 6, e->crc);\n\n\t\t\t*pr = r6;\n\t\t}\n', 'if (!*pr)\n\t\t\t*pr = checkBl(e->data, e->size, 6, e->crc);\n'),
    'pad': ('\te->size = size;\n\tif (pad && (size & 15))\n\t\te->size = (size + 15) & ~15;\n', '\te->size = size;\n\tif (pad && size & 15)\n\t\te->size = (size + 15) & ~15;\n'),
    'd': ('\t\t{\n\t\t\tuint8_t *d = xb.files[xb.nFlashFiles].data;\n\n\t\t\t__asm__("" : "+a"(d));\n\t\t\tif (d)\n\t\t\t\t*pr = extractSmcConfig(e, d, xb.files[xb.nFlashFiles].size);\n\t\t}\n', '\t\tif (xb.files[xb.nFlashFiles].data)\n\t\t\t*pr = extractSmcConfig(e, xb.files[xb.nFlashFiles].data, xb.files[xb.nFlashFiles].size);\n'),
}


def CASES(base):
    return [(k, base.replace(*v)) for k, v in OPS.items()]

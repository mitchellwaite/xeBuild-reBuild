"""Landed shapes reviewed one by one: do any still pay?  blMagic, crcSame, the case 24 double calls, `int size`, `int crc`, findSmcConfig's pos, and the types of checkBl's helpers."""
BM_DEF = '''static void blMagic(const uint8_t *bl, int *m)
{
	*m = bl[0];
}
'''
C24A = '''			if (loadBaseFile(e->name, e))
				*pr = defaultBl60(e);
			else if (e->size != 0x60)
				*pr = defaultBl60(e);
'''
C24B = '''			*pr = 0;
			if (loadBaseFile(e->name, e) || e->size != 0x60)
				*pr = defaultBl60(e);
'''
C24C = '''				if (loadBaseFile(e->name, e))
					r = defaultBl60(e);
				else if (e->size != 0x60)
					r = defaultBl60(e);
'''


def CASES(base):
    out = [
        ('case24 first with ||', base.replace(C24A, '			if (loadBaseFile(e->name, e) || e->size != 0x60)\n				*pr = defaultBl60(e);\n')),
        ('case24 second two calls', base.replace(C24B, '			*pr = 0;\n			if (loadBaseFile(e->name, e))\n				*pr = defaultBl60(e);\n			else if (e->size != 0x60)\n				*pr = defaultBl60(e);\n')),
        ('case24 second no pr0', base.replace(C24B, '			if (loadBaseFile(e->name, e))\n				*pr = defaultBl60(e);\n			else if (e->size != 0x60)\n				*pr = defaultBl60(e);\n')),
        ('case24 console ||', base.replace(C24C, '				if (loadBaseFile(e->name, e) || e->size != 0x60)\n					r = defaultBl60(e);\n')),
        ('blMagic ret', base.replace(BM_DEF, 'static int blMagic(const uint8_t *bl)\n{\n	return bl[0];\n}\n').replace('blMagic(bl, &m);', 'm = blMagic(bl);')),
        ('blMagic gone', base.replace('	blMagic(bl, &m);\n', '	m = bl[0];\n').replace(BM_DEF, '')),
        ('crcSame gone in 14', base.replace('		if (!crcSame(c, crc))\n			goto bad;\n', '		if (c != crc)\n			goto bad;\n')),
        ('toobig nest', None),
    ]
    return [x for x in out if x[1] is not None]

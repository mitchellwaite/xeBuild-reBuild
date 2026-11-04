# attempt 15: gen_iw218's block-offset places on the `small` family (build/iw/a15/s2n.c), plus more places and forms of the use.
import os, importlib.util
here = os.path.dirname(os.path.abspath(__file__))
sp = importlib.util.spec_from_file_location('g218', os.path.join(here, 'gen_iw218.py')); g = importlib.util.module_from_spec(sp); sp.loader.exec_module(g)
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_a15.c')
USE = g.USE
FOR = g.FOR
SS = '			s = xb.spare + (pg + p + b * 32) * 16;\n'
P = list(g.PLACES)
NEW = g.NEW
for lab, a, b, v in [
 ('ss', SS, SS + '			{ uint32_t bo = off & 0x1ffff;\n', None),
]:
    pass
P += [('forv', [(FOR, FOR + '			uint32_t bo;\n\n'), ('			pg = start * 32;\n', '			bo = off & 0x1ffff;\n			pg = start * 32;\n'), (USE, NEW.replace('V', 'bo'))]),
      ('forw', [(FOR, FOR + '			uint32_t bo;\n\n'), (SS, SS + '			bo = off & 0x1ffff;\n'), (USE, NEW.replace('V', 'bo'))]),
      ('forx', [(FOR, FOR + '			uint32_t bo;\n\n'), ('			memset(s, 0, 16);\n', '			memset(s, 0, 16);\n			bo = off & 0x1ffff;\n'), (USE, NEW.replace('V', 'bo'))]),
      ('big', [(FOR, FOR + '			uint32_t bo;\n\n'), ('			if (xb.bigBlock) {\n				((struct spb *)s)->b2lo', '			if (xb.bigBlock) {\n				bo = off & 0x1ffff;\n				((struct spb *)s)->b2lo'), (USE, NEW.replace('V', 'bo'))]),
      ('bt', [(FOR, FOR + '			uint32_t bo;\n\n'), ('				if (type > 1) {\n					((struct spt *)s)->type = type;\n					if (type != 0x2a', '				if (type > 1) {\n					bo = off & 0x1ffff;\n					((struct spt *)s)->type = type;\n					if (type != 0x2a'), (USE, NEW.replace('V', 'bo'))]),
      ('xp', [('		t = type - \'1\';\n', '		t = type - \'1\';\n		pg = off & 0x1ffff;\n'), ('			pg = start * 32;\n', '			uint32_t pp = start * 32;\n'), ('(pg + p + b * 32) * 16', '(pp + p + b * 32) * 16'), (USE, NEW.replace('V', 'pg'))]),
      ]
TL = [('', []), ('tb', [('	setBeU16(off >> 14, (uint8_t *)&xb.fsBlock);\n', '	setBeU16(blk, (uint8_t *)&xb.fsBlock);\n')])]
AXES = [P, TL]
FLAGS = []

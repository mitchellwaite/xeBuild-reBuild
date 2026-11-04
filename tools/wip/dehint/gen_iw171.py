# attempt 10: pin_hdr gone.  gen_iw170: the byte test through an if-shaped helper flips (A) with no expect.  `us` (`if (b != 0xff) return 1; return 0;`): pageErased right, blockEccOk 18,
# finalizeImage 61 with hdr/spare swapped.  `vs` (`if (b == 0xff) return 0; return 1;`): hdr/spare right (!), left: stack slots and the last bytes' layout, finalizeImage 34, pageErased 36.
# Here: the helper's parameter, shape and call, spare loop only.
import os
PIN = '			__asm__("" :: "a"(xb.hdr));\n'
HEAD = 'int pageErased(const uint8_t *data, const uint8_t *spare)\n{\n'
FLAG = '		if (spare[i] != 0xff)\n			return 0;\n	return 1;\n}\n\nint blockErased'
TY = {'u8': ('uint8_t b', 'b', 'spare[i]'), 'int': ('int b', 'b', 'spare[i]'), 'uns': ('unsigned b', 'b', 'spare[i]'),
      'ptr': ('const uint8_t *p', '*p', 'spare + i'), 'adr': ('const uint8_t *p', '*p', '&spare[i]'), 'idx': ('const uint8_t *p, int n', 'p[n]', 'spare, i')}
SH = {
 'u': ('byteUsed', 'if (%s != 0xff)\n		return 1;\n	return 0;\n', '%s'),
 'v': ('byteUsed', 'if (%s == 0xff)\n		return 0;\n	return 1;\n', '%s'),
 'n': ('byteErased', 'if (%s != 0xff)\n		return 0;\n	return 1;\n', '!%s'),
 'e': ('byteErased', 'if (%s == 0xff)\n		return 1;\n	return 0;\n', '!%s'),
 'U': ('byteUsed', 'int r = 0;\n\n	if (%s != 0xff)\n		r = 1;\n	return r;\n', '%s'),
 'V': ('byteUsed', 'int r = 1;\n\n	if (%s == 0xff)\n		r = 0;\n	return r;\n', '%s'),
 'N': ('byteErased', 'int r = 1;\n\n	if (%s != 0xff)\n		r = 0;\n	return r;\n', '!%s'),
 'E': ('byteErased', 'int r = 0;\n\n	if (%s == 0xff)\n		r = 1;\n	return r;\n', '!%s'),
 'W': ('byteUsed', 'int r;\n\n	if (%s != 0xff)\n		r = 1;\n	else\n		r = 0;\n	return r;\n', '%s'),
 'X': ('byteUsed', 'int r;\n\n	if (%s == 0xff)\n		r = 0;\n	else\n		r = 1;\n	return r;\n', '%s'),
}
V = []
for t, (par, ex, arg) in TY.items():
    for s, (nm, body, call) in SH.items():
        h = 'static int %s(%s)\n{\n	%s}\n\n' % (nm, par, body % ex)
        c = call % ('%s(%s)' % (nm, arg))
        V.append((t + s, [(HEAD, h + HEAD), (FLAG, FLAG.replace('spare[i] != 0xff', c))]))
AXES = [
 [('nopin', [(PIN, '')])],
 V,
]
BASE = os.environ.get('IWB', 'src/image_write.c')
FLAGS = []

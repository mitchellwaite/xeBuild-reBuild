# attempt 5: only imgFits' if form + imgAddMobile's `if (imgFits) {...; return ret;}` on the landed source: exp_mob gone, imgAddFile as landed
import os
import gen_iw70 as G70
import gen_iw69 as G69
BASE = 'src/image_write.c'
OLD_MOB_S = G70.SMALLA.replace('if (imgFits(off, len)) {', 'if (__builtin_expect(imgFits(off, len), 1)) {')
AXES = [
 [(k, [(G69.FITS, 'int imgFits(uint32_t off, uint32_t len)\n{\n	' + v + '}\n')]) for k, v in G69.FORMS.items() if k in ('if1', 'else1', 'r0', 'lim1', 'if0', 'lim0')],
 [(k, [(G70.BIGA, v)]) for k, v in G70.BIG.items()],
 [(k, [(OLD_MOB_S, v)]) for k, v in G70.SMALL.items()],
]

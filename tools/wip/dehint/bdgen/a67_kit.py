"""Attempt 67: the tail's kit arm through a helper (the >5 side's first block a call at profile_estimate
if it isn't einlined, PRED_CALL on the tail test X).
python tools/wip/dehint/bdgen/a62_semeas.py tools/wip/dehint/bdgen/a67_kit.py -x -p 0   (and -x -p 99, -p 0)
python tools/wip/dehint/bdgen/a60lib.py tools/wip/dehint/bdgen/a67_kit.py -p 0 -o "-;exp_pr" """
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a63_misc import T4, T5
from a66_h import helper

OLD = T4 + 'if (type == 14)\n' + T5 + 'setFlashBuild(getBeU16(xb.files[i].data + 2));\n'
K1 = ('/* an SE in a kit build sets the flash build number */\n'
      'static void setKitBuild(struct fileent *e, int type)\n{\n'
      '\tif (type == 14)\n\t\tsetFlashBuild(getBeU16(e->data + 2));\n}\n')
K2 = ('/* an SE in a kit build sets the flash build number */\n'
      'static void setKitBuild(int type, const uint8_t *bl)\n{\n'
      '\tif (type == 14)\n\t\tsetFlashBuild(getBeU16(bl + 2));\n}\n')
K3 = ('/* an SE in a kit build sets the flash build number */\n'
      'static void setKitBuild(int type, uint32_t i)\n{\n'
      '\tif (type == 14)\n\t\tsetFlashBuild(getBeU16(xb.files[i].data + 2));\n}\n')
K4 = ('/* an SE sets the flash build number */\n'
      'static void seBuild(const struct fileent *e)\n{\n'
      '\tif (e->type == 14)\n\t\tsetFlashBuild(getBeU16(e->data + 2));\n}\n')
V = {
    'src': [],
    'k1': [helper(K1), (OLD, T4 + 'setKitBuild(e, type);\n')],
    'k2': [helper(K2), (OLD, T4 + 'setKitBuild(type, xb.files[i].data);\n')],
    'k3': [helper(K3), (OLD, T4 + 'setKitBuild(type, i);\n')],
    'k4': [helper(K4), (OLD, T4 + 'seBuild(&xb.files[i]);\n')],
    'k4e': [helper(K4), (OLD, T4 + 'seBuild(e);\n')],
}
NOPR = ('if (__builtin_expect(r != 0, 0))', 'if (r != 0)')
NEG = ('if (__builtin_expect(r != 0, 0))', 'if ((int)r < 0)')
for k in ('k1', 'k3'):
    V[k + '_r'] = V[k] + [NOPR]
    V[k + '_n'] = V[k] + [NEG]

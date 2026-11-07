"""Attempt 64: forms of loadBlFiles' signature region where the no-key log block is not
dominated by a single pub1bl test (or has no call in its first block), with the key in a
local so vrp1 can thread a second test away.  Chain first, then scores:
python tools/wip/dehint/bdgen/a62_semeas.py tools/wip/dehint/bdgen/a64_nk.py [-x] -p 99
python tools/wip/dehint/bdgen/a60lib.py tools/wip/dehint/bdgen/a64_nk.py -p 99 -o "-;exp_pr" """
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a63_misc import T4, T5, T6, T7, FAILLOG, PASSLOG, NOKEYLOG, BODY

def wrap(inner):
    return T5 + '{\n' + T6 + 'const uint8_t *key = xb.pub1bl;\n\n' + inner + T5 + '}\n'

V = {
    'src': [],
    # ver_flat with a local key (second test threadable)
    'flat_local': [(BODY, wrap(T6 + 'if (key && !cbVerifySig(e->data, key)) {\n' + T7 + FAILLOG + T7 + 'r = -1;\n'
                  + T6 + '} else if (key)\n' + T7 + PASSLOG + T6 + 'else\n' + T7 + NOKEYLOG))],
    # passed first with a local key
    'flat_local2': [(BODY, wrap(T6 + 'if (key && cbVerifySig(e->data, key))\n' + T7 + PASSLOG
                  + T6 + 'else if (key) {\n' + T7 + FAILLOG + T7 + 'r = -1;\n' + T6 + '} else\n' + T7 + NOKEYLOG))],
    # ver_flat with xb.pub1bl but no-key test first? (single test) -- variants with !key
    'flat_local3': [(BODY, wrap(T6 + 'if (!key)\n' + T7 + NOKEYLOG + T6 + 'else if (!cbVerifySig(e->data, key)) {\n'
                  + T7 + FAILLOG + T7 + 'r = -1;\n' + T6 + '} else\n' + T7 + PASSLOG))],
    # r as the result: r = -1 when verify fails, tested for the log
    'r_res': [(BODY, T5 + 'if (xb.pub1bl) {\n' + T6 + 'if (!cbVerifySig(e->data, xb.pub1bl))\n' + T7 + 'r = -1;\n'
               + T6 + 'if (r)\n' + T7 + FAILLOG + T6 + 'else\n' + T7 + PASSLOG + T5 + '} else\n' + T6 + NOKEYLOG)],
    # flat with xb.pub1bl and local flat: key test inside (key ? verify : ...)
    'flat_xb_ok': [(BODY, T5 + 'if (!xb.pub1bl)\n' + T6 + NOKEYLOG + T5 + 'else if (cbVerifySig(e->data, xb.pub1bl))\n'
               + T6 + PASSLOG + T5 + 'else {\n' + T6 + FAILLOG + T6 + 'r = -1;\n' + T5 + '}\n')],
}

# opcode heuristics on the HDD bit tests (== nonzero constant -> NONEQUAL predicts the error arm)
T = 'if (cinfo->hwFlags & 0x20)'
def both(n):
    return [(T, n), (T, n)]
VARS = [
 ('eq20', both('if ((cinfo->hwFlags & 0x20) == 0x20)')),
 ('eq20A', [(T, 'if ((cinfo->hwFlags & 0x20) == 0x20)')]),
 ('ne0x', both('if ((cinfo->hwFlags & 0x20) != 0)')),
 ('sgn', both('if ((int)(cinfo->hwFlags << 26) < 0)')),
 ('gt0', both('if ((int)(cinfo->hwFlags & 0x20) > 0)')),
 ('sh', both('if (((cinfo->hwFlags >> 5) & 1) == 1)')),
 ('ge20', both('if ((cinfo->hwFlags & 0x20) >= 0x20)')),
]

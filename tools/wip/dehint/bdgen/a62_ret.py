"""Attempt 62: checkBl's return type and its `r` local's type, for exp_pr's SE chain (a61_semeas.py first,
then a60lib.py to score).  python tools/wip/dehint/bdgen/a61_semeas.py tools/wip/dehint/bdgen/a62_ret.py"""
HDR = 'int checkBl(uint8_t *bl, uint32_t size, int type, uint32_t crc)\n{\n\tuint32_t blsize, c = 0;\n\tint m, r = 0;\n'
def ret(rt, lt=None):
    new = HDR.replace('int checkBl', rt + ' checkBl', 1)
    if lt:
        new = new.replace('\tint m, r = 0;\n', '\tint m;\n\t%s r = 0;\n' % lt)
    return [(HDR, new)]
V = {
    'long': ret('long'),
    'long_l': ret('long', 'long'),
    'ulong': ret('unsigned long'),
    'u32_u32': ret('uint32_t', 'uint32_t'),
    'i32': ret('int32_t'),
    'ssize': ret('ssize_t'),
}
V['static'] = [(HDR, 'static ' + HDR)]

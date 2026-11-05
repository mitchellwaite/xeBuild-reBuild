"""addBlsToImage: exp_t24 kept imgSize()'s call out of the block right after type == 25.  A test on xb.type there, redundant but folded only after branch prediction, does the same."""

OLD = 'type == 25 && __builtin_expect(type != 24, 1) && e->offset < imgSize()'
T = {
    'le5': 'type == 25 && xb.type <= BUILD_DEVGL16 && e->offset < imgSize()',
    'ret': 'type == 25 && xb.type != BUILD_RETAIL && e->offset < imgSize()',
    'jtag': 'type == 25 && xb.type != BUILD_JTAG && e->offset < imgSize()',
    'le5a': 'xb.type <= BUILD_DEVGL16 && type == 25 && e->offset < imgSize()',
    'reta': 'xb.type != BUILD_RETAIL && type == 25 && e->offset < imgSize()',
    'jtaga': 'xb.type != BUILD_JTAG && type == 25 && e->offset < imgSize()',
    'gl': 'type == 25 && !xb.fromConsole && e->offset < imgSize()',
    'off': 'type == 25 && e->offset != 0xffffffff && e->offset < imgSize()',
}


def CASES(base):
    return [(k, base.replace(OLD, v)) for k, v in T.items()]

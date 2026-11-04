# attempt 24, pin_t: rescale by as little as possible. U4 (hottest 11955, F 753) gets t's slot right in imgAdd but moves registers in all three clones; below the rescale point (U3) the clones are clean. The `type == '0'` path of the small arm is 931, so n = 10 gives 10241 and F 879, r = 1.024. s[2]'s store goes in both arms to have something for the table.
# `IWB=build/iw/a24/np.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw308.py -n 12 -t 4`
T5 = '\t' * 5
T6 = '\t' * 6
O = T5 + "s[2] = 1;\n" + T5 + "if (type != '0') {\n" + T6 + "s[8] = len >> 8;\n" + T6 + "s[7] = len;\n" + T5 + "}\n"
def f(n):
    return (T5 + "if (type != '0') {\n" + T6 + "s[2] = 1;\n" + T6 + "s[8] = len >> 8;\n" + T6 + "s[7] = len;\n" + T5 + "} else {\n"
        + T6 + 'int part[%d] = { 1 };\n' % n + T6 + 'int sum = 0, j;\n\n' + T6 + 'for (j = 0; j < %d; j++)\n' % n + T6 + '\tsum += part[j];\n' + T6 + 's[2] = sum;\n' + T5 + '}\n')
AXES = [[(('n%d' % n), [(O, f(n))]) for n in (2, 9, 10, 11, 12, 13, 14)]]

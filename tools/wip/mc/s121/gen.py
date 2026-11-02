import sys
S = open(sys.argv[1]).read()
NL = chr(10); TB = chr(9)
FA = 'block); }' + NL + TB*2 + '} else' + NL + TB*3 + '{ eout:'
EO = 'if (__builtin_constant_p(block+5)) goto einv; JUMP(efail); }'
ER = 'eerase: if (__builtin_constant_p(block + 77)) goto einv;'
ES = 'if (__builtin_constant_p(block+9)) goto eout; }'
IV = 'einv: __attribute__((cold)); '
for x in (FA, EO, ER, ES, IV):
    assert S.count(x) == 1, x
V = {}
labs = ['einv', 'eout', 'esucc', 'eerase', 'efail2']
S2 = S.replace('eout; }' + NL + TB*3 + 'else' + NL + TB*4 + '{ AT(efail) log_printf',
               'eout; }' + NL + TB*3 + 'else' + NL + TB*4 + '{ efail2: log_printf')
assert S2 != S
D = 'if (__builtin_constant_p(block+%d)) goto %s;'
sites = {
    'fa': (FA, FA.replace('block); }', 'block); ' + D + ' }')),
    'eo': (EO, EO.replace('JUMP(efail); }', D + ' }')),
    'er': (ER, ER + ' ' + D),
    'es': (ES, ES.replace('goto eout; }', 'goto eout; ' + D + ' }')),
    'iv': (IV, IV + D + ' '),
}
k = 300
for sn, (a, b) in sites.items():
    for l in labs:
        k += 1
        V['g_%s_%s' % (sn, l)] = S2.replace(a, b % (k, l))
AV = '__asm__ volatile("");'
V['av_fa'] = S.replace(FA, FA.replace('block); }', 'block); ' + AV + ' }'))
V['av_eo'] = S.replace(EO, EO.replace('JUMP(efail); }', AV + ' }'))
V['av_er'] = S.replace(ER, ER + ' ' + AV)
V['ab_er'] = S.replace(ER, 'eerase: ' + AV + ER[7:])
V['av_es'] = S.replace(ES, ES.replace('goto eout; }', 'goto eout; ' + AV + ' }'))
V['av_iv'] = S.replace(IV, IV + AV + ' ')
V['ab_es'] = S.replace('esucc:  log_printf', 'esucc: ' + AV + ' log_printf')
V['ab_fa'] = S.replace('{ AT(efail) log_printf(0, "' + chr(92) + 'n' + chr(92) + 'n***** ERROR: Failed to erase block 0x%x!' + chr(92) + 'n", block); }' + NL + TB*2 + '} else' + NL + TB*3 + '{ eout:',
                       '{ AT(efail) ' + AV + ' log_printf(0, "' + chr(92) + 'n' + chr(92) + 'n***** ERROR: Failed to erase block 0x%x!' + chr(92) + 'n", block); }' + NL + TB*2 + '} else' + NL + TB*3 + '{ eout:')
V['ab_eo'] = S.replace('{ eout: log_printf', '{ eout: ' + AV + ' log_printf')
for n, t in V.items():
    assert t != S, n
    open(sys.argv[2]+'/%s.c' % n, 'w', newline=NL).write(t)
print(len(V))

"""Attempt 3: every hint off alone, against every integer type of every parameter and local of its function.
(Attempt 2's sweeps turned all of a function's hints off at once.)"""
from bdone import retype, vars_of, INTS

BY_FN = {
    'int loadFileCrc(': ['exp_verbose', 'pin_e'],
    'uint32_t patchSmcConfig(': ['nei_smc', 'cb1', 'cb2', 'cb3', 'cb4'],
    'int extractSmcConfig(': ['exp_200', 'pin_i', 'exp_210', 'exp_400', 'pin_src', 'lab_nf1', 'lab_nf2', 'lab_nf1,lab_nf2'],
    'int checkBl(': ['nei_chk', 'pin_type', 'lab_size', 'cb5', 'pin_m', 'crc5'],
    'static void loadBl(': ['exp_t10', 'lab_t5le', 'exp_pr', 'lab_t5le,exp_pr', 'lab_badsize', 'exp_27', 'pin_d', 'vol_fail'],
    'int loadConsoleBlFiles(': ['exp_t9', 'lab_none'],
    'int loadBlFiles(': ['exp_t10', 'lab_t5le', 'exp_pr', 'lab_badsize', 'exp_27', 'pin_d', 'vol_fail'],
    'void patchBlsBlmod(': ['nei_blmod'],
    'void addBlsToImage(': ['exp_t24'],
    'int isUpdateBl(': ['exp_upd'],
    'void addUpdateBls(': ['exp_upd'],
    'uint32_t calcBlAreaSize(': ['pin_size'],
    'int buildFlash(': ['exp_devgl'],
}


def CASES(base):
    out = []
    for head, offs in BY_FN.items():
        for name, ty in vars_of(base, head):
            for new in INTS:
                if new != ty:
                    for off in offs:
                        out.append((off, '%s %s %s' % (head.split('(')[0].split()[-1], name, new), retype(head, name, new)))
    return out

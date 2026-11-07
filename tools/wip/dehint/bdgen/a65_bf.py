"""Attempt 65: buildFlash restructured into / out of helpers (whole-function level), each with the devgl
expect kept and off.
python tools/wip/dehint/bdgen/a60lib.py tools/wip/dehint/bdgen/a65_bf.py -p 99 -o "-;exp_devgl" [-f label]
C text is written with 4 spaces per tab level (converted by T)."""


def T(s):
    return s.replace('    ', '\t')


BF = 'int buildFlash(void)\n{\n'


def helper(code):
    """insert static helpers just before buildFlash"""
    return (BF, T(code) + '\n' + BF)


def E(old, new):
    return (T(old), T(new))


FUSE = r'''    fuse = 1;
    if (xb.type != BUILD_JTAG) {
        fuse = xb.glitch2mfg != 0;
        if (__builtin_expect(xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16, 0))
            fuse = 1;
    }
'''
HDR_OLD = r'''    if (!xb.fromConsole) {
        log_printf(1, "Writing initial header to flash image\n");
        writeInitialHeader();
    } else {
        log_printf(1, "\n------ Copying bootloader image to flash image ------ \n");
        r = checkBootImage(1);
        if (r) {
            log_printf(0, "******* ERROR: bootloaders retrieved from console are inconsistent, cannot proceed!\n\n");
            return r;
        }
    }
'''
HDR_FN = r'''/* the initial flash header, or the console's bootloaders checked */
static int initImage(void)
{
    int r;

    if (!xb.fromConsole) {
        log_printf(1, "Writing initial header to flash image\n");
        writeInitialHeader();
        return 0;
    }
    log_printf(1, "\n------ Copying bootloader image to flash image ------ \n");
    r = checkBootImage(1);
    if (r)
        log_printf(0, "******* ERROR: bootloaders retrieved from console are inconsistent, cannot proceed!\n\n");
    return r;
}
'''
HDR_NEW = r'''    r = initImage();
    if (r)
        return r;
'''
LD_OLD = r'''    suLoadDir(xb.dataDir);
    log_printf(1, "\n------ Loading bootloaders and required security files ------\n");
    if (xb.fromConsole)
        r = loadConsoleBlFiles();
    else
        r = loadBlFiles();
    if (r) {
        log_printf(0, "******* ERROR: critical bootloader files are missing, cannot proceed!\n\n");
        return r;
    }
    if (!xb.fromConsole && !verifyBlSigs())
        return 1;
    log_printf(1, "done!\n");
'''
LD_FN = ('/* the bootloaders and security files */\nstatic int loadFlashFiles(void)\n{\n    int r;\n\n' +
         LD_OLD + '    return 0;\n}\n')
LD_NEW = r'''    r = loadFlashFiles();
    if (r)
        return r;
'''
FZ_OLD = r'''    if (fuse) {
        struct fileent *e = &xb.files[findFile(24)];
        setFuseCpuKey(e->data);
        if (xb.type != BUILD_JTAG)
            e->offset = imgCfOffset() + imgCfSize();
    }
'''
FZ_FN = r'''/* the virtual fuses' CPU key, and their place after the CF */
static void setVfuses(void)
{
    struct fileent *e = &xb.files[findFile(24)];

    setFuseCpuKey(e->data);
    if (xb.type != BUILD_JTAG)
        e->offset = imgCfOffset() + imgCfSize();
}
'''
FZ_NEW = '    if (fuse)\n        setVfuses();\n'
GL_OLD = r'''        if (xb.fromConsole)
            fixupPatchSet();
        else {
            struct fileent f;

            memset(&f, 0, sizeof(f));
            if (!loadBaseFile("blmod.bin", &f)) {
                patchBlsBlmod(f.data, f.size);
                free(f.data);
            } else
                patchConsoleBlmod();
        }
'''
GL_FN = r'''/* blmod.bin if there is one, else the console's */
static void patchBlmod(void)
{
    struct fileent f;

    memset(&f, 0, sizeof(f));
    if (!loadBaseFile("blmod.bin", &f)) {
        patchBlsBlmod(f.data, f.size);
        free(f.data);
    } else
        patchConsoleBlmod();
}
'''
GL_NEW = r'''        if (xb.fromConsole)
            fixupPatchSet();
        else
            patchBlmod();
'''
ENC_OLD = r'''    if (!xb.fromConsole) {
        if (encodeBls(salt, blocks))
            return -4;
    } else if (encodeUpdateBls((int)salt, blocks))
        return -4;
'''
ENC_FN = r'''static int encodeFlashBls(uint8_t *salt, int blocks)
{
    if (!xb.fromConsole)
        return encodeBls(salt, blocks);
    return encodeUpdateBls((int)salt, blocks);
}
'''
ENC_NEW = '    if (encodeFlashBls(salt, blocks))\n        return -4;\n'

# the fuse decision and the header in one setup helper, the flag returned through a pointer
SETUP_FN = ('static int initFlash(int *fuse)\n{\n    int r;\n\n' + FUSE.replace('fuse =', '*fuse =') +
            HDR_OLD + '    return 0;\n}\n')
SETUP_NEW = '    r = initFlash(&fuse);\n    if (r)\n        return r;\n'
# the same returning the fuse flag, r through a pointer
SETUP2_FN = ('static int initFlash(int *pr)\n{\n    int fuse, r;\n\n' + FUSE +
             HDR_OLD.replace('            return r;\n', '            *pr = r;\n            return fuse;\n') +
             '    *pr = 0;\n    return fuse;\n}\n')
SETUP2_NEW = '    fuse = initFlash(&r);\n    if (r)\n        return r;\n'


def ovf(t):
    """the three patch slot overflow writers through one helper"""
    fn = T(r'''/* a CG patch slot's overflow, as a file in the filesystem */
static void addSlotOverflow(const char *msg, const char *name, int cf, int cg, uint32_t off)
{
    uint32_t ts;

    log_printf(1, msg);
    log_printf(1, "\tat raw offset 0x%x len 0x%08x (end: 0x%08x)...", off, xb.files[cf].fsSize, off + xb.files[cf].fsSize);
    makeTimestamp((uint8_t *)&ts, NULL);
    imgAddFile(name, xb.files[cg].data + xb.files[cf].fsOffset, &ts, xb.files[cf].fsSize);
    log_printf(1, "done!\n");
}
''')
    t = t.replace(BF, fn + '\n' + BF, 1)
    import re
    pat = re.compile(r'(\t+)cf = findFile\((\d+)\);\n\t+cg = findFile\((\d+)\);\n\t+log_printf\(1, ("[^"]*")\);\n'
                     r'\t+log_printf\(1, "\\tat raw[^\n]*\n\t+makeTimestamp[^\n]*\n\t+imgAddFile\(("[^"]*")[^\n]*\n'
                     r'\t+log_printf\(1, "done!\\n"\);\n')
    t, n = pat.subn(lambda m: '%saddSlotOverflow(%s, %s, findFile(%s), findFile(%s), off);\n'
                    % (m.group(1), m.group(4), m.group(5), m.group(2), m.group(3)), t)
    if n != 3:
        raise ValueError('ovf: %d sites' % n)
    return t


V = {
    'src': [],
    'ovf': ovf,
    'hdr': [helper(HDR_FN), E(HDR_OLD, HDR_NEW)],
    'ld': [helper(LD_FN), E(LD_OLD, LD_NEW)],
    'hdr_ld': [helper(HDR_FN + '\n' + LD_FN), E(HDR_OLD, HDR_NEW), E(LD_OLD, LD_NEW)],
    'fz': [helper(FZ_FN), E(FZ_OLD, FZ_NEW)],
    'blmod': [helper(GL_FN), E(GL_OLD, GL_NEW)],
    'enc': [helper(ENC_FN), E(ENC_OLD, ENC_NEW)],
    'setup_ptr': [helper(SETUP_FN), E(FUSE + HDR_OLD, SETUP_NEW)],
    'setup_ret': [helper(SETUP2_FN), E(FUSE + HDR_OLD, SETUP2_NEW)],
}

"""Split the whole-image source into one .s per original object file.

python re/split.py <xeBuild.exe> <build/xeBuild.lines.json> <src_dir>

Writes <src_dir>/<group>/<name>.s for every object, <src_dir>/objects.txt (link
order) and prints the data-assignment summary.  Objects that have a C source
(<src_dir>/<group>/<name>.c) get no .s; functions they share with the .s files
are named by SYMBOLS.  Mixed objects, with some functions in C (C_FUNCS), get
both: the .s keeps everything else and marks where each C function goes.  How
the pieces are found:

  .text      exact: every gcc object has its own CIE in .eh_frame, in link
             order, and its FDEs list its functions (units.py).  Objects
             without unwind info (chkstk, import stubs) are known runtime
             matches.  .text.startup holds main (unit 10), unit 21's startup
             function and crtend's constructor, then the link script's
             ctor/dtor lists.
  .eh_frame  exact: one CIE + FDEs per object.
  .rdata$zzz exact count: one `GCC: ...` ident per gcc-compiled object (104;
             identical bytes, so which object carries which is immaterial).
  .data .rdata .bss
             inferred: split at labels into atoms, find which objects reference
             each atom (code refs, propagated through data-to-data pointers),
             then choose monotone boundaries in link order minimising atoms
             placed in an object that doesn't reference them.
  COMMON     the end of .bss is uninitialized (common) globals, which ld lays
             out in hash-table order, so it stays one file (common_bss.s).
"""
import bisect, collections, json, os, re, sys

sys.path.insert(0, os.path.dirname(__file__))
from ddfix import Image
from units import units

# unit index (CIE order) -> (path, evidence)
NAMES = {
    0: ('runtime/crt2', 'mingw-w64 crt2.o, byte match'),
    1: ('runtime/crtbegin', 'gcc crtbegin.o, byte match'),
    2: ('app/bootloaders', 'CB/CF/CD/CE decryption, pairing, FCRT, bootloader signature checks'),
    3: ('app/mode_update', '"Usage: %s update", bad block handling'),
    4: ('app/stfs', 'container header/content/manifest hash checks, STFS file listing'),
    5: ('app/mode_client', '"Usage: %s client", network read/write of NAND'),
    6: ('app/filelist_ini', '"parsing ini at", file list ini labels'),
    7: ('app/timeutil', 'gmtime/mktime/rand, date arithmetic constants'),
    8: ('app/smc', 'SMC checksum, type detection, reset-limit/eject/blink patches'),
    9: ('app/sysupdate', 'system update container, xboxupd.bin extraction'),
    10: ('app/main', 'main (.text.startup), signal handlers, mode dispatch'),
    11: ('app/mode_extract', '"Usage: %s extract"'),
    12: ('app/xboxrom', 'XBOX_ROM_B/4/3 names'),
    13: ('app/image_write', 'flash layout (CB/CE/SMC/Mobile*.dat), writing image to disk'),
    14: ('app/keyvault', 'keyvault hash check, DVD key, console serial/date formatting'),
    15: ('app/image_read', 'parsing an existing NAND image: sectors, pairing, LDV, smc.bin'),
    16: ('app/mode_ini', '"Usage: %s ini"'),
    17: ('app/mode_build', 'default build mode usage and switches (-t/-c/-d/-b/-p)'),
    18: ('app/keys', 'CPU/1BL key setup, SMC/keyvault/CRL input decryption, pairing init'),
    19: ('app/net', 'winsock: beacon, send/recv'),
    20: ('app/fileutil', 'file read/write/dump helpers, mkdir; called by almost every unit'),
    21: ('app/options', 'console types (xenon...corona), command line options; startup fn'),
    22: ('app/build', 'image build: reading inputs with crc32 checks, patches, payloads'),
    23: ('app/consoleinfo', 'options/launch ini writing, console info response parsing'),
    24: ('app/console_hdd', 'manifest + avatar/kinect data to console HDD, remote dirs'),
    25: ('app/log', 'build.log, verbose levels; called by every app unit'),
    26: ('app/crc32', "table-driven crc32; Gary S. Brown's (per xeBuild's docs), byte match from C"),
    27: ('crypto/xecrypt', 'XeCrypt-style API: SHA/HMAC (0x36/0x5c pads), RC4, DES, AES, RSA'),
    28: ('crypto/xecryptBn', 'big-endian qword bignum helpers, Montgomery inverse (XeCrypt xecryptBn.c)'),
    29: ('crypto/aes/aes_modes', 'Gladman AES: ECB/CBC over the block functions'),
    30: ('crypto/aes/aestab', 'Gladman AES: aes_init() returning 0, and the tables'),
    31: ('crypto/aes/aescrypt', 'Gladman AES: block encrypt/decrypt'),
    32: ('crypto/aes/aeskey', 'Gladman AES: key schedules for 128/192/256'),
    33: ('crypto/bign/mpSubtract', 'assert path .../XeCrypt/bign/mpSubtract.c'),
    34: ('crypto/bign/pkcs1-rsa', 'RSA key generation, PKCS#1 v1.5/OAEP/PSS (XeCrypt bign/pkcs1-rsa.c)'),
    35: ('crypto/bign/mpMultiply', 'assert path .../XeCrypt/bign/mpMultiply.c'),
    36: ('crypto/bign/mpShortMod', 'remainder of mpShortDiv'),
    37: ('crypto/bign/mpModExp', 'square-and-multiply over mpModMult'),
    38: ('crypto/bign/mpSetZero', 'memset digits'),
    39: ('crypto/bign/mpShortDiv', 'divide by one digit'),
    40: ('crypto/bign/base64', 'base64 alphabet, encode/decode'),
    41: ('crypto/bign/hash', 'hash-id size table, SHA-1 one-shot wrappers'),
    42: ('crypto/bign/mpModInv', 'extended Euclid'),
    43: ('crypto/bign/mpModulo', 'mpDivide keeping the remainder'),
    44: ('crypto/bign/mpShortSub', 'subtract one digit with borrow'),
    45: ('crypto/bign/mpSizeof', 'count significant digits'),
    46: ('crypto/bign/mpCompare', 'compare from the top digit'),
    47: ('crypto/bign/common', 'memset wrapper + two empty functions (XeCrypt bign/common.c)'),
    48: ('crypto/bign/mpSetDigit', 'set low digit, zero the rest'),
    49: ('crypto/bign/mpIsPrime', 'small-prime sieve + Rabin-Miller'),
    50: ('crypto/bign/mpIsZero', 'all digits zero'),
    51: ('crypto/bign/mpShiftLeft', 'multi-digit shift left'),
    52: ('crypto/bign/spMultiply', '32x32->64 multiply via 16-bit halves'),
    53: ('crypto/bign/mpAdd', 'assert path .../XeCrypt/bign/mpAdd.c'),
    54: ('crypto/bign/mpModMult', 'mpMultiply then mpModulo'),
    55: ('crypto/bign/bigdUtils', 'digit alloc/free, hex print, random fill, string conversion (bign/bigdUtils.c)'),
    56: ('crypto/bign/mpShortAdd', 'add one digit with carry'),
    57: ('crypto/rc4/rc4_enc', 'RC4 stream (OpenSSL RC4())'),
    58: ('crypto/rc4/rc4_skey', 'RC4 key setup; RC4_options() "rc4(idx,int)"'),
    59: ('crypto/sha/sha1dgst', 'SHA-1 init/block/update/final'),
    60: ('crypto/md5/md5', 'MD5 init/block/update/final (XeCrypt md5/md5.c)'),
    61: ('crypto/des/des', 'DES/3DES key schedule and block functions'),
    62: ('crypto/bign/mpSetEqual', 'copy digits'),
    63: ('crypto/bign/mpShiftRight', 'multi-digit shift right'),
    64: ('crypto/bign/mpDivide', 'long division (quotient, remainder)'),
    65: ('crypto/bign/spDivide', '64/32 digit division'),
    66: ('crypto/bign/mpShortCmp', 'compare with one digit'),
    67: ('crypto/bign/spPseudoRand', 'rand()-based random digit'),
    68: ('runtime/libmingw32/atonexit', 'byte match'),
    69: ('runtime/libmingw32/gccmain', 'byte match'),
    70: ('runtime/libmingw32/charmax', 'byte match; calls __lconv_init'),
    71: ('runtime/libmingw32/dllargv', '`return 0` (_setargv); 16-byte match is ambiguous'),
    72: ('runtime/libmingw32/gs_support', 'byte match'),
    73: ('runtime/libmingw32/tlssup', 'byte match'),
    74: ('runtime/libmingw32/merr', 'byte match'),
    75: ('runtime/libmingw32/CRT_fp10', 'byte match (_fpreset)'),
    76: ('runtime/libmingw32/mingw_helpers', 'byte match'),
    77: ('runtime/libmingw32/pseudo-reloc', 'byte match'),
    78: ('runtime/libmingw32/crt_handler', 'byte match'),
    79: ('runtime/libmingw32/tlsthrd', 'byte match'),
    80: ('runtime/libmingw32/pesect', 'byte match'),
    81: ('runtime/libgcc/_divdi3', 'byte match'),
    82: ('runtime/libgcc/_moddi3', 'byte match'),
    83: ('runtime/libgcc/_udivdi3', 'byte match'),
    84: ('runtime/libgcc/_umoddi3', 'byte match'),
    85: ('runtime/libmingwex/difftime32', 'byte match'),
    86: ('runtime/libmingwex/dirent', 'byte match'),
    87: ('runtime/libmingwex/wassert', 'byte match (_assert)'),
    88: ('runtime/libmingwex/_stat', 'byte match'),
    89: ('runtime/libmingwex/fseeko64', 'byte match'),
    90: ('runtime/libmingwex/ftello64', 'byte match'),
    91: ('runtime/ms_vsnprintf', '__ms_vsnprintf jump'),
    92: ('runtime/libmingwex/invalid_parameter_handler', 'get/set (xchg) of one global'),
    93: ('runtime/crtend', 'gcc crtend.o: register_frame_ctor, .jcr, eh_frame terminator'),
}
# Real names for functions and data shared with C sources (src/<obj>.c): gcc
# objects define and use these names, so the .s files must use them too
# (FUN_/L_ labels at the address).  Address -> symbol (with the leading
# underscore of i386 PE).
SYMBOLS = {
    # BigDigits (src/crypto/bign/*.c); names from XeCrypt's bign sources
    0x43e550: '_mpSubtract', 0x440e20: '_mpMultiply', 0x440f80: '_mpShortMod',
    0x440fc0: '_mpModExp', 0x4410e0: '_mpSetZero', 0x441110: '_mpShortDiv',
    0x441540: '_mpModInv', 0x441710: '_mpModulo', 0x441780: '_mpShortSub',
    0x4417d0: '_mpSizeof', 0x441800: '_mpCompare', 0x4418a0: '_mpSetDigit',
    0x441be0: '_mpIsPrimeShort', 0x441c80: '_mpIsPrimeRabin', 0x441f00: '_mpIsZero',
    0x441f40: '_mpShiftLeft', 0x442050: '_spMultiply', 0x4420b0: '_mpAdd',
    0x442130: '_mpModMult', 0x4425d0: '_mpShortAdd', 0x446200: '_mpSetEqual',
    0x446230: '_mpShiftRight', 0x446360: '_mpDivide', 0x446830: '_spDivide',
    0x446a40: '_mpShortCmp', 0x446a90: '_spPseudoRand',
    0x4421a0: '_mpMalloc', 0x4421f0: '_mpFree', 0x4423a0: '_mpMakeRandom',
    # XeCrypt (src/crypto/**/*.c); names from its sources
    # xecrypt
    0x4348f0: '_XeCryptAesCbc', 0x4348a0: '_XeCryptAesEcb', 0x434850: '_XeCryptAesKey',
    0x433e10: '_XeCryptBnQw_SwapDwQwLeBe', 0x435210: '_XeCryptBnQwBeSigCompute',
    0x435530: '_XeCryptBnQwBeSigCreate', 0x435020: '_XeCryptBnQwBeSigFormat',
    0x435440: '_XeCryptBnQwBeSigVerify', 0x435820: '_XeCryptBnQwNeRsaPrvCrypt',
    0x434090: '_XeCryptHammingWeight', 0x434110: '_XeCryptHmacSha',
    0x4346c0: '_XeCryptRandom', 0x4345b0: '_XeCryptRc4', 0x434be0: '_XeCryptRotSum',
    0x434c00: '_XeCryptRotSumSha', 0x434a30: '_XeCryptSha', 0x4349c0: '_XeCryptShaFinal',
    0x434950: '_XeCryptShaInit', 0x434960: '_XeCryptShaUpdate',
    0x433ff0: '_XeCryptUidEccEncode', 0x435b00: '_XeKeysPkcs1Verify',
    # xecryptBn
    0x436e50: '_BnQwBeBufSwap', 0x437040: '_mpGetBeQwBigNum', 0x436fe0: '_mpSetBeQwBigNum',
    0x436d80: '_XeCryptBnQw_Copy', 0x436df0: '_XeCryptBnQw_Zero',
    0x4389b0: '_XeCryptBnQwNeAdd', 0x438620: '_XeCryptBnQwNeCompare',
    0x438460: '_XeCryptBnQwNeMod', 0x4380f0: '_XeCryptBnQwNeModExp',
    0x437120: '_XeCryptBnQwNeModInv', 0x4372a0: '_XeCryptBnQwNeModMul',
    0x4382c0: '_XeCryptBnQwNeMul', 0x438860: '_XeCryptBnQwNeSub',
    0x436b00: '_XeCryptLoadQuad', 0x436e20: '_XeCryptMemcpyRev',
    0x436c50: '_XeCryptStoreQuad',
    # aes/aestab
    0x439eb0: '_aes_init',
    # aes/aescrypt
    0x43aca0: '_aes_decrypt', 0x439ec0: '_aes_encrypt',
    # aes/aeskey
    0x43e4e0: '_aes_decrypt_key', 0x43c6f0: '_aes_encrypt_key',
    # bign/pkcs1-rsa
    0x43f6b0: '_PKCS1_EME_OAEP_DEC', 0x43e870: '_PKCS1_RSA_FreeKey',
    0x43e940: '_PKCS1_RSA_GenKey',
    # bign/base64
    0x441330: '_mpBase64Decode',
    # bign/hash
    0x441400: '_GenSeed', 0x441480: '_Hash', 0x441410: '_HashLenQuery',
    # bign/common
    0x441890: '_mcrypto_dump',
    # rc4/rc4_enc
    0x442630: '_RC4',
    # rc4/rc4_skey
    0x4429d0: '_RC4_set_key',
    # sha/sha1dgst
    0x442b40: '_sha1_block', 0x444da0: '_SHA1_Final', 0x442b00: '_SHA1_Init',
    0x4448d0: '_SHA1_Update',
    # md5/md5
    0x445830: '_MD5_Final', 0x445690: '_MD5_Init', 0x4456c0: '_MD5_Update',
    # des/des
    0x445fd0: '_des_ecb_decrypt', 0x445f60: '_des_ecb_encrypt', 0x445e50: '_des_setup',
    0x4460e0: '_des3_ecb_decrypt', 0x446050: '_des3_ecb_encrypt', 0x445ea0: '_des3_setup',
    # app/crc32 (src/app/crc32.c); Gary S. Brown's crc32
    0x433800: '_crc32',
    # app/log (src/app/log.c); names are ours
    0x433570: '_log_set_verbose', 0x4335a0: '_log_verbose_flag', 0x433600: '_log_get_verbose',
    0x433610: '_log_set_name', 0x433690: '_log_printf', 0x433740: '_log_init',
    0x4337a0: '_log_finish',
    # app/filelist_ini (src/app/filelist_ini.c, mixed); names are ours
    0x40aa10: '_getIniValue', 0x4c93a4: '_iniBuf', 0x4c97ac: '_iniSize',
    0x408ec0: '_fixFileCase',       # copies the dir's casing of smc.bin/kv.bin/patches_
    0x408fe0: '_iniPreParse',       # (buf, len) -> new len; DashLaunch iniPreParse
    0x409310: '_memFindStr',        # (buf, len, str, skipNul) -> offset after str or -1
    0x4093d0: '_memFindChar',       # (buf, c, len) -> index or -1
    0x409410: '_checkFileCase',     # fixFileCase if the base dir is set
    # app/fileutil (src/app/fileutil.c); the author's names where his tools'
    # util.c has the function (cOzInABox/XeBuild tools/*/util.c), else ours
    0x420a90: '_getConsoleTypeStr', 0x420ab0: '_getBeU16', 0x420ad0: '_getBeU32',
    0x420ae0: '_getBeU64', 0x420af0: '_getLeU32', 0x420b00: '_setBeU16',
    0x420b20: '_setBeU32', 0x420b50: '_setBeU64', 0x420bb0: '_display_buffer_hex',
    0x420c30: '_dump_buffer_hex', 0x420d00: '_writeFile', 0x420d80: '_writeFileIn',
    0x420e40: '_writeKeyFile', 0x420f10: '_writeFuseFile', 0x421000: '_findInst',
    0x4210b0: '_countInst', 0x421170: '_findInstExists', 0x421200: '_replaceInst',
    0x4212d0: '_myatox', 0x421300: '_myatox8', 0x421380: '_myatox32', 0x421840: '_myatol',
    0x421860: '_myatou32', 0x421de0: '_myatoh32', 0x422350: '_validateString',
    0x4223b0: '_checkZeros', 0x4223f0: '_memcpyrev', 0x422420: '_getFileSize',
    0x422470: '_getFileSizeName', 0x4224d0: '_getFileSize64', 0x422530: '_getFileSize64Name',
    0x4225a0: '_FileExists', 0x4225d0: '_FileExistsIn', 0x422670: '_FileToBuffer',
    0x422740: '_readFileTo', 0x4227e0: '_readFileInTo', 0x4228c0: '_readFileIn',
    0x422aa0: '_calcConfigSum', 0x422ae0: '_sumBytes', 0x422b10: '_showExpectedFuses',
    0x4232e0: '_showFuses', 0x423370: '_showKey', 0x4233b0: '_showMac',
    0x423420: '_showHexPairs', 0x423490: '_writeSha1File', 0x423650: '_createDir',
    0x4236c0: '_makeBranch',
    # app/timeutil (src/app/timeutil.c); Wine's names, cdecl
    0x40b130: '_RtlTimeFieldsToTime', 0x40b330: '_RtlTimeToTimeFields',
    0x40b500: '_FileTimeToSystemTime', 0x40b700: '_SystemTimeToFileTime',
    0x40b910: '_FileTimeToDosDateTime', 0x40ba30: '_DosDateTimeToFileTime',
    0x40bae0: '_GetSystemTime',
    # app/mode_extract (src/app/mode_extract.c); names are ours
    0x40e020: '_extract_usage', 0x40e200: '_mode_extract',
    0x417680: '_loadDump', 0x414650: '_listFlashFiles', 0x411800: '_checkBootImage',
    0x44a4e0: '_separator', 0x44a524: '_promptEnter', 0x4c8fe4: '_flashFiles',
    0x4c9160: '_buildMode', 0x479f4c: '_g479f4c', 0x47a080: '_g47a080',
    0x50f318: '__imp___iob',
    # app/xboxrom (src/app/xboxrom.c); names are ours
    0x40e520: '_kvVerifySig', 0x40e5a0: '_cbVerifySig', 0x40e620: '_blVerifySig',
    0x40e690: '_blSign', 0x40e7b0: '_blCheckHash', 0x40e810: '_blUpdateHash',
    0x40e8a0: '_blHashAndSign', 0x44a540: '_romSalts',
    # app/smc (src/app/smc.c); names are ours
    0x40bd30: '_smcFindResetLimit', 0x40bd80: '_smcCheck', 0x40c020: '_smcPatch',
    0x40c210: '_smcConfigOk', 0x44a480: '_knownSmcs',
    # app/mode_ini (src/app/mode_ini.c); names are ours
    0x418240: '_ini_usage', 0x418380: '_iniSetFile', 0x4183d0: '_iniPrintf',
    0x418450: '_iniWriteFlashfs', 0x418680: '_iniWriteBl', 0x418830: '_mode_ini',
    0x40c260: '_suGetDir', 0x40cc80: '_suLoad', 0x40c650: '_suGetCF', 0x40c700: '_suGetCG',
    0x40c940: '_suFirstFile', 0x40c860: '_suNextFile', 0x40c7b0: '_suGetFile',
    # app/sysupdate (src/app/sysupdate.c); names are ours
    0x40c240: '_suGetPath', 0x40c280: '_suFreeBl', 0x40c2e0: '_suExtractBl',
    0x40ca30: '_suLoadDir', 0x401ce0: '_cfDecrypt', 0x401dc0: '_cgDecrypt',
    0x449070: '_strncat',
    0x418ee0: '_loadKeyFile', 0x41b740: '_checkKeys',
    # app/keyvault (src/app/keyvault.c); names are ours
    0x413090: '_kvGetType', 0x4130b0: '_kvIsLoaded', 0x4130c0: '_kvCheckHash',
    0x4131a0: '_kvSet', 0x413370: '_kvGetGameRegion', 0x4133d0: '_kvGetDvdKey',
    0x4133f0: '_kvGetConsoleId', 0x413410: '_kvGetSerial', 0x4134f0: '_kvGetConsoleCert',
    0x413510: '_kvGetMfgDate', 0x413590: '_kvHashIsOk', 0x4135a0: '_kvSetDvdKey',
    0x47a140: '_masterPub', 0x47a11c: '_cpuKey', 0x479ea8: '_g479ea8',
    # app/stfs (src/app/stfs.c); names are ours
    0x405610: '_stfsCheckHashes', 0x405980: '_stfsListFiles', 0x405ac0: '_stfsCheckHeader',
    0x405d50: '_stfsGetFile', 0x405f20: '_stfsInit', 0x405f50: '_stfsFree',
    0x405fa0: '_stfsLoad',
    # app/main (src/app/main.c); names are ours.  xb is the one big global
    # (main's init memsets 0x479ea0-0x4c97b0); the names above inside it
    # (g479ea8, cpuKey, masterPub, flashFiles, buildMode, iniBuf, ...) are fields
    0x40d010: '_sigHandler', 0x40d0a0: '_installSignals', 0x40d120: '_verifyFlashFile',
    0x40d370: '_logButton', 0x40d500: '_showConsoleInfo', 0x40de60: '_initGlobals',
    0x40df90: '_setBasePath', 0x4492c0: '_main', 0x479ea0: '_xb',
    0x401630: '_verifyExtended', 0x401e60: '_verifySecdata', 0x402020: '_verifyCrl',
    0x402410: '_verifyDae', 0x402720: '_verifyFcrt',
    0x41abb0: '_setCrlKey', 0x41ac00: '_setDaeKey', 0x41ac50: '_setSecdataKey',
    0x40cfa0: '_suFree', 0x40fb10: '_imageFree', 0x404770: '_mode_update',
    0x408260: '_mode_client', 0x418a10: '_build_usage', 0x419230: '_mode_build',
    # app/mode_client (wip/app/mode_client.c); names are ours
    0x406330: '_client_usage', 0x406740: '_clientInfo', 0x406980: '_clientWrite',
    0x406aa0: '_clientManifest', 0x406b60: '_dumpKey', 0x406c60: '_clientKeys',
    0x406e50: '_checkPatches', 0x407160: '_updatePatches', 0x407320: '_clientPatches',
    0x4076b0: '_clientReadBlocks', 0x407850: '_clientWriteBlocks', 0x407a00: '_patchNand',
    0x407bf0: '_clientBinPatch', 0x408080: '_clientEraseBlock', 0x408160: '_getArgs',
    0x40fbb0: '_calcPageEcc', 0x41fa40: '_netDisconnect', 0x420140: '_netReadBlocks',
    0x420200: '_netWriteBlocks', 0x420320: '_netEraseBlock', 0x420910: '_netWritePatches',
    0x46f160: '_cinfo',
    # mode_client.s strings the mixed mode_client.c refers to
    0x44e10c: '_mc_44e10c', 0x44e158: '_mc_44e158', 0x44e1a8: '_mc_44e1a8',
    0x44e1f4: '_mc_44e1f4', 0x44e234: '_mc_44e234', 0x44e273: '_mc_44e273',
    0x44e27c: '_mc_44e27c', 0x44e2a9: '_mc_44e2a9', 0x44e2b4: '_mc_44e2b4',
    0x44e2d4: '_mc_44e2d4', 0x44e305: '_mc_44e305', 0x44e314: '_mc_44e314',
    0x44e35c: '_mc_44e35c', 0x44e3c0: '_mc_44e3c0', 0x44e3f8: '_mc_44e3f8',
    0x44e434: '_mc_44e434', 0x44e4a4: '_mc_44e4a4', 0x44e4fc: '_mc_44e4fc',
    0x44e560: '_mc_44e560', 0x44e590: '_mc_44e590', 0x44e5d4: '_mc_44e5d4',
    0x44e630: '_mc_44e630', 0x44e684: '_mc_44e684', 0x44e6d8: '_mc_44e6d8',
    0x44e720: '_mc_44e720', 0x44e748: '_mc_44e748', 0x44e798: '_mc_44e798',
    0x44e7dc: '_mc_44e7dc', 0x44e814: '_mc_44e814', 0x44e850: '_mc_44e850',
    0x44e876: '_mc_44e876', 0x44e880: '_mc_44e880', 0x44e8d4: '_mc_44e8d4',
    0x44e928: '_mc_44e928', 0x44e95c: '_mc_44e95c', 0x44e9b0: '_mc_44e9b0',
    0x44e9d8: '_mc_44e9d8', 0x44ea04: '_mc_44ea04', 0x44ea50: '_mc_44ea50',
    0x44ea58: '_mc_44ea58', 0x44eaa8: '_mc_44eaa8', 0x44eaf8: '_mc_44eaf8',
    0x44eb40: '_mc_44eb40', 0x44eb8b: '_mc_44eb8b', 0x44ebc0: '_mc_44ebc0',
    0x44ebe8: '_mc_44ebe8', 0x44ec11: '_mc_44ec11', 0x44ec16: '_mc_44ec16',
    0x44ec18: '_mc_44ec18', 0x44ec35: '_mc_44ec35', 0x44ec3f: '_mc_44ec3f',
    0x44ec48: '_mc_44ec48', 0x44ec5b: '_mc_44ec5b', 0x44ec6e: '_mc_44ec6e',
    0x44ec88: '_mc_44ec88', 0x44eca4: '_mc_44eca4', 0x44ecec: '_mc_44ecec',
    0x44ed30: '_mc_44ed30', 0x44ed5c: '_mc_44ed5c', 0x44ed74: '_mc_44ed74',
    0x44ed8d: '_mc_44ed8d', 0x44eda8: '_mc_44eda8', 0x44ee04: '_mc_44ee04',
    0x44ee23: '_mc_44ee23', 0x44ee26: '_mc_44ee26', 0x44ee31: '_mc_44ee31',
    0x44ee39: '_mc_44ee39', 0x44ee45: '_mc_44ee45', 0x44ee55: '_mc_44ee55',
    0x44ee62: '_mc_44ee62', 0x44ee73: '_mc_44ee73', 0x44ee80: '_mc_44ee80',
    0x44ee94: '_mc_44ee94', 0x44eee4: '_mc_44eee4', 0x44ef10: '_mc_44ef10',
    0x44ef50: '_mc_44ef50', 0x44ef7c: '_mc_44ef7c',
    0x44efc8: '_mc_44efc8', 0x44efe8: '_mc_44efe8',
    0x44f00b: '_mc_44f00b', 0x44f014: '_mc_44f014', 0x44f037: '_mc_44f037',
    0x44f04c: '_mc_44f04c', 0x44f074: '_mc_44f074', 0x44f0b8: '_mc_44f0b8',
    0x44f0ec: '_mc_44f0ec', 0x44f118: '_mc_44f118', 0x44f140: '_mc_44f140',
    0x44f164: '_mc_44f164', 0x44f184: '_mc_44f184', 0x44f19a: '_mc_44f19a',
    0x44f1b2: '_mc_44f1b2', 0x44f1cb: '_mc_44f1cb', 0x44f1e4: '_mc_44f1e4',
    0x44f208: '_mc_44f208', 0x44f240: '_mc_44f240', 0x44f288: '_mc_44f288',
    0x44f2b0: '_mc_44f2b0', 0x44f2b8: '_mc_44f2b8', 0x44f2f0: '_mc_44f2f0',
    0x44f330: '_mc_44f330', 0x44f384: '_mc_44f384', 0x44f3f0: '_mc_44f3f0',
    0x44f434: '_mc_44f434', 0x44f464: '_mc_44f464', 0x44f494: '_mc_44f494',
    0x44f4e8: '_mc_44f4e8', 0x44f684: '_mc_44f684', 0x44f6d5: '_mc_44f6d5',
    0x44f6eb: '_mc_44f6eb', 0x44f6f8: '_mc_44f6f8', 0x44f724: '_mc_44f724',
    0x446c90: '___main',
    # app/consoleinfo (src/app/consoleinfo.c); names are ours
    0x430460: '_optOpen', 0x430540: '_optClose', 0x430570: '_optWrite',
    0x4305b0: '_optLdv', 0x4305e0: '_optHex', 0x430660: '_optButton',
    0x4308d0: '_showImageType', 0x430b60: '_getFreebootOpts',
    0x430e00: '_getFlashHdrOpts', 0x430fe0: '_showInfoKeys',
    0x4317c0: '_showCurrentInfo', 0x4318e0: '_setInfoKeys',
    0x431a60: '_parseConsoleInfo',
    0x41fd60: '_netGetFile', 0x41fe10: '_netGetInfo', 0x41ea70: '_netFree',
    0x424170: '_setConsoleType', 0x4276f0: '_findFile',
    0x41ae40: '_checkCpuKey', 0x41b120: '_setCpuKey', 0x41b600: '_set1blKey',
    0x41ade0: '_setPairing', 0x41ac70: '_setInfoKey0', 0x41aca0: '_setInfoKey1',
    0x41acd0: '_setInfoKey2', 0x41ad00: '_setInfoKey3', 0x41ad30: '_setInfoKey4',
    0x41ad60: '_setInfoKey5', 0x449180: '_fflush',
    # app/mode_build (src/app/mode_build.c) and what it calls; names are ours
    0x418fd0: '_loadPubKey', 0x419150: '_loadPubKeys',
    0x40aef0: '_loadUserIni', 0x409430: '_parseIni', 0x4259a0: '_applyIniOptions',
    0x427340: '_loadAddons', 0x4258e0: '_parseCmdOptions', 0x4271a0: '_parseRawPatches',
    0x423830: '_iniConsoleType', 0x4137f0: '_buildCleanup', 0x40f330: '_buildImage',
    0x412260: '_writeImage', 0x41afe0: '_setCpuKeyStr',
    # app/options (src/app/options.c) and what it calls; names are ours
    0x4236f0: '_baseFileExists.part.0',   # gcc's ipa-split tail of baseFileExists
    0x423730: '_baseFileExists', 0x423750: '_perboxExists',
    0x424930: '_optIniBool', 0x424a10: '_optIniInt', 0x424a70: '_parseButton',
    0x449640: '_parseButton.part.0',  # gcc's ipa-split tail of parseButton
    0x424b20: '_stripColons', 0x424b60: '_macidSet', 0x424bb0: '_setBoolOption',
    0x425110: '_parseOption', 0x427000: '_parseRawPatch', 0x427260: '_addPatch',
    0x40aad0: '_getIniBool', 0x40abf0: '_iniBoolInvalid', 0x40acf0: '_getIniU32',
    0x40ade0: '_iniU32Invalid',
    # options.s strings the mixed options.c refers to (extern names)
    0x457e3a: '_str_xenon', 0x457e40: '_msg_ctype_xenon', 0x457e61: '_str_zephyr',
    0x457e68: '_msg_ctype_zephyr', 0x457e8a: '_str_falcon', 0x457e94: '_msg_ctype_falcon',
    0x457eb6: '_str_jasper', 0x457ebd: '_str_jasperbc', 0x457ec8: '_msg_ctype_jasper',
    0x457eea: '_str_jaspersb', 0x457ef4: '_msg_ctype_jaspersb', 0x457f21: '_str_jasperbb',
    0x457f2c: '_msg_ctype_jasperbb', 0x457f58: '_str_jasper256', 0x457f62: '_str_jasper512',
    0x457f6c: '_str_trinity', 0x457f74: '_msg_ctype_trinity', 0x457f97: '_str_trinitybb',
    0x457fa4: '_msg_ctype_trinitybb', 0x457fd1: '_str_trinitybigffs', 0x457fe0: '_msg_ctype_trinitybigffs',
    0x45801d: '_str_corona', 0x458024: '_msg_ctype_corona', 0x458046: '_str_coronabb',
    0x458050: '_msg_ctype_coronabb', 0x45807c: '_str_coronabigffs', 0x45808c: '_msg_ctype_coronabigffs',
    0x4580c8: '_str_corona4g', 0x4580d4: '_msg_ctype_corona4g', 0x4580fa: '_str_winchester',
    0x458108: '_msg_ctype_winchester', 0x45812e: '_str_winchester4g', 0x45813c: '_msg_ctype_winchester4g',
    0x458166: '_str_winchesterbb', 0x458174: '_msg_ctype_winchesterbb', 0x4581a4: '_str_winchesterbigffs',
    0x4581b8: '_msg_ctype_winchesterbigffs', 0x4581f8: '_str_jasperbigffs', 0x458244: '_msg_iniInvalid',
    0x4582ad: '_str_false', 0x4582b3: '_str_true', 0x4582b8: '_msg_opt_nodvd',
    0x4582ec: '_msg_opt_olddvd', 0x45831f: '_msg_opt_cygnos', 0x458333: '_msg_opt_demon',
    0x458346: '_str_nomobile', 0x45834f: '_msg_opt_nomobile', 0x458365: '_str_smcnocheck',
    0x458370: '_msg_opt_smcnocheck', 0x458388: '_str_noremap', 0x458390: '_msg_opt_noremap',
    0x4583a5: '_str_noecdremap', 0x4583b0: '_msg_opt_noecdremap', 0x4583c8: '_str_nandmu',
    0x4583cf: '_msg_opt_nandmu', 0x4583e3: '_str_nosecurity', 0x4583ee: '_msg_opt_nosecurity',
    0x458406: '_str_nosusecurity', 0x458413: '_str_patchsmc', 0x45841c: '_msg_opt_patchsmc',
    0x458432: '_str_smcnoeject', 0x45843d: '_msg_opt_smcnoeject', 0x458455: '_str_smcnoblink',
    0x458460: '_msg_opt_smcnoblink', 0x458478: '_str_nodvd', 0x45847e: '_str_olddvd',
    0x458485: '_str_cygnos', 0x45848c: '_str_demon', 0x458494: '_msg_optNoValue',
    0x458ae8: '_msg_rawPatchParsed', 0x458b28: '_msg_rawPatchBadOffset', 0x458b80: '_msg_rawPatchSlotsFull',
    0x458bbc: '_msg_patchParseFailed', 0x458bf5: '_str_binFmt', 0x458bfc: '_msg_patchDuplicate',
    0x458c54: '_msg_patchTooMany',
    # app/console_hdd (src/app/console_hdd.c) and what it calls; names are ours
    0x431c20: '_createSysexDirs', 0x431d20: '_addTitleId',
    0x431d70: '_checkManifestHeader', 0x431f20: '_readManifestString',
    0x431f80: '_loadFileChecked', 0x4320b0: '_loadStfsChecked',
    0x432190: '_parseManifestEntries', 0x4327a0: '_parseManifest',
    0x432aa0: '_freeManifest', 0x432b10: '_loadManifest', 0x432de0: '_prepSysex',
    0x432e50: '_sendAvatarData', 0x433130: '_sendDir', 0x433440: '_sendCompatData',
    0x4cdc60: '_manifest',
    0x41ed50: '_netTimerStart', 0x41ed70: '_netTimerEnd', 0x41faf0: '_netMount',
    0x41fc30: '_netUnmount', 0x420470: '_netSendFile', 0x4205d0: '_netFormatSysex',
    0x420670: '_netFormatCompat', 0x420710: '_netMkdir',
    # (libmingwex's stat at 448820 stays unnamed: `_stat` is the msvcrt import in idata.s)
    0x4481c0: '_opendir', 0x448360: '_readdir', 0x448470: '_closedir',
    # data: .bss, and a COMMON symbol (xecrypt.o's .comm resolves to common_bss.s)
    0x479ac0: '_XeRandomIsInit', 0x50e880: '_XeCryptRandomState',
    # app/bootloaders (src/app/bootloaders.c) and what it uses; names are ours
    0x401730: '_unscramble', 0x4017d0: '_cbGetPairing', 0x401910: '_cfGetPairing',
    0x401a00: '_cfBestPairing', 0x401f80: '_crlVerifySig', 0x402210: '_daeDecrypt',
    0x4022f0: '_daeVerifySig', 0x402610: '_fcrtVerifySig', 0x402a00: '_shaSelfCheck',
    0x402a70: '_cbDecrypt', 0x402c70: '_cdDecrypt', 0x402ec0: '_ceDecrypt',
    0x41db70: '_shaCheck',
    # app/keys (src/app/keys.c); names are ours
    0x41aa00: '_keysInit', 0x41ad90: '_setKvSalt', 0x41adb0: '_setKvAltSalt',
    0x41add0: '_setSmcKey', 0x41b1d0: '_setFuseLdv', 0x41b320: '_setFuseCpuKey',
    0x41b420: '_calcXexKey', 0x41b520: '_check1blKey', 0x41b8e0: '_smcChecksum',
    0x41ba00: '_smcEncrypt', 0x41ba80: '_smcPrepare', 0x41bf50: '_cbaEncrypt',
    0x41c0c0: '_cbaEncryptZero', 0x41c1b0: '_cbaEncrypt2', 0x41c370: '_cbbEncrypt',
    0x41c5e0: '_cdEncryptZero', 0x41c6b0: '_cdEncrypt', 0x41c760: '_cdEncryptCpu',
    0x41c860: '_ceEncrypt', 0x41c910: '_cfPatchSlots', 0x41ca20: '_cfEncrypt',
    0x41ce50: '_cgEncrypt', 0x41cf00: '_kvEncrypt', 0x41cff0: '_kvEncryptAlt',
    0x41d0e0: '_kvPrepare', 0x41d6a0: '_extendedPrepare', 0x41d9b0: '_secdataPrepare',
    0x41dc30: '_crlEncrypt', 0x41dfa0: '_daeEncryptOne', 0x41e180: '_daeEncrypt',
    0x41e620: '_fcrtEncrypt', 0x41e7b0: '_shaHeader',
    0x44a5e0: '_secdataKey', 0x44a600: '_daeKey', 0x44a620: '_crlKey', 0x44a640: '_smcKey',
    0x44a644: '_kvAltSalt', 0x44a64c: '_kvSalt', 0x44a654: '_infoKey5', 0x44a664: '_infoKey4',
    0x44a674: '_infoKey3', 0x44a684: '_infoKey2', 0x44a694: '_infoKey1', 0x44a6a4: '_infoKey0',
    0x479560: '_zeroKey', 0x479570: '_pairing',
    # keys.s strings the mixed keys.c refers to (extern names)
    0x456664: '_msg_initRandom', 0x456680: '_msg_initStatic', 0x4566a4: '_msg_pairingSet',
    0x4566c4: '_str_valid', 0x4566ca: '_str_error', 0x4566d0: '_msg_weight',
    0x4566eb: '_msg_cpuKeySet', 0x4566fe: '_str_hexByte', 0x456703: '_str_newline',
    0x456708: '_msg_cpuKeyWarn', 0x45674c: '_msg_cpuKeyChars', 0x45678c: '_msg_cpuKeyLen',
    0x4567eb: '_msg_cpuKeySet2', 0x4567fe: '_msg_fuseLdv', 0x456816: '_msg_fuseCpuKey',
    0x456830: '_msg_fuseNull', 0x45685e: '_msg_1blKeySet', 0x456873: '_msg_1blSum',
    0x456890: '_msg_xexKeySet', 0x4568a5: '_msg_xexSum', 0x4568c2: '_msg_1blBad',
    0x4568e0: '_msg_1blBad2', 0x456904: '_msg_1blChars', 0x456944: '_msg_1blLen',
    0x4569a3: '_msg_1blBadStr', 0x4569c4: '_msg_1blBadStr2', 0x456cfc: '_msg_cbencPairing',
    0x456d22: '_msg_dualCb', 0x456d40: '_msg_cbb15572', 0x456d6c: '_msg_cbbMfg',
    0x456f74: '_str_Success', 0x456fc0: '_msg_extMissing', 0x457028: '_msg_extSize',
    0x457088: '_msg_extEncrypted', 0x4570c8: '_msg_extDecryptFail', 0x457110: '_msg_sdMissing',
    0x457178: '_msg_sdSize', 0x4571d5: '_str_successNl', 0x4571e0: '_msg_crlRetry',
    0x457200: '_str_failedNl', 0x45720c: '_msg_crlCrypted', 0x457248: '_msg_crlBad',
    0x47a10c: '_key1bl', 0x47a12c: '_key28c', 0x47a13c: '_pub1bl', 0x47a144: '_pub2a4',
    # bootloaders.s strings the mixed bootloaders.c refers to (extern names)
    0x44c064: '_msg_cbPairOk', 0x44c09c: '_msg_cbPairFail', 0x44c0dc: '_msg_cfSlot0',
    0x44c110: '_msg_cfSlot1', 0x44c143: '_msg_sigGood', 0x44c14e: '_msg_sigCheckFail',
    0x44c200: '_msg_sigFail', 0x44c214: '_msg_noPub',
    # app/mode_update (src/app/mode_update.c) and what it calls; names are ours
    0x4030b0: '_getBadBlocks', 0x4031d0: '_update_usage', 0x403460: '_wantFile',
    0x4034f0: '_parseAddonIdx', 0x403700: '_getAddons', 0x403820: '_getMobileFiles',
    0x403cf0: '_bldrGetKv', 0x403d80: '_bldrGetSmc', 0x403e10: '_getSecurityFiles',
    0x404320: '_checkBadBlocks', 0x404340: '_getBootloaders',
    0x404430: '_getConsoleFiles', 0x404600: '_updateGetFile',
    0x44a008: '_useConsoleAddons',
    0x412230: '_imageGetBuffer', 0x415ef0: '_remapBadBlocks',
    0x41f700: '_netConnect', 0x41fe20: '_netDumpNand', 0x41ff90: '_netGetBldrs',
    0x41ffe0: '_netSendFlash', 0x420420: '_netGetBadBlocks', 0x420840: '_netReboot',
    # app/net's other functions and data (names are ours; nothing outside calls them)
    0x41e800: '_netRecv', 0x41ea90: '_netFindBeacon', 0x41edb0: '_netTimerElapsed',
    0x41ede0: '_netSendStr', 0x41ee30: '_netRecvVerbose', 0x41f1a0: '_netSendData',
    0x41f330: '_netCheckOk', 0x41f390: '_netOpenSocket', 0x41f470: '_netReadInfo',
    0x41fa00: '_netClose', 0x44a6c0: '_netSock', 0x479574: '_netInfo',
    0x479578: '_netEmpty', 0x4cd844: '_netStartTime', 0x448190: '__difftime32',
    # net.s strings the mixed net.c refers to
    0x45763e: '_net_45763e', 0x457688: '_net_457688', 0x4576ac: '_net_4576ac',
    0x4576cf: '_net_4576cf', 0x4576e8: '_net_4576e8', 0x457712: '_net_457712',
    0x45773c: '_net_45773c', 0x4577bb: '_net_4577bb', 0x4578f5: '_net_4578f5',
    0x457913: '_net_457913', 0x457919: '_net_457919', 0x45791d: '_net_45791d',
    0x45796c: '_net_45796c', 0x457990: '_net_457990', 0x457998: '_net_457998',
    0x4579cb: '_net_4579cb', 0x457a23: '_net_457a23', 0x457a35: '_net_457a35',
    0x457a51: '_net_457a51', 0x457a57: '_net_457a57', 0x457a71: '_net_457a71',
    # mode_update.s strings and variables the mixed mode_update.c refers to
    0x46f040: '_path', 0x46f144: '_noReboot', 0x46f148: '_noAvatar', 0x46f14c: '_noWrite',
    0x46f150: '_clean', 0x46f154: '_hasHdd', 0x46f158: '_updating', 0x46f15c: '_info',
    0x44c6e8: '_mu_44c6e8', 0x44c70c: '_mu_44c70c', 0x44c730: '_mu_44c730', 0x44c74c: '_mu_44c74c',
    0x44c76c: '_mu_44c76c', 0x44c7ab: '_mu_44c7ab', 0x44c7b4: '_mu_44c7b4', 0x44c7e1: '_mu_44c7e1',
    0x44c7ec: '_mu_44c7ec', 0x44c810: '_mu_44c810', 0x44c844: '_mu_44c844', 0x44c850: '_mu_44c850',
    0x44c888: '_mu_44c888', 0x44c8ca: '_mu_44c8ca', 0x44c8e8: '_mu_44c8e8', 0x44c918: '_mu_44c918',
    0x44c95c: '_mu_44c95c', 0x44c9a8: '_mu_44c9a8', 0x44c9e8: '_mu_44c9e8', 0x44ca2c: '_mu_44ca2c',
    0x44ca74: '_mu_44ca74', 0x44cac8: '_mu_44cac8', 0x44cb18: '_mu_44cb18', 0x44cb58: '_mu_44cb58',
    0x44cb90: '_mu_44cb90', 0x44cbb0: '_mu_44cbb0', 0x44cbbc: '_mu_44cbbc', 0x44cc04: '_mu_44cc04',
    0x44cc58: '_mu_44cc58', 0x44ccc8: '_mu_44ccc8', 0x44cd14: '_mu_44cd14', 0x44cd6c: '_mu_44cd6c',
    0x44cdc0: '_mu_44cdc0', 0x44cddb: '_mu_44cddb', 0x44cde8: '_mu_44cde8', 0x44cdf4: '_mu_44cdf4',
    0x44ce08: '_mu_44ce08', 0x44ce21: '_mu_44ce21', 0x44ce40: '_mu_44ce40', 0x44ce9c: '_mu_44ce9c',
    0x44cea3: '_mu_44cea3', 0x44cebc: '_mu_44cebc', 0x44ced0: '_mu_44ced0', 0x44cf18: '_mu_44cf18',
    0x44cf6c: '_mu_44cf6c', 0x44cfac: '_mu_44cfac', 0x44cfd4: '_mu_44cfd4', 0x44cfe1: '_mu_44cfe1',
    0x44cff0: '_mu_44cff0', 0x44d009: '_mu_44d009', 0x44d010: '_mu_44d010', 0x44d054: '_mu_44d054',
    0x44d074: '_mu_44d074', 0x44d090: '_mu_44d090', 0x44d0d4: '_mu_44d0d4', 0x44d0f8: '_mu_44d0f8',
    0x44d12c: '_mu_44d12c', 0x44d144: '_mu_44d144', 0x44d171: '_mu_44d171', 0x44d186: '_mu_44d186',
    0x44d198: '_mu_44d198', 0x44d1d3: '_mu_44d1d3', 0x44d1db: '_mu_44d1db', 0x44d400: '_mu_44d400',
    0x44d424: '_mu_44d424', 0x44d440: '_mu_44d440', 0x44d46e: '_mu_44d46e', 0x44d479: '_mu_44d479',
    0x44d484: '_mu_44d484', 0x44d5ba: '_mu_44d5ba', 0x44d5d4: '_mu_44d5d4',
    # app/image_read (wip/app/image_read.c) and what it calls; names are ours
    0x4136a0: '_fsFind', 0x4138c0: '_getImageLdv', 0x413ad0: '_getImageSmc',
    0x413d30: '_getImageKv', 0x414050: '_getImageMobiles', 0x414300: '_getNetKd',
    0x4144e0: '_loadFlashFile', 0x414610: '_fsFindFile', 0x414760: '_fsGetFile',
    0x414960: '_findAnchor', 0x414af0: '_mmcFindMobiles', 0x414b90: '_spareVersion',
    0x414be0: '_showMobilePages', 0x414e90: '_scanMobiles', 0x4151c0: '_setFsOffset',
    0x415230: '_findFsRoot', 0x4154d0: '_imgGetSecurityFiles', 0x415970: '_findSmcConfig',
    0x415b00: '_checkBlock', 0x415d90: '_addRemap', 0x415e90: '_findFreeRemap',
    0x416040: '_notZeropair', 0x416070: '_spareLbaOk', 0x4160d0: '_copyMmcImage',
    0x416150: '_parseDump', 0x416840: '_copyMuData', 0x416aa0: '_detectController',
    0x416cd0: '_checkHeader', 0x4172c0: '_getNonces',
    0x40fc30: '_pageEccOk', 0x40fcc0: '_blockEccOk', 0x40ff40: '_blockErased',
    0x410070: '_isErased', 0x412e90: '_statisticsOffset', 0x412f60: '_manufacturingOffset',
    # image_read.s strings and variables the mixed image_read.c refers to
    0x44a5c0: '_zeropair', 0x44a5d0: '_mobileName', 0x44a5d8: '_fs', 0x474a20: '_mobiles', 0x474b20: '_anchor',
    0x474d20: '_fsOffset', 0x474d24: '_fsValid', 0x474d40: '_fsBuf', 0x478d40: '_dumpSize',
    0x4521b8: '_ir_4521b8', 0x4521e0: '_ir_4521e0', 0x452220: '_ir_452220', 0x452260: '_ir_452260',
    0x4522c4: '_ir_4522c4', 0x4522e4: '_ir_4522e4', 0x45230f: '_ir_45230f', 0x45232c: '_ir_45232c',
    0x45235c: '_ir_45235c', 0x45238c: '_ir_45238c', 0x4523bc: '_ir_4523bc', 0x4523ec: '_ir_4523ec',
    0x45242c: '_ir_45242c', 0x452450: '_ir_452450', 0x452494: '_ir_452494', 0x4524dc: '_ir_4524dc',
    0x452508: '_ir_452508', 0x452538: '_ir_452538', 0x45256c: '_ir_45256c', 0x4525a8: '_ir_4525a8',
    0x4525d0: '_ir_4525d0', 0x45261c: '_ir_45261c', 0x452674: '_ir_452674', 0x4526ac: '_ir_4526ac',
    0x4526f0: '_ir_4526f0', 0x45271c: '_ir_45271c', 0x45276c: '_ir_45276c', 0x452799: '_ir_452799',
    0x4527a0: '_ir_4527a0', 0x4527e4: '_ir_4527e4', 0x452824: '_ir_452824', 0x452864: '_ir_452864',
    0x4528a4: '_ir_4528a4', 0x4528e1: '_ir_4528e1', 0x4528fe: '_ir_4528fe', 0x452912: '_ir_452912',
    0x452930: '_ir_452930', 0x452958: '_ir_452958', 0x45296a: '_ir_45296a', 0x452988: '_ir_452988',
    0x4529d0: '_ir_4529d0', 0x4529f8: '_ir_4529f8', 0x452a24: '_ir_452a24', 0x452a4c: '_ir_452a4c',
    0x452a78: '_ir_452a78', 0x452aa4: '_ir_452aa4', 0x452acc: '_ir_452acc', 0x452af8: '_ir_452af8',
    0x452b20: '_ir_452b20', 0x452b6c: '_ir_452b6c', 0x452bc3: '_ir_452bc3', 0x452bc9: '_ir_452bc9',
    0x452bd3: '_ir_452bd3', 0x452bd8: '_ir_452bd8', 0x452c20: '_ir_452c20', 0x452c47: '_ir_452c47',
    0x452c5e: '_ir_452c5e', 0x452c70: '_ir_452c70', 0x452cbc: '_ir_452cbc', 0x452d0c: '_ir_452d0c',
    0x452d33: '_ir_452d33', 0x452d4e: '_ir_452d4e', 0x452d55: '_ir_452d55', 0x452d74: '_ir_452d74',
    0x452db0: '_ir_452db0', 0x452e09: '_ir_452e09', 0x452e18: '_ir_452e18', 0x452e50: '_ir_452e50',
    0x452e80: '_ir_452e80', 0x452eb0: '_ir_452eb0', 0x452edc: '_ir_452edc', 0x452f0c: '_ir_452f0c',
    0x452f44: '_ir_452f44', 0x452f7c: '_ir_452f7c', 0x452fb8: '_ir_452fb8', 0x452ffc: '_ir_452ffc',
    0x453049: '_ir_453049', 0x453064: '_ir_453064', 0x45309c: '_ir_45309c', 0x4530d4: '_ir_4530d4',
    0x45310c: '_ir_45310c', 0x453150: '_ir_453150', 0x45318c: '_ir_45318c', 0x4531b4: '_ir_4531b4',
    0x4531e8: '_ir_4531e8', 0x453248: '_ir_453248', 0x4532b0: '_ir_4532b0', 0x453310: '_ir_453310',
    0x453354: '_ir_453354', 0x4533a8: '_ir_4533a8', 0x4533ec: '_ir_4533ec', 0x453420: '_ir_453420',
    0x453474: '_ir_453474', 0x4534b8: '_ir_4534b8', 0x4534e9: '_ir_4534e9', 0x4534fc: '_ir_4534fc',
    0x453510: '_ir_453510', 0x453538: '_ir_453538', 0x45355c: '_ir_45355c', 0x453594: '_ir_453594',
    0x4535a7: '_ir_4535a7', 0x4535ac: '_ir_4535ac', 0x4535e4: '_ir_4535e4', 0x453610: '_ir_453610',
    0x453649: '_ir_453649', 0x453664: '_ir_453664', 0x453694: '_ir_453694', 0x4536b8: '_ir_4536b8',
    0x4536e0: '_ir_4536e0', 0x453708: '_ir_453708', 0x453760: '_ir_453760', 0x45378c: '_ir_45378c',
    0x4537b4: '_ir_4537b4', 0x453810: '_ir_453810', 0x453828: '_ir_453828', 0x45386c: '_ir_45386c',
    0x4538ac: '_ir_4538ac', 0x4538ec: '_ir_4538ec', 0x453928: '_ir_453928', 0x45396c: '_ir_45396c',
    0x4539b4: '_ir_4539b4', 0x453a0c: '_ir_453a0c', 0x453a68: '_ir_453a68', 0x453aac: '_ir_453aac',
    0x453af4: '_ir_453af4', 0x453b48: '_ir_453b48', 0x453b98: '_ir_453b98', 0x453bdc: '_ir_453bdc',
    0x453c28: '_ir_453c28', 0x453c9c: '_ir_453c9c', 0x453d18: '_ir_453d18', 0x453d3c: '_ir_453d3c',
    0x453d78: '_ir_453d78', 0x453db0: '_ir_453db0', 0x453dec: '_ir_453dec', 0x453e2c: '_ir_453e2c',
    0x453e64: '_ir_453e64', 0x453ea4: '_ir_453ea4', 0x453edc: '_ir_453edc', 0x453f1c: '_ir_453f1c',
    0x453f54: '_ir_453f54', 0x453f94: '_ir_453f94', 0x453fcc: '_ir_453fcc', 0x454009: '_ir_454009',
    0x454025: '_ir_454025', 0x454044: '_ir_454044', 0x454098: '_ir_454098', 0x4540dc: '_ir_4540dc',
    0x454114: '_ir_454114', 0x454138: '_ir_454138', 0x45417c: '_ir_45417c', 0x4541b0: '_ir_4541b0',
    # app/build; names are ours.  Its file table entry is {name[0x400], crc,
    # type, offset, data, size, ...}, 0x42c bytes.  findFile is named above.
    0x427500: '_loadBaseFile',          # baseDir+name; regparm (eax, edx)
    0x427650: '_findFileOffset', 0x4276a0: '_findFileSize',
    0x427730: '_loadFileCrc', 0x427950: '_readMetaFile',
    0x4279b0: '_makeTimestamp', 0x427a70: '_timestampToFileTime',
    0x427ab0: '_loadBaseFileMeta', 0x427cc0: '_loadCommonFile',
    0x428040: '_loadInputFile', 0x428780: '_loadBinFile', 0x4288c0: '_loadLocalFile',
    0x428ac0: '_setFileData', 0x428b10: '_appendAddonPatches',
    0x428d20: '_showSmcConfig', 0x429180: '_iniRangeOk', 0x4291f0: '_patchSmcConfig',
    0x4297d0: '_extractSmcConfig', 0x429b10: '_raiseKernel', 0x429b30: '_checkBl',
    0x429e70: '_verifyBlSigs', 0x42a370: '_loadBlFiles', 0x42adc0: '_loadConsoleBlFiles',
    0x42b2b0: '_patchHeaderOpts', 0x42b3d0: '_blmodMissing', 0x42b3f0: '_rotSumSha',
    0x42b610: '_countBits', 0x42b660: '_patchBlsResign', 0x42bb10: '_patchBlsBlmod',
    0x42bf70: '_fixupPatchSet', 0x42c090: '_addBlsToImage', 0x42c600: '_isUpdateBl',
    0x42c620: '_addUpdateBls', 0x42c900: '_logPowerButton', 0x42cbb0: '_patchFreeboot',
    0x42cee0: '_patchPayloadSize', 0x42cfa0: '_encodeBls', 0x42dfb0: '_encodeUpdateBls',
    0x42e160: '_calcBlAreaSize', 0x42e760: '_buildFlash',   # buildImage tail-calls it
    # app/image_write functions app/build calls (names are ours, from what
    # build does with them)
    0x410240: '_setFlashBuild', 0x410290: '_smcSetLoad', 0x410360: '_setPatchSlot',
    0x410460: '_imgCfOffset', 0x410490: '_imgCfSize', 0x4104d0: '_imgSize',
    0x4104f0: '_imgBigBlock', 0x410500: '_imgAdd',
    # the rest of app/image_write (names are ours).  0x4cb7c0 is a u16 per
    # block from fsStart (479efc) to fsEnd (479ef8): the FS table build.s's
    # "Fixing up FS table..." / "Writing FS table to image" logs refer to.
    0x40e950: '_imgWriteStart',     # regparm (src, len, fs type): copy to offset 0
    0x40eef0: '_imgWriteAt',        # regparm (offset, src, len) + stack fs type
    0x4100b0: '_setBlockSpare',     # per-page LBA + ECD for one block
    0x410220: '_imgSizeAligned',    # image size rounded up to 0x4000
    0x4104e0: '_imgSetSize',
    0x410bb0: '_imgAddFile',        # "adding %s will exceed available flash space"
    0x411030: '_imgAddFileAs',      # "adding as %s ...", tail-calls imgAddFile
    0x4110b0: '_imgAddMobile',      # Mobile%c.dat
    0x4112b0: '_fixupFsTable',      # build logs "Fixing up FS table..." first
    0x4112f0: '_fixupEmptyFsBlocks',  # "Fixing up empty FS block entries..."
    0x411600: '_addSmcConfig', 0x411680: '_writeInitialHeader',
    0x411bd0: '_writeFsTable', 0x412110: '_copyAnchorBlock',
    0x4125a0: '_finalizeImage',     # "------ finalizing image ------"
    0x412dd0: '_fsStartBlock', 0x413030: '_imgAddRaw',  # "adding %s at raw offset"
    # never called (only .eh_frame refers to them) except imgWritePage
    0x40ecc0: '_imgWritePage',      # regparm (offset, src, fs type), 0x1000 bytes
    0x40fb60: '_calcEcd',           # page ECD over separate data/spare pointers
    0x40feb0: '_pageErased',        # 512 data + 16 spare bytes all 0xff
    0x40ff80: '_blockPagesErased',  # same for each page of a block
    0x410040: '_blockIsFF',         # 0x4000 bytes all 0xff
    0x410350: '_imgSmcOffset',      # flash header +0x7c
    0x410b90: '_imgFits',           # (offset, len) within the FS end block
    0x4121b0: '_spareUsed',         # 16 spare bytes not all 0xff
    0x412de0: '_reservedAreaOffset',  # like statisticsOffset, per NAND type
    # app/image_write's data (COMMON globals in common_bss.s, and its own)
    0x4c9164: '_mmcAnchor', 0x4c97c0: '_fsFiles', 0x4cb7c0: '_fsTable',
    0x4cd7c0: '_hdrTemplate', 0x4cd840: '_imgEnd', 0x44a580: '_copyright',
    0x46f9e0: '_smcPage',
    # app/image_write's strings that its C functions use (wip/mixed.py)
    0x4517f8: '_iw_4517f8', 0x45187c: '_iw_45187c', 0x4518e8: '_iw_4518e8',
    0x4519c4: '_iw_4519c4', 0x451a20: '_iw_451a20', 0x451a44: '_iw_451a44',
    0x451a6c: '_iw_451a6c', 0x451a94: '_iw_451a94', 0x451ab8: '_iw_451ab8',
    0x451adc: '_iw_451adc', 0x451b2c: '_iw_451b2c', 0x451b54: '_iw_451b54',
    0x451b7a: '_iw_451b7a', 0x451b7d: '_iw_451b7d', 0x451b9a: '_iw_451b9a',
    0x451ba4: '_iw_451ba4', 0x451be4: '_iw_451be4', 0x451c18: '_iw_451c18',
    0x451c38: '_iw_451c38', 0x451c94: '_iw_451c94', 0x451cdd: '_iw_451cdd',
    0x451f80: '_iw_451f80',
    # app/build's strings that its C functions use (wip/mixed.py)
    0x458ca4: '_bd_458ca4', 0x458ca8: '_bd_458ca8', 0x458ce1: '_bd_458ce1',
    0x458cf9: '_bd_458cf9', 0x458cfc: '_bd_458cfc', 0x458d1b: '_bd_458d1b',
    0x458d3c: '_bd_458d3c', 0x458d74: '_bd_458d74', 0x458d98: '_bd_458d98',
    0x458f80: '_bd_458f80', 0x458fb4: '_bd_458fb4', 0x458fe6: '_bd_458fe6',
    0x458ff5: '_bd_458ff5', 0x45900a: '_bd_45900a', 0x459012: '_bd_459012',
    0x459021: '_bd_459021', 0x459030: '_bd_459030', 0x459050: '_bd_459050',
    0x459070: '_bd_459070', 0x459090: '_bd_459090', 0x4590b0: '_bd_4590b0',
    0x4590d1: '_bd_4590d1', 0x4590e7: '_bd_4590e7', 0x4590f2: '_bd_4590f2',
    0x4590fe: '_bd_4590fe', 0x45910a: '_bd_45910a', 0x459115: '_bd_459115',
    0x45911f: '_bd_45911f', 0x45912a: '_bd_45912a', 0x459134: '_bd_459134',
    0x45913f: '_bd_45913f', 0x459151: '_bd_459151', 0x459160: '_bd_459160',
    0x459164: '_bd_459164', 0x459955: '_bd_459955', 0x459e3c: '_bd_459e3c',
    0x459e74: '_bd_459e74', 0x459e9c: '_bd_459e9c', 0x459ec8: '_bd_459ec8',
    0x459ed2: '_bd_459ed2', 0x459ed8: '_bd_459ed8', 0x459ede: '_bd_459ede',
    0x459ee4: '_bd_459ee4', 0x45a590: '_bd_45a590', 0x45a5cc: '_bd_45a5cc',
    0x45a5e0: '_bd_45a5e0', 0x45a618: '_bd_45a618', 0x45a664: '_bd_45a664',
    0x45a6a4: '_bd_45a6a4', 0x45a6b0: '_bd_45a6b0', 0x45a6df: '_bd_45a6df',
    0x45a6f8: '_bd_45a6f8', 0x45a71e: '_bd_45a71e', 0x45a728: '_bd_45a728',
    0x45a738: '_bd_45a738', 0x45a748: '_bd_45a748', 0x45a785: '_bd_45a785',
    0x45a78c: '_bd_45a78c', 0x45a7c4: '_bd_45a7c4', 0x45a7f8: '_bd_45a7f8',
    0x45a80e: '_bd_45a80e', 0x45a8af: '_bd_45a8af',
    # runtime functions the C code calls
    0x448760: '__assert',      # libmingwex wassert.o
    0x447c00: '___chkstk_ms',   # libgcc _chkstk_ms.o
    0x449050: '__time32',       # import stub, msvcrt `time`
    # import stubs
    0x449078: '_strlen', 0x449090: '_srand', 0x449098: '_sprintf', 0x4490c0: '_rand',
    0x4490d8: '_putchar', 0x4490e0: '_printf', 0x4490f0: '_memset', 0x4490f8: '_memcpy',
    0x449108: '_malloc', 0x449140: '_free', 0x4491a0: '_calloc',
    0x4490d0: '_puts', 0x449100: '_memcmp', 0x449160: '_fopen', 0x449168: '_fgets',
    0x449188: '_feof', 0x449190: '_fclose', 0x4491a8: '_atoi', 0x449200: '__lrotl',
    0x449080: '_strcpy', 0x4490b0: '_rename', 0x4490b8: '_remove', 0x449158: '_fprintf',
    0x4490e8: '__mktime32', 0x449110: '__gmtime32',   # msvcrt mktime/gmtime
    0x449088: '_strcat', 0x4490a8: '_rewind', 0x449118: '_fwrite', 0x449128: '_ftell',
    0x449138: '_fseek', 0x449148: '_fread', 0x449150: '_fputc', 0x4491f0: '__mkdir',
    0x448af0: '_fseeko64', 0x448ff0: '_ftello64',   # libmingwex
    # libgcc (64-bit division) and the vsnprintf mingw's stdio.h calls
    0x447c30: '___divdi3', 0x447d70: '___moddi3', 0x447f20: '___udivdi3',
    0x448040: '___umoddi3', 0x449030: '___ms_vsnprintf',
    0x449058: '_strrchr', 0x4490a0: '_signal', 0x449258: '__chdir', 0x449060: '_strncpy',
    0x4491d0: '_strnicmp', 0x4491d8: '_stricmp', 0x449198: '_exit', 0x449178: '_fgetc',
    # IAT slots that dllimport declarations reference directly
    0x50f2f0: '__imp___errno',
}
# IAT slot labels (ddfix names them after the import) that clash with a
# SYMBOLS name: msvcrt's `_strnicmp`/`_exit` slots vs the stubs for strnicmp/exit.
IAT_NAMES = {'_strnicmp': '__imp___strnicmp', '_exit': '__imp___exit',
             '_stricmp': '__imp___stricmp'}
# ws2_32 imports, named as winsock2.h's dllimport __stdcall declarations
# reference them (app/net.c)
IAT_NAMES.update({n: '__imp__%s@%d' % (n, a) for n, a in (
    ('WSAGetLastError', 0), ('WSAStartup', 8), ('WSAStringToAddressA', 20),
    ('bind', 12), ('closesocket', 4), ('connect', 12), ('htons', 4), ('recv', 16),
    ('recvfrom', 24), ('select', 20), ('send', 16), ('setsockopt', 20), ('socket', 12))})
# Functions already in C inside objects that are otherwise still assembly
# (mixed objects).  Their range in the .s becomes a `#@C <name>` marker that
# build.sh fills from `gcc -S` of src/<obj>.c (re/splice.py); data, the
# ident and .eh_frame stay in the .s.  Names come from SYMBOLS.
C_FUNCS = {
    0x40aa10,   # app/filelist_ini getIniValue
    # app/mode_update (getSecurityFiles, getConsoleFiles, mode_update stay asm)
    0x4030b0, 0x4031d0, 0x403460, 0x4034f0,  # getBadBlocks update_usage wantFile parseAddonIdx
    0x403700, 0x403820, 0x403cf0, 0x403d80,  # getAddons getMobileFiles bldrGetKv bldrGetSmc
    0x404320, 0x404340, 0x404600,            # checkBadBlocks getBootloaders updateGetFile
    # app/options (parseButton stays asm: its ipa-split part at 449640 is
    # called from asm, and gcc would put it in .text.unlikely)
    0x4236f0,                                # baseFileExists.part.0
    0x423730, 0x423750, 0x423830, 0x424170,  # baseFileExists perboxExists iniConsoleType setConsoleType
    0x424a10, 0x424b20, 0x424b60, 0x424bb0,  # optIniInt stripColons macidSet setBoolOption
    0x427000, 0x4271a0, 0x427260,            # parseRawPatch parseRawPatches addPatch
    # app/keys (the rest are drafted in wip/app/keys.c)
    0x41aa00, 0x41abb0, 0x41ac00, 0x41ac50,  # keysInit setCrlKey setDaeKey setSecdataKey
    0x41ac70, 0x41aca0, 0x41acd0, 0x41ad00,  # setInfoKey0..3
    0x41ad30, 0x41ad60, 0x41ad90, 0x41adb0,  # setInfoKey4 setInfoKey5 setKvSalt setKvAltSalt
    0x41add0, 0x41ade0, 0x41ae40, 0x41afe0,  # setSmcKey setPairing checkCpuKey setCpuKeyStr
    0x41b120, 0x41b1d0, 0x41b420, 0x41b520,  # setCpuKey setFuseLdv calcXexKey check1blKey
    0x41b600, 0x41b320,                      # set1blKey setFuseCpuKey
    0x41b740, 0x41ba00, 0x41bf50, 0x41c0c0,  # checkKeys smcEncrypt cbaEncrypt cbaEncryptZero
    0x41c1b0, 0x41c370, 0x41c5e0, 0x41c6b0,  # cbaEncrypt2 cbbEncrypt cdEncryptZero cdEncrypt
    0x41c760, 0x41c860, 0x41ce50, 0x41cf00,  # cdEncryptCpu ceEncrypt cgEncrypt kvEncrypt
    0x41cff0, 0x41d6a0, 0x41d9b0, 0x41db70,  # kvEncryptAlt extendedPrepare secdataPrepare shaCheck
    0x41dc30, 0x41dfa0, 0x41e7b0,            # crlEncrypt daeEncryptOne shaHeader
    # app/image_read (the rest are drafted in wip/app/image_read.c)
    0x4136a0, 0x414050, 0x414300, 0x4144e0,  # fsFind getImageMobiles getNetKd loadFlashFile
    0x414610, 0x414af0, 0x414b90, 0x4151c0,  # fsFindFile mmcFindMobiles spareVersion setFsOffset
    0x415230, 0x415970, 0x415d90, 0x415e90,  # findFsRoot findSmcConfig addRemap findFreeRemap
    0x416040, 0x416070, 0x416840,            # notZeropair spareLbaOk copyMuData
    0x4154d0, 0x4172c0,                      # imgGetSecurityFiles getNonces
    # app/mode_client (client_usage: switch table; clientKeys, clientBinPatch, mode_client stay asm)
    0x406740, 0x406980, 0x406aa0,            # clientInfo clientWrite clientManifest
    0x406b60, 0x407160, 0x407320,            # dumpKey updatePatches clientPatches
    0x4076b0, 0x407850, 0x407a00, 0x408080,  # clientReadBlocks clientWriteBlocks patchNand clientEraseBlock
    0x408160, 0x406e50,                      # getArgs checkPatches
    # app/net (the rest are drafted in wip/app/net.c)
    0x41ea70, 0x41ed50, 0x41ed70, 0x41edb0,  # netFree netTimerStart netTimerEnd netTimerElapsed
    0x41ede0, 0x41f1a0, 0x41f330, 0x41f390,  # netSendStr netSendData netCheckOk netOpenSocket
    0x41fa00, 0x41fa40, 0x41fe10, 0x41fe20,  # netClose netDisconnect netGetInfo netDumpNand
    0x41ff90, 0x420420, 0x420840,            # netGetBldrs netGetBadBlocks netReboot
    # app/build (wip/app/build.c is the whole draft; wip/mixed.py)
    0x427650, 0x4276a0, 0x4276f0, 0x427950,  # findFileOffset findFileSize findFile readMetaFile
    0x4279b0, 0x427cc0, 0x428780, 0x4288c0,  # makeTimestamp loadCommonFile loadBinFile loadLocalFile
    0x428ac0, 0x429180, 0x429b10, 0x42b2b0,  # setFileData iniRangeOk raiseKernel patchHeaderOpts
    0x42b3f0, 0x42b610, 0x42c600, 0x42cee0,  # rotSumSha countBits isUpdateBl patchPayloadSize
    0x428d20, 0x42b3d0, 0x42cbb0, 0x42dfb0,  # showSmcConfig blmodMissing patchFreeboot encodeUpdateBls
    # app/image_write (wip/app/image_write.c is the whole draft; wip/mixed.py)
    0x40fb10, 0x40fb60, 0x40fbb0, 0x40fc30,  # imageFree calcEcd calcPageEcc pageEccOk
    0x40feb0, 0x40ff40, 0x40ff80, 0x410040,  # pageErased blockErased blockPagesErased blockIsFF
    0x410070, 0x4100b0, 0x410220, 0x410240,  # isErased setBlockSpare imgSizeAligned setFlashBuild
    0x410350, 0x410360, 0x410460, 0x410490,  # imgSmcOffset setPatchSlot imgCfOffset imgCfSize
    0x4104d0, 0x4104e0, 0x4104f0, 0x410b90,  # imgSize imgSetSize imgBigBlock imgFits
    0x411030, 0x4112b0, 0x4112f0, 0x411600,  # imgAddFileAs fixupFsTable fixupEmptyFsBlocks addSmcConfig
    0x411800, 0x412110, 0x4121b0, 0x412230,  # checkBootImage copyAnchorBlock spareUsed imageGetBuffer
    0x412260, 0x412dd0, 0x412de0, 0x412e90,  # writeImage fsStartBlock reservedAreaOffset statisticsOffset
    0x412f60, 0x413030,                      # manufacturingOffset imgAddRaw
}
CHKSTK = (0x447c00,'runtime/libgcc/_chkstk_ms', 'byte match; assembly, no unwind info')
STUBS = (0x449038, 'runtime/import_stubs', 'dlltool `jmp [__imp_x]` stubs, no unwind info')
STARTUP = 0x4492c0          # .text.startup begins (main)
LISTS = (0x4497a0, 0x4497b4, 'runtime/ctor_dtor_lists', '__CTOR_LIST__/__DTOR_LIST__ from the link script')
NOCODE = ('runtime/no_code_objects', '10 gcc objects without code (idents only; data merged into neighbours)')
# Data whose defining object is known from its C source, where references
# alone would place it wrongly: (lo, hi, file, evidence).
DATA_OWNERS = [
    (0x45cc20, 0x461c60, 'crypto/aes/aestab',
     'aestab.c defines t_im, t_il, t_in, t_fl, t_fn, t_rc; only aescrypt/aeskey code uses them'),
]
# One-past-the-end pointers that ddisasm symbolized as the label that follows
# (an object's next data).  instruction address -> (target, expression).
END_POINTERS = {
    # console_hdd loops over the 4-pointer table at 45c644; 45c654 starts log's strings
    0x431cc5: (0x45c654, 'L_45c644+16'),
}
COMMON = (0x479e84,'common_bss', 'COMMON globals, laid out by ld in hash order')
WHOLE = {'.idata': ('runtime/idata', 'import tables (ld builds these from import libraries)'),
         '.CRT': ('runtime/crt_tls_sections', '.CRT initializer tables and .tls directory'),
         '.tls': ('runtime/crt_tls_sections', None),
         '.rsrc': ('runtime/manifest', 'default application manifest resource')}

# output section in the object file: (directive, alignment cap)
OUT = {'.text': ('.text', 16), '.text.startup': ('.section .text.startup,"xr"', 16),
       '.ctors_dtors': ('.section .ctors_dtors,"dxr"', 4), '.data': ('.data', 32),
       '.jcr': ('.section .jcr,"dw"', 4), '.rdata': ('.section .rdata,"dr"', 32),
       '.rdata$zzz': ('.section .rdata$zzz,"dr"', 4), '.eh_frame': ('.section .eh_frame,"dr"', 4),
       '.bss': ('.bss', 32), '.idata': ('.section .idata,"dw"', 4), '.CRT': ('.section .CRT,"dw"', 4),
       '.tls': ('.section .tls,"dw"', 4), '.rsrc': ('.section .rsrc,"dw"', 4)}

SECDIR = re.compile(r'^(?:\.section\s+([^\s,]+)\s*,.*|(\.text|\.data|\.bss))$')
LABEL = re.compile(r'^([A-Za-z_.$][\w.$@]*):\s*$')
SYM = re.compile(r'(?<![\w.$])((?:FUN|L)_[0-9a-f]+(?:_END)?|[A-Za-z_][\w@]*)')
REFADDR = re.compile(r'(?<![\w.$])(?:FUN|L)_([0-9a-f]+)')
ZERO = re.compile(r'^(\s*)\.zero\s+(\d+)\s*$')
IDENT = 44


def lowbit(x):
    return x & -x if x else 1 << 30


def main():
    exe, lj, outdir = sys.argv[1:4]
    img = Image(exe)
    d = json.load(open(lj))
    L = [re.sub(r'(?<![\w.$])\.L_', 'L_', l) for l in d['lines']]
    A = d['addr']
    for i, a in enumerate(A):
        if a in END_POINTERS:
            t, expr = END_POINTERS[a]
            L[i], n = re.subn(r'(?<![\w.$])L_%x(?![\w$+])' % t, expr, L[i])
            assert n == 1, (hex(a), L[i])
    sec = {n: (va, va + max(vsz, rsz) if n == '.bss' else va + vsz) for n, va, vsz, _, rsz in img.secs}
    sec['.bss'] = (sec['.bss'][0], img.sec('.bss')[1] + img.sec('.bss')[2])
    us = units(img)

    # ---- lines: section and position (labels sit at the next addressed line)
    cur, secof = None, []
    for l in L:
        m = SECDIR.match(l.strip())
        if m:
            s = m.group(1) or m.group(2)
            cur = '.eh_fram' if s == '.eh_frame' else s
        secof.append(cur)
    pos = [None] * len(L)
    nxt = None
    for i in range(len(L) - 1, -1, -1):
        if SECDIR.match(L[i].strip()) or secof[i] is None:
            nxt = None
            continue
        if A[i] is not None:
            nxt = A[i]
        pos[i] = A[i] if A[i] is not None else (nxt if nxt is not None else sec[secof[i]][1])

    # ---- link order and fixed pieces: (section, lo, hi, file, out_section)
    order, info = [], {}
    def add(path, why):
        if path not in info:
            order.append(path)
            info[path] = why
    pieces = []
    text_starts = {}
    for i, (cie, fdes) in enumerate(us):
        path, why = NAMES[i]
        if i == 81:
            add(CHKSTK[1], CHKSTK[2])
            text_starts[CHKSTK[0]] = CHKSTK[1]
        if i == 92:
            add(STUBS[1], STUBS[2])
            text_starts[STUBS[0]] = STUBS[1]
        add(path, why)
        normal = [a for a, _ in fdes if a < STARTUP]
        if normal:
            text_starts[min(normal)] = path
    add(LISTS[2], LISTS[3])
    add(NOCODE[0], NOCODE[1])
    add(COMMON[1], COMMON[2])
    for s, (p, why) in WHOLE.items():
        add(p, why or info.get(p))
    ts = sorted(text_starts)
    for k, a in enumerate(ts):
        pieces.append(('.text', a, ts[k + 1] if k + 1 < len(ts) else STARTUP, text_starts[a], '.text'))
    startup = sorted((a, NAMES[i][0]) for i, (_, f) in enumerate(us) for a, _ in f if a >= STARTUP)
    for k, (a, p) in enumerate(startup):
        pieces.append(('.text', a, startup[k + 1][0] if k + 1 < len(startup) else LISTS[0], p, '.text.startup'))
    pieces.append(('.text', LISTS[0], LISTS[1], LISTS[2], '.ctors_dtors'))
    # eh_frame: one piece per CIE; crtend's starts with the 4-byte zero terminator
    ehs = []
    for i, (cie, _) in enumerate(us):
        lo = cie - 4 if i == 93 and img.read(cie - 4, 4) == b'\0' * 4 else cie
        ehs.append((lo, NAMES[i][0]))
    for k, (lo, p) in enumerate(ehs):
        pieces.append(('.eh_fram', lo, ehs[k + 1][0] if k + 1 < len(ehs) else sec['.eh_fram'][1], p, '.eh_frame'))
    # idents: one per gcc object in link order, the remainder to NOCODE
    rlo, rhi = sec['.rdata']
    nid = (rhi - rlo) // IDENT
    id0 = rhi - IDENT * 104
    gcc_objs = [NAMES[i][0] for i in range(len(us))]
    for k in range(104):
        p = gcc_objs[k] if k < len(gcc_objs) else NOCODE[0]
        pieces.append(('.rdata', id0 + IDENT * k, id0 + IDENT * (k + 1), p, '.rdata$zzz'))
    jcr = sec['.data'][1] - 4
    pieces.append(('.data', jcr, sec['.data'][1], NAMES[93][0], '.jcr'))
    pieces.append(('.bss', COMMON[0], sec['.bss'][1], COMMON[1], '.bss'))
    for s, (p, _) in WHOLE.items():
        pieces.append((s, sec[s][0], sec[s][1], p, s))

    # ---- inferred pieces for .data/.rdata/.bss
    owner_text = []
    for s, lo, hi, p, o in pieces:
        if s == '.text':
            owner_text.append((lo, hi, p))
    owner_text.sort()
    tlos = [x[0] for x in owner_text]
    def text_owner(a):
        k = bisect.bisect_right(tlos, a) - 1
        return owner_text[k][2] if k >= 0 and a < owner_text[k][1] else None

    regions = {'.data': (sec['.data'][0], jcr), '.rdata': (rlo, id0), '.bss': (sec['.bss'][0], COMMON[0])}
    labels_at = collections.defaultdict(set)
    for i, l in enumerate(L):
        if LABEL.match(l.strip()) and secof[i] in regions:
            labels_at[secof[i]].add(pos[i])
    # refs: target address -> set of files (code) / set of source addresses (data)
    code_refs = collections.defaultdict(set)
    data_refs = collections.defaultdict(set)
    for i, l in enumerate(L):
        if pos[i] is None:
            continue
        code = l.split('#')[0]
        for m in REFADDR.finditer(code):
            t = int(m.group(1), 16)
            if secof[i] == '.text':
                o = text_owner(pos[i])
                if o:
                    code_refs[t].add(o)
            elif secof[i] in regions:
                data_refs[t].add(pos[i])
    participants = [p for p in order if p not in (LISTS[2], NOCODE[0], COMMON[1]) and p not in
                    {v[0] for v in WHOLE.values()} and p != STUBS[1] and p != CHKSTK[1]]
    pidx = {p: k for k, p in enumerate(participants)}
    # atoms of all three regions, with the files referencing them
    atoms = {}
    for s, (lo, hi) in regions.items():
        # gas pads every section to a multiple of 4, so objects start 4-aligned
        cuts = sorted({lo} | {a for a in labels_at[s] if lo < a < hi and a % 4 == 0})
        atoms[s] = list(zip(cuts, cuts[1:] + [hi]))
    flat = sorted((a0, a1, s) for s, al in atoms.items() for a0, a1 in al)
    fstarts = [a for a, _, _ in flat]
    def atom_of(v):
        k = bisect.bisect_right(fstarts, v) - 1
        return k if k >= 0 and v < flat[k][1] else None
    refset = [set() for _ in flat]
    for t, fs in code_refs.items():
        k = atom_of(t)
        if k is not None:
            refset[k] |= fs
    for _ in range(6):  # propagate through data-to-data pointers, any direction
        changed = False
        for t, srcs in data_refs.items():
            k = atom_of(t)
            if k is None:
                continue
            for a in srcs:
                j = atom_of(a)
                if j is not None and not refset[j] <= refset[k]:
                    refset[k] |= refset[j]
                    changed = True
        if not changed:
            break
    for lo, hi, p, _ in DATA_OWNERS:
        for k, (a0, a1, _s) in enumerate(flat):
            if lo <= a0 and a1 <= hi:
                refset[k] = {p}
    summary = {}
    for s, al in atoms.items():
        rsets = [refset[atom_of(a0)] for a0, _ in al]
        # DP: monotone assignment in link order, cost 1 per atom placed in a file
        # that doesn't reference it.  Ties switch files as late as possible, so
        # alignment padding stays with the object before it.
        m = len(participants)
        cost_prev = [0] * m
        back = []
        for k, (a0, a1) in enumerate(al):
            rs = {pidx[p] for p in rsets[k] if p in pidx}
            best, bj, row, ch = None, -1, [0] * m, [0] * m
            for j in range(m):
                stay = cost_prev[j]
                if bj >= 0 and best <= stay:
                    base, src = best, bj
                else:
                    base, src = stay, j
                row[j] = base + (0 if not rs or j in rs else 1)
                ch[j] = src
                if best is None or cost_prev[j] < best:
                    best, bj = cost_prev[j], j
            back.append(ch)
            cost_prev = row
        atoms_s = al
        refset_s = rsets
        j = min(range(m), key=lambda x: (cost_prev[x], x))
        assign = [0] * len(atoms_s)
        for k in range(len(atoms_s) - 1, -1, -1):
            assign[k] = j
            j = back[k][j]
        runs = []
        for k, (a0, a1) in enumerate(atoms_s):
            p = participants[assign[k]]
            if runs and runs[-1][2] == p:
                runs[-1][1] = a1
            else:
                runs.append([a0, a1, p])
        for a0, a1, p in runs:
            pieces.append((s, a0, a1, p, s))
        bad = sum(1 for k in range(len(atoms_s)) if refset_s[k] and participants[assign[k]] not in refset_s[k])
        summary[s] = (len(atoms_s), len(runs), bad)

    # ---- functions in C (mixed objects): [start, end) -> marker
    fde_len = {a: n for _, f in us for a, n in f}
    cranges = sorted((a, a + fde_len[a]) for a in C_FUNCS)
    cstarts = [a for a, _ in cranges]
    mixed = {text_owner(a) for a in C_FUNCS}
    def cfunc_at(i):
        if secof[i] != '.text' or pos[i] is None:
            return None
        k = bisect.bisect_right(cstarts, pos[i]) - 1
        return cranges[k][0] if k >= 0 and pos[i] < cranges[k][1] else None
    marked, cfunc_labels = set(), {}

    # ---- distribute lines to pieces
    by_sec = collections.defaultdict(list)
    for pc in pieces:
        by_sec[pc[0]].append(pc)
    for s in by_sec:
        by_sec[s].sort(key=lambda x: x[1])
    files = collections.defaultdict(lambda: collections.defaultdict(list))  # file -> outsec -> [(lo,hi,lines)]
    piece_lines = {pc: [] for pc in pieces}
    for i, l in enumerate(L):
        s = secof[i]
        st = l.strip()
        if s is None or SECDIR.match(st) or re.match(r'^\.align\s', st) or st.startswith('#') or not st \
                or st == '.intel_syntax noprefix' or st.startswith('.set __ImageBase'):
            continue  # __ImageBase comes from the link script instead
        lst = by_sec[s]
        k = bisect.bisect_right([x[1] for x in lst], pos[i]) - 1
        if k < 0:
            sys.exit('line %d %r at %x before first piece of %s' % (i, st, pos[i], s))
        pc = lst[k]
        if pos[i] >= pc[2] and not (pos[i] == pc[2] == sec[s][1]):
            sys.exit('line %d %r at %x not in a piece of %s' % (i, st, pos[i], s))
        cf = cfunc_at(i)
        if cf is not None:
            if cf not in marked:
                marked.add(cf)
                piece_lines[pc].append('#@C ' + SYMBOLS[cf])
            m = LABEL.match(st)
            if m and m.group(1) != 'FUN_%x' % cf:
                cfunc_labels[m.group(1)] = cf
            continue
        z = ZERO.match(l)
        if z and A[i] is not None and A[i] + int(z.group(2)) > pc[2]:
            # .zero straddling a piece boundary: split it
            a, n = A[i], int(z.group(2))
            for pc2 in lst[k:]:
                take = min(a + n, pc2[2]) - max(a, pc2[1])
                if take > 0:
                    piece_lines[pc2].append('%s.zero %d' % (z.group(1), take))
                if pc2[2] >= a + n:
                    break
            continue
        piece_lines[pc].append(l)

    # ---- real names (after the address-based analysis above)
    irename = re.compile(r'(?<![\w.$])(%s)(?![\w$])' % '|'.join(map(re.escape, IAT_NAMES)))
    rename = re.compile(r'(?<![\w.$])(?:FUN|L)_(%s)(?![\w$])' % '|'.join('%x' % a for a in SYMBOLS))
    for pc, ls in piece_lines.items():
        ls = [l if l.lstrip().startswith(('.string', '.ascii')) else
              irename.sub(lambda m: IAT_NAMES[m.group(1)], l) for l in ls]
        piece_lines[pc] = [rename.sub(lambda m: SYMBOLS[int(m.group(1), 16)], l) for l in ls]

    # gcc's labels inside a C function are its own; nothing else may use ours
    for pc, ls in piece_lines.items():
        for l in ls:
            for t in SYM.findall(l.split('#')[0]):
                if t in cfunc_labels:
                    sys.exit('%s (inside C function at %x) is referenced from %s: %r'
                             % (t, cfunc_labels[t], pc[3], l))

    # ---- globals: labels referenced from another file
    defined = {}
    used = collections.defaultdict(set)
    for pc, ls in piece_lines.items():
        for l in ls:
            m = LABEL.match(l.strip())
            if m:
                defined[m.group(1)] = pc[3]
            for t in SYM.findall(l.split('#')[0]):
                used[pc[3]].add(t)
    need_global = collections.defaultdict(set)
    for f, syms in used.items():
        for t in syms:
            if t in defined and defined[t] != f:
                need_global[defined[t]].add(t)
    # SYMBOLS names are there for the C objects, whose references aren't seen
    for t in SYMBOLS.values():
        if t in defined:
            need_global[defined[t]].add(t)

    # ---- write
    secname = {'.eh_fram': '.eh_frame'}
    written = []
    for f in order:
        mine = [pc for pc in pieces if pc[3] == f and piece_lines[pc]]
        if not mine:
            continue
        if os.path.exists(os.path.join(outdir, f + '.c')) and f not in mixed:
            written.append(f)   # rebuilt from C source; keep it in the link order
            continue
        out =['# %s.s -- %s' % (f, info[f]), '#']
        if f in mixed:
            out += ['# mixed: `#@C name` lines are functions from %s.c (re/splice.py)' %
                    os.path.basename(f), '#']
        out.append('# original placement:')
        for pc in sorted(mine, key=lambda x: (x[0], x[1])):
            out.append('#   %-14s %08x-%08x' % (pc[4], pc[1], pc[2]))
        out += ['', '.intel_syntax noprefix']
        globs = sorted(need_global.get(f, ()))
        for g in globs:
            out.append('.globl ' + g)
        for pc in sorted(mine, key=lambda x: (list(OUT).index(x[4]), x[1])):
            directive, cap = OUT[pc[4]]
            al = min(cap, lowbit(pc[1]), lowbit(pc[2]))
            out += ['', directive, '.p2align %d' % (al.bit_length() - 1)]
            out += piece_lines[pc]
        path = os.path.join(outdir, f + '.s')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
        written.append(f)
    open(os.path.join(outdir, 'objects.txt'), 'w', newline='\n').write(
        '# link order (one object per line), generated by re/split.py\n' + '\n'.join(written) + '\n')
    for s, (na, nr, bad) in summary.items():
        print('%-6s %5d atoms -> %3d pieces, %d atoms outside their referencing object' % (s, na, nr, bad))
    print('%d files' % len(written))


if __name__ == '__main__':
    main()

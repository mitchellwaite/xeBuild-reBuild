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
    # runtime functions the C code calls
    0x448760: '__assert',       # libmingwex wassert.o
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
    0x449058: '_strrchr', 0x4490a0: '_signal', 0x449258: '__chdir',
    0x4491d0: '_strnicmp', 0x4491d8: '_stricmp', 0x449198: '_exit', 0x449178: '_fgetc',
    # IAT slots that dllimport declarations reference directly
    0x50f2f0: '__imp___errno',
}
# IAT slot labels (ddfix names them after the import) that clash with a
# SYMBOLS name: msvcrt's `_strnicmp`/`_exit` slots vs the stubs for strnicmp/exit.
IAT_NAMES = {'_strnicmp': '__imp___strnicmp', '_exit': '__imp___exit',
             '_stricmp': '__imp___stricmp'}
# Functions already in C inside objects that are otherwise still assembly
# (mixed objects).  Their range in the .s becomes a `#@C <name>` marker that
# build.sh fills from `gcc -S` of src/<obj>.c (re/splice.py); data, the
# ident and .eh_frame stay in the .s.  Names come from SYMBOLS.
C_FUNCS = {
    0x40aa10,   # app/filelist_ini getIniValue
    # app/options (parseButton stays asm: its ipa-split part at 449640 is
    # called from asm, and gcc would put it in .text.unlikely)
    0x4236f0,                                # baseFileExists.part.0
    0x423730, 0x423750, 0x423830, 0x424170,  # baseFileExists perboxExists iniConsoleType setConsoleType
    0x424a10, 0x424b20, 0x424b60, 0x424bb0,  # optIniInt stripColons macidSet setBoolOption
    0x427000, 0x4271a0, 0x427260,            # parseRawPatch parseRawPatches addPatch
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
        ls = [irename.sub(lambda m: IAT_NAMES[m.group(1)], l) for l in ls]
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

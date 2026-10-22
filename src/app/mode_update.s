# app/mode_update.s -- "Usage: %s update", bad block handling
#
# mixed: `#@C name` lines are functions from mode_update.c (re/splice.py)
#
# original placement:
#   .bss           0046f040-0046f160
#   .data          0044a008-0044a020
#   .eh_frame      00465650-0046599c
#   .rdata         0044c6e8-0044deb8
#   .rdata$zzz     004637a4-004637d0
#   .text          004030b0-00405610

.intel_syntax noprefix
.globl _clean
.globl _hasHdd
.globl _info
.globl _mu_44c6e8
.globl _mu_44c70c
.globl _mu_44c730
.globl _mu_44c74c
.globl _mu_44c76c
.globl _mu_44c7ab
.globl _mu_44c7b4
.globl _mu_44c7e1
.globl _mu_44c7ec
.globl _mu_44c810
.globl _mu_44c844
.globl _mu_44c850
.globl _mu_44c888
.globl _mu_44c8ca
.globl _mu_44c8e8
.globl _mu_44c918
.globl _mu_44c95c
.globl _mu_44c9a8
.globl _mu_44c9e8
.globl _mu_44ca2c
.globl _mu_44ca74
.globl _mu_44cac8
.globl _mu_44cb18
.globl _mu_44cb58
.globl _mu_44cb90
.globl _mu_44cbb0
.globl _mu_44cbbc
.globl _mu_44cc04
.globl _mu_44cc58
.globl _mu_44ccc8
.globl _mu_44cd14
.globl _mu_44cd6c
.globl _mu_44cdc0
.globl _mu_44cddb
.globl _mu_44cde8
.globl _mu_44cdf4
.globl _mu_44ce08
.globl _mu_44ce21
.globl _mu_44ce40
.globl _mu_44ce9c
.globl _mu_44cea3
.globl _mu_44cebc
.globl _mu_44ced0
.globl _mu_44cf18
.globl _mu_44cf6c
.globl _mu_44cfac
.globl _mu_44cfd4
.globl _mu_44cfe1
.globl _mu_44cff0
.globl _mu_44d009
.globl _mu_44d010
.globl _mu_44d054
.globl _mu_44d074
.globl _mu_44d090
.globl _mu_44d0d4
.globl _mu_44d0f8
.globl _mu_44d12c
.globl _mu_44d144
.globl _mu_44d171
.globl _mu_44d186
.globl _mu_44d198
.globl _mu_44d1d3
.globl _mu_44d1db
.globl _mu_44d1f4
.globl _mu_44d21c
.globl _mu_44d23d
.globl _mu_44d257
.globl _mu_44d25e
.globl _mu_44d278
.globl _mu_44d2ae
.globl _mu_44d2c1
.globl _mu_44d2c8
.globl _mu_44d300
.globl _mu_44d339
.globl _mu_44d354
.globl _mu_44d35c
.globl _mu_44d377
.globl _mu_44d385
.globl _mu_44d390
.globl _mu_44d3c8
.globl _mu_44d400
.globl _mu_44d424
.globl _mu_44d440
.globl _mu_44d46e
.globl _mu_44d479
.globl _mu_44d484
.globl _mu_44d4b9
.globl _mu_44d4c5
.globl _mu_44d4cc
.globl _mu_44d4fc
.globl _mu_44d528
.globl _mu_44d55c
.globl _mu_44d590
.globl _mu_44d5ba
.globl _mu_44d5d4
.globl _mu_44d5f7
.globl _mu_44d5fe
.globl _mu_44d603
.globl _mu_44d606
.globl _mu_44d609
.globl _mu_44d614
.globl _mu_44d63a
.globl _mu_44d640
.globl _mu_44d68a
.globl _mu_44d6a3
.globl _mu_44d6a8
.globl _mu_44d6f4
.globl _mu_44d73a
.globl _mu_44d740
.globl _mu_44d78c
.globl _mu_44d7e3
.globl _mu_44d7e7
.globl _mu_44d7ec
.globl _mu_44d840
.globl _mu_44d882
.globl _mu_44d88c
.globl _mu_44d8c8
.globl _mu_44d8d0
.globl _mu_44d910
.globl _mu_44d918
.globl _mu_44d950
.globl _mu_44d958
.globl _mu_44d9c7
.globl _mu_44d9ca
.globl _mu_44d9d0
.globl _mu_44da21
.globl _mu_44da3d
.globl _mu_44da40
.globl _mu_44da91
.globl _mu_44da98
.globl _mu_44dac6
.globl _mu_44dad0
.globl _mu_44db0e
.globl _mu_44db21
.globl _mu_44db26
.globl _mu_44db30
.globl _mu_44db58
.globl _mu_44db7c
.globl _mu_44dba0
.globl _mu_44dbcc
.globl _mu_44dbfc
.globl _mu_44dc2c
.globl _mu_44dc54
.globl _mu_44dca8
.globl _mu_44dcf8
.globl _mu_44dd40
.globl _mu_44dd67
.globl _mu_44dd80
.globl _mu_44ddc0
.globl _mu_44de04
.globl _mu_44de38
.globl _mu_44de80
.globl _noAvatar
.globl _noReboot
.globl _noWrite
.globl _path
.globl _updating
.globl _useConsoleAddons

.text
.p2align 4
#@C _getBadBlocks
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
#@C _update_usage
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _wantFile
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _parseAddonIdx
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8d
          .byte 0xbc
          .byte 0x27
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _getAddons
          .byte 0x8d
          .byte 0x76
          .byte 0x0
#@C _getMobileFiles
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8d
          .byte 0xbc
          .byte 0x27
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _bldrGetKv
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
#@C _bldrGetSmc
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
#@C _getSecurityFiles
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _checkBadBlocks
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
          .byte 0x8d
          .byte 0xbc
          .byte 0x27
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _getBootloaders
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _getConsoleFiles
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
          .byte 0x8d
          .byte 0xbc
          .byte 0x27
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _updateGetFile
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
#@C _mode_update
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop

.data
.p2align 3
_useConsoleAddons:
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0

.section .rdata,"dr"
.p2align 3
_mu_44c6e8:
          .string "\n------ getting bad blocks ------\n"
          .zero 1
_mu_44c70c:
          .string "processing %d bad blocks on device\n"
_mu_44c730:
          .string "marking bad block at 0x%x\n"
          .zero 1
_mu_44c74c:
          .string "no bad blocks found on device\n"
          .zero 1
_mu_44c76c:
          .string "\n\n***** ERROR: unable to retrieve bad block list from device!\n"
_mu_44c7ab:
          .string "xeBuild"
          .zero 1
_mu_44c7b4:
          .string "Usage   :\n   %s update <switch> [<option>]\n\n"
_mu_44c7e1:
          .string "Examples:\n"
_mu_44c7ec:
          .string "   %s update -f 16197 -a nofcrt\n"
          .zero 3
_mu_44c810:
          .string "   %s update -f 16203 -d myflash -ip 192.168.2.100\n"
_mu_44c844:
          .string "\nSwitches:\n"
_mu_44c850:
          .string "   -f <dir> : use different data dir and file lists\n"
          .zero 3
_mu_44c888:
          .string "   -d <dir> : dumps NAND and other data to <dir> before flashing\n"
_mu_44c8ca:
          .string "   -a <name>: append patches\n"
_mu_44c8e8:
          .string "   -ip <add>: force attempt to connect to addr\n"
_mu_44c918:
          .string "   -i <ext> : adds _<ext> into firmware ini and patches file names\n"
_mu_44c95c:
          .string "   -r <ext> : adds _<ext> into ini bl section name and patches file names\n"
          .zero 1
_mu_44c9a8:
          .string "   -nowrite : will not write anything to console flash or HDD\n"
          .zero 1
_mu_44c9e8:
          .string "              without -d results of update are not kept anywhere\n"
          .zero 2
_mu_44ca2c:
          .string "   -noava   : will not send avatar data if available and HDD present\n"
          .zero 2
_mu_44ca74:
          .string "   -clean   : secdata, extended and statistics will not be retrieved from console\n"
          .zero 1
_mu_44cac8:
          .string "   -noreeb  : do not automatically reboot console after writes are completed\n"
          .zero 2
_mu_44cb18:
          .string "   -noenter : suppresses prompt for enter key when finished\n"
          .zero 3
_mu_44cb58:
          .string "   -v       : shows more info during update process\n"
          .zero 3
_mu_44cb90:
          .string "   -?       : shows this help\n\n"
_mu_44cbb0:
          .string "legend:\n"
          .zero 3
_mu_44cbbc:
          .string "<name>      = name.bin contents will be appended to hv/kernel patches\n\n"
_mu_44cc04:
          .string "<dir>       = path, absolute or relative, to a directory - do not terminate with \\\n"
_mu_44cc58:
          .string "<ext>       = using this option would cause the builder to look for _glitch_<ext>.ini instead of _glitch.ini\n"
          .zero 2
_mu_44ccc8:
          .string "              and patches_jasper_<ext>.bin instead of patches_jasper.bin\n"
          .zero 2
_mu_44cd14:
          .string "<add>       = without this option network will be scanned for server broadcast beacon\n"
          .zero 1
_mu_44cd6c:
          .string "              If provided the correct format is an IPv4 address like 192.168.0.100\n"
_mu_44cdc0:
          .string "\npress <enter> to quit...\n"
_mu_44cddb:
          .string "extended.bin"
_mu_44cde8:
          .string "secdata.bin"
_mu_44cdf4:
          .string "Statistics.settings"
_mu_44ce08:
          .string "skipping %s, -clean flag"
_mu_44ce21:
          .string "addon patch from console: %s\n"
          .zero 1
_mu_44ce40:
          .string "***** WARNING: exceeded total number of optional patches while processing %s from console!\n"
_mu_44ce9c:
          .string "addons"
_mu_44cea3:
          .string "OK, received 0x%x bytes\n"
_mu_44cebc:
          .string ".\\%d\\bin\\addon.idx"
          .zero 1
_mu_44ced0:
          .string "\n\n***** WARNING: unable to open %s to parse addons.bin from console!\n"
          .zero 2
_mu_44cf18:
          .string "\n\n***** WARNING: addons.bin from console is not a multiple of 4 bytes! Skipping!\n"
          .zero 2
_mu_44cf6c:
          .string "\n\n***** WARNING: Unable to retrieve addons.bin from console!\n"
          .zero 2
_mu_44cfac:
          .string "\n------ getting mobile settings ------\n"
_mu_44cfd4:
          .string "Mobile%c.dat"
_mu_44cfe1:
          .string "not available\n"
_mu_44cff0:
          .string "retrieving USVR\\blmod..."
_mu_44d009:
          .string "blmod"
          .zero 1
_mu_44d010:
          .string "\n\n***** WARNING: Unable to retrieve blmod.bin data from console!\n"
          .zero 2
_mu_44d054:
          .string "console has no available blmod\n"
_mu_44d074:
          .string "retrieving USVR\\addons..."
          .zero 2
_mu_44d090:
          .string "skipping USVR\\addons, addons have been specified on command line\n"
          .zero 2
_mu_44d0d4:
          .string "console has no available addons\n"
          .zero 3
_mu_44d0f8:
          .string "retrieving USVR\\Static.settings (smc_config.bin)..."
_mu_44d12c:
          .string "usv:\\Static.settings"
          .zero 3
_mu_44d144:
          .string "OK, received 0x%x bytes\n        verifying..."
_mu_44d171:
          .string "smc_config is good!\n"
_mu_44d186:
          .string "smc_config.bin"
          .zero 3
_mu_44d198:
          .string "\n***** ERROR: could not retrieve smc_config from console!\n"
_mu_44d1d3:
          .string "usv:\\%s"
_mu_44d1db:
          .string "retrieving USVR\\%s..."
          .zero 3
_mu_44d1f4:
          .string "\n------ getting security files ------\n"
          .zero 1
_mu_44d21c:
          .string "OK, received 0x%x bytes\n        "
_mu_44d23d:
          .string "retrieving USVR\\kv_enc..."
_mu_44d257:
          .string "kv_enc"
_mu_44d25e:
          .string "extracting BLDR\\kv_enc..."
_mu_44d278:
          .string "OK, received 0x%x bytes\n        decrypt and verify..."
_mu_44d2ae:
          .string "keyvault is good!\n"
_mu_44d2c1:
          .string "kv.bin"
_mu_44d2c8:
          .string "\n***** ERROR: could not decrypt keyvault from console!\n"
_mu_44d300:
          .string "\n***** ERROR: could not retrieve keyvault from console!\n"
_mu_44d339:
          .string "retrieving USVR\\smc_enc..."
_mu_44d354:
          .string "smc_enc"
_mu_44d35c:
          .string "extracting BLDR\\smc_enc..."
_mu_44d377:
          .string "smc is good!\n"
_mu_44d385:
          .string "smc.bin"
          .zero 3
_mu_44d390:
          .string "\n***** ERROR: could not decrypt smc.bin from console!\n"
          .zero 1
_mu_44d3c8:
          .string "\n***** ERROR: could not retrieve smc.bin from console!\n"
_mu_44d400:
          .string "\n------ getting bootloaders ------\n"
_mu_44d424:
          .string "reading bootloader data..."
          .zero 1
_mu_44d440:
          .string "success! Bootloader size with xell is 0x%08x\n"
_mu_44d46e:
          .string "fbldrs.bin"
_mu_44d479:
          .string "failed!\n"
          .zero 2
_mu_44d484:
          .string "Skipping getting bootloaders on non-glitch machine!\n"
_mu_44d4b9:
          .string "\\SystemRoot"
_mu_44d4c5:
          .string "usv"
          .zero 3
_mu_44d4cc:
          .string "\n***** ERROR: getting raw boot loaders failed!\n"
_mu_44d4fc:
          .string "\n***** ERROR: getting mobile files failed!\n"
_mu_44d528:
          .string "\n***** ERROR: retrieving security files failed!\n"
          .zero 3
_mu_44d55c:
          .string "\n***** ERROR: mounting remote SystemRoot failed!\n"
          .zero 2
_mu_44d590:
          .string "\n***** ERROR: getting bad blocks failed!\n"
_mu_44d5ba:
          .string "failed! received 0 bytes\n"
_mu_44d5d4:
          .string "failed! file not found on console\n"
_mu_44d5f7:
          .string "update"
_mu_44d5fe:
          .string "help"
_mu_44d603:
          .string "-?"
_mu_44d606:
          .string "/?"
_mu_44d609:
          .string "-noenter"
          .zero 2
_mu_44d614:
          .string "<enter> key on completion suppressed\n"
_mu_44d63a:
          .string "-ip"
          .zero 2
_mu_44d640:
          .string "\n\n***** ERROR: option flag -ip on command line but no argument provided!\n"
_mu_44d68a:
          .string "setting forced IP to %s\n"
_mu_44d6a3:
          .string "-a"
          .zero 2
_mu_44d6a8:
          .string "\n\n***** ERROR: option flag -a on command line but no argument provided!\n"
          .zero 3
_mu_44d6f4:
          .string "***** WARNING: exceeded total number of optional patches with -a %s!\n"
_mu_44d73a:
          .string "-r"
          .zero 3
_mu_44d740:
          .string "\n\n***** ERROR: option flag -r on command line but no argument provided!\n"
          .zero 3
_mu_44d78c:
          .string "***** WARNING: option flag -r %s on command line replacing previous setting of -r %s!\n"
_mu_44d7e3:
          .string "_%s"
_mu_44d7e7:
          .string "-i"
          .zero 2
_mu_44d7ec:
          .string "\n\n***** ERROR: data directory flag -i on command line but no argument provided!\n"
          .zero 3
_mu_44d840:
          .string "suffix '%s' added from command line to ini and patches filenames\n"
_mu_44d882:
          .string "-nowrite"
          .zero 1
_mu_44d88c:
          .string "-nowrite: flash image and avatars will not be sent to xbox\n"
_mu_44d8c8:
          .string "-noava"
          .zero 1
_mu_44d8d0:
          .string "-noava: avatar data, if available, will not be sent to console\n"
_mu_44d910:
          .string "-noreeb"
_mu_44d918:
          .string "-noreeb: console will not reboot after writes are done\n"
_mu_44d950:
          .string "-clean"
          .zero 1
_mu_44d958:
          .string "-clean: secdata, extended and statistics will not be retrieved from console, builder will make clean versions\n"
_mu_44d9c7:
          .string "-v"
_mu_44d9ca:
          .string "-d"
          .zero 3
_mu_44d9d0:
          .string "\n\n***** ERROR: dump directory flag -d on command line but no argument provided!\n"
_mu_44da21:
          .string "dump directory set to '%s'\n"
_mu_44da3d:
          .string "-f"
_mu_44da40:
          .string "\n\n***** ERROR: data directory flag -f on command line but no argument provided!\n"
_mu_44da91:
          .string "%s\\"
          .zero 3
_mu_44da98:
          .string "data directory set from command line to '%s'\n"
_mu_44dac6:
          .string "%s\\bin\\"
          .zero 2
_mu_44dad0:
          .string "\n\n***** ERROR: unknown option '%s' provided on command line!\n"
_mu_44db0e:
          .string "Dumping disabled!\n"
_mu_44db21:
          .string "%s%s"
_mu_44db26:
          .string "%s_update"
_mu_44db30:
          .string "\n------ dumping console flash ------\n"
          .zero 2
_mu_44db58:
          .string "\n------ flashing console ------\n"
          .zero 3
_mu_44db7c:
          .string "sending flash data to console...\n"
          .zero 2
_mu_44dba0:
          .string "flashing console skipped, -nowrite used\n"
          .zero 3
_mu_44dbcc:
          .string "\n------ loading and sending avatar data ------\n"
_mu_44dbfc:
          .string "avatar data skipped, -noava or -nowrite used\n"
          .zero 2
_mu_44dc2c:
          .string "avatar data skipped, no HDD detected\n"
          .zero 2
_mu_44dc54:
          .string "\n***** WARNING: due to previous possible errors, console reboot is not being done\n"
          .zero 1
_mu_44dca8:
          .string "               it is not recommended to use update mode on this console again\n"
          .zero 1
_mu_44dcf8:
          .string "               until you have determined it's got a good image on it\n\n"
          .zero 1
_mu_44dd40:
          .string "\n\n***** ERROR: %i writing to file %s\n\n"
_mu_44dd67:
          .string "%s image built, info:\n"
          .zero 2
_mu_44dd80:
          .string "\n\n***** FATAL UPDATE ERROR: %i unable to complete NAND image\n\n"
          .zero 1
_mu_44ddc0:
          .string "\n\n***** FATAL UPDATE ERROR: unable to get console unique files\n\n"
          .zero 3
_mu_44de04:
          .string "\n\n***** FATAL UPDATE ERROR: unable to parse %s\n\n"
          .zero 3
_mu_44de38:
          .string "\n\n***** FATAL UPDATE ERROR: unable to parse info reply from console!\n\n"
          .zero 1
_mu_44de80:
          .string "\n\n***** FATAL UPDATE ERROR: unable to find console!\n\n"
          .zero 2

.section .rdata$zzz,"dr"
.p2align 2
          .byte 0x47
          .byte 0x43
          .byte 0x43
          .byte 0x3a
          .byte 0x20
          .byte 0x28
          .byte 0x52
          .byte 0x65
          .byte 0x76
          .byte 0x32
          .byte 0x2c
          .byte 0x20
          .byte 0x42
          .byte 0x75
          .byte 0x69
          .byte 0x6c
          .byte 0x74
          .byte 0x20
          .byte 0x62
          .byte 0x79
          .byte 0x20
          .byte 0x4d
          .byte 0x53
          .byte 0x59
          .byte 0x53
          .byte 0x32
          .byte 0x20
          .byte 0x70
          .byte 0x72
          .byte 0x6f
          .byte 0x6a
          .byte 0x65
          .byte 0x63
          .byte 0x74
          .byte 0x29
          .byte 0x20
          .byte 0x36
          .byte 0x2e
          .byte 0x32
          .byte 0x2e
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0

.section .eh_frame,"dr"
.p2align 2
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1
          .byte 0x7a
          .byte 0x52
          .byte 0x0
          .byte 0x1
          .byte 0x7c
          .byte 0x8
          .byte 0x1
          .byte 0x1b
          .byte 0xc
          .byte 0x4
          .byte 0x4
          .byte 0x88
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _getBadBlocks - .
          .byte 0x1b
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x85
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x87
          .byte 0x3
          .byte 0x41
          .byte 0xe
          .byte 0x10
          .byte 0x86
          .byte 0x4
          .byte 0x41
          .byte 0xe
          .byte 0x14
          .byte 0x83
          .byte 0x5
          .byte 0x43
          .byte 0xe
          .byte 0x40
          .byte 0x2
          .byte 0x56
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc5
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x5c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _update_usage - .
          .byte 0x88
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x70
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _wantFile - .
          .byte 0x89
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x53
          .byte 0xe
          .byte 0x20
          .byte 0x79
          .byte 0xa
          .byte 0xe
          .byte 0x4
          .byte 0x44
          .byte 0xb
          .byte 0x78
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x90
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _parseAddonIdx - .
          .byte 0x2
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x85
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x87
          .byte 0x3
          .byte 0x41
          .byte 0xe
          .byte 0x10
          .byte 0x86
          .byte 0x4
          .byte 0x41
          .byte 0xe
          .byte 0x14
          .byte 0x83
          .byte 0x5
          .byte 0x4b
          .byte 0xe
          .byte 0xc0
          .byte 0x8
          .byte 0x2
          .byte 0xac
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc5
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x3
          .byte 0x36
          .byte 0x1
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc5
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x48
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xe8
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _getAddons - .
          .byte 0x1d
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x87
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x86
          .byte 0x3
          .byte 0x41
          .byte 0xe
          .byte 0x10
          .byte 0x83
          .byte 0x4
          .byte 0x46
          .byte 0xe
          .byte 0xb0
          .byte 0x8
          .byte 0x2
          .byte 0x54
          .byte 0xa
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x2
          .byte 0x99
          .byte 0xa
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x4
          .byte 0x43
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x40
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x34
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _getMobileFiles - .
          .byte 0xc3
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x85
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x87
          .byte 0x3
          .byte 0x46
          .byte 0xe
          .byte 0x10
          .byte 0x86
          .byte 0x4
          .byte 0x41
          .byte 0xe
          .byte 0x14
          .byte 0x83
          .byte 0x5
          .byte 0x4a
          .byte 0xe
          .byte 0x80
          .byte 0x1
          .byte 0x3
          .byte 0x1c
          .byte 0x3
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc5
          .byte 0xe
          .byte 0x4
          .byte 0x4b
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x78
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _bldrGetKv - .
          .byte 0x8b
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x87
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x86
          .byte 0x3
          .byte 0x41
          .byte 0xe
          .byte 0x10
          .byte 0x83
          .byte 0x4
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x2
          .byte 0x7f
          .byte 0xe
          .byte 0x10
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xac
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _bldrGetSmc - .
          .byte 0x8b
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x87
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x86
          .byte 0x3
          .byte 0x41
          .byte 0xe
          .byte 0x10
          .byte 0x83
          .byte 0x4
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x2
          .byte 0x7f
          .byte 0xe
          .byte 0x10
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x6c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xe0
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _getSecurityFiles - .
          .byte 0x8
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x85
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x87
          .byte 0x3
          .byte 0x43
          .byte 0xe
          .byte 0x10
          .byte 0x86
          .byte 0x4
          .byte 0x41
          .byte 0xe
          .byte 0x14
          .byte 0x83
          .byte 0x5
          .byte 0x4d
          .byte 0xe
          .byte 0x30
          .byte 0x3
          .byte 0x63
          .byte 0x1
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc5
          .byte 0xe
          .byte 0x4
          .byte 0x44
          .byte 0xb
          .byte 0x3
          .byte 0x8f
          .byte 0x1
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc5
          .byte 0xe
          .byte 0x4
          .byte 0x4b
          .byte 0xb
          .byte 0x2
          .byte 0x97
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc5
          .byte 0xe
          .byte 0x4
          .byte 0x43
          .byte 0xb
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x50
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long _checkBadBlocks - .
          .byte 0x15
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x24
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x64
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long _getBootloaders - .
          .byte 0xe9
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x79
          .byte 0xa
          .byte 0xe
          .byte 0x4
          .byte 0x44
          .byte 0xb
          .byte 0x2
          .byte 0x4b
          .byte 0xa
          .byte 0xe
          .byte 0x4
          .byte 0x45
          .byte 0xb
          .byte 0x2
          .byte 0x58
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x24
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8c
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long _getConsoleFiles - .
          .byte 0xc5
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x2
          .byte 0xc3
          .byte 0xa
          .byte 0xe
          .byte 0x4
          .byte 0x4a
          .byte 0xb
          .byte 0x59
          .byte 0xa
          .byte 0xe
          .byte 0x4
          .byte 0x47
          .byte 0xb
          .byte 0x2
          .byte 0x7f
          .byte 0xa
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb4
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long _updateGetFile - .
          .byte 0x6b
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x85
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x87
          .byte 0x3
          .byte 0x41
          .byte 0xe
          .byte 0x10
          .byte 0x86
          .byte 0x4
          .byte 0x41
          .byte 0xe
          .byte 0x14
          .byte 0x83
          .byte 0x5
          .byte 0x46
          .byte 0xe
          .byte 0xc0
          .byte 0x2
          .byte 0x2
          .byte 0xd9
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc5
          .byte 0xe
          .byte 0x4
          .byte 0x49
          .byte 0xb
          .byte 0x67
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x46
          .byte 0xc3
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc5
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x40
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long _mode_update - .
          .byte 0x97
          .byte 0xe
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x85
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x87
          .byte 0x3
          .byte 0x46
          .byte 0xe
          .byte 0x10
          .byte 0x86
          .byte 0x4
          .byte 0x41
          .byte 0xe
          .byte 0x14
          .byte 0x83
          .byte 0x5
          .byte 0x4c
          .byte 0xe
          .byte 0xc0
          .byte 0x20
          .byte 0x3
          .byte 0xd
          .byte 0x2
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc5
          .byte 0xe
          .byte 0x4
          .byte 0x4a
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0

.bss
.p2align 5
_path:
          .zero 4
L_46f044:
          .zero 4
L_46f048:
          .zero 4
L_46f04c:
          .zero 4
L_46f050:
          .zero 244
_noReboot:
          .zero 4
_noAvatar:
          .zero 4
_noWrite:
          .zero 4
_clean:
          .zero 4
_hasHdd:
          .zero 4
_updating:
          .zero 4
_info:
          .zero 4

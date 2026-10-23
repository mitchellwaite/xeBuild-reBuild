# app/options.s -- console types (xenon...corona), command line options; startup fn
#
# mixed: `#@C name` lines are functions from options.c (re/splice.py)
#
# original placement:
#   .eh_frame      00469d48-0046a23c
#   .rdata         00457df0-00458ca4
#   .rdata$zzz     00463abc-00463ae8
#   .text          004236f0-00427500
#   .text.startup  00449640-00449790

.intel_syntax noprefix
.globl _msg_cfldvTooLarge
.globl _msg_ctype_corona
.globl _msg_ctype_corona4g
.globl _msg_ctype_coronabb
.globl _msg_ctype_coronabigffs
.globl _msg_ctype_falcon
.globl _msg_ctype_jasper
.globl _msg_ctype_jasperbb
.globl _msg_ctype_jaspersb
.globl _msg_ctype_trinity
.globl _msg_ctype_trinitybb
.globl _msg_ctype_trinitybigffs
.globl _msg_ctype_winchester
.globl _msg_ctype_winchester4g
.globl _msg_ctype_winchesterbb
.globl _msg_ctype_winchesterbigffs
.globl _msg_ctype_xenon
.globl _msg_ctype_zephyr
.globl _msg_dualbootIgnored
.globl _msg_iniCfldvTooLarge
.globl _msg_iniInvalid
.globl _msg_iniMacidBadChars
.globl _msg_iniMacidBadLength
.globl _msg_iniMacidDiscard
.globl _msg_macidBadLength
.globl _msg_macidBadValues
.globl _msg_optBadValue
.globl _msg_optIncomplete
.globl _msg_optIni
.globl _msg_optNoValue
.globl _msg_optPerbox
.globl _msg_optUnknownValue
.globl _msg_opt_avregion
.globl _msg_opt_cfldv
.globl _msg_opt_cpufan
.globl _msg_opt_cputemp
.globl _msg_opt_cygnos
.globl _msg_opt_demon
.globl _msg_opt_dualboot
.globl _msg_opt_dvdregion
.globl _msg_opt_edramtemp
.globl _msg_opt_gameregion
.globl _msg_opt_gpufan
.globl _msg_opt_gputemp
.globl _msg_opt_macid
.globl _msg_opt_nandmu
.globl _msg_opt_nodvd
.globl _msg_opt_noecdremap
.globl _msg_opt_nomobile
.globl _msg_opt_noremap
.globl _msg_opt_nosecurity
.globl _msg_opt_olddvd
.globl _msg_opt_overcputemp
.globl _msg_opt_overedramtemp
.globl _msg_opt_overgputemp
.globl _msg_opt_patchsmc
.globl _msg_opt_smcnoblink
.globl _msg_opt_smcnocheck
.globl _msg_opt_smcnoeject
.globl _msg_opt_xellbutton
.globl _msg_opt_xellbutton2
.globl _msg_patchDuplicate
.globl _msg_patchParseFailed
.globl _msg_patchTooMany
.globl _msg_rawPatchBadOffset
.globl _msg_rawPatchParsed
.globl _msg_rawPatchSlotsFull
.globl _msg_xellAltDisabled
.globl _msg_xellDefault
.globl _str_addon
.globl _str_avregion
.globl _str_binFmt
.globl _str_cfldv
.globl _str_colon
.globl _str_corona
.globl _str_corona4g
.globl _str_coronabb
.globl _str_coronabigffs
.globl _str_cpufan
.globl _str_cputemp
.globl _str_cygnos
.globl _str_demon
.globl _str_dualboot
.globl _str_dvdkey
.globl _str_dvdregion
.globl _str_edramtemp
.globl _str_eject
.globl _str_falcon
.globl _str_false
.globl _str_gameregion
.globl _str_gpufan
.globl _str_gputemp
.globl _str_hex02
.globl _str_jasper
.globl _str_jasper256
.globl _str_jasper512
.globl _str_jasperbb
.globl _str_jasperbc
.globl _str_jasperbigffs
.globl _str_jaspersb
.globl _str_kiosk
.globl _str_macid
.globl _str_nandmu
.globl _str_nl
.globl _str_nodvd
.globl _str_noecdremap
.globl _str_nomobile
.globl _str_noremap
.globl _str_nosecurity
.globl _str_nosusecurity
.globl _str_olddvd
.globl _str_overcputemp
.globl _str_overedramtemp
.globl _str_overgputemp
.globl _str_patchsmc
.globl _str_power
.globl _str_remopower
.globl _str_remox
.globl _str_rev
.globl _str_revSuffix
.globl _str_smcnoblink
.globl _str_smcnocheck
.globl _str_smcnoeject
.globl _str_trinity
.globl _str_trinitybb
.globl _str_trinitybigffs
.globl _str_true
.globl _str_winbutton
.globl _str_winchester
.globl _str_winchester4g
.globl _str_winchesterbb
.globl _str_winchesterbigffs
.globl _str_wiredx
.globl _str_wiredxb1
.globl _str_wiredxb2
.globl _str_wiredxb3
.globl _str_wiredxf1
.globl _str_wiredxf2
.globl _str_wirelessx
.globl _str_xellbutton
.globl _str_xellbutton2
.globl _str_xenon
.globl _str_zephyr

.text
.p2align 4
#@C _baseFileExists.part.0
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
#@C _baseFileExists
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
#@C _perboxExists
          .byte 0x66
          .byte 0x90
#@C _iniConsoleType
          .byte 0x8d
          .byte 0x76
          .byte 0x0
#@C _setConsoleType
          .byte 0x90
#@C _optIniBool
          .byte 0x66
          .byte 0x90
#@C _optIniInt
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
#@C _parseButton
          .byte 0x66
          .byte 0x90
#@C _stripColons
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
#@C _macidSet
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
#@C _setBoolOption
#@C _parseOption
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _parseCmdOptions
L_425991:
          jmp _applyIniOptions
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
#@C _applyIniOptions
          .byte 0x90
#@C _parseRawPatch
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
#@C _parseRawPatches
L_427251:
          jmp _addPatch
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
#@C _addPatch
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _loadAddons
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90

.section .text.startup,"xr"
.p2align 4
#@C _parseButton.part.0
          .byte 0x90
          .byte 0x90
          .byte 0x66
          .byte 0x90
          .byte 0x66
          .byte 0x90
          .byte 0x66
          .byte 0x90
          .byte 0x66
          .byte 0x90
          .byte 0x66
          .byte 0x90
          .byte 0x66   # nop
          nop

.section .rdata,"dr"
.p2align 2
_str_wirelessx:
          .string "wirelessx"
_str_wiredx:
          .string "wiredx"
_str_wiredxb1:
          .string "wiredxb1"
_str_wiredxb2:
          .string "wiredxb2"
_str_wiredxb3:
          .string "wiredxb3"
_str_wiredxf1:
          .string "wiredxf1"
_str_wiredxf2:
          .string "wiredxf2"
_str_eject:
          .string "eject"
_str_kiosk:
          .string "kiosk"
_str_xenon:
          .string "xenon"
_msg_ctype_xenon:
          .string "Using xenon ctype (perbox file)\n"
_str_zephyr:
          .string "zephyr"
_msg_ctype_zephyr:
          .string "Using zephyr ctype (perbox file)\n"
_str_falcon:
          .string "falcon"
          .zero 3
_msg_ctype_falcon:
          .string "Using falcon ctype (perbox file)\n"
_str_jasper:
          .string "jasper"
_str_jasperbc:
          .string "jasperbc"
          .zero 2
_msg_ctype_jasper:
          .string "Using jasper ctype (perbox file)\n"
_str_jaspersb:
          .string "jaspersb"
          .zero 1
_msg_ctype_jaspersb:
          .string "Using jasper smallblock ctype (perbox file)\n"
_str_jasperbb:
          .string "jasperbb"
          .zero 2
_msg_ctype_jasperbb:
          .string "Using jasper big block ctype (perbox file)\n"
_str_jasper256:
          .string "jasper256"
_str_jasper512:
          .string "jasper512"
_str_trinity:
          .string "trinity"
_msg_ctype_trinity:
          .string "Using trinity ctype (perbox file)\n"
_str_trinitybb:
          .string "trinitybb"
          .zero 3
_msg_ctype_trinitybb:
          .string "Using trinity big block ctype (perbox file)\n"
_str_trinitybigffs:
          .string "trinitybigffs"
          .zero 1
_msg_ctype_trinitybigffs:
          .string "Using trinity big block big file system ctype (perbox file)\n"
_str_corona:
          .string "corona"
_msg_ctype_corona:
          .string "Using corona ctype (perbox file)\n"
_str_coronabb:
          .string "coronabb"
          .zero 1
_msg_ctype_coronabb:
          .string "Using corona big block ctype (perbox file)\n"
_str_coronabigffs:
          .string "coronabigffs"
          .zero 3
_msg_ctype_coronabigffs:
          .string "Using corona big block big file system ctype (perbox file)\n"
_str_corona4g:
          .string "corona4g"
          .zero 3
_msg_ctype_corona4g:
          .string "Using corona MMC ctype (perbox file)\n"
_str_winchester:
          .string "winchester"
          .zero 3
_msg_ctype_winchester:
          .string "Using winchester ctype (perbox file)\n"
_str_winchester4g:
          .string "winchester4g"
          .zero 1
_msg_ctype_winchester4g:
          .string "Using winchester MMC ctype (perbox file)\n"
_str_winchesterbb:
          .string "winchesterbb"
          .zero 1
_msg_ctype_winchesterbb:
          .string "Using winchester big block ctype (perbox file)\n"
_str_winchesterbigffs:
          .string "winchesterbigffs"
          .zero 3
_msg_ctype_winchesterbigffs:
          .string "Using winchester big block big file system ctype (perbox file)\n"
_str_jasperbigffs:
          .string "jasperbigffs"
          .zero 3
_msg_optPerbox:
          .string "Using %s option (perbox file)\n"
_msg_optIni:
          .string "Using %s option (ini file)\n"
          .zero 1
_msg_iniInvalid:
          .string "***** WARNING: options.ini setting '%s' invalid value '%s', discarding!\n"
_str_power:
          .string "power"
_str_remopower:
          .string "remopower"
_str_remox:
          .string "remox"
_str_winbutton:
          .string "winbutton"
_str_false:
          .string "false"
_str_true:
          .string "true"
_msg_opt_nodvd:
          .string "Using NODVD (tray status fully open check) option"
          .zero 2
_msg_opt_olddvd:
          .string "Using OLDDVD (tray status not closed check) option"
_msg_opt_cygnos:
          .string "Using CYGNOS option"
_msg_opt_demon:
          .string "Using DEMON option"
_str_nomobile:
          .string "nomobile"
_msg_opt_nomobile:
          .string "Using NOMOBILE option"
_str_smcnocheck:
          .string "smcnocheck"
_msg_opt_smcnocheck:
          .string "Using SMCNOCHECK option"
_str_noremap:
          .string "noremap"
_msg_opt_noremap:
          .string "Using NOREMAP option"
_str_noecdremap:
          .string "noecdremap"
_msg_opt_noecdremap:
          .string "Using NOECDREMAP option"
_str_nandmu:
          .string "nandmu"
_msg_opt_nandmu:
          .string "Using NANDMU option"
_str_nosecurity:
          .string "nosecurity"
_msg_opt_nosecurity:
          .string "Using NOSECURITY option"
_str_nosusecurity:
          .string "nosusecurity"
_str_patchsmc:
          .string "patchsmc"
_msg_opt_patchsmc:
          .string "Using PATCHSMC option"
_str_smcnoeject:
          .string "smcnoeject"
_msg_opt_smcnoeject:
          .string "Using SMCNOEJECT option"
_str_smcnoblink:
          .string "smcnoblink"
_msg_opt_smcnoblink:
          .string "Using SMCNOBLINK option"
_str_nodvd:
          .string "nodvd"
_str_olddvd:
          .string "olddvd"
_str_cygnos:
          .string "cygnos"
_str_demon:
          .string "demon"
          .zero 2
_msg_optNoValue:
          .string "\n\n***** ERROR: option '%s' provided on command line with = but no value!\n"
_str_nl:
          .string "\n"
_str_cputemp:
          .string "cputemp"
_msg_opt_cputemp:
          .string "Using CPUTEMP option, value %d\n"
_str_gputemp:
          .string "gputemp"
_msg_opt_gputemp:
          .string "Using GPUTEMP option, value %d\n"
_str_edramtemp:
          .string "edramtemp"
          .zero 2
_msg_opt_edramtemp:
          .string "Using EDRAMTEMP option, value %d\n"
_str_overcputemp:
          .string "overcputemp"
          .zero 2
_msg_opt_overcputemp:
          .string "Using OVERCPUTEMP option, value %d\n"
_str_overgputemp:
          .string "overgputemp"
_msg_opt_overgputemp:
          .string "Using OVERGPUTEMP option, value %d\n"
_str_overedramtemp:
          .string "overedramtemp"
          .zero 2
_msg_opt_overedramtemp:
          .string "Using OVEREDRAMTEMP option, value %d\n"
_str_cpufan:
          .string "cpufan"
          .zero 3
_msg_opt_cpufan:
          .string "Using CPUFAN option, value %d\n"
_str_gpufan:
          .string "gpufan"
          .zero 2
_msg_opt_gpufan:
          .string "Using GPUFAN option, value %d\n"
_str_avregion:
          .string "avregion"
_msg_opt_avregion:
          .string "Using AVREGION option, value 0x%x\n"
_str_gameregion:
          .string "gameregion"
          .zero 2
_msg_opt_gameregion:
          .string "Using GAMEREGION option, value 0x%x\n"
_str_dvdregion:
          .string "dvdregion"
          .zero 1
_msg_opt_dvdregion:
          .string "Using DVDREGION option, value 0x%x\n"
_str_xellbutton:
          .string "xellbutton"
          .zero 1
_msg_opt_xellbutton:
          .string "Using XELLBUTTON option, value %s\n"
_str_xellbutton2:
          .string "xellbutton2"
          .zero 1
_msg_opt_xellbutton2:
          .string "Using XELLBUTTON2 option, value %s\n"
_str_dualboot:
          .string "dualboot"
          .zero 3
_msg_opt_dualboot:
          .string "Using DUALBOOT option, value %s\n"
_str_cfldv:
          .string "cfldv"
          .zero 1
_msg_cfldvTooLarge:
          .string "***** WARNING: cfldv value %d on command line is too large, setting to max value of 32\n"
_msg_opt_cfldv:
          .string "Using CFLDV option, value %d\n"
_str_macid:
          .string "macid"
_msg_opt_macid:
          .string "Using MACID option address: "
_str_hex02:
          .string "%02x"
_str_colon:
          .string ":"
_msg_macidBadValues:
          .string "\n\n***** ERROR: invalid values in macid %s provided on the command line!\n"
          .zero 3
_msg_macidBadLength:
          .string "\n\n***** ERROR: invalid length macid %s provided on the command line!\n"
_str_dvdkey:
          .string "dvdkey"
          .zero 3
_msg_optUnknownValue:
          .string "\n\n***** ERROR: unknown option '%s' with value '%s' provided on the command line!\n"
          .zero 2
_msg_optIncomplete:
          .string "\n\n***** ERROR: unknown or incomplete option '%s' provided on the command line!\n"
_msg_optBadValue:
          .string "\n\n***** ERROR: parsing option '%s', value '%s' is incorrect!\n"
          .zero 2
_msg_iniCfldvTooLarge:
          .string "***** WARNING: cfldv value %d in options.ini is too large, setting to max value of 32\n"
          .zero 1
_msg_iniMacidBadChars:
          .string "***** WARNING: invalid characters in macid '"
          .zero 3
_msg_iniMacidDiscard:
          .string "' provided in ini file! Discarding!\n"
          .zero 3
_msg_iniMacidBadLength:
          .string "***** WARNING: invalid length macid '"
          .zero 2
_msg_xellDefault:
          .string "default console DVD eject button is being used to start xell\n"
          .zero 2
_msg_xellAltDisabled:
          .string "alternate xell button is disabled\n"
_msg_dualbootIgnored:
          .string "dualboot setting ignored!\n"
_str_rev:
          .string "rev"
_str_revSuffix:
          .string "_%s"
          .zero 2
_msg_rawPatchParsed:
          .string "parsed [rawpatch] (%d) from command line file '%s' offset 0x%x\n"
_msg_rawPatchBadOffset:
          .string "***** ERROR: [rawpatch] command option '%s' does not appear to have sane offset info!\n"
          .zero 1
_msg_rawPatchSlotsFull:
          .string "***** ERROR: %d of %d [rawpatch] slots are already full!\n"
          .zero 2
_msg_patchParseFailed:
          .string "***** ERROR: parsing optional patch string '%s' failed!\n"
_str_binFmt:
          .string "%s.bin"
_msg_patchDuplicate:
          .string "***** WARNING: %s was provided both on command line and in ini, filtered duplicate!\n"
          .zero 3
_msg_patchTooMany:
          .string "***** WARNING: exceeded total number of optional patches with ini  %s!\n"
_str_addon:
          .string "addon"
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
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _baseFileExists.part.0 - .
          .byte 0x3b
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x86
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x83
          .byte 0x3
          .byte 0x48
          .byte 0xe
          .byte 0xa0
          .byte 0x8
          .byte 0x6e
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x48
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _parseButton.part.0 - .
          .byte 0x42
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x45
          .byte 0xe
          .byte 0x20
          .byte 0x3
          .byte 0x38
          .byte 0x1
          .byte 0xe
          .byte 0x8
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x6c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _baseFileExists - .
          .byte 0x12
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x50
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x80
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _perboxExists - .
          .byte 0xde
          .byte 0x0
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
          .byte 0xb0
          .byte 0x10
          .byte 0x2
          .byte 0x64
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
          .byte 0x41
          .byte 0xb
          .byte 0x2
          .byte 0x60
          .byte 0xe
          .byte 0x14
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x10
          .byte 0x43
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
          .byte 0x34
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _iniConsoleType - .
          .byte 0x3d
          .byte 0x9
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
          .byte 0x3
          .byte 0xc4
          .byte 0x2
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
          .byte 0x34
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _setConsoleType - .
          .byte 0xbf
          .byte 0x7
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
          .byte 0x52
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
          .byte 0x45
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x2c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x44
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _optIniBool - .
          .byte 0xde
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x57
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x42
          .byte 0xb
          .byte 0x2
          .byte 0x42
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x46
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x48
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x34
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x74
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _optIniInt - .
          .byte 0x52
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x86
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x83
          .byte 0x3
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x73
          .byte 0xa
          .byte 0xe
          .byte 0xc
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x44
          .byte 0xb
          .byte 0x4b
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x34
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xac
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _parseButton - .
          .byte 0xae
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x6c
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x45
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x44
          .byte 0xb
          .byte 0x2
          .byte 0x66
          .byte 0xe
          .byte 0x8
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xe4
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _stripColons - .
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x86
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x83
          .byte 0x3
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x74
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long _macidSet - .
          .byte 0x46
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x48
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x24
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long _setBoolOption - .
          .byte 0x60
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x86
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x83
          .byte 0x3
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x2
          .byte 0x43
          .byte 0xa
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x46
          .byte 0xb
          .byte 0x2
          .byte 0x53
          .byte 0xa
          .byte 0xe
          .byte 0xc
          .byte 0x46
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x46
          .byte 0xb
          .byte 0x62
          .byte 0xa
          .byte 0xe
          .byte 0xc
          .byte 0x46
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x47
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x98
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x70
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long _parseOption - .
          .byte 0xc8
          .byte 0x7
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
          .byte 0xbd
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
          .byte 0x43
          .byte 0xb
          .byte 0x2
          .byte 0x71
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
          .byte 0x4b
          .byte 0xb
          .byte 0x5b
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
          .byte 0x41
          .byte 0xb
          .byte 0x2
          .byte 0x65
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
          .byte 0x74
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
          .byte 0x41
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long _parseCmdOptions - .
          .byte 0xb1
          .byte 0x0
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
          .byte 0xb0
          .byte 0x4
          .byte 0x2
          .byte 0x92
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
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x4c
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long _applyIniOptions - .
          .byte 0x5f
          .byte 0x16
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x86
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x83
          .byte 0x3
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x3
          .byte 0xb8
          .byte 0x2
          .byte 0xa
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x3
          .byte 0x7f
          .byte 0x1
          .byte 0xa
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x78
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8c
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long _parseRawPatch - .
          .byte 0x93
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
          .byte 0x43
          .byte 0xe
          .byte 0x30
          .byte 0x2
          .byte 0xf2
          .byte 0xa
          .byte 0xe
          .byte 0x10
          .byte 0x46
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
          .byte 0x67
          .byte 0xa
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
          .byte 0x43
          .byte 0xb
          .byte 0x5b
          .byte 0xa
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
          .byte 0x41
          .byte 0xb
          .byte 0x5b
          .byte 0xa
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
          .byte 0x41
          .byte 0xb
          .byte 0x5b
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
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long _parseRawPatches - .
          .byte 0xb1
          .byte 0x0
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
          .byte 0xb0
          .byte 0x4
          .byte 0x2
          .byte 0x92
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
          .byte 0x68
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x48
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long _addPatch - .
          .byte 0xd9
          .byte 0x0
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
          .byte 0xb0
          .byte 0x8
          .byte 0x2
          .byte 0x7a
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
          .byte 0x48
          .byte 0xb
          .byte 0x5a
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
          .byte 0x42
          .byte 0xb
          .byte 0x64
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
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x40
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb4
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long _loadAddons - .
          .byte 0xbc
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
          .byte 0xc
          .byte 0x3
          .byte 0x4a
          .byte 0x1
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
          .byte 0x43
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0

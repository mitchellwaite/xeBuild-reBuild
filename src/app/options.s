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
.globl _applyIniOptions
.globl _loadAddons
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
.globl _msg_iniInvalid
.globl _msg_optIni
.globl _msg_optNoValue
.globl _msg_optPerbox
.globl _msg_opt_cygnos
.globl _msg_opt_demon
.globl _msg_opt_nandmu
.globl _msg_opt_nodvd
.globl _msg_opt_noecdremap
.globl _msg_opt_nomobile
.globl _msg_opt_noremap
.globl _msg_opt_nosecurity
.globl _msg_opt_olddvd
.globl _msg_opt_patchsmc
.globl _msg_opt_smcnoblink
.globl _msg_opt_smcnocheck
.globl _msg_opt_smcnoeject
.globl _msg_patchDuplicate
.globl _msg_patchParseFailed
.globl _msg_patchTooMany
.globl _msg_rawPatchBadOffset
.globl _msg_rawPatchParsed
.globl _msg_rawPatchSlotsFull
.globl _parseCmdOptions
.globl _parseOption
.globl _str_binFmt
.globl _str_corona
.globl _str_corona4g
.globl _str_coronabb
.globl _str_coronabigffs
.globl _str_cygnos
.globl _str_demon
.globl _str_eject
.globl _str_falcon
.globl _str_false
.globl _str_jasper
.globl _str_jasper256
.globl _str_jasper512
.globl _str_jasperbb
.globl _str_jasperbc
.globl _str_jasperbigffs
.globl _str_jaspersb
.globl _str_kiosk
.globl _str_nandmu
.globl _str_nodvd
.globl _str_noecdremap
.globl _str_nomobile
.globl _str_noremap
.globl _str_nosecurity
.globl _str_nosusecurity
.globl _str_olddvd
.globl _str_patchsmc
.globl _str_power
.globl _str_remopower
.globl _str_remox
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
_parseOption:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov EBX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP],EBX
          call _strlen
          test EAX,EAX
          jle L_4252bb
          mov ESI,EAX
          xor EDI,EDI
          xor EAX,EAX
          jmp L_42513a
L_425133:
          add EAX,1
          cmp ESI,EAX
          jle L_42515c
L_42513a:
          lea EDX,DWORD PTR [EBX+EAX*1]
          cmp BYTE PTR [EDX],61
          jne L_425133
          lea EDI,DWORD PTR [EBX+EAX*1+1]
          mov BYTE PTR [EDX],0
          cmp BYTE PTR [EDI],0
          je L_425260
          lea EAX,DWORD PTR [ESI+1]
          add EAX,1
          cmp ESI,EAX
          jg L_42513a
L_42515c:
          mov DWORD PTR [ESP],EBX
          call _strlen
          cmp ESI,EAX
          je L_4252f1
          mov DWORD PTR [ESP],EDI
          call _strlen
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EBX
          mov EBP,EAX
          call _setBoolOption
          cmp EAX,1
          je L_4252d0
L_42518b:
          mov DWORD PTR [ESP+4],OFFSET L_4584e0
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          jne L_4251e0
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],EDI
          call _myatou32
          cmp EAX,-1
          mov DWORD PTR [L_479f18],EAX
          je L_425230
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_4584e8
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,44
          mov EAX,1
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x66
          .byte 0x90
L_4251e0:
          mov DWORD PTR [ESP+4],OFFSET L_458508
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          je L_425282
          mov DWORD PTR [ESP+4],OFFSET L_458530
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          jne L_42532c
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],EDI
          call _myatou32
          cmp EAX,-1
          mov DWORD PTR [L_479f20],EAX
          jne L_4253d8
          .byte 0x66   # nop
          nop
L_425230:
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_458948
          mov DWORD PTR [ESP],1
          call _log_printf
          xor EAX,EAX
L_42524e:
          add ESP,44
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_425260:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET _msg_optNoValue
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,44
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_425282:
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],EDI
          call _myatou32
          cmp EAX,-1
          mov DWORD PTR [L_479f1c],EAX
          je L_425230
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_458510
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,1
          jmp L_42524e
L_4252bb:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],EBX
          call _setBoolOption
          cmp EAX,1
          jne L_42530a
L_4252d0:
          mov DWORD PTR [ESP+4],OFFSET L_4584de
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,44
          mov EAX,1
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_4252f1:
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EBX
          call _setBoolOption
          cmp EAX,1
          je L_4252d0
          test EDI,EDI
          jne L_4255a4
L_42530a:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_4588f8
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,44
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_42532c:
          mov DWORD PTR [ESP+4],OFFSET L_45855e
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          je L_425398
          mov DWORD PTR [ESP+4],OFFSET L_458590
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          jne L_4253fa
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],EDI
          call _myatou32
          cmp EAX,-1
          mov DWORD PTR [L_479f28],EAX
          je L_425230
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_45859c
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,1
          jmp L_42524e
L_425398:
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],EDI
          call _myatou32
          cmp EAX,-1
          mov DWORD PTR [L_479f24],EAX
          je L_425230
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_45856c
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,1
          jmp L_42524e
L_4253d8:
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_45853c
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,1
          jmp L_42524e
L_4253fa:
          mov DWORD PTR [ESP+4],OFFSET L_4585c0
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          jne L_42544e
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],EDI
          call _myatou32
          cmp EAX,-1
          mov DWORD PTR [L_479f2c],EAX
          je L_425230
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_4585d0
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,1
          jmp L_42524e
L_42544e:
          mov DWORD PTR [ESP+4],OFFSET L_4585f6
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          jne L_4254a2
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],EDI
          call _myatou32
          cmp EAX,-1
          mov DWORD PTR [L_479f30],EAX
          je L_425230
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_458600
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,1
          jmp L_42524e
L_4254a2:
          mov DWORD PTR [ESP+4],OFFSET L_45861f
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          jne L_4254f6
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],EDI
          call _myatou32
          cmp EAX,-1
          mov DWORD PTR [L_479f34],EAX
          je L_425230
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_458628
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,1
          jmp L_42524e
L_4254f6:
          mov DWORD PTR [ESP+4],OFFSET L_458647
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          jne L_425550
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],EDI
          call _myatou32
          cmp EAX,-1
          mov DWORD PTR [L_479f38],EAX
          je L_425230
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_458650
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,1
          jmp L_42524e
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_425550:
          mov DWORD PTR [ESP+4],OFFSET L_458673
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          jne L_4255ab
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],EDI
          call _myatou32
          cmp EAX,-1
          mov DWORD PTR [L_479f3c],EAX
          je L_425230
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_458680
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,1
          jmp L_42524e
L_4255a4:
          xor EBP,EBP
          jmp L_42518b
L_4255ab:
          mov DWORD PTR [ESP+4],OFFSET L_4586a5
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          jne L_4255ff
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],EDI
          call _myatou32
          cmp EAX,-1
          mov DWORD PTR [L_479f40],EAX
          je L_425230
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_4586b0
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,1
          jmp L_42524e
L_4255ff:
          mov DWORD PTR [ESP+4],OFFSET L_4586d4
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          jne L_42564a
          mov DWORD PTR [ESP],EDI
          call _parseButton
          test EAX,EAX
          mov DWORD PTR [L_479f08],EAX
          je L_425230
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET L_4586e0
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,1
          jmp L_42524e
L_42564a:
          mov DWORD PTR [ESP+4],OFFSET L_458703
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          jne L_425695
          mov DWORD PTR [ESP],EDI
          call _parseButton
          test EAX,EAX
          mov DWORD PTR [L_479f0c],EAX
          je L_425230
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET L_458710
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,1
          jmp L_42524e
L_425695:
          mov DWORD PTR [ESP+4],OFFSET L_458734
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          jne L_4256e0
          mov DWORD PTR [ESP],EDI
          call _parseButton
          test EAX,EAX
          mov DWORD PTR [L_479f10],EAX
          je L_425230
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET L_458740
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,1
          jmp L_42524e
L_4256e0:
          mov DWORD PTR [ESP+4],OFFSET L_458761
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          jne L_42573a
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],EDI
          call _myatou32
          cmp AL,32
          mov BYTE PTR [L_479f15],AL
          ja L_425788
          test AL,AL
          je L_425230
          movzx EAX,AL
L_425718:
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_4587c0
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,1
          jmp L_42524e
L_42573a:
          mov DWORD PTR [ESP+4],OFFSET L_4587de
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          mov ESI,EAX
          jne L_425850
          mov DWORD PTR [ESP],EDI
          call _stripColons
          mov DWORD PTR [ESP],EDI
          call _strlen
          cmp EAX,12
          je L_4257b4
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_458854
          mov DWORD PTR [ESP],1
          call _log_printf
          xor EAX,EAX
          jmp L_42524e
L_425788:
          movzx EAX,AL
          mov DWORD PTR [ESP+4],OFFSET L_458768
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov BYTE PTR [L_479f15],32
          mov EAX,32
          jmp L_425718
L_4257b4:
          mov DWORD PTR [ESP],EDI
          call _validateString
          test EAX,EAX
          je L_42588f
          mov DWORD PTR [ESP+4],OFFSET L_4587e4
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP],EDI
          add EDI,2
          call _myatox8
          mov BYTE PTR [L_479f44],AL
          movzx EAX,AL
          mov DWORD PTR [ESP+4],OFFSET L_458801
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],1
          call _log_printf
L_425803:
          mov DWORD PTR [ESP+4],OFFSET L_458806
          mov DWORD PTR [ESP],1
          add ESI,1
          call _log_printf
          mov DWORD PTR [ESP],EDI
          add EDI,2
          call _myatox8
          mov BYTE PTR [ESI+L_479f44],AL
          movzx EAX,AL
          mov DWORD PTR [ESP+4],OFFSET L_458801
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],1
          call _log_printf
          cmp ESI,5
          jne L_425803
          jmp L_4252d0
L_425850:
          mov DWORD PTR [ESP+4],OFFSET L_45889a
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          je L_4258b4
          test EBP,EBP
          je L_42530a
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_4588a4
          mov DWORD PTR [ESP],1
          call _log_printf
          xor EAX,EAX
          jmp L_42524e
L_42588f:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_458808
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+28],EAX
          call _log_printf
          mov EAX,DWORD PTR [ESP+28]
          jmp L_42524e
L_4258b4:
          mov DWORD PTR [ESP],EDI
          call _kvSetDvdKey
          test EAX,EAX
          je L_425230
          or DWORD PTR [L_479f00],33554432
          mov EAX,1
          jmp L_42524e
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
_parseCmdOptions:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,540
          mov ESI,DWORD PTR [ESP+560]
          mov DWORD PTR [ESP],ESI
          call _strlen
          test EAX,EAX
          js L_425971
          mov EDI,EAX
          xor EDX,EDX
          xor EBX,EBX
          lea EBP,DWORD PTR [ESP+16]
          jmp L_425922
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_425910:
          test AL,AL
          je L_42592a
          add EBX,1
          mov BYTE PTR [ESP+EDX*1+16],AL
          add EDX,1
          cmp EDI,EBX
          jl L_425971
L_425922:
          movzx EAX,BYTE PTR [ESI+EBX*1]
          cmp AL,59
          jne L_425910
L_42592a:
          mov BYTE PTR [ESP+EDX*1+16],0
          mov EDX,EBP
L_425931:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_425931
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          sbb EDX,3
          sub EDX,EBP
          cmp EDX,4
          ja L_425981
          xor EDX,EDX
L_42596a:
          add EBX,1
          cmp EDI,EBX
          jge L_425922
L_425971:
          mov EAX,1
L_425976:
          add ESP,540
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_425981:
          mov DWORD PTR [ESP],EBP
          call _parseOption
          test EAX,EAX
          je L_425976
          xor EDX,EDX
          jmp L_42596a
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
_applyIniOptions:
          push ESI
          push EBX
          sub ESP,20
          mov EAX,DWORD PTR [L_479f00]
          test EAX,536870912
          je L_426350
L_4259b5:
          test EAX,1073741824
          je L_4263b0
L_4259c0:
          test EAX,EAX
          js L_4259d2
          mov ESI,DWORD PTR [L_479f04]
          test ESI,ESI
          jns L_4261c3
L_4259d2:
          test EAX,268435456
          je L_426501
L_4259dd:
          test EAX,67108864
          je L_426450
L_4259e8:
          test EAX,16777216
          je L_4264b0
L_4259f3:
          test EAX,2097152
          je L_426401
L_4259fe:
          cmp BYTE PTR [L_479f15],0
          je L_425e15
L_425a0b:
          cmp DWORD PTR [L_479f30],-1
          je L_425e5d
L_425a18:
          cmp DWORD PTR [L_479f34],-1
          je L_425eb0
L_425a25:
          cmp DWORD PTR [L_479f18],-1
          je L_425f00
L_425a32:
          cmp DWORD PTR [L_479f1c],-1
          je L_425f50
L_425a3f:
          cmp DWORD PTR [L_479f20],-1
          je L_425fa0
L_425a4c:
          cmp DWORD PTR [L_479f24],-1
          je L_425ff0
L_425a59:
          cmp DWORD PTR [L_479f28],-1
          je L_426040
L_425a66:
          cmp DWORD PTR [L_479f2c],-1
          je L_426090
L_425a73:
          cmp DWORD PTR [L_479f38],-1
          je L_4260e0
L_425a80:
          cmp DWORD PTR [L_479f3c],-1
          je L_426130
L_425a8d:
          cmp DWORD PTR [L_479f40],-1
          je L_426180
L_425a9a:
          cmp BYTE PTR [L_479f44],255
          jne L_425b73
          cmp BYTE PTR [L_479f45],255
          jne L_425b73
          cmp BYTE PTR [L_479f46],255
          jne L_425b73
          cmp BYTE PTR [L_479f47],255
          jne L_425b73
          cmp BYTE PTR [L_479f48],255
          jne L_425b73
          cmp BYTE PTR [L_479f49],255
          jne L_425b73
          mov DWORD PTR [ESP],OFFSET L_4587de
          call _getIniValue
          test EAX,EAX
          mov EBX,EAX
          je L_425b73
          mov DWORD PTR [ESP],EAX
          call _strlen
          lea ESI,DWORD PTR [EAX+1]
          test ESI,ESI
          jle L_425b2e
          xor ECX,ECX
          xor EAX,EAX
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
L_425b10:
          movzx EDX,BYTE PTR [EBX+EAX*1]
          cmp DL,58
          je L_425b1f
          mov BYTE PTR [EBX+ECX*1],DL
          add ECX,1
L_425b1f:
          add EAX,1
          cmp ESI,EAX
          jne L_425b10
          mov DWORD PTR [ESP],EBX
          call _strlen
L_425b2e:
          cmp EAX,12
          je L_426304
          mov DWORD PTR [ESP+4],OFFSET L_458a38
L_425b3f:
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],0
          call _showHexPairs
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_458a10
          mov DWORD PTR [ESP],0
          call _log_printf
L_425b73:
          mov EAX,DWORD PTR [_g479ea8]
          sub EAX,2
          cmp EAX,3
          mov EAX,DWORD PTR [L_479f00]
          ja L_425c42
          test AL,1
          je L_426215
L_425b91:
          test AL,8
          je L_426264
L_425b99:
          test EAX,134217728
          je L_4262b3
L_425ba4:
          mov EBX,DWORD PTR [L_479f08]
          test EBX,EBX
          jne L_425d40
          test AL,4
          jne L_425c60
L_425bba:
          test EAX,OFFSET __ImageBase
          je L_4265a3
L_425bc5:
          test EAX,8388608
          je L_426552
L_425bd0:
          mov EDX,DWORD PTR [_g479ea8]
L_425bd6:
          cmp EDX,2
          jne L_425c42
          test AL,2
          je L_426620
L_425be3:
          mov DWORD PTR [ESP],OFFSET _str_olddvd
          call _perboxExists
          test EAX,EAX
          jne L_4265f4
          mov DWORD PTR [ESP],OFFSET _str_olddvd
          call _iniBoolInvalid
          test EAX,EAX
          je L_426dda
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET _str_olddvd
          mov DWORD PTR [ESP+4],OFFSET _msg_iniInvalid
          mov DWORD PTR [ESP],0
          call _log_printf
          nop
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_425c30:
          mov EAX,DWORD PTR [L_479f10]
          test EAX,EAX
          je L_426730
L_425c3d:
          mov EAX,DWORD PTR [L_479f00]
L_425c42:
          test EAX,33554432
          je L_425de2
L_425c4d:
          cmp BYTE PTR [L_4c4f54],0
          je L_425db0
L_425c5a:
          add ESP,20
          pop EBX
          pop ESI
          ret 
L_425c60:
          mov DWORD PTR [ESP],OFFSET L_4586d4
          call _getIniValue
          test EAX,EAX
          mov EBX,EAX
          je L_42698e
          mov DWORD PTR [ESP+8],5
          mov DWORD PTR [ESP+4],OFFSET _str_power
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          mov EDX,17
          je L_426340
          mov DWORD PTR [ESP+8],9
          mov DWORD PTR [ESP+4],OFFSET _str_remopower
          mov DWORD PTR [ESP],EBX
          call _strnicmp
          test EAX,EAX
          mov EDX,32
          je L_426340
          mov DWORD PTR [ESP+8],5
          mov DWORD PTR [ESP+4],OFFSET _str_remox
          mov DWORD PTR [ESP],EBX
          call _strnicmp
          test EAX,EAX
          mov EDX,34
          je L_426340
          mov DWORD PTR [ESP+8],9
          mov DWORD PTR [ESP+4],OFFSET _str_winbutton
          mov DWORD PTR [ESP],EBX
          call _strnicmp
          test EAX,EAX
          mov EDX,36
          je L_426340
          mov EAX,EBX
          call _parseButton.part.0
          test EAX,EAX
          mov DWORD PTR [L_479f08],EAX
          jne L_425d38
L_425d1a:
          mov DWORD PTR [ESP+4],OFFSET L_458a60
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [L_479f08],18
L_425d38:
          mov EAX,DWORD PTR [L_479f00]
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
L_425d40:
          mov ECX,DWORD PTR [L_479f0c]
          test ECX,ECX
          jne L_425bba
          test AL,4
          je L_425bba
          mov DWORD PTR [ESP],OFFSET L_458703
          call _getIniValue
          xor EDX,EDX
          test EAX,EAX
          mov EBX,EAX
          je L_425d8f
          mov DWORD PTR [ESP+8],5
          mov DWORD PTR [ESP+4],OFFSET _str_power
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          mov EDX,17
          jne L_4266af
L_425d8f:
          mov DWORD PTR [L_479f0c],EDX
          mov EDX,DWORD PTR [L_479f08]
          test EDX,EDX
          je L_4267f0
L_425da3:
          mov EAX,DWORD PTR [L_479f00]
          jmp L_425bba
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_425db0:
          mov DWORD PTR [ESP],OFFSET L_458ade
          call _getIniValue
          test EAX,EAX
          je L_425c5a
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_458ae2
          mov DWORD PTR [ESP],OFFSET L_4c4f54
          call _sprintf
          add ESP,20
          pop EBX
          pop ESI
          ret 
L_425de2:
          mov DWORD PTR [ESP],OFFSET L_45889a
          call _getIniValue
          test EAX,EAX
          je L_425c4d
          mov DWORD PTR [ESP],EAX
          call _kvSetDvdKey
          test EAX,EAX
          je L_425c4d
          or DWORD PTR [L_479f00],33554432
          jmp L_425c4d
L_425e15:
          mov DWORD PTR [ESP],OFFSET L_458761
          call _iniU32Invalid
          test EAX,EAX
          je L_4267a0
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_458761
          mov DWORD PTR [ESP+4],OFFSET _msg_iniInvalid
          mov DWORD PTR [ESP],0
          call _log_printf
          cmp DWORD PTR [L_479f30],-1
          mov BYTE PTR [L_479f15],0
          jne L_425a18
L_425e5d:
          mov DWORD PTR [ESP],OFFSET L_4585f6
          call _iniU32Invalid
          test EAX,EAX
          je L_426a4c
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_4585f6
          mov DWORD PTR [ESP+4],OFFSET _msg_iniInvalid
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,4294967295
L_425e96:
          cmp DWORD PTR [L_479f34],-1
          mov DWORD PTR [L_479f30],EAX
          jne L_425a25
          nop
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_425eb0:
          mov DWORD PTR [ESP],OFFSET L_45861f
          call _iniU32Invalid
          test EAX,EAX
          je L_426a33
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_45861f
          mov DWORD PTR [ESP+4],OFFSET _msg_iniInvalid
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,4294967295
L_425ee9:
          cmp DWORD PTR [L_479f18],-1
          mov DWORD PTR [L_479f34],EAX
          jne L_425a32
          nop
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_425f00:
          mov DWORD PTR [ESP],OFFSET L_4584e0
          call _iniU32Invalid
          test EAX,EAX
          je L_4269b6
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_4584e0
          mov DWORD PTR [ESP+4],OFFSET _msg_iniInvalid
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,4294967295
L_425f39:
          cmp DWORD PTR [L_479f1c],-1
          mov DWORD PTR [L_479f18],EAX
          jne L_425a3f
          nop
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_425f50:
          mov DWORD PTR [ESP],OFFSET L_458508
          call _iniU32Invalid
          test EAX,EAX
          je L_42699d
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_458508
          mov DWORD PTR [ESP+4],OFFSET _msg_iniInvalid
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,4294967295
L_425f89:
          cmp DWORD PTR [L_479f20],-1
          mov DWORD PTR [L_479f1c],EAX
          jne L_425a4c
          nop
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_425fa0:
          mov DWORD PTR [ESP],OFFSET L_458530
          call _iniU32Invalid
          test EAX,EAX
          je L_426a7e
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_458530
          mov DWORD PTR [ESP+4],OFFSET _msg_iniInvalid
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,4294967295
L_425fd9:
          cmp DWORD PTR [L_479f24],-1
          mov DWORD PTR [L_479f20],EAX
          jne L_425a59
          nop
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_425ff0:
          mov DWORD PTR [ESP],OFFSET L_45855e
          call _iniU32Invalid
          test EAX,EAX
          je L_426a65
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_45855e
          mov DWORD PTR [ESP+4],OFFSET _msg_iniInvalid
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,4294967295
L_426029:
          cmp DWORD PTR [L_479f28],-1
          mov DWORD PTR [L_479f24],EAX
          jne L_425a66
          nop
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_426040:
          mov DWORD PTR [ESP],OFFSET L_458590
          call _iniU32Invalid
          test EAX,EAX
          je L_426a1a
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_458590
          mov DWORD PTR [ESP+4],OFFSET _msg_iniInvalid
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,4294967295
L_426079:
          cmp DWORD PTR [L_479f2c],-1
          mov DWORD PTR [L_479f28],EAX
          jne L_425a73
          nop
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_426090:
          mov DWORD PTR [ESP],OFFSET L_4585c0
          call _iniU32Invalid
          test EAX,EAX
          je L_426a01
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_4585c0
          mov DWORD PTR [ESP+4],OFFSET _msg_iniInvalid
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,4294967295
L_4260c9:
          cmp DWORD PTR [L_479f38],-1
          mov DWORD PTR [L_479f2c],EAX
          jne L_425a80
          nop
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_4260e0:
          mov DWORD PTR [ESP],OFFSET L_458647
          call _iniU32Invalid
          test EAX,EAX
          je L_4269e8
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_458647
          mov DWORD PTR [ESP+4],OFFSET _msg_iniInvalid
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,4294967295
L_426119:
          cmp DWORD PTR [L_479f3c],-1
          mov DWORD PTR [L_479f38],EAX
          jne L_425a8d
          nop
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_426130:
          mov DWORD PTR [ESP],OFFSET L_458673
          call _iniU32Invalid
          test EAX,EAX
          je L_4269cf
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_458673
          mov DWORD PTR [ESP+4],OFFSET _msg_iniInvalid
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,4294967295
L_426169:
          cmp DWORD PTR [L_479f40],-1
          mov DWORD PTR [L_479f3c],EAX
          jne L_425a9a
          nop
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_426180:
          mov DWORD PTR [ESP],OFFSET L_4586a5
          call _iniU32Invalid
          test EAX,EAX
          je L_426a97
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_4586a5
          mov DWORD PTR [ESP+4],OFFSET _msg_iniInvalid
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,4294967295
L_4261b9:
          mov DWORD PTR [L_479f40],EAX
          jmp L_425a9a
L_4261c3:
          mov DWORD PTR [ESP],OFFSET _str_noecdremap
          call _perboxExists
          test EAX,EAX
          jne L_426672
          mov DWORD PTR [ESP],OFFSET _str_noecdremap
          call _iniBoolInvalid
          test EAX,EAX
          je L_426ca9
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET _str_noecdremap
          mov DWORD PTR [ESP+4],OFFSET _msg_iniInvalid
          mov DWORD PTR [ESP],0
          call _log_printf
L_42620b:
          mov EAX,DWORD PTR [L_479f00]
          jmp L_4259d2
L_426215:
          test BYTE PTR [L_479f04],1
          jne L_425b91
          mov DWORD PTR [ESP],OFFSET _str_cygnos
          call _perboxExists
          test EAX,EAX
          je L_426ab0
          mov DWORD PTR [ESP+8],OFFSET _str_cygnos
          mov DWORD PTR [ESP+4],OFFSET _msg_optPerbox
          mov DWORD PTR [ESP],1
          call _log_printf
L_426252:
          mov EAX,DWORD PTR [L_479f00]
          or EAX,1
          mov DWORD PTR [L_479f00],EAX
          jmp L_425b91
L_426264:
          test BYTE PTR [L_479f04],8
          jne L_425b99
          mov DWORD PTR [ESP],OFFSET _str_demon
          call _perboxExists
          test EAX,EAX
          je L_426aee
          mov DWORD PTR [ESP+8],OFFSET _str_demon
          mov DWORD PTR [ESP+4],OFFSET _msg_optPerbox
          mov DWORD PTR [ESP],1
          call _log_printf
L_4262a1:
          mov EAX,DWORD PTR [L_479f00]
          or EAX,8
          mov DWORD PTR [L_479f00],EAX
          jmp L_425b99
L_4262b3:
          test BYTE PTR [L_479f07],8
          jne L_425ba4
          mov DWORD PTR [ESP],OFFSET _str_patchsmc
          call _perboxExists
          test EAX,EAX
          je L_426bf4
          mov DWORD PTR [ESP+8],OFFSET _str_patchsmc
          mov DWORD PTR [ESP+4],OFFSET _msg_optPerbox
          mov DWORD PTR [ESP],1
          call _log_printf
L_4262f0:
          mov EAX,DWORD PTR [L_479f00]
          or EAX,134217728
          mov DWORD PTR [L_479f00],EAX
          jmp L_425ba4
L_426304:
          mov DWORD PTR [ESP],EBX
          call _validateString
          test EAX,EAX
          je L_4266a2
          xor ESI,ESI
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_426320:
          mov DWORD PTR [ESP],EBX
          add ESI,1
          add EBX,2
          call _myatox8
          mov BYTE PTR [ESI+L_479f43],AL
          cmp ESI,6
          jne L_426320
          jmp L_425b73
          .byte 0x66
          .byte 0x90
L_426340:
          mov DWORD PTR [L_479f08],EDX
          mov EAX,DWORD PTR [L_479f00]
          jmp L_425d40
L_426350:
          test BYTE PTR [L_479f07],32
          jne L_4259b5
          mov DWORD PTR [ESP],OFFSET _str_nomobile
          call _perboxExists
          test EAX,EAX
          je L_426890
          mov DWORD PTR [ESP+8],OFFSET _str_nomobile
          mov DWORD PTR [ESP+4],OFFSET _msg_optPerbox
          mov DWORD PTR [ESP],1
          call _log_printf
L_42638d:
          mov EAX,DWORD PTR [L_479f00]
          or EAX,536870912
          test EAX,1073741824
          mov DWORD PTR [L_479f00],EAX
          jne L_4259c0
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_4263b0:
          test BYTE PTR [L_479f07],64
          jne L_4259c0
          mov DWORD PTR [ESP],OFFSET _str_noremap
          call _perboxExists
          test EAX,EAX
          je L_426850
          mov DWORD PTR [ESP+8],OFFSET _str_noremap
          mov DWORD PTR [ESP+4],OFFSET _msg_optPerbox
          mov DWORD PTR [ESP],1
          call _log_printf
L_4263ed:
          mov EAX,DWORD PTR [L_479f00]
          or EAX,1073741824
          mov DWORD PTR [L_479f00],EAX
          jmp L_4259c0
L_426401:
          test BYTE PTR [L_479f06],32
          jne L_4259fe
          mov DWORD PTR [ESP],OFFSET _str_smcnocheck
          call _perboxExists
          test EAX,EAX
          je L_426910
          mov DWORD PTR [ESP+8],OFFSET _str_smcnocheck
          mov DWORD PTR [ESP+4],OFFSET _msg_optPerbox
          mov DWORD PTR [ESP],1
          call _log_printf
L_42643e:
          or DWORD PTR [L_479f00],2097152
          jmp L_4259fe
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_426450:
          test BYTE PTR [L_479f07],4
          jne L_4259e8
          mov DWORD PTR [ESP],OFFSET _str_nosecurity
          call _perboxExists
          test EAX,EAX
          je L_426950
          mov DWORD PTR [ESP+8],OFFSET _str_nosecurity
          mov DWORD PTR [ESP+4],OFFSET _msg_optPerbox
          mov DWORD PTR [ESP],1
          call _log_printf
L_42648d:
          mov EAX,DWORD PTR [L_479f00]
          or EAX,67108864
          test EAX,16777216
          mov DWORD PTR [L_479f00],EAX
          jne L_4259f3
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_4264b0:
          test BYTE PTR [L_479f07],1
          jne L_4259f3
          mov DWORD PTR [ESP],OFFSET _str_nosusecurity
          call _perboxExists
          test EAX,EAX
          je L_4268d0
          mov DWORD PTR [ESP+8],OFFSET _str_nosusecurity
          mov DWORD PTR [ESP+4],OFFSET _msg_optPerbox
          mov DWORD PTR [ESP],1
          call _log_printf
L_4264ed:
          mov EAX,DWORD PTR [L_479f00]
          or EAX,16777216
          mov DWORD PTR [L_479f00],EAX
          jmp L_4259f3
L_426501:
          test BYTE PTR [L_479f07],16
          jne L_4259dd
          mov DWORD PTR [ESP],OFFSET _str_nandmu
          call _perboxExists
          test EAX,EAX
          je L_426810
          mov DWORD PTR [ESP+8],OFFSET _str_nandmu
          mov DWORD PTR [ESP+4],OFFSET _msg_optPerbox
          mov DWORD PTR [ESP],1
          call _log_printf
L_42653e:
          mov EAX,DWORD PTR [L_479f00]
          or EAX,268435456
          mov DWORD PTR [L_479f00],EAX
          jmp L_4259dd
L_426552:
          test BYTE PTR [L_479f06],128
          jne L_425bd0
          mov DWORD PTR [ESP],OFFSET _str_smcnoblink
          call _perboxExists
          test EAX,EAX
          je L_426bb0
          mov DWORD PTR [ESP+8],OFFSET _str_smcnoblink
          mov DWORD PTR [ESP+4],OFFSET _msg_optPerbox
          mov DWORD PTR [ESP],1
          call _log_printf
L_42658f:
          mov EAX,DWORD PTR [L_479f00]
          or EAX,8388608
          mov DWORD PTR [L_479f00],EAX
          jmp L_425bd0
L_4265a3:
          test BYTE PTR [L_479f06],64
          jne L_425bc5
          mov DWORD PTR [ESP],OFFSET _str_smcnoeject
          call _perboxExists
          test EAX,EAX
          je L_426c32
          mov DWORD PTR [ESP+8],OFFSET _str_smcnoeject
          mov DWORD PTR [ESP+4],OFFSET _msg_optPerbox
          mov DWORD PTR [ESP],1
          call _log_printf
L_4265e0:
          mov EAX,DWORD PTR [L_479f00]
          or EAX,OFFSET __ImageBase
          mov DWORD PTR [L_479f00],EAX
          jmp L_425bc5
L_4265f4:
          mov DWORD PTR [ESP+8],OFFSET _str_olddvd
          mov DWORD PTR [ESP+4],OFFSET _msg_optPerbox
          mov DWORD PTR [ESP],1
          call _log_printf
L_426610:
          and DWORD PTR [L_479f00],4294967291
          jmp L_425c30
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_426620:
          test BYTE PTR [L_479f04],2
          jne L_425be3
          mov DWORD PTR [ESP],OFFSET _str_nodvd
          call _perboxExists
          test EAX,EAX
          je L_426c70
          mov DWORD PTR [ESP+8],OFFSET _str_nodvd
          mov DWORD PTR [ESP+4],OFFSET _msg_optPerbox
          mov DWORD PTR [ESP],1
          call _log_printf
L_42665d:
          mov EAX,DWORD PTR [L_479f00]
          and EAX,4294967291
          or EAX,2
          mov DWORD PTR [L_479f00],EAX
          jmp L_425be3
L_426672:
          mov DWORD PTR [ESP+8],OFFSET _str_noecdremap
          mov DWORD PTR [ESP+4],OFFSET _msg_optPerbox
          mov DWORD PTR [ESP],1
          call _log_printf
L_42668e:
          mov EAX,DWORD PTR [L_479f00]
          or EAX,2147483648
          mov DWORD PTR [L_479f00],EAX
          jmp L_4259d2
L_4266a2:
          mov DWORD PTR [ESP+4],OFFSET L_4589e0
          jmp L_425b3f
L_4266af:
          mov DWORD PTR [ESP+8],9
          mov DWORD PTR [ESP+4],OFFSET _str_remopower
          mov DWORD PTR [ESP],EBX
          call _strnicmp
          test EAX,EAX
          mov EDX,32
          je L_425d8f
          mov DWORD PTR [ESP+8],5
          mov DWORD PTR [ESP+4],OFFSET _str_remox
          mov DWORD PTR [ESP],EBX
          call _strnicmp
          test EAX,EAX
          mov EDX,34
          je L_425d8f
          mov DWORD PTR [ESP+8],9
          mov DWORD PTR [ESP+4],OFFSET _str_winbutton
          mov DWORD PTR [ESP],EBX
          call _strnicmp
          test EAX,EAX
          mov EDX,36
          je L_425d8f
          mov EAX,EBX
          call _parseButton.part.0
          mov EDX,EAX
          jmp L_425d8f
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_426730:
          mov DWORD PTR [ESP],OFFSET L_458734
          call _getIniValue
          xor EDX,EDX
          test EAX,EAX
          mov EBX,EAX
          je L_426769
          mov DWORD PTR [ESP+8],5
          mov DWORD PTR [ESP+4],OFFSET _str_power
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          mov EDX,17
          jne L_426b2c
L_426769:
          cmp DWORD PTR [L_479f08],EDX
          mov DWORD PTR [L_479f10],EDX
          jne L_425c3d
          mov DWORD PTR [ESP+4],OFFSET L_458ac3
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [L_479f10],0
          jmp L_425c3d
          .byte 0x66
          .byte 0x90
L_4267a0:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_458761
          call _getIniU32
          cmp AL,32
          mov BYTE PTR [L_479f15],AL
          jbe L_425a0b
          movzx EAX,AL
          mov DWORD PTR [ESP+4],OFFSET L_458988
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov BYTE PTR [L_479f15],32
          jmp L_425a0b
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4267f0:
          mov DWORD PTR [ESP+4],OFFSET L_458aa0
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_425da3
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_426810:
          mov DWORD PTR [ESP],OFFSET _str_nandmu
          call _iniBoolInvalid
          test EAX,EAX
          je L_426e54
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET _str_nandmu
          mov DWORD PTR [ESP+4],OFFSET _msg_iniInvalid
          mov DWORD PTR [ESP],0
          call _log_printf
L_426844:
          mov EAX,DWORD PTR [L_479f00]
          jmp L_4259dd
          .byte 0x66
          .byte 0x90
L_426850:
          mov DWORD PTR [ESP],OFFSET _str_noremap
          call _iniBoolInvalid
          test EAX,EAX
          je L_426ce6
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET _str_noremap
          mov DWORD PTR [ESP+4],OFFSET _msg_iniInvalid
          mov DWORD PTR [ESP],0
          call _log_printf
L_426884:
          mov EAX,DWORD PTR [L_479f00]
          jmp L_4259c0
          .byte 0x66
          .byte 0x90
L_426890:
          mov DWORD PTR [ESP],OFFSET _str_nomobile
          call _iniBoolInvalid
          test EAX,EAX
          je L_426d60
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET _str_nomobile
          mov DWORD PTR [ESP+4],OFFSET _msg_iniInvalid
          mov DWORD PTR [ESP],0
          call _log_printf
L_4268c4:
          mov EAX,DWORD PTR [L_479f00]
          jmp L_4259b5
          .byte 0x66
          .byte 0x90
L_4268d0:
          mov DWORD PTR [ESP],OFFSET _str_nosusecurity
          call _iniBoolInvalid
          test EAX,EAX
          je L_426d23
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET _str_nosusecurity
          mov DWORD PTR [ESP+4],OFFSET _msg_iniInvalid
          mov DWORD PTR [ESP],0
          call _log_printf
L_426904:
          mov EAX,DWORD PTR [L_479f00]
          jmp L_4259f3
          .byte 0x66
          .byte 0x90
L_426910:
          mov DWORD PTR [ESP],OFFSET _str_smcnocheck
          call _iniBoolInvalid
          test EAX,EAX
          je L_426d9d
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET _str_smcnocheck
          mov DWORD PTR [ESP+4],OFFSET _msg_iniInvalid
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_4259fe
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_426950:
          mov DWORD PTR [ESP],OFFSET _str_nosecurity
          call _iniBoolInvalid
          test EAX,EAX
          je L_426e17
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET _str_nosecurity
          mov DWORD PTR [ESP+4],OFFSET _msg_iniInvalid
          mov DWORD PTR [ESP],0
          call _log_printf
L_426984:
          mov EAX,DWORD PTR [L_479f00]
          jmp L_4259e8
L_42698e:
          mov DWORD PTR [L_479f08],0
          jmp L_425d1a
L_42699d:
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],OFFSET L_458508
          call _getIniU32
          jmp L_425f89
L_4269b6:
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],OFFSET L_4584e0
          call _getIniU32
          jmp L_425f39
L_4269cf:
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],OFFSET L_458673
          call _getIniU32
          jmp L_426169
L_4269e8:
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],OFFSET L_458647
          call _getIniU32
          jmp L_426119
L_426a01:
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],OFFSET L_4585c0
          call _getIniU32
          jmp L_4260c9
L_426a1a:
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],OFFSET L_458590
          call _getIniU32
          jmp L_426079
L_426a33:
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],OFFSET L_45861f
          call _getIniU32
          jmp L_425ee9
L_426a4c:
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],OFFSET L_4585f6
          call _getIniU32
          jmp L_425e96
L_426a65:
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],OFFSET L_45855e
          call _getIniU32
          jmp L_426029
L_426a7e:
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],OFFSET L_458530
          call _getIniU32
          jmp L_425fd9
L_426a97:
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],OFFSET L_4586a5
          call _getIniU32
          jmp L_4261b9
L_426ab0:
          mov DWORD PTR [ESP],OFFSET _str_cygnos
          call _iniBoolInvalid
          test EAX,EAX
          je L_426f85
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET _str_cygnos
          mov DWORD PTR [ESP+4],OFFSET _msg_iniInvalid
          mov DWORD PTR [ESP],0
          call _log_printf
L_426ae4:
          mov EAX,DWORD PTR [L_479f00]
          jmp L_425b91
L_426aee:
          mov DWORD PTR [ESP],OFFSET _str_demon
          call _iniBoolInvalid
          test EAX,EAX
          je L_426e91
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET _str_demon
          mov DWORD PTR [ESP+4],OFFSET _msg_iniInvalid
          mov DWORD PTR [ESP],0
          call _log_printf
L_426b22:
          mov EAX,DWORD PTR [L_479f00]
          jmp L_425b99
L_426b2c:
          mov DWORD PTR [ESP+8],9
          mov DWORD PTR [ESP+4],OFFSET _str_remopower
          mov DWORD PTR [ESP],EBX
          call _strnicmp
          test EAX,EAX
          mov EDX,32
          je L_426769
          mov DWORD PTR [ESP+8],5
          mov DWORD PTR [ESP+4],OFFSET _str_remox
          mov DWORD PTR [ESP],EBX
          call _strnicmp
          test EAX,EAX
          mov EDX,34
          je L_426769
          mov DWORD PTR [ESP+8],9
          mov DWORD PTR [ESP+4],OFFSET _str_winbutton
          mov DWORD PTR [ESP],EBX
          call _strnicmp
          test EAX,EAX
          mov EDX,36
          je L_426769
          mov EAX,EBX
          call _parseButton.part.0
          mov EDX,EAX
          jmp L_426769
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_426bb0:
          mov DWORD PTR [ESP],OFFSET _str_smcnoblink
          call _iniBoolInvalid
          test EAX,EAX
          je L_426f0b
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET _str_smcnoblink
          mov DWORD PTR [ESP+4],OFFSET _msg_iniInvalid
          mov DWORD PTR [ESP],0
          call _log_printf
L_426be4:
          mov EDX,DWORD PTR [_g479ea8]
          mov EAX,DWORD PTR [L_479f00]
          jmp L_425bd6
L_426bf4:
          mov DWORD PTR [ESP],OFFSET _str_patchsmc
          call _iniBoolInvalid
          test EAX,EAX
          je L_426ece
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET _str_patchsmc
          mov DWORD PTR [ESP+4],OFFSET _msg_iniInvalid
          mov DWORD PTR [ESP],0
          call _log_printf
L_426c28:
          mov EAX,DWORD PTR [L_479f00]
          jmp L_425ba4
L_426c32:
          mov DWORD PTR [ESP],OFFSET _str_smcnoeject
          call _iniBoolInvalid
          test EAX,EAX
          je L_426f48
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET _str_smcnoeject
          mov DWORD PTR [ESP+4],OFFSET _msg_iniInvalid
          mov DWORD PTR [ESP],0
          call _log_printf
L_426c66:
          mov EAX,DWORD PTR [L_479f00]
          jmp L_425bc5
L_426c70:
          mov DWORD PTR [ESP],OFFSET _str_nodvd
          call _iniBoolInvalid
          test EAX,EAX
          je L_426fc2
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET _str_nodvd
          mov DWORD PTR [ESP+4],OFFSET _msg_iniInvalid
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_425be3
L_426ca9:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET _str_noecdremap
          call _getIniBool
          test EAX,EAX
          je L_42620b
          mov DWORD PTR [ESP+8],OFFSET _str_noecdremap
          mov DWORD PTR [ESP+4],OFFSET _msg_optIni
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_42668e
L_426ce6:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET _str_noremap
          call _getIniBool
          test EAX,EAX
          je L_426884
          mov DWORD PTR [ESP+8],OFFSET _str_noremap
          mov DWORD PTR [ESP+4],OFFSET _msg_optIni
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_4263ed
L_426d23:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET _str_nosusecurity
          call _getIniBool
          test EAX,EAX
          je L_426904
          mov DWORD PTR [ESP+8],OFFSET _str_nosusecurity
          mov DWORD PTR [ESP+4],OFFSET _msg_optIni
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_4264ed
L_426d60:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET _str_nomobile
          call _getIniBool
          test EAX,EAX
          je L_4268c4
          mov DWORD PTR [ESP+8],OFFSET _str_nomobile
          mov DWORD PTR [ESP+4],OFFSET _msg_optIni
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_42638d
L_426d9d:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET _str_smcnocheck
          call _getIniBool
          test EAX,EAX
          je L_4259fe
          mov DWORD PTR [ESP+8],OFFSET _str_smcnocheck
          mov DWORD PTR [ESP+4],OFFSET _msg_optIni
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_42643e
L_426dda:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET _str_olddvd
          call _getIniBool
          test EAX,EAX
          je L_425c30
          mov DWORD PTR [ESP+8],OFFSET _str_olddvd
          mov DWORD PTR [ESP+4],OFFSET _msg_optIni
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_426610
L_426e17:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET _str_nosecurity
          call _getIniBool
          test EAX,EAX
          je L_426984
          mov DWORD PTR [ESP+8],OFFSET _str_nosecurity
          mov DWORD PTR [ESP+4],OFFSET _msg_optIni
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_42648d
L_426e54:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET _str_nandmu
          call _getIniBool
          test EAX,EAX
          je L_426844
          mov DWORD PTR [ESP+8],OFFSET _str_nandmu
          mov DWORD PTR [ESP+4],OFFSET _msg_optIni
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_42653e
L_426e91:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET _str_demon
          call _getIniBool
          test EAX,EAX
          je L_426b22
          mov DWORD PTR [ESP+8],OFFSET _str_demon
          mov DWORD PTR [ESP+4],OFFSET _msg_optIni
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_4262a1
L_426ece:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET _str_patchsmc
          call _getIniBool
          test EAX,EAX
          je L_426c28
          mov DWORD PTR [ESP+8],OFFSET _str_patchsmc
          mov DWORD PTR [ESP+4],OFFSET _msg_optIni
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_4262f0
L_426f0b:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET _str_smcnoblink
          call _getIniBool
          test EAX,EAX
          je L_426be4
          mov DWORD PTR [ESP+8],OFFSET _str_smcnoblink
          mov DWORD PTR [ESP+4],OFFSET _msg_optIni
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_42658f
L_426f48:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET _str_smcnoeject
          call _getIniBool
          test EAX,EAX
          je L_426c66
          mov DWORD PTR [ESP+8],OFFSET _str_smcnoeject
          mov DWORD PTR [ESP+4],OFFSET _msg_optIni
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_4265e0
L_426f85:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET _str_cygnos
          call _getIniBool
          test EAX,EAX
          je L_426ae4
          mov DWORD PTR [ESP+8],OFFSET _str_cygnos
          mov DWORD PTR [ESP+4],OFFSET _msg_optIni
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_426252
L_426fc2:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET _str_nodvd
          call _getIniBool
          test EAX,EAX
          je L_425be3
          mov DWORD PTR [ESP+8],OFFSET _str_nodvd
          mov DWORD PTR [ESP+4],OFFSET _msg_optIni
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_42665d
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
_loadAddons:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,1580
          mov DWORD PTR [ESP],OFFSET L_458c9c
          call _getIniValue
          test EAX,EAX
          je L_42748e
          mov DWORD PTR [ESP],EAX
          mov EBX,EAX
          call _strlen
          test EAX,EAX
          mov DWORD PTR [ESP+24],EAX
          js L_42748e
          xor EAX,EAX
          xor EBP,EBP
          jmp L_427398
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_427380:
          test DL,DL
          je L_4273a1
          mov BYTE PTR [ESP+EAX*1+32],DL
          add EAX,1
L_42738b:
          add EBP,1
          cmp DWORD PTR [ESP+24],EBP
          jl L_42748e
L_427398:
          movzx EDX,BYTE PTR [EBX+EBP*1]
          cmp DL,58
          jne L_427380
L_4273a1:
          lea EDX,DWORD PTR [ESP+32]
          mov BYTE PTR [ESP+EAX*1+32],0
L_4273aa:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_4273aa
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          lea EAX,DWORD PTR [ESP+32]
          sbb EDX,3
          sub EDX,EAX
          xor EAX,EAX
          cmp EDX,4
          jbe L_42738b
          cmp DWORD PTR [L_4c4f94],15
          jg L_4274a0
          lea EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],OFFSET _str_binFmt
          mov DWORD PTR [ESP+8],EAX
          lea EAX,DWORD PTR [ESP+544]
          mov DWORD PTR [ESP],EAX
          call _sprintf
          mov EAX,DWORD PTR [L_4c4f94]
          test EAX,EAX
          jle L_4274d0
          mov EDI,OFFSET L_4c0c94
          xor ESI,ESI
          jmp L_427446
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_427430:
          mov EAX,DWORD PTR [L_4c4f94]
          add ESI,1
          add EDI,1068
          cmp ESI,EAX
          jge L_4274d0
L_427446:
          lea EAX,DWORD PTR [ESP+544]
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EAX
          call _stricmp
          test EAX,EAX
          jne L_427430
          mov DWORD PTR [ESP+28],EAX
          lea EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],OFFSET _msg_patchDuplicate
          mov DWORD PTR [ESP],1
          add EBP,1
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          cmp DWORD PTR [ESP+24],EBP
          mov EAX,DWORD PTR [ESP+28]
          jge L_427398
L_42748e:
          add ESP,1580
          mov EAX,1
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x66
          .byte 0x90
L_4274a0:
          mov DWORD PTR [ESP+28],EAX
          lea EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],OFFSET _msg_patchTooMany
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov EAX,DWORD PTR [ESP+28]
          jmp L_42738b
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4274d0:
          imul EAX,EAX,1068
          lea EDI,DWORD PTR [ESP+544]
          mov DWORD PTR [ESP+4],EDI
          add EAX,OFFSET L_4c0c94
          mov DWORD PTR [ESP],EAX
          call _strcpy
          add DWORD PTR [L_4c4f94],1
          xor EAX,EAX
          jmp L_42738b
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
L_4584de:
          .string "\n"
L_4584e0:
          .string "cputemp"
L_4584e8:
          .string "Using CPUTEMP option, value %d\n"
L_458508:
          .string "gputemp"
L_458510:
          .string "Using GPUTEMP option, value %d\n"
L_458530:
          .string "edramtemp"
          .zero 2
L_45853c:
          .string "Using EDRAMTEMP option, value %d\n"
L_45855e:
          .string "overcputemp"
          .zero 2
L_45856c:
          .string "Using OVERCPUTEMP option, value %d\n"
L_458590:
          .string "overgputemp"
L_45859c:
          .string "Using OVERGPUTEMP option, value %d\n"
L_4585c0:
          .string "overedramtemp"
          .zero 2
L_4585d0:
          .string "Using OVEREDRAMTEMP option, value %d\n"
L_4585f6:
          .string "cpufan"
          .zero 3
L_458600:
          .string "Using CPUFAN option, value %d\n"
L_45861f:
          .string "gpufan"
          .zero 2
L_458628:
          .string "Using GPUFAN option, value %d\n"
L_458647:
          .string "avregion"
L_458650:
          .string "Using AVREGION option, value 0x%x\n"
L_458673:
          .string "gameregion"
          .zero 2
L_458680:
          .string "Using GAMEREGION option, value 0x%x\n"
L_4586a5:
          .string "dvdregion"
          .zero 1
L_4586b0:
          .string "Using DVDREGION option, value 0x%x\n"
L_4586d4:
          .string "xellbutton"
          .zero 1
L_4586e0:
          .string "Using XELLBUTTON option, value %s\n"
L_458703:
          .string "xellbutton2"
          .zero 1
L_458710:
          .string "Using XELLBUTTON2 option, value %s\n"
L_458734:
          .string "dualboot"
          .zero 3
L_458740:
          .string "Using DUALBOOT option, value %s\n"
L_458761:
          .string "cfldv"
          .zero 1
L_458768:
          .string "***** WARNING: cfldv value %d on command line is too large, setting to max value of 32\n"
L_4587c0:
          .string "Using CFLDV option, value %d\n"
L_4587de:
          .string "macid"
L_4587e4:
          .string "Using MACID option address: "
L_458801:
          .string "%02x"
L_458806:
          .string ":"
L_458808:
          .string "\n\n***** ERROR: invalid values in macid %s provided on the command line!\n"
          .zero 3
L_458854:
          .string "\n\n***** ERROR: invalid length macid %s provided on the command line!\n"
L_45889a:
          .string "dvdkey"
          .zero 3
L_4588a4:
          .string "\n\n***** ERROR: unknown option '%s' with value '%s' provided on the command line!\n"
          .zero 2
L_4588f8:
          .string "\n\n***** ERROR: unknown or incomplete option '%s' provided on the command line!\n"
L_458948:
          .string "\n\n***** ERROR: parsing option '%s', value '%s' is incorrect!\n"
          .zero 2
L_458988:
          .string "***** WARNING: cfldv value %d in options.ini is too large, setting to max value of 32\n"
          .zero 1
L_4589e0:
          .string "***** WARNING: invalid characters in macid '"
          .zero 3
L_458a10:
          .string "' provided in ini file! Discarding!\n"
          .zero 3
L_458a38:
          .string "***** WARNING: invalid length macid '"
          .zero 2
L_458a60:
          .string "default console DVD eject button is being used to start xell\n"
          .zero 2
L_458aa0:
          .string "alternate xell button is disabled\n"
L_458ac3:
          .string "dualboot setting ignored!\n"
L_458ade:
          .string "rev"
L_458ae2:
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
L_458c9c:
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

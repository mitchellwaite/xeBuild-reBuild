# app/mode_extract.s -- "Usage: %s extract"
#
# original placement:
#   .eh_frame      00466a1c-00466a88
#   .rdata         0045132c-00451760
#   .rdata$zzz     00463904-00463930
#   .text          0040e020-0040e520

.intel_syntax noprefix
.globl FUN_40e200

.text
.p2align 4
FUN_40e020:
          sub ESP,28
          mov EAX,DWORD PTR [ESP+32]
          cmp EAX,5
          ja L_40e050
          jmp DWORD PTR [EAX*4+L_451620]
L_40e033:
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+4],OFFSET L_4513c8
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          nop
L_40e050:
          mov DWORD PTR [ESP+4],OFFSET L_44a4e0
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+8],OFFSET L_451493
          mov DWORD PTR [ESP+4],OFFSET L_45149c
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_4514d2
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+8],OFFSET L_451493
          mov DWORD PTR [ESP+4],OFFSET L_4514e0
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_4514ff
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_45150c
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_45154c
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_451584
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_4515a4
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_4515b0
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44a4e0
          mov DWORD PTR [ESP],0
          call _log_printf
          call _log_finish
          mov EAX,DWORD PTR [L_44a524]
          test EAX,EAX
          jne L_40e156
L_40e14a:
          mov DWORD PTR [ESP],1
          call FUN_449198
L_40e156:
          mov DWORD PTR [ESP+4],OFFSET L_451604
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [_iob]
          mov DWORD PTR [ESP],EAX
          call FUN_449178
          jmp L_40e14a
L_40e179:
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+4],OFFSET L_451414
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          jmp L_40e050
L_40e19a:
          mov DWORD PTR [ESP+4],OFFSET L_451454
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_40e050
L_40e1b3:
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+4],OFFSET L_45132c
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          jmp L_40e050
L_40e1d4:
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+4],OFFSET L_451378
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          jmp L_40e050
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
FUN_40e200:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,28
          mov EBP,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],OFFSET L_451638
          call _log_set_name
          mov DWORD PTR [ESP+4],OFFSET L_451640
          mov DWORD PTR [ESP],0
          call _log_printf
          test EBP,EBP
          jle L_40e4e4
          mov EBX,DWORD PTR [ESP+52]
          xor EDI,EDI
          xor ESI,ESI
          jmp L_40e260
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_40e240:
          test DL,DL
          je L_40e508
          test EDI,EDI
          jne L_40e4f8
          mov EDI,EAX
L_40e252:
          add ESI,1
          add EBX,4
          cmp EBP,ESI
          je L_40e320
L_40e260:
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],OFFSET L_4516b1
          mov EAX,DWORD PTR [EBX]
          mov DWORD PTR [ESP],EAX
          call FUN_4491d0
          test EAX,EAX
          je L_40e4b5
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],OFFSET L_4516b6
          mov EAX,DWORD PTR [EBX]
          mov DWORD PTR [ESP],EAX
          call FUN_4491d0
          test EAX,EAX
          je L_40e4b5
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],OFFSET L_4516b9
          mov EAX,DWORD PTR [EBX]
          mov DWORD PTR [ESP],EAX
          call FUN_4491d0
          test EAX,EAX
          je L_40e4b5
          mov EAX,DWORD PTR [EBX]
          movzx EDX,BYTE PTR [EAX]
          cmp DL,45
          jne L_40e240
          mov DWORD PTR [ESP+8],8
          mov DWORD PTR [ESP+4],OFFSET L_4516bc
          mov DWORD PTR [ESP],EAX
          call FUN_4491d0
          test EAX,EAX
          jne L_40e480
          mov DWORD PTR [ESP+4],OFFSET L_4516c8
          mov DWORD PTR [ESP],0
          add ESI,1
          call _log_printf
          add EBX,4
          cmp EBP,ESI
          mov DWORD PTR [L_44a524],0
          jne L_40e260
L_40e320:
          test EDI,EDI
          je L_40e4e4
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [L_4c8fe4],778859107
          mov DWORD PTR [L_4c8fe8],7235938
          mov DWORD PTR [L_4c8ffa],778396004
          mov DWORD PTR [L_4c8ffe],7235938
          mov DWORD PTR [L_4c9010],1702131813
          mov DWORD PTR [L_4c9014],1684366446
          mov DWORD PTR [L_4c9018],1852400174
          mov BYTE PTR [L_4c901c],0
          mov DWORD PTR [L_4c9026],1953653606
          mov DWORD PTR [L_4c902a],1852400174
          mov BYTE PTR [L_4c902e],0
          mov DWORD PTR [L_4c903c],1684235635
          mov DWORD PTR [L_4c9040],778138721
          mov DWORD PTR [L_4c9044],7235938
          mov DWORD PTR [L_4c9160],5
          call FUN_417680
          test EAX,EAX
          je L_40e4c9
          mov DWORD PTR [ESP+4],OFFSET L_451707
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44a4e0
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_45171c
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44a4e0
          mov DWORD PTR [ESP],1
          call _log_printf
          call FUN_414650
          mov DWORD PTR [ESP+4],OFFSET L_44a4e0
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_451734
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44a4e0
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [L_479f4c]
          mov DWORD PTR [ESP],0
          mov DWORD PTR [L_47a080],EAX
          call FUN_411800
          xor EAX,EAX
L_40e471:
          add ESP,28
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_40e480:
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],OFFSET L_4516ee
          mov EAX,DWORD PTR [EBX]
          mov DWORD PTR [ESP],EAX
          call FUN_4491d0
          test EAX,EAX
          jne L_40e252
          mov EAX,DWORD PTR [EBX]
          movzx EAX,BYTE PTR [EAX+2]
          mov DWORD PTR [ESP],EAX
          call _log_verbose_flag
          jmp L_40e252
L_40e4b5:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],0
          call FUN_40e020
L_40e4c9:
          mov DWORD PTR [ESP+4],OFFSET L_4516f1
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,4294967295
          jmp L_40e471
L_40e4e4:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],2
          call FUN_40e020
L_40e4f8:
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],5
          call FUN_40e020
L_40e508:
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],1
          call FUN_40e020
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop

.section .rdata,"dr"
.p2align 2
L_45132c:
          .string "\n\n***** ERROR: option flag %s on command line but no argument provided!\n"
          .zero 3
L_451378:
          .string "\n\n***** ERROR: option flag %s on command line not enough arguments provided!\n"
          .zero 2
L_4513c8:
          .string "\n\n***** ERROR: option flag %s on command line but option was already set!\n"
          .zero 1
L_451414:
          .string "\n\n***** ERROR: unknown option '%s' provided on command line!\n"
          .zero 2
L_451454:
          .string "\n\n***** ERROR: not enough info provided to carry out command!\n"
L_451493:
          .string "xeBuild"
          .zero 1
L_45149c:
          .string "Usage   :\n   %s extract <switch> <input NAND image>\n\n"
L_4514d2:
          .string "Examples:\n"
          .zero 3
L_4514e0:
          .string "   %s extract -v nanddump.bin\n"
L_4514ff:
          .string "\nSwitches:\n"
          .zero 1
L_45150c:
          .string "   -noenter : suppresses prompt for enter key when finished\n"
          .zero 3
L_45154c:
          .string "   -v       : shows more info during extract process\n"
          .zero 2
L_451584:
          .string "   -?       : shows this help\n\n"
L_4515a4:
          .string "legend:\n"
          .zero 3
L_4515b0:
          .string "<dir>       = path, absolute or relative, to a directory - do not terminate with /\n"
L_451604:
          .string "\npress <enter> to quit...\n"
          .zero 1
L_451620:
          .long L_40e050
          .long L_40e179
          .long L_40e19a
          .long L_40e1b3
          .long L_40e1d4
          .long L_40e033
L_451638:
          .string "extract"
L_451640:
          .string "***** NOTE: Most errors/warnings will be due to the fact extract mode does not process 1BL and CPU keys! *****\n\n"
L_4516b1:
          .string "help"
L_4516b6:
          .string "-?"
L_4516b9:
          .string "/?"
L_4516bc:
          .string "-noenter"
          .zero 3
L_4516c8:
          .string "<enter> key on completion suppressed\n"
L_4516ee:
          .string "-v"
L_4516f1:
          .string "Loading dump failed!\n"
L_451707:
          .string "Dump load success!\n\n"
L_45171c:
          .string "flash fs file list:\n"
          .zero 3
L_451734:
          .string "checking boot image (update mode test):\n"
          .zero 3

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
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_40e020 - .
          .byte 0xd5
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_40e200 - .
          .byte 0x18
          .byte 0x3
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
          .byte 0x30
          .byte 0x3
          .byte 0x6d
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
          .byte 0x48
          .byte 0xb

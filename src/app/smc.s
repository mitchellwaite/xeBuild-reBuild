# app/smc.s -- SMC checksum, type detection, reset-limit/eject/blink patches
#
# original placement:
#   .data          0044a480-0044a4e0
#   .eh_frame      00466590-004666a0
#   .rdata         00450480-0045066c
#   .rdata$zzz     00463880-004638ac
#   .text          0040bd30-0040c240

.intel_syntax noprefix
.globl FUN_40bd80
.globl FUN_40c020
.globl FUN_40c210

.text
.p2align 4
L_40bd30:
          mov ECX,DWORD PTR [ESP+8]
          mov EDX,DWORD PTR [ESP+4]
          cmp ECX,10
          jle L_40bd74
          sub ECX,6
          mov EAX,4
          jmp L_40bd57
L_40bd47:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_40bd50:
          add EAX,1
          cmp EAX,ECX
          je L_40bd74
L_40bd57:
          cmp BYTE PTR [EDX+EAX*1],5
          jne L_40bd50
          cmp BYTE PTR [EDX+EAX*1+2],229
          jne L_40bd50
          cmp BYTE PTR [EDX+EAX*1+4],180
          jne L_40bd50
          cmp BYTE PTR [EDX+EAX*1+5],5
          jne L_40bd50
          repz ret 
L_40bd74:
          xor EAX,EAX
          ret 
L_40bd77:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_40bd80:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,76
          mov ESI,DWORD PTR [ESP+96]
          mov EAX,DWORD PTR [ESP+100]
          mov BYTE PTR [ESP+57],120
          mov BYTE PTR [ESP+58],186
          mov BYTE PTR [ESP+59],182
          mov DWORD PTR [ESP+60],452985040
          lea EBX,DWORD PTR [ESI+4]
          sub EAX,4
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],EBX
          call _crc32
          mov EBP,EAX
          movzx EAX,BYTE PTR [ESI+256]
          mov DWORD PTR [ESP+4],OFFSET L_450480
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP],1
          shr AL,4
          movzx EAX,AL
          mov DWORD PTR [ESP+44],EAX
          call _log_printf
          cmp EBP,DWORD PTR [L_44a480]
          mov EAX,DWORD PTR [ESP+44]
          je L_40bf73
          cmp EBP,DWORD PTR [L_44a488]
          je L_40bf73
          cmp EBP,DWORD PTR [L_44a490]
          je L_40bf73
          cmp EBP,DWORD PTR [L_44a498]
          je L_40bf73
          cmp EBP,DWORD PTR [L_44a4a0]
          je L_40bf73
          cmp EBP,DWORD PTR [L_44a4a8]
          je L_40bf73
          cmp EBP,DWORD PTR [L_44a4b0]
          je L_40bf73
          cmp EBP,DWORD PTR [L_44a4b8]
          je L_40bf73
          cmp EBP,DWORD PTR [L_44a4c0]
          je L_40bf73
          cmp EBP,DWORD PTR [L_44a4c8]
          je L_40bf73
          cmp EBP,DWORD PTR [L_44a4d0]
          je L_40bf73
          movzx ECX,BYTE PTR [ESI+256]
          movzx EBP,BYTE PTR [ESI+258]
          movzx EDI,BYTE PTR [ESI+257]
          mov DWORD PTR [ESP],EAX
          mov BYTE PTR [ESP+44],CL
          call _getConsoleTypeStr
          movzx ECX,BYTE PTR [ESP+44]
          mov DWORD PTR [ESP+24],EBP
          mov DWORD PTR [ESP+20],EDI
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_4504c8
          mov DWORD PTR [ESP],1
          mov EDX,ECX
          and EDX,15
          mov DWORD PTR [ESP+16],EDX
          mov EDX,ECX
          shr DL,4
          movzx EBP,DL
          mov DWORD PTR [ESP+12],EBP
          call _log_printf
          cmp DWORD PTR [ESP+104],3
          je L_40bfd0
          cmp DWORD PTR [ESP+104],2
          je L_40bf22
          cmp DWORD PTR [ESP+104],1
          je L_40bef3
          cmp DWORD PTR [ESP+104],5
          jg L_40bef3
L_40bee6:
          mov EAX,1
L_40beeb:
          add ESP,76
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_40bef3:
          cmp DWORD PTR [ESP+100],10
          jle L_40bee6
          mov EAX,DWORD PTR [ESP+100]
          lea EAX,DWORD PTR [ESI+EAX*1-6]
          jmp L_40bf0b
L_40bf04:
          add EBX,1
          cmp EAX,EBX
          je L_40bee6
L_40bf0b:
          cmp BYTE PTR [EBX],5
          jne L_40bf04
          cmp BYTE PTR [EBX+2],229
          jne L_40bf04
          cmp BYTE PTR [EBX+4],180
          jne L_40bf04
          cmp BYTE PTR [EBX+5],5
          jne L_40bf04
L_40bf22:
          lea EAX,DWORD PTR [ESP+57]
          mov DWORD PTR [ESP+12],3
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+100]
          mov DWORD PTR [ESP+4],EAX
          call _findInstExists
          test EAX,EAX
          jne L_40bee6
          lea EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+12],4
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+100]
          mov DWORD PTR [ESP+4],EAX
          call _findInstExists
          test EAX,EAX
          setne AL
          movzx EAX,AL
          jmp L_40beeb
L_40bf73:
          movzx EBX,BYTE PTR [ESI+256]
          movzx EBP,BYTE PTR [ESI+258]
          movzx EDI,BYTE PTR [ESI+257]
          mov DWORD PTR [ESP],EAX
          call _getConsoleTypeStr
          mov DWORD PTR [ESP+4],OFFSET L_450494
          mov DWORD PTR [ESP+8],EAX
          mov EDX,EBX
          shr BL,4
          mov DWORD PTR [ESP+24],EBP
          and EDX,15
          movzx EBX,BL
          mov DWORD PTR [ESP+20],EDI
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+16],EDX
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,76
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_40bfd0:
          cmp DWORD PTR [ESP+100],10
          jle L_40bee6
          mov EAX,DWORD PTR [ESP+100]
          lea EDI,DWORD PTR [EAX-6]
          mov EAX,4
          jmp L_40bffb
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_40bff0:
          add EAX,1
          cmp EAX,EDI
          je L_40bee6
L_40bffb:
          cmp BYTE PTR [ESI+EAX*1],5
          jne L_40bff0
          cmp BYTE PTR [ESI+EAX*1+2],229
          jne L_40bff0
          cmp BYTE PTR [ESI+EAX*1+4],180
          jne L_40bff0
          cmp BYTE PTR [ESI+EAX*1+5],5
          jne L_40bff0
          xor EAX,EAX
          jmp L_40beeb
          .byte 0x8d
          .byte 0x76
          .byte 0x0
FUN_40c020:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,76
          mov EBX,DWORD PTR [ESP+104]
          mov ECX,DWORD PTR [ESP+100]
          mov EAX,DWORD PTR [ESP+96]
          test EBX,134217728
          lea EBP,DWORD PTR [ECX-4]
          lea EDI,DWORD PTR [EAX+4]
          .byte 0x0f,0x84; .long L_40c0c1-.-4   # je L_40c0c1
          cmp ECX,10
          jle L_40c0e0
          mov EAX,EDI
          sub ECX,6
          mov ESI,4
          jmp L_40c06a
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_40c060:
          add ESI,1
          add EAX,1
          cmp ECX,ESI
          je L_40c0e0
L_40c06a:
          cmp BYTE PTR [EAX],5
          jne L_40c060
          cmp BYTE PTR [EAX+2],229
          jne L_40c060
          cmp BYTE PTR [EAX+4],180
          jne L_40c060
          cmp BYTE PTR [EAX+5],5
          jne L_40c060
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_4505e0
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+44],EAX
          call _log_printf
          mov EAX,DWORD PTR [ESP+44]
          mov BYTE PTR [EAX],0
          mov EAX,DWORD PTR [ESP+96]
          mov BYTE PTR [EAX+ESI*1+1],0
          mov DWORD PTR [ESP+4],OFFSET L_45060c
          mov DWORD PTR [ESP],1
          call _log_printf
L_40c0c1:
          test EBX,OFFSET __ImageBase
          jne L_40c0fc
L_40c0c9:
          and EBX,8388608
          jne L_40c160
L_40c0d5:
          add ESP,76
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_40c0e0:
          mov DWORD PTR [ESP+4],OFFSET L_450634
          mov DWORD PTR [ESP],0
          call _log_printf
          test EBX,OFFSET __ImageBase
          je L_40c0c9
L_40c0fc:
          lea EAX,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP+20],4
          mov DWORD PTR [ESP+12],4
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+16],EAX
          lea EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+48],582193314
          mov DWORD PTR [ESP+56],8899
          mov DWORD PTR [ESP+8],EAX
          call _replaceInst
          test EAX,EAX
          je L_40c1f0
          mov DWORD PTR [ESP+4],OFFSET L_4504f8
          mov DWORD PTR [ESP],1
          call _log_printf
          and EBX,8388608
          je L_40c0d5
L_40c160:
          lea EAX,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP+20],8
          mov DWORD PTR [ESP+12],8
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+16],EAX
          lea EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+48],2463081188
          mov DWORD PTR [ESP+52],583967456
          mov DWORD PTR [ESP+56],2282468
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+60],0
          call _replaceInst
          test EAX,EAX
          je L_40c1d0
          mov DWORD PTR [ESP+4],OFFSET L_450568
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,76
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_40c1d0:
          mov DWORD PTR [ESP+4],OFFSET L_450598
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,76
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_40c1f0:
          mov DWORD PTR [ESP+4],OFFSET L_450524
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_40c0c9
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_40c210:
          push EBX
          sub ESP,24
          mov EAX,DWORD PTR [ESP+32]
          movzx EBX,BYTE PTR [EAX]
          movzx EDX,BYTE PTR [EAX+1]
          mov DWORD PTR [ESP],EAX
          shl EDX,16
          shl EBX,24
          or EBX,EDX
          call _calcConfigSum
          cmp EBX,EAX
          sete AL
          add ESP,24
          movzx EAX,AL
          pop EBX
          ret 
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90

.data
.p2align 5
L_44a480:
          .byte 0xdb
          .byte 0x59
          .byte 0x0
          .byte 0x3a
          .byte 0x7f
          .byte 0x13
          .byte 0x0
          .byte 0x0
L_44a488:
          .byte 0x9f
          .byte 0xab
          .byte 0x42
          .byte 0xba
          .byte 0xb4
          .byte 0x13
          .byte 0x0
          .byte 0x0
L_44a490:
          .byte 0x0
          .byte 0x46
          .byte 0x22
          .byte 0x74
          .byte 0xb4
          .byte 0x13
          .byte 0x0
          .byte 0x0
L_44a498:
          .byte 0x39
          .byte 0x66
          .byte 0xc9
          .byte 0xf9
          .byte 0xb3
          .byte 0x13
          .byte 0x0
          .byte 0x0
L_44a4a0:
          .byte 0x0
          .byte 0xed
          .byte 0x3a
          .byte 0x5b
          .byte 0xba
          .byte 0x12
          .byte 0x0
          .byte 0x0
L_44a4a8:
          .byte 0x3e
          .byte 0x61
          .byte 0xc
          .byte 0x1d
          .byte 0xa3
          .byte 0x12
          .byte 0x0
          .byte 0x0
L_44a4b0:
          .byte 0x17
          .byte 0xc2
          .byte 0x5b
          .byte 0x7e
          .byte 0xa3
          .byte 0x12
          .byte 0x0
          .byte 0x0
L_44a4b8:
          .byte 0xee
          .byte 0xb7
          .byte 0xd5
          .byte 0x9a
          .byte 0x57
          .byte 0x12
          .byte 0x0
          .byte 0x0
L_44a4c0:
          .byte 0x19
          .byte 0xe4
          .byte 0x4a
          .byte 0xb7
          .byte 0x42
          .byte 0x12
          .byte 0x0
          .byte 0x0
L_44a4c8:
          .byte 0xb2
          .byte 0xc3
          .byte 0xb0
          .byte 0xca
          .byte 0x80
          .byte 0x11
          .byte 0x0
          .byte 0x0
L_44a4d0:
          .byte 0xc1
          .byte 0x8f
          .byte 0xad
          .byte 0x6d
          .byte 0x80
          .byte 0x11
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
.p2align 2
L_450480:
          .string "SMC checksum: %08x\n"
L_450494:
          .string "known clean SMC found, type: %s v%d.%d(%d.%02d)\n"
          .zero 3
L_4504c8:
          .string "unknown SMC found, type: %s v%d.%d(%d.%02d)\n"
          .zero 3
L_4504f8:
          .string "SMC EJECT button disabled successfully!\n"
          .zero 3
L_450524:
          .string "\n******* WARNING: could not patch SMC to disable EJECT button.\n\n"
          .zero 3
L_450568:
          .string "SMC ROL center blink disabled successfully!\n"
          .zero 3
L_450598:
          .string "\n******* WARNING: could not patch SMC to disable ROL center blinking\n\n"
          .zero 1
L_4505e0:
          .string "patching SMC reset limit at offset: 0x%x\n"
          .zero 2
L_45060c:
          .string "SMC reset limit patched successfully!\n"
          .zero 1
L_450634:
          .string "\n******* WARNING: could not patch SMC reset limit!\n\n"
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
          .long L_40bd30 - .
          .byte 0x47
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_40bd80 - .
          .byte 0x9d
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
          .byte 0x43
          .byte 0xe
          .byte 0x60
          .byte 0x3
          .byte 0x67
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
          .byte 0x2
          .byte 0xd3
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
          .byte 0x0
          .byte 0x68
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x88
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_40c020 - .
          .byte 0xe9
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
          .byte 0x60
          .byte 0x2
          .byte 0xb1
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
          .byte 0x44
          .byte 0xb
          .byte 0x2
          .byte 0xe7
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
          .byte 0x45
          .byte 0xb
          .byte 0x57
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
          .byte 0x45
          .byte 0xb
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xf4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_40c210 - .
          .byte 0x2c
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
          .byte 0x63
          .byte 0xe
          .byte 0x8
          .byte 0x44
          .byte 0xc3
          .byte 0xe
          .byte 0x4

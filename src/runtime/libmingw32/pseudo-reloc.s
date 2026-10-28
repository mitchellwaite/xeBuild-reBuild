# runtime/libmingw32/pseudo-reloc.s -- byte match
#
# original placement:
#   .bss           00479e3c-00479e4c
#   .eh_frame      0046e218-0046e2c0
#   .rdata         004633c4-004634bc
#   .rdata$zzz     0046445c-00464488
#   .text          00446fe0-00447450

.intel_syntax noprefix
.globl FUN_447180
.globl L_479e48

.text
.p2align 4
FUN_446fe0:
          push EBX
          sub ESP,24
          mov EAX,DWORD PTR [_iob]
          mov DWORD PTR [ESP+8],27
          mov DWORD PTR [ESP+4],1
          lea EBX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],OFFSET L_4633c4
          add EAX,64
          mov DWORD PTR [ESP+12],EAX
          call _fwrite
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [_iob]
          add EAX,64
          mov DWORD PTR [ESP],EAX
          call FUN_449048
          call FUN_4491b0
L_447031:
          jmp FUN_447040
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
FUN_447040:
          push EDI
          push ESI
          push EBX
          sub ESP,48
          mov ESI,DWORD PTR [L_479e40]
          test ESI,ESI
          jle L_44712d
          mov EDI,DWORD PTR [L_479e44]
          xor EBX,EBX
          lea EDX,DWORD PTR [EDI+4]
          nop
L_447060:
          mov ECX,DWORD PTR [EDX]
          cmp ECX,EAX
          ja L_447074
          mov EDI,DWORD PTR [EDX+4]
          add ECX,DWORD PTR [EDI+8]
          cmp EAX,ECX
          jb L_447126
L_447074:
          add EBX,1
          add EDX,12
          cmp EBX,ESI
          jne L_447060
L_44707e:
          mov DWORD PTR [ESP],EAX
          mov ESI,EAX
          call FUN_447990
          test EAX,EAX
          mov EDI,EAX
          je L_44716a
          mov ESI,DWORD PTR [L_479e44]
          lea EBX,DWORD PTR [EBX+EBX*2]
          shl EBX,2
          add ESI,EBX
          mov DWORD PTR [ESI+8],EAX
          mov DWORD PTR [ESI],0
          call FUN_447aa0
          add EAX,DWORD PTR [EDI+12]
          mov DWORD PTR [ESI+4],EAX
          lea EAX,DWORD PTR [ESP+20]
          mov DWORD PTR [ESP+8],28
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [L_479e44]
          mov EAX,DWORD PTR [EAX+EBX*1+4]
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [VirtualQuery]
          sub ESP,12
          test EAX,EAX
          je L_44714a
          mov EAX,DWORD PTR [ESP+40]
          lea EDX,DWORD PTR [EAX-4]
          and EDX,4294967291
          je L_44711f
          sub EAX,64
          and EAX,4294967231
          je L_44711f
          mov EAX,DWORD PTR [ESP+32]
          add EBX,DWORD PTR [L_479e44]
          mov DWORD PTR [ESP+8],64
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+20]
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [VirtualProtect]
          sub ESP,16
          test EAX,EAX
          je L_447134
L_44711f:
          add DWORD PTR [L_479e40],1
L_447126:
          add ESP,48
          pop EBX
          pop ESI
          pop EDI
          ret 
L_44712d:
          xor EBX,EBX
          jmp L_44707e
L_447134:
          call DWORD PTR [GetLastError]
          mov DWORD PTR [ESP],OFFSET L_463434
          mov DWORD PTR [ESP+4],EAX
          call FUN_446fe0
L_44714a:
          mov EAX,DWORD PTR [L_479e44]
          mov EAX,DWORD PTR [EAX+EBX*1+4]
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [EDI+8]
          mov DWORD PTR [ESP],OFFSET L_463400
          mov DWORD PTR [ESP+4],EAX
          call FUN_446fe0
L_44716a:
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],OFFSET L_4633e0
          call FUN_446fe0
          .byte 0x8d,0xb6,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
FUN_447180:
          push EBP
          mov EBP,ESP
          push EDI
          push ESI
          push EBX
          sub ESP,76
          mov EBX,DWORD PTR [L_479e3c]
          test EBX,EBX
          je L_4471a0
L_447193:
          lea ESP,DWORD PTR [EBP-12]
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_4471a0:
          mov DWORD PTR [L_479e3c],1
          call FUN_447a00
          lea EAX,DWORD PTR [EAX+EAX*2]
          lea EAX,DWORD PTR [EAX*4+30]
          shr EAX,4
          shl EAX,4
          call ___chkstk_ms
          mov DWORD PTR [L_479e40],0
          sub ESP,EAX
          lea EAX,DWORD PTR [ESP+31]
          and EAX,4294967280
          mov DWORD PTR [L_479e44],EAX
          mov EAX,OFFSET ___RUNTIME_PSEUDO_RELOC_LIST_END__
          sub EAX,OFFSET ___RUNTIME_PSEUDO_RELOC_LIST__
          cmp EAX,7
          jle L_447193
          cmp EAX,11
          jle L_447360
          mov EAX,DWORD PTR [___RUNTIME_PSEUDO_RELOC_LIST__]
          test EAX,EAX
          jne L_447288
          mov EAX,DWORD PTR [___RUNTIME_PSEUDO_RELOC_LIST__+4]
          test EAX,EAX
          jne L_447288
          mov EAX,DWORD PTR [___RUNTIME_PSEUDO_RELOC_LIST__+8]
          mov ESI,OFFSET ___RUNTIME_PSEUDO_RELOC_LIST__+12
          test EAX,EAX
          je L_447365
          mov ESI,OFFSET ___RUNTIME_PSEUDO_RELOC_LIST__
L_447221:
          mov EAX,DWORD PTR [ESI+8]
          cmp EAX,1
          jne L_447433
          add ESI,12
          cmp ESI,OFFSET ___RUNTIME_PSEUDO_RELOC_LIST_END__
          jae L_447193
          mov DWORD PTR [EBP-64],EBX
L_44723f:
          mov EAX,DWORD PTR [ESI]
          movzx EDX,BYTE PTR [ESI+8]
          mov EDI,DWORD PTR [ESI+4]
          lea ECX,DWORD PTR [EAX+__image_base__]
          mov EAX,DWORD PTR [EAX+__image_base__]
          cmp EDX,16
          lea EBX,DWORD PTR [EDI+__image_base__]
          mov DWORD PTR [EBP-60],EAX
          je L_44737f
          cmp EDX,32
          je L_4473f7
          cmp EDX,8
          je L_4473d0
          mov DWORD PTR [ESP+4],EDX
          mov DWORD PTR [ESP],OFFSET L_463490
          call FUN_446fe0
L_447288:
          mov ESI,OFFSET ___RUNTIME_PSEUDO_RELOC_LIST__
L_44728d:
          cmp ESI,OFFSET ___RUNTIME_PSEUDO_RELOC_LIST_END__
          jae L_447193
          mov DWORD PTR [EBP-60],EBX
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_4472a0:
          mov EDI,DWORD PTR [ESI+4]
          mov EDX,DWORD PTR [ESI]
          add ESI,8
          add EDX,DWORD PTR [EDI+__image_base__]
          lea EAX,DWORD PTR [EDI+__image_base__]
          mov EBX,EDX
          call FUN_447040
          cmp ESI,OFFSET ___RUNTIME_PSEUDO_RELOC_LIST_END__
          mov DWORD PTR [EDI+__image_base__],EBX
          jb L_4472a0
          mov EBX,DWORD PTR [EBP-60]
          mov EAX,DWORD PTR [L_479e40]
L_4472d1:
          test EAX,EAX
          jg L_4472ef
          jmp L_447193
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4472e0:
          add EBX,1
          cmp EBX,DWORD PTR [L_479e40]
          jge L_447193
L_4472ef:
          lea EDI,DWORD PTR [EBX+EBX*2]
          mov EAX,DWORD PTR [L_479e44]
          lea ESI,DWORD PTR [EDI*4]
          add EAX,ESI
          mov EDX,DWORD PTR [EAX]
          test EDX,EDX
          je L_4472e0
          lea ECX,DWORD PTR [EBP-52]
          mov DWORD PTR [ESP+8],28
          mov DWORD PTR [ESP+4],ECX
          mov EAX,DWORD PTR [EAX+4]
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [VirtualQuery]
          sub ESP,12
          test EAX,EAX
          je L_44740e
          lea EAX,DWORD PTR [EBP-56]
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [L_479e44]
          mov EAX,DWORD PTR [EAX+EDI*4]
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [EBP-40]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [EBP-52]
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [VirtualProtect]
          sub ESP,16
          jmp L_4472e0
L_447357:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_447360:
          mov ESI,OFFSET ___RUNTIME_PSEUDO_RELOC_LIST__
L_447365:
          mov EDI,DWORD PTR [ESI]
          test EDI,EDI
          jne L_44728d
          mov ECX,DWORD PTR [ESI+4]
          test ECX,ECX
          je L_447221
          jmp L_44728d
L_44737f:
          movzx EDX,WORD PTR [EDI+__image_base__]
          mov EAX,EDX
          or EAX,4294901760
          cmp WORD PTR [EDI+__image_base__],0
          cmovs EDX,EAX
          mov EAX,DWORD PTR [EBP-60]
          sub EDX,ECX
          add EAX,EDX
          mov DWORD PTR [EBP-52],EAX
          mov EAX,EBX
          call FUN_447040
          movzx EAX,WORD PTR [EBP-52]
          mov WORD PTR [EDI+__image_base__],AX
L_4473b4:
          add ESI,12
          cmp ESI,OFFSET ___RUNTIME_PSEUDO_RELOC_LIST_END__
          jb L_44723f
          mov EBX,DWORD PTR [EBP-64]
          mov EAX,DWORD PTR [L_479e40]
          jmp L_4472d1
L_4473d0:
          movzx EDX,BYTE PTR [EBX]
          mov EDI,EDX
          or EDI,4294967040
          cmp BYTE PTR [EBX],0
          cmovs EDX,EDI
          sub EDX,ECX
          add EAX,EDX
          mov DWORD PTR [EBP-52],EAX
          mov EAX,EBX
          call FUN_447040
          movzx EAX,BYTE PTR [EBP-52]
          mov BYTE PTR [EBX],AL
          jmp L_4473b4
L_4473f7:
          mov EAX,DWORD PTR [EBP-60]
          sub EAX,ECX
          add EAX,DWORD PTR [EBX]
          mov EDI,EAX
          mov DWORD PTR [EBP-52],EAX
          mov EAX,EBX
          call FUN_447040
          mov DWORD PTR [EBX],EDI
          jmp L_4473b4
L_44740e:
          mov ECX,DWORD PTR [L_479e44]
          add ECX,ESI
          mov EAX,DWORD PTR [ECX+4]
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ECX+8]
          mov EAX,DWORD PTR [EAX+8]
          mov DWORD PTR [ESP],OFFSET L_463400
          mov DWORD PTR [ESP+4],EAX
          call FUN_446fe0
L_447433:
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],OFFSET L_46345c
          call FUN_446fe0
          nop
          nop
          nop
          nop
          nop
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
L_4633c4:
          .string "Mingw-w64 runtime failure:\n"
L_4633e0:
          .string "Address %p has no image-section"
L_463400:
          .string "  VirtualQuery failed for %d bytes at address %p"
          .zero 3
L_463434:
          .string "  VirtualProtect failed with code 0x%x"
          .zero 1
L_46345c:
          .string "  Unknown pseudo relocation protocol version %d.\n"
          .zero 2
L_463490:
          .string "  Unknown pseudo relocation bit size %d.\n"
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
          .byte 0x18
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_446fe0 - .
          .byte 0x51
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
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x40
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_447040 - .
          .byte 0x3a
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
          .byte 0x40
          .byte 0x2
          .byte 0x90
          .byte 0xe
          .byte 0x34
          .byte 0x43
          .byte 0xe
          .byte 0x40
          .byte 0x7f
          .byte 0xe
          .byte 0x30
          .byte 0x43
          .byte 0xe
          .byte 0x40
          .byte 0x4e
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
          .byte 0x0
          .byte 0x0
          .byte 0x2c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x7c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_447180 - .
          .byte 0xc3
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x85
          .byte 0x2
          .byte 0x42
          .byte 0xd
          .byte 0x5
          .byte 0x46
          .byte 0x87
          .byte 0x3
          .byte 0x86
          .byte 0x4
          .byte 0x83
          .byte 0x5
          .byte 0x4e
          .byte 0xa
          .byte 0xc3
          .byte 0x41
          .byte 0xc6
          .byte 0x41
          .byte 0xc7
          .byte 0x41
          .byte 0xc5
          .byte 0xc
          .byte 0x4
          .byte 0x4
          .byte 0x46
          .byte 0xb
          .byte 0x0
          .byte 0x0

.bss
.p2align 2
L_479e3c:
          .zero 4
L_479e40:
          .zero 4
L_479e44:
          .zero 4
L_479e48:
          .zero 4

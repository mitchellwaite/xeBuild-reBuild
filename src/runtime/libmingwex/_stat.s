# runtime/libmingwex/_stat.s -- byte match
#
# original placement:
#   .eh_frame      0046ea1c-0046ea74
#   .rdata$zzz     00464640-0046466c
#   .text          00448820-00448a20

.intel_syntax noprefix
.globl FUN_448820

.text
.p2align 4
FUN_448820:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,92
          mov ESI,DWORD PTR [ESP+112]
          mov EBX,DWORD PTR [ESP+116]
          test ESI,ESI
          je L_4489d0
          movzx EDX,BYTE PTR [ESI]
          test DL,DL
          mov BYTE PTR [ESP+31],DL
          je L_4488e0
          mov DWORD PTR [ESP],ESI
          call FUN_449078
          cmp EAX,1
          mov EBP,EAX
          jle L_4488e0
          lea EAX,DWORD PTR [EAX-2]
          movzx EDX,BYTE PTR [ESP+31]
          cmp EAX,1
          jbe L_4489c0
L_44886a:
          cmp DL,92
          je L_448945
          cmp DL,47
          je L_448945
L_44887c:
          movzx EDX,BYTE PTR [ESI+EBP*1-1]
          cmp DL,47
          je L_44888d
          cmp DL,92
          mov EAX,ESI
          jne L_4488e2
L_44888d:
          mov DWORD PTR [ESP],EBP
          call FUN_449108
          mov EDI,EAX
          lea EAX,DWORD PTR [EBP-1]
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+8],EAX
          call FUN_4490f8
          lea EAX,DWORD PTR [ESP+44]
          mov BYTE PTR [EDI+EBP*1-1],0
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],EAX
          call FUN_4491e0
          cmp ESI,EDI
          mov EBP,EAX
          je L_4488f4
          mov DWORD PTR [ESP],EDI
          call FUN_449140
          jmp L_4488f4
          .byte 0x90
L_4488d0:
          test DL,DL
          jne L_4489ac
          nop
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_4488e0:
          mov EAX,ESI
L_4488e2:
          lea EDX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],EDX
          call FUN_4491e0
          mov EBP,EAX
L_4488f4:
          cmp EBP,-1
          je L_4489f0
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [EBX],EAX
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [EBX+4],EAX
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [EBX+8],EAX
          mov EAX,DWORD PTR [ESP+56]
          mov DWORD PTR [EBX+12],EAX
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [EBX+16],EAX
          mov EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [EBX+20],EAX
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [EBX+24],EAX
          mov EAX,DWORD PTR [ESP+72]
          mov DWORD PTR [EBX+28],EAX
          mov EAX,DWORD PTR [ESP+76]
          mov DWORD PTR [EBX+32],EAX
L_44893b:
          add ESP,92
          mov EAX,EBP
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_448945:
          movzx EAX,BYTE PTR [ESI+1]
          cmp AL,92
          je L_448955
          cmp AL,47
          jne L_44887c
L_448955:
          movzx EDX,BYTE PTR [ESI+2]
          lea EAX,DWORD PTR [ESI+2]
          test DL,DL
          jne L_44896c
          jmp L_4489e0
L_448962:
          add EAX,1
          movzx EDX,BYTE PTR [EAX]
          test DL,DL
          je L_4489e0
L_44896c:
          cmp DL,92
          je L_4489e0
          cmp DL,47
          jne L_448962
L_448976:
          add EAX,1
L_448979:
          movzx EDX,BYTE PTR [EAX]
          test DL,DL
          je L_4488e0
          cmp DL,92
          jne L_4489a7
          jmp L_4489ac
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_448990:
          add EAX,1
          movzx EDX,BYTE PTR [EAX]
          test DL,DL
          je L_4488d0
          cmp DL,92
          je L_4488d0
L_4489a7:
          cmp DL,47
          jne L_448990
L_4489ac:
          cmp BYTE PTR [EAX+1],0
          jne L_44887c
          jmp L_4488e0
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_4489c0:
          cmp BYTE PTR [ESI+1],58
          jne L_44886a
          jmp L_4488e0
          .byte 0x90
L_4489d0:
          xor EAX,EAX
          jmp L_4488e2
L_4489d7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_4489e0:
          test DL,DL
          je L_448979
          jmp L_448976
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_4489f0:
          lea EDI,DWORD PTR [EBX+4]
          mov DWORD PTR [EBX],0
          mov DWORD PTR [EBX+32],0
          xor EAX,EAX
          and EDI,4294967292
          sub EBX,EDI
          lea ECX,DWORD PTR [EBX+36]
          shr ECX,2
          rep stosd DWORD PTR ES:[EDI]
          jmp L_44893b
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
          .long FUN_448820 - .
          .byte 0xf4
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
          .byte 0x70
          .byte 0x3
          .byte 0x17
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
          .byte 0x41
          .byte 0xb

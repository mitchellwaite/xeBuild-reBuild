# bigdigits/mpSubtract.s -- assert path .../XeCrypt/bign/mpSubtract.c
#
# original placement:
#   .eh_frame      0046c948-0046c9a0
#   .rdata         00461c60-00461ca4
#   .rdata$zzz     00463ccc-00463cf8
#   .text          0043e550-0043e5e0

.intel_syntax noprefix
.globl FUN_43e550

.text
.p2align 4
FUN_43e550:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,28
          mov EDI,DWORD PTR [ESP+48]
          mov EBP,DWORD PTR [ESP+56]
          mov ESI,DWORD PTR [ESP+52]
          cmp EDI,EBP
          je L_43e5c0
L_43e567:
          mov EAX,DWORD PTR [ESP+60]
          test EAX,EAX
          je L_43e5bc
          xor EBX,EBX
          xor EAX,EAX
          mov DWORD PTR [ESP+52],ESI
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_43e580:
          mov ECX,DWORD PTR [ESP+52]
          mov EDX,DWORD PTR [ECX+EBX*4]
          sub EDX,EAX
          not EAX
          cmp EDX,EAX
          mov DWORD PTR [EDI+EBX*4],EDX
          seta AL
          sub EDX,DWORD PTR [EBP+EBX*4]
          movzx EAX,AL
          lea ECX,DWORD PTR [EAX+1]
          mov DWORD PTR [EDI+EBX*4],EDX
          mov ESI,DWORD PTR [EBP+EBX*4]
          not ESI
          cmp EDX,ESI
          cmova EAX,ECX
          add EBX,1
          cmp DWORD PTR [ESP+60],EBX
          jne L_43e580
L_43e5b4:
          add ESP,28
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_43e5bc:
          xor EAX,EAX
          jmp L_43e5b4
L_43e5c0:
          mov DWORD PTR [ESP+8],18
          mov DWORD PTR [ESP+4],OFFSET L_461c60
          mov DWORD PTR [ESP],OFFSET L_461c9b
          call FUN_448760
          jmp L_43e567
          .byte 0x90
          .byte 0x90

.section .rdata,"dr"
.p2align 2
L_461c60:
          .string "H:/x360sdk/__NAND/nandbuild_trin/XeCrypt/bign/mpSubtract.c"
L_461c9b:
          .string "w != v"
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
          .long FUN_43e550 - .
          .byte 0x8e
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
          .byte 0x43
          .byte 0xe
          .byte 0x30
          .byte 0x2
          .byte 0x60
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

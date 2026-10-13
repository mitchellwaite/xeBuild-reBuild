# bigdigits/mpMultiply.s -- assert path .../XeCrypt/bign/mpMultiply.c
#
# original placement:
#   .eh_frame      0046ce10-0046ce68
#   .rdata         00462438-004624a0
#   .rdata$zzz     00463d24-00463d50
#   .text          00440e20-00440f80

.intel_syntax noprefix
.globl FUN_440e20

.text
.p2align 4
FUN_440e20:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,60
          mov EBP,DWORD PTR [ESP+80]
          cmp EBP,DWORD PTR [ESP+84]
          mov EDI,DWORD PTR [ESP+88]
          je L_440f52
          cmp EBP,EDI
          je L_440f52
L_440e41:
          mov EAX,DWORD PTR [ESP+92]
          mov DWORD PTR [ESP],EBP
          add EAX,EAX
          mov DWORD PTR [ESP+4],EAX
          call FUN_4410e0
          mov EAX,DWORD PTR [ESP+92]
          xor EDX,EDX
          test EAX,EAX
          je L_440f48
          mov DWORD PTR [ESP+88],EDI
          mov EDI,EDX
          mov EDX,DWORD PTR [ESP+88]
          jmp L_440e8c
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_440e70:
          mov EAX,DWORD PTR [ESP+92]
          add EDI,1
          mov DWORD PTR [EBP+EAX*4],0
          add EBP,4
          cmp DWORD PTR [ESP+92],EDI
          je L_440f48
L_440e8c:
          mov EAX,DWORD PTR [EDX+EDI*4]
          test EAX,EAX
          je L_440e70
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+84]
          xor EBX,EBX
          mov DWORD PTR [ESP+28],EDX
          mov EAX,DWORD PTR [EAX]
          mov DWORD PTR [ESP+4],EAX
          lea EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP],EAX
          call FUN_442050
          mov EAX,DWORD PTR [ESP+40]
          mov ESI,DWORD PTR [ESP+44]
          mov EDX,DWORD PTR [ESP+28]
          nop
L_440ec0:
          xor ECX,ECX
          add EAX,DWORD PTR [EBP+EBX*4]
          setb CL
          mov DWORD PTR [ESP+40],EAX
          test ECX,ECX
          je L_440ed8
          add ESI,1
          mov DWORD PTR [ESP+44],ESI
L_440ed8:
          mov DWORD PTR [EBP+EBX*4],EAX
          add EBX,1
          cmp DWORD PTR [ESP+92],EBX
          je L_440f30
          mov EAX,DWORD PTR [EDX+EDI*4]
          mov DWORD PTR [ESP+28],EDX
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+84]
          mov EAX,DWORD PTR [EAX+EBX*4]
          mov DWORD PTR [ESP+4],EAX
          lea EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP],EAX
          call FUN_442050
          mov EAX,ESI
          xor ECX,ECX
          add EAX,DWORD PTR [ESP+40]
          mov ESI,DWORD PTR [ESP+44]
          mov EDX,DWORD PTR [ESP+28]
          setb CL
          mov DWORD PTR [ESP+40],EAX
          test ECX,ECX
          je L_440ec0
          mov ECX,DWORD PTR [ESP+44]
          lea ESI,DWORD PTR [ECX+1]
          mov DWORD PTR [ESP+44],ESI
          jmp L_440ec0
          .byte 0x90
L_440f30:
          mov EAX,DWORD PTR [ESP+92]
          add EDI,1
          mov DWORD PTR [EBP+EAX*4],ESI
          add EBP,4
          cmp DWORD PTR [ESP+92],EDI
          jne L_440e8c
L_440f48:
          add ESP,60
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_440f52:
          mov DWORD PTR [ESP+8],17
          mov DWORD PTR [ESP+4],OFFSET L_462438
          mov DWORD PTR [ESP],OFFSET L_462473
          call FUN_448760
          jmp L_440e41
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

.section .rdata,"dr"
.p2align 3
L_462438:
          .string "H:/x360sdk/__NAND/nandbuild_trin/XeCrypt/bign/mpMultiply.c"
L_462473:
          .string "w != u && w != v"
          .zero 28

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
          .long FUN_440e20 - .
          .byte 0x53
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
          .byte 0x50
          .byte 0x3
          .byte 0x24
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

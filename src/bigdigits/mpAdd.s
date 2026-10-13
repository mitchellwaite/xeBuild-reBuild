# bigdigits/mpAdd.s -- assert path .../XeCrypt/bign/mpAdd.c
#
# original placement:
#   .eh_frame      0046d4fc-0046d554
#   .rdata         004628c0-00462900
#   .rdata$zzz     0046403c-00464068
#   .text          004420b0-00442130

.intel_syntax noprefix
.globl FUN_4420b0

.text
.p2align 4
FUN_4420b0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,28
          mov ESI,DWORD PTR [ESP+48]
          mov EDI,DWORD PTR [ESP+56]
          mov EBP,DWORD PTR [ESP+52]
          cmp ESI,EDI
          je L_442105
L_4420c7:
          mov EAX,DWORD PTR [ESP+60]
          test EAX,EAX
          je L_442101
          xor EBX,EBX
          xor EAX,EAX
L_4420d3:
          xor ECX,ECX
          add EAX,DWORD PTR [EBP+EBX*4]
          setb CL
          mov DWORD PTR [ESI+EBX*4],EAX
          add EAX,DWORD PTR [EDI+EBX*4]
          lea EDX,DWORD PTR [ECX+1]
          mov DWORD PTR [ESI+EBX*4],EAX
          cmp EAX,DWORD PTR [EDI+EBX*4]
          mov EAX,ECX
          cmovb EAX,EDX
          add EBX,1
          cmp DWORD PTR [ESP+60],EBX
          jne L_4420d3
L_4420f9:
          add ESP,28
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_442101:
          xor EAX,EAX
          jmp L_4420f9
L_442105:
          mov DWORD PTR [ESP+8],18
          mov DWORD PTR [ESP+4],OFFSET L_4628c0
          mov DWORD PTR [ESP],OFFSET L_4628f6
          call FUN_448760
          jmp L_4420c7
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
.p2align 5
L_4628c0:
          .string "H:/x360sdk/__NAND/nandbuild_trin/XeCrypt/bign/mpAdd.c"
L_4628f6:
          .string "w != v"
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
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_4420b0 - .
          .byte 0x73
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
          .byte 0x45
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

# bigdigits/mpCompare.s -- compare from the top digit
#
# original placement:
#   .eh_frame      0046d214-0046d254
#   .rdata$zzz     00463f08-00463f34
#   .text          00441800-00441850

.intel_syntax noprefix
.globl FUN_441800

.text
.p2align 4
FUN_441800:
          push EBX
          mov EDX,DWORD PTR [ESP+16]
          mov ECX,DWORD PTR [ESP+8]
          mov EBX,DWORD PTR [ESP+12]
          test EDX,EDX
          lea EAX,DWORD PTR [EDX-1]
          je L_441826
L_441814:
          mov EDX,DWORD PTR [EBX+EAX*4]
          cmp DWORD PTR [ECX+EAX*4],EDX
          ja L_441830
          jb L_441840
          sub EAX,1
          cmp EAX,-1
          jne L_441814
L_441826:
          xor EAX,EAX
          pop EBX
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_441830:
          mov EAX,1
          pop EBX
          ret 
L_441837:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_441840:
          mov EAX,4294967295
          pop EBX
          ret 
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
          .byte 0x24
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_441800 - .
          .byte 0x47
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x68
          .byte 0xa
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x47
          .byte 0xb
          .byte 0x46
          .byte 0xa
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x4a
          .byte 0xb
          .byte 0x46
          .byte 0xc3
          .byte 0xe
          .byte 0x4

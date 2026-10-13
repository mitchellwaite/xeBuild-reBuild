# bigdigits/mpSetDigit.s -- set low digit, zero the rest
#
# original placement:
#   .eh_frame      0046d2ac-0046d2e4
#   .rdata$zzz     00463f60-00463f8c
#   .text          004418a0-004418e0

.intel_syntax noprefix
.globl FUN_4418a0

.text
.p2align 4
FUN_4418a0:
          push EBX
          sub ESP,24
          mov EAX,DWORD PTR [ESP+40]
          mov EBX,DWORD PTR [ESP+32]
          cmp EAX,1
          jbe L_4418cf
          lea EDX,DWORD PTR [EAX*4-4]
          lea EAX,DWORD PTR [EBX+4]
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP],EAX
          call FUN_4490f0
L_4418cf:
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [EBX],EAX
          add ESP,24
          pop EBX
          ret 
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
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_4418a0 - .
          .byte 0x3a
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
          .byte 0x74
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4

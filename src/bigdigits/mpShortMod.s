# bigdigits/mpShortMod.s -- remainder of mpShortDiv
#
# original placement:
#   .eh_frame      0046ce68-0046ce98
#   .rdata$zzz     00463d50-00463d7c
#   .text          00440f80-00440fc0

.intel_syntax noprefix
.globl FUN_440f80

.text
.p2align 4
FUN_440f80:
          sub ESP,540
          mov EAX,DWORD PTR [ESP+552]
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+548]
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+544]
          mov DWORD PTR [ESP+4],EAX
          lea EAX,DWORD PTR [ESP+16]
          mov DWORD PTR [ESP],EAX
          call FUN_441110
          add ESP,540
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
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_440f80 - .
          .byte 0x3a
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x46
          .byte 0xe
          .byte 0xa0
          .byte 0x4
          .byte 0x73
          .byte 0xe
          .byte 0x4

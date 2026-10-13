# bigdigits/mpModMult.s -- mpMultiply then mpModulo
#
# original placement:
#   .eh_frame      0046d554-0046d598
#   .rdata$zzz     00464068-00464094
#   .text          00442130-004421a0

.intel_syntax noprefix
.globl FUN_442130

.text
.p2align 4
FUN_442130:
          push ESI
          push EBX
          sub ESP,548
          mov EAX,DWORD PTR [ESP+568]
          mov EBX,DWORD PTR [ESP+576]
          lea ESI,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+564]
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+4],EAX
          call FUN_440e20
          mov EAX,DWORD PTR [ESP+572]
          mov DWORD PTR [ESP+16],EBX
          add EBX,EBX
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+560]
          mov DWORD PTR [ESP],EAX
          call FUN_441710
          add ESP,548
          xor EAX,EAX
          pop EBX
          pop ESI
          ret 
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          nop
          nop
          nop

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
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_442130 - .
          .byte 0x68
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x86
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x83
          .byte 0x3
          .byte 0x46
          .byte 0xe
          .byte 0xb0
          .byte 0x4
          .byte 0x2
          .byte 0x5b
          .byte 0xe
          .byte 0xc
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x0

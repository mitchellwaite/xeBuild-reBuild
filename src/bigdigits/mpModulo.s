# bigdigits/mpModulo.s -- mpDivide keeping the remainder
#
# original placement:
#   .eh_frame      0046d15c-0046d1a0
#   .rdata$zzz     00463e84-00463eb0
#   .text          00441710-00441780

.intel_syntax noprefix
.globl FUN_441710

.text
.p2align 4
FUN_441710:
          push ESI
          push EBX
          sub ESP,1060
          mov EAX,DWORD PTR [ESP+1084]
          mov ESI,DWORD PTR [ESP+1088]
          lea EBX,DWORD PTR [ESP+544]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP+16],EAX
          mov EAX,DWORD PTR [ESP+1080]
          mov DWORD PTR [ESP+20],ESI
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+1076]
          mov DWORD PTR [ESP+8],EAX
          lea EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EAX
          call FUN_446360
          mov EAX,DWORD PTR [ESP+1072]
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EAX
          call FUN_446200
          add ESP,1060
          xor EAX,EAX
          pop EBX
          pop ESI
          ret 
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
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_441710 - .
          .byte 0x6d
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
          .byte 0x8
          .byte 0x2
          .byte 0x60
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

# bigdigits/mpModInv.s -- extended Euclid
#
# original placement:
#   .eh_frame      0046d0f0-0046d15c
#   .rdata$zzz     00463e58-00463e84
#   .text          00441540-00441710

.intel_syntax noprefix
.globl FUN_441540

.text
.p2align 4
FUN_441540:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,2364
          mov EBX,DWORD PTR [ESP+2396]
          lea EBP,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+4],1
          lea EDI,DWORD PTR [ESP+560]
          lea ESI,DWORD PTR [ESP+816]
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+8],EBX
          call FUN_4418a0
          mov EAX,DWORD PTR [ESP+2388]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EAX
          lea EAX,DWORD PTR [ESP+304]
          mov DWORD PTR [ESP],EAX
          call FUN_446200
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EDI
          call FUN_4410e0
          mov EAX,DWORD PTR [ESP+2392]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],EAX
          call FUN_446200
          mov DWORD PTR [ESP+44],1
          jmp L_441695
L_4415c5:
          lea EAX,DWORD PTR [ESP+304]
          mov DWORD PTR [ESP+20],EBX
          mov DWORD PTR [ESP+16],ESI
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+8],EAX
          lea EAX,DWORD PTR [ESP+1328]
          mov DWORD PTR [ESP+4],EAX
          lea EAX,DWORD PTR [ESP+1584]
          mov DWORD PTR [ESP],EAX
          call FUN_446360
          lea EDX,DWORD PTR [ESP+1840]
          lea EAX,DWORD PTR [ESP+1584]
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP],EDX
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP+40],EDX
          call FUN_440e20
          mov EDX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP+8],EDX
          lea EDX,DWORD PTR [ESP+1072]
          mov DWORD PTR [ESP],EDX
          mov DWORD PTR [ESP+40],EDX
          call FUN_4420b0
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EBP
          call FUN_446200
          mov EDX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],EDX
          call FUN_446200
          lea EAX,DWORD PTR [ESP+304]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EAX
          call FUN_446200
          lea EAX,DWORD PTR [ESP+1328]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],EAX
          call FUN_446200
          neg DWORD PTR [ESP+44]
L_441695:
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],ESI
          call FUN_441f00
          test EAX,EAX
          je L_4415c5
          cmp DWORD PTR [ESP+44],-1
          je L_4416d4
          mov EAX,DWORD PTR [ESP+2384]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EAX
          call FUN_446200
          add ESP,2364
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_4416d4:
          mov EAX,DWORD PTR [ESP+2392]
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+2384]
          mov DWORD PTR [ESP],EAX
          call FUN_43e550
          add ESP,2364
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
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
          .byte 0x50
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_441540 - .
          .byte 0xc3
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
          .byte 0x46
          .byte 0xe
          .byte 0xd0
          .byte 0x12
          .byte 0x3
          .byte 0x83
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
          .byte 0x68
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

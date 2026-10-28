# runtime/libmingw32/atonexit.s -- byte match
#
# original placement:
#   .eh_frame      0046df18-0046df74
#   .rdata$zzz     004642d0-004642fc
#   .text          00446b30-00446c10

.intel_syntax noprefix
.globl FUN_446bf0

.text
.p2align 4
FUN_446b30:
          push EBX
          sub ESP,40
          mov EAX,DWORD PTR [___onexitbegin]
          mov DWORD PTR [ESP],EAX
          call FUN_446fc0
          cmp EAX,-1
          mov DWORD PTR [ESP+24],EAX
          je L_446bd0
          mov DWORD PTR [ESP],8
          call FUN_449208
          mov EAX,DWORD PTR [___onexitbegin]
          mov DWORD PTR [ESP],EAX
          call FUN_446fc0
          mov DWORD PTR [ESP+24],EAX
          mov EAX,DWORD PTR [___onexitend]
          mov DWORD PTR [ESP],EAX
          call FUN_446fc0
          mov DWORD PTR [ESP+28],EAX
          lea EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+8],EAX
          lea EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],EAX
          call FUN_449290
          mov EBX,EAX
          mov EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP],EAX
          call FUN_446fd0
          mov DWORD PTR [___onexitbegin],EAX
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EAX
          call FUN_446fd0
          mov DWORD PTR [ESP],8
          mov DWORD PTR [___onexitend],EAX
          call FUN_4491c8
          add ESP,40
          mov EAX,EBX
          pop EBX
          ret 
          .byte 0x90
L_446bd0:
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [_onexit]
          add ESP,40
          mov EBX,EAX
          mov EAX,EBX
          pop EBX
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_446bf0:
          sub ESP,28
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EAX
          call FUN_446b30
          test EAX,EAX
          sete AL
          add ESP,28
          movzx EAX,AL
          neg EAX
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
          .long FUN_446b30 - .
          .byte 0xb6
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
          .byte 0x30
          .byte 0x2
          .byte 0x97
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x42
          .byte 0xb
          .byte 0x50
          .byte 0xe
          .byte 0x8
          .byte 0x45
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x48
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_446bf0 - .
          .byte 0x1d
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x54
          .byte 0xe
          .byte 0x4
          .byte 0x0

# runtime/libmingw32/tlssup.s -- byte match
#
# original placement:
#   .eh_frame      0046e0c8-0046e150
#   .rdata$zzz     004643ac-004643d8
#   .text          00446e10-00446ef0

.intel_syntax noprefix
.globl FUN_446e60
.globl L_446e10

.text
.p2align 4
L_446e10:
          sub ESP,28
          mov EAX,DWORD PTR [ESP+36]
          cmp EAX,3
          je L_446e30
          test EAX,EAX
          je L_446e30
          mov EAX,1
          add ESP,28
          ret 12
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_446e30:
          mov EDX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP],EAX
          call FUN_4477a0
          mov EAX,1
          add ESP,28
          ret 12
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8d
          .byte 0xbc
          .byte 0x27
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_446e60:
          push ESI
          push EBX
          sub ESP,20
          cmp DWORD PTR [L_44b6b8],2
          mov EAX,DWORD PTR [ESP+36]
          je L_446e7c
          mov DWORD PTR [L_44b6b8],2
L_446e7c:
          cmp EAX,2
          je L_446e93
          cmp EAX,1
          je L_446ec0
L_446e86:
          add ESP,20
          mov EAX,1
          pop EBX
          pop ESI
          ret 12
L_446e93:
          mov EBX,OFFSET L_510030
          mov ESI,OFFSET L_510030
          cmp ESI,EBX
          je L_446e86
L_446ea1:
          mov EAX,DWORD PTR [EBX]
          test EAX,EAX
          je L_446ea9
          call EAX
L_446ea9:
          add EBX,4
          cmp ESI,EBX
          jne L_446ea1
          add ESP,20
          mov EAX,1
          pop EBX
          pop ESI
          ret 12
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_446ec0:
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EAX
          call FUN_4477a0
          jmp L_446e86
          .byte 0x66
          .byte 0x90
L_446ee0:
          xor EAX,EAX
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
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_446e10 - .
          .byte 0x43
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x55
          .byte 0xa
          .byte 0xe
          .byte 0x4
          .byte 0x48
          .byte 0xb
          .byte 0x60
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_446e60 - .
          .byte 0x7e
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
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x64
          .byte 0xa
          .byte 0xe
          .byte 0xc
          .byte 0x46
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x43
          .byte 0xb
          .byte 0x60
          .byte 0xa
          .byte 0xe
          .byte 0xc
          .byte 0x46
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x46
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x78
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_446ee0 - .
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0

# bigdigits/mpShortDiv.s -- divide by one digit
#
# original placement:
#   .eh_frame      0046cf20-0046cf90
#   .rdata$zzz     00463dd4-00463e00
#   .text          00441110-004411f0

.intel_syntax noprefix
.globl FUN_441110

.text
.p2align 4
FUN_441110:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov ESI,DWORD PTR [ESP+72]
          mov EDI,DWORD PTR [ESP+76]
          test ESI,ESI
          je L_4411c2
          test EDI,EDI
          je L_4411c2
          mov EAX,2147483648
          xor EBX,EBX
          jmp L_44114e
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_441140:
          add EBX,1
          shr EAX,1
          cmp EBX,32
          je L_4411d0
L_44114e:
          test ESI,EAX
          je L_441140
          mov ECX,EBX
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+8],EBX
          shl ESI,CL
L_44115e:
          mov EAX,DWORD PTR [ESP+68]
          lea EBP,DWORD PTR [EDI-1]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP],EAX
          call FUN_441f40
          mov EDX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+20],EAX
          lea EDI,DWORD PTR [EDX+EDI*4-4]
L_441181:
          mov DWORD PTR [ESP+28],EAX
          mov EAX,DWORD PTR [EDI]
          sub EBP,1
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+12],ESI
          sub EDI,4
          mov DWORD PTR [ESP+24],EAX
          lea EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP+8],EAX
          lea EAX,DWORD PTR [ESP+20]
          mov DWORD PTR [ESP+4],EAX
          call FUN_446830
          cmp EBP,-1
          mov EAX,DWORD PTR [ESP+20]
          jne L_441181
          add ESP,44
          mov ECX,EBX
          shr EAX,CL
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_4411c2:
          add ESP,44
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_4411d0:
          mov ECX,32
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+8],32
          shl ESI,CL
          jmp L_44115e
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
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_441110 - .
          .byte 0xd8
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
          .byte 0x40
          .byte 0x2
          .byte 0xa2
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x45
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
          .byte 0x43
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
          .byte 0x45
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0

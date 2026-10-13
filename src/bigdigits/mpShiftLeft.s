# bigdigits/mpShiftLeft.s -- multi-digit shift left
#
# original placement:
#   .eh_frame      0046d428-0046d4ac
#   .rdata$zzz     00463fe4-00464010
#   .text          00441f40-00442050

.intel_syntax noprefix
.globl FUN_441f40

.text
.p2align 4
FUN_441f40:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          cmp DWORD PTR [ESP+72],31
          mov EAX,DWORD PTR [ESP+64]
          mov ESI,DWORD PTR [ESP+68]
          mov EDX,DWORD PTR [ESP+76]
          jbe L_441fc0
          mov EBX,DWORD PTR [ESP+72]
          mov EDI,ESI
          shr EBX,5
          lea ECX,DWORD PTR [EBX*4]
          sub EDI,ECX
          mov ECX,EDX
          .byte 0x66   # nop
          nop
L_441f70:
          sub ECX,1
          cmp ECX,-1
          je L_441f8a
L_441f78:
          cmp EBX,ECX
          ja L_441fb0
          mov EBP,DWORD PTR [EDI+ECX*4]
          mov DWORD PTR [EAX+ECX*4],EBP
          sub ECX,1
          cmp ECX,-1
          jne L_441f78
L_441f8a:
          mov EDI,EDX
          mov ECX,DWORD PTR [ESP+72]
          sub EDI,EBX
          mov EDI,DWORD PTR [ESI+EDI*4]
          and ECX,31
          shl EDI,CL
          test ECX,ECX
          .byte 0x0f,0x85; .long L_442021-.-4   # jne L_442021
L_441fa2:
          add ESP,44
          mov EAX,EDI
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_441fb0:
          mov DWORD PTR [EAX+ECX*4],0
          jmp L_441f70
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_441fc0:
          movzx ECX,BYTE PTR [ESP+72]
          mov EBX,4294967295
          shr EBX,CL
          mov ECX,32
          sub ECX,DWORD PTR [ESP+72]
          not EBX
          test EDX,EDX
          mov DWORD PTR [ESP+24],EBX
          mov DWORD PTR [ESP+28],ECX
          je L_442041
          lea EBP,DWORD PTR [ESI+EDX*4]
          xor EBX,EBX
          nop
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_441ff0:
          mov EDX,DWORD PTR [ESI]
          movzx ECX,BYTE PTR [ESP+28]
          add ESI,4
          mov EDI,DWORD PTR [ESP+24]
          add EAX,4
          and EDI,EDX
          shr EDI,CL
          movzx ECX,BYTE PTR [ESP+72]
          shl EDX,CL
          or EBX,EDX
          mov DWORD PTR [EAX-4],EBX
          cmp EBP,ESI
          mov EBX,EDI
          jne L_441ff0
          add ESP,44
          mov EAX,EDI
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_442021:
          mov DWORD PTR [ESP+12],EDX
          mov DWORD PTR [ESP+8],ECX
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],EAX
          call FUN_441f40
          add ESP,44
          or EDI,EAX
          pop EBX
          mov EAX,EDI
          pop ESI
          pop EDI
          pop EBP
          ret 
L_442041:
          xor EDI,EDI
          jmp L_441fa2
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
          .byte 0x68
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_441f40 - .
          .byte 0x8
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
          .byte 0x43
          .byte 0xe
          .byte 0x40
          .byte 0x2
          .byte 0x5e
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
          .byte 0x2
          .byte 0x6a
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
          .byte 0x57
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x10
          .byte 0x43
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

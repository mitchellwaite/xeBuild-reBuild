# bigdigits/mpShiftRight.s -- multi-digit shift right
#
# original placement:
#   .eh_frame      0046dd60-0046dde4
#   .rdata$zzz     004641f4-00464220
#   .text          00446230-00446360

.intel_syntax noprefix
.globl FUN_446230

.text
.p2align 4
FUN_446230:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          cmp DWORD PTR [ESP+72],31
          mov EBP,DWORD PTR [ESP+64]
          mov EAX,DWORD PTR [ESP+68]
          mov EDX,DWORD PTR [ESP+76]
          jbe L_4462b0
          mov EDI,DWORD PTR [ESP+72]
          shr EDI,5
          test EDX,EDX
          je L_446289
          lea ECX,DWORD PTR [EDI*4]
          mov EBX,EBP
          lea ESI,DWORD PTR [EDI+EDX*1]
          mov DWORD PTR [ESP+24],EDI
          sub EBX,ECX
          mov ECX,EDI
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_446270:
          cmp EDX,ECX
          jbe L_446311
          mov EDI,DWORD PTR [EAX+ECX*4]
          mov DWORD PTR [EBX+ECX*4],EDI
          add ECX,1
          cmp ECX,ESI
          jne L_446270
          mov EDI,DWORD PTR [ESP+24]
L_446289:
          mov ECX,DWORD PTR [ESP+72]
          mov EDI,DWORD PTR [EAX+EDI*4-4]
          and ECX,31
          shr EDI,CL
          test ECX,ECX
          jne L_446330
L_44629e:
          add ESP,44
          mov EAX,EDI
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4462b0:
          movzx ECX,BYTE PTR [ESP+72]
          mov EBX,4294967295
          lea ESI,DWORD PTR [EDX-1]
          shl EBX,CL
          mov ECX,32
          sub ECX,DWORD PTR [ESP+72]
          not EBX
          test EDX,EDX
          mov DWORD PTR [ESP+24],EBX
          mov DWORD PTR [ESP+28],ECX
          je L_446350
          xor EBX,EBX
          nop
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_4462e0:
          mov EDX,DWORD PTR [EAX+ESI*4]
          movzx ECX,BYTE PTR [ESP+28]
          mov EDI,DWORD PTR [ESP+24]
          and EDI,EDX
          shl EDI,CL
          movzx ECX,BYTE PTR [ESP+72]
          shr EDX,CL
          or EBX,EDX
          mov DWORD PTR [EBP+ESI*4],EBX
          sub ESI,1
          mov EBX,EDI
          cmp ESI,-1
          jne L_4462e0
          add ESP,44
          mov EAX,EDI
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_446311:
          mov DWORD PTR [EBX+ECX*4],0
          add ECX,1
          cmp ESI,ECX
          jne L_446270
          mov EDI,DWORD PTR [ESP+24]
          jmp L_446289
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_446330:
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+12],EDX
          mov DWORD PTR [ESP+8],ECX
          call FUN_446230
          add ESP,44
          or EDI,EAX
          pop EBX
          mov EAX,EDI
          pop ESI
          pop EDI
          pop EBP
          ret 
L_446350:
          xor EDI,EDI
          jmp L_44629e
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
          .byte 0x68
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_446230 - .
          .byte 0x27
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
          .byte 0x49
          .byte 0xb
          .byte 0x2
          .byte 0x5a
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
          .byte 0x76
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

# crypto/base64.s -- base64 alphabet, encode/decode
#
# original placement:
#   .eh_frame      0046cf90-0046d03c
#   .rdata         004624a0-00462600
#   .rdata$zzz     00463e00-00463e2c
#   .text          004411f0-00441400

.intel_syntax noprefix
.globl FUN_441330

.text
.p2align 4
L_4411f0:
          push EBP
          push EDI
          mov EBP,2863311531
          push ESI
          push EBX
          sub ESP,44
          mov ESI,DWORD PTR [ESP+68]
          shl ESI,5
          shr ESI,3
          mov EAX,ESI
          mul EBP
          shr EDX,1
          lea EAX,DWORD PTR [EDX+EDX*2]
          mov EDX,ESI
          sub EDX,EAX
          jne L_4412d0
          lea EDX,DWORD PTR [ESI*4]
          mov DWORD PTR [ESP+4],1
          mov EAX,EDX
          mul EBP
          shr EDX,1
          lea EAX,DWORD PTR [EDX+1]
          mov DWORD PTR [ESP],EAX
          call FUN_4491a0
          test ESI,ESI
          mov DWORD PTR [ESP+28],EAX
          mov EBX,DWORD PTR [ESP+64]
          je L_4412b9
L_441245:
          mov EBP,DWORD PTR [ESP+28]
          xor EDI,EDI
          nop
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_441250:
          movzx EAX,BYTE PTR [EBX+EDI*1+1]
          movzx EDX,BYTE PTR [EBX+EDI*1+2]
          add EBP,4
          shl EDX,16
          shl EAX,8
          or EAX,EDX
          movzx EDX,BYTE PTR [EBX+EDI*1]
          add EDI,3
          or EAX,EDX
          xor EDX,EDX
          mov ECX,EAX
          and ECX,63
          mov DL,BYTE PTR [ECX+L_4624a0]
          mov ECX,EAX
          shr ECX,6
          and ECX,63
          movzx ECX,BYTE PTR [ECX+L_4624a0]
          mov DH,CL
          mov ECX,EAX
          shr EAX,18
          shr ECX,12
          movzx EAX,BYTE PTR [EAX+L_4624a0]
          movzx EDX,DX
          and ECX,63
          movzx ECX,BYTE PTR [ECX+L_4624a0]
          shl EAX,24
          shl ECX,16
          or EDX,ECX
          or EDX,EAX
          mov DWORD PTR [EBP-4],EDX
          cmp EDI,ESI
          jb L_441250
L_4412b9:
          mov DWORD PTR [ESP],EBX
          call FUN_449140
          mov EAX,DWORD PTR [ESP+28]
          add ESP,44
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_4412d0:
          lea EDI,DWORD PTR [ESI+3]
          mov DWORD PTR [ESP+4],1
          sub EDI,EDX
          mov DWORD PTR [ESP],EDI
          call FUN_4491a0
          mov EBX,EAX
          mov EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP],EBX
          mov ESI,EDI
          mov DWORD PTR [ESP+4],EAX
          call FUN_4490f8
          lea EDX,DWORD PTR [EDI*4]
          mov DWORD PTR [ESP+4],1
          mov EAX,EDX
          mul EBP
          shr EDX,1
          lea EAX,DWORD PTR [EDX+1]
          mov DWORD PTR [ESP],EAX
          call FUN_4491a0
          mov DWORD PTR [ESP+28],EAX
          jmp L_441245
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_441330:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,28
          mov EDI,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP],EDI
          call FUN_449078
          test AL,3
          jne L_4413e0
          lea EBX,DWORD PTR [EAX+EAX*2]
          mov DWORD PTR [ESP+4],1
          mov EAX,EBX
          shr EBX,4
          shr EAX,2
          mov DWORD PTR [ESP],EAX
          call FUN_4491a0
          mov ESI,EAX
          mov EAX,DWORD PTR [ESP+48]
          mov EBP,ESI
          mov DWORD PTR [EAX],EBX
          xor EBX,EBX
          jmp L_4413c9
L_441374:
          movzx EAX,BYTE PTR [EDI+EBX*1+1]
          add EBP,3
          movzx EDX,BYTE PTR [EAX+L_462500]
          movzx EAX,BYTE PTR [EDI+EBX*1+2]
          movzx EAX,BYTE PTR [EAX+L_462500]
          shl EDX,6
          shl EAX,12
          or EDX,EAX
          movzx EAX,BYTE PTR [EDI+EBX*1]
          movzx EAX,BYTE PTR [EAX+L_462500]
          or EAX,EDX
          movzx EDX,BYTE PTR [EDI+EBX*1+3]
          add EBX,4
          movzx EDX,BYTE PTR [EDX+L_462500]
          shl EDX,18
          or EDX,EAX
          mov EAX,EDX
          mov BYTE PTR [EBP-3],DL
          shr EDX,16
          shr EAX,8
          mov BYTE PTR [EBP-1],DL
          mov BYTE PTR [EBP-2],AL
L_4413c9:
          mov DWORD PTR [ESP],EDI
          call FUN_449078
          cmp EBX,EAX
          jl L_441374
          add ESP,28
          mov EAX,ESI
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x90
L_4413e0:
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [EAX],0
          add ESP,28
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

.section .rdata,"dr"
.p2align 5
L_4624a0:
          .string "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
          .zero 31
L_462500:
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0x3e
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0x3f
          .byte 0x34
          .byte 0x35
          .byte 0x36
          .byte 0x37
          .byte 0x38
          .byte 0x39
          .byte 0x3a
          .byte 0x3b
          .byte 0x3c
          .byte 0x3d
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0x40
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0x0
          .byte 0x1
          .byte 0x2
          .byte 0x3
          .byte 0x4
          .byte 0x5
          .byte 0x6
          .byte 0x7
          .byte 0x8
          .byte 0x9
          .byte 0xa
          .byte 0xb
          .byte 0xc
          .byte 0xd
          .byte 0xe
          .byte 0xf
          .byte 0x10
          .byte 0x11
          .byte 0x12
          .byte 0x13
          .byte 0x14
          .byte 0x15
          .byte 0x16
          .byte 0x17
          .byte 0x18
          .byte 0x19
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0x1a
          .byte 0x1b
          .byte 0x1c
          .byte 0x1d
          .byte 0x1e
          .byte 0x1f
          .byte 0x20
          .byte 0x21
          .byte 0x22
          .byte 0x23
          .byte 0x24
          .byte 0x25
          .byte 0x26
          .byte 0x27
          .byte 0x28
          .byte 0x29
          .byte 0x2a
          .byte 0x2b
          .byte 0x2c
          .byte 0x2d
          .byte 0x2e
          .byte 0x2f
          .byte 0x30
          .byte 0x31
          .byte 0x32
          .byte 0x33
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff

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
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_4411f0 - .
          .byte 0x36
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
          .byte 0x46
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
          .byte 0xcc
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x41
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
          .byte 0x44
          .byte 0xb
          .byte 0x0
          .byte 0x50
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x5c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_441330 - .
          .byte 0xc4
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
          .byte 0x30
          .byte 0x2
          .byte 0xa1
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
          .byte 0x42
          .byte 0xb
          .byte 0x4d
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
          .byte 0x0
          .byte 0x0

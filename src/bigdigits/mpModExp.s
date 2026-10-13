# bigdigits/mpModExp.s -- square-and-multiply over mpModMult
#
# original placement:
#   .eh_frame      0046ce98-0046cef0
#   .rdata$zzz     00463d7c-00463da8
#   .text          00440fc0-004410e0

.intel_syntax noprefix
.globl FUN_440fc0

.text
.p2align 4
FUN_440fc0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,60
          mov EBX,DWORD PTR [ESP+96]
          mov EDI,DWORD PTR [ESP+80]
          test EBX,EBX
          je L_4410d7
          mov EAX,DWORD PTR [ESP+88]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EAX
          call FUN_4417d0
          mov EDX,DWORD PTR [ESP+88]
          mov DWORD PTR [ESP+44],EAX
          mov ECX,32
          mov EBP,DWORD PTR [EDX+EAX*4-4]
          mov EAX,2147483648
          jmp L_44100b
          .byte 0x90
L_441000:
          shr EAX,1
          sub ECX,1
          je L_4410d0
L_44100b:
          test EBP,EAX
          je L_441000
          cmp EAX,1
          je L_441070
          shr EAX,1
          mov ESI,EAX
L_441018:
          mov EAX,DWORD PTR [ESP+84]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],EAX
          call FUN_446200
          mov EAX,DWORD PTR [ESP+44]
          test EAX,EAX
          je L_4410c0
L_441038:
          lea EBP,DWORD PTR [EAX+1073741823]
L_44103e:
          mov EAX,DWORD PTR [ESP+92]
          mov DWORD PTR [ESP+16],EBX
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+12],EAX
          call FUN_442130
          mov EAX,DWORD PTR [ESP+88]
          test DWORD PTR [EAX+EBP*4],ESI
          jne L_441080
          cmp ESI,1
          je L_4410a5
L_441068:
          shr ESI,1
          jmp L_44103e
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_441070:
          sub DWORD PTR [ESP+44],1
          mov ESI,2147483648
          jmp L_441018
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_441080:
          mov EAX,DWORD PTR [ESP+92]
          mov DWORD PTR [ESP+16],EBX
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+84]
          mov DWORD PTR [ESP+8],EAX
          call FUN_442130
          cmp ESI,1
          jne L_441068
L_4410a5:
          sub DWORD PTR [ESP+44],1
          je L_4410c0
          mov ESI,2147483648
          mov EAX,DWORD PTR [ESP+44]
          .byte 0xe9; .long L_441038-.-4   # jmp L_441038
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4410c0:
          xor EAX,EAX
L_4410c2:
          add ESP,60
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4410d0:
          xor ESI,ESI
          jmp L_441018
L_4410d7:
          mov EAX,4294967295
          jmp L_4410c2
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
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_440fc0 - .
          .byte 0x1e
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
          .byte 0x50
          .byte 0x2
          .byte 0xfe
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
          .byte 0x47
          .byte 0xb
          .byte 0x0

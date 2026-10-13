# runtime/libmingw32/merr.s -- byte match
#
# original placement:
#   .bss           00479e34-00479e3c
#   .eh_frame      0046e150-0046e1ac
#   .rdata         00463290-004633c4
#   .rdata$zzz     004643d8-00464404
#   .text          00446ef0-00446fb0

.intel_syntax noprefix
.globl FUN_446f40
.globl L_446f50
.globl L_479e38

.text
.p2align 4
L_446ef0:
          sub ESP,60
          mov EAX,DWORD PTR [L_479e34]
          fld QWORD PTR [ESP+72]
          fld QWORD PTR [ESP+80]
          test EAX,EAX
          fld QWORD PTR [ESP+88]
          je L_446f31
          fxch ST(2)
          mov EDX,DWORD PTR [ESP+64]
          fstp QWORD PTR [ESP+24]
          fstp QWORD PTR [ESP+32]
          mov DWORD PTR [ESP+16],EDX
          mov EDX,DWORD PTR [ESP+68]
          fstp QWORD PTR [ESP+40]
          mov DWORD PTR [ESP+20],EDX
          lea EDX,DWORD PTR [ESP+16]
          mov DWORD PTR [ESP],EDX
          call EAX
          jmp L_446f37
L_446f31:
          fstp ST(0)
          fstp ST(0)
          fstp ST(0)
L_446f37:
          add ESP,60
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
FUN_446f40:
          mov EAX,DWORD PTR [ESP+4]
          mov DWORD PTR [L_479e34],EAX
          jmp L_449270
          .byte 0x66
          .byte 0x90
L_446f50:
          sub ESP,60
          mov ECX,OFFSET L_463290
          mov EAX,DWORD PTR [ESP+64]
          mov EDX,DWORD PTR [EAX]
          sub EDX,1
          cmp EDX,5
          ja L_446f6d
          mov ECX,DWORD PTR [EDX*4+L_4633ac]
L_446f6d:
          fld QWORD PTR [EAX+24]
          fstp QWORD PTR [ESP+32]
          fld QWORD PTR [EAX+16]
          fstp QWORD PTR [ESP+24]
          fld QWORD PTR [EAX+8]
          fstp QWORD PTR [ESP+16]
          mov EAX,DWORD PTR [EAX+4]
          mov DWORD PTR [ESP+8],ECX
          mov DWORD PTR [ESP+4],OFFSET L_4632a0
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [_iob]
          add EAX,64
          mov DWORD PTR [ESP],EAX
          call FUN_449158
          xor EAX,EAX
          add ESP,60
          ret 
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90

.section .rdata,"dr"
.p2align 2
L_463290:
          .string "Unknown error"
          .zero 2
L_4632a0:
          .string "_matherr(): %s in %s(%g, %g)  (retval=%g)\n"
          .zero 1
L_4632cc:
          .string "Argument domain error (DOMAIN)"
L_4632eb:
          .string "Argument singularity (SIGN)"
          .zero 1
L_463308:
          .string "Overflow range error (OVERFLOW)"
L_463328:
          .string "The result is too small to be represented (UNDERFLOW)"
          .zero 2
L_463360:
          .string "Total loss of significance (TLOSS)"
          .zero 1
L_463384:
          .string "Partial loss of significance (PLOSS)"
          .zero 3
L_4633ac:
          .long L_4632cc
          .long L_4632eb
          .long L_463308
          .long L_463328
          .long L_463360
          .long L_463384

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
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_446ef0 - .
          .byte 0x4b
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x40
          .byte 0x2
          .byte 0x47
          .byte 0xe
          .byte 0x4
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x34
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_446f40 - .
          .byte 0xe
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x48
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_446f50 - .
          .byte 0x5b
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x40
          .byte 0x2
          .byte 0x57
          .byte 0xe
          .byte 0x4

.bss
.p2align 2
L_479e34:
          .zero 4
L_479e38:
          .zero 4

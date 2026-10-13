# bigdigits/mpDivide.s -- long division (quotient, remainder)
#
# original placement:
#   .eh_frame      0046dde4-0046de40
#   .rdata$zzz     00464220-0046424c
#   .text          00446360-00446830

.intel_syntax noprefix
.globl FUN_446360

.text
.p2align 4
FUN_446360:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,108
          mov EBX,DWORD PTR [ESP+140]
          mov EAX,DWORD PTR [ESP+128]
          mov ESI,DWORD PTR [ESP+136]
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],EBX
          call FUN_4410e0
          mov EAX,DWORD PTR [ESP+132]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EAX
          call FUN_4410e0
          mov EAX,DWORD PTR [ESP+148]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+144]
          mov DWORD PTR [ESP],EAX
          call FUN_4417d0
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],ESI
          mov EDI,EAX
          mov DWORD PTR [ESP+24],EAX
          call FUN_4417d0
          mov EDX,EAX
          mov DWORD PTR [ESP+56],EAX
          sub EDX,EDI
          test EDI,EDI
          mov DWORD PTR [ESP+36],EDX
          je L_446803
          cmp EDI,1
          je L_4467cf
          mov ECX,DWORD PTR [ESP+36]
          test ECX,ECX
          js L_4467b1
          je L_446764
L_4463f6:
          mov EAX,DWORD PTR [ESP+24]
          xor ECX,ECX
          lea EBX,DWORD PTR [EAX*4-4]
          mov EAX,DWORD PTR [ESP+144]
          add EAX,EBX
          mov DWORD PTR [ESP+48],EAX
          mov EDX,DWORD PTR [EAX]
          mov EAX,2147483648
          jmp L_44642a
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_446420:
          add ECX,1
          shr EAX,1
          cmp ECX,32
          je L_44642e
L_44642a:
          test EDX,EAX
          je L_446420
L_44642e:
          mov EDX,DWORD PTR [ESP+24]
          mov EAX,DWORD PTR [ESP+144]
          mov EDI,ECX
          mov DWORD PTR [ESP+8],ECX
          mov DWORD PTR [ESP+60],ECX
          mov DWORD PTR [ESP+12],EDX
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],EAX
          call FUN_441f40
          mov EBP,DWORD PTR [ESP+56]
          mov EAX,DWORD PTR [ESP+132]
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP],EAX
          call FUN_441f40
          mov EDX,DWORD PTR [ESP+144]
          mov EDI,DWORD PTR [ESP+132]
          lea EDX,DWORD PTR [EDX+EBX*1-4]
          mov DWORD PTR [ESP+52],EDX
          lea EDX,DWORD PTR [EDI+EBP*4]
          mov EDI,DWORD PTR [ESP+132]
          mov DWORD PTR [ESP+32],EDX
          mov EDX,DWORD PTR [ESP+36]
          shl EDX,2
          add EDI,EDX
          mov DWORD PTR [ESP+44],EDX
          mov EBP,EDI
L_4464a5:
          mov EDI,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+84],EAX
          mov ESI,DWORD PTR [ESP+48]
          mov EAX,DWORD PTR [EDI-4]
          mov DWORD PTR [ESP+80],EAX
          mov EAX,DWORD PTR [ESI]
          mov DWORD PTR [ESP+12],EAX
          lea EAX,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP+8],EAX
          lea EAX,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP+4],EAX
          lea EAX,DWORD PTR [ESP+72]
          mov DWORD PTR [ESP],EAX
          call FUN_446830
          test EAX,EAX
          je L_4466f1
          xor EAX,EAX
          mov ESI,DWORD PTR [ESI]
          add ESI,DWORD PTR [EDI-4]
          mov DWORD PTR [ESP+72],4294967295
          jb L_446817
L_4464f7:
          test EAX,EAX
          mov DWORD PTR [ESP+76],ESI
          jne L_446752
          mov EAX,4294967295
L_446508:
          mov EDX,DWORD PTR [ESP+32]
          mov EBX,DWORD PTR [EDX-8]
          mov EDX,DWORD PTR [ESP+52]
          mov ECX,DWORD PTR [EDX]
          mov DWORD PTR [ESP+4],EAX
          lea EAX,DWORD PTR [ESP+88]
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+8],ECX
          call FUN_442050
          cmp DWORD PTR [ESP+92],ESI
          jb L_446540
          ja L_446681
          cmp EBX,DWORD PTR [ESP+88]
          jb L_446681
          nop
L_446540:
          mov ESI,DWORD PTR [ESP+72]
L_446544:
          mov EAX,DWORD PTR [ESP+84]
          test ESI,ESI
          mov DWORD PTR [ESP+40],EAX
          je L_4465be
L_446550:
          mov EDX,DWORD PTR [ESP+24]
          xor EBX,EBX
          test EDX,EDX
          je L_4465ba
          xor EDI,EDI
          mov DWORD PTR [ESP+28],ESI
          mov ESI,EBP
          mov EBP,EDI
          mov EDI,DWORD PTR [ESP+144]
          nop
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_446570:
          mov EAX,DWORD PTR [EDI+EBP*4]
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+4],EAX
          lea EAX,DWORD PTR [ESP+88]
          mov DWORD PTR [ESP],EAX
          call FUN_442050
          mov EAX,DWORD PTR [ESI+EBP*4]
          mov ECX,DWORD PTR [ESP+88]
          sub EAX,EBX
          not EBX
          cmp EAX,EBX
          seta BL
          sub EAX,ECX
          not ECX
          cmp ECX,EAX
          movzx EBX,BL
          mov DWORD PTR [ESI+EBP*4],EAX
          adc EBX,DWORD PTR [ESP+92]
          add EBP,1
          cmp DWORD PTR [ESP+24],EBP
          jne L_446570
          mov EBP,ESI
          mov ESI,DWORD PTR [ESP+72]
L_4465ba:
          sub DWORD PTR [ESP+40],EBX
L_4465be:
          mov EAX,DWORD PTR [ESP+40]
          test EAX,EAX
          jne L_446700
          mov EDI,DWORD PTR [ESP+128]
          mov EDX,DWORD PTR [ESP+44]
          sub DWORD PTR [ESP+36],1
          mov DWORD PTR [EDI+EDX*1],ESI
          mov EDI,DWORD PTR [ESP+32]
          mov ESI,DWORD PTR [ESP+36]
          mov EAX,DWORD PTR [EDI-4]
          sub EDI,4
          mov DWORD PTR [ESP+32],EDI
          mov DWORD PTR [ESP+80],EAX
L_4465f3:
          sub EDX,4
          sub EBP,4
          cmp ESI,-1
          mov DWORD PTR [ESP+44],EDX
          jne L_4464a5
          mov EDX,DWORD PTR [ESP+56]
          cmp DWORD PTR [ESP+24],EDX
          jge L_446639
          mov EAX,EDX
          mov EDI,DWORD PTR [ESP+132]
          mov EDX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP+4],0
          sub EAX,EDX
          lea EDX,DWORD PTR [EDI+EDX*4]
          shl EAX,2
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],EDX
          call FUN_4490f0
L_446639:
          mov EDI,DWORD PTR [ESP+24]
          mov ESI,DWORD PTR [ESP+60]
          mov EAX,DWORD PTR [ESP+132]
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],EAX
          call FUN_446230
          mov EAX,DWORD PTR [ESP+144]
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],EAX
          call FUN_446230
          xor EAX,EAX
L_446679:
          add ESP,108
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_446681:
          mov EAX,DWORD PTR [ESP+72]
          mov EDX,DWORD PTR [ESP+48]
          mov EDI,DWORD PTR [ESP+76]
          lea ESI,DWORD PTR [EAX-1]
          xor EAX,EAX
          add EDI,DWORD PTR [EDX]
          mov DWORD PTR [ESP+72],ESI
          jb L_44680d
L_44669e:
          test EAX,EAX
          mov DWORD PTR [ESP+76],EDI
          jne L_446544
          mov EAX,DWORD PTR [ESP+32]
          mov EBX,DWORD PTR [EAX-8]
          mov EAX,DWORD PTR [ESP+52]
          mov EAX,DWORD PTR [EAX]
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP+8],EAX
          lea EAX,DWORD PTR [ESP+88]
          mov DWORD PTR [ESP],EAX
          call FUN_442050
          cmp EDI,DWORD PTR [ESP+92]
          ja L_446540
          jb L_4466e1
          cmp EBX,DWORD PTR [ESP+88]
          jae L_446540
L_4466e1:
          mov EAX,DWORD PTR [ESP+72]
          lea ESI,DWORD PTR [EAX-1]
          mov DWORD PTR [ESP+72],ESI
          jmp L_446544
L_4466f1:
          mov ESI,DWORD PTR [ESP+76]
          mov EAX,DWORD PTR [ESP+72]
          jmp L_446508
          .byte 0x66
          .byte 0x90
L_446700:
          mov EDX,DWORD PTR [ESP+128]
          mov EDI,DWORD PTR [ESP+44]
          sub ESI,1
          mov EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [EDX+EDI*1],ESI
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+144]
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+8],EAX
          call FUN_4420b0
          mov EDX,DWORD PTR [ESP+32]
          sub DWORD PTR [ESP+36],1
          mov ESI,DWORD PTR [ESP+36]
          mov EAX,DWORD PTR [EDX-4]
          sub EDX,4
          mov DWORD PTR [ESP+32],EDX
          mov EDX,EDI
          mov DWORD PTR [ESP+80],EAX
          jmp L_4465f3
L_446752:
          mov EAX,DWORD PTR [ESP+84]
          mov ESI,4294967295
          mov DWORD PTR [ESP+40],EAX
          jmp L_446550
L_446764:
          mov EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+144]
          mov DWORD PTR [ESP+4],EAX
          call FUN_441800
          test EAX,EAX
          js L_4467b1
          jne L_4463f6
          mov DWORD PTR [ESP+24],EAX
          mov EAX,DWORD PTR [ESP+128]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_4418a0
          mov EAX,DWORD PTR [ESP+24]
          jmp L_446679
L_4467b1:
          mov EAX,DWORD PTR [ESP+132]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EAX
          call FUN_446200
          xor EAX,EAX
          jmp L_446679
L_4467cf:
          mov EAX,DWORD PTR [ESP+144]
          mov DWORD PTR [ESP+12],EBX
          mov EAX,DWORD PTR [EAX]
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+128]
          mov DWORD PTR [ESP],EAX
          call FUN_441110
          mov EDX,DWORD PTR [ESP+132]
          mov DWORD PTR [EDX],EAX
          xor EAX,EAX
          jmp L_446679
L_446803:
          mov EAX,4294967295
          jmp L_446679
L_44680d:
          mov EAX,1
          jmp L_44669e
L_446817:
          mov EAX,1
          jmp L_4464f7
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
          .byte 0x40
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_446360 - .
          .byte 0xc1
          .byte 0x4
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
          .byte 0x80
          .byte 0x1
          .byte 0x3
          .byte 0x15
          .byte 0x3
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
          .byte 0x41
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0

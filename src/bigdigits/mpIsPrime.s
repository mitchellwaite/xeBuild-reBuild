# bigdigits/mpIsPrime.s -- small-prime sieve + Rabin-Miller
#
# original placement:
#   .eh_frame      0046d2e4-0046d3fc
#   .rdata         00462620-004628c0
#   .rdata$zzz     00463f8c-00463fb8
#   .text          004418e0-00441f00

.intel_syntax noprefix
.globl _mpIsPrime
.globl _mpRabinMiller

.text
.p2align 4
L_4418e0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,1596
          mov EAX,DWORD PTR [ESP+1616]
          mov EBX,DWORD PTR [ESP+1620]
          test BYTE PTR [EAX],1
          jne L_441910
L_4418fd:
          add ESP,1596
          xor EAX,EAX
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
L_441910:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],997
          mov ESI,OFFSET L_462620
          mov DWORD PTR [ESP],EAX
          call _mpShortCmp
          test EAX,EAX
          mov EDI,DWORD PTR [ESP+1616]
          jg L_44194b
          jmp L_44196e
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_441940:
          add ESI,4
          cmp ESI,OFFSET L_4628bc
          je L_441994
L_44194b:
          mov DWORD PTR [ESP+8],EBX
          mov EAX,DWORD PTR [ESI]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],EAX
          call _mpShortMod
          test EAX,EAX
          jne L_441940
          jmp L_4418fd
L_441963:
          add ESI,4
          cmp ESI,OFFSET L_4628bc
          je L_4418fd
L_44196e:
          mov DWORD PTR [ESP+8],EBX
          mov EAX,DWORD PTR [ESI]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],EAX
          call _mpShortCmp
          test EAX,EAX
          jne L_441963
L_441984:
          add ESP,1596
          mov EAX,1
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_441994:
          mov EAX,DWORD PTR [ESP+1616]
          mov DWORD PTR [ESP+12],EBX
          lea EBP,DWORD PTR [ESP+304]
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP+4],EAX
          lea EAX,DWORD PTR [ESP+1072]
          mov DWORD PTR [ESP],EAX
          call _mpShortSub
          lea EAX,DWORD PTR [ESP+1072]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EAX
          lea EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],EAX
          call _mpSetEqual
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EBP
          call _mpSetZero
          test BYTE PTR [ESP+48],1
          jne L_441a2b
          nop
L_4419f0:
          lea EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],EAX
          call _mpShiftRight
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EBP
          call _mpShortAdd
          test BYTE PTR [ESP+48],1
          je L_4419f0
L_441a2b:
          mov EAX,DWORD PTR [ESP+1624]
          test EAX,EAX
          je L_441984
          lea ESI,DWORD PTR [ESP+1328]
          lea EDI,DWORD PTR [ESP+816]
          mov DWORD PTR [ESP+44],0
L_441a50:
          lea EAX,DWORD PTR [ESP+560]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EAX
          call _mpSetZero
L_441a63:
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],2
          call _spPseudoRand
          mov DWORD PTR [ESP+560],EAX
          mov EAX,DWORD PTR [ESP+1616]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EAX
          lea EAX,DWORD PTR [ESP+560]
          mov DWORD PTR [ESP],EAX
          call _mpCompare
          test EAX,EAX
          jns L_441a63
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],ESI
          call _mpSetZero
          mov EAX,DWORD PTR [ESP+1616]
          mov DWORD PTR [ESP+16],EBX
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+12],EAX
          lea EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+8],EAX
          lea EAX,DWORD PTR [ESP+560]
          mov DWORD PTR [ESP+4],EAX
          call _mpModExp
          jmp L_441af8
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_441ae0:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],ESI
          call _mpCompare
          test EAX,EAX
          jns L_4418fd
L_441af8:
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],ESI
          call _mpIsZero
          test EAX,EAX
          je L_441b24
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EDI
          call _mpShortCmp
          test EAX,EAX
          je L_441bc3
L_441b24:
          lea EAX,DWORD PTR [ESP+1072]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],EAX
          call _mpCompare
          test EAX,EAX
          je L_441bc3
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],ESI
          call _mpIsZero
          test EAX,EAX
          jne L_441b6f
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EDI
          call _mpShortCmp
          test EAX,EAX
          je L_4418fd
L_441b6f:
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],ESI
          call _mpShortAdd
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],ESI
          call _mpCompare
          test EAX,EAX
          jns L_441ae0
          mov EAX,DWORD PTR [ESP+1616]
          mov DWORD PTR [ESP+16],EBX
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+12],EAX
          call _mpModMult
          jmp L_441ae0
L_441bc3:
          add DWORD PTR [ESP+44],1
          mov EAX,DWORD PTR [ESP+44]
          cmp DWORD PTR [ESP+1624],EAX
          jne L_441a50
          jmp L_441984
          .byte 0x66
          .byte 0x90
_mpIsPrime:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,28
          mov ESI,DWORD PTR [ESP+48]
          mov EDI,DWORD PTR [ESP+52]
          test BYTE PTR [ESI],1
          jne L_441c00
L_441bf4:
          add ESP,28
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x66
          .byte 0x90
L_441c00:
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],997
          mov EBX,OFFSET L_462620
          mov DWORD PTR [ESP],ESI
          call _mpShortCmp
          test EAX,EAX
          jle L_441c4e
          mov EBP,OFFSET L_4628bc
          jmp L_441c2b
L_441c24:
          add EBX,4
          cmp EBP,EBX
          je L_441c64
L_441c2b:
          mov EAX,DWORD PTR [EBX]
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],EAX
          call _mpShortMod
          test EAX,EAX
          jne L_441c24
          jmp L_441bf4
L_441c43:
          add EBX,4
          cmp EBX,OFFSET L_4628bc
          je L_441bf4
L_441c4e:
          mov EAX,DWORD PTR [EBX]
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],EAX
          call _mpShortCmp
          test EAX,EAX
          jne L_441c43
L_441c64:
          add ESP,28
          mov EAX,1
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_441c71:
          jmp _mpRabinMiller
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
_mpRabinMiller:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,1596
          mov EAX,DWORD PTR [ESP+1616]
          mov EBX,DWORD PTR [ESP+1620]
          lea EBP,DWORD PTR [ESP+304]
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP+4],EAX
          lea EAX,DWORD PTR [ESP+1072]
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP],EAX
          call _mpShortSub
          lea EAX,DWORD PTR [ESP+1072]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EAX
          lea EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],EAX
          call _mpSetEqual
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EBP
          call _mpSetZero
          test BYTE PTR [ESP+48],1
          jne L_441d2b
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_441cf0:
          lea EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],EAX
          call _mpShiftRight
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EBP
          call _mpShortAdd
          test BYTE PTR [ESP+48],1
          je L_441cf0
L_441d2b:
          mov EAX,DWORD PTR [ESP+1624]
          test EAX,EAX
          je L_441ed9
          lea ESI,DWORD PTR [ESP+1328]
          lea EDI,DWORD PTR [ESP+816]
          mov DWORD PTR [ESP+44],0
L_441d50:
          lea EAX,DWORD PTR [ESP+560]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EAX
          call _mpSetZero
L_441d63:
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],2
          call _spPseudoRand
          mov DWORD PTR [ESP+560],EAX
          mov EAX,DWORD PTR [ESP+1616]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EAX
          lea EAX,DWORD PTR [ESP+560]
          mov DWORD PTR [ESP],EAX
          call _mpCompare
          test EAX,EAX
          jns L_441d63
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],ESI
          call _mpSetZero
          mov EAX,DWORD PTR [ESP+1616]
          mov DWORD PTR [ESP+16],EBX
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+12],EAX
          lea EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+8],EAX
          lea EAX,DWORD PTR [ESP+560]
          mov DWORD PTR [ESP+4],EAX
          call _mpModExp
          jmp L_441df8
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_441de0:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],ESI
          call _mpCompare
          test EAX,EAX
          jns L_441ef0
L_441df8:
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],ESI
          call _mpIsZero
          test EAX,EAX
          je L_441e24
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EDI
          call _mpShortCmp
          test EAX,EAX
          je L_441ec3
L_441e24:
          lea EAX,DWORD PTR [ESP+1072]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],EAX
          call _mpCompare
          test EAX,EAX
          je L_441ec3
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],ESI
          call _mpIsZero
          test EAX,EAX
          jne L_441e6f
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EDI
          call _mpShortCmp
          test EAX,EAX
          je L_441ef0
L_441e6f:
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],ESI
          call _mpShortAdd
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],ESI
          call _mpCompare
          test EAX,EAX
          jns L_441de0
          mov EAX,DWORD PTR [ESP+1616]
          mov DWORD PTR [ESP+16],EBX
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+12],EAX
          call _mpModMult
          jmp L_441de0
L_441ec3:
          add DWORD PTR [ESP+44],1
          mov EAX,DWORD PTR [ESP+44]
          cmp DWORD PTR [ESP+1624],EAX
          jne L_441d50
L_441ed9:
          add ESP,1596
          mov EAX,1
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_441ef0:
          add ESP,1596
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x90
          .byte 0x90
          .byte 0x90

.section .rdata,"dr"
.p2align 5
L_462620:
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x11
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x13
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x17
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1d
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1f
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x25
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x29
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x2b
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x2f
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x35
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x3b
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x3d
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x47
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x49
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x4f
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x53
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x59
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x61
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x65
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x67
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x6b
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x6d
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x71
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x7f
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x83
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x89
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8b
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x95
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x97
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x9d
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xa3
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xa7
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xad
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb3
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb5
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xbf
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc1
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc5
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc7
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd3
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xdf
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xe3
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xe5
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xe9
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xef
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xf1
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xfb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x7
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0xd
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0xf
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x15
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x19
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x1b
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x25
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x33
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x37
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x39
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x3d
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x4b
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x51
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x5b
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x5d
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x61
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x67
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x6f
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x75
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x7b
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x7f
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x85
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x8d
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x91
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x99
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0xa3
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0xa5
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0xaf
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0xb1
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0xb7
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0xbb
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0xc1
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0xc9
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0xcd
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0xcf
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0xd3
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0xdf
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0xe7
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0xeb
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0xf3
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0xf7
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0xfd
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x9
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0xb
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x1d
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x23
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x2d
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x33
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x39
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x3b
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x4b
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x51
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x57
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x59
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x5f
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x65
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x69
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x6b
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x77
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x81
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x83
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x87
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x8d
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x93
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x95
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0xa1
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0xa5
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0xab
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0xb3
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0xbd
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0xc5
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0xcf
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0xd7
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0xdd
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0xe3
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0xe7
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0xef
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0xf5
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0xf9
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x1
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x5
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x13
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x1d
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x29
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x2b
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x35
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x37
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x3b
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x3d
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x47
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x55
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x59
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x5b
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x5f
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x6d
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x71
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x73
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x77
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x8b
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x8f
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x97
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0xa1
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0xa9
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0xad
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0xb3
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0xb9
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0xc7
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0xcb
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0xd1
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0xd7
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0xdf
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0xe5
          .byte 0x3
          .byte 0x0
          .byte 0x0
L_4628bc:
          .zero 4

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
          .long L_4418e0 - .
          .byte 0xfe
          .byte 0x2
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
          .byte 0xc
          .byte 0x59
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
          .byte 0x47
          .byte 0xb
          .byte 0x2
          .byte 0x7a
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x46
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
          .byte 0x50
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x74
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _mpIsPrime - .
          .byte 0x91
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
          .byte 0x50
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
          .byte 0x43
          .byte 0xb
          .byte 0x2
          .byte 0x67
          .byte 0xe
          .byte 0x14
          .byte 0x46
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
          .byte 0x50
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc8
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _mpRabinMiller - .
          .byte 0x7d
          .byte 0x2
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
          .byte 0xc
          .byte 0x3
          .byte 0x55
          .byte 0x2
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x46
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
          .byte 0x48
          .byte 0xb
          .byte 0x46
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

# crypto/xecrypt.s -- XeCrypt-style API: SHA/HMAC (0x36/0x5c pads), RC4, DES, AES, RSA
#
# original placement:
#   .bss           00479ac0-00479ac4
#   .eh_frame      0046b424-0046be40
#   .rdata         0045cbe0-0045cbec
#   .rdata$zzz     00463bc4-00463bf0
#   .text          00433840-00436a50

.intel_syntax noprefix
.globl FUN_433ff0
.globl FUN_434090
.globl FUN_434110
.globl FUN_4345b0
.globl FUN_4346c0
.globl FUN_434850
.globl FUN_4348a0
.globl FUN_4348f0
.globl FUN_434950
.globl FUN_434960
.globl FUN_4349c0
.globl FUN_434a30
.globl FUN_434be0
.globl FUN_434c00
.globl FUN_435440
.globl FUN_435530
.globl FUN_435820
.globl FUN_435b00

.text
.p2align 4
FUN_433840:
          push EBP
          push EDI
          mov EDI,EAX
          push ESI
          push EBX
          mov EBP,EDX
          mov EBX,ECX
          sub ESP,92
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+60],ECX
          mov DWORD PTR [ESP+76],EAX
          call FUN_436b00
          mov DWORD PTR [ESP+40],EAX
          lea EAX,DWORD PTR [EDI+8]
          mov DWORD PTR [ESP+44],EDX
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+64],EAX
          call FUN_436b00
          mov DWORD PTR [ESP+32],EAX
          lea EAX,DWORD PTR [EDI+16]
          mov DWORD PTR [ESP+36],EDX
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+68],EAX
          call FUN_436b00
          mov DWORD PTR [ESP+48],EAX
          lea EAX,DWORD PTR [EDI+24]
          mov DWORD PTR [ESP+52],EDX
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+72],EAX
          call FUN_436b00
          test EBX,EBX
          mov ESI,EAX
          mov EDI,EDX
          je L_43395c
          mov DWORD PTR [ESP+56],0
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_4338c0:
          mov DWORD PTR [ESP],EBP
          call FUN_436b00
          mov ECX,DWORD PTR [ESP+32]
          mov EBX,DWORD PTR [ESP+36]
          add ECX,EAX
          adc EBX,EDX
          sub ESI,EAX
          sbb EDI,EDX
          mov DWORD PTR [ESP+24],ESI
          mov ESI,1
          mov DWORD PTR [ESP+28],EDI
          xor EDI,EDI
          cmp EDX,EBX
          ja L_4338f5
          jb L_4338f1
          cmp EAX,ECX
          ja L_4338f5
L_4338f1:
          xor ESI,ESI
          xor EDI,EDI
L_4338f5:
          add DWORD PTR [ESP+40],ESI
          mov ESI,DWORD PTR [ESP+24]
          adc DWORD PTR [ESP+44],EDI
          mov EDI,ECX
          shld ECX,EBX,29
          shld EBX,EDI,29
          mov EDI,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+36],EBX
          xor EBX,EBX
          mov DWORD PTR [ESP+32],ECX
          mov ECX,1
          cmp EDX,EDI
          jb L_433934
          ja L_433928
          cmp EAX,ESI
          jb L_433934
L_433928:
          mov ESI,DWORD PTR [ESP+24]
          mov EDI,DWORD PTR [ESP+28]
          xor ECX,ECX
          xor EBX,EBX
L_433934:
          sub DWORD PTR [ESP+48],ECX
          mov EAX,ESI
          sbb DWORD PTR [ESP+52],EBX
          add EBP,8
          add DWORD PTR [ESP+56],1
          shld ESI,EDI,31
          shld EDI,EAX,31
          mov EAX,DWORD PTR [ESP+56]
          cmp EAX,DWORD PTR [ESP+60]
          jne L_4338c0
L_43395c:
          mov EAX,DWORD PTR [ESP+76]
          mov EDX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+4],EDX
          mov DWORD PTR [ESP],EAX
          call FUN_436c50
          mov EAX,DWORD PTR [ESP+64]
          mov EDX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],EDX
          mov DWORD PTR [ESP],EAX
          call FUN_436c50
          mov EAX,DWORD PTR [ESP+68]
          mov EDX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+4],EDX
          mov DWORD PTR [ESP],EAX
          call FUN_436c50
          mov EAX,DWORD PTR [ESP+72]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP+8],EAX
          call FUN_436c50
          add ESP,92
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
FUN_4339d0:
          push EBP
          push EDI
          mov EBP,EAX
          push ESI
          push EBX
          mov EBX,ECX
          mov EDI,EDX
          sub ESP,44
          mov ESI,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP],ECX
          mov DWORD PTR [ESP+4],255
          mov DWORD PTR [ESP+8],ESI
          call FUN_4490f0
          mov BYTE PTR [EBX+ESI*1-1],0
          mov BYTE PTR [EBX+ESI*1-2],1
          mov DWORD PTR [ESP+8],20
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EBX
          call FUN_436e20
          test EDI,EDI
          je L_433a30
          cmp EDI,1
          je L_433a54
          mov BYTE PTR [EBX+20],0
          add ESP,44
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
L_433a30:
          mov DWORD PTR [EBX+20],83887124
          mov DWORD PTR [EBX+24],235078170
          mov DWORD PTR [EBX+28],151389483
          mov DWORD PTR [EBX+32],3154224
          add ESP,44
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_433a54:
          mov BYTE PTR [EBX+20],20
          mov BYTE PTR [EBX+21],4
          mov BYTE PTR [EBX+22],26
          mov BYTE PTR [EBX+23],2
          mov BYTE PTR [EBX+24],3
          mov BYTE PTR [EBX+25],14
          mov BYTE PTR [EBX+26],43
          mov BYTE PTR [EBX+27],5
          mov BYTE PTR [EBX+28],6
          mov BYTE PTR [EBX+29],7
          mov BYTE PTR [EBX+30],48
          mov BYTE PTR [EBX+31],31
          mov BYTE PTR [EBX+32],48
          mov BYTE PTR [EBX+33],0
          add ESP,44
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
          .byte 0x8d
          .byte 0xbf
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_433aa0:
          push EBP
          push EDI
          mov EBP,ECX
          push ESI
          push EBX
          mov EBX,EDX
          sub ESP,1084
          mov DWORD PTR [ESP+44],EAX
          mov EAX,DWORD PTR [ESP+1120]
          lea ESI,DWORD PTR [ESP+304]
          mov DWORD PTR [ESP+4],ECX
          mov DWORD PTR [ESP],EDX
          mov DWORD PTR [ESP+8],ESI
          lea EDI,DWORD PTR [EAX+EAX*1]
          mov DWORD PTR [ESP+16],EAX
          mov DWORD PTR [ESP+12],EDI
          call FUN_438460
          test EAX,EAX
          jne L_433af0
L_433adf:
          xor EAX,EAX
L_433ae1:
          add ESP,1084
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_433af0:
          mov EAX,DWORD PTR [ESP+1120]
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP+16],EAX
          mov EAX,DWORD PTR [ESP+1108]
          mov DWORD PTR [ESP+8],EAX
          lea EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],EAX
          call FUN_4380f0
          test EAX,EAX
          je L_433adf
          mov EAX,DWORD PTR [ESP+1120]
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+16],EAX
          mov EAX,DWORD PTR [ESP+1104]
          mov DWORD PTR [ESP+4],EAX
          call FUN_438460
          test EAX,EAX
          je L_433adf
          mov EAX,DWORD PTR [ESP+1120]
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP+16],EAX
          mov EAX,DWORD PTR [ESP+1104]
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+1112]
          mov DWORD PTR [ESP+8],EAX
          lea EAX,DWORD PTR [ESP+560]
          mov DWORD PTR [ESP],EAX
          call FUN_4380f0
          test EAX,EAX
          je L_433adf
          mov EAX,DWORD PTR [ESP+1120]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+12],EAX
          lea EAX,DWORD PTR [ESP+560]
          mov DWORD PTR [ESP+8],EAX
          lea EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+4],EAX
          call FUN_438860
          test EAX,EAX
          je L_433bcd
          mov EBX,DWORD PTR [ESP+1120]
L_433bb5:
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],ESI
          call FUN_4389b0
          test EAX,EAX
          je L_433bb5
L_433bcd:
          mov EAX,DWORD PTR [ESP+1120]
          mov EBX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+1116]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],EAX
          call FUN_4382c0
          mov EAX,DWORD PTR [ESP+1120]
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+16],EAX
          call FUN_438460
          test EAX,EAX
          je L_433adf
          mov EAX,DWORD PTR [ESP+1120]
          mov EBX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+1104]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],EAX
          call FUN_4382c0
          mov EAX,DWORD PTR [ESP+1120]
          mov DWORD PTR [ESP+4],EAX
          lea EAX,DWORD PTR [ESP+EAX*8+560]
          mov DWORD PTR [ESP],EAX
          call FUN_436df0
          lea EAX,DWORD PTR [ESP+560]
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],EAX
          call FUN_4389b0
          mov EAX,1
          jmp L_433ae1
          .byte 0x90
L_433c80:
          push EBP
          push EDI
          mov EBP,EAX
          push ESI
          push EBX
          mov EDI,EDX
          mov EBX,ECX
          sub ESP,556
          movzx EAX,BYTE PTR [EDX+22]
          test AL,AL
          je L_433ce0
          cmp AL,26
          je L_433d80
          lea ESI,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+8],ECX
          mov DWORD PTR [ESP+4],255
          mov DWORD PTR [ESP],ESI
          call FUN_4490f0
          mov BYTE PTR [ESP+EBX*1+31],0
          mov BYTE PTR [ESP+EBX*1+30],1
          mov DWORD PTR [ESP+8],20
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],ESI
          call FUN_436e20
          mov BYTE PTR [ESP+52],0
          jmp L_433d56
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_433ce0:
          lea ESI,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+8],ECX
          mov DWORD PTR [ESP+4],255
          mov DWORD PTR [ESP],ESI
          call FUN_4490f0
          mov BYTE PTR [ESP+EBX*1+31],0
          mov BYTE PTR [ESP+EBX*1+30],1
          mov DWORD PTR [ESP+8],20
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],ESI
          call FUN_436e20
          mov DWORD PTR [ESP+16],83887124
          mov DWORD PTR [ESP+20],235078170
          mov DWORD PTR [ESP+24],151389483
          mov DWORD PTR [ESP+28],3154224
          mov DWORD PTR [ESP+52],83887124
          mov DWORD PTR [ESP+56],235078170
          mov DWORD PTR [ESP+60],151389483
          mov DWORD PTR [ESP+64],3154224
L_433d56:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],ESI
          call FUN_449100
          test EAX,EAX
          sete AL
          add ESP,556
          pop EBX
          movzx EAX,AL
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
L_433d80:
          lea ESI,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+8],ECX
          mov DWORD PTR [ESP+4],255
          mov DWORD PTR [ESP],ESI
          call FUN_4490f0
          mov BYTE PTR [ESP+EBX*1+31],0
          mov BYTE PTR [ESP+EBX*1+30],1
          mov DWORD PTR [ESP+8],20
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],ESI
          call FUN_436e20
          mov BYTE PTR [ESP+52],20
          mov BYTE PTR [ESP+53],4
          mov BYTE PTR [ESP+54],26
          mov BYTE PTR [ESP+55],2
          mov BYTE PTR [ESP+56],3
          mov BYTE PTR [ESP+57],14
          mov BYTE PTR [ESP+58],43
          mov BYTE PTR [ESP+59],5
          mov BYTE PTR [ESP+60],6
          mov BYTE PTR [ESP+61],7
          mov BYTE PTR [ESP+62],48
          mov BYTE PTR [ESP+63],31
          mov BYTE PTR [ESP+64],48
          mov BYTE PTR [ESP+65],0
          jmp L_433d56
L_433e01:
          jmp FUN_433e10
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
FUN_433e10:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,140
          mov EDX,DWORD PTR [ESP+168]
          mov EBP,DWORD PTR [ESP+160]
          mov EAX,DWORD PTR [ESP+164]
          mov DWORD PTR [ESP+120],0
          test EDX,EDX
          je L_433fdf
          mov EDI,EAX
L_433e41:
          mov DWORD PTR [ESP],EBP
          call FUN_436b00
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+124],EAX
          call FUN_436b00
          mov DWORD PTR [ESP],EBP
          mov EBX,EAX
          call FUN_436b00
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+88],EAX
          mov DWORD PTR [ESP+92],EDX
          call FUN_436b00
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+96],EAX
          mov DWORD PTR [ESP+100],EDX
          call FUN_436b00
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+104],EAX
          mov DWORD PTR [ESP+108],EDX
          call FUN_436b00
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+112],EAX
          mov DWORD PTR [ESP+116],EDX
          call FUN_436b00
          mov DWORD PTR [ESP],EBP
          mov ESI,EDX
          call FUN_436b00
          mov EAX,DWORD PTR [ESP+124]
          shr EDX,24
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+32],EDX
          mov EDX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP+36],0
          mov DWORD PTR [ESP+40],0
          shl EAX,24
          add EDX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+48],0
          mov DWORD PTR [ESP+28],EAX
          mov ECX,DWORD PTR [ESP+28]
          adc ECX,DWORD PTR [ESP+36]
          shl EBX,8
          mov DWORD PTR [ESP+56],0
          and EBX,16711680
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+44],EBX
          mov EAX,EDX
          mov EBX,DWORD PTR [ESP+92]
          add EAX,DWORD PTR [ESP+40]
          mov EDX,ECX
          mov ECX,DWORD PTR [ESP+88]
          adc EDX,DWORD PTR [ESP+44]
          shld EBX,ECX,24
          mov ECX,DWORD PTR [ESP+96]
          and EBX,65280
          add EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+52],EBX
          mov EBX,DWORD PTR [ESP+100]
          adc EDX,DWORD PTR [ESP+52]
          shld EBX,ECX,8
          mov ECX,DWORD PTR [ESP+104]
          and EBX,255
          add EAX,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP+60],EBX
          mov EBX,DWORD PTR [ESP+108]
          adc EDX,DWORD PTR [ESP+60]
          shrd ECX,EBX,8
          mov EBX,ECX
          and EBX,4278190080
          mov DWORD PTR [ESP+64],EBX
          mov ECX,DWORD PTR [ESP+112]
          mov EBX,DWORD PTR [ESP+116]
          add EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+68],0
          adc EDX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+76],0
          mov DWORD PTR [ESP+84],0
          shrd ECX,EBX,24
          and ECX,16711680
          mov DWORD PTR [ESP+72],ECX
          add EAX,DWORD PTR [ESP+72]
          adc EDX,DWORD PTR [ESP+76]
          shr ESI,8
          and ESI,65280
          mov DWORD PTR [ESP+80],ESI
          add EAX,DWORD PTR [ESP+80]
          adc EDX,DWORD PTR [ESP+84]
          add EBP,8
          add EDI,8
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],EDX
          call FUN_436c50
          add DWORD PTR [ESP+120],1
          mov EAX,DWORD PTR [ESP+120]
          cmp DWORD PTR [ESP+168],EAX
          jne L_433e41
L_433fdf:
          add ESP,140
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
FUN_433ff0:
          push EBP
          push EDI
          xor EBP,EBP
          push ESI
          push EBX
          xor EAX,EAX
          xor EBX,EBX
          sub ESP,4
          mov DWORD PTR [ESP],EBP
          jmp L_434021
L_434002:
          xor EAX,EDX
          mov ECX,EAX
          xor ECX,3539749
          test AL,1
          cmovne EAX,ECX
          add EBX,1
          xor DWORD PTR [ESP],EDX
          shr EAX,1
          cmp EBX,128
          je L_43406a
L_434021:
          mov ESI,EBX
          mov ECX,EBX
          sar ESI,3
          add ESI,DWORD PTR [ESP+24]
          and ECX,7
          movzx EDI,BYTE PTR [ESI]
          mov EDX,EDI
          movzx EDX,DL
          sar EDX,CL
          and EDX,1
          cmp EBX,105
          jle L_434002
          cmp EBX,127
          je L_434072
          mov EBP,EAX
          and EBP,1
          cmp EDX,EBP
          je L_43405a
          mov EDX,1
          shl EDX,CL
          xor EDX,EDI
          mov BYTE PTR [ESI],DL
L_43405a:
          add EBX,1
          xor DWORD PTR [ESP],EBP
          shr EAX,1
          cmp EBX,128
          jne L_434021
L_43406a:
          add ESP,4
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_434072:
          mov EBP,DWORD PTR [ESP]
          cmp EDX,EBP
          je L_43406a
          lea EAX,DWORD PTR [EDI-128]
          mov EDI,DWORD PTR [ESP+24]
          mov BYTE PTR [EDI+15],AL
          add ESP,4
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
FUN_434090:
          push EBP
          push EDI
          push ESI
          push EBX
          mov EBX,DWORD PTR [ESP+24]
          test EBX,EBX
          jle L_434105
          mov ECX,DWORD PTR [ESP+20]
          xor EAX,EAX
          lea EBP,DWORD PTR [EBX+ECX*1]
L_4340a5:
          movzx EDX,BYTE PTR [ECX]
          add ECX,1
          mov EDI,EDX
          mov EBX,EDX
          and EDI,1
          shr BL,1
          add EAX,EDI
          mov EDI,EBX
          mov EBX,EDX
          and EDI,1
          shr BL,4
          add EDI,EAX
          mov EAX,EDX
          shr AL,2
          and EAX,1
          add EDI,EAX
          mov EAX,EDX
          shr AL,3
          mov ESI,EAX
          and ESI,1
          lea EAX,DWORD PTR [ESI+EDI*1]
          mov ESI,EBX
          and ESI,1
          add ESI,EAX
          mov EAX,EDX
          shr AL,5
          and EAX,1
          add ESI,EAX
          mov EAX,EDX
          shr DL,7
          shr AL,6
          movzx EDX,DL
          and EAX,1
          add EAX,ESI
          add EAX,EDX
          cmp EBP,ECX
          jne L_4340a5
L_434100:
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_434105:
          xor EAX,EAX
          jmp L_434100
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_434110:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,348
          mov EBX,DWORD PTR [ESP+376]
          mov EDI,DWORD PTR [ESP+388]
          mov EBP,DWORD PTR [ESP+380]
          mov ECX,DWORD PTR [ESP+396]
          mov EAX,DWORD PTR [ESP+372]
          mov ESI,DWORD PTR [ESP+368]
          mov DWORD PTR [ESP+52],EBX
          mov EBX,DWORD PTR [ESP+384]
          mov DWORD PTR [ESP+28],EDI
          add EDI,EBP
          mov DWORD PTR [ESP+32],ECX
          mov DWORD PTR [ESP+48],EDI
          lea EDI,DWORD PTR [EDI+ECX*1+64]
          mov DWORD PTR [ESP+24],EAX
          mov DWORD PTR [ESP+56],EBX
          mov EBX,DWORD PTR [ESP+392]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+40],EDI
          mov DWORD PTR [ESP+60],EBX
          mov EBX,DWORD PTR [ESP+400]
          mov DWORD PTR [ESP+44],EBX
          mov EBX,DWORD PTR [ESP+404]
          mov DWORD PTR [ESP+36],EBX
          call FUN_449108
          mov EBX,EAX
          xor EAX,EAX
          cmp DWORD PTR [ESP+24],64
          lea EDX,DWORD PTR [ESP+92]
          mov ECX,16
          mov EDI,EDX
          rep stosd DWORD PTR ES:[EDI]
          jbe L_434500
          mov EAX,DWORD PTR [ESI]
          mov DWORD PTR [ESP+92],EAX
          mov EAX,DWORD PTR [ESI+4]
          mov DWORD PTR [ESP+96],EAX
          mov EAX,DWORD PTR [ESI+8]
          mov DWORD PTR [ESP+100],EAX
          mov EAX,DWORD PTR [ESI+12]
          mov DWORD PTR [ESP+104],EAX
          mov EAX,DWORD PTR [ESI+16]
          mov DWORD PTR [ESP+108],EAX
          mov EAX,DWORD PTR [ESI+20]
          mov DWORD PTR [ESP+112],EAX
          mov EAX,DWORD PTR [ESI+24]
          mov DWORD PTR [ESP+116],EAX
          mov EAX,DWORD PTR [ESI+28]
          mov DWORD PTR [ESP+120],EAX
          mov EAX,DWORD PTR [ESI+32]
          mov DWORD PTR [ESP+124],EAX
          mov EAX,DWORD PTR [ESI+36]
          mov DWORD PTR [ESP+128],EAX
          mov EAX,DWORD PTR [ESI+40]
          mov DWORD PTR [ESP+132],EAX
          mov EAX,DWORD PTR [ESI+44]
          mov DWORD PTR [ESP+136],EAX
          mov EAX,DWORD PTR [ESI+48]
          mov DWORD PTR [ESP+140],EAX
          mov EAX,DWORD PTR [ESI+52]
          mov DWORD PTR [ESP+144],EAX
          mov EAX,DWORD PTR [ESI+56]
          mov DWORD PTR [ESP+148],EAX
          mov EAX,DWORD PTR [ESI+60]
          mov DWORD PTR [ESP+152],EAX
L_434236:
          mov EAX,DWORD PTR [ESP+92]
          mov EDX,EAX
          xor EAX,909522486
          mov DWORD PTR [EBX],EAX
          mov EAX,DWORD PTR [ESP+96]
          xor EDX,1549556828
          mov DWORD PTR [ESP+156],EDX
          mov EDX,EAX
          xor EAX,909522486
          mov DWORD PTR [EBX+4],EAX
          mov EAX,DWORD PTR [ESP+100]
          xor EDX,1549556828
          mov DWORD PTR [ESP+160],EDX
          mov EDX,EAX
          xor EAX,909522486
          mov DWORD PTR [EBX+8],EAX
          mov EAX,DWORD PTR [ESP+104]
          xor EDX,1549556828
          mov DWORD PTR [ESP+164],EDX
          mov EDX,EAX
          xor EAX,909522486
          mov DWORD PTR [EBX+12],EAX
          mov EAX,DWORD PTR [ESP+108]
          xor EDX,1549556828
          mov DWORD PTR [ESP+168],EDX
          mov EDX,EAX
          xor EAX,909522486
          mov DWORD PTR [EBX+16],EAX
          mov EAX,DWORD PTR [ESP+112]
          xor EDX,1549556828
          mov DWORD PTR [ESP+172],EDX
          mov EDX,EAX
          xor EAX,909522486
          mov DWORD PTR [EBX+20],EAX
          mov EAX,DWORD PTR [ESP+116]
          xor EDX,1549556828
          mov DWORD PTR [ESP+176],EDX
          mov EDX,EAX
          xor EAX,909522486
          mov DWORD PTR [EBX+24],EAX
          mov EAX,DWORD PTR [ESP+120]
          xor EDX,1549556828
          mov DWORD PTR [ESP+180],EDX
          mov EDX,EAX
          xor EAX,909522486
          mov DWORD PTR [EBX+28],EAX
          mov EAX,DWORD PTR [ESP+124]
          xor EDX,1549556828
          mov DWORD PTR [ESP+184],EDX
          mov EDX,EAX
          xor EAX,909522486
          mov DWORD PTR [EBX+32],EAX
          mov EAX,DWORD PTR [ESP+128]
          xor EDX,1549556828
          mov DWORD PTR [ESP+188],EDX
          mov EDX,EAX
          xor EAX,909522486
          mov DWORD PTR [EBX+36],EAX
          mov EAX,DWORD PTR [ESP+132]
          xor EDX,1549556828
          mov DWORD PTR [ESP+192],EDX
          mov EDX,EAX
          xor EAX,909522486
          xor EDX,1549556828
          mov DWORD PTR [ESP+196],EDX
          mov DWORD PTR [EBX+40],EAX
          mov EAX,DWORD PTR [ESP+136]
          mov EDX,EAX
          xor EAX,909522486
          mov DWORD PTR [EBX+44],EAX
          mov EAX,DWORD PTR [ESP+140]
          xor EDX,1549556828
          mov DWORD PTR [ESP+200],EDX
          mov EDX,EAX
          xor EAX,909522486
          mov DWORD PTR [EBX+48],EAX
          mov EAX,DWORD PTR [ESP+144]
          xor EDX,1549556828
          mov DWORD PTR [ESP+204],EDX
          mov EDX,EAX
          xor EAX,909522486
          mov DWORD PTR [EBX+52],EAX
          mov EAX,DWORD PTR [ESP+148]
          xor EDX,1549556828
          mov DWORD PTR [ESP+208],EDX
          mov EDX,EAX
          xor EAX,909522486
          mov DWORD PTR [EBX+56],EAX
          mov EAX,DWORD PTR [ESP+152]
          xor EDX,1549556828
          mov DWORD PTR [ESP+212],EDX
          mov EDX,EAX
          xor EAX,909522486
          xor EDX,1549556828
          test EBP,EBP
          mov DWORD PTR [EBX+60],EAX
          mov DWORD PTR [ESP+216],EDX
          jne L_434570
L_434402:
          mov EDX,DWORD PTR [ESP+28]
          test EDX,EDX
          jne L_434545
L_43440e:
          mov EAX,DWORD PTR [ESP+32]
          test EAX,EAX
          jne L_434520
L_43441a:
          lea ESI,DWORD PTR [ESP+240]
          lea EBP,DWORD PTR [ESP+72]
          mov DWORD PTR [ESP],ESI
          call FUN_442b00
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],EAX
          call FUN_4448d0
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EBP
          call FUN_444da0
          mov EAX,DWORD PTR [ESP+72]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+220],EAX
          mov EAX,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP+224],EAX
          mov EAX,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP+228],EAX
          mov EAX,DWORD PTR [ESP+84]
          mov DWORD PTR [ESP+232],EAX
          mov EAX,DWORD PTR [ESP+88]
          mov DWORD PTR [ESP+236],EAX
          call FUN_442b00
          lea EAX,DWORD PTR [ESP+156]
          mov DWORD PTR [ESP+8],84
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],EAX
          call FUN_4448d0
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EBP
          call FUN_444da0
          cmp DWORD PTR [ESP+36],20
          jbe L_434590
          mov ECX,DWORD PTR [ESP+44]
          mov EAX,DWORD PTR [ESP+72]
          mov DWORD PTR [ECX],EAX
          mov EAX,DWORD PTR [ESP+76]
          mov DWORD PTR [ECX+4],EAX
          mov EAX,DWORD PTR [ESP+80]
          mov DWORD PTR [ECX+8],EAX
          mov EAX,DWORD PTR [ESP+84]
          mov DWORD PTR [ECX+12],EAX
          mov EAX,DWORD PTR [ESP+88]
          mov DWORD PTR [ECX+16],EAX
L_4344e4:
          mov DWORD PTR [ESP+368],EBX
          add ESP,348
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          jmp FUN_449140
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_434500:
          mov EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EDX
          mov DWORD PTR [ESP+8],EAX
          call FUN_4490f8
          jmp L_434236
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_434520:
          mov ESI,DWORD PTR [ESP+32]
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+8],ESI
          mov ESI,DWORD PTR [ESP+60]
          lea EAX,DWORD PTR [EBX+EAX*1+64]
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],ESI
          call FUN_4490f8
          jmp L_43441a
L_434545:
          mov ESI,DWORD PTR [ESP+28]
          lea EAX,DWORD PTR [EBX+EBP*1+64]
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+8],ESI
          mov ESI,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP+4],ESI
          call FUN_4490f8
          jmp L_43440e
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_434570:
          mov ESI,DWORD PTR [ESP+52]
          lea EAX,DWORD PTR [EBX+64]
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],ESI
          call FUN_4490f8
          jmp L_434402
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_434590:
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EAX
          call FUN_4490f8
          jmp L_4344e4
          .byte 0x8d
          .byte 0x76
          .byte 0x0
FUN_4345b0:
          push ESI
          push EBX
          sub ESP,1060
          mov EAX,DWORD PTR [ESP+1072]
          lea EBX,DWORD PTR [ESP+24]
          mov ESI,DWORD PTR [ESP+1080]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+1076]
          mov DWORD PTR [ESP+4],EAX
          call FUN_4429d0
          mov EAX,DWORD PTR [ESP+1084]
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call FUN_442630
          add ESP,1060
          pop EBX
          pop ESI
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
          .byte 0x8d
          .byte 0xbc
          .byte 0x27
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_434610:
          mov EAX,DWORD PTR [ESP+12]
          mov EDX,DWORD PTR [ESP+8]
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+12],EDX
          jmp FUN_4429d0
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
          .byte 0x8d
          .byte 0xbc
          .byte 0x27
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_434630:
          sub ESP,28
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EAX
          call FUN_442630
          add ESP,28
          ret 
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_434660:
          push EDI
          push ESI
          push EBX
          sub ESP,32
          lea EDI,DWORD PTR [ESP+16]
          mov DWORD PTR [ESP],0
          lea ESI,DWORD PTR [ESP+32]
          call FUN_449050
          mov EBX,EDI
          mov DWORD PTR [ESP],EAX
          call FUN_449090
L_434684:
          call FUN_4490c0
          add EBX,1
          mov BYTE PTR [EBX-1],AL
          cmp EBX,ESI
          jne L_434684
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_50e880
          call FUN_4429d0
          mov DWORD PTR [L_479ac0],1
          add ESP,32
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
FUN_4346c0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,60
          mov EAX,DWORD PTR [ESP+84]
          mov ESI,DWORD PTR [ESP+84]
          mov EDI,DWORD PTR [ESP+80]
          and EAX,4294967280
          and ESI,15
          mov DWORD PTR [ESP+28],EAX
          mov EAX,DWORD PTR [L_479ac0]
          test EAX,EAX
          je L_4347c0
L_4346ea:
          mov EAX,DWORD PTR [ESP+84]
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+8],EAX
          call FUN_4490f0
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP],OFFSET L_50e880
          mov DWORD PTR [ESP+4],EAX
          call FUN_442630
          test ESI,ESI
          jne L_434730
L_434722:
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
L_434730:
          lea EBX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_50e880
          mov DWORD PTR [ESP+32],0
          mov DWORD PTR [ESP+36],0
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+40],0
          mov DWORD PTR [ESP+44],0
          call FUN_442630
          add EDI,DWORD PTR [ESP+28]
          cmp ESI,4
          jb L_434820
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [EDI],EAX
          mov EAX,DWORD PTR [ESP+ESI*1+28]
          mov DWORD PTR [EDI+ESI*1-4],EAX
          lea EAX,DWORD PTR [EDI+4]
          and EAX,4294967292
          sub EDI,EAX
          add ESI,EDI
          sub EBX,EDI
          and ESI,4294967292
          cmp ESI,4
          jb L_434722
          and ESI,4294967292
          xor EDX,EDX
L_4347a4:
          mov ECX,DWORD PTR [EBX+EDX*1]
          mov DWORD PTR [EAX+EDX*1],ECX
          add EDX,4
          cmp EDX,ESI
          jb L_4347a4
          jmp L_434722
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_4347c0:
          mov DWORD PTR [ESP],0
          lea EBP,DWORD PTR [ESP+32]
          lea EBX,DWORD PTR [ESP+48]
          call FUN_449050
          mov DWORD PTR [ESP],EAX
          call FUN_449090
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_4347e0:
          call FUN_4490c0
          add EBP,1
          mov BYTE PTR [EBP-1],AL
          cmp EBP,EBX
          jne L_4347e0
          lea EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_50e880
          mov DWORD PTR [ESP+8],EAX
          call FUN_4429d0
          mov DWORD PTR [L_479ac0],1
          jmp L_4346ea
          .byte 0x8d,0xb6,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_434820:
          test ESI,ESI
          je L_434722
          movzx EAX,BYTE PTR [EBX]
          test ESI,2
          mov BYTE PTR [EDI],AL
          je L_434722
          movzx EAX,WORD PTR [EBX+ESI*1-2]
          mov WORD PTR [EDI+ESI*1-2],AX
          jmp L_434722
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_434850:
          push ESI
          push EBX
          sub ESP,20
          mov ESI,DWORD PTR [ESP+36]
          mov EBX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP],ESI
          add EBX,244
          call FUN_43c6f0
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],16
          call FUN_43e4e0
          add ESP,20
          pop EBX
          pop ESI
          ret 
L_434891:
          jmp FUN_4348a0
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
FUN_4348a0:
          cmp DWORD PTR [ESP+16],0
          mov EAX,DWORD PTR [ESP+4]
          mov EDX,DWORD PTR [ESP+8]
          mov ECX,DWORD PTR [ESP+12]
          jne L_4348d1
          add EAX,244
          mov DWORD PTR [ESP+12],16
          mov DWORD PTR [ESP+8],ECX
          mov DWORD PTR [ESP+16],EAX
          mov DWORD PTR [ESP+4],EDX
          jmp L_438c30
L_4348d1:
          mov DWORD PTR [ESP+16],EAX
          mov DWORD PTR [ESP+12],16
          mov DWORD PTR [ESP+8],ECX
          mov DWORD PTR [ESP+4],EDX
          jmp L_438bc0
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_4348f0:
          push ESI
          push EBX
          cmp DWORD PTR [ESP+32],0
          mov EAX,DWORD PTR [ESP+12]
          mov EDX,DWORD PTR [ESP+16]
          mov EBX,DWORD PTR [ESP+20]
          mov ECX,DWORD PTR [ESP+24]
          mov ESI,DWORD PTR [ESP+28]
          jne L_434930
          add EAX,244
          mov DWORD PTR [ESP+24],ESI
          mov DWORD PTR [ESP+20],EBX
          mov DWORD PTR [ESP+28],EAX
          mov DWORD PTR [ESP+16],ECX
          mov DWORD PTR [ESP+12],EDX
          pop EBX
          pop ESI
          jmp L_438e20
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_434930:
          mov DWORD PTR [ESP+28],EAX
          mov DWORD PTR [ESP+24],ESI
          mov DWORD PTR [ESP+16],ECX
          mov DWORD PTR [ESP+12],EDX
          pop EBX
          pop ESI
          jmp L_438ca0
L_434947:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_434950:
          jmp FUN_442b00
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
          .byte 0x8d
          .byte 0xbc
          .byte 0x27
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_434960:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,28
          mov EBX,DWORD PTR [ESP+56]
          mov EDI,DWORD PTR [ESP+48]
          mov EBP,DWORD PTR [ESP+52]
          test EBX,EBX
          jne L_434980
          add ESP,28
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x90
L_434980:
          mov DWORD PTR [ESP],EBX
          call FUN_449108
          mov DWORD PTR [ESP+8],EBX
          mov ESI,EAX
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EAX
          call FUN_4490f8
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EDI
          call FUN_4448d0
          mov DWORD PTR [ESP+48],ESI
          add ESP,28
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          jmp FUN_449140
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_4349c0:
          push ESI
          push EBX
          sub ESP,52
          mov EAX,DWORD PTR [ESP+64]
          lea ESI,DWORD PTR [ESP+28]
          mov EBX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],EAX
          call FUN_444da0
          cmp DWORD PTR [ESP+72],20
          jbe L_434a10
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [EBX],EAX
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [EBX+4],EAX
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [EBX+8],EAX
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [EBX+12],EAX
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [EBX+16],EAX
          add ESP,52
          pop EBX
          pop ESI
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_434a10:
          mov EAX,DWORD PTR [ESP+72]
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],EAX
          call FUN_4490f8
          add ESP,52
          pop EBX
          pop ESI
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_434a30:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,156
          lea ESI,DWORD PTR [ESP+48]
          mov EDI,DWORD PTR [ESP+196]
          mov EBX,DWORD PTR [ESP+200]
          mov DWORD PTR [ESP],ESI
          call FUN_442b00
          mov EDX,DWORD PTR [ESP+180]
          test EDX,EDX
          jne L_434b53
L_434a63:
          mov EAX,DWORD PTR [ESP+188]
          test EAX,EAX
          jne L_434b00
L_434a72:
          test EDI,EDI
          je L_434aaf
          mov DWORD PTR [ESP],EDI
          call FUN_449108
          mov EBP,EAX
          mov EAX,DWORD PTR [ESP+192]
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+4],EAX
          call FUN_4490f8
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],ESI
          call FUN_4448d0
          mov DWORD PTR [ESP],EBP
          call FUN_449140
L_434aaf:
          mov DWORD PTR [ESP+4],ESI
          lea ESI,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],ESI
          call FUN_444da0
          cmp DWORD PTR [ESP+204],20
          jbe L_434bb0
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [EBX],EAX
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [EBX+4],EAX
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [EBX+8],EAX
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [EBX+12],EAX
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [EBX+16],EAX
          add ESP,156
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
L_434b00:
          mov EAX,DWORD PTR [ESP+188]
          mov DWORD PTR [ESP],EAX
          call FUN_449108
          mov EBP,EAX
          mov EAX,DWORD PTR [ESP+188]
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+184]
          mov DWORD PTR [ESP+4],EAX
          call FUN_4490f8
          mov EAX,DWORD PTR [ESP+188]
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],EAX
          call FUN_4448d0
          mov DWORD PTR [ESP],EBP
          call FUN_449140
          jmp L_434a72
L_434b53:
          mov EAX,DWORD PTR [ESP+180]
          mov DWORD PTR [ESP],EAX
          call FUN_449108
          mov EBP,EAX
          mov EAX,DWORD PTR [ESP+180]
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+176]
          mov DWORD PTR [ESP+4],EAX
          call FUN_4490f8
          mov EAX,DWORD PTR [ESP+180]
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],EAX
          call FUN_4448d0
          mov DWORD PTR [ESP],EBP
          call FUN_449140
          jmp L_434a63
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_434bb0:
          mov EAX,DWORD PTR [ESP+204]
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],EAX
          call FUN_4490f8
          add ESP,156
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
          .byte 0x8d
          .byte 0xbc
          .byte 0x27
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_434be0:
          mov ECX,DWORD PTR [ESP+12]
          mov EAX,DWORD PTR [ESP+4]
          mov EDX,DWORD PTR [ESP+8]
          test ECX,ECX
          jne L_434bf2
          repz ret 
L_434bf2:
          jmp FUN_433840
L_434bf7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_434c00:
          push EBP
          push EDI
          xor EAX,EAX
          push ESI
          push EBX
          sub ESP,188
          mov EBX,DWORD PTR [ESP+220]
          mov EDI,DWORD PTR [ESP+224]
L_434c1a:
          mov DWORD PTR [ESP+EAX*1+48],0
          add EAX,4
          cmp EAX,32
          jb L_434c1a
          mov ECX,DWORD PTR [ESP+212]
          shr ECX,3
          test ECX,ECX
          je L_434c48
          mov EDX,DWORD PTR [ESP+208]
          lea EAX,DWORD PTR [ESP+48]
          call FUN_433840
L_434c48:
          mov ECX,EBX
          shr ECX,3
          test ECX,ECX
          jne L_434e70
L_434c55:
          lea ESI,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP],ESI
          call FUN_442b00
          mov DWORD PTR [ESP],32
          call FUN_449108
          mov EDX,DWORD PTR [ESP+48]
          mov EBP,EAX
          mov DWORD PTR [EAX],EDX
          mov EDX,DWORD PTR [ESP+52]
          mov DWORD PTR [EAX+4],EDX
          mov EDX,DWORD PTR [ESP+56]
          mov DWORD PTR [EAX+8],EDX
          mov EDX,DWORD PTR [ESP+60]
          mov DWORD PTR [EAX+12],EDX
          mov EDX,DWORD PTR [ESP+64]
          mov DWORD PTR [EAX+16],EDX
          mov EDX,DWORD PTR [ESP+68]
          mov DWORD PTR [EAX+20],EDX
          mov EDX,DWORD PTR [ESP+72]
          mov DWORD PTR [EAX+24],EDX
          mov EDX,DWORD PTR [ESP+76]
          mov DWORD PTR [EAX+28],EDX
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP+8],32
          mov DWORD PTR [ESP],ESI
          call FUN_4448d0
          mov DWORD PTR [ESP],EBP
          call FUN_449140
          mov DWORD PTR [ESP],32
          call FUN_449108
          mov EDX,DWORD PTR [ESP+48]
          mov EBP,EAX
          mov DWORD PTR [EAX],EDX
          mov EDX,DWORD PTR [ESP+52]
          mov DWORD PTR [EAX+4],EDX
          mov EDX,DWORD PTR [ESP+56]
          mov DWORD PTR [EAX+8],EDX
          mov EDX,DWORD PTR [ESP+60]
          mov DWORD PTR [EAX+12],EDX
          mov EDX,DWORD PTR [ESP+64]
          mov DWORD PTR [EAX+16],EDX
          mov EDX,DWORD PTR [ESP+68]
          mov DWORD PTR [EAX+20],EDX
          mov EDX,DWORD PTR [ESP+72]
          mov DWORD PTR [EAX+24],EDX
          mov EDX,DWORD PTR [ESP+76]
          mov DWORD PTR [EAX+28],EDX
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP+8],32
          mov DWORD PTR [ESP],ESI
          call FUN_4448d0
          mov DWORD PTR [ESP],EBP
          call FUN_449140
          mov EAX,DWORD PTR [ESP+212]
          test EAX,EAX
          jne L_434ec3
L_434d32:
          test EBX,EBX
          jne L_434e85
L_434d3a:
          mov DWORD PTR [ESP],32
          not DWORD PTR [ESP+48]
          not DWORD PTR [ESP+52]
          not DWORD PTR [ESP+56]
          not DWORD PTR [ESP+60]
          not DWORD PTR [ESP+64]
          not DWORD PTR [ESP+68]
          not DWORD PTR [ESP+72]
          not DWORD PTR [ESP+76]
          call FUN_449108
          mov EBX,EAX
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [EBX],EAX
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [EBX+4],EAX
          mov EAX,DWORD PTR [ESP+56]
          mov DWORD PTR [EBX+8],EAX
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [EBX+12],EAX
          mov EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [EBX+16],EAX
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [EBX+20],EAX
          mov EAX,DWORD PTR [ESP+72]
          mov DWORD PTR [EBX+24],EAX
          mov EAX,DWORD PTR [ESP+76]
          mov DWORD PTR [EBX+28],EAX
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP+8],32
          mov DWORD PTR [ESP],ESI
          call FUN_4448d0
          mov DWORD PTR [ESP],EBX
          call FUN_449140
          mov DWORD PTR [ESP],32
          call FUN_449108
          mov EBX,EAX
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [EBX],EAX
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [EBX+4],EAX
          mov EAX,DWORD PTR [ESP+56]
          mov DWORD PTR [EBX+8],EAX
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [EBX+12],EAX
          mov EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [EBX+16],EAX
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [EBX+20],EAX
          mov EAX,DWORD PTR [ESP+72]
          mov DWORD PTR [EBX+24],EAX
          mov EAX,DWORD PTR [ESP+76]
          mov DWORD PTR [EBX+28],EAX
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP+8],32
          mov DWORD PTR [ESP],ESI
          call FUN_4448d0
          mov DWORD PTR [ESP],EBX
          lea EBX,DWORD PTR [ESP+28]
          call FUN_449140
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EBX
          call FUN_444da0
          cmp DWORD PTR [ESP+228],20
          jbe L_434f20
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [EDI],EAX
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [EDI+4],EAX
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [EDI+8],EAX
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [EDI+12],EAX
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [EDI+16],EAX
          add ESP,188
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_434e67:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_434e70:
          mov EDX,DWORD PTR [ESP+216]
          lea EAX,DWORD PTR [ESP+48]
          call FUN_433840
          jmp L_434c55
L_434e85:
          mov DWORD PTR [ESP],EBX
          call FUN_449108
          mov EBP,EAX
          mov EAX,DWORD PTR [ESP+216]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+4],EAX
          call FUN_4490f8
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],ESI
          call FUN_4448d0
          mov DWORD PTR [ESP],EBP
          call FUN_449140
          jmp L_434d3a
L_434ec3:
          mov EAX,DWORD PTR [ESP+212]
          mov DWORD PTR [ESP],EAX
          call FUN_449108
          mov EBP,EAX
          mov EAX,DWORD PTR [ESP+212]
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+208]
          mov DWORD PTR [ESP+4],EAX
          call FUN_4490f8
          mov EAX,DWORD PTR [ESP+212]
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],EAX
          call FUN_4448d0
          mov DWORD PTR [ESP],EBP
          call FUN_449140
          jmp L_434d32
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_434f20:
          mov EAX,DWORD PTR [ESP+228]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+8],EAX
          call FUN_4490f8
          add ESP,188
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
          .byte 0x8d
          .byte 0xbc
          .byte 0x27
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_434f50:
          push ESI
          push EBX
          sub ESP,36
          mov ESI,DWORD PTR [ESP+60]
          mov EBX,DWORD PTR [ESP+56]
          lea EAX,DWORD PTR [ESI-39]
          cmp EAX,473
          jbe L_434f70
L_434f67:
          add ESP,36
          pop EBX
          pop ESI
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_434f70:
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],255
          mov DWORD PTR [ESP],EBX
          call FUN_4490f0
          mov EAX,DWORD PTR [ESP+48]
          mov BYTE PTR [EBX+ESI*1-1],0
          mov BYTE PTR [EBX+ESI*1-2],1
          mov DWORD PTR [ESP+8],20
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call FUN_436e20
          mov EAX,DWORD PTR [ESP+52]
          test EAX,EAX
          je L_434fc0
          cmp DWORD PTR [ESP+52],1
          je L_434fe2
          mov BYTE PTR [EBX+20],0
          add ESP,36
          pop EBX
          pop ESI
          ret 
          .byte 0x90
L_434fc0:
          mov DWORD PTR [EBX+20],83887124
          mov DWORD PTR [EBX+24],235078170
          mov DWORD PTR [EBX+28],151389483
          mov DWORD PTR [EBX+32],3154224
          add ESP,36
          pop EBX
          pop ESI
          ret 
L_434fe2:
          mov BYTE PTR [EBX+20],20
          mov BYTE PTR [EBX+21],4
          mov BYTE PTR [EBX+22],26
          mov BYTE PTR [EBX+23],2
          mov BYTE PTR [EBX+24],3
          mov BYTE PTR [EBX+25],14
          mov BYTE PTR [EBX+26],43
          mov BYTE PTR [EBX+27],5
          mov BYTE PTR [EBX+28],6
          mov BYTE PTR [EBX+29],7
          mov BYTE PTR [EBX+30],48
          mov BYTE PTR [EBX+31],31
          mov BYTE PTR [EBX+32],48
          mov BYTE PTR [EBX+33],0
          jmp L_434f67
          .byte 0x90
FUN_435020:
          push EBP
          push EDI
          xor EAX,EAX
          push ESI
          push EBX
          sub ESP,1180
          mov EBX,DWORD PTR [ESP+1200]
          mov ESI,DWORD PTR [ESP+1208]
          mov EBP,DWORD PTR [ESP+1204]
          lea EDI,DWORD PTR [EBX+4]
          mov ECX,EBX
          mov DWORD PTR [EBX],0
          mov DWORD PTR [EBX+220],0
          and EDI,4294967292
          sub ECX,EDI
          add ECX,224
          shr ECX,2
          rep stosd DWORD PTR ES:[EDI]
          lea EDI,DWORD PTR [ESP+40]
          mov EDX,DWORD PTR [ESI]
          mov DWORD PTR [EBX+225],EDX
          mov EDX,DWORD PTR [ESI+4]
          mov DWORD PTR [EBX+229],EDX
          movzx EDX,WORD PTR [ESI+8]
          mov BYTE PTR [EBX+255],188
          mov BYTE PTR [EBX+224],1
          mov WORD PTR [EBX+233],DX
          mov DWORD PTR [ESP],EDI
          call FUN_442b00
          mov DWORD PTR [ESP],8
          call FUN_449108
          mov ECX,DWORD PTR [EBX+4]
          mov EDX,DWORD PTR [EBX]
          mov DWORD PTR [ESP+28],EAX
          mov DWORD PTR [EAX+4],ECX
          mov DWORD PTR [EAX],EDX
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+8],8
          call FUN_4448d0
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EAX
          call FUN_449140
          mov DWORD PTR [ESP],20
          call FUN_449108
          mov EDX,DWORD PTR [EBP]
          mov DWORD PTR [ESP+28],EAX
          mov DWORD PTR [EAX],EDX
          mov EDX,DWORD PTR [EBP+4]
          mov DWORD PTR [EAX+4],EDX
          mov EDX,DWORD PTR [EBP+8]
          mov DWORD PTR [EAX+8],EDX
          mov EDX,DWORD PTR [EBP+12]
          mov DWORD PTR [EAX+12],EDX
          mov EDX,DWORD PTR [EBP+16]
          mov DWORD PTR [EAX+16],EDX
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+8],20
          call FUN_4448d0
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EAX
          call FUN_449140
          mov DWORD PTR [ESP],10
          call FUN_449108
          mov EBP,EAX
          mov EAX,DWORD PTR [ESI]
          mov DWORD PTR [EBP],EAX
          mov EAX,DWORD PTR [ESI+4]
          mov DWORD PTR [EBP+4],EAX
          movzx EAX,WORD PTR [ESI+8]
          lea ESI,DWORD PTR [ESP+136]
          mov WORD PTR [EBP+8],AX
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+8],10
          call FUN_4448d0
          mov DWORD PTR [ESP],EBP
          call FUN_449140
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],ESI
          call FUN_444da0
          mov EAX,DWORD PTR [ESP+136]
          mov DWORD PTR [EBX+235],EAX
          mov EAX,DWORD PTR [ESP+140]
          mov DWORD PTR [EBX+239],EAX
          mov EAX,DWORD PTR [ESP+144]
          mov DWORD PTR [EBX+243],EAX
          mov EAX,DWORD PTR [ESP+148]
          mov DWORD PTR [EBX+247],EAX
          mov EAX,DWORD PTR [ESP+152]
          mov DWORD PTR [EBX+251],EAX
          lea EAX,DWORD PTR [EBX+235]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],20
          mov DWORD PTR [ESP+8],EAX
          call FUN_4429d0
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],235
          call FUN_442630
          and BYTE PTR [EBX],127
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],32
          call FUN_436e50
          add ESP,1180
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
          .byte 0x8d
          .byte 0xbf
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_435210:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,92
          mov ESI,DWORD PTR [ESP+116]
          mov EAX,DWORD PTR [ESP+112]
          mov EBX,DWORD PTR [ESP+128]
          mov DWORD PTR [ESP+64],ESI
          mov ESI,DWORD PTR [ESP+120]
          mov DWORD PTR [ESP+60],EAX
          mov EAX,DWORD PTR [ESP+132]
          mov DWORD PTR [ESP+56],EBX
          mov DWORD PTR [ESP+68],ESI
          mov ESI,DWORD PTR [ESP+124]
          mov DWORD PTR [ESP+52],EAX
          mov EAX,DWORD PTR [ESI+4]
          mov ECX,EAX
          mov EDX,EAX
          shl ECX,24
          shr EDX,24
          add EDX,ECX
          mov ECX,EAX
          shr EAX,8
          shl ECX,8
          and EAX,65280
          mov EBX,ECX
          mov ECX,DWORD PTR [ESI+16]
          and EBX,16711680
          add EDX,EBX
          add EAX,EDX
          mov EBX,ECX
          mov ECX,0
          mov DWORD PTR [ESP+40],EAX
          mov EAX,DWORD PTR [ESI]
          shl EBX,24
          mov EBP,EAX
          mov EDX,EAX
          shl EBP,24
          shr EDX,24
          add EDX,EBP
          mov EBP,EAX
          shr EAX,8
          shl EBP,8
          and EAX,65280
          and EBP,16711680
          add EDX,EBP
          lea EBP,DWORD PTR [EDX+EAX*1]
          mov EDX,DWORD PTR [ESI+20]
          mov EAX,EDX
          xor EDX,EDX
          shr EAX,24
          add ECX,EAX
          mov EAX,DWORD PTR [ESI+16]
          adc EBX,EDX
          mov EDX,DWORD PTR [ESI+20]
          shl EAX,8
          mov EDI,EAX
          xor EAX,EAX
          and EDI,16711680
          add ECX,EAX
          mov EAX,DWORD PTR [ESI+16]
          adc EBX,EDI
          shld EDX,EAX,24
          xor EAX,EAX
          mov DWORD PTR [ESP+76],EDX
          mov EDI,DWORD PTR [ESP+76]
          mov EDX,DWORD PTR [ESI+20]
          and EDI,65280
          add ECX,EAX
          mov EAX,DWORD PTR [ESI+16]
          adc EBX,EDI
          shld EDX,EAX,8
          xor EAX,EAX
          mov DWORD PTR [ESP+76],EDX
          movzx EDX,BYTE PTR [ESP+76]
          add ECX,EAX
          mov EAX,DWORD PTR [ESI+16]
          adc EBX,EDX
          mov EDX,DWORD PTR [ESI+20]
          shrd EAX,EDX,8
          xor EDX,EDX
          mov DWORD PTR [ESP+72],EAX
          mov EDI,DWORD PTR [ESP+72]
          mov EAX,DWORD PTR [ESI+16]
          and EDI,4278190080
          add ECX,EDI
          adc EBX,EDX
          mov EDX,DWORD PTR [ESI+20]
          shrd EAX,EDX,24
          shr EDX,24
          mov DWORD PTR [ESP+72],EAX
          mov EDI,DWORD PTR [ESP+72]
          mov EAX,DWORD PTR [ESI+20]
          mov DWORD PTR [ESP+76],EDX
          xor EDX,EDX
          and EDI,16711680
          add ECX,EDI
          adc EBX,EDX
          shr EAX,8
          xor EDX,EDX
          mov EDI,EAX
          and EDI,65280
          mov EAX,EDI
          add EAX,ECX
          adc EDX,EBX
          mov DWORD PTR [ESP],EAX
          add ESI,16
          mov DWORD PTR [ESP+4],EDX
          call FUN_437120
          mov EBX,DWORD PTR [ESP+56]
          mov ECX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+76],EDX
          mov DWORD PTR [ESP+72],EAX
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],ECX
          call FUN_436d80
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],EAX
          call FUN_436d80
          mov EBX,DWORD PTR [ESP+40]
          mov EAX,DWORD PTR [ESP+72]
          mov EDX,DWORD PTR [ESP+76]
          shr EBX,1
          je L_4353f8
          mov EDI,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+40],EAX
          mov DWORD PTR [ESP+44],EDX
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_4353c0:
          mov EAX,DWORD PTR [ESP+40]
          mov EDX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+24],EBP
          mov DWORD PTR [ESP+20],ESI
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+16],EDX
          mov DWORD PTR [ESP],EDI
          call FUN_4372a0
          shr EBX,1
          jne L_4353c0
          mov EAX,DWORD PTR [ESP+40]
          mov EDX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+52],EDI
L_4353f8:
          mov EBX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP+24],EBP
          mov DWORD PTR [ESP+20],ESI
          mov DWORD PTR [ESP+16],EDX
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],EAX
          call FUN_4372a0
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+112],EBX
          mov DWORD PTR [ESP+120],EAX
          mov EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+116],EAX
          add ESP,92
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          jmp FUN_435020
FUN_435440:
          push EDI
          push ESI
          push EBX
          sub ESP,544
          mov EBX,DWORD PTR [ESP+572]
          mov EAX,DWORD PTR [EBX]
          mov EDX,EAX
          mov ECX,EAX
          shl EDX,24
          shr ECX,24
          add ECX,EDX
          mov EDX,EAX
          shr EAX,8
          shl EDX,8
          and EAX,65280
          and EDX,16711680
          add EDX,ECX
          add EDX,EAX
          xor EAX,EAX
          cmp EDX,32
          je L_435490
L_43547c:
          add ESP,544
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_435490:
          mov EDX,DWORD PTR [EBX+4]
          mov ECX,EDX
          mov ESI,EDX
          shl ECX,24
          shr ESI,24
          add ESI,ECX
          mov ECX,EDX
          shr EDX,8
          shl ECX,8
          and EDX,65280
          and ECX,16711680
          add ECX,ESI
          add EDX,ECX
          cmp EDX,3
          je L_4354c4
          cmp EDX,65537
          jne L_43547c
L_4354c4:
          mov EAX,DWORD PTR [ESP+568]
          lea EDI,DWORD PTR [ESP+288]
          lea ESI,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+20],EDI
          mov DWORD PTR [ESP+16],ESI
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+564]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+560]
          mov DWORD PTR [ESP],EAX
          call FUN_435210
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],256
          call FUN_449100
          test EAX,EAX
          sete AL
          add ESP,544
          pop EBX
          movzx EAX,AL
          pop ESI
          pop EDI
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_435530:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,828
          mov EBX,DWORD PTR [ESP+860]
          mov EAX,DWORD PTR [EBX]
          mov EDX,EAX
          mov ECX,EAX
          shl EDX,24
          shr ECX,24
          add ECX,EDX
          mov EDX,EAX
          shr EAX,8
          shl EDX,8
          and EAX,65280
          and EDX,16711680
          add EDX,ECX
          add EAX,EDX
          cmp EAX,32
          je L_435580
L_43556b:
          xor EAX,EAX
L_43556d:
          add ESP,828
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
L_435580:
          mov EAX,DWORD PTR [EBX+4]
          mov ESI,EAX
          mov EDX,EAX
          shl ESI,24
          shr EDX,24
          add EDX,ESI
          mov ESI,EAX
          shr EAX,8
          shl ESI,8
          and EAX,65280
          and ESI,16711680
          add ESI,EDX
          add ESI,EAX
          cmp ESI,3
          je L_4355b3
          cmp ESI,65537
          jne L_43556b
L_4355b3:
          mov EAX,DWORD PTR [ESP+856]
          add EBX,16
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+852]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+848]
          mov DWORD PTR [ESP],EAX
          call FUN_435020
          mov EAX,DWORD PTR [ESP+848]
          mov DWORD PTR [ESP+8],32
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EAX
          call FUN_438620
          cmp EAX,-1
          jne L_43556b
          lea EAX,DWORD PTR [ESP+304]
          lea EBP,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+4],64
          xor EDI,EDI
          mov DWORD PTR [ESP],EAX
          call FUN_436df0
          mov DWORD PTR [ESP+4],32
          mov DWORD PTR [ESP],EBP
          call FUN_436df0
          add ESI,-1
          mov DWORD PTR [ESP+40],0
          mov DWORD PTR [ESP+304],0
          mov ECX,ESI
          adc EDI,-1
          mov EAX,ESI
          shl ECX,19
          mov EDX,EDI
          shl EAX,11
          and ECX,16776960
          mov DWORD PTR [ESP+32],EAX
          xor EAX,EAX
          mov DWORD PTR [ESP+44],ECX
          lea ECX,DWORD PTR [ESI*8]
          mov DWORD PTR [ESP+308],33554432
          shld EDX,ESI,11
          and ECX,65280
          mov DWORD PTR [ESP+16],32
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+36],EDX
          mov EDX,EAX
          add EDX,DWORD PTR [ESP+40]
          adc ECX,DWORD PTR [ESP+44]
          xor EAX,EAX
          mov DWORD PTR [ESP+8],EBP
          shld EDI,ESI,19
          mov DWORD PTR [ESP],EBP
          and EDI,255
          mov DWORD PTR [ESP+40],EDX
          add EAX,DWORD PTR [ESP+40]
          mov EDX,EDI
          mov EDI,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+44],ECX
          adc EDX,DWORD PTR [ESP+44]
          mov ECX,DWORD PTR [ESP+36]
          mov ESI,EDI
          xor EDI,EDI
          shr ESI,24
          add ESI,EAX
          mov EAX,DWORD PTR [ESP+32]
          adc EDI,EDX
          mov EDX,DWORD PTR [ESP+32]
          shrd EDX,ECX,8
          mov DWORD PTR [ESP+40],EDX
          mov ECX,DWORD PTR [ESP+40]
          xor EDX,EDX
          and ECX,4278190080
          add ESI,ECX
          adc EDI,EDX
          mov EDX,DWORD PTR [ESP+36]
          shrd EAX,EDX,24
          shr EDX,24
          mov DWORD PTR [ESP+40],EAX
          mov ECX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+44],EDX
          xor EDX,EDX
          and ECX,16711680
          mov EAX,ECX
          mov ECX,DWORD PTR [ESP+36]
          add EAX,ESI
          adc EDX,EDI
          xor EDI,EDI
          shr ECX,8
          and ECX,65280
          add EAX,ECX
          mov DWORD PTR [ESP+48],EAX
          lea EAX,DWORD PTR [ESP+304]
          adc EDX,EDI
          mov DWORD PTR [ESP+52],EDX
          mov DWORD PTR [ESP+4],EAX
          call FUN_4380f0
          mov EDX,EAX
          xor EAX,EAX
          test EDX,EDX
          je L_43556d
          mov EAX,DWORD PTR [ESP+848]
          mov DWORD PTR [ESP+12],32
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP+8],EAX
          lea EAX,DWORD PTR [ESP+304]
          mov DWORD PTR [ESP],EAX
          call FUN_4382c0
          mov EAX,DWORD PTR [ESP+848]
          mov DWORD PTR [ESP+16],32
          mov DWORD PTR [ESP+12],64
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP+8],EAX
          lea EAX,DWORD PTR [ESP+304]
          mov DWORD PTR [ESP],EAX
          call FUN_438460
          test EAX,EAX
          setne AL
          movzx EAX,AL
          jmp L_43556d
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_4357b0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,28
          mov EBX,DWORD PTR [ESP+76]
          mov ESI,DWORD PTR [ESP+60]
          mov EAX,DWORD PTR [ESP+48]
          mov EDX,DWORD PTR [ESP+52]
          mov ECX,DWORD PTR [ESP+56]
          mov EDI,DWORD PTR [ESP+68]
          cmp EBX,32
          mov DWORD PTR [ESP+12],ESI
          mov EBP,DWORD PTR [ESP+72]
          mov ESI,DWORD PTR [ESP+64]
          jbe L_4357f0
          add ESP,28
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
L_4357f0:
          mov DWORD PTR [ESP+56],EDI
          mov EDI,DWORD PTR [ESP+12]
          mov DWORD PTR [ESP+64],EBX
          mov DWORD PTR [ESP+60],EBP
          mov DWORD PTR [ESP+52],ESI
          mov DWORD PTR [ESP+48],EDI
          add ESP,28
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          jmp FUN_433aa0
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8d
          .byte 0xbf
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_435820:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov EBX,DWORD PTR [ESP+72]
          mov EAX,DWORD PTR [EBX]
          mov EDX,EAX
          mov ECX,EAX
          shl EDX,24
          shr ECX,24
          add ECX,EDX
          mov EDX,EAX
          shr EAX,8
          shl EDX,8
          and EAX,65280
          and EDX,16711680
          add EDX,ECX
          add EDX,EAX
          cmp EDX,64
          je L_435880
          cmp EDX,32
          je L_4358d0
          cmp EDX,24
          je L_4358f0
          xor EAX,EAX
          cmp EDX,16
          je L_435910
          add ESP,44
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_435880:
          lea ECX,DWORD PTR [EBX+528]
          lea ESI,DWORD PTR [EBX+784]
          lea EDI,DWORD PTR [EBX+1040]
          lea EBP,DWORD PTR [EBX+1296]
          lea EAX,DWORD PTR [EBX+1552]
L_43589e:
          shr EDX,1
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+16],EDX
          mov EDX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],ESI
          call FUN_433aa0
          add ESP,44
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
L_4358d0:
          lea ECX,DWORD PTR [EBX+272]
          lea ESI,DWORD PTR [EBX+400]
          lea EDI,DWORD PTR [EBX+528]
          lea EBP,DWORD PTR [EBX+656]
          lea EAX,DWORD PTR [EBX+784]
          jmp L_43589e
L_4358f0:
          lea ECX,DWORD PTR [EBX+208]
          lea ESI,DWORD PTR [EBX+304]
          lea EDI,DWORD PTR [EBX+400]
          lea EBP,DWORD PTR [EBX+496]
          lea EAX,DWORD PTR [EBX+592]
          jmp L_43589e
L_435910:
          lea ECX,DWORD PTR [EBX+144]
          lea ESI,DWORD PTR [EBX+208]
          lea EDI,DWORD PTR [EBX+272]
          lea EBP,DWORD PTR [EBX+336]
          lea EAX,DWORD PTR [EBX+400]
          jmp L_43589e
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
L_435940:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,572
          mov ESI,DWORD PTR [ESP+600]
          mov EAX,DWORD PTR [ESI]
          mov EBX,EAX
          mov EDX,EAX
          shl EBX,24
          shr EDX,24
          add EDX,EBX
          mov EBX,EAX
          shr EAX,8
          shl EBX,8
          and EAX,65280
          and EBX,16711680
          add EBX,EDX
          add EBX,EAX
          xor EAX,EAX
          lea EDX,DWORD PTR [EBX-1]
          cmp EDX,63
          ja L_435a54
          mov ECX,DWORD PTR [ESI+4]
          mov DWORD PTR [ESP+4],EBX
          mov EAX,ECX
          mov EDX,ECX
          mov EBP,ECX
          shl EAX,24
          shr EDX,24
          shl EBP,8
          add EDX,EAX
          and EBP,16711680
          shr ECX,8
          lea EAX,DWORD PTR [EDX+EBP*1]
          and ECX,65280
          xor EBP,EBP
          add EAX,ECX
          mov EDI,EAX
          mov DWORD PTR [ESP+32],EAX
          lea EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],EAX
          call FUN_436df0
          mov EAX,DWORD PTR [ESP+32]
          mov EDX,EBP
          mov DWORD PTR [ESP+40],0
          mov DWORD PTR [ESP+32],0
          mov DWORD PTR [ESP+16],EBX
          shl EAX,8
          mov ECX,EAX
          mov EAX,EDI
          shld EDX,EAX,24
          and ECX,16711680
          mov EAX,EDX
          mov EDX,EBP
          shld EDX,EDI,8
          and EAX,65280
          or ECX,EAX
          movzx EAX,DL
          mov EDX,EDI
          mov DWORD PTR [ESP+44],EAX
          shl EDX,24
          mov EAX,0
          add EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+36],ECX
          adc EDX,DWORD PTR [ESP+44]
          add EAX,DWORD PTR [ESP+32]
          adc EDX,DWORD PTR [ESP+36]
          add ESI,16
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+48],EAX
          lea EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+52],EDX
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+592]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+596]
          mov DWORD PTR [ESP],EAX
          call FUN_4380f0
L_435a54:
          add ESP,572
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x90
L_435a60:
          push EBX
          mov ECX,DWORD PTR [ESP+16]
          mov EAX,DWORD PTR [ESP+8]
          mov EDX,DWORD PTR [ESP+12]
          lea EBX,DWORD PTR [ECX-39]
          cmp EBX,473
          ja L_435a80
          pop EBX
          jmp L_433c80
          .byte 0x66
          .byte 0x90
L_435a80:
          xor EAX,EAX
          pop EBX
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8d
          .byte 0xbf
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_435a90:
          push EDI
          push ESI
          push EBX
          xor EBX,EBX
          sub ESP,16
          mov ESI,DWORD PTR [ESP+36]
          mov EDI,DWORD PTR [ESP+32]
          test ESI,ESI
          jg L_435acb
          jmp L_435ae0
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_435ab0:
          movzx EAX,BYTE PTR [EDI+EBX*1]
          mov DWORD PTR [ESP],OFFSET L_45cbe4
          add EBX,1
          mov DWORD PTR [ESP+4],EAX
          call FUN_4490e0
          cmp ESI,EBX
          je L_435ae0
L_435acb:
          test BL,15
          jne L_435ab0
          mov DWORD PTR [ESP],OFFSET L_45cbe0
          call FUN_4490e0
          jmp L_435ab0
          .byte 0x66
          .byte 0x90
L_435ae0:
          mov DWORD PTR [ESP+32],10
          add ESP,16
          pop EBX
          pop ESI
          pop EDI
          jmp FUN_4490d8
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
FUN_435b00:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,1100
          mov ESI,DWORD PTR [ESP+1128]
          mov EAX,DWORD PTR [ESI]
          mov EBX,EAX
          mov EDX,EAX
          shl EBX,24
          shr EDX,24
          add EDX,EBX
          mov EBX,EAX
          shr EAX,8
          shl EBX,8
          and EAX,65280
          and EBX,16711680
          add EBX,EDX
          add EBX,EAX
          xor EAX,EAX
          lea EDX,DWORD PTR [EBX-1]
          cmp EDX,63
          jbe L_435b50
L_435b40:
          add ESP,1100
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_435b50:
          mov EAX,DWORD PTR [ESP+1124]
          lea EDI,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EAX
          call FUN_433e10
          mov EAX,DWORD PTR [ESI]
          mov EBP,EAX
          mov EDX,EAX
          shl EBP,24
          shr EDX,24
          add EDX,EBP
          mov EBP,EAX
          shr EAX,8
          shl EBP,8
          and EAX,65280
          and EBP,16711680
          add EBP,EDX
          add EBP,EAX
          lea EAX,DWORD PTR [EBP-1]
          cmp EAX,63
          ja L_435c7c
          mov EAX,DWORD PTR [ESI+4]
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP+44],0
          mov ECX,EAX
          mov EDX,EAX
          shl ECX,24
          shr EDX,24
          add EDX,ECX
          mov ECX,EAX
          shr EAX,8
          shl ECX,8
          and EAX,65280
          and ECX,16711680
          add EDX,ECX
          lea ECX,DWORD PTR [EDX+EAX*1]
          mov DWORD PTR [ESP+40],ECX
          mov DWORD PTR [ESP+48],ECX
          lea ECX,DWORD PTR [ESP+576]
          mov DWORD PTR [ESP],ECX
          call FUN_436df0
          mov EAX,DWORD PTR [ESP+40]
          mov EDX,DWORD PTR [ESP+44]
          mov ECX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+56],0
          mov DWORD PTR [ESP+48],0
          mov DWORD PTR [ESP+16],EBP
          shld EDX,EAX,24
          shl ECX,8
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+4],EDI
          and EDX,65280
          and ECX,16711680
          mov DWORD PTR [ESP],EDI
          or ECX,EDX
          mov EDX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+52],ECX
          shld EDX,EAX,8
          mov EAX,DWORD PTR [ESP+40]
          movzx ECX,DL
          mov DWORD PTR [ESP+60],ECX
          mov EDX,EAX
          mov EAX,0
          shl EDX,24
          add EAX,DWORD PTR [ESP+56]
          adc EDX,DWORD PTR [ESP+60]
          add EAX,DWORD PTR [ESP+48]
          adc EDX,DWORD PTR [ESP+52]
          add ESI,16
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+576],EAX
          lea EAX,DWORD PTR [ESP+576]
          mov DWORD PTR [ESP+580],EDX
          mov DWORD PTR [ESP+8],EAX
          call FUN_4380f0
L_435c7c:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EDI
          shl EBX,3
          mov DWORD PTR [ESP],EDI
          call FUN_433e10
          lea EDX,DWORD PTR [EBX-39]
          xor EAX,EAX
          cmp EDX,473
          ja L_435b40
          movzx EAX,BYTE PTR [ESP+86]
          xor EDX,EDX
          test AL,AL
          je L_435cb5
          xor EDX,EDX
          cmp AL,26
          setne DL
          add EDX,1
L_435cb5:
          lea ESI,DWORD PTR [ESP+576]
          mov EAX,DWORD PTR [ESP+1120]
          mov DWORD PTR [ESP],EBX
          mov ECX,ESI
          call FUN_4339d0
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],ESI
          call FUN_449100
          test EAX,EAX
          sete AL
          add ESP,1100
          pop EBX
          movzx EAX,AL
          pop ESI
          pop EDI
          pop EBP
          ret 
L_435cf0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,572
          mov ESI,DWORD PTR [ESP+600]
          mov EAX,DWORD PTR [ESI]
          mov EBX,EAX
          mov EDX,EAX
          shl EBX,24
          shr EDX,24
          add EDX,EBX
          mov EBX,EAX
          shr EAX,8
          shl EBX,8
          and EAX,65280
          and EBX,16711680
          add EBX,EDX
          add EBX,EAX
          xor EAX,EAX
          lea EDX,DWORD PTR [EBX-1]
          cmp EDX,63
          ja L_435dd8
          mov EAX,DWORD PTR [ESP+596]
          xor EDX,EDX
          movzx EAX,BYTE PTR [EAX+22]
          test AL,AL
          jne L_435de3
L_435d49:
          lea EAX,DWORD PTR [EBX*8]
          lea EDI,DWORD PTR [ESP+48]
          lea ECX,DWORD PTR [EAX-39]
          cmp ECX,473
          jbe L_435df2
L_435d63:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EDI
          call FUN_433e10
          mov EDX,DWORD PTR [ESI]
          mov ECX,EDX
          mov EAX,EDX
          shl ECX,24
          shr EAX,24
          lea EBP,DWORD PTR [ECX+EAX*1]
          mov EAX,EDX
          shr EDX,8
          shl EAX,8
          and EDX,65280
          and EAX,16711680
          lea ECX,DWORD PTR [EBP+EAX*1]
          lea EAX,DWORD PTR [ECX+EDX*1]
          cmp EAX,64
          je L_435e10
          cmp EAX,32
          je L_435e84
          cmp EAX,24
          je L_435eb0
          cmp EAX,16
          je L_435e60
L_435dbc:
          mov EAX,DWORD PTR [ESP+596]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],EAX
          call FUN_433e10
          mov EAX,1
L_435dd8:
          add ESP,572
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_435de3:
          xor EDX,EDX
          cmp AL,26
          setne DL
          add EDX,1
          jmp L_435d49
L_435df2:
          mov DWORD PTR [ESP],EAX
          mov EAX,DWORD PTR [ESP+592]
          mov ECX,EDI
          call FUN_4339d0
          jmp L_435d63
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_435e10:
          lea EDX,DWORD PTR [ESI+784]
          lea ECX,DWORD PTR [ESI+528]
          lea EBP,DWORD PTR [ESI+1296]
          mov DWORD PTR [ESP+44],EDX
          lea EDX,DWORD PTR [ESI+1040]
          add ESI,1552
L_435e32:
          shr EAX,1
          mov DWORD PTR [ESP+4],EDX
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+16],EAX
          mov EAX,DWORD PTR [ESP+44]
          mov EDX,EDI
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP],EAX
          mov EAX,EDI
          call FUN_433aa0
          jmp L_435dbc
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_435e60:
          lea EDX,DWORD PTR [ESI+208]
          lea ECX,DWORD PTR [ESI+144]
          lea EBP,DWORD PTR [ESI+336]
          mov DWORD PTR [ESP+44],EDX
          lea EDX,DWORD PTR [ESI+272]
          add ESI,400
          jmp L_435e32
L_435e84:
          lea EDX,DWORD PTR [ESI+400]
          lea ECX,DWORD PTR [ESI+272]
          lea EBP,DWORD PTR [ESI+656]
          mov DWORD PTR [ESP+44],EDX
          lea EDX,DWORD PTR [ESI+528]
          add ESI,784
          jmp L_435e32
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_435eb0:
          lea EDX,DWORD PTR [ESI+304]
          lea ECX,DWORD PTR [ESI+208]
          lea EBP,DWORD PTR [ESI+496]
          mov DWORD PTR [ESP+44],EDX
          lea EDX,DWORD PTR [ESI+400]
          add ESI,592
          jmp L_435e32
L_435ed7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_435ee0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,76
          mov EBX,DWORD PTR [ESP+96]
          mov ESI,DWORD PTR [ESP+100]
          test EBX,4294966271
          je L_435f07
          cmp EBX,768
          je L_435f07
          cmp EBX,2048
          jne L_435f14
L_435f07:
          cmp ESI,2
          jbe L_435f14
          test ESI,1
          jne L_435f20
L_435f14:
          xor EAX,EAX
L_435f16:
          add ESP,76
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x66
          .byte 0x90
L_435f20:
          mov EAX,EBX
          lea EBP,DWORD PTR [ESP+20]
          mov DWORD PTR [ESP+8],ESI
          shr EAX,5
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],EBP
          call FUN_43e940
          cmp EAX,1
          jne L_435f14
          cmp EBX,4096
          je L_4360fd
          cmp EBX,2048
          je L_43624d
          cmp EBX,1536
          je L_435fb1
          cmp EBX,1024
          je L_43639b
L_435f6a:
          mov EAX,ESI
          mov EDX,ESI
          mov EDI,DWORD PTR [ESP+104]
          shl EAX,24
          shr EDX,24
          add EDX,EAX
          mov EAX,ESI
          shr ESI,8
          shl EAX,8
          and ESI,65280
          and EAX,16711680
          add EAX,EDX
          add ESI,EAX
          mov EAX,DWORD PTR [ESP+108]
          mov DWORD PTR [EAX+4],ESI
          mov EAX,DWORD PTR [EAX]
          mov DWORD PTR [EDI+4],ESI
          mov DWORD PTR [EDI],EAX
          mov DWORD PTR [ESP],EBP
          call FUN_43e870
          mov EAX,1
          jmp L_435f16
L_435fb1:
          mov EDI,DWORD PTR [ESP+108]
          xor EAX,EAX
          mov DWORD PTR [EDI+684],0
          mov EDX,DWORD PTR [ESP+108]
          lea EDI,DWORD PTR [EDX+4]
          mov ECX,EDX
          and EDI,4294967292
          sub ECX,EDI
          add ECX,688
          shr ECX,2
          rep stosd DWORD PTR ES:[EDI]
          mov EDI,DWORD PTR [ESP+104]
          mov DWORD PTR [EDI],0
          mov ECX,DWORD PTR [ESP+104]
          mov DWORD PTR [ECX+204],0
          mov EDX,DWORD PTR [ESP+104]
          lea EDI,DWORD PTR [EDX+4]
          mov ECX,EDX
          and EDI,4294967292
          sub ECX,EDI
          add ECX,208
          shr ECX,2
          rep stosd DWORD PTR ES:[EDI]
          mov EAX,DWORD PTR [ESP+108]
          mov DWORD PTR [EAX],402653184
          mov EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP],24
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+108]
          add EAX,16
          mov DWORD PTR [ESP+4],EAX
          call FUN_437040
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],12
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+108]
          add EAX,208
          mov DWORD PTR [ESP+4],EAX
          call FUN_437040
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],12
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+108]
          add EAX,304
          mov DWORD PTR [ESP+4],EAX
          call FUN_437040
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP],12
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+108]
          add EAX,400
          mov DWORD PTR [ESP+4],EAX
          call FUN_437040
          mov EAX,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP],12
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+108]
          add EAX,496
          mov DWORD PTR [ESP+4],EAX
          call FUN_437040
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP],12
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+108]
          add EAX,592
          mov DWORD PTR [ESP+4],EAX
          call FUN_437040
          mov EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP],24
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+104]
          add EAX,16
          mov DWORD PTR [ESP+4],EAX
          call FUN_437040
          jmp L_435f6a
L_4360fd:
          mov EDI,DWORD PTR [ESP+108]
          xor EAX,EAX
          mov DWORD PTR [EDI+1804],0
          mov EDI,DWORD PTR [ESP+108]
          mov ECX,DWORD PTR [ESP+108]
          add EDI,4
          and EDI,4294967292
          sub ECX,EDI
          add ECX,1808
          shr ECX,2
          rep stosd DWORD PTR ES:[EDI]
          mov EDI,DWORD PTR [ESP+104]
          mov DWORD PTR [EDI],0
          mov EDI,DWORD PTR [ESP+104]
          mov DWORD PTR [EDI+524],0
          mov EDI,DWORD PTR [ESP+104]
          mov ECX,DWORD PTR [ESP+104]
          add EDI,4
          and EDI,4294967292
          sub ECX,EDI
          add ECX,528
          shr ECX,2
          rep stosd DWORD PTR ES:[EDI]
          mov EAX,DWORD PTR [ESP+108]
          mov DWORD PTR [EAX],1073741824
          mov EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP],64
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+108]
          add EAX,16
          mov DWORD PTR [ESP+4],EAX
          call FUN_437040
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],32
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+108]
          add EAX,528
          mov DWORD PTR [ESP+4],EAX
          call FUN_437040
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],32
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+108]
          add EAX,784
          mov DWORD PTR [ESP+4],EAX
          call FUN_437040
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP],32
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+108]
          add EAX,1040
          mov DWORD PTR [ESP+4],EAX
          call FUN_437040
          mov EAX,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP],32
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+108]
          add EAX,1296
          mov DWORD PTR [ESP+4],EAX
          call FUN_437040
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP],32
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+108]
          add EAX,1552
          mov DWORD PTR [ESP+4],EAX
          call FUN_437040
          mov EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP],64
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+104]
          add EAX,16
          mov DWORD PTR [ESP+4],EAX
          call FUN_437040
          jmp L_435f6a
L_43624d:
          mov EDI,DWORD PTR [ESP+108]
          xor EAX,EAX
          mov DWORD PTR [EDI+908],0
          mov EDI,DWORD PTR [ESP+108]
          mov ECX,DWORD PTR [ESP+108]
          add EDI,4
          and EDI,4294967292
          sub ECX,EDI
          add ECX,912
          shr ECX,2
          rep stosd DWORD PTR ES:[EDI]
          mov EDX,DWORD PTR [ESP+104]
          mov DWORD PTR [EDX],0
          mov EDI,DWORD PTR [ESP+104]
          mov DWORD PTR [EDI+268],0
          mov EDX,DWORD PTR [ESP+104]
          lea EDI,DWORD PTR [EDX+4]
          mov ECX,EDX
          and EDI,4294967292
          sub ECX,EDI
          add ECX,272
          shr ECX,2
          rep stosd DWORD PTR ES:[EDI]
          mov EAX,DWORD PTR [ESP+108]
          mov DWORD PTR [EAX],536870912
          mov EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP],32
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+108]
          add EAX,16
          mov DWORD PTR [ESP+4],EAX
          call FUN_437040
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],16
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+108]
          add EAX,272
          mov DWORD PTR [ESP+4],EAX
          call FUN_437040
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],16
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+108]
          add EAX,400
          mov DWORD PTR [ESP+4],EAX
          call FUN_437040
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP],16
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+108]
          add EAX,528
          mov DWORD PTR [ESP+4],EAX
          call FUN_437040
          mov EAX,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP],16
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+108]
          add EAX,656
          mov DWORD PTR [ESP+4],EAX
          call FUN_437040
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP],16
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+108]
          add EAX,784
          mov DWORD PTR [ESP+4],EAX
          call FUN_437040
          mov EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP],32
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+104]
          add EAX,16
          mov DWORD PTR [ESP+4],EAX
          call FUN_437040
          jmp L_435f6a
L_43639b:
          mov EDI,DWORD PTR [ESP+108]
          xor EAX,EAX
          mov DWORD PTR [EDI+460],0
          mov ECX,DWORD PTR [ESP+108]
          lea EDI,DWORD PTR [ECX+4]
          and EDI,4294967292
          sub ECX,EDI
          add ECX,464
          shr ECX,2
          rep stosd DWORD PTR ES:[EDI]
          mov EDI,DWORD PTR [ESP+104]
          mov DWORD PTR [EDI],0
          mov EDX,DWORD PTR [ESP+104]
          mov DWORD PTR [EDX+140],0
          mov ECX,DWORD PTR [ESP+104]
          lea EDI,DWORD PTR [ECX+4]
          and EDI,4294967292
          sub ECX,EDI
          add ECX,144
          shr ECX,2
          rep stosd DWORD PTR ES:[EDI]
          mov EAX,DWORD PTR [ESP+108]
          mov DWORD PTR [EAX],268435456
          mov EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP],16
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+108]
          add EAX,16
          mov DWORD PTR [ESP+4],EAX
          call FUN_437040
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],8
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+108]
          add EAX,144
          mov DWORD PTR [ESP+4],EAX
          call FUN_437040
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],8
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+108]
          add EAX,208
          mov DWORD PTR [ESP+4],EAX
          call FUN_437040
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP],8
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+108]
          add EAX,272
          mov DWORD PTR [ESP+4],EAX
          call FUN_437040
          mov EAX,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP],8
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+108]
          add EAX,336
          mov DWORD PTR [ESP+4],EAX
          call FUN_437040
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP],8
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+108]
          add EAX,400
          mov DWORD PTR [ESP+4],EAX
          call FUN_437040
          mov EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP],16
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+104]
          add EAX,16
          mov DWORD PTR [ESP+4],EAX
          call FUN_437040
          jmp L_435f6a
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
L_4364f0:
          sub ESP,28
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+4],8
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],EAX
          call FUN_445e50
          add ESP,28
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_436520:
          cmp DWORD PTR [ESP+16],0
          mov ECX,DWORD PTR [ESP+4]
          mov EAX,DWORD PTR [ESP+8]
          mov EDX,DWORD PTR [ESP+12]
          mov DWORD PTR [ESP+12],ECX
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP+4],EAX
          jne L_436544
          jmp FUN_445fd0
L_436544:
          jmp FUN_445f60
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_436550:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov EDI,DWORD PTR [ESP+84]
          mov EDX,DWORD PTR [ESP+80]
          test EDI,EDI
          jne L_436620
          mov ESI,DWORD PTR [ESP+72]
          xor ECX,ECX
          mov EBP,DWORD PTR [ESP+68]
          mov EBX,DWORD PTR [ESP+76]
          test ESI,ESI
          je L_436611
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
L_436580:
          mov EAX,DWORD PTR [ESP+64]
          mov ESI,DWORD PTR [EBP]
          mov EDI,DWORD PTR [EBP+4]
          mov DWORD PTR [ESP+4],EBX
          add EBX,8
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+28],EDX
          add EBP,8
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+24],ECX
          call FUN_445fd0
          mov EDX,DWORD PTR [ESP+28]
          movzx EAX,BYTE PTR [EBP-8]
          mov ECX,DWORD PTR [ESP+24]
          xor AL,BYTE PTR [EDX]
          add ECX,8
          mov BYTE PTR [EBX-8],AL
          movzx EAX,BYTE PTR [EBP-7]
          xor AL,BYTE PTR [EDX+1]
          mov BYTE PTR [EBX-7],AL
          movzx EAX,BYTE PTR [EBP-6]
          xor AL,BYTE PTR [EDX+2]
          mov BYTE PTR [EBX-6],AL
          movzx EAX,BYTE PTR [EBP-5]
          xor AL,BYTE PTR [EDX+3]
          mov BYTE PTR [EBX-5],AL
          movzx EAX,BYTE PTR [EBP-4]
          xor AL,BYTE PTR [EDX+4]
          mov BYTE PTR [EBX-4],AL
          movzx EAX,BYTE PTR [EBP-3]
          xor AL,BYTE PTR [EDX+5]
          mov BYTE PTR [EBX-3],AL
          movzx EAX,BYTE PTR [EBP-2]
          xor AL,BYTE PTR [EDX+6]
          mov BYTE PTR [EBX-2],AL
          movzx EAX,BYTE PTR [EBP-1]
          xor AL,BYTE PTR [EDX+7]
          mov BYTE PTR [EBX-1],AL
          cmp DWORD PTR [ESP+72],ECX
          mov DWORD PTR [EDX],ESI
          mov DWORD PTR [EDX+4],EDI
          ja L_436580
L_436611:
          add ESP,44
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
L_436620:
          mov EAX,DWORD PTR [ESP+72]
          test EAX,EAX
          je L_436611
          mov ESI,DWORD PTR [ESP+68]
          mov EBX,DWORD PTR [ESP+76]
          xor EDI,EDI
          mov EBP,EDX
L_436634:
          movzx EAX,BYTE PTR [ESI]
          add EDI,8
          add ESI,8
          xor AL,BYTE PTR [EBP]
          mov BYTE PTR [EBX],AL
          movzx EAX,BYTE PTR [ESI-7]
          xor AL,BYTE PTR [EBP+1]
          mov BYTE PTR [EBX+1],AL
          movzx EAX,BYTE PTR [ESI-6]
          xor AL,BYTE PTR [EBP+2]
          mov BYTE PTR [EBX+2],AL
          movzx EAX,BYTE PTR [ESI-5]
          xor AL,BYTE PTR [EBP+3]
          mov BYTE PTR [EBX+3],AL
          movzx EAX,BYTE PTR [ESI-4]
          xor AL,BYTE PTR [EBP+4]
          mov BYTE PTR [EBX+4],AL
          movzx EAX,BYTE PTR [ESI-3]
          xor AL,BYTE PTR [EBP+5]
          mov BYTE PTR [EBX+5],AL
          movzx EAX,BYTE PTR [ESI-2]
          xor AL,BYTE PTR [EBP+6]
          mov BYTE PTR [EBX+6],AL
          movzx EAX,BYTE PTR [ESI-1]
          xor AL,BYTE PTR [EBP+7]
          mov BYTE PTR [EBX+7],AL
          mov EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EBX
          add EBX,8
          mov DWORD PTR [ESP+8],EAX
          call FUN_445f60
          mov EAX,DWORD PTR [EBX-8]
          mov EDX,DWORD PTR [EBX-4]
          cmp DWORD PTR [ESP+72],EDI
          mov DWORD PTR [EBP],EAX
          mov DWORD PTR [EBP+4],EDX
          ja L_436634
          add ESP,44
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
L_4366c0:
          sub ESP,28
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+4],24
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],EAX
          call FUN_445ea0
          add ESP,28
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_4366f0:
          cmp DWORD PTR [ESP+16],0
          mov ECX,DWORD PTR [ESP+4]
          mov EAX,DWORD PTR [ESP+8]
          mov EDX,DWORD PTR [ESP+12]
          mov DWORD PTR [ESP+12],ECX
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP+4],EAX
          jne L_436714
          jmp FUN_4460e0
L_436714:
          jmp FUN_446050
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_436720:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov EDI,DWORD PTR [ESP+84]
          mov EDX,DWORD PTR [ESP+80]
          test EDI,EDI
          jne L_4367f0
          mov ESI,DWORD PTR [ESP+72]
          xor ECX,ECX
          mov EBP,DWORD PTR [ESP+68]
          mov EBX,DWORD PTR [ESP+76]
          test ESI,ESI
          je L_4367e1
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
L_436750:
          mov EAX,DWORD PTR [ESP+64]
          mov ESI,DWORD PTR [EBP]
          mov EDI,DWORD PTR [EBP+4]
          mov DWORD PTR [ESP+4],EBX
          add EBX,8
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+28],EDX
          add EBP,8
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+24],ECX
          call FUN_4460e0
          mov EDX,DWORD PTR [ESP+28]
          movzx EAX,BYTE PTR [EBP-8]
          mov ECX,DWORD PTR [ESP+24]
          xor AL,BYTE PTR [EDX]
          add ECX,8
          mov BYTE PTR [EBX-8],AL
          movzx EAX,BYTE PTR [EBP-7]
          xor AL,BYTE PTR [EDX+1]
          mov BYTE PTR [EBX-7],AL
          movzx EAX,BYTE PTR [EBP-6]
          xor AL,BYTE PTR [EDX+2]
          mov BYTE PTR [EBX-6],AL
          movzx EAX,BYTE PTR [EBP-5]
          xor AL,BYTE PTR [EDX+3]
          mov BYTE PTR [EBX-5],AL
          movzx EAX,BYTE PTR [EBP-4]
          xor AL,BYTE PTR [EDX+4]
          mov BYTE PTR [EBX-4],AL
          movzx EAX,BYTE PTR [EBP-3]
          xor AL,BYTE PTR [EDX+5]
          mov BYTE PTR [EBX-3],AL
          movzx EAX,BYTE PTR [EBP-2]
          xor AL,BYTE PTR [EDX+6]
          mov BYTE PTR [EBX-2],AL
          movzx EAX,BYTE PTR [EBP-1]
          xor AL,BYTE PTR [EDX+7]
          mov BYTE PTR [EBX-1],AL
          cmp DWORD PTR [ESP+72],ECX
          mov DWORD PTR [EDX],ESI
          mov DWORD PTR [EDX+4],EDI
          ja L_436750
L_4367e1:
          add ESP,44
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
L_4367f0:
          mov EAX,DWORD PTR [ESP+72]
          test EAX,EAX
          je L_4367e1
          mov ESI,DWORD PTR [ESP+68]
          mov EBX,DWORD PTR [ESP+76]
          xor EDI,EDI
          mov EBP,EDX
L_436804:
          movzx EAX,BYTE PTR [ESI]
          add EDI,8
          add ESI,8
          xor AL,BYTE PTR [EBP]
          mov BYTE PTR [EBX],AL
          movzx EAX,BYTE PTR [ESI-7]
          xor AL,BYTE PTR [EBP+1]
          mov BYTE PTR [EBX+1],AL
          movzx EAX,BYTE PTR [ESI-6]
          xor AL,BYTE PTR [EBP+2]
          mov BYTE PTR [EBX+2],AL
          movzx EAX,BYTE PTR [ESI-5]
          xor AL,BYTE PTR [EBP+3]
          mov BYTE PTR [EBX+3],AL
          movzx EAX,BYTE PTR [ESI-4]
          xor AL,BYTE PTR [EBP+4]
          mov BYTE PTR [EBX+4],AL
          movzx EAX,BYTE PTR [ESI-3]
          xor AL,BYTE PTR [EBP+5]
          mov BYTE PTR [EBX+5],AL
          movzx EAX,BYTE PTR [ESI-2]
          xor AL,BYTE PTR [EBP+6]
          mov BYTE PTR [EBX+6],AL
          movzx EAX,BYTE PTR [ESI-1]
          xor AL,BYTE PTR [EBP+7]
          mov BYTE PTR [EBX+7],AL
          mov EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EBX
          add EBX,8
          mov DWORD PTR [ESP+8],EAX
          call FUN_446050
          mov EAX,DWORD PTR [EBX-8]
          mov EDX,DWORD PTR [EBX-4]
          cmp DWORD PTR [ESP+72],EDI
          mov DWORD PTR [EBP],EAX
          mov DWORD PTR [EBP+4],EDX
          ja L_436804
          add ESP,44
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
L_436890:
          jmp FUN_445690
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
          .byte 0x8d
          .byte 0xbc
          .byte 0x27
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4368a0:
          jmp FUN_4456c0
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
          .byte 0x8d
          .byte 0xbc
          .byte 0x27
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4368b0:
          push EDI
          push ESI
          push EBX
          sub ESP,32
          mov EAX,DWORD PTR [ESP+48]
          mov EDI,DWORD PTR [ESP+56]
          lea ESI,DWORD PTR [ESP+16]
          mov EBX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],EAX
          call FUN_445830
          cmp EDI,15
          jbe L_436900
          mov EAX,DWORD PTR [ESP+16]
          mov DWORD PTR [EBX],EAX
          mov EAX,DWORD PTR [ESP+20]
          mov DWORD PTR [EBX+4],EAX
          mov EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [EBX+8],EAX
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [EBX+12],EAX
          add ESP,32
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_436900:
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EBX
          call FUN_4490f8
          add ESP,32
          pop EBX
          pop ESI
          pop EDI
          ret 
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_436920:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,204
          mov EBP,DWORD PTR [ESP+228]
          lea EDI,DWORD PTR [ESP+40]
          mov ESI,DWORD PTR [ESP+244]
          mov EBX,DWORD PTR [ESP+248]
          mov DWORD PTR [ESP],EDI
          call FUN_445690
          test EBP,EBP
          je L_43695e
          mov EAX,DWORD PTR [ESP+224]
          test EAX,EAX
          jne L_436a03
L_43695e:
          mov ECX,DWORD PTR [ESP+236]
          test ECX,ECX
          je L_436974
          mov EDX,DWORD PTR [ESP+232]
          test EDX,EDX
          jne L_4369e0
L_436974:
          test ESI,ESI
          je L_43699a
          mov EAX,DWORD PTR [ESP+240]
          test EAX,EAX
          je L_43699a
          mov EAX,DWORD PTR [ESP+240]
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],EAX
          call FUN_4456c0
L_43699a:
          lea ESI,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],ESI
          call FUN_445830
          cmp DWORD PTR [ESP+252],15
          jbe L_436a20
          mov EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [EBX],EAX
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [EBX+4],EAX
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [EBX+8],EAX
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [EBX+12],EAX
          add ESP,204
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
L_4369e0:
          mov EAX,DWORD PTR [ESP+236]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+232]
          mov DWORD PTR [ESP+4],EAX
          call FUN_4456c0
          jmp L_436974
L_436a03:
          mov EAX,DWORD PTR [ESP+224]
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],EAX
          call FUN_4456c0
          jmp L_43695e
          .byte 0x90
L_436a20:
          mov EAX,DWORD PTR [ESP+252]
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],EAX
          call FUN_4490f8
          add ESP,204
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
          nop
          nop

.section .rdata,"dr"
.p2align 2
L_45cbe0:
          .string "\n  "
L_45cbe4:
          .string " %02X"
          .zero 2

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
          .long FUN_433840 - .
          .byte 0x8c
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
          .byte 0x43
          .byte 0xe
          .byte 0x10
          .byte 0x86
          .byte 0x4
          .byte 0x41
          .byte 0xe
          .byte 0x14
          .byte 0x83
          .byte 0x5
          .byte 0x47
          .byte 0xe
          .byte 0x70
          .byte 0x3
          .byte 0x7a
          .byte 0x1
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
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x64
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x5c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_4339d0 - .
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
          .byte 0x43
          .byte 0xe
          .byte 0x10
          .byte 0x86
          .byte 0x4
          .byte 0x41
          .byte 0xe
          .byte 0x14
          .byte 0x83
          .byte 0x5
          .byte 0x47
          .byte 0xe
          .byte 0x40
          .byte 0x2
          .byte 0x46
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
          .byte 0x49
          .byte 0xb
          .byte 0x5f
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
          .byte 0x7b
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
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_433aa0 - .
          .byte 0xdf
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
          .byte 0x43
          .byte 0xe
          .byte 0x10
          .byte 0x86
          .byte 0x4
          .byte 0x41
          .byte 0xe
          .byte 0x14
          .byte 0x83
          .byte 0x5
          .byte 0x48
          .byte 0xe
          .byte 0xd0
          .byte 0x8
          .byte 0x79
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
          .byte 0x45
          .byte 0xb
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x4
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long L_433c80 - .
          .byte 0x81
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
          .byte 0x43
          .byte 0xe
          .byte 0x10
          .byte 0x86
          .byte 0x4
          .byte 0x41
          .byte 0xe
          .byte 0x14
          .byte 0x83
          .byte 0x5
          .byte 0x4a
          .byte 0xe
          .byte 0xc0
          .byte 0x4
          .byte 0x2
          .byte 0xe1
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x10
          .byte 0x44
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
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x44
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_433e10 - .
          .byte 0xda
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
          .byte 0x46
          .byte 0xe
          .byte 0xa0
          .byte 0x1
          .byte 0x3
          .byte 0xcb
          .byte 0x1
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
          .byte 0x0
          .byte 0x0
          .byte 0x50
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x84
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_433ff0 - .
          .byte 0x9b
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
          .byte 0x43
          .byte 0xe
          .byte 0x10
          .byte 0x86
          .byte 0x4
          .byte 0x41
          .byte 0xe
          .byte 0x14
          .byte 0x83
          .byte 0x5
          .byte 0x47
          .byte 0xe
          .byte 0x18
          .byte 0x2
          .byte 0x70
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
          .byte 0x54
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
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd8
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_434090 - .
          .byte 0x79
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
          .byte 0x2
          .byte 0x6d
          .byte 0xa
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
          .byte 0x40
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x14
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long FUN_434110 - .
          .byte 0x9d
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
          .byte 0x46
          .byte 0xe
          .byte 0xf0
          .byte 0x2
          .byte 0x3
          .byte 0xd7
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
          .byte 0x4b
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x58
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long FUN_4345b0 - .
          .byte 0x55
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
          .byte 0x46
          .byte 0xe
          .byte 0xb0
          .byte 0x8
          .byte 0x2
          .byte 0x4a
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x84
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long L_434610 - .
          .byte 0x15
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
          .byte 0x98
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long L_434630 - .
          .byte 0x27
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x63
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb0
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long L_434660 - .
          .byte 0x5c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x87
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x86
          .byte 0x3
          .byte 0x41
          .byte 0xe
          .byte 0x10
          .byte 0x83
          .byte 0x4
          .byte 0x43
          .byte 0xe
          .byte 0x30
          .byte 0x2
          .byte 0x52
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xe4
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long FUN_4346c0 - .
          .byte 0x88
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
          .byte 0x5e
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
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x24
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long FUN_434850 - .
          .byte 0x41
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
          .byte 0x79
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x50
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long FUN_4348a0 - .
          .byte 0x4a
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x2c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x64
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long FUN_4348f0 - .
          .byte 0x57
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
          .byte 0x75
          .byte 0xa
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x48
          .byte 0xb
          .byte 0x51
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x94
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long FUN_434950 - .
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x50
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xa8
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long FUN_434960 - .
          .byte 0x5a
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
          .byte 0x53
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
          .byte 0x42
          .byte 0xb
          .byte 0x71
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
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x34
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xfc
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long FUN_4349c0 - .
          .byte 0x6a
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
          .byte 0x40
          .byte 0x2
          .byte 0x44
          .byte 0xa
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x45
          .byte 0xb
          .byte 0x57
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x50
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x34
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long FUN_434a30 - .
          .byte 0xa2
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
          .byte 0x46
          .byte 0xe
          .byte 0xb0
          .byte 0x1
          .byte 0x2
          .byte 0xbb
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
          .byte 0x2
          .byte 0xcd
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
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x88
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long FUN_434be0 - .
          .byte 0x17
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x9c
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long FUN_434c00 - .
          .byte 0x42
          .byte 0x3
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
          .byte 0x43
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
          .byte 0x1
          .byte 0x3
          .byte 0x56
          .byte 0x2
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
          .byte 0x4a
          .byte 0xb
          .byte 0x2
          .byte 0xcd
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
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x48
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xf4
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long L_434f50 - .
          .byte 0xcf
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
          .byte 0x30
          .byte 0x55
          .byte 0xa
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x44
          .byte 0xb
          .byte 0x2
          .byte 0x4c
          .byte 0xa
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x42
          .byte 0xb
          .byte 0x5f
          .byte 0xa
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x40
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .long FUN_435020 - .
          .byte 0xe4
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
          .byte 0x43
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
          .byte 0xb0
          .byte 0x9
          .byte 0x3
          .byte 0xd3
          .byte 0x1
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
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x80
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .long FUN_435210 - .
          .byte 0x30
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
          .byte 0x43
          .byte 0xe
          .byte 0x70
          .byte 0x3
          .byte 0x20
          .byte 0x2
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
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x44
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc0
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .long FUN_435440 - .
          .byte 0xe6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x87
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x86
          .byte 0x3
          .byte 0x41
          .byte 0xe
          .byte 0x10
          .byte 0x83
          .byte 0x4
          .byte 0x46
          .byte 0xe
          .byte 0xb0
          .byte 0x4
          .byte 0x79
          .byte 0xa
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x4
          .byte 0x4b
          .byte 0xb
          .byte 0x2
          .byte 0x8f
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0xc
          .byte 0x44
          .byte 0xc6
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .long FUN_435530 - .
          .byte 0x7c
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
          .byte 0x6
          .byte 0x79
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
          .byte 0x49
          .byte 0xb
          .byte 0x0
          .byte 0x50
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x48
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .long L_4357b0 - .
          .byte 0x64
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
          .byte 0x6c
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
          .byte 0x5b
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
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x9c
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .long FUN_435820 - .
          .byte 0x13
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
          .byte 0x4a
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
          .byte 0x4b
          .byte 0xb
          .byte 0x2
          .byte 0x43
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
          .byte 0x49
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xf4
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .long L_435940 - .
          .byte 0x1f
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
          .byte 0x46
          .byte 0xe
          .byte 0xd0
          .byte 0x4
          .byte 0x3
          .byte 0x10
          .byte 0x1
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
          .byte 0x0
          .byte 0x0
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x34
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .long L_435a60 - .
          .byte 0x24
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x58
          .byte 0xa
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x47
          .byte 0xb
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x58
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .long L_435a90 - .
          .byte 0x63
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x87
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x86
          .byte 0x3
          .byte 0x41
          .byte 0xe
          .byte 0x10
          .byte 0x83
          .byte 0x4
          .byte 0x45
          .byte 0xe
          .byte 0x20
          .byte 0x2
          .byte 0x53
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x50
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8c
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .long FUN_435b00 - .
          .byte 0xf0
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
          .byte 0x46
          .byte 0xe
          .byte 0xe0
          .byte 0x8
          .byte 0x7c
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
          .byte 0x46
          .byte 0xb
          .byte 0x3
          .byte 0x98
          .byte 0x1
          .byte 0xe
          .byte 0x14
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x10
          .byte 0x44
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
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xe0
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .long L_435cf0 - .
          .byte 0xe7
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
          .byte 0x46
          .byte 0xe
          .byte 0xd0
          .byte 0x4
          .byte 0x2
          .byte 0xe4
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
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x20
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .long L_435ee0 - .
          .byte 0x3
          .byte 0x6
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
          .byte 0x60
          .byte 0x72
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
          .byte 0x43
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x60
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .long L_4364f0 - .
          .byte 0x2b
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x67
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x78
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .long L_436520 - .
          .byte 0x29
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x50
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8c
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .long L_436550 - .
          .byte 0x69
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
          .byte 0xbd
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
          .byte 0x48
          .byte 0xb
          .byte 0x2
          .byte 0x94
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
          .byte 0x0
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xe0
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .long L_4366c0 - .
          .byte 0x2b
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x67
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xf8
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .long L_4366f0 - .
          .byte 0x29
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x50
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc
          .byte 0x9
          .byte 0x0
          .byte 0x0
          .long L_436720 - .
          .byte 0x69
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
          .byte 0xbd
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
          .byte 0x48
          .byte 0xb
          .byte 0x2
          .byte 0x94
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
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x60
          .byte 0x9
          .byte 0x0
          .byte 0x0
          .long L_436890 - .
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x74
          .byte 0x9
          .byte 0x0
          .byte 0x0
          .long L_4368a0 - .
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x40
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x88
          .byte 0x9
          .byte 0x0
          .byte 0x0
          .long L_4368b0 - .
          .byte 0x67
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x87
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x86
          .byte 0x3
          .byte 0x41
          .byte 0xe
          .byte 0x10
          .byte 0x83
          .byte 0x4
          .byte 0x43
          .byte 0xe
          .byte 0x30
          .byte 0x7f
          .byte 0xa
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x4
          .byte 0x48
          .byte 0xb
          .byte 0x53
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x4
          .byte 0x50
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xcc
          .byte 0x9
          .byte 0x0
          .byte 0x0
          .long L_436920 - .
          .byte 0x22
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
          .byte 0x46
          .byte 0xe
          .byte 0xe0
          .byte 0x1
          .byte 0x2
          .byte 0xab
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
          .byte 0x2
          .byte 0x5d
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

.bss
.p2align 2
L_479ac0:
          .zero 4

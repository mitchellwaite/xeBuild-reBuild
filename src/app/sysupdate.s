# app/sysupdate.s -- system update container, xboxupd.bin extraction
#
# original placement:
#   .bss           0046f180-0046f9c0
#   .eh_frame      004666a0-004668b8
#   .rdata         0045066c-00450884
#   .rdata$zzz     004638ac-004638d8
#   .text          0040c240-0040d010

.intel_syntax noprefix
.globl FUN_40c260
.globl FUN_40c650
.globl FUN_40c700
.globl FUN_40c7b0
.globl FUN_40c860
.globl FUN_40c940
.globl FUN_40ca30
.globl FUN_40cc80
.globl FUN_40cfa0

.text
.p2align 4
L_40c240:
          mov EAX,DWORD PTR [L_46f190]
          mov EDX,0
          test EAX,EAX
          mov EAX,OFFSET L_46f5c0
          cmove EAX,EDX
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
FUN_40c260:
          mov EAX,DWORD PTR [L_46f190]
          mov EDX,0
          test EAX,EAX
          mov EAX,OFFSET L_46f1c0
          cmove EAX,EDX
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
L_40c280:
          sub ESP,28
          mov EAX,DWORD PTR [L_46f18c]
          mov DWORD PTR [L_46f184],0
          mov DWORD PTR [L_46f180],0
          test EAX,EAX
          je L_40c2b2
          mov DWORD PTR [ESP],EAX
          call FUN_449140
          mov DWORD PTR [L_46f18c],0
L_40c2b2:
          mov EAX,DWORD PTR [L_46f188]
          test EAX,EAX
          je L_40c2cd
          mov DWORD PTR [ESP],EAX
          call FUN_449140
          mov DWORD PTR [L_46f188],0
L_40c2cd:
          add ESP,28
          ret 
L_40c2d1:
          jmp FUN_40c2e0
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
FUN_40c2e0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,108
          mov EAX,DWORD PTR [L_46f190]
          test EAX,EAX
          jne L_40c360
L_40c2f0:
          mov DWORD PTR [ESP+4],OFFSET L_4506ec
          mov DWORD PTR [ESP],0
          call FUN_433690
L_40c304:
          mov EAX,DWORD PTR [L_46f18c]
          mov EBX,DWORD PTR [L_46f188]
L_40c30f:
          test EAX,EAX
          mov DWORD PTR [L_46f184],0
          mov DWORD PTR [L_46f180],0
          je L_40c339
L_40c327:
          mov DWORD PTR [ESP],EAX
          call FUN_449140
          mov DWORD PTR [L_46f18c],0
L_40c339:
          test EBX,EBX
          je L_40c34f
          mov DWORD PTR [ESP],EBX
          call FUN_449140
          mov DWORD PTR [L_46f188],0
L_40c34f:
          add ESP,108
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_40c357:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_40c360:
          lea ESI,DWORD PTR [ESP+52]
          lea EBX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+4],OFFSET L_45066c
          mov DWORD PTR [ESP],OFFSET L_46f194
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+8],EBX
          call FUN_405d50
          test EAX,EAX
          je L_40c584
L_40c38c:
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+4],OFFSET L_450678
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call FUN_433690
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],EAX
          call FUN_420ab0
          mov ESI,EAX
          mov EAX,DWORD PTR [ESP+48]
          add EAX,2
          mov DWORD PTR [ESP],EAX
          call FUN_420ab0
          movzx EDI,AX
          mov EAX,DWORD PTR [ESP+48]
          add EAX,12
          mov DWORD PTR [ESP],EAX
          call FUN_420ad0
          lea EBX,DWORD PTR [EAX+15]
          mov EBP,EAX
          and EBX,4294967280
          cmp SI,17222
          mov DWORD PTR [L_46f184],EBX
          jne L_40c304
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EBX
          call FUN_4491a0
          test EAX,EAX
          mov DWORD PTR [L_46f18c],EAX
          je L_40c5f0
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+20],EBX
          mov DWORD PTR [ESP+16],EDI
          movzx EDX,BYTE PTR [EAX+1]
          mov DWORD PTR [ESP+12],EDX
          movzx EAX,BYTE PTR [EAX]
          mov DWORD PTR [ESP+4],OFFSET L_4506a4
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call FUN_433690
          mov EBX,DWORD PTR [L_46f18c]
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],EBX
          call FUN_4490f8
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EBX
          call FUN_401ce0
          test EAX,EAX
          je L_40c560
          mov DWORD PTR [ESP+4],OFFSET L_4506dc
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EAX,DWORD PTR [ESP+48]
          add EAX,EBP
          mov DWORD PTR [ESP],EAX
          call FUN_420ab0
          mov EBX,EAX
          mov EAX,DWORD PTR [ESP+48]
          lea EAX,DWORD PTR [EAX+EBP*1+2]
          mov DWORD PTR [ESP],EAX
          call FUN_420ab0
          movzx ESI,AX
          mov EAX,DWORD PTR [ESP+48]
          lea EAX,DWORD PTR [EAX+EBP*1+12]
          mov DWORD PTR [ESP],EAX
          call FUN_420ad0
          mov EDI,EAX
          lea EAX,DWORD PTR [EAX+15]
          and EAX,4294967280
          cmp BX,17223
          mov DWORD PTR [L_46f180],EAX
          jne L_40c304
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_4491a0
          test EAX,EAX
          mov DWORD PTR [L_46f188],EAX
          je L_40c60f
          mov EDX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP],EAX
          lea EBX,DWORD PTR [EDX+EBP*1]
          mov DWORD PTR [ESP+44],EDX
          mov DWORD PTR [ESP+4],EBX
          call FUN_4490f8
          mov EDX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+20],EDI
          mov DWORD PTR [ESP+16],ESI
          movzx EAX,BYTE PTR [EDX+EBP*1+1]
          mov DWORD PTR [ESP+12],EAX
          movzx EAX,BYTE PTR [EBX]
          mov DWORD PTR [ESP+4],OFFSET L_4506a4
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call FUN_433690
          mov EAX,DWORD PTR [L_46f18c]
          mov DWORD PTR [ESP+8],EDI
          add EAX,816
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [L_46f188]
          mov DWORD PTR [ESP],EAX
          call FUN_401dc0
          test EAX,EAX
          jne L_40c637
          nop
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_40c560:
          mov DWORD PTR [ESP+4],OFFSET L_4506e3
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EAX,DWORD PTR [L_46f18c]
          mov EBX,DWORD PTR [L_46f188]
          jmp L_40c30f
L_40c584:
          mov DWORD PTR [ESP+56],1634493988
          mov DWORD PTR [ESP+60],6252659
          xor EAX,EAX
L_40c596:
          mov DWORD PTR [ESP+EAX*1+64],0
          add EAX,4
          cmp EAX,32
          jb L_40c596
          lea EAX,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP],OFFSET L_46f194
          mov DWORD PTR [ESP+63],2020565624
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP+67],778334325
          mov DWORD PTR [ESP+71],7235938
          call FUN_405d50
          test EAX,EAX
          jne L_40c38c
          jmp L_40c2f0
L_40c5e7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_40c5f0:
          mov EBX,DWORD PTR [L_46f188]
          mov DWORD PTR [L_46f184],0
          mov DWORD PTR [L_46f180],0
          jmp L_40c339
L_40c60f:
          mov EAX,DWORD PTR [L_46f18c]
          xor EBX,EBX
          mov DWORD PTR [L_46f184],0
          mov DWORD PTR [L_46f180],0
          test EAX,EAX
          jne L_40c327
          jmp L_40c34f
L_40c637:
          mov DWORD PTR [ESP+4],OFFSET L_4506dc
          mov DWORD PTR [ESP],1
          call FUN_433690
          jmp L_40c34f
FUN_40c650:
          mov EDX,DWORD PTR [L_46f18c]
          xor EAX,EAX
          test EDX,EDX
          je L_40c6f1
          mov ECX,DWORD PTR [L_46f184]
          test ECX,ECX
          jne L_40c670
          repz ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_40c670:
          push EBX
          add EDX,12
          sub ESP,40
          mov DWORD PTR [ESP],EDX
          call FUN_420ad0
          mov EBX,EAX
          mov EAX,DWORD PTR [L_46f18c]
          add EAX,2
          mov DWORD PTR [ESP],EAX
          call FUN_420ab0
          mov EDX,DWORD PTR [L_46f18c]
          movzx EAX,AX
          mov DWORD PTR [ESP+20],EBX
          mov DWORD PTR [ESP+16],EAX
          movzx EAX,BYTE PTR [EDX+1]
          mov DWORD PTR [ESP+12],EAX
          movzx EAX,BYTE PTR [EDX]
          mov DWORD PTR [ESP+4],OFFSET L_450724
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call FUN_433690
          mov EDX,DWORD PTR [L_46f18c]
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [L_46f18c],0
          mov DWORD PTR [EAX],EDX
          mov EAX,DWORD PTR [ESP+52]
          mov EDX,DWORD PTR [L_46f184]
          mov DWORD PTR [EAX],EDX
          add ESP,40
          mov EAX,1
          pop EBX
          ret 
L_40c6f1:
          repz ret 
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
FUN_40c700:
          mov EDX,DWORD PTR [L_46f188]
          xor EAX,EAX
          test EDX,EDX
          je L_40c7a1
          mov ECX,DWORD PTR [L_46f180]
          test ECX,ECX
          jne L_40c720
          repz ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_40c720:
          push EBX
          add EDX,12
          sub ESP,40
          mov DWORD PTR [ESP],EDX
          call FUN_420ad0
          mov EBX,EAX
          mov EAX,DWORD PTR [L_46f188]
          add EAX,2
          mov DWORD PTR [ESP],EAX
          call FUN_420ab0
          mov EDX,DWORD PTR [L_46f188]
          movzx EAX,AX
          mov DWORD PTR [ESP+20],EBX
          mov DWORD PTR [ESP+16],EAX
          movzx EAX,BYTE PTR [EDX+1]
          mov DWORD PTR [ESP+12],EAX
          movzx EAX,BYTE PTR [EDX]
          mov DWORD PTR [ESP+4],OFFSET L_450724
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call FUN_433690
          mov EDX,DWORD PTR [L_46f188]
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [L_46f188],0
          mov DWORD PTR [EAX],EDX
          mov EAX,DWORD PTR [ESP+52]
          mov EDX,DWORD PTR [L_46f180]
          mov DWORD PTR [EAX],EDX
          add ESP,40
          mov EAX,1
          pop EBX
          ret 
L_40c7a1:
          repz ret 
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
FUN_40c7b0:
          mov EAX,DWORD PTR [L_46f190]
          test EAX,EAX
          jne L_40c7c0
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_40c7c0:
          push EBX
          sub ESP,72
          mov EAX,DWORD PTR [ESP+88]
          mov DWORD PTR [ESP],OFFSET L_46f194
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+84]
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP+4],EAX
          call FUN_405d50
          mov EDX,EAX
          mov EAX,1
          test EDX,EDX
          je L_40c800
L_40c7f3:
          add ESP,72
          pop EBX
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_40c800:
          mov DWORD PTR [ESP+24],1634493988
          mov DWORD PTR [ESP+28],6252659
          xor EAX,EAX
L_40c812:
          mov DWORD PTR [ESP+EAX*1+32],0
          add EAX,4
          cmp EAX,32
          jb L_40c812
          mov EAX,DWORD PTR [ESP+80]
          lea EBX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP+8],40
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call FUN_449070
          mov EAX,DWORD PTR [ESP+88]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],OFFSET L_46f194
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+84]
          mov DWORD PTR [ESP+8],EAX
          call FUN_405d50
          jmp L_40c7f3
FUN_40c860:
          push EDI
          push ESI
          push EBX
          sub ESP,16
          mov EBX,DWORD PTR [L_46f190]
          mov ESI,DWORD PTR [ESP+32]
          mov EDI,DWORD PTR [ESP+36]
          test EBX,EBX
          je L_40c8a4
          mov EAX,DWORD PTR [EDI]
          xor EBX,EBX
          cmp EAX,-1
          je L_40c8a4
          shl EAX,6
          add EAX,DWORD PTR [L_46f1a4]
          mov DWORD PTR [ESP+4],64
          mov DWORD PTR [ESP],EAX
          call FUN_4223b0
          test EAX,EAX
          je L_40c8b0
          mov DWORD PTR [EDI],4294967295
L_40c8a4:
          add ESP,16
          mov EAX,EBX
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_40c8b0:
          mov EAX,DWORD PTR [EDI]
          mov EBX,1
          shl EAX,6
          add EAX,DWORD PTR [L_46f1a4]
          mov EDX,DWORD PTR [EAX]
          mov DWORD PTR [ESI],EDX
          mov EDX,DWORD PTR [EAX+4]
          mov DWORD PTR [ESI+4],EDX
          mov EDX,DWORD PTR [EAX+8]
          mov DWORD PTR [ESI+8],EDX
          mov EDX,DWORD PTR [EAX+12]
          mov DWORD PTR [ESI+12],EDX
          mov EDX,DWORD PTR [EAX+16]
          mov DWORD PTR [ESI+16],EDX
          mov EDX,DWORD PTR [EAX+20]
          mov DWORD PTR [ESI+20],EDX
          mov EDX,DWORD PTR [EAX+24]
          mov DWORD PTR [ESI+24],EDX
          mov EDX,DWORD PTR [EAX+28]
          mov DWORD PTR [ESI+28],EDX
          mov EDX,DWORD PTR [EAX+32]
          mov DWORD PTR [ESI+32],EDX
          mov EAX,DWORD PTR [EAX+36]
          mov DWORD PTR [ESI+36],EAX
          mov EAX,DWORD PTR [EDI]
          shl EAX,6
          add EAX,DWORD PTR [L_46f1a4]
          mov EAX,DWORD PTR [EAX+52]
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
          mov DWORD PTR [ESI+40],EAX
          add DWORD PTR [EDI],1
          add ESP,16
          mov EAX,EBX
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_40c940:
          mov EAX,DWORD PTR [L_46f190]
          test EAX,EAX
          jne L_40c950
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_40c950:
          sub ESP,44
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [EAX],0
          mov EAX,DWORD PTR [L_46f1a4]
          mov DWORD PTR [ESP+4],64
          mov DWORD PTR [ESP],EAX
          call FUN_4223b0
          test EAX,EAX
          mov EAX,DWORD PTR [ESP+52]
          je L_40c990
          mov DWORD PTR [EAX],4294967295
          xor EAX,EAX
L_40c982:
          add ESP,44
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_40c990:
          mov EAX,DWORD PTR [EAX]
          mov ECX,DWORD PTR [ESP+48]
          shl EAX,6
          add EAX,DWORD PTR [L_46f1a4]
          mov EDX,DWORD PTR [EAX]
          mov DWORD PTR [ECX],EDX
          mov EDX,DWORD PTR [EAX+4]
          mov DWORD PTR [ECX+4],EDX
          mov EDX,DWORD PTR [EAX+8]
          mov DWORD PTR [ECX+8],EDX
          mov EDX,DWORD PTR [EAX+12]
          mov DWORD PTR [ECX+12],EDX
          mov EDX,DWORD PTR [EAX+16]
          mov DWORD PTR [ECX+16],EDX
          mov EDX,DWORD PTR [EAX+20]
          mov DWORD PTR [ECX+20],EDX
          mov EDX,DWORD PTR [EAX+24]
          mov DWORD PTR [ECX+24],EDX
          mov EDX,DWORD PTR [EAX+28]
          mov DWORD PTR [ECX+28],EDX
          mov EDX,DWORD PTR [EAX+32]
          mov DWORD PTR [ECX+32],EDX
          mov EAX,DWORD PTR [EAX+36]
          mov DWORD PTR [ECX+36],EAX
          mov EAX,DWORD PTR [ESP+52]
          mov EAX,DWORD PTR [EAX]
          mov DWORD PTR [ESP+28],EAX
          shl EAX,6
          add EAX,DWORD PTR [L_46f1a4]
          mov EAX,DWORD PTR [EAX+52]
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
          mov ECX,DWORD PTR [ESP+48]
          add EAX,EDX
          mov DWORD PTR [ECX+40],EAX
          mov EAX,DWORD PTR [ESP+52]
          add DWORD PTR [EAX],1
          mov EAX,1
          jmp L_40c982
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_40ca30:
          push ESI
          push EBX
          sub ESP,36
          mov EBX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],OFFSET L_46f5c0
          mov DWORD PTR [ESP+4],EBX
          call FUN_449080
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],OFFSET L_46f1c0
          call FUN_449080
          mov EDX,OFFSET L_46f5c0
L_40ca5e:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_40ca5e
          mov ECX,EAX
          mov DWORD PTR [ESP],OFFSET L_46f5c0
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          sbb EDX,OFFSET L_46f5c3
          mov DWORD PTR [EDX+L_46f5c0],808613235
          mov DWORD PTR [EDX+L_46f5c4],808859440
          mov DWORD PTR [EDX+L_46f5c8],811544624
          mov DWORD PTR [EDX+L_46f5cc],808464432
          mov DWORD PTR [EDX+L_46f5d0],3158064
          call FUN_4225a0
          mov DWORD PTR [ESP+4],OFFSET L_45075c
          mov ESI,EAX
          mov DWORD PTR [ESP],1
          call FUN_433690
          test ESI,ESI
          je L_40cb40
L_40cae9:
          mov DWORD PTR [ESP],OFFSET L_46f194
          call FUN_405f20
          mov DWORD PTR [ESP+24],1
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],4294838225
          mov DWORD PTR [ESP+12],720896
          mov DWORD PTR [ESP+8],1398100036
          mov DWORD PTR [ESP+4],OFFSET L_46f5c0
          mov DWORD PTR [ESP],OFFSET L_46f194
          call FUN_405fa0
          test EAX,EAX
          jne L_40cc60
          add ESP,36
          pop EBX
          pop ESI
          ret 
          .byte 0x90
L_40cb40:
          mov DWORD PTR [ESP+8],OFFSET L_46f5c0
          mov DWORD PTR [ESP+4],OFFSET L_45078c
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],OFFSET L_46f5c0
          mov EBX,OFFSET L_46f5c0
          call FUN_449080
L_40cb71:
          mov EDX,DWORD PTR [EBX]
          add EBX,4
          lea EAX,DWORD PTR [EDX-16843009]
          not EDX
          and EAX,EDX
          and EAX,2155905152
          je L_40cb71
          mov EDX,EAX
          mov DWORD PTR [ESP+4],OFFSET L_46f5c0
          mov DWORD PTR [ESP],OFFSET L_46f1c0
          shr EDX,16
          test EAX,32896
          cmove EAX,EDX
          lea EDX,DWORD PTR [EBX+2]
          mov ECX,EAX
          cmove EBX,EDX
          add CL,AL
          mov EAX,12133
          sbb EBX,OFFSET L_46f5c3
          mov WORD PTR [EBX+L_46f5cc],AX
          lea EAX,DWORD PTR [EBX+15]
          mov DWORD PTR [EBX+L_46f5c0],1937330980
          mov DWORD PTR [EBX+L_46f5c4],1433232756
          mov DWORD PTR [EBX+L_46f5c8],1952539760
          mov DWORD PTR [ESP+8],EAX
          mov BYTE PTR [EBX+L_46f5ce],0
          call FUN_4490f8
          mov DWORD PTR [ESP],OFFSET L_46f5c0
          mov DWORD PTR [EBX+L_46f5ce],808613235
          mov DWORD PTR [EBX+L_46f5d2],808859440
          mov DWORD PTR [EBX+L_46f5d6],811544624
          mov DWORD PTR [EBX+L_46f5da],808464432
          mov DWORD PTR [EBX+L_46f5de],3158064
          call FUN_4225a0
          test EAX,EAX
          jne L_40cae9
          mov DWORD PTR [ESP+8],OFFSET L_46f5c0
          mov DWORD PTR [ESP+4],OFFSET L_4507c4
          mov DWORD PTR [ESP],1
          call FUN_433690
          add ESP,36
          xor EAX,EAX
          pop EBX
          pop ESI
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_40cc60:
          mov DWORD PTR [L_46f190],1
          call FUN_40c2e0
          add ESP,36
          mov EAX,1
          pop EBX
          pop ESI
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_40cc80:
          push ESI
          push EBX
          sub ESP,36
          mov EBX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],OFFSET L_46f5c0
          mov DWORD PTR [ESP+4],EBX
          call FUN_449080
          mov DWORD PTR [ESP+4],OFFSET L_46f5c0
          mov DWORD PTR [ESP],OFFSET L_46f1c0
          call FUN_449080
          mov DWORD PTR [ESP],OFFSET L_46f5c0
          call FUN_4225a0
          test EAX,EAX
          jne L_40ce94
          mov DWORD PTR [ESP],EBX
          call FUN_449078
          movzx EAX,BYTE PTR [EAX+L_46f5bf]
          cmp AL,92
          je L_40cd1c
          cmp AL,47
          je L_40cd1c
          mov EDX,OFFSET L_46f5c0
L_40ccdd:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_40ccdd
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          mov ECX,47
          sbb EDX,OFFSET L_46f5c3
          mov WORD PTR [EDX+L_46f5c0],CX
L_40cd1c:
          mov DWORD PTR [ESP+4],OFFSET L_46f5c0
          mov DWORD PTR [ESP],OFFSET L_46f1c0
          call FUN_449080
          mov EDX,OFFSET L_46f5c0
L_40cd35:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_40cd35
          mov ECX,EAX
          mov DWORD PTR [ESP],OFFSET L_46f5c0
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          sbb EDX,OFFSET L_46f5c3
          mov DWORD PTR [EDX+L_46f5c0],808613235
          mov DWORD PTR [EDX+L_46f5c4],808859440
          mov DWORD PTR [EDX+L_46f5c8],811544624
          mov DWORD PTR [EDX+L_46f5cc],808464432
          mov DWORD PTR [EDX+L_46f5d0],3158064
          call FUN_4225a0
          test EAX,EAX
          jne L_40ceb4
          mov ESI,OFFSET L_46f1c0
L_40cdb3:
          mov EDX,DWORD PTR [ESI]
          add ESI,4
          lea EAX,DWORD PTR [EDX-16843009]
          not EDX
          and EAX,EDX
          and EAX,2155905152
          je L_40cdb3
          mov EDX,EAX
          mov DWORD PTR [ESP+4],OFFSET L_46f1c0
          mov DWORD PTR [ESP],OFFSET L_46f5c0
          shr EDX,16
          test EAX,32896
          cmove EAX,EDX
          lea EDX,DWORD PTR [ESI+2]
          cmove ESI,EDX
          mov EDX,EAX
          add DL,AL
          mov EAX,12133
          sbb ESI,OFFSET L_46f1c3
          mov WORD PTR [ESI+L_46f1cc],AX
          lea EAX,DWORD PTR [ESI+15]
          mov DWORD PTR [ESI+L_46f1c0],1937330980
          mov DWORD PTR [ESI+L_46f1c4],1433232756
          mov DWORD PTR [ESI+L_46f1c8],1952539760
          mov DWORD PTR [ESP+8],EAX
          mov BYTE PTR [ESI+L_46f1ce],0
          call FUN_4490f8
          mov DWORD PTR [ESP],OFFSET L_46f5c0
          mov DWORD PTR [ESI+L_46f5ce],808613235
          mov DWORD PTR [ESI+L_46f5d2],808859440
          mov DWORD PTR [ESI+L_46f5d6],811544624
          mov DWORD PTR [ESI+L_46f5da],808464432
          mov DWORD PTR [ESI+L_46f5de],3158064
          call FUN_4225a0
          test EAX,EAX
          jne L_40ceb4
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_450850
          mov DWORD PTR [ESP],1
          call FUN_433690
          add ESP,36
          xor EAX,EAX
          pop EBX
          pop ESI
          ret 
L_40ce94:
          mov DWORD PTR [ESP+4],47
          mov DWORD PTR [ESP],OFFSET L_46f1c0
          call FUN_449058
          test EAX,EAX
          je L_40cf74
L_40ceb0:
          mov BYTE PTR [EAX+1],0
L_40ceb4:
          mov DWORD PTR [ESP+4],OFFSET L_45075c
          mov DWORD PTR [ESP],0
          call FUN_433690
          mov DWORD PTR [ESP+8],OFFSET L_46f5c0
          mov DWORD PTR [ESP+4],OFFSET L_4507fc
          mov DWORD PTR [ESP],0
          call FUN_433690
          mov DWORD PTR [ESP],OFFSET L_46f194
          call FUN_405f20
          mov DWORD PTR [ESP+24],1
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],4294838225
          mov DWORD PTR [ESP+12],720896
          mov DWORD PTR [ESP+8],1398100036
          mov DWORD PTR [ESP+4],OFFSET L_46f5c0
          mov DWORD PTR [ESP],OFFSET L_46f194
          call FUN_405fa0
          test EAX,EAX
          je L_40cf50
          mov DWORD PTR [L_46f190],1
          call FUN_40c2e0
          add ESP,36
          mov EAX,1
          pop EBX
          pop ESI
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_40cf50:
          mov DWORD PTR [ESP+8],OFFSET L_46f5c0
          mov DWORD PTR [ESP+4],OFFSET L_450820
          mov DWORD PTR [ESP],0
          call FUN_433690
          add ESP,36
          xor EAX,EAX
          pop EBX
          pop ESI
          ret 
L_40cf74:
          mov DWORD PTR [ESP+4],92
          mov DWORD PTR [ESP],OFFSET L_46f1c0
          call FUN_449058
          test EAX,EAX
          je L_40ceb4
          jmp L_40ceb0
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
FUN_40cfa0:
          sub ESP,28
          mov EAX,DWORD PTR [L_46f18c]
          mov DWORD PTR [L_46f184],0
          mov DWORD PTR [L_46f180],0
          test EAX,EAX
          je L_40cfd2
          mov DWORD PTR [ESP],EAX
          call FUN_449140
          mov DWORD PTR [L_46f18c],0
L_40cfd2:
          mov EAX,DWORD PTR [L_46f188]
          test EAX,EAX
          je L_40cfed
          mov DWORD PTR [ESP],EAX
          call FUN_449140
          mov DWORD PTR [L_46f188],0
L_40cfed:
          mov DWORD PTR [ESP],OFFSET L_46f194
          mov DWORD PTR [L_46f190],0
          call FUN_405f50
          add ESP,28
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

.section .rdata,"dr"
.p2align 2
L_45066c:
          .string "xboxupd.bin"
L_450678:
          .string "extracted SUPD/xboxupd.bin (0x%x bytes)\n"
          .zero 3
L_4506a4:
          .string "decrypting SUPD/xboxupd.bin/%c%c_%d.bin (0x%x bytes)..."
L_4506dc:
          .string "done!\n"
L_4506e3:
          .string "failed!\n"
L_4506ec:
          .string "***** ERROR: xboxupd.bin not found in SU container!\n"
          .zero 3
L_450724:
          .string "extracted SUPD/xboxupd.bin/%c%c_%d.bin (0x%x bytes)\n"
          .zero 3
L_45075c:
          .string "\n------ loading system update container ------\n"
L_45078c:
          .string "system update container not found at %s, trying alt\n"
          .zero 3
L_4507c4:
          .string "system update container not found at %s, skipping load\n"
L_4507fc:
          .string "SU container found! Loading '%s'\n"
          .zero 2
L_450820:
          .string "\n***** ERROR could not load container '%s'!\n"
          .zero 3
L_450850:
          .string "system update container not found at or near %s!!\n"
          .zero 1

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
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_40c240 - .
          .byte 0x15
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
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_40c260 - .
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
          .byte 0x44
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_40c280 - .
          .byte 0x51
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x2
          .byte 0x4d
          .byte 0xe
          .byte 0x4
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x5c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_40c2e0 - .
          .byte 0x70
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
          .byte 0x2
          .byte 0x6b
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
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x9c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_40c650 - .
          .byte 0xa3
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x61
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x46
          .byte 0xe
          .byte 0x30
          .byte 0x2
          .byte 0x73
          .byte 0xe
          .byte 0x8
          .byte 0x46
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_40c700 - .
          .byte 0xa3
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x61
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x46
          .byte 0xe
          .byte 0x30
          .byte 0x2
          .byte 0x73
          .byte 0xe
          .byte 0x8
          .byte 0x46
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xe4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_40c7b0 - .
          .byte 0xb0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x51
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x43
          .byte 0xe
          .byte 0x50
          .byte 0x72
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x49
          .byte 0xb
          .byte 0x0
          .byte 0x44
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_40c860 - .
          .byte 0xda
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
          .byte 0x20
          .byte 0x2
          .byte 0x41
          .byte 0xa
          .byte 0xe
          .byte 0x10
          .byte 0x43
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
          .byte 0x44
          .byte 0xb
          .byte 0x2
          .byte 0x84
          .byte 0xe
          .byte 0x10
          .byte 0x43
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
          .byte 0x0
          .byte 0x18
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x50
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_40c940 - .
          .byte 0xea
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x53
          .byte 0xe
          .byte 0x30
          .byte 0x72
          .byte 0xa
          .byte 0xe
          .byte 0x4
          .byte 0x4b
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x48
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x6c
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_40ca30 - .
          .byte 0x4a
          .byte 0x2
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
          .byte 0x3
          .byte 0x7
          .byte 0x1
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
          .byte 0x3
          .byte 0x15
          .byte 0x1
          .byte 0xa
          .byte 0xe
          .byte 0xc
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x47
          .byte 0xb
          .byte 0x52
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
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x48
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb8
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_40cc80 - .
          .byte 0x15
          .byte 0x3
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
          .byte 0x3
          .byte 0xa
          .byte 0x2
          .byte 0xa
          .byte 0xe
          .byte 0xc
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x2
          .byte 0xae
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
          .byte 0x47
          .byte 0xb
          .byte 0x5f
          .byte 0xa
          .byte 0xe
          .byte 0xc
          .byte 0x43
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
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x4
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long FUN_40cfa0 - .
          .byte 0x67
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x2
          .byte 0x63
          .byte 0xe
          .byte 0x4

.bss
.p2align 5
L_46f180:
          .zero 4
L_46f184:
          .zero 4
L_46f188:
          .zero 4
L_46f18c:
          .zero 4
L_46f190:
          .zero 4
L_46f194:
          .zero 16
L_46f1a4:
          .zero 28
L_46f1c0:
          .zero 3
L_46f1c3:
          .zero 1
L_46f1c4:
          .zero 4
L_46f1c8:
          .zero 4
L_46f1cc:
          .zero 2
L_46f1ce:
          .zero 1009
L_46f5bf:
          .zero 1
L_46f5c0:
          .zero 3
L_46f5c3:
          .zero 1
L_46f5c4:
          .zero 4
L_46f5c8:
          .zero 4
L_46f5cc:
          .zero 2
L_46f5ce:
          .zero 2
L_46f5d0:
          .zero 2
L_46f5d2:
          .zero 4
L_46f5d6:
          .zero 4
L_46f5da:
          .zero 4
L_46f5de:
          .zero 994

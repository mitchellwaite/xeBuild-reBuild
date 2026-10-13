# crypto/aes_modes.s -- Gladman AES: ECB/CBC over the block functions
#
# original placement:
#   .eh_frame      0046c344-0046c630
#   .rdata$zzz     00463c1c-00463c48
#   .text          00438b00-00439eb0

.intel_syntax noprefix
.globl L_438bc0
.globl L_438c30
.globl L_438ca0
.globl L_438e20

.text
.p2align 4
L_438b00:
          push EBP
          push EDI
          mov EAX,1
          push ESI
          push EBX
          sub ESP,24
          mov ESI,DWORD PTR [ESP+44]
          lea EDX,DWORD PTR [ESI-4]
          cmp EDX,12
          ja L_438b82
          xor EBP,EBP
          lea EDI,DWORD PTR [ESI-1]
          lea EBX,DWORD PTR [ESP+8]
          mov DWORD PTR [ESP+4],0
          xor ECX,ECX
          mov DWORD PTR [ESP],EBP
          jmp L_438b44
L_438b30:
          add EDX,ESI
          cmp EAX,EDX
          jne L_438b90
          add ECX,1
          add DWORD PTR [ESP],1
          add EBX,1
          cmp ESI,ECX
          je L_438b73
L_438b44:
          mov EAX,EBX
          mov EDX,ECX
          lea EBP,DWORD PTR [ESP+8]
          and EAX,EDI
          sub EDX,EAX
          lea EAX,DWORD PTR [ESP+8]
          add EDX,EAX
          mov EAX,EBX
          neg EAX
          and EAX,EDI
          add EAX,ECX
          add EAX,EBP
          cmp EDX,EAX
          jne L_438b30
          add ECX,1
          add DWORD PTR [ESP+4],1
          add EBX,1
          cmp ESI,ECX
          jne L_438b44
L_438b73:
          cmp DWORD PTR [ESP+4],1
          mov EBP,DWORD PTR [ESP]
          mov EAX,1
          je L_438ba0
L_438b82:
          add ESP,24
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
L_438b90:
          add ESP,24
          mov EAX,1
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_438ba0:
          xor EAX,EAX
          cmp EBP,EDI
          setne AL
          add ESP,24
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x90
L_438bb0:
          mov EAX,DWORD PTR [ESP+4]
          mov BYTE PTR [EAX+242],0
          xor EAX,EAX
          ret 
          .byte 0x66
          .byte 0x90
L_438bc0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov EBX,DWORD PTR [ESP+72]
          mov ESI,DWORD PTR [ESP+64]
          mov EBP,DWORD PTR [ESP+68]
          mov EDI,DWORD PTR [ESP+76]
          mov EAX,EBX
          and EAX,15
          mov DWORD PTR [ESP+28],EAX
          jne L_438c0f
          sar EBX,4
          test EBX,EBX
          jne L_438bfb
          jmp L_438c17
          nop
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_438bf0:
          add ESI,16
          add EBP,16
          sub EBX,1
          je L_438c17
L_438bfb:
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],ESI
          call FUN_439ec0
          test EAX,EAX
          je L_438bf0
L_438c0f:
          mov DWORD PTR [ESP+28],1
L_438c17:
          mov EAX,DWORD PTR [ESP+28]
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
          .byte 0xbc
          .byte 0x27
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_438c30:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov EBX,DWORD PTR [ESP+72]
          mov ESI,DWORD PTR [ESP+64]
          mov EBP,DWORD PTR [ESP+68]
          mov EDI,DWORD PTR [ESP+76]
          mov EAX,EBX
          and EAX,15
          mov DWORD PTR [ESP+28],EAX
          jne L_438c7f
          sar EBX,4
          test EBX,EBX
          jne L_438c6b
          jmp L_438c87
          nop
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_438c60:
          add ESI,16
          add EBP,16
          sub EBX,1
          je L_438c87
L_438c6b:
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],ESI
          call FUN_43aca0
          test EAX,EAX
          je L_438c60
L_438c7f:
          mov DWORD PTR [ESP+28],1
L_438c87:
          mov EAX,DWORD PTR [ESP+28]
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
          .byte 0xbc
          .byte 0x27
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_438ca0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov EBP,DWORD PTR [ESP+72]
          mov ESI,DWORD PTR [ESP+64]
          mov EDI,DWORD PTR [ESP+68]
          mov EBX,DWORD PTR [ESP+76]
          mov EAX,EBP
          and EAX,15
          mov DWORD PTR [ESP+28],EAX
          jne L_438d32
          mov EAX,EBX
          sar EBP,4
          or EAX,ESI
          test AL,3
          .byte 0x0f,0x85; .long L_438d50-.-4   # jne L_438d50
          test EBP,EBP
          je L_438d3a
          mov DWORD PTR [ESP+24],EBP
          jmp L_438d04
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_438ce0:
          mov ECX,DWORD PTR [EBX+4]
          mov EDX,DWORD PTR [EBX+8]
          add ESI,16
          mov EAX,DWORD PTR [EBX+12]
          mov EBP,DWORD PTR [EBX]
          add EDI,16
          mov DWORD PTR [EDI-12],ECX
          mov DWORD PTR [EDI-8],EDX
          mov DWORD PTR [EDI-16],EBP
          mov DWORD PTR [EDI-4],EAX
          sub DWORD PTR [ESP+24],1
          je L_438d3a
L_438d04:
          mov EAX,DWORD PTR [ESI]
          xor DWORD PTR [EBX],EAX
          mov EAX,DWORD PTR [ESI+4]
          xor DWORD PTR [EBX+4],EAX
          mov EAX,DWORD PTR [ESI+8]
          xor DWORD PTR [EBX+8],EAX
          mov EAX,DWORD PTR [ESI+12]
          xor DWORD PTR [EBX+12],EAX
          mov EAX,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],EAX
          call FUN_439ec0
          test EAX,EAX
          je L_438ce0
L_438d32:
          mov DWORD PTR [ESP+28],1
L_438d3a:
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
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_438d50:
          test EBP,EBP
          je L_438d3a
          mov DWORD PTR [ESP+24],EBP
          jmp L_438d84
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_438d60:
          mov ECX,DWORD PTR [EBX+4]
          mov EDX,DWORD PTR [EBX+8]
          add ESI,16
          mov EAX,DWORD PTR [EBX+12]
          mov EBP,DWORD PTR [EBX]
          add EDI,16
          mov DWORD PTR [EDI-12],ECX
          mov DWORD PTR [EDI-8],EDX
          mov DWORD PTR [EDI-16],EBP
          mov DWORD PTR [EDI-4],EAX
          sub DWORD PTR [ESP+24],1
          je L_438d3a
L_438d84:
          movzx EAX,BYTE PTR [ESI]
          xor BYTE PTR [EBX],AL
          movzx EAX,BYTE PTR [ESI+1]
          xor BYTE PTR [EBX+1],AL
          movzx EAX,BYTE PTR [ESI+2]
          xor BYTE PTR [EBX+2],AL
          movzx EAX,BYTE PTR [ESI+3]
          xor BYTE PTR [EBX+3],AL
          movzx EAX,BYTE PTR [ESI+4]
          xor BYTE PTR [EBX+4],AL
          movzx EAX,BYTE PTR [ESI+5]
          xor BYTE PTR [EBX+5],AL
          movzx EAX,BYTE PTR [ESI+6]
          xor BYTE PTR [EBX+6],AL
          movzx EAX,BYTE PTR [ESI+7]
          xor BYTE PTR [EBX+7],AL
          movzx EAX,BYTE PTR [ESI+8]
          xor BYTE PTR [EBX+8],AL
          movzx EAX,BYTE PTR [ESI+9]
          xor BYTE PTR [EBX+9],AL
          movzx EAX,BYTE PTR [ESI+10]
          xor BYTE PTR [EBX+10],AL
          movzx EAX,BYTE PTR [ESI+11]
          xor BYTE PTR [EBX+11],AL
          movzx EAX,BYTE PTR [ESI+12]
          xor BYTE PTR [EBX+12],AL
          movzx EAX,BYTE PTR [ESI+13]
          xor BYTE PTR [EBX+13],AL
          movzx EAX,BYTE PTR [ESI+14]
          xor BYTE PTR [EBX+14],AL
          movzx EAX,BYTE PTR [ESI+15]
          xor BYTE PTR [EBX+15],AL
          mov EAX,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],EAX
          call FUN_439ec0
          test EAX,EAX
          je L_438d60
          jmp L_438d32
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
L_438e20:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,60
          mov EAX,DWORD PTR [ESP+88]
          mov ESI,DWORD PTR [ESP+80]
          mov EDI,DWORD PTR [ESP+84]
          mov EBP,DWORD PTR [ESP+92]
          mov EDX,EAX
          and EDX,15
          mov DWORD PTR [ESP+44],EDX
          jne L_438ed0
          mov EBX,EBP
          sar EAX,4
          or EBX,EDI
          and EBX,3
          jne L_438ee4
          test EAX,EAX
          je L_438ed8
          mov EBX,ESI
          mov DWORD PTR [ESP+40],EAX
          mov ESI,EBP
          jmp L_438e9e
L_438e64:
          mov EAX,DWORD PTR [ESI]
          xor DWORD PTR [EDI],EAX
          add EBX,16
          mov EAX,DWORD PTR [ESI+4]
          xor DWORD PTR [EDI+4],EAX
          mov EAX,DWORD PTR [ESI+8]
          xor DWORD PTR [EDI+8],EAX
          mov EAX,DWORD PTR [ESI+12]
          xor DWORD PTR [EDI+12],EAX
          add EDI,16
          sub DWORD PTR [ESP+40],1
          mov EAX,DWORD PTR [ESP+28]
          mov EDX,DWORD PTR [ESP+32]
          mov ECX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESI],EBP
          mov DWORD PTR [ESI+4],EAX
          mov DWORD PTR [ESI+8],EDX
          mov DWORD PTR [ESI+12],ECX
          je L_438ed8
L_438e9e:
          mov EAX,DWORD PTR [EBX+4]
          mov EDX,DWORD PTR [EBX+8]
          mov ECX,DWORD PTR [EBX+12]
          mov EBP,DWORD PTR [EBX]
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+28],EAX
          mov EAX,DWORD PTR [ESP+96]
          mov DWORD PTR [ESP+32],EDX
          mov DWORD PTR [ESP+36],ECX
          mov DWORD PTR [ESP+8],EAX
          call FUN_43aca0
          test EAX,EAX
          je L_438e64
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
L_438ed0:
          mov DWORD PTR [ESP+44],1
L_438ed8:
          mov EAX,DWORD PTR [ESP+44]
          add ESP,60
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_438ee4:
          test EAX,EAX
          mov EBX,ESI
          mov DWORD PTR [ESP+40],EAX
          mov ESI,EBP
          jne L_438f96
          jmp L_438ed8
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_438f00:
          movzx EAX,BYTE PTR [ESI]
          add EBX,16
          xor BYTE PTR [EDI],AL
          movzx EAX,BYTE PTR [ESI+1]
          xor BYTE PTR [EDI+1],AL
          movzx EAX,BYTE PTR [ESI+2]
          xor BYTE PTR [EDI+2],AL
          movzx EAX,BYTE PTR [ESI+3]
          xor BYTE PTR [EDI+3],AL
          movzx EAX,BYTE PTR [ESI+4]
          xor BYTE PTR [EDI+4],AL
          movzx EAX,BYTE PTR [ESI+5]
          xor BYTE PTR [EDI+5],AL
          movzx EAX,BYTE PTR [ESI+6]
          xor BYTE PTR [EDI+6],AL
          movzx EAX,BYTE PTR [ESI+7]
          xor BYTE PTR [EDI+7],AL
          movzx EAX,BYTE PTR [ESI+8]
          xor BYTE PTR [EDI+8],AL
          movzx EAX,BYTE PTR [ESI+9]
          xor BYTE PTR [EDI+9],AL
          movzx EAX,BYTE PTR [ESI+10]
          xor BYTE PTR [EDI+10],AL
          movzx EAX,BYTE PTR [ESI+11]
          xor BYTE PTR [EDI+11],AL
          movzx EAX,BYTE PTR [ESI+12]
          xor BYTE PTR [EDI+12],AL
          movzx EAX,BYTE PTR [ESI+13]
          xor BYTE PTR [EDI+13],AL
          movzx EAX,BYTE PTR [ESI+14]
          xor BYTE PTR [EDI+14],AL
          movzx EAX,BYTE PTR [ESI+15]
          xor BYTE PTR [EDI+15],AL
          add EDI,16
          sub DWORD PTR [ESP+40],1
          mov EAX,DWORD PTR [ESP+28]
          mov EDX,DWORD PTR [ESP+32]
          mov ECX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESI],EBP
          mov DWORD PTR [ESI+4],EAX
          mov DWORD PTR [ESI+8],EDX
          mov DWORD PTR [ESI+12],ECX
          je L_438ed8
L_438f96:
          mov EAX,DWORD PTR [EBX+4]
          mov EDX,DWORD PTR [EBX+8]
          mov ECX,DWORD PTR [EBX+12]
          mov EBP,DWORD PTR [EBX]
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+28],EAX
          mov EAX,DWORD PTR [ESP+96]
          mov DWORD PTR [ESP+32],EDX
          mov DWORD PTR [ESP+36],ECX
          mov DWORD PTR [ESP+8],EAX
          call FUN_43aca0
          test EAX,EAX
          je L_438f00
          jmp L_438ed0
          .byte 0x66
          .byte 0x90
L_438fd0:
          push EBP
          push EDI
          push ESI
          push EBX
          xor EBX,EBX
          sub ESP,44
          mov EAX,DWORD PTR [ESP+80]
          mov ESI,DWORD PTR [ESP+64]
          mov EDI,DWORD PTR [ESP+68]
          mov ECX,DWORD PTR [ESP+72]
          mov EDX,DWORD PTR [ESP+76]
          movzx EBP,BYTE PTR [EAX+242]
          test EBP,EBP
          je L_43903f
          test ECX,ECX
          mov EBX,EBP
          jle L_4392d4
          cmp EBP,15
          jg L_4392d4
          xor EBP,EBP
          jmp L_439014
          .byte 0x90
L_439010:
          cmp ECX,EBP
          jle L_439034
L_439014:
          add ESI,1
          add EBX,1
          movzx EAX,BYTE PTR [ESI-1]
          xor AL,BYTE PTR [EDX+EBX*1-1]
          add EDI,1
          add EBP,1
          cmp EBX,15
          mov BYTE PTR [EDX+EBX*1-1],AL
          mov BYTE PTR [EDI-1],AL
          jle L_439010
L_439034:
          cmp EBX,16
          mov EAX,0
          cmove EBX,EAX
L_43903f:
          mov EAX,ECX
          sub EAX,EBP
          sar EAX,4
          test EAX,EAX
          je L_439109
          mov EAX,ESI
          or EAX,EDI
          test AL,3
          lea EAX,DWORD PTR [EBP+15]
          jne L_439197
          test DL,3
          jne L_439197
          cmp ECX,EAX
          jle L_439109
          lea EAX,DWORD PTR [ECX-16]
          mov DWORD PTR [ESP+68],EDI
          mov DWORD PTR [ESP+28],EBX
          mov EDI,EBP
          mov DWORD PTR [ESP+72],ECX
          mov EBX,EDX
          sub EAX,EBP
          and EAX,4294967280
          lea EAX,DWORD PTR [EBP+EAX*1+16]
          mov EBP,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+24],EAX
          jmp L_4390d0
L_439094:
          mov EAX,DWORD PTR [EBX]
          xor EAX,DWORD PTR [ESI]
          add EBP,16
          add ESI,16
          add EDI,16
          mov DWORD PTR [EBX],EAX
          mov DWORD PTR [EBP-16],EAX
          mov EAX,DWORD PTR [EBX+4]
          xor EAX,DWORD PTR [ESI-12]
          mov DWORD PTR [EBX+4],EAX
          mov DWORD PTR [EBP-12],EAX
          mov EAX,DWORD PTR [EBX+8]
          xor EAX,DWORD PTR [ESI-8]
          mov DWORD PTR [EBX+8],EAX
          mov DWORD PTR [EBP-8],EAX
          mov EAX,DWORD PTR [EBX+12]
          xor EAX,DWORD PTR [ESI-4]
          mov DWORD PTR [EBX+12],EAX
          mov DWORD PTR [EBP-4],EAX
          cmp EDI,DWORD PTR [ESP+24]
          je L_4390f5
L_4390d0:
          mov EAX,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],EAX
          call FUN_439ec0
          test EAX,EAX
          je L_439094
L_4390e8:
          add ESP,44
          mov EAX,1
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_4390f5:
          mov DWORD PTR [ESP+68],EBP
          mov EDX,EBX
          mov EBP,EDI
          mov ECX,DWORD PTR [ESP+72]
          mov EBX,DWORD PTR [ESP+28]
          mov EDI,DWORD PTR [ESP+68]
L_439109:
          cmp ECX,EBP
          jle L_43914f
          mov EAX,EBX
          mov EBX,EDX
L_439111:
          test EAX,EAX
          je L_43916b
          cmp EAX,15
          jg L_439144
          cmp ECX,EBP
          jg L_439125
          jmp L_439144
L_439120:
          cmp EAX,15
          jg L_439144
L_439125:
          add ESI,1
          add EAX,1
          movzx EDX,BYTE PTR [ESI-1]
          xor DL,BYTE PTR [EBX+EAX*1-1]
          add EBP,1
          add EDI,1
          cmp ECX,EBP
          mov BYTE PTR [EBX+EAX*1-1],DL
          mov BYTE PTR [EDI-1],DL
          jg L_439120
L_439144:
          cmp EAX,16
          je L_439163
          cmp ECX,EBP
          jg L_439111
          mov EBX,EAX
L_43914f:
          mov EAX,DWORD PTR [ESP+80]
          mov BYTE PTR [EAX+242],BL
          add ESP,44
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_439163:
          cmp ECX,EBP
          jle L_4392cd
L_43916b:
          mov EAX,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+24],ECX
          mov DWORD PTR [ESP+8],EAX
          call FUN_439ec0
          test EAX,EAX
          mov ECX,DWORD PTR [ESP+24]
          jne L_4390e8
          cmp ECX,EBP
          jg L_439125
          mov EBX,EAX
          jmp L_43914f
L_439197:
          cmp ECX,EAX
          jle L_439109
          lea EAX,DWORD PTR [ECX-16]
          mov DWORD PTR [ESP+28],EBX
          mov DWORD PTR [ESP+72],ECX
          mov EBX,EDX
          sub EAX,EBP
          and EAX,4294967280
          lea EAX,DWORD PTR [EBP+EAX*1+16]
          mov DWORD PTR [ESP+24],EAX
          jmp L_43929d
          .byte 0x66
          .byte 0x90
L_4391c0:
          movzx EAX,BYTE PTR [EBX]
          add ESI,16
          add EDI,16
          xor AL,BYTE PTR [ESI-16]
          add EBP,16
          mov BYTE PTR [EBX],AL
          mov BYTE PTR [EDI-16],AL
          movzx EAX,BYTE PTR [EBX+1]
          xor AL,BYTE PTR [ESI-15]
          mov BYTE PTR [EBX+1],AL
          mov BYTE PTR [EDI-15],AL
          movzx EAX,BYTE PTR [EBX+2]
          xor AL,BYTE PTR [ESI-14]
          mov BYTE PTR [EBX+2],AL
          mov BYTE PTR [EDI-14],AL
          movzx EAX,BYTE PTR [EBX+3]
          xor AL,BYTE PTR [ESI-13]
          mov BYTE PTR [EBX+3],AL
          mov BYTE PTR [EDI-13],AL
          movzx EAX,BYTE PTR [EBX+4]
          xor AL,BYTE PTR [ESI-12]
          mov BYTE PTR [EBX+4],AL
          mov BYTE PTR [EDI-12],AL
          movzx EAX,BYTE PTR [EBX+5]
          xor AL,BYTE PTR [ESI-11]
          mov BYTE PTR [EBX+5],AL
          mov BYTE PTR [EDI-11],AL
          movzx EAX,BYTE PTR [EBX+6]
          xor AL,BYTE PTR [ESI-10]
          mov BYTE PTR [EBX+6],AL
          mov BYTE PTR [EDI-10],AL
          movzx EAX,BYTE PTR [EBX+7]
          xor AL,BYTE PTR [ESI-9]
          mov BYTE PTR [EBX+7],AL
          mov BYTE PTR [EDI-9],AL
          movzx EAX,BYTE PTR [EBX+8]
          xor AL,BYTE PTR [ESI-8]
          mov BYTE PTR [EBX+8],AL
          mov BYTE PTR [EDI-8],AL
          movzx EAX,BYTE PTR [EBX+9]
          xor AL,BYTE PTR [ESI-7]
          mov BYTE PTR [EBX+9],AL
          mov BYTE PTR [EDI-7],AL
          movzx EAX,BYTE PTR [EBX+10]
          xor AL,BYTE PTR [ESI-6]
          mov BYTE PTR [EBX+10],AL
          mov BYTE PTR [EDI-6],AL
          movzx EAX,BYTE PTR [EBX+11]
          xor AL,BYTE PTR [ESI-5]
          mov BYTE PTR [EBX+11],AL
          mov BYTE PTR [EDI-5],AL
          movzx EAX,BYTE PTR [EBX+12]
          xor AL,BYTE PTR [ESI-4]
          mov BYTE PTR [EBX+12],AL
          mov BYTE PTR [EDI-4],AL
          movzx EAX,BYTE PTR [EBX+13]
          xor AL,BYTE PTR [ESI-3]
          mov BYTE PTR [EBX+13],AL
          mov BYTE PTR [EDI-3],AL
          movzx EAX,BYTE PTR [EBX+14]
          xor AL,BYTE PTR [ESI-2]
          mov BYTE PTR [EBX+14],AL
          mov BYTE PTR [EDI-2],AL
          movzx EAX,BYTE PTR [EBX+15]
          xor AL,BYTE PTR [ESI-1]
          mov BYTE PTR [EBX+15],AL
          mov BYTE PTR [EDI-1],AL
          cmp EBP,DWORD PTR [ESP+24]
          je L_4392be
L_43929d:
          mov EAX,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],EAX
          call FUN_439ec0
          test EAX,EAX
          je L_4391c0
          jmp L_4390e8
L_4392be:
          mov EDX,EBX
          mov ECX,DWORD PTR [ESP+72]
          mov EBX,DWORD PTR [ESP+28]
          jmp L_439109
L_4392cd:
          xor EBX,EBX
          jmp L_43914f
L_4392d4:
          xor EBP,EBP
          jmp L_439034
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_4392e0:
          push EBP
          push EDI
          push ESI
          push EBX
          xor EBX,EBX
          sub ESP,44
          mov EAX,DWORD PTR [ESP+80]
          mov ESI,DWORD PTR [ESP+64]
          mov EDI,DWORD PTR [ESP+68]
          mov EDX,DWORD PTR [ESP+76]
          movzx EBP,BYTE PTR [EAX+242]
          test EBP,EBP
          je L_439352
          mov EAX,DWORD PTR [ESP+72]
          mov EBX,EBP
          test EAX,EAX
          jle L_43960d
          cmp EBP,15
          jg L_43960d
          xor EBP,EBP
          jmp L_439326
          .byte 0x90
L_439320:
          cmp DWORD PTR [ESP+72],EBP
          jle L_439347
L_439326:
          add ESI,1
          movzx EAX,BYTE PTR [ESI-1]
          add EDI,1
          add EBP,1
          mov ECX,EAX
          xor CL,BYTE PTR [EDX+EBX*1]
          add EBX,1
          cmp EBX,15
          mov BYTE PTR [EDI-1],CL
          mov BYTE PTR [EDX+EBX*1-1],AL
          jle L_439320
L_439347:
          cmp EBX,16
          mov EAX,0
          cmove EBX,EAX
L_439352:
          mov EAX,DWORD PTR [ESP+72]
          sub EAX,EBP
          sar EAX,4
          test EAX,EAX
          je L_439410
          mov EAX,ESI
          or EAX,EDI
          test AL,3
          lea EAX,DWORD PTR [EBP+15]
          jne L_4394b0
          test DL,3
          jne L_4394b0
          cmp DWORD PTR [ESP+72],EAX
          jle L_439410
          mov EAX,DWORD PTR [ESP+72]
          mov DWORD PTR [ESP+28],EBX
          mov EBX,EDX
          sub EAX,16
          sub EAX,EBP
          and EAX,4294967280
          lea EAX,DWORD PTR [EBP+EAX*1+16]
          mov DWORD PTR [ESP+24],EAX
          jmp L_4393e5
L_4393a1:
          mov EAX,DWORD PTR [ESI]
          mov ECX,DWORD PTR [EBX]
          add ESI,16
          add EDI,16
          add EBP,16
          xor ECX,EAX
          mov DWORD PTR [EDI-16],ECX
          mov DWORD PTR [EBX],EAX
          mov ECX,DWORD PTR [EBX+4]
          mov EAX,DWORD PTR [ESI-12]
          xor ECX,EAX
          mov DWORD PTR [EDI-12],ECX
          mov DWORD PTR [EBX+4],EAX
          mov ECX,DWORD PTR [EBX+8]
          mov EAX,DWORD PTR [ESI-8]
          xor ECX,EAX
          mov DWORD PTR [EDI-8],ECX
          mov DWORD PTR [EBX+8],EAX
          mov ECX,DWORD PTR [EBX+12]
          mov EAX,DWORD PTR [ESI-4]
          xor ECX,EAX
          mov DWORD PTR [EDI-4],ECX
          cmp EBP,DWORD PTR [ESP+24]
          mov DWORD PTR [EBX+12],EAX
          je L_43940a
L_4393e5:
          mov EAX,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],EAX
          call FUN_439ec0
          test EAX,EAX
          je L_4393a1
L_4393fd:
          mov EAX,1
L_439402:
          add ESP,44
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_43940a:
          mov EDX,EBX
          mov EBX,DWORD PTR [ESP+28]
L_439410:
          cmp DWORD PTR [ESP+72],EBP
          jle L_439465
          mov EAX,EBX
          mov EBX,EDX
          .byte 0x8d,0xb6,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_439420:
          test EAX,EAX
          je L_43948a
          cmp EAX,15
          jg L_439458
          cmp DWORD PTR [ESP+72],EBP
          jg L_439436
          jmp L_439458
L_439431:
          cmp EAX,15
          jg L_439458
L_439436:
          add ESI,1
          movzx EDX,BYTE PTR [ESI-1]
          add EDI,1
          add EBP,1
          mov ECX,EDX
          xor CL,BYTE PTR [EBX+EAX*1]
          add EAX,1
          cmp DWORD PTR [ESP+72],EBP
          mov BYTE PTR [EDI-1],CL
          mov BYTE PTR [EBX+EAX*1-1],DL
          jg L_439431
L_439458:
          cmp EAX,16
          je L_439480
          cmp DWORD PTR [ESP+72],EBP
          jg L_439420
          mov EBX,EAX
L_439465:
          mov EAX,DWORD PTR [ESP+80]
          mov BYTE PTR [EAX+242],BL
          add ESP,44
          xor EAX,EAX
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
L_439480:
          cmp DWORD PTR [ESP+72],EBP
          jle L_439606
L_43948a:
          mov EAX,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],EAX
          call FUN_439ec0
          test EAX,EAX
          jne L_4393fd
          cmp DWORD PTR [ESP+72],EBP
          jg L_439436
          mov EBX,EAX
          jmp L_439465
L_4394b0:
          cmp DWORD PTR [ESP+72],EAX
          jle L_439410
          mov EAX,DWORD PTR [ESP+72]
          mov DWORD PTR [ESP+28],EBX
          mov EBX,EDX
          sub EAX,16
          sub EAX,EBP
          and EAX,4294967280
          lea EAX,DWORD PTR [EBP+EAX*1+16]
          mov DWORD PTR [ESP+24],EAX
          jmp L_4395e0
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4394e0:
          movzx EAX,BYTE PTR [ESI]
          add EDI,16
          add ESI,16
          add EBP,16
          mov ECX,EAX
          xor CL,BYTE PTR [EBX]
          mov BYTE PTR [EDI-16],CL
          mov BYTE PTR [EBX],AL
          movzx EAX,BYTE PTR [ESI-15]
          mov ECX,EAX
          xor CL,BYTE PTR [EBX+1]
          mov BYTE PTR [EDI-15],CL
          mov BYTE PTR [EBX+1],AL
          movzx EAX,BYTE PTR [ESI-14]
          mov ECX,EAX
          xor CL,BYTE PTR [EBX+2]
          mov BYTE PTR [EDI-14],CL
          mov BYTE PTR [EBX+2],AL
          movzx EAX,BYTE PTR [ESI-13]
          mov ECX,EAX
          xor CL,BYTE PTR [EBX+3]
          mov BYTE PTR [EDI-13],CL
          mov BYTE PTR [EBX+3],AL
          movzx EAX,BYTE PTR [ESI-12]
          mov ECX,EAX
          xor CL,BYTE PTR [EBX+4]
          mov BYTE PTR [EDI-12],CL
          mov BYTE PTR [EBX+4],AL
          movzx EAX,BYTE PTR [ESI-11]
          mov ECX,EAX
          xor CL,BYTE PTR [EBX+5]
          mov BYTE PTR [EDI-11],CL
          mov BYTE PTR [EBX+5],AL
          movzx EAX,BYTE PTR [ESI-10]
          mov ECX,EAX
          xor CL,BYTE PTR [EBX+6]
          mov BYTE PTR [EDI-10],CL
          mov BYTE PTR [EBX+6],AL
          movzx EAX,BYTE PTR [ESI-9]
          mov ECX,EAX
          xor CL,BYTE PTR [EBX+7]
          mov BYTE PTR [EDI-9],CL
          mov BYTE PTR [EBX+7],AL
          movzx EAX,BYTE PTR [ESI-8]
          mov ECX,EAX
          xor CL,BYTE PTR [EBX+8]
          mov BYTE PTR [EDI-8],CL
          mov BYTE PTR [EBX+8],AL
          movzx EAX,BYTE PTR [ESI-7]
          mov ECX,EAX
          xor CL,BYTE PTR [EBX+9]
          mov BYTE PTR [EDI-7],CL
          mov BYTE PTR [EBX+9],AL
          movzx EAX,BYTE PTR [ESI-6]
          mov ECX,EAX
          xor CL,BYTE PTR [EBX+10]
          mov BYTE PTR [EDI-6],CL
          mov BYTE PTR [EBX+10],AL
          movzx EAX,BYTE PTR [ESI-5]
          mov ECX,EAX
          xor CL,BYTE PTR [EBX+11]
          mov BYTE PTR [EDI-5],CL
          mov BYTE PTR [EBX+11],AL
          movzx EAX,BYTE PTR [ESI-4]
          mov ECX,EAX
          xor CL,BYTE PTR [EBX+12]
          mov BYTE PTR [EDI-4],CL
          mov BYTE PTR [EBX+12],AL
          movzx EAX,BYTE PTR [ESI-3]
          mov ECX,EAX
          xor CL,BYTE PTR [EBX+13]
          mov BYTE PTR [EDI-3],CL
          mov BYTE PTR [EBX+13],AL
          movzx EAX,BYTE PTR [ESI-2]
          mov ECX,EAX
          xor CL,BYTE PTR [EBX+14]
          mov BYTE PTR [EDI-2],CL
          mov BYTE PTR [EBX+14],AL
          movzx EAX,BYTE PTR [ESI-1]
          mov ECX,EAX
          xor CL,BYTE PTR [EBX+15]
          mov BYTE PTR [EDI-1],CL
          mov BYTE PTR [EBX+15],AL
          cmp EBP,DWORD PTR [ESP+24]
          je L_43940a
L_4395e0:
          mov EAX,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],EAX
          call FUN_439ec0
          test EAX,EAX
          je L_4394e0
          mov EAX,1
          jmp L_439402
L_439606:
          xor EBX,EBX
          jmp L_439465
L_43960d:
          xor EBP,EBP
          jmp L_439347
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
L_439620:
          push EBP
          push EDI
          push ESI
          push EBX
          xor EBX,EBX
          sub ESP,44
          mov EAX,DWORD PTR [ESP+80]
          mov ESI,DWORD PTR [ESP+64]
          mov EDI,DWORD PTR [ESP+68]
          mov ECX,DWORD PTR [ESP+72]
          mov EDX,DWORD PTR [ESP+76]
          movzx EBP,BYTE PTR [EAX+242]
          test EBP,EBP
          je L_43968b
          test ECX,ECX
          mov EBX,EBP
          jle L_4398d5
          cmp EBP,15
          jg L_4398d5
          xor EBP,EBP
          jmp L_439664
          .byte 0x90
L_439660:
          cmp ECX,EBP
          jle L_439680
L_439664:
          add EBX,1
          add ESI,1
          add EDI,1
          movzx EAX,BYTE PTR [EDX+EBX*1-1]
          add EBP,1
          xor AL,BYTE PTR [ESI-1]
          cmp EBX,15
          mov BYTE PTR [EDI-1],AL
          jle L_439660
L_439680:
          cmp EBX,16
          mov EAX,0
          cmove EBX,EAX
L_43968b:
          mov EAX,ECX
          sub EAX,EBP
          sar EAX,4
          test EAX,EAX
          je L_43973b
          mov EAX,ESI
          or EAX,EDI
          test AL,3
          lea EAX,DWORD PTR [EBP+15]
          jne L_4397c5
          test DL,3
          jne L_4397c5
          cmp ECX,EAX
          jle L_43973b
          lea EAX,DWORD PTR [ECX-16]
          mov DWORD PTR [ESP+28],EBX
          mov DWORD PTR [ESP+72],ECX
          mov EBX,EBP
          sub EAX,EBP
          and EAX,4294967280
          lea EAX,DWORD PTR [EBP+EAX*1+16]
          mov EBP,EDX
          mov DWORD PTR [ESP+24],EAX
          jmp L_43970a
L_4396d8:
          mov EAX,DWORD PTR [EBP]
          xor EAX,DWORD PTR [ESI]
          add EDI,16
          add ESI,16
          add EBX,16
          mov DWORD PTR [EDI-16],EAX
          mov EAX,DWORD PTR [EBP+4]
          xor EAX,DWORD PTR [ESI-12]
          mov DWORD PTR [EDI-12],EAX
          mov EAX,DWORD PTR [EBP+8]
          xor EAX,DWORD PTR [ESI-8]
          mov DWORD PTR [EDI-8],EAX
          mov EAX,DWORD PTR [EBP+12]
          xor EAX,DWORD PTR [ESI-4]
          mov DWORD PTR [EDI-4],EAX
          cmp EBX,DWORD PTR [ESP+24]
          je L_43972f
L_43970a:
          mov EAX,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+8],EAX
          call FUN_439ec0
          test EAX,EAX
          je L_4396d8
L_439722:
          add ESP,44
          mov EAX,1
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_43972f:
          mov EDX,EBP
          mov ECX,DWORD PTR [ESP+72]
          mov EBP,EBX
          mov EBX,DWORD PTR [ESP+28]
L_43973b:
          cmp ECX,EBP
          jle L_43977d
          mov EAX,EBX
          mov EBX,ECX
L_439743:
          test EAX,EAX
          je L_439799
          cmp EAX,15
          jg L_439772
          cmp EBX,EBP
          jg L_439757
          jmp L_439772
L_439752:
          cmp EAX,15
          jg L_439772
L_439757:
          add EAX,1
          add ESI,1
          add EBP,1
          movzx ECX,BYTE PTR [EDX+EAX*1-1]
          add EDI,1
          xor CL,BYTE PTR [ESI-1]
          cmp EBX,EBP
          mov BYTE PTR [EDI-1],CL
          jg L_439752
L_439772:
          cmp EAX,16
          je L_439791
          cmp EBX,EBP
          jg L_439743
          mov EBX,EAX
L_43977d:
          mov EAX,DWORD PTR [ESP+80]
          mov BYTE PTR [EAX+242],BL
          add ESP,44
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_439791:
          cmp EBX,EBP
          jle L_4398ce
L_439799:
          mov EAX,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP+4],EDX
          mov DWORD PTR [ESP],EDX
          mov DWORD PTR [ESP+24],EDX
          mov DWORD PTR [ESP+8],EAX
          call FUN_439ec0
          test EAX,EAX
          mov EDX,DWORD PTR [ESP+24]
          jne L_439722
          cmp EBX,EBP
          jg L_439757
          mov EBX,EAX
          jmp L_43977d
L_4397c5:
          cmp ECX,EAX
          jle L_43973b
          lea EAX,DWORD PTR [ECX-16]
          mov DWORD PTR [ESP+28],EBX
          mov DWORD PTR [ESP+72],ECX
          mov EBX,EDX
          sub EAX,EBP
          and EAX,4294967280
          lea EAX,DWORD PTR [EBP+EAX*1+16]
          mov DWORD PTR [ESP+24],EAX
          jmp L_43989e
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_4397f0:
          movzx EAX,BYTE PTR [EBX]
          add ESI,16
          add EDI,16
          xor AL,BYTE PTR [ESI-16]
          add EBP,16
          mov BYTE PTR [EDI-16],AL
          movzx EAX,BYTE PTR [EBX+1]
          xor AL,BYTE PTR [ESI-15]
          mov BYTE PTR [EDI-15],AL
          movzx EAX,BYTE PTR [EBX+2]
          xor AL,BYTE PTR [ESI-14]
          mov BYTE PTR [EDI-14],AL
          movzx EAX,BYTE PTR [EBX+3]
          xor AL,BYTE PTR [ESI-13]
          mov BYTE PTR [EDI-13],AL
          movzx EAX,BYTE PTR [EBX+4]
          xor AL,BYTE PTR [ESI-12]
          mov BYTE PTR [EDI-12],AL
          movzx EAX,BYTE PTR [EBX+5]
          xor AL,BYTE PTR [ESI-11]
          mov BYTE PTR [EDI-11],AL
          movzx EAX,BYTE PTR [EBX+6]
          xor AL,BYTE PTR [ESI-10]
          mov BYTE PTR [EDI-10],AL
          movzx EAX,BYTE PTR [EBX+7]
          xor AL,BYTE PTR [ESI-9]
          mov BYTE PTR [EDI-9],AL
          movzx EAX,BYTE PTR [EBX+8]
          xor AL,BYTE PTR [ESI-8]
          mov BYTE PTR [EDI-8],AL
          movzx EAX,BYTE PTR [EBX+9]
          xor AL,BYTE PTR [ESI-7]
          mov BYTE PTR [EDI-7],AL
          movzx EAX,BYTE PTR [EBX+10]
          xor AL,BYTE PTR [ESI-6]
          mov BYTE PTR [EDI-6],AL
          movzx EAX,BYTE PTR [EBX+11]
          xor AL,BYTE PTR [ESI-5]
          mov BYTE PTR [EDI-5],AL
          movzx EAX,BYTE PTR [EBX+12]
          xor AL,BYTE PTR [ESI-4]
          mov BYTE PTR [EDI-4],AL
          movzx EAX,BYTE PTR [EBX+13]
          xor AL,BYTE PTR [ESI-3]
          mov BYTE PTR [EDI-3],AL
          movzx EAX,BYTE PTR [EBX+14]
          xor AL,BYTE PTR [ESI-2]
          mov BYTE PTR [EDI-2],AL
          movzx EAX,BYTE PTR [EBX+15]
          xor AL,BYTE PTR [ESI-1]
          mov BYTE PTR [EDI-1],AL
          cmp EBP,DWORD PTR [ESP+24]
          je L_4398bf
L_43989e:
          mov EAX,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],EAX
          call FUN_439ec0
          test EAX,EAX
          je L_4397f0
          jmp L_439722
L_4398bf:
          mov EDX,EBX
          mov ECX,DWORD PTR [ESP+72]
          mov EBX,DWORD PTR [ESP+28]
          jmp L_43973b
L_4398ce:
          xor EBX,EBX
          jmp L_43977d
L_4398d5:
          xor EBP,EBP
          jmp L_439680
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_4398e0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,188
          mov EAX,DWORD PTR [ESP+228]
          mov EBX,DWORD PTR [ESP+208]
          mov EDI,DWORD PTR [ESP+220]
          movzx ESI,BYTE PTR [EAX+242]
          test ESI,ESI
          je L_4399c9
          mov EAX,DWORD PTR [EDI]
          mov DWORD PTR [ESP+48],EAX
          mov EAX,DWORD PTR [EDI+4]
          mov DWORD PTR [ESP+52],EAX
          mov EAX,DWORD PTR [EDI+8]
          mov DWORD PTR [ESP+56],EAX
          mov EAX,DWORD PTR [EDI+12]
          mov DWORD PTR [ESP+60],EAX
          mov EAX,DWORD PTR [ESP+228]
          mov DWORD PTR [ESP+8],EAX
          lea EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+32],EAX
          call FUN_439ec0
          test EAX,EAX
          jne L_439aaf
          mov EBP,DWORD PTR [ESP+216]
          test EBP,EBP
          je L_43999e
          cmp ESI,15
          jg L_43999e
          mov EDX,DWORD PTR [ESP+212]
          mov ECX,DWORD PTR [ESP+216]
          jmp L_439974
L_439970:
          test ECX,ECX
          je L_439990
L_439974:
          add EBX,1
          add ESI,1
          movzx EAX,BYTE PTR [EBX-1]
          xor AL,BYTE PTR [ESP+ESI*1+47]
          add EDX,1
          sub ECX,1
          cmp ESI,15
          mov BYTE PTR [EDX-1],AL
          jle L_439970
L_439990:
          mov DWORD PTR [ESP+212],EDX
          mov DWORD PTR [ESP+216],ECX
L_43999e:
          mov ECX,DWORD PTR [ESP+216]
          test ECX,ECX
          jne L_439e95
          mov EBX,ESI
L_4399af:
          mov EAX,DWORD PTR [ESP+228]
          mov BYTE PTR [EAX+242],BL
          add ESP,188
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_4399c9:
          lea EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+32],EAX
          mov EAX,DWORD PTR [ESP+216]
          test EAX,EAX
          je L_439ea4
L_4399e0:
          mov DWORD PTR [ESP+40],0
          nop
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_4399f0:
          cmp DWORD PTR [ESP+216],128
          mov EAX,128
          cmovle EAX,DWORD PTR [ESP+216]
          sub DWORD PTR [ESP+216],EAX
          mov DWORD PTR [ESP+28],EAX
          sar EAX,4
          test EAX,EAX
          mov DWORD PTR [ESP+36],EAX
          jle L_439e48
          mov EBP,EAX
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+208],EBX
          mov EBX,DWORD PTR [ESP+224]
          shl EBP,4
          lea ESI,DWORD PTR [EAX+EBP*1]
          mov EBP,EAX
          .byte 0x66   # nop
          nop
L_439a40:
          mov EDX,DWORD PTR [EDI]
          add EBP,16
          mov DWORD PTR [EBP-16],EDX
          mov EDX,DWORD PTR [EDI+4]
          mov DWORD PTR [EBP-12],EDX
          mov EDX,DWORD PTR [EDI+8]
          mov DWORD PTR [EBP-8],EDX
          mov EDX,DWORD PTR [EDI+12]
          mov DWORD PTR [EBP-4],EDX
          mov DWORD PTR [ESP],EDI
          call EBX
          cmp EBP,ESI
          jne L_439a40
          test BYTE PTR [ESP+28],15
          mov EBX,DWORD PTR [ESP+208]
          mov ESI,DWORD PTR [ESP+36]
          jne L_439ac0
          sub ESI,1
L_439a78:
          mov DWORD PTR [ESP+208],EBX
          mov EBP,DWORD PTR [ESP+32]
          mov EBX,ESI
          mov ESI,DWORD PTR [ESP+228]
          jmp L_439a9b
          .byte 0x66
          .byte 0x90
L_439a90:
          sub EBX,1
          add EBP,16
          cmp EBX,-1
          je L_439ae5
L_439a9b:
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EBP
          call FUN_439ec0
          test EAX,EAX
          je L_439a90
L_439aaf:
          add ESP,188
          mov EAX,1
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x90
L_439ac0:
          mov EDX,DWORD PTR [EDI]
          add ESI,1
          shl ESI,4
          sar ESI,4
          mov DWORD PTR [EBP],EDX
          mov EDX,DWORD PTR [EDI+4]
          sub ESI,1
          mov DWORD PTR [EBP+4],EDX
          mov EDX,DWORD PTR [EDI+8]
          mov DWORD PTR [EBP+8],EDX
          mov EDX,DWORD PTR [EDI+12]
          mov DWORD PTR [EBP+12],EDX
          jmp L_439a78
L_439ae5:
          mov EBX,DWORD PTR [ESP+208]
L_439aec:
          mov EAX,DWORD PTR [ESP+212]
          or EAX,EBX
          test AL,3
          jne L_439d40
          mov ESI,DWORD PTR [ESP+28]
          cmp ESI,15
          jle L_439e85
          mov EAX,DWORD PTR [ESP+48]
          xor EAX,DWORD PTR [EBX]
          mov ECX,DWORD PTR [ESP+212]
          mov DWORD PTR [ECX],EAX
          mov EAX,DWORD PTR [ESP+52]
          xor EAX,DWORD PTR [EBX+4]
          mov DWORD PTR [ECX+4],EAX
          mov EAX,DWORD PTR [ESP+56]
          xor EAX,DWORD PTR [EBX+8]
          mov DWORD PTR [ECX+8],EAX
          mov EAX,DWORD PTR [ESP+60]
          xor EAX,DWORD PTR [EBX+12]
          cmp ESI,31
          mov DWORD PTR [ECX+12],EAX
          jle L_439cac
          mov EAX,DWORD PTR [ESP+64]
          xor EAX,DWORD PTR [EBX+16]
          mov DWORD PTR [ECX+16],EAX
          mov EAX,DWORD PTR [ESP+68]
          xor EAX,DWORD PTR [EBX+20]
          mov DWORD PTR [ECX+20],EAX
          mov EAX,DWORD PTR [ESP+72]
          xor EAX,DWORD PTR [EBX+24]
          mov DWORD PTR [ECX+24],EAX
          mov EAX,DWORD PTR [ESP+76]
          xor EAX,DWORD PTR [EBX+28]
          cmp ESI,47
          mov DWORD PTR [ECX+28],EAX
          jle L_439cac
          mov EAX,DWORD PTR [EBX+32]
          xor EAX,DWORD PTR [ESP+80]
          mov DWORD PTR [ECX+32],EAX
          mov EAX,DWORD PTR [EBX+36]
          xor EAX,DWORD PTR [ESP+84]
          mov DWORD PTR [ECX+36],EAX
          mov EAX,DWORD PTR [EBX+40]
          xor EAX,DWORD PTR [ESP+88]
          mov DWORD PTR [ECX+40],EAX
          mov EAX,DWORD PTR [EBX+44]
          xor EAX,DWORD PTR [ESP+92]
          cmp ESI,63
          mov DWORD PTR [ECX+44],EAX
          jle L_439cac
          mov EAX,DWORD PTR [EBX+48]
          xor EAX,DWORD PTR [ESP+96]
          mov DWORD PTR [ECX+48],EAX
          mov EAX,DWORD PTR [EBX+52]
          xor EAX,DWORD PTR [ESP+100]
          mov DWORD PTR [ECX+52],EAX
          mov EAX,DWORD PTR [EBX+56]
          xor EAX,DWORD PTR [ESP+104]
          mov DWORD PTR [ECX+56],EAX
          mov EAX,DWORD PTR [EBX+60]
          xor EAX,DWORD PTR [ESP+108]
          cmp ESI,79
          mov DWORD PTR [ECX+60],EAX
          jle L_439cac
          mov EAX,DWORD PTR [EBX+64]
          xor EAX,DWORD PTR [ESP+112]
          mov DWORD PTR [ECX+64],EAX
          mov EAX,DWORD PTR [EBX+68]
          xor EAX,DWORD PTR [ESP+116]
          mov DWORD PTR [ECX+68],EAX
          mov EAX,DWORD PTR [EBX+72]
          xor EAX,DWORD PTR [ESP+120]
          mov DWORD PTR [ECX+72],EAX
          mov EAX,DWORD PTR [EBX+76]
          xor EAX,DWORD PTR [ESP+124]
          cmp ESI,95
          mov DWORD PTR [ECX+76],EAX
          jle L_439cac
          mov EAX,DWORD PTR [EBX+80]
          xor EAX,DWORD PTR [ESP+128]
          mov DWORD PTR [ECX+80],EAX
          mov EAX,DWORD PTR [EBX+84]
          xor EAX,DWORD PTR [ESP+132]
          mov DWORD PTR [ECX+84],EAX
          mov EAX,DWORD PTR [EBX+88]
          xor EAX,DWORD PTR [ESP+136]
          mov DWORD PTR [ECX+88],EAX
          mov EAX,DWORD PTR [EBX+92]
          xor EAX,DWORD PTR [ESP+140]
          cmp ESI,111
          mov DWORD PTR [ECX+92],EAX
          jle L_439cac
          mov EAX,DWORD PTR [EBX+96]
          xor EAX,DWORD PTR [ESP+144]
          mov DWORD PTR [ECX+96],EAX
          mov EAX,DWORD PTR [EBX+100]
          xor EAX,DWORD PTR [ESP+148]
          mov DWORD PTR [ECX+100],EAX
          mov EAX,DWORD PTR [EBX+104]
          xor EAX,DWORD PTR [ESP+152]
          mov DWORD PTR [ECX+104],EAX
          mov EAX,DWORD PTR [EBX+108]
          xor EAX,DWORD PTR [ESP+156]
          mov DWORD PTR [ECX+108],EAX
          mov EAX,ESI
          add EAX,-128
          jne L_439cac
          mov EAX,DWORD PTR [EBX+112]
          xor EAX,DWORD PTR [ESP+160]
          mov DWORD PTR [ECX+112],EAX
          mov EAX,DWORD PTR [EBX+116]
          xor EAX,DWORD PTR [ESP+164]
          mov DWORD PTR [ECX+116],EAX
          mov EAX,DWORD PTR [EBX+120]
          xor EAX,DWORD PTR [ESP+168]
          mov DWORD PTR [ECX+120],EAX
          mov EAX,DWORD PTR [EBX+124]
          xor EAX,DWORD PTR [ESP+172]
          mov DWORD PTR [ECX+124],EAX
L_439cac:
          mov EAX,DWORD PTR [ESP+28]
          lea EDX,DWORD PTR [EAX-16]
          mov EAX,EDX
          and EAX,4294967280
          add EAX,16
          mov EDX,EAX
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
L_439cc0:
          mov ESI,DWORD PTR [ESP+32]
          add DWORD PTR [ESP+212],EDX
          add EBX,EDX
          lea ECX,DWORD PTR [ESI+EDX*1]
          lea ESI,DWORD PTR [EAX+1]
L_439cd3:
          cmp DWORD PTR [ESP+28],EAX
          jle L_439d23
          mov EBP,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+220],EDI
          mov EDI,DWORD PTR [ESP+212]
          mov EDX,EBP
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
L_439cf0:
          add EBX,1
          add EDX,1
          movzx EAX,BYTE PTR [EBX-1]
          xor AL,BYTE PTR [ECX+EDX*1-1]
          add EDI,1
          mov BYTE PTR [EDI-1],AL
          lea EAX,DWORD PTR [EDX-1]
          sub EAX,EBP
          add EAX,ESI
          cmp DWORD PTR [ESP+28],EAX
          jg L_439cf0
          mov DWORD PTR [ESP+212],EDI
          mov EDI,DWORD PTR [ESP+220]
          mov DWORD PTR [ESP+40],EDX
L_439d23:
          mov EDX,DWORD PTR [ESP+216]
          test EDX,EDX
          jne L_4399f0
          movzx EBX,BYTE PTR [ESP+40]
          jmp L_4399af
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_439d40:
          cmp DWORD PTR [ESP+28],15
          jle L_439e75
          mov EAX,DWORD PTR [ESP+28]
          mov ECX,DWORD PTR [ESP+212]
          mov ESI,EBX
          mov EDX,DWORD PTR [ESP+32]
          sub EAX,16
          mov DWORD PTR [ESP+36],EAX
          shr EAX,4
          add EAX,1
          mov EBP,EAX
          mov DWORD PTR [ESP+44],EAX
          mov EAX,EBX
          shl EBP,4
          add EBP,EBX
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_439d80:
          movzx EBX,BYTE PTR [EAX]
          add EAX,16
          add EDX,16
          xor BL,BYTE PTR [EDX-16]
          add ECX,16
          mov BYTE PTR [ECX-16],BL
          movzx EBX,BYTE PTR [EAX-15]
          xor BL,BYTE PTR [EDX-15]
          mov BYTE PTR [ECX-15],BL
          movzx EBX,BYTE PTR [EAX-14]
          xor BL,BYTE PTR [EDX-14]
          mov BYTE PTR [ECX-14],BL
          movzx EBX,BYTE PTR [EAX-13]
          xor BL,BYTE PTR [EDX-13]
          mov BYTE PTR [ECX-13],BL
          movzx EBX,BYTE PTR [EAX-12]
          xor BL,BYTE PTR [EDX-12]
          mov BYTE PTR [ECX-12],BL
          movzx EBX,BYTE PTR [EAX-11]
          xor BL,BYTE PTR [EDX-11]
          mov BYTE PTR [ECX-11],BL
          movzx EBX,BYTE PTR [EAX-10]
          xor BL,BYTE PTR [EDX-10]
          mov BYTE PTR [ECX-10],BL
          movzx EBX,BYTE PTR [EAX-9]
          xor BL,BYTE PTR [EDX-9]
          mov BYTE PTR [ECX-9],BL
          movzx EBX,BYTE PTR [EAX-8]
          xor BL,BYTE PTR [EDX-8]
          mov BYTE PTR [ECX-8],BL
          movzx EBX,BYTE PTR [EAX-7]
          xor BL,BYTE PTR [EDX-7]
          mov BYTE PTR [ECX-7],BL
          movzx EBX,BYTE PTR [EAX-6]
          xor BL,BYTE PTR [EDX-6]
          mov BYTE PTR [ECX-6],BL
          movzx EBX,BYTE PTR [EAX-5]
          xor BL,BYTE PTR [EDX-5]
          mov BYTE PTR [ECX-5],BL
          movzx EBX,BYTE PTR [EAX-4]
          xor BL,BYTE PTR [EDX-4]
          mov BYTE PTR [ECX-4],BL
          movzx EBX,BYTE PTR [EAX-3]
          xor BL,BYTE PTR [EDX-3]
          mov BYTE PTR [ECX-3],BL
          movzx EBX,BYTE PTR [EAX-2]
          xor BL,BYTE PTR [EDX-2]
          mov BYTE PTR [ECX-2],BL
          movzx EBX,BYTE PTR [EAX-1]
          xor BL,BYTE PTR [EDX-1]
          mov BYTE PTR [ECX-1],BL
          cmp EAX,EBP
          jne L_439d80
          mov EDX,DWORD PTR [ESP+36]
          mov EAX,DWORD PTR [ESP+44]
          mov EBX,ESI
          and EDX,4294967280
          shl EAX,4
          add EDX,16
          jmp L_439cc0
L_439e48:
          test BYTE PTR [ESP+28],15
          je L_439aec
          mov EAX,DWORD PTR [EDI]
          xor ESI,ESI
          mov DWORD PTR [ESP+48],EAX
          mov EAX,DWORD PTR [EDI+4]
          mov DWORD PTR [ESP+52],EAX
          mov EAX,DWORD PTR [EDI+8]
          mov DWORD PTR [ESP+56],EAX
          mov EAX,DWORD PTR [EDI+12]
          mov DWORD PTR [ESP+60],EAX
          jmp L_439a78
L_439e75:
          mov ESI,1
          xor EAX,EAX
          mov ECX,DWORD PTR [ESP+32]
          jmp L_439cd3
L_439e85:
          xor EAX,EAX
          mov ESI,1
          mov ECX,DWORD PTR [ESP+32]
          jmp L_439cd3
L_439e95:
          mov DWORD PTR [ESP],EDI
          call DWORD PTR [ESP+224]
          jmp L_4399e0
L_439ea4:
          xor EBX,EBX
          jmp L_4399af
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
          .byte 0x64
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_438b00 - .
          .byte 0xaf
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
          .byte 0x2c
          .byte 0x2
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
          .byte 0x47
          .byte 0xb
          .byte 0x43
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
          .byte 0x44
          .byte 0xb
          .byte 0x4a
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
          .byte 0x84
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_438bb0 - .
          .byte 0xe
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x98
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_438bc0 - .
          .byte 0x63
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
          .byte 0x57
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
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_438c30 - .
          .byte 0x63
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
          .byte 0x57
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
          .byte 0x10
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long L_438ca0 - .
          .byte 0x73
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
          .byte 0x9a
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
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x50
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long L_438e20 - .
          .byte 0xae
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
          .byte 0xb8
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
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x90
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long L_438fd0 - .
          .byte 0xb
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
          .byte 0x45
          .byte 0xe
          .byte 0x40
          .byte 0x3
          .byte 0x12
          .byte 0x1
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
          .byte 0x2
          .byte 0x67
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
          .byte 0x0
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xe8
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long L_4392e0 - .
          .byte 0x34
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
          .byte 0x45
          .byte 0xe
          .byte 0x40
          .byte 0x3
          .byte 0x1c
          .byte 0x1
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
          .byte 0x2
          .byte 0x68
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
          .byte 0x48
          .byte 0xb
          .byte 0x0
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x40
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long L_439620 - .
          .byte 0xbc
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
          .byte 0x45
          .byte 0xe
          .byte 0x40
          .byte 0x2
          .byte 0xfc
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
          .byte 0x2
          .byte 0x5b
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
          .byte 0x0
          .byte 0x0
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x98
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long L_4398e0 - .
          .byte 0xcb
          .byte 0x5
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
          .byte 0x1
          .byte 0x2
          .byte 0xd8
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
          .byte 0x2
          .byte 0xec
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
          .byte 0x42
          .byte 0xb
          .byte 0x0

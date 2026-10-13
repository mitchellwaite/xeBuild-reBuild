# app/main.s -- main (.text.startup), signal handlers, mode dispatch
#
# original placement:
#   .data          0044a4e0-0044a540
#   .eh_frame      004668b8-00466a1c
#   .rdata         00450884-0045132c
#   .rdata$zzz     004638d8-00463904
#   .text          0040d010-0040e020
#   .text.startup  004492c0-00449640

.intel_syntax noprefix
.globl FUN_40d120
.globl FUN_40d370
.globl FUN_4492c0
.globl L_44a4e0
.globl L_44a524

.text
.p2align 4
L_40d010:
          push EBX
          sub ESP,24
          mov EBX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],OFFSET L_450884
          call _printf
          cmp EBX,22
          ja L_40d090
          jmp DWORD PTR [EBX*4+L_450990]
L_40d030:
          mov DWORD PTR [ESP],OFFSET L_4508b0
          call _puts
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_40d040:
          mov DWORD PTR [ESP],OFFSET L_450983
          call _puts
          mov DWORD PTR [ESP],4
          call FUN_449198
L_40d058:
          mov DWORD PTR [ESP],OFFSET L_450925
          call _puts
          jmp L_40d040
L_40d066:
          mov DWORD PTR [ESP],OFFSET L_450909
          call _puts
          jmp L_40d040
L_40d074:
          mov DWORD PTR [ESP],OFFSET L_4508e8
          call _puts
          jmp L_40d040
L_40d082:
          mov DWORD PTR [ESP],OFFSET L_450937
          call _puts
          jmp L_40d040
L_40d090:
          mov DWORD PTR [ESP],OFFSET L_450954
          call _puts
          jmp L_40d040
          .byte 0x66
          .byte 0x90
FUN_40d0a0:
          sub ESP,28
          mov DWORD PTR [ESP+4],OFFSET L_40d010
          mov DWORD PTR [ESP],22
          call FUN_4490a0
          mov DWORD PTR [ESP+4],OFFSET L_40d010
          mov DWORD PTR [ESP],8
          call FUN_4490a0
          mov DWORD PTR [ESP+4],OFFSET L_40d010
          mov DWORD PTR [ESP],4
          call FUN_4490a0
          mov DWORD PTR [ESP+4],OFFSET L_40d010
          mov DWORD PTR [ESP],2
          call FUN_4490a0
          mov DWORD PTR [ESP+4],OFFSET L_40d010
          mov DWORD PTR [ESP],11
          call FUN_4490a0
          mov DWORD PTR [ESP+4],OFFSET L_40d010
          mov DWORD PTR [ESP],15
          call FUN_4490a0
          add ESP,28
          ret 
          .byte 0x90
FUN_40d120:
          push EDI
          push ESI
          push EBX
          sub ESP,16
          mov EAX,DWORD PTR [ESP+32]
          lea ESI,DWORD PTR [EAX+81032]
          lea EDI,DWORD PTR [EAX+81040]
          mov EDX,DWORD PTR [ESI*4+L_479ea0]
          test EDX,EDX
          je L_40d154
          mov ECX,DWORD PTR [EDI*4+L_479ea8]
          test ECX,ECX
          jne L_40d173
L_40d14c:
          mov DWORD PTR [ESP],EDX
          call _free
L_40d154:
          mov DWORD PTR [ESI*4+L_479ea0],0
          mov DWORD PTR [EDI*4+L_479ea8],0
          add ESP,16
          pop EBX
          xor EAX,EAX
          pop ESI
          pop EDI
          ret 
L_40d173:
          imul EAX,EAX,22
          mov DWORD PTR [ESP+8],8
          mov DWORD PTR [ESP+4],OFFSET L_4509ec
          lea EBX,DWORD PTR [EAX+L_4c8fe4]
          mov DWORD PTR [ESP],EBX
          call FUN_4491d0
          test EAX,EAX
          jne L_40d1e0
          mov EAX,DWORD PTR [EDI*4+L_479ea8]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESI*4+L_479ea0]
          mov DWORD PTR [ESP],EAX
          call FUN_402720
          test EAX,EAX
          je L_40d21a
L_40d1b6:
          mov DWORD PTR [ESP+4],OFFSET L_450a28
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,16
          mov EAX,1
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_40d1e0:
          mov DWORD PTR [ESP+8],12
          mov DWORD PTR [ESP+4],OFFSET L_4509f5
          mov DWORD PTR [ESP],EBX
          call FUN_4491d0
          test EAX,EAX
          jne L_40d242
          mov EAX,DWORD PTR [EDI*4+L_479ea8]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESI*4+L_479ea0]
          mov DWORD PTR [ESP],EAX
          call FUN_401630
          test EAX,EAX
          jne L_40d1b6
L_40d21a:
          mov DWORD PTR [ESP+4],OFFSET L_450a58
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EDX,DWORD PTR [ESI*4+L_479ea0]
          test EDX,EDX
          je L_40d154
          jmp L_40d14c
L_40d242:
          mov DWORD PTR [ESP+8],7
          mov DWORD PTR [ESP+4],OFFSET L_450a02
          mov DWORD PTR [ESP],EBX
          call FUN_4491d0
          test EAX,EAX
          je L_40d2b1
          mov DWORD PTR [ESP+8],7
          mov DWORD PTR [ESP+4],OFFSET L_450a0a
          mov DWORD PTR [ESP],EBX
          call FUN_4491d0
          test EAX,EAX
          jne L_40d2f4
          mov EAX,DWORD PTR [EDI*4+L_479ea8]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESI*4+L_479ea0]
          mov DWORD PTR [ESP],EAX
          call FUN_402410
          test EAX,EAX
          je L_40d21a
          mov EAX,DWORD PTR [ESI*4+L_479ea0]
          add EAX,288
          mov DWORD PTR [ESP],EAX
          call FUN_41ac00
          jmp L_40d1b6
L_40d2b1:
          mov EAX,DWORD PTR [EDI*4+L_479ea8]
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESI*4+L_479ea0]
          mov DWORD PTR [ESP],EAX
          call FUN_402020
          test EAX,EAX
          je L_40d21a
          mov EAX,DWORD PTR [ESI*4+L_479ea0]
          add EAX,288
          mov DWORD PTR [ESP],EAX
          call FUN_41abb0
          jmp L_40d1b6
L_40d2f4:
          mov DWORD PTR [ESP+8],11
          mov DWORD PTR [ESP+4],OFFSET L_450a12
          mov DWORD PTR [ESP],EBX
          call FUN_4491d0
          test EAX,EAX
          jne L_40d349
          mov EAX,DWORD PTR [EDI*4+L_479ea8]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESI*4+L_479ea0]
          mov DWORD PTR [ESP],EAX
          call FUN_401e60
          test EAX,EAX
          je L_40d21a
          mov EAX,DWORD PTR [ESI*4+L_479ea0]
          add EAX,16
          mov DWORD PTR [ESP],EAX
          call FUN_41ac50
          jmp L_40d1b6
L_40d349:
          mov DWORD PTR [ESP+8],7
          mov DWORD PTR [ESP+4],OFFSET L_450a1e
          mov DWORD PTR [ESP],EBX
          call FUN_4491d0
          test EAX,EAX
          je L_40d1b6
          jmp L_40d21a
          .byte 0x66
          .byte 0x90
FUN_40d370:
          mov EAX,DWORD PTR [ESP+8]
          mov EDX,DWORD PTR [ESP+4]
          sub EAX,17
          cmp EAX,73
          ja L_40d4b1
          jmp DWORD PTR [EAX*4+L_450c6c]
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_40d390:
          mov EAX,DWORD PTR [L_479ea4]
          and EAX,7
          cmp EAX,4
          jbe L_40d4e4
          mov DWORD PTR [ESP+8],OFFSET L_450b60
          mov DWORD PTR [ESP+4],EDX
          jmp _log_printf
L_40d3b2:
          mov DWORD PTR [ESP+8],OFFSET L_450a79
          mov DWORD PTR [ESP+4],EDX
          jmp _log_printf
L_40d3c3:
          mov DWORD PTR [ESP+8],OFFSET L_450a87
          mov DWORD PTR [ESP+4],EDX
          jmp _log_printf
L_40d3d4:
          mov DWORD PTR [ESP+8],OFFSET L_450a98
          mov DWORD PTR [ESP+4],EDX
          jmp _log_printf
L_40d3e5:
          mov DWORD PTR [ESP+8],OFFSET L_450aab
          mov DWORD PTR [ESP+4],EDX
          jmp _log_printf
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_40d400:
          mov DWORD PTR [ESP+8],OFFSET L_450abe
          mov DWORD PTR [ESP+4],EDX
          jmp _log_printf
L_40d411:
          mov DWORD PTR [ESP+8],OFFSET L_450acf
          mov DWORD PTR [ESP+4],EDX
          jmp _log_printf
L_40d422:
          mov EAX,DWORD PTR [L_479ea4]
          and EAX,7
          cmp EAX,4
          jbe L_40d4d3
          mov DWORD PTR [ESP+8],OFFSET L_450bb0
          mov DWORD PTR [ESP+4],EDX
          jmp _log_printf
L_40d444:
          mov EAX,DWORD PTR [L_479ea4]
          and EAX,7
          cmp EAX,4
          jbe L_40d4c2
          mov DWORD PTR [ESP+8],OFFSET L_450c00
          mov DWORD PTR [ESP+4],EDX
          jmp _log_printf
L_40d462:
          mov EAX,DWORD PTR [L_479ea4]
          and EAX,7
          cmp EAX,4
          jbe L_40d4a0
          mov DWORD PTR [ESP+8],OFFSET L_450b34
          mov DWORD PTR [ESP+4],EDX
          jmp _log_printf
L_40d480:
          mov EAX,DWORD PTR [L_479ea4]
          and EAX,7
          cmp EAX,4
          jbe L_40d4a0
          mov DWORD PTR [ESP+8],OFFSET L_450ae4
          mov DWORD PTR [ESP+4],EDX
          jmp _log_printf
          .byte 0x66
          .byte 0x90
L_40d4a0:
          mov DWORD PTR [ESP+8],OFFSET L_450b0c
          mov DWORD PTR [ESP+4],EDX
          jmp _log_printf
L_40d4b1:
          mov DWORD PTR [ESP+8],OFFSET L_450c56
          mov DWORD PTR [ESP+4],EDX
          jmp _log_printf
L_40d4c2:
          mov DWORD PTR [ESP+8],OFFSET L_450c2c
          mov DWORD PTR [ESP+4],EDX
          jmp _log_printf
L_40d4d3:
          mov DWORD PTR [ESP+8],OFFSET L_450bd8
          mov DWORD PTR [ESP+4],EDX
          jmp _log_printf
L_40d4e4:
          mov DWORD PTR [ESP+8],OFFSET L_450b8c
          mov DWORD PTR [ESP+4],EDX
          jmp _log_printf
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
FUN_40d500:
          push EDI
          push ESI
          push EBX
          sub ESP,96
          mov DWORD PTR [ESP+4],OFFSET L_44a4e0
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_479eac]
          test EAX,EAX
          jne L_40d670
L_40d527:
          mov DWORD PTR [ESP+4],OFFSET L_450dad
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_479ea4]
          and EAX,1073741831
          cmp EAX,5
          je L_40dd5b
          jbe L_40d630
          cmp EAX,7
          je L_40dcab
          jb L_40dc92
          cmp EAX,1073741828
          je L_40d6b1
          cmp EAX,1073741829
          jne L_40dd29
          mov DWORD PTR [ESP+4],OFFSET L_450de2
          mov DWORD PTR [ESP],0
          call _log_printf
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
L_40d590:
          mov DWORD PTR [ESP+4],OFFSET L_450e46
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_479ea4]
          test EAX,268435456
          jne L_40db50
          test EAX,1073741824
          je L_40dab0
          mov EAX,DWORD PTR [L_479f6c]
          test EAX,EAX
          je L_40dc10
          mov DWORD PTR [ESP+4],OFFSET L_450e6b
          mov DWORD PTR [ESP],0
          call _log_printf
          test BYTE PTR [L_479ea7],32
          jne L_40dc31
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
L_40d5f0:
          mov DWORD PTR [ESP+4],OFFSET L_450ec3
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_450ec5
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_479ea8]
          cmp EAX,9
          ja L_40d700
          jmp DWORD PTR [EAX*4+L_45119c]
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_40d630:
          cmp EAX,2
          je L_40dd42
          jbe L_40dc70
          cmp EAX,3
          je L_40d6ca
          cmp EAX,4
          jne L_40dd29
          mov DWORD PTR [ESP+4],OFFSET L_450dd1
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_40d590
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_40d670:
          mov EDX,EAX
          mov DWORD PTR [ESP+4],OFFSET L_450d94
          mov DWORD PTR [ESP],0
          and EDX,15
          mov DWORD PTR [ESP+20],EDX
          mov EDX,EAX
          shr EDX,8
          movzx EDX,DX
          mov DWORD PTR [ESP+16],EDX
          mov EDX,EAX
          shr EAX,28
          shr EDX,24
          mov DWORD PTR [ESP+8],EAX
          and EDX,15
          mov DWORD PTR [ESP+12],EDX
          call _log_printf
          jmp L_40d527
L_40d6b1:
          mov DWORD PTR [ESP+4],OFFSET L_450e0b
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_40d590
L_40d6ca:
          mov DWORD PTR [ESP+4],OFFSET L_450dc9
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_40d590
L_40d6e3:
          mov DWORD PTR [ESP+4],OFFSET L_450f31
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_479ea8]
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_40d700:
          lea EDX,DWORD PTR [EAX-3]
          cmp EDX,2
          jbe L_40d950
L_40d70c:
          cmp EAX,2
          je L_40db90
L_40d715:
          sub EAX,2
          cmp EAX,1
          jbe L_40d998
L_40d721:
          call FUN_4133f0
          test EAX,EAX
          lea ESI,DWORD PTR [ESP+32]
          je L_40d75f
          mov EDX,DWORD PTR [EAX]
          mov DWORD PTR [ESP+32],EDX
          mov EDX,DWORD PTR [EAX+4]
          mov DWORD PTR [ESP+36],EDX
          mov EAX,DWORD PTR [EAX+8]
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_45101c
          mov DWORD PTR [ESP],0
          mov BYTE PTR [ESP+44],0
          mov DWORD PTR [ESP+40],EAX
          call _log_printf
L_40d75f:
          mov DWORD PTR [ESP],ESI
          call FUN_413410
          test EAX,EAX
          jne L_40db70
L_40d76f:
          call FUN_4134f0
          test EAX,EAX
          mov EBX,EAX
          je L_40d7c7
          lea EDI,DWORD PTR [EBX+8]
          mov DWORD PTR [ESP+4],OFFSET L_45103c
          mov DWORD PTR [ESP],0
          call _log_printf
L_40d791:
          movzx EAX,BYTE PTR [EBX]
          mov DWORD PTR [ESP+4],OFFSET L_451049
          add EBX,1
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          cmp EDI,EBX
          jne L_40d791
          mov DWORD PTR [ESP+4],OFFSET L_450ec3
          mov DWORD PTR [ESP],0
          call _log_printf
L_40d7c7:
          mov DWORD PTR [ESP],ESI
          call FUN_413510
          test EAX,EAX
          jne L_40db30
L_40d7d7:
          mov DWORD PTR [ESP+4],OFFSET L_45105e
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_47a11c
          mov DWORD PTR [ESP],0
          call _showKey
          mov DWORD PTR [ESP+4],OFFSET L_45106b
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_47a10c
          mov DWORD PTR [ESP],0
          call _showKey
          mov DWORD PTR [ESP+4],OFFSET L_450ec3
          mov DWORD PTR [ESP],0
          call _log_printf
          call FUN_4133d0
          test EAX,EAX
          mov EBX,EAX
          je L_40d8c0
          lea ESI,DWORD PTR [EBX+16]
          mov DWORD PTR [ESP+4],OFFSET L_451079
          mov DWORD PTR [ESP],0
          call _log_printf
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
L_40d860:
          movzx EAX,BYTE PTR [EBX]
          mov DWORD PTR [ESP+4],OFFSET L_451049
          add EBX,1
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          cmp ESI,EBX
          jne L_40d860
          test BYTE PTR [L_479f03],2
          je L_40d8ac
          cmp DWORD PTR [L_479ea8],1
          je L_40dd74
          mov DWORD PTR [ESP+4],OFFSET L_45109f
          mov DWORD PTR [ESP],0
          call _log_printf
L_40d8ac:
          mov DWORD PTR [ESP+4],OFFSET L_450ec3
          mov DWORD PTR [ESP],0
          call _log_printf
L_40d8c0:
          movzx EAX,BYTE PTR [L_479f15]
          mov DWORD PTR [ESP+4],OFFSET L_4510aa
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          call FUN_4130b0
          test EAX,EAX
          jne L_40dae0
L_40d8ec:
          mov EAX,DWORD PTR [L_4c97a8]
          test EAX,EAX
          je L_40d91a
          cmp BYTE PTR [L_4c93a8],0
          je L_40d91a
          mov DWORD PTR [ESP+8],OFFSET L_4c93a8
          mov DWORD PTR [ESP+4],OFFSET L_451189
          mov DWORD PTR [ESP],0
          call _log_printf
L_40d91a:
          add ESP,96
          pop EBX
          pop ESI
          pop EDI
          ret 
L_40d921:
          mov DWORD PTR [ESP+4],OFFSET L_450f28
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_479ea8]
          lea EDX,DWORD PTR [EAX-3]
          cmp EDX,2
          ja L_40d70c
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_40d950:
          mov DWORD PTR [ESP+4],OFFSET L_450f3c
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_479f08]
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+4],EAX
          call FUN_40d370
          mov EBX,DWORD PTR [L_479f0c]
          test EBX,EBX
          jne L_40dd8d
L_40d987:
          mov EAX,DWORD PTR [L_479ea8]
          sub EAX,2
          cmp EAX,1
          ja L_40d721
L_40d998:
          test BYTE PTR [L_479f00],9
          je L_40d721
          mov DWORD PTR [ESP+4],OFFSET L_450ff8
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_40d721
L_40d9be:
          mov DWORD PTR [ESP+4],OFFSET L_450f0e
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_479ea8]
          jmp L_40d700
L_40d9dc:
          mov DWORD PTR [ESP+4],OFFSET L_450f06
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_479ea8]
          jmp L_40d700
L_40d9fa:
          mov DWORD PTR [ESP+4],OFFSET L_450f1f
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_479ea8]
          jmp L_40d700
L_40da18:
          mov DWORD PTR [ESP+4],OFFSET L_450f18
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_479ea8]
          jmp L_40d700
L_40da36:
          mov EDI,DWORD PTR [L_479eb4]
          test EDI,EDI
          jne L_40de42
          mov ESI,DWORD PTR [L_479eb0]
          test ESI,ESI
          je L_40de24
          mov DWORD PTR [ESP+4],OFFSET L_450ee9
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_479ea8]
          jmp L_40d700
L_40da70:
          mov DWORD PTR [ESP+4],OFFSET L_450ed2
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_479ea8]
          jmp L_40d700
L_40da8e:
          mov DWORD PTR [ESP+4],OFFSET L_450efe
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_479ea8]
          jmp L_40d700
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_40dab0:
          mov EAX,DWORD PTR [L_479ea8]
          sub EAX,6
          and EAX,4294967293
          jne L_40dc50
          mov DWORD PTR [ESP+4],OFFSET L_450ea9
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_40d5f0
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_40dae0:
          mov DWORD PTR [ESP+4],OFFSET L_4510ba
          mov DWORD PTR [ESP],0
          call _log_printf
          call FUN_413090
          cmp EAX,2
          je L_40ddf2
          cmp EAX,3
          je L_40ddd9
          cmp EAX,1
          je L_40ddc0
          mov DWORD PTR [ESP+4],OFFSET L_451178
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_40d8ec
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_40db30:
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_45104e
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_40d7d7
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_40db50:
          mov DWORD PTR [ESP+4],OFFSET L_450e53
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_40d5f0
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_40db70:
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_45102c
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_40d76f
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_40db90:
          test BYTE PTR [L_479f00],4
          jne L_40dcc4
          mov DWORD PTR [ESP+4],OFFSET L_450f84
          mov DWORD PTR [ESP],0
          call _log_printf
          test BYTE PTR [L_479f00],2
          jne L_40de0b
          mov DWORD PTR [ESP+4],OFFSET L_450fa3
          mov DWORD PTR [ESP],0
          call _log_printf
L_40dbd2:
          mov EDX,DWORD PTR [L_479f10]
          test EDX,EDX
          je L_40d987
          mov DWORD PTR [ESP+4],OFFSET L_450fd4
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_479f10]
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+4],EAX
          call FUN_40d370
          jmp L_40d987
          .byte 0x66
          .byte 0x90
L_40dc10:
          mov DWORD PTR [ESP+4],OFFSET L_450e80
          mov DWORD PTR [ESP],0
          call _log_printf
          test BYTE PTR [L_479ea7],32
          je L_40d5f0
L_40dc31:
          mov DWORD PTR [ESP+4],OFFSET L_450e94
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_40d5f0
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_40dc50:
          mov DWORD PTR [ESP+4],OFFSET L_450ebd
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_40d5f0
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_40dc70:
          cmp EAX,1
          jne L_40dd29
          mov DWORD PTR [ESP+4],OFFSET L_450dba
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_40d590
L_40dc92:
          mov DWORD PTR [ESP+4],OFFSET L_450df7
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_40d590
L_40dcab:
          mov DWORD PTR [ESP+4],OFFSET L_450dff
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_40d590
L_40dcc4:
          mov DWORD PTR [ESP+4],OFFSET L_450f3c
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_479f08]
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+4],EAX
          call FUN_40d370
          mov ECX,DWORD PTR [L_479f0c]
          test ECX,ECX
          je L_40dbd2
          mov DWORD PTR [ESP+4],OFFSET L_450f60
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_479f0c]
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+4],EAX
          call FUN_40d370
          jmp L_40dbd2
L_40dd29:
          mov DWORD PTR [ESP+4],OFFSET L_450e20
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_40d590
L_40dd42:
          mov DWORD PTR [ESP+4],OFFSET L_450dc1
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_40d590
L_40dd5b:
          mov DWORD PTR [ESP+4],OFFSET L_450dd9
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_40d590
L_40dd74:
          mov DWORD PTR [ESP+4],OFFSET L_451086
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_40d8ac
L_40dd8d:
          mov DWORD PTR [ESP+4],OFFSET L_450f60
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_479f0c]
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+4],EAX
          call FUN_40d370
          mov EAX,DWORD PTR [L_479ea8]
          jmp L_40d715
L_40ddc0:
          mov DWORD PTR [ESP+4],OFFSET L_4510c8
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_40d8ec
L_40ddd9:
          mov DWORD PTR [ESP+4],OFFSET L_45114c
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_40d8ec
L_40ddf2:
          mov DWORD PTR [ESP+4],OFFSET L_451100
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_40d8ec
L_40de0b:
          mov DWORD PTR [ESP+4],OFFSET L_450fbb
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_40dbd2
L_40de24:
          mov DWORD PTR [ESP+4],OFFSET L_450ef6
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_479ea8]
          jmp L_40d700
L_40de42:
          mov DWORD PTR [ESP+4],OFFSET L_450ed8
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_479ea8]
          jmp L_40d700
FUN_40de60:
          sub ESP,28
          mov DWORD PTR [ESP+8],325904
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_479ea0
          call _memset
          mov EAX,12078
          mov EDX,12142
          mov ECX,47
          mov DWORD PTR [L_479f00],4
          mov WORD PTR [L_47ad4c],AX
          mov BYTE PTR [L_47ad4e],0
          mov DWORD PTR [L_47a54c],1768042286
          mov WORD PTR [L_47a550],DX
          mov BYTE PTR [L_47a552],0
          mov DWORD PTR [L_47b14c],1633955630
          mov DWORD PTR [L_47b150],3105140
          mov DWORD PTR [L_47b54c],1868771118
          mov DWORD PTR [L_47b550],1852796269
          mov WORD PTR [L_47b554],CX
          mov DWORD PTR [L_479ec0],1
          mov DWORD PTR [L_479ec4],1
          mov DWORD PTR [L_479f18],4294967295
          mov DWORD PTR [L_479f1c],4294967295
          mov DWORD PTR [L_479f20],4294967295
          mov DWORD PTR [L_479f24],4294967295
          mov DWORD PTR [L_479f28],4294967295
          mov DWORD PTR [L_479f2c],4294967295
          mov DWORD PTR [L_479f30],4294967295
          mov DWORD PTR [L_479f34],4294967295
          mov DWORD PTR [L_479f38],4294967295
          mov DWORD PTR [L_479f3c],4294967295
          mov DWORD PTR [L_479f40],4294967295
          mov DWORD PTR [L_479f44],4294967295
          mov DWORD PTR [L_479f48],4294967295
          add ESP,28
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_40df90:
          push EBX
          sub ESP,296
          mov EAX,DWORD PTR [ESP+304]
          test EAX,EAX
          je L_40dfd5
          lea EBX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],EBX
          call _strcpy
          mov DWORD PTR [ESP+4],47
          mov DWORD PTR [ESP],EBX
          call FUN_449058
          test EAX,EAX
          je L_40e000
L_40dfc6:
          mov BYTE PTR [EAX],0
          mov DWORD PTR [ESP],EBX
          call FUN_449258
          test EAX,EAX
          je L_40dfe0
L_40dfd5:
          add ESP,296
          pop EBX
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_40dfe0:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_4511c4
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,296
          pop EBX
          ret 
L_40e000:
          mov DWORD PTR [ESP+4],92
          mov DWORD PTR [ESP],EBX
          call FUN_449058
          test EAX,EAX
          jne L_40dfc6
          add ESP,296
          pop EBX
          ret 
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90

.section .text.startup,"xr"
.p2align 4
FUN_4492c0:
          push EBP
          mov EBP,ESP
          push ESI
          push EBX
          and ESP,4294967280
          sub ESP,32
          mov ESI,DWORD PTR [EBP+8]
          mov EBX,DWORD PTR [EBP+12]
          call FUN_446c90
          call FUN_40de60
          mov DWORD PTR [ESP],0
          call _log_set_verbose
          call FUN_40d0a0
          call _log_init
          mov DWORD PTR [ESP+4],OFFSET L_44a4e0
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+20],OFFSET L_4511dd
          mov DWORD PTR [ESP+16],21
          mov DWORD PTR [ESP+12],1
          mov DWORD PTR [ESP+8],OFFSET L_4511e1
          mov DWORD PTR [ESP+4],OFFSET L_4511e9
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44a4e0
          mov DWORD PTR [ESP],0
          call _log_printf
          cmp ESI,1
          jle L_449512
          mov EAX,DWORD PTR [EBX]
          mov DWORD PTR [ESP],EAX
          call FUN_40df90
          mov DWORD PTR [ESP+8],3
          mov DWORD PTR [ESP+4],OFFSET L_4511fe
          mov EAX,DWORD PTR [EBX+4]
          mov DWORD PTR [ESP],EAX
          call FUN_4491d0
          test EAX,EAX
          jne L_449490
          add EBX,8
          mov DWORD PTR [ESP+4],OFFSET L_451202
          mov DWORD PTR [ESP],0
          sub ESI,2
          mov DWORD PTR [L_479ea0],4
          call _log_printf
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],ESI
          call FUN_418830
          mov EBX,EAX
L_4493b5:
          call FUN_40cfa0
          call FUN_40fb10
          mov EAX,DWORD PTR [_iniBuf]
          test EAX,EAX
          je L_4493d0
          mov DWORD PTR [ESP],EAX
          call _free
L_4493d0:
          mov EAX,DWORD PTR [L_47a13c]
          test EAX,EAX
          je L_4493e1
          mov DWORD PTR [ESP],EAX
          call _free
L_4493e1:
          mov EAX,DWORD PTR [L_47a144]
          test EAX,EAX
          je L_4493f2
          mov DWORD PTR [ESP],EAX
          call _free
L_4493f2:
          mov EAX,DWORD PTR [L_47a140]
          test EAX,EAX
          je L_449403
          mov DWORD PTR [ESP],EAX
          call _free
L_449403:
          mov EAX,DWORD PTR [L_47a148]
          test EAX,EAX
          je L_449414
          mov DWORD PTR [ESP],EAX
          call _free
L_449414:
          mov DWORD PTR [ESP+4],OFFSET L_44a4e0
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+8],OFFSET L_4511e1
          mov DWORD PTR [ESP+4],OFFSET L_4512ec
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44a4e0
          mov DWORD PTR [ESP],0
          call _log_printf
          call _log_finish
          mov EAX,DWORD PTR [L_44a524]
          test EAX,EAX
          je L_449487
          mov DWORD PTR [ESP+4],OFFSET L_45130f
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [_iob]
          mov DWORD PTR [ESP],EAX
          call FUN_449178
L_449487:
          lea ESP,DWORD PTR [EBP-8]
          mov EAX,EBX
          pop EBX
          pop ESI
          pop EBP
          ret 
L_449490:
          mov DWORD PTR [ESP+8],6
          mov DWORD PTR [ESP+4],OFFSET L_45121a
          mov EAX,DWORD PTR [EBX+4]
          mov DWORD PTR [ESP],EAX
          call FUN_4491d0
          test EAX,EAX
          je L_449537
          mov DWORD PTR [ESP+8],6
          mov DWORD PTR [ESP+4],OFFSET L_45123c
          mov EAX,DWORD PTR [EBX+4]
          mov DWORD PTR [ESP],EAX
          call FUN_4491d0
          test EAX,EAX
          jne L_44956e
          add EBX,8
          mov DWORD PTR [ESP+4],OFFSET L_451243
          mov DWORD PTR [ESP],0
          sub ESI,2
          mov DWORD PTR [L_479ea0],2
          call _log_printf
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],ESI
          call FUN_404770
          mov EBX,EAX
L_449508:
          test EBX,EBX
          jne L_4493b5
          jmp L_44952b
L_449512:
          mov DWORD PTR [ESP+4],OFFSET L_4512ac
          mov DWORD PTR [ESP],0
          call _log_printf
          call FUN_418a10
L_44952b:
          call FUN_40d500
          xor EBX,EBX
          jmp L_4493b5
L_449537:
          add EBX,8
          mov DWORD PTR [ESP+4],OFFSET L_451221
          mov DWORD PTR [ESP],0
          sub ESI,2
          call _log_printf
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [L_479ea0],3
          call FUN_408260
          mov EBX,EAX
          jmp L_4493b5
L_44956e:
          mov DWORD PTR [ESP+8],7
          mov DWORD PTR [ESP+4],OFFSET L_45125e
          mov EAX,DWORD PTR [EBX+4]
          mov DWORD PTR [ESP],EAX
          call FUN_4491d0
          test EAX,EAX
          je L_4495e3
          mov DWORD PTR [ESP+4],OFFSET L_451284
          mov DWORD PTR [ESP],0
          mov DWORD PTR [L_479ea0],1
          call _log_printf
          mov DWORD PTR [ESP+8],5
          mov DWORD PTR [ESP+4],OFFSET L_4512a4
          mov EAX,DWORD PTR [EBX+4]
          mov DWORD PTR [ESP],EAX
          call FUN_4491d0
          test EAX,EAX
          jne L_44961a
          add EBX,8
          sub ESI,2
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],ESI
          call FUN_419230
          mov EBX,EAX
          jmp L_449508
L_4495e3:
          add EBX,8
          mov DWORD PTR [ESP+4],OFFSET L_451266
          mov DWORD PTR [ESP],0
          sub ESI,2
          mov DWORD PTR [L_479ea0],5
          call _log_printf
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],ESI
          call FUN_40e200
          mov EBX,EAX
          jmp L_4493b5
L_44961a:
          add EBX,4
          sub ESI,1
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],ESI
          call FUN_419230
          mov EBX,EAX
          jmp L_449508
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

.data
.p2align 5
L_44a4e0:
          .string "---------------------------------------------------------------\n"
          .zero 3
L_44a524:
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0

.section .rdata,"dr"
.p2align 2
L_450884:
          .string "\n\nAn unhandled exception has occurred:\n\t"
          .zero 3
L_4508b0:
          .string "SIGABRT: abnormal termination triggered by abort call"
          .zero 2
L_4508e8:
          .string "SIGFPE: floating point exception"
L_450909:
          .string "SIGILL: illegal instruction"
L_450925:
          .string "SIGINT: interrupt"
L_450937:
          .string "SIGSEGV: segment violation"
          .zero 2
L_450954:
          .string "SIGTERM: Software termination signal from kill"
L_450983:
          .string "exiting...\n"
          .zero 1
L_450990:
          .long L_40d090
          .long L_40d090
          .long L_40d058
          .long L_40d090
          .long L_40d066
          .long L_40d090
          .long L_40d090
          .long L_40d090
          .long L_40d074
          .long L_40d090
          .long L_40d090
          .long L_40d082
          .long L_40d090
          .long L_40d090
          .long L_40d090
          .long L_40d090
          .long L_40d090
          .long L_40d090
          .long L_40d090
          .long L_40d090
          .long L_40d090
          .long L_40d090
          .long L_40d030
L_4509ec:
          .string "fcrt.bin"
L_4509f5:
          .string "extended.bin"
L_450a02:
          .string "crl.bin"
L_450a0a:
          .string "dae.bin"
L_450a12:
          .string "secdata.bin"
L_450a1e:
          .string "odd.bin"
          .zero 2
L_450a28:
          .string "verified! Will use if external file not found.\n"
L_450a58:
          .string "verify failed! Discarding data.\n"
L_450a79:
          .string "power button\n"
L_450a87:
          .string "IR power button\n"
L_450a98:
          .string "IR guide/X button\n"
L_450aab:
          .string "IR windows button\n"
L_450abe:
          .string "KIOSK debug pin\n"
L_450acf:
          .string "wireless controller\n"
L_450ae4:
          .string "wired controller (rear top usb port)\n"
          .zero 2
L_450b0c:
          .string "wired controller (INVALID FOR FATS!!)\n"
          .zero 1
L_450b34:
          .string "wired controller (rear middle usb port)\n"
          .zero 3
L_450b60:
          .string "wired controller (rear bottom usb port)\n"
          .zero 3
L_450b8c:
          .string "wired controller (rear usb port)\n"
          .zero 2
L_450bb0:
          .string "wired controller (front left usb port)\n"
L_450bd8:
          .string "wired controller (front top usb port)\n"
          .zero 1
L_450c00:
          .string "wired controller (front right usb port)\n"
          .zero 3
L_450c2c:
          .string "wired controller (front bottom usb port)\n"
L_450c56:
          .string "console eject button\n"
L_450c6c:
          .long L_40d3b2
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d3c3
          .long L_40d4b1
          .long L_40d3d4
          .long L_40d4b1
          .long L_40d3e5
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d400
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d4b1
          .long L_40d411
          .long L_40d422
          .long L_40d444
          .long L_40d462
          .long L_40d480
          .long L_40d390
L_450d94:
          .string "Kernel    : %d.%d.%d.%d\n"
L_450dad:
          .string "Console   : "
L_450dba:
          .string "Xenon\n"
L_450dc1:
          .string "Zephyr\n"
L_450dc9:
          .string "Falcon\n"
L_450dd1:
          .string "Jasper\n"
L_450dd9:
          .string "Trinity\n"
L_450de2:
          .string "Trinity (big block)\n"
L_450df7:
          .string "Corona\n"
L_450dff:
          .string "Winchester\n"
L_450e0b:
          .string "Jasper (big block)\n"
          .zero 1
L_450e20:
          .string "whoops, console type was not caught!\n"
L_450e46:
          .string "NAND size : "
L_450e53:
          .string "48MiB MMC (system only)"
L_450e6b:
          .string "64MiB + NAND MU area"
L_450e80:
          .string "64MiB (system only)"
L_450e94:
          .string " (extended size FFS)"
L_450ea9:
          .string "64MiB (small block)"
L_450ebd:
          .string "16MiB"
L_450ec3:
          .string "\n"
L_450ec5:
          .string "Build     : "
L_450ed2:
          .string "JTAG\n"
L_450ed8:
          .string "Glitch (v2 mfg)\n"
L_450ee9:
          .string "Glitch (v2)\n"
L_450ef6:
          .string "Glitch\n"
L_450efe:
          .string "Retail\n"
L_450f06:
          .string "Devkit\n"
L_450f0e:
          .string "Devkit16\n"
L_450f18:
          .string "Devgl\n"
L_450f1f:
          .string "Devgl16\n"
L_450f28:
          .string "Testkit\n"
L_450f31:
          .string "Testkit16\n"
L_450f3c:
          .string "Xell      : power on console with "
          .zero 1
L_450f60:
          .string "XellAlt   : power on console with "
          .zero 1
L_450f84:
          .string "Xell      : starts if tray is "
L_450fa3:
          .string "fully out at boot time\n"
L_450fbb:
          .string "not closed at boot time\n"
L_450fd4:
          .string "Dualboot  : power on console with "
          .zero 1
L_450ff8:
          .string "UART      : cygnos/demon speed set\n"
L_45101c:
          .string "Serial    : %s\n"
L_45102c:
          .string "ConsoleId : %s\n"
L_45103c:
          .string "MoboSerial: "
L_451049:
          .string "%02X"
L_45104e:
          .string "Mfg Date  : %s\n"
L_45105e:
          .string "CPU Key   : "
L_45106b:
          .string "\n1BL Key   : "
L_451079:
          .string "DVD Key   : "
L_451086:
          .string " (retail - not patched!)"
L_45109f:
          .string " (patched)"
L_4510aa:
          .string "CF LDV    : %d\n"
L_4510ba:
          .string "KV type   : "
          .zero 1
L_4510c8:
          .string "type2 (hashed - unchecked, master key not available)\n"
          .zero 2
L_451100:
          .string "type2 (hashed - Invalid! Keyvault is modified or from a different CPU key)\n"
L_45114c:
          .string "type2 (hashed - Good! Signature is valid.)\n"
L_451178:
          .string "type1 (no hash)\n"
L_451189:
          .string "SHA-1 file: %s\n"
          .zero 3
L_45119c:
          .long L_40d700
          .long L_40da8e
          .long L_40da70
          .long L_40da36
          .long L_40da18
          .long L_40d9fa
          .long L_40d9dc
          .long L_40d9be
          .long L_40d921
          .long L_40d6e3
L_4511c4:
          .string "base path changed to %s\n"
L_4511dd:
          .string "810"
L_4511e1:
          .string "xeBuild"
L_4511e9:
          .string "     %s v%d.%02d.%s\n"
L_4511fe:
          .string "ini"
L_451202:
          .string "---- { Ini Mode } ----\n"
L_45121a:
          .string "client"
L_451221:
          .string "---- { Client Mode } ----\n"
L_45123c:
          .string "update"
L_451243:
          .string "---- { Update Mode } ----\n"
L_45125e:
          .string "extract"
L_451266:
          .string "---- { Extract Mode } ----\n"
          .zero 2
L_451284:
          .string "---- { Image Build Mode } ----\n"
L_4512a4:
          .string "build"
          .zero 2
L_4512ac:
          .string "ERROR: invalid command line, you need to specify parameters!\n"
          .zero 2
L_4512ec:
          .string "    %s Finished. Have a nice day.\n"
L_45130f:
          .string "\npress <enter> to quit...\n"
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
          .byte 0x18
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_40d010 - .
          .byte 0x8e
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_40d0a0 - .
          .byte 0x7f
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x2
          .byte 0x7b
          .byte 0xe
          .byte 0x4
          .byte 0x48
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x50
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_40d120 - .
          .byte 0x4e
          .byte 0x2
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
          .byte 0x47
          .byte 0xa
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0xc
          .byte 0x43
          .byte 0xc6
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x2
          .byte 0x5a
          .byte 0xa
          .byte 0xe
          .byte 0x10
          .byte 0x46
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
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x9c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_40d370 - .
          .byte 0x85
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x34
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_40d500 - .
          .byte 0x60
          .byte 0x9
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
          .byte 0x70
          .byte 0x3
          .byte 0x17
          .byte 0x4
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
          .byte 0x41
          .byte 0xb
          .byte 0x0
          .byte 0x18
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xe8
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_40de60 - .
          .byte 0x26
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x3
          .byte 0x22
          .byte 0x1
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x34
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x4
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_40df90 - .
          .byte 0x8c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x46
          .byte 0xe
          .byte 0xb0
          .byte 0x2
          .byte 0x2
          .byte 0x44
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x44
          .byte 0xb
          .byte 0x5e
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x5a
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_4492c0 - .
          .byte 0x73
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x85
          .byte 0x2
          .byte 0x42
          .byte 0xd
          .byte 0x5
          .byte 0x48
          .byte 0x86
          .byte 0x3
          .byte 0x83
          .byte 0x4
          .byte 0x3
          .byte 0xc2
          .byte 0x1
          .byte 0xa
          .byte 0xc3
          .byte 0x41
          .byte 0xc6
          .byte 0x41
          .byte 0xc5
          .byte 0xc
          .byte 0x4
          .byte 0x4
          .byte 0x41
          .byte 0xb

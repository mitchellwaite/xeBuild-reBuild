# app/consoleinfo.s -- options/launch ini writing, console info response parsing
#
# original placement:
#   .bss           0047957c-004795a0
#   .eh_frame      0046ac70-0046af40
#   .rdata         0045b4a4-0045bdb4
#   .rdata$zzz     00463b14-00463b40
#   .text          00430460-00431c20

.intel_syntax noprefix
.globl FUN_431a60

.text
.p2align 4
FUN_430460:
          push ESI
          push EBX
          sub ESP,292
          mov ESI,DWORD PTR [ESP+304]
          test ESI,ESI
          je L_43052b
          lea EBX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EBX
          call FUN_449080
          mov DWORD PTR [ESP],ESI
          call _strlen
          cmp BYTE PTR [ESP+EAX*1+28],47
          je L_4304d0
          mov EDX,EBX
L_430498:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_430498
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          mov EAX,47
          sbb EDX,3
          mov WORD PTR [EDX],AX
L_4304d0:
          mov EDX,EBX
L_4304d2:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_4304d2
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          sbb EDX,3
          mov DWORD PTR [EDX],1769238639
          mov DWORD PTR [EDX+4],779316847
          mov DWORD PTR [EDX+8],6909545
          mov DWORD PTR [ESP+4],OFFSET L_45b4a4
          mov DWORD PTR [ESP],EBX
          call _fopen
          mov DWORD PTR [L_47957c],EAX
L_43052b:
          add ESP,292
          pop EBX
          pop ESI
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
L_430540:
          mov EAX,DWORD PTR [L_47957c]
          test EAX,EAX
          je L_430564
          sub ESP,28
          mov DWORD PTR [ESP],EAX
          call FUN_449180
          mov EAX,DWORD PTR [L_47957c]
          mov DWORD PTR [ESP],EAX
          call _fclose
          add ESP,28
L_430564:
          repz ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_430570:
          mov EAX,DWORD PTR [L_47957c]
          test EAX,EAX
          je L_43059f
          sub ESP,28
          mov EDX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+4],OFFSET L_45b4a7
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+12],EDX
          mov EDX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+8],EDX
          call FUN_449158
          add ESP,28
L_43059f:
          repz ret 
          jmp L_4305b0
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
L_4305b0:
          sub ESP,28
          mov EDX,DWORD PTR [L_47957c]
          mov EAX,DWORD PTR [ESP+32]
          test EDX,EDX
          je L_4305d8
          movzx EAX,AL
          mov DWORD PTR [ESP+4],OFFSET L_45b4b2
          mov DWORD PTR [ESP],EDX
          mov DWORD PTR [ESP+8],EAX
          call FUN_449158
L_4305d8:
          add ESP,28
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_4305e0:
          mov EAX,DWORD PTR [L_47957c]
          test EAX,EAX
          je L_43065d
          push ESI
          push EBX
          sub ESP,20
          mov EDX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],OFFSET L_45b4c0
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+8],EDX
          call FUN_449158
          mov EBX,DWORD PTR [ESP+36]
          lea ESI,DWORD PTR [EBX+16]
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
L_430610:
          movzx EAX,BYTE PTR [EBX]
          mov DWORD PTR [ESP+4],OFFSET L_45b4c6
          add EBX,1
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [L_47957c]
          mov DWORD PTR [ESP],EAX
          call FUN_449158
          cmp ESI,EBX
          jne L_430610
          mov EAX,DWORD PTR [L_47957c]
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],OFFSET L_45b4cb
          mov DWORD PTR [ESP+12],EAX
          call FUN_449118
          add ESP,20
          pop EBX
          pop ESI
L_43065d:
          repz ret 
          .byte 0x90
FUN_430660:
          mov EDX,DWORD PTR [L_47957c]
          test EDX,EDX
          je L_4306a3
          sub ESP,28
          mov EAX,DWORD PTR [ESP+36]
          sub EAX,17
          cmp EAX,73
          ja L_430830
          jmp DWORD PTR [EAX*4+L_45b804]
L_430684:
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],OFFSET L_45b4d0
          mov DWORD PTR [ESP],EDX
          mov DWORD PTR [ESP+8],EAX
          call FUN_449158
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_4306a0:
          add ESP,28
L_4306a3:
          repz ret 
L_4306a5:
          mov EAX,DWORD PTR [L_479ea4]
          and EAX,7
          cmp EAX,4
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+8],EAX
          jbe L_4308b0
          mov DWORD PTR [ESP+4],OFFSET L_45b688
          mov DWORD PTR [ESP],EDX
          call FUN_449158
          jmp L_4306a0
L_4306d0:
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],OFFSET L_45b4f4
          mov DWORD PTR [ESP],EDX
          mov DWORD PTR [ESP+8],EAX
          call FUN_449158
          jmp L_4306a0
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4306f0:
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],OFFSET L_45b518
          mov DWORD PTR [ESP],EDX
          mov DWORD PTR [ESP+8],EAX
          call FUN_449158
          jmp L_4306a0
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_430710:
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],OFFSET L_45b538
          mov DWORD PTR [ESP],EDX
          mov DWORD PTR [ESP+8],EAX
          call FUN_449158
          jmp L_4306a0
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_430730:
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],OFFSET L_45b55c
          mov DWORD PTR [ESP],EDX
          mov DWORD PTR [ESP+8],EAX
          call FUN_449158
          jmp L_4306a0
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_430750:
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],OFFSET L_45b57c
          mov DWORD PTR [ESP],EDX
          mov DWORD PTR [ESP+8],EAX
          call FUN_449158
          jmp L_4306a0
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_430770:
          mov EAX,DWORD PTR [L_479ea4]
          and EAX,7
          cmp EAX,4
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+8],EAX
          jbe L_430895
          mov DWORD PTR [ESP+4],OFFSET L_45b6f8
          mov DWORD PTR [ESP],EDX
          call FUN_449158
          jmp L_4306a0
          .byte 0x66
          .byte 0x90
L_4307a0:
          mov EAX,DWORD PTR [L_479ea4]
          and EAX,7
          cmp EAX,4
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+8],EAX
          jbe L_430880
          mov DWORD PTR [ESP+4],OFFSET L_45b768
          mov DWORD PTR [ESP],EDX
          call FUN_449158
          jmp L_4306a0
          .byte 0x66
          .byte 0x90
L_4307d0:
          mov EAX,DWORD PTR [L_479ea4]
          and EAX,7
          cmp EAX,4
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+8],EAX
          .byte 0x0f,0x86; .long L_430865-.-4   # jbe L_430865
          mov DWORD PTR [ESP+4],OFFSET L_45b614
          mov DWORD PTR [ESP],EDX
          call FUN_449158
          jmp L_4306a0
          .byte 0x66
          .byte 0x90
L_430800:
          mov EAX,DWORD PTR [L_479ea4]
          and EAX,7
          cmp EAX,4
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+8],EAX
          jbe L_430850
          mov DWORD PTR [ESP+4],OFFSET L_45b5a4
          mov DWORD PTR [ESP],EDX
          call FUN_449158
          jmp L_4306a0
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_430830:
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],OFFSET L_45b7e0
          mov DWORD PTR [ESP],EDX
          mov DWORD PTR [ESP+8],EAX
          call FUN_449158
          jmp L_4306a0
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_430850:
          mov DWORD PTR [ESP+4],OFFSET L_45b5dc
          mov DWORD PTR [ESP],EDX
          call FUN_449158
          jmp L_4306a0
L_430865:
          mov DWORD PTR [ESP+4],OFFSET L_45b650
          mov DWORD PTR [ESP],EDX
          call FUN_449158
          jmp L_4306a0
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_430880:
          mov DWORD PTR [ESP+4],OFFSET L_45b7a4
          mov DWORD PTR [ESP],EDX
          call FUN_449158
          jmp L_4306a0
L_430895:
          mov DWORD PTR [ESP+4],OFFSET L_45b730
          mov DWORD PTR [ESP],EDX
          call FUN_449158
          jmp L_4306a0
          .byte 0x8d,0xb6,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_4308b0:
          mov DWORD PTR [ESP+4],OFFSET L_45b6c4
          mov DWORD PTR [ESP],EDX
          call FUN_449158
          jmp L_4306a0
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
FUN_4308d0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,92
          mov EBX,DWORD PTR [ESP+116]
          lea ESI,DWORD PTR [ESP+16]
          mov EBP,EBX
          and EBP,15
          lea EDI,DWORD PTR [EBP+1]
          mov DWORD PTR [ESP],EDI
          call FUN_420a90
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],EAX
          call FUN_449080
          cmp EDI,4
          jb L_43091c
          cmp EDI,5
          jbe L_4309b3
          cmp EDI,6
          jne L_43091c
          cmp DWORD PTR [ESP+120],50331648
          je L_430ad0
L_43091c:
          mov EAX,DWORD PTR [ESP+112]
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_45b92c
          mov DWORD PTR [ESP],EAX
          call FUN_433690
          test EBX,EBX
          js L_430a80
          test EBX,536870912
          mov DWORD PTR [L_479ea8],3
          jne L_430a20
          test EBX,1073741824
          jne L_430a43
          and EBX,268435456
          jne L_430aa3
L_43096a:
          mov EAX,DWORD PTR [ESP+112]
          mov DWORD PTR [ESP+4],OFFSET L_45b965
          mov DWORD PTR [ESP],EAX
          call FUN_433690
          mov EAX,DWORD PTR [L_47957c]
          test EAX,EAX
          je L_4309a3
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+8],OFFSET L_45b968
          mov DWORD PTR [ESP+4],OFFSET L_45b4a7
          mov DWORD PTR [ESP],EAX
          call FUN_449158
L_4309a3:
          mov DWORD PTR [ESP],ESI
          call FUN_424170
          add ESP,92
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_4309b3:
          cmp DWORD PTR [ESP+120],69206016
          jne L_43091c
          mov EAX,DWORD PTR [L_479580]
          mov EDX,ESI
          cmp BYTE PTR [EAX+4],8
          je L_4309d8
          test BYTE PTR [EAX+8],8
          je L_430b13
L_4309d8:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_4309d8
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          mov ECX,29542
          sbb EDX,3
          mov DWORD PTR [EDX],1718053218
          mov WORD PTR [EDX+4],CX
          mov BYTE PTR [EDX+6],0
          jmp L_43091c
L_430a20:
          mov EAX,DWORD PTR [ESP+112]
          mov DWORD PTR [ESP+4],OFFSET L_45b948
          mov DWORD PTR [L_479eb0],1
          mov DWORD PTR [ESP],EAX
          call FUN_433690
          jmp L_43096a
L_430a43:
          mov EAX,DWORD PTR [ESP+112]
          mov DWORD PTR [ESP+4],OFFSET L_45b950
          mov DWORD PTR [ESP],EAX
          call FUN_433690
          test EBP,EBP
          jne L_43096a
          mov EAX,DWORD PTR [ESP+112]
          mov DWORD PTR [ESP+4],OFFSET L_45b957
          mov DWORD PTR [ESP],EAX
          call FUN_433690
          jmp L_43096a
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_430a80:
          mov EAX,DWORD PTR [ESP+112]
          mov DWORD PTR [ESP+4],OFFSET L_45b943
          mov DWORD PTR [L_479ea8],2
          mov DWORD PTR [ESP],EAX
          call FUN_433690
          jmp L_43096a
L_430aa3:
          mov EAX,DWORD PTR [ESP+112]
          mov DWORD PTR [ESP+4],OFFSET L_45b95c
          mov DWORD PTR [L_479eb4],1
          mov DWORD PTR [L_479eb0],1
          mov DWORD PTR [ESP],EAX
          call FUN_433690
          jmp L_43096a
L_430ad0:
          mov EDX,ESI
L_430ad2:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_430ad2
          mov ECX,EAX
          mov EDI,26420
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          sbb EDX,3
          mov WORD PTR [EDX],DI
          mov BYTE PTR [EDX+2],0
          jmp L_43091c
L_430b13:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_430b13
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          mov EAX,25186
          sbb EDX,3
          mov WORD PTR [EDX],AX
          mov BYTE PTR [EDX+2],0
          jmp L_43091c
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
FUN_430b60:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,60
          mov DWORD PTR [ESP],22
          mov EDI,DWORD PTR [ESP+80]
          call FUN_4276f0
          mov ESI,EAX
          mov DWORD PTR [ESP+4],OFFSET L_45b970
          mov DWORD PTR [ESP],1
          imul EBX,ESI,1068
          call FUN_433690
          mov DWORD PTR [ESP],OFFSET L_45b990
          lea EAX,DWORD PTR [EBX+L_4bc150+16]
          mov DWORD PTR [ESP+4],EAX
          call FUN_41fd60
          mov DWORD PTR [EBX+L_4bc150+12],EAX
          add EBX,OFFSET L_479ea0
          test EAX,EAX
          je L_430d02
          mov ECX,DWORD PTR [EBX+271040]
          mov EDX,EAX
          xor EAX,EAX
          test ECX,ECX
          jne L_430bd3
          add ESP,60
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_430bd3:
          lea EAX,DWORD PTR [ESP+20]
          mov DWORD PTR [ESP+12],27
          mov DWORD PTR [ESP+4],ECX
          mov DWORD PTR [ESP],EDX
          mov DWORD PTR [ESP+20],774927963
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+24],757086256
          mov DWORD PTR [ESP+28],1936615712
          mov DWORD PTR [ESP+32],1701996912
          mov DWORD PTR [ESP+36],2036473956
          mov DWORD PTR [ESP+40],1634429216
          mov DWORD PTR [ESP+44],6121842
          call FUN_421000
          test EAX,EAX
          je L_430dd0
          mov DWORD PTR [ESP+4],OFFSET L_45b9a0
          mov DWORD PTR [ESP],EDI
          mov EBP,DWORD PTR [L_479f00]
          call FUN_433690
          mov EAX,DWORD PTR [EBX+271036]
          and EBP,4294967280
          movzx EDX,BYTE PTR [EAX+2471]
          add EAX,2464
          mov DWORD PTR [L_479f08],EDX
          movzx EDX,BYTE PTR [EAX+11]
          mov DWORD PTR [L_479f10],EDX
          movzx EDX,BYTE PTR [EAX+15]
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [L_479f0c],EDX
          call FUN_420ad0
          mov DWORD PTR [ESP+4],OFFSET L_45b9c5
          and EAX,15
          mov DWORD PTR [ESP],EDI
          or EBP,EAX
          call FUN_433690
          mov EAX,DWORD PTR [L_479f08]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],EAX
          call FUN_40d370
          mov EAX,DWORD PTR [L_479f08]
          mov DWORD PTR [ESP],OFFSET L_45b9d8
          mov DWORD PTR [ESP+4],EAX
          call FUN_430660
          mov EDX,DWORD PTR [L_479f0c]
          test EDX,EDX
          jne L_430d92
L_430cc5:
          and EBP,9
          jne L_430d50
L_430cce:
          mov EAX,DWORD PTR [L_479f10]
          test EAX,EAX
          jne L_430d10
L_430cd7:
          imul ESI,ESI,1068
          mov EAX,DWORD PTR [ESI+L_4bc150+12]
          mov DWORD PTR [ESP],EAX
          call FUN_41ea70
          mov DWORD PTR [ESI+L_4bc150+16],0
          add ESP,60
          mov EAX,1
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_430d02:
          add ESP,60
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_430d10:
          mov DWORD PTR [ESP+4],OFFSET L_45ba3a
          mov DWORD PTR [ESP],EDI
          call FUN_433690
          mov EAX,DWORD PTR [L_479f10]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],EAX
          call FUN_40d370
          mov EAX,DWORD PTR [L_479f10]
          mov DWORD PTR [ESP],OFFSET L_45ba4c
          mov DWORD PTR [ESP+4],EAX
          call FUN_430660
          jmp L_430cd7
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_430d50:
          mov DWORD PTR [ESP+4],OFFSET L_45ba04
          mov DWORD PTR [ESP],EDI
          call FUN_433690
          mov EAX,DWORD PTR [L_47957c]
          test EAX,EAX
          je L_430cce
          mov DWORD PTR [ESP+12],OFFSET L_45ba2e
          mov DWORD PTR [ESP+8],OFFSET L_45ba33
          mov DWORD PTR [ESP+4],OFFSET L_45b4a7
          mov DWORD PTR [ESP],EAX
          call FUN_449158
          jmp L_430cce
L_430d92:
          mov DWORD PTR [ESP+4],OFFSET L_45b9e3
          mov DWORD PTR [ESP],EDI
          call FUN_433690
          mov EAX,DWORD PTR [L_479f0c]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],EAX
          call FUN_40d370
          mov EAX,DWORD PTR [L_479f0c]
          mov DWORD PTR [ESP],OFFSET L_45b9f6
          mov DWORD PTR [ESP+4],EAX
          call FUN_430660
          jmp L_430cc5
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_430dd0:
          mov DWORD PTR [ESP+4],OFFSET L_45ba58
          mov DWORD PTR [ESP],0
          call FUN_433690
          mov DWORD PTR [L_479f08],18
          jmp L_430cd7
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
FUN_430e00:
          push EDI
          push ESI
          push EBX
          sub ESP,48
          lea EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],OFFSET L_45babc
          mov ESI,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+4],EAX
          call FUN_41fd60
          test EAX,EAX
          je L_430fd5
          mov EBX,EAX
          mov EAX,DWORD PTR [ESP+44]
          test EAX,EAX
          je L_430ef9
          movzx EDI,BYTE PTR [EBX+77]
          mov EAX,EDI
          and EAX,7
          or DWORD PTR [L_479f00],EAX
          cmp DWORD PTR [L_479ea8],2
          je L_430f00
L_430e50:
          movzx EAX,BYTE PTR [EBX+79]
          mov DWORD PTR [L_479f08],EAX
          movzx EAX,BYTE PTR [EBX+78]
          mov DWORD PTR [ESP+4],OFFSET L_45b9c5
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [L_479f0c],EAX
          call FUN_433690
          mov EAX,DWORD PTR [L_479f08]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],EAX
          call FUN_40d370
          mov EAX,DWORD PTR [L_479f08]
          mov DWORD PTR [ESP],OFFSET L_45b9d8
          mov DWORD PTR [ESP+4],EAX
          call FUN_430660
          mov EAX,DWORD PTR [L_479f0c]
          test EAX,EAX
          jne L_430f80
L_430ea5:
          test EDI,1
          jne L_430f40
L_430eb1:
          and EDI,2
          je L_430edf
          mov EAX,DWORD PTR [L_47957c]
          test EAX,EAX
          je L_430edf
          mov DWORD PTR [ESP+12],OFFSET L_45ba2e
          mov DWORD PTR [ESP+8],OFFSET L_45bac6
          mov DWORD PTR [ESP+4],OFFSET L_45b4a7
          mov DWORD PTR [ESP],EAX
          call FUN_449158
L_430edf:
          mov EAX,DWORD PTR [L_479f10]
          test EAX,EAX
          jne L_430fc0
L_430eec:
          mov DWORD PTR [ESP],EBX
          call FUN_41ea70
          mov EAX,1
L_430ef9:
          add ESP,48
          pop EBX
          pop ESI
          pop EDI
          ret 
L_430f00:
          cmp BYTE PTR [EBX+75],1
          jne L_430f14
          movzx EAX,BYTE PTR [EBX+76]
          mov DWORD PTR [L_479f10],EAX
          jmp L_430e50
L_430f14:
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],EAX
          call FUN_430b60
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+28],EAX
          call FUN_41ea70
          mov EAX,DWORD PTR [ESP+28]
          add ESP,48
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_430f40:
          mov DWORD PTR [ESP+4],OFFSET L_45ba04
          mov DWORD PTR [ESP],ESI
          call FUN_433690
          mov EAX,DWORD PTR [L_47957c]
          test EAX,EAX
          je L_430edf
          mov DWORD PTR [ESP+12],OFFSET L_45ba2e
          mov DWORD PTR [ESP+8],OFFSET L_45ba33
          mov DWORD PTR [ESP+4],OFFSET L_45b4a7
          mov DWORD PTR [ESP],EAX
          call FUN_449158
          jmp L_430eb1
          .byte 0x66
          .byte 0x90
L_430f80:
          mov DWORD PTR [ESP+4],OFFSET L_45b9e3
          mov DWORD PTR [ESP],ESI
          call FUN_433690
          mov EAX,DWORD PTR [L_479f0c]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],EAX
          call FUN_40d370
          mov EAX,DWORD PTR [L_479f0c]
          mov DWORD PTR [ESP],OFFSET L_45b9f6
          mov DWORD PTR [ESP+4],EAX
          call FUN_430660
          jmp L_430ea5
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_430fc0:
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],OFFSET L_45ba4c
          call FUN_430660
          jmp L_430eec
L_430fd5:
          add ESP,48
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x66
          .byte 0x90
FUN_430fe0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,28
          mov EAX,DWORD PTR [L_479580]
          mov DWORD PTR [ESP+4],16
          mov EBX,DWORD PTR [ESP+48]
          mov EDI,DWORD PTR [ESP+52]
          add EAX,256
          mov DWORD PTR [ESP],EAX
          call FUN_422ae0
          cmp EAX,2435
          mov ESI,DWORD PTR [L_479580]
          je L_4316a2
L_43101a:
          add ESI,32
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],ESI
          call FUN_4223b0
          test EAX,EAX
          je L_431422
L_431035:
          mov EDX,DWORD PTR [L_47957c]
          mov EAX,DWORD PTR [L_479580]
          test EDX,EDX
          je L_431061
          movzx EAX,BYTE PTR [EAX+28]
          mov DWORD PTR [ESP+4],OFFSET L_45b4b2
          mov DWORD PTR [ESP],EDX
          mov DWORD PTR [ESP+8],EAX
          call FUN_449158
          mov EAX,DWORD PTR [L_479580]
L_431061:
          add EAX,48
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],EAX
          call FUN_4223b0
          test EAX,EAX
          je L_431371
L_43107c:
          mov EAX,DWORD PTR [L_479580]
          mov DWORD PTR [ESP+4],16
          add EAX,256
          mov DWORD PTR [ESP],EAX
          call FUN_422ae0
          mov DWORD PTR [ESP+4],OFFSET L_45bb12
          mov DWORD PTR [ESP],EBX
          mov ESI,EAX
          call FUN_433690
          mov EAX,DWORD PTR [L_479580]
          mov DWORD PTR [ESP],EBX
          lea EDX,DWORD PTR [EAX+256]
          mov DWORD PTR [ESP+4],EDX
          call FUN_423370
          cmp ESI,2435
          mov EDX,OFFSET L_45bacc
          mov EAX,OFFSET L_45bad1
          cmove EAX,EDX
          mov DWORD PTR [ESP+4],OFFSET L_45bb25
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],EAX
          call FUN_433690
          mov DWORD PTR [ESP+4],OFFSET L_45bb2c
          mov DWORD PTR [ESP],EBX
          call FUN_433690
          mov EAX,DWORD PTR [L_479580]
          mov DWORD PTR [ESP+4],96
          add EAX,64
          mov DWORD PTR [ESP],EAX
          call FUN_4223b0
          test EAX,EAX
          jne L_4312f5
          mov EAX,DWORD PTR [L_479580]
          mov DWORD PTR [ESP+4],OFFSET L_45bb3f
          mov DWORD PTR [ESP],EBX
          add EAX,64
          mov DWORD PTR [ESP+8],EAX
          call FUN_4232e0
L_431132:
          mov DWORD PTR [ESP+4],OFFSET L_45bb54
          mov DWORD PTR [ESP],EBX
          call FUN_433690
          mov EAX,DWORD PTR [L_479580]
          mov DWORD PTR [ESP+4],96
          add EAX,160
          mov DWORD PTR [ESP],EAX
          call FUN_4223b0
          test EAX,EAX
          jne L_4312e0
          mov EAX,DWORD PTR [L_479580]
          mov DWORD PTR [ESP+4],OFFSET L_45bb3f
          mov DWORD PTR [ESP],EBX
          add EAX,160
          mov DWORD PTR [ESP+8],EAX
          call FUN_4232e0
L_431182:
          mov EAX,DWORD PTR [L_479580]
          mov DWORD PTR [ESP+4],272
          add EAX,272
          mov DWORD PTR [ESP],EAX
          call FUN_422ae0
          cmp EAX,31175
          je L_431590
          mov DWORD PTR [ESP+8],OFFSET L_45bad1
          mov DWORD PTR [ESP+4],OFFSET L_45bbb8
          mov DWORD PTR [ESP],EBX
          call FUN_433690
          mov EAX,DWORD PTR [L_479580]
L_4311c4:
          add EAX,544
          mov DWORD PTR [ESP+4],272
          mov DWORD PTR [ESP],EAX
          call FUN_422ae0
          cmp EAX,32976
          je L_4314f0
          mov DWORD PTR [ESP+8],OFFSET L_45bad1
          mov DWORD PTR [ESP+4],OFFSET L_45bbce
          mov DWORD PTR [ESP],EBX
          call FUN_433690
          mov EAX,DWORD PTR [L_479580]
          mov DWORD PTR [ESP+4],272
          add EAX,816
          mov DWORD PTR [ESP],EAX
          call FUN_422ae0
          cmp EAX,33852
          je L_4315f4
          mov DWORD PTR [ESP+8],OFFSET L_45bad1
          mov DWORD PTR [ESP+4],OFFSET L_45bb80
          mov DWORD PTR [ESP],EBX
          call FUN_433690
          test EDI,EDI
          je L_43127f
L_43123d:
          mov EAX,DWORD PTR [L_479580]
          mov DWORD PTR [ESP+4],96
          add EAX,64
          mov DWORD PTR [ESP],EAX
          call FUN_4223b0
          test EAX,EAX
          je L_431350
L_43125d:
          mov EAX,DWORD PTR [L_479580]
          mov DWORD PTR [ESP+4],96
          add EAX,160
          mov DWORD PTR [ESP],EAX
          call FUN_4223b0
          test EAX,EAX
          je L_431310
L_43127f:
          mov EDI,DWORD PTR [ESP+56]
          test EDI,EDI
          je L_43133a
L_43128b:
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],OFFSET L_45baf6
          call FUN_433690
          mov EAX,DWORD PTR [L_479580]
          mov DWORD PTR [ESP],EBX
          add EAX,32
          mov DWORD PTR [ESP+4],EAX
          call FUN_41b120
          mov EBX,EAX
          mov EAX,DWORD PTR [L_479580]
          add EAX,256
          mov DWORD PTR [ESP],EAX
          call FUN_41b600
          xor EDX,EDX
          cmp EAX,1
          je L_431690
          add ESP,28
          mov EAX,EDX
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
L_4312e0:
          mov DWORD PTR [ESP+4],OFFSET L_45bb47
          mov DWORD PTR [ESP],EBX
          call FUN_433690
          jmp L_431182
L_4312f5:
          mov DWORD PTR [ESP+4],OFFSET L_45bb47
          mov DWORD PTR [ESP],EBX
          call FUN_433690
          jmp L_431132
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_431310:
          mov EAX,DWORD PTR [L_479580]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],OFFSET L_45bbad
          add EAX,160
          mov DWORD PTR [ESP+8],EAX
          call FUN_420f10
          mov EDI,DWORD PTR [ESP+56]
          test EDI,EDI
          jne L_43128b
L_43133a:
          add ESP,28
          mov EDX,1
          pop EBX
          mov EAX,EDX
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
L_431350:
          mov EAX,DWORD PTR [L_479580]
          mov DWORD PTR [ESP+4],OFFSET L_45bba3
          mov DWORD PTR [ESP],EDI
          add EAX,64
          mov DWORD PTR [ESP+8],EAX
          call FUN_420f10
          jmp L_43125d
L_431371:
          mov EAX,DWORD PTR [L_47957c]
          mov ESI,DWORD PTR [L_479580]
          test EAX,EAX
          lea EBP,DWORD PTR [ESI+48]
          je L_4313e9
          mov DWORD PTR [ESP+8],OFFSET L_45baf8
          mov DWORD PTR [ESP+4],OFFSET L_45b4c0
          add ESI,64
          mov DWORD PTR [ESP],EAX
          call FUN_449158
          .byte 0x66   # nop
          nop
L_4313a0:
          movzx EAX,BYTE PTR [EBP]
          mov DWORD PTR [ESP+4],OFFSET L_45b4c6
          add EBP,1
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [L_47957c]
          mov DWORD PTR [ESP],EAX
          call FUN_449158
          cmp ESI,EBP
          jne L_4313a0
          mov EAX,DWORD PTR [L_47957c]
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],OFFSET L_45b4cb
          mov DWORD PTR [ESP+12],EAX
          call FUN_449118
L_4313e9:
          mov DWORD PTR [ESP+4],OFFSET L_45baff
          mov DWORD PTR [ESP],EBX
          call FUN_433690
          mov EAX,DWORD PTR [L_479580]
          mov DWORD PTR [ESP],EBX
          add EAX,48
          mov DWORD PTR [ESP+4],EAX
          call FUN_423370
          mov DWORD PTR [ESP+4],OFFSET L_45baf6
          mov DWORD PTR [ESP],EBX
          call FUN_433690
          jmp L_43107c
L_431422:
          mov EAX,DWORD PTR [L_47957c]
          mov ESI,DWORD PTR [L_479580]
          test EAX,EAX
          lea EBP,DWORD PTR [ESI+32]
          je L_431499
          mov DWORD PTR [ESP+8],OFFSET L_45badc
          mov DWORD PTR [ESP+4],OFFSET L_45b4c0
          add ESI,48
          mov DWORD PTR [ESP],EAX
          call FUN_449158
          nop
L_431450:
          movzx EAX,BYTE PTR [EBP]
          mov DWORD PTR [ESP+4],OFFSET L_45b4c6
          add EBP,1
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [L_47957c]
          mov DWORD PTR [ESP],EAX
          call FUN_449158
          cmp ESI,EBP
          jne L_431450
          mov EAX,DWORD PTR [L_47957c]
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],OFFSET L_45b4cb
          mov DWORD PTR [ESP+12],EAX
          call FUN_449118
L_431499:
          mov DWORD PTR [ESP+4],OFFSET L_45bae3
          mov DWORD PTR [ESP],EBX
          call FUN_433690
          mov EAX,DWORD PTR [L_479580]
          mov DWORD PTR [ESP],EBX
          add EAX,32
          mov DWORD PTR [ESP+4],EAX
          call FUN_423370
          mov EAX,DWORD PTR [L_479580]
          mov DWORD PTR [ESP],EBX
          add EAX,32
          mov DWORD PTR [ESP+4],EAX
          call FUN_41ae40
          mov DWORD PTR [ESP+4],OFFSET L_45baf6
          mov DWORD PTR [ESP],EBX
          call FUN_433690
          jmp L_431035
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_4314f0:
          mov DWORD PTR [ESP+8],OFFSET L_45bacc
          mov DWORD PTR [ESP+4],OFFSET L_45bbce
          mov DWORD PTR [ESP],EBX
          call FUN_433690
          mov ECX,DWORD PTR [ESP+56]
          mov EAX,DWORD PTR [L_479580]
          test ECX,ECX
          je L_431521
          lea EDX,DWORD PTR [EAX+544]
          mov DWORD PTR [L_47a144],EDX
L_431521:
          test EDI,EDI
          je L_431650
          add EAX,544
          mov DWORD PTR [ESP+12],272
          mov DWORD PTR [ESP+4],OFFSET L_45bb73
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],EDI
          call FUN_420d80
          mov EAX,DWORD PTR [L_479580]
          mov DWORD PTR [ESP+4],272
          add EAX,816
          mov DWORD PTR [ESP],EAX
          call FUN_422ae0
          cmp EAX,33852
          je L_431730
          mov DWORD PTR [ESP+8],OFFSET L_45bad1
          mov DWORD PTR [ESP+4],OFFSET L_45bb80
          mov DWORD PTR [ESP],EBX
          call FUN_433690
          jmp L_43123d
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_431590:
          mov DWORD PTR [ESP+8],OFFSET L_45bacc
          mov DWORD PTR [ESP+4],OFFSET L_45bbb8
          mov DWORD PTR [ESP],EBX
          call FUN_433690
          mov ESI,DWORD PTR [ESP+56]
          mov EAX,DWORD PTR [L_479580]
          test ESI,ESI
          je L_4315c1
          lea EDX,DWORD PTR [EAX+272]
          mov DWORD PTR [L_47a13c],EDX
L_4315c1:
          test EDI,EDI
          je L_4311c4
          add EAX,272
          mov DWORD PTR [ESP+12],272
          mov DWORD PTR [ESP+4],OFFSET L_45bb67
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],EDI
          call FUN_420d80
          mov EAX,DWORD PTR [L_479580]
          jmp L_4311c4
L_4315f4:
          mov DWORD PTR [ESP+8],OFFSET L_45bacc
          mov DWORD PTR [ESP+4],OFFSET L_45bb80
          mov DWORD PTR [ESP],EBX
          call FUN_433690
          mov EBP,DWORD PTR [ESP+56]
          test EBP,EBP
          je L_431764
          mov EAX,DWORD PTR [L_479580]
          add EAX,816
          test EDI,EDI
          mov DWORD PTR [L_47a140],EAX
          je L_43128b
L_43162f:
          mov DWORD PTR [ESP+12],272
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_45bb96
          mov DWORD PTR [ESP],EDI
          call FUN_420d80
          jmp L_43123d
L_431650:
          add EAX,816
          mov DWORD PTR [ESP+4],272
          mov DWORD PTR [ESP],EAX
          call FUN_422ae0
          cmp EAX,33852
          je L_431780
          mov DWORD PTR [ESP+8],OFFSET L_45bad1
          mov DWORD PTR [ESP+4],OFFSET L_45bb80
          mov DWORD PTR [ESP],EBX
          call FUN_433690
          jmp L_43127f
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_431690:
          xor EDX,EDX
          cmp EBX,1
          sete DL
          add ESP,28
          pop EBX
          mov EAX,EDX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_4316a2:
          mov EAX,DWORD PTR [L_47957c]
          lea EBP,DWORD PTR [ESI+256]
          test EAX,EAX
          je L_43101a
          mov DWORD PTR [ESP+8],OFFSET L_45bad5
          mov DWORD PTR [ESP+4],OFFSET L_45b4c0
          add ESI,272
          mov DWORD PTR [ESP],EAX
          call FUN_449158
L_4316d3:
          movzx EAX,BYTE PTR [EBP]
          mov DWORD PTR [ESP+4],OFFSET L_45b4c6
          add EBP,1
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [L_47957c]
          mov DWORD PTR [ESP],EAX
          call FUN_449158
          cmp ESI,EBP
          jne L_4316d3
          mov EAX,DWORD PTR [L_47957c]
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],OFFSET L_45b4cb
          mov DWORD PTR [ESP+12],EAX
          call FUN_449118
          mov ESI,DWORD PTR [L_479580]
          jmp L_43101a
L_431727:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_431730:
          mov DWORD PTR [ESP+8],OFFSET L_45bacc
          mov DWORD PTR [ESP+4],OFFSET L_45bb80
          mov DWORD PTR [ESP],EBX
          call FUN_433690
          mov EDX,DWORD PTR [ESP+56]
          test EDX,EDX
          je L_43176c
          mov EAX,DWORD PTR [L_479580]
          add EAX,816
          mov DWORD PTR [L_47a140],EAX
          jmp L_43162f
L_431764:
          test EDI,EDI
          je L_43133a
L_43176c:
          mov EAX,DWORD PTR [L_479580]
          add EAX,816
          jmp L_43162f
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_431780:
          mov DWORD PTR [ESP+8],OFFSET L_45bacc
          mov DWORD PTR [ESP+4],OFFSET L_45bb80
          mov DWORD PTR [ESP],EBX
          call FUN_433690
          mov EAX,DWORD PTR [ESP+56]
          test EAX,EAX
          je L_43133a
          mov EAX,DWORD PTR [L_479580]
          add EAX,816
          mov DWORD PTR [L_47a140],EAX
          jmp L_43128b
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_4317c0:
          push ESI
          push EBX
          sub ESP,36
          mov EBX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+4],OFFSET L_45bbf0
          mov ESI,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP],EBX
          call FUN_433690
          mov EAX,DWORD PTR [L_479580]
          mov EAX,DWORD PTR [EAX+4]
          mov DWORD PTR [ESP+4],OFFSET L_45bc08
          mov DWORD PTR [ESP],EBX
          mov EDX,EAX
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
          call FUN_433690
          mov EAX,DWORD PTR [L_479580]
          mov EAX,DWORD PTR [EAX+12]
          and EAX,15
          add EAX,1
          mov DWORD PTR [ESP],EAX
          call FUN_420a90
          mov DWORD PTR [ESP+4],OFFSET L_45bc27
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],EBX
          call FUN_433690
          mov EAX,DWORD PTR [L_479580]
          mov EAX,DWORD PTR [EAX+16]
          shr EAX,28
          add EAX,1
          mov DWORD PTR [ESP],EAX
          call FUN_420a90
          mov DWORD PTR [ESP+4],OFFSET L_45bc3d
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],EBX
          call FUN_433690
          mov EAX,DWORD PTR [L_479580]
          mov EAX,DWORD PTR [EAX+16]
          mov DWORD PTR [ESP+4],OFFSET L_45bc53
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],EAX
          call FUN_433690
          mov EAX,DWORD PTR [L_479580]
          mov EDX,OFFSET L_45bbe4
          test BYTE PTR [EAX+16],32
          mov EAX,OFFSET L_45bb3f
          mov DWORD PTR [ESP+4],OFFSET L_45bc6d
          mov DWORD PTR [ESP],EBX
          cmove EAX,EDX
          mov DWORD PTR [ESP+8],EAX
          call FUN_433690
          mov EAX,DWORD PTR [L_479580]
          test BYTE PTR [EAX+16],32
          je L_4318cc
          test ESI,ESI
          je L_4318cc
          mov DWORD PTR [ESI],1
L_4318cc:
          add ESP,36
          pop EBX
          pop ESI
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
FUN_4318e0:
          sub ESP,28
          mov EAX,DWORD PTR [L_479580]
          mov DWORD PTR [L_479ec0],0
          mov DWORD PTR [ESP+4],16
          add EAX,1088
          mov DWORD PTR [ESP],EAX
          call FUN_4223b0
          test EAX,EAX
          je L_431a40
L_43190f:
          mov EAX,DWORD PTR [L_479580]
          mov DWORD PTR [ESP+4],16
          add EAX,1104
          mov DWORD PTR [ESP],EAX
          call FUN_4223b0
          test EAX,EAX
          je L_431a20
L_431931:
          mov EAX,DWORD PTR [L_479580]
          mov DWORD PTR [ESP+4],16
          add EAX,1120
          mov DWORD PTR [ESP],EAX
          call FUN_4223b0
          test EAX,EAX
          je L_431a00
L_431953:
          mov EAX,DWORD PTR [L_479580]
          mov DWORD PTR [ESP+4],16
          add EAX,1136
          mov DWORD PTR [ESP],EAX
          call FUN_4223b0
          test EAX,EAX
          je L_4319e0
L_431971:
          mov EAX,DWORD PTR [L_479580]
          mov DWORD PTR [ESP+4],16
          add EAX,1152
          mov DWORD PTR [ESP],EAX
          call FUN_4223b0
          test EAX,EAX
          je L_4319c3
L_43198f:
          mov EAX,DWORD PTR [L_479580]
          mov DWORD PTR [ESP+4],16
          add EAX,1168
          mov DWORD PTR [ESP],EAX
          call FUN_4223b0
          test EAX,EAX
          jne L_4319bf
          mov EAX,DWORD PTR [L_479580]
          add EAX,1168
          mov DWORD PTR [ESP],EAX
          call FUN_41ad60
L_4319bf:
          add ESP,28
          ret 
L_4319c3:
          mov EAX,DWORD PTR [L_479580]
          add EAX,1152
          mov DWORD PTR [ESP],EAX
          call FUN_41ad30
          jmp L_43198f
L_4319d7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_4319e0:
          mov EAX,DWORD PTR [L_479580]
          add EAX,1136
          mov DWORD PTR [ESP],EAX
          call FUN_41ad00
          .byte 0xe9; .long L_431971-.-4   # jmp L_431971
L_4319f7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_431a00:
          mov EAX,DWORD PTR [L_479580]
          add EAX,1120
          mov DWORD PTR [ESP],EAX
          call FUN_41acd0
          jmp L_431953
L_431a17:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_431a20:
          mov EAX,DWORD PTR [L_479580]
          add EAX,1104
          mov DWORD PTR [ESP],EAX
          call FUN_41aca0
          jmp L_431931
L_431a37:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_431a40:
          mov EAX,DWORD PTR [L_479580]
          add EAX,1088
          mov DWORD PTR [ESP],EAX
          call FUN_41ac70
          jmp L_43190f
L_431a57:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_431a60:
          push ESI
          push EBX
          sub ESP,20
          mov EBX,DWORD PTR [ESP+32]
          mov ESI,DWORD PTR [ESP+44]
          call FUN_41fe10
          mov DWORD PTR [ESP+4],OFFSET L_45bc84
          mov DWORD PTR [L_479580],EAX
          mov DWORD PTR [ESP],EBX
          call FUN_433690
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EBX
          call FUN_4317c0
          mov EAX,DWORD PTR [L_479580]
          test ESI,ESI
          mov EAX,DWORD PTR [EAX]
          je L_431aa6
          cmp AL,1
          jbe L_431bc5
L_431aa6:
          xor AL,AL
          cmp EAX,767
          jbe L_431b10
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP],EAX
          call FUN_430460
          mov EAX,DWORD PTR [L_479580]
          mov EDX,DWORD PTR [EAX+24]
          mov DWORD PTR [ESP+12],EDX
          mov EDX,DWORD PTR [EAX+20]
          mov DWORD PTR [ESP+8],EDX
          mov EAX,DWORD PTR [EAX+12]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call FUN_4308d0
          test EAX,EAX
          jne L_431b30
L_431ae1:
          xor EBX,EBX
L_431ae3:
          mov EAX,DWORD PTR [L_47957c]
          test EAX,EAX
          je L_431b01
L_431aec:
          mov DWORD PTR [ESP],EAX
          call FUN_449180
          mov EAX,DWORD PTR [L_47957c]
          mov DWORD PTR [ESP],EAX
          call _fclose
L_431b01:
          add ESP,20
          mov EAX,EBX
          pop EBX
          pop ESI
          ret 
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_431b10:
          mov DWORD PTR [ESP+4],OFFSET L_45bd4c
          mov DWORD PTR [ESP],0
          xor EBX,EBX
          call FUN_433690
          add ESP,20
          mov EAX,EBX
          pop EBX
          pop ESI
          ret 
          .byte 0x66
          .byte 0x90
L_431b30:
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call FUN_430fe0
          test EAX,EAX
          je L_431ae1
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call FUN_430e00
          test EAX,EAX
          je L_431ae1
          mov EAX,DWORD PTR [L_479580]
          mov EAX,DWORD PTR [EAX+28]
          mov DWORD PTR [ESP+4],OFFSET L_45bd81
          mov DWORD PTR [ESP],EBX
          mov BYTE PTR [L_479f15],AL
          movzx EAX,AL
          mov DWORD PTR [ESP+8],EAX
          call FUN_433690
          mov EAX,DWORD PTR [L_479580]
          mov EAX,DWORD PTR [EAX+28]
          mov DWORD PTR [ESP+4],OFFSET L_45bd97
          mov DWORD PTR [ESP],EBX
          shr EAX,8
          mov DWORD PTR [ESP+8],EAX
          call FUN_433690
          test ESI,ESI
          je L_431c01
          mov EAX,DWORD PTR [L_479580]
          mov EAX,DWORD PTR [EAX+28]
          shr EAX,8
          mov DWORD PTR [ESP],EAX
          call FUN_41ade0
L_431bb6:
          call FUN_4318e0
          mov EBX,1
          jmp L_431ae3
L_431bc5:
          mov DWORD PTR [ESP+4],OFFSET L_45bcb4
          mov DWORD PTR [ESP],0
          xor EBX,EBX
          call FUN_433690
          mov DWORD PTR [ESP+4],OFFSET L_45bd04
          mov DWORD PTR [ESP],0
          call FUN_433690
          mov EAX,DWORD PTR [L_47957c]
          test EAX,EAX
          jne L_431aec
          jmp L_431b01
L_431c01:
          mov DWORD PTR [ESP+4],OFFSET L_45baf6
          mov DWORD PTR [ESP],EBX
          call FUN_433690
          jmp L_431bb6
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

.section .rdata,"dr"
.p2align 2
L_45b4a4:
          .string "wb"
L_45b4a7:
          .string "%s = %s;\n\n"
L_45b4b2:
          .string "cfldv = %d;\n\n"
L_45b4c0:
          .string "%s = "
L_45b4c6:
          .string "%02X"
L_45b4cb:
          .string "\n\n"
          .zero 2
L_45b4d0:
          .string "%s = power; console power button\n\n"
          .zero 1
L_45b4f4:
          .string "%s = remopower; IR power button\n\n"
          .zero 2
L_45b518:
          .string "%s = remox; IR guide/X button\n\n"
L_45b538:
          .string "%s = winbutton; IR windows button\n\n"
L_45b55c:
          .string "%s = kiosk; KIOSK debug pin\n\n"
          .zero 2
L_45b57c:
          .string "%s = wirelessx; wireless controller\n\n"
          .zero 2
L_45b5a4:
          .string "%s = wiredxb1; wired controller (rear top usb port)\n\n"
          .zero 2
L_45b5dc:
          .string "%s = wiredxb1; wired controller (INVALID FOR FATS!!)\n\n"
          .zero 1
L_45b614:
          .string "%s = wiredxb2; wired controller (rear middle usb port)\n\n"
          .zero 3
L_45b650:
          .string "%s = wiredxb2; wired controller (INVALID FOR FATS!!)\n\n"
          .zero 1
L_45b688:
          .string "%s = wiredxb3; wired controller (rear bottom usb port)\n\n"
          .zero 3
L_45b6c4:
          .string "%s = wiredxb3; wired controller (rear usb port)\n\n"
          .zero 2
L_45b6f8:
          .string "%s = wiredxf1; wired controller (front left usb port)\n\n"
L_45b730:
          .string "%s = wiredxf1; wired controller (front top usb port)\n\n"
          .zero 1
L_45b768:
          .string "%s = wiredxf2; wired controller (front right usb port)\n\n"
          .zero 3
L_45b7a4:
          .string "%s = wiredxf2; wired controller (front bottom usb port)\n\n"
          .zero 2
L_45b7e0:
          .string "%s = eject; console eject button\n\n"
          .zero 1
L_45b804:
          .long L_430684
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_4306d0
          .long L_430830
          .long L_4306f0
          .long L_430830
          .long L_430710
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430730
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430830
          .long L_430750
          .long L_430770
          .long L_4307a0
          .long L_4307d0
          .long L_430800
          .long L_4306a5
L_45b92c:
          .string "Image Type      : %s ("
L_45b943:
          .string "JTAG"
L_45b948:
          .string "Glitch2"
L_45b950:
          .string "Glitch"
L_45b957:
          .string "-FAT"
L_45b95c:
          .string "Glitch2M"
L_45b965:
          .string ")\n"
L_45b968:
          .string "type"
          .zero 3
L_45b970:
          .string "retrieving USVR\\freeboot_bin..."
L_45b990:
          .string "freeboot_bin"
          .zero 3
L_45b9a0:
          .string "parsing freeboot 0.08 core for opts\n"
L_45b9c5:
          .string "Xell Reason     : "
L_45b9d8:
          .string "xellbutton"
L_45b9e3:
          .string "Xell Alt Reason : "
L_45b9f6:
          .string "xellbutton2"
          .zero 2
L_45ba04:
          .string "UART speed      : cygnos/demon speed set\n"
L_45ba2e:
          .string "true"
L_45ba33:
          .string "cygnos"
L_45ba3a:
          .string "DualBoot Reason :"
L_45ba4c:
          .string "dualboot"
          .zero 3
L_45ba58:
          .string "\n*****WARNING: unrecognized freeboot binary on console! Using default options for xell/uart speed!\n"
L_45babc:
          .string "flash_hdr"
L_45bac6:
          .string "nodvd"
L_45bacc:
          .string "good"
L_45bad1:
          .string "bad"
L_45bad5:
          .string "1blkey"
L_45badc:
          .string "cpukey"
L_45bae3:
          .string "CPU key         : "
L_45baf6:
          .string "\n"
L_45baf8:
          .string "dvdkey"
L_45baff:
          .string "DVD key         : "
L_45bb12:
          .string "1BL key         : "
L_45bb25:
          .string " (%s)\n"
L_45bb2c:
          .string "Fuses           : "
L_45bb3f:
          .string "present"
L_45bb47:
          .string "not present\n"
L_45bb54:
          .string "Virtual Fuses   : "
L_45bb67:
          .string "1BL_pub.bin"
L_45bb73:
          .string "PIRS_pub.bin"
L_45bb80:
          .string "MASTER RSA pub  : %s\n"
L_45bb96:
          .string "MAST_pub.bin"
L_45bba3:
          .string "fuses.txt"
L_45bbad:
          .string "vfuses.txt"
L_45bbb8:
          .string "1BL RSA pub     : %s\n"
L_45bbce:
          .string "PIRS RSA pub    : %s\n"
L_45bbe4:
          .string "not present"
L_45bbf0:
          .string "Console Current Info:\n"
          .zero 1
L_45bc08:
          .string "running kernel  : %d.%d.%d.%d\n"
L_45bc27:
          .string "bootstrap type  : %s\n"
L_45bc3d:
          .string "hardware type   : %s\n"
L_45bc53:
          .string "hardware flags  : 0x%08x\n"
L_45bc6d:
          .string "internal HDD    : %s\n"
          .zero 1
L_45bc84:
          .string "\n------ parsing console info response ------\n"
          .zero 2
L_45bcb4:
          .string "\n*****ERROR: console hv patches are not recent enough to support update mode!\n"
          .zero 1
L_45bd04:
          .string "\n            update console patches and reboot before trying again.\n"
          .zero 3
L_45bd4c:
          .string "\n*****ERROR: updsvr on console needs to be updated!\n"
L_45bd81:
          .string "CF LDV          : %d\n"
L_45bd97:
          .string "Pairing Value   : 0x%06x "
          .zero 3

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
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_430460 - .
          .byte 0xd4
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
          .byte 0x2
          .byte 0x2
          .byte 0xc9
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
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x48
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_430540 - .
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x4c
          .byte 0xe
          .byte 0x20
          .byte 0x58
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x60
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_430570 - .
          .byte 0x31
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x4c
          .byte 0xe
          .byte 0x20
          .byte 0x63
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x78
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_4305b0 - .
          .byte 0x2c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x68
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x90
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_4305e0 - .
          .byte 0x7f
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x4a
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
          .byte 0x2
          .byte 0x6d
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
          .byte 0x18
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xbc
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_430660 - .
          .byte 0x65
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x4d
          .byte 0xe
          .byte 0x20
          .byte 0x76
          .byte 0xe
          .byte 0x4
          .byte 0x42
          .byte 0xe
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd8
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_4308d0 - .
          .byte 0x84
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
          .byte 0x2
          .byte 0xd7
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
          .byte 0x6c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x18
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_430b60 - .
          .byte 0x93
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
          .byte 0x50
          .byte 0x2
          .byte 0x67
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
          .byte 0x3
          .byte 0x25
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
          .byte 0x43
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
          .byte 0x45
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x88
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_430e00 - .
          .byte 0xde
          .byte 0x1
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
          .byte 0x40
          .byte 0x2
          .byte 0xf6
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
          .byte 0x77
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
          .byte 0x46
          .byte 0xb
          .byte 0x2
          .byte 0x98
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
          .byte 0x6c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xe0
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_430fe0 - .
          .byte 0xd8
          .byte 0x7
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
          .byte 0x3
          .byte 0xea
          .byte 0x2
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
          .byte 0x5d
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x46
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
          .byte 0x48
          .byte 0xb
          .byte 0x3
          .byte 0x4b
          .byte 0x3
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x41
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
          .byte 0x0
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x50
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long FUN_4317c0 - .
          .byte 0x12
          .byte 0x1
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
          .byte 0x1
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
          .byte 0x18
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x7c
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long FUN_4318e0 - .
          .byte 0x77
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x2
          .byte 0xdf
          .byte 0xa
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x0
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x98
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long FUN_431a60 - .
          .byte 0xb3
          .byte 0x1
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
          .byte 0x2
          .byte 0x9f
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
          .byte 0x48
          .byte 0xb
          .byte 0x59
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
          .byte 0x43
          .byte 0xb
          .byte 0x0

.bss
.p2align 2
L_47957c:
          .zero 4
L_479580:
          .zero 32

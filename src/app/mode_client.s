# app/mode_client.s -- "Usage: %s client", network read/write of NAND
#
# original placement:
#   .bss           0046f160-0046f180
#   .eh_frame      00465b68-00466040
#   .rdata         0044e10c-0044fb60
#   .rdata$zzz     004637fc-00463828
#   .text          00406330-00408ec0

.intel_syntax noprefix
.globl FUN_408260

.text
.p2align 4
FUN_406330:
          sub ESP,28
          mov EAX,DWORD PTR [ESP+32]
          cmp EAX,5
          ja L_406360
          jmp DWORD PTR [EAX*4+L_44eba8]
L_406343:
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+4],OFFSET L_44e1a8
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          nop
L_406360:
          mov DWORD PTR [ESP+4],OFFSET L_44a4e0
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+8],OFFSET L_44e273
          mov DWORD PTR [ESP+4],OFFSET L_44e27c
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44e2a9
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+8],OFFSET L_44e273
          mov DWORD PTR [ESP+4],OFFSET L_44e2b4
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+8],OFFSET L_44e273
          mov DWORD PTR [ESP+4],OFFSET L_44e2d4
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44e305
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44e314
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44e35c
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44e3c0
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44e3f8
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44e434
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44e4a4
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44e4fc
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44e560
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44e590
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44e5d4
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44e630
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44e684
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44e6d8
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44e720
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44e748
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44e798
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44e7dc
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44e814
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44e850
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44e876
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44e880
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44e8d4
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44e928
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44e95c
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44e9b0
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44e9d8
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44ea04
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44ea50
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44ea58
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44eaa8
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44eaf8
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44eb40
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44a4e0
          mov DWORD PTR [ESP],0
          call _log_printf
          call _log_finish
          mov EAX,DWORD PTR [L_44a524]
          test EAX,EAX
          jne L_40669e
L_406692:
          mov DWORD PTR [ESP],1
          call FUN_449198
L_40669e:
          mov DWORD PTR [ESP+4],OFFSET L_44eb8b
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [_iob]
          mov DWORD PTR [ESP],EAX
          call FUN_449178
          jmp L_406692
L_4066c1:
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+4],OFFSET L_44e1f4
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          jmp L_406360
L_4066e2:
          mov DWORD PTR [ESP+4],OFFSET L_44e234
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_406360
L_4066fb:
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+4],OFFSET L_44e10c
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          jmp L_406360
L_40671c:
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+4],OFFSET L_44e158
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          jmp L_406360
          .byte 0x8d
          .byte 0x76
          .byte 0x0
FUN_406740:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,1068
          mov ESI,DWORD PTR [ESP+1088]
          test ESI,ESI
          je L_406879
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_44ebc0
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP],ESI
          call _createDir
          test EAX,EAX
          je L_406861
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],0
          call FUN_431a60
          lea EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EAX
          call FUN_420420
          test EAX,EAX
          mov EDI,EAX
          je L_4067bb
          mov EAX,DWORD PTR [ESP+28]
          test EAX,EAX
          jne L_406952
L_4067bb:
          lea EBX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EBX
          call _strcpy
          mov EDX,EBX
L_4067cd:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_4067cd
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          mov ECX,110
          sbb EDX,3
          mov DWORD PTR [EDX],1851878959
          mov DWORD PTR [EDX+4],1836409956
          mov DWORD PTR [EDX+8],1768042096
          mov WORD PTR [EDX+12],CX
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_44ec18
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP],EBX
          call FUN_41fe20
          test EAX,EAX
          je L_406933
          mov DWORD PTR [ESP+4],OFFSET L_44ec35
          mov DWORD PTR [ESP],0
          call _log_printf
L_406856:
          add ESP,1068
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_406861:
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_44ebe8
          mov DWORD PTR [ESP],0
          call _log_printf
L_406879:
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],0
          call FUN_431a60
          lea EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EAX
          call FUN_420420
          test EAX,EAX
          mov EDI,EAX
          je L_406856
          mov EDX,DWORD PTR [ESP+28]
          test EDX,EDX
          je L_406856
          mov DWORD PTR [ESP+4],OFFSET L_44ec48
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EBX,DWORD PTR [ESP+28]
          sub EBX,2
          js L_406856
          xor EBP,EBP
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_4068e0:
          lea EAX,DWORD PTR [EDI+EBX*1]
          mov DWORD PTR [ESP],EAX
          call _getBeU16
          movzx EAX,AX
          mov DWORD PTR [ESP+4],OFFSET L_44ec11
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          test EBX,EBX
          je L_406926
          mov DWORD PTR [ESP+4],OFFSET L_44ec16
          mov DWORD PTR [ESP],0
          sub EBX,2
          call _log_printf
          cmp EBX,-1
          jne L_4068e0
L_406926:
          test EBP,EBP
          jne L_4067bb
          jmp L_406856
L_406933:
          mov DWORD PTR [ESP+4],OFFSET L_44ec3f
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,1068
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_406952:
          mov DWORD PTR [ESP+4],OFFSET L_44ec48
          mov DWORD PTR [ESP],0
          mov EBP,ESI
          call _log_printf
          mov EBX,DWORD PTR [ESP+28]
          sub EBX,2
          jns L_4068e0
          jmp L_4067bb
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_406980:
          push ESI
          push EBX
          sub ESP,36
          mov EBX,DWORD PTR [ESP+48]
          call FUN_41ed50
          mov DWORD PTR [ESP+4],OFFSET L_44ec5b
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EBX
          call _log_printf
          lea EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call _FileToBuffer
          test EAX,EAX
          je L_406a50
          mov EBX,EAX
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+4],OFFSET L_44ec6e
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov DWORD PTR [ESP],EBX
          call _getBeU16
          cmp AX,65359
          je L_406a20
          mov DWORD PTR [ESP],EBX
          xor ESI,ESI
          call _getBeU16
          movzx EAX,AX
          mov DWORD PTR [ESP+4],OFFSET L_44ecec
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
L_406a0f:
          mov DWORD PTR [ESP],EBX
          call _free
          add ESP,36
          mov EAX,ESI
          pop EBX
          pop ESI
          ret 
          .byte 0x90
L_406a20:
          mov EAX,DWORD PTR [L_46f160]
          mov EDX,DWORD PTR [ESP+28]
          mov EAX,DWORD PTR [EAX+20]
          cmp EAX,EDX
          je L_406a70
          mov DWORD PTR [ESP+12],EDX
          mov DWORD PTR [ESP+8],EAX
          xor ESI,ESI
          mov DWORD PTR [ESP+4],OFFSET L_44eca4
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_406a0f
L_406a50:
          mov DWORD PTR [ESP+4],OFFSET L_44ed30
          mov DWORD PTR [ESP],0
          xor ESI,ESI
          call _log_printf
          add ESP,36
          mov EAX,ESI
          pop EBX
          pop ESI
          ret 
          .byte 0x66
          .byte 0x90
L_406a70:
          mov DWORD PTR [ESP+4],OFFSET L_44ec88
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call FUN_41ffe0
          mov ESI,EAX
          jmp L_406a0f
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_406aa0:
          push ESI
          push EBX
          sub ESP,36
          mov EAX,DWORD PTR [L_46f160]
          mov EAX,DWORD PTR [EAX+4]
          and EAX,4294967280
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],EAX
          call FUN_432b10
          test EAX,EAX
          je L_406b51
          mov EAX,DWORD PTR [L_4ce068]
          test EAX,EAX
          jle L_406b1e
          mov EBX,OFFSET L_4ce074
          xor ESI,ESI
          nop
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_406ae0:
          mov EAX,DWORD PTR [EBX-8]
          add ESI,1
          mov DWORD PTR [ESP+20],EBX
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_44ed74
          add EBX,1032
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+16],EAX
          mov EAX,DWORD PTR [EBX-1036]
          mov DWORD PTR [ESP+12],EAX
          call _log_printf
          cmp DWORD PTR [L_4ce068],ESI
          jg L_406ae0
L_406b1e:
          mov EAX,DWORD PTR [L_4ce064]
          mov DWORD PTR [ESP+16],OFFSET L_4cdc64
          mov DWORD PTR [ESP+4],OFFSET L_44ed5c
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          add ESP,36
          pop EBX
          pop ESI
          jmp L_432aa0
L_406b51:
          add ESP,36
          pop EBX
          pop ESI
          ret 
L_406b57:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_406b60:
          push EDI
          push ESI
          push EBX
          sub ESP,16
          mov EBX,DWORD PTR [ESP+36]
          mov ESI,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],OFFSET L_44ed8d
          mov DWORD PTR [ESP],0
          mov EDI,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+8],ESI
          call _log_printf
          mov DWORD PTR [ESP],EBX
          call _FileExists
          test EAX,EAX
          jne L_406bd5
L_406b9a:
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],EAX
          call _sumBytes
          cmp DWORD PTR [ESP+48],EAX
          je L_406bf0
L_406bb0:
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_44eda8
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,16
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          ret 
L_406bd5:
          lea EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call _FileToBuffer
          jmp L_406b9a
L_406be7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_406bf0:
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_44ee04
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [ESP+44]
          cmp EAX,16
          je L_406c40
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],OFFSET L_44ee23
          call _writeFileIn
L_406c2d:
          test EAX,EAX
          .byte 0x0f,0x84; .long L_406bb0-.-4   # je L_406bb0
          add ESP,16
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_406c40:
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],OFFSET L_44ee23
          call _writeKeyFile
          jmp L_406c2d
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_406c60:
          push EBX
          sub ESP,56
          mov EAX,DWORD PTR [L_46f160]
          cmp BYTE PTR [EAX],1
          jbe L_406d92
          mov DWORD PTR [ESP+12],OFFSET L_44ee26
          mov DWORD PTR [ESP+8],OFFSET L_44ee31
          lea EBX,DWORD PTR [EAX+256]
          mov DWORD PTR [ESP+4],OFFSET L_44ed8d
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+44],16
          call _log_printf
          mov DWORD PTR [ESP],OFFSET L_44ee26
          call _FileExists
          test EAX,EAX
          jne L_406db0
L_406cb8:
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call _sumBytes
          cmp EAX,2435
          je L_406dd0
L_406cd3:
          mov DWORD PTR [ESP+12],OFFSET L_44ee26
          mov DWORD PTR [ESP+8],OFFSET L_44ee31
          mov DWORD PTR [ESP+4],OFFSET L_44eda8
          mov DWORD PTR [ESP],0
          call _log_printf
L_406cf7:
          mov EAX,DWORD PTR [L_46f160]
          mov DWORD PTR [ESP+16],31175
          mov DWORD PTR [ESP+12],272
          mov DWORD PTR [ESP+4],OFFSET L_44ee39
          mov DWORD PTR [ESP],OFFSET L_44ee45
          add EAX,272
          mov DWORD PTR [ESP+8],EAX
          call FUN_406b60
          mov EAX,DWORD PTR [L_46f160]
          mov DWORD PTR [ESP+16],32976
          mov DWORD PTR [ESP+12],272
          mov DWORD PTR [ESP+4],OFFSET L_44ee55
          mov DWORD PTR [ESP],OFFSET L_44ee62
          add EAX,544
          mov DWORD PTR [ESP+8],EAX
          call FUN_406b60
          mov EAX,DWORD PTR [L_46f160]
          mov DWORD PTR [ESP+16],33852
          mov DWORD PTR [ESP+12],272
          mov DWORD PTR [ESP+4],OFFSET L_44ee73
          mov DWORD PTR [ESP],OFFSET L_44ee80
          add EAX,816
          mov DWORD PTR [ESP+8],EAX
          call FUN_406b60
          add ESP,56
          pop EBX
          ret 
L_406d92:
          mov DWORD PTR [ESP+4],OFFSET L_44ee94
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,56
          pop EBX
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_406db0:
          lea EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],OFFSET L_44ee26
          mov DWORD PTR [ESP+4],EAX
          call _FileToBuffer
          jmp L_406cb8
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_406dd0:
          mov DWORD PTR [ESP+12],OFFSET L_44ee26
          mov DWORD PTR [ESP+8],OFFSET L_44ee31
          mov DWORD PTR [ESP+4],OFFSET L_44ee04
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [ESP+44]
          cmp EAX,16
          je L_406e30
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_44ee26
          mov DWORD PTR [ESP],OFFSET L_44ee23
          call _writeFileIn
L_406e19:
          test EAX,EAX
          jne L_406cf7
          jmp L_406cd3
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_406e30:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_44ee26
          mov DWORD PTR [ESP],OFFSET L_44ee23
          call _writeKeyFile
          jmp L_406e19
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_406e50:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,60
          cmp DWORD PTR [ESP+88],1
          mov EBX,DWORD PTR [ESP+84]
          mov DWORD PTR [ESP+44],4294967295
          jbe L_407034
          lea ESI,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+4],OFFSET L_44eee4
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+12],4
          mov DWORD PTR [ESP+8],ESI
          mov EAX,DWORD PTR [EBX]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP],EAX
          call _countInst
          cmp EAX,3
          je L_406ed0
          mov DWORD PTR [ESP+4],OFFSET L_44ef10
          mov DWORD PTR [ESP],0
          call _log_printf
L_406ebd:
          xor EAX,EAX
L_406ebf:
          add ESP,60
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_406ec7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_406ed0:
          mov DWORD PTR [ESP+12],4
          mov DWORD PTR [ESP+8],ESI
          mov EAX,DWORD PTR [EBX]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP],EAX
          call _findInst
          test EAX,EAX
          je L_406ebd
          mov EDX,DWORD PTR [ESP+80]
          sub EDX,EAX
          add EDX,DWORD PTR [EBX]
          add EAX,4
          mov DWORD PTR [ESP+12],4
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],EDX
          call _findInst
          test EAX,EAX
          mov DWORD PTR [ESP+20],EAX
          je L_406ebd
          mov EDX,DWORD PTR [ESP+80]
          lea ESI,DWORD PTR [EAX+4]
          sub EDX,ESI
          add EDX,DWORD PTR [EBX]
          cmp DWORD PTR [ESP+88],2
          je L_4070f1
          test EDX,EDX
          mov DWORD PTR [ESP+16],0
          je L_407150
L_406f43:
          mov EAX,DWORD PTR [ESP+16]
          mov ECX,DWORD PTR [ESP+80]
          mov EDI,DWORD PTR [ESP+80]
          add ECX,EAX
          lea EDI,DWORD PTR [EDI+EAX*1+4]
          mov EAX,DWORD PTR [ESP+20]
          mov DWORD PTR [ESP+24],ECX
          cmp ESI,EDI
          setae CL
          lea EDI,DWORD PTR [EAX+8]
          cmp DWORD PTR [ESP+24],EDI
          mov EBP,ECX
          setae CL
          mov EDI,ECX
          or EDI,EBP
          cmp EDX,9
          seta CL
          mov EBP,ECX
          mov ECX,EDI
          mov EAX,EBP
          test CL,AL
          je L_407120
          mov ECX,DWORD PTR [ESP+24]
          or ESI,ECX
          and ESI,3
          jne L_407120
          test EDX,EDX
          mov ESI,1
          mov EAX,DWORD PTR [ESP+20]
          cmovne ESI,EDX
          mov DWORD PTR [ESP+24],EDX
          xor EDI,EDI
          lea EBP,DWORD PTR [ESI-4]
          mov DWORD PTR [ESP+28],ESI
          shr EBP,2
          add EBP,1
          lea ESI,DWORD PTR [EBP*4]
L_406fbd:
          mov EDX,DWORD PTR [EAX+EDI*4+4]
          mov DWORD PTR [ECX+EDI*4],EDX
          add EDI,1
          cmp EBP,EDI
          ja L_406fbd
          cmp DWORD PTR [ESP+28],ESI
          mov EDX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP+20],EAX
          mov DWORD PTR [ESP+24],ECX
          je L_407019
          mov EDI,ECX
          mov ECX,EAX
          movzx EAX,BYTE PTR [EAX+ESI*1+4]
          mov BYTE PTR [EDI+ESI*1],AL
          lea EDI,DWORD PTR [ESI+1]
          cmp EDX,EDI
          jbe L_407019
          movzx EBP,BYTE PTR [ECX+ESI*1+5]
          add EDI,DWORD PTR [ESP+80]
          add ESI,2
          mov ECX,DWORD PTR [ESP+16]
          cmp EDX,ESI
          mov EAX,EBP
          mov BYTE PTR [EDI+ECX*1],AL
          jbe L_407019
          mov EAX,DWORD PTR [ESP+20]
          mov EDI,DWORD PTR [ESP+24]
          movzx EAX,BYTE PTR [EAX+ESI*1+4]
          mov BYTE PTR [EDI+ESI*1],AL
L_407019:
          mov EAX,DWORD PTR [ESP+16]
          test EAX,EAX
          jne L_4070a0
L_407021:
          add EDX,DWORD PTR [ESP+16]
          mov EAX,1
          mov DWORD PTR [EBX],EDX
          add ESP,60
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_407034:
          lea EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+12],4
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [EBX]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP],EAX
          call _countInst
          mov DWORD PTR [ESP+4],OFFSET L_44ef50
          mov EBX,EAX
          mov DWORD PTR [ESP],0
          call _log_printf
          cmp EBX,4
          mov EAX,1
          je L_406ebf
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_44ef7c
          mov DWORD PTR [ESP],0
          call _log_printf
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
L_4070a0:
          cmp EAX,4
          jb L_407103
L_4070a5:
          mov EAX,DWORD PTR [ESP+80]
          mov DWORD PTR [EAX],4294967295
          mov ECX,DWORD PTR [ESP+80]
          mov EDI,DWORD PTR [ESP+16]
          mov DWORD PTR [ECX+EDI*1-4],4294967295
          mov EAX,DWORD PTR [ESP+80]
          lea ECX,DWORD PTR [EAX+4]
          and ECX,4294967292
          sub EAX,ECX
          add EAX,EDI
          and EAX,4294967292
          cmp EAX,4
          jb L_407021
          and EAX,4294967292
          xor ESI,ESI
L_4070de:
          mov DWORD PTR [ECX+ESI*1],4294967295
          add ESI,4
          cmp ESI,EAX
          jb L_4070de
          jmp L_407021
L_4070f1:
          test EDX,EDX
          mov DWORD PTR [ESP+16],16
          jne L_406f43
          jmp L_4070a5
L_407103:
          test EAX,EAX
          je L_407021
          mov EAX,DWORD PTR [ESP+80]
          mov BYTE PTR [EAX],255
          jmp L_407021
L_407117:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_407120:
          mov EAX,DWORD PTR [ESP+20]
          mov ECX,DWORD PTR [ESP+24]
          xor ESI,ESI
          mov EDI,EBX
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_407130:
          movzx EBX,BYTE PTR [EAX+ESI*1+4]
          mov BYTE PTR [ECX+ESI*1],BL
          add ESI,1
          cmp EDX,ESI
          ja L_407130
          mov EBX,EDI
          jmp L_407019
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_407150:
          mov DWORD PTR [ESP+16],EDX
          jmp L_407021
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_407160:
          push EDI
          push ESI
          push EBX
          sub ESP,48
          mov ESI,DWORD PTR [ESP+64]
          lea EDI,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],ESI
          call _FileToBuffer
          test EAX,EAX
          je L_407290
          mov EBX,EAX
          mov EAX,DWORD PTR [ESP+40]
          test EAX,EAX
          jne L_4071b3
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_44f0b8
          mov DWORD PTR [ESP],0
          call _log_printf
L_4071a4:
          mov DWORD PTR [ESP],EBX
          call _free
L_4071ac:
          add ESP,48
          pop EBX
          pop ESI
          pop EDI
          ret 
L_4071b3:
          mov DWORD PTR [ESP+16],EAX
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_44efc8
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],EAX
          call FUN_406e50
          test EAX,EAX
          je L_4071a4
          mov DWORD PTR [ESP+4],OFFSET L_44efe8
          mov DWORD PTR [ESP],0
          call _log_printf
          lea EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],OFFSET L_44f00b
          mov DWORD PTR [ESP+4],EAX
          call FUN_41fd60
          test EAX,EAX
          mov ESI,EAX
          je L_407300
          mov EDX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+4],OFFSET L_44f014
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+12],EDX
          mov DWORD PTR [ESP+8],EDX
          call _log_printf
          mov EAX,DWORD PTR [ESP+40]
          cmp EAX,DWORD PTR [ESP+44]
          je L_4072b0
L_407247:
          mov DWORD PTR [ESP+4],OFFSET L_44f118
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call FUN_420910
          test EAX,EAX
          je L_4072e0
          mov DWORD PTR [ESP+4],OFFSET L_44f037
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_4071a4
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_407290:
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_44f0ec
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_4071ac
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_4072b0:
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EBX
          call _memcmp
          test EAX,EAX
          jne L_407247
          mov DWORD PTR [ESP+4],OFFSET L_44f140
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_4071a4
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_4072e0:
          mov DWORD PTR [ESP+4],OFFSET L_44f04c
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_4071a4
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_407300:
          mov DWORD PTR [ESP+4],OFFSET L_44f074
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_4071a4
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_407320:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,1084
          mov ECX,DWORD PTR [L_46f160]
          mov EDX,DWORD PTR [ESP+1104]
          mov EAX,DWORD PTR [ECX+12]
          test EAX,EAX
          js L_407470
          test EAX,536870912
          je L_4073f3
          test EDX,EDX
          mov EBX,2
          je L_407581
L_40735a:
          lea ESI,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+4],EDX
          mov DWORD PTR [ESP],ESI
          call _strcpy
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_44f164
          mov DWORD PTR [ESP],0
          call _log_printf
L_407382:
          lea EBP,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],EBP
          call _FileToBuffer
          test EAX,EAX
          mov EDI,EAX
          je L_4075e0
          mov EAX,DWORD PTR [ESP+40]
          test EAX,EAX
          je L_407450
          mov DWORD PTR [ESP+16],EAX
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_44efc8
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EDI
          call FUN_406e50
          test EAX,EAX
          jne L_4074e0
L_4073e0:
          mov DWORD PTR [ESP],EDI
          call _free
L_4073e8:
          add ESP,1084
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_4073f3:
          test EAX,268435456
          jne L_4074b5
          test EAX,1073741824
          je L_4074c0
          mov EBX,2
L_40740e:
          test EDX,EDX
          jne L_40735a
          test EAX,268435456
          jne L_407600
          test EAX,1073741824
          lea ESI,DWORD PTR [ESP+48]
          jne L_407671
L_407430:
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_44f1e4
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_407382
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
L_407450:
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_44f0b8
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_4073e0
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_407470:
          test EDX,EDX
          mov EBX,1
          jne L_40735a
          and EAX,15
          lea ESI,DWORD PTR [ESP+48]
          add EAX,1
          mov DWORD PTR [ESP],EAX
          call _getConsoleTypeStr
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [L_46f160]
          movzx EAX,WORD PTR [EAX+5]
          mov DWORD PTR [ESP+4],OFFSET L_44f184
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],EAX
          call _sprintf
          jmp L_407430
L_4074b5:
          mov EBX,3
          jmp L_40740e
          .byte 0x90
L_4074c0:
          mov DWORD PTR [ESP+4],OFFSET L_44f208
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,1084
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x90
L_4074e0:
          mov DWORD PTR [ESP+4],OFFSET L_44efe8
          mov DWORD PTR [ESP],0
          call _log_printf
          lea EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],OFFSET L_44f00b
          mov DWORD PTR [ESP+4],EAX
          call FUN_41fd60
          test EAX,EAX
          mov EBX,EAX
          je L_407690
          mov EDX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+4],OFFSET L_44f014
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+12],EDX
          mov DWORD PTR [ESP+8],EDX
          call _log_printf
          mov EAX,DWORD PTR [ESP+40]
          cmp EAX,DWORD PTR [ESP+44]
          je L_407640
L_407540:
          mov DWORD PTR [ESP+4],OFFSET L_44f118
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],EAX
          call FUN_420910
          test EAX,EAX
          je L_4075c0
          mov DWORD PTR [ESP+4],OFFSET L_44f037
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_4073e0
L_407581:
          and EAX,15
          lea ESI,DWORD PTR [ESP+48]
          add EAX,1
          mov DWORD PTR [ESP],EAX
          call _getConsoleTypeStr
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [L_46f160]
          movzx EAX,WORD PTR [EAX+5]
          mov DWORD PTR [ESP+4],OFFSET L_44f19a
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],EAX
          call _sprintf
          jmp L_407430
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4075c0:
          mov DWORD PTR [ESP+4],OFFSET L_44f04c
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_4073e0
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4075e0:
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_44f0ec
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_4073e8
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_407600:
          and EAX,15
          lea ESI,DWORD PTR [ESP+48]
          add EAX,1
          mov DWORD PTR [ESP],EAX
          call _getConsoleTypeStr
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [L_46f160]
          movzx EAX,WORD PTR [EAX+5]
          mov DWORD PTR [ESP+4],OFFSET L_44f1b2
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],EAX
          call _sprintf
          jmp L_407430
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_407640:
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EDI
          call _memcmp
          test EAX,EAX
          jne L_407540
          mov DWORD PTR [ESP+4],OFFSET L_44f140
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_4073e0
L_407671:
          movzx EAX,WORD PTR [ECX+5]
          mov DWORD PTR [ESP+4],OFFSET L_44f1cb
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],EAX
          call _sprintf
          jmp L_407430
          .byte 0x66
          .byte 0x90
L_407690:
          mov DWORD PTR [ESP+4],OFFSET L_44f074
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_4073e0
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_4076b0:
          push ESI
          push EBX
          sub ESP,52
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],EAX
          call _myatoh32
          mov ESI,EAX
          mov EAX,DWORD PTR [ESP+72]
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],EAX
          call _myatoh32
          mov EBX,EAX
          sub EAX,1
          cmp EAX,-3
          ja L_4077c3
          cmp ESI,-1
          je L_4077c3
          mov ECX,DWORD PTR [L_46f160]
          xor EDX,EDX
          mov EAX,DWORD PTR [ECX+20]
          div DWORD PTR [ECX+24]
          lea EDX,DWORD PTR [ESI+EBX*1]
          cmp EDX,EAX
          ja L_4077e0
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+20],ESI
          mov DWORD PTR [ESP+16],ESI
          mov DWORD PTR [ESP+4],OFFSET L_44f240
          mov DWORD PTR [ESP],0
          call _log_printf
          lea EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EAX
          call FUN_420140
          test EAX,EAX
          mov EBX,EAX
          je L_407800
          mov EAX,DWORD PTR [ESP+44]
          test EAX,EAX
          jle L_407800
          mov ECX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_44f288
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+16],ECX
          call _log_printf
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP],EAX
          call _writeFile
          test EAX,EAX
          .byte 0x0f,0x84; .long L_407820-.-4   # je L_407820
          mov DWORD PTR [ESP+4],OFFSET L_44f2b0
          mov DWORD PTR [ESP],0
          call _log_printf
L_4077b5:
          mov DWORD PTR [ESP],EBX
          call _free
          add ESP,52
          pop EBX
          pop ESI
          ret 
L_4077c3:
          mov DWORD PTR [ESP+4],OFFSET L_44f384
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,52
          pop EBX
          pop ESI
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_4077e0:
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_44f330
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,52
          pop EBX
          pop ESI
          ret 
          .byte 0x66
          .byte 0x90
L_407800:
          mov DWORD PTR [ESP+4],OFFSET L_44f2f0
          mov DWORD PTR [ESP],0
          call _log_printf
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
L_407820:
          mov EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+4],OFFSET L_44f2b8
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          jmp L_4077b5
L_407841:
          jmp FUN_407850
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
FUN_407850:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,76
          mov EAX,DWORD PTR [ESP+100]
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],EAX
          call _myatoh32
          cmp EAX,-1
          je L_407964
          mov EBX,EAX
          lea EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+96]
          mov DWORD PTR [ESP],EAX
          call _FileToBuffer
          test EAX,EAX
          mov EDI,EAX
          je L_407940
          mov ECX,DWORD PTR [ESP+60]
          test ECX,ECX
          jle L_407940
          mov EBP,DWORD PTR [L_46f160]
          xor EDX,EDX
          mov EAX,ECX
          mov ESI,DWORD PTR [EBP+24]
          div ESI
          test EDX,EDX
          mov DWORD PTR [ESP+44],EAX
          jne L_4079b0
          mov EAX,DWORD PTR [EBP+20]
          xor EDX,EDX
          div ESI
          mov ESI,DWORD PTR [ESP+44]
          lea EDX,DWORD PTR [EBX+ESI*1]
          cmp EDX,EAX
          ja L_407980
          mov DWORD PTR [ESP+20],EBX
          mov DWORD PTR [ESP+16],EBX
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_44f3f0
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],EAX
          call FUN_420200
          test EAX,EAX
          je L_4079e0
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+4],OFFSET L_44f434
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          jmp L_407998
L_407937:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_407940:
          mov EAX,DWORD PTR [ESP+96]
          mov DWORD PTR [ESP+4],OFFSET L_44f4e8
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          add ESP,76
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_407964:
          mov DWORD PTR [ESP+4],OFFSET L_44f384
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,76
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_407980:
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_44f330
          mov DWORD PTR [ESP],0
          call _log_printf
L_407998:
          mov DWORD PTR [ESP],EDI
          call _free
          add ESP,76
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
L_4079b0:
          mov EAX,DWORD PTR [ESP+96]
          mov DWORD PTR [ESP+16],ESI
          mov DWORD PTR [ESP+12],ECX
          mov DWORD PTR [ESP+4],OFFSET L_44f494
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          jmp L_407998
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_4079e0:
          mov DWORD PTR [ESP+4],OFFSET L_44f464
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_407998
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_407a00:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,60
          mov EDX,DWORD PTR [ESP+88]
          mov EBX,DWORD PTR [ESP+80]
          mov EAX,DWORD PTR [ESP+84]
          mov EBP,DWORD PTR [ESP+92]
          mov DWORD PTR [ESP+32],EDX
          lea EDX,DWORD PTR [EBX+512]
          cmp EAX,511
          mov DWORD PTR [ESP+28],EDX
          jle L_407a4e
          sub EAX,512
          mov ESI,EDX
          mov EDX,EAX
          shr EDX,9
          lea ECX,DWORD PTR [EDX+1]
          shl EDX,9
          sub EAX,EDX
          imul ECX,ECX,528
          add ESI,ECX
          add EBX,ECX
          mov DWORD PTR [ESP+28],ESI
L_407a4e:
          test EAX,EAX
          jne L_407b60
L_407a56:
          cmp EBP,511
          jle L_407b0f
          lea EAX,DWORD PTR [EBP-512]
          mov EBP,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+44],EAX
          shr EAX,9
          mov DWORD PTR [ESP+36],EAX
          add EAX,1
          imul EAX,EAX,528
          mov DWORD PTR [ESP+40],EAX
          add EAX,EBX
          mov DWORD PTR [ESP+24],EAX
          mov EAX,DWORD PTR [ESP+28]
          .byte 0x66   # nop
          nop
L_407a90:
          mov EDX,DWORD PTR [EBP]
          lea EDI,DWORD PTR [EBX+4]
          mov ECX,EBX
          mov ESI,EBP
          add EBP,512
          and EDI,4294967292
          mov DWORD PTR [EBX],EDX
          mov EDX,DWORD PTR [EBP-4]
          sub ECX,EDI
          sub ESI,ECX
          add ECX,512
          shr ECX,2
          mov DWORD PTR [EBX+508],EDX
          rep movsd 
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],EBX
          add EBX,528
          mov DWORD PTR [ESP+20],EAX
          call FUN_40fbb0
          mov EAX,DWORD PTR [ESP+20]
          add EAX,528
          cmp EBX,DWORD PTR [ESP+24]
          jne L_407a90
          mov EDX,DWORD PTR [ESP+44]
          mov EAX,DWORD PTR [ESP+36]
          mov EBP,EDX
          shl EAX,9
          sub EBP,EAX
          mov EAX,EDX
          mov EDX,DWORD PTR [ESP+32]
          and EAX,4294966784
          lea EAX,DWORD PTR [EDX+EAX*1+512]
          mov EDX,DWORD PTR [ESP+40]
          add DWORD PTR [ESP+28],EDX
          mov DWORD PTR [ESP+32],EAX
L_407b0f:
          test EBP,EBP
          jne L_407b20
          add ESP,60
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
L_407b20:
          cmp EBP,4
          jae L_407bb0
          test EBP,EBP
          je L_407b42
          mov EAX,DWORD PTR [ESP+32]
          test EBP,2
          movzx EAX,BYTE PTR [EAX]
          mov BYTE PTR [EBX],AL
          jne L_407bd8
L_407b42:
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+80],EBX
          mov DWORD PTR [ESP+84],EAX
          add ESP,60
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          jmp FUN_40fbb0
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_407b60:
          mov EDI,DWORD PTR [ESP+32]
          mov ESI,512
          sub ESI,EAX
          add EAX,EBX
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP],EAX
          sub EBP,ESI
          mov DWORD PTR [ESP+4],EDI
          call _memcpy
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EBX
          add EBX,528
          mov DWORD PTR [ESP+4],EAX
          call FUN_40fbb0
          mov EDX,EDI
          add DWORD PTR [ESP+28],528
          add EDX,ESI
          mov DWORD PTR [ESP+32],EDX
          jmp L_407a56
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_407bb0:
          mov ESI,DWORD PTR [ESP+32]
          lea EDI,DWORD PTR [EBX+4]
          mov ECX,EBX
          and EDI,4294967292
          mov EAX,DWORD PTR [ESI]
          sub ECX,EDI
          mov DWORD PTR [EBX],EAX
          mov EAX,DWORD PTR [ESI+EBP*1-4]
          sub ESI,ECX
          add ECX,EBP
          shr ECX,2
          mov DWORD PTR [EBX+EBP*1-4],EAX
          rep movsd 
          jmp L_407b42
L_407bd8:
          mov EAX,DWORD PTR [ESP+32]
          movzx EAX,WORD PTR [EAX+EBP*1-2]
          mov WORD PTR [EBX+EBP*1-2],AX
          jmp L_407b42
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
FUN_407bf0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,108
          mov EAX,DWORD PTR [L_46f160]
          mov EDI,DWORD PTR [ESP+128]
          mov EBP,DWORD PTR [EAX+20]
          mov EBX,DWORD PTR [EAX+24]
          mov EAX,DWORD PTR [ESP+132]
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],EAX
          call _myatoh32
          mov ECX,DWORD PTR [L_46f160]
          mov ESI,EAX
          mov EDX,DWORD PTR [ECX+20]
          cmp EDX,50331648
          je L_407c53
          mov EBX,1041204193
          mov EAX,EDX
          mul EBX
          shr EDX,12
          shl EDX,14
          mov EBP,EDX
          mov EDX,DWORD PTR [ECX+24]
          mov EAX,EDX
          mul EBX
          mov EBX,EDX
          shr EBX,12
          shl EBX,14
L_407c53:
          cmp ESI,-1
          je L_407d60
          mov EAX,DWORD PTR [ESP+132]
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET L_44f510
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+12],EAX
          call _log_printf
          lea EAX,DWORD PTR [ESP+88]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],EAX
          call _FileToBuffer
          test EAX,EAX
          mov DWORD PTR [ESP+44],EAX
          je L_407d40
          mov ECX,DWORD PTR [ESP+88]
          test ECX,ECX
          je L_407d40
          lea EAX,DWORD PTR [ESI+ECX*1]
          cmp EBP,EAX
          jbe L_407f20
          mov EAX,ESI
          xor EDX,EDX
          mov DWORD PTR [ESP+4],OFFSET L_44f52c
          div EBX
          mov DWORD PTR [ESP],0
          mov ESI,EDX
          mov EAX,EDX
          xor EDX,EDX
          div EBX
          xor EDX,EDX
          mov DWORD PTR [ESP+48],EAX
          lea EAX,DWORD PTR [ECX+ESI*1]
          div EBX
          mov EBX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+16],EBX
          mov DWORD PTR [ESP+12],EBX
          cmp EDX,1
          sbb EAX,-1
          mov EDI,EAX
          mov DWORD PTR [ESP+60],EAX
          mov DWORD PTR [ESP+8],EDI
          call _log_printf
          lea EAX,DWORD PTR [ESP+92]
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EAX
          call FUN_420140
          test EAX,EAX
          mov DWORD PTR [ESP+56],EAX
          je L_407d1f
          mov EAX,DWORD PTR [ESP+92]
          test EAX,EAX
          jne L_407d80
L_407d1f:
          mov DWORD PTR [ESP+4],OFFSET L_44f5f4
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,108
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
L_407d40:
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET L_44f4e8
          mov DWORD PTR [ESP],0
          call _log_printf
L_407d58:
          add ESP,108
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_407d60:
          mov DWORD PTR [ESP+4],OFFSET L_44f684
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,108
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_407d80:
          mov DWORD PTR [ESP+4],OFFSET L_44f570
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_46f160]
          cmp DWORD PTR [EAX+20],50331648
          je L_407f45
          mov EDI,DWORD PTR [ESP+56]
          cmp ESI,511
          mov EBX,DWORD PTR [ESP+88]
          lea EDX,DWORD PTR [EDI+512]
          jle L_408054
          sub ESI,512
          mov EAX,ESI
          shr EAX,9
          lea ECX,DWORD PTR [EAX+1]
          shl EAX,9
          sub ESI,EAX
          imul ECX,ECX,528
          add EDI,ECX
          add EDX,ECX
          mov DWORD PTR [ESP+64],EDI
L_407de1:
          test ESI,ESI
          jne L_407fd0
L_407de9:
          cmp EBX,511
          jle L_407ea1
          lea EAX,DWORD PTR [EBX-512]
          mov EBP,DWORD PTR [ESP+44]
          mov EBX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+76],EAX
          shr EAX,9
          mov DWORD PTR [ESP+68],EAX
          add EAX,1
          imul EAX,EAX,528
          mov DWORD PTR [ESP+72],EAX
          add EAX,EDX
          mov DWORD PTR [ESP+52],EAX
L_407e21:
          mov EAX,DWORD PTR [EBP]
          lea EDI,DWORD PTR [EBX+4]
          mov ECX,EBX
          mov ESI,EBP
          add EBP,512
          and EDI,4294967292
          mov DWORD PTR [EBX],EAX
          mov EAX,DWORD PTR [EBP-4]
          sub ECX,EDI
          sub ESI,ECX
          add ECX,512
          shr ECX,2
          mov DWORD PTR [EBX+508],EAX
          rep movsd 
          mov DWORD PTR [ESP+4],EDX
          mov DWORD PTR [ESP],EBX
          add EBX,528
          mov DWORD PTR [ESP+40],EDX
          call FUN_40fbb0
          mov EDX,DWORD PTR [ESP+40]
          add EDX,528
          cmp EDX,DWORD PTR [ESP+52]
          jne L_407e21
          mov ESI,DWORD PTR [ESP+76]
          mov EAX,DWORD PTR [ESP+68]
          mov EBX,ESI
          shl EAX,9
          sub EBX,EAX
          mov EAX,ESI
          mov ESI,DWORD PTR [ESP+44]
          and EAX,4294966784
          lea EAX,DWORD PTR [ESI+EAX*1+512]
          mov ESI,DWORD PTR [ESP+72]
          add DWORD PTR [ESP+64],ESI
          mov DWORD PTR [ESP+44],EAX
L_407ea1:
          test EBX,EBX
          jne L_407f90
L_407ea9:
          mov DWORD PTR [ESP+4],OFFSET L_44f2b0
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EDI,DWORD PTR [ESP+48]
          mov ESI,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+4],OFFSET L_44f594
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+8],ESI
          call _log_printf
          mov EAX,DWORD PTR [ESP+92]
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP],EAX
          call FUN_420200
          test EAX,EAX
          je L_407f70
          mov DWORD PTR [ESP+4],OFFSET L_44f5d0
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_407d58
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_407f20:
          mov DWORD PTR [ESP+16],EBP
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET L_44f628
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_407d58
L_407f45:
          mov EAX,DWORD PTR [ESP+88]
          add ESI,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],EAX
          call _memcpy
          jmp L_407ea9
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_407f70:
          mov DWORD PTR [ESP+4],OFFSET L_44f464
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_407d58
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_407f90:
          cmp EBX,4
          jae L_408025
          test EBX,EBX
          je L_407fb3
          mov EAX,DWORD PTR [ESP+44]
          mov EDI,DWORD PTR [ESP+64]
          test BL,2
          movzx EAX,BYTE PTR [EAX]
          mov BYTE PTR [EDI],AL
          jne L_40805d
L_407fb3:
          mov EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+4],EDX
          mov DWORD PTR [ESP],EAX
          call FUN_40fbb0
          jmp L_407ea9
          nop
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_407fd0:
          mov EDI,DWORD PTR [ESP+64]
          mov EAX,DWORD PTR [ESP+44]
          mov EBP,512
          sub EBP,ESI
          mov DWORD PTR [ESP+40],EDX
          mov DWORD PTR [ESP+8],EBP
          sub EBX,EBP
          add ESI,EDI
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],ESI
          call _memcpy
          mov EDX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],EDX
          call FUN_40fbb0
          mov EDX,DWORD PTR [ESP+40]
          mov EAX,EDI
          add DWORD PTR [ESP+44],EBP
          add EAX,528
          mov DWORD PTR [ESP+64],EAX
          add EDX,528
          jmp L_407de9
L_408025:
          mov EBP,DWORD PTR [ESP+44]
          mov ESI,DWORD PTR [ESP+64]
          mov EAX,DWORD PTR [EBP]
          lea EDI,DWORD PTR [ESI+4]
          mov ECX,ESI
          and EDI,4294967292
          mov DWORD PTR [ESI],EAX
          mov EAX,DWORD PTR [EBP+EBX*1-4]
          sub ECX,EDI
          mov DWORD PTR [ESI+EBX*1-4],EAX
          mov ESI,EBP
          sub ESI,ECX
          add ECX,EBX
          shr ECX,2
          rep movsd 
          jmp L_407fb3
L_408054:
          mov DWORD PTR [ESP+64],EDI
          jmp L_407de1
L_40805d:
          mov EAX,DWORD PTR [ESP+44]
          mov EDI,DWORD PTR [ESP+64]
          movzx EAX,WORD PTR [EAX+EBX*1-2]
          mov WORD PTR [EDI+EBX*1-2],AX
          jmp L_407fb3
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
L_408080:
          push EBX
          sub ESP,24
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],EAX
          call _myatoh32
          cmp EAX,-1
          je L_408140
          mov ECX,DWORD PTR [L_46f160]
          mov EBX,EAX
          xor EDX,EDX
          mov EAX,DWORD PTR [ECX+20]
          div DWORD PTR [ECX+24]
          mov DWORD PTR [ESP+8],EBX
          cmp EBX,EAX
          jae L_408120
          mov DWORD PTR [ESP+4],OFFSET L_44f6d5
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EBX
          call FUN_420320
          test EAX,EAX
          jne L_408100
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_44f6f8
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,24
          pop EBX
          ret 
          .byte 0x66
          .byte 0x90
L_408100:
          mov DWORD PTR [ESP+4],OFFSET L_44f6eb
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,24
          pop EBX
          ret 
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_408120:
          mov DWORD PTR [ESP+4],OFFSET L_44f724
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,24
          pop EBX
          ret 
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_408140:
          mov DWORD PTR [ESP+4],OFFSET L_44f684
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,24
          pop EBX
          ret 
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_408160:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov EAX,DWORD PTR [ESP+72]
          mov ECX,DWORD PTR [ESP+68]
          mov EDI,DWORD PTR [ESP+64]
          mov EBP,DWORD PTR [EAX]
          lea EAX,DWORD PTR [EBP+1]
          lea EDX,DWORD PTR [EAX*4]
          cmp EAX,EDI
          lea ESI,DWORD PTR [ECX+EDX*1]
          mov EBX,DWORD PTR [ESI]
          je L_40823e
          test EBX,EBX
          je L_40823e
          cmp BYTE PTR [EBX],45
          je L_40823e
          mov EBX,DWORD PTR [ESP+84]
          test EBX,EBX
          je L_408210
          lea EBX,DWORD PTR [EDX+4]
          lea EAX,DWORD PTR [EBP+2]
          mov DWORD PTR [ESP+28],EBX
          mov EBX,DWORD PTR [ECX+EDX*1+4]
          test EBX,EBX
          je L_40822a
          cmp EDI,EAX
          je L_40822a
          cmp BYTE PTR [EBX],45
          je L_40822a
          mov EBP,DWORD PTR [ESP+84]
          mov DWORD PTR [EBP],EBX
L_4081c7:
          mov EBP,DWORD PTR [ESP+88]
          test EBP,EBP
          je L_4081ed
          mov EBX,DWORD PTR [ESP+28]
          add EAX,1
          mov EBX,DWORD PTR [ECX+EBX*1+4]
          test EBX,EBX
          je L_40822a
          cmp EDI,EAX
          je L_40822a
          cmp BYTE PTR [EBX],45
          je L_40822a
          mov EDI,DWORD PTR [ESP+88]
          mov DWORD PTR [EDI],EBX
L_4081ed:
          mov EDI,DWORD PTR [ESP+76]
          test EDI,EDI
          je L_4081fd
          mov EBX,DWORD PTR [ESP+80]
          test EBX,EBX
          jne L_408216
L_4081fd:
          mov EDI,DWORD PTR [ESP+72]
          mov DWORD PTR [EDI],EAX
          mov EAX,DWORD PTR [ESI]
          add ESP,44
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_408210:
          mov DWORD PTR [ESP+28],EDX
          jmp L_4081c7
L_408216:
          mov EAX,DWORD PTR [ECX+EDX*1-4]
          mov DWORD PTR [ESP],5
          mov DWORD PTR [ESP+4],EAX
          call FUN_406330
L_40822a:
          mov EAX,DWORD PTR [ECX+EDX*1-4]
          mov DWORD PTR [ESP],4
          mov DWORD PTR [ESP+4],EAX
          call FUN_406330
L_40823e:
          mov EAX,DWORD PTR [ECX+EDX*1-4]
          mov DWORD PTR [ESP],3
          mov DWORD PTR [ESP+4],EAX
          call FUN_406330
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_408260:
          push EBP
          push EDI
          mov EAX,121
          push ESI
          push EBX
          sub ESP,92
          mov ESI,DWORD PTR [ESP+112]
          mov DWORD PTR [ESP],OFFSET L_44f757
          mov EBX,DWORD PTR [ESP+116]
          mov DWORD PTR [ESP+74],1835890020
          mov WORD PTR [ESP+78],AX
          mov DWORD PTR [ESP+60],0
          mov DWORD PTR [ESP+64],0
          mov DWORD PTR [ESP+68],0
          call _log_set_name
          test ESI,ESI
          mov DWORD PTR [ESP+68],0
          jle L_408a30
          xor EAX,EAX
          mov DWORD PTR [ESP+40],0
          xor EBP,EBP
          mov DWORD PTR [ESP+44],0
          xor EDI,EDI
          jmp L_408301
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
L_4082d0:
          mov DWORD PTR [ESP+4],OFFSET L_44f774
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [L_44a524],0
          add EAX,1
L_4082f5:
          cmp ESI,EAX
          mov DWORD PTR [ESP+68],EAX
          jle L_4083f5
L_408301:
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],OFFSET L_44f75e
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call FUN_4491d0
          test EAX,EAX
          je L_408885
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],OFFSET L_44f763
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call FUN_4491d0
          test EAX,EAX
          je L_408885
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],OFFSET L_44f766
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call FUN_4491d0
          test EAX,EAX
          je L_408885
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],8
          mov DWORD PTR [ESP+4],OFFSET L_44f769
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call FUN_4491d0
          test EAX,EAX
          je L_4082d0
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],7
          mov DWORD PTR [ESP+4],OFFSET L_44f79a
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call FUN_4491d0
          test EAX,EAX
          jne L_408440
          cmp EDI,1
          je L_4085a0
L_4083c9:
          mov DWORD PTR [ESP+4],OFFSET L_44f7e4
          mov DWORD PTR [ESP],0
          mov EDI,2
          call _log_printf
          mov EAX,DWORD PTR [ESP+68]
          add EAX,1
          cmp ESI,EAX
          mov DWORD PTR [ESP+68],EAX
          jg L_408301
L_4083f5:
          mov EAX,DWORD PTR [ESP+40]
          test EAX,EAX
          je L_408405
          test EBP,EBP
          jne L_408758
L_408405:
          test EDI,EDI
          je L_408a30
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EAX
          call FUN_41f700
          test EAX,EAX
          jne L_408812
L_408421:
          mov DWORD PTR [ESP+4],OFFSET L_44fae8
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,92
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x90
L_408440:
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],3
          mov DWORD PTR [ESP+4],OFFSET L_44f802
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call FUN_4491d0
          test EAX,EAX
          jne L_408500
          mov ECX,DWORD PTR [ESP+68]
          lea EAX,DWORD PTR [ECX+1]
          mov EBP,DWORD PTR [EBX+EAX*4]
          lea EDX,DWORD PTR [EAX*4]
          test EBP,EBP
          je L_408b9b
          cmp ESI,EAX
          je L_408b9b
          cmp BYTE PTR [EBP],45
          je L_408b9b
          lea EBP,DWORD PTR [ECX+2]
          mov EDX,DWORD PTR [EBX+EDX*1+4]
          cmp ESI,EBP
          je L_408b88
          test EDX,EDX
          je L_408b88
          cmp BYTE PTR [EDX],45
          je L_408b88
          cmp DWORD PTR [ESP+40],0
          mov DWORD PTR [ESP+60],EDX
          jne L_408c70
          mov DWORD PTR [ESP+68],EBP
          mov EBP,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP+12],EDX
          mov DWORD PTR [ESP+4],OFFSET L_44f808
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EBP
          call _log_printf
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+40],11
          add EAX,1
          jmp L_4082f5
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_408500:
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],3
          mov DWORD PTR [ESP+4],OFFSET L_44f834
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call FUN_4491d0
          test EAX,EAX
          jne L_4085c0
          lea EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+16],1
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+24],EAX
          lea EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+20],EAX
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+12],EAX
          lea EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],EAX
          call FUN_408160
          mov EBP,EAX
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+4],OFFSET L_44f838
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+16],EAX
          mov EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+40],8
          add EAX,1
          jmp L_4082f5
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4085a0:
          mov DWORD PTR [ESP+4],OFFSET L_44f7a4
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_4083c9
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4085c0:
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],3
          mov DWORD PTR [ESP+4],OFFSET L_44f864
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call FUN_4491d0
          test EAX,EAX
          jne L_408680
          mov ECX,DWORD PTR [ESP+68]
          lea EDX,DWORD PTR [ECX+1]
          cmp ESI,EDX
          lea EAX,DWORD PTR [EDX*4]
          mov EBP,DWORD PTR [EBX+EDX*4]
          je L_408b9b
          test EBP,EBP
          je L_408b9b
          cmp BYTE PTR [EBP],45
          je L_408b9b
          mov EAX,DWORD PTR [EBX+EAX*1+4]
          lea EBP,DWORD PTR [ECX+2]
          test EAX,EAX
          je L_408b88
          cmp ESI,EBP
          je L_408b88
          cmp BYTE PTR [EAX],45
          je L_408b88
          cmp DWORD PTR [ESP+40],0
          mov DWORD PTR [ESP+60],EAX
          jne L_408c70
          mov DWORD PTR [ESP+68],EBP
          mov EBP,DWORD PTR [EBX+EDX*4]
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+4],OFFSET L_44f868
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EBP
          call _log_printf
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+40],9
          add EAX,1
          jmp L_4082f5
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_408680:
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],3
          mov DWORD PTR [ESP+4],OFFSET L_44f896
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call FUN_4491d0
          test EAX,EAX
          jne L_408703
          mov EDX,DWORD PTR [ESP+68]
          lea EAX,DWORD PTR [EDX+1]
          mov EBP,DWORD PTR [EBX+EAX*4]
          test EBP,EBP
          je L_408c96
          cmp ESI,EAX
          je L_408c96
          cmp BYTE PTR [EBP],45
          je L_408c96
          mov ECX,DWORD PTR [ESP+40]
          test ECX,ECX
          jne L_408c83
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_44f89a
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+68],EAX
          call _log_printf
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+40],10
          add EAX,1
          jmp L_4082f5
L_408703:
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],OFFSET L_44f8b1
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call FUN_4491d0
          test EAX,EAX
          jne L_408826
          cmp EDI,2
          je L_408865
          mov DWORD PTR [ESP+4],OFFSET L_44f8f0
          mov DWORD PTR [ESP],0
          mov EDI,1
          call _log_printf
          mov EAX,DWORD PTR [ESP+68]
          add EAX,1
          jmp L_4082f5
L_408758:
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EAX
          call FUN_41f700
          test EAX,EAX
          je L_408421
          call FUN_41fe10
          mov ECX,DWORD PTR [ESP+40]
          mov DWORD PTR [L_46f160],EAX
          cmp ECX,12
          ja L_40896b
          jmp DWORD PTR [ECX*4+L_44fb1c]
L_40878a:
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],EBP
          call _myatoh32
          cmp EAX,-1
          mov EBX,EAX
          je L_408c35
          mov ECX,DWORD PTR [L_46f160]
          xor EDX,EDX
          mov EAX,DWORD PTR [ECX+20]
          div DWORD PTR [ECX+24]
          mov DWORD PTR [ESP+8],EBX
          cmp EBX,EAX
          jae L_408acb
          mov DWORD PTR [ESP+4],OFFSET L_44f6d5
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EBX
          call FUN_420320
          test EAX,EAX
          je L_408ae4
          mov DWORD PTR [ESP+4],OFFSET L_44f6eb
          mov DWORD PTR [ESP],0
          call _log_printf
L_4087ff:
          test EDI,EDI
          jne L_40881c
L_408803:
          call FUN_41fa40
          add ESP,92
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_408812:
          call FUN_41fe10
          mov DWORD PTR [L_46f160],EAX
L_40881c:
          mov DWORD PTR [ESP],EDI
          call FUN_420840
          jmp L_408803
L_408826:
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],5
          mov DWORD PTR [ESP+4],OFFSET L_44f910
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call FUN_4491d0
          test EAX,EAX
          jne L_408984
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+40],3
          lea EBP,DWORD PTR [ESP+74]
          add EAX,1
          jmp L_4082f5
L_408865:
          mov DWORD PTR [ESP+4],OFFSET L_44f8b4
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [ESP+68]
          add EAX,1
          jmp L_4082f5
L_408885:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],0
          call FUN_406330
L_408899:
          lea EAX,DWORD PTR [ESP+74]
          cmp EBP,EAX
          je L_408c5f
          mov DWORD PTR [ESP],EBP
          call FUN_406740
          jmp L_4087ff
L_4088b2:
          mov DWORD PTR [ESP],EBP
          call FUN_41fe20
          jmp L_4087ff
L_4088bf:
          call FUN_406c60
          jmp L_4087ff
L_4088c9:
          test BYTE PTR [EAX+16],32
          je L_408a17
          mov EAX,DWORD PTR [EAX+4]
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+4],EAX
          call FUN_432e50
          jmp L_4087ff
L_4088e7:
          test BYTE PTR [EAX+16],32
          je L_4089fe
          mov DWORD PTR [ESP],EBP
          call FUN_433440
          jmp L_4087ff
L_4088fe:
          mov DWORD PTR [ESP],EBP
          call FUN_406980
          jmp L_4087ff
L_40890b:
          mov EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+4],EAX
          call FUN_4076b0
          jmp L_4087ff
L_408928:
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+4],EAX
          call FUN_407850
          jmp L_4087ff
L_40893d:
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+4],EAX
          call FUN_407bf0
          jmp L_4087ff
L_408952:
          lea EAX,DWORD PTR [ESP+74]
          cmp EBP,EAX
          je L_408c4e
          mov DWORD PTR [ESP],EBP
          call FUN_407320
          jmp L_4087ff
L_40896b:
          mov DWORD PTR [ESP+4],OFFSET L_44faa8
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_4087ff
L_408984:
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],3
          mov DWORD PTR [ESP+4],OFFSET L_44f916
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call FUN_4491d0
          test EAX,EAX
          jne L_408a44
          mov EDX,DWORD PTR [ESP+68]
          lea EAX,DWORD PTR [EDX+1]
          mov ECX,DWORD PTR [EBX+EAX*4]
          test ECX,ECX
          mov DWORD PTR [ESP+44],ECX
          je L_408c96
          cmp ESI,EAX
          je L_408c96
          cmp BYTE PTR [ECX],45
          je L_408c96
          mov DWORD PTR [ESP+68],EAX
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+4],OFFSET L_44f91a
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov EAX,DWORD PTR [ESP+68]
          add EAX,1
          jmp L_4082f5
L_4089fe:
          mov DWORD PTR [ESP+4],OFFSET L_44fa58
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_4087ff
L_408a17:
          mov DWORD PTR [ESP+4],OFFSET L_44fa14
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_4087ff
L_408a30:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],2
          call FUN_406330
L_408a44:
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],OFFSET L_44f933
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call FUN_4491d0
          test EAX,EAX
          jne L_408b01
          mov EAX,DWORD PTR [ESP+68]
          lea EDX,DWORD PTR [EAX+1]
          cmp ESI,EDX
          mov EBP,DWORD PTR [EBX+EDX*4]
          je L_408ca9
          test EBP,EBP
          je L_408ca9
          cmp BYTE PTR [EBP],45
          je L_408ca9
          mov ECX,DWORD PTR [ESP+40]
          test ECX,ECX
          jne L_408cbc
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_44f936
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+68],EDX
          call _log_printf
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+40],1
          add EAX,1
          jmp L_4082f5
L_408acb:
          mov DWORD PTR [ESP+4],OFFSET L_44f724
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_4087ff
L_408ae4:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_44f6f8
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_4087ff
L_408b01:
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],OFFSET L_44f953
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call FUN_4491d0
          test EAX,EAX
          jne L_408bae
          mov EAX,DWORD PTR [ESP+68]
          lea EDX,DWORD PTR [EAX+1]
          cmp ESI,EDX
          mov EBP,DWORD PTR [EBX+EDX*4]
          je L_408ca9
          test EBP,EBP
          je L_408ca9
          cmp BYTE PTR [EBP],45
          je L_408ca9
          mov ECX,DWORD PTR [ESP+40]
          test ECX,ECX
          jne L_408cbc
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_44f956
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+68],EDX
          call _log_printf
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+40],2
          add EAX,1
          jmp L_4082f5
L_408b88:
          mov EAX,DWORD PTR [EBX+ECX*4]
          mov DWORD PTR [ESP],4
          mov DWORD PTR [ESP+4],EAX
          call FUN_406330
L_408b9b:
          mov EAX,DWORD PTR [EBX+ECX*4]
          mov DWORD PTR [ESP],3
          mov DWORD PTR [ESP+4],EAX
          call FUN_406330
L_408bae:
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],OFFSET L_44f974
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call FUN_4491d0
          test EAX,EAX
          jne L_408ccf
          mov EAX,DWORD PTR [ESP+68]
          lea EDX,DWORD PTR [EAX+1]
          mov EBP,DWORD PTR [EBX+EDX*4]
          test EBP,EBP
          je L_408ca9
          cmp ESI,EDX
          je L_408ca9
          cmp BYTE PTR [EBP],45
          je L_408ca9
          mov ECX,DWORD PTR [ESP+40]
          test ECX,ECX
          jne L_408cbc
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_44f978
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+68],EDX
          call _log_printf
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+40],4
          add EAX,1
          jmp L_4082f5
L_408c35:
          mov DWORD PTR [ESP+4],OFFSET L_44f684
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_4087ff
L_408c4e:
          mov DWORD PTR [ESP],0
          call FUN_407320
          jmp L_4087ff
L_408c5f:
          mov DWORD PTR [ESP],0
          call FUN_406740
          jmp L_4087ff
L_408c70:
          mov EAX,DWORD PTR [EBX+ECX*4]
          mov DWORD PTR [ESP],5
          mov DWORD PTR [ESP+4],EAX
          call FUN_406330
L_408c83:
          mov EAX,DWORD PTR [EBX+EDX*4]
          mov DWORD PTR [ESP],5
          mov DWORD PTR [ESP+4],EAX
          call FUN_406330
L_408c96:
          mov EAX,DWORD PTR [EBX+EDX*4]
          mov DWORD PTR [ESP],3
          mov DWORD PTR [ESP+4],EAX
          call FUN_406330
L_408ca9:
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],3
          mov DWORD PTR [ESP+4],EAX
          call FUN_406330
L_408cbc:
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],5
          mov DWORD PTR [ESP+4],EAX
          call FUN_406330
L_408ccf:
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],OFFSET L_44f9a5
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call FUN_4491d0
          test EAX,EAX
          jne L_408d42
          mov EAX,DWORD PTR [ESP+68]
          lea EDX,DWORD PTR [EAX+1]
          mov EBP,DWORD PTR [EBX+EDX*4]
          test EBP,EBP
          je L_408ca9
          cmp ESI,EDX
          je L_408ca9
          cmp BYTE PTR [EBP],45
          je L_408ca9
          mov ECX,DWORD PTR [ESP+40]
          test ECX,ECX
          jne L_408cbc
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_44f9a8
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+68],EDX
          call _log_printf
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+40],5
          add EAX,1
          jmp L_4082f5
L_408d42:
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],OFFSET L_44f9da
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call FUN_4491d0
          test EAX,EAX
          jne L_408dbb
          mov EAX,DWORD PTR [ESP+68]
          lea EDX,DWORD PTR [EAX+1]
          mov EBP,DWORD PTR [EBX+EDX*4]
          mov EAX,EDX
          test EBP,EBP
          je L_408e41
          cmp ESI,EDX
          je L_408e2c
          cmp BYTE PTR [EBP],45
          je L_408e41
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_44f9dd
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+68],EDX
          call _log_printf
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+40],12
          add EAX,1
          jmp L_4082f5
L_408dbb:
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],OFFSET L_44f9f7
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call FUN_4491d0
          test EAX,EAX
          jne L_408e6d
          mov EAX,DWORD PTR [ESP+68]
          lea EDX,DWORD PTR [EAX+1]
          mov EBP,DWORD PTR [EBX+EDX*4]
          mov EAX,EDX
          test EBP,EBP
          je L_408e5c
          cmp ESI,EDX
          je L_408e52
          cmp BYTE PTR [EBP],45
          je L_408e5c
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_44f9fa
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+68],EDX
          call _log_printf
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+40],7
          add EAX,1
          jmp L_4082f5
L_408e2c:
          mov DWORD PTR [ESP+40],12
L_408e34:
          mov DWORD PTR [ESP+68],EAX
          lea EBP,DWORD PTR [ESP+74]
          jmp L_4083f5
L_408e41:
          mov DWORD PTR [ESP+40],12
          lea EBP,DWORD PTR [ESP+74]
          jmp L_4082f5
L_408e52:
          mov DWORD PTR [ESP+40],7
          jmp L_408e34
L_408e5c:
          mov DWORD PTR [ESP+40],7
          lea EBP,DWORD PTR [ESP+74]
          jmp L_4082f5
L_408e6d:
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],OFFSET L_44fa10
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call FUN_4491d0
          test EAX,EAX
          mov EAX,DWORD PTR [ESP+68]
          mov EAX,DWORD PTR [EBX+EAX*4]
          jne L_408eaf
          movzx EAX,BYTE PTR [EAX+2]
          mov DWORD PTR [ESP],EAX
          call _log_verbose_flag
          mov EAX,DWORD PTR [ESP+68]
          add EAX,1
          jmp L_4082f5
L_408eaf:
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],1
          call FUN_406330
          nop

.section .rdata,"dr"
.p2align 2
L_44e10c:
          .string "\n\n***** ERROR: option flag %s on command line but no argument provided!\n"
          .zero 3
L_44e158:
          .string "\n\n***** ERROR: option flag %s on command line not enough arguments provided!\n"
          .zero 2
L_44e1a8:
          .string "\n\n***** ERROR: option flag %s on command line but option was already set!\n"
          .zero 1
L_44e1f4:
          .string "\n\n***** ERROR: unknown option '%s' provided on command line!\n"
          .zero 2
L_44e234:
          .string "\n\n***** ERROR: not enough info provided to carry out command!\n"
L_44e273:
          .string "xeBuild"
          .zero 1
L_44e27c:
          .string "Usage   :\n   %s client <switch> [<option>]\n\n"
L_44e2a9:
          .string "Examples:\n"
L_44e2b4:
          .string "   %s client -r nanddump.bin\n"
          .zero 2
L_44e2d4:
          .string "   %s client -w nandflash.bin -ip 192.168.2.100\n"
L_44e305:
          .string "\nSwitches:\n"
          .zero 3
L_44e314:
          .string "   -i             : connects to console and shows some info about it\n"
          .zero 2
L_44e35c:
          .string "*  -i <d>         : collects console information into folder <d>, usually enough for build mode\n"
          .zero 3
L_44e3c0:
          .string "   -r <f>         : dumps system area of NAND to <f>\n"
          .zero 2
L_44e3f8:
          .string "   -w <f>         : writes system area of NAND from <f>\n"
          .zero 3
L_44e434:
          .string "   -e <d>         : format partition and send avatar/kinect data to HDD from <d>, must match running kernel\n"
          .zero 3
L_44e4a4:
          .string "   -c <d>         : format partition and send xbox compatibility data to HDD from <d>\n"
          .zero 1
L_44e4fc:
          .string "   -p             : will attempt to automatically update patches based on running kernel version\n"
          .zero 2
L_44e560:
          .string "   -p <f>         : update patches with <f>\n"
          .zero 3
L_44e590:
          .string "   -rb <f> <b> <l>: read series of blocks starting at <b> for <l>\n"
          .zero 1
L_44e5d4:
          .string "   -wb <f> <b>    : write series of blocks starting at <b> for the number of blocks in <f>\n"
L_44e630:
          .string "   -eb <b>        : attempt to erase a single block, even if marked bad on console\n"
L_44e684:
          .string "   -bp <f> <o>    : binary patch NAND with contents of <f> to logical offset <o>\n"
          .zero 2
L_44e6d8:
          .string "*  -keys          : will attempt to dump RSA and 1BL keys from console\n"
L_44e720:
          .string "   -s             : shutdown console\n"
          .zero 2
L_44e748:
          .string "   -ip <add>      : force attempt to connect to addr (ie: -i 192.168.0.100)\n"
          .zero 3
L_44e798:
          .string "   -noenter       : suppresses prompt for enter key when finished\n"
          .zero 1
L_44e7dc:
          .string "   -reboot        : causes the console to hard reboot\n"
          .zero 1
L_44e814:
          .string "   -v             : shows more info during client process\n"
          .zero 1
L_44e850:
          .string "   -?             : shows this help\n\n"
L_44e876:
          .string "legend:\n"
          .zero 1
L_44e880:
          .string "<add>    = without this option network will be scanned for server broadcast beacon\n"
L_44e8d4:
          .string "           If provided the correct format is an IPv4 address like 192.168.0.100\n"
          .zero 3
L_44e928:
          .string "<f>      = path, absolute or relative, to a file\n"
          .zero 2
L_44e95c:
          .string "<d>      = path, absolute or relative, to a directory - do not terminate with /\n"
          .zero 3
L_44e9b0:
          .string "<b>      = hexadecimal block number\n"
          .zero 3
L_44e9d8:
          .string "<l>      = hexadecimal number of blocks\n"
          .zero 3
L_44ea04:
          .string "<o>      = hexadecimal logical offset (spare data not considered) in flash\n"
L_44ea50:
          .string "notes:\n"
L_44ea58:
          .string "* functions not fully supported with older patch versions, use with caution.\n"
          .zero 2
L_44eaa8:
          .string "- client mode tends to operate on a single command basis, stacking commands.\n"
          .zero 2
L_44eaf8:
          .string "  is not possible with the exception of v, noenter, ip, s and reboot.\n"
          .zero 1
L_44eb40:
          .string "- patch update (-p) will retain any addon patches already on the console.\n"
L_44eb8b:
          .string "\npress <enter> to quit...\n"
          .zero 2
L_44eba8:
          .long L_406360
          .long L_4066c1
          .long L_4066e2
          .long L_4066fb
          .long L_40671c
          .long L_406343
L_44ebc0:
          .string "creating mydata folder output at %s\n"
          .zero 3
L_44ebe8:
          .string "unable to dump details to %s, disabling\n"
L_44ec11:
          .string "0x%x"
L_44ec16:
          .string ","
L_44ec18:
          .string "dumping console flash to %s\n"
L_44ec35:
          .string "success!\n"
L_44ec3f:
          .string "failed!\n"
L_44ec48:
          .string "Bad Block list  : "
L_44ec5b:
          .string "reading file %s..."
L_44ec6e:
          .string "success, read 0x%x bytes\n"
L_44ec88:
          .string "sending data to console...\n"
L_44eca4:
          .string "\n\n***** ERROR: file size should be 0x%x but its 0x%x bytes! Aborted!\n"
          .zero 2
L_44ecec:
          .string "\n\n***** ERROR: image magic should be 0xFF4F but its 0x%x! Aborted!\n"
L_44ed30:
          .string "\n\n***** ERROR: unable to read file to send\n"
L_44ed5c:
          .string "manifest, %08x %08x %s\n"
L_44ed74:
          .string "item %03d: %08x %08x %s\n"
L_44ed8d:
          .string "checking %s (file ./%s)\n"
          .zero 2
L_44eda8:
          .string "\n\n****** ERROR: unable to dump %s to file ./%s, key is not valid or file is inaccessible!\n"
          .zero 1
L_44ee04:
          .string "dumping valid %s to file ./%s\n"
L_44ee23:
          .string "./"
L_44ee26:
          .string "1blkey.txt"
L_44ee31:
          .string "1BL key"
L_44ee39:
          .string "1BL_pub.bin"
L_44ee45:
          .string "1BL RSA pub key"
L_44ee55:
          .string "PIRS_pub.bin"
L_44ee62:
          .string "PIRS RSA pub key"
L_44ee73:
          .string "MAST_pub.bin"
L_44ee80:
          .string "MASTER RSA pub key"
          .zero 1
L_44ee94:
          .string "\n\n****** ERROR: console patches need to be updated to support this operation!\n"
          .zero 1
L_44eee4:
          .string "checking patch sections for glitch console\n"
L_44ef10:
          .string "\n\n***** ERROR: patches do not contain all segments, aborting!\n"
          .zero 1
L_44ef50:
          .string "checking patch sections for JTAG console\n"
          .zero 2
L_44ef7c:
          .string "\n\n***** ERROR: patches do not contain all segments, counted %d - aborting!\n"
L_44efc8:
          .string "loaded %s size 0x%x (%d) bytes\n"
L_44efe8:
          .string "retrieving patches from console..."
L_44f00b:
          .string "patches"
          .zero 1
L_44f014:
          .string "success! received 0x%x (%d) bytes\n"
L_44f037:
          .string "patches updated OK!\n"
L_44f04c:
          .string "\n\n***** ERROR: patch update failed!\n"
          .zero 3
L_44f074:
          .string "\n\n***** ERROR: failed to retrieve current patches from console!\n"
          .zero 3
L_44f0b8:
          .string "\n\n***** ERROR: %s exists but is 0 len, aborting\n"
          .zero 3
L_44f0ec:
          .string "\n\n***** ERROR: could not load %s, aborting\n"
L_44f118:
          .string "sending update patches to console..."
          .zero 3
L_44f140:
          .string "patches are already up to date!\n"
          .zero 3
L_44f164:
          .string "Updating patches from file: %s\n"
L_44f184:
          .string "%d/bin/patches_%s.bin"
L_44f19a:
          .string "%d/bin/patches_g2%s.bin"
L_44f1b2:
          .string "%d/bin/patches_g2m%s.bin"
L_44f1cb:
          .string "%d/bin/patches_fat.bin"
          .zero 2
L_44f1e4:
          .string "Updating patches in auto mode: %s\n"
          .zero 1
L_44f208:
          .string "\n***** ERROR: unable to determine console hack type!\n"
          .zero 2
L_44f240:
          .string "Reading 0x%x (%d) blocks from console starting at block 0x%x (%d)...\n"
          .zero 2
L_44f288:
          .string "Done!\nWriting 0x%x (%d) bytes to %s...\n"
L_44f2b0:
          .string "Done!\n"
          .zero 1
L_44f2b8:
          .string "\n\n***** ERROR: Failed to write block data to file %s!\n"
          .zero 1
L_44f2f0:
          .string "\n\n***** ERROR: Trying to read blocks from the console failed!\n"
          .zero 1
L_44f330:
          .string "\n\n***** ERROR: This read command will exceed the system area size of 0x%x blocks!\n"
          .zero 1
L_44f384:
          .string "\n\n***** ERROR: Invalid arguments specified, please provide hex only for start block and number of blocks!\n"
          .zero 1
L_44f3f0:
          .string "Writing 0x%x (%d) blocks to console starting at block 0x%x (%d)...\n"
L_44f434:
          .string "Done! Wrote 0x%x (%d) bytes to console flash!\n"
          .zero 1
L_44f464:
          .string "\n\n***** ERROR: Writing data to console failed!\n"
L_44f494:
          .string "\n\n***** ERROR: File %s size (0x%x) is not a multiple of console block size (0x%x)!\n"
L_44f4e8:
          .string "\n\n***** ERROR: Unable to read file %s!\n"
L_44f510:
          .string "file: %s start offset 0x%x\n"
L_44f52c:
          .string "Reading 0x%x blocks from console starting at block 0x%x (%d)...\n"
          .zero 3
L_44f570:
          .string "Success!\nPatching in binary data..."
L_44f594:
          .string "Writing 0x%x blocks from console starting at block 0x%x...\n"
L_44f5d0:
          .string "Success! Completed patching NAND!\n"
          .zero 1
L_44f5f4:
          .string "\n\n***** ERROR: Reading data from console failed!\n"
          .zero 2
L_44f628:
          .string "\n\n***** ERROR: File %s size patched into offset 0x%x will exceed NAND system area (0x%x)!\n"
          .zero 1
L_44f684:
          .string "\n\n***** ERROR: Invalid arguments specified, please provide hex only for offset!\n"
L_44f6d5:
          .string "erasing block 0x%x..."
L_44f6eb:
          .string "Success!\n"
          .zero 3
L_44f6f8:
          .string "\n\n***** ERROR: Failed to erase block 0x%x!\n"
L_44f724:
          .string "\n\n***** ERROR: Block 0x%x is outside system area!\n"
L_44f757:
          .string "client"
L_44f75e:
          .string "help"
L_44f763:
          .string "-?"
L_44f766:
          .string "/?"
L_44f769:
          .string "-noenter"
          .zero 2
L_44f774:
          .string "<enter> key on completion suppressed\n"
L_44f79a:
          .string "-reboot"
          .zero 2
L_44f7a4:
          .string "shutdown superseded by reboot, ignoring -s in favor of -reboot\n"
L_44f7e4:
          .string "setting reboot on completion\n"
L_44f802:
          .string "-bp"
          .zero 2
L_44f808:
          .string "setting binary patch file to %s, offset %s\n"
L_44f834:
          .string "-rb"
L_44f838:
          .string "reading %s blocks to %s, starting block %s\n"
L_44f864:
          .string "-wb"
L_44f868:
          .string "writing blocks from %s, starting at block %s\n"
L_44f896:
          .string "-eb"
L_44f89a:
          .string "erase block set to %s\n"
L_44f8b1:
          .string "-s"
L_44f8b4:
          .string "reboot has already been set on command line, ignoring -s\n"
          .zero 2
L_44f8f0:
          .string "setting shutdown on completion\n"
L_44f910:
          .string "-keys"
L_44f916:
          .string "-ip"
L_44f91a:
          .string "setting forced IP to %s\n"
L_44f933:
          .string "-r"
L_44f936:
          .string "setting read filename to %s\n"
L_44f953:
          .string "-w"
L_44f956:
          .string "setting write filename to %s\n"
L_44f974:
          .string "-e"
          .zero 1
L_44f978:
          .string "setting avatar/kinect files base path to %s\n"
L_44f9a5:
          .string "-c"
L_44f9a8:
          .string "setting xbox compatibility files base path to %s\n"
L_44f9da:
          .string "-i"
L_44f9dd:
          .string "info dump path set to %s\n"
L_44f9f7:
          .string "-p"
L_44f9fa:
          .string "patch file set to %s\n"
L_44fa10:
          .string "-v"
          .zero 1
L_44fa14:
          .string "\n\n***** ERROR: cannot send avatar data when a HDD does not exist!\n"
          .zero 1
L_44fa58:
          .string "\n\n***** ERROR: cannot send xbox compatibility data when a HDD does not exist!\n"
          .zero 1
L_44faa8:
          .string "\n\n***** ERROR: invalid mode specified, please inform author\n"
          .zero 3
L_44fae8:
          .string "\n\n***** ERROR: unable to connect to xbox server\n"
          .zero 3
L_44fb1c:
          .long L_40896b
          .long L_4088b2
          .long L_4088fe
          .long L_4088bf
          .long L_4088c9
          .long L_4088e7
          .long L_4087ff
          .long L_408952
          .long L_40890b
          .long L_408928
          .long L_40878a
          .long L_40893d
          .long L_408899
          .zero 16

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
          .long FUN_406330 - .
          .byte 0xd
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_406740 - .
          .byte 0x3a
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
          .byte 0xc0
          .byte 0x8
          .byte 0x3
          .byte 0x12
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
          .byte 0xec
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
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x88
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_406980 - .
          .byte 0x1b
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
          .byte 0x2
          .byte 0x95
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
          .byte 0x42
          .byte 0xb
          .byte 0x2
          .byte 0x49
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
          .byte 0x34
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_406aa0 - .
          .byte 0xb7
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
          .byte 0x2
          .byte 0xa5
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
          .byte 0x43
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
          .byte 0x48
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xfc
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_406b60 - .
          .byte 0xf6
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
          .byte 0x69
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
          .byte 0x41
          .byte 0xb
          .byte 0x2
          .byte 0x63
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
          .byte 0x45
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x2c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x48
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_406c60 - .
          .byte 0xea
          .byte 0x1
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
          .byte 0x40
          .byte 0x3
          .byte 0x2c
          .byte 0x1
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x57
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x46
          .byte 0xb
          .byte 0x0
          .byte 0x6c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x78
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_406e50 - .
          .byte 0x9
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
          .byte 0x50
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
          .byte 0x3
          .byte 0x5f
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
          .byte 0x61
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
          .byte 0x34
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xe8
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long L_407160 - .
          .byte 0xb9
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
          .byte 0x49
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
          .byte 0x0
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x20
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long FUN_407320 - .
          .byte 0x89
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
          .byte 0x46
          .byte 0xe
          .byte 0xd0
          .byte 0x8
          .byte 0x2
          .byte 0xc4
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
          .byte 0xe7
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
          .byte 0x0
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x78
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long FUN_4076b0 - .
          .byte 0x91
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
          .byte 0x40
          .byte 0x3
          .byte 0xb
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
          .byte 0x41
          .byte 0xb
          .byte 0x57
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
          .byte 0x5b
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
          .byte 0x43
          .byte 0xb
          .byte 0x57
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
          .byte 0x47
          .byte 0xb
          .byte 0x68
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd0
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long FUN_407850 - .
          .byte 0xa6
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
          .byte 0x60
          .byte 0x3
          .byte 0x8
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
          .byte 0x57
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
          .byte 0x63
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
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long L_407a00 - .
          .byte 0xeb
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
          .byte 0x3
          .byte 0xf
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
          .byte 0x46
          .byte 0xb
          .byte 0x71
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
          .byte 0x6c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x94
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long FUN_407bf0 - .
          .byte 0x84
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
          .byte 0x3f
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
          .byte 0x46
          .byte 0xb
          .byte 0x5b
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
          .byte 0x57
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
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x4
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long L_408080 - .
          .byte 0xd9
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
          .byte 0x2
          .byte 0x78
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x43
          .byte 0xb
          .byte 0x57
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x48
          .byte 0xb
          .byte 0x57
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x48
          .byte 0xb
          .byte 0x57
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x44
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long FUN_408160 - .
          .byte 0xf2
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
          .byte 0xa1
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
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x84
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long FUN_408260 - .
          .byte 0x5f
          .byte 0xc
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
          .byte 0x70
          .byte 0x3
          .byte 0xcc
          .byte 0x1
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
          .byte 0x3
          .byte 0xcb
          .byte 0x3
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

.bss
.p2align 5
L_46f160:
          .zero 32

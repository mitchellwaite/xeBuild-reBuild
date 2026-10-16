# app/build.s -- image build: reading inputs with crc32 checks, patches, payloads
#
# mixed: `#@C name` lines are functions from build.c (re/splice.py)
#
# original placement:
#   .data          0044a700-0044b6a0
#   .eh_frame      0046a23c-0046ac70
#   .rdata         00458ca4-0045b4a4
#   .rdata$zzz     00463ae8-00463b14
#   .text          00427500-00430460

.intel_syntax noprefix
.globl _addBlsToImage
.globl _addUpdateBls
.globl _appendAddonPatches
.globl _bd_458ca4
.globl _bd_458ca8
.globl _bd_458ce1
.globl _bd_458cf9
.globl _bd_458cfc
.globl _bd_458d1b
.globl _bd_458d3c
.globl _bd_458d74
.globl _bd_458d98
.globl _bd_458f80
.globl _bd_458fb4
.globl _bd_458fe6
.globl _bd_458ff5
.globl _bd_45900a
.globl _bd_459012
.globl _bd_459021
.globl _bd_459030
.globl _bd_459050
.globl _bd_459070
.globl _bd_459090
.globl _bd_4590b0
.globl _bd_4590d1
.globl _bd_4590e7
.globl _bd_4590f2
.globl _bd_4590fe
.globl _bd_45910a
.globl _bd_459115
.globl _bd_45911f
.globl _bd_45912a
.globl _bd_459134
.globl _bd_45913f
.globl _bd_459151
.globl _bd_459160
.globl _bd_459164
.globl _bd_459955
.globl _bd_459e3c
.globl _bd_459e74
.globl _bd_459e9c
.globl _bd_459ec8
.globl _bd_459ed2
.globl _bd_459ed8
.globl _bd_459ede
.globl _bd_459ee4
.globl _bd_45a590
.globl _bd_45a5cc
.globl _bd_45a5e0
.globl _bd_45a618
.globl _bd_45a664
.globl _bd_45a6a4
.globl _bd_45a6b0
.globl _bd_45a6df
.globl _bd_45a6f8
.globl _bd_45a71e
.globl _bd_45a728
.globl _bd_45a738
.globl _bd_45a748
.globl _bd_45a785
.globl _bd_45a78c
.globl _bd_45a7c4
.globl _bd_45a7f8
.globl _bd_45a80e
.globl _bd_45a8af
.globl _buildFlash
.globl _calcBlAreaSize
.globl _checkBl
.globl _encodeBls
.globl _extractSmcConfig
.globl _fixupPatchSet
.globl _loadBaseFile
.globl _loadBaseFileMeta
.globl _loadBlFiles
.globl _loadConsoleBlFiles
.globl _loadFileCrc
.globl _loadInputFile
.globl _logPowerButton
.globl _patchBlsBlmod
.globl _patchBlsResign
.globl _patchSmcConfig
.globl _timestampToFileTime
.globl _verifyBlSigs

.text
.p2align 4
_loadBaseFile:
          cmp BYTE PTR [L_47ad4c],0
          je L_427635
          push EBP
          push EDI
          mov EDI,EAX
          push ESI
          push EBX
          mov EBX,EDX
          sub ESP,1052
          lea ESI,DWORD PTR [ESP+16]
          mov DWORD PTR [ESP+4],OFFSET L_47ad4c
          mov DWORD PTR [ESP],ESI
          call _strcpy
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],ESI
          call _strcat
          mov DWORD PTR [ESP+4],OFFSET _bd_458ca4
          mov DWORD PTR [ESP],ESI
          call _fopen
          test EAX,EAX
          mov EDI,EAX
          je L_427647
          mov EAX,DWORD PTR [EBX+1036]
          test EAX,EAX
          je L_427567
          mov DWORD PTR [ESP],EAX
          call _free
L_427567:
          mov DWORD PTR [ESP],EDI
          call _getFileSize
          test EAX,EAX
          mov EBP,EAX
          je L_427605
          mov DWORD PTR [EBX+1040],EAX
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET _bd_458ce1
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+4],1
          mov EAX,DWORD PTR [EBX+1040]
          add EAX,65536
          mov DWORD PTR [ESP],EAX
          call _calloc
          test EAX,EAX
          mov DWORD PTR [EBX+1036],EAX
          .byte 0x0f,0x84; .long L_427640-.-4   # je L_427640
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EAX
          call _fread
          mov DWORD PTR [ESP],EDI
          call _fclose
          mov DWORD PTR [ESP+4],OFFSET _bd_458cf9
          mov DWORD PTR [ESP],1
          call _log_printf
          xor EAX,EAX
L_4275fa:
          add ESP,1052
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_427605:
          mov DWORD PTR [ESP],EDI
          call _fclose
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET _bd_458ca8
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,1052
          mov EAX,1
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_427635:
          mov EAX,4294967295
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_427640:
          mov EAX,4294967294
          jmp L_4275fa
L_427647:
          mov EAX,4294967295
          jmp L_4275fa
          .byte 0x66
          .byte 0x90
#@C _findFileOffset
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _findFileSize
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _findFile
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
_loadFileCrc:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov EDI,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+4],OFFSET _bd_458ca4
          mov ESI,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP],EDI
          call _fopen
          test EAX,EAX
          je L_42793a
          mov EBX,EAX
          mov EAX,DWORD PTR [ESI+1036]
          test EAX,EAX
          je L_42776b
          mov DWORD PTR [ESP],EAX
          call _free
L_42776b:
          mov DWORD PTR [ESP],EBX
          call _getFileSize
          test EAX,EAX
          mov EBP,EAX
          je L_427900
          mov DWORD PTR [ESI+1040],EAX
          mov EAX,DWORD PTR [ESP+76]
          test EAX,EAX
          je L_4277e0
          test EBP,15
          je L_4277e0
          mov ECX,DWORD PTR [ESP+72]
          lea EAX,DWORD PTR [EBP+15]
          and EAX,4294967280
          test ECX,ECX
          mov DWORD PTR [ESI+1040],EAX
          je L_4277ee
          cmp EBP,EAX
          je L_4278b0
          mov DWORD PTR [ESP+16],EAX
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET _bd_458cfc
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [ESI+1040]
          jmp L_4277ee
L_4277d7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_4277e0:
          mov EAX,DWORD PTR [ESP+72]
          test EAX,EAX
          jne L_4278b0
          mov EAX,EBP
L_4277ee:
          add EAX,65536
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call _calloc
          test EAX,EAX
          mov DWORD PTR [ESI+1036],EAX
          je L_427930
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EAX
          call _fread
          mov DWORD PTR [ESP],EBX
          call _fclose
          mov EDX,DWORD PTR [ESP+80]
          test EDX,EDX
          je L_4278e0
          mov DWORD PTR [ESP+4],EBP
          mov EAX,DWORD PTR [ESI+1036]
          mov DWORD PTR [ESP],EAX
          call _crc32
          mov EBX,EAX
          mov EAX,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP+4],OFFSET _bd_458d1b
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+12],EAX
          call _log_printf
          xor EAX,EAX
          cmp DWORD PTR [ESP+80],EBX
          je L_4278a2
          mov EAX,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET _bd_458d3c
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+16],EAX
          call _log_printf
          mov EAX,1
L_4278a2:
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
L_4278b0:
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET _bd_458ce1
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [ESI+1040]
          jmp L_4277ee
L_4278d7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_4278e0:
          mov DWORD PTR [ESP+4],OFFSET _bd_458cf9
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,44
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x66
          .byte 0x90
L_427900:
          mov DWORD PTR [ESP],EBX
          call _fclose
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET _bd_458ca8
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,44
          mov EAX,1
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_427930:
          mov EAX,4294967294
          jmp L_4278a2
L_42793a:
          mov EAX,4294967295
          jmp L_4278a2
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
#@C _readMetaFile
L_4279a7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
#@C _makeTimestamp
_timestampToFileTime:
          sub ESP,28
          mov EDX,DWORD PTR [ESP+32]
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+8],EAX
          movzx EAX,WORD PTR [EDX+2]
          rol AX,8
          movzx EAX,AX
          mov DWORD PTR [ESP+4],EAX
          movzx EAX,WORD PTR [EDX]
          rol AX,8
          movzx EAX,AX
          mov DWORD PTR [ESP],EAX
          call _DosDateTimeToFileTime
          add ESP,28
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
_loadBaseFileMeta:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,1052
          cmp BYTE PTR [L_47ad4c],0
          mov EDI,DWORD PTR [ESP+1076]
          je L_427ca0
          lea EBX,DWORD PTR [ESP+16]
          mov DWORD PTR [ESP+4],OFFSET L_47ad4c
          mov DWORD PTR [ESP],EBX
          call _strcpy
          mov EAX,DWORD PTR [ESP+1072]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call _strcat
          mov DWORD PTR [ESP+4],OFFSET _bd_458ca4
          mov DWORD PTR [ESP],EBX
          call _fopen
          test EAX,EAX
          mov ESI,EAX
          je L_427ca0
          mov EAX,DWORD PTR [EDI+1036]
          test EAX,EAX
          je L_427b21
          mov DWORD PTR [ESP],EAX
          call _free
L_427b21:
          mov DWORD PTR [ESP],ESI
          call _getFileSize
          test EAX,EAX
          mov EBP,EAX
          je L_427c70
          mov DWORD PTR [EDI+1040],EAX
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET _bd_458ce1
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+4],1
          mov EAX,DWORD PTR [EDI+1040]
          add EAX,65536
          mov DWORD PTR [ESP],EAX
          call _calloc
          test EAX,EAX
          mov DWORD PTR [EDI+1036],EAX
          je L_427cb0
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EAX
          call _fread
          mov DWORD PTR [ESP],ESI
          call _fclose
          mov DWORD PTR [ESP+4],OFFSET _bd_458cf9
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EDX,DWORD PTR [ESP+1080]
          test EDX,EDX
          jne L_427bd0
L_427bbd:
          xor EAX,EAX
L_427bbf:
          add ESP,1052
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
L_427bd0:
          mov EDX,EBX
L_427bd2:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_427bd2
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          mov EAX,97
          sbb EDX,3
          mov DWORD PTR [EDX],1952804142
          mov WORD PTR [EDX+4],AX
          mov DWORD PTR [ESP+4],OFFSET _bd_458ca4
          mov DWORD PTR [ESP],EBX
          call _fopen
          test EAX,EAX
          mov ESI,EAX
          je L_427bbd
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+1080]
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP+4],4
          mov DWORD PTR [ESP],EAX
          call _fread
          mov DWORD PTR [ESP],ESI
          call _fclose
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET _bd_458d98
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_427bbd
          .byte 0x90
L_427c70:
          mov DWORD PTR [ESP],ESI
          call _fclose
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET _bd_458ca8
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,1052
          mov EAX,1
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_427ca0:
          mov EAX,4294967295
          jmp L_427bbf
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_427cb0:
          mov EAX,4294967294
          jmp L_427bbf
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _loadCommonFile
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
_loadInputFile:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,1116
          mov ESI,DWORD PTR [ESP+1136]
          mov DWORD PTR [ESP+4],47
          mov EDI,DWORD PTR [ESP+1140]
          mov DWORD PTR [ESP],ESI
          call _strrchr
          test EAX,EAX
          je L_428340
L_428070:
          lea EBX,DWORD PTR [EAX+1]
L_428073:
          mov DWORD PTR [ESP+4],58
          mov DWORD PTR [ESP],ESI
          call _strrchr
          test EAX,EAX
          je L_428360
          lea EBP,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EBP
          call _strcpy
L_42809b:
          mov EAX,DWORD PTR [ESP+1148]
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+16],EAX
          mov EAX,DWORD PTR [ESP+1144]
          mov DWORD PTR [ESP+12],EAX
          call _loadFileCrc
          mov ESI,EAX
          mov EAX,DWORD PTR [ESP+1152]
          test EAX,EAX
          je L_4280da
          test ESI,ESI
          je L_428290
L_4280da:
          mov EAX,DWORD PTR [ESP+1156]
          test ESI,ESI
          setne DL
          test EAX,EAX
          je L_4280f2
          test DL,DL
          jne L_4281b2
L_4280f2:
          mov EAX,DWORD PTR [ESP+1160]
          test EAX,EAX
          je L_428101
          test DL,DL
          jne L_428160
L_428101:
          mov EAX,DWORD PTR [ESP+1164]
          test EAX,EAX
          setne AL
          and EAX,EDX
L_42810f:
          test AL,AL
          jne L_428120
L_428113:
          mov EAX,ESI
L_428115:
          add ESP,1116
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_428120:
          mov EAX,DWORD PTR [ESP+1152]
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+16],EAX
          mov EAX,DWORD PTR [ESP+1148]
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+1144]
          mov DWORD PTR [ESP+8],EAX
          call _loadCommonFile
          add ESP,1116
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
L_428160:
          lea EDX,DWORD PTR [EDI+1040]
          lea EAX,DWORD PTR [ESP+52]
          lea EBP,DWORD PTR [EDI+1036]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP+44],EDX
          call _fsGetFile
          test EAX,EAX
          mov EDX,DWORD PTR [ESP+44]
          jne L_428400
          cmp DWORD PTR [_xb],2
          je L_428580
L_4281a1:
          mov ECX,DWORD PTR [ESP+1164]
          test ECX,ECX
          setne AL
          jmp L_42810f
L_4281b2:
          lea EAX,DWORD PTR [EDI+1040]
          mov DWORD PTR [ESP],EBX
          mov BYTE PTR [ESP+44],DL
          mov DWORD PTR [ESP+8],EAX
          lea EAX,DWORD PTR [EDI+1036]
          mov DWORD PTR [ESP+4],EAX
          call _suGetFile
          test EAX,EAX
          movzx EDX,BYTE PTR [ESP+44]
          je L_4280f2
          mov EAX,DWORD PTR [EDI+1040]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_458dd0
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+12],EAX
          call _log_printf
          mov EBP,DWORD PTR [ESP+1148]
          movzx EDX,BYTE PTR [ESP+44]
          test EBP,EBP
          je L_428555
          mov EAX,DWORD PTR [EDI+1040]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [EDI+1036]
          mov DWORD PTR [ESP],EAX
          call _crc32
          mov EBP,EAX
          mov EAX,DWORD PTR [ESP+1148]
          mov DWORD PTR [ESP+4],OFFSET _bd_458d1b
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+12],EAX
          call _log_printf
          cmp DWORD PTR [ESP+1148],EBP
          je L_428690
          mov EAX,DWORD PTR [ESP+1148]
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET _bd_458d3c
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+16],EAX
          call _log_printf
          movzx EDX,BYTE PTR [ESP+44]
          jmp L_4280f2
L_428290:
          mov EDX,EBP
L_428292:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_428292
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          mov EAX,97
          sbb EDX,3
          mov DWORD PTR [EDX],1952804142
          mov WORD PTR [EDX+4],AX
          mov DWORD PTR [ESP+4],OFFSET _bd_458ca4
          mov DWORD PTR [ESP],EBP
          call _fopen
          test EAX,EAX
          je L_428385
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+44],EAX
          mov EAX,DWORD PTR [ESP+1152]
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP+4],4
          mov DWORD PTR [ESP],EAX
          call _fread
          mov EDX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EDX
          call _fclose
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET _bd_458d98
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_4280da
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_428340:
          mov DWORD PTR [ESP+4],92
          mov DWORD PTR [ESP],ESI
          call _strrchr
          test EAX,EAX
          jne L_428070
          mov EBX,ESI
          jmp L_428073
          .byte 0x90
L_428360:
          lea EBP,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP+4],OFFSET L_47b14c
          mov DWORD PTR [ESP],EBP
          call _strcpy
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EBP
          call _strcat
          jmp L_42809b
L_428385:
          mov EAX,DWORD PTR [L_479ec4]
          test EAX,EAX
          je L_428500
          lea EAX,DWORD PTR [ESP+64]
          lea EBP,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+44],EAX
          call _GetSystemTime
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EAX
          call _SystemTimeToFileTime
L_4283b6:
          lea EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+8],EAX
          lea EAX,DWORD PTR [ESP+50]
          mov DWORD PTR [ESP+4],EAX
          call _FileTimeToDosDateTime
          movzx EAX,WORD PTR [ESP+50]
          mov ECX,DWORD PTR [ESP+1152]
          mov EDX,EAX
          mov BYTE PTR [ECX+1],AL
          movzx EAX,WORD PTR [ESP+52]
          shr DX,8
          mov BYTE PTR [ECX],DL
          mov EDX,EAX
          mov BYTE PTR [ECX+3],AL
          shr DX,8
          mov BYTE PTR [ECX+2],DL
          jmp L_4280da
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_428400:
          mov EAX,DWORD PTR [EDI+1040]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_458df0
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+12],EAX
          call _log_printf
          mov EAX,DWORD PTR [ESP+1148]
          test EAX,EAX
          je L_428530
          mov EAX,DWORD PTR [EDI+1040]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [EDI+1036]
          mov DWORD PTR [ESP],EAX
          call _crc32
          mov EBP,EAX
          mov EAX,DWORD PTR [ESP+1148]
          mov DWORD PTR [ESP+4],OFFSET _bd_458d1b
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+12],EAX
          call _log_printf
          cmp DWORD PTR [ESP+1148],EBP
          jne L_428640
          mov EAX,DWORD PTR [ESP+1152]
          test EAX,EAX
          je L_428631
          mov EAX,DWORD PTR [L_479ec4]
          test EAX,EAX
          je L_428732
          lea EBX,DWORD PTR [ESP+64]
          lea EBP,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP],EBX
          call _GetSystemTime
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EBX
          call _SystemTimeToFileTime
L_4284b3:
          lea EAX,DWORD PTR [ESP+50]
          mov DWORD PTR [ESP],EBP
          xor ESI,ESI
          mov DWORD PTR [ESP+8],EAX
          lea EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+4],EAX
          call _FileTimeToDosDateTime
          movzx EAX,WORD PTR [ESP+48]
          mov EBX,DWORD PTR [ESP+1152]
          mov EDX,EAX
          mov BYTE PTR [EBX+1],AL
          movzx EAX,WORD PTR [ESP+50]
          shr DX,8
          mov BYTE PTR [EBX],DL
          mov EDX,EAX
          mov BYTE PTR [EBX+3],AL
          shr DX,8
          mov BYTE PTR [EBX+2],DL
          jmp L_428113
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_428500:
          mov DWORD PTR [ESP+4],OFFSET _bd_458d74
          mov DWORD PTR [ESP],2
          lea EBP,DWORD PTR [ESP+56]
          call _log_printf
          mov DWORD PTR [ESP+60],30268127
          mov DWORD PTR [ESP+56],1903825408
          jmp L_4283b6
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_428530:
          mov DWORD PTR [ESP+4],OFFSET _bd_458cf9
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [ESP+1164]
          test EAX,EAX
          setne AL
          jmp L_42810f
L_428555:
          mov DWORD PTR [ESP+4],OFFSET _bd_458cf9
          mov DWORD PTR [ESP],1
          mov BYTE PTR [ESP+44],DL
          call _log_printf
          movzx EDX,BYTE PTR [ESP+44]
          jmp L_4280f2
L_428577:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_428580:
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EBX
          call _updateGetFile
          test EAX,EAX
          je L_4281a1
          mov EAX,DWORD PTR [EDI+1040]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_458e14
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+12],EAX
          call _log_printf
          mov EBP,DWORD PTR [ESP+1148]
          test EBP,EBP
          je L_42875f
          mov EAX,DWORD PTR [EDI+1040]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [EDI+1036]
          mov DWORD PTR [ESP],EAX
          call _crc32
          mov EBP,EAX
          mov EAX,DWORD PTR [ESP+1148]
          mov DWORD PTR [ESP+4],OFFSET _bd_458d1b
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+12],EAX
          call _log_printf
          cmp DWORD PTR [ESP+1148],EBP
          jne L_428640
          mov EDX,DWORD PTR [ESP+1152]
          test EDX,EDX
          je L_428631
          mov EAX,DWORD PTR [ESP+1152]
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],EAX
          call _makeTimestamp
L_428631:
          xor ESI,ESI
          jmp L_428113
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_428640:
          mov EAX,DWORD PTR [EDI+1036]
          mov DWORD PTR [ESP],EAX
          call _free
          mov EAX,DWORD PTR [ESP+1148]
          mov DWORD PTR [EDI+1036],0
          mov DWORD PTR [EDI+1040],0
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET _bd_458d3c
          mov DWORD PTR [ESP+16],EAX
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_4281a1
          .byte 0x66
          .byte 0x90
L_428690:
          mov ECX,DWORD PTR [ESP+1152]
          test ECX,ECX
          je L_428701
          mov EDX,DWORD PTR [L_479ec4]
          test EDX,EDX
          je L_428708
          lea EBX,DWORD PTR [ESP+64]
          lea EBP,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP],EBX
          call _GetSystemTime
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EBX
          call _SystemTimeToFileTime
L_4286c1:
          lea EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+8],EAX
          lea EAX,DWORD PTR [ESP+50]
          mov DWORD PTR [ESP+4],EAX
          call _FileTimeToDosDateTime
          movzx EAX,WORD PTR [ESP+50]
          mov EBX,DWORD PTR [ESP+1152]
          mov EDX,EAX
          mov BYTE PTR [EBX+1],AL
          movzx EAX,WORD PTR [ESP+52]
          shr DX,8
          mov BYTE PTR [EBX],DL
          mov EDX,EAX
          mov BYTE PTR [EBX+3],AL
          shr DX,8
          mov BYTE PTR [EBX+2],DL
L_428701:
          xor EAX,EAX
          jmp L_428115
L_428708:
          mov DWORD PTR [ESP+4],OFFSET _bd_458d74
          mov DWORD PTR [ESP],2
          lea EBP,DWORD PTR [ESP+56]
          call _log_printf
          mov DWORD PTR [ESP+60],30268127
          mov DWORD PTR [ESP+56],1903825408
          jmp L_4286c1
L_428732:
          mov DWORD PTR [ESP+4],OFFSET _bd_458d74
          mov DWORD PTR [ESP],2
          lea EBP,DWORD PTR [ESP+56]
          call _log_printf
          mov DWORD PTR [ESP+60],30268127
          mov DWORD PTR [ESP+56],1903825408
          jmp L_4284b3
L_42875f:
          mov DWORD PTR [ESP+4],OFFSET _bd_458cf9
          mov DWORD PTR [ESP],1
          xor ESI,ESI
          call _log_printf
          jmp L_428113
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _loadBinFile
          .byte 0x66
          .byte 0x90
#@C _loadLocalFile
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
#@C _setFileData
_appendAddonPatches:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,60
          mov EAX,DWORD PTR [ESP+80]
          mov EAX,DWORD PTR [EAX+1040]
          mov DWORD PTR [ESP],16384
          lea ESI,DWORD PTR [EAX-4]
          mov DWORD PTR [ESP+44],EAX
          call _malloc
          mov DWORD PTR [ESP+8],16384
          mov DWORD PTR [ESP+4],255
          mov EDI,EAX
          mov DWORD PTR [ESP],EAX
          call _memset
          mov EAX,DWORD PTR [ESP+80]
          mov EAX,DWORD PTR [EAX+1036]
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],EAX
          call _memcpy
          mov EAX,DWORD PTR [L_4c4f94]
          test EAX,EAX
          jle L_428c54
          mov EBP,OFFSET L_4c0c94
          xor EBX,EBX
          mov DWORD PTR [ESP+44],0
          jmp L_428bf6
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_428b90:
          mov EDX,DWORD PTR [EBP+1036]
          lea EAX,DWORD PTR [EDX+EAX*1-4]
          mov DWORD PTR [ESP],EAX
          call _getBeU32
          cmp EAX,-1
          mov EAX,DWORD PTR [EBP+1040]
          je L_428d05
L_428bb1:
          lea EDX,DWORD PTR [ESI+EAX*1]
          cmp EDX,16384
          ja L_428ce0
          mov ECX,DWORD PTR [EBP+1036]
          lea EDX,DWORD PTR [EDI+ESI*1]
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],EDX
          mov DWORD PTR [ESP+4],ECX
          call _memcpy
          mov EAX,DWORD PTR [EBP+1040]
          add DWORD PTR [ESP+44],EAX
          add ESI,EAX
L_428be5:
          add EBX,1
          add EBP,1068
          cmp DWORD PTR [L_4c4f94],EBX
          jle L_428c60
L_428bf6:
          mov DWORD PTR [ESP],EBP
          call _loadBinFile
          test EAX,EAX
          jne L_428c32
          mov EAX,DWORD PTR [EBP+1040]
          test AL,3
          je L_428b90
          mov DWORD PTR [ESP+16],EAX
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+8],OFFSET L_47a54c
          mov DWORD PTR [ESP+4],OFFSET L_458e7c
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_428be5
L_428c32:
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+8],OFFSET L_47a54c
          mov DWORD PTR [ESP+4],OFFSET L_458ed0
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_428be5
L_428c54:
          mov DWORD PTR [ESP+44],0
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_428c60:
          lea EAX,DWORD PTR [EDI+ESI*1+4]
          mov DWORD PTR [EDI+ESI*1],4294967295
          add ESI,8
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EAX
          call _setBeU32
          mov EAX,DWORD PTR [ESP+80]
          mov EAX,DWORD PTR [EAX+1036]
          test EAX,EAX
          je L_428c94
          mov DWORD PTR [ESP],EAX
          call _free
L_428c94:
          mov EAX,DWORD PTR [ESP+80]
          mov DWORD PTR [EAX+1036],EDI
          mov DWORD PTR [EAX+1040],ESI
          mov EAX,DWORD PTR [L_4c4f94]
          test EAX,EAX
          je L_428cd1
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+16],ESI
          mov DWORD PTR [ESP+4],OFFSET L_458f04
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
L_428cd1:
          add ESP,60
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
L_428ce0:
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+8],OFFSET L_47a54c
          mov DWORD PTR [ESP+4],OFFSET L_458e34
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_428be5
L_428d05:
          sub EAX,4
          mov DWORD PTR [EBP+1040],EAX
          jmp L_428bb1
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
#@C _showSmcConfig
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _iniRangeOk
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
_patchSmcConfig:
          push ESI
          push EBX
          sub ESP,36
          mov DWORD PTR [ESP+4],OFFSET L_45919c
          mov DWORD PTR [ESP],1
          mov ESI,DWORD PTR [ESP+48]
          call _log_printf
          mov EAX,DWORD PTR [L_479f18]
          lea EDX,DWORD PTR [EAX-40]
          cmp EDX,80
          jbe L_429560
          lea EDX,DWORD PTR [EAX-1]
          xor EBX,EBX
          cmp EDX,-3
          jbe L_4296b5
L_42922c:
          mov EAX,DWORD PTR [L_479f1c]
          lea EDX,DWORD PTR [EAX-40]
          cmp EDX,80
          jbe L_429550
          lea EDX,DWORD PTR [EAX-1]
          cmp EDX,-3
          jbe L_429680
L_429249:
          mov EAX,DWORD PTR [L_479f20]
          lea EDX,DWORD PTR [EAX-40]
          cmp EDX,80
          jbe L_429540
          lea EDX,DWORD PTR [EAX-1]
          cmp EDX,-3
          jbe L_429645
L_429266:
          mov EAX,DWORD PTR [L_479f24]
          lea EDX,DWORD PTR [EAX-40]
          cmp EDX,80
          jbe L_429530
          lea EDX,DWORD PTR [EAX-1]
          cmp EDX,-3
          jbe L_429610
L_429283:
          mov EAX,DWORD PTR [L_479f28]
          lea EDX,DWORD PTR [EAX-40]
          cmp EDX,80
          jbe L_429520
          lea EDX,DWORD PTR [EAX-1]
          cmp EDX,-3
          jbe L_4295d5
L_4292a0:
          mov EAX,DWORD PTR [L_479f2c]
          lea EDX,DWORD PTR [EAX-40]
          cmp EDX,80
          jbe L_429510
          lea EDX,DWORD PTR [EAX-1]
          cmp EDX,-3
          jbe L_4295a0
L_4292bd:
          mov EAX,DWORD PTR [L_479f30]
          cmp EAX,-1
          je L_4292f0
          lea EDX,DWORD PTR [EAX-40]
          cmp EDX,60
          jbe L_429700
          lea EDX,DWORD PTR [EAX-1]
          cmp EDX,-3
          jbe L_429770
L_4292df:
          cmp BYTE PTR [ESI+17],127
          je L_4292f0
          mov BYTE PTR [ESI+17],127
          mov EBX,1
          .byte 0x66   # nop
          nop
L_4292f0:
          mov EAX,DWORD PTR [L_479f34]
          cmp EAX,-1
          je L_429320
          lea EDX,DWORD PTR [EAX-40]
          cmp EDX,60
          jbe L_4296f0
          lea EDX,DWORD PTR [EAX-1]
          cmp EDX,-3
          jbe L_429710
L_429312:
          mov BYTE PTR [ESI+18],127
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_429320:
          mov EAX,DWORD PTR [L_479f38]
          cmp EAX,-1
          je L_429358
          mov EDX,EAX
          mov ECX,EAX
          mov EBX,1
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
          mov DWORD PTR [ESI+552],EAX
L_429358:
          mov EAX,DWORD PTR [L_479f3c]
          cmp EAX,-1
          je L_42936b
          test AX,AX
          jne L_429570
L_42936b:
          mov EAX,DWORD PTR [L_479f40]
          cmp EAX,-1
          je L_42958e
L_429379:
          mov EDX,EAX
          mov ECX,EAX
          mov EBX,1
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
          mov DWORD PTR [ESI+564],EAX
L_4293a7:
          test EAX,EAX
          je L_4293f0
          call _macidSet
          test EAX,EAX
          .byte 0x0f,0x85; .long L_429434-.-4   # jne L_429434
          test EBX,EBX
          jne L_4294c5
L_4293c0:
          mov DWORD PTR [ESP+4],OFFSET L_459355
          mov DWORD PTR [ESP],1
          call _log_printf
L_4293d4:
          mov DWORD PTR [ESP+4],OFFSET L_459371
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,36
          mov EAX,EBX
          pop EBX
          pop ESI
          ret 
L_4293f0:
          mov DWORD PTR [ESP+4],OFFSET L_459260
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_4592d8
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESI+564],16777216
          call _macidSet
          test EAX,EAX
          je L_4294c5
          mov EBX,1
L_429434:
          movzx EAX,BYTE PTR [L_479f44]
          mov EDX,1
          cmp AL,BYTE PTR [ESI+544]
          mov BYTE PTR [ESI+544],AL
          movzx EAX,BYTE PTR [L_479f45]
          cmovne EBX,EDX
          cmp AL,BYTE PTR [ESI+545]
          mov BYTE PTR [ESI+545],AL
          movzx EAX,BYTE PTR [L_479f46]
          cmovne EBX,EDX
          cmp AL,BYTE PTR [ESI+546]
          mov BYTE PTR [ESI+546],AL
          movzx EAX,BYTE PTR [L_479f47]
          cmovne EBX,EDX
          cmp AL,BYTE PTR [ESI+547]
          mov BYTE PTR [ESI+547],AL
          movzx EAX,BYTE PTR [L_479f48]
          cmovne EBX,EDX
          cmp AL,BYTE PTR [ESI+548]
          mov BYTE PTR [ESI+548],AL
          movzx EAX,BYTE PTR [L_479f49]
          cmovne EBX,EDX
          cmp BYTE PTR [ESI+549],AL
          mov BYTE PTR [ESI+549],AL
          cmovne EBX,EDX
          test EBX,EBX
          je L_4293c0
L_4294c5:
          mov DWORD PTR [ESP],ESI
          mov EBX,1
          call _calcConfigSum
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
          mov DWORD PTR [ESI],EAX
          mov DWORD PTR [ESP+4],OFFSET L_459340
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_4293d4
L_429510:
          mov BYTE PTR [ESI+46],AL
          mov EBX,1
          jmp L_4292bd
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_429520:
          mov BYTE PTR [ESI+45],AL
          mov EBX,1
          jmp L_4292a0
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_429530:
          mov BYTE PTR [ESI+44],AL
          mov EBX,1
          jmp L_429283
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_429540:
          mov BYTE PTR [ESI+43],AL
          mov EBX,1
          jmp L_429266
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_429550:
          mov BYTE PTR [ESI+42],AL
          mov EBX,1
          jmp L_429249
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_429560:
          mov BYTE PTR [ESI+41],AL
          mov EBX,1
          jmp L_42922c
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_429570:
          rol AX,8
          mov EBX,1
          mov WORD PTR [ESI+556],AX
          mov EAX,DWORD PTR [L_479f40]
          cmp EAX,-1
          jne L_429379
L_42958e:
          mov EAX,DWORD PTR [ESI+564]
          jmp L_4293a7
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4295a0:
          mov DWORD PTR [ESP+20],120
          mov DWORD PTR [ESP+16],40
          mov DWORD PTR [ESP+12],OFFSET L_4591f4
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET _bd_459164
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_4292bd
L_4295d5:
          mov DWORD PTR [ESP+20],120
          mov DWORD PTR [ESP+16],40
          mov DWORD PTR [ESP+12],OFFSET L_4591e8
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET _bd_459164
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_4292a0
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_429610:
          mov DWORD PTR [ESP+20],120
          mov DWORD PTR [ESP+16],40
          mov DWORD PTR [ESP+12],OFFSET L_4591dc
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET _bd_459164
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_429283
L_429645:
          mov DWORD PTR [ESP+20],120
          mov DWORD PTR [ESP+16],40
          mov DWORD PTR [ESP+12],OFFSET L_4591d2
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET _bd_459164
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_429266
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_429680:
          mov DWORD PTR [ESP+20],120
          mov DWORD PTR [ESP+16],40
          mov DWORD PTR [ESP+12],OFFSET L_4591ca
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET _bd_459164
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_429249
L_4296b5:
          mov DWORD PTR [ESP+20],120
          mov DWORD PTR [ESP+16],40
          mov DWORD PTR [ESP+12],OFFSET L_4591c2
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET _bd_459164
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_42922c
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4296f0:
          or EAX,4294967168
          mov EBX,1
          mov BYTE PTR [ESI+18],AL
          jmp L_429320
L_429700:
          or EAX,4294967168
          mov EBX,1
          mov BYTE PTR [ESI+17],AL
          jmp L_4292f0
L_429710:
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+20],100
          mov DWORD PTR [ESP+16],40
          mov DWORD PTR [ESP+12],OFFSET L_459256
          mov DWORD PTR [ESP+4],OFFSET _bd_459164
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_479f34]
          test EAX,EAX
          je L_429312
          mov DWORD PTR [ESP+4],OFFSET L_459388
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_429320
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_429770:
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+20],100
          mov DWORD PTR [ESP+16],40
          mov DWORD PTR [ESP+12],OFFSET L_459202
          mov DWORD PTR [ESP+4],OFFSET _bd_459164
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_479f30]
          test EAX,EAX
          je L_4292df
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_45920c
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_4292f0
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
_extractSmcConfig:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov EAX,DWORD PTR [ESP+64]
          mov EDI,DWORD PTR [ESP+68]
          mov EBP,DWORD PTR [ESP+72]
          mov EAX,DWORD PTR [EAX+1036]
          test EAX,EAX
          je L_4297f5
          mov DWORD PTR [ESP],EAX
          call _free
L_4297f5:
          mov EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [EAX+1040],1024
          mov DWORD PTR [ESP],1024
          call _malloc
          mov EDX,DWORD PTR [ESP+64]
          test EAX,EAX
          mov DWORD PTR [EDX+1036],EAX
          je L_429adb
          mov DWORD PTR [ESP+4],OFFSET L_4593d7
          mov DWORD PTR [ESP],1
          xor EBX,EBX
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_4593ec
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_4593d7
          mov DWORD PTR [ESP],1
          call _log_printf
          xor EAX,EAX
          jmp L_429865
L_429863:
          mov EBX,ESI
L_429865:
          lea ESI,DWORD PTR [EBX+512]
          cmp ESI,EBP
          ja L_4299b0
          lea EAX,DWORD PTR [EDI+EBX*1]
          mov DWORD PTR [ESP],EAX
          call _smcConfigOk
          cmp EAX,1
          jne L_429863
L_429883:
          lea EAX,DWORD PTR [EDI+EBX*1+524]
          mov DWORD PTR [ESP+4],4
          mov DWORD PTR [ESP],EAX
          call _checkZeros
          test EAX,EAX
          jne L_429a0a
          sub EBP,EBX
          cmp EBP,16895
          jbe L_429ae5
          mov DWORD PTR [ESP+4],OFFSET L_459414
          mov DWORD PTR [ESP],1
          call _log_printf
          lea EAX,DWORD PTR [EDI+EBX*1]
          xor EDX,EDX
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_4298d0:
          mov EDI,DWORD PTR [ESP+64]
          mov ESI,DWORD PTR [EAX]
          mov ECX,DWORD PTR [EDI+1036]
          add ECX,EDX
          add EDX,512
          mov DWORD PTR [ECX],ESI
          lea EDI,DWORD PTR [ECX+4]
          mov ESI,DWORD PTR [EAX+508]
          and EDI,4294967292
          mov DWORD PTR [ECX+508],ESI
          sub ECX,EDI
          mov ESI,EAX
          sub ESI,ECX
          add ECX,512
          add EAX,528
          shr ECX,2
          cmp EDX,4096
          rep movsd 
          jne L_4298d0
L_429916:
          test EBX,EBX
          jne L_429abe
L_42991e:
          mov DWORD PTR [ESP+4],OFFSET L_4594a4
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_4594b8
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_4594a4
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [ESP+64]
          mov EAX,DWORD PTR [EAX+1036]
          mov DWORD PTR [ESP],EAX
          call _showSmcConfig
          mov DWORD PTR [ESP+4],OFFSET L_459371
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [ESP+64]
          mov EAX,DWORD PTR [EAX+1036]
          mov DWORD PTR [ESP],EAX
          call _patchSmcConfig
          mov EDX,EAX
          xor EAX,EAX
          test EDX,EDX
          jne L_429a63
L_42999e:
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
L_4299b0:
          test EAX,EAX
          jne L_429883
          xor EBX,EBX
          jmp L_4299c2
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_4299c0:
          mov EBX,ESI
L_4299c2:
          lea ESI,DWORD PTR [EBX+528]
          cmp ESI,EBP
          ja L_4299e1
          lea EAX,DWORD PTR [EDI+EBX*1]
          mov DWORD PTR [ESP],EAX
          call _smcConfigOk
          cmp EAX,1
          jne L_4299c0
          jmp L_429883
L_4299e1:
          test EAX,EAX
          jne L_429883
          mov DWORD PTR [ESP+4],OFFSET L_4594e0
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,44
          mov EAX,2
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_429a0a:
          mov DWORD PTR [ESP+4],OFFSET L_459401
          mov DWORD PTR [ESP],1
          sub EBP,EBX
          call _log_printf
          cmp EBP,1023
          jbe L_429916
          mov EAX,DWORD PTR [ESP+64]
          lea ESI,DWORD PTR [EDI+EBX*1]
          mov EDX,DWORD PTR [ESI]
          mov EAX,DWORD PTR [EAX+1036]
          mov DWORD PTR [EAX],EDX
          lea EDI,DWORD PTR [EAX+4]
          mov EDX,DWORD PTR [ESI+1020]
          and EDI,4294967292
          mov DWORD PTR [EAX+1020],EDX
          sub EAX,EDI
          lea ECX,DWORD PTR [EAX+1024]
          sub ESI,EAX
          shr ECX,2
          rep movsd 
          jmp L_429916
L_429a63:
          mov DWORD PTR [ESP+4],OFFSET L_4594ca
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+28],EAX
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_4594a4
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [ESP+64]
          mov EDX,DWORD PTR [EAX+1036]
          mov DWORD PTR [ESP],EDX
          call _showSmcConfig
          mov DWORD PTR [ESP+4],OFFSET L_459371
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [ESP+28]
          jmp L_42999e
L_429abe:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_459478
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_42991e
L_429adb:
          mov EAX,4294967294
          jmp L_42999e
L_429ae5:
          mov DWORD PTR [ESP+4],OFFSET L_45942c
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,4294967294
          jmp L_42999e
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
#@C _raiseKernel
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
_checkBl:
          push EDI
          push ESI
          push EBX
          sub ESP,32
          mov EBX,DWORD PTR [ESP+48]
          mov EDI,DWORD PTR [ESP+56]
          lea EAX,DWORD PTR [EBX+12]
          mov DWORD PTR [ESP],EAX
          call _getBeU32
          cmp EAX,DWORD PTR [ESP+52]
          mov ESI,EAX
          ja L_429e30
          movzx EAX,BYTE PTR [EBX]
          mov EDX,EAX
          and EDX,67
          cmp DL,67
          jne L_429e60
          lea EDX,DWORD PTR [EDI-5]
          cmp EDX,16
          ja L_429e66
          jmp DWORD PTR [EDX*4+L_4595d8]
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_429b80:
          movzx EDX,BYTE PTR [EBX+1]
          cmp DL,68
          jne L_429ded
L_429b8d:
          mov DWORD PTR [EBX+16],0
          mov DWORD PTR [EBX+20],0
          mov DWORD PTR [EBX+24],0
          mov DWORD PTR [EBX+28],0
          cmp DWORD PTR [ESP+60],-1
          je L_429bc6
L_429bb0:
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EBX
          call _crc32
          cmp DWORD PTR [ESP+60],EAX
          jne L_429ca0
L_429bc6:
          xor EAX,EAX
L_429bc8:
          add ESP,32
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x90
L_429bd0:
          movzx EDX,BYTE PTR [EBX+1]
          cmp DL,69
          jne L_429ded
          mov DWORD PTR [EBX+16],0
          mov DWORD PTR [EBX+20],0
          mov DWORD PTR [EBX+24],0
          mov DWORD PTR [EBX+28],0
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EBX
          call _crc32
          lea EAX,DWORD PTR [EBX+4]
          mov DWORD PTR [ESP],EAX
          call _getBeU16
          lea EAX,DWORD PTR [EBX+2]
          mov DWORD PTR [ESP],EAX
          call _getBeU16
          mov DWORD PTR [ESP],EBX
          mov EDI,EAX
          call _getBeU16
          movzx EAX,DI
          shl EAX,8
          or EAX,536870912
          cmp EAX,DWORD PTR [L_479eac]
          jbe L_429c3d
          mov DWORD PTR [L_479eac],EAX
L_429c3d:
          cmp DWORD PTR [ESP+60],-1
          jne L_429bb0
          jmp L_429bc6
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_429c50:
          movzx EDX,BYTE PTR [EBX+1]
          cmp DL,66
          jne L_429ded
          lea EDI,DWORD PTR [EBX+20]
          lea ECX,DWORD PTR [EBX+16]
          xor EAX,EAX
          mov DWORD PTR [EBX+16],0
          mov DWORD PTR [EBX+60],0
          and EDI,4294967292
          sub ECX,EDI
          add ECX,48
          shr ECX,2
          rep stosd DWORD PTR ES:[EDI]
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EBX
          call _crc32
          cmp EAX,DWORD PTR [ESP+60]
          je L_429bc6
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_429ca0:
          mov ECX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_459510
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+12],ECX
          call _log_printf
          mov EAX,4294967294
          jmp L_429bc8
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_429cd0:
          movzx EDX,BYTE PTR [EBX+1]
          cmp DL,68
          jne L_429ded
L_429cdd:
          mov DWORD PTR [EBX+16],0
          mov DWORD PTR [EBX+20],0
          mov DWORD PTR [EBX+24],0
          mov DWORD PTR [EBX+28],0
          jmp L_429bb0
          .byte 0x66
          .byte 0x90
L_429d00:
          movzx EDX,BYTE PTR [EBX+1]
          cmp DL,69
          jne L_429ded
          mov DWORD PTR [EBX+16],0
          mov DWORD PTR [EBX+20],0
          mov DWORD PTR [EBX+24],0
          mov DWORD PTR [EBX+28],0
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EBX
          call _crc32
          cmp DWORD PTR [ESP+60],EAX
          jne L_429ca0
          lea EAX,DWORD PTR [EBX+4]
          mov DWORD PTR [ESP],EAX
          call _getBeU16
          lea EAX,DWORD PTR [EBX+2]
L_429d4d:
          mov DWORD PTR [ESP],EAX
          call _getBeU16
          mov DWORD PTR [ESP],EBX
          mov ESI,EAX
          call _getBeU16
          movzx EAX,SI
          shl EAX,8
          or EAX,536870912
          cmp EAX,DWORD PTR [L_479eac]
          jbe L_429bc6
          mov DWORD PTR [L_479eac],EAX
          jmp L_429bc6
L_429d80:
          movzx EDX,BYTE PTR [EBX+1]
          cmp DL,70
          jne L_429ded
          lea EDI,DWORD PTR [EBX+36]
          lea ECX,DWORD PTR [EBX+32]
          xor EAX,EAX
          mov DWORD PTR [EBX+32],0
          mov DWORD PTR [EBX+556],0
          and EDI,4294967292
          sub ECX,EDI
          add ECX,528
          shr ECX,2
          rep stosd DWORD PTR ES:[EDI]
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EBX
          call _crc32
          cmp DWORD PTR [ESP+60],EAX
          jne L_429ca0
          lea EAX,DWORD PTR [EBX+22]
          mov DWORD PTR [ESP],EAX
          call _getBeU16
          lea EAX,DWORD PTR [EBX+20]
          jmp L_429d4d
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_429de0:
          movzx EDX,BYTE PTR [EBX+1]
          cmp DL,71
          je L_429cdd
L_429ded:
          mov DWORD PTR [ESP+16],EDI
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+12],EDX
          mov DWORD PTR [ESP+4],OFFSET L_4595a0
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,32
          mov EAX,4294967295
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
L_429e20:
          movzx EDX,BYTE PTR [EBX+1]
          cmp DL,67
          je L_429b8d
          jmp L_429ded
          .byte 0x90
L_429e30:
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_459558
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+12],EAX
          call _log_printf
          add ESP,32
          mov EAX,4294967293
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_429e60:
          movzx EDX,BYTE PTR [EBX+1]
          jmp L_429ded
L_429e66:
          xor EAX,EAX
          jmp L_429ca0
          .byte 0x8d
          .byte 0x76
          .byte 0x0
_verifyBlSigs:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,60
          mov EAX,DWORD PTR [L_4c4f98]
          cmp EAX,1
          jbe L_42a340
          mov ESI,OFFSET L_4bc17c
          mov EDI,1
          mov DWORD PTR [ESP+44],1
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_429ea0:
          mov ECX,DWORD PTR [ESI+1028]
          cmp ECX,17
          ja L_429f20
          mov EDX,1
          shl EDX,CL
          test EDX,133152
          .byte 0x0f,0x85; .long L_429f40-.-4   # jne L_429f40
          test DH,64
          je L_429f82
          test EAX,EAX
          jle L_429efa
          xor EBX,EBX
          cmp DWORD PTR [L_4bc150+4],13
          mov EBP,OFFSET L_4bc580
          mov EDX,EBP
          jne L_429ef3
          jmp L_429efa
          .byte 0x90
L_429ee0:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],13
          je L_42a000
L_429ef3:
          add EBX,1
          cmp EBX,EAX
          jne L_429ee0
L_429efa:
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_459920
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [L_4c4f98]
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_429f20:
          add EDI,1
          add ESI,1068
          cmp EAX,EDI
          ja L_429ea0
L_429f31:
          mov EAX,DWORD PTR [ESP+44]
          add ESP,60
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_429f40:
          mov EAX,DWORD PTR [_pub1bl]
          test EAX,EAX
          je L_42a260
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESI+1036]
          mov DWORD PTR [ESP],EAX
          call _cbVerifySig
          test EAX,EAX
          mov DWORD PTR [ESP+8],ESI
          jne L_429fe0
          mov DWORD PTR [ESP+4],OFFSET L_45961c
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_4c4f98]
          jmp L_429f20
L_429f82:
          and DH,48
          je L_429f20
          test EAX,EAX
          jle L_429fba
          xor EBX,EBX
          cmp DWORD PTR [L_4bc150+4],11
          mov EDX,OFFSET L_4bc580
          jne L_429fb3
          jmp L_429fba
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_429fa0:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],11
          je L_42a150
L_429fb3:
          add EBX,1
          cmp EBX,EAX
          jne L_429fa0
L_429fba:
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_4597bc
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [L_4c4f98]
          jmp L_429f20
L_429fdc:
          mov DWORD PTR [ESP+8],ESI
L_429fe0:
          mov DWORD PTR [ESP+4],OFFSET L_459646
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [L_4c4f98]
          jmp L_429f20
          .byte 0x66
          .byte 0x90
L_42a000:
          imul EAX,EBX,1068
          mov EAX,DWORD PTR [EAX+L_4bc150+12]
          add EAX,588
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESI+1040]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESI+1036]
          mov DWORD PTR [ESP],EAX
          call _blCheckHash
          test EAX,EAX
          jne L_42a2c0
          mov EDX,DWORD PTR [L_47a148]
          test EDX,EDX
          je L_42a31e
          mov ECX,DWORD PTR [L_4c4f98]
          test ECX,ECX
          jle L_42a076
          cmp DWORD PTR [L_4bc150+4],11
          jne L_42a06f
          jmp L_42a076
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42a060:
          add EBP,1068
          cmp DWORD PTR [EBP-1068],11
          je L_42a078
L_42a06f:
          add EAX,1
          cmp EAX,ECX
          jne L_42a060
L_42a076:
          xor EAX,EAX
L_42a078:
          imul EAX,EAX,1068
          mov DWORD PTR [ESP+8],272
          mov DWORD PTR [ESP],EDX
          lea EBP,DWORD PTR [EAX+_xb]
          mov EAX,DWORD PTR [EAX+L_4bc150+12]
          add EAX,616
          mov DWORD PTR [ESP+4],EAX
          call _memcmp
          test EAX,EAX
          mov DWORD PTR [ESP+8],ESI
          jne L_42a282
          mov DWORD PTR [ESP+4],OFFSET L_4597e4
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EDX,DWORD PTR [L_47a148]
          imul EAX,EBX,1068
          mov DWORD PTR [ESP+24],EDX
          mov EDX,DWORD PTR [EBP+271036]
          mov ECX,DWORD PTR [EAX+L_4bc150+12]
          add EAX,OFFSET _xb
          add EDX,616
          mov DWORD PTR [ESP+20],EDX
          lea EDX,DWORD PTR [ECX+588]
          mov DWORD PTR [ESP+16],EDX
          mov EAX,DWORD PTR [EAX+271040]
          mov DWORD PTR [ESP+8],ECX
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESI+1040]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESI+1036]
          mov DWORD PTR [ESP],EAX
          call _blHashAndSign
          test EAX,EAX
          mov DWORD PTR [ESP+8],ESI
          jne L_42a2e2
          mov DWORD PTR [ESP+4],OFFSET L_459820
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_4c4f98]
          jmp L_429f20
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42a150:
          imul EAX,EBX,1068
          cmp ECX,12
          mov EAX,DWORD PTR [EAX+L_4bc150+12]
          lea EBP,DWORD PTR [EAX+904]
          je L_42a16d
          lea EBP,DWORD PTR [EAX+914]
L_42a16d:
          add EAX,616
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESI+1040]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESI+1036]
          mov DWORD PTR [ESP],EAX
          call _blVerifySig
          test EAX,EAX
          jne L_429fdc
          mov EAX,DWORD PTR [L_47a148]
          test EAX,EAX
          je L_42a34d
          imul EBX,EBX,1068
          mov DWORD PTR [ESP+8],272
          mov DWORD PTR [ESP],EAX
          mov ECX,DWORD PTR [EBX+L_4bc150+12]
          add EBX,OFFSET _xb
          lea EDX,DWORD PTR [ECX+616]
          mov DWORD PTR [ESP+4],EDX
          call _memcmp
          test EAX,EAX
          mov DWORD PTR [ESP+8],ESI
          jne L_42a2a0
          mov DWORD PTR [ESP+4],OFFSET L_459698
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_47a148]
          mov DWORD PTR [ESP+16],EBP
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [EBX+271036]
          add EAX,616
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESI+1040]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESI+1036]
          mov DWORD PTR [ESP],EAX
          call _blSign
          test EAX,EAX
          mov DWORD PTR [ESP+8],ESI
          jne L_42a300
          mov DWORD PTR [ESP+4],OFFSET L_4596cc
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_4c4f98]
          mov DWORD PTR [ESP+44],0
          jmp L_429f20
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42a260:
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_45965c
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [L_4c4f98]
          jmp L_429f20
L_42a282:
          mov DWORD PTR [ESP+4],OFFSET L_459888
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_4c4f98]
          jmp L_429f20
L_42a2a0:
          mov DWORD PTR [ESP+4],OFFSET L_45970c
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_4c4f98]
          jmp L_429f20
          .byte 0x66
          .byte 0x90
L_42a2c0:
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_459905
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [L_4c4f98]
          jmp L_429f20
L_42a2e2:
          mov DWORD PTR [ESP+4],OFFSET L_459858
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [L_4c4f98]
          jmp L_429f20
L_42a300:
          mov DWORD PTR [ESP+4],OFFSET L_4596f0
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [L_4c4f98]
          jmp L_429f20
L_42a31e:
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_4598e0
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_4c4f98]
          jmp L_429f20
L_42a340:
          mov DWORD PTR [ESP+44],1
          jmp L_429f31
L_42a34d:
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_45976c
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_4c4f98]
          jmp L_429f20
          .byte 0x90
_loadBlFiles:
          push EBP
          push EDI
          push ESI
          push EBX
          mov EBX,OFFSET L_4bc588
          sub ESP,60
          cmp DWORD PTR [L_4c4f98],1
          mov DWORD PTR [ESP+44],1
          jbe L_42a44b
L_42a391:
          lea EBP,DWORD PTR [EBX-1036]
          mov DWORD PTR [ESP+8],4
          mov DWORD PTR [ESP+4],OFFSET _bd_459955
          mov DWORD PTR [ESP],EBP
          call _strnicmp
          test EAX,EAX
          jne L_42a3ba
          mov EAX,DWORD PTR [EBX-12]
          test EAX,EAX
          je L_42a430
L_42a3ba:
          mov ESI,DWORD PTR [EBX-8]
          cmp ESI,27
          ja L_42a970
          jmp DWORD PTR [ESI*4+L_459bf4]
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_42a3d0:
          imul EDX,DWORD PTR [L_4c4f9c],1068
          mov EAX,EBP
          add EDX,OFFSET L_4bbd50
          call _loadBaseFile
          test EAX,EAX
          mov EDX,DWORD PTR [L_4c4f9c]
          jne L_42ab70
L_42a3f5:
          imul EDX,EDX,1068
          add EDX,OFFSET _xb
          mov EAX,DWORD PTR [EDX+271036]
          test EAX,EAX
          je L_42a430
          mov EDX,DWORD PTR [EDX+271040]
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+8],EDX
          call _extractSmcConfig
          mov EDI,EAX
L_42a423:
          test EDI,EDI
          jne L_42a8d9
          nop
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_42a430:
          add DWORD PTR [ESP+44],1
          add EBX,1068
          mov EAX,DWORD PTR [ESP+44]
          cmp DWORD PTR [L_4c4f98],EAX
          ja L_42a391
L_42a44b:
          add ESP,60
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_42a455:
          mov EAX,DWORD PTR [_g479ea8]
          cmp EAX,1
          je L_42a430
          cmp EAX,5
          ja L_42a430
          mov EDX,EBP
          mov EAX,EBP
          call _loadBaseFile
          test EAX,EAX
          je L_42a430
          mov DWORD PTR [ESP+4],OFFSET L_459a68
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP],EBP
          call _loadBinFile
          test EAX,EAX
          je L_42a430
          mov DWORD PTR [ESP+4],OFFSET L_459ab0
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP],EBP
          call _loadLocalFile
          mov EDI,EAX
          jmp L_42a423
L_42a4b4:
          mov EAX,DWORD PTR [_g479ea8]
          cmp EAX,2
          je L_42a4cc
          mov EDI,DWORD PTR [L_479eb4]
          test EDI,EDI
          je L_42aab0
L_42a4cc:
          mov EDX,EBP
          mov EAX,EBP
          call _loadBaseFile
          test EAX,EAX
          jne L_42a4df
          cmp DWORD PTR [EBX+4],96
          je L_42a50a
L_42a4df:
          mov DWORD PTR [ESP],96
          call _malloc
          test EAX,EAX
          mov DWORD PTR [EBX],EAX
          je L_42ab95
          mov DWORD PTR [EBX+4],96
          mov ESI,OFFSET L_44a700
          mov ECX,24
          mov EDI,EAX
          rep movsd 
L_42a50a:
          mov EAX,DWORD PTR [_g479ea8]
          sub EAX,4
          cmp EAX,1
          ja L_42a430
L_42a51b:
          mov EDX,EBP
          mov EAX,EBP
          call _loadBaseFile
          test EAX,EAX
          jne L_42a532
          cmp DWORD PTR [EBX+4],96
          je L_42a430
L_42a532:
          mov DWORD PTR [ESP],96
          call _malloc
          test EAX,EAX
          mov DWORD PTR [EBX],EAX
          je L_42aba6
          mov DWORD PTR [EBX+4],96
          mov ESI,OFFSET L_44a700
          mov ECX,24
          mov EDI,EAX
          rep movsd 
          jmp L_42a430
L_42a562:
          cmp DWORD PTR [_g479ea8],1
          je L_42a430
          mov DWORD PTR [ESP],EBP
          call _loadBinFile
          test EAX,EAX
          mov EDI,EAX
          jne L_42a8d9
          mov EAX,DWORD PTR [EBX+4]
          test AL,3
          je L_42abf7
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_459b54
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_42a8d4
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42a5b0:
          mov DWORD PTR [ESP],EBP
          call _loadBinFile
          test EAX,EAX
          je L_42a430
          mov DWORD PTR [ESP+16],3392
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+8],OFFSET L_47a54c
          mov DWORD PTR [ESP+4],OFFSET L_459a30
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP],3392
          call _malloc
          test EAX,EAX
          mov DWORD PTR [EBX],EAX
          je L_42aba6
          mov DWORD PTR [EBX+4],3392
          mov ECX,848
          mov EDI,EAX
          mov ESI,OFFSET L_44a960
          rep movsd 
          jmp L_42a430
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42a620:
          mov EAX,DWORD PTR [L_479eb8]
          test EAX,EAX
          je L_42a430
          mov DWORD PTR [ESP+28],1
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EBP
          call _loadInputFile
          test EAX,EAX
          mov EDI,EAX
          jne L_42a8d9
          mov EAX,DWORD PTR [EBX-12]
          mov DWORD PTR [ESP+8],6
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [EBX+4]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [EBX]
          mov DWORD PTR [ESP],EAX
          call _checkBl
          mov EDI,EAX
          jmp L_42a423
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42a6a0:
          mov DWORD PTR [ESP+28],1
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EBP
          call _loadInputFile
          test EAX,EAX
          mov EDI,EAX
          je L_42aa00
          cmp ESI,9
          je L_42abb0
          cmp ESI,10
          jne L_42a8d9
          lea EAX,DWORD PTR [EBX+4]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call _suGetCG
          test EAX,EAX
          je L_42a8d9
          mov EAX,DWORD PTR [EBX-12]
          mov DWORD PTR [ESP+8],10
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [EBX+4]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [EBX]
          jmp L_42abe8
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_42a730:
          imul EDX,DWORD PTR [L_4c4f9c],1068
          mov EAX,EBP
          add EDX,OFFSET L_4bbd50
          call _loadBaseFile
          test EAX,EAX
          jne L_42aac1
L_42a74f:
          mov EAX,DWORD PTR [EBX]
          test EAX,EAX
          je L_42a75d
          mov DWORD PTR [ESP],EAX
          call _free
L_42a75d:
          imul EAX,DWORD PTR [L_4c4f9c],1068
          mov EDX,DWORD PTR [EAX+L_4bc150+12]
          mov DWORD PTR [EBX],EDX
          mov EDX,DWORD PTR [EAX+L_4bc150+16]
          mov DWORD PTR [EBX+4],EDX
          mov DWORD PTR [EAX+L_4bc150+12],0
          mov DWORD PTR [EAX+L_4bc150+16],0
          jmp L_42a430
L_42a791:
          imul EDX,DWORD PTR [L_4c4f9c],1068
          mov EAX,EBP
          add EDX,OFFSET L_4bbd50
          call _loadBaseFile
          test EAX,EAX
          je L_42a74f
          imul EDX,DWORD PTR [L_4c4f9c],1068
          mov EAX,OFFSET L_459aec
          add EDX,OFFSET L_4bbd50
          call _loadBaseFile
          test EAX,EAX
          je L_42a74f
          imul EDX,DWORD PTR [L_4c4f9c],1068
          mov EAX,OFFSET L_459af9
          add EDX,OFFSET L_4bbd50
          call _loadBaseFile
          test EAX,EAX
          mov EDI,EAX
          je L_42a74f
          mov ESI,DWORD PTR [L_47a0e8+4]
          test ESI,ESI
          je L_42a8d9
          mov DWORD PTR [ESP+16],EBP
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+8],OFFSET L_47ad4c
          mov DWORD PTR [ESP+4],OFFSET L_459b04
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [EBX]
          test EAX,EAX
          je L_42a82e
          mov DWORD PTR [ESP],EAX
          call _free
L_42a82e:
          mov EAX,DWORD PTR [L_47a0e8+4]
          mov DWORD PTR [EBX],EAX
          mov EAX,DWORD PTR [L_47a0ec+4]
          mov DWORD PTR [EBX+4],EAX
          mov DWORD PTR [L_47a0e8+4],0
          mov DWORD PTR [L_47a0ec+4],0
          jmp L_42a430
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_42a860:
          imul EDX,DWORD PTR [L_4c4f9c],1068
          mov EAX,EBP
          add EDX,OFFSET L_4bbd50
          call _loadBaseFile
          test EAX,EAX
          mov EDI,EAX
          jne L_42a991
          mov EAX,DWORD PTR [EBX]
          test EAX,EAX
          je L_42a88f
          mov DWORD PTR [ESP],EAX
          call _free
L_42a88f:
          imul EAX,DWORD PTR [L_4c4f9c],1068
          mov EDX,DWORD PTR [EAX+L_4bc150+12]
          mov DWORD PTR [EBX],EDX
          mov EDX,DWORD PTR [EAX+L_4bc150+16]
          mov DWORD PTR [EBX+4],EDX
          mov DWORD PTR [EAX+L_4bc150+12],0
          mov DWORD PTR [EAX+L_4bc150+16],0
          mov EAX,DWORD PTR [EBX+4]
L_42a8c1:
          mov DWORD PTR [ESP],EAX
          call _smcSetLoad
          test EAX,EAX
          mov DWORD PTR [EBX-4],EAX
          jne L_42a430
L_42a8d4:
          mov EDI,4294967295
L_42a8d9:
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_459bcc
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,60
          mov EAX,4294967295
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_42a902:
          mov DWORD PTR [ESP],EBP
          call _loadBinFile
          test EAX,EAX
          je L_42a430
          mov DWORD PTR [ESP+16],512
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+8],OFFSET L_47a54c
          mov DWORD PTR [ESP+4],OFFSET L_4599f4
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP],512
          call _malloc
          test EAX,EAX
          mov DWORD PTR [EBX],EAX
          je L_42aba6
          mov DWORD PTR [EBX+4],512
          mov ECX,128
          mov EDI,EAX
          mov ESI,OFFSET L_44a760
          rep movsd 
          jmp L_42a430
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42a970:
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_459ba8
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_42a430
L_42a991:
          mov EAX,DWORD PTR [L_47a0e0+4]
          test EAX,EAX
          je L_42a8d9
          mov DWORD PTR [ESP+16],EBP
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+8],OFFSET L_47ad4c
          mov DWORD PTR [ESP+4],OFFSET L_459b04
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [EBX]
          test EAX,EAX
          je L_42a9d0
          mov DWORD PTR [ESP],EAX
          call _free
L_42a9d0:
          mov EAX,DWORD PTR [L_47a0e0+4]
          mov DWORD PTR [EBX],EAX
          mov EAX,DWORD PTR [L_47a0e4+4]
          mov DWORD PTR [EBX+4],EAX
          mov DWORD PTR [L_47a0e0+4],0
          mov DWORD PTR [L_47a0e4+4],0
          jmp L_42a8c1
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42aa00:
          cmp ESI,9
          je L_42abc7
          mov EAX,DWORD PTR [EBX-12]
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [EBX+4]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [EBX]
          mov DWORD PTR [ESP],EAX
          call _checkBl
          test EAX,EAX
          mov EDI,EAX
          jne L_42a8d9
          cmp ESI,5
          je L_42aa3d
          cmp ESI,17
          jne L_42ad0d
L_42aa3d:
          mov EAX,DWORD PTR [_pub1bl]
          test EAX,EAX
          je L_42ada0
L_42aa4a:
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [EBX]
          mov DWORD PTR [ESP],EAX
          call _cbVerifySig
          test EAX,EAX
          mov DWORD PTR [ESP+8],EBP
          je L_42acb5
          mov DWORD PTR [ESP+4],OFFSET L_4599d0
          mov DWORD PTR [ESP],1
          call _log_printf
L_42aa78:
          cmp DWORD PTR [_g479ea8],5
          jbe L_42a430
          cmp ESI,14
          jne L_42a430
L_42aa8e:
          mov EAX,DWORD PTR [EBX]
          add EAX,2
          mov DWORD PTR [ESP],EAX
          call _getBeU16
          movzx EAX,AX
          mov DWORD PTR [ESP],EAX
          call _setFlashBuild
          jmp L_42a430
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_42aab0:
          sub EAX,4
          cmp EAX,1
          ja L_42a430
          jmp L_42a51b
L_42aac1:
          imul EDX,DWORD PTR [L_4c4f9c],1068
          mov EAX,OFFSET L_459b32
          add EDX,OFFSET L_4bbd50
          call _loadBaseFile
          test EAX,EAX
          je L_42a74f
          imul EDX,DWORD PTR [L_4c4f9c],1068
          mov EAX,OFFSET L_459b43
          add EDX,OFFSET L_4bbd50
          call _loadBaseFile
          test EAX,EAX
          mov EDI,EAX
          je L_42a74f
          mov ECX,DWORD PTR [L_47a0f4]
          test ECX,ECX
          je L_42a8d9
          mov DWORD PTR [ESP+16],EBP
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+8],OFFSET L_47ad4c
          mov DWORD PTR [ESP+4],OFFSET L_459b04
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [EBX]
          test EAX,EAX
          je L_42ab47
          mov DWORD PTR [ESP],EAX
          call _free
L_42ab47:
          mov EAX,DWORD PTR [L_47a0f4]
          mov DWORD PTR [EBX],EAX
          mov EAX,DWORD PTR [L_47a0f8]
          mov DWORD PTR [EBX+4],EAX
          mov DWORD PTR [L_47a0f4],0
          mov DWORD PTR [L_47a0f8],0
          jmp L_42a430
          .byte 0x90
L_42ab70:
          imul EDX,EDX,1068
          mov EAX,OFFSET L_459b8c
          add EDX,OFFSET L_4bbd50
          call _loadBaseFile
          test EAX,EAX
          jne L_42ac04
L_42ab8a:
          mov EDX,DWORD PTR [L_4c4f9c]
          jmp L_42a3f5
L_42ab95:
          mov EAX,DWORD PTR [_g479ea8]
          sub EAX,4
          cmp EAX,1
          jbe L_42a51b
L_42aba6:
          mov EDI,1
          jmp L_42a8d9
L_42abb0:
          lea EAX,DWORD PTR [EBX+4]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call _suGetCF
          test EAX,EAX
          je L_42a8d9
L_42abc7:
          mov EAX,DWORD PTR [EBX]
          cmp BYTE PTR [EAX],83
          je L_42ad40
L_42abd2:
          mov EDX,DWORD PTR [EBX-12]
          mov DWORD PTR [ESP+8],9
          mov DWORD PTR [ESP+12],EDX
          mov EDX,DWORD PTR [EBX+4]
          mov DWORD PTR [ESP+4],EDX
L_42abe8:
          mov DWORD PTR [ESP],EAX
          call _checkBl
          mov EDI,EAX
          jmp L_42a423
L_42abf7:
          mov DWORD PTR [ESP],EBP
          call _appendAddonPatches
          jmp L_42a430
L_42ac04:
          imul EDX,DWORD PTR [L_4c4f9c],1068
          mov EAX,OFFSET L_459b97
          add EDX,OFFSET L_4bbd50
          call _loadBaseFile
          test EAX,EAX
          mov EDI,EAX
          je L_42ab8a
          mov EDX,DWORD PTR [L_47a0fc]
          test EDX,EDX
          je L_42a8d9
          mov DWORD PTR [ESP+16],EBP
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+8],OFFSET L_47ad4c
          mov DWORD PTR [ESP+4],OFFSET L_459b04
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EDX,DWORD PTR [L_4c4f9c]
          imul EAX,EDX,1068
          mov EAX,DWORD PTR [EAX+L_4bc150+12]
          test EAX,EAX
          je L_42ac7e
          mov DWORD PTR [ESP],EAX
          call _free
          mov EDX,DWORD PTR [L_4c4f9c]
L_42ac7e:
          mov ECX,DWORD PTR [L_47a0fc]
          mov DWORD PTR [L_47a0fc],0
          imul EAX,EDX,1068
          mov DWORD PTR [EAX+L_4bc150+12],ECX
          mov ECX,DWORD PTR [L_47a100]
          mov DWORD PTR [L_47a100],0
          mov DWORD PTR [EAX+L_4bc150+16],ECX
          jmp L_42a3f5
L_42acb5:
          mov DWORD PTR [ESP+4],OFFSET L_459998
          mov DWORD PTR [ESP],0
          call _log_printf
          cmp DWORD PTR [_g479ea8],5
          jbe L_42a8d4
          cmp ESI,14
          mov EDI,4294967295
          jne L_42a8d9
          imul EAX,DWORD PTR [ESP+44],1068
          mov EAX,DWORD PTR [EAX+L_4bc150+12]
          add EAX,2
          mov DWORD PTR [ESP],EAX
          call _getBeU16
          movzx EAX,AX
          mov DWORD PTR [ESP],EAX
          call _setFlashBuild
          jmp L_42a8d9
L_42ad0d:
          cmp ESI,11
          jne L_42aa78
          mov EAX,DWORD PTR [_pub1bl]
          test EAX,EAX
          jne L_42aa4a
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_45995c
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_42a430
L_42ad40:
          cmp BYTE PTR [EAX+1],69
          jne L_42abd2
          mov DWORD PTR [EBX-8],14
          mov BYTE PTR [L_479f15],0
          mov DWORD PTR [L_479ebc],1
          mov EDX,DWORD PTR [EBX-12]
          mov DWORD PTR [ESP+8],14
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+12],EDX
          mov EDX,DWORD PTR [EBX+4]
          mov DWORD PTR [ESP+4],EDX
          call _checkBl
          test EAX,EAX
          mov EDI,EAX
          jne L_42a8d9
          cmp DWORD PTR [_g479ea8],5
          jbe L_42a430
          jmp L_42aa8e
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_42ada0:
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_45995c
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_42aa78
          .byte 0x8d
          .byte 0x76
          .byte 0x0
_loadConsoleBlFiles:
          cmp DWORD PTR [L_4c4f98],1
          jbe L_42b2ac
          push EBP
          push EDI
          mov EBP,1
          push ESI
          push EBX
          mov EBX,OFFSET L_4bc588
          sub ESP,60
          .byte 0x66   # nop
          nop
L_42ade0:
          lea ESI,DWORD PTR [EBX-1036]
          mov DWORD PTR [ESP+8],4
          mov DWORD PTR [ESP+4],OFFSET _bd_459955
          mov DWORD PTR [ESP],ESI
          call _strnicmp
          test EAX,EAX
          jne L_42ae0d
          mov EAX,DWORD PTR [EBX-12]
          test EAX,EAX
          je L_42af50
L_42ae0d:
          mov EDI,DWORD PTR [EBX-8]
          cmp EDI,27
          ja L_42b1a0
          jmp DWORD PTR [EDI*4+L_459dcc]
L_42ae20:
          mov EDX,DWORD PTR [L_47a0fc]
          test EDX,EDX
          je L_42b240
          mov DWORD PTR [ESP+4],OFFSET L_459d14
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [L_4c4f9c]
          imul EDX,EAX,1068
          mov EDX,DWORD PTR [EDX+L_4bc150+12]
          test EDX,EDX
          je L_42ae64
          mov DWORD PTR [ESP],EDX
          call _free
          mov EAX,DWORD PTR [L_4c4f9c]
L_42ae64:
          mov EDX,DWORD PTR [L_47a0fc]
          mov ECX,DWORD PTR [L_47a100]
          imul EAX,EAX,1068
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [L_47a0fc],0
          mov DWORD PTR [L_47a100],0
          mov DWORD PTR [ESP+4],EDX
          mov DWORD PTR [ESP+8],ECX
          mov DWORD PTR [EAX+L_4bc150+12],EDX
          mov DWORD PTR [EAX+L_4bc150+16],ECX
          call _extractSmcConfig
          mov EDX,EAX
L_42aea8:
          test EDX,EDX
          je L_42af50
L_42aeb0:
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+12],EDX
          mov DWORD PTR [ESP+4],OFFSET L_459bcc
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,60
          mov EAX,4294967295
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
L_42aee0:
          mov EAX,DWORD PTR [_g479ea8]
          cmp EAX,1
          je L_42af50
          cmp EAX,5
          ja L_42af50
          mov EDX,ESI
          mov EAX,ESI
          call _loadBaseFile
          test EAX,EAX
          je L_42af50
          mov DWORD PTR [ESP+4],OFFSET L_459a68
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP],ESI
          call _loadBinFile
          test EAX,EAX
          je L_42af50
          mov DWORD PTR [ESP+4],OFFSET L_459ab0
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP],ESI
          call _loadLocalFile
          mov EDX,EAX
          jmp L_42aea8
          .byte 0x90
L_42af40:
          mov EAX,DWORD PTR [L_479eb4]
          test EAX,EAX
          jne L_42b1e0
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
L_42af50:
          add EBP,1
          add EBX,1068
          cmp DWORD PTR [L_4c4f98],EBP
          ja L_42ade0
          add ESP,60
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x90
L_42af70:
          mov DWORD PTR [ESP],ESI
          call _loadBinFile
          test EAX,EAX
          mov EDX,EAX
          jne L_42aeb0
          mov EAX,DWORD PTR [EBX+4]
          test AL,3
          je L_42b230
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_459b54
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EDX,4294967295
          jmp L_42aeb0
          .byte 0x90
L_42afb0:
          mov DWORD PTR [ESP+28],1
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],ESI
          call _loadInputFile
          test EAX,EAX
          mov EDX,EAX
          je L_42b020
          cmp EDI,9
          je L_42b27e
          cmp EDI,10
          jne L_42aeb0
          mov DWORD PTR [ESP+44],EAX
          lea EAX,DWORD PTR [EBX+4]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call _suGetCG
          test EAX,EAX
          je L_42b299
          nop
L_42b020:
          mov EAX,DWORD PTR [EBX-12]
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [EBX+4]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [EBX]
          mov DWORD PTR [ESP],EAX
          call _checkBl
          mov EDX,EAX
          jmp L_42aea8
L_42b043:
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+8],OFFSET L_47ad4c
          mov DWORD PTR [ESP+4],OFFSET L_459c64
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_42af50
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42b070:
          mov ECX,DWORD PTR [L_47a0f4]
          test ECX,ECX
          je L_42b1c1
          mov DWORD PTR [ESP+4],OFFSET L_459cec
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [EBX]
          test EAX,EAX
          je L_42b0a0
          mov DWORD PTR [ESP],EAX
          call _free
L_42b0a0:
          mov EAX,DWORD PTR [L_47a0f4]
          mov DWORD PTR [EBX],EAX
          mov EAX,DWORD PTR [L_47a0f8]
          mov DWORD PTR [EBX+4],EAX
          mov DWORD PTR [L_47a0f4],0
          mov DWORD PTR [L_47a0f8],0
          jmp L_42af50
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42b0d0:
          mov EDI,DWORD PTR [L_47a0e8+4]
          test EDI,EDI
          je L_42b1c1
          mov DWORD PTR [ESP+4],OFFSET L_459c98
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [EBX]
          test EAX,EAX
          je L_42b100
          mov DWORD PTR [ESP],EAX
          call _free
L_42b100:
          mov EAX,DWORD PTR [L_47a0e8+4]
          mov DWORD PTR [EBX],EAX
          mov EAX,DWORD PTR [L_47a0ec+4]
          mov DWORD PTR [EBX+4],EAX
          mov DWORD PTR [L_47a0e8+4],0
          mov DWORD PTR [L_47a0ec+4],0
          jmp L_42af50
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42b130:
          mov EAX,DWORD PTR [L_47a0e0+4]
          test EAX,EAX
          je L_42b260
          mov DWORD PTR [ESP+4],OFFSET L_459d78
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [EBX]
          test EAX,EAX
          je L_42b15f
          mov DWORD PTR [ESP],EAX
          call _free
L_42b15f:
          mov EAX,DWORD PTR [L_47a0e0+4]
          mov DWORD PTR [EBX],EAX
          mov EAX,DWORD PTR [L_47a0e4+4]
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [EBX+4],EAX
          mov DWORD PTR [L_47a0e0+4],0
          mov DWORD PTR [L_47a0e4+4],0
          call _smcSetLoad
          test EAX,EAX
          mov DWORD PTR [EBX-4],EAX
          jne L_42af50
          mov EDX,4294967295
          jmp L_42aeb0
          .byte 0x90
L_42b1a0:
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET L_459ba8
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_42af50
L_42b1c1:
          mov DWORD PTR [ESP+4],OFFSET L_459cbc
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EDX,4294967295
          jmp L_42aeb0
          .byte 0x90
L_42b1e0:
          mov EDX,ESI
          mov EAX,ESI
          call _loadBaseFile
          test EAX,EAX
          jne L_42b1f7
          cmp DWORD PTR [EBX+4],96
          je L_42af50
L_42b1f7:
          mov DWORD PTR [ESP],96
          call _malloc
          test EAX,EAX
          mov DWORD PTR [EBX],EAX
          je L_42b2a2
          mov DWORD PTR [EBX+4],96
          mov ECX,24
          mov EDI,EAX
          mov ESI,OFFSET L_44a700
          rep movsd 
          jmp L_42af50
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_42b230:
          mov DWORD PTR [ESP],ESI
          call _appendAddonPatches
          jmp L_42af50
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_42b240:
          mov DWORD PTR [ESP+4],OFFSET L_459d3c
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EDX,4294967295
          jmp L_42aeb0
          .byte 0x66
          .byte 0x90
L_42b260:
          mov DWORD PTR [ESP+4],OFFSET L_459d98
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EDX,4294967295
          jmp L_42aeb0
L_42b27e:
          mov DWORD PTR [ESP+44],EAX
          lea EAX,DWORD PTR [EBX+4]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call _suGetCF
          test EAX,EAX
          jne L_42b020
L_42b299:
          mov EDX,DWORD PTR [ESP+44]
          jmp L_42aeb0
L_42b2a2:
          mov EDX,1
          jmp L_42aeb0
L_42b2ac:
          xor EAX,EAX
          ret 
          .byte 0x90
#@C _patchHeaderOpts
          .byte 0x90
#@C _blmodMissing
          .byte 0x8d
          .byte 0x76
          .byte 0x0
#@C _rotSumSha
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
#@C _countBits
          .byte 0x8d
          .byte 0x76
          .byte 0x0
_patchBlsResign:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,92
          mov EAX,DWORD PTR [L_4c4f98]
          test EAX,EAX
          jle L_42babd
          mov ECX,DWORD PTR [L_4bc150+4]
          xor EBP,EBP
          mov EDX,OFFSET L_4bc580
          cmp ECX,11
          jne L_42b69f
          jmp L_42badf
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_42b690:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],11
          je L_42b6a8
L_42b69f:
          add EBP,1
          cmp EAX,EBP
          jne L_42b690
          xor EBP,EBP
L_42b6a8:
          cmp ECX,7
          je L_42bad0
L_42b6b1:
          mov EDX,OFFSET L_4bc580
          xor EDI,EDI
          jmp L_42b6d3
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42b6c0:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],7
          je L_42b9eb
L_42b6d3:
          add EDI,1
          cmp EAX,EDI
          jne L_42b6c0
          mov DWORD PTR [ESP+76],270000
          xor EDI,EDI
L_42b6e4:
          cmp ECX,23
          je L_42b708
L_42b6e9:
          mov EDX,OFFSET L_4bc580
          xor ESI,ESI
          jmp L_42b701
L_42b6f2:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],23
          je L_42b70a
L_42b701:
          add ESI,1
          cmp EAX,ESI
          jne L_42b6f2
L_42b708:
          xor ESI,ESI
L_42b70a:
          imul EAX,ESI,1068
          mov DWORD PTR [ESP+4],OFFSET L_459eea
          mov DWORD PTR [ESP],1
          mov EBX,DWORD PTR [EAX+L_4bc150+12]
          add EAX,OFFSET _xb
          mov DWORD PTR [ESP+52],EAX
          mov DWORD PTR [ESP+44],EBX
          xor EBX,EBX
          call _log_printf
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+48],0
          mov DWORD PTR [ESP+68],ESI
          mov DWORD PTR [ESP+56],EAX
          imul EAX,EDI,1068
          mov DWORD PTR [ESP+64],EAX
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_42b760:
          mov EAX,DWORD PTR [ESP+56]
          cmp EBX,DWORD PTR [EAX+271040]
          jae L_42b7bd
          mov ESI,DWORD PTR [ESP+48]
          cmp ESI,2
          jne L_42b900
          mov ESI,DWORD PTR [ESP+68]
          xor EAX,EAX
          mov DWORD PTR [ESP+44],EBX
          imul ECX,ESI,1068
          add ECX,OFFSET _xb
          nop
L_42b790:
          mov EDX,DWORD PTR [ECX+271036]
          mov EBX,DWORD PTR [ESP+44]
          lea ESI,DWORD PTR [EDX+EBX*1]
          movzx ESI,BYTE PTR [ESI+EAX*1]
          mov EBX,ESI
          mov BYTE PTR [EDX+EAX*1],BL
          mov EDX,DWORD PTR [ECX+271040]
          add EAX,1
          sub EDX,DWORD PTR [ESP+44]
          cmp EDX,EAX
          ja L_42b790
          mov DWORD PTR [ECX+271040],EDX
L_42b7bd:
          mov DWORD PTR [ESP+4],OFFSET L_459efa
          mov DWORD PTR [ESP],1
          call _log_printf
          test EBP,EBP
          je L_42b9c0
          imul ESI,EBP,1068
          mov DWORD PTR [ESP+4],OFFSET L_459f04
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [ESI+L_4bc150+12]
          add ESI,OFFSET _xb
          imul EBX,EDI,1068
          lea EDX,DWORD PTR [EAX+914]
          add EAX,616
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [EBX+L_4bc150+16]
          mov DWORD PTR [ESP+12],EDX
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [EBX+L_4bc150+12]
          add EBX,OFFSET _xb
          mov DWORD PTR [ESP],EAX
          call _blVerifySig
          test EAX,EAX
          jne L_42ba63
          mov EDX,DWORD PTR [L_47a148]
          test EDX,EDX
          je L_42bae6
          mov DWORD PTR [ESP+8],272
          mov EAX,DWORD PTR [ESI+271036]
          mov DWORD PTR [ESP],EDX
          add EAX,616
          mov DWORD PTR [ESP+4],EAX
          call _memcmp
          test EAX,EAX
          jne L_42ba36
          mov EDI,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP+4],OFFSET L_459698
          mov DWORD PTR [ESP],0
          add EDI,OFFSET _xb
          mov DWORD PTR [ESP+8],EDI
          call _log_printf
          mov EAX,DWORD PTR [ESI+271036]
          lea EDX,DWORD PTR [EAX+914]
          add EAX,616
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+16],EDX
          mov EDX,DWORD PTR [L_47a148]
          mov DWORD PTR [ESP+12],EDX
          mov EAX,DWORD PTR [EBX+271040]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [EBX+271036]
          mov DWORD PTR [ESP],EAX
          call _blSign
          test EAX,EAX
          mov DWORD PTR [ESP+8],EDI
          jne L_42baa7
          mov DWORD PTR [ESP+4],OFFSET L_4596cc
          mov DWORD PTR [ESP],0
          xor EBP,EBP
          call _log_printf
          jmp L_42b9e1
L_42b8f7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_42b900:
          mov EAX,DWORD PTR [ESP+44]
          add EAX,EBX
          mov DWORD PTR [ESP],EAX
          call _getBeU32
          mov ECX,EAX
          lea EAX,DWORD PTR [EBX+4]
          cmp ECX,-1
          mov DWORD PTR [ESP+52],ECX
          je L_42b9b0
          add EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EAX
          call _getBeU32
          lea EDX,DWORD PTR [EAX*4]
          lea EAX,DWORD PTR [EBX+8]
          test ESI,ESI
          mov ECX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+60],EAX
          je L_42b99d
          mov EAX,DWORD PTR [ESP+64]
          lea ESI,DWORD PTR [ECX+EDX*1]
          add EAX,OFFSET _xb
          cmp ESI,DWORD PTR [EAX+271040]
          ja L_42ba00
L_42b95a:
          test EDX,EDX
          je L_42b99d
          sub EBX,ECX
          mov EAX,ECX
          add EBX,DWORD PTR [ESP+44]
          mov ECX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+52],EDX
          mov DWORD PTR [ESP+72],EDI
          add ECX,OFFSET _xb
          nop
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_42b980:
          movzx EDX,BYTE PTR [EBX+EAX*1+8]
          mov EDI,DWORD PTR [ECX+271036]
          mov BYTE PTR [EDI+EAX*1],DL
          add EAX,1
          cmp ESI,EAX
          jne L_42b980
          mov EDX,DWORD PTR [ESP+52]
          mov EDI,DWORD PTR [ESP+72]
L_42b99d:
          mov EBX,DWORD PTR [ESP+60]
          add EBX,EDX
          jmp L_42b760
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42b9b0:
          add DWORD PTR [ESP+48],1
          mov EBX,EAX
          jmp L_42b760
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_42b9c0:
          mov EAX,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP+4],OFFSET L_4597bc
          mov DWORD PTR [ESP],1
          add EAX,OFFSET _xb
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
L_42b9e1:
          add ESP,92
          mov EAX,EBP
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_42b9eb:
          imul EDX,EDI,1068
          lea EBX,DWORD PTR [EDX+270000]
          mov DWORD PTR [ESP+76],EBX
          jmp L_42b6e4
L_42ba00:
          mov DWORD PTR [ESP+52],ECX
          lea ECX,DWORD PTR [ESI+15]
          mov DWORD PTR [ESP+72],EDX
          and ECX,4294967280
          mov DWORD PTR [ESP],ECX
          mov DWORD PTR [EAX+271040],ECX
          mov EAX,DWORD PTR [EAX+271036]
          add EAX,12
          mov DWORD PTR [ESP+4],EAX
          call _setBeU32
          mov EDX,DWORD PTR [ESP+72]
          mov ECX,DWORD PTR [ESP+52]
          jmp L_42b95a
L_42ba36:
          mov EAX,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP+4],OFFSET L_45970c
          xor EBP,EBP
          mov DWORD PTR [ESP],0
          add EAX,OFFSET _xb
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          add ESP,92
          mov EAX,EBP
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_42ba63:
          mov EAX,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP+4],OFFSET L_459646
          mov DWORD PTR [ESP],1
          add EAX,OFFSET _xb
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
L_42ba84:
          mov DWORD PTR [ESP+4],OFFSET L_459efa
          mov DWORD PTR [ESP],1
          mov EBP,1
          call _log_printf
          add ESP,92
          mov EAX,EBP
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_42baa7:
          mov DWORD PTR [ESP+4],OFFSET L_4596f0
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_42ba84
L_42babd:
          mov DWORD PTR [ESP+76],270000
          xor EBP,EBP
          xor EDI,EDI
          xor ESI,ESI
          jmp L_42b70a
L_42bad0:
          mov DWORD PTR [ESP+76],270000
          xor EDI,EDI
          jmp L_42b6e9
L_42badf:
          xor EBP,EBP
          jmp L_42b6b1
L_42bae6:
          mov EAX,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP+4],OFFSET L_45976c
          xor EBP,EBP
          mov DWORD PTR [ESP],0
          add EAX,OFFSET _xb
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          jmp L_42b9e1
          .byte 0x66
          .byte 0x90
_patchBlsBlmod:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,76
          mov EAX,DWORD PTR [ESP+96]
          mov DWORD PTR [ESP+56],EAX
          mov EAX,DWORD PTR [ESP+100]
          mov DWORD PTR [ESP+60],EAX
          mov EAX,DWORD PTR [L_4c4f98]
          test EAX,EAX
          jle L_42bf50
          mov ECX,DWORD PTR [L_4bc150+4]
          xor EDI,EDI
          mov EDX,OFFSET L_4bc580
          cmp ECX,7
          jne L_42bb5f
          jmp L_42bf49
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_42bb50:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],7
          je L_42bb68
L_42bb5f:
          add EDI,1
          cmp EDI,EAX
          jne L_42bb50
          xor EDI,EDI
L_42bb68:
          cmp ECX,6
          je L_42bf5b
L_42bb71:
          mov EDX,OFFSET L_4bc580
          xor EBP,EBP
          jmp L_42bb8f
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42bb80:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],6
          je L_42bb98
L_42bb8f:
          add EBP,1
          cmp EBP,EAX
          jne L_42bb80
          xor EBP,EBP
L_42bb98:
          cmp ECX,23
          je L_42bbc6
L_42bb9d:
          mov EDX,OFFSET L_4bc580
          xor ESI,ESI
          jmp L_42bbbf
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_42bbb0:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],23
          je L_42bbc8
L_42bbbf:
          add ESI,1
          cmp ESI,EAX
          jne L_42bbb0
L_42bbc6:
          xor ESI,ESI
L_42bbc8:
          imul EAX,ESI,1068
          mov DWORD PTR [ESP+4],OFFSET L_459eea
          mov DWORD PTR [ESP],1
          mov EBX,DWORD PTR [EAX+L_4bc150+12]
          add EAX,OFFSET _xb
          mov DWORD PTR [ESP+32],EAX
          mov DWORD PTR [ESP+24],EBX
          xor EBX,EBX
          call _log_printf
          imul EAX,EDI,1068
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+40],EDI
          mov DWORD PTR [ESP+48],ESI
          mov DWORD PTR [ESP+44],EAX
L_42bc11:
          mov EAX,DWORD PTR [ESP+32]
          cmp EBX,DWORD PTR [EAX+271040]
          jae L_42be4f
L_42bc21:
          mov ESI,DWORD PTR [ESP+28]
          cmp ESI,2
          jne L_42bda4
          mov ESI,DWORD PTR [ESP+48]
          mov EDI,DWORD PTR [ESP+40]
          xor EAX,EAX
          mov DWORD PTR [ESP+24],EBX
          imul ECX,ESI,1068
          add ECX,OFFSET _xb
          nop
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_42bc50:
          mov EDX,DWORD PTR [ECX+271036]
          mov EBX,DWORD PTR [ESP+24]
          lea ESI,DWORD PTR [EDX+EBX*1]
          movzx ESI,BYTE PTR [ESI+EAX*1]
          mov EBX,ESI
          mov BYTE PTR [EDX+EAX*1],BL
          mov EDX,DWORD PTR [ECX+271040]
          add EAX,1
          sub EDX,DWORD PTR [ESP+24]
          cmp EDX,EAX
          ja L_42bc50
          mov DWORD PTR [ECX+271040],EDX
L_42bc7d:
          mov ECX,DWORD PTR [ESP+56]
          test ECX,ECX
          je L_42bd88
          mov ESI,DWORD PTR [ESP+60]
          test ESI,ESI
          je L_42bd88
          mov DWORD PTR [ESP+4],OFFSET L_459efa
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EDX,DWORD PTR [L_479eb8]
          test EDX,EDX
          cmove EBP,EDI
          cmp DWORD PTR [L_479eb8],1
          sbb EDI,EDI
          imul EAX,EBP,1068
          and EDI,16384
          add EDI,49152
          mov EAX,DWORD PTR [EAX+L_4bc150+12]
          add EAX,12
          mov DWORD PTR [ESP],EAX
          call _getBeU32
          mov EBX,EAX
          lea EAX,DWORD PTR [EBX+ESI*1+15]
          and EAX,4294967280
          cmp EDI,EAX
          jb L_42bf16
L_42bcf1:
          mov EAX,DWORD PTR [L_479eb8]
          mov EDX,OFFSET L_459f25
          mov DWORD PTR [ESP+4],OFFSET L_459f7c
          mov DWORD PTR [ESP],1
          test EAX,EAX
          mov EAX,OFFSET L_459f29
          cmovne EAX,EDX
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+60]
          imul EDI,EBP,1068
          mov DWORD PTR [ESP+8],EAX
          add EDI,OFFSET _xb
          call _log_printf
          mov EAX,DWORD PTR [EDI+271036]
          mov ECX,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP+8],ESI
          add EAX,EBX
          mov DWORD PTR [ESP+4],ECX
          mov DWORD PTR [ESP],EAX
          call _memcpy
          lea EAX,DWORD PTR [EBX+ESI*1+15]
          mov EDX,DWORD PTR [L_479ed8]
          and EAX,4294967280
          mov ECX,EAX
          sub ECX,DWORD PTR [EDI+271040]
          mov EBX,ECX
          mov BYTE PTR [EDX+74],CL
          shr EBX,8
          mov BYTE PTR [EDX+73],BL
          mov EDX,DWORD PTR [EDI+271036]
          mov DWORD PTR [EDI+271040],EAX
          mov DWORD PTR [ESP],EAX
          add EDX,12
          mov DWORD PTR [ESP+4],EDX
          call _setBeU32
L_42bd88:
          mov DWORD PTR [ESP+100],OFFSET L_459efa
          mov DWORD PTR [ESP+96],1
          add ESP,76
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          jmp _log_printf
L_42bda4:
          mov EAX,DWORD PTR [ESP+24]
          add EAX,EBX
          mov DWORD PTR [ESP],EAX
          call _getBeU32
          mov EDI,EAX
          lea EAX,DWORD PTR [EBX+4]
          cmp EDI,-1
          je L_42be60
          add EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP],EAX
          call _getBeU32
          lea EDX,DWORD PTR [EAX*4]
          lea EAX,DWORD PTR [EBX+8]
          mov DWORD PTR [ESP+36],EAX
          mov EAX,ESI
          lea ESI,DWORD PTR [EDI+EDX*1]
          test EAX,EAX
          jne L_42be70
          imul EAX,EBP,1068
          add EAX,OFFSET _xb
          cmp ESI,DWORD PTR [EAX+271040]
          ja L_42beba
L_42bdfe:
          test EDX,EDX
          mov EAX,EDI
          je L_42be39
          sub EBX,EDI
          add EBX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP+52],EDX
          imul ECX,EBP,1068
          add ECX,OFFSET _xb
          .byte 0x8d,0xb6,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_42be20:
          movzx EDX,BYTE PTR [EBX+EAX*1+8]
          mov EDI,DWORD PTR [ECX+271036]
          mov BYTE PTR [EDI+EAX*1],DL
          add EAX,1
          cmp ESI,EAX
          jne L_42be20
L_42be35:
          mov EDX,DWORD PTR [ESP+52]
L_42be39:
          mov EBX,DWORD PTR [ESP+36]
          mov EAX,DWORD PTR [ESP+32]
          add EBX,EDX
          cmp EBX,DWORD PTR [EAX+271040]
          jb L_42bc21
L_42be4f:
          mov EDI,DWORD PTR [ESP+40]
          jmp L_42bc7d
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42be60:
          add DWORD PTR [ESP+28],1
          mov EBX,EAX
          jmp L_42bc11
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_42be70:
          mov EAX,DWORD PTR [ESP+44]
          add EAX,OFFSET _xb
          cmp ESI,DWORD PTR [EAX+271040]
          ja L_42bee8
L_42be81:
          test EDX,EDX
          je L_42be39
          sub EBX,EDI
          mov EAX,EDI
          mov EDI,DWORD PTR [ESP+44]
          add EBX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP+52],EDX
          lea ECX,DWORD PTR [EDI+_xb]
          nop
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_42bea0:
          movzx EDX,BYTE PTR [EBX+EAX*1+8]
          mov EDI,DWORD PTR [ECX+271036]
          mov BYTE PTR [EDI+EAX*1],DL
          add EAX,1
          cmp ESI,EAX
          jne L_42bea0
          .byte 0xe9; .long L_42be35-.-4   # jmp L_42be35
L_42beba:
          lea ECX,DWORD PTR [ESI+15]
          mov DWORD PTR [ESP+52],EDX
          and ECX,4294967280
          mov DWORD PTR [EAX+271040],ECX
          mov EAX,DWORD PTR [EAX+271036]
          mov DWORD PTR [ESP],ECX
          add EAX,12
          mov DWORD PTR [ESP+4],EAX
          call _setBeU32
          mov EDX,DWORD PTR [ESP+52]
          jmp L_42bdfe
L_42bee8:
          lea ECX,DWORD PTR [ESI+15]
          mov DWORD PTR [ESP+52],EDX
          and ECX,4294967280
          mov DWORD PTR [EAX+271040],ECX
          mov EAX,DWORD PTR [EAX+271036]
          mov DWORD PTR [ESP],ECX
          add EAX,12
          mov DWORD PTR [ESP+4],EAX
          call _setBeU32
          mov EDX,DWORD PTR [ESP+52]
          jmp L_42be81
L_42bf16:
          mov ESI,DWORD PTR [ESP+60]
          mov EDX,EDI
          mov DWORD PTR [ESP+4],OFFSET L_459f2c
          sub EDX,EBX
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+12],EDX
          add ESI,EDI
          sub ESI,EAX
          sub EAX,EDI
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+60],ESI
          call _log_printf
          jmp L_42bcf1
L_42bf49:
          xor EDI,EDI
          jmp L_42bb71
L_42bf50:
          xor EDI,EDI
          xor EBP,EBP
          xor ESI,ESI
          jmp L_42bbc8
L_42bf5b:
          xor EBP,EBP
          jmp L_42bb9d
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
_fixupPatchSet:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov EDX,DWORD PTR [L_4c4f98]
          test EDX,EDX
          jle L_42bfa8
          xor EBP,EBP
          cmp DWORD PTR [L_4bc150+4],23
          mov EAX,OFFSET L_4bc580
          jne L_42bfa1
          jmp L_42bfa8
L_42bf93:
          add EAX,1068
          cmp DWORD PTR [EAX-1068],23
          je L_42bfaa
L_42bfa1:
          add EBP,1
          cmp EDX,EBP
          jne L_42bf93
L_42bfa8:
          xor EBP,EBP
L_42bfaa:
          imul ESI,EBP,1068
          xor EDI,EDI
          add ESI,OFFSET _xb
          mov EAX,DWORD PTR [ESI+271036]
          mov DWORD PTR [ESP+4],OFFSET L_459fa6
          mov DWORD PTR [ESP],1
          mov EBX,EAX
          call _log_printf
          mov DWORD PTR [ESP+28],0
          mov EAX,DWORD PTR [ESP+28]
L_42bfe0:
          cmp EAX,DWORD PTR [ESI+271040]
          jae L_42c027
          cmp EDI,2
          jne L_42c043
          imul ECX,EBP,1068
          mov EDI,DWORD PTR [ESP+28]
          xor EAX,EAX
          add ECX,OFFSET _xb
          nop
L_42c000:
          mov EDX,DWORD PTR [ECX+271036]
          lea ESI,DWORD PTR [EDX+EDI*1]
          movzx ESI,BYTE PTR [ESI+EAX*1]
          mov EBX,ESI
          mov BYTE PTR [EDX+EAX*1],BL
          mov EDX,DWORD PTR [ECX+271040]
          add EAX,1
          sub EDX,EDI
          cmp EDX,EAX
          ja L_42c000
          mov DWORD PTR [ECX+271040],EDX
L_42c027:
          mov DWORD PTR [ESP+4],OFFSET L_459efa
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,44
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_42c043:
          mov EAX,DWORD PTR [ESP+28]
          add EAX,EBX
          mov DWORD PTR [ESP],EAX
          call _getBeU32
          mov ECX,DWORD PTR [ESP+28]
          cmp EAX,-1
          lea EDX,DWORD PTR [ECX+4]
          je L_42c080
          add EDX,EBX
          mov DWORD PTR [ESP],EDX
          call _getBeU32
          mov ECX,DWORD PTR [ESP+28]
          lea EAX,DWORD PTR [ECX+EAX*4+8]
          mov DWORD PTR [ESP+28],EAX
          jmp L_42bfe0
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42c080:
          add EDI,1
          mov DWORD PTR [ESP+28],EDX
          mov EAX,EDX
          jmp L_42bfe0
          .byte 0x66
          .byte 0x90
_addBlsToImage:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,60
          call _imgBigBlock
          cmp EAX,1
          sbb EAX,EAX
          and EAX,4294913546
          add EAX,61937
          cmp DWORD PTR [L_4c4f9c],1
          mov DWORD PTR [ESP+40],EAX
          jbe L_42c5f1
          xor EDI,EDI
          mov EBX,OFFSET L_4bc17c
          mov ESI,1
          mov EBP,EDI
          jmp L_42c15b
          .byte 0x90
L_42c0d0:
          cmp EDI,9
          je L_42c3f2
          cmp EDI,23
          je L_42c440
          cmp EAX,1
          je L_42c2c0
          cmp EAX,5
          jbe L_42c2cc
          lea EAX,DWORD PTR [EDI-23]
          and EAX,4294967293
          je L_42c420
L_42c100:
          cmp EDI,10
          je L_42c272
          cmp EDI,16
          je L_42c272
          cmp EDI,24
          jne L_42c2ee
L_42c11b:
          mov EDX,DWORD PTR [L_479eb4]
          test EDX,EDX
          jne L_42c380
          mov EAX,DWORD PTR [_g479ea8]
          sub EAX,4
          cmp EAX,1
          jbe L_42c380
          .byte 0x8d,0xb6,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_42c140:
          add EBP,DWORD PTR [EBX+1040]
L_42c146:
          add ESI,1
          add EBX,1068
          cmp DWORD PTR [L_4c4f9c],ESI
          jbe L_42c493
L_42c15b:
          mov EAX,DWORD PTR [EBX+1032]
          mov EDI,DWORD PTR [EBX+1028]
          mov DWORD PTR [ESP+8],4
          mov DWORD PTR [ESP+4],OFFSET _bd_459955
          mov DWORD PTR [ESP],EBX
          cmp EAX,-1
          cmovne EBP,EAX
          call _strnicmp
          test EAX,EAX
          jne L_42c193
          mov EAX,DWORD PTR [EBX+1024]
          test EAX,EAX
          je L_42c146
L_42c193:
          mov EAX,DWORD PTR [_g479ea8]
          cmp EAX,2
          jne L_42c0d0
          cmp EDI,14
          je L_42c140
          cmp EDI,21
          je L_42c560
          cmp EDI,10
          jne L_42c380
          mov EDI,DWORD PTR [L_4c4f98]
          test EDI,EDI
          jle L_42c1f0
          xor EAX,EAX
          cmp DWORD PTR [L_4bc150+4],9
          mov EDX,OFFSET L_4bc580
          jne L_42c1e3
          jmp L_42c1f0
L_42c1d4:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],9
          je L_42c1f2
L_42c1e3:
          add EAX,1
          cmp EAX,EDI
          jne L_42c1d4
          .byte 0x8d,0xb6,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_42c1f0:
          xor EAX,EAX
L_42c1f2:
          mov ECX,DWORD PTR [EBX+1040]
          mov DWORD PTR [ESP+12],EBP
          imul EAX,EAX,1068
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_459fc0
          mov DWORD PTR [ESP],1
          lea EDX,DWORD PTR [ECX+EBP*1]
          mov DWORD PTR [ESP+16],ECX
          sub EDX,DWORD PTR [EAX+L_4bc174]
          lea EDI,DWORD PTR [EAX+_xb]
          mov DWORD PTR [ESP+20],EDX
          call _log_printf
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+20],1
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+16],EAX
          mov EDX,DWORD PTR [EBX+1040]
          mov EAX,EDX
          sub EAX,DWORD PTR [EDI+271060]
L_42c257:
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [EBX+1036]
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+4],EAX
          call _imgAdd
          jmp L_42c140
L_42c272:
          cmp EDI,10
          jne L_42c31b
          mov EDI,DWORD PTR [L_4c4f98]
          test EDI,EDI
          jle L_42c1f0
          xor EAX,EAX
          cmp DWORD PTR [L_4bc150+4],9
          mov EDX,OFFSET L_4bc580
          jne L_42c2b3
          jmp L_42c1f0
          .byte 0x66
          .byte 0x90
L_42c2a0:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],9
          je L_42c1f2
L_42c2b3:
          add EAX,1
          cmp EAX,EDI
          jne L_42c2a0
          jmp L_42c1f0
          .byte 0x90
L_42c2c0:
          lea EAX,DWORD PTR [EDI-23]
          and EAX,4294967293
          je L_42c360
L_42c2cc:
          cmp EDI,25
          jne L_42c100
          mov EAX,DWORD PTR [EBX+1032]
          mov DWORD PTR [ESP+44],EAX
          call _imgSize
          cmp DWORD PTR [ESP+44],EAX
          jb L_42c5c0
L_42c2ee:
          mov EAX,DWORD PTR [EBX+1040]
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_45a000
          mov DWORD PTR [ESP],1
          lea EDX,DWORD PTR [EAX+EBP*1]
          mov DWORD PTR [ESP+16],EAX
          mov DWORD PTR [ESP+20],EDX
          call _log_printf
L_42c31b:
          cmp EDI,16
          je L_42c3b0
          cmp EDI,6
          je L_42c480
          cmp EDI,24
          je L_42c11b
L_42c336:
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+20],1
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+16],EAX
          mov EAX,DWORD PTR [EBX+1040]
          jmp L_42c257
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42c360:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_45a034
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_42c146
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_42c380:
          mov EAX,DWORD PTR [EBX+1040]
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_45a000
          mov DWORD PTR [ESP],1
          lea EDX,DWORD PTR [EAX+EBP*1]
          mov DWORD PTR [ESP+16],EAX
          mov DWORD PTR [ESP+20],EDX
          call _log_printf
          jmp L_42c336
          .byte 0x90
L_42c3b0:
          mov EDI,DWORD PTR [L_4c4f98]
          test EDI,EDI
          jle L_42c1f0
          xor EAX,EAX
          cmp DWORD PTR [L_4bc150+4],15
          mov EDX,OFFSET L_4bc580
          jne L_42c3e6
          jmp L_42c1f0
L_42c3d3:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],15
          je L_42c1f2
L_42c3e6:
          add EAX,1
          cmp EAX,EDI
          jne L_42c3d3
          jmp L_42c1f0
L_42c3f2:
          call _imgCfOffset
          mov EBP,EAX
          mov EAX,DWORD PTR [_g479ea8]
          cmp EAX,1
          je L_42c2ee
          cmp EAX,5
          jbe L_42c100
          lea EAX,DWORD PTR [EDI-23]
          and EAX,4294967293
          jne L_42c100
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_42c420:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_45a050
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_42c146
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_42c440:
          call _imgCfOffset
          mov EBP,EAX
          call _imgCfSize
          lea EDX,DWORD PTR [EBP+EAX*1]
          mov EBP,DWORD PTR [L_479eb4]
          test EBP,EBP
          je L_42c5a2
          mov EAX,DWORD PTR [_g479ea8]
          lea EBP,DWORD PTR [EDX+96]
L_42c466:
          cmp EAX,1
          je L_42c360
L_42c46f:
          cmp EAX,5
          ja L_42c420
          jmp L_42c100
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42c480:
          mov ECX,DWORD PTR [L_479eb8]
          test ECX,ECX
          je L_42c140
          jmp L_42c336
L_42c493:
          mov EDI,EBP
L_42c495:
          mov EAX,DWORD PTR [L_479ebc]
          test EAX,EAX
          je L_42c554
          mov EBX,DWORD PTR [L_4c4f98]
          test EBX,EBX
          jle L_42c4da
          xor EAX,EAX
          cmp DWORD PTR [L_4bc150+4],14
          mov EDX,OFFSET L_4bc580
          jne L_42c4d3
          jmp L_42c4da
          .byte 0x66
          .byte 0x90
L_42c4c0:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],14
          je L_42c5e0
L_42c4d3:
          add EAX,1
          cmp EBX,EAX
          jne L_42c4c0
L_42c4da:
          mov EDX,270000
          xor EAX,EAX
L_42c4e1:
          imul EAX,EAX,1068
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+4],OFFSET L_45a000
          mov DWORD PTR [ESP],1
          lea EBX,DWORD PTR [EAX+_xb]
          mov EAX,DWORD PTR [EAX+L_4bc150+16]
          lea ESI,DWORD PTR [EAX+EDI*1]
          mov DWORD PTR [ESP+16],EAX
          lea EAX,DWORD PTR [EDX+_xb]
          mov DWORD PTR [ESP+20],ESI
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+20],1
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+16],EAX
          mov EAX,DWORD PTR [EBX+271040]
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [EBX+271036]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],EAX
          call _imgAdd
L_42c554:
          add ESP,60
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_42c560:
          mov EDI,DWORD PTR [L_4c4f98]
          test EDI,EDI
          jle L_42c1f0
          xor EAX,EAX
          cmp DWORD PTR [L_4bc150+4],20
          mov EDX,OFFSET L_4bc580
          jne L_42c596
          jmp L_42c1f0
L_42c583:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],20
          je L_42c1f2
L_42c596:
          add EAX,1
          cmp EAX,EDI
          jne L_42c583
          jmp L_42c1f0
L_42c5a2:
          mov EAX,DWORD PTR [_g479ea8]
          lea EBP,DWORD PTR [EDX+16]
          lea ECX,DWORD PTR [EAX-4]
          cmp ECX,1
          ja L_42c466
          lea EBP,DWORD PTR [EDX+96]
          jmp L_42c46f
          .byte 0x66
          .byte 0x90
L_42c5c0:
          mov DWORD PTR [ESP+4],OFFSET L_45a074
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_42c146
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42c5e0:
          imul EDX,EAX,1068
          add EDX,270000
          jmp L_42c4e1
L_42c5f1:
          xor EDI,EDI
          jmp L_42c495
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _isUpdateBl
          .byte 0x8d
          .byte 0x76
          .byte 0x0
_addUpdateBls:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,60
          call _imgBigBlock
          cmp EAX,1
          sbb EAX,EAX
          and EAX,4294913546
          add EAX,61937
          mov DWORD PTR [ESP+44],EAX
          mov EAX,DWORD PTR [L_4c4f9c]
          cmp EAX,1
          jbe L_42c71d
          mov EBX,OFFSET L_4bc17c
          xor EBP,EBP
          mov EDI,1
          jmp L_42c671
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_42c660:
          add EDI,1
          add EBX,1068
          cmp EAX,EDI
          jbe L_42c71d
L_42c671:
          mov ESI,DWORD PTR [EBX+1028]
          cmp ESI,23
          je L_42c68b
          cmp ESI,25
          ja L_42c660
          mov ECX,50431488
          bt ECX,ESI
          jae L_42c660
L_42c68b:
          mov EAX,DWORD PTR [EBX+1032]
          mov DWORD PTR [ESP+8],4
          mov DWORD PTR [ESP+4],OFFSET _bd_459955
          mov DWORD PTR [ESP],EBX
          cmp EAX,-1
          cmovne EBP,EAX
          call _strnicmp
          test EAX,EAX
          jne L_42c6bd
          mov ECX,DWORD PTR [EBX+1024]
          test ECX,ECX
          je L_42c707
L_42c6bd:
          cmp ESI,9
          je L_42c725
          cmp ESI,23
          je L_42c8d1
          cmp ESI,25
          je L_42c8a0
L_42c6d4:
          cmp ESI,10
          je L_42c792
          cmp ESI,16
          je L_42c792
          cmp ESI,24
          jne L_42c72c
L_42c6eb:
          mov EAX,DWORD PTR [L_479eb4]
          test EAX,EAX
          jne L_42c72c
          mov EAX,DWORD PTR [_g479ea8]
          sub EAX,4
          cmp EAX,1
          jbe L_42c72c
L_42c701:
          add EBP,DWORD PTR [EBX+1040]
L_42c707:
          mov EAX,DWORD PTR [L_4c4f9c]
          add EDI,1
          add EBX,1068
          cmp EAX,EDI
          ja L_42c671
L_42c71d:
          add ESP,60
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_42c725:
          call _imgCfOffset
          mov EBP,EAX
L_42c72c:
          mov EAX,DWORD PTR [EBX+1040]
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_45a000
          mov DWORD PTR [ESP],1
          lea EDX,DWORD PTR [EAX+EBP*1]
          mov DWORD PTR [ESP+16],EAX
          mov DWORD PTR [ESP+20],EDX
          call _log_printf
L_42c759:
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+20],1
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+16],EAX
          mov EAX,DWORD PTR [EBX+1040]
L_42c777:
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [EBX+1036]
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+4],EAX
          call _imgAdd
          jmp L_42c701
L_42c792:
          cmp ESI,10
          jne L_42c842
          mov ESI,DWORD PTR [L_4c4f98]
          test ESI,ESI
          jle L_42c7d6
          xor EAX,EAX
          cmp DWORD PTR [L_4bc150+4],9
          mov EDX,OFFSET L_4bc580
          jne L_42c7cf
          jmp L_42c7d6
L_42c7b7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_42c7c0:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],9
          je L_42c7d8
L_42c7cf:
          add EAX,1
          cmp EAX,ESI
          jne L_42c7c0
L_42c7d6:
          xor EAX,EAX
L_42c7d8:
          imul EAX,EAX,1068
          mov ECX,DWORD PTR [EBX+1040]
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_459fc0
          mov DWORD PTR [ESP],1
          lea EDX,DWORD PTR [ECX+EBP*1]
          sub EDX,DWORD PTR [EAX+L_4bc174]
          mov DWORD PTR [ESP+16],ECX
          lea ESI,DWORD PTR [EAX+_xb]
          mov DWORD PTR [ESP+20],EDX
          call _log_printf
          mov EAX,DWORD PTR [ESP+44]
          mov EDX,DWORD PTR [EBX+1040]
          mov DWORD PTR [ESP+20],1
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+16],EAX
          mov EAX,EDX
          sub EAX,DWORD PTR [ESI+271060]
          jmp L_42c777
L_42c842:
          cmp ESI,16
          je L_42c855
          cmp ESI,24
          jne L_42c759
          jmp L_42c6eb
L_42c855:
          mov ESI,DWORD PTR [L_4c4f98]
          test ESI,ESI
          jle L_42c7d6
          xor EAX,EAX
          cmp DWORD PTR [L_4bc150+4],15
          mov EDX,OFFSET L_4bc580
          jne L_42c893
          jmp L_42c7d6
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42c880:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],15
          je L_42c7d8
L_42c893:
          add EAX,1
          cmp EAX,ESI
          jne L_42c880
          jmp L_42c7d6
          .byte 0x90
L_42c8a0:
          mov ESI,DWORD PTR [EBX+1032]
          call _imgSize
          cmp ESI,EAX
          jae L_42c72c
          mov DWORD PTR [ESP+4],OFFSET L_45a074
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_4c4f9c]
          jmp L_42c660
L_42c8d1:
          call _imgCfOffset
          mov EBP,EAX
          call _imgCfSize
          mov EDX,DWORD PTR [L_479eb4]
          add EAX,EBP
          lea ECX,DWORD PTR [EAX+96]
          add EAX,16
          test EDX,EDX
          cmove ECX,EAX
          mov EBP,ECX
          jmp L_42c6d4
L_42c8f7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
_logPowerButton:
          sub ESP,28
          mov EAX,DWORD PTR [ESP+32]
          sub EAX,17
          cmp EAX,73
          ja L_42cb80
          jmp DWORD PTR [EAX*4+L_45a468]
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42c920:
          mov EAX,DWORD PTR [L_479ea4]
          and EAX,7
          cmp EAX,4
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+8],EAX
          jbe L_42cb60
          mov DWORD PTR [ESP+4],OFFSET L_45a2f4
          mov DWORD PTR [ESP],1
          call _log_printf
          xor EAX,EAX
          jmp L_42c96f
L_42c951:
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+4],OFFSET L_45a0bc
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          xor EAX,EAX
L_42c96f:
          add ESP,28
          ret 
L_42c973:
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+4],OFFSET L_45a0f0
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          xor EAX,EAX
          jmp L_42c96f
L_42c993:
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+4],OFFSET L_45a128
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          xor EAX,EAX
          jmp L_42c96f
L_42c9b3:
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+4],OFFSET L_45a15c
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          xor EAX,EAX
          jmp L_42c96f
L_42c9d3:
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+4],OFFSET L_45a194
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          xor EAX,EAX
          jmp L_42c96f
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_42ca00:
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+4],OFFSET L_45a1cc
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          xor EAX,EAX
          jmp L_42c96f
L_42ca23:
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+4],OFFSET L_45a1f8
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          xor EAX,EAX
          jmp L_42c96f
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_42ca50:
          mov EAX,DWORD PTR [L_479ea4]
          and EAX,7
          cmp EAX,4
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+8],EAX
          jbe L_42cb43
          mov DWORD PTR [ESP+4],OFFSET L_45a36c
          mov DWORD PTR [ESP],1
          call _log_printf
          xor EAX,EAX
          jmp L_42c96f
L_42ca84:
          mov EAX,DWORD PTR [L_479ea4]
          and EAX,7
          cmp EAX,4
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+8],EAX
          ja L_42cb90
          mov DWORD PTR [ESP+4],OFFSET L_45a428
          mov DWORD PTR [ESP],1
          call _log_printf
          xor EAX,EAX
          jmp L_42c96f
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42cac0:
          mov EAX,DWORD PTR [L_479ea4]
          and EAX,7
          cmp EAX,4
          jbe L_42cb20
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+4],OFFSET L_45a2b4
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          xor EAX,EAX
          jmp L_42c96f
L_42caf0:
          mov EAX,DWORD PTR [L_479ea4]
          and EAX,7
          cmp EAX,4
          jbe L_42cb20
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+4],OFFSET L_45a23c
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          xor EAX,EAX
          jmp L_42c96f
L_42cb20:
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+4],OFFSET L_45a278
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          xor EAX,EAX
          jmp L_42c96f
L_42cb43:
          mov DWORD PTR [ESP+4],OFFSET L_45a3ac
          mov DWORD PTR [ESP],1
          call _log_printf
          xor EAX,EAX
          jmp L_42c96f
          .byte 0x66
          .byte 0x90
L_42cb60:
          mov DWORD PTR [ESP+4],OFFSET L_45a334
          mov DWORD PTR [ESP],1
          call _log_printf
          xor EAX,EAX
          jmp L_42c96f
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_42cb80:
          mov EAX,1
          jmp L_42c96f
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42cb90:
          mov DWORD PTR [ESP+4],OFFSET L_45a3e8
          mov DWORD PTR [ESP],1
          call _log_printf
          xor EAX,EAX
          jmp L_42c96f
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
#@C _patchFreeboot
L_42ced1:
          jmp _patchPayloadSize
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
#@C _patchPayloadSize
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
_encodeBls:
          push EBP
          push EDI
          push ESI
          push EBX
          mov ESI,1
          mov EBX,OFFSET L_4bc590
          sub ESP,76
          cmp DWORD PTR [L_4c4f9c],1
          jbe L_42d065
          .byte 0x66   # nop
          nop
L_42cfc0:
          lea EDI,DWORD PTR [EBX-1044]
          mov DWORD PTR [ESP+8],4
          mov DWORD PTR [ESP+4],OFFSET _bd_459955
          mov DWORD PTR [ESP],EDI
          call _strnicmp
          test EAX,EAX
          jne L_42cfe9
          mov EAX,DWORD PTR [EBX-20]
          test EAX,EAX
          je L_42d050
L_42cfe9:
          mov EAX,DWORD PTR [_g479ea8]
          mov EBP,DWORD PTR [EBX-16]
          cmp EAX,2
          je L_42d860
          cmp EAX,3
          jbe L_42d520
          cmp EBP,24
          je L_42d050
          mov EAX,DWORD PTR [EBX-4]
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET _bd_45a8af
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+12],EAX
          call _log_printf
          cmp EBP,25
          ja L_42d503
          jmp DWORD PTR [EBP*4+L_45a968]
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_42d040:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],EDI
          call _kvPrepare
L_42d050:
          add ESI,1
          add EBX,1068
          cmp DWORD PTR [L_4c4f9c],ESI
          ja L_42cfc0
L_42d065:
          mov EAX,DWORD PTR [L_479ebc]
          test EAX,EAX
          je L_42d153
          mov EBX,DWORD PTR [L_4c4f98]
          test EBX,EBX
          jle L_42df95
          mov ECX,DWORD PTR [L_4bc150+4]
          xor EAX,EAX
          mov EDX,OFFSET L_4bc580
          cmp ECX,14
          jne L_42d0b3
          jmp L_42df84
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_42d0a0:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],14
          je L_42de92
L_42d0b3:
          add EAX,1
          cmp EAX,EBX
          jne L_42d0a0
          mov ESI,271044
          mov EDI,270000
          xor EAX,EAX
L_42d0c6:
          cmp ECX,7
          je L_42d0ee
L_42d0cb:
          mov ECX,OFFSET L_4bc580
          xor EDX,EDX
          jmp L_42d0e7
L_42d0d4:
          add ECX,1068
          cmp DWORD PTR [ECX-1068],7
          je L_42dea9
L_42d0e7:
          add EDX,1
          cmp EDX,EBX
          jne L_42d0d4
L_42d0ee:
          mov EBX,271044
L_42d0f3:
          imul EAX,EAX,1068
          add EDI,OFFSET _xb
          mov DWORD PTR [ESP+4],OFFSET L_45a94c
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP],1
          add ESI,OFFSET _xb
          add EBX,OFFSET _xb
          lea EBP,DWORD PTR [EAX+_xb]
          mov EAX,DWORD PTR [EAX+L_4bc150+16]
          mov DWORD PTR [ESP+12],EAX
          call _log_printf
          mov EAX,DWORD PTR [EBP+271040]
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [EBP+271036]
          mov DWORD PTR [ESP],EAX
          call _ceEncrypt
L_42d153:
          xor EAX,EAX
L_42d155:
          add ESP,76
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_42d160:
          mov EAX,DWORD PTR [EBX-4]
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+96]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [EBX-8]
          mov DWORD PTR [ESP],EAX
          call _smcPrepare
          test EAX,EAX
          je L_42d050
          mov EAX,1
          jmp L_42d155
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42d190:
          mov ECX,DWORD PTR [L_4c4f98]
          test ECX,ECX
          jle L_42d1d0
          xor EAX,EAX
          cmp DWORD PTR [L_4bc150+4],15
          mov EDX,OFFSET L_4bc580
          jne L_42d1c3
          jmp L_42d1d0
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_42d1b0:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],15
          je L_42d890
L_42d1c3:
          add EAX,1
          cmp EAX,ECX
          jne L_42d1b0
          .byte 0x8d,0xb6,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_42d1d0:
          mov EAX,271044
L_42d1d5:
          mov EDX,DWORD PTR [EBX-4]
          add EAX,OFFSET _xb
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP+12],EDX
          mov EAX,DWORD PTR [EBX-8]
          mov DWORD PTR [ESP],EAX
          call _cgEncrypt
          jmp L_42d050
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42d200:
          mov EDX,DWORD PTR [L_4c4f98]
          test EDX,EDX
          jle L_42d235
          xor EBP,EBP
          cmp DWORD PTR [L_4bc150+4],16
          mov EAX,OFFSET L_4bc580
          jne L_42d22e
          jmp L_42d235
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_42d220:
          add EAX,1068
          cmp DWORD PTR [EAX-1068],16
          je L_42d237
L_42d22e:
          add EBP,1
          cmp EDX,EBP
          jne L_42d220
L_42d235:
          xor EBP,EBP
L_42d237:
          call _imgCfSize
          mov DWORD PTR [ESP+16],EAX
          movzx EAX,WORD PTR [ESP+100]
          imul EBP,EBP,1068
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [EBP+L_4bc150+16]
          mov DWORD PTR [ESP+4],EAX
          call _cfEncrypt
          jmp L_42d050
          .byte 0x66
          .byte 0x90
L_42d270:
          mov ECX,DWORD PTR [L_4c4f98]
          test ECX,ECX
          jle L_42d2aa
          xor EAX,EAX
          cmp DWORD PTR [L_4bc150+4],13
          mov EDX,OFFSET L_4bc580
          jne L_42d2a3
          jmp L_42d2aa
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_42d290:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],13
          je L_42d8a0
L_42d2a3:
          add EAX,1
          cmp ECX,EAX
          jne L_42d290
L_42d2aa:
          mov EAX,271044
L_42d2af:
          mov EDX,DWORD PTR [EBX-4]
          add EAX,OFFSET _xb
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP+12],EDX
          mov EAX,DWORD PTR [EBX-8]
          mov DWORD PTR [ESP],EAX
          call _ceEncrypt
          jmp L_42d050
L_42d2d3:
          mov ECX,DWORD PTR [L_4c4f98]
          test ECX,ECX
          jle L_42d30a
          xor EAX,EAX
          cmp DWORD PTR [L_4bc150+4],12
          mov EDX,OFFSET L_4bc580
          jne L_42d303
          jmp L_42d30a
          .byte 0x90
L_42d2f0:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],12
          je L_42d8b0
L_42d303:
          add EAX,1
          cmp EAX,ECX
          jne L_42d2f0
L_42d30a:
          mov EAX,271044
L_42d30f:
          mov EDX,DWORD PTR [EBX-4]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+12],EDX
L_42d31a:
          add EAX,OFFSET _xb
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [EBX-8]
          mov DWORD PTR [ESP],EAX
          call _cdEncrypt
          jmp L_42d050
L_42d333:
          mov EAX,DWORD PTR [EBX-4]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [EBX-8]
          mov DWORD PTR [ESP],EAX
          call _cdEncryptZero
          jmp L_42d050
          .byte 0x66
          .byte 0x90
L_42d350:
          mov EDX,DWORD PTR [L_4c4f98]
          test EDX,EDX
          jle L_42d235
          xor EBP,EBP
          cmp DWORD PTR [L_4bc150+4],10
          mov EAX,OFFSET L_4bc580
          jne L_42d385
          jmp L_42d235
L_42d373:
          add EAX,1068
          cmp DWORD PTR [EAX-1068],10
          je L_42d237
L_42d385:
          add EBP,1
          cmp EBP,EDX
          jne L_42d373
          jmp L_42d235
L_42d391:
          mov ECX,DWORD PTR [L_4c4f98]
          test ECX,ECX
          jle L_42d2aa
          xor EAX,EAX
          cmp DWORD PTR [L_4bc150+4],7
          mov EDX,OFFSET L_4bc580
          jne L_42d3c7
          jmp L_42d2aa
L_42d3b4:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],7
          je L_42d8a0
L_42d3c7:
          add EAX,1
          cmp EAX,ECX
          jne L_42d3b4
          jmp L_42d2aa
L_42d3d3:
          mov ECX,DWORD PTR [L_4c4f98]
          test ECX,ECX
          jle L_42d30a
          xor EAX,EAX
          cmp DWORD PTR [L_4bc150+4],12
          mov EDX,OFFSET L_4bc580
          jne L_42d413
          jmp L_42d30a
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_42d400:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],12
          je L_42d8b0
L_42d413:
          add EAX,1
          cmp EAX,ECX
          jne L_42d400
          jmp L_42d30a
          .byte 0x90
L_42d420:
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EDI
          call _kvPrepare
          jmp L_42d050
L_42d435:
          mov EAX,DWORD PTR [_g479ea8]
          sub EAX,4
          cmp EAX,1
          jbe L_42da00
          mov EAX,DWORD PTR [EBX-8]
          mov EBP,DWORD PTR [L_479ebc]
          add EAX,2
          mov DWORD PTR [ESP],EAX
          call _getBeU16
          movzx EDI,AX
          mov EAX,DWORD PTR [EBX-8]
          add EAX,944
          mov DWORD PTR [ESP],EAX
          call _getBeU32
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+4],EDI
          call _showExpectedFuses
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET _cpuKey
          call _checkZeros
          test EAX,EAX
          je L_42d9ea
          mov DWORD PTR [ESP+4],OFFSET L_45a8d8
          mov DWORD PTR [ESP],1
          call _log_printf
          mov BYTE PTR [L_479f15],0
          jmp L_42d94c
L_42d4c1:
          mov ECX,DWORD PTR [L_4c4f98]
          test ECX,ECX
          jle L_42d1d0
          xor EAX,EAX
          cmp DWORD PTR [L_4bc150+4],9
          mov EDX,OFFSET L_4bc580
          jne L_42d4f7
          jmp L_42d1d0
L_42d4e4:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],9
          je L_42d890
L_42d4f7:
          add EAX,1
          cmp EAX,ECX
          jne L_42d4e4
          jmp L_42d1d0
L_42d503:
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_45a900
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_42d050
L_42d520:
          cmp EBP,24
          jne L_42d560
          mov EBP,DWORD PTR [L_479eb4]
          test EBP,EBP
          je L_42d050
          mov EAX,DWORD PTR [EBX-4]
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET _bd_45a8af
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+12],EAX
          call _log_printf
          jmp L_42d050
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_42d560:
          mov EAX,DWORD PTR [EBX-4]
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET _bd_45a8af
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+12],EAX
          call _log_printf
          cmp EBP,10
          ja L_42d050
          jmp DWORD PTR [EBP*4+L_45a9d0]
          .byte 0x90
L_42d590:
          mov ECX,DWORD PTR [L_4c4f98]
          test ECX,ECX
          jle L_42d1d0
          xor EAX,EAX
          cmp DWORD PTR [L_4bc150+4],9
          mov EDX,OFFSET L_4bc580
          jne L_42d5c6
          jmp L_42d1d0
L_42d5b3:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],9
          je L_42d890
L_42d5c6:
          add EAX,1
          cmp EAX,ECX
          jne L_42d5b3
          jmp L_42d1d0
L_42d5d2:
          mov EDX,DWORD PTR [L_4c4f98]
          test EDX,EDX
          jle L_42d235
          xor EBP,EBP
          cmp DWORD PTR [L_4bc150+4],10
          mov EAX,OFFSET L_4bc580
          jne L_42d607
          jmp L_42d235
L_42d5f5:
          add EAX,1068
          cmp DWORD PTR [EAX-1068],10
          je L_42d237
L_42d607:
          add EBP,1
          cmp EBP,EDX
          jne L_42d5f5
          jmp L_42d235
L_42d613:
          mov ECX,DWORD PTR [L_4c4f98]
          test ECX,ECX
          jle L_42d2aa
          xor EAX,EAX
          cmp DWORD PTR [L_4bc150+4],7
          mov EDX,OFFSET L_4bc580
          jne L_42d653
          jmp L_42d2aa
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_42d640:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],7
          je L_42d8a0
L_42d653:
          add EAX,1
          cmp EAX,ECX
          jne L_42d640
          jmp L_42d2aa
          .byte 0x90
L_42d660:
          mov EAX,DWORD PTR [L_479eb8]
          mov ECX,DWORD PTR [L_4c4f98]
          test EAX,EAX
          jne L_42d8c0
          test ECX,ECX
          jle L_42d6aa
          xor EAX,EAX
          cmp DWORD PTR [L_4bc150+4],5
          mov EDX,OFFSET L_4bc580
          jne L_42d6a3
          jmp L_42d6aa
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42d690:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],5
          je L_42de82
L_42d6a3:
          add EAX,1
          cmp EAX,ECX
          jne L_42d690
L_42d6aa:
          mov EAX,271044
L_42d6af:
          cmp DWORD PTR [_g479ea8],1
          mov EDX,DWORD PTR [EBX-4]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+12],EDX
          jne L_42d31a
          add EAX,OFFSET _xb
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [EBX-8]
          mov DWORD PTR [ESP],EAX
          call _cdEncryptCpu
          jmp L_42d050
L_42d6e0:
          mov ECX,DWORD PTR [L_479eb8]
          test ECX,ECX
          je L_42d050
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET _cpuKey
          call _checkZeros
          mov ECX,DWORD PTR [L_4c4f98]
          mov EDI,EAX
          test ECX,ECX
          jle L_42d736
          xor EAX,EAX
          cmp DWORD PTR [L_4bc150+4],24
          mov EDX,OFFSET L_4bc580
          jne L_42d72f
          jmp L_42d736
L_42d720:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],24
          je L_42d738
L_42d72f:
          add EAX,1
          cmp EAX,ECX
          jne L_42d720
L_42d736:
          xor EAX,EAX
L_42d738:
          mov EDX,DWORD PTR [L_479eb4]
          test EDX,EDX
          je L_42deba
          imul EAX,EAX,1068
          mov ECX,DWORD PTR [L_479ebc]
          mov EBP,DWORD PTR [EAX+L_4bc150+12]
          mov EAX,DWORD PTR [EBX-8]
          mov DWORD PTR [ESP+44],ECX
          add EAX,2
          mov DWORD PTR [ESP],EAX
          call _getBeU16
          mov ECX,DWORD PTR [EBX-8]
          mov WORD PTR [ESP+40],AX
          lea EAX,DWORD PTR [ECX+944]
          mov DWORD PTR [ESP],EAX
          call _getBeU32
          mov DWORD PTR [ESP+8],EBP
          movzx EBP,WORD PTR [ESP+40]
          mov ECX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+12],ECX
          mov DWORD PTR [ESP+4],EBP
          call _showExpectedFuses
          test EDI,EDI
          jne L_42df09
L_42d7a5:
          mov ECX,DWORD PTR [L_4c4f98]
          test ECX,ECX
          jle L_42d7db
          xor EAX,EAX
          cmp DWORD PTR [L_4bc150+4],5
          mov EDX,OFFSET L_4bc580
          jne L_42d7d4
          jmp L_42d7db
L_42d7c1:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],5
          je L_42df58
L_42d7d4:
          add EAX,1
          cmp EAX,ECX
          jne L_42d7c1
L_42d7db:
          mov EDX,271044
          xor EAX,EAX
L_42d7e2:
          imul EAX,EAX,1068
          mov DWORD PTR [ESP+24],EDI
          mov ECX,DWORD PTR [EBX-4]
          add EDX,OFFSET _xb
          mov DWORD PTR [ESP+16],EBX
          mov DWORD PTR [ESP+8],EDX
          mov EAX,DWORD PTR [EAX+L_4bc150+12]
          mov DWORD PTR [ESP+20],ECX
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [EBX-8]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+96]
          mov DWORD PTR [ESP],EAX
          call _cbbEncrypt
          jmp L_42d050
L_42d823:
          mov EDI,DWORD PTR [L_479eb8]
          test EDI,EDI
          je L_42d900
          mov DWORD PTR [ESP+16],1
L_42d839:
          mov EAX,DWORD PTR [EBX-4]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [EBX-8]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+96]
          mov DWORD PTR [ESP],EAX
          call _cbaEncrypt
          jmp L_42d050
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_42d860:
          mov EAX,DWORD PTR [EBX-4]
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET L_45a824
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+12],EAX
          call _log_printf
          cmp EBP,22
          ja L_42d050
          jmp DWORD PTR [EBP*4+L_45a9fc]
          .byte 0x90
L_42d890:
          imul EAX,EAX,1068
          add EAX,271044
          jmp L_42d1d5
L_42d8a0:
          imul EAX,EAX,1068
          add EAX,271044
          jmp L_42d2af
L_42d8b0:
          imul EAX,EAX,1068
          add EAX,271044
          jmp L_42d30f
L_42d8c0:
          test ECX,ECX
          jle L_42d30a
          xor EAX,EAX
          cmp DWORD PTR [L_4bc150+4],6
          mov EDX,OFFSET L_4bc580
          jne L_42d8ef
          jmp L_42d30a
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_42d8e0:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],6
          je L_42d8b0
L_42d8ef:
          add EAX,1
          cmp EAX,ECX
          jne L_42d8e0
          jmp L_42d30a
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_42d900:
          mov EAX,DWORD PTR [EBX-8]
          mov EBP,DWORD PTR [L_479ebc]
          add EAX,2
          mov DWORD PTR [ESP],EAX
          call _getBeU16
          movzx EDI,AX
          mov EAX,DWORD PTR [EBX-8]
          add EAX,944
          mov DWORD PTR [ESP],EAX
          call _getBeU32
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EAX
          call _showExpectedFuses
          cmp DWORD PTR [_g479ea8],1
          je L_42d9ea
L_42d94c:
          mov EAX,DWORD PTR [EBX-4]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [EBX-8]
          mov DWORD PTR [ESP],EAX
          call _cbaEncryptZero
          jmp L_42d050
L_42d967:
          mov ECX,DWORD PTR [L_4c4f98]
          test ECX,ECX
          jle L_42d999
          xor EAX,EAX
          cmp DWORD PTR [L_4bc150+4],24
          mov EDX,OFFSET L_4bc580
          jne L_42d992
          jmp L_42d999
L_42d983:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],24
          je L_42d99b
L_42d992:
          add EAX,1
          cmp EAX,ECX
          jne L_42d983
L_42d999:
          xor EAX,EAX
L_42d99b:
          imul EAX,EAX,1068
          mov EDI,DWORD PTR [L_479ebc]
          mov EBP,DWORD PTR [EAX+L_4bc150+12]
          mov EAX,DWORD PTR [EBX-8]
          add EAX,2
          mov DWORD PTR [ESP],EAX
          call _getBeU16
          mov ECX,DWORD PTR [EBX-8]
          mov WORD PTR [ESP+40],AX
          lea EAX,DWORD PTR [ECX+944]
          mov DWORD PTR [ESP],EAX
          call _getBeU32
          mov DWORD PTR [ESP+12],EDI
          movzx EDI,WORD PTR [ESP+40]
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],EDI
          call _showExpectedFuses
L_42d9ea:
          mov DWORD PTR [ESP+16],0
          jmp L_42d839
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_42da00:
          mov EDX,DWORD PTR [L_4c4f98]
          test EDX,EDX
          jle L_42da35
          xor EDI,EDI
          cmp DWORD PTR [L_4bc150+4],24
          mov EAX,OFFSET L_4bc580
          jne L_42da2e
          jmp L_42da35
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_42da20:
          add EAX,1068
          cmp DWORD PTR [EAX-1068],24
          je L_42da37
L_42da2e:
          add EDI,1
          cmp EDI,EDX
          jne L_42da20
L_42da35:
          xor EDI,EDI
L_42da37:
          mov EAX,DWORD PTR [L_479ea4]
          mov EBP,DWORD PTR [L_479ebc]
          and EAX,7
          cmp EAX,4
          mov EAX,DWORD PTR [EBX-8]
          jbe L_42df29
          add EAX,2
          mov DWORD PTR [ESP],EAX
          call _getBeU16
          movzx EAX,AX
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],50331648
          call _showExpectedFuses
L_42da7b:
          imul EDI,EDI,1068
          mov DWORD PTR [ESP+4],OFFSET L_45a8c6
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [EDI+L_4bc150+12]
          mov DWORD PTR [ESP],EAX
          call _setFuseCpuKey
          jmp L_42d94c
L_42daa8:
          mov EDI,DWORD PTR [EBX-8]
          mov DWORD PTR [ESP+8],512
          mov DWORD PTR [ESP+4],OFFSET L_44a760
          mov DWORD PTR [ESP],EDI
          call _memcmp
          test EAX,EAX
          jne L_42d050
          mov EBP,DWORD PTR [L_4c4f98]
          test EBP,EBP
          jle L_42db0a
          xor EDX,EDX
          cmp DWORD PTR [L_4bc150+4],22
          mov ECX,OFFSET L_4bc580
          jne L_42db03
          jmp L_42db0a
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_42daf0:
          add ECX,1068
          cmp DWORD PTR [ECX-1068],22
          je L_42df7d
L_42db03:
          add EDX,1
          cmp EDX,EBP
          jne L_42daf0
L_42db0a:
          imul EAX,EAX,1068
          mov EDX,DWORD PTR [EBX-4]
          mov DWORD PTR [ESP+4],OFFSET _bd_45a7c4
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+60],4294934584
          mov EAX,DWORD PTR [EAX+L_4bc150+16]
          mov DWORD PTR [ESP+40],EDX
          lea EBP,DWORD PTR [EAX+3]
          mov DWORD PTR [ESP+8],EAX
          sar EBP,2
          mov DWORD PTR [ESP+12],EBP
          call _log_printf
          mov EDX,DWORD PTR [ESP+40]
          lea EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+12],4
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],EDX
          call _findInst
          test EAX,EAX
          mov EDI,EAX
          je L_42d050
          movzx EAX,BYTE PTR [EAX+3]
          mov DWORD PTR [ESP+12],EAX
          movzx EAX,BYTE PTR [EDI+2]
          mov DWORD PTR [ESP+4],OFFSET _bd_45a7f8
          mov DWORD PTR [ESP],2
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov EDX,EBP
          mov EAX,EBP
          shr EDX,8
          movzx EBP,AL
          mov BYTE PTR [EDI+3],AL
          mov BYTE PTR [EDI+2],DL
          movzx EDX,DL
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP+4],OFFSET _bd_45a80e
          mov DWORD PTR [ESP],2
          call _log_printf
          jmp L_42d050
L_42dbc9:
          mov EDI,DWORD PTR [EBX-8]
          mov DWORD PTR [ESP+8],3392
          mov DWORD PTR [ESP+4],OFFSET L_44a960
          mov DWORD PTR [ESP],EDI
          call _memcmp
          test EAX,EAX
          je L_42df69
          mov EAX,DWORD PTR [L_479f00]
          test EAX,EAX
          je L_42d050
          mov DWORD PTR [ESP+4],OFFSET L_45a844
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_42d050
L_42dc12:
          mov ECX,DWORD PTR [L_4c4f98]
          test ECX,ECX
          jle L_42d1d0
          xor EAX,EAX
          cmp DWORD PTR [L_4bc150+4],20
          mov EDX,OFFSET L_4bc580
          jne L_42dc48
          jmp L_42d1d0
L_42dc35:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],20
          je L_42d890
L_42dc48:
          add EAX,1
          cmp EAX,ECX
          jne L_42dc35
          jmp L_42d1d0
L_42dc54:
          mov EDX,DWORD PTR [L_4c4f98]
          test EDX,EDX
          jle L_42dc85
          xor EBP,EBP
          cmp DWORD PTR [L_4bc150+4],21
          mov EAX,OFFSET L_4bc580
          jne L_42dc7e
          jmp L_42dc85
L_42dc70:
          add EAX,1068
          cmp DWORD PTR [EAX-1068],21
          je L_42dc87
L_42dc7e:
          add EBP,1
          cmp EBP,EDX
          jne L_42dc70
L_42dc85:
          xor EBP,EBP
L_42dc87:
          call _imgCfSize
          mov DWORD PTR [ESP+16],EAX
          movzx EAX,WORD PTR [ESP+100]
          imul EBP,EBP,1068
          mov DWORD PTR [ESP+12],1
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [EBP+L_4bc150+16]
          mov DWORD PTR [ESP+4],EAX
          call _cfEncrypt
          movzx EAX,AX
          add DWORD PTR [ESP+100],EAX
          jmp L_42d050
L_42dcc5:
          mov ECX,DWORD PTR [L_4c4f98]
          test ECX,ECX
          jle L_42d2aa
          xor EAX,EAX
          cmp DWORD PTR [L_4bc150+4],18
          mov EDX,OFFSET L_4bc580
          jne L_42dd03
          jmp L_42d2aa
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42dcf0:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],18
          je L_42d8a0
L_42dd03:
          add EAX,1
          cmp EAX,ECX
          jne L_42dcf0
          jmp L_42d2aa
L_42dd0f:
          mov ECX,DWORD PTR [L_4c4f98]
          test ECX,ECX
          jle L_42d30a
          xor EAX,EAX
          cmp DWORD PTR [L_4bc150+4],17
          mov EDX,OFFSET L_4bc580
          jne L_42dd45
          jmp L_42d30a
L_42dd32:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],17
          je L_42d8b0
L_42dd45:
          add EAX,1
          cmp EAX,ECX
          jne L_42dd32
          jmp L_42d30a
L_42dd51:
          mov EAX,DWORD PTR [EBX-8]
          mov EBP,DWORD PTR [L_479ebc]
          add EAX,2
          mov DWORD PTR [ESP],EAX
          call _getBeU16
          movzx EDI,AX
          mov EAX,DWORD PTR [EBX-8]
          add EAX,944
          mov DWORD PTR [ESP],EAX
          call _getBeU32
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+4],EDI
          call _showExpectedFuses
          mov DWORD PTR [ESP+16],1
          mov EAX,DWORD PTR [EBX-4]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [EBX-8]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+96]
          mov DWORD PTR [ESP],EAX
          call _cbaEncrypt2
          jmp L_42d050
L_42ddbb:
          mov ECX,DWORD PTR [L_4c4f98]
          test ECX,ECX
          jle L_42d1d0
          xor EAX,EAX
          cmp DWORD PTR [L_4bc150+4],9
          mov EDX,OFFSET L_4bc580
          jne L_42ddf3
          jmp L_42d1d0
          .byte 0x66
          .byte 0x90
L_42dde0:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],9
          je L_42d890
L_42ddf3:
          add EAX,1
          cmp ECX,EAX
          jne L_42dde0
          jmp L_42d1d0
L_42ddff:
          mov EDX,DWORD PTR [L_4c4f98]
          test EDX,EDX
          jle L_42d235
          xor EBP,EBP
          cmp DWORD PTR [L_4bc150+4],10
          mov EAX,OFFSET L_4bc580
          jne L_42de34
          jmp L_42d235
L_42de22:
          add EAX,1068
          cmp DWORD PTR [EAX-1068],10
          je L_42d237
L_42de34:
          add EBP,1
          cmp EBP,EDX
          jne L_42de22
          jmp L_42d235
L_42de40:
          mov ECX,DWORD PTR [L_4c4f98]
          test ECX,ECX
          jle L_42d30a
          xor EAX,EAX
          cmp DWORD PTR [L_4bc150+4],5
          mov EDX,OFFSET L_4bc580
          jne L_42de76
          jmp L_42d30a
L_42de63:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],5
          je L_42d8b0
L_42de76:
          add EAX,1
          cmp EAX,ECX
          jne L_42de63
          jmp L_42d30a
L_42de82:
          imul EAX,EAX,1068
          add EAX,271044
          jmp L_42d6af
L_42de92:
          imul ESI,EAX,1068
          lea EDI,DWORD PTR [ESI+270000]
          add ESI,271044
          jmp L_42d0c6
L_42dea9:
          imul EDX,EDX,1068
          lea EBX,DWORD PTR [EDX+271044]
          jmp L_42d0f3
L_42deba:
          mov EAX,DWORD PTR [EBX-8]
          mov EBP,DWORD PTR [L_479ebc]
          add EAX,2
          mov DWORD PTR [ESP],EAX
          call _getBeU16
          mov ECX,DWORD PTR [EBX-8]
          mov WORD PTR [ESP+40],AX
          lea EAX,DWORD PTR [ECX+944]
          mov DWORD PTR [ESP],EAX
          call _getBeU32
          mov DWORD PTR [ESP+12],EBP
          movzx EBP,WORD PTR [ESP+40]
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],EBP
          call _showExpectedFuses
          test EDI,EDI
          je L_42d7a5
L_42df09:
          mov DWORD PTR [ESP+4],OFFSET L_45a924
          mov DWORD PTR [ESP],1
          call _log_printf
          mov BYTE PTR [L_479f15],0
          jmp L_42d7a5
L_42df29:
          add EAX,2
          mov DWORD PTR [ESP],EAX
          call _getBeU16
          movzx EAX,AX
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],16777216
          call _showExpectedFuses
          jmp L_42da7b
L_42df58:
          imul EDX,EAX,1068
          add EDX,271044
          jmp L_42d7e2
L_42df69:
          mov EAX,DWORD PTR [EBX-4]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],EAX
          call _patchFreeboot
          jmp L_42d050
L_42df7d:
          mov EAX,EDX
          jmp L_42db0a
L_42df84:
          mov ESI,271044
          mov EDI,270000
          xor EAX,EAX
          jmp L_42d0cb
L_42df95:
          mov EBX,271044
          mov ESI,271044
          mov EDI,270000
          xor EAX,EAX
          jmp L_42d0f3
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
#@C _encodeUpdateBls
_calcBlAreaSize:
          push EDI
          push ESI
          push EBX
          sub ESP,16
          mov ECX,DWORD PTR [_g479ea8]
          cmp ECX,2
          je L_42e465
          cmp ECX,5
          jbe L_42e2e0
          mov EAX,DWORD PTR [L_4c4f98]
          test EAX,EAX
          jle L_42e577
          xor EDX,EDX
          cmp DWORD PTR [L_4bc150+4],11
          mov ECX,OFFSET L_4bc580
          jne L_42e1af
          jmp L_42e6ca
L_42e1a0:
          add ECX,1068
          cmp DWORD PTR [ECX-1068],11
          je L_42e1b8
L_42e1af:
          add EDX,1
          cmp EDX,EAX
          jne L_42e1a0
          xor EDX,EDX
L_42e1b8:
          mov ESI,DWORD PTR [L_4c4f9c]
          test ESI,ESI
          jle L_42e6dc
L_42e1c6:
          mov EBX,OFFSET L_4bc580
          xor ECX,ECX
          jmp L_42e1e3
          .byte 0x90
L_42e1d0:
          add EBX,1068
          cmp DWORD PTR [EBX-1068],11
          je L_42e5a0
L_42e1e3:
          add ECX,1
          cmp ECX,ESI
          jl L_42e1d0
          xor ESI,ESI
L_42e1ec:
          imul EDX,EDX,1068
          mov EBX,DWORD PTR [L_4bc150+16]
          add ESI,DWORD PTR [EDX+L_4bc150+16]
          test EAX,EAX
          jle L_42e6ac
L_42e206:
          mov ECX,DWORD PTR [L_4bc150+4]
          xor EDX,EDX
          mov EBX,OFFSET L_4bc580
          cmp ECX,12
          jne L_42e22f
          jmp L_42e6ed
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_42e220:
          add EBX,1068
          cmp DWORD PTR [EBX-1068],12
          je L_42e238
L_42e22f:
          add EDX,1
          cmp EDX,EAX
          jne L_42e220
          xor EDX,EDX
L_42e238:
          imul EDX,EDX,1068
          add ESI,DWORD PTR [EDX+L_4bc150+16]
          cmp ECX,13
          je L_42e6bd
L_42e24d:
          mov EBX,OFFSET L_4bc580
          xor EDX,EDX
          jmp L_42e26f
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_42e260:
          add EBX,1068
          cmp DWORD PTR [EBX-1068],13
          je L_42e278
L_42e26f:
          add EDX,1
          cmp EDX,EAX
          jne L_42e260
          xor EDX,EDX
L_42e278:
          imul EDX,EDX,1068
          add ESI,DWORD PTR [EDX+L_4bc150+16]
          cmp ECX,14
          mov EBX,ESI
          je L_42e2ae
L_42e28b:
          mov ECX,OFFSET L_4bc580
          xor EDX,EDX
          jmp L_42e2a7
L_42e294:
          add ECX,1068
          cmp DWORD PTR [ECX-1068],14
          je L_42e631
L_42e2a7:
          add EDX,1
          cmp EDX,EAX
          jne L_42e294
L_42e2ae:
          mov EAX,DWORD PTR [L_4bc150+16]
L_42e2b3:
          add EBX,EAX
          mov DWORD PTR [ESP],EBX
          call _setPatchSlot
          call _imgCfSize
          lea EAX,DWORD PTR [EBX+EAX*2]
L_42e2c5:
          lea EDX,DWORD PTR [EAX+16383]
          and EDX,4294950912
          test EAX,16383
          cmovne EAX,EDX
          add ESP,16
          pop EBX
          pop ESI
          pop EDI
          ret 
L_42e2e0:
          mov EAX,DWORD PTR [L_4c4f9c]
          test EAX,EAX
          jle L_42e6b6
          mov EBX,DWORD PTR [L_4bc150+4]
          xor EDX,EDX
          mov ESI,OFFSET L_4bc580
          cmp EBX,5
          jne L_42e317
          jmp L_42e5f4
L_42e304:
          add ESI,1068
          cmp DWORD PTR [ESI-1068],5
          je L_42e600
L_42e317:
          add EDX,1
          cmp EDX,EAX
          jne L_42e304
          xor EDI,EDI
L_42e320:
          mov ESI,OFFSET L_4bc580
          xor EDX,EDX
          jmp L_42e343
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42e330:
          add ESI,1068
          cmp DWORD PTR [ESI-1068],5
          je L_42e620
L_42e343:
          add EDX,1
          cmp EDX,EAX
          jne L_42e330
          xor ESI,ESI
L_42e34c:
          add EDI,ESI
          xor EDX,EDX
          cmp EBX,6
          mov ESI,OFFSET L_4bc580
          jne L_42e373
          jmp L_42e5c4
          .byte 0x90
L_42e360:
          add ESI,1068
          cmp DWORD PTR [ESI-1068],6
          je L_42e5d0
L_42e373:
          add EDX,1
          cmp EDX,EAX
          jne L_42e360
          xor ESI,ESI
L_42e37c:
          add EDI,ESI
          xor EDX,EDX
          cmp EBX,7
          mov ESI,OFFSET L_4bc580
          jne L_42e3a3
          jmp L_42e5e1
          .byte 0x90
L_42e390:
          add ESI,1068
          cmp DWORD PTR [ESI-1068],7
          je L_42e5e3
L_42e3a3:
          add EDX,1
          cmp EDX,EAX
          jne L_42e390
          xor ESI,ESI
L_42e3ac:
          add ESI,EDI
          cmp EBX,8
          je L_42e5b1
          mov EBX,OFFSET L_4bc580
          xor EDX,EDX
          jmp L_42e3d3
L_42e3c0:
          add EBX,1068
          cmp DWORD PTR [EBX-1068],8
          je L_42e5b3
L_42e3d3:
          add EDX,1
          cmp EDX,EAX
          jne L_42e3c0
L_42e3da:
          cmp ECX,1
          je L_42e447
          mov ECX,DWORD PTR [L_4c4f98]
          test ECX,ECX
          jle L_42e416
          xor EAX,EAX
          cmp DWORD PTR [L_4bc150+4],25
          mov EDX,OFFSET L_4bc580
          jne L_42e40f
          jmp L_42e416
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_42e400:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],25
          je L_42e418
L_42e40f:
          add EAX,1
          cmp EAX,ECX
          jne L_42e400
L_42e416:
          xor EAX,EAX
L_42e418:
          imul EBX,EAX,1068
          mov EAX,DWORD PTR [EBX+L_4bc150+8]
          add EBX,OFFSET _xb
          cmp EAX,ESI
          jbe L_42e447
          mov ESI,DWORD PTR [EBX+271040]
          cmp ESI,262144
          ja L_42e685
          mov ESI,262144
L_42e445:
          add ESI,EAX
L_42e447:
          add ESI,65535
          xor SI,SI
          mov DWORD PTR [ESP],ESI
          call _setPatchSlot
          call _imgCfSize
          lea EAX,DWORD PTR [ESI+EAX*2]
          jmp L_42e2c5
L_42e465:
          mov ECX,DWORD PTR [L_4c4f98]
          test ECX,ECX
          jle L_42e642
          xor EAX,EAX
          cmp DWORD PTR [L_4bc150+4],5
          mov EDX,OFFSET L_4bc580
          jne L_42e49f
          jmp L_42e717
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42e490:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],5
          je L_42e4a8
L_42e49f:
          add EAX,1
          cmp EAX,ECX
          jne L_42e490
          xor EAX,EAX
L_42e4a8:
          mov ESI,DWORD PTR [L_4c4f9c]
          test ESI,ESI
          jle L_42e729
L_42e4b6:
          mov EBX,OFFSET L_4bc580
          xor EDX,EDX
          jmp L_42e4d3
          .byte 0x90
L_42e4c0:
          add EBX,1068
          cmp DWORD PTR [EBX-1068],5
          je L_42e661
L_42e4d3:
          add EDX,1
          cmp EDX,ESI
          jl L_42e4c0
          xor EDX,EDX
L_42e4dc:
          imul EAX,EAX,1068
          mov EBX,DWORD PTR [L_4bc150+16]
          add EDX,DWORD PTR [EAX+L_4bc150+16]
          test ECX,ECX
          mov EAX,EDX
          jle L_42e700
L_42e4f8:
          mov ESI,DWORD PTR [L_4bc150+4]
          xor EDX,EDX
          mov EBX,OFFSET L_4bc580
          cmp ESI,7
          jne L_42e51f
          jmp L_42e73a
          .byte 0x90
L_42e510:
          add EBX,1068
          cmp DWORD PTR [EBX-1068],7
          je L_42e528
L_42e51f:
          add EDX,1
          cmp EDX,ECX
          jne L_42e510
          xor EDX,EDX
L_42e528:
          imul EDX,EDX,1068
          mov EDI,DWORD PTR [L_479ebc]
          add EAX,DWORD PTR [EDX+L_4bc150+16]
          test EDI,EDI
          je L_42e2c5
          cmp ESI,14
          je L_42e56a
L_42e547:
          mov EBX,OFFSET L_4bc580
          xor EDX,EDX
          jmp L_42e563
L_42e550:
          add EBX,1068
          cmp DWORD PTR [EBX-1068],14
          je L_42e672
L_42e563:
          add EDX,1
          cmp EDX,ECX
          jne L_42e550
L_42e56a:
          mov EBX,DWORD PTR [L_4bc150+16]
          add EAX,EBX
          jmp L_42e2c5
L_42e577:
          mov ESI,DWORD PTR [L_4c4f9c]
          test ESI,ESI
          jle L_42e6a4
          xor EDX,EDX
          cmp DWORD PTR [L_4bc150+4],11
          jne L_42e1c6
          xor ECX,ECX
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_42e5a0:
          imul ECX,ECX,1068
          mov ESI,DWORD PTR [ECX+L_4bc150+8]
          jmp L_42e1ec
L_42e5b1:
          xor EDX,EDX
L_42e5b3:
          imul EDX,EDX,1068
          add ESI,DWORD PTR [EDX+L_4bc150+16]
          jmp L_42e3da
L_42e5c4:
          xor EDX,EDX
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_42e5d0:
          imul EDX,EDX,1068
          mov ESI,DWORD PTR [EDX+L_4bc150+16]
          jmp L_42e37c
L_42e5e1:
          xor EDX,EDX
L_42e5e3:
          imul EDX,EDX,1068
          mov ESI,DWORD PTR [EDX+L_4bc150+16]
          jmp L_42e3ac
L_42e5f4:
          xor EDX,EDX
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_42e600:
          imul EDX,EDX,1068
          cmp EBX,5
          mov EDI,DWORD PTR [EDX+L_4bc150+8]
          jne L_42e320
          xor EDX,EDX
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_42e620:
          imul EDX,EDX,1068
          mov ESI,DWORD PTR [EDX+L_4bc150+16]
          jmp L_42e34c
L_42e631:
          imul EDX,EDX,1068
          mov EAX,DWORD PTR [EDX+L_4bc150+16]
          jmp L_42e2b3
L_42e642:
          mov ESI,DWORD PTR [L_4c4f9c]
          test ESI,ESI
          jle L_42e6f8
          xor EAX,EAX
          cmp DWORD PTR [L_4bc150+4],5
          jne L_42e4b6
          xor EDX,EDX
L_42e661:
          imul EDX,EDX,1068
          mov EDX,DWORD PTR [EDX+L_4bc150+8]
          jmp L_42e4dc
L_42e672:
          imul EDX,EDX,1068
          mov EBX,DWORD PTR [EDX+L_4bc150+16]
          add EAX,EBX
          jmp L_42e2c5
L_42e685:
          mov DWORD PTR [ESP+4],OFFSET L_45aa58
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [EBX+271032]
          jmp L_42e445
L_42e6a4:
          mov EBX,DWORD PTR [L_4bc150+16]
          mov ESI,EBX
L_42e6ac:
          mov EAX,EBX
          lea EBX,DWORD PTR [ESI+EBX*2]
          jmp L_42e2b3
L_42e6b6:
          xor ESI,ESI
          jmp L_42e3da
L_42e6bd:
          add ESI,DWORD PTR [L_4bc150+16]
          mov EBX,ESI
          jmp L_42e28b
L_42e6ca:
          mov EBX,DWORD PTR [L_4c4f9c]
          xor EDX,EDX
          xor ECX,ECX
          test EBX,EBX
          jg L_42e5a0
L_42e6dc:
          imul EDX,EDX,1068
          mov ESI,DWORD PTR [EDX+L_4bc150+16]
          jmp L_42e206
L_42e6ed:
          add ESI,DWORD PTR [L_4bc150+16]
          jmp L_42e24d
L_42e6f8:
          mov EBX,DWORD PTR [L_4bc150+16]
          mov EAX,EBX
L_42e700:
          mov EDX,DWORD PTR [L_479ebc]
          add EAX,EBX
          test EDX,EDX
          je L_42e2c5
          add EAX,EBX
          jmp L_42e2c5
L_42e717:
          mov EBX,DWORD PTR [L_4c4f9c]
          xor EAX,EAX
          xor EDX,EDX
          test EBX,EBX
          jg L_42e661
L_42e729:
          imul EAX,EAX,1068
          mov EAX,DWORD PTR [EAX+L_4bc150+16]
          jmp L_42e4f8
L_42e73a:
          mov EDX,DWORD PTR [L_479ebc]
          add EAX,DWORD PTR [L_4bc150+16]
          test EDX,EDX
          jne L_42e547
          jmp L_42e2c5
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
_buildFlash:
          push EBP
          push EDI
          push ESI
          push EBX
          mov EBX,1
          sub ESP,1180
          mov EAX,DWORD PTR [_g479ea8]
          mov DWORD PTR [ESP+84],0
          mov DWORD PTR [ESP+88],0
          mov DWORD PTR [ESP+92],0
          mov DWORD PTR [ESP+96],0
          cmp EAX,2
          je L_42e7b4
          mov EDX,DWORD PTR [L_479eb4]
          xor EBX,EBX
          test EDX,EDX
          setne BL
          sub EAX,4
          cmp EAX,1
          mov EAX,1
          cmovbe EBX,EAX
L_42e7b4:
          mov EAX,DWORD PTR [L_47a088]
          test EAX,EAX
          jne L_42ec40
          mov DWORD PTR [ESP+4],OFFSET L_45aa94
          mov DWORD PTR [ESP],1
          call _log_printf
          call _writeInitialHeader
L_42e7da:
          mov DWORD PTR [ESP],OFFSET L_47b14c
          call _suLoadDir
          mov DWORD PTR [ESP+4],OFFSET L_45ab50
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [L_47a088]
          test EAX,EAX
          jne L_42ec90
          call _loadBlFiles
          mov DWORD PTR [ESP+40],EAX
          mov EAX,DWORD PTR [ESP+40]
          test EAX,EAX
          jne L_42eca5
L_42e81c:
          mov EAX,DWORD PTR [L_47a088]
          test EAX,EAX
          jne L_42e832
          call _verifyBlSigs
          test EAX,EAX
          je L_42fb05
L_42e832:
          mov DWORD PTR [ESP+4],OFFSET L_45abd8
          mov DWORD PTR [ESP],1
          call _log_printf
          call _fsStartBlock
          mov ESI,EAX
          call _calcBlAreaSize
          test ESI,ESI
          mov DWORD PTR [ESP+32],EAX
          jne L_42f9c0
          mov ESI,EAX
          shr ESI,14
L_42e863:
          mov EAX,DWORD PTR [_g479ea8]
          cmp EAX,3
          je L_42fecc
          sub EAX,4
          cmp EAX,1
          jbe L_42fae4
L_42e87d:
          mov EBP,DWORD PTR [L_47a088]
          test EBP,EBP
          jne L_42e8b0
          mov EAX,DWORD PTR [_g479ea8]
          cmp EAX,1
          je L_42e8b0
          cmp EAX,5
          ja L_42e8b0
          mov DWORD PTR [ESP+4],OFFSET L_45ac14
          mov DWORD PTR [ESP],1
          call _log_printf
          call _patchHeaderOpts
          nop
L_42e8b0:
          mov DWORD PTR [ESP+4],OFFSET L_45ac58
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [L_479ec0]
          mov DWORD PTR [ESP],EAX
          call _keysInit
          test EBX,EBX
          je L_42e940
          mov ECX,DWORD PTR [L_4c4f98]
          test ECX,ECX
          jle L_42e907
          xor EAX,EAX
          cmp DWORD PTR [L_4bc150+4],24
          mov EDX,OFFSET L_4bc580
          jne L_42e900
          jmp L_42e907
L_42e8f1:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],24
          je L_42e909
L_42e900:
          add EAX,1
          cmp EAX,ECX
          jne L_42e8f1
L_42e907:
          xor EAX,EAX
L_42e909:
          imul EAX,EAX,1068
          lea EBP,DWORD PTR [EAX+_xb]
          mov EAX,DWORD PTR [EAX+L_4bc150+12]
          mov DWORD PTR [ESP],EAX
          call _setFuseCpuKey
          cmp DWORD PTR [_g479ea8],2
          je L_42e940
          call _imgCfOffset
          mov EDI,EAX
          call _imgCfSize
          add EDI,EAX
          mov DWORD PTR [EBP+271032],EDI
L_42e940:
          mov EDI,DWORD PTR [L_47a088]
          lea EAX,DWORD PTR [ESP+84]
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EAX
          test EDI,EDI
          jne L_42f9d0
          call _encodeBls
          test EAX,EAX
          jne L_42f9dd
L_42e966:
          test EBX,EBX
          je L_42e9cc
          mov ECX,DWORD PTR [L_4c4f98]
          test ECX,ECX
          jle L_42e9a6
          xor EAX,EAX
          cmp DWORD PTR [L_4bc150+4],24
          mov EDX,OFFSET L_4bc580
          jne L_42e99f
          jmp L_42e9a6
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_42e990:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],24
          je L_42e9a8
L_42e99f:
          add EAX,1
          cmp ECX,EAX
          jne L_42e990
L_42e9a6:
          xor EAX,EAX
L_42e9a8:
          imul EAX,EAX,1068
          mov DWORD PTR [ESP+4],OFFSET L_45ac8e
          mov DWORD PTR [ESP],1
          mov EAX,DWORD PTR [EAX+L_4bc150+12]
          mov DWORD PTR [ESP+8],EAX
          call _showFuses
L_42e9cc:
          mov DWORD PTR [ESP+4],OFFSET L_45aca8
          mov DWORD PTR [ESP],1
          call _log_printf
          mov ESI,DWORD PTR [L_47a088]
          test ESI,ESI
          jne L_42f9f0
          call _addBlsToImage
          call _fsStartBlock
          test EAX,EAX
          je L_42fa02
L_42ea00:
          call _fsStartBlock
          test EAX,EAX
          jne L_42fa4b
L_42ea0d:
          cmp DWORD PTR [_g479ea8],2
          je L_42ff3e
          mov ECX,DWORD PTR [L_4c4f98]
          test ECX,ECX
          jle L_42ea56
          xor EAX,EAX
          cmp DWORD PTR [L_4bc150+4],9
          mov EDX,OFFSET L_4bc580
          jne L_42ea4f
          jmp L_42ea56
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_42ea40:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],9
          je L_42ea58
L_42ea4f:
          add EAX,1
          cmp EAX,ECX
          jne L_42ea40
L_42ea56:
          xor EAX,EAX
L_42ea58:
          imul EAX,EAX,1068
          lea EBP,DWORD PTR [ESP+100]
          mov EBX,DWORD PTR [EAX+L_4bc174]
          test EBX,EBX
          jne L_42fc73
L_42ea70:
          mov EAX,DWORD PTR [L_4bbd4c]
          mov DWORD PTR [ESP+4],OFFSET L_45ae04
          xor EBX,EBX
          mov DWORD PTR [ESP],1
          mov ESI,OFFSET L_47b94c
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov EAX,DWORD PTR [L_4bbd4c]
          test EAX,EAX
          jne L_42eade
          jmp L_42ef10
L_42eaa2:
          mov EDX,DWORD PTR [EBX*4+L_4bb94c]
          test EDX,EDX
          jne L_42fc30
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_45aef8
          mov DWORD PTR [ESP],1
          call _log_printf
L_42eac9:
          add EBX,1
          add ESI,1024
          cmp DWORD PTR [L_4bbd4c],EBX
          jbe L_42ef10
L_42eade:
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EBP
          call _strcpy
          mov EDX,EBP
L_42eaec:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_42eaec
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          sbb EDX,3
          sub EDX,EBP
          movzx EDI,BYTE PTR [ESP+EDX*1+99]
          mov DWORD PTR [ESP+8],14
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],OFFSET L_45ae59
          call _strnicmp
          test EAX,EAX
          je L_42ecd0
          mov EAX,DWORD PTR [EBX*4+L_4bb94c]
          test EAX,EAX
          je L_42ecf0
          mov ECX,EDI
          cmp CL,112
          je L_42ed20
          lea EDI,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+28],1
          mov DWORD PTR [ESP+24],1
          mov DWORD PTR [ESP+20],1
          mov DWORD PTR [ESP+16],EDI
L_42eb7d:
          mov DWORD PTR [ESP+12],EAX
L_42eb81:
          imul EAX,DWORD PTR [L_4c4f9c],1068
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP],EBP
          add EAX,OFFSET L_4bbd50
          mov DWORD PTR [ESP+4],EAX
          call _loadInputFile
          test EAX,EAX
          jne L_42eaa2
L_42ebac:
          mov DWORD PTR [ESP+4],47
          mov DWORD PTR [ESP],ESI
          call _strrchr
          test EAX,EAX
          je L_42eef0
L_42ebc4:
          lea EDI,DWORD PTR [EAX+1]
L_42ebc7:
          call _imgSize
          imul EDX,DWORD PTR [L_4c4f9c],1068
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET L_45aebc
          mov DWORD PTR [ESP],1
          mov EDX,DWORD PTR [EDX+L_4bc150+16]
          lea ECX,DWORD PTR [EAX+EDX*1]
          mov DWORD PTR [ESP+16],EDX
          mov DWORD PTR [ESP+32],EDX
          mov DWORD PTR [ESP+20],ECX
          call _log_printf
          lea EAX,DWORD PTR [ESP+64]
          mov EDX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+8],EAX
          imul EAX,DWORD PTR [L_4c4f9c],1068
          mov DWORD PTR [ESP+12],EDX
          mov EAX,DWORD PTR [EAX+L_4bc150+12]
          mov DWORD PTR [ESP+4],EAX
          call _imgAddFile
          jmp L_42eac9
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42ec40:
          mov DWORD PTR [ESP+4],OFFSET L_45aabc
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP],1
          call _checkBootImage
          test EAX,EAX
          mov DWORD PTR [ESP+40],EAX
          je L_42e7da
          mov DWORD PTR [ESP+4],OFFSET L_45aaf8
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [ESP+40]
          add ESP,1180
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x90
L_42ec90:
          call _loadConsoleBlFiles
          mov DWORD PTR [ESP+40],EAX
          mov EAX,DWORD PTR [ESP+40]
          test EAX,EAX
          je L_42e81c
L_42eca5:
          mov DWORD PTR [ESP+4],OFFSET L_45ab90
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [ESP+40]
          add ESP,1180
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
L_42ecd0:
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_45ae68
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_42eac9
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_42ecf0:
          lea EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],1
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+16],EAX
          jmp L_42eb81
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_42ed20:
          cmp DWORD PTR [_g479ea8],2
          mov EDX,ESI
          je L_42eeb2
L_42ed2f:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_42ed2f
          mov ECX,EAX
          mov EDI,49
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          sbb EDX,3
          mov WORD PTR [EDX],DI
L_42ed67:
          lea EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+28],1
          mov DWORD PTR [ESP+24],1
          mov DWORD PTR [ESP+20],1
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+16],EAX
          mov EAX,DWORD PTR [EBX*4+L_4bb94c]
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+12],EAX
          imul EAX,DWORD PTR [L_4c4f9c],1068
          add EAX,OFFSET L_4bbd50
          mov DWORD PTR [ESP+4],EAX
          call _loadInputFile
          test EAX,EAX
          je L_42ebac
          mov EDX,EBP
L_42edbf:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_42edbf
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          lea EAX,DWORD PTR [ESP+64]
          mov ECX,49
          sbb EDX,3
          mov WORD PTR [EDX],CX
          mov DWORD PTR [ESP+16],EAX
          mov EAX,DWORD PTR [EBX*4+L_4bb94c]
          mov DWORD PTR [ESP+28],1
          mov DWORD PTR [ESP+24],1
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+12],EAX
          imul EAX,DWORD PTR [L_4c4f9c],1068
          add EAX,OFFSET L_4bbd50
          mov DWORD PTR [ESP+4],EAX
          call _loadInputFile
          test EAX,EAX
          je L_42ebac
          mov EDX,EBP
L_42ee4f:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_42ee4f
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          lea EAX,DWORD PTR [ESP+64]
          sbb EDX,3
          sub EDX,EBP
          mov BYTE PTR [ESP+EDX*1+99],50
          mov DWORD PTR [ESP+16],EAX
          mov DWORD PTR [ESP+28],1
          mov DWORD PTR [ESP+24],1
          mov DWORD PTR [ESP+20],0
          mov EAX,DWORD PTR [EBX*4+L_4bb94c]
          jmp L_42eb7d
L_42eeb2:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_42eeb2
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          mov EAX,50
          sbb EDX,3
          mov WORD PTR [EDX],AX
          jmp L_42ed67
          .byte 0x90
L_42eef0:
          mov DWORD PTR [ESP+4],92
          mov DWORD PTR [ESP],ESI
          call _strrchr
          test EAX,EAX
          jne L_42ebc4
          mov EDI,ESI
          jmp L_42ebc7
          .byte 0x90
L_42ef10:
          mov EAX,DWORD PTR [_buildMode]
          mov DWORD PTR [ESP+4],OFFSET L_45ae30
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov EAX,DWORD PTR [_buildMode]
          test EAX,EAX
          je L_42f299
          imul EDX,DWORD PTR [L_4c4f9c],1068
          xor EAX,EAX
          mov ECX,267
          mov EBX,OFFSET _flashFiles
          add EDX,OFFSET L_4bbd50
          mov EDI,EDX
          rep stosd DWORD PTR ES:[EDI]
          lea EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP+32],EAX
          call _setBeU32
          xor EAX,EAX
          mov DWORD PTR [ESP+36],EBP
          mov EBP,EAX
          .byte 0x8d,0xb6,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_42ef80:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_45afbd
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],EAX
          imul EAX,DWORD PTR [L_4c4f9c],1068
          add EAX,OFFSET L_4bbd50
          mov DWORD PTR [ESP+4],EAX
          call _loadBaseFileMeta
          test EAX,EAX
          je L_42f080
          test BYTE PTR [L_479f03],1
          jne L_42f017
          mov EAX,DWORD PTR [L_4c4f9c]
          imul EDX,EAX,1068
          mov EDX,DWORD PTR [EDX+L_4bc150+12]
          test EDX,EDX
          je L_42efee
          mov DWORD PTR [ESP],EDX
          call _free
          mov EAX,DWORD PTR [L_4c4f9c]
L_42efee:
          imul EAX,EAX,1068
          mov DWORD PTR [ESP],EBX
          lea EDX,DWORD PTR [EAX+L_4bc150+16]
          add EAX,OFFSET L_4bc150+12
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP+8],EDX
          call _suGetFile
          test EAX,EAX
          jne L_42f9a0
L_42f017:
          mov EDX,DWORD PTR [EBP*4+L_4c90c0]
          test EDX,EDX
          je L_42fb20
          mov EAX,DWORD PTR [L_4c4f9c]
          imul ECX,EAX,1068
          mov ECX,DWORD PTR [ECX+L_4bc150+12]
          test ECX,ECX
          je L_42f04f
          mov DWORD PTR [ESP],ECX
          call _free
          mov EAX,DWORD PTR [L_4c4f9c]
          mov EDX,DWORD PTR [EBP*4+L_4c90c0]
L_42f04f:
          imul EAX,EAX,1068
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_45b004
          mov DWORD PTR [ESP],1
          mov DWORD PTR [EAX+L_4bc150+12],EDX
          mov EDX,DWORD PTR [EBP*4+L_4c90e8]
          mov DWORD PTR [EAX+L_4bc150+16],EDX
          call _log_printf
L_42f080:
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EAX
          call _getBeU32
          test EAX,EAX
          jne L_42f1c0
          mov EAX,DWORD PTR [L_479ec4]
          test EAX,EAX
          je L_42f970
          mov EDI,DWORD PTR [ESP+36]
          lea ESI,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP],EDI
          call _GetSystemTime
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EDI
          call _SystemTimeToFileTime
L_42f0bd:
          lea EAX,DWORD PTR [ESP+62]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],EAX
          lea EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+4],EAX
          call _FileTimeToDosDateTime
          lea EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],EAX
          movzx EAX,WORD PTR [ESP+62]
          mov DWORD PTR [ESP+4],EAX
          movzx EAX,WORD PTR [ESP+60]
          mov DWORD PTR [ESP],EAX
          call _DosDateTimeToFileTime
          movzx ECX,WORD PTR [ESP+60]
          movzx EDI,WORD PTR [ESP+62]
          xor EAX,EAX
          mov ESI,ECX
          shr SI,8
          mov EDX,ESI
          mov ESI,EBX
          mov AL,DL
          mov BYTE PTR [ESP+44],DL
          mov EDX,EDI
          mov AH,CL
          mov ECX,EDI
          shl EDX,24
          movzx ECX,CH
          movzx EAX,AX
          mov EDI,OFFSET L_45b03b
          shl ECX,16
          or EAX,ECX
          mov ECX,12
          or EAX,EDX
          mov DWORD PTR [ESP+64],EAX
          repe cmpsb BYTE PTR [ESI],BYTE PTR ES:[EDI]
          je L_42f200
L_42f13b:
          mov EDI,OFFSET L_45b047
          mov ECX,13
          mov ESI,EBX
          repe cmpsb BYTE PTR [ESI],BYTE PTR ES:[EDI]
          je L_42fa60
          mov EDI,OFFSET L_45b054
          mov ECX,8
          mov ESI,EBX
          repe cmpsb BYTE PTR [ESI],BYTE PTR ES:[EDI]
          je L_42fab0
          mov EDI,OFFSET L_45b05c
          mov ECX,8
          mov ESI,EBX
          repe cmpsb BYTE PTR [ESI],BYTE PTR ES:[EDI]
          je L_42fe00
          mov EDI,OFFSET L_45b064
          mov ECX,9
          mov ESI,EBX
          repe cmpsb BYTE PTR [ESI],BYTE PTR ES:[EDI]
          je L_42fea0
          mov EDI,OFFSET L_45b06d
          mov ECX,8
          mov ESI,EBX
          repe cmpsb BYTE PTR [ESI],BYTE PTR ES:[EDI]
          jne L_42fa7c
          mov EAX,DWORD PTR [EBP*4+L_4c9110]
          test EAX,EAX
          je L_42f21f
          mov EDI,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],EDI
          call _setBeU32
          jmp L_42f21f
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_42f1c0:
          lea EAX,DWORD PTR [ESP+68]
          mov ESI,EBX
          mov EDI,OFFSET L_45b03b
          mov DWORD PTR [ESP+8],EAX
          movzx EAX,WORD PTR [ESP+66]
          rol AX,8
          movzx EAX,AX
          mov DWORD PTR [ESP+4],EAX
          movzx EAX,WORD PTR [ESP+64]
          rol AX,8
          movzx EAX,AX
          mov DWORD PTR [ESP],EAX
          call _DosDateTimeToFileTime
          mov ECX,12
          repe cmpsb BYTE PTR [ESI],BYTE PTR ES:[EDI]
          jne L_42f13b
L_42f200:
          lea EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+4],EAX
          imul EAX,DWORD PTR [L_4c4f9c],1068
          add EAX,OFFSET L_4bbd50
          mov DWORD PTR [ESP],EAX
          call _secdataPrepare
L_42f21f:
          imul EAX,DWORD PTR [L_4c4f9c],1068
          mov EDI,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+8],EDI
          mov EDX,DWORD PTR [EAX+L_4bc150+16]
          add EAX,OFFSET _xb
          mov DWORD PTR [ESP+12],EDX
          mov EAX,DWORD PTR [EAX+271036]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call _imgAddFileAs
L_42f252:
          mov EDI,DWORD PTR [L_4c4f9c]
          imul EAX,EDI,1068
          mov EAX,DWORD PTR [EAX+L_4bc150+12]
          test EAX,EAX
          je L_42f286
          mov DWORD PTR [ESP],EAX
          call _free
          mov EDI,DWORD PTR [L_4c4f9c]
          imul EAX,EDI,1068
          mov DWORD PTR [EAX+L_4bc150+12],0
L_42f286:
          add EBP,1
          cmp EBP,DWORD PTR [_buildMode]
          jb L_42f920
          mov EBP,DWORD PTR [ESP+36]
L_42f299:
          mov DWORD PTR [ESP+4],OFFSET L_45af94
          mov DWORD PTR [ESP],1
          mov ESI,OFFSET L_4c9186
          call _log_printf
          mov EBX,49
          xor EDI,EDI
          mov EAX,EBP
          mov DWORD PTR [ESP+36],OFFSET L_4c9184
          mov EBP,ESI
          mov ESI,EBX
          mov EBX,EDI
          mov EDI,EAX
          jmp L_42f391
L_42f2d0:
          cmp EBX,10
          jne L_42f401
          mov EAX,24948
          mov DWORD PTR [EDI],1970168141
          mov DWORD PTR [EDI+4],1952670054
          mov WORD PTR [EDI+16],AX
          mov EAX,DWORD PTR [L_479ea4]
          mov DWORD PTR [EDI+8],1852404341
          mov DWORD PTR [EDI+12],1633955431
          mov BYTE PTR [EDI+18],0
          mov DWORD PTR [ESP+16],0
          shr EAX,28
          mov DWORD PTR [ESP+12],0
          and EAX,1
          mov DWORD PTR [ESP+8],EAX
          xor EAX,EAX
          cmp DWORD PTR [_g479ea8],5
          seta AL
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [L_479ef0]
          mov DWORD PTR [ESP],EAX
          call _manufacturingOffset
          mov DWORD PTR [ESP+32],EAX
L_42f341:
          imul EDX,DWORD PTR [L_4c4f9c],1068
          mov EAX,EDI
          add EDX,OFFSET L_4bbd50
          call _loadBaseFile
          test EAX,EAX
          je L_42f450
L_42f360:
          mov EAX,DWORD PTR [EBX*8+L_47a08c]
          test EAX,EAX
          je L_42f37a
          mov EAX,DWORD PTR [EBX*8+L_47a08c+4]
          test EAX,EAX
          jne L_42f4e0
L_42f37a:
          add EBX,1
          add EBP,4
          add DWORD PTR [ESP+36],4
          add ESI,1
          cmp EBX,11
          je L_42f5e0
L_42f391:
          cmp EBX,9
          jne L_42f2d0
          mov EAX,DWORD PTR [L_479ea4]
          mov DWORD PTR [EDI],1952543827
          mov DWORD PTR [EDI+4],1769239401
          mov DWORD PTR [EDI+8],1932424035
          mov DWORD PTR [EDI+12],1769239653
          mov DWORD PTR [EDI+16],7563118
          shr EAX,28
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],0
          and EAX,1
          mov DWORD PTR [ESP+8],EAX
          xor EAX,EAX
          cmp DWORD PTR [_g479ea8],5
          seta AL
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [L_479ef0]
          mov DWORD PTR [ESP],EAX
          call _statisticsOffset
          mov DWORD PTR [ESP+32],EAX
          jmp L_42f341
L_42f401:
          imul EDX,DWORD PTR [L_4c4f9c],1068
          lea EAX,DWORD PTR [EBX+66]
          mov DWORD PTR [EDI],1768058701
          mov DWORD PTR [EDI+4],776037740
          mov DWORD PTR [EDI+8],7627108
          mov BYTE PTR [ESP+106],AL
          mov EAX,EDI
          add EDX,OFFSET L_4bbd50
          call _loadBaseFile
          test EAX,EAX
          je L_42f530
          mov DWORD PTR [ESP+32],0
          jmp L_42f360
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42f450:
          imul EAX,DWORD PTR [L_4c4f9c],1068
          mov DWORD PTR [ESP+16],ESI
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET L_45b29d
          mov DWORD PTR [ESP],1
          mov EAX,DWORD PTR [EAX+L_4bc150+16]
          mov DWORD PTR [ESP+12],EAX
          call _log_printf
          mov EAX,DWORD PTR [ESP+32]
          test EAX,EAX
          je L_42f560
          call _imgSize
          imul EDX,DWORD PTR [L_4c4f9c],1068
          mov DWORD PTR [ESP+44],EAX
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+12],EAX
          mov ECX,DWORD PTR [EDX+L_4bc150+16]
          add EDX,OFFSET _xb
          mov DWORD PTR [ESP+8],ECX
          mov EDX,DWORD PTR [EDX+271036]
L_42f4bd:
          mov DWORD PTR [ESP+4],EDX
          mov DWORD PTR [ESP],EDI
          call _imgAddRaw
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EAX
          call _imgSetSize
          jmp L_42f37a
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42f4e0:
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET L_45b2bc
          mov DWORD PTR [ESP],1
          call _log_printf
          mov ECX,DWORD PTR [ESP+32]
          test ECX,ECX
          je L_42f8b0
          call _imgSize
          mov EDX,DWORD PTR [EBX*8+L_47a08c+4]
          mov DWORD PTR [ESP+44],EAX
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+8],EDX
          mov EDX,DWORD PTR [EBX*8+L_47a08c]
          mov DWORD PTR [ESP+12],EAX
          jmp L_42f4bd
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42f530:
          imul EAX,DWORD PTR [L_4c4f9c],1068
          mov DWORD PTR [ESP+16],ESI
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET L_45b29d
          mov DWORD PTR [ESP],1
          mov EAX,DWORD PTR [EAX+L_4bc150+16]
          mov DWORD PTR [ESP+12],EAX
          call _log_printf
L_42f560:
          imul EAX,DWORD PTR [L_4c4f9c],1068
          mov DWORD PTR [ESP+8],ESI
          mov EDX,DWORD PTR [EAX+L_4bc150+16]
          add EAX,OFFSET _xb
          mov DWORD PTR [ESP+4],EDX
          mov EAX,DWORD PTR [EAX+271036]
          mov DWORD PTR [ESP],EAX
          call _imgAddMobile
          test AX,AX
          je L_42f37a
          cmp EBX,8
          ja L_42f37a
          mov ECX,DWORD PTR [ESP+36]
          movzx EAX,AX
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],ECX
          call _setBeU16
          imul EAX,DWORD PTR [L_4c4f9c],1068
          mov ECX,0
          mov DWORD PTR [ESP+4],EBP
          mov EAX,DWORD PTR [EAX+L_4bc150+16]
          cmp EAX,16384
          cmovae EAX,ECX
          mov DWORD PTR [ESP],EAX
          call _setBeU16
          jmp L_42f37a
          .byte 0x66
          .byte 0x90
L_42f5e0:
          call _imgSizeAligned
          mov ESI,EAX
          mov EBP,EDI
          call _imgSizeAligned
          mov DWORD PTR [ESP+4],OFFSET L_45b2e4
          mov DWORD PTR [ESP],1
          mov EBX,EAX
          call _log_printf
          mov ECX,DWORD PTR [L_4c4f98]
          test ECX,ECX
          jle L_42f63a
          xor EAX,EAX
          cmp DWORD PTR [L_4bc150+4],27
          mov EDX,OFFSET L_4bc580
          jne L_42f633
          jmp L_42f63a
L_42f620:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],27
          je L_42faa1
L_42f633:
          add EAX,1
          cmp EAX,ECX
          jne L_42f620
L_42f63a:
          imul EAX,DWORD PTR [ESP+40],1068
          mov EDX,DWORD PTR [EAX+L_4bc150+16]
          add EAX,OFFSET _xb
          mov DWORD PTR [ESP+4],EDX
          mov EAX,DWORD PTR [EAX+271036]
          mov DWORD PTR [ESP],EAX
          call _addSmcConfig
          mov DWORD PTR [ESP+4],OFFSET L_45b30c
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_45b330
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP],ESI
          call _fixupEmptyFsBlocks
          mov DWORD PTR [ESP+4],OFFSET L_45b354
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP],EBX
          call _writeFsTable
          mov DWORD PTR [ESP+4],OFFSET L_45abd8
          mov DWORD PTR [ESP],1
          call _log_printf
          test BYTE PTR [L_479ea7],16
          jne L_42fe34
L_42f6cc:
          mov EBX,OFFSET L_4bc150+16
          mov ESI,OFFSET L_4c10a4
          jmp L_42f6f0
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42f6e0:
          mov DWORD PTR [EBX],0
          add EBX,1068
          cmp ESI,EBX
          je L_42f719
L_42f6f0:
          mov EAX,DWORD PTR [EBX-4]
          test EAX,EAX
          je L_42f6e0
          mov EDX,DWORD PTR [EBX]
          test EDX,EDX
          je L_42f6e0
          mov DWORD PTR [ESP],EAX
          add EBX,1068
          call _free
          mov DWORD PTR [EBX-1068],0
          cmp ESI,EBX
          jne L_42f6f0
L_42f719:
          mov EAX,DWORD PTR [L_4c8fe0]
          test EAX,EAX
          je L_42f885
          mov DWORD PTR [ESP+4],OFFSET L_45b378
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [L_4c8fe0]
          mov DWORD PTR [ESP+1136],0
          test EAX,EAX
          je L_42f871
          lea EAX,DWORD PTR [ESP+64]
          mov EBX,OFFSET L_4c4fa0
          xor ESI,ESI
          mov DWORD PTR [ESP+36],EBP
          mov DWORD PTR [ESP+32],EAX
          jmp L_42f807
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42f770:
          mov EDI,DWORD PTR [EBX+1024]
          mov EAX,DWORD PTR [ESP+1140]
          mov EDX,DWORD PTR [L_479edc]
          lea EBP,DWORD PTR [EDI+EAX*1]
          cmp EBP,EDX
          ja L_43017f
          mov EDX,DWORD PTR [L_479ed8]
          mov DWORD PTR [ESP+8],EAX
          add ESI,1
          mov EAX,DWORD PTR [ESP+1136]
          add EDX,EDI
          mov DWORD PTR [ESP],EDX
          mov DWORD PTR [ESP+4],EAX
          call _memcpy
          mov EAX,DWORD PTR [ESP+1140]
          mov DWORD PTR [ESP+12],EBX
          add EBX,1028
          mov DWORD PTR [ESP+24],EBP
          mov DWORD PTR [ESP+16],EDI
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_45b3a0
          mov DWORD PTR [ESP+20],EAX
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [ESP+1136]
          mov DWORD PTR [ESP],EAX
          call _free
          cmp DWORD PTR [L_4c8fe0],ESI
          mov DWORD PTR [ESP+1136],0
          jbe L_42f871
L_42f807:
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+16],EAX
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call _loadInputFile
          test EAX,EAX
          je L_42f770
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_45b44c
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+40],EAX
          call _log_printf
          mov EAX,DWORD PTR [ESP+40]
          jmp L_42f8a2
L_42f871:
          mov DWORD PTR [ESP+4],OFFSET L_45abd8
          mov DWORD PTR [ESP],1
          call _log_printf
L_42f885:
          mov DWORD PTR [ESP+4],OFFSET L_45b480
          mov DWORD PTR [ESP],1
          call _log_printf
          call _finalizeImage
          mov DWORD PTR [ESP+40],EAX
L_42f8a2:
          add ESP,1180
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_42f8b0:
          mov EAX,DWORD PTR [EBX*8+L_47a08c+4]
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [EBX*8+L_47a08c]
          mov DWORD PTR [ESP],EAX
          call _imgAddMobile
          test AX,AX
          je L_42f37a
          cmp EBX,8
          ja L_42f37a
          mov ECX,DWORD PTR [ESP+36]
          movzx EAX,AX
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],ECX
          call _setBeU16
          mov EDX,DWORD PTR [EBX*8+L_47a08c+4]
          mov ECX,0
          mov DWORD PTR [ESP+4],EBP
          movzx EAX,DX
          cmp EDX,16383
          cmovg EAX,ECX
          mov DWORD PTR [ESP],EAX
          call _setBeU16
          jmp L_42f37a
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_42f920:
          imul EDI,EDI,1068
          xor EAX,EAX
          mov ECX,267
          add EBX,22
          lea EDX,DWORD PTR [EDI+L_4bbd50]
          mov EDI,EDX
          rep stosd DWORD PTR ES:[EDI]
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+4],EAX
          call _setBeU32
          mov DWORD PTR [ESP+4],OFFSET _bd_458cf9
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_42ef80
L_42f967:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_42f970:
          mov DWORD PTR [ESP+4],OFFSET _bd_458d74
          mov DWORD PTR [ESP],2
          lea ESI,DWORD PTR [ESP+76]
          call _log_printf
          mov DWORD PTR [ESP+80],30268127
          mov DWORD PTR [ESP+76],1903825408
          jmp L_42f0bd
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_42f9a0:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_45afd4
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_42f080
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_42f9c0:
          mov EAX,ESI
          shl EAX,14
          mov DWORD PTR [ESP+32],EAX
          jmp L_42e863
          .byte 0x66
          .byte 0x90
L_42f9d0:
          call _encodeUpdateBls
          test EAX,EAX
          je L_42e966
L_42f9dd:
          mov DWORD PTR [ESP+40],4294967292
          mov EAX,DWORD PTR [ESP+40]
          jmp L_42f8a2
          .byte 0x66
          .byte 0x90
L_42f9f0:
          call _addUpdateBls
          call _fsStartBlock
          test EAX,EAX
          jne L_42ea00
L_42fa02:
          mov DWORD PTR [ESP+4],OFFSET L_45ace0
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EDI,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EDI
          call _fixupFsTable
          mov DWORD PTR [ESP],EDI
          call _imgSetSize
          mov DWORD PTR [ESP+4],OFFSET L_45abd8
          mov DWORD PTR [ESP],1
          call _log_printf
          call _fsStartBlock
          test EAX,EAX
          je L_42ea0d
L_42fa4b:
          call _fsStartBlock
          shl EAX,14
          mov DWORD PTR [ESP],EAX
          call _imgSetSize
          jmp L_42ea0d
L_42fa60:
          imul EAX,DWORD PTR [L_4c4f9c],1068
          add EAX,OFFSET L_4bbd50
          mov DWORD PTR [ESP],EAX
          call _extendedPrepare
          jmp L_42f21f
L_42fa7c:
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+8],OFFSET L_47ad4c
          mov DWORD PTR [ESP+4],OFFSET L_45b078
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_42f21f
L_42faa1:
          mov DWORD PTR [ESP+40],EAX
          jmp L_42f63a
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42fab0:
          lea EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],EAX
          imul EAX,DWORD PTR [L_4c4f9c],1068
          mov EDX,DWORD PTR [EAX+L_4bc150+16]
          add EAX,OFFSET _xb
          mov DWORD PTR [ESP+4],EDX
          mov EAX,DWORD PTR [EAX+271036]
          mov DWORD PTR [ESP],EAX
          call _daeEncrypt
          jmp L_42f21f
L_42fae4:
          mov DWORD PTR [ESP+4],OFFSET L_45abe0
          mov DWORD PTR [ESP],1
          call _log_printf
          call _patchBlsResign
          test EAX,EAX
          jne L_42e87d
L_42fb05:
          mov DWORD PTR [ESP+40],1
          mov EAX,DWORD PTR [ESP+40]
          add ESP,1180
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_42fb20:
          mov ECX,12
          mov ESI,EBX
          mov EDI,OFFSET L_45b03b
          repe cmpsb BYTE PTR [ESI],BYTE PTR ES:[EDI]
          je L_42fbd0
          mov EDI,OFFSET L_45b047
          mov ECX,13
          mov ESI,EBX
          repe cmpsb BYTE PTR [ESI],BYTE PTR ES:[EDI]
          je L_42fbd0
          mov EDI,OFFSET L_45b064
          mov ECX,9
          mov ESI,EBX
          repe cmpsb BYTE PTR [ESI],BYTE PTR ES:[EDI]
          jne L_42fbf0
          call _kvGetGameRegion
          test EAX,EAX
          mov ESI,EAX
          mov DWORD PTR [ESP+8],EBX
          je L_42fc10
          mov DWORD PTR [ESP+4],OFFSET L_45b0d4
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [_g479ea8]
          cmp EAX,1
          je L_42f252
          cmp EAX,5
          ja L_42f252
          cmp ESI,1
          je L_42fe80
          mov DWORD PTR [ESP+4],OFFSET L_45b1a0
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_45b1fc
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_42f252
L_42fbd0:
          imul EAX,DWORD PTR [L_4c4f9c],1068
          mov DWORD PTR [EAX+L_4bc150+16],0
          jmp L_42f080
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42fbf0:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_45b270
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_42f252
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_42fc10:
          mov DWORD PTR [ESP+4],OFFSET L_45b238
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_42f252
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42fc30:
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_45af28
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+32],EAX
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_45af50
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+40],EAX
          add ESP,1180
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_42fc73:
          call _imgSize
          mov ECX,DWORD PTR [L_4c4f98]
          mov EDI,EAX
          test ECX,ECX
          jle L_4303ef
          mov EAX,DWORD PTR [L_4bc150+4]
          xor EBX,EBX
          mov EDX,OFFSET L_4bc580
          cmp EAX,9
          jne L_42fcaf
          jmp L_4303f8
          .byte 0x66
          .byte 0x90
L_42fca0:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],9
          je L_42fcb8
L_42fcaf:
          add EBX,1
          cmp EBX,ECX
          jne L_42fca0
          xor EBX,EBX
L_42fcb8:
          cmp EAX,10
          je L_42fce6
L_42fcbd:
          mov EDX,OFFSET L_4bc580
          xor ESI,ESI
          jmp L_42fcdf
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_42fcd0:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],10
          je L_42fce8
L_42fcdf:
          add ESI,1
          cmp ESI,ECX
          jne L_42fcd0
L_42fce6:
          xor ESI,ESI
L_42fce8:
          mov DWORD PTR [ESP+4],OFFSET L_45acf8
          mov DWORD PTR [ESP],1
          call _log_printf
          imul EAX,EBX,1068
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET L_45ad3c
          mov DWORD PTR [ESP],1
          mov EAX,DWORD PTR [EAX+L_4bc174]
          lea EDX,DWORD PTR [EDI+EAX*1]
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+16],EDX
          call _log_printf
          mov ECX,DWORD PTR [L_479ec4]
          test ECX,ECX
          je L_43014e
          lea EBP,DWORD PTR [ESP+100]
          lea EDI,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP],EBP
          call _GetSystemTime
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EBP
          call _SystemTimeToFileTime
L_42fd55:
          lea EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP],EDI
          imul ESI,ESI,1068
          mov DWORD PTR [ESP+8],EAX
          lea EAX,DWORD PTR [ESP+62]
          mov DWORD PTR [ESP+4],EAX
          call _FileTimeToDosDateTime
          movzx ECX,WORD PTR [ESP+62]
          movzx EDX,WORD PTR [ESP+68]
          xor EAX,EAX
          mov EDI,ECX
          mov WORD PTR [ESP+32],DX
          shr DI,8
          mov EDX,EDI
          lea EDI,DWORD PTR [ESP+64]
          mov BYTE PTR [ESP+36],DL
          mov AL,DL
          movzx EDX,WORD PTR [ESP+32]
          mov AH,CL
          mov DWORD PTR [ESP+8],EDI
          movzx EAX,AX
          movzx ECX,DH
          shl EDX,24
          shl ECX,16
          or EAX,ECX
          or EDX,EAX
          imul EAX,EBX,1068
          mov DWORD PTR [ESP+64],EDX
          mov EDX,DWORD PTR [EAX+L_4bc174]
          add EAX,OFFSET _xb
          mov DWORD PTR [ESP+12],EDX
          mov EAX,DWORD PTR [EAX+271064]
          add EAX,DWORD PTR [ESI+L_4bc150+12]
          mov DWORD PTR [ESP],OFFSET L_45ad6c
          mov DWORD PTR [ESP+4],EAX
          call _imgAddFile
          mov DWORD PTR [ESP+4],OFFSET L_45abd8
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_42ea70
          .byte 0x90
L_42fe00:
          lea EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],EAX
          imul EAX,DWORD PTR [L_4c4f9c],1068
          mov EDX,DWORD PTR [EAX+L_4bc150+16]
          add EAX,OFFSET _xb
          mov DWORD PTR [ESP+4],EDX
          mov EAX,DWORD PTR [EAX+271036]
          mov DWORD PTR [ESP],EAX
          call _crlEncrypt
          jmp L_42f21f
L_42fe34:
          mov DWORD PTR [ESP],OFFSET _mmcAnchor
          mov BYTE PTR [L_4c917f],1
          call _shaHeader
          mov DWORD PTR [ESP],1
          call _copyAnchorBlock
          mov DWORD PTR [ESP],OFFSET _mmcAnchor
          mov BYTE PTR [L_4c917f],2
          call _shaHeader
          mov DWORD PTR [ESP],2
          call _copyAnchorBlock
          jmp L_42f6cc
L_42fe77:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_42fe80:
          mov DWORD PTR [ESP+4],OFFSET L_45b13c
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_42f252
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_42fea0:
          imul EAX,DWORD PTR [L_4c4f9c],1068
          mov EDX,DWORD PTR [EAX+L_4bc150+16]
          add EAX,OFFSET _xb
          mov DWORD PTR [ESP+4],EDX
          mov EAX,DWORD PTR [EAX+271036]
          mov DWORD PTR [ESP],EAX
          call _fcrtEncrypt
          jmp L_42f21f
L_42fecc:
          mov DWORD PTR [ESP+4],OFFSET L_45abe0
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [L_47a088]
          test EAX,EAX
          jne L_4301ca
          lea EBP,DWORD PTR [ESP+100]
          xor EAX,EAX
          mov ECX,267
          mov EDI,EBP
          mov EDX,EBP
          rep stosd DWORD PTR ES:[EDI]
          mov EAX,OFFSET _bd_459ec8
          call _loadBaseFile
          test EAX,EAX
          jne L_430347
          mov EAX,DWORD PTR [ESP+1140]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+1136]
          mov DWORD PTR [ESP],EAX
          call _patchBlsBlmod
          mov EAX,DWORD PTR [ESP+1136]
          mov DWORD PTR [ESP],EAX
          call _free
          jmp L_42e87d
L_42ff3e:
          call _imgSize
          mov DWORD PTR [ESP+32],EAX
          mov EAX,DWORD PTR [L_4c4f98]
          test EAX,EAX
          jle L_430443
          mov EDX,DWORD PTR [L_4bc150+4]
          xor ECX,ECX
          mov EBX,OFFSET L_4bc580
          cmp EDX,20
          jne L_42ff7f
          jmp L_430414
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_42ff70:
          add EBX,1068
          cmp DWORD PTR [EBX-1068],20
          je L_42ff88
L_42ff7f:
          add ECX,1
          cmp EAX,ECX
          jne L_42ff70
          xor ECX,ECX
L_42ff88:
          imul ECX,ECX,1068
          lea EBP,DWORD PTR [ESP+100]
          mov EBX,DWORD PTR [ECX+L_4bc174]
          test EBX,EBX
          jne L_4301d4
L_42ffa0:
          cmp EDX,9
          je L_4303ff
L_42ffa9:
          mov EBX,OFFSET L_4bc580
          xor ECX,ECX
          jmp L_42ffc1
L_42ffb2:
          add EBX,1068
          cmp DWORD PTR [EBX-1068],9
          je L_42ffca
L_42ffc1:
          add ECX,1
          cmp EAX,ECX
          jne L_42ffb2
          xor ECX,ECX
L_42ffca:
          imul ECX,ECX,1068
          mov ECX,DWORD PTR [ECX+L_4bc174]
          test ECX,ECX
          je L_42ea70
          mov ECX,OFFSET L_4bc580
          xor EBX,EBX
          jmp L_42ffff
L_42ffe7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_42fff0:
          add ECX,1068
          cmp DWORD PTR [ECX-1068],9
          je L_430008
L_42ffff:
          add EBX,1
          cmp EAX,EBX
          jne L_42fff0
          xor EBX,EBX
L_430008:
          cmp EDX,10
          je L_430036
L_43000d:
          mov EDX,OFFSET L_4bc580
          xor ESI,ESI
          jmp L_43002f
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_430020:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],10
          je L_430038
L_43002f:
          add ESI,1
          cmp EAX,ESI
          jne L_430020
L_430036:
          xor ESI,ESI
L_430038:
          mov DWORD PTR [ESP+4],OFFSET L_45adb4
          mov DWORD PTR [ESP],1
          call _log_printf
          imul EAX,EBX,1068
          mov EDI,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],OFFSET L_45ad3c
          mov DWORD PTR [ESP],1
          mov EAX,DWORD PTR [EAX+L_4bc174]
          mov DWORD PTR [ESP+8],EDI
          lea EDX,DWORD PTR [EDI+EAX*1]
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+16],EDX
          call _log_printf
          mov EAX,DWORD PTR [L_479ec4]
          test EAX,EAX
          je L_430373
          lea EDI,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP],EBP
          call _GetSystemTime
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EBP
          call _SystemTimeToFileTime
L_4300a4:
          lea EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+8],EAX
          lea EAX,DWORD PTR [ESP+62]
          mov DWORD PTR [ESP+4],EAX
          call _FileTimeToDosDateTime
          movzx ECX,WORD PTR [ESP+62]
          movzx EDX,WORD PTR [ESP+68]
          xor EAX,EAX
          mov EDI,ECX
          mov WORD PTR [ESP+32],DX
          shr DI,8
          mov EDX,EDI
          lea EDI,DWORD PTR [ESP+64]
          mov BYTE PTR [ESP+36],DL
          mov AL,DL
          movzx EDX,WORD PTR [ESP+32]
          mov AH,CL
          mov DWORD PTR [ESP+8],EDI
          movzx EAX,AX
          movzx ECX,DH
          shl EDX,24
          shl ECX,16
          or EAX,ECX
          or EDX,EAX
          imul EAX,EBX,1068
          mov DWORD PTR [ESP+64],EDX
          mov EDX,DWORD PTR [EAX+L_4bc174]
          add EAX,OFFSET _xb
          mov DWORD PTR [ESP+12],EDX
          mov EAX,DWORD PTR [EAX+271064]
          imul EDX,ESI,1068
          mov DWORD PTR [ESP],OFFSET L_45adf3
          add EAX,DWORD PTR [EDX+L_4bc150+12]
          mov DWORD PTR [ESP+4],EAX
          call _imgAddFile
          mov DWORD PTR [ESP+4],OFFSET L_45abd8
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_42ea70
L_43014e:
          mov DWORD PTR [ESP+4],OFFSET _bd_458d74
          mov DWORD PTR [ESP],2
          lea EBP,DWORD PTR [ESP+100]
          call _log_printf
          lea EDI,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP+80],30268127
          mov DWORD PTR [ESP+76],1903825408
          jmp L_42fd55
L_43017f:
          add ESI,1
          mov DWORD PTR [ESP+24],EDX
          mov DWORD PTR [ESP+20],EAX
          mov DWORD PTR [ESP+16],EDI
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_45b3f4
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [ESP+1136]
          mov DWORD PTR [ESP],EAX
          call _free
          mov DWORD PTR [ESP+40],4294967295
          mov EAX,DWORD PTR [ESP+40]
          jmp L_42f8a2
L_4301ca:
          call _fixupPatchSet
          jmp L_42e87d
L_4301d4:
          mov ECX,OFFSET L_4bc580
          xor EBX,EBX
          jmp L_4301ef
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_4301e0:
          add ECX,1068
          cmp DWORD PTR [ECX-1068],20
          je L_4301f8
L_4301ef:
          add EBX,1
          cmp EAX,EBX
          jne L_4301e0
          xor EBX,EBX
L_4301f8:
          cmp EDX,21
          je L_430226
L_4301fd:
          mov EDX,OFFSET L_4bc580
          xor ESI,ESI
          jmp L_43021f
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_430210:
          add EDX,1068
          cmp DWORD PTR [EDX-1068],21
          je L_430228
L_43021f:
          add ESI,1
          cmp EAX,ESI
          jne L_430210
L_430226:
          xor ESI,ESI
L_430228:
          mov DWORD PTR [ESP+4],OFFSET L_45ad7c
          mov DWORD PTR [ESP],1
          call _log_printf
          imul EAX,EBX,1068
          mov EDI,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],OFFSET L_45ad3c
          mov DWORD PTR [ESP],1
          mov EAX,DWORD PTR [EAX+L_4bc174]
          mov DWORD PTR [ESP+8],EDI
          lea EDX,DWORD PTR [EDI+EAX*1]
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+16],EDX
          call _log_printf
          mov EAX,DWORD PTR [L_479ec4]
          test EAX,EAX
          je L_4303a0
          lea EBP,DWORD PTR [ESP+100]
          lea EDI,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP],EBP
          call _GetSystemTime
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EBP
          call _SystemTimeToFileTime
L_430298:
          lea EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+8],EAX
          lea EAX,DWORD PTR [ESP+62]
          mov DWORD PTR [ESP+4],EAX
          call _FileTimeToDosDateTime
          movzx EDX,WORD PTR [ESP+62]
          movzx EDI,WORD PTR [ESP+68]
          xor EAX,EAX
          mov ECX,EDX
          shr CX,8
          mov AL,CL
          mov ECX,EDI
          shl EDI,24
          mov AH,DL
          movzx EDX,CH
          shl EDX,16
          movzx EAX,AX
          or EAX,EDX
          or EDI,EAX
          imul EAX,EBX,1068
          mov DWORD PTR [ESP+64],EDI
          lea EDI,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+8],EDI
          mov EDX,DWORD PTR [EAX+L_4bc174]
          add EAX,OFFSET _xb
          mov DWORD PTR [ESP+12],EDX
          mov EAX,DWORD PTR [EAX+271064]
          imul EDX,ESI,1068
          mov DWORD PTR [ESP],OFFSET L_45ad6c
          add EAX,DWORD PTR [EDX+L_4bc150+12]
          mov DWORD PTR [ESP+4],EAX
          call _imgAddFile
          mov DWORD PTR [ESP+4],OFFSET L_45abd8
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [L_4c4f98]
          test EAX,EAX
          jle L_43042d
          mov EDX,DWORD PTR [L_4bc150+4]
          jmp L_42ffa0
L_430347:
          mov EAX,DWORD PTR [L_47a078]
          test EAX,EAX
          je L_43035a
          mov EDX,DWORD PTR [L_47a07c]
          test EDX,EDX
          jne L_4303d1
L_43035a:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],0
          call _patchBlsBlmod
          jmp L_42e87d
L_430373:
          mov DWORD PTR [ESP+4],OFFSET _bd_458d74
          mov DWORD PTR [ESP],2
          lea EDI,DWORD PTR [ESP+76]
          call _log_printf
          mov DWORD PTR [ESP+80],30268127
          mov DWORD PTR [ESP+76],1903825408
          jmp L_4300a4
L_4303a0:
          mov DWORD PTR [ESP+4],OFFSET _bd_458d74
          mov DWORD PTR [ESP],2
          lea EBP,DWORD PTR [ESP+100]
          call _log_printf
          lea EDI,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP+80],30268127
          mov DWORD PTR [ESP+76],1903825408
          jmp L_430298
L_4303d1:
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],EDX
          call _patchBlsBlmod
          mov EAX,DWORD PTR [L_47a078]
          mov DWORD PTR [ESP],EAX
          call _free
          jmp L_42e87d
L_4303ef:
          xor EBX,EBX
          xor ESI,ESI
          jmp L_42fce8
L_4303f8:
          xor EBX,EBX
          jmp L_42fcbd
L_4303ff:
          mov ESI,DWORD PTR [L_4bc174]
          test ESI,ESI
          je L_42ea70
          xor EBX,EBX
          jmp L_43000d
L_430414:
          mov EDI,DWORD PTR [L_4bc174]
          lea EBP,DWORD PTR [ESP+100]
          test EDI,EDI
          je L_42ffa9
          xor EBX,EBX
          jmp L_4301fd
L_43042d:
          mov EAX,DWORD PTR [L_4bc174]
          test EAX,EAX
          je L_42ea70
          xor EBX,EBX
          xor ESI,ESI
          jmp L_430038
L_430443:
          mov EDX,DWORD PTR [L_4bc174]
          lea EBP,DWORD PTR [ESP+100]
          test EDX,EDX
          je L_43042d
          xor EBX,EBX
          xor ESI,ESI
          jmp L_430228
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90

.data
.p2align 5
L_44a700:
          .byte 0xc0
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xff
          .byte 0xf
          .byte 0xf
          .byte 0xf
          .byte 0xf
          .byte 0xf
          .byte 0xf
          .byte 0xf
          .byte 0xf0
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
          .byte 0xff
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
L_44a760:
          .byte 0x80
          .byte 0x13
          .byte 0x1d
          .byte 0xb0
          .byte 0x80
          .byte 0x13
          .byte 0x3
          .byte 0xa0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x12
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x80
          .byte 0x13
          .byte 0x3
          .byte 0x74
          .byte 0x80
          .byte 0x13
          .byte 0x3
          .byte 0x74
          .byte 0x80
          .byte 0x13
          .byte 0x3
          .byte 0x7c
          .byte 0x80
          .byte 0x13
          .byte 0x3
          .byte 0x7c
          .byte 0x80
          .byte 0x12
          .byte 0x50
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xfd
          .byte 0xff
          .byte 0xd7
          .byte 0xff
          .byte 0x38
          .byte 0x60
          .byte 0x0
          .byte 0x10
          .byte 0x78
          .byte 0x63
          .byte 0xc1
          .byte 0xc6
          .byte 0xf8
          .byte 0x67
          .byte 0x0
          .byte 0x0
          .byte 0x7c
          .byte 0xc8
          .byte 0x3
          .byte 0xa6
          .byte 0x38
          .byte 0x80
          .byte 0xff
          .byte 0xff
          .byte 0x7c
          .byte 0x89
          .byte 0x3
          .byte 0xa6
          .byte 0x81
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .byte 0x91
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .byte 0x7c
          .byte 0x0
          .byte 0x30
          .byte 0x6c
          .byte 0x7c
          .byte 0x0
          .byte 0x37
          .byte 0xac
          .byte 0x7c
          .byte 0x0
          .byte 0x4
          .byte 0xac
          .byte 0x4c
          .byte 0x0
          .byte 0x1
          .byte 0x2c
          .byte 0x38
          .byte 0xc6
          .byte 0x0
          .byte 0x4
          .byte 0x38
          .byte 0xa5
          .byte 0x0
          .byte 0x4
          .byte 0x42
          .byte 0x0
          .byte 0xff
          .byte 0xe0
          .byte 0x38
          .byte 0x60
          .byte 0x0
          .byte 0x11
          .byte 0x78
          .byte 0x63
          .byte 0xc1
          .byte 0xc6
          .byte 0xf8
          .byte 0x67
          .byte 0x0
          .byte 0x0
          .byte 0x4e
          .byte 0x80
          .byte 0x0
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x48
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x80
          .byte 0x13
          .byte 0x3
          .byte 0xa0
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
          .byte 0xe0
          .byte 0x80
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x13
          .byte 0x3
          .byte 0xa0
          .byte 0x80
          .byte 0x0
          .byte 0x2
          .byte 0x0
          .byte 0xc8
          .byte 0x9
          .byte 0x0
          .byte 0x0
          .byte 0x80
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x80
          .byte 0x0
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x6
          .byte 0x10
          .byte 0x10
          .byte 0x80
          .byte 0x0
          .byte 0x2
          .byte 0x0
          .byte 0xea
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
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
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x80
          .byte 0x7
          .byte 0x1
          .byte 0x90
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
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x80
          .byte 0x7
          .byte 0x2
          .byte 0x28
          .byte 0x80
          .byte 0x7
          .byte 0x2
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x90
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_44a960:
          .byte 0x3c
          .byte 0x20
          .byte 0x80
          .byte 0x0
          .byte 0x78
          .byte 0x21
          .byte 0x7
          .byte 0xc6
          .byte 0x64
          .byte 0x21
          .byte 0x1e
          .byte 0x0
          .byte 0x7f
          .byte 0xdf
          .byte 0xfa
          .byte 0xa6
          .byte 0x7b
          .byte 0xc4
          .byte 0x83
          .byte 0xe4
          .byte 0x7c
          .byte 0x24
          .byte 0x8
          .byte 0x50
          .byte 0x38
          .byte 0x21
          .byte 0xff
          .byte 0x80
          .byte 0x7c
          .byte 0x71
          .byte 0xfa
          .byte 0xa6
          .byte 0x38
          .byte 0x80
          .byte 0x0
          .byte 0x1
          .byte 0x78
          .byte 0x83
          .byte 0x64
          .byte 0xce
          .byte 0x4c
          .byte 0x0
          .byte 0x1
          .byte 0x2c
          .byte 0x7c
          .byte 0x71
          .byte 0xfb
          .byte 0xa6
          .byte 0x4c
          .byte 0x0
          .byte 0x1
          .byte 0x2c
          .byte 0x7c
          .byte 0x79
          .byte 0xfa
          .byte 0xa6
          .byte 0x38
          .byte 0x80
          .byte 0x0
          .byte 0x8
          .byte 0x78
          .byte 0x83
          .byte 0x64
          .byte 0xe
          .byte 0x4c
          .byte 0x0
          .byte 0x1
          .byte 0x2c
          .byte 0x7c
          .byte 0x79
          .byte 0xfb
          .byte 0xa6
          .byte 0x4c
          .byte 0x0
          .byte 0x1
          .byte 0x2c
          .byte 0x7c
          .byte 0x7e
          .byte 0x4a
          .byte 0xa6
          .byte 0x38
          .byte 0x80
          .byte 0x0
          .byte 0x1
          .byte 0x78
          .byte 0x83
          .byte 0x55
          .byte 0x6c
          .byte 0x4c
          .byte 0x0
          .byte 0x1
          .byte 0x2c
          .byte 0x7c
          .byte 0x7e
          .byte 0x4b
          .byte 0xa6
          .byte 0x4c
          .byte 0x0
          .byte 0x1
          .byte 0x2c
          .byte 0x28
          .byte 0x3e
          .byte 0x0
          .byte 0x0
          .byte 0x40
          .byte 0x82
          .byte 0x0
          .byte 0x58
          .byte 0x3d
          .byte 0xa0
          .byte 0x2
          .byte 0x0
          .byte 0x7d
          .byte 0xa1
          .byte 0x1
          .byte 0x64
          .byte 0x3c
          .byte 0x60
          .byte 0x80
          .byte 0x0
          .byte 0x78
          .byte 0x63
          .byte 0x7
          .byte 0xc6
          .byte 0x64
          .byte 0x63
          .byte 0x1c
          .byte 0x0
          .byte 0x60
          .byte 0x63
          .byte 0xb
          .byte 0x0
          .byte 0xe8
          .byte 0x43
          .byte 0x0
          .byte 0x8
          .byte 0x48
          .byte 0x0
          .byte 0x3
          .byte 0x69
          .byte 0x28
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x40
          .byte 0x82
          .byte 0x0
          .byte 0xa8
          .byte 0x3f
          .byte 0xe0
          .byte 0x80
          .byte 0x0
          .byte 0x7b
          .byte 0xff
          .byte 0x7
          .byte 0xc6
          .byte 0x63
          .byte 0xff
          .byte 0x1
          .byte 0x0
          .byte 0x38
          .byte 0x60
          .byte 0x0
          .byte 0x0
          .byte 0x4c
          .byte 0x0
          .byte 0x1
          .byte 0x2c
          .byte 0x7c
          .byte 0x79
          .byte 0x4b
          .byte 0xa6
          .byte 0x7c
          .byte 0x70
          .byte 0x4b
          .byte 0xa6
          .byte 0x7c
          .byte 0x71
          .byte 0x4b
          .byte 0xa6
          .byte 0x4c
          .byte 0x0
          .byte 0x1
          .byte 0x2c
          .byte 0x7f
          .byte 0xe8
          .byte 0x3
          .byte 0xa6
          .byte 0x4e
          .byte 0x80
          .byte 0x0
          .byte 0x20
          .byte 0x3c
          .byte 0x80
          .byte 0x80
          .byte 0x0
          .byte 0x78
          .byte 0x84
          .byte 0x7
          .byte 0xc6
          .byte 0x64
          .byte 0x84
          .byte 0x1c
          .byte 0x0
          .byte 0x60
          .byte 0x84
          .byte 0xa
          .byte 0xa8
          .byte 0x7c
          .byte 0x7f
          .byte 0xfa
          .byte 0xa6
          .byte 0x54
          .byte 0x63
          .byte 0x10
          .byte 0x3a
          .byte 0x7c
          .byte 0x84
          .byte 0x1a
          .byte 0x14
          .byte 0x38
          .byte 0xa0
          .byte 0x0
          .byte 0x1
          .byte 0x90
          .byte 0xa4
          .byte 0x0
          .byte 0x0
          .byte 0x3f
          .byte 0x80
          .byte 0x80
          .byte 0x0
          .byte 0x7b
          .byte 0x9c
          .byte 0x7
          .byte 0xc6
          .byte 0x67
          .byte 0x9c
          .byte 0x1c
          .byte 0x8
          .byte 0x63
          .byte 0x9c
          .byte 0x0
          .byte 0x0
          .byte 0x3f
          .byte 0xa0
          .byte 0x80
          .byte 0x0
          .byte 0x7b
          .byte 0xbd
          .byte 0x7
          .byte 0xc6
          .byte 0x67
          .byte 0xbd
          .byte 0x1c
          .byte 0x0
          .byte 0x63
          .byte 0xbd
          .byte 0xa
          .byte 0xc8
          .byte 0xeb
          .byte 0xbd
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xf8
          .byte 0x1d
          .byte 0x0
          .byte 0x0
          .byte 0xe8
          .byte 0x7d
          .byte 0x0
          .byte 0x0
          .byte 0x28
          .byte 0x23
          .byte 0x0
          .byte 0x0
          .byte 0x40
          .byte 0x82
          .byte 0x0
          .byte 0x34
          .byte 0x80
          .byte 0x7c
          .byte 0x0
          .byte 0x0
          .byte 0x28
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0x82
          .byte 0xff
          .byte 0xec
          .byte 0x3c
          .byte 0x60
          .byte 0x0
          .byte 0x1
          .byte 0x7c
          .byte 0x69
          .byte 0x3
          .byte 0xa6
          .byte 0x60
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x42
          .byte 0x0
          .byte 0xff
          .byte 0xfc
          .byte 0x3f
          .byte 0xe0
          .byte 0x80
          .byte 0x0
          .byte 0x7b
          .byte 0xff
          .byte 0x7
          .byte 0xc6
          .byte 0x67
          .byte 0xff
          .byte 0x1c
          .byte 0x4
          .byte 0x7f
          .byte 0xe8
          .byte 0x3
          .byte 0xa6
          .byte 0x4e
          .byte 0x80
          .byte 0x0
          .byte 0x20
          .byte 0x7c
          .byte 0x79
          .byte 0xfa
          .byte 0xa6
          .byte 0x38
          .byte 0x80
          .byte 0x0
          .byte 0x1
          .byte 0x78
          .byte 0x83
          .byte 0x83
          .byte 0xce
          .byte 0x38
          .byte 0x80
          .byte 0x0
          .byte 0x8
          .byte 0x78
          .byte 0x83
          .byte 0x64
          .byte 0xe
          .byte 0x38
          .byte 0x80
          .byte 0x0
          .byte 0xe
          .byte 0x78
          .byte 0x83
          .byte 0x16
          .byte 0x8e
          .byte 0x4c
          .byte 0x0
          .byte 0x1
          .byte 0x2c
          .byte 0x7c
          .byte 0x79
          .byte 0xfb
          .byte 0xa6
          .byte 0x7c
          .byte 0x0
          .byte 0x4
          .byte 0xac
          .byte 0x4c
          .byte 0x0
          .byte 0x1
          .byte 0x2c
          .byte 0x7c
          .byte 0x7e
          .byte 0x4a
          .byte 0xa6
          .byte 0x38
          .byte 0x80
          .byte 0x0
          .byte 0x1
          .byte 0x78
          .byte 0x83
          .byte 0xf
          .byte 0xac
          .byte 0x4c
          .byte 0x0
          .byte 0x1
          .byte 0x2c
          .byte 0x7c
          .byte 0x7e
          .byte 0x4b
          .byte 0xa6
          .byte 0x7c
          .byte 0x0
          .byte 0x4
          .byte 0xac
          .byte 0x4c
          .byte 0x0
          .byte 0x1
          .byte 0x2c
          .byte 0x38
          .byte 0x60
          .byte 0x3
          .byte 0xff
          .byte 0x78
          .byte 0x63
          .byte 0x7
          .byte 0xc6
          .byte 0x7c
          .byte 0x20
          .byte 0x1a
          .byte 0x24
          .byte 0x7c
          .byte 0x0
          .byte 0x4
          .byte 0xac
          .byte 0x7c
          .byte 0x74
          .byte 0xfa
          .byte 0xa6
          .byte 0x38
          .byte 0x80
          .byte 0x0
          .byte 0x3f
          .byte 0x78
          .byte 0x83
          .byte 0x44
          .byte 0x8e
          .byte 0x4c
          .byte 0x0
          .byte 0x1
          .byte 0x2c
          .byte 0x7c
          .byte 0x74
          .byte 0xfb
          .byte 0xa6
          .byte 0x7c
          .byte 0x0
          .byte 0x4
          .byte 0xac
          .byte 0x4c
          .byte 0x0
          .byte 0x1
          .byte 0x2c
          .byte 0x38
          .byte 0x60
          .byte 0x0
          .byte 0x0
          .byte 0x7c
          .byte 0x70
          .byte 0x4b
          .byte 0xa6
          .byte 0x7c
          .byte 0x71
          .byte 0x4b
          .byte 0xa6
          .byte 0x7c
          .byte 0x71
          .byte 0xfa
          .byte 0xa6
          .byte 0x38
          .byte 0x80
          .byte 0x0
          .byte 0x1
          .byte 0x78
          .byte 0x83
          .byte 0xf8
          .byte 0xe
          .byte 0x38
          .byte 0x80
          .byte 0x0
          .byte 0x7
          .byte 0x78
          .byte 0x83
          .byte 0xd0
          .byte 0xce
          .byte 0x38
          .byte 0x80
          .byte 0x0
          .byte 0x3
          .byte 0x78
          .byte 0x83
          .byte 0xa2
          .byte 0x8e
          .byte 0x38
          .byte 0x80
          .byte 0x0
          .byte 0x1
          .byte 0x78
          .byte 0x83
          .byte 0x36
          .byte 0x4e
          .byte 0x38
          .byte 0x80
          .byte 0x1
          .byte 0x0
          .byte 0x78
          .byte 0x84
          .byte 0x7
          .byte 0xc6
          .byte 0x7c
          .byte 0xa0
          .byte 0x0
          .byte 0xa6
          .byte 0x38
          .byte 0xc0
          .byte 0x0
          .byte 0x30
          .byte 0x7c
          .byte 0xa5
          .byte 0x30
          .byte 0x78
          .byte 0x7c
          .byte 0xbb
          .byte 0x3
          .byte 0xa6
          .byte 0x38
          .byte 0xc0
          .byte 0x1
          .byte 0x0
          .byte 0x7c
          .byte 0xda
          .byte 0x3
          .byte 0xa6
          .byte 0x7c
          .byte 0x71
          .byte 0xfb
          .byte 0xa6
          .byte 0x7c
          .byte 0x99
          .byte 0x4b
          .byte 0xa6
          .byte 0x4c
          .byte 0x0
          .byte 0x0
          .byte 0x24
          .byte 0x3c
          .byte 0x80
          .byte 0x80
          .byte 0x0
          .byte 0x60
          .byte 0x84
          .byte 0x2
          .byte 0x0
          .byte 0x78
          .byte 0x84
          .byte 0x7
          .byte 0xc6
          .byte 0x64
          .byte 0x84
          .byte 0xea
          .byte 0x0
          .byte 0x80
          .byte 0xa4
          .byte 0x10
          .byte 0x18
          .byte 0x54
          .byte 0xa5
          .byte 0x1
          .byte 0x8d
          .byte 0x41
          .byte 0x82
          .byte 0xff
          .byte 0xf8
          .byte 0x54
          .byte 0x63
          .byte 0xc0
          .byte 0xe
          .byte 0x90
          .byte 0x64
          .byte 0x10
          .byte 0x14
          .byte 0x4e
          .byte 0x80
          .byte 0x0
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0xe0
          .byte 0x0
          .byte 0x10
          .byte 0x39
          .byte 0x21
          .byte 0xff
          .byte 0xef
          .byte 0x39
          .byte 0x40
          .byte 0x0
          .byte 0x0
          .byte 0x7c
          .byte 0xe9
          .byte 0x3
          .byte 0xa6
          .byte 0x9d
          .byte 0x49
          .byte 0x0
          .byte 0x1
          .byte 0x42
          .byte 0x0
          .byte 0xff
          .byte 0xfc
          .byte 0x39
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x39
          .byte 0x21
          .byte 0xff
          .byte 0xdf
          .byte 0x39
          .byte 0x40
          .byte 0x0
          .byte 0x0
          .byte 0x7d
          .byte 0x9
          .byte 0x3
          .byte 0xa6
          .byte 0x9d
          .byte 0x49
          .byte 0x0
          .byte 0x1
          .byte 0x42
          .byte 0x0
          .byte 0xff
          .byte 0xfc
          .byte 0x3d
          .byte 0x0
          .byte 0x80
          .byte 0x0
          .byte 0x98
          .byte 0x61
          .byte 0xff
          .byte 0xf0
          .byte 0x61
          .byte 0x8
          .byte 0x2
          .byte 0x0
          .byte 0x79
          .byte 0x8
          .byte 0x7
          .byte 0xc6
          .byte 0x65
          .byte 0x8
          .byte 0xea
          .byte 0x0
          .byte 0x61
          .byte 0x8
          .byte 0x10
          .byte 0x84
          .byte 0x3d
          .byte 0x20
          .byte 0x80
          .byte 0x0
          .byte 0x81
          .byte 0x48
          .byte 0x0
          .byte 0x0
          .byte 0x61
          .byte 0x29
          .byte 0x2
          .byte 0x0
          .byte 0x55
          .byte 0x4a
          .byte 0x1
          .byte 0x4a
          .byte 0x79
          .byte 0x29
          .byte 0x7
          .byte 0xc6
          .byte 0x2f
          .byte 0x8a
          .byte 0x0
          .byte 0x0
          .byte 0x65
          .byte 0x29
          .byte 0xea
          .byte 0x0
          .byte 0x61
          .byte 0x29
          .byte 0x10
          .byte 0x84
          .byte 0x41
          .byte 0x9e
          .byte 0xff
          .byte 0xe0
          .byte 0x3d
          .byte 0x40
          .byte 0x80
          .byte 0x0
          .byte 0x3d
          .byte 0x0
          .byte 0x4
          .byte 0x0
          .byte 0x61
          .byte 0x4a
          .byte 0x2
          .byte 0x0
          .byte 0x91
          .byte 0x9
          .byte 0x0
          .byte 0x0
          .byte 0x3d
          .byte 0x0
          .byte 0x80
          .byte 0x0
          .byte 0x79
          .byte 0x4a
          .byte 0x7
          .byte 0xc6
          .byte 0x80
          .byte 0xe1
          .byte 0xff
          .byte 0xf0
          .byte 0x61
          .byte 0x8
          .byte 0x2
          .byte 0x0
          .byte 0x65
          .byte 0x4a
          .byte 0xea
          .byte 0x0
          .byte 0x79
          .byte 0x8
          .byte 0x7
          .byte 0xc6
          .byte 0x61
          .byte 0x4a
          .byte 0x10
          .byte 0x80
          .byte 0x65
          .byte 0x8
          .byte 0xea
          .byte 0x0
          .byte 0x90
          .byte 0xea
          .byte 0x0
          .byte 0x0
          .byte 0x39
          .byte 0x60
          .byte 0x0
          .byte 0x4
          .byte 0x80
          .byte 0xe1
          .byte 0xff
          .byte 0xf4
          .byte 0x7d
          .byte 0x6
          .byte 0x43
          .byte 0x78
          .byte 0x38
          .byte 0xa1
          .byte 0xff
          .byte 0xec
          .byte 0x90
          .byte 0xea
          .byte 0x0
          .byte 0x0
          .byte 0x61
          .byte 0x8
          .byte 0x10
          .byte 0x94
          .byte 0x80
          .byte 0xe1
          .byte 0xff
          .byte 0xf8
          .byte 0x60
          .byte 0xc6
          .byte 0x10
          .byte 0x90
          .byte 0x38
          .byte 0x80
          .byte 0x0
          .byte 0x0
          .byte 0x90
          .byte 0xea
          .byte 0x0
          .byte 0x0
          .byte 0x80
          .byte 0xe1
          .byte 0xff
          .byte 0xfc
          .byte 0x90
          .byte 0xea
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0xe0
          .byte 0x0
          .byte 0x0
          .byte 0x39
          .byte 0x40
          .byte 0x0
          .byte 0x0
          .byte 0x90
          .byte 0xe9
          .byte 0x0
          .byte 0x0
          .byte 0x60
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x89
          .byte 0x21
          .byte 0xff
          .byte 0xe0
          .byte 0x7f
          .byte 0x89
          .byte 0x18
          .byte 0x0
          .byte 0x41
          .byte 0x9e
          .byte 0x0
          .byte 0x50
          .byte 0x38
          .byte 0xe0
          .byte 0x0
          .byte 0x10
          .byte 0x39
          .byte 0x21
          .byte 0xff
          .byte 0xdf
          .byte 0x7c
          .byte 0xe9
          .byte 0x3
          .byte 0xa6
          .byte 0x9d
          .byte 0x49
          .byte 0x0
          .byte 0x1
          .byte 0x42
          .byte 0x0
          .byte 0xff
          .byte 0xfc
          .byte 0x81
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x55
          .byte 0x29
          .byte 0x1
          .byte 0x4a
          .byte 0x2f
          .byte 0x89
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0x9e
          .byte 0xff
          .byte 0xd4
          .byte 0x39
          .byte 0x21
          .byte 0xff
          .byte 0xdc
          .byte 0x91
          .byte 0x68
          .byte 0x0
          .byte 0x0
          .byte 0x80
          .byte 0xe6
          .byte 0x0
          .byte 0x0
          .byte 0x94
          .byte 0xe9
          .byte 0x0
          .byte 0x4
          .byte 0x7f
          .byte 0xa9
          .byte 0x28
          .byte 0x0
          .byte 0x40
          .byte 0x9e
          .byte 0xff
          .byte 0xf4
          .byte 0x90
          .byte 0x88
          .byte 0x0
          .byte 0x0
          .byte 0x89
          .byte 0x21
          .byte 0xff
          .byte 0xe0
          .byte 0x7f
          .byte 0x89
          .byte 0x18
          .byte 0x0
          .byte 0x40
          .byte 0x9e
          .byte 0xff
          .byte 0xb8
          .byte 0x88
          .byte 0x61
          .byte 0xff
          .byte 0xe1
          .byte 0x4e
          .byte 0x80
          .byte 0x0
          .byte 0x20
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
          .byte 0x60
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xfb
          .byte 0xe1
          .byte 0xff
          .byte 0xf8
          .byte 0x7c
          .byte 0x8
          .byte 0x2
          .byte 0xa6
          .byte 0xf8
          .byte 0x1
          .byte 0x0
          .byte 0x10
          .byte 0x7c
          .byte 0x7f
          .byte 0x1b
          .byte 0x78
          .byte 0xf8
          .byte 0x21
          .byte 0xff
          .byte 0x81
          .byte 0x88
          .byte 0x63
          .byte 0x0
          .byte 0x0
          .byte 0x2f
          .byte 0xa3
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0x9e
          .byte 0x0
          .byte 0x18
          .byte 0x4b
          .byte 0xff
          .byte 0xfe
          .byte 0x65
          .byte 0x60
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8c
          .byte 0x7f
          .byte 0x0
          .byte 0x1
          .byte 0x2f
          .byte 0xa3
          .byte 0x0
          .byte 0x0
          .byte 0x40
          .byte 0x9e
          .byte 0xff
          .byte 0xf0
          .byte 0x38
          .byte 0x21
          .byte 0x0
          .byte 0x80
          .byte 0xe8
          .byte 0x1
          .byte 0x0
          .byte 0x10
          .byte 0xeb
          .byte 0xe1
          .byte 0xff
          .byte 0xf8
          .byte 0x7c
          .byte 0x8
          .byte 0x3
          .byte 0xa6
          .byte 0x4e
          .byte 0x80
          .byte 0x0
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1
          .byte 0x80
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x60
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x3d
          .byte 0x42
          .byte 0x0
          .byte 0x7
          .byte 0x7c
          .byte 0x8
          .byte 0x2
          .byte 0xa6
          .byte 0x3d
          .byte 0x22
          .byte 0x0
          .byte 0x7
          .byte 0xf8
          .byte 0x1
          .byte 0x0
          .byte 0x10
          .byte 0xfa
          .byte 0xc1
          .byte 0xff
          .byte 0xb0
          .byte 0xfa
          .byte 0xe1
          .byte 0xff
          .byte 0xb8
          .byte 0xfb
          .byte 0x1
          .byte 0xff
          .byte 0xc0
          .byte 0x39
          .byte 0x4a
          .byte 0x75
          .byte 0x34
          .byte 0xfb
          .byte 0x21
          .byte 0xff
          .byte 0xc8
          .byte 0x39
          .byte 0x29
          .byte 0x75
          .byte 0x30
          .byte 0x7d
          .byte 0x9
          .byte 0x50
          .byte 0x51
          .byte 0xfb
          .byte 0x41
          .byte 0xff
          .byte 0xd0
          .byte 0xfb
          .byte 0x61
          .byte 0xff
          .byte 0xd8
          .byte 0xfb
          .byte 0x81
          .byte 0xff
          .byte 0xe0
          .byte 0xfb
          .byte 0xa1
          .byte 0xff
          .byte 0xe8
          .byte 0xfb
          .byte 0xc1
          .byte 0xff
          .byte 0xf0
          .byte 0xfb
          .byte 0xe1
          .byte 0xff
          .byte 0xf8
          .byte 0xf8
          .byte 0x21
          .byte 0xff
          .byte 0x41
          .byte 0x41
          .byte 0x82
          .byte 0x0
          .byte 0x18
          .byte 0x39
          .byte 0x29
          .byte 0xff
          .byte 0xff
          .byte 0x7d
          .byte 0x9
          .byte 0x3
          .byte 0xa6
          .byte 0x39
          .byte 0x40
          .byte 0x0
          .byte 0x0
          .byte 0x9d
          .byte 0x49
          .byte 0x0
          .byte 0x1
          .byte 0x42
          .byte 0x0
          .byte 0xff
          .byte 0xfc
          .byte 0x3d
          .byte 0x22
          .byte 0xff
          .byte 0xff
          .byte 0x60
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x3f
          .byte 0x40
          .byte 0x78
          .byte 0x63
          .byte 0x3b
          .byte 0x22
          .byte 0x80
          .byte 0x48
          .byte 0x3f
          .byte 0x60
          .byte 0x7c
          .byte 0x68
          .byte 0x39
          .byte 0x29
          .byte 0x75
          .byte 0x30
          .byte 0x3f
          .byte 0x80
          .byte 0x4e
          .byte 0x80
          .byte 0x3f
          .byte 0xa0
          .byte 0x4b
          .byte 0xff
          .byte 0x79
          .byte 0x36
          .byte 0x84
          .byte 0x20
          .byte 0x79
          .byte 0x37
          .byte 0x84
          .byte 0x22
          .byte 0x79
          .byte 0x29
          .byte 0x4
          .byte 0x20
          .byte 0x3b
          .byte 0xd9
          .byte 0xff
          .byte 0xf8
          .byte 0x66
          .byte 0xd6
          .byte 0x3c
          .byte 0x60
          .byte 0x66
          .byte 0xf7
          .byte 0x64
          .byte 0x63
          .byte 0x65
          .byte 0x38
          .byte 0x60
          .byte 0x63
          .byte 0x3b
          .byte 0x39
          .byte 0x0
          .byte 0x98
          .byte 0x63
          .byte 0x5a
          .byte 0x7
          .byte 0xc6
          .byte 0x63
          .byte 0x7b
          .byte 0x3
          .byte 0xa6
          .byte 0x63
          .byte 0x9c
          .byte 0x0
          .byte 0x21
          .byte 0x63
          .byte 0xbd
          .byte 0xff
          .byte 0xe8
          .byte 0xeb
          .byte 0xfe
          .byte 0x0
          .byte 0x9
          .byte 0x38
          .byte 0x80
          .byte 0x1
          .byte 0x0
          .byte 0x38
          .byte 0x7f
          .byte 0xff
          .byte 0x80
          .byte 0x48
          .byte 0x0
          .byte 0x5
          .byte 0x6d
          .byte 0x60
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0x7f
          .byte 0xff
          .byte 0xe8
          .byte 0x92
          .byte 0xdf
          .byte 0xff
          .byte 0xe8
          .byte 0x38
          .byte 0x80
          .byte 0x0
          .byte 0x18
          .byte 0x93
          .byte 0x5f
          .byte 0xff
          .byte 0xec
          .byte 0x92
          .byte 0xff
          .byte 0xff
          .byte 0xf0
          .byte 0x93
          .byte 0x1f
          .byte 0xff
          .byte 0xf4
          .byte 0x93
          .byte 0x7f
          .byte 0xff
          .byte 0xf8
          .byte 0x93
          .byte 0x9f
          .byte 0xff
          .byte 0xfc
          .byte 0x48
          .byte 0x0
          .byte 0x5
          .byte 0x9d
          .byte 0x60
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x7f
          .byte 0xe3
          .byte 0xfb
          .byte 0x78
          .byte 0x93
          .byte 0xbf
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0x80
          .byte 0x0
          .byte 0x80
          .byte 0x48
          .byte 0x0
          .byte 0x5
          .byte 0x89
          .byte 0x60
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x7f
          .byte 0xbe
          .byte 0xc8
          .byte 0x0
          .byte 0x40
          .byte 0x9e
          .byte 0xff
          .byte 0xac
          .byte 0x3d
          .byte 0x40
          .byte 0x80
          .byte 0x0
          .byte 0x3d
          .byte 0x0
          .byte 0x0
          .byte 0x3e
          .byte 0x61
          .byte 0x4a
          .byte 0x2
          .byte 0x0
          .byte 0x3f
          .byte 0xe2
          .byte 0xff
          .byte 0xff
          .byte 0x79
          .byte 0x4a
          .byte 0x7
          .byte 0xc6
          .byte 0x61
          .byte 0x8
          .byte 0x0
          .byte 0x78
          .byte 0x65
          .byte 0x4a
          .byte 0x0
          .byte 0x5
          .byte 0x38
          .byte 0xc0
          .byte 0x0
          .byte 0x0
          .byte 0x61
          .byte 0x4a
          .byte 0x20
          .byte 0x10
          .byte 0x39
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x3b
          .byte 0xff
          .byte 0x7f
          .byte 0xd8
          .byte 0xf9
          .byte 0xa
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0xa0
          .byte 0x0
          .byte 0x1
          .byte 0x60
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x79
          .byte 0x28
          .byte 0x17
          .byte 0x64
          .byte 0x39
          .byte 0x49
          .byte 0x0
          .byte 0x1
          .byte 0x7c
          .byte 0xa7
          .byte 0x48
          .byte 0x30
          .byte 0x7d
          .byte 0x49
          .byte 0x7
          .byte 0xb4
          .byte 0x7c
          .byte 0xe7
          .byte 0x33
          .byte 0x78
          .byte 0x7d
          .byte 0x1f
          .byte 0x40
          .byte 0x2e
          .byte 0x2f
          .byte 0x8a
          .byte 0x0
          .byte 0x6
          .byte 0x2f
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0x9a
          .byte 0x0
          .byte 0x8
          .byte 0x7c
          .byte 0xe6
          .byte 0x7
          .byte 0xb4
          .byte 0x40
          .byte 0x9e
          .byte 0xff
          .byte 0xd8
          .byte 0x2f
          .byte 0x86
          .byte 0x0
          .byte 0x3f
          .byte 0x39
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0xc0
          .byte 0x0
          .byte 0x0
          .byte 0x40
          .byte 0x9e
          .byte 0xff
          .byte 0xc8
          .byte 0x3d
          .byte 0x40
          .byte 0x80
          .byte 0x0
          .byte 0x61
          .byte 0x4a
          .byte 0x2
          .byte 0x0
          .byte 0x79
          .byte 0x4a
          .byte 0x7
          .byte 0xc6
          .byte 0x65
          .byte 0x4a
          .byte 0xc8
          .byte 0x0
          .byte 0x7d
          .byte 0x49
          .byte 0x53
          .byte 0x78
          .byte 0x61
          .byte 0x4a
          .byte 0x0
          .byte 0x48
          .byte 0x61
          .byte 0x29
          .byte 0x0
          .byte 0x4c
          .byte 0x81
          .byte 0x4a
          .byte 0x0
          .byte 0x0
          .byte 0x91
          .byte 0x5f
          .byte 0x0
          .byte 0x18
          .byte 0x81
          .byte 0x29
          .byte 0x0
          .byte 0x0
          .byte 0x55
          .byte 0x2a
          .byte 0x6
          .byte 0x3e
          .byte 0x91
          .byte 0x3f
          .byte 0x0
          .byte 0x1c
          .byte 0x2f
          .byte 0x8a
          .byte 0x0
          .byte 0x0
          .byte 0x40
          .byte 0x9e
          .byte 0x0
          .byte 0xc
          .byte 0x39
          .byte 0x20
          .byte 0x0
          .byte 0x12
          .byte 0x99
          .byte 0x3f
          .byte 0x0
          .byte 0x1f
          .byte 0x89
          .byte 0x5f
          .byte 0x0
          .byte 0x1d
          .byte 0x55
          .byte 0x49
          .byte 0x7
          .byte 0xfe
          .byte 0x2f
          .byte 0x89
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0x9e
          .byte 0x0
          .byte 0x20
          .byte 0x3d
          .byte 0x20
          .byte 0x80
          .byte 0x0
          .byte 0x3d
          .byte 0x0
          .byte 0xae
          .byte 0x1
          .byte 0x61
          .byte 0x29
          .byte 0x2
          .byte 0x0
          .byte 0x79
          .byte 0x29
          .byte 0x7
          .byte 0xc6
          .byte 0x65
          .byte 0x29
          .byte 0xea
          .byte 0x0
          .byte 0x61
          .byte 0x29
          .byte 0x10
          .byte 0x1c
          .byte 0x91
          .byte 0x9
          .byte 0x0
          .byte 0x0
          .byte 0x55
          .byte 0x4a
          .byte 0x7
          .byte 0x7a
          .byte 0x55
          .byte 0x48
          .byte 0x6
          .byte 0x3e
          .byte 0x2c
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0x82
          .byte 0x0
          .byte 0xc4
          .byte 0x38
          .byte 0x60
          .byte 0x0
          .byte 0x1
          .byte 0x3b
          .byte 0xc0
          .byte 0x0
          .byte 0x1
          .byte 0x4b
          .byte 0xff
          .byte 0xfc
          .byte 0x59
          .byte 0x89
          .byte 0x3f
          .byte 0x0
          .byte 0x1f
          .byte 0x7f
          .byte 0x89
          .byte 0x18
          .byte 0x0
          .byte 0x41
          .byte 0x9e
          .byte 0x0
          .byte 0x20
          .byte 0x89
          .byte 0x3f
          .byte 0x0
          .byte 0x1e
          .byte 0x3b
          .byte 0xc0
          .byte 0x0
          .byte 0x0
          .byte 0x2f
          .byte 0xa9
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0x9e
          .byte 0x0
          .byte 0x10
          .byte 0x7c
          .byte 0x7e
          .byte 0x4a
          .byte 0x78
          .byte 0x7f
          .byte 0xde
          .byte 0x0
          .byte 0x74
          .byte 0x7b
          .byte 0xde
          .byte 0xd1
          .byte 0x82
          .byte 0x89
          .byte 0x3f
          .byte 0x0
          .byte 0x1c
          .byte 0x2f
          .byte 0xa9
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0x9e
          .byte 0x0
          .byte 0xb0
          .byte 0x7f
          .byte 0x83
          .byte 0x48
          .byte 0x40
          .byte 0x40
          .byte 0x9e
          .byte 0x0
          .byte 0xa8
          .byte 0x60
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0x62
          .byte 0x80
          .byte 0xe8
          .byte 0x4b
          .byte 0xff
          .byte 0xfd
          .byte 0x61
          .byte 0x60
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0x62
          .byte 0x80
          .byte 0xf0
          .byte 0x4b
          .byte 0xff
          .byte 0xfd
          .byte 0x55
          .byte 0x60
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0x62
          .byte 0x81
          .byte 0x20
          .byte 0x4b
          .byte 0xff
          .byte 0xfd
          .byte 0x49
          .byte 0x60
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0x62
          .byte 0x81
          .byte 0x50
          .byte 0x4b
          .byte 0xff
          .byte 0xfd
          .byte 0x3d
          .byte 0x60
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0x62
          .byte 0x81
          .byte 0x80
          .byte 0x4b
          .byte 0xff
          .byte 0xfd
          .byte 0x31
          .byte 0x60
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0x62
          .byte 0x81
          .byte 0xb0
          .byte 0x4b
          .byte 0xff
          .byte 0xfd
          .byte 0x25
          .byte 0x60
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0x62
          .byte 0x81
          .byte 0xe0
          .byte 0x4b
          .byte 0xff
          .byte 0xfd
          .byte 0x19
          .byte 0x60
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0x62
          .byte 0x82
          .byte 0x10
          .byte 0x4b
          .byte 0xff
          .byte 0xfd
          .byte 0xd
          .byte 0x2f
          .byte 0xbe
          .byte 0x0
          .byte 0x0
          .byte 0x40
          .byte 0x9e
          .byte 0x2
          .byte 0x5c
          .byte 0x60
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0x62
          .byte 0x82
          .byte 0x60
          .byte 0x4b
          .byte 0xff
          .byte 0xfc
          .byte 0xf9
          .byte 0x48
          .byte 0x0
          .byte 0x0
          .byte 0x98
          .byte 0x38
          .byte 0x60
          .byte 0x0
          .byte 0xa
          .byte 0x4b
          .byte 0xff
          .byte 0xfb
          .byte 0x9d
          .byte 0x89
          .byte 0x3f
          .byte 0x0
          .byte 0x1d
          .byte 0x55
          .byte 0x29
          .byte 0x7
          .byte 0xbc
          .byte 0x55
          .byte 0x2a
          .byte 0x6
          .byte 0x3e
          .byte 0x2c
          .byte 0xa
          .byte 0x0
          .byte 0x0
          .byte 0x40
          .byte 0x82
          .byte 0x2
          .byte 0x8
          .byte 0x68
          .byte 0x63
          .byte 0x0
          .byte 0x62
          .byte 0x78
          .byte 0x7e
          .byte 0x6
          .byte 0x20
          .byte 0x7f
          .byte 0xde
          .byte 0x0
          .byte 0xd0
          .byte 0x7b
          .byte 0xde
          .byte 0xf
          .byte 0xe0
          .byte 0x60
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0x62
          .byte 0x80
          .byte 0xf0
          .byte 0x4b
          .byte 0xff
          .byte 0xfc
          .byte 0xbd
          .byte 0x60
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0x62
          .byte 0x81
          .byte 0x20
          .byte 0x4b
          .byte 0xff
          .byte 0xfc
          .byte 0xb1
          .byte 0x60
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0x62
          .byte 0x81
          .byte 0x50
          .byte 0x4b
          .byte 0xff
          .byte 0xfc
          .byte 0xa5
          .byte 0x60
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0x62
          .byte 0x81
          .byte 0x80
          .byte 0x4b
          .byte 0xff
          .byte 0xfc
          .byte 0x99
          .byte 0x60
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0x62
          .byte 0x81
          .byte 0xb0
          .byte 0x4b
          .byte 0xff
          .byte 0xfc
          .byte 0x8d
          .byte 0x60
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0x62
          .byte 0x81
          .byte 0xe0
          .byte 0x4b
          .byte 0xff
          .byte 0xfc
          .byte 0x81
          .byte 0x60
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0x62
          .byte 0x82
          .byte 0x10
          .byte 0x4b
          .byte 0xff
          .byte 0xfc
          .byte 0x75
          .byte 0x2f
          .byte 0xbe
          .byte 0x0
          .byte 0x0
          .byte 0x40
          .byte 0x9e
          .byte 0x1
          .byte 0xc4
          .byte 0x60
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0x62
          .byte 0x82
          .byte 0x30
          .byte 0x4b
          .byte 0xff
          .byte 0xfc
          .byte 0x61
          .byte 0x3d
          .byte 0x20
          .byte 0x80
          .byte 0x0
          .byte 0x39
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x61
          .byte 0x29
          .byte 0x1
          .byte 0xff
          .byte 0x39
          .byte 0x40
          .byte 0xff
          .byte 0xff
          .byte 0x79
          .byte 0x29
          .byte 0x7
          .byte 0xc6
          .byte 0x61
          .byte 0x19
          .byte 0x80
          .byte 0x0
          .byte 0x65
          .byte 0x29
          .byte 0xff
          .byte 0xff
          .byte 0x79
          .byte 0x4a
          .byte 0x0
          .byte 0x40
          .byte 0x7f
          .byte 0x29
          .byte 0x3
          .byte 0xa6
          .byte 0x61
          .byte 0x29
          .byte 0xff
          .byte 0xff
          .byte 0x60
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8d
          .byte 0x9
          .byte 0x0
          .byte 0x1
          .byte 0x9d
          .byte 0xa
          .byte 0x0
          .byte 0x1
          .byte 0x42
          .byte 0x0
          .byte 0xff
          .byte 0xf8
          .byte 0x3d
          .byte 0x20
          .byte 0x80
          .byte 0x0
          .byte 0x61
          .byte 0x29
          .byte 0x2
          .byte 0x0
          .byte 0x79
          .byte 0x29
          .byte 0x7
          .byte 0xc6
          .byte 0x65
          .byte 0x29
          .byte 0xc8
          .byte 0x9
          .byte 0x61
          .byte 0x29
          .byte 0x10
          .byte 0x0
          .byte 0x81
          .byte 0x49
          .byte 0x0
          .byte 0x0
          .byte 0x3d
          .byte 0x20
          .byte 0x80
          .byte 0x0
          .byte 0x2f
          .byte 0x8a
          .byte 0xff
          .byte 0xff
          .byte 0x41
          .byte 0x9e
          .byte 0x1
          .byte 0x48
          .byte 0x61
          .byte 0x29
          .byte 0x2
          .byte 0x0
          .byte 0x38
          .byte 0x80
          .byte 0xff
          .byte 0xff
          .byte 0x79
          .byte 0x29
          .byte 0x7
          .byte 0xc6
          .byte 0x78
          .byte 0x84
          .byte 0x0
          .byte 0x4
          .byte 0x65
          .byte 0x29
          .byte 0xc8
          .byte 0x9
          .byte 0x61
          .byte 0x29
          .byte 0x10
          .byte 0x4
          .byte 0x81
          .byte 0x9
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0xc9
          .byte 0x0
          .byte 0x4
          .byte 0x7d
          .byte 0x4a
          .byte 0x22
          .byte 0x14
          .byte 0x2f
          .byte 0xa8
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0x9e
          .byte 0x0
          .byte 0x34
          .byte 0x39
          .byte 0x8
          .byte 0xff
          .byte 0xff
          .byte 0x39
          .byte 0x4a
          .byte 0xff
          .byte 0xfc
          .byte 0x79
          .byte 0x5
          .byte 0x0
          .byte 0x20
          .byte 0x78
          .byte 0xa7
          .byte 0x17
          .byte 0x64
          .byte 0x7c
          .byte 0xe6
          .byte 0x3a
          .byte 0x14
          .byte 0x85
          .byte 0x9
          .byte 0x0
          .byte 0x4
          .byte 0x7f
          .byte 0xa9
          .byte 0x38
          .byte 0x0
          .byte 0x95
          .byte 0xa
          .byte 0x0
          .byte 0x4
          .byte 0x40
          .byte 0x9e
          .byte 0xff
          .byte 0xf4
          .byte 0x38
          .byte 0xa5
          .byte 0x0
          .byte 0x1
          .byte 0x78
          .byte 0xa5
          .byte 0x17
          .byte 0x64
          .byte 0x7c
          .byte 0xc6
          .byte 0x2a
          .byte 0x14
          .byte 0x81
          .byte 0x46
          .byte 0x0
          .byte 0x0
          .byte 0x39
          .byte 0x26
          .byte 0x0
          .byte 0x4
          .byte 0x2f
          .byte 0x8a
          .byte 0xff
          .byte 0xff
          .byte 0x40
          .byte 0x9e
          .byte 0xff
          .byte 0xb0
          .byte 0x3d
          .byte 0x40
          .byte 0x80
          .byte 0x0
          .byte 0x39
          .byte 0x29
          .byte 0xff
          .byte 0xfc
          .byte 0x79
          .byte 0x4a
          .byte 0x7
          .byte 0xc6
          .byte 0x38
          .byte 0xe0
          .byte 0x0
          .byte 0x0
          .byte 0x65
          .byte 0x4a
          .byte 0x1
          .byte 0x0
          .byte 0x7d
          .byte 0x46
          .byte 0x53
          .byte 0x78
          .byte 0x48
          .byte 0x0
          .byte 0x0
          .byte 0xc
          .byte 0x2b
          .byte 0x87
          .byte 0x0
          .byte 0x2
          .byte 0x41
          .byte 0x9d
          .byte 0x0
          .byte 0x30
          .byte 0x85
          .byte 0x9
          .byte 0x0
          .byte 0x4
          .byte 0x2f
          .byte 0x88
          .byte 0xff
          .byte 0xff
          .byte 0x91
          .byte 0xa
          .byte 0x0
          .byte 0x0
          .byte 0x39
          .byte 0x4a
          .byte 0x0
          .byte 0x4
          .byte 0x40
          .byte 0x9e
          .byte 0xff
          .byte 0xe8
          .byte 0x38
          .byte 0xe7
          .byte 0x0
          .byte 0x1
          .byte 0x78
          .byte 0xea
          .byte 0x60
          .byte 0x28
          .byte 0x78
          .byte 0xe7
          .byte 0x0
          .byte 0x20
          .byte 0x7d
          .byte 0x4a
          .byte 0x32
          .byte 0x14
          .byte 0x2b
          .byte 0x87
          .byte 0x0
          .byte 0x2
          .byte 0x40
          .byte 0x9d
          .byte 0xff
          .byte 0xd8
          .byte 0x3d
          .byte 0x20
          .byte 0x80
          .byte 0x0
          .byte 0x3d
          .byte 0x40
          .byte 0x80
          .byte 0x0
          .byte 0x61
          .byte 0x29
          .byte 0x2
          .byte 0x0
          .byte 0x79
          .byte 0x4a
          .byte 0x7
          .byte 0xc6
          .byte 0x79
          .byte 0x29
          .byte 0x7
          .byte 0xc6
          .byte 0x65
          .byte 0x4a
          .byte 0x1
          .byte 0x0
          .byte 0x65
          .byte 0x29
          .byte 0xc8
          .byte 0x9
          .byte 0x39
          .byte 0x0
          .byte 0x0
          .byte 0x60
          .byte 0x61
          .byte 0x4a
          .byte 0x2f
          .byte 0xff
          .byte 0x61
          .byte 0x29
          .byte 0x4f
          .byte 0xff
          .byte 0x7d
          .byte 0x9
          .byte 0x3
          .byte 0xa6
          .byte 0x8d
          .byte 0x9
          .byte 0x0
          .byte 0x1
          .byte 0x9d
          .byte 0xa
          .byte 0x0
          .byte 0x1
          .byte 0x42
          .byte 0x0
          .byte 0xff
          .byte 0xf8
          .byte 0x38
          .byte 0x21
          .byte 0x0
          .byte 0xc0
          .byte 0x38
          .byte 0x60
          .byte 0x0
          .byte 0x0
          .byte 0xe8
          .byte 0x1
          .byte 0x0
          .byte 0x10
          .byte 0xea
          .byte 0xc1
          .byte 0xff
          .byte 0xb0
          .byte 0xea
          .byte 0xe1
          .byte 0xff
          .byte 0xb8
          .byte 0x7c
          .byte 0x8
          .byte 0x3
          .byte 0xa6
          .byte 0xeb
          .byte 0x1
          .byte 0xff
          .byte 0xc0
          .byte 0xeb
          .byte 0x21
          .byte 0xff
          .byte 0xc8
          .byte 0xeb
          .byte 0x41
          .byte 0xff
          .byte 0xd0
          .byte 0xeb
          .byte 0x61
          .byte 0xff
          .byte 0xd8
          .byte 0xeb
          .byte 0x81
          .byte 0xff
          .byte 0xe0
          .byte 0xeb
          .byte 0xa1
          .byte 0xff
          .byte 0xe8
          .byte 0xeb
          .byte 0xc1
          .byte 0xff
          .byte 0xf0
          .byte 0xeb
          .byte 0xe1
          .byte 0xff
          .byte 0xf8
          .byte 0x4e
          .byte 0x80
          .byte 0x0
          .byte 0x20
          .byte 0x68
          .byte 0x7e
          .byte 0x0
          .byte 0x60
          .byte 0x7f
          .byte 0xde
          .byte 0x0
          .byte 0x34
          .byte 0x57
          .byte 0xde
          .byte 0xd9
          .byte 0x7e
          .byte 0x7b
          .byte 0xde
          .byte 0x0
          .byte 0x20
          .byte 0x4b
          .byte 0xff
          .byte 0xfd
          .byte 0xfc
          .byte 0x61
          .byte 0x29
          .byte 0x2
          .byte 0x0
          .byte 0x79
          .byte 0x29
          .byte 0x7
          .byte 0xc6
          .byte 0x65
          .byte 0x29
          .byte 0xc8
          .byte 0x9
          .byte 0x61
          .byte 0x29
          .byte 0x10
          .byte 0x4
          .byte 0x4b
          .byte 0xff
          .byte 0xff
          .byte 0x18
          .byte 0x3f
          .byte 0xa0
          .byte 0x80
          .byte 0x0
          .byte 0x60
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x63
          .byte 0xbd
          .byte 0x2
          .byte 0x0
          .byte 0x38
          .byte 0x62
          .byte 0x82
          .byte 0x20
          .byte 0x7b
          .byte 0xbd
          .byte 0x7
          .byte 0xc6
          .byte 0x3f
          .byte 0x40
          .byte 0x2
          .byte 0x0
          .byte 0x4b
          .byte 0xff
          .byte 0xfa
          .byte 0x91
          .byte 0x3d
          .byte 0x40
          .byte 0x80
          .byte 0x0
          .byte 0x7f
          .byte 0xa9
          .byte 0xeb
          .byte 0x78
          .byte 0x67
          .byte 0xbd
          .byte 0xea
          .byte 0x0
          .byte 0x79
          .byte 0x4a
          .byte 0x7
          .byte 0xc6
          .byte 0x7f
          .byte 0xbe
          .byte 0xeb
          .byte 0x78
          .byte 0x7f
          .byte 0xbf
          .byte 0xeb
          .byte 0x78
          .byte 0x7f
          .byte 0xab
          .byte 0xeb
          .byte 0x78
          .byte 0x7f
          .byte 0xa3
          .byte 0xeb
          .byte 0x78
          .byte 0x7f
          .byte 0xa4
          .byte 0xeb
          .byte 0x78
          .byte 0x7f
          .byte 0xa5
          .byte 0xeb
          .byte 0x78
          .byte 0x7f
          .byte 0xa6
          .byte 0xeb
          .byte 0x78
          .byte 0x65
          .byte 0x4a
          .byte 0x1c
          .byte 0x3
          .byte 0x65
          .byte 0x29
          .byte 0xc8
          .byte 0x9
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x63
          .byte 0xa7
          .byte 0x30
          .byte 0x20
          .byte 0x63
          .byte 0xa8
          .byte 0x50
          .byte 0x20
          .byte 0x3b
          .byte 0x60
          .byte 0x8
          .byte 0x0
          .byte 0x3f
          .byte 0x80
          .byte 0xff
          .byte 0xff
          .byte 0x63
          .byte 0xbd
          .byte 0x30
          .byte 0x28
          .byte 0x63
          .byte 0xde
          .byte 0x50
          .byte 0x28
          .byte 0x63
          .byte 0xff
          .byte 0x30
          .byte 0x60
          .byte 0x90
          .byte 0x1d
          .byte 0x0
          .byte 0x0
          .byte 0x61
          .byte 0x6b
          .byte 0x50
          .byte 0x60
          .byte 0x90
          .byte 0x1e
          .byte 0x0
          .byte 0x0
          .byte 0x60
          .byte 0x63
          .byte 0x30
          .byte 0x2c
          .byte 0x93
          .byte 0x47
          .byte 0x0
          .byte 0x0
          .byte 0x60
          .byte 0x84
          .byte 0x50
          .byte 0x2c
          .byte 0x93
          .byte 0x48
          .byte 0x0
          .byte 0x0
          .byte 0x60
          .byte 0xa5
          .byte 0x30
          .byte 0x24
          .byte 0x93
          .byte 0x67
          .byte 0x0
          .byte 0x0
          .byte 0x60
          .byte 0xc6
          .byte 0x50
          .byte 0x24
          .byte 0x93
          .byte 0x68
          .byte 0x0
          .byte 0x0
          .byte 0x3f
          .byte 0x20
          .byte 0x0
          .byte 0x1
          .byte 0x90
          .byte 0x1f
          .byte 0x0
          .byte 0x0
          .byte 0x61
          .byte 0x4a
          .byte 0xff
          .byte 0xfc
          .byte 0x90
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x61
          .byte 0x29
          .byte 0x50
          .byte 0x5c
          .byte 0x90
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x7f
          .byte 0x29
          .byte 0x3
          .byte 0xa6
          .byte 0x90
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x93
          .byte 0x85
          .byte 0x0
          .byte 0x0
          .byte 0x93
          .byte 0x86
          .byte 0x0
          .byte 0x0
          .byte 0x60
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x85
          .byte 0x9
          .byte 0x0
          .byte 0x4
          .byte 0x95
          .byte 0xa
          .byte 0x0
          .byte 0x4
          .byte 0x42
          .byte 0x0
          .byte 0xff
          .byte 0xf8
          .byte 0x38
          .byte 0x21
          .byte 0x0
          .byte 0xc0
          .byte 0x3d
          .byte 0x22
          .byte 0x0
          .byte 0x7
          .byte 0x38
          .byte 0x60
          .byte 0x0
          .byte 0x1
          .byte 0x39
          .byte 0x40
          .byte 0x0
          .byte 0x1
          .byte 0xe8
          .byte 0x1
          .byte 0x0
          .byte 0x10
          .byte 0x91
          .byte 0x49
          .byte 0x75
          .byte 0x30
          .byte 0xea
          .byte 0xc1
          .byte 0xff
          .byte 0xb0
          .byte 0xea
          .byte 0xe1
          .byte 0xff
          .byte 0xb8
          .byte 0x7c
          .byte 0x8
          .byte 0x3
          .byte 0xa6
          .byte 0xeb
          .byte 0x1
          .byte 0xff
          .byte 0xc0
          .byte 0xeb
          .byte 0x21
          .byte 0xff
          .byte 0xc8
          .byte 0xeb
          .byte 0x41
          .byte 0xff
          .byte 0xd0
          .byte 0xeb
          .byte 0x61
          .byte 0xff
          .byte 0xd8
          .byte 0xeb
          .byte 0x81
          .byte 0xff
          .byte 0xe0
          .byte 0xeb
          .byte 0xa1
          .byte 0xff
          .byte 0xe8
          .byte 0xeb
          .byte 0xc1
          .byte 0xff
          .byte 0xf0
          .byte 0xeb
          .byte 0xe1
          .byte 0xff
          .byte 0xf8
          .byte 0x4e
          .byte 0x80
          .byte 0x0
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1
          .byte 0x80
          .byte 0xa
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0xa0
          .byte 0xff
          .byte 0xff
          .byte 0x60
          .byte 0xa5
          .byte 0xff
          .byte 0xf1
          .byte 0x7c
          .byte 0xa5
          .byte 0x18
          .byte 0x38
          .byte 0x7c
          .byte 0x65
          .byte 0x18
          .byte 0x50
          .byte 0x7c
          .byte 0x84
          .byte 0x1a
          .byte 0x14
          .byte 0x7c
          .byte 0x0
          .byte 0x28
          .byte 0x6c
          .byte 0x30
          .byte 0xa5
          .byte 0x0
          .byte 0x80
          .byte 0x34
          .byte 0x84
          .byte 0xff
          .byte 0x80
          .byte 0x40
          .byte 0x80
          .byte 0xff
          .byte 0xf4
          .byte 0x4c
          .byte 0x0
          .byte 0x1
          .byte 0x2c
          .byte 0x4e
          .byte 0x80
          .byte 0x0
          .byte 0x20
          .byte 0x3c
          .byte 0xa0
          .byte 0xff
          .byte 0xff
          .byte 0x60
          .byte 0xa5
          .byte 0xff
          .byte 0xf1
          .byte 0x7c
          .byte 0xa5
          .byte 0x18
          .byte 0x38
          .byte 0x7c
          .byte 0x65
          .byte 0x18
          .byte 0x50
          .byte 0x7c
          .byte 0x84
          .byte 0x1a
          .byte 0x14
          .byte 0x7c
          .byte 0x0
          .byte 0x28
          .byte 0xac
          .byte 0x30
          .byte 0xa5
          .byte 0x0
          .byte 0x80
          .byte 0x34
          .byte 0x84
          .byte 0xff
          .byte 0x80
          .byte 0x40
          .byte 0x80
          .byte 0xff
          .byte 0xf4
          .byte 0x4c
          .byte 0x0
          .byte 0x1
          .byte 0x2c
          .byte 0x4e
          .byte 0x80
          .byte 0x0
          .byte 0x20
          .byte 0x3c
          .byte 0xa0
          .byte 0xff
          .byte 0xff
          .byte 0x60
          .byte 0xa5
          .byte 0xff
          .byte 0xf1
          .byte 0x7c
          .byte 0xa5
          .byte 0x18
          .byte 0x38
          .byte 0x7c
          .byte 0x65
          .byte 0x18
          .byte 0x50
          .byte 0x7c
          .byte 0x84
          .byte 0x1a
          .byte 0x14
          .byte 0x7c
          .byte 0x0
          .byte 0x28
          .byte 0x6c
          .byte 0x7c
          .byte 0x0
          .byte 0x4
          .byte 0xac
          .byte 0x7c
          .byte 0x0
          .byte 0x2f
          .byte 0xac
          .byte 0x30
          .byte 0xa5
          .byte 0x0
          .byte 0x80
          .byte 0x34
          .byte 0x84
          .byte 0xff
          .byte 0x80
          .byte 0x40
          .byte 0x80
          .byte 0xff
          .byte 0xec
          .byte 0x7c
          .byte 0x0
          .byte 0x4
          .byte 0xac
          .byte 0x4c
          .byte 0x0
          .byte 0x1
          .byte 0x2c
          .byte 0x4e
          .byte 0x80
          .byte 0x0
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
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
          .byte 0x1
          .byte 0x0
          .byte 0x5
          .byte 0x41
          .byte 0x12
          .byte 0x80
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1
          .byte 0x0
          .byte 0x30
          .byte 0x78
          .byte 0x80
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x2
          .byte 0x48
          .byte 0x80
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x8a
          .byte 0xd0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x80
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x3
          .byte 0x98
          .byte 0x80
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x8a
          .byte 0xd0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x80
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x3
          .byte 0xf0
          .byte 0x80
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x8a
          .byte 0xd0
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
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x3
          .byte 0x80
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x4
          .byte 0x80
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x9
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x9
          .byte 0x80
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xf
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xf
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x13
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x16
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x17
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x18
          .byte 0x0
          .byte 0x21
          .byte 0x53
          .byte 0x57
          .byte 0x49
          .byte 0x54
          .byte 0x43
          .byte 0x48
          .byte 0x0
          .byte 0xa
          .byte 0x20
          .byte 0x20
          .byte 0x5f
          .byte 0x5f
          .byte 0x20
          .byte 0x20
          .byte 0x20
          .byte 0x20
          .byte 0x20
          .byte 0x20
          .byte 0x20
          .byte 0x20
          .byte 0x20
          .byte 0x20
          .byte 0x20
          .byte 0x20
          .byte 0x20
          .byte 0x20
          .byte 0x20
          .byte 0x5f
          .byte 0x5f
          .byte 0x5f
          .byte 0x5f
          .byte 0x20
          .byte 0x20
          .byte 0x20
          .byte 0x5f
          .byte 0x5f
          .byte 0x5f
          .byte 0x20
          .byte 0x20
          .byte 0x20
          .byte 0x5f
          .byte 0x5f
          .byte 0x5f
          .byte 0x20
          .byte 0x5f
          .byte 0x5f
          .byte 0x5f
          .byte 0x5f
          .byte 0x5f
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xa
          .byte 0x20
          .byte 0x2f
          .byte 0x20
          .byte 0x5f
          .byte 0x7c
          .byte 0x5f
          .byte 0x20
          .byte 0x5f
          .byte 0x5f
          .byte 0x20
          .byte 0x5f
          .byte 0x5f
          .byte 0x5f
          .byte 0x20
          .byte 0x20
          .byte 0x5f
          .byte 0x5f
          .byte 0x5f
          .byte 0x7c
          .byte 0x20
          .byte 0x5f
          .byte 0x5f
          .byte 0x20
          .byte 0x29
          .byte 0x20
          .byte 0x2f
          .byte 0x20
          .byte 0x5f
          .byte 0x20
          .byte 0x5c
          .byte 0x20
          .byte 0x2f
          .byte 0x20
          .byte 0x5f
          .byte 0x20
          .byte 0x5c
          .byte 0x5f
          .byte 0x20
          .byte 0x20
          .byte 0x20
          .byte 0x5f
          .byte 0x7c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xa
          .byte 0x7c
          .byte 0x20
          .byte 0x7c
          .byte 0x5f
          .byte 0x7c
          .byte 0x20
          .byte 0x27
          .byte 0x5f
          .byte 0x5f
          .byte 0x2f
          .byte 0x20
          .byte 0x5f
          .byte 0x20
          .byte 0x5c
          .byte 0x2f
          .byte 0x20
          .byte 0x5f
          .byte 0x20
          .byte 0x5c
          .byte 0x20
          .byte 0x20
          .byte 0x5f
          .byte 0x20
          .byte 0x5c
          .byte 0x7c
          .byte 0x20
          .byte 0x7c
          .byte 0x20
          .byte 0x7c
          .byte 0x20
          .byte 0x7c
          .byte 0x20
          .byte 0x7c
          .byte 0x20
          .byte 0x7c
          .byte 0x20
          .byte 0x7c
          .byte 0x7c
          .byte 0x20
          .byte 0x7c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xa
          .byte 0x7c
          .byte 0x20
          .byte 0x20
          .byte 0x5f
          .byte 0x7c
          .byte 0x20
          .byte 0x7c
          .byte 0x20
          .byte 0x7c
          .byte 0x20
          .byte 0x20
          .byte 0x5f
          .byte 0x5f
          .byte 0x2f
          .byte 0x20
          .byte 0x20
          .byte 0x5f
          .byte 0x5f
          .byte 0x2f
          .byte 0x20
          .byte 0x7c
          .byte 0x5f
          .byte 0x29
          .byte 0x20
          .byte 0x7c
          .byte 0x20
          .byte 0x7c
          .byte 0x5f
          .byte 0x7c
          .byte 0x20
          .byte 0x7c
          .byte 0x20
          .byte 0x7c
          .byte 0x5f
          .byte 0x7c
          .byte 0x20
          .byte 0x7c
          .byte 0x7c
          .byte 0x20
          .byte 0x7c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xa
          .byte 0x7c
          .byte 0x5f
          .byte 0x7c
          .byte 0x20
          .byte 0x7c
          .byte 0x5f
          .byte 0x7c
          .byte 0x20
          .byte 0x20
          .byte 0x5c
          .byte 0x5f
          .byte 0x5f
          .byte 0x5f
          .byte 0x7c
          .byte 0x5c
          .byte 0x5f
          .byte 0x5f
          .byte 0x5f
          .byte 0x7c
          .byte 0x5f
          .byte 0x5f
          .byte 0x5f
          .byte 0x5f
          .byte 0x2f
          .byte 0x20
          .byte 0x5c
          .byte 0x5f
          .byte 0x5f
          .byte 0x5f
          .byte 0x2f
          .byte 0x20
          .byte 0x5c
          .byte 0x5f
          .byte 0x5f
          .byte 0x5f
          .byte 0x2f
          .byte 0x20
          .byte 0x7c
          .byte 0x5f
          .byte 0x7c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xa
          .byte 0x20
          .byte 0x20
          .byte 0x20
          .byte 0x20
          .byte 0x20
          .byte 0x20
          .byte 0x20
          .byte 0x20
          .byte 0x20
          .byte 0x20
          .byte 0x20
          .byte 0x20
          .byte 0x20
          .byte 0x5b
          .byte 0x76
          .byte 0x30
          .byte 0x2e
          .byte 0x31
          .byte 0x30
          .byte 0x20
          .byte 0x2d
          .byte 0x20
          .byte 0x69
          .byte 0x6e
          .byte 0x73
          .byte 0x70
          .byte 0x69
          .byte 0x72
          .byte 0x65
          .byte 0x64
          .byte 0x20
          .byte 0x62
          .byte 0x79
          .byte 0x20
          .byte 0x69
          .byte 0x6b
          .byte 0x61
          .byte 0x72
          .byte 0x69
          .byte 0x5d
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xa
          .byte 0x62
          .byte 0x6f
          .byte 0x6f
          .byte 0x74
          .byte 0x69
          .byte 0x6e
          .byte 0x67
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x78
          .byte 0x65
          .byte 0x6c
          .byte 0x6c
          .byte 0x2e
          .byte 0x2e
          .byte 0x2e
          .byte 0x2e
          .byte 0xa
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x66
          .byte 0x69
          .byte 0x72
          .byte 0x6d
          .byte 0x77
          .byte 0x61
          .byte 0x72
          .byte 0x65
          .byte 0x20
          .byte 0x76
          .byte 0x2e
          .byte 0x58
          .byte 0x58
          .byte 0x58
          .byte 0x58
          .byte 0x58
          .byte 0x58
          .byte 0x58
          .byte 0x58
          .byte 0x58
          .byte 0x58
          .byte 0x58
          .byte 0x58
          .byte 0x58
          .byte 0x58
          .byte 0x58
          .byte 0x58
          .byte 0x58
          .byte 0x58
          .byte 0x58
          .byte 0x58
          .byte 0x58
          .byte 0x58
          .byte 0x58
          .byte 0x58
          .byte 0x58
          .byte 0x58
          .byte 0x58
          .byte 0x58
          .byte 0x58
          .byte 0x58
          .byte 0x58
          .byte 0x58
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x61
          .byte 0x6c
          .byte 0x74
          .byte 0x20
          .byte 0x66
          .byte 0x69
          .byte 0x72
          .byte 0x6d
          .byte 0x77
          .byte 0x61
          .byte 0x72
          .byte 0x65
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0

.section .rdata,"dr"
.p2align 2
_bd_458ca4:
          .string "rb"
          .zero 1
_bd_458ca8:
          .string "\n******WARNING: '%s' is a 0 byte file, loading skipped!\n"
_bd_458ce1:
          .string "reading %s (0x%x bytes)"
_bd_458cf9:
          .string "\n"
          .zero 1
_bd_458cfc:
          .string "reading %s (0x%x b pad 0x%x b)"
_bd_458d1b:
          .string " (crc32: 0x%08x ini: 0x%08x)\n"
          .zero 3
_bd_458d3c:
          .string "\n******WARNING: '%s' crc32: 0x%08x expected: 0x%08x\n"
          .zero 3
_bd_458d74:
          .string "**** using default time!!! ****\n"
          .zero 3
_bd_458d98:
          .string "**** %s metadata found, not using system time *****\n\n"
          .zero 2
L_458dd0:
          .string "extracted SUPD/%s (0x%x bytes)"
          .zero 1
L_458df0:
          .string "extracted nanddump/%s (0x%x bytes)"
          .zero 1
L_458e14:
          .string "extracted USVR/%s (0x%x bytes)"
          .zero 1
L_458e34:
          .string "\n***** ERROR: could not append %s%s into patches, not enough room!\n\n"
          .zero 3
L_458e7c:
          .string "\n***** ERROR: could %s%s size 0x%x is not a multiple of 4, discarding patch data!\n\n"
L_458ed0:
          .string "\n***** WARNING: could not load addon patch %s%s!\n\n"
          .zero 1
L_458f04:
          .string "added 0x%x bytes to patches via %d external patch files\n    patches now 0x%x bytes total with addon byte count appended\n"
          .zero 3
_bd_458f80:
          .byte 0x54
          .byte 0x61
          .byte 0x72
          .byte 0x67
          .byte 0x65
          .byte 0x74
          .byte 0x20
          .byte 0x74
          .byte 0x65
          .byte 0x6d
          .byte 0x70
          .byte 0x73
          .byte 0x3a
          .byte 0x20
          .byte 0x43
          .byte 0x70
          .byte 0x75
          .byte 0x3a
          .byte 0x20
          .byte 0x25
          .byte 0x33
          .byte 0x64
          .byte 0xf8
          .byte 0x43
          .byte 0x20
          .byte 0x47
          .byte 0x70
          .byte 0x75
          .byte 0x3a
          .byte 0x20
          .byte 0x25
          .byte 0x33
          .byte 0x64
          .byte 0xf8
          .byte 0x43
          .byte 0x20
          .byte 0x45
          .byte 0x64
          .byte 0x72
          .byte 0x61
          .byte 0x6d
          .byte 0x3a
          .byte 0x20
          .byte 0x25
          .byte 0x33
          .byte 0x64
          .byte 0xf8
          .byte 0x43
          .byte 0xa
          .byte 0x0
          .byte 0x0
          .byte 0x0
_bd_458fb4:
          .byte 0x4d
          .byte 0x61
          .byte 0x78
          .byte 0x20
          .byte 0x74
          .byte 0x65
          .byte 0x6d
          .byte 0x70
          .byte 0x73
          .byte 0x20
          .byte 0x20
          .byte 0x20
          .byte 0x3a
          .byte 0x20
          .byte 0x43
          .byte 0x70
          .byte 0x75
          .byte 0x3a
          .byte 0x20
          .byte 0x25
          .byte 0x33
          .byte 0x64
          .byte 0xf8
          .byte 0x43
          .byte 0x20
          .byte 0x47
          .byte 0x70
          .byte 0x75
          .byte 0x3a
          .byte 0x20
          .byte 0x25
          .byte 0x33
          .byte 0x64
          .byte 0xf8
          .byte 0x43
          .byte 0x20
          .byte 0x45
          .byte 0x64
          .byte 0x72
          .byte 0x61
          .byte 0x6d
          .byte 0x3a
          .byte 0x20
          .byte 0x25
          .byte 0x33
          .byte 0x64
          .byte 0xf8
          .byte 0x43
          .byte 0xa
          .byte 0x0
_bd_458fe6:
          .string "Cpu Fan     : "
_bd_458ff5:
          .string "%d%%%% (overridden)\n"
_bd_45900a:
          .string "(auto)\n"
_bd_459012:
          .string "Gpu Fan     : "
_bd_459021:
          .string "MAC Address : "
_bd_459030:
          .string "\nAVRegion    : 0x%08x (NTSC-M)\n"
_bd_459050:
          .string "\nAVRegion    : 0x%08x (NTSC-J)\n"
_bd_459070:
          .string "\nAVRegion    : 0x%08x (PAL50)\n"
          .zero 1
_bd_459090:
          .string "\nAVRegion    : 0x%08x (PAL60)\n"
          .zero 1
_bd_4590b0:
          .string "\nAVRegion    : 0x%08x (Unknown)\n"
_bd_4590d1:
          .string "GameRegion  : 0x%04x "
_bd_4590e7:
          .string "(NTSC/US)\n"
_bd_4590f2:
          .string "(NTSC/JAP)\n"
_bd_4590fe:
          .string "(NTSC/KOR)\n"
_bd_45910a:
          .string "(NTSC/HK)\n"
_bd_459115:
          .string "(PAL/EU)\n"
_bd_45911f:
          .string "(PAL/AUS)\n"
_bd_45912a:
          .string "(DEVKIT)\n"
_bd_459134:
          .string "(Unknown)\n"
_bd_45913f:
          .string "DVDRegion   : %d\n"
_bd_459151:
          .string "resetKey    : "
_bd_459160:
          .string "%c"
          .zero 1
_bd_459164:
          .string "Ini value %d for %s is out of range (%d-%d), not using\n"
L_45919c:
          .string "Checking for smc config data patches\n"
L_4591c2:
          .string "cputemp"
L_4591ca:
          .string "gputemp"
L_4591d2:
          .string "edramtemp"
L_4591dc:
          .string "overcputemp"
L_4591e8:
          .string "overgputemp"
L_4591f4:
          .string "overedramtemp"
L_459202:
          .string "cpufan"
          .zero 3
L_45920c:
          .string "***** WARNING: cpu fan speed %d override ignored, not between 40 and 100\n"
L_459256:
          .string "gpufan"
          .zero 3
L_459260:
          .string "****** Warning! SMC config has dvd region as 0, xbox will not play DVD videos like this... forcing it to 1 (NTSC/USA)\n"
          .zero 1
L_4592d8:
          .string "       Please set it in boxdata ini file if you require a different region, and run the builder again\n\n"
L_459340:
          .string "smc config patched!\n"
L_459355:
          .string "smc config was not patched\n"
L_459371:
          .string "---------------------\n"
L_459388:
          .string "***** WARNING: gpu fan speed override setting ignored, not between 40 and 100\n"
L_4593d7:
          .string "-------------------\n"
L_4593ec:
          .string "checking smc_config\n"
L_459401:
          .string "extracting config\n"
L_459414:
          .string "extracting config raw\n"
          .zero 1
L_45942c:
          .string "******* ERROR: extracting config did not work, not enough data to copy!\n"
          .zero 3
L_459478:
          .string "valid SMC config data found at offset 0x%x\n"
L_4594a4:
          .string "------------------\n"
L_4594b8:
          .string "SMC config info:\n"
L_4594ca:
          .string "SMC patched info:\n"
          .zero 3
L_4594e0:
          .string "******* ERROR: unable to find SMC config data!\n"
L_459510:
          .string "\n\n***** ERROR: BL crc check failed! calculated: %08x expected: %08x\n"
          .zero 3
L_459558:
          .string "\n\n***** ERROR: BL size (0x%x) is bigger than the file (0x%x) read in!\n"
          .zero 1
L_4595a0:
          .string "\n\n***** ERROR: BL magic check %c%c for type %d failed!\n"
L_4595d8:
          .long L_429c50
          .long L_429c50
          .long L_429cd0
          .long L_429d00
          .long L_429d80
          .long L_429de0
          .long L_429c50
          .long L_429e20
          .long L_429b80
          .long L_429bd0
          .long L_429d80
          .long L_429de0
          .long L_429c50
          .long L_429cd0
          .long L_429d00
          .long L_429d80
          .long L_429de0
L_45961c:
          .string "\n***** ERROR: %s failed signature check!\n"
L_459646:
          .string "%s signature is good\n"
L_45965c:
          .string "could not check signature of %s, 1BL RSA key not present!\n"
          .zero 1
L_459698:
          .string "%s failed signature check, attempting to resign\n"
          .zero 3
L_4596cc:
          .string "\n***** ERROR: failed to resign %s!\n"
L_4596f0:
          .string "%s resigned successfully!\n"
          .zero 1
L_45970c:
          .string "\n***** ERROR: %s failed signature check, RSA key provided does not match the pub key in SB!\n"
          .zero 3
L_45976c:
          .string "\n***** ERROR: %s failed signature check, RSA key not available for resigning!\n"
          .zero 1
L_4597bc:
          .string "could not locate SB data to check %s!\n"
          .zero 1
L_4597e4:
          .string "%s failed hash check, attempting to correct SE and resign\n"
          .zero 1
L_459820:
          .string "\n***** ERROR: failed to resign SE to correct %s hash!\n"
          .zero 1
L_459858:
          .string "SE resigned successfully to correct %s hash!\n"
          .zero 2
L_459888:
          .string "\n***** ERROR: %s failed hash check, RSA key provided does not match the pub key in SD!\n"
L_4598e0:
          .string "\n***** ERROR: %s failed hash check!\n"
L_459905:
          .string "%s hash from SE is good\n"
          .zero 2
L_459920:
          .string "\n***** ERROR: could not locate SD data to check %s!\n"
_bd_459955:
          .string "none"
          .zero 2
L_45995c:
          .string "loaded %s, could not check signature rsa key not present!\n"
          .zero 1
L_459998:
          .string "\n***** ERROR: loaded %s, but signature check failed!\n"
          .zero 2
L_4599d0:
          .string "loaded %s, signature check passed!\n"
L_4599f4:
          .string "could not read %s%s, using built in payload (0x%x bytes)\n"
          .zero 2
L_459a30:
          .string "could not read %s%s, using built in core (0x%x bytes)\n"
          .zero 1
L_459a68:
          .string "xell not found in perbuild directory, checking firmware /bin folder\n"
          .zero 3
L_459ab0:
          .string "xell not found in firmware /bin folder, checking base path\n"
L_459aec:
          .string "keyvault.bin"
L_459af9:
          .string "KV_dec.bin"
L_459b04:
          .string "reading %s%s failed, using %s from nand dump\n"
L_459b32:
          .string "keyvault_alt.bin"
L_459b43:
          .string "KV_alt_dec.bin"
          .zero 2
L_459b54:
          .string "\n\n***** ERROR: patch size 0x%x is not a multiple of 4!\n"
L_459b8c:
          .string "config.bin"
L_459b97:
          .string "config_raw.bin"
          .zero 2
L_459ba8:
          .string "####### unhandled bl load %d %s\n"
          .zero 3
L_459bcc:
          .string "\n\n**** could not read %s (%i) ****\n\n"
          .zero 3
L_459bf4:
          .long L_42a970
          .long L_42a902
          .long L_42a860
          .long L_42a791
          .long L_42a730
          .long L_42a6a0
          .long L_42a620
          .long L_42a6a0
          .long L_42a6a0
          .long L_42a6a0
          .long L_42a6a0
          .long L_42a6a0
          .long L_42a6a0
          .long L_42a6a0
          .long L_42a6a0
          .long L_42a6a0
          .long L_42a6a0
          .long L_42a6a0
          .long L_42a6a0
          .long L_42a6a0
          .long L_42a6a0
          .long L_42a6a0
          .long L_42a5b0
          .long L_42a562
          .long L_42a4b4
          .long L_42a455
          .long L_42a970
          .long L_42a3d0
L_459c64:
          .string "skipping %s%s as it is in glitch bootloader dump\n"
          .zero 2
L_459c98:
          .string "using keyvault data from console\n"
          .zero 2
L_459cbc:
          .string "\n***** ERROR!: acquiring keyvault data failed!\n"
L_459cec:
          .string "using keyvault alt data from console\n"
          .zero 2
L_459d14:
          .string "using smc configuration from console\n"
          .zero 2
L_459d3c:
          .string "\n***** ERROR!: acquiring smc configuration data failed!\n"
          .zero 3
L_459d78:
          .string "using smc binary from console\n"
          .zero 1
L_459d98:
          .string "\n***** ERROR!: acquiring smc binary data failed!\n"
          .zero 2
L_459dcc:
          .long L_42b1a0
          .long L_42b1a0
          .long L_42b130
          .long L_42b0d0
          .long L_42b070
          .long L_42b043
          .long L_42b043
          .long L_42b043
          .long L_42b043
          .long L_42afb0
          .long L_42afb0
          .long L_42b043
          .long L_42b043
          .long L_42b043
          .long L_42b043
          .long L_42afb0
          .long L_42afb0
          .long L_42b043
          .long L_42b043
          .long L_42b043
          .long L_42afb0
          .long L_42afb0
          .long L_42b1a0
          .long L_42af70
          .long L_42af40
          .long L_42aee0
          .long L_42b1a0
          .long L_42ae20
_bd_459e3c:
          .string "\tPatching header for slower demon/cygnos UART speed\n"
          .zero 3
_bd_459e74:
          .string "\tPatching header for xell power reason\n"
_bd_459e9c:
          .string "\tPatching header for xell alt power reason\n"
_bd_459ec8:
          .string "blmod.bin"
_bd_459ed2:
          .string "sum1:"
_bd_459ed8:
          .string "sum2:"
_bd_459ede:
          .string "sum3:"
_bd_459ee4:
          .string "fin :"
L_459eea:
          .string "Patching BLs..."
L_459efa:
          .string "Done!\n"
          .zero 3
L_459f04:
          .string "Checking patched CD signature..."
L_459f25:
          .string "CBB"
L_459f29:
          .string "CD"
L_459f2c:
          .string "***** WARNING: blmod.bin is 0x%x bytes too large, truncating to 0x%x bytes!\n"
          .zero 3
L_459f7c:
          .string "Adding 0x%x bytes blmod.bin data to %s..."
L_459fa6:
          .string "Fixing up patch set..."
          .zero 3
L_459fc0:
          .string "adding %s at raw offset 0x%08x len 0x%x (end 0x%x, rest in fs)\n"
L_45a000:
          .string "adding %s at raw offset 0x%08x len 0x%x (end 0x%x)\n"
L_45a034:
          .string "retail image, skipping %s\n"
          .zero 1
L_45a050:
          .string "devkit/testkit image, skipping %s\n"
          .zero 1
L_45a074:
          .string "***** WARNING: skipping xell, there doesn't appear to be enough room!\n"
          .zero 1
L_45a0bc:
          .string "    - console power button is being used to %s \n"
          .zero 3
L_45a0f0:
          .string "    - console DVD eject button is being used to %s \n"
          .zero 3
L_45a128:
          .string "    - IR remote power button is being used to %s \n"
          .zero 1
L_45a15c:
          .string "    - IR remote guide/X button is being used to %s \n"
          .zero 3
L_45a194:
          .string "    - IR remote windows button is being used to %s \n"
          .zero 3
L_45a1cc:
          .string "    - KIOSK debug pin is being used to %s \n"
L_45a1f8:
          .string "    - wireless controller powering on console is being used to %s \n"
L_45a23c:
          .string "wired controller (rear top usb port) is being used to %s \n"
          .zero 1
L_45a278:
          .string "wired controller (INVALID FOR FATS!!) is being used to %s \n"
L_45a2b4:
          .string "wired controller (rear middle usb port) is being used to %s \n"
          .zero 2
L_45a2f4:
          .string "wired controller (rear bottom usb port) is being used to %s \n"
          .zero 2
L_45a334:
          .string "wired controller (rear usb port) is being used to %s \n"
          .zero 1
L_45a36c:
          .string "wired controller (front left usb port) is being used to %s \n"
          .zero 3
L_45a3ac:
          .string "wired controller (front top usb port) is being used to %s \n"
L_45a3e8:
          .string "wired controller (front right usb port) is being used to %s \n"
          .zero 2
L_45a428:
          .string "wired controller (front bottom usb port) is being used to %s \n"
          .zero 1
L_45a468:
          .long L_42c951
          .long L_42c973
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42c993
          .long L_42cb80
          .long L_42c9b3
          .long L_42cb80
          .long L_42c9d3
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42ca00
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42cb80
          .long L_42ca23
          .long L_42ca50
          .long L_42ca84
          .long L_42cac0
          .long L_42caf0
          .long L_42c920
_bd_45a590:
          .string "patching freeboot.bin with with kernel version string '%s'\n"
_bd_45a5cc:
          .string "Boot options set:\n"
          .zero 1
_bd_45a5e0:
          .string "    - Set debug UART speed to cygnos/demon compatible\n"
          .zero 1
_bd_45a618:
          .string "    - Tray has to be fully ejected for Xell to start (old nodvd method)\n"
          .zero 3
_bd_45a664:
          .string "    - When powered on, if tray is not fully closed Xell starts\n"
_bd_45a6a4:
          .string "start xell"
          .zero 1
_bd_45a6b0:
          .string "    - UKNOWN POWER REASON, using eject button\n"
_bd_45a6df:
          .string "alternately start xell"
          .zero 2
_bd_45a6f8:
          .string "    - alternate xell button disabled\n"
_bd_45a71e:
          .string "dual boot"
_bd_45a728:
          .string "org version %s\n"
_bd_45a738:
          .string "fin version %s\n"
_bd_45a748:
          .string "**** ERROR PATCHING FREEBOOT.BIN for kernel version string!\n"
_bd_45a785:
          .string "9199"
          .zero 2
_bd_45a78c:
          .string "9199 ini string detected, patching to old hold address\n"
_bd_45a7c4:
          .string "patching payload.bin to load size 0x%x (0x%x reps)\n"
_bd_45a7f8:
          .string "org li %r4, %02x%02x\n"
_bd_45a80e:
          .string "fin li %r4, %02x%02x\n"
L_45a824:
          .string "encoding %s size 0x%x (JTAG)\n"
          .zero 2
L_45a844:
          .string "\n******* WARNING: CYGNOS, DEMON and NODVD command line options are ignored due to external freeboot.bin!\n\n"
_bd_45a8af:
          .string "encoding %s size 0x%x\n"
L_45a8c6:
          .string "zeropairing SB\n"
          .zero 2
L_45a8d8:
          .string "CPU key is all zeros, zeropairing SB\n"
          .zero 2
L_45a900:
          .string "****** Unhandled BL typ %d ******\n"
          .zero 1
L_45a924:
          .string "CPU key is all zeros, zeropairing CB_B\n"
L_45a94c:
          .string "re-encoding %s size 0x%x\n"
          .zero 2
L_45a968:
          .long L_42d503
          .long L_42d503
          .long L_42d160
          .long L_42d040
          .long L_42d420
          .long L_42d503
          .long L_42d503
          .long L_42d3d3
          .long L_42d391
          .long L_42d350
          .long L_42d4c1
          .long L_42d435
          .long L_42d333
          .long L_42d2d3
          .long L_42d270
          .long L_42d200
          .long L_42d190
          .long L_42d503
          .long L_42d503
          .long L_42d503
          .long L_42d503
          .long L_42d503
          .long L_42d503
          .long L_42d050
          .long L_42d050
          .long L_42d050
L_45a9d0:
          .long L_42d050
          .long L_42d050
          .long L_42d160
          .long L_42d040
          .long L_42d050
          .long L_42d823
          .long L_42d6e0
          .long L_42d660
          .long L_42d613
          .long L_42d5d2
          .long L_42d590
L_45a9fc:
          .long L_42d050
          .long L_42daa8
          .long L_42d160
          .long L_42d040
          .long L_42d050
          .long L_42d967
          .long L_42d050
          .long L_42de40
          .long L_42d050
          .long L_42ddff
          .long L_42ddbb
          .long L_42d050
          .long L_42d050
          .long L_42d050
          .long L_42d050
          .long L_42d050
          .long L_42d050
          .long L_42dd51
          .long L_42dd0f
          .long L_42dcc5
          .long L_42dc54
          .long L_42dc12
          .long L_42dbc9
L_45aa58:
          .string "***** WARNING: xell is unexpectedly larger than 256KiB!!\n"
          .zero 2
L_45aa94:
          .string "Writing initial header to flash image\n"
          .zero 1
L_45aabc:
          .string "\n------ Copying bootloader image to flash image ------ \n"
          .zero 3
L_45aaf8:
          .string "******* ERROR: bootloaders retrieved from console are inconsistent, cannot proceed!\n\n"
          .zero 2
L_45ab50:
          .string "\n------ Loading bootloaders and required security files ------\n"
L_45ab90:
          .string "******* ERROR: critical bootloader files are missing, cannot proceed!\n\n"
L_45abd8:
          .string "done!\n"
          .zero 1
L_45abe0:
          .string "\n------ Patching BLs and modifying patches ------\n"
          .zero 1
L_45ac14:
          .string "\n------ Patching boot reasons and options into flash header ------\n"
L_45ac58:
          .string "\n------ Encrypting and finalizing bootloaders ------\n"
L_45ac8e:
          .string "\nVirtual Fuses set to:"
          .zero 3
L_45aca8:
          .string "done!\n\n------ Adding bootloaders to flash image ------\n"
L_45ace0:
          .string "Fixing up FS table..."
          .zero 2
L_45acf8:
          .string "Writing zeropair CG patch slot overflow data to sysupdate.xexp1\n"
          .zero 3
L_45ad3c:
          .string "\tat raw offset 0x%x len 0x%08x (end: 0x%08x)..."
L_45ad6c:
          .string "sysupdate.xexp1"
L_45ad7c:
          .string "Writing CG patch slot overflow data to sysupdate.xexp1\n"
L_45adb4:
          .string "Writing target CG patch slot overflow data to sysupdate.xexp2\n"
L_45adf3:
          .string "sysupdate.xexp2"
          .zero 1
L_45ae04:
          .string "\n------ adding %d firmware files ------\n"
          .zero 3
L_45ae30:
          .string "\n------ adding %d security files ------\n"
L_45ae59:
          .string "sysupdate.xexp"
L_45ae68:
          .string "\n******* WARNING: firmware file %s ignored, 'sysupdate.xexp' is a reserved name!\n\n"
          .zero 1
L_45aebc:
          .string "\tadding as %s at raw offset 0x%x len 0x%08x (end 0x%08x)\n"
          .zero 2
L_45aef8:
          .string "***** could not read file '%s', skipping *****\n"
L_45af28:
          .string "***** could not read file '%s' *****\n"
          .zero 2
L_45af50:
          .string "\n******* ERROR: critical firmware file missing, cannot proceed!\n\n"
          .zero 2
L_45af94:
          .string "\n------ checking for Mobile*.dat ------\n"
L_45afbd:
          .string "<- Processing %s ->\n"
          .zero 2
L_45afd4:
          .string "\tcould not read %s, using data from SUPD...\n"
          .zero 3
L_45b004:
          .string "\tcould not read %s, using data from previous parse...\n"
L_45b03b:
          .string "secdata.bin"
L_45b047:
          .string "extended.bin"
L_45b054:
          .string "dae.bin"
L_45b05c:
          .string "crl.bin"
L_45b064:
          .string "fcrt.bin"
L_45b06d:
          .string "odd.bin"
          .zero 3
L_45b078:
          .string "******* WARNING: writing %s%s as-is to NAND, if .meta was not included it may be invalid!\n"
          .zero 1
L_45b0d4:
          .string "\n\n***** ERROR: %s not found, keyvault has this file flagged as required but it's being skipped *****\n"
          .zero 2
L_45b13c:
          .string "             note - on hacked images a nofcrt patch should allow the drive and machine to function\n"
L_45b1a0:
          .string "             note - on hacked images a nofcrt patch WILL NOT allow the drive to function\n"
          .zero 2
L_45b1fc:
          .string "             but should allow the machine to boot normally\n"
L_45b238:
          .string "\t%s not found and not required by keyvault, skipped\n"
          .zero 3
L_45b270:
          .string "***** WARNING: %s not found, skipping *****\n"
L_45b29d:
          .string "%s found, adding from file\n"
          .zero 3
L_45b2bc:
          .string "%s found, adding from previous parse\n"
          .zero 2
L_45b2e4:
          .string "\n------ adding smc_config.bin ------\n"
          .zero 2
L_45b30c:
          .string "\n------ cleaning up image ------\n"
          .zero 2
L_45b330:
          .string "Fixing up empty FS block entries..."
L_45b354:
          .string "done!\nWriting FS table to image "
          .zero 3
L_45b378:
          .string "\n------ adding [rawpatch] data ------\n"
          .zero 1
L_45b3a0:
          .string "[rawpatch] (%d): '%s' copied to offset 0x%x len: 0x%x (end: 0x%x) successfully!\n\n"
          .zero 2
L_45b3f4:
          .string "[rawpatch] (%d): '%s' copied to offset 0x%x (len: 0x%x) would exceed user size 0x%x!\n\n"
          .zero 1
L_45b44c:
          .string "***** ERROR: could not load [rawpatch] file '%s'!!\n"
L_45b480:
          .string "\n------ finalizing image ------\n"
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
          .byte 0x5c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _loadBaseFile - .
          .byte 0x4e
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x4e
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
          .byte 0xb0
          .byte 0x8
          .byte 0x2
          .byte 0xe5
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
          .byte 0x66
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
          .byte 0x4c
          .byte 0xe
          .byte 0xb0
          .byte 0x8
          .byte 0x83
          .byte 0x5
          .byte 0x85
          .byte 0x2
          .byte 0x86
          .byte 0x4
          .byte 0x87
          .byte 0x3
          .byte 0x0
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x7c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _findFileOffset - .
          .byte 0x49
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x47
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x71
          .byte 0xa
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x49
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
          .byte 0xa0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _findFileSize - .
          .byte 0x49
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x47
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x71
          .byte 0xa
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x49
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x18
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _findFile - .
          .byte 0x39
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x47
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x71
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x6c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xe0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _loadFileCrc - .
          .byte 0x14
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
          .byte 0x40
          .byte 0x3
          .byte 0x6e
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
          .byte 0x47
          .byte 0xb
          .byte 0x2
          .byte 0x47
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
          .byte 0x63
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
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x50
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _readMetaFile - .
          .byte 0x57
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
          .byte 0x47
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x44
          .byte 0xb
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x74
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _makeTimestamp - .
          .byte 0xc0
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
          .byte 0x50
          .byte 0x2
          .byte 0x87
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
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb4
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _timestampToFileTime - .
          .byte 0x34
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x70
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xcc
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _loadBaseFileMeta - .
          .byte 0xa
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
          .byte 0xb0
          .byte 0x8
          .byte 0x3
          .byte 0xb
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
          .byte 0x47
          .byte 0xb
          .byte 0x2
          .byte 0xc6
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
          .byte 0x84
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x24
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long _loadCommonFile - .
          .byte 0x74
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
          .byte 0xe0
          .byte 0x8
          .byte 0x3
          .byte 0xc0
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
          .byte 0x42
          .byte 0xb
          .byte 0x2
          .byte 0xb6
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
          .byte 0x66
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
          .byte 0x6d
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
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xac
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long _loadInputFile - .
          .byte 0x3a
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
          .byte 0x46
          .byte 0xe
          .byte 0xf0
          .byte 0x8
          .byte 0x2
          .byte 0xd1
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
          .byte 0x73
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
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x4
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long _loadBinFile - .
          .byte 0x3e
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
          .byte 0x8
          .byte 0x2
          .byte 0xe8
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
          .byte 0x66
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
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x5c
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long _loadLocalFile - .
          .byte 0xf4
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
          .byte 0x8
          .byte 0x2
          .byte 0xd8
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
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x9c
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long _setFileData - .
          .byte 0x50
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
          .byte 0x2
          .byte 0x48
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
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc8
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long _appendAddonPatches - .
          .byte 0x3
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
          .byte 0x3
          .byte 0xbd
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
          .byte 0x48
          .byte 0xb
          .byte 0x2c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long _showSmcConfig - .
          .byte 0x59
          .byte 0x4
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
          .byte 0x70
          .byte 0x3
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
          .byte 0x49
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long _iniRangeOk - .
          .byte 0x66
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x40
          .byte 0x58
          .byte 0xa
          .byte 0xe
          .byte 0x4
          .byte 0x45
          .byte 0xb
          .byte 0x2
          .byte 0x45
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x2c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x58
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long _patchSmcConfig - .
          .byte 0xda
          .byte 0x5
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
          .byte 0xf6
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
          .byte 0x41
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x88
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long _extractSmcConfig - .
          .byte 0x33
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
          .byte 0x40
          .byte 0x3
          .byte 0xca
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
          .byte 0x4b
          .byte 0xb
          .byte 0x2
          .byte 0x50
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
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xe0
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long _raiseKernel - .
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x58
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xf4
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long _checkBl - .
          .byte 0x3d
          .byte 0x3
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
          .byte 0x95
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
          .byte 0x42
          .byte 0xb
          .byte 0x3
          .byte 0x40
          .byte 0x2
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
          .byte 0x48
          .byte 0xb
          .byte 0x73
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
          .byte 0x45
          .byte 0xb
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x50
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .long _verifyBlSigs - .
          .byte 0xff
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
          .byte 0x50
          .byte 0x2
          .byte 0xc1
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
          .byte 0x90
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .long _loadBlFiles - .
          .byte 0x4d
          .byte 0xa
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
          .byte 0x48
          .byte 0xe
          .byte 0x50
          .byte 0x2
          .byte 0xd2
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
          .byte 0x3
          .byte 0xa3
          .byte 0x4
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
          .byte 0x5c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xe8
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .long _loadConsoleBlFiles - .
          .byte 0xef
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x4e
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
          .byte 0x48
          .byte 0xe
          .byte 0x50
          .byte 0x2
          .byte 0xf1
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
          .byte 0x2
          .byte 0x88
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
          .byte 0x3c
          .byte 0x3
          .byte 0xe
          .byte 0x4
          .byte 0xc3
          .byte 0xc5
          .byte 0xc6
          .byte 0xc7
          .byte 0x0
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x48
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .long _patchHeaderOpts - .
          .byte 0x1f
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x45
          .byte 0xe
          .byte 0x20
          .byte 0x2
          .byte 0x92
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x47
          .byte 0xb
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x6c
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .long _blmodMissing - .
          .byte 0x1d
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x10
          .byte 0x56
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x84
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .long _rotSumSha - .
          .byte 0x17
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x48
          .byte 0xe
          .byte 0xa0
          .byte 0x1
          .byte 0x3
          .byte 0xc
          .byte 0x2
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xa8
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .long _countBits - .
          .byte 0x4d
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x6c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xbc
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .long _patchBlsResign - .
          .byte 0xae
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
          .byte 0x70
          .byte 0x3
          .byte 0x7d
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
          .byte 0x2
          .byte 0x71
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
          .byte 0x7d
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
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x2c
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .long _patchBlsBlmod - .
          .byte 0x52
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
          .byte 0x60
          .byte 0x3
          .byte 0x84
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
          .byte 0x45
          .byte 0xb
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x6c
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .long _fixupPatchSet - .
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
          .byte 0x40
          .byte 0x2
          .byte 0xc7
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
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xac
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .long _addBlsToImage - .
          .byte 0x68
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
          .byte 0x43
          .byte 0xe
          .byte 0x50
          .byte 0x3
          .byte 0xc0
          .byte 0x4
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
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xec
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .long _isUpdateBl - .
          .byte 0x1d
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .long _addUpdateBls - .
          .byte 0xd7
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
          .byte 0xf9
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
          .byte 0x18
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x40
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .long _logPowerButton - .
          .byte 0xab
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x2
          .byte 0x6f
          .byte 0xa
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x0
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x5c
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .long _patchFreeboot - .
          .byte 0x21
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
          .byte 0x70
          .byte 0x3
          .byte 0x8d
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
          .byte 0x48
          .byte 0xb
          .byte 0x2
          .byte 0x8c
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
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb4
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .long _patchPayloadSize - .
          .byte 0xb4
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
          .byte 0xac
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
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xe0
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .long _encodeBls - .
          .byte 0xb
          .byte 0x10
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
          .byte 0x4d
          .byte 0xe
          .byte 0x60
          .byte 0x3
          .byte 0xa7
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
          .byte 0x44
          .byte 0xb
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x20
          .byte 0x9
          .byte 0x0
          .byte 0x0
          .long _encodeUpdateBls - .
          .byte 0xb0
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
          .byte 0xfe
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
          .byte 0x34
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x60
          .byte 0x9
          .byte 0x0
          .byte 0x0
          .long _calcBlAreaSize - .
          .byte 0xf3
          .byte 0x5
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
          .byte 0x3
          .byte 0x76
          .byte 0x1
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
          .byte 0x9c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x98
          .byte 0x9
          .byte 0x0
          .byte 0x0
          .long _buildFlash - .
          .byte 0xfa
          .byte 0x1c
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
          .byte 0x4b
          .byte 0xe
          .byte 0xb0
          .byte 0x9
          .byte 0x3
          .byte 0x1b
          .byte 0x5
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
          .byte 0x73
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
          .byte 0x3
          .byte 0xd8
          .byte 0xb
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
          .byte 0x3
          .byte 0x67
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
          .byte 0x45
          .byte 0xb
          .byte 0x3
          .byte 0x4e
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
          .byte 0x0

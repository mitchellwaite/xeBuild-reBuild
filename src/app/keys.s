# app/keys.s -- CPU/1BL key setup, SMC/keyvault/CRL input decryption, pairing init
#
# mixed: `#@C name` lines are functions from keys.c (re/splice.py)
#
# original placement:
#   .bss           00479560-00479574
#   .data          0044a5e0-0044a6c0
#   .eh_frame      00468230-00468bd0
#   .rdata         00456664-004574b0
#   .rdata$zzz     00463a38-00463a64
#   .text          0041aa00-0041e800

.intel_syntax noprefix
.globl _cfEncrypt
.globl _cfPatchSlots
.globl _crlKey
.globl _daeEncrypt
.globl _daeKey
.globl _infoKey0
.globl _infoKey1
.globl _infoKey2
.globl _infoKey3
.globl _infoKey4
.globl _infoKey5
.globl _kvAltSalt
.globl _kvSalt
.globl _msg_1blBad
.globl _msg_1blBad2
.globl _msg_1blBadStr
.globl _msg_1blBadStr2
.globl _msg_1blChars
.globl _msg_1blKeySet
.globl _msg_1blLen
.globl _msg_1blSum
.globl _msg_cbb15572
.globl _msg_cbbMfg
.globl _msg_cbencPairing
.globl _msg_cpuKeyChars
.globl _msg_cpuKeyLen
.globl _msg_cpuKeySet
.globl _msg_cpuKeySet2
.globl _msg_cpuKeyWarn
.globl _msg_crlBad
.globl _msg_crlCrypted
.globl _msg_crlRetry
.globl _msg_dualCb
.globl _msg_extDecryptFail
.globl _msg_extEncrypted
.globl _msg_extMissing
.globl _msg_extSize
.globl _msg_fcrtBad
.globl _msg_fcrtOffset
.globl _msg_fcrtSize
.globl _msg_fuseCpuKey
.globl _msg_fuseLdv
.globl _msg_fuseNull
.globl _msg_initRandom
.globl _msg_initStatic
.globl _msg_kvDecryptErr
.globl _msg_kvDecryptFail
.globl _msg_kvEncrypted
.globl _msg_kvHash
.globl _msg_kvNotDecrypted
.globl _msg_kvPreDecrypted
.globl _msg_kvSize
.globl _msg_pairingSet
.globl _msg_sdMissing
.globl _msg_sdSize
.globl _msg_smcBad
.globl _msg_smcClean
.globl _msg_smcCleanType
.globl _msg_smcDevkit
.globl _msg_smcEncrypted
.globl _msg_smcGlitch
.globl _msg_smcHacked
.globl _msg_smcJtag
.globl _msg_smcNoGlitch
.globl _msg_smcNoJtag
.globl _msg_smcRetail
.globl _msg_weight
.globl _msg_xexKeySet
.globl _msg_xexSum
.globl _pairing
.globl _secdataKey
.globl _smcKey
.globl _str_Success
.globl _str_altKv
.globl _str_error
.globl _str_failed
.globl _str_failedNl
.globl _str_hexByte
.globl _str_kv
.globl _str_kvAltBin
.globl _str_kvBin
.globl _str_newline
.globl _str_success
.globl _str_successNl
.globl _str_valid
.globl _zeroKey

.text
.p2align 4
#@C _keysInit
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
#@C _setCrlKey
          .byte 0x8d
          .byte 0x76
          .byte 0x0
#@C _setDaeKey
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
#@C _setSecdataKey
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
#@C _setInfoKey0
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _setInfoKey1
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _setInfoKey2
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _setInfoKey3
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _setInfoKey4
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _setInfoKey5
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _setKvSalt
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
#@C _setKvAltSalt
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
#@C _setSmcKey
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
#@C _setPairing
          .byte 0x66
          .byte 0x90
#@C _checkCpuKey
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _setCpuKeyStr
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _setCpuKey
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
#@C _setFuseLdv
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
#@C _setFuseCpuKey
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
#@C _calcXexKey
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
#@C _check1blKey
L_41b5f7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
#@C _set1blKey
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
#@C _checkKeys
L_41b8d1:
          jmp _smcChecksum
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
#@C _smcChecksum
#@C _smcEncrypt
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
#@C _smcPrepare
L_41bf41:
          jmp _cbaEncrypt
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
#@C _cbaEncrypt
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _cbaEncryptZero
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _cbaEncrypt2
          .byte 0x8d
          .byte 0x76
          .byte 0x0
#@C _cbbEncrypt
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
#@C _cdEncryptZero
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _cdEncrypt
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
#@C _cdEncryptCpu
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
#@C _ceEncrypt
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
_cfPatchSlots:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,12
          mov EBX,DWORD PTR [ESP+32]
          mov EAX,DWORD PTR [ESP+36]
          mov EDX,DWORD PTR [ESP+44]
          mov ECX,DWORD PTR [ESP+40]
          mov ESI,DWORD PTR [EBX+1040]
          mov EBP,DWORD PTR [EBX+1036]
          add EAX,ESI
          cmp EAX,EDX
          jbe L_41c9e2
          sub EAX,EDX
          sub EDX,ESI
          cmp EAX,16384
          mov DWORD PTR [EBX+1064],EDX
          mov DWORD PTR [EBX+1060],EAX
          jbe L_41c9f2
          movzx EBX,CX
          sub EAX,16385
          mov ESI,EBP
          lea EDI,DWORD PTR [EBX-1]
          lea EDX,DWORD PTR [EBX+1]
          shr EAX,14
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],EDI
          lea EDI,DWORD PTR [ECX-1]
          shl ECX,8
          mov WORD PTR [ESP+6],DI
          lea EDI,DWORD PTR [EDX+EAX*1]
          lea EAX,DWORD PTR [EBX+EBX*1]
          sub ESI,EAX
          jmp L_41c993
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_41c990:
          add EDX,1
L_41c993:
          mov EAX,EBX
          shr AX,8
          add EAX,ECX
          add CX,256
          cmp EDX,EDI
          mov WORD PTR [ESI+EBX*2+50],AX
          mov EBX,EDX
          jne L_41c990
          mov EAX,DWORD PTR [ESP+8]
          lea EDX,DWORD PTR [EAX+2]
          add EAX,2
          mov ESI,EAX
          lea ECX,DWORD PTR [EDX+EDX*1]
          mov EBX,EDX
          rol SI,8
L_41c9c0:
          add EDX,DWORD PTR [ESP]
          add BX,WORD PTR [ESP+6]
          shl EBX,8
          shr DX,8
          add EDX,EBX
          mov WORD PTR [EBP+ECX*1+48],DX
          mov WORD PTR [EBP+48],SI
          add ESP,12
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_41c9e2:
          xor ESI,ESI
          xor EAX,EAX
          mov WORD PTR [EBP+48],SI
          add ESP,12
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_41c9f2:
          movzx EAX,CX
          mov ESI,256
          mov EBX,1
          sub EAX,1
          mov EDX,1
          mov DWORD PTR [ESP],EAX
          lea EAX,DWORD PTR [ECX-1]
          mov ECX,2
          mov WORD PTR [ESP+6],AX
          mov EAX,1
          jmp L_41c9c0
          .byte 0x66
          .byte 0x90
_cfEncrypt:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,108
          mov EAX,DWORD PTR [ESP+136]
          mov ESI,DWORD PTR [ESP+140]
          mov EBX,DWORD PTR [ESP+128]
          mov EDX,DWORD PTR [ESP+144]
          mov DWORD PTR [ESP+52],EAX
          mov EAX,DWORD PTR [_infoKey4]
          test ESI,ESI
          mov DWORD PTR [ESP+80],EAX
          mov EAX,DWORD PTR [L_44a668]
          mov DWORD PTR [ESP+84],EAX
          mov EAX,DWORD PTR [L_44a66c]
          mov DWORD PTR [ESP+88],EAX
          mov EAX,DWORD PTR [L_44a670]
          mov DWORD PTR [ESP+92],EAX
          je L_41cb82
          mov EAX,DWORD PTR [EBX+1036]
          mov ECX,DWORD PTR [EBX+1040]
          mov DWORD PTR [ESP+48],EAX
          mov EAX,DWORD PTR [ESP+132]
          add EAX,ECX
          cmp EDX,EAX
          jb L_41cc25
          mov EAX,DWORD PTR [ESP+48]
          xor EDX,EDX
          lea EDI,DWORD PTR [ESP+64]
          xor ESI,ESI
          mov WORD PTR [EAX+48],DX
          lea EAX,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+32],EDI
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],16
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET _key1bl
          call _XeCryptHmacSha
L_41caf4:
          mov EAX,DWORD PTR [EBX+1036]
          mov EDX,DWORD PTR [EAX+828]
          mov ECX,DWORD PTR [EAX+824]
          mov EBP,DWORD PTR [EAX+820]
          mov DWORD PTR [ESP+48],EDX
          mov EDX,DWORD PTR [EAX+816]
          mov DWORD PTR [EBX+1052],ECX
          mov ECX,DWORD PTR [ESP+48]
          mov DWORD PTR [EBX+1048],EBP
          mov DWORD PTR [EBX+1044],EDX
          mov EDX,DWORD PTR [ESP+80]
          mov DWORD PTR [EBX+1056],ECX
          mov DWORD PTR [EAX+32],EDX
          mov EDX,DWORD PTR [ESP+84]
          mov DWORD PTR [EAX+36],EDX
          mov EDX,DWORD PTR [ESP+88]
          mov DWORD PTR [EAX+40],EDX
          mov EDX,DWORD PTR [ESP+92]
          mov DWORD PTR [EAX+44],EDX
          mov EAX,DWORD PTR [EBX+1040]
          sub EAX,48
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [EBX+1036]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],16
          add EAX,48
          mov DWORD PTR [ESP+8],EAX
          call _XeCryptRc4
          add ESP,108
          mov EAX,ESI
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_41cb82:
          mov EDI,DWORD PTR [EBX+1036]
          mov DWORD PTR [EDI+32],0
          mov DWORD PTR [EDI+556],0
          lea ECX,DWORD PTR [EDI+32]
          add EDI,36
          mov EAX,DWORD PTR [ESP+140]
          and EDI,4294967292
          sub ECX,EDI
          add ECX,528
          shr ECX,2
          rep stosd DWORD PTR ES:[EDI]
          cmp DWORD PTR [_g479ea8],2
          mov EAX,DWORD PTR [EBX+1036]
          je L_41cdb0
          mov BYTE PTR [EAX+539],0
L_41cbd0:
          movzx ECX,WORD PTR [_pairing]
          mov EAX,DWORD PTR [EBX+1036]
          mov WORD PTR [EAX+540],CX
          movzx ECX,BYTE PTR [L_479572]
          mov BYTE PTR [EAX+542],CL
          movzx ECX,BYTE PTR [L_479f15]
          mov EAX,DWORD PTR [EBX+1036]
          mov BYTE PTR [EAX+543],CL
          mov EAX,DWORD PTR [EBX+1036]
          mov ECX,DWORD PTR [EBX+1040]
          mov DWORD PTR [ESP+48],EAX
          mov EAX,DWORD PTR [ESP+132]
          add EAX,ECX
          cmp EDX,EAX
          jae L_41cde2
L_41cc25:
          sub EAX,EDX
          sub EDX,ECX
          cmp EAX,16384
          mov DWORD PTR [EBX+1064],EDX
          mov DWORD PTR [EBX+1060],EAX
          jbe L_41cdbc
          mov ECX,DWORD PTR [ESP+52]
          sub EAX,16385
          shr EAX,14
          mov DWORD PTR [ESP+56],EAX
          movzx EDI,CX
          shl ECX,8
          lea EDX,DWORD PTR [EDI+1]
          mov DWORD PTR [ESP+60],EDI
          mov ESI,EDI
          lea EBP,DWORD PTR [EDX+EAX*1]
          lea EAX,DWORD PTR [EDI+EDI*1]
          mov EDI,DWORD PTR [ESP+48]
          sub EDI,EAX
          jmp L_41cc73
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_41cc70:
          add EDX,1
L_41cc73:
          mov EAX,ESI
          shr AX,8
          add EAX,ECX
          add CX,256
          cmp EDX,EBP
          mov WORD PTR [EDI+ESI*2+50],AX
          mov ESI,EDX
          jne L_41cc70
          mov EAX,DWORD PTR [ESP+56]
          lea EDX,DWORD PTR [EAX+2]
          lea ESI,DWORD PTR [EAX+1]
          mov EAX,DWORD PTR [ESP+60]
L_41cc99:
          lea EAX,DWORD PTR [EDX+EAX*1-1]
          mov EDI,DWORD PTR [ESP+48]
          add ESI,1
          mov ECX,EAX
          movzx EAX,WORD PTR [ESP+52]
          shr CX,8
          lea EAX,DWORD PTR [EAX+EDX*1-1]
          shl EAX,8
          add EAX,ECX
          mov WORD PTR [EDI+EDX*2+48],AX
          mov EAX,ESI
          rol AX,8
L_41ccc3:
          mov WORD PTR [EDI+48],AX
          lea EAX,DWORD PTR [ESP+80]
          lea EDI,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+32],EDI
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],16
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET _key1bl
          call _XeCryptHmacSha
          mov ECX,DWORD PTR [ESP+140]
          test ECX,ECX
          jne L_41caf4
L_41cd2a:
          mov EAX,DWORD PTR [EBX+1036]
          mov EDX,DWORD PTR [ESP+64]
          mov DWORD PTR [EAX+32],EDX
          mov EDX,DWORD PTR [ESP+68]
          mov DWORD PTR [EAX+36],EDX
          mov EDX,DWORD PTR [ESP+72]
          mov DWORD PTR [EAX+40],EDX
          mov EDX,DWORD PTR [ESP+76]
          mov DWORD PTR [EAX+44],EDX
          mov EAX,DWORD PTR [EBX+1036]
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+20],0
          lea EDX,DWORD PTR [EAX+544]
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],544
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP+32],EDX
          mov DWORD PTR [ESP],OFFSET _cpuKey
          call _XeCryptHmacSha
          jmp L_41caf4
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_41cdb0:
          mov BYTE PTR [EAX+539],1
          jmp L_41cbd0
L_41cdbc:
          test EAX,EAX
          jne L_41cdcd
          xor EAX,EAX
          xor ESI,ESI
          mov EDI,DWORD PTR [ESP+48]
          jmp L_41ccc3
L_41cdcd:
          movzx EAX,WORD PTR [ESP+52]
          xor ESI,ESI
          mov EDX,1
          mov DWORD PTR [ESP+60],EAX
          jmp L_41cc99
L_41cde2:
          mov EAX,DWORD PTR [ESP+48]
          lea EDI,DWORD PTR [ESP+64]
          xor ESI,ESI
          mov WORD PTR [EAX+48],0
          lea EAX,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+32],EDI
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],16
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET _key1bl
          call _XeCryptHmacSha
          jmp L_41cd2a
L_41ce47:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
#@C _cgEncrypt
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
#@C _kvEncrypt
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _kvEncryptAlt
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _kvPrepare
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
#@C _extendedPrepare
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _secdataPrepare
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
#@C _shaCheck
L_41dc27:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
#@C _crlEncrypt
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _daeEncryptOne
L_41e177:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
_daeEncrypt:
          push EBP
          push EDI
          push ESI
          push EBX
          xor EBX,EBX
          sub ESP,108
          mov EBP,DWORD PTR [ESP+132]
          mov EDI,DWORD PTR [ESP+128]
          mov EAX,DWORD PTR [ESP+136]
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+36],EAX
          call _malloc
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],EDI
          mov ESI,EAX
          mov DWORD PTR [ESP],EAX
          call _memcpy
          test EBP,EBP
          mov DWORD PTR [ESP+32],0
          mov EDX,EBX
          je L_41e210
L_41e1ca:
          lea EBX,DWORD PTR [EDI+EDX*1]
          cmp BYTE PTR [EBX],68
          jne L_41e1d9
          cmp BYTE PTR [EDI+EDX*1+1],65
          je L_41e230
L_41e1d9:
          mov DWORD PTR [ESP+4],OFFSET L_457340
          mov DWORD PTR [ESP],0
          call _log_printf
L_41e1ed:
          cmp DWORD PTR [ESP+32],2
          jne L_41e210
L_41e1f4:
          mov DWORD PTR [ESP+128],ESI
          add ESP,108
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          jmp _free
L_41e207:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_41e210:
          mov DWORD PTR [ESP+4],OFFSET L_457298
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_41e1f4
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_41e230:
          cmp BYTE PTR [EDI+EDX*1+2],69
          jne L_41e1d9
          cmp BYTE PTR [EDI+EDX*1+3],80
          jne L_41e1d9
          movzx EAX,BYTE PTR [EDI+EDX*1+4]
          movzx ECX,BYTE PTR [EDI+EDX*1+5]
          mov DWORD PTR [ESP+56],EDX
          lea EDX,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP+28],20
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+24],EDX
          mov DWORD PTR [ESP+12],0
          shl EAX,8
          mov DWORD PTR [ESP+8],0
          add EAX,ECX
          lea ECX,DWORD PTR [EBX+336]
          movzx EAX,AX
          mov DWORD PTR [ESP+40],EAX
          sub EAX,336
          mov DWORD PTR [ESP],ECX
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP+44],EAX
          mov DWORD PTR [ESP+48],ECX
          call _XeCryptSha
          lea EAX,DWORD PTR [EBX+12]
          lea ECX,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP+8],20
          mov DWORD PTR [ESP+4],ECX
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+52],EAX
          call _memcmp
          test EAX,EAX
          mov EDX,DWORD PTR [ESP+56]
          jne L_41e304
L_41e2ce:
          mov DWORD PTR [ESP+44],EDX
L_41e2d2:
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+4],EAX
          call _daeEncryptOne
          add DWORD PTR [ESP+32],1
          mov EDX,DWORD PTR [ESP+44]
L_41e2f3:
          add EDX,DWORD PTR [ESP+40]
          cmp EBP,EDX
          ja L_41e1ca
          jmp L_41e1ed
L_41e304:
          mov EAX,DWORD PTR [ESP+32]
          test EAX,EAX
          je L_41e47c
          mov EAX,DWORD PTR [ESP+40]
          lea ECX,DWORD PTR [ESI+EDX*1]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+60],EDX
          mov DWORD PTR [ESP+4],ECX
          mov DWORD PTR [ESP+56],ECX
          mov DWORD PTR [ESP+8],EAX
          call _memcpy
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call _daeDecrypt
          lea EAX,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP+28],20
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+24],EAX
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],EAX
          call _XeCryptSha
          lea EAX,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP+8],20
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP],EAX
          call _memcmp
          test EAX,EAX
          mov ECX,DWORD PTR [ESP+56]
          mov EDX,DWORD PTR [ESP+60]
          jne L_41e3d0
L_41e3b3:
          mov DWORD PTR [ESP+4],OFFSET _str_successNl
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+44],EDX
          call _log_printf
          jmp L_41e2d2
L_41e3d0:
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+4],ECX
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+56],EDX
          mov DWORD PTR [ESP+8],EAX
          call _memcpy
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call _daeDecrypt
          lea EAX,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP+28],20
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+24],EAX
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],EAX
          call _XeCryptSha
          lea EAX,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP+8],20
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP],EAX
          call _memcmp
          test EAX,EAX
          mov EDX,DWORD PTR [ESP+56]
          je L_41e2ce
L_41e46c:
          lea EDX,DWORD PTR [EBP+1]
          mov DWORD PTR [ESP+32],0
          jmp L_41e2f3
L_41e47c:
          mov DWORD PTR [ESP+4],OFFSET L_457300
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+56],EDX
          call _log_printf
          mov EDX,DWORD PTR [ESP+56]
          mov ECX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP],EBX
          lea EAX,DWORD PTR [ESI+EDX*1]
          mov DWORD PTR [ESP+8],ECX
          mov DWORD PTR [ESP+60],EDX
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP+56],EAX
          call _memcpy
          mov ECX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],ECX
          call _daeDecrypt
          lea EAX,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP+28],20
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+24],EAX
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],EAX
          call _XeCryptSha
          lea EAX,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP+8],20
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP],EAX
          call _memcmp
          test EAX,EAX
          mov EDX,DWORD PTR [ESP+60]
          je L_41e3b3
          mov DWORD PTR [ESP+4],OFFSET L_457380
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+60],EDX
          call _log_printf
          mov ECX,DWORD PTR [ESP+56]
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],ECX
          mov DWORD PTR [ESP+8],EAX
          call _memcpy
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call _daeDecrypt
          lea EAX,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP+28],20
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+24],EAX
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],EAX
          call _XeCryptSha
          lea EAX,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP+8],20
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP],EAX
          call _memcmp
          test EAX,EAX
          jne L_41e604
          mov DWORD PTR [ESP+4],OFFSET _str_successNl
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EDX,DWORD PTR [ESP+60]
          jmp L_41e2ce
L_41e604:
          mov DWORD PTR [ESP+4],OFFSET L_4573b8
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_41e46c
          .byte 0x8d
          .byte 0x76
          .byte 0x0
#@C _fcrtEncrypt
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
#@C _shaHeader
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90

.data
.p2align 5
_secdataKey:
          .byte 0x5a
          .byte 0xa4
          .byte 0xd1
          .byte 0xd2
L_44a5e4:
          .byte 0x7d
          .byte 0xe4
          .byte 0x45
          .byte 0x3e
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
_daeKey:
          .byte 0xa1
          .byte 0xb2
          .byte 0x69
          .byte 0x50
L_44a604:
          .byte 0x58
          .byte 0xf4
          .byte 0xed
          .byte 0x5
L_44a608:
          .byte 0xe5
          .byte 0x80
          .byte 0xc7
          .byte 0xee
L_44a60c:
          .byte 0x18
          .byte 0x9a
          .byte 0x27
          .byte 0xb5
L_44a610:
          .byte 0xac
          .byte 0x5e
          .byte 0xbc
          .byte 0x70
L_44a614:
          .byte 0x89
          .byte 0x29
          .byte 0x65
          .byte 0x90
L_44a618:
          .byte 0xf4
          .byte 0x24
          .byte 0xed
          .byte 0x2a
L_44a61c:
          .byte 0xd3
          .byte 0x62
          .byte 0x83
          .byte 0x14
_crlKey:
          .byte 0xc7
          .byte 0x3
          .byte 0xb9
          .byte 0x32
L_44a624:
          .byte 0xd4
          .byte 0x7
          .byte 0x7d
          .byte 0x41
L_44a628:
          .byte 0x60
          .byte 0x52
          .byte 0xa8
          .byte 0x13
L_44a62c:
          .byte 0x5e
          .byte 0xde
          .byte 0x68
          .byte 0x18
L_44a630:
          .byte 0xd9
          .byte 0x75
          .byte 0x98
          .byte 0xa6
L_44a634:
          .byte 0xf8
          .byte 0x5d
          .byte 0x9b
          .byte 0x86
L_44a638:
          .byte 0x7b
          .byte 0xc4
          .byte 0x34
          .byte 0x99
L_44a63c:
          .byte 0xe3
          .byte 0x3d
          .byte 0xa4
          .byte 0xaa
_smcKey:
          .byte 0x8e
          .byte 0x3
          .byte 0x75
          .byte 0xcc
_kvAltSalt:
          .byte 0x36
          .byte 0xca
          .byte 0xb0
          .byte 0x87
L_44a648:
          .byte 0x8b
          .byte 0x83
          .byte 0xb7
          .byte 0xf6
_kvSalt:
          .byte 0x36
          .byte 0xca
          .byte 0xb0
          .byte 0x87
L_44a650:
          .byte 0x8b
          .byte 0x83
          .byte 0xb7
          .byte 0xf6
_infoKey5:
          .byte 0xb9
          .byte 0xa2
          .byte 0x1e
          .byte 0x3b
L_44a658:
          .byte 0xfc
          .byte 0x2e
          .byte 0xab
          .byte 0xb4
L_44a65c:
          .byte 0x19
          .byte 0x81
          .byte 0x2d
          .byte 0x8a
L_44a660:
          .byte 0x85
          .byte 0xaa
          .byte 0xa8
          .byte 0xce
_infoKey4:
          .byte 0xce
          .byte 0xe5
          .byte 0x4
          .byte 0xee
L_44a668:
          .byte 0x9f
          .byte 0x61
          .byte 0x2b
          .byte 0x9b
L_44a66c:
          .byte 0xa5
          .byte 0x20
          .byte 0xf8
          .byte 0xeb
L_44a670:
          .byte 0xb
          .byte 0x64
          .byte 0x68
          .byte 0x2a
_infoKey3:
          .byte 0x56
          .byte 0xa9
          .byte 0x81
          .byte 0xcd
L_44a678:
          .byte 0x8c
          .byte 0xbc
          .byte 0x7
          .byte 0x29
L_44a67c:
          .byte 0xdd
          .byte 0xb
          .byte 0x7b
          .byte 0xbc
L_44a680:
          .byte 0x76
          .byte 0xe5
          .byte 0x79
          .byte 0x98
_infoKey2:
          .byte 0xb3
          .byte 0x38
          .byte 0x64
          .byte 0x1c
L_44a688:
          .byte 0xeb
          .byte 0xd0
          .byte 0x1e
          .byte 0x10
L_44a68c:
          .byte 0x2c
          .byte 0xdd
          .byte 0xe0
          .byte 0xf3
L_44a690:
          .byte 0x19
          .byte 0xa1
          .byte 0x9f
          .byte 0x84
_infoKey1:
          .byte 0xfb
          .byte 0xe2
          .byte 0x70
          .byte 0x9a
L_44a698:
          .byte 0xe7
          .byte 0xa1
          .byte 0x3f
          .byte 0x42
L_44a69c:
          .byte 0xcf
          .byte 0xec
          .byte 0x45
          .byte 0x92
L_44a6a0:
          .byte 0x8e
          .byte 0x3f
          .byte 0xe
          .byte 0x37
_infoKey0:
          .byte 0x37
          .byte 0x10
          .byte 0xa2
          .byte 0xf2
L_44a6a8:
          .byte 0x2e
          .byte 0xd5
          .byte 0xf0
          .byte 0xa8
L_44a6ac:
          .byte 0xe4
          .byte 0x9c
          .byte 0xb4
          .byte 0xc7
L_44a6b0:
          .byte 0xa1
          .byte 0x39
          .byte 0x5d
          .byte 0xaa
          .byte 0x0
          .byte 0x0
          .byte 0x0
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
_msg_initRandom:
          .string "initializing random nonces\n"
_msg_initStatic:
          .string "initializing static pairing value\n"
          .zero 1
_msg_pairingSet:
          .string "pairing set to: %02x %02x %02x\n"
_str_valid:
          .string "valid"
_str_error:
          .string "error"
_msg_weight:
          .string " (weight:0x%x %s; ecd: %s)"
_msg_cpuKeySet:
          .string "CPU Key set to: 0x"
_str_hexByte:
          .string "%02X"
_str_newline:
          .string "\n"
          .zero 3
_msg_cpuKeyWarn:
          .string "\n***** WARNING: CPU key check failed, CPU key may not be valid!\n\n"
          .zero 2
_msg_cpuKeyChars:
          .string "\n******* ERROR: invalid or unexpected characters in CPU key!\n"
          .zero 2
_msg_cpuKeyLen:
          .string "\n***** ERROR: unable to set CPU key to '%s', %d is not the correct length, 32 chars required!\n"
_msg_cpuKeySet2:
          .string "CPU Key set to  : "
_msg_fuseLdv:
          .string "Fuse CF LDV set to : 0x"
_msg_fuseCpuKey:
          .string "Fuse CPU Key set to: 0x"
          .zero 2
_msg_fuseNull:
          .string "\nERROR: YOU SHOULD NOT BE SEEING THIS ERROR!\n"
_msg_1blKeySet:
          .string "1BL Key set to  : 0x"
_msg_1blSum:
          .string " sum: 0x%x (expects: 0x983)\n"
_msg_xexKeySet:
          .string "xex Key set to  : 0x"
_msg_xexSum:
          .string " sum: 0x%x (expects: 0x800)\n"
_msg_1blBad:
          .string "\n******* ERROR: 1BL key 0x"
          .zero 3
_msg_1blBad2:
          .string " does not appear to be correct!\n"
          .zero 3
_msg_1blChars:
          .string "\n******* ERROR: invalid or unexpected characters in 1BL key!\n"
          .zero 2
_msg_1blLen:
          .string "\n***** ERROR: unable to set 1BL key to '%s', %d is not the correct length, 32 chars required!\n"
_msg_1blBadStr:
          .string "\n******* ERROR: 1BL key 0x%s "
          .zero 3
_msg_1blBadStr2:
          .string "does not appear to be correct!\n"
_msg_smcEncrypted:
          .string "SMC binary appears to be encrypted, attempting to decrypt..."
_str_success:
          .string "success!"
_str_failed:
          .string "failed!"
          .zero 2
_msg_smcBad:
          .string "\n******* ERROR: please make sure your provided a valid/decryptable SMC binary!\n\n"
          .zero 3
_msg_smcRetail:
          .string "\n******* ERROR: hacked or unknown SMC binary found? you should use a clean SMC binary for a retail image!\n\n"
_msg_smcCleanType:
          .string "known/clean SMC binary found! type 0x%x\n"
          .zero 3
_msg_smcDevkit:
          .string "\n******* WARNING: hacked or unknown SMC binary found? Just a warning, there are a lot of different SMC binaries for devkits!\n\n"
          .zero 1
_msg_smcClean:
          .string "known/clean SMC binary found!\n"
          .zero 1
_msg_smcGlitch:
          .string "glitch hack found in SMC binary!\n"
          .zero 2
_msg_smcHacked:
          .string "\n******* WARNING: hacked or unknown SMC binary found!\n"
          .zero 1
_msg_smcJtag:
          .string "jtag hack found in SMC binary!\n"
_msg_smcNoGlitch:
          .string "\n******* ERROR: clean SMC binary found? you should use a hacked SMC binary for glitch images.\n\n"
_msg_smcNoJtag:
          .string "\n******* ERROR: clean SMC binary found? you should use a hacked SMC binary for JTAG images.\n\n"
          .zero 2
_msg_cbencPairing:
          .string "CBENC pairing set to: %02x %02x %02x\n"
_msg_dualCb:
          .string "\t**dual CB flag detected!**\n"
          .zero 1
_msg_cbb15572:
          .string "\t**15572+ CBB crypto method detected!**\n"
          .zero 3
_msg_cbbMfg:
          .string "\t** CBB crypto method set to work with mfg CBA!**\n"
_str_kv:
          .string "kv"
_str_kvBin:
          .string "kv.bin"
_str_altKv:
          .string "alt kv"
_str_kvAltBin:
          .string "kv_alt.bin"
          .zero 1
_msg_kvSize:
          .string "\n******* ERROR: %s is not the correct size! Skipping verification and encryption!\n"
          .zero 1
_msg_kvHash:
          .string "%s appears to be decrypted already, but the hash does not match the CPU key..."
          .zero 1
_msg_kvPreDecrypted:
          .string "\n******* WARNING: could not verify pre-decrypted keyvault, please be sure your provided a valid %s!\n"
          .zero 3
_msg_kvEncrypted:
          .string "%s appears to be encrypted, attempting to decrypt..."
          .zero 3
_msg_kvDecryptFail:
          .string "Failed!\n%s could not be decrypted!\n"
_msg_kvDecryptErr:
          .string "\n******* ERROR: could not decrypt %s, please be sure your provided a valid %s!\n"
_str_Success:
          .string "Success!\n"
          .zero 2
_msg_kvNotDecrypted:
          .string "\n******* ERROR: please be sure your provided a DEcrypted %s!\n"
          .zero 2
_msg_extMissing:
          .string "******* WARNING: extended.bin was not provided or was invalid! Making up an clean/empty extended.bin!\n"
          .zero 1
_msg_extSize:
          .string "******* WARNING: extended.bin is not the correct size! Making up an clean/empty extended.bin!\n"
          .zero 1
_msg_extEncrypted:
          .string "extended.bin appears to be encrypted, attempting to decrypt..."
          .zero 1
_msg_extDecryptFail:
          .string "Failed!\nextended.bin could not be decrypted, filling clean/empty data.\n"
_msg_sdMissing:
          .string "******* WARNING: secdata.bin was not provided or was invalid! Making up an clean/empty secdata.bin!\n"
          .zero 3
_msg_sdSize:
          .string "******* WARNING: secdata.bin is not the correct size! Making up an clean/empty secdata.bin!\n"
_str_successNl:
          .string "success!\n"
          .zero 1
_msg_crlRetry:
          .string "failed! Trying alternate key..."
_str_failedNl:
          .string "failed!\n"
          .zero 3
_msg_crlCrypted:
          .string "crl appears crypted, attempting to decrypt with CPU key..."
          .zero 1
_msg_crlBad:
          .string "\n******* ERROR: crl data appears to be crypted with the wrong key or damaged!\n"
          .zero 1
L_457298:
          .string "\n******* WARNING: dae data appears to be crypted with a different key or damaged! Skipping encryption.\n"
L_457300:
          .string "dae appears encrypted, attempting to decrypt with CPU key..."
          .zero 3
L_457340:
          .string "\n******* ERROR: dae segment does not have the expected header!\n"
L_457380:
          .string "failed! Attempting to decrypt with alternate key...\n"
          .zero 3
L_4573b8:
          .string "failed!\n******* ERROR: dae hash incorrect, could not verify decrypted dae!\n"
_msg_fcrtSize:
          .string "****** ERROR: FCRT encrypt invalid size!\n"
          .zero 2
_msg_fcrtOffset:
          .string "**** ERROR: FCRT encrypt invalid offset!\n"
          .zero 2
_msg_fcrtBad:
          .string "****** WARNING: FCRT data appears to be crypted or damaged!! Skipping encryption.\n"
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
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _keysInit - .
          .byte 0xa3
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x2
          .byte 0x58
          .byte 0xa
          .byte 0xe
          .byte 0x4
          .byte 0x45
          .byte 0xb
          .byte 0x3
          .byte 0x42
          .byte 0x1
          .byte 0xe
          .byte 0x4
          .byte 0x18
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _setCrlKey - .
          .byte 0x4d
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x2
          .byte 0x4b
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x58
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _setDaeKey - .
          .byte 0x4b
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
          .byte 0x6c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _setSecdataKey - .
          .byte 0x15
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x18
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x80
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _setInfoKey0 - .
          .byte 0x29
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x67
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x18
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x9c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _setInfoKey1 - .
          .byte 0x29
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x67
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x18
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb8
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _setInfoKey2 - .
          .byte 0x29
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x67
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x18
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _setInfoKey3 - .
          .byte 0x29
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x67
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x18
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xf0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _setInfoKey4 - .
          .byte 0x29
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x67
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x18
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _setInfoKey5 - .
          .byte 0x29
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x67
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x28
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _setKvSalt - .
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
          .byte 0x3c
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _setKvAltSalt - .
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
          .byte 0x50
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _setSmcKey - .
          .byte 0xc
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
          .byte 0x64
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _setPairing - .
          .byte 0x5e
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x30
          .byte 0x2
          .byte 0x5a
          .byte 0xe
          .byte 0x4
          .byte 0x34
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x7c
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _checkCpuKey - .
          .byte 0x99
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
          .byte 0x50
          .byte 0x2
          .byte 0xc8
          .byte 0xa
          .byte 0xe
          .byte 0x10
          .byte 0x44
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
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb4
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _setCpuKeyStr - .
          .byte 0x39
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
          .byte 0x72
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
          .byte 0x45
          .byte 0xb
          .byte 0x34
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xe0
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _setCpuKey - .
          .byte 0xa6
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
          .byte 0x71
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
          .byte 0x41
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x18
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long _setFuseLdv - .
          .byte 0x42
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
          .byte 0x30
          .byte 0x2
          .byte 0xde
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
          .byte 0x50
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x58
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long _setFuseCpuKey - .
          .byte 0xfc
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
          .byte 0x2
          .byte 0xd2
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
          .byte 0x0
          .byte 0x0
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xac
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long _calcXexKey - .
          .byte 0xf5
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
          .byte 0x70
          .byte 0x2
          .byte 0xef
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd0
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long _check1blKey - .
          .byte 0xd7
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
          .byte 0xbd
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x46
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x49
          .byte 0xb
          .byte 0x43
          .byte 0xe
          .byte 0x8
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xfc
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long _set1blKey - .
          .byte 0x33
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
          .byte 0x20
          .byte 0x2
          .byte 0xe3
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x46
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x43
          .byte 0xb
          .byte 0x7f
          .byte 0xe
          .byte 0x8
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x48
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x28
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long _checkKeys - .
          .byte 0x91
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
          .byte 0x30
          .byte 0x72
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
          .byte 0x3
          .byte 0x20
          .byte 0x1
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
          .byte 0x4b
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x74
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long _smcChecksum - .
          .byte 0x20
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
          .byte 0x6
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
          .byte 0x45
          .byte 0xb
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb4
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long _smcEncrypt - .
          .byte 0x72
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
          .byte 0x24
          .byte 0x2
          .byte 0x66
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
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xf0
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long _smcPrepare - .
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
          .byte 0x60
          .byte 0x3
          .byte 0xca
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
          .byte 0x49
          .byte 0xb
          .byte 0x3
          .byte 0x17
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
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x48
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long _cbaEncrypt - .
          .byte 0x6a
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
          .byte 0x5a
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
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x88
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long _cbaEncryptZero - .
          .byte 0xea
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
          .byte 0x47
          .byte 0xe
          .byte 0x40
          .byte 0x2
          .byte 0xde
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
          .byte 0xb4
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long _cbaEncrypt2 - .
          .byte 0xbd
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
          .byte 0x16
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
          .byte 0x4f
          .byte 0xb
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xf4
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long _cbbEncrypt - .
          .byte 0x66
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
          .byte 0x60
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
          .byte 0x45
          .byte 0xb
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x34
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .long _cdEncryptZero - .
          .byte 0xc8
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
          .byte 0x50
          .byte 0x2
          .byte 0xc0
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
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x60
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .long _cdEncrypt - .
          .byte 0xa6
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
          .byte 0x40
          .byte 0x2
          .byte 0x98
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
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x94
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .long _cdEncryptCpu - .
          .byte 0xf2
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
          .byte 0x40
          .byte 0x2
          .byte 0xe4
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
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc8
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .long _ceEncrypt - .
          .byte 0xa6
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
          .byte 0x40
          .byte 0x2
          .byte 0x98
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
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xfc
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .long _cfPatchSlots - .
          .byte 0xe
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
          .byte 0x20
          .byte 0x2
          .byte 0xc6
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
          .byte 0x4b
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
          .byte 0x40
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x54
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .long _cfEncrypt - .
          .byte 0x27
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
          .byte 0x54
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
          .byte 0x41
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x98
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .long _cgEncrypt - .
          .byte 0xa6
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
          .byte 0x40
          .byte 0x2
          .byte 0x98
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
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xcc
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .long _kvEncrypt - .
          .byte 0xe8
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
          .byte 0x70
          .byte 0x2
          .byte 0xdc
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
          .byte 0x8
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .long _kvEncryptAlt - .
          .byte 0xe8
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
          .byte 0x70
          .byte 0x2
          .byte 0xdc
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
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x44
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .long _kvPrepare - .
          .byte 0xb2
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
          .byte 0x4d
          .byte 0xe
          .byte 0x80
          .byte 0x1
          .byte 0x2
          .byte 0x4e
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
          .byte 0x3
          .byte 0xa0
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
          .byte 0x4c
          .byte 0xb
          .byte 0x40
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x9c
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .long _extendedPrepare - .
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
          .byte 0x80
          .byte 0x1
          .byte 0x3
          .byte 0xb2
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
          .byte 0x43
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x2c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xe0
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .long _secdataPrepare - .
          .byte 0xbb
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
          .byte 0x50
          .byte 0x3
          .byte 0x8d
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
          .byte 0x0
          .byte 0x0
          .byte 0x34
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .long _shaCheck - .
          .byte 0xb7
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
          .byte 0x50
          .byte 0x2
          .byte 0x9c
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
          .byte 0x49
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x40
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x48
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .long _crlEncrypt - .
          .byte 0x6a
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
          .byte 0x4
          .byte 0x3
          .byte 0x83
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
          .byte 0x4f
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8c
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .long _daeEncryptOne - .
          .byte 0xd7
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
          .byte 0xf0
          .byte 0x4
          .byte 0x3
          .byte 0xc4
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
          .byte 0xcc
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .long _daeEncrypt - .
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
          .byte 0x45
          .byte 0xe
          .byte 0x80
          .byte 0x1
          .byte 0x2
          .byte 0x75
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
          .byte 0x4e
          .byte 0xb
          .byte 0x7c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc
          .byte 0x9
          .byte 0x0
          .byte 0x0
          .long _fcrtEncrypt - .
          .byte 0x82
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
          .byte 0x56
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
          .byte 0xae
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
          .byte 0x7e
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
          .byte 0x5a
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
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8c
          .byte 0x9
          .byte 0x0
          .byte 0x0
          .long _shaHeader - .
          .byte 0x4a
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x30
          .byte 0x2
          .byte 0x46
          .byte 0xe
          .byte 0x4

.bss
.p2align 2
_zeroKey:
          .zero 16
_pairing:
          .zero 1
L_479571:
          .zero 1
L_479572:
          .zero 2

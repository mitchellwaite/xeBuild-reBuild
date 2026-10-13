# app/stfs.s -- container header/content/manifest hash checks, STFS file listing
#
# mixed: `#@C name` lines are functions from stfs.c (re/splice.py)
#
# original placement:
#   .eh_frame      0046599c-00465b68
#   .rdata         0044deb8-0044e10c
#   .rdata$zzz     004637d0-004637fc
#   .text          00405610-00406330

.intel_syntax noprefix
.globl _sCorrupt
.globl _sDone
.globl _sFnamelen
.globl _sFound
.globl _sManifestBad
.globl _sManifestOk
.globl _sName
.globl _sNotFound
.globl _sValid
.globl _sValidVer
.globl _stfsCheckHashes
.globl _stfsGetFile
.globl _stfsListFiles

.text
.p2align 4
_stfsCheckHashes:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,108
          mov EDI,DWORD PTR [ESP+128]
          lea EAX,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP+28],20
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+24],EAX
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],0
          mov EAX,DWORD PTR [EDI+12]
          mov ESI,DWORD PTR [ESP+132]
          sub EAX,836
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [EDI]
          add EAX,836
          mov DWORD PTR [ESP],EAX
          call _XeCryptSha
          lea EAX,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP+8],20
          mov DWORD PTR [ESP+4],EAX
          lea EAX,DWORD PTR [ESI+812]
          mov DWORD PTR [ESP],EAX
          call _memcmp
          test EAX,EAX
          jne L_405860
          mov EBX,DWORD PTR [EDI+12]
          mov EAX,DWORD PTR [EDI]
          lea EBP,DWORD PTR [EBX+4096]
          add EBX,EAX
          add EAX,EBP
          mov DWORD PTR [EDI+16],EAX
          mov EAX,DWORD PTR [ESP+136]
          test EAX,EAX
          jne L_405942
L_4056b7:
          lea EAX,DWORD PTR [ESI+897]
          mov DWORD PTR [ESP+52],24
          mov DWORD PTR [ESP+56],0
          mov DWORD PTR [ESP+44],0
          mov DWORD PTR [ESP+60],EAX
L_4056d9:
          mov EAX,DWORD PTR [ESP+44]
          lea ESI,DWORD PTR [EAX*4]
          add EAX,170
          mov DWORD PTR [ESP+48],EAX
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
L_4056f0:
          mov DWORD PTR [ESP+4],24
          mov DWORD PTR [ESP],EBX
          call _checkZeros
          test EAX,EAX
          je L_4057d0
          xor ESI,ESI
L_40570a:
          lea EAX,DWORD PTR [EBP+8192]
          cmp EAX,DWORD PTR [EDI+8]
          jae L_4057b0
          mov EBX,DWORD PTR [EDI]
          add EBX,EBP
          mov EAX,DWORD PTR [EBX+20]
          test EAX,EAX
          je L_40586a
          mov ECX,DWORD PTR [ESP+56]
          test ECX,ECX
          je L_405798
L_405730:
          lea EAX,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP+28],20
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+24],EAX
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+4],4096
          mov DWORD PTR [ESP],EBX
          call _XeCryptSha
          mov EAX,DWORD PTR [ESP+56]
          add EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+8],20
          mov DWORD PTR [ESP+4],EAX
          lea EAX,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP],EAX
          call _memcmp
          test EAX,EAX
          jne L_405860
L_405798:
          add EBP,4096
          add DWORD PTR [ESP+52],24
          test ESI,ESI
          jne L_4056d9
          nop
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_4057b0:
          mov EDX,DWORD PTR [ESP+136]
          mov EAX,1
          test EDX,EDX
          jne L_40595b
L_4057c4:
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
L_4057d0:
          lea EAX,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP+28],20
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+24],EAX
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+4],4096
          mov EAX,DWORD PTR [EDI]
          add EAX,EBP
          mov DWORD PTR [ESP],EAX
          call _XeCryptSha
          lea EAX,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP+8],20
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EAX
          call _memcmp
          test EAX,EAX
          jne L_405860
          mov EAX,DWORD PTR [EDI+4]
          add DWORD PTR [ESP+44],1
          add EBX,24
          mov DWORD PTR [EAX+ESI*1],EBP
          add EBP,4096
          add ESI,4
          mov EAX,DWORD PTR [ESP+44]
          cmp EAX,DWORD PTR [ESP+48]
          jne L_4056f0
          mov ESI,1
          jmp L_40570a
          .byte 0x90
L_405860:
          add ESP,108
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_40586a:
          lea EAX,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP+28],20
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+24],EAX
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+4],4096
          mov DWORD PTR [ESP],EBX
          call _XeCryptSha
          lea EAX,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP+8],20
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP],EAX
          call _memcmp
          test EAX,EAX
          jne L_405860
          lea EAX,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP+28],20
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+24],EAX
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+4],4096
          mov EAX,DWORD PTR [EDI+12]
          add EAX,DWORD PTR [EDI]
          mov DWORD PTR [ESP],EAX
          call _XeCryptSha
          lea EAX,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP+8],20
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EAX
          call _memcmp
          test EAX,EAX
          jne L_405860
          mov DWORD PTR [ESP+56],EBX
          mov EBX,DWORD PTR [EDI]
          add EBP,4096
          add EBX,EBP
          jmp L_405730
L_405942:
          mov DWORD PTR [ESP+4],OFFSET L_44deb8
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_4056b7
L_40595b:
          mov DWORD PTR [ESP+4],OFFSET L_44dee8
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+44],EAX
          call _log_printf
          mov EAX,DWORD PTR [ESP+44]
          jmp L_4057c4
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
_stfsListFiles:
          push EBP
          push EDI
          xor EDI,EDI
          push ESI
          push EBX
          sub ESP,44
          mov EBP,DWORD PTR [ESP+64]
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
L_405990:
          mov DWORD PTR [ESP+4],64
          mov EAX,DWORD PTR [EBP+16]
          lea ESI,DWORD PTR [EDI+64]
          add EAX,EDI
          mov DWORD PTR [ESP],EAX
          call _checkZeros
          test EAX,EAX
          jne L_405ab0
          mov EAX,DWORD PTR [EBP+16]
          add EAX,EDI
          movzx EDX,BYTE PTR [EAX+48]
          movzx ECX,BYTE PTR [EAX+47]
          mov EBX,DWORD PTR [EAX+52]
          shl EDX,8
          shl EBX,24
          add ECX,EDX
          movzx EDX,BYTE PTR [EAX+49]
          shl EDX,16
          add EDX,ECX
          mov ECX,DWORD PTR [EAX+52]
          shr ECX,24
          add EBX,ECX
          mov ECX,DWORD PTR [EAX+52]
          shl ECX,8
          and ECX,16711680
          add ECX,EBX
          mov EBX,DWORD PTR [EAX+52]
          shr EBX,8
          and EBX,65280
          add ECX,EBX
          mov DWORD PTR [ESP+28],ECX
          mov ECX,DWORD PTR [EBP+4]
          mov ECX,DWORD PTR [ECX+EDX*4]
          mov DWORD PTR [ESP+20],EDX
          mov DWORD PTR [ESP+24],ECX
          movzx EDX,BYTE PTR [EAX+45]
          movzx ECX,BYTE PTR [EAX+44]
          shl EDX,8
          add ECX,EDX
          movzx EDX,BYTE PTR [EAX+46]
          shl EDX,16
          add EDX,ECX
          mov DWORD PTR [ESP+16],EDX
          movzx EDX,BYTE PTR [EAX+42]
          movzx ECX,BYTE PTR [EAX+41]
          shl EDX,8
          add ECX,EDX
          movzx EDX,BYTE PTR [EAX+43]
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET _sName
          mov DWORD PTR [ESP],1
          shl EDX,16
          add EDX,ECX
          mov DWORD PTR [ESP+12],EDX
          call _log_printf
          add EDI,DWORD PTR [EBP+16]
          movzx EDX,WORD PTR [EDI+50]
          mov EAX,EDX
          movzx EDX,DH
          shl EAX,8
          and EAX,65280
          add EAX,EDX
          mov DWORD PTR [ESP+20],EAX
          movzx EAX,BYTE PTR [EDI+40]
          shr AL,7
          movzx EAX,AL
          mov DWORD PTR [ESP+16],EAX
          movzx EAX,BYTE PTR [EDI+40]
          shr AL,6
          and EAX,1
          mov DWORD PTR [ESP+12],EAX
          movzx EAX,BYTE PTR [EDI+40]
          mov EDI,ESI
          mov DWORD PTR [ESP+4],OFFSET _sFnamelen
          mov DWORD PTR [ESP],1
          and EAX,63
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          jmp L_405990
          .byte 0x90
L_405ab0:
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
#@C _stfsCheckHeader
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
_stfsGetFile:
          push EBP
          push EDI
          push ESI
          push EBX
          mov ESI,1
          sub ESP,44
          mov EDI,DWORD PTR [ESP+64]
          mov EBP,DWORD PTR [ESP+68]
          mov EDX,DWORD PTR [EDI+16]
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_405d70:
          lea EBX,DWORD PTR [ESI+67108863]
          mov DWORD PTR [ESP+4],64
          shl EBX,6
          add EDX,EBX
          mov DWORD PTR [ESP],EDX
          call _checkZeros
          test EAX,EAX
          je L_405da0
          xor EAX,EAX
L_405d91:
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
L_405da0:
          mov EAX,DWORD PTR [EDI+16]
          mov DWORD PTR [ESP],EBP
          add EAX,EBX
          mov DWORD PTR [ESP+4],EAX
          call _stricmp
          test EAX,EAX
          mov EDX,DWORD PTR [EDI+16]
          jne L_405e1a
          lea ECX,DWORD PTR [EDX+EBX*1]
          mov DWORD PTR [ESP+16],EDX
          test BYTE PTR [ECX+40],64
          je L_405e22
          mov EBX,DWORD PTR [ECX+52]
          mov DWORD PTR [ESP+20],ECX
          mov EAX,EBX
          shl EAX,8
          and EAX,16711680
          mov ECX,EAX
          mov DWORD PTR [ESP+24],EAX
          mov EAX,EBX
          shr EAX,8
          and EAX,65280
          mov EDX,EAX
          mov DWORD PTR [ESP+28],EAX
          mov EAX,EBX
          shl EAX,24
          shr EBX,24
          add EBX,EAX
          mov EAX,ECX
          or EAX,EDX
          lea EAX,DWORD PTR [EBX+EAX*1+4095]
          and EAX,4294963200
          mov DWORD PTR [ESP],EAX
          call _malloc
          test EAX,EAX
          mov ECX,DWORD PTR [ESP+20]
          mov EDX,DWORD PTR [ESP+16]
          jne L_405e3b
L_405e1a:
          add ESI,1
          jmp L_405d70
L_405e22:
          mov DWORD PTR [ESP+4],OFFSET L_44e01c
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EDX,DWORD PTR [EDI+16]
          jmp L_405e1a
L_405e3b:
          movzx EDX,BYTE PTR [ECX+45]
          mov DWORD PTR [ESP+16],EBX
          mov EBX,ECX
          movzx ECX,BYTE PTR [ECX+44]
          movzx ESI,BYTE PTR [EBX+47]
          movzx EBP,BYTE PTR [EBX+46]
          shl EDX,8
          add ECX,EDX
          movzx EDX,BYTE PTR [EBX+48]
          shl EBP,16
          shl EDX,8
          add EDX,ESI
          movzx ESI,BYTE PTR [EBX+49]
          shl ESI,16
          add ESI,EDX
          add ECX,EBP
          mov DWORD PTR [ESP+20],ECX
          je L_405ef2
          mov EDX,DWORD PTR [EDI]
          mov ECX,DWORD PTR [EDI+4]
          mov EBP,EAX
          mov DWORD PTR [ESP+24],EAX
          mov DWORD PTR [ESP+16],EDX
          lea EDX,DWORD PTR [ECX+ESI*4]
          add ESI,DWORD PTR [ESP+20]
          mov EAX,DWORD PTR [ESP+16]
          mov DWORD PTR [ESP+20],EBX
          lea EDI,DWORD PTR [ECX+ESI*4]
          mov EBX,EDI
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_405ea0:
          mov ESI,DWORD PTR [EDX]
          add EDX,4
          mov EDI,EBP
          add EBP,4096
          mov ECX,1024
          add ESI,EAX
          cmp EBX,EDX
          rep movsd 
          jne L_405ea0
          mov EBX,DWORD PTR [ESP+20]
          mov EAX,DWORD PTR [ESP+24]
          mov ECX,DWORD PTR [EBX+52]
          mov EDX,ECX
          shl EDX,8
          and EDX,16711680
          mov DWORD PTR [ESP+24],EDX
          mov EDX,ECX
          shr EDX,8
          and EDX,65280
          mov DWORD PTR [ESP+28],EDX
          mov EDX,ECX
          shr ECX,24
          shl EDX,24
          lea EDI,DWORD PTR [EDX+ECX*1]
          mov DWORD PTR [ESP+16],EDI
L_405ef2:
          mov EDX,DWORD PTR [ESP+72]
          mov DWORD PTR [EDX],EAX
          mov EAX,DWORD PTR [ESP+24]
          add EAX,DWORD PTR [ESP+28]
          mov EDX,DWORD PTR [ESP+76]
          add EAX,DWORD PTR [ESP+16]
          mov DWORD PTR [EDX],EAX
          mov EAX,1
          jmp L_405d91
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
#@C _stfsInit
L_405f47:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
#@C _stfsFree
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
#@C _stfsLoad
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90

.section .rdata,"dr"
.p2align 2
L_44deb8:
          .string "header hash is OK, checking content hashes...\n"
          .zero 1
L_44dee8:
          .string "content hashes seem OK, everything looks good!\n"
_sName:
          .string "name: %s vb: 0x%x ab: 0x%x fb: 0x%x (off 0x%x) size 0x%x\n"
          .zero 2
_sFnamelen:
          .string "\tfnamelen: %d cont: %d dir: %d idx: 0x%x\n"
          .zero 2
_sValidVer:
          .string "header seems valid, version %d.%d.%d.%d\n"
_sValid:
          .string "header seems valid\n"
          .zero 3
_sManifestBad:
          .string "manifest hash does not match container header!\n"
_sManifestOk:
          .string "manifest hash matches container header!\n"
          .zero 3
L_44e01c:
          .string "\n\n***** WARNING !!! file %s is not contiguous and contents are being skipped!\n\n"
_sFound:
          .string "%s found, loading..."
          .zero 3
_sDone:
          .string "done!\n\tRead 0x%x bytes to memory\nchecking integrity...\n"
_sNotFound:
          .string "container not found at %s, skipping load\n"
          .zero 2
_sCorrupt:
          .string "checks failed! Container corrupt!\n"
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
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _stfsCheckHashes - .
          .byte 0x6c
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
          .byte 0xb0
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
          .byte 0x2
          .byte 0x93
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
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x74
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _stfsListFiles - .
          .byte 0x38
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
          .byte 0x43
          .byte 0xe
          .byte 0x40
          .byte 0x3
          .byte 0x2a
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
          .byte 0x48
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _stfsCheckHeader - .
          .byte 0x89
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
          .byte 0x30
          .byte 0x2
          .byte 0x76
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
          .byte 0x3
          .byte 0x2a
          .byte 0x1
          .byte 0xa
          .byte 0xe
          .byte 0x10
          .byte 0x48
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
          .byte 0x4a
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _stfsGetFile - .
          .byte 0xc4
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
          .byte 0x48
          .byte 0xe
          .byte 0x40
          .byte 0x78
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
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x40
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _stfsInit - .
          .byte 0x27
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x54
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _stfsFree - .
          .byte 0x4c
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
          .byte 0x46
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x78
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _stfsLoad - .
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
          .byte 0x43
          .byte 0xe
          .byte 0x40
          .byte 0x3
          .byte 0x18
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
          .byte 0x3
          .byte 0x87
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

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
.globl _sContentOk
.globl _sCorrupt
.globl _sDone
.globl _sFnamelen
.globl _sFound
.globl _sHashOk
.globl _sManifestBad
.globl _sManifestOk
.globl _sName
.globl _sNotFound
.globl _sValid
.globl _sValidVer
.globl _stfsGetFile

.text
.p2align 4
#@C _stfsCheckHashes
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
#@C _stfsListFiles
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
_sHashOk:
          .string "header hash is OK, checking content hashes...\n"
          .zero 1
_sContentOk:
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

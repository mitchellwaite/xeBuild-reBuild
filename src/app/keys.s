# app/keys.s -- CPU/1BL key setup, SMC/keyvault/CRL input decryption, pairing init
#
# original placement:
#   .bss           00479560-00479574
#   .data          0044a5e0-0044a6c0
#   .eh_frame      00468230-00468bd0
#   .rdata         00456664-004574b0
#   .rdata$zzz     00463a38-00463a64
#   .text          0041aa00-0041e800

.intel_syntax noprefix
.globl FUN_41aa00
.globl FUN_41abb0
.globl FUN_41ac00
.globl FUN_41ac50
.globl FUN_41ac70
.globl FUN_41aca0
.globl FUN_41acd0
.globl FUN_41ad00
.globl FUN_41ad30
.globl FUN_41ad60
.globl FUN_41ad90
.globl FUN_41adb0
.globl FUN_41add0
.globl FUN_41ade0
.globl FUN_41ae40
.globl FUN_41afe0
.globl FUN_41b120
.globl FUN_41b320
.globl FUN_41b600
.globl FUN_41b740
.globl FUN_41ba80
.globl FUN_41bf50
.globl FUN_41c0c0
.globl FUN_41c1b0
.globl FUN_41c370
.globl FUN_41c5e0
.globl FUN_41c6b0
.globl FUN_41c760
.globl FUN_41c860
.globl FUN_41ca20
.globl FUN_41ce50
.globl FUN_41d0e0
.globl FUN_41d6a0
.globl FUN_41d9b0
.globl FUN_41db70
.globl FUN_41dc30
.globl FUN_41e180
.globl FUN_41e620
.globl FUN_41e7b0

.text
.p2align 4
FUN_41aa00:
          sub ESP,28
          call _aes_init
          mov EAX,DWORD PTR [ESP+32]
          test EAX,EAX
          jne L_41aa60
          cmp BYTE PTR [L_479570],0
          jne L_41aa58
          cmp BYTE PTR [L_479571],0
          jne L_41aa58
          cmp BYTE PTR [L_479572],0
          jne L_41ab7e
          mov DWORD PTR [ESP+4],OFFSET L_456680
          mov DWORD PTR [ESP],1
          call _log_printf
          mov BYTE PTR [L_479570],35
          mov BYTE PTR [L_479571],69
          mov BYTE PTR [L_479572],241
L_41aa58:
          add ESP,28
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_41aa60:
          mov DWORD PTR [ESP+4],OFFSET L_456664
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_44a6a4
          call _XeCryptRandom
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_44a694
          call _XeCryptRandom
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_44a684
          call _XeCryptRandom
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_44a674
          call _XeCryptRandom
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_44a664
          call _XeCryptRandom
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_44a654
          call _XeCryptRandom
          mov DWORD PTR [ESP+4],8
          mov DWORD PTR [ESP],OFFSET L_44a64c
          call _XeCryptRandom
          mov DWORD PTR [ESP+4],8
          mov DWORD PTR [ESP],OFFSET L_44a644
          call _XeCryptRandom
          mov DWORD PTR [ESP+4],4
          mov DWORD PTR [ESP],OFFSET L_44a640
          call _XeCryptRandom
          mov DWORD PTR [ESP+4],32
          mov DWORD PTR [ESP],OFFSET L_44a620
          call _XeCryptRandom
          mov DWORD PTR [ESP+4],32
          mov DWORD PTR [ESP],OFFSET L_44a600
          call _XeCryptRandom
          mov DWORD PTR [ESP+4],8
          mov DWORD PTR [ESP],OFFSET L_44a5e0
          call _XeCryptRandom
          cmp BYTE PTR [L_479570],0
          jne L_41aa58
          cmp BYTE PTR [L_479571],0
          jne L_41aa58
L_41ab7e:
          cmp BYTE PTR [L_479572],0
          jne L_41aa58
          mov DWORD PTR [ESP+4],3
          mov DWORD PTR [ESP],OFFSET L_479570
          call _XeCryptRandom
          add ESP,28
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
FUN_41abb0:
          push EBX
          mov EAX,DWORD PTR [ESP+8]
          mov EDX,DWORD PTR [EAX+16]
          mov DWORD PTR [L_44a620],EDX
          mov EDX,DWORD PTR [EAX+20]
          mov DWORD PTR [L_44a624],EDX
          mov EDX,DWORD PTR [EAX+24]
          mov DWORD PTR [L_44a628],EDX
          mov EDX,DWORD PTR [EAX+28]
          mov DWORD PTR [L_44a62c],EDX
          mov EBX,DWORD PTR [EAX]
          mov ECX,DWORD PTR [EAX+4]
          mov EDX,DWORD PTR [EAX+8]
          mov EAX,DWORD PTR [EAX+12]
          mov DWORD PTR [L_44a630],EBX
          mov DWORD PTR [L_44a634],ECX
          mov DWORD PTR [L_44a638],EDX
          mov DWORD PTR [L_44a63c],EAX
          pop EBX
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
FUN_41ac00:
          mov EAX,DWORD PTR [ESP+4]
          mov EDX,DWORD PTR [EAX]
          mov DWORD PTR [L_44a600],EDX
          mov EDX,DWORD PTR [EAX+4]
          mov DWORD PTR [L_44a604],EDX
          mov EDX,DWORD PTR [EAX+8]
          mov DWORD PTR [L_44a608],EDX
          mov EDX,DWORD PTR [EAX+12]
          mov DWORD PTR [L_44a60c],EDX
          mov EDX,DWORD PTR [EAX+16]
          mov DWORD PTR [L_44a610],EDX
          mov EDX,DWORD PTR [EAX+20]
          mov DWORD PTR [L_44a614],EDX
          mov EDX,DWORD PTR [EAX+24]
          mov DWORD PTR [L_44a618],EDX
          mov EAX,DWORD PTR [EAX+28]
          mov DWORD PTR [L_44a61c],EAX
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
FUN_41ac50:
          mov EAX,DWORD PTR [ESP+4]
          mov EDX,DWORD PTR [EAX+4]
          mov EAX,DWORD PTR [EAX]
          mov DWORD PTR [L_44a5e4],EDX
          mov DWORD PTR [L_44a5e0],EAX
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
FUN_41ac70:
          push EBX
          mov EAX,DWORD PTR [ESP+8]
          mov EBX,DWORD PTR [EAX]
          mov ECX,DWORD PTR [EAX+4]
          mov EDX,DWORD PTR [EAX+8]
          mov EAX,DWORD PTR [EAX+12]
          mov DWORD PTR [L_44a6a4],EBX
          mov DWORD PTR [L_44a6a8],ECX
          mov DWORD PTR [L_44a6ac],EDX
          mov DWORD PTR [L_44a6b0],EAX
          pop EBX
          ret 
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_41aca0:
          push EBX
          mov EAX,DWORD PTR [ESP+8]
          mov EBX,DWORD PTR [EAX]
          mov ECX,DWORD PTR [EAX+4]
          mov EDX,DWORD PTR [EAX+8]
          mov EAX,DWORD PTR [EAX+12]
          mov DWORD PTR [L_44a694],EBX
          mov DWORD PTR [L_44a698],ECX
          mov DWORD PTR [L_44a69c],EDX
          mov DWORD PTR [L_44a6a0],EAX
          pop EBX
          ret 
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_41acd0:
          push EBX
          mov EAX,DWORD PTR [ESP+8]
          mov EBX,DWORD PTR [EAX]
          mov ECX,DWORD PTR [EAX+4]
          mov EDX,DWORD PTR [EAX+8]
          mov EAX,DWORD PTR [EAX+12]
          mov DWORD PTR [L_44a684],EBX
          mov DWORD PTR [L_44a688],ECX
          mov DWORD PTR [L_44a68c],EDX
          mov DWORD PTR [L_44a690],EAX
          pop EBX
          ret 
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_41ad00:
          push EBX
          mov EAX,DWORD PTR [ESP+8]
          mov EBX,DWORD PTR [EAX]
          mov ECX,DWORD PTR [EAX+4]
          mov EDX,DWORD PTR [EAX+8]
          mov EAX,DWORD PTR [EAX+12]
          mov DWORD PTR [L_44a674],EBX
          mov DWORD PTR [L_44a678],ECX
          mov DWORD PTR [L_44a67c],EDX
          mov DWORD PTR [L_44a680],EAX
          pop EBX
          ret 
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_41ad30:
          push EBX
          mov EAX,DWORD PTR [ESP+8]
          mov EBX,DWORD PTR [EAX]
          mov ECX,DWORD PTR [EAX+4]
          mov EDX,DWORD PTR [EAX+8]
          mov EAX,DWORD PTR [EAX+12]
          mov DWORD PTR [L_44a664],EBX
          mov DWORD PTR [L_44a668],ECX
          mov DWORD PTR [L_44a66c],EDX
          mov DWORD PTR [L_44a670],EAX
          pop EBX
          ret 
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_41ad60:
          push EBX
          mov EAX,DWORD PTR [ESP+8]
          mov EBX,DWORD PTR [EAX]
          mov ECX,DWORD PTR [EAX+4]
          mov EDX,DWORD PTR [EAX+8]
          mov EAX,DWORD PTR [EAX+12]
          mov DWORD PTR [L_44a654],EBX
          mov DWORD PTR [L_44a658],ECX
          mov DWORD PTR [L_44a65c],EDX
          mov DWORD PTR [L_44a660],EAX
          pop EBX
          ret 
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_41ad90:
          mov EAX,DWORD PTR [ESP+4]
          mov EDX,DWORD PTR [EAX+4]
          mov EAX,DWORD PTR [EAX]
          mov DWORD PTR [L_44a650],EDX
          mov DWORD PTR [L_44a64c],EAX
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
FUN_41adb0:
          mov EAX,DWORD PTR [ESP+4]
          mov EDX,DWORD PTR [EAX+4]
          mov EAX,DWORD PTR [EAX]
          mov DWORD PTR [L_44a648],EDX
          mov DWORD PTR [L_44a644],EAX
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
FUN_41add0:
          mov EAX,DWORD PTR [ESP+4]
          mov EAX,DWORD PTR [EAX]
          mov DWORD PTR [L_44a640],EAX
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
FUN_41ade0:
          sub ESP,44
          xor EAX,EAX
          mov EDX,DWORD PTR [ESP+48]
          test EDX,16777215
          je L_41ae3a
          mov EAX,EDX
          mov ECX,EDX
          mov BYTE PTR [L_479572],DL
          shr EAX,16
          shr ECX,8
          movzx EDX,DL
          mov BYTE PTR [L_479570],AL
          mov BYTE PTR [L_479571],CL
          movzx EAX,AL
          movzx ECX,CL
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+16],EDX
          mov DWORD PTR [ESP+12],ECX
          mov DWORD PTR [ESP+4],OFFSET L_4566a4
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,1
L_41ae3a:
          add ESP,44
          ret 
          .byte 0x66
          .byte 0x90
FUN_41ae40:
          push EDI
          push ESI
          push EBX
          sub ESP,64
          mov EBX,DWORD PTR [ESP+84]
          mov DWORD PTR [ESP+32],4294967295
          mov DWORD PTR [ESP+36],4294967295
          mov DWORD PTR [ESP+40],4294967295
          mov DWORD PTR [ESP+44],1023
          test BL,3
          jne L_41af15
          mov EAX,DWORD PTR [EBX]
          mov DWORD PTR [ESP+48],EAX
          mov EAX,DWORD PTR [EBX+4]
          mov DWORD PTR [ESP+52],EAX
          mov EAX,DWORD PTR [EBX+8]
          mov DWORD PTR [ESP+56],EAX
          mov EAX,DWORD PTR [EBX+12]
          and EAX,1023
          mov DWORD PTR [ESP+60],EAX
L_41ae93:
          lea ESI,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],ESI
          call _XeCryptHammingWeight
          mov DWORD PTR [ESP],ESI
          mov EDI,EAX
          call _XeCryptUidEccEncode
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],16
          call _memcmp
          test EAX,EAX
          mov EDX,OFFSET L_4566c4
          mov DWORD PTR [ESP+8],EDI
          sete BL
          cmp EDI,53
          mov DWORD PTR [ESP+4],OFFSET L_4566d0
          sete CL
          test EAX,EAX
          mov EAX,EDX
          mov ESI,ECX
          mov ECX,OFFSET L_4566ca
          cmovne EAX,ECX
          cmp EDI,53
          mov DWORD PTR [ESP+16],EAX
          mov EAX,DWORD PTR [ESP+80]
          cmovne EDX,ECX
          mov DWORD PTR [ESP+12],EDX
          and EBX,ESI
          mov DWORD PTR [ESP],EAX
          call _log_printf
          add ESP,64
          movzx EAX,BL
          pop EBX
          pop ESI
          pop EDI
          ret 
L_41af15:
          movzx EAX,BYTE PTR [EBX]
          and AL,BYTE PTR [ESP+32]
          mov BYTE PTR [ESP+48],AL
          movzx EAX,BYTE PTR [EBX+1]
          and AL,BYTE PTR [ESP+33]
          mov BYTE PTR [ESP+49],AL
          movzx EAX,BYTE PTR [EBX+2]
          and AL,BYTE PTR [ESP+34]
          mov BYTE PTR [ESP+50],AL
          movzx EAX,BYTE PTR [EBX+3]
          and AL,BYTE PTR [ESP+35]
          mov BYTE PTR [ESP+51],AL
          movzx EAX,BYTE PTR [EBX+4]
          and AL,BYTE PTR [ESP+36]
          mov BYTE PTR [ESP+52],AL
          movzx EAX,BYTE PTR [EBX+5]
          and AL,BYTE PTR [ESP+37]
          mov BYTE PTR [ESP+53],AL
          movzx EAX,BYTE PTR [EBX+6]
          and AL,BYTE PTR [ESP+38]
          mov BYTE PTR [ESP+54],AL
          movzx EAX,BYTE PTR [EBX+7]
          and AL,BYTE PTR [ESP+39]
          mov BYTE PTR [ESP+55],AL
          movzx EAX,BYTE PTR [EBX+8]
          and AL,BYTE PTR [ESP+40]
          mov BYTE PTR [ESP+56],AL
          movzx EAX,BYTE PTR [EBX+9]
          and AL,BYTE PTR [ESP+41]
          mov BYTE PTR [ESP+57],AL
          movzx EAX,BYTE PTR [EBX+10]
          and AL,BYTE PTR [ESP+42]
          mov BYTE PTR [ESP+58],AL
          movzx EAX,BYTE PTR [EBX+11]
          and AL,BYTE PTR [ESP+43]
          mov BYTE PTR [ESP+59],AL
          movzx EAX,BYTE PTR [EBX+12]
          and AL,BYTE PTR [ESP+44]
          mov BYTE PTR [ESP+60],AL
          movzx EAX,BYTE PTR [EBX+13]
          and AL,BYTE PTR [ESP+45]
          mov BYTE PTR [ESP+61],AL
          movzx EAX,BYTE PTR [EBX+14]
          and AL,BYTE PTR [ESP+46]
          mov BYTE PTR [ESP+62],AL
          movzx EAX,BYTE PTR [ESP+47]
          and AL,BYTE PTR [EBX+15]
          mov BYTE PTR [ESP+63],AL
          jmp L_41ae93
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_41afe0:
          push ESI
          push EBX
          sub ESP,20
          mov ESI,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],ESI
          call _strlen
          cmp EAX,32
          je L_41b020
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],ESI
          xor EBX,EBX
          mov DWORD PTR [ESP+4],OFFSET L_45678c
          mov DWORD PTR [ESP],0
          call _log_printf
L_41b014:
          add ESP,20
          mov EAX,EBX
          pop EBX
          pop ESI
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_41b020:
          mov DWORD PTR [ESP],ESI
          call FUN_422350
          test EAX,EAX
          mov EBX,EAX
          je L_41b0e0
          xor EBX,EBX
L_41b034:
          mov DWORD PTR [ESP],ESI
          add EBX,1
          add ESI,2
          call FUN_421300
          mov BYTE PTR [EBX+L_47a11b],AL
          cmp EBX,16
          jne L_41b034
          mov DWORD PTR [ESP+4],OFFSET L_4566eb
          mov DWORD PTR [ESP],1
          xor EBX,EBX
          call _log_printf
L_41b063:
          movzx EAX,BYTE PTR [EBX+L_47a11c]
          mov DWORD PTR [ESP+4],OFFSET L_4566fe
          add EBX,1
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          cmp EBX,16
          jne L_41b063
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_47a11c
          mov EBX,1
          call FUN_4223b0
          test EAX,EAX
          jne L_41b014
          mov DWORD PTR [ESP+4],OFFSET L_47a11c
          mov DWORD PTR [ESP],1
          call FUN_41ae40
          test EAX,EAX
          je L_41b100
          mov DWORD PTR [ESP+4],OFFSET L_456703
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_41b014
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_41b0e0:
          mov DWORD PTR [ESP+4],OFFSET L_45674c
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_41b014
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_41b100:
          mov DWORD PTR [ESP+4],OFFSET L_456708
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_41b014
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_41b120:
          push EDI
          push ESI
          push EBX
          sub ESP,16
          mov EBX,DWORD PTR [ESP+36]
          mov ESI,DWORD PTR [ESP+32]
          mov ECX,DWORD PTR [EBX+4]
          mov EDX,DWORD PTR [EBX+8]
          mov EAX,DWORD PTR [EBX+12]
          mov EDI,DWORD PTR [EBX]
          mov DWORD PTR [ESP+4],OFFSET L_4567eb
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [L_47a120],ECX
          mov DWORD PTR [L_47a124],EDX
          mov DWORD PTR [L_47a128],EAX
          mov DWORD PTR [L_47a11c],EDI
          call _log_printf
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],ESI
          call FUN_423370
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_47a11c
          call FUN_4223b0
          test EAX,EAX
          je L_41b1a0
L_41b184:
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],OFFSET L_456703
          call _log_printf
          add ESP,16
          mov EAX,1
          pop EBX
          pop ESI
          pop EDI
          ret 
L_41b1a0:
          mov DWORD PTR [ESP+4],OFFSET L_47a11c
          mov DWORD PTR [ESP],ESI
          call FUN_41ae40
          test EAX,EAX
          jne L_41b184
          mov DWORD PTR [ESP+4],OFFSET L_456708
          mov DWORD PTR [ESP],ESI
          call _log_printf
          jmp L_41b184
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_41b1d0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,28
          mov EAX,DWORD PTR [ESP+52]
          mov ESI,DWORD PTR [ESP+48]
          cmp AL,16
          jbe L_41b201
          cmp AL,31
          jbe L_41b2c0
          mov EDI,4294967295
          mov EBP,4294967295
L_41b1f5:
          mov EAX,4294967295
          mov EDX,4294967295
          jmp L_41b242
L_41b201:
          je L_41b2f2
          test AL,AL
          movzx EBP,AL
          je L_41b305
          xor EAX,EAX
          xor EDX,EDX
          xor EDI,EDI
          nop
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_41b220:
          mov ECX,EAX
          mov EBX,EDX
          add EDI,1
          shrd ECX,EDX,4
          shr EBX,4
          mov EAX,ECX
          mov ECX,EBX
          or ECX,4026531840
          cmp EDI,EBP
          mov EDX,ECX
          jne L_41b220
          xor EDI,EDI
          xor EBP,EBP
L_41b242:
          lea EBX,DWORD PTR [ESI+56]
          mov DWORD PTR [ESP+4],EDX
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+8],EBX
          call FUN_420b50
          lea EAX,DWORD PTR [ESI+64]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],EBP
          add ESI,72
          mov DWORD PTR [ESP+8],EAX
          call FUN_420b50
          mov DWORD PTR [ESP+4],OFFSET L_4567fe
          mov DWORD PTR [ESP],1
          call _log_printf
          nop
L_41b280:
          movzx EAX,BYTE PTR [EBX]
          mov DWORD PTR [ESP+4],OFFSET L_4566fe
          add EBX,1
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          cmp EBX,ESI
          jne L_41b280
          mov DWORD PTR [ESP+52],OFFSET L_456703
          mov DWORD PTR [ESP+48],1
          add ESP,28
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          jmp _log_printf
          .byte 0x66
          .byte 0x90
L_41b2c0:
          movzx EAX,AL
          xor EDI,EDI
          xor EBP,EBP
          lea EBX,DWORD PTR [EAX-16]
          xor ECX,ECX
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_41b2d0:
          mov EAX,EDI
          mov EDX,EBP
          add ECX,1
          shrd EAX,EBP,4
          shr EDX,4
          mov EDI,EAX
          mov EAX,EDX
          or EAX,4026531840
          cmp ECX,EBX
          mov EBP,EAX
          jb L_41b2d0
          jmp L_41b1f5
L_41b2f2:
          xor EDI,EDI
          xor EBP,EBP
          mov EAX,4294967295
          mov EDX,4294967295
          jmp L_41b242
L_41b305:
          xor EDI,EDI
          xor EBP,EBP
          xor EAX,EAX
          xor EDX,EDX
          jmp L_41b242
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
FUN_41b320:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,28
          mov ESI,DWORD PTR [ESP+48]
          test ESI,ESI
          je L_41b400
          mov EAX,DWORD PTR [L_47a11c]
          mov EDX,DWORD PTR [L_47a120]
          mov DWORD PTR [ESI+24],EAX
          mov DWORD PTR [ESI+28],EDX
          mov EBX,DWORD PTR [L_47a124]
          mov ECX,DWORD PTR [L_47a128]
          mov EBP,DWORD PTR [L_47a11c]
          mov EDI,DWORD PTR [L_47a120]
          mov DWORD PTR [ESI+40],EBX
          mov DWORD PTR [ESI+44],ECX
          mov DWORD PTR [ESI+32],EBP
          mov DWORD PTR [ESI+36],EDI
          mov EAX,DWORD PTR [L_47a124]
          mov EDX,DWORD PTR [L_47a128]
          mov DWORD PTR [ESI+48],EAX
          mov DWORD PTR [ESI+52],EDX
          movzx EAX,BYTE PTR [L_479f15]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [L_47a124],EBX
          mov DWORD PTR [L_47a128],ECX
          lea EBX,DWORD PTR [ESI+32]
          mov DWORD PTR [L_47a11c],EBP
          mov DWORD PTR [L_47a120],EDI
          add ESI,48
          mov DWORD PTR [ESP+4],EAX
          call FUN_41b1d0
          mov DWORD PTR [ESP+4],OFFSET L_456816
          mov DWORD PTR [ESP],1
          call _log_printf
          .byte 0x66   # nop
          nop
L_41b3c0:
          movzx EAX,BYTE PTR [EBX]
          mov DWORD PTR [ESP+4],OFFSET L_4566fe
          add EBX,1
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          cmp EBX,ESI
          jne L_41b3c0
          mov DWORD PTR [ESP+4],OFFSET L_456703
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,28
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x66
          .byte 0x90
L_41b400:
          mov DWORD PTR [ESP+4],OFFSET L_456830
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,28
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
FUN_41b420:
          push EBX
          sub ESP,104
          lea EBX,DWORD PTR [ESP+80]
          lea EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+32],EBX
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],16
          mov DWORD PTR [ESP+8],OFFSET L_47a10c
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP+48],3211929493
          mov DWORD PTR [ESP+52],2566307911
          mov DWORD PTR [ESP+56],1358069084
          mov DWORD PTR [ESP+60],3444919653
          mov DWORD PTR [ESP+64],1936287860
          mov DWORD PTR [ESP+68],1969910633
          mov DWORD PTR [ESP+72],1784771699
          mov DWORD PTR [ESP+76],2037083765
          call _XeCryptHmacSha
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+12],16
          mov DWORD PTR [ESP+8],OFFSET L_47a12c
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [L_47a12c],EAX
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [L_47a130],EAX
          mov EAX,DWORD PTR [ESP+56]
          mov DWORD PTR [L_47a134],EAX
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [L_47a138],EAX
          call _XeCryptRc4
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_47a12c
          call FUN_422ae0
          add ESP,104
          pop EBX
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
L_41b520:
          push EBX
          sub ESP,24
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_47a10c
          call FUN_422ae0
          mov EBX,EAX
          call FUN_41b420
          cmp EBX,2435
          jne L_41b5f0
          cmp EAX,2048
          jne L_41b5f0
          mov DWORD PTR [ESP+4],OFFSET L_45685e
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_47a10c
          mov DWORD PTR [ESP],1
          call FUN_423370
          mov DWORD PTR [ESP+8],2435
          mov DWORD PTR [ESP+4],OFFSET L_456873
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_456890
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_47a12c
          mov DWORD PTR [ESP],1
          call FUN_423370
          mov DWORD PTR [ESP+8],2048
          mov DWORD PTR [ESP+4],OFFSET L_4568a5
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,24
          mov EAX,1
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
L_41b5f0:
          add ESP,24
          xor EAX,EAX
          pop EBX
          ret 
L_41b5f7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_41b600:
          push EBX
          sub ESP,24
          mov EAX,DWORD PTR [ESP+32]
          mov EBX,DWORD PTR [EAX]
          mov ECX,DWORD PTR [EAX+4]
          mov EDX,DWORD PTR [EAX+8]
          mov EAX,DWORD PTR [EAX+12]
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_47a10c
          mov DWORD PTR [L_47a10c],EBX
          mov DWORD PTR [L_47a110],ECX
          mov DWORD PTR [L_47a114],EDX
          mov DWORD PTR [L_47a118],EAX
          call FUN_422ae0
          mov EBX,EAX
          call FUN_41b420
          cmp EBX,2435
          jne L_41b6f0
          cmp EAX,2048
          jne L_41b6f0
          mov DWORD PTR [ESP+4],OFFSET L_45685e
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_47a10c
          mov DWORD PTR [ESP],1
          call FUN_423370
          mov DWORD PTR [ESP+8],2435
          mov DWORD PTR [ESP+4],OFFSET L_456873
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_456890
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_47a12c
          mov DWORD PTR [ESP],1
          call FUN_423370
          mov DWORD PTR [ESP+8],2048
          mov DWORD PTR [ESP+4],OFFSET L_4568a5
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,24
          mov EAX,1
          pop EBX
          ret 
          .byte 0x66
          .byte 0x90
L_41b6f0:
          mov DWORD PTR [ESP+4],OFFSET L_4568c2
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_47a10c
          mov DWORD PTR [ESP],0
          call FUN_423370
          mov DWORD PTR [ESP+4],OFFSET L_4568e0
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,24
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
          .byte 0xbc
          .byte 0x27
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_41b740:
          push EDI
          push ESI
          push EBX
          sub ESP,32
          mov EDI,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],EDI
          call _strlen
          cmp EAX,32
          je L_41b780
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET L_456944
          mov DWORD PTR [ESP],0
          call _log_printf
          xor EAX,EAX
L_41b775:
          add ESP,32
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_41b780:
          mov DWORD PTR [ESP],EDI
          call FUN_422350
          test EAX,EAX
          je L_41b8b0
          mov ESI,EDI
          xor EBX,EBX
L_41b794:
          mov DWORD PTR [ESP],ESI
          add EBX,1
          add ESI,2
          call FUN_421300
          mov BYTE PTR [EBX+L_47a10b],AL
          cmp EBX,16
          jne L_41b794
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_47a10c
          call FUN_422ae0
          mov EBX,EAX
          call FUN_41b420
          cmp EBX,2435
          jne L_41b871
          cmp EAX,2048
          jne L_41b871
          mov DWORD PTR [ESP+4],OFFSET L_45685e
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_47a10c
          mov DWORD PTR [ESP],1
          call FUN_423370
          mov DWORD PTR [ESP+8],2435
          mov DWORD PTR [ESP+4],OFFSET L_456873
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_456890
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_47a12c
          mov DWORD PTR [ESP],1
          call FUN_423370
          mov DWORD PTR [ESP+8],2048
          mov DWORD PTR [ESP+4],OFFSET L_4568a5
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,1
          jmp L_41b775
L_41b871:
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET L_4569a3
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_4569c4
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,32
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_41b8b0:
          mov DWORD PTR [ESP+4],OFFSET L_456904
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+28],EAX
          call _log_printf
          mov EAX,DWORD PTR [ESP+28]
          jmp L_41b775
L_41b8d1:
          jmp L_41b8e0
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
L_41b8e0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,60
          mov EAX,DWORD PTR [ESP+84]
          mov EBP,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP+44],EAX
          mov EAX,DWORD PTR [ESP+88]
          test EAX,EAX
          je L_41b9f6
          lea EAX,DWORD PTR [EBP+EAX*4]
          mov DWORD PTR [ESP+32],0
          mov DWORD PTR [ESP+36],0
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+40],EAX
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_41b930:
          mov EDX,DWORD PTR [EBP]
          mov ESI,DWORD PTR [ESP+24]
          mov EDI,DWORD PTR [ESP+28]
          mov EBX,EDX
          mov EAX,EDX
          mov ECX,EDX
          shr EAX,24
          shl ECX,8
          shl EBX,24
          add EBX,EAX
          mov EAX,ECX
          mov ECX,DWORD PTR [ESP+32]
          and EAX,16711680
          add EBX,EAX
          mov EAX,EDX
          xor EDX,EDX
          shr EAX,8
          and EAX,65280
          add EAX,EBX
          mov EBX,DWORD PTR [ESP+36]
          add ESI,EAX
          adc EDI,EDX
          sub ECX,EAX
          sbb EBX,EDX
          mov EAX,ECX
          mov ECX,ESI
          mov EDX,EBX
          mov EBX,EDI
          shl ECX,29
          shld EBX,ESI,29
          mov ESI,EDI
          add EBP,4
          shr ESI,3
          mov DWORD PTR [ESP+28],EBX
          mov EBX,EDX
          or ESI,ECX
          mov ECX,EAX
          shld EBX,EAX,31
          mov EAX,EDX
          shl ECX,31
          mov DWORD PTR [ESP+24],ESI
          shr EAX,1
          mov DWORD PTR [ESP+36],EBX
          or EAX,ECX
          cmp EBP,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+32],EAX
          jne L_41b930
          mov EAX,DWORD PTR [ESP+24]
          mov EDX,DWORD PTR [ESP+28]
          mov ESI,DWORD PTR [ESP+32]
          mov EDI,DWORD PTR [ESP+36]
L_41b9c7:
          mov EBX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],EDX
          mov DWORD PTR [ESP+8],EBX
          call FUN_420b50
          lea EAX,DWORD PTR [EBX+8]
          mov DWORD PTR [ESP+80],ESI
          mov DWORD PTR [ESP+84],EDI
          mov DWORD PTR [ESP+88],EAX
          add ESP,60
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          jmp FUN_420b50
L_41b9f6:
          xor ESI,ESI
          xor EDI,EDI
          xor EAX,EAX
          xor EDX,EDX
          jmp L_41b9c7
L_41ba00:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,16
          mov ESI,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+12],2035184962
          test ESI,ESI
          je L_41ba6a
          mov EDX,DWORD PTR [ESP+36]
          mov ECX,117
          mov EAX,66
          mov EBX,1
          add ESI,EDX
          jmp L_41ba35
          .byte 0x66   # nop
          nop
L_41ba30:
          movzx EAX,BYTE PTR [ESP+EDI*1+12]
L_41ba35:
          xor AL,BYTE PTR [EDX]
          and EBX,3
          add EDX,1
          mov EDI,EBX
          mov BYTE PTR [EDX-1],AL
          movzx EAX,AL
          imul EAX,EAX,251
          add ECX,EAX
          sar EAX,8
          mov BYTE PTR [ESP+EBX*1+12],CL
          lea EBX,DWORD PTR [EBX+1]
          mov ECX,EAX
          mov EBP,EBX
          and EBP,3
          add CL,BYTE PTR [ESP+EBP*1+12]
          cmp EDX,ESI
          mov BYTE PTR [ESP+EBP*1+12],CL
          jne L_41ba30
L_41ba6a:
          add ESP,16
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
FUN_41ba80:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,76
          mov EBX,DWORD PTR [ESP+104]
          mov DWORD PTR [ESP],EBX
          call _malloc
          mov EDI,DWORD PTR [ESP+96]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+44],EAX
          mov DWORD PTR [ESP+4],EDI
          mov EDI,EAX
          lea ESI,DWORD PTR [EDI+EBX*1-4]
          call _memcpy
          mov DWORD PTR [ESP+4],4
          mov DWORD PTR [ESP],ESI
          call FUN_4223b0
          test EAX,EAX
          jne L_41bb15
          mov DWORD PTR [ESP+4],OFFSET L_4569e4
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EDI
          call FUN_401730
          test EAX,EAX
          je L_41bd43
          mov EAX,DWORD PTR [ESP+96]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EAX
          call _memcpy
          mov DWORD PTR [ESP+4],OFFSET L_456a21
          mov DWORD PTR [ESP],1
          call _log_printf
L_41bb15:
          mov DWORD PTR [ESP+4],4
          mov DWORD PTR [ESP],ESI
          call FUN_4223b0
          test EAX,EAX
          jne L_41bc60
L_41bb2d:
          mov EAX,DWORD PTR [ESP+96]
          mov EDI,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+8],EBX
          shr EBX,2
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],EDI
          call _memcpy
          test EBX,EBX
          je L_41be81
          lea EAX,DWORD PTR [EDI+EBX*4]
          mov EBP,EDI
          mov DWORD PTR [ESP+32],0
          mov DWORD PTR [ESP+36],0
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+40],EAX
          mov DWORD PTR [ESP+28],0
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_41bb80:
          mov EDX,DWORD PTR [EBP]
          mov ESI,DWORD PTR [ESP+24]
          mov EDI,DWORD PTR [ESP+28]
          mov EBX,EDX
          mov EAX,EDX
          mov ECX,EDX
          shr EAX,24
          shl ECX,8
          shl EBX,24
          add EBX,EAX
          mov EAX,ECX
          mov ECX,DWORD PTR [ESP+32]
          and EAX,16711680
          add EBX,EAX
          mov EAX,EDX
          xor EDX,EDX
          shr EAX,8
          and EAX,65280
          add EAX,EBX
          mov EBX,DWORD PTR [ESP+36]
          add ESI,EAX
          adc EDI,EDX
          sub ECX,EAX
          sbb EBX,EDX
          mov EAX,ECX
          mov ECX,ESI
          mov EDX,EBX
          mov EBX,EDI
          shl ECX,29
          shld EBX,ESI,29
          mov ESI,EDI
          add EBP,4
          shr ESI,3
          mov DWORD PTR [ESP+28],EBX
          mov EBX,EDX
          or ESI,ECX
          mov ECX,EAX
          shld EBX,EAX,31
          mov EAX,EDX
          shl ECX,31
          mov DWORD PTR [ESP+24],ESI
          shr EAX,1
          mov DWORD PTR [ESP+36],EBX
          or EAX,ECX
          cmp EBP,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+32],EAX
          jne L_41bb80
          mov EAX,DWORD PTR [ESP+24]
          mov EDX,DWORD PTR [ESP+28]
          mov ESI,DWORD PTR [ESP+32]
          mov EDI,DWORD PTR [ESP+36]
L_41bc17:
          mov EBX,DWORD PTR [ESP+100]
          mov DWORD PTR [ESP+4],EDX
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+8],EBX
          call FUN_420b50
          mov EAX,DWORD PTR [ESP+100]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],EDI
          add EAX,8
          mov DWORD PTR [ESP+8],EAX
          call FUN_420b50
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EAX
          call _free
          add ESP,76
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x90
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_41bc60:
          mov EAX,DWORD PTR [L_479ea8]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+96]
          mov DWORD PTR [ESP],EAX
          call FUN_40bd80
          mov EDX,DWORD PTR [L_479ea8]
          cmp EDX,1
          je L_41bde0
          cmp EDX,5
          jbe L_41bd81
          test EAX,EAX
          je L_41be68
          mov DWORD PTR [ESP+4],OFFSET L_456b20
          mov DWORD PTR [ESP],0
          call _log_printf
L_41bcad:
          mov EAX,DWORD PTR [L_479f00]
L_41bcb2:
          and EAX,4148166655
          mov DWORD PTR [L_479f00],EAX
L_41bcbc:
          and EAX,146800640
          jne L_41be11
L_41bcc7:
          mov EAX,DWORD PTR [L_44a640]
          mov EDI,DWORD PTR [ESP+96]
          test EBX,EBX
          mov DWORD PTR [ESP+60],2035184962
          mov DWORD PTR [EDI],EAX
          je L_41bb2d
          mov EAX,EBX
          mov ECX,EDI
          mov EDX,66
          add EAX,EDI
          mov DWORD PTR [ESP+104],EBX
          mov EDI,1
          mov EBP,EAX
          mov EAX,117
          jmp L_41bd05
          .byte 0x90
L_41bd00:
          movzx EDX,BYTE PTR [ESP+EBX*1+60]
L_41bd05:
          xor DL,BYTE PTR [ECX]
          and EDI,3
          add ECX,1
          mov EBX,EDI
          mov BYTE PTR [ECX-1],DL
          movzx EDX,DL
          imul EDX,EDX,251
          add EAX,EDX
          sar EDX,8
          mov BYTE PTR [ESP+EDI*1+60],AL
          lea EDI,DWORD PTR [EDI+1]
          mov EAX,EDX
          mov ESI,EDI
          and ESI,3
          add AL,BYTE PTR [ESP+ESI*1+60]
          cmp EBP,ECX
          mov BYTE PTR [ESP+ESI*1+60],AL
          jne L_41bd00
          mov EBX,DWORD PTR [ESP+104]
          jmp L_41bb2d
L_41bd43:
          mov DWORD PTR [ESP+4],OFFSET L_456a2a
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_456a34
          mov DWORD PTR [ESP],0
          call _log_printf
          test BYTE PTR [L_479f02],32
          jne L_41bdc0
L_41bd74:
          add ESP,76
          mov EAX,1
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_41bd81:
          test EAX,EAX
          je L_41be2a
          cmp EDX,3
          je L_41bf19
          sub EDX,4
          cmp EDX,1
          jbe L_41beaf
          mov DWORD PTR [ESP+4],OFFSET L_456c1c
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [L_479f00]
          jmp L_41bcbc
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_41bdc0:
          mov EAX,DWORD PTR [ESP+96]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EAX
          call _memcpy
          jmp L_41bb15
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_41bde0:
          test EAX,EAX
          je L_41be8e
          mov DWORD PTR [ESP+4],OFFSET L_456a88
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_479f00]
          test EAX,2097152
          jne L_41bcb2
          jmp L_41bd74
L_41be11:
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+96]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EAX
          call FUN_40c020
          jmp L_41bcc7
L_41be2a:
          cmp EDX,3
          je L_41beeb
          sub EDX,4
          cmp EDX,1
          jbe L_41becd
          mov DWORD PTR [ESP+4],OFFSET L_456c9c
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_479f00]
          test EAX,2097152
          jne L_41bcbc
          jmp L_41bd74
L_41be68:
          mov DWORD PTR [ESP+4],OFFSET L_456ba0
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_41bcad
L_41be81:
          xor ESI,ESI
          xor EDI,EDI
          xor EAX,EAX
          xor EDX,EDX
          jmp L_41bc17
L_41be8e:
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP+4],OFFSET L_456af4
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_41bcad
L_41beaf:
          mov DWORD PTR [ESP+4],OFFSET L_456be4
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [L_479f00]
          jmp L_41bcbc
L_41becd:
          mov DWORD PTR [ESP+4],OFFSET L_456ba0
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [L_479f00]
          jmp L_41bcbc
L_41beeb:
          mov EAX,DWORD PTR [L_479f00]
          test EAX,134217728
          jne L_41bcbc
          mov DWORD PTR [ESP+4],OFFSET L_456c3c
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_479f00]
          jmp L_41bcbc
L_41bf19:
          mov DWORD PTR [ESP+4],OFFSET L_456bc0
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [L_479f00]
          and EAX,4160749567
          mov DWORD PTR [L_479f00],EAX
          jmp L_41bcbc
L_41bf41:
          jmp FUN_41bf50
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
FUN_41bf50:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,76
          mov EDX,DWORD PTR [L_44a6a4]
          mov EBX,DWORD PTR [ESP+100]
          mov EAX,DWORD PTR [ESP+96]
          mov EDI,DWORD PTR [ESP+104]
          mov EBP,DWORD PTR [ESP+112]
          mov ESI,DWORD PTR [ESP+108]
          mov DWORD PTR [EBX+16],EDX
          mov EDX,DWORD PTR [L_44a6a8]
          mov DWORD PTR [ESP+60],EAX
          mov DWORD PTR [EBX+20],EDX
          mov EDX,DWORD PTR [L_44a6ac]
          mov DWORD PTR [EBX+24],EDX
          mov EDX,DWORD PTR [L_44a6b0]
          mov DWORD PTR [EBX+28],EDX
          lea EDX,DWORD PTR [EBX+16]
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_47a10c
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP+32],EDI
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],16
          call _XeCryptHmacSha
          test EBP,EBP
          lea EAX,DWORD PTR [EBX+32]
          jne L_41c097
          movzx EAX,BYTE PTR [L_479572]
          mov DWORD PTR [ESP+4],OFFSET L_456cfc
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+16],EAX
          movzx EAX,BYTE PTR [L_479571]
          mov DWORD PTR [ESP+12],EAX
          movzx EAX,BYTE PTR [L_479570]
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          movzx EAX,WORD PTR [L_479570]
          mov ECX,DWORD PTR [ESP+60]
          mov WORD PTR [EBX+32],AX
          movzx EAX,BYTE PTR [L_479572]
          mov BYTE PTR [EBX+34],AL
          movzx EAX,BYTE PTR [L_479f14]
          mov BYTE PTR [EBX+35],AL
          lea EAX,DWORD PTR [EBX+32]
          add EBX,48
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+32],EBX
          mov DWORD PTR [ESP+16],EAX
          mov DWORD PTR [ESP+28],16
          mov DWORD PTR [ESP+24],ECX
          mov DWORD PTR [ESP+20],16
          mov DWORD PTR [ESP+12],16
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_47a11c
          mov DWORD PTR [ESP+60],EAX
          call _XeCryptHmacSha
          mov EAX,DWORD PTR [ESP+60]
L_41c097:
          sub ESI,32
          mov DWORD PTR [ESP+96],EDI
          mov DWORD PTR [ESP+104],EAX
          mov DWORD PTR [ESP+108],ESI
          mov DWORD PTR [ESP+100],16
          add ESP,76
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          jmp _XeCryptRc4
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_41c0c0:
          push ESI
          push EBX
          xor EDX,EDX
          xor ECX,ECX
          sub ESP,52
          mov WORD PTR [L_479570],DX
          mov EDX,DWORD PTR [L_44a6a4]
          mov EAX,DWORD PTR [ESP+64]
          mov BYTE PTR [L_479572],0
          mov DWORD PTR [EAX+16],EDX
          mov EDX,DWORD PTR [L_44a6a8]
          lea EBX,DWORD PTR [EAX+32]
          lea ESI,DWORD PTR [EAX+36]
          mov DWORD PTR [EAX+20],EDX
          mov EDX,DWORD PTR [L_44a6ac]
          and ESI,4294967292
          mov DWORD PTR [EAX+24],EDX
          mov EDX,DWORD PTR [L_44a6b0]
          mov DWORD PTR [EAX+32],0
          mov DWORD PTR [EAX+28],EDX
          mov EDX,EBX
          mov DWORD PTR [EBX+28],0
          sub EDX,ESI
          add EDX,32
          and EDX,4294967292
L_41c120:
          mov DWORD PTR [ESI+ECX*1],0
          add ECX,4
          cmp ECX,EDX
          jb L_41c120
          mov ECX,DWORD PTR [ESP+68]
          add EAX,16
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+32],ECX
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],16
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_47a10c
          call _XeCryptHmacSha
          mov EAX,DWORD PTR [ESP+72]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],16
          sub EAX,32
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP],EAX
          call _XeCryptRc4
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
FUN_41c1b0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,76
          mov EAX,DWORD PTR [L_44a6a4]
          mov EBX,DWORD PTR [ESP+100]
          mov EBP,DWORD PTR [ESP+96]
          mov EDI,DWORD PTR [ESP+104]
          mov ESI,DWORD PTR [ESP+108]
          mov DWORD PTR [EBX+16],EAX
          mov EAX,DWORD PTR [L_44a6a8]
          mov DWORD PTR [EBX+20],EAX
          mov EAX,DWORD PTR [L_44a6ac]
          mov DWORD PTR [EBX+24],EAX
          mov EAX,DWORD PTR [L_44a6b0]
          mov DWORD PTR [EBX+28],EAX
          mov EAX,DWORD PTR [ESP+112]
          test EAX,EAX
          jne L_41c2e0
          lea EAX,DWORD PTR [EBX+16]
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+32],EDI
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],16
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_47a10c
          call _XeCryptHmacSha
          movzx EAX,WORD PTR [L_479570]
          mov WORD PTR [EBX+32],AX
          movzx EAX,BYTE PTR [L_479572]
          mov BYTE PTR [EBX+34],AL
          movzx EAX,BYTE PTR [L_479f14]
          mov BYTE PTR [EBX+35],AL
          lea EAX,DWORD PTR [EBX+32]
          add EBX,48
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+32],EBX
          mov DWORD PTR [ESP+16],EAX
          mov DWORD PTR [ESP+28],16
          mov DWORD PTR [ESP+24],EBP
          mov DWORD PTR [ESP+20],16
          mov DWORD PTR [ESP+12],16
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_47a11c
          mov DWORD PTR [ESP+60],EAX
          call _XeCryptHmacSha
          mov EAX,DWORD PTR [ESP+60]
L_41c2b3:
          sub ESI,32
          mov DWORD PTR [ESP+96],EDI
          mov DWORD PTR [ESP+104],EAX
          mov DWORD PTR [ESP+108],ESI
          mov DWORD PTR [ESP+100],16
          add ESP,76
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          jmp _XeCryptRc4
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_41c2e0:
          lea EAX,DWORD PTR [EBX+32]
          lea ECX,DWORD PTR [EBX+36]
          mov DWORD PTR [EBX+32],0
          xor EBP,EBP
          and ECX,4294967292
          mov EDX,EAX
          mov DWORD PTR [EAX+28],0
          sub EDX,ECX
          add EDX,32
          and EDX,4294967292
L_41c303:
          mov DWORD PTR [ECX+EBP*1],0
          add EBP,4
          cmp EBP,EDX
          jb L_41c303
          add EBX,16
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+32],EDI
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],16
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_47a10c
          mov DWORD PTR [ESP+60],EAX
          call _XeCryptHmacSha
          mov EAX,DWORD PTR [ESP+60]
          jmp L_41c2b3
          .byte 0x8d
          .byte 0x76
          .byte 0x0
FUN_41c370:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,92
          mov EBP,DWORD PTR [ESP+124]
          mov EBX,DWORD PTR [ESP+116]
          lea EAX,DWORD PTR [EBP+6]
          mov DWORD PTR [ESP],EAX
          call FUN_420ab0
          mov EDX,DWORD PTR [L_44a694]
          mov EDI,EAX
          mov ECX,OFFSET L_479560
          and DI,1
          mov DWORD PTR [EBX+16],EDX
          mov EDX,DWORD PTR [L_44a698]
          mov DWORD PTR [EBX+20],EDX
          mov EDX,DWORD PTR [L_44a69c]
          mov DWORD PTR [EBX+24],EDX
          mov EDX,DWORD PTR [L_44a6a0]
          mov DWORD PTR [EBX+28],EDX
          mov EDX,OFFSET L_47a11c
          mov ESI,EDX
          cmovne ESI,ECX
          test AH,8
          jne L_41c570
L_41c3cc:
          test AH,16
          je L_41c4e0
          mov DWORD PTR [ESP+4],OFFSET L_456d40
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [EBP]
          mov DWORD PTR [ESP+64],EAX
          mov EAX,DWORD PTR [EBP+4]
          mov DWORD PTR [ESP+68],EAX
          mov EAX,DWORD PTR [EBP+8]
          mov BYTE PTR [ESP+70],0
          mov BYTE PTR [ESP+71],0
          mov DWORD PTR [ESP+72],EAX
          mov EAX,DWORD PTR [EBP+12]
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+28],16
          mov DWORD PTR [ESP+76],EAX
          mov EAX,DWORD PTR [ESP+128]
          mov DWORD PTR [ESP+32],EAX
          lea EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+24],EAX
L_41c432:
          lea EAX,DWORD PTR [EBX+16]
          mov DWORD PTR [ESP+20],16
          mov DWORD PTR [ESP+16],ESI
          mov DWORD PTR [ESP+12],16
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+120]
          mov DWORD PTR [ESP],EAX
          call _XeCryptHmacSha
          mov EDX,DWORD PTR [ESP+136]
          test EDX,EDX
          jne L_41c591
          movzx EAX,WORD PTR [L_479570]
          test DI,DI
          mov WORD PTR [EBX+32],AX
          movzx EAX,BYTE PTR [L_479572]
          mov BYTE PTR [EBX+34],AL
          movzx EAX,BYTE PTR [L_479f14]
          mov BYTE PTR [EBX+35],AL
          je L_41c510
          lea EDI,DWORD PTR [EBX+32]
          mov DWORD PTR [ESP+4],OFFSET L_456d6c
          mov DWORD PTR [ESP],1
          call _log_printf
L_41c4ab:
          mov EAX,DWORD PTR [ESP+132]
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],16
          sub EAX,32
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+128]
          mov DWORD PTR [ESP],EAX
          call _XeCryptRc4
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
L_41c4e0:
          mov EAX,DWORD PTR [ESP+128]
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+32],EAX
          jmp L_41c432
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_41c510:
          mov EAX,DWORD PTR [ESP+112]
          lea EDI,DWORD PTR [EBX+32]
          add EBX,48
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+32],EBX
          mov DWORD PTR [ESP+28],16
          mov DWORD PTR [ESP+20],16
          mov DWORD PTR [ESP+24],EAX
          mov EAX,DWORD PTR [ESP+128]
          mov DWORD PTR [ESP+16],EDI
          mov DWORD PTR [ESP+12],16
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_47a11c
          mov DWORD PTR [ESP+8],EAX
          call _XeCryptHmacSha
          jmp L_41c4ab
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_41c570:
          mov DWORD PTR [ESP+4],OFFSET L_456d22
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+60],EAX
          call _log_printf
          mov EAX,DWORD PTR [ESP+60]
          jmp L_41c3cc
L_41c591:
          lea EDI,DWORD PTR [EBX+32]
          xor EAX,EAX
          mov BYTE PTR [L_479572],0
          mov WORD PTR [L_479570],AX
          add EBX,36
          mov DWORD PTR [EBX-4],0
          mov EAX,EDI
          and EBX,4294967292
          mov DWORD PTR [EDI+28],0
          sub EAX,EBX
          xor EDX,EDX
          add EAX,32
          and EAX,4294967292
L_41c5c3:
          mov DWORD PTR [EBX+EDX*1],0
          add EDX,4
          cmp EDX,EAX
          jb L_41c5c3
          jmp L_41c4ab
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_41c5e0:
          push ESI
          push EBX
          sub ESP,68
          mov EDX,DWORD PTR [L_44a694]
          mov EBX,DWORD PTR [ESP+80]
          mov ESI,DWORD PTR [ESP+84]
          lea EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+48],0
          mov DWORD PTR [ESP+52],0
          mov DWORD PTR [ESP+56],0
          mov DWORD PTR [ESP+60],0
          mov DWORD PTR [EBX+16],EDX
          mov EDX,DWORD PTR [L_44a698]
          mov DWORD PTR [EBX+20],EDX
          mov EDX,DWORD PTR [L_44a69c]
          mov DWORD PTR [EBX+24],EDX
          mov EDX,DWORD PTR [L_44a6a0]
          mov DWORD PTR [EBX+28],EDX
          lea EDX,DWORD PTR [EBX+16]
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],16
          add EBX,32
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP+32],ESI
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+20],0
          call _XeCryptHmacSha
          mov EAX,DWORD PTR [ESP+88]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],16
          sub EAX,32
          mov DWORD PTR [ESP+12],EAX
          call _XeCryptRc4
          add ESP,68
          pop EBX
          pop ESI
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_41c6b0:
          push EDI
          push ESI
          push EBX
          sub ESP,48
          mov EAX,DWORD PTR [L_44a684]
          mov EBX,DWORD PTR [ESP+64]
          mov ESI,DWORD PTR [ESP+76]
          mov EDI,DWORD PTR [ESP+72]
          mov DWORD PTR [EBX+16],EAX
          mov EAX,DWORD PTR [L_44a688]
          sub ESI,32
          mov DWORD PTR [EBX+20],EAX
          mov EAX,DWORD PTR [L_44a68c]
          mov DWORD PTR [EBX+24],EAX
          mov EAX,DWORD PTR [L_44a690]
          mov DWORD PTR [EBX+28],EAX
          lea EAX,DWORD PTR [EBX+16]
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],16
          add EBX,32
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP+32],EDI
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+24],0
          call _XeCryptHmacSha
          mov DWORD PTR [ESP+76],ESI
          mov DWORD PTR [ESP+72],EBX
          mov DWORD PTR [ESP+64],EDI
          mov DWORD PTR [ESP+68],16
          add ESP,48
          pop EBX
          pop ESI
          pop EDI
          jmp _XeCryptRc4
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_41c760:
          push EDI
          push ESI
          push EBX
          sub ESP,48
          mov EAX,DWORD PTR [L_44a684]
          mov EBX,DWORD PTR [ESP+64]
          mov ESI,DWORD PTR [ESP+72]
          mov EDI,DWORD PTR [ESP+76]
          mov DWORD PTR [EBX+16],EAX
          mov EAX,DWORD PTR [L_44a688]
          sub EDI,32
          mov DWORD PTR [EBX+20],EAX
          mov EAX,DWORD PTR [L_44a68c]
          mov DWORD PTR [EBX+24],EAX
          mov EAX,DWORD PTR [L_44a690]
          mov DWORD PTR [EBX+28],EAX
          lea EAX,DWORD PTR [EBX+16]
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],16
          add EBX,32
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP+32],ESI
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+24],0
          call _XeCryptHmacSha
          mov DWORD PTR [ESP+32],ESI
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],16
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_47a11c
          call _XeCryptHmacSha
          mov DWORD PTR [ESP+76],EDI
          mov DWORD PTR [ESP+72],EBX
          mov DWORD PTR [ESP+64],ESI
          mov DWORD PTR [ESP+68],16
          add ESP,48
          pop EBX
          pop ESI
          pop EDI
          jmp _XeCryptRc4
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_41c860:
          push EDI
          push ESI
          push EBX
          sub ESP,48
          mov EAX,DWORD PTR [L_44a674]
          mov EBX,DWORD PTR [ESP+64]
          mov ESI,DWORD PTR [ESP+76]
          mov EDI,DWORD PTR [ESP+72]
          mov DWORD PTR [EBX+16],EAX
          mov EAX,DWORD PTR [L_44a678]
          sub ESI,32
          mov DWORD PTR [EBX+20],EAX
          mov EAX,DWORD PTR [L_44a67c]
          mov DWORD PTR [EBX+24],EAX
          mov EAX,DWORD PTR [L_44a680]
          mov DWORD PTR [EBX+28],EAX
          lea EAX,DWORD PTR [EBX+16]
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],16
          add EBX,32
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP+32],EDI
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+24],0
          call _XeCryptHmacSha
          mov DWORD PTR [ESP+76],ESI
          mov DWORD PTR [ESP+72],EBX
          mov DWORD PTR [ESP+64],EDI
          mov DWORD PTR [ESP+68],16
          add ESP,48
          pop EBX
          pop ESI
          pop EDI
          jmp _XeCryptRc4
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_41c910:
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
FUN_41ca20:
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
          mov EAX,DWORD PTR [L_44a664]
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
          mov DWORD PTR [ESP],OFFSET L_47a10c
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
          cmp DWORD PTR [L_479ea8],2
          mov EAX,DWORD PTR [EBX+1036]
          je L_41cdb0
          mov BYTE PTR [EAX+539],0
L_41cbd0:
          movzx ECX,WORD PTR [L_479570]
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
          mov DWORD PTR [ESP],OFFSET L_47a10c
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
          mov DWORD PTR [ESP],OFFSET L_47a11c
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
          mov DWORD PTR [ESP],OFFSET L_47a10c
          call _XeCryptHmacSha
          jmp L_41cd2a
L_41ce47:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_41ce50:
          push EDI
          push ESI
          push EBX
          sub ESP,48
          mov EAX,DWORD PTR [L_44a654]
          mov EBX,DWORD PTR [ESP+64]
          mov ESI,DWORD PTR [ESP+76]
          mov EDI,DWORD PTR [ESP+72]
          mov DWORD PTR [EBX+16],EAX
          mov EAX,DWORD PTR [L_44a658]
          sub ESI,32
          mov DWORD PTR [EBX+20],EAX
          mov EAX,DWORD PTR [L_44a65c]
          mov DWORD PTR [EBX+24],EAX
          mov EAX,DWORD PTR [L_44a660]
          mov DWORD PTR [EBX+28],EAX
          lea EAX,DWORD PTR [EBX+16]
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],16
          add EBX,32
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP+32],EDI
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+24],0
          call _XeCryptHmacSha
          mov DWORD PTR [ESP+76],ESI
          mov DWORD PTR [ESP+72],EBX
          mov DWORD PTR [ESP+64],EDI
          mov DWORD PTR [ESP+68],16
          add ESP,48
          pop EBX
          pop ESI
          pop EDI
          jmp _XeCryptRc4
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_41cf00:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,92
          mov EAX,DWORD PTR [L_44a64c]
          mov EDX,DWORD PTR [L_44a650]
          mov ESI,DWORD PTR [ESP+112]
          lea EDI,DWORD PTR [ESP+64]
          mov BYTE PTR [ESP+62],7
          mov BYTE PTR [ESP+63],18
          mov DWORD PTR [ESI+16],EAX
          mov EAX,DWORD PTR [ESP+116]
          lea EBP,DWORD PTR [ESI+16]
          mov DWORD PTR [ESI+20],EDX
          mov DWORD PTR [ESP+32],ESI
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+28],0
          lea EBX,DWORD PTR [EAX-16]
          lea EAX,DWORD PTR [ESP+62]
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+20],2
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP+16],EAX
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP],OFFSET L_47a11c
          mov DWORD PTR [ESP+36],16
          call _XeCryptHmacSha
          mov DWORD PTR [ESP+32],EDI
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],16
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_47a11c
          call _XeCryptHmacSha
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],16
          call _XeCryptRc4
          add ESP,92
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
L_41cff0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,92
          mov EAX,DWORD PTR [L_44a644]
          mov EDX,DWORD PTR [L_44a648]
          mov ESI,DWORD PTR [ESP+112]
          lea EDI,DWORD PTR [ESP+64]
          mov BYTE PTR [ESP+62],7
          mov BYTE PTR [ESP+63],18
          mov DWORD PTR [ESI+16],EAX
          mov EAX,DWORD PTR [ESP+116]
          lea EBP,DWORD PTR [ESI+16]
          mov DWORD PTR [ESI+20],EDX
          mov DWORD PTR [ESP+32],ESI
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+28],0
          lea EBX,DWORD PTR [EAX-16]
          lea EAX,DWORD PTR [ESP+62]
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+20],2
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP+16],EAX
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP],OFFSET L_47a11c
          mov DWORD PTR [ESP+36],16
          call _XeCryptHmacSha
          mov DWORD PTR [ESP+32],EDI
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],16
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_47a11c
          call _XeCryptHmacSha
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],16
          call _XeCryptRc4
          add ESP,92
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
FUN_41d0e0:
          push EBP
          push EDI
          mov EAX,OFFSET L_456d9f
          push ESI
          push EBX
          mov ESI,OFFSET L_456da9
          mov EBX,OFFSET L_456db0
          sub ESP,108
          mov ECX,DWORD PTR [ESP+132]
          mov EDI,DWORD PTR [ESP+128]
          test ECX,ECX
          cmove ESI,EAX
          mov EAX,OFFSET L_456da2
          cmove EBX,EAX
          mov EAX,DWORD PTR [EDI+1040]
          cmp EAX,16368
          je L_41d490
          cmp EAX,16384
          je L_41d150
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_456dbc
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,108
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
L_41d150:
          mov EBP,DWORD PTR [EDI+1036]
L_41d156:
          mov DWORD PTR [ESP],16384
          mov DWORD PTR [ESP+56],ECX
          call _malloc
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP+8],16384
          mov EBP,EAX
          mov DWORD PTR [ESP],EAX
          call _memcpy
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+52],EBP
          call FUN_4223b0
          test EAX,EAX
          mov ECX,DWORD PTR [ESP+56]
          je L_41d300
          mov DWORD PTR [ESP+4],8
          mov EAX,DWORD PTR [EDI+1036]
          mov DWORD PTR [ESP+56],ECX
          add EAX,88
          mov DWORD PTR [ESP],EAX
          call FUN_4223b0
          test EAX,EAX
          mov ECX,DWORD PTR [ESP+56]
          je L_41d503
          lea EAX,DWORD PTR [ESP+78]
          mov ESI,DWORD PTR [EDI+1040]
          mov EBX,DWORD PTR [EDI+1036]
          lea EBP,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP+56],EAX
L_41d1dd:
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+60],ECX
          mov DWORD PTR [ESP+4],EAX
          call _memcpy
          mov ECX,DWORD PTR [ESP+60]
          test ECX,ECX
          je L_41d3a3
          mov EBX,DWORD PTR [EDI+1036]
          mov EDX,DWORD PTR [L_44a648]
          mov ECX,DWORD PTR [EDI+1040]
          mov EAX,DWORD PTR [L_44a644]
          mov BYTE PTR [ESP+78],7
          mov BYTE PTR [ESP+79],18
          mov DWORD PTR [EBX+20],EDX
          mov EDX,DWORD PTR [ESP+56]
          mov DWORD PTR [EBX+16],EAX
          lea ESI,DWORD PTR [ECX-16]
          lea EAX,DWORD PTR [EBX+16]
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+32],EBX
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+16],EDX
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+20],2
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_47a11c
          mov DWORD PTR [ESP+56],EAX
          call _XeCryptHmacSha
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+32],EBP
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],16
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_47a11c
          call _XeCryptHmacSha
          mov EAX,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+8],EAX
          call _XeCryptRc4
L_41d2e2:
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+128],EAX
          add ESP,108
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          jmp _free
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_41d300:
          lea EDX,DWORD PTR [ESP+78]
          lea EBP,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+32],EBP
          mov DWORD PTR [ESP+20],2
          mov DWORD PTR [ESP+56],EDX
          mov DWORD PTR [ESP+16],EDX
          mov EDX,DWORD PTR [EDI+1040]
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_47a11c
          mov DWORD PTR [ESP+60],ECX
          mov BYTE PTR [ESP+78],7
          mov BYTE PTR [ESP+79],18
          lea EAX,DWORD PTR [EDX-16]
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+52]
          add EAX,16
          mov DWORD PTR [ESP+8],EAX
          call _XeCryptHmacSha
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+8],16
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EAX
          call _memcmp
          test EAX,EAX
          mov ECX,DWORD PTR [ESP+60]
          jne L_41d540
          mov ESI,DWORD PTR [EDI+1040]
          mov EBX,DWORD PTR [EDI+1036]
          jmp L_41d1dd
L_41d3a3:
          mov EAX,DWORD PTR [EDI+1036]
          mov DWORD PTR [ESP],EAX
          call FUN_4131a0
          mov EBX,DWORD PTR [EDI+1036]
          mov EAX,DWORD PTR [L_44a64c]
          mov ECX,DWORD PTR [EDI+1040]
          mov BYTE PTR [ESP+78],7
          mov BYTE PTR [ESP+79],18
          mov EDX,DWORD PTR [L_44a650]
          mov DWORD PTR [EBX+16],EAX
          mov EAX,DWORD PTR [ESP+56]
          lea EDI,DWORD PTR [EBX+16]
          lea ESI,DWORD PTR [ECX-16]
          mov DWORD PTR [EBX+20],EDX
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+16],EAX
          mov DWORD PTR [ESP+32],EBX
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+20],2
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_47a11c
          call _XeCryptHmacSha
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+32],EBP
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],16
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_47a11c
          call _XeCryptHmacSha
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],EBP
          call _XeCryptRc4
          jmp L_41d2e2
          .byte 0x90
L_41d490:
          mov DWORD PTR [ESP],16384
          mov DWORD PTR [ESP+56],ECX
          call _malloc
          mov EDX,DWORD PTR [EDI+1036]
          mov DWORD PTR [EAX],0
          mov EBP,EAX
          mov DWORD PTR [EAX+4],0
          mov DWORD PTR [EAX+8],0
          lea EAX,DWORD PTR [EAX+16]
          mov DWORD PTR [EAX-4],0
          mov DWORD PTR [ESP+8],16368
          mov DWORD PTR [ESP+4],EDX
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+52],EDX
          call _memcpy
          mov EDX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP],EDX
          call _free
          mov DWORD PTR [EDI+1036],EBP
          mov DWORD PTR [EDI+1040],16384
          mov ECX,DWORD PTR [ESP+56]
          jmp L_41d156
L_41d503:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_456f80
          lea EBP,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+60],ECX
          call _log_printf
          lea EAX,DWORD PTR [ESP+78]
          mov ESI,DWORD PTR [EDI+1040]
          mov EBX,DWORD PTR [EDI+1036]
          mov ECX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+56],EAX
          jmp L_41d1dd
L_41d540:
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+4],88
          mov DWORD PTR [ESP+60],ECX
          add EAX,56
          mov DWORD PTR [ESP],EAX
          call FUN_4223b0
          test EAX,EAX
          mov ECX,DWORD PTR [ESP+60]
          jne L_41d620
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_456ec8
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+60],ECX
          call _log_printf
          mov EAX,DWORD PTR [EDI+1040]
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [EDI+1036]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP],EAX
          call _memcpy
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+4],16384
          mov DWORD PTR [ESP],EAX
          call FUN_401630
          test EAX,EAX
          mov ECX,DWORD PTR [ESP+60]
          jne L_41d665
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_456f00
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_456f24
          mov DWORD PTR [ESP],0
          call _log_printf
          mov ESI,DWORD PTR [EDI+1040]
          mov EBX,DWORD PTR [EDI+1036]
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EAX
          call _memcpy
          mov ECX,DWORD PTR [ESP+60]
          jmp L_41d1dd
L_41d620:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_456e10
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_456e60
          mov DWORD PTR [ESP],0
          call _log_printf
          mov ESI,DWORD PTR [EDI+1040]
          mov EBX,DWORD PTR [EDI+1036]
          mov ECX,DWORD PTR [ESP+60]
          jmp L_41d1dd
L_41d665:
          mov DWORD PTR [ESP+4],OFFSET L_456f74
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+60],ECX
          call _log_printf
          mov ESI,DWORD PTR [EDI+1040]
          mov EBX,DWORD PTR [EDI+1036]
          mov ECX,DWORD PTR [ESP+60]
          jmp L_41d1dd
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
FUN_41d6a0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,108
          mov EBX,DWORD PTR [ESP+128]
          mov EAX,DWORD PTR [EBX+1040]
          cmp EAX,16384
          je L_41d905
          test EAX,EAX
          je L_41d860
          mov DWORD PTR [ESP+4],OFFSET L_457028
          mov DWORD PTR [ESP],1
          call _log_printf
L_41d6db:
          mov EAX,DWORD PTR [EBX+1036]
          test EAX,EAX
          je L_41d6ed
          mov DWORD PTR [ESP],EAX
          call _free
L_41d6ed:
          mov DWORD PTR [EBX+1040],16384
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],16384
          call _calloc
          mov DWORD PTR [EBX+1036],EAX
          mov EDI,EAX
L_41d713:
          mov DWORD PTR [ESP],16384
          call _malloc
          mov DWORD PTR [ESP+8],16384
          mov ESI,EAX
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EAX
          call _memcpy
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],ESI
          call FUN_4223b0
          test EAX,EAX
          je L_41d880
          mov EDX,DWORD PTR [EBX+1040]
          lea EDI,DWORD PTR [ESP+80]
          lea EBP,DWORD PTR [ESP+78]
L_41d75b:
          mov EAX,DWORD PTR [EBX+1036]
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EAX
          call _memcpy
          mov DWORD PTR [ESP],ESI
          call _free
          mov ESI,DWORD PTR [EBX+1036]
          mov ECX,DWORD PTR [EBX+1040]
          mov EAX,DWORD PTR [L_44a64c]
          mov EDX,DWORD PTR [L_44a650]
          mov BYTE PTR [ESP+78],7
          mov BYTE PTR [ESP+79],18
          lea EBX,DWORD PTR [ECX-16]
          mov DWORD PTR [ESI+16],EAX
          lea EAX,DWORD PTR [ESI+16]
          mov DWORD PTR [ESI+20],EDX
          mov DWORD PTR [ESP+32],ESI
          mov DWORD PTR [ESP+16],EBP
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+20],2
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_47a11c
          mov DWORD PTR [ESP+60],EAX
          call _XeCryptHmacSha
          mov DWORD PTR [ESP+32],EDI
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],16
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_47a11c
          call _XeCryptHmacSha
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP+8],EAX
          call _XeCryptRc4
          add ESP,108
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x66
          .byte 0x90
L_41d860:
          mov DWORD PTR [ESP+4],OFFSET L_456fc0
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_41d6db
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_41d880:
          lea EDI,DWORD PTR [ESP+80]
          lea EBP,DWORD PTR [ESP+78]
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+32],EDI
          mov DWORD PTR [ESP+20],2
          mov DWORD PTR [ESP+16],EBP
          mov EAX,DWORD PTR [EBX+1040]
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_47a11c
          mov BYTE PTR [ESP+78],7
          mov BYTE PTR [ESP+79],18
          sub EAX,16
          mov DWORD PTR [ESP+12],EAX
          lea EAX,DWORD PTR [ESI+16]
          mov DWORD PTR [ESP+8],EAX
          call _XeCryptHmacSha
          mov DWORD PTR [ESP+8],16
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],ESI
          call _memcmp
          test EAX,EAX
          jne L_41d910
L_41d8fa:
          mov EDX,DWORD PTR [EBX+1040]
          jmp L_41d75b
L_41d905:
          mov EDI,DWORD PTR [EBX+1036]
          jmp L_41d713
L_41d910:
          mov DWORD PTR [ESP+4],OFFSET L_457088
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EDX,DWORD PTR [EBX+1040]
          mov EAX,DWORD PTR [EBX+1036]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP+4],EAX
          call _memcpy
          mov DWORD PTR [ESP+4],16384
          mov DWORD PTR [ESP],ESI
          call FUN_401630
          test EAX,EAX
          jne L_41d990
          mov DWORD PTR [ESP+4],OFFSET L_4570c8
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EDX,DWORD PTR [EBX+1040]
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP+60],EDX
          call _memset
          mov EDX,DWORD PTR [ESP+60]
          jmp L_41d75b
          .byte 0x90
L_41d990:
          mov DWORD PTR [ESP+4],OFFSET L_456f74
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_41d8fa
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_41d9b0:
          push ESI
          push EBX
          sub ESP,68
          mov EBX,DWORD PTR [ESP+80]
          mov EAX,DWORD PTR [EBX+1040]
          cmp EAX,1024
          je L_41db60
          test EAX,EAX
          je L_41db45
          mov DWORD PTR [ESP+4],OFFSET L_457178
          mov DWORD PTR [ESP],1
          call _log_printf
L_41d9e6:
          mov EAX,DWORD PTR [EBX+1036]
          mov DWORD PTR [ESP],EAX
          call _free
          mov DWORD PTR [EBX+1040],1024
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],1024
          call _calloc
          mov DWORD PTR [EBX+1036],EAX
L_41da18:
          mov EDX,DWORD PTR [L_44a5e0]
          mov ECX,DWORD PTR [L_44a5e4]
          lea ESI,DWORD PTR [ESP+48]
          mov DWORD PTR [EAX+16],EDX
          mov DWORD PTR [EAX+20],ECX
          mov EAX,DWORD PTR [ESP+84]
          mov DWORD PTR [ESP+8],8
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [EBX+1036]
          add EAX,32
          mov DWORD PTR [ESP],EAX
          call FUN_4223f0
          mov EAX,DWORD PTR [EBX+1036]
          mov BYTE PTR [EAX+24],1
          movzx EDX,BYTE PTR [L_479f15]
          mov EAX,DWORD PTR [EBX+1036]
          mov BYTE PTR [EAX+25],DL
          mov EAX,DWORD PTR [EBX+1036]
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+32],EAX
          mov DWORD PTR [ESP+16],0
          add EAX,16
          mov ECX,DWORD PTR [EBX+1040]
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_47a11c
          lea EDX,DWORD PTR [ECX-16]
          mov DWORD PTR [ESP+12],EDX
          call _XeCryptHmacSha
          mov DWORD PTR [ESP+32],ESI
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],16
          mov EAX,DWORD PTR [EBX+1036]
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_47a11c
          mov DWORD PTR [ESP+8],EAX
          call _XeCryptHmacSha
          mov EAX,DWORD PTR [EBX+1040]
          sub EAX,16
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [EBX+1036]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],16
          add EAX,16
          mov DWORD PTR [ESP+8],EAX
          call _XeCryptRc4
          add ESP,68
          pop EBX
          pop ESI
          ret 
L_41db45:
          mov DWORD PTR [ESP+4],OFFSET L_457110
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_41d9e6
          .byte 0x66
          .byte 0x90
L_41db60:
          mov EAX,DWORD PTR [EBX+1036]
          jmp L_41da18
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
FUN_41db70:
          push EDI
          push ESI
          push EBX
          sub ESP,64
          mov EBX,DWORD PTR [ESP+80]
          mov EAX,DWORD PTR [ESP+96]
          lea EDI,DWORD PTR [ESP+44]
          mov EDX,DWORD PTR [ESP+84]
          mov DWORD PTR [ESP+28],20
          mov DWORD PTR [ESP+24],EDI
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],0
          sub EDX,EAX
          add EAX,EBX
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+4],EDX
          mov DWORD PTR [ESP],EAX
          mov ESI,DWORD PTR [ESP+100]
          call _XeCryptSha
          add EBX,DWORD PTR [ESP+88]
          mov EAX,DWORD PTR [ESP+92]
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],EBX
          call _memcmp
          xor EDX,EDX
          test EAX,EAX
          jne L_41dc0f
          test ESI,ESI
          je L_41dc20
          mov EAX,DWORD PTR [ESP+44]
          mov EDX,1
          mov DWORD PTR [ESI],EAX
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESI+4],EAX
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESI+8],EAX
          mov EAX,DWORD PTR [ESP+56]
          mov DWORD PTR [ESI+12],EAX
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESI+16],EAX
L_41dc0f:
          add ESP,64
          mov EAX,EDX
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_41dc20:
          mov EDX,1
          jmp L_41dc0f
L_41dc27:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_41dc30:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,588
          mov EDI,DWORD PTR [ESP+612]
          mov EBX,DWORD PTR [ESP+608]
          lea ESI,DWORD PTR [ESP+88]
          mov EAX,DWORD PTR [ESP+616]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+44],EAX
          call _malloc
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],EBX
          mov EBP,EAX
          mov DWORD PTR [ESP],EAX
          call _memcpy
          lea EAX,DWORD PTR [EDI-336]
          lea ECX,DWORD PTR [EBX+336]
          mov DWORD PTR [ESP+28],20
          mov DWORD PTR [ESP+24],ESI
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],ECX
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+32],EAX
          mov DWORD PTR [ESP+36],ECX
          call _XeCryptSha
          lea EAX,DWORD PTR [EBX+12]
          mov DWORD PTR [ESP+8],20
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+40],EAX
          call _memcmp
          test EAX,EAX
          jne L_41def0
L_41dce0:
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+28],20
          mov DWORD PTR [ESP+24],ESI
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP],EAX
          call _XeCryptSha
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+8],20
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EAX
          call _memcmp
          test EAX,EAX
          jne L_41ded0
          mov EDX,DWORD PTR [ESP+44]
          lea EAX,DWORD PTR [EBX+320]
          mov DWORD PTR [ESP+8],8
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+40],EAX
          mov DWORD PTR [ESP+4],EDX
          call FUN_4223f0
          mov EAX,DWORD PTR [L_44a620]
          mov EDX,DWORD PTR [L_44a630]
          mov ECX,DWORD PTR [L_44a634]
          mov DWORD PTR [ESP+56],EAX
          mov EAX,DWORD PTR [L_44a624]
          mov DWORD PTR [ESP+72],EDX
          mov EDX,DWORD PTR [L_44a638]
          mov DWORD PTR [EBX+292],ECX
          mov DWORD PTR [ESP+76],ECX
          mov DWORD PTR [ESP+60],EAX
          mov EAX,DWORD PTR [L_44a628]
          mov ECX,DWORD PTR [L_44a638]
          mov DWORD PTR [ESP+80],EDX
          mov EDX,DWORD PTR [L_44a630]
          mov DWORD PTR [ESP+64],EAX
          mov EAX,DWORD PTR [L_44a62c]
          mov DWORD PTR [EBX+296],ECX
          mov DWORD PTR [EBX+288],EDX
          mov DWORD PTR [ESP+68],EAX
          mov EAX,DWORD PTR [L_44a63c]
          mov DWORD PTR [EBX+300],EAX
          mov DWORD PTR [ESP+84],EAX
          movzx EAX,BYTE PTR [L_479f15]
          mov BYTE PTR [EBX+335],AL
          mov DWORD PTR [ESP+8],EDI
          lea EDI,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EBP
          add EBX,304
          call _memcpy
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],ESI
          call _XeCryptAesKey
          lea EAX,DWORD PTR [ESP+72]
          lea EDX,DWORD PTR [EBP+320]
          mov DWORD PTR [ESP+20],1
          mov DWORD PTR [ESP+8],16
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+16],EAX
          mov DWORD PTR [ESP+44],EAX
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+4],EDX
          mov DWORD PTR [ESP+12],EAX
          call _XeCryptAesCbc
          mov EDX,DWORD PTR [EBX+16]
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+72],EDX
          mov EDX,DWORD PTR [EBX+20]
          mov DWORD PTR [ESP+76],EDX
          mov EDX,DWORD PTR [EBX+24]
          mov DWORD PTR [ESP+80],EDX
          mov EDX,DWORD PTR [EBX+28]
          mov DWORD PTR [ESP+16],EAX
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+20],1
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+84],EDX
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+8],EAX
          lea EAX,DWORD PTR [EBP+336]
          mov DWORD PTR [ESP+4],EAX
          call _XeCryptAesCbc
          mov DWORD PTR [ESP+4],OFFSET L_47a11c
          mov DWORD PTR [ESP],ESI
          call _XeCryptAesKey
          mov DWORD PTR [ESP+12],1
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],ESI
          call _XeCryptAesEcb
L_41deb0:
          mov DWORD PTR [ESP+608],EBP
          add ESP,588
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          jmp _free
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_41ded0:
          mov DWORD PTR [ESP+4],OFFSET L_457248
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_41deb0
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_41def0:
          mov DWORD PTR [ESP+4],OFFSET L_45720c
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EBP
          call FUN_402020
          test EAX,EAX
          jne L_41df71
          mov DWORD PTR [ESP+4],OFFSET L_4571e0
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EBP
          call _memcpy
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EBP
          call FUN_402020
          test EAX,EAX
          jne L_41df71
          mov DWORD PTR [ESP+4],OFFSET L_457200
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_41dce0
L_41df71:
          mov DWORD PTR [ESP+4],OFFSET L_4571d5
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EBX
          call _memcpy
          jmp L_41dce0
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_41dfa0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,604
          mov ESI,DWORD PTR [ESP+628]
          mov EDX,DWORD PTR [ESP+632]
          mov EBX,DWORD PTR [ESP+624]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+60],EDX
          call _malloc
          mov EDI,EAX
          mov EAX,DWORD PTR [L_44a600]
          mov EDX,DWORD PTR [ESP+60]
          lea EBP,DWORD PTR [EBX+304]
          mov DWORD PTR [EBX+288],EAX
          mov EAX,DWORD PTR [L_44a604]
          or BYTE PTR [EBX+289],1
          mov DWORD PTR [EBX+292],EAX
          mov EAX,DWORD PTR [L_44a608]
          mov DWORD PTR [EBX+296],EAX
          mov EAX,DWORD PTR [L_44a60c]
          mov DWORD PTR [EBX+300],EAX
          mov EAX,DWORD PTR [L_44a610]
          mov DWORD PTR [EBX+304],EAX
          mov EAX,DWORD PTR [L_44a614]
          mov DWORD PTR [EBX+308],EAX
          mov EAX,DWORD PTR [L_44a618]
          mov DWORD PTR [EBX+312],EAX
          mov EAX,DWORD PTR [L_44a61c]
          mov DWORD PTR [EBX+316],EAX
          mov DWORD PTR [ESP+4],EDX
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+8],8
          call FUN_4223f0
          movzx EAX,BYTE PTR [L_479f15]
          mov BYTE PTR [EBX+319],AL
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EDI
          call _memcpy
          lea EAX,DWORD PTR [ESP+72]
          lea EDX,DWORD PTR [ESP+88]
          mov DWORD PTR [ESP+36],16
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+32],EAX
          lea EAX,DWORD PTR [EDI+288]
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],32
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],16
          mov DWORD PTR [ESP],OFFSET L_47a11c
          mov DWORD PTR [ESP+60],EDX
          mov DWORD PTR [ESP+88],0
          mov DWORD PTR [ESP+92],0
          mov DWORD PTR [ESP+96],0
          mov DWORD PTR [ESP+100],0
          call _XeCryptHmacSha
          mov EAX,DWORD PTR [ESP+72]
          mov DWORD PTR [EBX+320],EAX
          mov EAX,DWORD PTR [ESP+76]
          mov DWORD PTR [EBX+324],EAX
          mov EAX,DWORD PTR [ESP+80]
          mov DWORD PTR [EBX+328],EAX
          mov EAX,DWORD PTR [ESP+84]
          mov DWORD PTR [EBX+332],EAX
          mov DWORD PTR [ESP+4],EBX
          lea EBX,DWORD PTR [ESP+104]
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP],EDI
          sub ESI,304
          call _memcpy
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],OFFSET L_47a11c
          call _XeCryptAesKey
          mov EDX,DWORD PTR [ESP+60]
          lea EAX,DWORD PTR [EDI+304]
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+20],1
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP+16],EDX
          call _XeCryptAesCbc
          mov DWORD PTR [ESP+624],EDI
          add ESP,604
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          jmp _free
L_41e177:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_41e180:
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
          call FUN_41dfa0
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
          call FUN_402210
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
          mov DWORD PTR [ESP+4],OFFSET L_4571d5
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
          call FUN_402210
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
          call FUN_402210
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
          call FUN_402210
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
          mov DWORD PTR [ESP+4],OFFSET L_4571d5
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
FUN_41e620:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,572
          mov EBX,DWORD PTR [ESP+592]
          cmp DWORD PTR [ESP+596],16384
          mov EAX,DWORD PTR [EBX+256]
          mov DWORD PTR [ESP+36],EAX
          mov EAX,DWORD PTR [EBX+260]
          mov DWORD PTR [ESP+40],EAX
          mov EAX,DWORD PTR [EBX+264]
          mov DWORD PTR [ESP+44],EAX
          mov EAX,DWORD PTR [EBX+268]
          mov DWORD PTR [ESP+48],EAX
          je L_41e685
          mov DWORD PTR [ESP+4],OFFSET L_457404
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,572
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_41e685:
          lea EAX,DWORD PTR [EBX+284]
          mov DWORD PTR [ESP],EAX
          call FUN_420ad0
          cmp EAX,16383
          ja L_41e783
          mov ESI,DWORD PTR [ESP+596]
          lea EDI,DWORD PTR [EBX+EAX*1]
          lea EBP,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+28],20
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+24],EBP
          mov DWORD PTR [ESP+16],0
          sub ESI,EAX
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EDI
          call _XeCryptSha
          lea EAX,DWORD PTR [EBX+300]
          mov DWORD PTR [ESP+8],20
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EAX
          call _memcmp
          test EAX,EAX
          je L_41e740
          mov DWORD PTR [ESP+4],16384
          mov DWORD PTR [ESP],EBX
          call FUN_402720
          cmp EAX,1
          je L_41e740
          mov DWORD PTR [ESP+4],OFFSET L_45745c
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,572
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
L_41e740:
          lea EBX,DWORD PTR [ESP+72]
          mov DWORD PTR [ESP+4],OFFSET L_47a11c
          mov DWORD PTR [ESP],EBX
          call _XeCryptAesKey
          lea EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+20],1
          mov DWORD PTR [ESP+16],EAX
          call _XeCryptAesCbc
          add ESP,572
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_41e783:
          mov DWORD PTR [ESP+4],OFFSET L_457430
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,572
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
FUN_41e7b0:
          sub ESP,44
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+28],20
          mov DWORD PTR [ESP+20],0
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+24],EAX
          add EAX,20
          mov DWORD PTR [ESP+4],492
          mov DWORD PTR [ESP],EAX
          call _XeCryptSha
          add ESP,44
          ret 
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90

.data
.p2align 5
L_44a5e0:
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
L_44a600:
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
L_44a620:
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
L_44a640:
          .byte 0x8e
          .byte 0x3
          .byte 0x75
          .byte 0xcc
L_44a644:
          .byte 0x36
          .byte 0xca
          .byte 0xb0
          .byte 0x87
L_44a648:
          .byte 0x8b
          .byte 0x83
          .byte 0xb7
          .byte 0xf6
L_44a64c:
          .byte 0x36
          .byte 0xca
          .byte 0xb0
          .byte 0x87
L_44a650:
          .byte 0x8b
          .byte 0x83
          .byte 0xb7
          .byte 0xf6
L_44a654:
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
L_44a664:
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
L_44a674:
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
L_44a684:
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
L_44a694:
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
L_44a6a4:
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
L_456664:
          .string "initializing random nonces\n"
L_456680:
          .string "initializing static pairing value\n"
          .zero 1
L_4566a4:
          .string "pairing set to: %02x %02x %02x\n"
L_4566c4:
          .string "valid"
L_4566ca:
          .string "error"
L_4566d0:
          .string " (weight:0x%x %s; ecd: %s)"
L_4566eb:
          .string "CPU Key set to: 0x"
L_4566fe:
          .string "%02X"
L_456703:
          .string "\n"
          .zero 3
L_456708:
          .string "\n***** WARNING: CPU key check failed, CPU key may not be valid!\n\n"
          .zero 2
L_45674c:
          .string "\n******* ERROR: invalid or unexpected characters in CPU key!\n"
          .zero 2
L_45678c:
          .string "\n***** ERROR: unable to set CPU key to '%s', %d is not the correct length, 32 chars required!\n"
L_4567eb:
          .string "CPU Key set to  : "
L_4567fe:
          .string "Fuse CF LDV set to : 0x"
L_456816:
          .string "Fuse CPU Key set to: 0x"
          .zero 2
L_456830:
          .string "\nERROR: YOU SHOULD NOT BE SEEING THIS ERROR!\n"
L_45685e:
          .string "1BL Key set to  : 0x"
L_456873:
          .string " sum: 0x%x (expects: 0x983)\n"
L_456890:
          .string "xex Key set to  : 0x"
L_4568a5:
          .string " sum: 0x%x (expects: 0x800)\n"
L_4568c2:
          .string "\n******* ERROR: 1BL key 0x"
          .zero 3
L_4568e0:
          .string " does not appear to be correct!\n"
          .zero 3
L_456904:
          .string "\n******* ERROR: invalid or unexpected characters in 1BL key!\n"
          .zero 2
L_456944:
          .string "\n***** ERROR: unable to set 1BL key to '%s', %d is not the correct length, 32 chars required!\n"
L_4569a3:
          .string "\n******* ERROR: 1BL key 0x%s "
          .zero 3
L_4569c4:
          .string "does not appear to be correct!\n"
L_4569e4:
          .string "SMC binary appears to be encrypted, attempting to decrypt..."
L_456a21:
          .string "success!"
L_456a2a:
          .string "failed!"
          .zero 2
L_456a34:
          .string "\n******* ERROR: please make sure your provided a valid/decryptable SMC binary!\n\n"
          .zero 3
L_456a88:
          .string "\n******* ERROR: hacked or unknown SMC binary found? you should use a clean SMC binary for a retail image!\n\n"
L_456af4:
          .string "known/clean SMC binary found! type 0x%x\n"
          .zero 3
L_456b20:
          .string "\n******* WARNING: hacked or unknown SMC binary found? Just a warning, there are a lot of different SMC binaries for devkits!\n\n"
          .zero 1
L_456ba0:
          .string "known/clean SMC binary found!\n"
          .zero 1
L_456bc0:
          .string "glitch hack found in SMC binary!\n"
          .zero 2
L_456be4:
          .string "\n******* WARNING: hacked or unknown SMC binary found!\n"
          .zero 1
L_456c1c:
          .string "jtag hack found in SMC binary!\n"
L_456c3c:
          .string "\n******* ERROR: clean SMC binary found? you should use a hacked SMC binary for glitch images.\n\n"
L_456c9c:
          .string "\n******* ERROR: clean SMC binary found? you should use a hacked SMC binary for JTAG images.\n\n"
          .zero 2
L_456cfc:
          .string "CBENC pairing set to: %02x %02x %02x\n"
L_456d22:
          .string "\t**dual CB flag detected!**\n"
          .zero 1
L_456d40:
          .string "\t**15572+ CBB crypto method detected!**\n"
          .zero 3
L_456d6c:
          .string "\t** CBB crypto method set to work with mfg CBA!**\n"
L_456d9f:
          .string "kv"
L_456da2:
          .string "kv.bin"
L_456da9:
          .string "alt kv"
L_456db0:
          .string "kv_alt.bin"
          .zero 1
L_456dbc:
          .string "\n******* ERROR: %s is not the correct size! Skipping verification and encryption!\n"
          .zero 1
L_456e10:
          .string "%s appears to be decrypted already, but the hash does not match the CPU key..."
          .zero 1
L_456e60:
          .string "\n******* WARNING: could not verify pre-decrypted keyvault, please be sure your provided a valid %s!\n"
          .zero 3
L_456ec8:
          .string "%s appears to be encrypted, attempting to decrypt..."
          .zero 3
L_456f00:
          .string "Failed!\n%s could not be decrypted!\n"
L_456f24:
          .string "\n******* ERROR: could not decrypt %s, please be sure your provided a valid %s!\n"
L_456f74:
          .string "Success!\n"
          .zero 2
L_456f80:
          .string "\n******* ERROR: please be sure your provided a DEcrypted %s!\n"
          .zero 2
L_456fc0:
          .string "******* WARNING: extended.bin was not provided or was invalid! Making up an clean/empty extended.bin!\n"
          .zero 1
L_457028:
          .string "******* WARNING: extended.bin is not the correct size! Making up an clean/empty extended.bin!\n"
          .zero 1
L_457088:
          .string "extended.bin appears to be encrypted, attempting to decrypt..."
          .zero 1
L_4570c8:
          .string "Failed!\nextended.bin could not be decrypted, filling clean/empty data.\n"
L_457110:
          .string "******* WARNING: secdata.bin was not provided or was invalid! Making up an clean/empty secdata.bin!\n"
          .zero 3
L_457178:
          .string "******* WARNING: secdata.bin is not the correct size! Making up an clean/empty secdata.bin!\n"
L_4571d5:
          .string "success!\n"
          .zero 1
L_4571e0:
          .string "failed! Trying alternate key..."
L_457200:
          .string "failed!\n"
          .zero 3
L_45720c:
          .string "crl appears crypted, attempting to decrypt with CPU key..."
          .zero 1
L_457248:
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
L_457404:
          .string "****** ERROR: FCRT encrypt invalid size!\n"
          .zero 2
L_457430:
          .string "**** ERROR: FCRT encrypt invalid offset!\n"
          .zero 2
L_45745c:
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
          .long FUN_41aa00 - .
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
          .long FUN_41abb0 - .
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
          .long FUN_41ac00 - .
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
          .long FUN_41ac50 - .
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
          .long FUN_41ac70 - .
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
          .long FUN_41aca0 - .
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
          .long FUN_41acd0 - .
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
          .long FUN_41ad00 - .
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
          .long FUN_41ad30 - .
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
          .long FUN_41ad60 - .
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
          .long FUN_41ad90 - .
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
          .long FUN_41adb0 - .
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
          .long FUN_41add0 - .
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
          .long FUN_41ade0 - .
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
          .long FUN_41ae40 - .
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
          .long FUN_41afe0 - .
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
          .long FUN_41b120 - .
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
          .long FUN_41b1d0 - .
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
          .long FUN_41b320 - .
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
          .long FUN_41b420 - .
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
          .long L_41b520 - .
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
          .long FUN_41b600 - .
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
          .long FUN_41b740 - .
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
          .long L_41b8e0 - .
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
          .long L_41ba00 - .
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
          .long FUN_41ba80 - .
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
          .long FUN_41bf50 - .
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
          .long FUN_41c0c0 - .
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
          .long FUN_41c1b0 - .
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
          .long FUN_41c370 - .
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
          .long FUN_41c5e0 - .
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
          .long FUN_41c6b0 - .
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
          .long FUN_41c760 - .
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
          .long FUN_41c860 - .
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
          .long L_41c910 - .
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
          .long FUN_41ca20 - .
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
          .long FUN_41ce50 - .
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
          .long L_41cf00 - .
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
          .long L_41cff0 - .
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
          .long FUN_41d0e0 - .
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
          .long FUN_41d6a0 - .
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
          .long FUN_41d9b0 - .
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
          .long FUN_41db70 - .
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
          .long FUN_41dc30 - .
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
          .long FUN_41dfa0 - .
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
          .long FUN_41e180 - .
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
          .long FUN_41e620 - .
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
          .long FUN_41e7b0 - .
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
L_479560:
          .zero 16
L_479570:
          .zero 1
L_479571:
          .zero 1
L_479572:
          .zero 2

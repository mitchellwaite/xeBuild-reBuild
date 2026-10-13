# crypto/aeskey.s -- Gladman AES: key schedules for 128/192/256
#
# original placement:
#   .eh_frame      0046c724-0046c948
#   .rdata         00461c20-00461c60
#   .rdata$zzz     00463ca0-00463ccc
#   .text          0043bae0-0043e550

.intel_syntax noprefix
.globl FUN_43c6f0
.globl FUN_43e4e0

.text
.p2align 4
L_43bae0:
          push EBP
          push EDI
          push ESI
          push EBX
          mov ECX,DWORD PTR [ESP+20]
          mov EDX,DWORD PTR [ESP+24]
          mov EAX,DWORD PTR [ECX]
          mov DWORD PTR [EDX],EAX
          mov ESI,DWORD PTR [ECX+4]
          xor EAX,DWORD PTR [L_461c20]
          mov DWORD PTR [EDX+4],ESI
          mov EBX,DWORD PTR [ECX+8]
          mov DWORD PTR [EDX+8],EBX
          mov ECX,DWORD PTR [ECX+12]
          mov EDI,ECX
          mov DWORD PTR [EDX+12],ECX
          shr EDI,24
          xor EAX,DWORD PTR [EDI*4+L_460420]
          movzx EDI,CL
          xor EAX,DWORD PTR [EDI*4+L_460820]
          movzx EDI,CH
          xor EAX,DWORD PTR [EDI*4+L_45fc20]
          mov EDI,ECX
          shr EDI,16
          mov EBP,EAX
          mov EAX,EDI
          movzx EDI,AL
          mov EAX,DWORD PTR [EDI*4+L_460020]
          xor EAX,EBP
          xor ESI,EAX
          mov DWORD PTR [EDX+16],EAX
          xor EAX,DWORD PTR [L_461c24]
          xor EBX,ESI
          mov DWORD PTR [EDX+20],ESI
          xor ECX,EBX
          mov DWORD PTR [EDX+24],EBX
          mov EDI,ECX
          mov DWORD PTR [EDX+28],ECX
          shr EDI,24
          xor EAX,DWORD PTR [EDI*4+L_460420]
          movzx EDI,CL
          xor EAX,DWORD PTR [EDI*4+L_460820]
          movzx EDI,CH
          xor EAX,DWORD PTR [EDI*4+L_45fc20]
          mov EDI,ECX
          shr EDI,16
          mov EBP,EAX
          mov EAX,EDI
          movzx EDI,AL
          mov EAX,DWORD PTR [EDI*4+L_460020]
          xor EAX,EBP
          xor ESI,EAX
          mov DWORD PTR [EDX+32],EAX
          xor EBX,ESI
          mov DWORD PTR [EDX+36],ESI
          xor ECX,EBX
          mov DWORD PTR [EDX+40],EBX
          mov EDI,ECX
          mov DWORD PTR [EDX+44],ECX
          xor EAX,DWORD PTR [L_461c28]
          shr EDI,24
          xor EAX,DWORD PTR [EDI*4+L_460420]
          movzx EDI,CL
          xor EAX,DWORD PTR [EDI*4+L_460820]
          movzx EDI,CH
          xor EAX,DWORD PTR [EDI*4+L_45fc20]
          mov EDI,ECX
          shr EDI,16
          mov EBP,EAX
          mov EAX,EDI
          movzx EDI,AL
          mov EAX,DWORD PTR [EDI*4+L_460020]
          xor EAX,EBP
          xor ESI,EAX
          mov DWORD PTR [EDX+48],EAX
          xor EAX,DWORD PTR [L_461c2c]
          xor EBX,ESI
          mov DWORD PTR [EDX+52],ESI
          xor ECX,EBX
          mov DWORD PTR [EDX+56],EBX
          mov EDI,ECX
          mov DWORD PTR [EDX+60],ECX
          shr EDI,24
          xor EAX,DWORD PTR [EDI*4+L_460420]
          movzx EDI,CL
          xor EAX,DWORD PTR [EDI*4+L_460820]
          movzx EDI,CH
          xor EAX,DWORD PTR [EDI*4+L_45fc20]
          mov EDI,ECX
          shr EDI,16
          mov EBP,EAX
          mov EAX,EDI
          movzx EDI,AL
          mov EAX,DWORD PTR [EDI*4+L_460020]
          xor EAX,EBP
          xor ESI,EAX
          mov DWORD PTR [EDX+64],EAX
          xor EAX,DWORD PTR [L_461c30]
          xor EBX,ESI
          mov DWORD PTR [EDX+68],ESI
          xor ECX,EBX
          mov DWORD PTR [EDX+72],EBX
          mov EDI,ECX
          mov DWORD PTR [EDX+76],ECX
          shr EDI,24
          xor EAX,DWORD PTR [EDI*4+L_460420]
          movzx EDI,CL
          xor EAX,DWORD PTR [EDI*4+L_460820]
          movzx EDI,CH
          xor EAX,DWORD PTR [EDI*4+L_45fc20]
          mov EDI,ECX
          shr EDI,16
          mov EBP,EAX
          mov EAX,EDI
          movzx EDI,AL
          mov EAX,DWORD PTR [EDI*4+L_460020]
          xor EAX,EBP
          xor ESI,EAX
          mov DWORD PTR [EDX+80],EAX
          xor EAX,DWORD PTR [L_461c34]
          xor EBX,ESI
          mov DWORD PTR [EDX+84],ESI
          xor ECX,EBX
          mov DWORD PTR [EDX+88],EBX
          mov EDI,ECX
          mov DWORD PTR [EDX+92],ECX
          shr EDI,24
          xor EAX,DWORD PTR [EDI*4+L_460420]
          movzx EDI,CL
          xor EAX,DWORD PTR [EDI*4+L_460820]
          movzx EDI,CH
          xor EAX,DWORD PTR [EDI*4+L_45fc20]
          mov EDI,ECX
          shr EDI,16
          mov EBP,EAX
          mov EAX,EDI
          movzx EDI,AL
          mov EAX,DWORD PTR [EDI*4+L_460020]
          xor EAX,EBP
          xor ESI,EAX
          mov DWORD PTR [EDX+96],EAX
          xor EAX,DWORD PTR [L_461c38]
          xor EBX,ESI
          mov DWORD PTR [EDX+100],ESI
          xor ECX,EBX
          mov DWORD PTR [EDX+104],EBX
          mov EDI,ECX
          mov DWORD PTR [EDX+108],ECX
          shr EDI,24
          xor EAX,DWORD PTR [EDI*4+L_460420]
          movzx EDI,CL
          xor EAX,DWORD PTR [EDI*4+L_460820]
          movzx EDI,CH
          xor EAX,DWORD PTR [EDI*4+L_45fc20]
          mov EDI,ECX
          shr EDI,16
          mov EBP,EAX
          mov EAX,EDI
          movzx EDI,AL
          mov EAX,DWORD PTR [EDI*4+L_460020]
          xor EAX,EBP
          xor ESI,EAX
          mov DWORD PTR [EDX+112],EAX
          xor EAX,DWORD PTR [L_461c3c]
          xor EBX,ESI
          mov DWORD PTR [EDX+116],ESI
          xor ECX,EBX
          mov DWORD PTR [EDX+120],EBX
          mov EDI,ECX
          mov DWORD PTR [EDX+124],ECX
          shr EDI,24
          xor EAX,DWORD PTR [EDI*4+L_460420]
          movzx EDI,CL
          xor EAX,DWORD PTR [EDI*4+L_460820]
          movzx EDI,CH
          xor EAX,DWORD PTR [EDI*4+L_45fc20]
          mov EDI,ECX
          shr EDI,16
          mov EBP,EAX
          mov EAX,EDI
          movzx EDI,AL
          mov EAX,DWORD PTR [EDI*4+L_460020]
          xor EAX,EBP
          xor ESI,EAX
          mov DWORD PTR [EDX+128],EAX
          xor EAX,DWORD PTR [L_461c40]
          xor EBX,ESI
          mov DWORD PTR [EDX+132],ESI
          xor ECX,EBX
          mov DWORD PTR [EDX+136],EBX
          mov EDI,ECX
          mov DWORD PTR [EDX+140],ECX
          shr EDI,24
          xor EAX,DWORD PTR [EDI*4+L_460420]
          movzx EDI,CL
          xor EAX,DWORD PTR [EDI*4+L_460820]
          movzx EDI,CH
          xor EAX,DWORD PTR [EDI*4+L_45fc20]
          mov EDI,ECX
          shr EDI,16
          mov EBP,EAX
          mov EAX,EDI
          movzx EDI,AL
          mov EAX,DWORD PTR [EDI*4+L_460020]
          xor EAX,EBP
          xor ESI,EAX
          mov DWORD PTR [EDX+144],EAX
          xor EAX,DWORD PTR [L_461c44]
          xor EBX,ESI
          mov DWORD PTR [EDX+148],ESI
          xor ECX,EBX
          mov DWORD PTR [EDX+152],EBX
          mov EDI,ECX
          mov DWORD PTR [EDX+156],ECX
          shr EDI,24
          xor EAX,DWORD PTR [EDI*4+L_460420]
          movzx EDI,CL
          xor EAX,DWORD PTR [EDI*4+L_460820]
          movzx EDI,CH
          mov DWORD PTR [EDX+240],0
          xor EAX,DWORD PTR [EDI*4+L_45fc20]
          mov EDI,ECX
          mov BYTE PTR [EDX+240],160
          shr EDI,16
          mov EBP,EAX
          mov EAX,EDI
          movzx EDI,AL
          mov EAX,DWORD PTR [EDI*4+L_460020]
          xor EAX,EBP
          mov DWORD PTR [EDX+160],EAX
          xor EAX,ESI
          xor EBX,EAX
          mov DWORD PTR [EDX+164],EAX
          xor EAX,EAX
          xor ECX,EBX
          mov DWORD PTR [EDX+168],EBX
          mov DWORD PTR [EDX+172],ECX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_43be40:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,8
          mov ECX,DWORD PTR [ESP+28]
          mov EDX,DWORD PTR [ESP+32]
          mov EAX,DWORD PTR [ECX]
          mov DWORD PTR [EDX],EAX
          mov ESI,DWORD PTR [ECX+4]
          xor EAX,DWORD PTR [L_461c20]
          mov DWORD PTR [EDX+4],ESI
          mov EBX,DWORD PTR [ECX+8]
          mov DWORD PTR [EDX+8],EBX
          mov EDI,DWORD PTR [ECX+12]
          mov DWORD PTR [EDX+12],EDI
          mov EBP,DWORD PTR [ECX+16]
          mov DWORD PTR [EDX+16],EBP
          mov ECX,DWORD PTR [ECX+20]
          mov DWORD PTR [ESP],EBP
          mov EBP,ECX
          mov DWORD PTR [EDX+20],ECX
          shr EBP,24
          xor EAX,DWORD PTR [EBP*4+L_460420]
          movzx EBP,CL
          xor EAX,DWORD PTR [EBP*4+L_460820]
          movzx EBP,CH
          xor EAX,DWORD PTR [EBP*4+L_45fc20]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,ECX
          shr EAX,16
          movzx EBP,AL
          mov EAX,DWORD PTR [ESP+4]
          xor EAX,DWORD PTR [EBP*4+L_460020]
          mov EBP,DWORD PTR [ESP]
          xor ESI,EAX
          mov DWORD PTR [EDX+24],EAX
          xor EBX,ESI
          mov DWORD PTR [EDX+28],ESI
          xor EDI,EBX
          mov DWORD PTR [EDX+32],EBX
          xor EBP,EDI
          mov DWORD PTR [EDX+36],EDI
          xor ECX,EBP
          mov DWORD PTR [EDX+40],EBP
          mov DWORD PTR [ESP],EBP
          mov EBP,ECX
          xor EAX,DWORD PTR [L_461c24]
          mov DWORD PTR [EDX+44],ECX
          shr EBP,24
          xor EAX,DWORD PTR [EBP*4+L_460420]
          movzx EBP,CL
          xor EAX,DWORD PTR [EBP*4+L_460820]
          movzx EBP,CH
          xor EAX,DWORD PTR [EBP*4+L_45fc20]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,ECX
          shr EAX,16
          movzx EBP,AL
          mov EAX,DWORD PTR [ESP+4]
          xor EAX,DWORD PTR [EBP*4+L_460020]
          mov EBP,DWORD PTR [ESP]
          xor ESI,EAX
          mov DWORD PTR [EDX+48],EAX
          xor EAX,DWORD PTR [L_461c28]
          xor EBX,ESI
          mov DWORD PTR [EDX+52],ESI
          xor EDI,EBX
          mov DWORD PTR [EDX+56],EBX
          xor EBP,EDI
          mov DWORD PTR [EDX+60],EDI
          xor ECX,EBP
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [EDX+64],EBP
          mov EBP,ECX
          mov DWORD PTR [EDX+68],ECX
          shr EBP,24
          xor EAX,DWORD PTR [EBP*4+L_460420]
          movzx EBP,CL
          xor EAX,DWORD PTR [EBP*4+L_460820]
          movzx EBP,CH
          xor EAX,DWORD PTR [EBP*4+L_45fc20]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,ECX
          shr EAX,16
          movzx EBP,AL
          mov EAX,DWORD PTR [ESP+4]
          xor EAX,DWORD PTR [EBP*4+L_460020]
          mov EBP,DWORD PTR [ESP]
          xor ESI,EAX
          mov DWORD PTR [EDX+72],EAX
          xor EBX,ESI
          mov DWORD PTR [EDX+76],ESI
          xor EDI,EBX
          mov DWORD PTR [EDX+80],EBX
          xor EBP,EDI
          mov DWORD PTR [EDX+84],EDI
          xor ECX,EBP
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [EDX+88],EBP
          mov EBP,ECX
          mov DWORD PTR [EDX+92],ECX
          xor EAX,DWORD PTR [L_461c2c]
          shr EBP,24
          xor EAX,DWORD PTR [EBP*4+L_460420]
          movzx EBP,CL
          xor EAX,DWORD PTR [EBP*4+L_460820]
          movzx EBP,CH
          xor EAX,DWORD PTR [EBP*4+L_45fc20]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,ECX
          shr EAX,16
          movzx EBP,AL
          mov EAX,DWORD PTR [ESP+4]
          xor EAX,DWORD PTR [EBP*4+L_460020]
          mov EBP,DWORD PTR [ESP]
          xor ESI,EAX
          mov DWORD PTR [EDX+96],EAX
          xor EAX,DWORD PTR [L_461c30]
          xor EBX,ESI
          mov DWORD PTR [EDX+100],ESI
          xor EDI,EBX
          mov DWORD PTR [EDX+104],EBX
          xor EBP,EDI
          mov DWORD PTR [EDX+108],EDI
          xor ECX,EBP
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [EDX+112],EBP
          mov EBP,ECX
          mov DWORD PTR [EDX+116],ECX
          shr EBP,24
          xor EAX,DWORD PTR [EBP*4+L_460420]
          movzx EBP,CL
          xor EAX,DWORD PTR [EBP*4+L_460820]
          movzx EBP,CH
          xor EAX,DWORD PTR [EBP*4+L_45fc20]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,ECX
          shr EAX,16
          movzx EBP,AL
          mov EAX,DWORD PTR [ESP+4]
          xor EAX,DWORD PTR [EBP*4+L_460020]
          mov EBP,DWORD PTR [ESP]
          xor ESI,EAX
          mov DWORD PTR [EDX+120],EAX
          xor EAX,DWORD PTR [L_461c34]
          xor EBX,ESI
          mov DWORD PTR [EDX+124],ESI
          xor EDI,EBX
          mov DWORD PTR [EDX+128],EBX
          xor EBP,EDI
          mov DWORD PTR [EDX+132],EDI
          xor ECX,EBP
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [EDX+136],EBP
          mov EBP,ECX
          mov DWORD PTR [EDX+140],ECX
          shr EBP,24
          xor EAX,DWORD PTR [EBP*4+L_460420]
          movzx EBP,CL
          xor EAX,DWORD PTR [EBP*4+L_460820]
          movzx EBP,CH
          xor EAX,DWORD PTR [EBP*4+L_45fc20]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,ECX
          shr EAX,16
          movzx EBP,AL
          mov EAX,DWORD PTR [ESP+4]
          xor EAX,DWORD PTR [EBP*4+L_460020]
          mov EBP,DWORD PTR [ESP]
          xor ESI,EAX
          mov DWORD PTR [EDX+144],EAX
          xor EAX,DWORD PTR [L_461c38]
          xor EBX,ESI
          mov DWORD PTR [EDX+148],ESI
          xor EDI,EBX
          mov DWORD PTR [EDX+152],EBX
          xor EBP,EDI
          mov DWORD PTR [EDX+156],EDI
          xor ECX,EBP
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [EDX+160],EBP
          mov EBP,ECX
          mov DWORD PTR [EDX+164],ECX
          shr EBP,24
          xor EAX,DWORD PTR [EBP*4+L_460420]
          movzx EBP,CL
          xor EAX,DWORD PTR [EBP*4+L_460820]
          movzx EBP,CH
          xor EAX,DWORD PTR [EBP*4+L_45fc20]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,ECX
          shr EAX,16
          movzx EBP,AL
          mov EAX,DWORD PTR [ESP+4]
          xor EAX,DWORD PTR [EBP*4+L_460020]
          mov EBP,DWORD PTR [ESP]
          xor ESI,EAX
          mov DWORD PTR [EDX+168],EAX
          xor EAX,DWORD PTR [L_461c3c]
          xor EBX,ESI
          mov DWORD PTR [EDX+172],ESI
          xor EDI,EBX
          mov DWORD PTR [EDX+176],EBX
          xor EBP,EDI
          mov DWORD PTR [EDX+180],EDI
          xor ECX,EBP
          mov DWORD PTR [EDX+184],EBP
          mov EBP,ECX
          mov DWORD PTR [EDX+188],ECX
          shr EBP,24
          xor EAX,DWORD PTR [EBP*4+L_460420]
          movzx EBP,CL
          xor EAX,DWORD PTR [EBP*4+L_460820]
          movzx EBP,CH
          shr ECX,16
          xor EAX,DWORD PTR [EBP*4+L_45fc20]
          movzx ECX,CL
          xor EAX,DWORD PTR [ECX*4+L_460020]
          xor ESI,EAX
          mov DWORD PTR [EDX+192],EAX
          mov DWORD PTR [EDX+240],0
          xor EBX,ESI
          mov DWORD PTR [EDX+196],ESI
          mov BYTE PTR [EDX+240],192
          xor EDI,EBX
          mov DWORD PTR [EDX+200],EBX
          xor EAX,EAX
          mov DWORD PTR [EDX+204],EDI
          add ESP,8
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_43c1b0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,20
          mov EBX,DWORD PTR [ESP+40]
          mov EDX,DWORD PTR [ESP+44]
          mov EAX,DWORD PTR [EBX]
          mov DWORD PTR [EDX],EAX
          mov ESI,DWORD PTR [EBX+4]
          xor EAX,DWORD PTR [L_461c20]
          mov DWORD PTR [EDX+4],ESI
          mov EDI,DWORD PTR [EBX+8]
          mov DWORD PTR [EDX+8],EDI
          mov ECX,DWORD PTR [EBX+12]
          mov DWORD PTR [EDX+12],ECX
          mov EBP,DWORD PTR [EBX+16]
          mov DWORD PTR [EDX+16],EBP
          mov DWORD PTR [ESP],EBP
          mov EBP,DWORD PTR [EBX+20]
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [EDX+20],EBP
          mov EBP,DWORD PTR [EBX+24]
          mov DWORD PTR [EDX+24],EBP
          mov EBX,DWORD PTR [EBX+28]
          mov DWORD PTR [ESP+8],EBP
          mov EBP,EBX
          mov DWORD PTR [EDX+28],EBX
          shr EBP,24
          xor EAX,DWORD PTR [EBP*4+L_460420]
          movzx EBP,BL
          xor EAX,DWORD PTR [EBP*4+L_460820]
          movzx EBP,BH
          xor EAX,DWORD PTR [EBP*4+L_45fc20]
          mov DWORD PTR [ESP+12],EAX
          mov EAX,EBX
          shr EAX,16
          movzx EBP,AL
          mov EAX,DWORD PTR [ESP+12]
          xor EAX,DWORD PTR [EBP*4+L_460020]
          mov EBP,EAX
          mov DWORD PTR [EDX+32],EAX
          mov EAX,ESI
          xor EAX,EBP
          mov DWORD PTR [ESP+12],EBP
          xor EDI,EAX
          mov EBP,EAX
          mov DWORD PTR [EDX+36],EAX
          xor ECX,EDI
          mov DWORD PTR [ESP+16],EDI
          mov DWORD PTR [EDX+40],EDI
          mov ESI,ECX
          movzx EDI,CL
          mov DWORD PTR [EDX+44],ECX
          shr ESI,24
          mov EDI,DWORD PTR [EDI*4+L_45fc20]
          xor EDI,DWORD PTR [ESI*4+L_460820]
          movzx ESI,CH
          xor EDI,DWORD PTR [ESP]
          xor EDI,DWORD PTR [ESI*4+L_460020]
          mov ESI,ECX
          shr ESI,16
          mov EAX,ESI
          movzx ESI,AL
          mov EAX,DWORD PTR [ESP+4]
          xor EDI,DWORD PTR [ESI*4+L_460420]
          mov ESI,DWORD PTR [ESP+8]
          xor EAX,EDI
          mov DWORD PTR [EDX+48],EDI
          xor ESI,EAX
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [EDX+52],EAX
          xor EBX,ESI
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [EDX+56],ESI
          mov ESI,EBX
          mov EAX,DWORD PTR [ESP+12]
          xor EAX,DWORD PTR [L_461c24]
          shr ESI,24
          mov DWORD PTR [EDX+60],EBX
          xor EAX,DWORD PTR [ESI*4+L_460420]
          movzx ESI,BL
          xor EAX,DWORD PTR [ESI*4+L_460820]
          movzx ESI,BH
          xor EAX,DWORD PTR [ESI*4+L_45fc20]
          mov ESI,EBX
          shr ESI,16
          mov DWORD PTR [ESP+8],EAX
          mov EAX,ESI
          movzx ESI,AL
          mov EAX,DWORD PTR [ESP+8]
          xor EAX,DWORD PTR [ESI*4+L_460020]
          xor EBP,EAX
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [EDX+64],EAX
          mov EAX,DWORD PTR [ESP+16]
          mov DWORD PTR [EDX+68],EBP
          mov DWORD PTR [ESP+12],EBP
          xor EAX,EBP
          xor ECX,EAX
          mov DWORD PTR [ESP+16],EAX
          mov DWORD PTR [EDX+72],EAX
          mov EAX,ECX
          movzx EBP,CL
          movzx ESI,CH
          shr EAX,24
          mov EBP,DWORD PTR [EBP*4+L_45fc20]
          mov DWORD PTR [EDX+76],ECX
          xor EBP,DWORD PTR [EAX*4+L_460820]
          xor EBP,EDI
          mov EDI,ECX
          xor EBP,DWORD PTR [ESI*4+L_460020]
          shr EDI,16
          mov EAX,EDI
          movzx ESI,AL
          mov EAX,DWORD PTR [ESP]
          xor EBP,DWORD PTR [ESI*4+L_460420]
          mov ESI,DWORD PTR [ESP+4]
          xor EAX,EBP
          mov DWORD PTR [EDX+80],EBP
          xor ESI,EAX
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [EDX+84],EAX
          xor EBX,ESI
          mov EAX,DWORD PTR [ESP+8]
          xor EAX,DWORD PTR [L_461c28]
          mov EDI,EBX
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [EDX+88],ESI
          shr EDI,24
          movzx ESI,BL
          mov DWORD PTR [EDX+92],EBX
          xor EAX,DWORD PTR [EDI*4+L_460420]
          mov EDI,EBX
          xor EAX,DWORD PTR [ESI*4+L_460820]
          movzx ESI,BH
          shr EDI,16
          xor EAX,DWORD PTR [ESI*4+L_45fc20]
          mov DWORD PTR [ESP+8],EAX
          mov EAX,EDI
          mov EDI,DWORD PTR [ESP+12]
          movzx ESI,AL
          mov EAX,DWORD PTR [ESP+8]
          xor EAX,DWORD PTR [ESI*4+L_460020]
          mov ESI,DWORD PTR [ESP+16]
          xor EDI,EAX
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [EDX+96],EAX
          xor ESI,EDI
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [EDX+100],EDI
          xor ECX,ESI
          mov DWORD PTR [ESP+16],ESI
          mov DWORD PTR [EDX+104],ESI
          mov EDI,ECX
          movzx ESI,CL
          mov DWORD PTR [EDX+108],ECX
          shr EDI,24
          mov ESI,DWORD PTR [ESI*4+L_45fc20]
          xor ESI,DWORD PTR [EDI*4+L_460820]
          movzx EDI,CH
          xor ESI,EBP
          mov EBP,ECX
          xor ESI,DWORD PTR [EDI*4+L_460020]
          shr EBP,16
          mov EAX,EBP
          movzx EDI,AL
          mov EAX,DWORD PTR [ESP]
          xor ESI,DWORD PTR [EDI*4+L_460420]
          mov EDI,DWORD PTR [ESP+4]
          xor EAX,ESI
          mov DWORD PTR [EDX+112],ESI
          xor EDI,EAX
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [EDX+116],EAX
          xor EBX,EDI
          mov EAX,DWORD PTR [ESP+8]
          xor EAX,DWORD PTR [L_461c2c]
          mov EBP,EBX
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [EDX+120],EDI
          shr EBP,24
          movzx EDI,BL
          mov DWORD PTR [ESP+8],EBX
          xor EAX,DWORD PTR [EBP*4+L_460420]
          mov EBP,EBX
          mov DWORD PTR [EDX+124],EBX
          shr EBP,16
          xor EAX,DWORD PTR [EDI*4+L_460820]
          movzx EDI,BH
          mov EBX,EBP
          xor EAX,DWORD PTR [EDI*4+L_45fc20]
          mov EBP,DWORD PTR [ESP+12]
          movzx EDI,BL
          mov EBX,DWORD PTR [ESP+16]
          xor EAX,DWORD PTR [EDI*4+L_460020]
          xor EBP,EAX
          mov DWORD PTR [EDX+128],EAX
          xor EBX,EBP
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [EDX+132],EBP
          xor ECX,EBX
          mov EBP,EBX
          mov DWORD PTR [EDX+136],EBX
          mov EBX,ECX
          movzx EDI,CL
          mov DWORD PTR [EDX+140],ECX
          shr EBX,24
          mov EDI,DWORD PTR [EDI*4+L_45fc20]
          xor EDI,DWORD PTR [EBX*4+L_460820]
          xor EDI,ESI
          movzx ESI,CH
          xor EDI,DWORD PTR [ESI*4+L_460020]
          mov ESI,ECX
          shr ESI,16
          mov EBX,ESI
          movzx ESI,BL
          mov EBX,DWORD PTR [ESP]
          xor EDI,DWORD PTR [ESI*4+L_460420]
          xor EBX,EDI
          mov DWORD PTR [EDX+144],EDI
          mov DWORD PTR [EDX+148],EBX
          mov ESI,DWORD PTR [ESP+4]
          mov DWORD PTR [ESP],EBX
          xor EAX,DWORD PTR [L_461c30]
          xor ESI,EBX
          mov EBX,DWORD PTR [ESP+8]
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [EDX+152],ESI
          xor EBX,ESI
          mov ESI,EBX
          mov DWORD PTR [EDX+156],EBX
          shr ESI,24
          xor EAX,DWORD PTR [ESI*4+L_460420]
          movzx ESI,BL
          xor EAX,DWORD PTR [ESI*4+L_460820]
          movzx ESI,BH
          xor EAX,DWORD PTR [ESI*4+L_45fc20]
          mov DWORD PTR [ESP+8],EAX
          mov EAX,EBX
          shr EAX,16
          movzx ESI,AL
          mov EAX,DWORD PTR [ESP+8]
          xor EAX,DWORD PTR [ESI*4+L_460020]
          mov ESI,EAX
          mov DWORD PTR [EDX+160],EAX
          mov EAX,DWORD PTR [ESP+12]
          mov DWORD PTR [ESP+8],ESI
          xor EAX,ESI
          xor EBP,EAX
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [EDX+164],EAX
          xor ECX,EBP
          mov DWORD PTR [ESP+16],EBP
          mov DWORD PTR [EDX+168],EBP
          mov EBP,ECX
          movzx ESI,CL
          mov DWORD PTR [EDX+172],ECX
          shr EBP,24
          mov ESI,DWORD PTR [ESI*4+L_45fc20]
          xor ESI,DWORD PTR [EBP*4+L_460820]
          xor ESI,EDI
          movzx EDI,CH
          xor ESI,DWORD PTR [EDI*4+L_460020]
          mov EDI,ECX
          shr EDI,16
          mov EAX,EDI
          movzx EDI,AL
          mov EAX,DWORD PTR [ESP]
          mov EBP,DWORD PTR [EDI*4+L_460420]
          xor EBP,ESI
          mov ESI,DWORD PTR [ESP+4]
          xor EAX,EBP
          mov DWORD PTR [EDX+176],EBP
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [EDX+180],EAX
          xor ESI,EAX
          xor EBX,ESI
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [EDX+184],ESI
          mov EDI,EBX
          mov DWORD PTR [EDX+188],EBX
          mov EAX,DWORD PTR [ESP+8]
          shr EDI,24
          xor EAX,DWORD PTR [L_461c34]
          movzx ESI,BL
          xor EAX,DWORD PTR [EDI*4+L_460420]
          mov EDI,EBX
          mov DWORD PTR [ESP+8],EBX
          shr EDI,16
          xor EAX,DWORD PTR [ESI*4+L_460820]
          movzx ESI,BH
          mov EBX,EDI
          xor EAX,DWORD PTR [ESI*4+L_45fc20]
          mov EDI,DWORD PTR [ESP+12]
          movzx ESI,BL
          xor EAX,DWORD PTR [ESI*4+L_460020]
          mov ESI,DWORD PTR [ESP+16]
          xor EDI,EAX
          mov DWORD PTR [EDX+192],EAX
          xor EAX,DWORD PTR [L_461c38]
          xor ESI,EDI
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [EDX+196],EDI
          xor ECX,ESI
          mov EDI,ESI
          mov DWORD PTR [EDX+200],ESI
          mov EBX,ECX
          movzx ESI,CL
          mov DWORD PTR [EDX+204],ECX
          shr EBX,24
          mov ESI,DWORD PTR [ESI*4+L_45fc20]
          xor ESI,DWORD PTR [EBX*4+L_460820]
          xor ESI,EBP
          movzx EBP,CH
          xor ESI,DWORD PTR [EBP*4+L_460020]
          mov EBP,ECX
          shr EBP,16
          mov EBX,EBP
          movzx EBP,BL
          mov EBX,DWORD PTR [ESP+8]
          xor ESI,DWORD PTR [EBP*4+L_460420]
          mov DWORD PTR [EDX+208],ESI
          xor ESI,DWORD PTR [ESP]
          mov DWORD PTR [EDX+212],ESI
          xor ESI,DWORD PTR [ESP+4]
          xor EBX,ESI
          mov DWORD PTR [EDX+216],ESI
          mov ESI,EBX
          mov DWORD PTR [EDX+220],EBX
          shr ESI,24
          xor EAX,DWORD PTR [ESI*4+L_460420]
          movzx ESI,BL
          xor EAX,DWORD PTR [ESI*4+L_460820]
          movzx ESI,BH
          shr EBX,16
          xor EAX,DWORD PTR [ESI*4+L_45fc20]
          movzx EBX,BL
          xor EAX,DWORD PTR [EBX*4+L_460020]
          mov DWORD PTR [EDX+224],EAX
          xor EAX,DWORD PTR [ESP+12]
          xor EDI,EAX
          mov DWORD PTR [EDX+228],EAX
          mov DWORD PTR [EDX+240],0
          xor ECX,EDI
          mov DWORD PTR [EDX+232],EDI
          mov BYTE PTR [EDX+240],224
          mov DWORD PTR [EDX+236],ECX
          add ESP,20
          xor EAX,EAX
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
FUN_43c6f0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,8
          mov EAX,DWORD PTR [ESP+32]
          mov ECX,DWORD PTR [ESP+28]
          mov EDX,DWORD PTR [ESP+36]
          cmp EAX,32
          je L_43cac0
          jle L_43c740
          cmp EAX,192
          je L_43c74e
          cmp EAX,256
          je L_43cac0
          add EAX,-128
          je L_43caa5
L_43c729:
          add ESP,8
          mov EAX,1
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_43c740:
          cmp EAX,16
          je L_43caa5
          cmp EAX,24
          jne L_43c729
L_43c74e:
          mov EAX,DWORD PTR [ECX]
          mov DWORD PTR [EDX],EAX
          mov ESI,DWORD PTR [ECX+4]
          xor EAX,DWORD PTR [L_461c20]
          mov DWORD PTR [EDX+4],ESI
          mov EBX,DWORD PTR [ECX+8]
          mov DWORD PTR [EDX+8],EBX
          mov EDI,DWORD PTR [ECX+12]
          mov DWORD PTR [EDX+12],EDI
          mov EBP,DWORD PTR [ECX+16]
          mov DWORD PTR [EDX+16],EBP
          mov ECX,DWORD PTR [ECX+20]
          mov DWORD PTR [ESP],EBP
          mov EBP,ECX
          mov DWORD PTR [EDX+20],ECX
          shr EBP,24
          xor EAX,DWORD PTR [EBP*4+L_460420]
          movzx EBP,CL
          xor EAX,DWORD PTR [EBP*4+L_460820]
          movzx EBP,CH
          xor EAX,DWORD PTR [EBP*4+L_45fc20]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,ECX
          shr EAX,16
          movzx EBP,AL
          mov EAX,DWORD PTR [ESP+4]
          xor EAX,DWORD PTR [EBP*4+L_460020]
          mov EBP,DWORD PTR [ESP]
          xor ESI,EAX
          mov DWORD PTR [EDX+24],EAX
          xor EAX,DWORD PTR [L_461c24]
          xor EBX,ESI
          mov DWORD PTR [EDX+28],ESI
          xor EDI,EBX
          mov DWORD PTR [EDX+32],EBX
          xor EBP,EDI
          mov DWORD PTR [EDX+36],EDI
          xor ECX,EBP
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [EDX+40],EBP
          mov EBP,ECX
          mov DWORD PTR [EDX+44],ECX
          shr EBP,24
          xor EAX,DWORD PTR [EBP*4+L_460420]
          movzx EBP,CL
          xor EAX,DWORD PTR [EBP*4+L_460820]
          movzx EBP,CH
          xor EAX,DWORD PTR [EBP*4+L_45fc20]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,ECX
          shr EAX,16
          movzx EBP,AL
          mov EAX,DWORD PTR [ESP+4]
          xor EAX,DWORD PTR [EBP*4+L_460020]
          mov EBP,DWORD PTR [ESP]
          xor ESI,EAX
          mov DWORD PTR [EDX+48],EAX
          xor EAX,DWORD PTR [L_461c28]
          xor EBX,ESI
          mov DWORD PTR [EDX+52],ESI
          xor EDI,EBX
          mov DWORD PTR [EDX+56],EBX
          xor EBP,EDI
          mov DWORD PTR [EDX+60],EDI
          xor ECX,EBP
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [EDX+64],EBP
          mov EBP,ECX
          mov DWORD PTR [EDX+68],ECX
          shr EBP,24
          xor EAX,DWORD PTR [EBP*4+L_460420]
          movzx EBP,CL
          xor EAX,DWORD PTR [EBP*4+L_460820]
          movzx EBP,CH
          xor EAX,DWORD PTR [EBP*4+L_45fc20]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,ECX
          shr EAX,16
          movzx EBP,AL
          mov EAX,DWORD PTR [ESP+4]
          xor EAX,DWORD PTR [EBP*4+L_460020]
          mov EBP,DWORD PTR [ESP]
          xor ESI,EAX
          mov DWORD PTR [EDX+72],EAX
          xor EBX,ESI
          xor EAX,DWORD PTR [L_461c2c]
          mov DWORD PTR [EDX+76],ESI
          xor EDI,EBX
          mov DWORD PTR [EDX+80],EBX
          xor EBP,EDI
          mov DWORD PTR [EDX+84],EDI
          xor ECX,EBP
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [EDX+88],EBP
          mov EBP,ECX
          mov DWORD PTR [EDX+92],ECX
          shr EBP,24
          xor EAX,DWORD PTR [EBP*4+L_460420]
          movzx EBP,CL
          xor EAX,DWORD PTR [EBP*4+L_460820]
          movzx EBP,CH
          xor EAX,DWORD PTR [EBP*4+L_45fc20]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,ECX
          shr EAX,16
          movzx EBP,AL
          mov EAX,DWORD PTR [ESP+4]
          xor EAX,DWORD PTR [EBP*4+L_460020]
          mov DWORD PTR [EDX+96],EAX
          xor ESI,EAX
          mov EBP,DWORD PTR [ESP]
          xor EBX,ESI
          xor EAX,DWORD PTR [L_461c30]
          mov DWORD PTR [EDX+100],ESI
          xor EDI,EBX
          mov DWORD PTR [EDX+104],EBX
          xor EBP,EDI
          mov DWORD PTR [EDX+108],EDI
          xor ECX,EBP
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [EDX+112],EBP
          mov EBP,ECX
          mov DWORD PTR [EDX+116],ECX
          shr EBP,24
          xor EAX,DWORD PTR [EBP*4+L_460420]
          movzx EBP,CL
          xor EAX,DWORD PTR [EBP*4+L_460820]
          movzx EBP,CH
          xor EAX,DWORD PTR [EBP*4+L_45fc20]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,ECX
          shr EAX,16
          movzx EBP,AL
          mov EAX,DWORD PTR [ESP+4]
          xor EAX,DWORD PTR [EBP*4+L_460020]
          mov EBP,DWORD PTR [ESP]
          xor ESI,EAX
          mov DWORD PTR [EDX+120],EAX
          xor EAX,DWORD PTR [L_461c34]
          xor EBX,ESI
          mov DWORD PTR [EDX+124],ESI
          xor EDI,EBX
          mov DWORD PTR [EDX+128],EBX
          xor EBP,EDI
          mov DWORD PTR [EDX+132],EDI
          xor ECX,EBP
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [EDX+136],EBP
          mov EBP,ECX
          mov DWORD PTR [EDX+140],ECX
          shr EBP,24
          xor EAX,DWORD PTR [EBP*4+L_460420]
          movzx EBP,CL
          xor EAX,DWORD PTR [EBP*4+L_460820]
          movzx EBP,CH
          xor EAX,DWORD PTR [EBP*4+L_45fc20]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,ECX
          shr EAX,16
          movzx EBP,AL
          mov EAX,DWORD PTR [ESP+4]
          xor EAX,DWORD PTR [EBP*4+L_460020]
          xor ESI,EAX
          mov DWORD PTR [EDX+144],EAX
          xor EBX,ESI
          mov DWORD PTR [EDX+148],ESI
          xor EDI,EBX
          mov DWORD PTR [EDX+152],EBX
          mov DWORD PTR [EDX+156],EDI
          mov EBP,DWORD PTR [ESP]
          xor EAX,DWORD PTR [L_461c38]
          mov DWORD PTR [EDX+240],0
          mov BYTE PTR [EDX+240],192
          xor EBP,EDI
          xor ECX,EBP
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [EDX+160],EBP
          mov EBP,ECX
          mov DWORD PTR [EDX+164],ECX
          shr EBP,24
          xor EAX,DWORD PTR [EBP*4+L_460420]
          movzx EBP,CL
          xor EAX,DWORD PTR [EBP*4+L_460820]
          movzx EBP,CH
          xor EAX,DWORD PTR [EBP*4+L_45fc20]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,ECX
          shr EAX,16
          movzx EBP,AL
          mov EAX,DWORD PTR [ESP+4]
          xor EAX,DWORD PTR [EBP*4+L_460020]
          mov EBP,DWORD PTR [ESP]
          xor ESI,EAX
          mov DWORD PTR [EDX+168],EAX
          xor EAX,DWORD PTR [L_461c3c]
          xor EBX,ESI
          mov DWORD PTR [EDX+172],ESI
          xor EDI,EBX
          mov DWORD PTR [EDX+176],EBX
          xor EBP,EDI
          mov DWORD PTR [EDX+180],EDI
          xor ECX,EBP
          mov DWORD PTR [EDX+184],EBP
          mov EBP,ECX
          mov DWORD PTR [EDX+188],ECX
          shr EBP,24
          xor EAX,DWORD PTR [EBP*4+L_460420]
          movzx EBP,CL
          xor EAX,DWORD PTR [EBP*4+L_460820]
          movzx EBP,CH
          shr ECX,16
          xor EAX,DWORD PTR [EBP*4+L_45fc20]
          movzx ECX,CL
          xor EAX,DWORD PTR [ECX*4+L_460020]
          xor ESI,EAX
          mov DWORD PTR [EDX+192],EAX
          xor EAX,EAX
          xor EBX,ESI
          mov DWORD PTR [EDX+196],ESI
          xor EDI,EBX
          mov DWORD PTR [EDX+200],EBX
          mov DWORD PTR [EDX+204],EDI
          add ESP,8
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_43caa5:
          mov DWORD PTR [ESP+32],EDX
          mov DWORD PTR [ESP+28],ECX
          add ESP,8
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          jmp L_43bae0
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_43cac0:
          mov DWORD PTR [ESP+32],EDX
          mov DWORD PTR [ESP+28],ECX
          add ESP,8
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          jmp L_43c1b0
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
L_43cae0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,24
          mov EDX,DWORD PTR [ESP+44]
          mov EBX,DWORD PTR [ESP+48]
          mov ECX,DWORD PTR [EDX]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [EBX],ECX
          mov ESI,DWORD PTR [EDX+4]
          mov DWORD PTR [EBX+4],ESI
          mov EAX,DWORD PTR [EDX+8]
          mov EDI,EAX
          mov DWORD PTR [EBX+8],EAX
          mov EAX,DWORD PTR [EDX+12]
          mov EDX,EAX
          mov DWORD PTR [EBX+12],EAX
          movzx EBX,AL
          shr EDX,24
          mov EDX,DWORD PTR [EDX*4+L_460420]
          xor EDX,DWORD PTR [EBX*4+L_460820]
          movzx EBX,AH
          xor EDX,DWORD PTR [L_461c20]
          xor EDX,DWORD PTR [EBX*4+L_45fc20]
          mov EBX,EAX
          shr EBX,16
          movzx EBX,BL
          xor EDX,DWORD PTR [EBX*4+L_460020]
          mov EBX,EDI
          xor EBX,ESI
          xor EBX,ECX
          xor EBX,EAX
          xor EBX,EDX
          xor EDX,ECX
          mov ECX,EDX
          mov DWORD PTR [ESP+4],EBX
          movzx EBX,DL
          shr ECX,24
          mov EBP,DWORD PTR [EBX*4+L_45cc20]
          mov EBX,DWORD PTR [ESP]
          xor EBP,DWORD PTR [ECX*4+L_45d820]
          movzx ECX,DH
          xor EBP,DWORD PTR [ECX*4+L_45d020]
          mov ECX,EDX
          xor EDX,ESI
          shr ECX,16
          movzx ECX,CL
          xor EBP,DWORD PTR [ECX*4+L_45d420]
          movzx ECX,DL
          mov ECX,DWORD PTR [ECX*4+L_45cc20]
          mov DWORD PTR [EBX+16],EBP
          mov EBX,EDX
          mov DWORD PTR [ESP+16],EBP
          shr EBX,24
          xor ECX,DWORD PTR [EBX*4+L_45d820]
          movzx EBX,DH
          xor ECX,DWORD PTR [EBX*4+L_45d020]
          mov EBX,EDX
          xor EDX,EDI
          shr EBX,16
          movzx EBX,BL
          xor ECX,DWORD PTR [EBX*4+L_45d420]
          mov EBP,DWORD PTR [ESP]
          movzx EBX,DH
          mov DWORD PTR [ESP+12],EDI
          mov EDI,EDX
          shr EDI,24
          mov DWORD PTR [EBP+20],ECX
          mov DWORD PTR [ESP+20],ECX
          movzx ECX,DL
          mov ECX,DWORD PTR [ECX*4+L_45cc20]
          xor ECX,DWORD PTR [EDI*4+L_45d820]
          mov EDI,EDX
          shr EDI,16
          xor EDX,EAX
          xor ECX,DWORD PTR [EBX*4+L_45d020]
          mov EBX,EDI
          mov EDI,EDX
          movzx EBX,BL
          shr EDI,24
          xor ECX,DWORD PTR [EBX*4+L_45d420]
          movzx EBX,DL
          mov EBX,DWORD PTR [EBX*4+L_45cc20]
          xor EBX,DWORD PTR [EDI*4+L_45d820]
          movzx EDI,DH
          xor EBX,DWORD PTR [EDI*4+L_45d020]
          shr EDX,16
          mov EDI,DWORD PTR [ESP]
          movzx EDX,DL
          mov DWORD PTR [EBP+24],ECX
          xor EBX,DWORD PTR [EDX*4+L_45d420]
          mov EBP,EAX
          mov EAX,DWORD PTR [ESP+4]
          xor ESI,EBP
          mov DWORD PTR [ESP+8],EBP
          mov EDX,EAX
          mov DWORD PTR [EDI+28],EBX
          movzx EDI,AL
          shr EDX,24
          mov EDX,DWORD PTR [EDX*4+L_460420]
          xor EDX,DWORD PTR [EDI*4+L_460820]
          movzx EDI,AH
          xor EDX,DWORD PTR [L_461c24]
          xor EDX,DWORD PTR [EDI*4+L_45fc20]
          mov EDI,EAX
          shr EDI,16
          mov EAX,EDI
          movzx EDI,AL
          xor EDX,DWORD PTR [EDI*4+L_460020]
          xor ESI,EDX
          movzx EDI,DL
          mov EAX,ESI
          mov ESI,EDX
          mov EBP,DWORD PTR [EDI*4+L_45cc20]
          shr ESI,24
          mov EDI,DWORD PTR [ESP]
          xor EBP,DWORD PTR [ESI*4+L_45d820]
          movzx ESI,DH
          shr EDX,16
          xor EBP,DWORD PTR [ESP+16]
          movzx EDX,DL
          xor EBP,DWORD PTR [ESI*4+L_45d020]
          movzx ESI,AL
          xor EBP,DWORD PTR [EDX*4+L_45d420]
          mov EDX,DWORD PTR [ESP+20]
          xor EDX,EBP
          mov DWORD PTR [EDI+32],EBP
          xor ECX,EDX
          mov DWORD PTR [EDI+36],EDX
          xor EBX,ECX
          mov DWORD PTR [EDI+40],ECX
          mov DWORD PTR [ESP+16],EAX
          mov DWORD PTR [EDI+44],EBX
          mov DWORD PTR [ESP+20],EBX
          mov EBX,EAX
          shr EBX,24
          mov EBX,DWORD PTR [EBX*4+L_460420]
          xor EBX,DWORD PTR [ESI*4+L_460820]
          movzx ESI,AH
          xor EBX,DWORD PTR [L_461c28]
          xor EBX,DWORD PTR [ESI*4+L_45fc20]
          mov ESI,EAX
          shr ESI,16
          mov EAX,ESI
          movzx ESI,AL
          xor EBX,DWORD PTR [ESI*4+L_460020]
          mov ESI,DWORD PTR [ESP+12]
          xor ESI,DWORD PTR [ESP+8]
          movzx EDI,BL
          xor ESI,EBX
          mov EDI,DWORD PTR [EDI*4+L_45cc20]
          mov EAX,ESI
          mov ESI,EBX
          shr ESI,24
          mov DWORD PTR [ESP+12],EAX
          xor EDI,DWORD PTR [ESI*4+L_45d820]
          movzx ESI,BH
          xor EBP,EDI
          xor EBP,DWORD PTR [ESI*4+L_45d020]
          shr EBX,16
          movzx EBX,BL
          mov ESI,DWORD PTR [ESP]
          xor EBP,DWORD PTR [EBX*4+L_45d420]
          mov EBX,EAX
          shr EBX,24
          mov EBX,DWORD PTR [EBX*4+L_460420]
          xor EDX,EBP
          mov DWORD PTR [ESI+48],EBP
          mov EDI,EBP
          mov EBP,DWORD PTR [ESP+20]
          xor ECX,EDX
          mov DWORD PTR [ESI+52],EDX
          mov DWORD PTR [ESI+56],ECX
          xor EBP,ECX
          mov DWORD PTR [ESI+60],EBP
          movzx ESI,AL
          mov DWORD PTR [ESP+20],EBP
          xor EBX,DWORD PTR [ESI*4+L_460820]
          movzx ESI,AH
          xor EBX,DWORD PTR [L_461c2c]
          xor EBX,DWORD PTR [ESI*4+L_45fc20]
          mov ESI,EAX
          shr ESI,16
          mov EAX,ESI
          movzx ESI,AL
          xor EBX,DWORD PTR [ESI*4+L_460020]
          mov ESI,DWORD PTR [ESP+8]
          mov EBP,EBX
          xor ESI,EBX
          mov EAX,ESI
          shr EBP,24
          movzx ESI,BL
          mov ESI,DWORD PTR [ESI*4+L_45cc20]
          xor ESI,DWORD PTR [EBP*4+L_45d820]
          xor EDI,ESI
          movzx ESI,BH
          shr EBX,16
          xor EDI,DWORD PTR [ESI*4+L_45d020]
          movzx EBX,BL
          xor EDI,DWORD PTR [EBX*4+L_45d420]
          mov ESI,DWORD PTR [ESP]
          mov EBX,DWORD PTR [ESP+20]
          mov DWORD PTR [ESP+8],EAX
          xor EDX,EDI
          mov DWORD PTR [ESI+64],EDI
          xor ECX,EDX
          mov DWORD PTR [ESI+68],EDX
          xor EBX,ECX
          mov DWORD PTR [ESI+72],ECX
          mov DWORD PTR [ESP+20],EBX
          mov DWORD PTR [ESI+76],EBX
          mov EBX,EAX
          movzx ESI,AL
          shr EBX,24
          mov EBX,DWORD PTR [EBX*4+L_460420]
          xor EBX,DWORD PTR [ESI*4+L_460820]
          movzx ESI,AH
          xor EBX,DWORD PTR [L_461c30]
          xor EBX,DWORD PTR [ESI*4+L_45fc20]
          mov ESI,EAX
          shr ESI,16
          mov EAX,ESI
          movzx ESI,AL
          xor EBX,DWORD PTR [ESI*4+L_460020]
          mov ESI,DWORD PTR [ESP+4]
          mov EBP,EBX
          xor ESI,EBX
          mov EAX,ESI
          shr EBP,24
          movzx ESI,BL
          mov ESI,DWORD PTR [ESI*4+L_45cc20]
          xor ESI,DWORD PTR [EBP*4+L_45d820]
          mov EBP,DWORD PTR [ESP+20]
          mov DWORD PTR [ESP+4],EAX
          xor EDI,ESI
          movzx ESI,BH
          xor EDI,DWORD PTR [ESI*4+L_45d020]
          shr EBX,16
          mov ESI,DWORD PTR [ESP]
          movzx EBX,BL
          xor EDI,DWORD PTR [EBX*4+L_45d420]
          mov EBX,EAX
          shr EBX,24
          mov EBX,DWORD PTR [EBX*4+L_460420]
          xor EDX,EDI
          mov DWORD PTR [ESI+80],EDI
          xor ECX,EDX
          mov DWORD PTR [ESI+84],EDX
          xor EBP,ECX
          mov DWORD PTR [ESI+88],ECX
          mov DWORD PTR [ESP+20],EBP
          mov DWORD PTR [ESI+92],EBP
          movzx ESI,AL
          mov EBP,EAX
          xor EBX,DWORD PTR [ESI*4+L_460820]
          movzx ESI,AH
          shr EBP,16
          xor EBX,DWORD PTR [L_461c34]
          mov EAX,EBP
          xor EBX,DWORD PTR [ESI*4+L_45fc20]
          movzx ESI,AL
          xor EBX,DWORD PTR [ESI*4+L_460020]
          mov ESI,DWORD PTR [ESP+16]
          xor ESI,EBX
          movzx EBP,BL
          mov EAX,ESI
          mov ESI,EBX
          mov EBP,DWORD PTR [EBP*4+L_45cc20]
          shr ESI,24
          mov DWORD PTR [ESP+16],EAX
          xor EBP,DWORD PTR [ESI*4+L_45d820]
          movzx ESI,BH
          shr EBX,16
          movzx EBX,BL
          xor EDI,EBP
          xor EDI,DWORD PTR [ESI*4+L_45d020]
          mov EBP,DWORD PTR [ESP+20]
          xor EDI,DWORD PTR [EBX*4+L_45d420]
          mov ESI,DWORD PTR [ESP]
          mov EBX,EAX
          shr EBX,24
          mov EBX,DWORD PTR [EBX*4+L_460420]
          xor EDX,EDI
          mov DWORD PTR [ESI+96],EDI
          xor ECX,EDX
          mov DWORD PTR [ESI+100],EDX
          xor EBP,ECX
          mov DWORD PTR [ESI+104],ECX
          mov DWORD PTR [ESI+108],EBP
          movzx ESI,AL
          mov DWORD PTR [ESP+20],EBP
          xor EBX,DWORD PTR [ESI*4+L_460820]
          movzx ESI,AH
          xor EBX,DWORD PTR [L_461c38]
          xor EBX,DWORD PTR [ESI*4+L_45fc20]
          mov ESI,EAX
          shr ESI,16
          mov EAX,ESI
          movzx ESI,AL
          xor EBX,DWORD PTR [ESI*4+L_460020]
          mov ESI,DWORD PTR [ESP+12]
          mov EBP,EBX
          xor ESI,EBX
          mov EAX,ESI
          shr EBP,24
          movzx ESI,BL
          mov ESI,DWORD PTR [ESI*4+L_45cc20]
          xor ESI,DWORD PTR [EBP*4+L_45d820]
          xor EDI,ESI
          movzx ESI,BH
          xor EDI,DWORD PTR [ESI*4+L_45d020]
          shr EBX,16
          movzx EBX,BL
          xor EDI,DWORD PTR [EBX*4+L_45d420]
          movzx EBX,AL
          mov ESI,EDI
          mov EDI,DWORD PTR [ESP]
          xor EDX,ESI
          xor ECX,EDX
          mov EBP,ECX
          mov DWORD PTR [EDI+112],ESI
          mov DWORD PTR [EDI+116],EDX
          mov DWORD PTR [EDI+120],EBP
          mov ECX,EDI
          mov EDI,DWORD PTR [ESP+20]
          xor EDI,EBP
          mov DWORD PTR [ECX+124],EDI
          mov ECX,EAX
          mov DWORD PTR [ESP+20],EDI
          shr ECX,24
          mov ECX,DWORD PTR [ECX*4+L_460420]
          xor ECX,DWORD PTR [EBX*4+L_460820]
          movzx EBX,AH
          xor ECX,DWORD PTR [L_461c3c]
          xor ECX,DWORD PTR [EBX*4+L_45fc20]
          mov EBX,EAX
          mov DWORD PTR [ESP+12],EAX
          shr EBX,16
          movzx EBX,BL
          xor ECX,DWORD PTR [EBX*4+L_460020]
          mov EBX,DWORD PTR [ESP+8]
          mov EAX,ECX
          xor EBX,ECX
          mov EDI,EBX
          shr EAX,24
          movzx EBX,CL
          mov EBX,DWORD PTR [EBX*4+L_45cc20]
          xor EBX,DWORD PTR [EAX*4+L_45d820]
          xor ESI,EBX
          movzx EBX,CH
          shr ECX,16
          xor ESI,DWORD PTR [EBX*4+L_45d020]
          movzx ECX,CL
          mov EBX,EDI
          xor ESI,DWORD PTR [ECX*4+L_45d420]
          mov ECX,DWORD PTR [ESP]
          shr EBX,16
          xor EDX,ESI
          mov DWORD PTR [ECX+128],ESI
          xor EBP,EDX
          mov DWORD PTR [ECX+132],EDX
          mov DWORD PTR [ESP+8],EDX
          mov EDX,ECX
          mov ECX,DWORD PTR [ESP+20]
          mov DWORD PTR [ESP+20],EBP
          mov DWORD PTR [EDX+136],EBP
          xor ECX,EBP
          mov DWORD PTR [EDX+140],ECX
          mov EAX,ECX
          mov EDX,EDI
          mov ECX,EDI
          movzx EDX,DL
          shr ECX,24
          mov ECX,DWORD PTR [ECX*4+L_460420]
          xor ECX,DWORD PTR [EDX*4+L_460820]
          mov EDX,EDI
          xor ECX,DWORD PTR [L_461c40]
          movzx EDX,DH
          xor ECX,DWORD PTR [EDX*4+L_45fc20]
          movzx EDX,BL
          mov EBX,DWORD PTR [ESP+4]
          xor ECX,DWORD PTR [EDX*4+L_460020]
          mov EBP,ECX
          movzx EDX,CL
          xor EBX,ECX
          shr EBP,24
          mov EDX,DWORD PTR [EDX*4+L_45cc20]
          xor EDX,DWORD PTR [EBP*4+L_45d820]
          xor ESI,EDX
          movzx EDX,CH
          xor ESI,DWORD PTR [EDX*4+L_45d020]
          shr ECX,16
          movzx ECX,CL
          xor ESI,DWORD PTR [ECX*4+L_45d420]
          mov ECX,DWORD PTR [ESP]
          mov EDX,ECX
          mov DWORD PTR [ECX+144],ESI
          xor ESI,DWORD PTR [ESP+8]
          mov DWORD PTR [ECX+148],ESI
          xor ESI,DWORD PTR [ESP+20]
          mov DWORD PTR [ECX+152],ESI
          xor ESI,EAX
          mov ECX,EBX
          mov DWORD PTR [EDX+156],ESI
          mov EAX,EDX
          shr ECX,24
          mov EDX,DWORD PTR [ESP+16]
          xor EDX,DWORD PTR [L_461c44]
          xor EDX,DWORD PTR [ECX*4+L_460420]
          movzx ECX,BL
          mov ESI,DWORD PTR [ESP+12]
          xor EDX,DWORD PTR [ECX*4+L_460820]
          movzx ECX,BH
          mov DWORD PTR [EAX+240],0
          xor EDX,DWORD PTR [ECX*4+L_45fc20]
          mov ECX,EBX
          mov BYTE PTR [EAX+240],160
          shr ECX,16
          xor ESI,EDI
          movzx ECX,CL
          xor EDX,DWORD PTR [ECX*4+L_460020]
          xor EBX,EDX
          xor EDI,EDX
          mov DWORD PTR [EAX+172],EDX
          xor ESI,EBX
          mov DWORD PTR [EAX+164],EDI
          mov DWORD PTR [EAX+168],EBX
          mov DWORD PTR [EAX+160],ESI
          add ESP,24
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x66
          .byte 0x90
L_43d150:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov EBX,DWORD PTR [ESP+64]
          mov ESI,DWORD PTR [ESP+68]
          mov EAX,DWORD PTR [EBX]
          mov DWORD PTR [ESI],EAX
          mov DWORD PTR [ESP],EAX
          mov EAX,DWORD PTR [EBX+4]
          mov DWORD PTR [ESI+4],EAX
          mov EDI,DWORD PTR [EBX+8]
          mov DWORD PTR [ESP+8],EAX
          mov EAX,ESI
          mov EDX,EAX
          mov DWORD PTR [ESI+8],EDI
          mov ESI,DWORD PTR [EBX+12]
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [EAX+12],ESI
          mov EDI,DWORD PTR [EBX+16]
          mov DWORD PTR [ESP+16],ESI
          mov ECX,EDI
          mov EBP,EDI
          mov EAX,EDI
          shr EBP,24
          movzx ECX,CL
          movzx ESI,AH
          mov ECX,DWORD PTR [ECX*4+L_45cc20]
          xor ECX,DWORD PTR [EBP*4+L_45d820]
          mov EBP,EDI
          shr EBP,16
          xor ECX,DWORD PTR [ESI*4+L_45d020]
          mov EAX,EBP
          movzx ESI,AL
          xor ECX,DWORD PTR [ESI*4+L_45d420]
          mov ESI,EDX
          mov DWORD PTR [EDX+16],ECX
          mov EAX,DWORD PTR [EBX+20]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+4]
          movzx EBP,BYTE PTR [ESP+4]
          mov ECX,EAX
          movzx EBX,AH
          shr ECX,16
          mov DWORD PTR [ESP+20],EBX
          movzx EAX,CL
          mov ECX,DWORD PTR [ESP+4]
          mov EDX,EAX
          shr ECX,24
          mov EAX,ECX
          mov ECX,DWORD PTR [EBP*4+L_45cc20]
          xor ECX,DWORD PTR [EAX*4+L_45d820]
          mov EBX,DWORD PTR [ESP+20]
          mov DWORD PTR [ESP+20],EDX
          xor ECX,DWORD PTR [EBX*4+L_45d020]
          xor ECX,DWORD PTR [EDX*4+L_45d420]
          mov EDX,DWORD PTR [ESP]
          xor EDX,DWORD PTR [L_461c20]
          xor EDX,DWORD PTR [EAX*4+L_460420]
          mov EAX,DWORD PTR [ESP+20]
          xor EDX,DWORD PTR [EBP*4+L_460820]
          xor EDX,DWORD PTR [EBX*4+L_45fc20]
          mov DWORD PTR [ESI+20],ECX
          xor EDX,DWORD PTR [EAX*4+L_460020]
          mov EBP,EDX
          movzx ECX,DL
          shr EDX,24
          mov EAX,EBP
          mov EBX,DWORD PTR [ECX*4+L_45cc20]
          xor EBX,DWORD PTR [EDX*4+L_45d820]
          movzx EDX,AH
          mov EAX,DWORD PTR [ESP+8]
          xor EBX,DWORD PTR [EDX*4+L_45d020]
          mov EDX,EBP
          shr EDX,16
          xor EAX,EBP
          movzx EDX,DL
          xor EBX,DWORD PTR [EDX*4+L_45d420]
          mov EDX,EAX
          movzx ECX,AL
          shr EDX,24
          mov ECX,DWORD PTR [ECX*4+L_45cc20]
          xor ECX,DWORD PTR [EDX*4+L_45d820]
          movzx EDX,AH
          xor ECX,DWORD PTR [EDX*4+L_45d020]
          mov EDX,EAX
          shr EDX,16
          mov DWORD PTR [ESP+20],EBX
          mov DWORD PTR [ESI+24],EBX
          movzx EDX,DL
          mov EBX,EAX
          mov EAX,DWORD PTR [EDX*4+L_45d420]
          mov DWORD PTR [ESP+8],EBX
          xor EAX,ECX
          mov ECX,DWORD PTR [ESP+12]
          mov DWORD PTR [ESP+24],EAX
          mov DWORD PTR [ESI+28],EAX
          xor ECX,EBX
          mov EAX,ECX
          movzx ECX,CL
          mov EDX,EAX
          mov ECX,DWORD PTR [ECX*4+L_45cc20]
          shr EDX,24
          xor ECX,DWORD PTR [EDX*4+L_45d820]
          movzx EDX,AH
          xor ECX,DWORD PTR [EDX*4+L_45d020]
          mov EDX,EAX
          shr EDX,16
          movzx EDX,DL
          xor ECX,DWORD PTR [EDX*4+L_45d420]
          mov DWORD PTR [ESP+28],ECX
          mov DWORD PTR [ESI+32],ECX
          mov ECX,DWORD PTR [ESP+16]
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP],ESI
          xor ECX,EAX
          mov EBX,ECX
          movzx ECX,CL
          mov EAX,EBX
          mov ECX,DWORD PTR [ECX*4+L_45cc20]
          movzx EDX,BH
          shr EAX,24
          xor EDI,EBX
          mov DWORD PTR [ESP+16],EBX
          xor ECX,DWORD PTR [EAX*4+L_45d820]
          mov EAX,EBX
          shr EAX,16
          xor ECX,DWORD PTR [EDX*4+L_45d020]
          movzx EDX,AL
          mov EAX,EDI
          xor ECX,DWORD PTR [EDX*4+L_45d420]
          movzx EDX,AL
          mov EAX,EDI
          mov EDX,DWORD PTR [EDX*4+L_45cc20]
          mov DWORD PTR [ESI+36],ECX
          mov DWORD PTR [ESP+32],ECX
          mov ECX,EDI
          shr ECX,24
          xor EDX,DWORD PTR [ECX*4+L_45d820]
          movzx ECX,AH
          xor EDX,DWORD PTR [ECX*4+L_45d020]
          mov ECX,EDI
          shr ECX,16
          movzx ECX,CL
          xor EDX,DWORD PTR [ECX*4+L_45d420]
          mov DWORD PTR [ESI+40],EDX
          mov ESI,DWORD PTR [ESP+4]
          mov DWORD PTR [ESP+36],EDX
          xor ESI,EDI
          mov EDX,ESI
          mov ECX,EDX
          movzx ESI,DL
          shr ECX,16
          movzx EBX,CL
          mov ECX,EDX
          shr ECX,24
          mov EAX,ECX
          mov ECX,DWORD PTR [ESI*4+L_45cc20]
          mov DWORD PTR [ESP+4],EAX
          xor ECX,DWORD PTR [EAX*4+L_45d820]
          movzx EAX,DH
          xor ECX,DWORD PTR [EAX*4+L_45d020]
          mov EAX,DWORD PTR [EBX*4+L_45d420]
          xor EAX,ECX
          mov ECX,DWORD PTR [ESP]
          mov DWORD PTR [ESP+40],EAX
          mov DWORD PTR [ECX+44],EAX
          mov ECX,DWORD PTR [ESP+4]
          mov ECX,DWORD PTR [ECX*4+L_460420]
          xor ECX,DWORD PTR [ESI*4+L_460820]
          movzx ESI,DH
          xor ECX,DWORD PTR [L_461c24]
          xor ECX,DWORD PTR [ESI*4+L_45fc20]
          xor ECX,DWORD PTR [EBX*4+L_460020]
          mov ESI,ECX
          movzx EBX,CL
          xor EBP,ECX
          shr ESI,24
          mov EBX,DWORD PTR [EBX*4+L_45cc20]
          xor EBX,DWORD PTR [ESI*4+L_45d820]
          movzx ESI,CH
          shr ECX,16
          xor EBX,DWORD PTR [ESP+20]
          movzx ECX,CL
          xor EBX,DWORD PTR [ESI*4+L_45d020]
          mov EAX,DWORD PTR [ECX*4+L_45d420]
          mov ESI,DWORD PTR [ESP+24]
          xor EAX,EBX
          mov EBX,DWORD PTR [ESP]
          mov ECX,EAX
          xor ESI,ECX
          mov DWORD PTR [EBX+48],EAX
          mov EAX,DWORD PTR [ESP+8]
          mov DWORD PTR [EBX+52],ESI
          mov DWORD PTR [ESP+8],ECX
          mov ECX,ESI
          mov ESI,DWORD PTR [ESP+12]
          xor EAX,EBP
          mov DWORD PTR [ESP+12],EAX
          xor ESI,EAX
          mov EAX,ESI
          mov ESI,DWORD PTR [ESP+28]
          xor ESI,ECX
          mov DWORD PTR [EBX+56],ESI
          mov EBX,DWORD PTR [ESP+16]
          mov DWORD PTR [ESP+16],EAX
          mov DWORD PTR [ESP+20],ESI
          xor EBX,EAX
          mov EAX,DWORD PTR [ESP+32]
          xor EDI,EBX
          mov DWORD PTR [ESP+24],EBX
          mov EBX,DWORD PTR [ESP+36]
          xor EDX,EDI
          mov DWORD PTR [ESP+32],EDI
          mov EDI,DWORD PTR [ESP+40]
          xor EAX,ESI
          mov ESI,DWORD PTR [ESP]
          xor EBX,EAX
          mov DWORD PTR [ESP+28],EAX
          mov DWORD PTR [ESI+60],EAX
          mov EAX,DWORD PTR [ESP]
          mov ESI,EBX
          xor EDI,ESI
          mov DWORD PTR [ESP+36],ESI
          mov DWORD PTR [ESP+40],EDI
          mov DWORD PTR [EAX+68],EDI
          mov EDI,EDX
          mov DWORD PTR [EAX+64],EBX
          shr EDI,24
          mov ESI,EDI
          movzx EDI,DL
          mov ESI,DWORD PTR [ESI*4+L_460420]
          xor ESI,DWORD PTR [EDI*4+L_460820]
          movzx EDI,DH
          xor ESI,DWORD PTR [L_461c28]
          mov EBX,DWORD PTR [ESP+8]
          xor ESI,DWORD PTR [EDI*4+L_45fc20]
          mov EDI,EDX
          shr EDI,16
          mov EAX,EDI
          movzx EDI,AL
          xor ESI,DWORD PTR [EDI*4+L_460020]
          xor EBP,ESI
          mov EAX,ESI
          mov DWORD PTR [ESP+4],EBP
          mov EBP,ESI
          movzx EDI,AL
          shr EBP,24
          mov EDI,DWORD PTR [EDI*4+L_45cc20]
          mov EAX,ESI
          xor EDI,DWORD PTR [EBP*4+L_45d820]
          shr ESI,16
          mov EBP,DWORD PTR [ESP+16]
          xor EBX,EDI
          movzx EDI,AH
          mov EAX,ESI
          xor EBX,DWORD PTR [EDI*4+L_45d020]
          movzx ESI,AL
          mov EDI,DWORD PTR [ESP+12]
          xor EBX,DWORD PTR [ESI*4+L_45d420]
          mov ESI,DWORD PTR [ESP]
          xor EDI,DWORD PTR [ESP+4]
          mov EAX,ESI
          xor ECX,EBX
          mov DWORD PTR [ESI+72],EBX
          mov DWORD PTR [ESI+76],ECX
          mov ESI,DWORD PTR [ESP+20]
          xor EBP,EDI
          mov DWORD PTR [ESP+8],EDI
          mov EDI,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP+12],EBP
          xor ESI,ECX
          mov DWORD PTR [EAX+80],ESI
          mov EAX,DWORD PTR [ESP+28]
          xor EDI,EBP
          mov DWORD PTR [ESP+16],ESI
          mov EBP,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+20],EDI
          xor EAX,ESI
          mov ESI,DWORD PTR [ESP]
          xor EBP,EAX
          mov DWORD PTR [ESP+24],EAX
          mov DWORD PTR [ESI+84],EAX
          mov ESI,DWORD PTR [ESP+32]
          xor ESI,EDI
          mov EDI,DWORD PTR [ESP]
          xor EDX,ESI
          mov DWORD PTR [ESP+28],ESI
          mov DWORD PTR [EDI+88],EBP
          mov ESI,DWORD PTR [ESP+40]
          xor ESI,EBP
          mov DWORD PTR [EDI+92],ESI
          mov EDI,EDX
          mov DWORD PTR [ESP+32],ESI
          shr EDI,24
          mov ESI,EDI
          movzx EDI,DL
          mov ESI,DWORD PTR [ESI*4+L_460420]
          xor ESI,DWORD PTR [EDI*4+L_460820]
          movzx EDI,DH
          xor ESI,DWORD PTR [L_461c2c]
          xor ESI,DWORD PTR [EDI*4+L_45fc20]
          mov EDI,EDX
          shr EDI,16
          mov EAX,EDI
          movzx EDI,AL
          mov EAX,DWORD PTR [ESP+4]
          xor ESI,DWORD PTR [EDI*4+L_460020]
          xor EAX,ESI
          mov DWORD PTR [ESP+4],EAX
          mov EAX,ESI
          movzx EDI,AL
          mov EAX,ESI
          shr EAX,24
          mov EDI,DWORD PTR [EDI*4+L_45cc20]
          xor EDI,DWORD PTR [EAX*4+L_45d820]
          mov EAX,ESI
          shr ESI,16
          xor EBX,EDI
          movzx EDI,AH
          mov EAX,ESI
          xor EBX,DWORD PTR [EDI*4+L_45d020]
          movzx ESI,AL
          mov EDI,DWORD PTR [ESP+8]
          xor EBX,DWORD PTR [ESI*4+L_45d420]
          xor EDI,DWORD PTR [ESP+4]
          mov ESI,DWORD PTR [ESP]
          mov EAX,DWORD PTR [ESP+12]
          xor ECX,EBX
          mov DWORD PTR [ESI+96],EBX
          xor EAX,EDI
          mov DWORD PTR [ESI+100],ECX
          mov ESI,DWORD PTR [ESP+16]
          mov DWORD PTR [ESP+8],EDI
          mov EDI,DWORD PTR [ESP]
          mov DWORD PTR [ESP+12],EAX
          xor ESI,ECX
          mov DWORD PTR [EDI+104],ESI
          mov EDI,DWORD PTR [ESP+20]
          mov DWORD PTR [ESP+16],ESI
          xor EDI,EAX
          mov EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP+20],EDI
          xor EAX,ESI
          mov ESI,DWORD PTR [ESP]
          xor EBP,EAX
          mov DWORD PTR [ESI+108],EAX
          mov ESI,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+24],EAX
          mov EAX,DWORD PTR [ESP]
          xor ESI,EDI
          mov EDI,EBP
          mov DWORD PTR [EAX+112],EBP
          mov EBP,DWORD PTR [ESP+32]
          xor EDX,ESI
          mov DWORD PTR [ESP+28],ESI
          movzx ESI,DL
          mov DWORD PTR [ESP+32],EDI
          xor EBP,EDI
          mov DWORD PTR [ESP+36],EBP
          mov DWORD PTR [EAX+116],EBP
          mov EBP,EDX
          shr EBP,24
          mov EBP,DWORD PTR [EBP*4+L_460420]
          xor EBP,DWORD PTR [ESI*4+L_460820]
          movzx ESI,DH
          xor EBP,DWORD PTR [L_461c30]
          xor EBP,DWORD PTR [ESI*4+L_45fc20]
          mov ESI,EDX
          shr ESI,16
          mov EAX,ESI
          movzx ESI,AL
          mov EAX,DWORD PTR [ESP+4]
          xor EBP,DWORD PTR [ESI*4+L_460020]
          xor EAX,EBP
          mov ESI,EBP
          mov DWORD PTR [ESP+4],EAX
          mov EAX,EBP
          shr ESI,24
          movzx EDI,AL
          mov EAX,EBP
          mov EDI,DWORD PTR [EDI*4+L_45cc20]
          xor EDI,DWORD PTR [ESI*4+L_45d820]
          movzx ESI,AH
          xor EBX,EDI
          xor EBX,DWORD PTR [ESI*4+L_45d020]
          shr EBP,16
          mov EAX,EBP
          mov EDI,DWORD PTR [ESP+8]
          xor EDI,DWORD PTR [ESP+4]
          movzx EBP,AL
          mov ESI,DWORD PTR [ESP+16]
          mov EAX,DWORD PTR [ESP]
          xor EBX,DWORD PTR [EBP*4+L_45d420]
          mov EBP,DWORD PTR [ESP+12]
          mov DWORD PTR [ESP+8],EDI
          xor EBP,EDI
          mov EDI,DWORD PTR [ESP+20]
          xor ECX,EBX
          mov DWORD PTR [EAX+120],EBX
          mov DWORD PTR [ESP+12],EBP
          xor ESI,ECX
          mov DWORD PTR [EAX+124],ECX
          mov DWORD PTR [EAX+128],ESI
          mov EAX,DWORD PTR [ESP+24]
          xor EDI,EBP
          mov EBP,DWORD PTR [ESP]
          mov DWORD PTR [ESP+16],ESI
          xor EAX,ESI
          mov DWORD PTR [EBP+132],EAX
          mov ESI,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+20],EDI
          mov DWORD PTR [ESP+24],EAX
          xor ESI,EDI
          mov EDI,DWORD PTR [ESP+32]
          xor EDX,ESI
          mov DWORD PTR [ESP+28],ESI
          movzx ESI,DL
          xor EDI,EAX
          mov EAX,EBP
          mov DWORD PTR [EBP+136],EDI
          mov EBP,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+32],EDI
          xor EBP,EDI
          mov DWORD PTR [EAX+140],EBP
          mov EAX,EDX
          mov DWORD PTR [ESP+36],EBP
          shr EAX,24
          mov EBP,DWORD PTR [EAX*4+L_460420]
          xor EBP,DWORD PTR [ESI*4+L_460820]
          movzx ESI,DH
          xor EBP,DWORD PTR [L_461c34]
          xor EBP,DWORD PTR [ESI*4+L_45fc20]
          mov ESI,EDX
          shr ESI,16
          mov EAX,ESI
          movzx ESI,AL
          mov EAX,DWORD PTR [ESP+4]
          xor EBP,DWORD PTR [ESI*4+L_460020]
          xor EAX,EBP
          mov DWORD PTR [ESP+4],EAX
          mov EAX,EBP
          movzx EDI,AL
          mov EAX,EBP
          shr EAX,24
          mov EDI,DWORD PTR [EDI*4+L_45cc20]
          xor EDI,DWORD PTR [EAX*4+L_45d820]
          mov EAX,EBP
          shr EBP,16
          movzx ESI,AH
          mov EAX,EBP
          movzx EBP,AL
          xor EBX,EDI
          xor EBX,DWORD PTR [ESI*4+L_45d020]
          mov ESI,DWORD PTR [ESP]
          xor EBX,DWORD PTR [EBP*4+L_45d420]
          mov EBP,ESI
          mov DWORD PTR [EBP+144],EBX
          mov EDI,EBX
          mov EBP,DWORD PTR [ESP+16]
          xor ECX,EDI
          mov EBX,DWORD PTR [ESP+8]
          xor EBX,DWORD PTR [ESP+4]
          mov EAX,ECX
          mov DWORD PTR [ESI+148],ECX
          mov ECX,DWORD PTR [ESP+12]
          xor EBP,EAX
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP],EBP
          mov EAX,DWORD PTR [ESP]
          mov EBP,ESI
          mov DWORD PTR [ESP+8],EBX
          xor ECX,EBX
          mov DWORD PTR [ESI+152],EAX
          mov ESI,DWORD PTR [ESP+20]
          mov EAX,DWORD PTR [ESP+24]
          xor EAX,DWORD PTR [ESP]
          mov DWORD PTR [ESP+16],ECX
          mov EBX,DWORD PTR [ESP+32]
          xor ESI,ECX
          mov ECX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+20],ESI
          mov DWORD PTR [EBP+156],EAX
          xor ECX,ESI
          xor EBX,EAX
          mov ESI,EBX
          mov DWORD PTR [EBP+160],EBX
          mov EBX,DWORD PTR [ESP+36]
          xor EDX,ECX
          mov DWORD PTR [ESP+24],ECX
          mov DWORD PTR [ESP+28],ESI
          mov ECX,EDX
          mov DWORD PTR [ESP+32],EDX
          xor EBX,ESI
          shr ECX,24
          mov ESI,DWORD PTR [ESP+4]
          mov DWORD PTR [ESP+36],EBX
          mov DWORD PTR [EBP+164],EBX
          movzx EBX,DL
          mov ECX,DWORD PTR [ECX*4+L_460420]
          xor ECX,DWORD PTR [EBX*4+L_460820]
          movzx EBX,DH
          xor ECX,DWORD PTR [L_461c38]
          xor ECX,DWORD PTR [EBX*4+L_45fc20]
          mov EBX,EDX
          shr EBX,16
          movzx EBX,BL
          xor ECX,DWORD PTR [EBX*4+L_460020]
          xor ESI,ECX
          mov EDX,ECX
          mov EBX,ESI
          shr EDX,24
          movzx ESI,CL
          mov ESI,DWORD PTR [ESI*4+L_45cc20]
          xor ESI,DWORD PTR [EDX*4+L_45d820]
          xor EDI,ESI
          movzx ESI,CH
          shr ECX,16
          xor EDI,DWORD PTR [ESI*4+L_45d020]
          movzx ECX,CL
          mov ESI,DWORD PTR [ESP+16]
          mov EDX,DWORD PTR [ECX*4+L_45d420]
          xor EDX,EDI
          mov EDI,DWORD PTR [ESP+8]
          mov ECX,EDX
          mov EDX,EBP
          mov DWORD PTR [EBP+168],ECX
          xor ECX,DWORD PTR [ESP+12]
          xor EDI,EBX
          xor ESI,EDI
          mov DWORD PTR [EBP+172],ECX
          xor ECX,DWORD PTR [ESP]
          mov DWORD PTR [EBP+176],ECX
          xor ECX,EAX
          mov EBP,DWORD PTR [ESP+20]
          mov DWORD PTR [EDX+180],ECX
          xor ECX,DWORD PTR [ESP+28]
          mov EAX,EDX
          xor EBX,DWORD PTR [L_461c3c]
          xor EBP,ESI
          mov DWORD PTR [EDX+184],ECX
          mov EDX,DWORD PTR [ESP+32]
          xor EDX,DWORD PTR [ESP+24]
          xor ECX,DWORD PTR [ESP+36]
          mov DWORD PTR [EAX+240],0
          mov BYTE PTR [EAX+240],192
          xor EDX,EBP
          mov DWORD PTR [EAX+188],ECX
          mov ECX,EDX
          shr ECX,24
          xor EBX,DWORD PTR [ECX*4+L_460420]
          movzx ECX,DL
          xor EBX,DWORD PTR [ECX*4+L_460820]
          movzx ECX,DH
          xor EBX,DWORD PTR [ECX*4+L_45fc20]
          shr EDX,16
          movzx EDX,DL
          xor EBX,DWORD PTR [EDX*4+L_460020]
          xor EDI,EBX
          mov DWORD PTR [EAX+192],EBX
          xor ESI,EDI
          mov DWORD PTR [EAX+196],EDI
          mov DWORD PTR [EAX+200],ESI
          xor ESI,EBP
          mov DWORD PTR [EAX+204],ESI
          add ESP,44
          xor EAX,EAX
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
L_43d9a0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,64
          mov ECX,DWORD PTR [ESP+84]
          mov EAX,DWORD PTR [ESP+88]
          mov EDX,DWORD PTR [ECX]
          mov DWORD PTR [EAX],EDX
          mov EDI,DWORD PTR [ECX+4]
          mov DWORD PTR [ESP],EDX
          mov DWORD PTR [EAX+4],EDI
          mov EDX,DWORD PTR [ECX+8]
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [EAX+8],EDX
          mov ESI,DWORD PTR [ECX+12]
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [EAX+12],ESI
          mov EBP,DWORD PTR [ECX+16]
          mov DWORD PTR [ESP+12],ESI
          mov EDX,EBP
          shr EBP,24
          movzx EBX,DL
          movzx ESI,DH
          mov DWORD PTR [ESP+16],EDX
          mov EBX,DWORD PTR [EBX*4+L_45cc20]
          xor EBX,DWORD PTR [EBP*4+L_45d820]
          mov EBP,EDX
          shr EBP,16
          xor EBX,DWORD PTR [ESI*4+L_45d020]
          mov EDX,EBP
          movzx ESI,DL
          xor EBX,DWORD PTR [ESI*4+L_45d420]
          mov DWORD PTR [EAX+16],EBX
          mov EBP,DWORD PTR [ECX+20]
          mov EDX,EBP
          shr EBP,24
          movzx EBX,DL
          movzx ESI,DH
          mov DWORD PTR [ESP+20],EDX
          mov EBX,DWORD PTR [EBX*4+L_45cc20]
          xor EBX,DWORD PTR [EBP*4+L_45d820]
          xor EBX,DWORD PTR [ESI*4+L_45d020]
          mov ESI,EDX
          shr ESI,16
          mov EDX,ESI
          movzx ESI,DL
          xor EBX,DWORD PTR [ESI*4+L_45d420]
          mov DWORD PTR [EAX+20],EBX
          mov EBP,DWORD PTR [ECX+24]
          mov EDX,EBP
          shr EBP,24
          movzx EBX,DL
          movzx ESI,DH
          mov DWORD PTR [ESP+24],EDX
          mov EBX,DWORD PTR [EBX*4+L_45cc20]
          xor EBX,DWORD PTR [EBP*4+L_45d820]
          mov EBP,EDX
          shr EBP,16
          xor EBX,DWORD PTR [ESI*4+L_45d020]
          mov EDX,EBP
          movzx ESI,DL
          mov EDX,DWORD PTR [ESP]
          xor EDX,DWORD PTR [L_461c20]
          xor EBX,DWORD PTR [ESI*4+L_45d420]
          mov DWORD PTR [EAX+24],EBX
          mov ECX,DWORD PTR [ECX+28]
          mov EBP,ECX
          movzx EDI,CL
          mov EBX,ECX
          shr EBP,24
          movzx ESI,CH
          mov DWORD PTR [ESP+28],ECX
          xor EDX,DWORD PTR [EBP*4+L_460420]
          mov ECX,DWORD PTR [EDI*4+L_45cc20]
          shr EBX,16
          xor ECX,DWORD PTR [EBP*4+L_45d820]
          xor EDX,DWORD PTR [EDI*4+L_460820]
          movzx EBX,BL
          xor EDX,DWORD PTR [ESI*4+L_45fc20]
          xor ECX,DWORD PTR [ESI*4+L_45d020]
          xor ECX,DWORD PTR [EBX*4+L_45d420]
          mov ESI,DWORD PTR [EBX*4+L_460020]
          xor ESI,EDX
          mov DWORD PTR [EAX+28],ECX
          mov ECX,ESI
          mov EBP,ESI
          movzx ECX,CL
          shr EBP,24
          mov EDI,ESI
          mov EBX,DWORD PTR [ECX*4+L_45cc20]
          mov ECX,ESI
          xor EBX,DWORD PTR [EBP*4+L_45d820]
          movzx EDX,CH
          shr EDI,16
          mov DWORD PTR [ESP],ESI
          xor EBX,DWORD PTR [EDX*4+L_45d020]
          mov EDX,EDI
          movzx EDX,DL
          xor EBX,DWORD PTR [EDX*4+L_45d420]
          mov DWORD PTR [ESP+32],EBX
          mov DWORD PTR [EAX+32],EBX
          mov EBX,DWORD PTR [ESP+4]
          xor EBX,ESI
          mov ESI,EBX
          movzx ECX,BL
          movzx EDX,BH
          shr ESI,24
          mov EBP,DWORD PTR [ECX*4+L_45cc20]
          xor EBP,DWORD PTR [ESI*4+L_45d820]
          mov ESI,EBX
          shr ESI,16
          xor EBP,DWORD PTR [EDX*4+L_45d020]
          mov EDX,ESI
          movzx EDX,DL
          xor EBP,DWORD PTR [EDX*4+L_45d420]
          mov DWORD PTR [ESP+36],EBP
          mov EDI,DWORD PTR [ESP+8]
          mov DWORD PTR [ESP+4],EBX
          mov ESI,DWORD PTR [ESP+12]
          mov DWORD PTR [EAX+36],EBP
          xor EDI,EBX
          mov EBX,EDI
          shr EDI,24
          movzx ECX,BL
          movzx EDX,BH
          xor ESI,EBX
          mov EBP,DWORD PTR [ECX*4+L_45cc20]
          mov ECX,EBX
          xor EBP,DWORD PTR [EDI*4+L_45d820]
          shr ECX,16
          xor EBP,DWORD PTR [EDX*4+L_45d020]
          mov DWORD PTR [ESP+8],EBX
          movzx EDX,CL
          mov EBX,ESI
          shr ESI,16
          mov ECX,DWORD PTR [EDX*4+L_45d420]
          mov EDX,ESI
          mov ESI,EBX
          shr ESI,24
          movzx EDI,BL
          mov DWORD PTR [ESP+12],EBX
          movzx EDX,DL
          xor ECX,EBP
          add EDX,512
          mov DWORD PTR [ESP+40],ECX
          mov DWORD PTR [EAX+40],ECX
          movzx ECX,BH
          mov EBX,ESI
          add ECX,256
          mov ESI,DWORD PTR [EDI*4+L_45cc20]
          add EBX,768
          xor ESI,DWORD PTR [EBX*4+L_45cc20]
          xor ESI,DWORD PTR [ECX*4+L_45cc20]
          xor ESI,DWORD PTR [EDX*4+L_45cc20]
          mov DWORD PTR [ESP+44],ESI
          mov DWORD PTR [EAX+44],ESI
          mov ESI,DWORD PTR [EDI*4+L_45fc20]
          xor ESI,DWORD PTR [EBX*4+L_45fc20]
          xor ESI,DWORD PTR [ESP+16]
          mov EDI,DWORD PTR [EDX*4+L_45fc20]
          xor ESI,DWORD PTR [ECX*4+L_45fc20]
          xor EDI,ESI
          mov ECX,EDI
          mov EDX,EDI
          movzx ECX,CL
          shr EDX,24
          mov ESI,DWORD PTR [ECX*4+L_45cc20]
          mov ECX,EDI
          xor ESI,DWORD PTR [EDX*4+L_45d820]
          movzx EDX,CH
          xor ESI,DWORD PTR [EDX*4+L_45d020]
          mov EDX,EDI
          shr EDX,16
          movzx EDX,DL
          mov EBP,DWORD PTR [EDX*4+L_45d420]
          mov EDX,DWORD PTR [ESP+20]
          xor EDX,EDI
          xor EBP,ESI
          mov EBX,EDX
          mov DWORD PTR [ESP+16],EBP
          mov DWORD PTR [EAX+48],EBP
          mov EBP,EBX
          movzx EDX,DL
          movzx ECX,BH
          shr EBP,24
          mov EDX,DWORD PTR [EDX*4+L_45cc20]
          mov ESI,EBX
          xor EDX,DWORD PTR [EBP*4+L_45d820]
          xor EDX,DWORD PTR [ECX*4+L_45d020]
          shr ESI,16
          mov DWORD PTR [ESP+20],EBX
          mov ECX,ESI
          movzx ECX,CL
          mov ESI,DWORD PTR [ECX*4+L_45d420]
          xor ESI,EDX
          mov EDX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP+48],ESI
          mov DWORD PTR [EAX+52],ESI
          xor EDX,EBX
          mov ESI,EDX
          movzx EBX,DL
          shr EDX,24
          mov EBP,DWORD PTR [EBX*4+L_45cc20]
          xor EBP,DWORD PTR [EDX*4+L_45d820]
          mov EDX,ESI
          movzx ECX,DH
          shr EDX,16
          mov DWORD PTR [ESP+24],ESI
          xor EBP,DWORD PTR [ECX*4+L_45d020]
          movzx ECX,DL
          mov EDX,DWORD PTR [ECX*4+L_45d420]
          mov ECX,DWORD PTR [ESP+28]
          xor EDX,EBP
          xor ECX,ESI
          mov DWORD PTR [ESP+52],EDX
          mov DWORD PTR [EAX+56],EDX
          mov EDX,ECX
          shr EDX,24
          movzx EBP,CL
          mov EBX,ECX
          movzx ESI,CH
          mov DWORD PTR [ESP+28],ECX
          shr EBX,16
          mov ECX,DWORD PTR [EBP*4+L_45cc20]
          xor ECX,DWORD PTR [EDX*4+L_45d820]
          movzx EBX,BL
          xor ECX,DWORD PTR [ESI*4+L_45d020]
          mov DWORD PTR [ESP+56],EDX
          mov EDX,DWORD PTR [EBX*4+L_45d420]
          xor EDX,ECX
          mov ECX,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP+60],EDX
          mov DWORD PTR [EAX+60],EDX
          mov EDX,DWORD PTR [ESP]
          mov ECX,DWORD PTR [ECX*4+L_460420]
          xor ECX,DWORD PTR [EBP*4+L_460820]
          xor ECX,DWORD PTR [L_461c24]
          xor ECX,DWORD PTR [ESI*4+L_45fc20]
          xor ECX,DWORD PTR [EBX*4+L_460020]
          mov EBP,ECX
          movzx EBX,CL
          xor EDX,ECX
          shr EBP,24
          mov EBX,DWORD PTR [EBX*4+L_45cc20]
          movzx ESI,CH
          xor EBX,DWORD PTR [EBP*4+L_45d820]
          shr ECX,16
          xor EBX,DWORD PTR [ESP+32]
          movzx ECX,CL
          xor EBX,DWORD PTR [ESI*4+L_45d020]
          mov ESI,DWORD PTR [ESP+36]
          xor EBX,DWORD PTR [ECX*4+L_45d420]
          mov ECX,DWORD PTR [ESP+8]
          mov EBP,EBX
          mov DWORD PTR [EAX+64],EBX
          mov EBX,DWORD PTR [ESP+4]
          mov DWORD PTR [ESP+4],EDX
          xor ESI,EBP
          mov DWORD PTR [EAX+68],ESI
          mov DWORD PTR [ESP+32],ESI
          xor EBX,EDX
          xor ECX,EBX
          mov DWORD PTR [ESP+8],EBX
          mov EDX,ECX
          mov ECX,DWORD PTR [ESP+40]
          xor ECX,ESI
          mov ESI,DWORD PTR [ESP+12]
          mov DWORD PTR [ESP+12],EDX
          mov EBX,ECX
          mov DWORD PTR [EAX+72],ECX
          mov DWORD PTR [ESP+36],EBX
          xor ESI,EDX
          mov ECX,ESI
          mov ESI,DWORD PTR [ESP+44]
          xor ESI,EBX
          movzx EBX,CL
          mov DWORD PTR [ESP+40],ESI
          mov DWORD PTR [EAX+76],ESI
          mov ESI,ECX
          shr ESI,24
          mov EBX,DWORD PTR [EBX*4+L_45fc20]
          xor EBX,DWORD PTR [ESI*4+L_460820]
          movzx ESI,CH
          xor EBX,DWORD PTR [ESI*4+L_460020]
          mov ESI,ECX
          shr ESI,16
          mov EDX,ESI
          movzx ESI,DL
          xor EBX,DWORD PTR [ESI*4+L_460420]
          xor EDI,EBX
          movzx ESI,BL
          mov EDX,EDI
          mov EDI,EBX
          mov ESI,DWORD PTR [ESI*4+L_45cc20]
          shr EDI,24
          xor ESI,DWORD PTR [EDI*4+L_45d820]
          movzx EDI,BH
          shr EBX,16
          xor ESI,DWORD PTR [ESP+16]
          movzx EBX,BL
          mov DWORD PTR [ESP+16],EDX
          xor ESI,DWORD PTR [EDI*4+L_45d020]
          mov EDI,DWORD PTR [EBX*4+L_45d420]
          xor EDI,ESI
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [EAX+80],EDI
          mov EDI,DWORD PTR [ESP+20]
          xor EDI,EDX
          mov ESI,EDI
          mov EDI,DWORD PTR [ESP+48]
          xor EDI,DWORD PTR [ESP]
          mov EBX,DWORD PTR [ESP+24]
          mov EDX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+20],ESI
          xor EBX,ESI
          mov ESI,DWORD PTR [ESP+28]
          xor EDX,EDI
          mov DWORD PTR [EAX+84],EDI
          mov DWORD PTR [ESP+24],EDI
          mov EDI,DWORD PTR [ESP+60]
          mov DWORD PTR [EAX+88],EDX
          xor ESI,EBX
          mov DWORD PTR [ESP+44],EDX
          mov DWORD PTR [ESP+28],EBX
          xor EDI,EDX
          mov EDX,ESI
          shr EDX,24
          mov DWORD PTR [ESP+52],EDI
          mov DWORD PTR [EAX+92],EDI
          mov EBX,EDX
          mov EDX,ESI
          mov EDI,ESI
          movzx ESI,DL
          mov EBX,DWORD PTR [EBX*4+L_460420]
          mov EDX,EDI
          xor EBX,DWORD PTR [ESI*4+L_460820]
          movzx ESI,DH
          shr EDX,16
          xor EBX,DWORD PTR [L_461c28]
          mov DWORD PTR [ESP+48],EDI
          xor EBX,DWORD PTR [ESI*4+L_45fc20]
          movzx ESI,DL
          mov EDX,DWORD PTR [ESP+4]
          xor EBX,DWORD PTR [ESI*4+L_460020]
          mov EDI,EBX
          movzx ESI,BL
          xor EDX,EBX
          shr EDI,24
          mov ESI,DWORD PTR [ESI*4+L_45cc20]
          mov DWORD PTR [ESP+4],EDX
          xor ESI,DWORD PTR [EDI*4+L_45d820]
          mov EDI,DWORD PTR [ESP+12]
          xor EBP,ESI
          movzx ESI,BH
          shr EBX,16
          xor EBP,DWORD PTR [ESI*4+L_45d020]
          movzx EBX,BL
          mov ESI,DWORD PTR [ESP+32]
          xor EBP,DWORD PTR [EBX*4+L_45d420]
          mov EBX,DWORD PTR [ESP+8]
          xor EBX,EDX
          mov DWORD PTR [ESP+8],EBX
          xor ESI,EBP
          xor EDI,EBX
          mov EBX,DWORD PTR [ESP+36]
          mov DWORD PTR [EAX+96],EBP
          xor ECX,EDI
          mov DWORD PTR [EAX+100],ESI
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+32],EDI
          xor EBX,ESI
          mov ESI,DWORD PTR [ESP+40]
          mov DWORD PTR [EAX+104],EBX
          mov DWORD PTR [ESP+36],EBX
          xor ESI,EBX
          movzx EBX,CL
          mov DWORD PTR [ESP+40],ESI
          mov DWORD PTR [EAX+108],ESI
          mov ESI,ECX
          shr ESI,24
          mov EBX,DWORD PTR [EBX*4+L_45fc20]
          xor EBX,DWORD PTR [ESI*4+L_460820]
          movzx ESI,CH
          xor EBX,DWORD PTR [ESI*4+L_460020]
          mov ESI,ECX
          shr ESI,16
          mov EDX,ESI
          movzx ESI,DL
          mov EDX,DWORD PTR [ESP+16]
          xor EBX,DWORD PTR [ESI*4+L_460420]
          mov EDI,EBX
          movzx ESI,BL
          xor EDX,EBX
          shr EDI,24
          mov ESI,DWORD PTR [ESI*4+L_45cc20]
          mov DWORD PTR [ESP+16],EDX
          xor ESI,DWORD PTR [EDI*4+L_45d820]
          movzx EDI,BH
          shr EBX,16
          xor ESI,DWORD PTR [ESP]
          movzx EBX,BL
          xor ESI,DWORD PTR [EDI*4+L_45d020]
          mov EDI,DWORD PTR [ESP+24]
          xor ESI,DWORD PTR [EBX*4+L_45d420]
          mov EBX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [EAX+112],ESI
          mov ESI,DWORD PTR [ESP+20]
          xor EDI,DWORD PTR [ESP]
          xor ESI,EDX
          mov EDX,DWORD PTR [ESP+44]
          mov DWORD PTR [EAX+116],EDI
          mov DWORD PTR [ESP+24],EDI
          xor EBX,ESI
          mov DWORD PTR [ESP+20],ESI
          mov DWORD PTR [ESP+28],EBX
          xor EDX,EDI
          mov EDI,DWORD PTR [ESP+48]
          mov DWORD PTR [EAX+120],EDX
          mov DWORD PTR [ESP+44],EDX
          xor EDI,EBX
          mov ESI,EDI
          mov EDI,DWORD PTR [ESP+52]
          xor EDI,EDX
          mov EDX,ESI
          shr EDX,24
          mov DWORD PTR [ESP+52],EDI
          mov DWORD PTR [EAX+124],EDI
          mov EBX,EDX
          mov EDX,ESI
          mov EDI,ESI
          movzx ESI,DL
          mov EBX,DWORD PTR [EBX*4+L_460420]
          mov EDX,EDI
          xor EBX,DWORD PTR [ESI*4+L_460820]
          movzx ESI,DH
          mov DWORD PTR [ESP+48],EDI
          xor EBX,DWORD PTR [L_461c2c]
          xor EBX,DWORD PTR [ESI*4+L_45fc20]
          mov ESI,EDI
          shr ESI,16
          mov EDX,ESI
          movzx ESI,DL
          mov EDX,DWORD PTR [ESP+4]
          xor EBX,DWORD PTR [ESI*4+L_460020]
          mov EDI,EBX
          movzx ESI,BL
          xor EDX,EBX
          shr EDI,24
          mov ESI,DWORD PTR [ESI*4+L_45cc20]
          mov DWORD PTR [ESP+4],EDX
          xor ESI,DWORD PTR [EDI*4+L_45d820]
          mov EDI,DWORD PTR [ESP+32]
          xor EBP,ESI
          movzx ESI,BH
          shr EBX,16
          xor EBP,DWORD PTR [ESI*4+L_45d020]
          movzx EBX,BL
          mov ESI,DWORD PTR [ESP+12]
          xor EBP,DWORD PTR [EBX*4+L_45d420]
          mov EBX,DWORD PTR [ESP+8]
          xor EBX,EDX
          xor EDI,EBX
          mov DWORD PTR [ESP+8],EBX
          mov EBX,DWORD PTR [ESP+36]
          xor ESI,EBP
          xor ECX,EDI
          mov DWORD PTR [ESP+32],EDI
          mov DWORD PTR [EAX+132],ESI
          mov DWORD PTR [ESP+12],ESI
          xor EBX,ESI
          mov ESI,DWORD PTR [ESP+40]
          mov DWORD PTR [EAX+128],EBP
          mov DWORD PTR [EAX+136],EBX
          mov DWORD PTR [ESP+36],EBX
          xor ESI,EBX
          movzx EBX,CL
          mov DWORD PTR [ESP+40],ESI
          mov DWORD PTR [EAX+140],ESI
          mov ESI,ECX
          shr ESI,24
          mov EBX,DWORD PTR [EBX*4+L_45fc20]
          xor EBX,DWORD PTR [ESI*4+L_460820]
          movzx ESI,CH
          xor EBX,DWORD PTR [ESI*4+L_460020]
          mov ESI,ECX
          shr ESI,16
          mov EDX,ESI
          movzx ESI,DL
          mov EDX,DWORD PTR [ESP+16]
          xor EBX,DWORD PTR [ESI*4+L_460420]
          mov EDI,EBX
          movzx ESI,BL
          xor EDX,EBX
          shr EDI,24
          mov ESI,DWORD PTR [ESI*4+L_45cc20]
          mov DWORD PTR [ESP+16],EDX
          xor ESI,DWORD PTR [EDI*4+L_45d820]
          movzx EDI,BH
          shr EBX,16
          xor ESI,DWORD PTR [ESP]
          movzx EBX,BL
          xor ESI,DWORD PTR [EDI*4+L_45d020]
          mov EDI,DWORD PTR [ESP+24]
          xor ESI,DWORD PTR [EBX*4+L_45d420]
          mov EBX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [EAX+144],ESI
          mov ESI,DWORD PTR [ESP+20]
          xor EDI,DWORD PTR [ESP]
          xor ESI,EDX
          mov EDX,DWORD PTR [ESP+44]
          mov DWORD PTR [EAX+148],EDI
          mov DWORD PTR [ESP+24],EDI
          xor EBX,ESI
          mov DWORD PTR [ESP+20],ESI
          mov DWORD PTR [ESP+28],EBX
          xor EDX,EDI
          mov EDI,DWORD PTR [ESP+48]
          mov DWORD PTR [EAX+152],EDX
          mov DWORD PTR [ESP+44],EDX
          xor EDI,EBX
          mov ESI,EDI
          mov EDI,DWORD PTR [ESP+52]
          xor EDI,EDX
          mov EDX,ESI
          mov DWORD PTR [ESP+52],EDI
          mov DWORD PTR [EAX+156],EDI
          mov EDI,ESI
          shr EDI,24
          movzx ESI,DL
          mov DWORD PTR [ESP+48],EDX
          mov EBX,DWORD PTR [EDI*4+L_460420]
          xor EBX,DWORD PTR [ESI*4+L_460820]
          mov EDI,EDX
          xor EBX,DWORD PTR [L_461c30]
          movzx ESI,DH
          xor EBX,DWORD PTR [ESI*4+L_45fc20]
          shr EDI,16
          mov EDX,EDI
          movzx ESI,DL
          mov EDX,DWORD PTR [ESP+4]
          xor EBX,DWORD PTR [ESI*4+L_460020]
          mov EDI,EBX
          movzx ESI,BL
          xor EDX,EBX
          shr EDI,24
          mov ESI,DWORD PTR [ESI*4+L_45cc20]
          xor ESI,DWORD PTR [EDI*4+L_45d820]
          xor EBP,ESI
          movzx ESI,BH
          shr EBX,16
          xor EBP,DWORD PTR [ESI*4+L_45d020]
          movzx EBX,BL
          mov ESI,DWORD PTR [ESP+12]
          xor EBP,DWORD PTR [EBX*4+L_45d420]
          mov EBX,DWORD PTR [ESP+8]
          xor EBX,EDX
          mov EDI,EBP
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [EAX+160],EBP
          xor ESI,EDI
          mov DWORD PTR [ESP+8],EDI
          mov EDI,DWORD PTR [ESP+32]
          mov EBP,EDX
          mov EDX,DWORD PTR [ESP+40]
          mov DWORD PTR [EAX+164],ESI
          mov DWORD PTR [ESP+32],ESI
          xor EDI,EBX
          mov EBX,DWORD PTR [ESP+36]
          xor ECX,EDI
          mov DWORD PTR [ESP+36],EDI
          xor EBX,ESI
          mov ESI,ECX
          xor EDX,EBX
          mov DWORD PTR [EAX+168],EBX
          mov DWORD PTR [ESP+40],EBX
          shr ESI,24
          movzx EBX,CL
          mov DWORD PTR [ESP+56],EDX
          mov EBX,DWORD PTR [EBX*4+L_45fc20]
          xor EBX,DWORD PTR [ESI*4+L_460820]
          movzx ESI,CH
          xor EBX,DWORD PTR [ESI*4+L_460020]
          mov ESI,ECX
          mov DWORD PTR [EAX+172],EDX
          shr ESI,16
          mov EDX,ESI
          movzx ESI,DL
          mov EDX,DWORD PTR [ESP+16]
          xor EBX,DWORD PTR [ESI*4+L_460420]
          xor EDX,EBX
          movzx ESI,BL
          movzx EDI,BH
          mov DWORD PTR [ESP+4],EDX
          mov EDX,EBX
          mov ESI,DWORD PTR [ESI*4+L_45cc20]
          shr EDX,24
          shr EBX,16
          xor ESI,DWORD PTR [EDX*4+L_45d820]
          movzx EBX,BL
          xor ESI,DWORD PTR [ESP]
          mov EDX,DWORD PTR [EBX*4+L_45d420]
          xor ESI,DWORD PTR [EDI*4+L_45d020]
          mov EDI,DWORD PTR [ESP+24]
          xor EDX,ESI
          mov EBX,EDX
          mov DWORD PTR [EAX+176],EDX
          mov EDX,DWORD PTR [ESP+20]
          xor EDX,DWORD PTR [ESP+4]
          mov DWORD PTR [ESP],EBX
          xor EDI,EBX
          mov ESI,DWORD PTR [ESP+28]
          mov EBX,DWORD PTR [ESP+48]
          mov DWORD PTR [EAX+180],EDI
          mov DWORD PTR [ESP+20],EDI
          xor ESI,EDX
          mov DWORD PTR [ESP+16],EDX
          mov EDX,DWORD PTR [ESP+44]
          xor EBX,ESI
          mov DWORD PTR [ESP+24],ESI
          mov ESI,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+44],EBX
          xor EDX,EDI
          mov EDI,EBX
          xor ESI,EDX
          shr EDI,24
          mov DWORD PTR [EAX+184],EDX
          mov DWORD PTR [ESP+28],EDX
          mov DWORD PTR [ESP+48],ESI
          mov DWORD PTR [EAX+188],ESI
          mov EDX,DWORD PTR [EDI*4+L_460420]
          movzx ESI,BL
          mov EDI,EBX
          xor EDX,DWORD PTR [ESI*4+L_460820]
          movzx ESI,BH
          shr EDI,16
          xor EDX,DWORD PTR [L_461c34]
          mov EBX,EDI
          xor EDX,DWORD PTR [ESI*4+L_45fc20]
          mov EDI,EBP
          movzx ESI,BL
          xor EDX,DWORD PTR [ESI*4+L_460020]
          mov EBP,EDX
          xor EDI,EDX
          shr EBP,24
          mov EBX,EDI
          movzx EDI,DL
          mov ESI,EBP
          mov EBP,DWORD PTR [EDI*4+L_45cc20]
          mov EDI,DWORD PTR [ESP+36]
          xor EBP,DWORD PTR [ESI*4+L_45d820]
          movzx ESI,DH
          shr EDX,16
          xor EBP,DWORD PTR [ESP+8]
          movzx EDX,DL
          mov DWORD PTR [ESP+8],EBX
          xor EBP,DWORD PTR [ESI*4+L_45d020]
          mov ESI,DWORD PTR [ESP+12]
          xor EBP,DWORD PTR [EDX*4+L_45d420]
          xor ESI,EBX
          mov DWORD PTR [ESP+12],ESI
          xor EDI,ESI
          mov DWORD PTR [EAX+192],EBP
          xor EBP,DWORD PTR [ESP+32]
          xor ECX,EDI
          movzx ESI,CL
          movzx EDX,CH
          mov DWORD PTR [EAX+196],EBP
          xor EBP,DWORD PTR [ESP+40]
          mov DWORD PTR [EAX+200],EBP
          xor EBP,DWORD PTR [ESP+56]
          mov ESI,DWORD PTR [ESI*4+L_45fc20]
          mov DWORD PTR [EAX+204],EBP
          mov EBP,ECX
          shr EBP,24
          xor ESI,DWORD PTR [EBP*4+L_460820]
          mov EBP,ECX
          shr EBP,16
          xor ESI,DWORD PTR [EDX*4+L_460020]
          mov EDX,EBP
          movzx EDX,DL
          xor ESI,DWORD PTR [EDX*4+L_460420]
          mov EDX,ESI
          mov EBP,ESI
          mov EBX,ESI
          shr EBP,24
          movzx EDX,DL
          mov EDX,DWORD PTR [EDX*4+L_45cc20]
          xor EDX,DWORD PTR [EBP*4+L_45d820]
          movzx EBP,BH
          xor EDX,DWORD PTR [ESP]
          xor EDX,DWORD PTR [EBP*4+L_45d020]
          mov EBP,ESI
          shr EBP,16
          mov EBX,EBP
          movzx EBP,BL
          mov EBX,DWORD PTR [EBP*4+L_45d420]
          xor EBX,EDX
          mov EDX,DWORD PTR [ESP+24]
          mov EBP,EBX
          xor EBP,DWORD PTR [ESP+20]
          mov DWORD PTR [EAX+208],EBX
          mov EBX,DWORD PTR [ESP+4]
          mov DWORD PTR [EAX+212],EBP
          xor EBP,DWORD PTR [ESP+28]
          xor EBX,DWORD PTR [ESP+16]
          mov DWORD PTR [EAX+216],EBP
          xor EBP,DWORD PTR [ESP+48]
          xor EDX,EBX
          mov EBX,DWORD PTR [ESP+44]
          xor EBX,EDX
          mov DWORD PTR [EAX+220],EBP
          mov EBP,DWORD PTR [ESP+8]
          xor EBX,ESI
          xor EBP,DWORD PTR [L_461c38]
          mov EDX,EBX
          shr EDX,24
          xor EBP,DWORD PTR [EDX*4+L_460420]
          movzx EDX,BL
          xor EBP,DWORD PTR [EDX*4+L_460820]
          movzx EDX,BH
          shr EBX,16
          xor EBP,DWORD PTR [EDX*4+L_45fc20]
          movzx EBX,BL
          xor EBP,DWORD PTR [EBX*4+L_460020]
          mov DWORD PTR [EAX+224],EBP
          xor EBP,DWORD PTR [ESP+12]
          xor EDI,EBP
          mov DWORD PTR [EAX+228],EBP
          xor ECX,EDI
          mov DWORD PTR [EAX+232],EDI
          mov DWORD PTR [EAX+236],ECX
          mov DWORD PTR [EAX+240],0
          mov BYTE PTR [EAX+240],224
          add ESP,64
          xor EAX,EAX
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
FUN_43e4e0:
          mov EAX,DWORD PTR [ESP+8]
          mov EDX,DWORD PTR [ESP+4]
          mov ECX,DWORD PTR [ESP+12]
          cmp EAX,32
          je L_43e540
          jle L_43e510
          cmp EAX,192
          je L_43e51a
          cmp EAX,256
          je L_43e540
          add EAX,-128
          je L_43e530
L_43e506:
          mov EAX,1
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_43e510:
          cmp EAX,16
          je L_43e530
          cmp EAX,24
          jne L_43e506
L_43e51a:
          mov DWORD PTR [ESP+8],ECX
          mov DWORD PTR [ESP+4],EDX
          jmp L_43d150
L_43e527:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_43e530:
          mov DWORD PTR [ESP+8],ECX
          mov DWORD PTR [ESP+4],EDX
          jmp L_43cae0
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_43e540:
          mov DWORD PTR [ESP+8],ECX
          mov DWORD PTR [ESP+4],EDX
          jmp L_43d9a0
          .byte 0x90
          .byte 0x90
          .byte 0x90

.section .rdata,"dr"
.p2align 5
L_461c20:
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_461c24:
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_461c28:
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_461c2c:
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_461c30:
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_461c34:
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_461c38:
          .byte 0x40
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_461c3c:
          .byte 0x80
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_461c40:
          .byte 0x1b
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_461c44:
          .byte 0x36
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0

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
          .byte 0x34
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_43bae0 - .
          .byte 0x60
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
          .byte 0x3
          .byte 0x58
          .byte 0x3
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
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_43be40 - .
          .byte 0x66
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
          .byte 0x1c
          .byte 0x3
          .byte 0x5a
          .byte 0x3
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
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x94
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_43c1b0 - .
          .byte 0x3b
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
          .byte 0x28
          .byte 0x3
          .byte 0x2d
          .byte 0x5
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
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x7c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_43c6f0 - .
          .byte 0xe4
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
          .byte 0x1c
          .byte 0x75
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
          .byte 0x4b
          .byte 0xb
          .byte 0x3
          .byte 0x60
          .byte 0x3
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
          .byte 0x4c
          .byte 0xb
          .byte 0x4b
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
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x54
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long L_43cae0 - .
          .byte 0x6e
          .byte 0x6
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
          .byte 0x2c
          .byte 0x3
          .byte 0x60
          .byte 0x6
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
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x94
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long L_43d150 - .
          .byte 0x48
          .byte 0x8
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
          .byte 0x3a
          .byte 0x8
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
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd4
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long L_43d9a0 - .
          .byte 0x33
          .byte 0xb
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
          .byte 0x54
          .byte 0x3
          .byte 0x25
          .byte 0xb
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
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x14
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long FUN_43e4e0 - .
          .byte 0x6d
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0

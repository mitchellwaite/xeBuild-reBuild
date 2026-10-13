# crypto/md5_dgst.s -- MD5 init/block/update/final
#
# original placement:
#   .eh_frame      0046da18-0046db18
#   .rdata$zzz     00464170-0046419c
#   .text          00444fb0-00445a50

.intel_syntax noprefix
.globl FUN_445690
.globl FUN_4456c0
.globl FUN_445830

.text
.p2align 4
FUN_444fb0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,24
          mov EDI,DWORD PTR [EAX+8]
          mov DWORD PTR [ESP+20],EAX
          mov DWORD PTR [ESP+16],ECX
          mov DWORD PTR [ESP+12],EDI
          mov EDI,DWORD PTR [EAX+12]
          mov DWORD PTR [ESP],EDI
          mov EDI,DWORD PTR [EAX+16]
          mov EAX,DWORD PTR [EAX+20]
          mov DWORD PTR [ESP+4],EDI
          mov EDI,EDX
          mov DWORD PTR [ESP+8],EAX
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_444fe0:
          mov ESI,DWORD PTR [EDI]
          mov EAX,DWORD PTR [ESP+12]
          mov ECX,DWORD PTR [ESP+4]
          mov EBX,DWORD PTR [ESP+8]
          mov EBP,DWORD PTR [EDI+16]
          lea EDX,DWORD PTR [EAX+ESI*1-680876936]
          mov ESI,DWORD PTR [ESP]
          mov EAX,ECX
          xor EAX,EBX
          and EAX,ESI
          xor EAX,EBX
          add EAX,EDX
          mov EDX,DWORD PTR [EDI+4]
          rol EAX,7
          add EAX,ESI
          lea EDX,DWORD PTR [EBX+EDX*1-389564586]
          mov EBX,ESI
          xor EBX,ECX
          and EBX,EAX
          xor EBX,ECX
          add EBX,EDX
          mov EDX,DWORD PTR [EDI+8]
          rol EBX,12
          add EBX,EAX
          lea EDX,DWORD PTR [ECX+EDX*1+606105819]
          mov ECX,ESI
          xor ECX,EAX
          and ECX,EBX
          xor ECX,ESI
          add ECX,EDX
          mov EDX,DWORD PTR [EDI+12]
          ror ECX,15
          add ECX,EBX
          lea ESI,DWORD PTR [ESI+EDX*1-1044525330]
          mov EDX,EAX
          xor EDX,EBX
          and EDX,ECX
          xor EDX,EAX
          add EDX,ESI
          lea ESI,DWORD PTR [EAX+EBP*1-176418897]
          mov EBP,EBX
          xor EBP,ECX
          ror EDX,10
          add EDX,ECX
          mov EAX,EBP
          mov EBP,DWORD PTR [EDI+20]
          and EAX,EDX
          xor EAX,EBX
          add EAX,ESI
          lea ESI,DWORD PTR [EBX+EBP*1+1200080426]
          mov EBP,ECX
          xor EBP,EDX
          rol EAX,7
          add EAX,EDX
          mov EBX,EBP
          mov EBP,DWORD PTR [EDI+24]
          and EBX,EAX
          xor EBX,ECX
          add EBX,ESI
          lea ESI,DWORD PTR [ECX+EBP*1-1473231341]
          mov EBP,EDX
          xor EBP,EAX
          rol EBX,12
          add EBX,EAX
          mov ECX,EBP
          mov EBP,DWORD PTR [EDI+28]
          and ECX,EBX
          xor ECX,EDX
          add ECX,ESI
          lea ESI,DWORD PTR [EDX+EBP*1-45705983]
          mov EDX,EAX
          ror ECX,15
          mov EBP,DWORD PTR [EDI+32]
          xor EDX,EBX
          add ECX,EBX
          and EDX,ECX
          xor EDX,EAX
          add EDX,ESI
          lea ESI,DWORD PTR [EAX+EBP*1+1770035416]
          mov EBP,EBX
          xor EBP,ECX
          ror EDX,10
          add EDX,ECX
          mov EAX,EBP
          mov EBP,DWORD PTR [EDI+36]
          and EAX,EDX
          xor EAX,EBX
          add EAX,ESI
          lea ESI,DWORD PTR [EBX+EBP*1-1958414417]
          mov EBP,ECX
          xor EBP,EDX
          rol EAX,7
          add EAX,EDX
          mov EBX,EBP
          mov EBP,DWORD PTR [EDI+40]
          and EBX,EAX
          xor EBX,ECX
          add EBX,ESI
          lea ESI,DWORD PTR [ECX+EBP*1-42063]
          mov EBP,EDX
          xor EBP,EAX
          rol EBX,12
          add EBX,EAX
          mov ECX,EBP
          mov EBP,DWORD PTR [EDI+44]
          and ECX,EBX
          xor ECX,EDX
          add ECX,ESI
          lea ESI,DWORD PTR [EDX+EBP*1-1990404162]
          mov EDX,EAX
          ror ECX,15
          mov EBP,DWORD PTR [EDI+48]
          xor EDX,EBX
          add ECX,EBX
          and EDX,ECX
          xor EDX,EAX
          add EDX,ESI
          lea ESI,DWORD PTR [EAX+EBP*1+1804603682]
          mov EBP,EBX
          xor EBP,ECX
          ror EDX,10
          add EDX,ECX
          mov EAX,EBP
          mov EBP,DWORD PTR [EDI+52]
          and EAX,EDX
          xor EAX,EBX
          add EAX,ESI
          lea EBX,DWORD PTR [EBX+EBP*1-40341101]
          mov EBP,ECX
          xor EBP,EDX
          rol EAX,7
          add EAX,EDX
          mov ESI,EBP
          mov EBP,DWORD PTR [EDI+56]
          and ESI,EAX
          xor ESI,ECX
          add ESI,EBX
          lea EBX,DWORD PTR [ECX+EBP*1-1502002290]
          mov EBP,EDX
          xor EBP,EAX
          rol ESI,12
          add ESI,EAX
          mov ECX,EBP
          mov EBP,DWORD PTR [EDI+60]
          and ECX,ESI
          xor ECX,EDX
          add ECX,EBX
          lea EBX,DWORD PTR [EDX+EBP*1+1236535329]
          mov EDX,EAX
          ror ECX,15
          xor EDX,ESI
          mov EBP,DWORD PTR [EDI+4]
          add ECX,ESI
          and EDX,ECX
          xor EDX,EAX
          lea EAX,DWORD PTR [EBP+EAX*1-165796510]
          mov EBP,ECX
          add EDX,EBX
          ror EDX,10
          add EDX,ECX
          xor EBP,EDX
          mov EBX,EBP
          mov EBP,DWORD PTR [EDI+24]
          and EBX,ESI
          xor EBX,ECX
          add EBX,EAX
          lea ESI,DWORD PTR [EBP+ESI*1-1069501632]
          mov EBP,EDX
          rol EBX,5
          add EBX,EDX
          xor EBP,EBX
          mov EAX,EBP
          mov EBP,DWORD PTR [EDI+44]
          and EAX,ECX
          xor EAX,EDX
          add EAX,ESI
          lea ESI,DWORD PTR [EBP+ECX*1+643717713]
          mov EBP,EBX
          rol EAX,9
          add EAX,EBX
          xor EBP,EAX
          mov ECX,EBP
          mov EBP,DWORD PTR [EDI]
          and ECX,EDX
          xor ECX,EBX
          add ECX,ESI
          lea ESI,DWORD PTR [EBP+EDX*1-373897302]
          mov EDX,EAX
          rol ECX,14
          mov EBP,DWORD PTR [EDI+20]
          add ECX,EAX
          xor EDX,ECX
          and EDX,EBX
          xor EDX,EAX
          add EDX,ESI
          lea ESI,DWORD PTR [EBP+EBX*1-701558691]
          mov EBP,ECX
          ror EDX,12
          add EDX,ECX
          xor EBP,EDX
          mov EBX,EBP
          mov EBP,DWORD PTR [EDI+40]
          and EBX,EAX
          xor EBX,ECX
          add EBX,ESI
          lea ESI,DWORD PTR [EBP+EAX*1+38016083]
          mov EBP,EDX
          rol EBX,5
          add EBX,EDX
          xor EBP,EBX
          mov EAX,EBP
          mov EBP,DWORD PTR [EDI+60]
          and EAX,ECX
          xor EAX,EDX
          add EAX,ESI
          lea ESI,DWORD PTR [EBP+ECX*1-660478335]
          mov EBP,EBX
          rol EAX,9
          add EAX,EBX
          xor EBP,EAX
          mov ECX,EBP
          mov EBP,DWORD PTR [EDI+16]
          and ECX,EDX
          xor ECX,EBX
          add ECX,ESI
          lea ESI,DWORD PTR [EBP+EDX*1-405537848]
          mov EDX,EAX
          rol ECX,14
          mov EBP,DWORD PTR [EDI+36]
          add ECX,EAX
          xor EDX,ECX
          and EDX,EBX
          xor EDX,EAX
          add EDX,ESI
          lea ESI,DWORD PTR [EBP+EBX*1+568446438]
          mov EBP,ECX
          ror EDX,12
          add EDX,ECX
          xor EBP,EDX
          mov EBX,EBP
          mov EBP,DWORD PTR [EDI+56]
          and EBX,EAX
          xor EBX,ECX
          add EBX,ESI
          lea ESI,DWORD PTR [EBP+EAX*1-1019803690]
          mov EBP,EDX
          rol EBX,5
          add EBX,EDX
          xor EBP,EBX
          mov EAX,EBP
          mov EBP,DWORD PTR [EDI+12]
          and EAX,ECX
          xor EAX,EDX
          add EAX,ESI
          lea ESI,DWORD PTR [EBP+ECX*1-187363961]
          mov EBP,EBX
          rol EAX,9
          add EAX,EBX
          xor EBP,EAX
          mov ECX,EBP
          mov EBP,DWORD PTR [EDI+32]
          and ECX,EDX
          xor ECX,EBX
          add ECX,ESI
          lea ESI,DWORD PTR [EBP+EDX*1+1163531501]
          mov EDX,EAX
          rol ECX,14
          mov EBP,DWORD PTR [EDI+52]
          add ECX,EAX
          xor EDX,ECX
          and EDX,EBX
          xor EDX,EAX
          add EDX,ESI
          lea ESI,DWORD PTR [EBP+EBX*1-1444681467]
          mov EBP,ECX
          ror EDX,12
          add EDX,ECX
          xor EBP,EDX
          mov EBX,EBP
          mov EBP,DWORD PTR [EDI+8]
          and EBX,EAX
          xor EBX,ECX
          add EBX,ESI
          lea ESI,DWORD PTR [EBP+EAX*1-51403784]
          mov EBP,EDX
          rol EBX,5
          add EBX,EDX
          xor EBP,EBX
          mov EAX,EBP
          mov EBP,DWORD PTR [EDI+28]
          and EAX,ECX
          xor EAX,EDX
          add EAX,ESI
          lea ESI,DWORD PTR [EBP+ECX*1+1735328473]
          mov EBP,EBX
          rol EAX,9
          add EAX,EBX
          xor EBP,EAX
          mov ECX,EBP
          mov EBP,DWORD PTR [EDI+48]
          and ECX,EDX
          xor ECX,EBX
          add ECX,ESI
          lea ESI,DWORD PTR [EBP+EDX*1-1926607734]
          mov EDX,EAX
          rol ECX,14
          add ECX,EAX
          xor EDX,ECX
          mov EBP,ECX
          and EDX,EBX
          xor EDX,EAX
          add EDX,ESI
          ror EDX,12
          add EDX,ECX
          xor EBP,EDX
          mov ESI,EBP
          mov EBP,DWORD PTR [EDI+20]
          lea EBP,DWORD PTR [EBP+EBX*1-378558]
          mov EBX,EAX
          xor EBX,ESI
          add EBX,EBP
          mov EBP,DWORD PTR [EDI+32]
          rol EBX,4
          add EBX,EDX
          lea EBP,DWORD PTR [EBP+EAX*1-2022574463]
          xor ESI,EBX
          add ESI,EBP
          mov EBP,EBX
          rol ESI,11
          lea EAX,DWORD PTR [EBX+ESI*1]
          mov ESI,DWORD PTR [EDI+44]
          xor EBP,EAX
          lea ECX,DWORD PTR [ESI+ECX*1+1839030562]
          mov ESI,EDX
          xor ESI,EBP
          add ESI,ECX
          mov ECX,DWORD PTR [EDI+56]
          rol ESI,16
          add ESI,EAX
          lea EDX,DWORD PTR [ECX+EDX*1-35309556]
          xor EBP,ESI
          add EBP,EDX
          mov EDX,ESI
          ror EBP,9
          lea ECX,DWORD PTR [ESI+EBP*1]
          mov EBP,DWORD PTR [EDI+4]
          xor EDX,ECX
          lea EBP,DWORD PTR [EBP+EBX*1-1530992060]
          mov EBX,EAX
          xor EBX,EDX
          add EBX,EBP
          mov EBP,DWORD PTR [EDI+16]
          rol EBX,4
          add EBX,ECX
          lea EAX,DWORD PTR [EBP+EAX*1+1272893353]
          xor EDX,EBX
          mov EBP,EBX
          add EDX,EAX
          rol EDX,11
          add EDX,EBX
          xor EBP,EDX
          mov EAX,EBP
          mov EBP,DWORD PTR [EDI+28]
          lea ESI,DWORD PTR [EBP+ESI*1-155497632]
          mov EBP,ECX
          xor EBP,EAX
          add EBP,ESI
          mov ESI,DWORD PTR [EDI+40]
          rol EBP,16
          add EBP,EDX
          lea ECX,DWORD PTR [ESI+ECX*1-1094730640]
          xor EAX,EBP
          mov ESI,DWORD PTR [EDI+52]
          add EAX,ECX
          mov ECX,EBP
          ror EAX,9
          lea EBX,DWORD PTR [ESI+EBX*1+681279174]
          mov ESI,EDX
          add EAX,EBP
          xor ECX,EAX
          xor ESI,ECX
          add ESI,EBX
          mov EBX,DWORD PTR [EDI]
          rol ESI,4
          add ESI,EAX
          lea EBX,DWORD PTR [EBX+EDX*1-358537222]
          xor ECX,ESI
          add ECX,EBX
          mov EBX,DWORD PTR [EDI+12]
          rol ECX,11
          lea EDX,DWORD PTR [ESI+ECX*1]
          mov ECX,ESI
          lea EBP,DWORD PTR [EBX+EBP*1-722521979]
          mov EBX,EAX
          xor ECX,EDX
          xor EBX,ECX
          add EBX,EBP
          mov EBP,DWORD PTR [EDI+24]
          rol EBX,16
          add EBX,EDX
          lea EAX,DWORD PTR [EBP+EAX*1+76029189]
          xor ECX,EBX
          mov EBP,EBX
          add ECX,EAX
          ror ECX,9
          add ECX,EBX
          xor EBP,ECX
          mov EAX,EBP
          mov EBP,DWORD PTR [EDI+36]
          lea EBP,DWORD PTR [EBP+ESI*1-640364487]
          mov ESI,EDX
          xor ESI,EAX
          add ESI,EBP
          mov EBP,DWORD PTR [EDI+48]
          rol ESI,4
          add ESI,ECX
          lea EBP,DWORD PTR [EBP+EDX*1-421815835]
          xor EAX,ESI
          add EAX,EBP
          mov EBP,ESI
          rol EAX,11
          lea EDX,DWORD PTR [ESI+EAX*1]
          xor EBP,EDX
          mov EAX,EBP
          mov EBP,DWORD PTR [EDI+60]
          lea EBP,DWORD PTR [EBP+EBX*1+530742520]
          mov EBX,ECX
          xor EBX,EAX
          add EBX,EBP
          mov EBP,DWORD PTR [EDI+8]
          rol EBX,16
          add EBX,EDX
          lea ECX,DWORD PTR [EBP+ECX*1-995338651]
          mov EBP,DWORD PTR [EDI]
          xor EAX,EBX
          add EAX,ECX
          lea ESI,DWORD PTR [EBP+ESI*1-198630844]
          mov EBP,EDX
          ror EAX,9
          not EBP
          add EAX,EBX
          mov ECX,EBP
          mov EBP,DWORD PTR [EDI+28]
          or ECX,EAX
          xor ECX,EBX
          add ECX,ESI
          lea ESI,DWORD PTR [EBP+EDX*1+1126891415]
          mov EDX,EBX
          rol ECX,6
          mov EBP,DWORD PTR [EDI+56]
          not EDX
          add ECX,EAX
          or EDX,ECX
          xor EDX,EAX
          add EDX,ESI
          lea ESI,DWORD PTR [EBP+EBX*1-1416354905]
          mov EBP,EAX
          rol EDX,10
          not EBP
          add EDX,ECX
          mov EBX,EBP
          mov EBP,DWORD PTR [EDI+20]
          or EBX,EDX
          xor EBX,ECX
          add EBX,ESI
          lea ESI,DWORD PTR [EBP+EAX*1-57434055]
          mov EBP,ECX
          rol EBX,15
          not EBP
          add EBX,EDX
          mov EAX,EBP
          mov EBP,DWORD PTR [EDI+48]
          or EAX,EBX
          xor EAX,EDX
          add EAX,ESI
          lea ESI,DWORD PTR [EBP+ECX*1+1700485571]
          mov EBP,EDX
          ror EAX,11
          not EBP
          add EAX,EBX
          mov ECX,EBP
          mov EBP,DWORD PTR [EDI+12]
          or ECX,EAX
          xor ECX,EBX
          add ECX,ESI
          lea ESI,DWORD PTR [EBP+EDX*1-1894986606]
          mov EDX,EBX
          rol ECX,6
          mov EBP,DWORD PTR [EDI+40]
          not EDX
          add ECX,EAX
          or EDX,ECX
          xor EDX,EAX
          add EDX,ESI
          lea ESI,DWORD PTR [EBP+EBX*1-1051523]
          mov EBP,EAX
          rol EDX,10
          not EBP
          add EDX,ECX
          mov EBX,EBP
          mov EBP,DWORD PTR [EDI+4]
          or EBX,EDX
          xor EBX,ECX
          add EBX,ESI
          lea EAX,DWORD PTR [EBP+EAX*1-2054922799]
          mov EBP,ECX
          rol EBX,15
          not EBP
          add EBX,EDX
          mov ESI,EBP
          mov EBP,DWORD PTR [EDI+32]
          or ESI,EBX
          xor ESI,EDX
          add ESI,EAX
          lea ECX,DWORD PTR [EBP+ECX*1+1873313359]
          mov EBP,EDX
          ror ESI,11
          not EBP
          add ESI,EBX
          mov EAX,EBP
          mov EBP,DWORD PTR [EDI+60]
          or EAX,ESI
          xor EAX,EBX
          add EAX,ECX
          lea ECX,DWORD PTR [EBP+EDX*1-30611744]
          mov EDX,EBX
          rol EAX,6
          mov EBP,DWORD PTR [EDI+24]
          not EDX
          add EAX,ESI
          or EDX,EAX
          xor EDX,ESI
          lea EBX,DWORD PTR [EBP+EBX*1-1560198380]
          mov EBP,ESI
          add EDX,ECX
          not EBP
          rol EDX,10
          mov ECX,EBP
          mov EBP,DWORD PTR [EDI+52]
          add EDX,EAX
          or ECX,EDX
          xor ECX,EAX
          lea ESI,DWORD PTR [EBP+ESI*1+1309151649]
          mov EBP,EAX
          add ECX,EBX
          not EBP
          rol ECX,15
          mov EBX,EBP
          mov EBP,DWORD PTR [EDI+16]
          add ECX,EDX
          or EBX,ECX
          xor EBX,EDX
          add EBX,ESI
          lea ESI,DWORD PTR [EBP+EAX*1-145523070]
          mov EBP,EDX
          ror EBX,11
          not EBP
          add EBX,ECX
          mov EAX,EBP
          mov EBP,DWORD PTR [EDI+44]
          or EAX,EBX
          add EDI,64
          xor EAX,ECX
          add EAX,ESI
          lea ESI,DWORD PTR [EBP+EDX*1-1120210379]
          mov EDX,ECX
          rol EAX,6
          mov EBP,DWORD PTR [EDI-56]
          not EDX
          add EAX,EBX
          add DWORD PTR [ESP+12],EAX
          or EDX,EAX
          xor EDX,EBX
          add EDX,ESI
          lea ESI,DWORD PTR [EBP+ECX*1+718787259]
          mov EBP,EBX
          rol EDX,10
          not EBP
          add EDX,EAX
          mov ECX,EBP
          mov EBP,DWORD PTR [EDI-28]
          or ECX,EDX
          add DWORD PTR [ESP+8],EDX
          xor ECX,EAX
          add ECX,ESI
          lea ESI,DWORD PTR [EBP+EBX*1-343485551]
          mov EBP,EAX
          rol ECX,15
          not EBP
          add ECX,EDX
          mov EBX,EBP
          add DWORD PTR [ESP+4],ECX
          or EBX,ECX
          xor EBX,EDX
          add EBX,ESI
          ror EBX,11
          add EBX,ECX
          add DWORD PTR [ESP],EBX
          sub DWORD PTR [ESP+16],64
          jne L_444fe0
          mov EAX,DWORD PTR [ESP+20]
          mov ESI,DWORD PTR [ESP+12]
          mov DWORD PTR [EAX+8],ESI
          mov ESI,DWORD PTR [ESP]
          mov DWORD PTR [EAX+12],ESI
          mov ESI,DWORD PTR [ESP+4]
          mov DWORD PTR [EAX+16],ESI
          mov ESI,DWORD PTR [ESP+8]
          mov DWORD PTR [EAX+20],ESI
          add ESP,24
          mov EAX,EDI
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x90
FUN_445690:
          mov EAX,DWORD PTR [ESP+4]
          mov DWORD PTR [EAX+8],1732584193
          mov DWORD PTR [EAX+12],4023233417
          mov DWORD PTR [EAX+16],2562383102
          mov DWORD PTR [EAX+20],271733878
          mov DWORD PTR [EAX],0
          mov DWORD PTR [EAX+4],0
          ret 
          .byte 0x66
          .byte 0x90
FUN_4456c0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,28
          mov ESI,DWORD PTR [ESP+48]
          mov EBX,DWORD PTR [ESP+56]
          mov EDI,DWORD PTR [ESP+52]
          mov EAX,DWORD PTR [ESI]
          mov ECX,DWORD PTR [ESI+4]
          lea EDX,DWORD PTR [EAX+EBX*1]
          and EDX,536870911
          cmp EAX,EDX
          mov DWORD PTR [ESI],EDX
          jbe L_4456ea
          add ECX,1
L_4456ea:
          mov EDX,EBX
          lea EBP,DWORD PTR [ESI+24]
          shr EDX,29
          add EDX,ECX
          and EAX,63
          mov DWORD PTR [ESI+4],EDX
          mov EDX,EAX
          je L_445786
          mov EAX,64
          sub EAX,EDX
          cmp EBX,EAX
          jb L_445805
          cmp EAX,4
          lea EDX,DWORD PTR [ESI+EDX*1+24]
          jb L_445760
          mov ECX,DWORD PTR [EDI]
          mov EBP,EDI
          mov DWORD PTR [EDX],ECX
          mov ECX,DWORD PTR [EDI+EAX*1-4]
          mov DWORD PTR [EDX+EAX*1-4],ECX
          lea ECX,DWORD PTR [EDX+4]
          and ECX,4294967292
          sub EDX,ECX
          sub EBP,EDX
          add EDX,EAX
          and EDX,4294967292
          cmp EDX,4
          jb L_445771
          and EDX,4294967292
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],EDX
          xor EDX,EDX
L_445749:
          mov EAX,DWORD PTR [EBP+EDX*1]
          mov DWORD PTR [ECX+EDX*1],EAX
          add EDX,4
          cmp EDX,DWORD PTR [ESP+8]
          jb L_445749
          mov EAX,DWORD PTR [ESP+12]
          jmp L_445771
          .byte 0x90
L_445760:
          test EAX,EAX
          je L_445771
          movzx ECX,BYTE PTR [EDI]
          test AL,2
          mov BYTE PTR [EDX],CL
          jne L_445821
L_445771:
          lea EBP,DWORD PTR [ESI+24]
          add EDI,EAX
          sub EBX,EAX
          mov ECX,64
          mov EAX,ESI
          mov EDX,EBP
          call FUN_444fb0
L_445786:
          cmp EBX,63
          ja L_4457f0
L_44578b:
          cmp EBX,4
          jb L_4457d0
          mov EAX,DWORD PTR [EDI]
          mov DWORD PTR [EBP],EAX
          mov EAX,DWORD PTR [EDI+EBX*1-4]
          mov DWORD PTR [EBP+EBX*1-4],EAX
          lea EAX,DWORD PTR [EBP+4]
          and EAX,4294967292
          sub EBP,EAX
          add EBX,EBP
          sub EDI,EBP
          and EBX,4294967292
          cmp EBX,4
          jb L_4457c3
          and EBX,4294967292
          xor EDX,EDX
L_4457b6:
          mov ECX,DWORD PTR [EDI+EDX*1]
          mov DWORD PTR [EAX+EDX*1],ECX
          add EDX,4
          cmp EDX,EBX
          jb L_4457b6
L_4457c3:
          add ESP,28
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
L_4457d0:
          test EBX,EBX
          je L_4457c3
          movzx EAX,BYTE PTR [EDI]
          test BL,2
          mov BYTE PTR [EBP],AL
          je L_4457c3
          movzx EAX,WORD PTR [EDI+EBX*1-2]
          mov WORD PTR [EBP+EBX*1-2],AX
          jmp L_4457c3
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_4457f0:
          mov ECX,EBX
          mov EDX,EDI
          mov EAX,ESI
          and ECX,4294967232
          and EBX,63
          call FUN_444fb0
          mov EDI,EAX
          jmp L_44578b
L_445805:
          lea EAX,DWORD PTR [ESI+EDX*1+24]
          mov DWORD PTR [ESP+56],EBX
          mov DWORD PTR [ESP+52],EDI
          mov DWORD PTR [ESP+48],EAX
          add ESP,28
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          jmp _memcpy
L_445821:
          movzx ECX,WORD PTR [EDI+EAX*1-2]
          mov WORD PTR [EDX+EAX*1-2],CX
          jmp L_445771
FUN_445830:
          push EBP
          push EDI
          mov EDX,64
          push ESI
          push EBX
          mov EBX,DWORD PTR [ESP+24]
          mov ESI,DWORD PTR [ESP+20]
          mov EAX,DWORD PTR [EBX]
          and EAX,63
          lea ECX,DWORD PTR [EAX+1]
          mov BYTE PTR [EBX+EAX*1+24],128
          sub EDX,ECX
          cmp EDX,7
          jbe L_4459d0
          mov EDX,56
          lea EDI,DWORD PTR [EBX+24]
          add EAX,25
          sub EDX,ECX
L_445866:
          add EAX,EBX
          cmp EDX,4
          jae L_445970
          test EDX,EDX
          jne L_4459b0
L_445879:
          mov EAX,DWORD PTR [EBX]
          xor EDX,EDX
          mov ECX,DWORD PTR [EBX+4]
          shl EAX,3
          mov DL,AL
          mov EBP,EAX
          mov DWORD PTR [EBX],EAX
          mov DH,AH
          and EBP,16711680
          and EAX,4278190080
          movzx EDX,DX
          or EDX,EBP
          or EAX,EDX
          mov EDX,ECX
          mov DWORD PTR [EBX+80],EAX
          xor EAX,EAX
          and EDX,16711680
          mov AL,CL
          mov AH,CH
          and ECX,4278190080
          movzx EAX,AX
          or EAX,EDX
          mov EDX,EDI
          lea EDI,DWORD PTR [EBX+4]
          or EAX,ECX
          mov ECX,64
          mov DWORD PTR [EBX+84],EAX
          mov EAX,EBX
          and EDI,4294967292
          call FUN_444fb0
          mov EAX,DWORD PTR [EBX+8]
          mov BYTE PTR [ESI],AL
          mov EAX,DWORD PTR [EBX+8]
          shr EAX,8
          mov BYTE PTR [ESI+1],AL
          movzx EAX,WORD PTR [EBX+10]
          mov BYTE PTR [ESI+2],AL
          movzx EAX,BYTE PTR [EBX+11]
          mov BYTE PTR [ESI+3],AL
          mov EAX,DWORD PTR [EBX+12]
          mov BYTE PTR [ESI+4],AL
          mov EAX,DWORD PTR [EBX+12]
          shr EAX,8
          mov BYTE PTR [ESI+5],AL
          movzx EAX,WORD PTR [EBX+14]
          mov BYTE PTR [ESI+6],AL
          movzx EAX,BYTE PTR [EBX+15]
          mov BYTE PTR [ESI+7],AL
          mov EAX,DWORD PTR [EBX+16]
          mov BYTE PTR [ESI+8],AL
          mov EAX,DWORD PTR [EBX+16]
          shr EAX,8
          mov BYTE PTR [ESI+9],AL
          movzx EAX,WORD PTR [EBX+18]
          mov BYTE PTR [ESI+10],AL
          movzx EAX,BYTE PTR [EBX+19]
          mov BYTE PTR [ESI+11],AL
          mov EAX,DWORD PTR [EBX+20]
          mov BYTE PTR [ESI+12],AL
          mov EAX,DWORD PTR [EBX+20]
          shr EAX,8
          mov BYTE PTR [ESI+13],AL
          movzx EAX,WORD PTR [EBX+22]
          mov BYTE PTR [ESI+14],AL
          movzx EAX,BYTE PTR [EBX+23]
          mov BYTE PTR [ESI+15],AL
          mov DWORD PTR [EBX],0
          xor EAX,EAX
          mov DWORD PTR [EBX+148],0
          sub EBX,EDI
          lea ECX,DWORD PTR [EBX+152]
          shr ECX,2
          rep stosd DWORD PTR ES:[EDI]
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
L_445970:
          lea ECX,DWORD PTR [EAX+4]
          mov DWORD PTR [EAX],0
          mov DWORD PTR [EAX+EDX*1-4],0
          and ECX,4294967292
          sub EAX,ECX
          add EAX,EDX
          and EAX,4294967292
          cmp EAX,4
          jb L_445879
          and EAX,4294967292
          xor EDX,EDX
L_445999:
          mov DWORD PTR [ECX+EDX*1],0
          add EDX,4
          cmp EDX,EAX
          jb L_445999
          jmp L_445879
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_4459b0:
          test DL,2
          mov BYTE PTR [EAX],0
          je L_445879
          xor ECX,ECX
          mov WORD PTR [EAX+EDX*1-2],CX
          jmp L_445879
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4459d0:
          cmp EDX,4
          lea EAX,DWORD PTR [EBX+EAX*1+25]
          jb L_445a10
          lea ECX,DWORD PTR [EAX+4]
          mov DWORD PTR [EAX],0
          mov DWORD PTR [EAX+EDX*1-4],0
          and ECX,4294967292
          sub EAX,ECX
          add EDX,EAX
          and EDX,4294967292
          cmp EDX,4
          jb L_445a1c
          and EDX,4294967292
          xor EAX,EAX
L_4459fe:
          mov DWORD PTR [ECX+EAX*1],0
          add EAX,4
          cmp EAX,EDX
          jb L_4459fe
          jmp L_445a1c
          .byte 0x66
          .byte 0x90
L_445a10:
          test EDX,EDX
          je L_445a1c
          test DL,2
          mov BYTE PTR [EAX],0
          jne L_445a3c
L_445a1c:
          lea EDI,DWORD PTR [EBX+24]
          mov ECX,64
          mov EAX,EBX
          mov EDX,EDI
          call FUN_444fb0
          mov EAX,24
          mov EDX,56
          jmp L_445866
L_445a3c:
          xor EDI,EDI
          mov WORD PTR [EAX+EDX*1-2],DI
          jmp L_445a1c
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
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_444fb0 - .
          .byte 0xdf
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
          .byte 0xd1
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
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x5c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_445690 - .
          .byte 0x2e
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x70
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_4456c0 - .
          .byte 0x70
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
          .byte 0xff
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
          .byte 0x2
          .byte 0x48
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
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc8
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_445830 - .
          .byte 0x15
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
          .byte 0x3
          .byte 0x2c
          .byte 0x1
          .byte 0xa
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

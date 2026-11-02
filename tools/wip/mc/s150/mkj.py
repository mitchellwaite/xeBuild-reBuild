s=open('ua11.c',newline='').read()
dyx='__asm__ goto ("" :::: dx); '; assert s.count(dyx)==1
cp=lambda a:'__builtin_constant_p(block + %d)'%a
# only dw
fx='if (%s) goto dx; dxb:;'%cp(907); assert s.count(fx)==1
i=s.index('if (0) { dx:'); j=s.index('if (0) { dy:',i)
only=s[:i]+s[j:]; only=only.replace(dyx,'').replace(fx,'')
open('v1.c','w',newline='\n').write(only)
# dx through a cold folded arm in dy (edge frequency 0, no trace-end boost), key from its feed
open('v2.c','w',newline='\n').write(s.replace(dyx,'if (!%s) { dxc: __attribute__((cold)); __asm__ goto ("" :::: dx); } '%cp(952)))
open('v3.c','w',newline='\n').write(s.replace(dyx,'').replace('JMP(dy,dw);','JMP(dy,dw,dx);'))
open('v4.c','w',newline='\n').write(s.replace(dyx,'').replace('JMP(dy,dw);','JMP(dx,dy,dw);'))

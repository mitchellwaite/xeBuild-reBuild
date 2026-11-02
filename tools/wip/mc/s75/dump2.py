import struct,re,sys
b=open('xeBuild.exe','rb').read()
pe=struct.unpack_from('<I',b,0x3c)[0]
ns=struct.unpack_from('<H',b,pe+6)[0]; osz=struct.unpack_from('<H',b,pe+20)[0]
ib=struct.unpack_from('<I',b,pe+24+28)[0]
secs=[]
o=pe+24+osz
for i in range(ns):
    va,rs,rp=struct.unpack_from('<I',b,o+12)[0],struct.unpack_from('<I',b,o+16)[0],struct.unpack_from('<I',b,o+20)[0]
    secs.append((va+ib,rs,rp)); o+=40
def s(a):
    for va,rs,rp in secs:
        if va<=a<va+rs:
            p=rp+a-va; e=b.index(b'\0',p); return b[p:e][:40].decode('latin1').replace('\n','\n')
for l in open(sys.argv[1]):
    l=re.sub(r'OFFSET \.L_([0-9a-f]+)',lambda m:'"%s"'%s(int(m.group(1),16)),l)
    print(l,end='')

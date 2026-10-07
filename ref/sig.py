# Locate vanilla pokered symbols inside the Creepy Black ROM by masked byte signatures.
import re,sys
red=open('ref/red.gb','rb').read();cb=open(sys.argv[1] if len(sys.argv)>1 and sys.argv[1].endswith('.gb') else 'overhaul/Creepy_Black_Mu_v2.gb','rb').read()
sym={}
for l in open('ref/pokered.sym'):
    m=re.match(r'([0-9a-f]{2}):([0-9a-f]{4}) (\S+)',l)
    if m:sym[m.group(3)]=(int(m.group(1),16),int(m.group(2),16))
def off(b,a):return a if b==0 else b*0x4000+a-0x4000
OPS3={0xc3,0xcd,0xc2,0xca,0xd2,0xda,0xc4,0xcc,0xd4,0xdc,0x01,0x11,0x21,0x31,0xfa,0xea,0x08}
def masked(o,n):
    pat=[];i=0;b=red[o:o+n]
    while i<len(b):
        op=b[i];pat.append(re.escape(bytes([op])))
        if op in OPS3 and i+2<len(b):pat+=[b'.',b'.'];i+=3
        elif op==0xcb and i+1<len(b):pat.append(re.escape(bytes([b[i+1]])));i+=2
        elif op in (0x18,0x20,0x28,0x30,0x38,0x3e,0x06,0x0e,0x16,0x1e,0x26,0x2e,0x36,0xe0,0xf0,0xc6,0xd6,0xe6,0xee,0xf6,0xfe,0xce,0xde,0xe8,0xf8) and i+1<len(b):pat.append(re.escape(bytes([b[i+1]])));i+=2
        else:i+=1
    return re.compile(b''.join(pat),re.S)
def find(name,n=20,bank=None):
    b,a=sym[name];o=off(b,a);rx=masked(o,n)
    hits=[m.start() for m in rx.finditer(cb)]
    if bank is not None:hits=[h for h in hits if h//0x4000==bank]
    return hits
if __name__=='__main__':
    for name in sys.argv[2:] if sys.argv[1].endswith('.gb') else sys.argv[1:]:
        for n in (24,16,12):
            h=find(name,n)
            if h:break
        print(name,'vanilla',sym[name],'-> CB',[(hex(x//0x4000),hex(0x4000+x%0x4000 if x>=0x4000 else x)) for x in h[:4]],'n',n)

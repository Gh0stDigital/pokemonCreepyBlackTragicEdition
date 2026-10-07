# Creepy Black Mu v8: fossils immune to MACABRE (PRETA may fight the Black Tamer), Mr. Mu moves to the
# Pokemon Mansion 1F after PRETA, fully white fossil Kabutops back sprite. Logged patches on top of verified Mu v7.
from pathlib import Path
import json,hashlib,re,io,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'ref'));import pic
M7=json.loads((ROOT/'manifest_v7.json').read_text());V7_SHA=M7['sha256']
src=(ROOT/'Creepy_Black_Mu_v7.gb').read_bytes();assert hashlib.sha256(src).hexdigest()==V7_SHA
r=bytearray(src);log=[]
def patch(o,data,name,old):
    data=bytes(data);old=bytes.fromhex(old) if isinstance(old,str) else bytes(old)
    assert r[o:o+len(old)]==old,(name,hex(o),r[o:o+len(old)].hex())
    log.append(dict(offset=hex(o),before=r[o:o+len(data)].hex(),after=data.hex(),name=name));r[o:o+len(data)]=data
def put(o,data,name):            # write into verified-empty space
    assert not any(r[o:o+len(data)]),('not free',name,hex(o));patch(o,data,name,'00'*len(data))
def fo(bank,addr):return addr if bank==0 else bank*0x4000+addr-0x4000

class Code:
    def __init__(self,bank,org):self.bank=bank;self.org=org;self.b=bytearray();self.labels={};self.refs=[];self.rel=[]
    def emit(self,h):self.b+=bytes.fromhex(h)
    def raw(self,b):self.b+=bytes(b)
    def label(self,n):self.labels[n]=self.org+len(self.b)
    def ref(self,op,n):self.emit(op);self.refs.append((len(self.b),n));self.b+=b'\0\0'
    def jr(self,op,n):self.emit(op);self.rel.append((len(self.b),n));self.b+=b'\0'
    def finish(self,ext={}):
        L={**ext,**self.labels}
        for p,n in self.refs:self.b[p:p+2]=L[n].to_bytes(2,'little')
        for p,n in self.rel:
            d=L[n]-(self.org+p+1);assert -128<=d<128,n;self.b[p]=d&255
        return bytes(self.b)
def le(a):return a.to_bytes(2,'little').hex()
def far(addr,bank):return '21 %s 06 %02x cd 18 36'%(le(addr),bank)

cm={}
for k,v in re.findall(r'^\s*charmap "([^"]+)",\s*\$([0-9A-Fa-f]+)',(ROOT.parent/'pokeblack/charmap.asm').read_text(encoding='utf8'),re.M):cm.setdefault(k,int(v,16))
def enc(s):
    out=bytearray()
    while s:
        k=next(k for k in sorted(cm,key=len,reverse=True) if s.startswith(k));out.append(cm[k]);s=s[len(k):]
    return out


def shown(line):return len(line.replace('#','POKé').replace('<PLAYER>','X'*7))
def txt(paras,end=0x58):
    out=bytearray([0])
    for i,p in enumerate(paras):
        if i:out.append(0x51)
        for j,line in enumerate(p):
            assert shown(line)<=17,line
            if j:out.append(0x4f if j==1 else 0x55)
            out+=enc(line)
    out.append(end);return out
PRINTTEXT,TEXTSCRIPTEND,ISGHOSTBATTLE,MOVEHITTEST=0x3c94,0x2504,0x5910,0x6641
KAB,AERO,MACABRE,GENTLEMAN=0xb6,0xb7,0xa9,0x10
MU2=0xd460            # v6: 0 not met, 1 introduced, 2 PRETA given; v8: 3 = left the trade house -> Mansion
M6=json.loads((ROOT/'manifest_v6.json').read_text())['labels']['bank7']
SCARED=int(json.loads((ROOT/'manifest_v3.json').read_text())['labels']['bankF']['scared'],16)

# 1. MACABRE has no effect on the fossil Kabutops / Aerodactyl ("It doesn't affect..."), and PRETA is not
#    "too scared" in the Mirage battle, so it can fight them with its other moves.
f=Code(0xf,0x7e50)
f.label('hit');f.emit('cd '+le(MOVEHITTEST)+' fa d2 cf fe %02x c0 fa e5 cf fe %02x'%(MACABRE,KAB));f.jr('28','immune')
f.emit('fe %02x c0'%AERO)
f.label('immune');f.emit('3e 01 ea 5f d0 af ea 5b d0 c9')                # missed + multiplier 0 = doesn't affect
f.label('scared');f.emit('fa 14 d0 fe %02x ca %s c3 %s'%(KAB,le(ISGHOSTBATTLE),le(SCARED)))
codeF=f.finish();put(fo(0xf,0x7e50),codeF,'Bank F: fossil immunity to MACABRE, PRETA not scared')
patch(fo(0xf,0x57d3),bytes.fromhex('cd'+le(f.labels['hit'])),'Player MoveHitTest: MACABRE vs fossils','cd'+le(MOVEHITTEST))
patch(fo(0xf,0x58e2),bytes.fromhex('cd'+le(f.labels['scared'])),'PrintGhostText: PRETA is never too scared','cd'+le(SCARED))

# 2. Mr. Mu leaves the Cerulean trade house once the player leaves it after receiving PRETA (D460 2 -> 3
#    on the next map load) and waits on the Pokemon Mansion 1F entrance carpet.
old_ml=r[0xb8000:0xb8003];assert old_ml[0]==0xc3;ML_NEXT=int.from_bytes(old_ml[1:],'little')
g=Code(0x2e,0x4800)
g.label('mapload');g.emit('fa %s fe 02'%le(MU2));g.jr('20','next');g.emit('fa 5e d3 fe 3f');g.jr('28','next')
g.emit('3e 03 ea '+le(MU2))
g.label('next');g.emit('c3 '+le(ML_NEXT))
code2e=g.finish();put(fo(0x2e,0x4800),code2e,'Bank 2E: Mu moves on after PRETA')
patch(0xb8000,bytes.fromhex('c3'+le(g.labels['mapload'])),'Map load: Mu state 2 -> 3 outside the trade house',old_ml)
t=Code(7,0x7600)                                  # trade house: hide unless Ghost owned and Mu still there
t.label('script');t.emit('fa 51 d4 a7');t.jr('28','hide');t.emit('fa %s fe 03'%le(MU2));t.jr('38','show')
t.label('hide');t.emit('af ea 30 c1 3e ff ea 34 c2 ea 35 c2')
t.label('show');t.emit('c3 87 3c')
code7=t.finish();put(fo(7,0x7600),code7,'Bank 7: trade house Mu visibility v8')
patch(fo(7,0x56fa+7),bytes.fromhex(le(t.labels['script'])),'Trade house script pointer -> v8',le(int(M6['script'],16)))

MAN=0x42a3;BANK=0x11
assert r[fo(BANK,MAN):fo(BANK,MAN)+12]==bytes.fromhex('160e0ffe432c43af4200a443')
OBJ=fo(BANK,0x43a4);obj=bytearray(r[OBJ:OBJ+0x43fe-0x43a4]);assert obj[1]==8 and obj[34]==0 and obj[35]==3
WT=36+8+7+7                                         # start of warp-to data after the 3 objects
c=Code(BANK,0x7100)
c.label('objects');c.raw(obj[:35]+bytes([4])+obj[36:WT]+bytes([GENTLEMAN,21+4,6+4,0xff,0xd0,4])+obj[WT:])
c.label('texts');c.raw(r[fo(BANK,0x432c):fo(BANK,0x432c)+6]);c.ref('','mu')
c.label('script');c.emit('fa %s fe 03'%le(MU2));c.jr('30','show')
c.emit('af ea 40 c1 3e ff ea 44 c2 ea 45 c2')
c.label('show');c.emit('c3 af 42')
c.label('mu');c.emit('08');c.ref('21','t_mu');c.emit('cd %s c3 %s'%(le(PRINTTEXT),le(TEXTSCRIPTEND)))
DIALOGUE=json.loads((ROOT/'dialogue_v8.json').read_text(encoding='utf8'))
c.label('t_mu');c.raw(txt(DIALOGUE['mansion']))
code11=c.finish();put(fo(BANK,0x7100),code11,'Bank 11: Mansion 1F Mr. Mu (objects, texts, script)')
patch(fo(BANK,MAN+5),bytes.fromhex(le(c.labels['texts'])+le(c.labels['script'])),'Mansion 1F text + script pointers','2c43af42')
patch(fo(BANK,MAN+10),bytes.fromhex(le(c.labels['objects'])),'Mansion 1F object pointer','a443')

# 3. Fossil Kabutops back sprite: the remaining dark-grey rib lines become white too (black + white only).
BACK=fo(0x0b,0x7f3c);OLD=(ROOT/'kab_back_v7.bin').read_bytes();SLOT=191
assert r[BACK:BACK+SLOT]==OLD.ljust(SLOT,b'\0')
d=bytearray(pic.decompress(io.BytesIO(bytes(r)),offset=BACK));whitened=0
for i in range(0,256,2):                       # colour 2 (lo=0,hi=1) -> 0
    lo,hi=d[i],d[i+1];m2=hi&~lo&0xff;whitened+=bin(m2).count('1');d[i+1]=hi&~m2
assert all((d[i]^d[i+1])==0 for i in range(0,256,2))   # only white (00) and black (11) left
new=bytes(pic.compress(bytes(d)));assert len(new)<=SLOT and bytes(pic.decompress(io.BytesIO(new)))==bytes(d)
(ROOT/'kab_back_v8.bin').write_bytes(new)
patch(BACK,new.ljust(SLOT,b'\0'),'Fossil Kabutops back sprite: grey rib lines -> white (%d px, %d bytes)'%(whitened,len(new)),OLD.ljust(SLOT,b'\0'))

# Header -----------------------------------------------------------------------
patch(0x134,b'CREEPY MU V8'.ljust(16,b'\0'),'Branch identity v8',b'CREEPY MU V7'.ljust(16,b'\0'))
v=0
for x in r[0x134:0x14d]:v=(v-x-1)&255
r[0x14d]=v;r[0x14e:0x150]=((sum(r[:0x14e])+sum(r[0x150:]))&65535).to_bytes(2,'big')
assert len(r)==1048576
out=ROOT/'Creepy_Black_Mu_v8.gb';out.write_bytes(r);sha=hashlib.sha256(r).hexdigest()
(ROOT/'manifest_v8.json').write_text(json.dumps(dict(input='Creepy_Black_Mu_v7.gb',input_sha256=V7_SHA,sha256=sha,size=len(r),
  labels={'bankF':{k:hex(v) for k,v in f.labels.items()},'bank2e':{k:hex(v) for k,v in g.labels.items()},'bank7':{k:hex(v) for k,v in t.labels.items()},'bank11':{k:hex(v) for k,v in c.labels.items()}},changes=log),indent=2))
print('Built',out.name,sha,'| F',len(codeF),'2E',len(code2e),'7',len(code7),'11',len(code11),'back',len(new),'whitened',whitened)

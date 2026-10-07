# Creepy Black Mu v9: species B6 is named PRETA, PRETA is immune to MACABREBLADE, no Rare Candy and no
# Pokemon Center healing for GHOST / PRETA / fossil Aerodactyl. Logged patches on top of verified Mu v8.
from pathlib import Path
import json,hashlib,re,io,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'ref'));import pic
M8=json.loads((ROOT/'manifest_v8.json').read_text());V8_SHA=M8['sha256']
src=(ROOT/'Creepy_Black_Mu_v8.gb').read_bytes();assert hashlib.sha256(src).hexdigest()==V8_SHA
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



GHOST,KAB,AERO,MACABREBLADE=0x1f,0xb6,0xb7,0xa7
MOVEHITTEST,PREDEF=0x6641,0x3ec1
CENTER=0xd462                 # temp flag: HealParty is running for the Pokemon Center nurse

# 1. Species B6 (player's PRETA and the Black Tamer's undead fossil) is named PRETA.
NAMES=0x1c21e;o=NAMES+10*(KAB-1)
patch(o,enc('PRETA').ljust(10,b'\x50'),'Species name B6 = PRETA',enc('KABUTOPS').ljust(10,b'\x50'))

# 2. MACABREBLADE (the Black Tamer's PRETA) doesn't affect the player's PRETA.
f=Code(0xf,0x7e80)
f.label('ehit');f.emit('cd %s fa cc cf fe %02x c0 fa 14 d0 fe %02x c0'%(le(MOVEHITTEST),MACABREBLADE,KAB))
f.emit('3e 01 ea 5f d0 af ea 5b d0 c9')
codeF=f.finish();put(fo(0xf,0x7e80),codeF,'Bank F: PRETA immune to MACABREBLADE')
patch(fo(0xf,0x6865),bytes.fromhex('cd'+le(f.labels['ehit'])),'Enemy MoveHitTest: MACABREBLADE vs PRETA','cd'+le(MOVEHITTEST))

# 3. GHOST, PRETA and fossil Aerodactyl: Rare Candy has no effect, and the Pokemon Center skips them
#    (HP, status and PP stay as they are). Mom and other HealParty users are unchanged.
c=Code(3,0x7fce)
c.label('cursed');c.emit('fe %02x c8 fe %02x c8 fe %02x c9'%(GHOST,KAB,AERO))      # z = one of them
c.label('candy');c.emit('fa b5 d0');c.ref('cd','cursed');c.emit('c8 7e fe 64 c9')   # z -> "won't have any effect"
c.label('heal');c.emit('2a fe ff c8 47 fa %s a7 78'%le(CENTER));c.jr('28','ok');c.ref('cd','cursed');c.jr('28','skip')
c.label('ok');c.emit('fe ff c9')
c.label('skip');c.emit('e5 21 2c 00 19 54 5d e1');c.jr('18','heal')
code3=c.finish();assert 0x7fce+len(code3)<=0x8000;put(fo(3,0x7fce),code3,'Bank 3: cursed Pokemon - no Rare Candy, no Center heal')
patch(fo(3,0x61b9),bytes.fromhex('cd'+le(c.labels['candy'])),'Rare Candy: no effect on GHOST/PRETA/fossil Aerodactyl','7efe64')
patch(fo(3,0x79da),bytes.fromhex('cd'+le(c.labels['heal'])),'HealParty loop: skip cursed Pokemon at the Center','2afeff')
n=Code(1,0x7c50)
n.label('nurse');n.emit('3e 01 ea %s 3e 07 cd %s af ea %s c9'%(le(CENTER),le(PREDEF),le(CENTER)))
code1=n.finish();put(fo(1,0x7c50),code1,'Bank 1: Pokemon Center heal flag')
patch(fo(1,0x7016),bytes.fromhex('cd'+le(n.labels['nurse'])+'0000'),'Pokemon Center: HealParty with cursed-Pokemon skip','3e07cdc13e')

# Header -----------------------------------------------------------------------
patch(0x134,b'CREEPY MU V9'.ljust(16,b'\0'),'Branch identity v9',b'CREEPY MU V8'.ljust(16,b'\0'))
v=0
for x in r[0x134:0x14d]:v=(v-x-1)&255
r[0x14d]=v;r[0x14e:0x150]=((sum(r[:0x14e])+sum(r[0x150:]))&65535).to_bytes(2,'big')
assert len(r)==1048576
out=ROOT/'Creepy_Black_Mu_v9.gb';out.write_bytes(r);sha=hashlib.sha256(r).hexdigest()
(ROOT/'manifest_v9.json').write_text(json.dumps(dict(input='Creepy_Black_Mu_v8.gb',input_sha256=V8_SHA,sha256=sha,size=len(r),
  labels={'bankF':{k:hex(v) for k,v in f.labels.items()},'bank3':{k:hex(v) for k,v in c.labels.items()},'bank1':{k:hex(v) for k,v in n.labels.items()}},changes=log),indent=2))
print('Built',out.name,sha,'| F',len(codeF),'3',len(code3),'1',len(code1))

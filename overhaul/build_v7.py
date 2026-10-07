# Creepy Black Mu v7: PRETA's Silph Scope sight, cleaner fossil Kabutops back sprite, PRETA's revival.
# Logged patches on top of verified Mu v6.
from pathlib import Path
import json,hashlib,re,io,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'ref'));import pic
M6=json.loads((ROOT/'manifest_v6.json').read_text());V6_SHA=M6['sha256']
src=(ROOT/'Creepy_Black_Mu_v6.gb').read_bytes();assert hashlib.sha256(src).hexdigest()==V6_SHA
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

# ---- verified engine addresses (signature-matched against pokered, see ref/sig.py) ----
ISITEMINBAG,PRINTTEXT,READPLAYERMON=0x34d5,0x3c94,0x4d6e
MAININBATTLELOOP=0x4233                              # bank F
KAB,SILPH_SCOPE=0xb6,0x48
REVIVE_TURNS=2
# New saved RAM (inside v1's NEW GAME clear range D450-D4AD): D461 PRETA revival countdown.
COUNT=0xd461
M3=json.loads((ROOT/'manifest_v3.json').read_text())['labels']
MIRAGE_POST=int(M3['bank2e']['mirage_post'],16)

# 1. PRETA in the party works like the SILPH SCOPE: IsGhostBattle (F) and PrintBeginningBattleText (16)
#    both ask IsItemInBag(SILPH_SCOPE); the hook answers "yes" (b=1, nz) when species B6 is in the party.
def scope_hook(c):
    c.label('scope');c.emit('21 64 d1')
    c.label('sloop');c.emit('2a fe ff');c.jr('28','none');c.emit('fe %02x'%KAB);c.jr('20','sloop')
    c.emit('06 01 78 a7 c9')
    c.label('none');c.emit('06 %02x c3 %s'%(SILPH_SCOPE,le(ISITEMINBAG)))
CALL='06 48 cd d5 34'.replace(' ','')
s16=Code(0x16,0x65c0);scope_hook(s16);code16=s16.finish();put(fo(0x16,0x65c0),code16,'Bank 16: PRETA counts as SILPH SCOPE')
patch(fo(0x16,0x4dd8),bytes.fromhex('cd'+le(s16.labels['scope'])+'0000'),'PrintBeginningBattleText: PRETA unveils ghosts',CALL)

# 3. Revival. Every pass through MainInBattleLoop (start of each turn) looks for a fainted PRETA in the
#    party: first sighting starts a countdown, after REVIVE_TURNS more turns it is restored to full HP
#    with no status and a message. After every battle a fainted PRETA is restored (before the Mirage
#    cleanup, so PRETA is never permanently lost there).
g=Code(0x2e,0x4700)
g.label('tick');g.emit('21 64 d1 11 6c d1 0e 00')                           # hl species, de HP, c index
g.label('tloop');g.emit('2a fe ff c8 fe %02x'%KAB);g.jr('20','tnext')
g.emit('1a 47 13 1a 1b b0');g.jr('20','tnext')                                # HP == 0 ?
g.emit('fa %s a7'%le(COUNT));g.jr('20','counting');g.emit('3e %02x'%(REVIVE_TURNS+1))
g.label('counting');g.emit('3d ea %s c0'%le(COUNT))                          # still waiting
g.ref('cd','restore')
g.emit('21 b5 d2 79 01 0b 00 cd bb 3a 11 6d cd 06 0b')                         # nickname -> wcd6d
g.label('ncopy');g.emit('2a 12 13 05');g.jr('20','ncopy')
g.ref('21','rose_text');g.emit('c3 '+le(PRINTTEXT))
g.label('tnext');g.emit('e5 21 2c 00 19 54 5d e1 0c');g.jr('18','tloop')
g.label('restore');g.emit('d5 21 21 00 19 2a 12 13 7e 12 d1 21 03 00 19 36 00 c9')   # HP = max HP, status 0
g.label('post')                                                                # after every battle
g.emit('af ea %s 21 64 d1 11 6c d1'%le(COUNT))
g.label('ploop');g.emit('2a fe ff');g.jr('28','pdone');g.emit('fe %02x'%KAB);g.jr('20','pnext')
g.emit('1a 47 13 1a 1b b0');g.jr('20','pnext');g.ref('cd','restore')
g.label('pnext');g.emit('e5 21 2c 00 19 54 5d e1');g.jr('18','ploop')
g.label('pdone');g.emit('c3 '+le(MIRAGE_POST))
g.label('rose_text');g.emit('01 6d cd 00');g.raw(enc(' rose')+b'\x4f'+enc('from the dead!')+b'\x58')
code2e=g.finish();put(fo(0x2e,0x4700),code2e,'Bank 2E: PRETA revival (battle countdown + after battle)')

f=Code(0xf,0x7e20)
scope_hook(f)
f.label('turn');f.emit(far(g.labels['tick'],0x2e)+' c3 '+le(READPLAYERMON))
codeF=f.finish();put(fo(0xf,0x7e20),codeF,'Bank F: PRETA scope + turn hooks')
patch(fo(0xf,0x5920),bytes.fromhex('cd'+le(f.labels['scope'])+'0000'),'IsGhostBattle: PRETA unveils ghosts',CALL)
patch(fo(0xf,MAININBATTLELOOP),bytes.fromhex('cd'+le(f.labels['turn'])),'MainInBattleLoop: PRETA revival tick','cd'+le(READPLAYERMON))
patch(0xc4,bytes.fromhex('21'+le(g.labels['post'])),'After every battle: restore fainted PRETA, then Mirage cleanup','21'+le(MIRAGE_POST))

# 2. Fossil Kabutops back sprite: the light-grey patches on its back become white (dark-grey ribs kept).
BACK=fo(0x0b,0x7f3c);OLD=(ROOT/'kab_back_v5.bin').read_bytes();SLOT=191   # v4 sprite length = space reserved
assert r[BACK:BACK+SLOT]==OLD.ljust(SLOT,b'\0')
d=bytearray(pic.decompress(io.BytesIO(bytes(r)),offset=BACK));assert len(d)==256
whitened=0
for i in range(0,256,2):                       # colour 1 (lo=1,hi=0) -> 0
    lo,hi=d[i],d[i+1];m1=lo&~hi&0xff;whitened+=bin(m1).count('1');d[i]=lo&~m1
new=bytes(pic.compress(bytes(d)));assert len(new)<=SLOT,len(new)
assert bytes(pic.decompress(io.BytesIO(new)))==bytes(d)
(ROOT/'kab_back_v7.bin').write_bytes(new)
patch(BACK,new.ljust(SLOT,b'\0'),'Fossil Kabutops back sprite: grey back patches -> white (%d px, %d bytes)'%(whitened,len(new)),OLD.ljust(SLOT,b'\0'))

# Header -----------------------------------------------------------------------
patch(0x134,b'CREEPY MU V7'.ljust(16,b'\0'),'Branch identity v7',b'CREEPY MU V6'.ljust(16,b'\0'))
v=0
for x in r[0x134:0x14d]:v=(v-x-1)&255
r[0x14d]=v;r[0x14e:0x150]=((sum(r[:0x14e])+sum(r[0x150:]))&65535).to_bytes(2,'big')
assert len(r)==1048576
out=ROOT/'Creepy_Black_Mu_v7.gb';out.write_bytes(r);sha=hashlib.sha256(r).hexdigest()
(ROOT/'manifest_v7.json').write_text(json.dumps(dict(input='Creepy_Black_Mu_v6.gb',input_sha256=V6_SHA,sha256=sha,size=len(r),
  labels={'bank2e':{k:hex(v) for k,v in g.labels.items()},'bankF':{k:hex(v) for k,v in f.labels.items()},'bank16':{k:hex(v) for k,v in s16.labels.items()}},changes=log),indent=2))
print('Built',out.name,sha,'| 2E',len(code2e),'F',len(codeF),'16',len(code16),'back',len(new),'whitened',whitened)

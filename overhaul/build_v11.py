# Creepy Black Mu v11: blacked-out GENTLEMAN as the Mirage trainer, AZHI knows DRAGON RAGE (DRAGONBREATH removed),
# BLACK FLAME never kills a person and spares GHOST / PRETA / AZHI. Logged patches on top of verified Mu v10.
from pathlib import Path
import json,hashlib,re,io,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'ref'));import pic
M10=json.loads((ROOT/'manifest_v10.json').read_text());V10_SHA=M10['sha256']
src=(ROOT/'Creepy_Black_Mu_v10.gb').read_bytes();assert hashlib.sha256(src).hexdigest()==V10_SHA
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





GHOST,KAB,AERO,DUMMY=0x1f,0xb6,0xb7,0x79
BLACKFLAME,DRAGONBREATH,FLY,DRAGON_RAGE,FIRE_BLAST=0xa8,0xaa,0x13,0x52,0x7e
MOVEHITTEST=0x6641
L10=M10['labels'];F10={k:int(v,16) for k,v in L10['bankF'].items()}
AERO_DATA=int(json.loads((ROOT/'manifest_v3.json').read_text())['labels']['bankE']['aero_data'],16)

# 1. Mirage trainer pic: the GENTLEMAN trainer pic (class 41, 13:73D0) with its outside flood-filled white and
#    everything else solid black (made by the snippet in README_v11). Same 91-byte slot as the v3 silhouette.
SIL=(ROOT/'mirage_gentleman_pic.bin').read_bytes();OLD=(ROOT/'mirage_pic.bin').read_bytes()
assert len(SIL)<=91;patch(fo(0x13,0x7fa5),SIL.ljust(91,b'\0'),'Mirage trainer pic: blacked-out GENTLEMAN',OLD.ljust(91,b'\0'))

# 2. AZHI: DRAGON RAGE instead of DRAGONBREATH; the DRAGONBREATH move (AA) is removed again.
mv=fo(0xe,AERO_DATA)+11
patch(mv,bytes([BLACKFLAME,FLY,DRAGON_RAGE,FIRE_BLAST]),'AZHI moves: BLACK FLAME, FLY, DRAGON RAGE, FIRE BLAST',bytes([BLACKFLAME,FLY,DRAGONBREATH,FIRE_BLAST]))
patch(fo(0xe,0x7d42),bytes(6),'Remove move data AA DRAGONBREATH',bytes([DRAGONBREATH,0x24,60,0x1a,0xff,20]))
patch(0xb0636,bytes(13),'Remove move name AA DRAGONBREATH',enc('DRAGONBREATH')+b'\x50')

# 3. BLACK FLAME faints every Pokemon on the target's side except GHOST, PRETA and AZHI. People are never harmed:
#    the player's stand-in "YOU" is unaffected (no save wipe) and nothing here touches the trainer-death flag.
#    The party faint now happens right after the move's hit test (so it also happens when the target itself is
#    one of the spared ones, which then gets "It doesn't affect ...").
g=Code(0x2e,0x4a00)
g.label('spared');g.emit('fe %02x c8 fe %02x c8 fe %02x c8 fe %02x c9'%(GHOST,KAB,AERO,DUMMY))     # z = spared
def faint_loop(c,tag,species,hp,active):
    c.emit('21 %s 11 %s 0e 00'%(le(species),le(hp)))
    c.label(tag+'l');c.emit('2a fe ff c8 47 fa %s b9'%le(active));c.jr('28',tag+'n')
    c.emit('78');c.ref('cd','spared');c.jr('28',tag+'n')
    c.emit('af 12 13 12 1b e5 21 03 00 19 77 e1')                                    # HP 0, status 0
    c.label(tag+'n');c.emit('e5 21 2c 00 19 54 5d e1 0c');c.jr('18',tag+'l')
g.label('faint_player');faint_loop(g,'fp',0xd164,0xd16c,0xcc2f)
g.label('faint_enemy');g.emit('fa 57 d0 fe 02 c0');faint_loop(g,'fe',0xd89d,0xd8a5,0xcfe8)
g.label('vs_player');g.ref('cd','faint_player');g.emit('fa 14 d0');g.ref('cd','spared');g.emit('c0');g.jr('18','immune')
g.label('vs_enemy');g.ref('cd','faint_enemy');g.emit('fa e5 cf');g.ref('cd','spared');g.emit('c0')
g.label('immune');g.emit('3e 01 ea 5f d0 af ea 5b d0 c9')
code2e=g.finish();put(fo(0x2e,0x4a00),code2e,'Bank 2E: BLACK FLAME v11 (spares GHOST/PRETA/AZHI and people)')

f=Code(0xf,0x7fc0)
f.label('ehit');f.emit('fa cc cf fe %02x c2 %s cd %s '%(BLACKFLAME,le(F10['ehit']),le(MOVEHITTEST))+far(g.labels['vs_player'],0x2e)+' c9')
f.label('phit');f.emit('fa d2 cf fe %02x c2 %s cd %s '%(BLACKFLAME,le(F10['phit']),le(MOVEHITTEST))+far(g.labels['vs_enemy'],0x2e)+' c9')
codeF=f.finish();assert 0x7fc0+len(codeF)<=0x8000;put(fo(0xf,0x7fc0),codeF,'Bank F: BLACK FLAME v11 hit-test hooks')
patch(fo(0xf,0x6865),bytes.fromhex('cd'+le(f.labels['ehit'])),'Enemy MoveHitTest -> v11 (BLACK FLAME)','cd'+le(F10['ehit']))
patch(fo(0xf,0x57d3),bytes.fromhex('cd'+le(f.labels['phit'])),'Player MoveHitTest -> v11 (BLACK FLAME)','cd'+le(F10['phit']))
# The v10 damage hooks still knock out the (non-spared) target; their party sweeps now use the v11 loops.
patch(fo(0xf,F10['bf']+8),bytes.fromhex(le(g.labels['faint_player'])),'v10 BLACK FLAME damage hook -> v11 party faint',le(L10 and int(L10['bank2e']['bf_player'],16)))
patch(fo(0xf,F10['pdmg']+9),bytes.fromhex(le(g.labels['faint_enemy'])),'v10 player BLACK FLAME damage hook -> v11 party faint',le(int(L10['bank2e']['bf_enemy'],16)))

# Header -----------------------------------------------------------------------
patch(0x134,b'CREEPY MU V11'.ljust(16,b'\0'),'Branch identity v11',b'CREEPY MU V10'.ljust(16,b'\0'))
v=0
for x in r[0x134:0x14d]:v=(v-x-1)&255
r[0x14d]=v;r[0x14e:0x150]=((sum(r[:0x14e])+sum(r[0x150:]))&65535).to_bytes(2,'big')
assert len(r)==1048576
out=ROOT/'Creepy_Black_Mu_v11.gb';out.write_bytes(r);sha=hashlib.sha256(r).hexdigest()
(ROOT/'manifest_v11.json').write_text(json.dumps(dict(input='Creepy_Black_Mu_v10.gb',input_sha256=V10_SHA,sha256=sha,size=len(r),
  labels={'bankF':{k:hex(v) for k,v in f.labels.items()},'bank2e':{k:hex(v) for k,v in g.labels.items()}},changes=log),indent=2))
print('Built',out.name,sha,'| F',len(codeF),'2E',len(code2e))

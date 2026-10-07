# Creepy Black Mu v10: the Mirage trainer is "?????", species B7 is AZHI (BLACK FLAME / FLY / DRAGONBREATH /
# FIRE BLAST), BLACK FLAME faints the whole opposing party, AZHI is immune to CURSE, MACABRE and BLACK FLAME.
# Logged patches on top of verified Mu v9.
from pathlib import Path
import json,hashlib,re,io,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'ref'));import pic
M9=json.loads((ROOT/'manifest_v9.json').read_text());V9_SHA=M9['sha256']
src=(ROOT/'Creepy_Black_Mu_v9.gb').read_bytes();assert hashlib.sha256(src).hexdigest()==V9_SHA
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




KAB,AERO,DUMMY=0xb6,0xb7,0x79
CURSE,MACABREBLADE,BLACKFLAME,MACABRE,DRAGONBREATH=0xa5,0xa7,0xa8,0xa9,0xaa
FLY,FIRE_BLAST,SLASH,DRAGON_RAGE=0x13,0x7e,0xa3,0x52
MOVEHITTEST,PLAYMOVEANIM,ISGHOSTBATTLE=0x6641,0x6fed,0x5910
L3=json.loads((ROOT/'manifest_v3.json').read_text())['labels']
FLASH=int(L3['bank2e']['flash'],16);OLD_DMG=int(L3['bankF']['dmg'],16);KILL=int(L3['bankF']['kill'],16)
MIRAGE_DEATH=int(L3['bank2e']['mirage_death'],16);AERO_DATA=int(L3['bankE']['aero_data'],16)
OLD_PDMG=int(json.loads((ROOT/'manifest_v6.json').read_text())['labels']['bankF']['pdmg'],16)
SCARED=int(L3['bankF']['scared'],16)

# 1. Names: trainer class 13 "BLACK TAMER" -> "?????", species B7 "AERODACTYL" -> "AZHI".
TN=0x39a3d;names=r[TN:TN+400].split(b'\x50')[:47];old=b'\x50'.join(names)+b'\x50'
assert names[12]==enc('BLACK TAMER');names[12]=enc('?????')
new=b'\x50'.join(names)+b'\x50';patch(TN,new.ljust(len(old),b'\x50'),'Trainer class 13 name BLACK TAMER -> ?????',old)
NAMES=0x1c21e;o=NAMES+10*(AERO-1)
patch(o,enc('AZHI').ljust(10,b'\x50'),'Species name B7 = AZHI',enc('AERODACTYL').ljust(10,b'\x50'))

# 2. New move AA DRAGONBREATH (Gen-2 style: DRAGON, 60 power, 100%, 20 PP, 30% paralysis = Body Slam effect).
put(fo(0xe,0x7d42),bytes([DRAGONBREATH,0x24,60,0x1a,0xff,20]),'Move data AA DRAGONBREATH (death-move table entry 4)')
assert r[0xb0635]==0x50;put(0xb0636,enc('DRAGONBREATH')+b'\x50','Move name AA = DRAGONBREATH')
# AZHI knows BLACK FLAME, FLY, DRAGONBREATH, FIRE BLAST (initial moves in its custom header).
mv=fo(0xe,AERO_DATA)+11
patch(mv,bytes([BLACKFLAME,FLY,DRAGONBREATH,FIRE_BLAST]),'AZHI moves: BLACK FLAME, FLY, DRAGONBREATH, FIRE BLAST',bytes([BLACKFLAME,0,0,0]))

# 3. BLACK FLAME faints every Pokemon in the opposing party (never misses, typeless, Fire Blast animation +
#    black flash). Opposing AZHI and the player's stand-in (only the active target can be "YOU") are spared.
g=Code(0x2e,0x4900)
g.label('bf_player')          # enemy used BLACK FLAME: every player party mon except the active one, AZHI, YOU
g.emit('21 64 d1 11 6c d1 0e 00')
g.label('bpl');g.emit('2a fe ff c8 47 fa 2f cc b9');g.jr('28','bpn')
g.emit('78 fe %02x'%AERO);g.jr('28','bpn');g.emit('fe %02x'%DUMMY);g.jr('28','bpn')
g.emit('af 12 13 12 1b e5 21 03 00 19 77 e1')                                   # HP 0, status 0
g.label('bpn');g.emit('e5 21 2c 00 19 54 5d e1 0c');g.jr('18','bpl')
g.label('bf_enemy')           # player used BLACK FLAME in a trainer battle: every other enemy party mon except AZHI
g.emit('fa 57 d0 fe 02 c0 21 9d d8 11 a5 d8 0e 00')
g.label('bel');g.emit('2a fe ff c8 47 fa e8 cf b9');g.jr('28','ben')
g.emit('78 fe %02x'%AERO);g.jr('28','ben')
g.emit('af 12 13 12 1b e5 21 03 00 19 77 e1')
g.label('ben');g.emit('e5 21 2c 00 19 54 5d e1 0c');g.jr('18','bel')
code2e=g.finish();put(fo(0x2e,0x4900),code2e,'Bank 2E: BLACK FLAME party faint')

f=Code(0xf,0x7ea0)
def immune(c):c.emit('3e 01 ea 5f d0 af ea 5b d0 c9')        # missed + x0 = "It doesn't affect ..."
# player's attack: MACABRE vs PRETA/AZHI, CURSE and BLACK FLAME vs AZHI
f.label('phit');f.emit('cd %s fa e5 cf 47 fa d2 cf fe %02x'%(le(MOVEHITTEST),MACABRE));f.jr('28','p_both')
f.emit('fe %02x'%CURSE);f.jr('28','p_azhi');f.emit('fe %02x'%BLACKFLAME);f.jr('28','p_azhi');f.emit('c9')
f.label('p_both');f.emit('78 fe %02x'%KAB);f.jr('28','p_imm')
f.label('p_azhi');f.emit('78 fe %02x c0'%AERO)
f.label('p_imm');immune(f)
# enemy's attack: MACABREBLADE vs PRETA, MACABRE vs PRETA/AZHI, BLACK FLAME vs AZHI
f.label('ehit');f.emit('cd %s fa 14 d0 47 fa cc cf fe %02x'%(le(MOVEHITTEST),MACABREBLADE));f.jr('28','e_kab')
f.emit('fe %02x'%MACABRE);f.jr('28','e_both');f.emit('fe %02x'%BLACKFLAME);f.jr('28','e_azhi');f.emit('c9')
f.label('e_both');f.emit('78 fe %02x'%AERO);f.jr('28','e_imm')
f.label('e_kab');f.emit('78 fe %02x c0'%KAB);f.jr('18','e_imm')
f.label('e_azhi');f.emit('78 fe %02x c0'%AERO)
f.label('e_imm');immune(f)
# damage to the player's Pokemon: BLACK FLAME kills the target and the rest of the party; MACABREBLADE keeps the
# v3 death-move rule; other moves (FLY, DRAGONBREATH, FIRE BLAST) do normal damage, except that any hit on the
# player's stand-in in a Mirage battle is still fatal.
f.label('dmg');f.emit('fa cc cf fe %02x ca %s fe %02x'%(MACABREBLADE,le(OLD_DMG),BLACKFLAME));f.jr('28','bf')
f.emit('fa 5d d4 a7');f.jr('28','dret');f.emit('fa 14 d0 fe %02x'%DUMMY);f.jr('20','dret')
f.label('wipe');f.emit(far(MIRAGE_DEATH,0x2e))
f.label('bf');f.emit('fa 14 d0 fe %02x'%DUMMY);f.jr('28','wipe');f.emit(far(g.labels['bf_player'],0x2e)+' c3 '+le(KILL))
f.label('dret');f.emit('21 d7 d0 c9')
# damage to the enemy: BLACK FLAME kills the target and the rest of a trainer's party
f.label('pdmg');f.emit('fa d2 cf fe %02x c2 %s'%(BLACKFLAME,le(OLD_PDMG))+' '+far(g.labels['bf_enemy'],0x2e))
f.emit('3e 03 ea d7 d0 3e e7 ea d8 d0 af ea 5e d0 21 d7 d0 c9')
# animations (both sides): MACABREBLADE/MACABRE = Slash, BLACK FLAME = Fire Blast, DRAGONBREATH = Dragon Rage;
# the two death moves end with the black flash.
f.label('anim');f.emit('fe %02x da %s'%(MACABREBLADE,le(PLAYMOVEANIM)))
f.emit('47 fe %02x 3e %02x'%(BLACKFLAME,FIRE_BLAST));f.jr('28','ago');f.emit('78 fe %02x 3e %02x'%(DRAGONBREATH,DRAGON_RAGE));f.jr('28','ago');f.emit('3e %02x'%SLASH)
f.label('ago');f.emit('c5 cd %s c1 78 fe %02x'%(le(PLAYMOVEANIM),MACABRE));f.emit('d0 '+far(FLASH,0x2e)+' c9')
# PRETA and AZHI are never "too scared" in Mirage battles
f.label('scared');f.emit('fa 14 d0 fe %02x ca %s fe %02x ca %s c3 %s'%(KAB,le(ISGHOSTBATTLE),AERO,le(ISGHOSTBATTLE),le(SCARED)))
# CURSE vs AZHI: the base game arms its curse kill (flag CC39) when CURSE is chosen; don't arm it against AZHI,
# so CURSE becomes an ordinary move that "doesn't affect" AZHI (phit above).
f.label('curse');f.emit('fa e5 cf fe %02x c8 3e 01 ea 39 cc c9'%AERO)
f.label('eff01');f.emit('f0 f3 a7 c2 eb 72 fa d2 cf fe %02x c2 eb 72 fa e5 cf fe %02x c2 eb 72'%(CURSE,AERO))   # CURSE's effect hook
f.emit('21 2d 5d c3 94 3c')                                                       # "It doesn't affect <enemy>!"
codeF=f.finish();assert 0x7ea0+len(codeF)<=0x8000;put(fo(0xf,0x7ea0),codeF,'Bank F: AZHI / BLACK FLAME / DRAGONBREATH hooks')
for addr,lab,old,name in ((0x57d3,'phit','cd507e','Player MoveHitTest -> v10 immunities'),(0x6865,'ehit','cd807e','Enemy MoveHitTest -> v10 immunities'),
                          (0x62d6,'dmg','cd637d','ApplyDamageToPlayerPokemon -> BLACK FLAME / death moves'),(0x6218,'pdmg','cde07d','ApplyDamageToEnemyPokemon -> BLACK FLAME'),
                          (0x689f,'anim','cd867d','Enemy move animation -> v10 table'),(0x5804,'anim','cd047e','Player move animation -> v10 table'),
                          (0x58e2,'scared','cd6d7e','PrintGhostText: PRETA and AZHI never too scared')):
    patch(fo(0xf,addr),bytes.fromhex('cd'+le(f.labels[lab])),name,old)
patch(fo(0xf,0x723f),bytes.fromhex(le(f.labels['eff01'])),'Effect 01 (CURSE): says it does not affect AZHI','eb72')
patch(fo(0xf,0x572d),bytes.fromhex('cd'+le(f.labels['curse'])+'0000'),'CURSE chosen: no curse kill against AZHI','3e01ea39cc')
for addr,lab,old,name in ():
    patch(fo(0xf,addr),bytes.fromhex('cd'+le(f.labels[lab])),name,old)

# Header -----------------------------------------------------------------------
patch(0x134,b'CREEPY MU V10'.ljust(16,b'\0'),'Branch identity v10',b'CREEPY MU V9'.ljust(16,b'\0'))
v=0
for x in r[0x134:0x14d]:v=(v-x-1)&255
r[0x14d]=v;r[0x14e:0x150]=((sum(r[:0x14e])+sum(r[0x150:]))&65535).to_bytes(2,'big')
assert len(r)==1048576
out=ROOT/'Creepy_Black_Mu_v10.gb';out.write_bytes(r);sha=hashlib.sha256(r).hexdigest()
(ROOT/'manifest_v10.json').write_text(json.dumps(dict(input='Creepy_Black_Mu_v9.gb',input_sha256=V9_SHA,sha256=sha,size=len(r),
  labels={'bankF':{k:hex(v) for k,v in f.labels.items()},'bank2e':{k:hex(v) for k,v in g.labels.items()}},changes=log),indent=2))
print('Built',out.name,sha,'| F',len(codeF),'2E',len(code2e))

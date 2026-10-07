# Creepy Black Mu v3: the Mirage Black Tamer. Logged patches on top of verified Mu v2.
from pathlib import Path
import json,hashlib,re
ROOT=Path(__file__).resolve().parent
V2_SHA='e7855fae19f3c8c3ee1c9a3791a13e6804836b0a0f25bc67893f8e3bfd4d280d'
src=(ROOT/'Creepy_Black_Mu_v2.gb').read_bytes();assert hashlib.sha256(src).hexdigest()==V2_SHA
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

# ---- verified engine addresses (signature-matched against pokered, see ref/) ----
BANKSWITCH,PLAYCRY,DELAYFRAMES,ADDNTIMES=0x3618,0x13ff,0x3773,0x3abb
ISGHOSTBATTLE,CANTESCAPE,BATTLERANDOM,PLAYMOVEANIM=0x5910,0x4b6d,0x6f81,0x6fed   # bank F
MOVEMON=(3,0x784d);REMOVEMON=(1,0x7b61)
V2=json.loads((ROOT/'manifest_v2.json').read_text())['labels_bank2e']
BLACK_ON,BLACK_OFF=int(V2['black_on'],16),int(V2['black_off'],16)
WIPE_AND_RESET=int(V2['eat_player'],16)+13      # v2: SRAM wipe + cold restart (after its cry/delay)
GHOST,KAB,AERO,DUMMY=0x1f,0xb6,0xb7,0x79       # DUMMY = unused MISSINGNO slot whose pics live in bank C
MACABRE,BLACKFLAME=0xa7,0xa8
CLASS=13;OPP=0xc8+CLASS                         # unused JUGGLER class -> BLACK TAMER
# New saved RAM: D45C Ghost-use counter, D45D Mirage battle active, D45E party alive-at-start mask,
# D45F Ghost was deposited for the fight. (All inside v1's NEW GAME clear range D450-D4AD.)
TUNING=dict(per_curse=2,chance_cap=64,run_success=166)   # chance/256 = min(uses*2,64); run 166/256 = 65%

# 1. Silhouette trainer pic (player front pic, flood-filled solid black) -> bank 13 free space
SIL=(ROOT/'mirage_pic.bin').read_bytes();assert len(SIL)<=91
SIL_ADDR=0x7fa5;put(fo(0x13,SIL_ADDR),SIL,'Mirage Black Tamer silhouette pic')

# 2. Bank E: species headers, move data, trainer parties, bank-E move reader
e=Code(0xe,0x7c60)
e.label('special_header');e.emit('fa b5 d0 fe %02x'%KAB);e.jr('28','kab');e.emit('fe %02x'%AERO);e.jr('28','aero')
e.emit('fe %02x'%DUMMY);e.jr('28','dummy')
e.label('fin');e.emit('fa b5 d0 ea b8 d0 c9')                     # replaced GetMonHeader instructions
e.label('kab');e.ref('21','kab_data');e.jr('18','partial')
e.label('aero');e.ref('21','aero_data')
e.label('partial');e.emit('11 b9 d0 06 09');e.ref('cd','copyb');e.emit('11 c5 d0 06 0f');e.ref('cd','copyb');e.jr('18','fin')
e.label('dummy');e.ref('21','dummy_hdr');e.emit('11 b9 d0 06 1b');e.ref('cd','copyb');e.jr('18','fin')
e.label('copyb');e.emit('2a 12 13 05');e.jr('20','copyb');e.emit('c9')
# fossil headers: hp atk def spd spc | type1 type2 | catch | exp  ;  back ptr | 4 moves | growth | 7 TM bytes | pad
e.label('kab_data');e.raw([60,115,105,80,70, 0x08,0x05, 0,0]);e.raw(bytes.fromhex(le(0x79e8)));e.raw([MACABRE,0,0,0,5]+[0]*8)
e.label('aero_data');e.raw([80,105,65,130,60, 0x08,0x02, 0,0]);e.raw(bytes.fromhex(le(0x6536)));e.raw([BLACKFLAME,0,0,0,5]+[0]*8)
# the player as a party member: stats, normal type, dims, front/back = player back pic (bank C), one move
e.label('dummy_hdr');e.raw([15,5,5,5,5, 0,0, 0,0, 0x44]);e.raw(bytes.fromhex(le(0x7e0a)*2));e.raw([0x21,0,0,0,0]+[0]*8)
# move data: id, effect (SWIFT = never misses), power, type (Curse's 0x1B: no type-chart entries), acc, pp
e.label('mymoves');e.raw([MACABRE,0x11,250,0x1b,0xff,10, BLACKFLAME,0x11,250,0x1b,0xff,10])
e.label('party');e.raw([50,KAB,0, 50,AERO,0])                      # trainer 1 = Kabutops, 2 = Aerodactyl
def movehelper(c,tbl_addr):
    c.label('movehelper');c.emit('fe a6');c.jr('30','mine');c.emit('21 00 40 01 06 00 c3 '+le(ADDNTIMES))
    c.label('mine');c.emit('d6 a6 4f 87 81 87 4f 06 00 21 '+le(tbl_addr)+' 09 01 06 00 c9')
MYMOVES=e.labels['mymoves']
movehelper(e,MYMOVES)
codeE=e.finish();put(fo(0xe,0x7c60),codeE,'Bank E: fossil/dummy headers, death moves, Black Tamer party')

# 3. Bank 2e: encounter conversion, post-battle cleanup, death, flash
g=Code(0x2e,0x4300)
g.label('mirage_start')
g.emit('fa 51 d4 a7 c8 fa 90 d7 cb 7f c0 fa 5d d4 a7 c0 fa 5c d4 a7 c8')       # Ghost owned, not Safari, counter>0
g.emit('4f af');g.label('chance');g.emit('c6 %02x'%TUNING['per_curse']);g.jr('38','cap');g.emit('fe %02x'%TUNING['chance_cap']);g.jr('30','cap')
g.emit('0d');g.jr('20','chance');g.jr('18','have');g.label('cap');g.emit('3e %02x'%TUNING['chance_cap'])
g.label('have');g.emit('47 f0 d3 b8 d0')                                    # random >= chance -> normal wild battle
g.emit('21 64 d1 0e 00');g.label('find');g.emit('2a fe ff');g.jr('28','noghost');g.emit('fe %02x'%GHOST);g.jr('28','ghost');g.emit('0c');g.jr('18','find')
g.label('ghost');g.emit('fa 80 da fe 14 d0')                                 # PC box full -> no Mirage
g.emit('79 ea 92 cf 3e %02x ea 91 cf 3e 01 ea 95 cf '%GHOST+far(MOVEMON[1],MOVEMON[0]))   # deposit Ghost
g.emit('af ea 95 cf '+far(REMOVEMON[1],REMOVEMON[0])+' 3e 01 ea 5f d4')
g.label('noghost')
g.emit('21 6c d1 fa 63 d1 4f 06 00 1e 01')                                   # alive-at-start mask
g.label('mask');g.emit('79 a7');g.jr('28','maskdone');g.emit('2a b6');g.jr('28','dead');g.emit('78 b3 47')
g.label('dead');g.emit('c5 01 2b 00 09 c1 cb 23 0d');g.jr('18','mask')
g.label('maskdone');g.emit('78 ea 5e d4')
g.emit('fa 63 d1 4f 3c ea 63 d1 21 64 d1 06 00 09 3e %02x 22 3e ff 77'%DUMMY)   # append dummy species
g.emit('21 6b d1 79 01 2c 00 cd '+le(ADDNTIMES));g.ref('11','dummy_struct');g.emit('06 2c')
g.label('cpy');g.emit('1a 22 13 05');g.jr('20','cpy')
g.emit('fa 63 d1 3d f5 21 73 d2 01 0b 00 cd '+le(ADDNTIMES));g.ref('cd','copyname')     # OT name = player
g.emit('f1 21 b5 d2 01 0b 00 cd '+le(ADDNTIMES));g.ref('cd','copyname')                # nickname = player
g.emit('3e %02x ea 59 d0 ea d8 cf f0 d4 e6 01 3c ea 5d d0 3e 01 ea 5d d4 c9'%OPP)      # become Black Tamer battle
g.label('copyname');g.emit('11 58 d1 06 0b');g.label('cn');g.emit('1a 22 13 05');g.jr('20','cn');g.emit('c9')
# dummy party struct (44 bytes): species,hp(2),boxlvl,status,types(2),catch,moves(4),otid(2),exp(3),statexp(10),dvs(2),pp(4),lvl,stats(10)
g.label('dummy_struct');g.raw([DUMMY,0,15,5,0,0,0,0, 0x21,0,0,0, 0,0, 0,0,0]+[0]*10+[0,0, 35,0,0,0, 5, 0,15,0,5,0,5,0,5,0,5])
g.label('mirage_post')
g.emit('fa 5d d4 a7 c8 af ea 5d d4 ea 59 d0 fa 63 d1 4f')
g.label('rloop');g.emit('79 a7');g.jr('28','rdone');g.emit('0d 21 64 d1 06 00 09 7e fe %02x'%DUMMY);g.jr('28','remove')
g.emit('1e 01 41');g.label('bit');g.emit('78 a7');g.jr('28','bitdone');g.emit('cb 23 05');g.jr('18','bit')
g.label('bitdone');g.emit('fa 5e d4 a3');g.jr('28','rloop')                      # fainted before the fight: keep
g.emit('21 6c d1 79 c5 01 2c 00 cd '+le(ADDNTIMES)+' c1 2a b6');g.jr('20','rloop') # still alive: keep
g.label('remove');g.emit('79 ea 92 cf af ea 95 cf c5 '+far(REMOVEMON[1],REMOVEMON[0])+' c1');g.jr('18','rloop')
g.label('rdone');g.emit('fa 5f d4 a7 c8 af ea 5f d4')
g.emit('fa 80 da a7 c8 3d 4f 21 81 da 06 00 09 7e fe %02x c0'%GHOST)              # Ghost is last in box
g.emit('79 ea 92 cf 3e %02x ea 91 cf af ea 95 cf '%GHOST+far(MOVEMON[1],MOVEMON[0]))
g.emit('3e 01 ea 95 cf '+far(REMOVEMON[1],REMOVEMON[0])+' c9')
g.label('mirage_death');g.emit('cd '+le(BLACK_ON)+' fa e5 cf cd '+le(PLAYCRY)+' 0e 78 cd '+le(DELAYFRAMES)+' c3 '+le(WIPE_AND_RESET))
g.label('flash');g.emit('cd '+le(BLACK_ON)+' 0e 14 cd '+le(DELAYFRAMES)+' c3 '+le(BLACK_OFF))
code2e=g.finish();put(fo(0x2e,0x4300),code2e,'Bank 2E: Mirage encounter, cleanup, death, flash')

# 4. Bank F: run / scared / damage / animation / move reader / Curse counter
f=Code(0xf,0x7d40)
f.label('scared');f.emit('fa 5d d4 a7 ca %s f0 f3 a7 c2 %s af c9'%(le(ISGHOSTBATTLE),le(ISGHOSTBATTLE)))
f.label('run');f.emit('fa 5d d4 a7 ca %s cd %s fe %02x'%(le(ISGHOSTBATTLE),le(BATTLERANDOM),TUNING['run_success']));f.jr('30','runfail');f.emit('af c9')
f.label('runfail');f.emit('e1 c3 '+le(CANTESCAPE))
f.label('dmg');f.emit('fa 5d d4 a7');f.jr('28','dmgret');f.emit('fa 14 d0 fe %02x'%DUMMY);f.jr('20','kill')
f.emit(far(g.labels['mirage_death'],0x2e))
f.label('kill');f.emit('3e 03 ea d7 d0 3e e7 ea d8 d0')
f.label('dmgret');f.emit('21 d7 d0 c9')
f.label('anim');f.emit('fe %02x da %s fe %02x 3e a3'%(MACABRE,le(PLAYMOVEANIM),MACABRE));f.jr('28','animgo');f.emit('3e 7e')
f.label('animgo');f.emit('cd '+le(PLAYMOVEANIM)+' '+far(g.labels['flash'],0x2e)+' c9')
f.label('cursecnt');f.emit('3e 01 ea 52 d4 e5 21 5c d4')
f.emit('34 20 01 35 e1 c9')                                    # counter += 1, saturating at 255
movehelper(f,MYMOVES)
codeF=f.finish();put(fo(0xf,0x7d40),codeF,'Bank F: Mirage battle hooks')
patch(fo(0xf,0x58e2),bytes.fromhex('cd'+le(f.labels['scared'])),'PrintGhostText: your Pokemon are too scared in Mirage battles','cd1059')
patch(fo(0xf,0x4ae4),bytes.fromhex('cd'+le(f.labels['run'])),'TryRunningFromBattle: 65% run in Mirage battles','cd1059')
patch(fo(0xf,0x62d6),bytes.fromhex('cd'+le(f.labels['dmg'])),'ApplyDamageToPlayerPokemon: death moves kill / wipe','21d7d0')
patch(fo(0xf,0x689f),bytes.fromhex('cd'+le(f.labels['anim'])),'Enemy move animation: death-move visuals','cded6f')
patch(fo(0xf,0x7d08),bytes.fromhex('cd'+le(f.labels['cursecnt'])+'0000'),'Curse use also raises Ghost-use counter','3e01ea52d4')
READER='21 00 40 01 06 00 cd bb 3a'
for o,name in ((0x6403,'f6403'),(0x6bc6,'GetCurrentMove')):
    patch(fo(0xf,o),bytes.fromhex('cd'+le(f.labels['movehelper']))+bytes(6),'Move reader '+name+' -> death moves',READER.replace(' ',''))
patch(fo(0xe,0x58c6),bytes.fromhex('cd'+le(e.labels['movehelper']))+bytes(6),'AI move reader -> death moves',READER.replace(' ',''))
m3=Code(3,0x7fb0);movehelper(m3,MYMOVES);code3=m3.finish();put(fo(3,0x7fb0),code3,'Bank 3 move reader helper')
patch(fo(3,0x77af),bytes.fromhex('cd'+le(m3.labels['movehelper']))+bytes(6),'LoadMovePPs -> death moves',READER.replace(' ',''))

# 5. GetMonHeader exit (bank E switched in) -> custom headers
patch(0x15c6,bytes.fromhex('cd'+le(e.labels['special_header'])+'000000'),'GetMonHeader: fossil/dummy headers','fab5d0eab8d0')

# 6. Encounter hook: TryDoWildEncounter success path -> maybe Mirage
w=Code(4,0x7aec);w.emit(far(g.labels['mirage_start'],0x2e)+' af c9');codeW=w.finish();put(fo(4,0x7aec),codeW,'Bank 4 Mirage roll stub')
patch(fo(4,0x795e),bytes.fromhex('f6 01 c9 c3'+le(0x7aec)),'Encounter exit: can\'t = or 1/ret, will = jp Mirage roll','3e01a7c9afc9')
patch(fo(4,0x7944),[0x1c],'retarget jr z -> 0x7961','1d')
patch(fo(4,0x7950),[0x10],'retarget jr -> 0x7961','11')
# 7. Post-battle cleanup after every NewBattle (home padding 0x00C0)
patch(0xc0,bytes.fromhex('cd 90 06 f5 '+far(g.labels['mirage_post'],0x2e)+' f1 c9'),'Home: NewBattle then Mirage cleanup','00'*14)
patch(0x639,bytes.fromhex('cd c0 00'),'Overworld NewBattle call -> wrapper','cd9006')
patch(0x582,bytes.fromhex('cd c0 00'),'Step NewBattle call -> wrapper','cd9006')

# 8. Data tables
cm={}
for k,v in re.findall(r'^\s*charmap "([^"]+)",\s*\$([0-9A-Fa-f]+)',(ROOT.parent/'pokeblack/charmap.asm').read_text(encoding='utf8'),re.M):cm.setdefault(k,int(v,16))
def enc(s):return bytes(cm[c] for c in s)
NAMES=0x1c21e
for sp,nm in ((KAB,'KABUTOPS'),(AERO,'AERODACTYL'),(DUMMY,'YOU')):
    o=NAMES+10*(sp-1);patch(o,enc(nm).ljust(10,b'\x50'),'Species name %02x = %s'%(sp,nm),r[o:o+10])
DEX=0x4102e
patch(DEX+KAB-1,[141],'Fossil Kabutops dex -> Kabutops (seen flag safety)','00')
patch(DEX+AERO-1,[142],'Fossil Aerodactyl dex -> Aerodactyl (seen flag safety)','00')
CRY=0x39484
patch(CRY+3*(KAB-1),bytes.fromhex('18ee01'),'Fossil Kabutops cry = Kabutops','000000')
patch(CRY+3*(AERO-1),bytes.fromhex('2320f0'),'Fossil Aerodactyl cry = Aerodactyl','000000')
assert r[0xb0614]==0x50
put(0xb0615,enc('MACABREBLADE')+b'\x50'+enc('BLACK FLAME')+b'\x50','Move names A7/A8')
PICMONEY=0x39952;o=PICMONEY+5*(CLASS-1)
patch(o,bytes.fromhex(le(SIL_ADDR)+'000000'),'Class 13 pic = silhouette, no prize money',r[o:o+5])
TDP=0x39d79;o=TDP+2*(CLASS-1)
patch(o,bytes.fromhex(le(e.labels['party'])),'Class 13 party data -> Fossil Kabutops / Aerodactyl Lv50',r[o:o+2])
TN=0x39a3d;names=r[TN:TN+400].split(b'\x50')[:47];old=b'\x50'.join(names)+b'\x50'
names[CLASS-1]=enc('BLACK TAMER');names[25]=enc('OAK')
new=b'\x50'.join(names)+b'\x50';assert len(new)<=len(old)
patch(TN,new.ljust(len(old),b'\x50'),'Trainer class names: JUGGLER(13) -> BLACK TAMER, PROF.OAK -> OAK',old)

# Header -----------------------------------------------------------------------
patch(0x134,b'CREEPY MU V3'.ljust(16,b'\0'),'Branch identity v3',b'CREEPY MU V2'.ljust(16,b'\0'))
v=0
for x in r[0x134:0x14d]:v=(v-x-1)&255
r[0x14d]=v;r[0x14e:0x150]=((sum(r[:0x14e])+sum(r[0x150:]))&65535).to_bytes(2,'big')
assert len(r)==1048576
out=ROOT/'Creepy_Black_Mu_v3.gb';out.write_bytes(r);sha=hashlib.sha256(r).hexdigest()
(ROOT/'manifest_v3.json').write_text(json.dumps(dict(input='Creepy_Black_Mu_v2.gb',input_sha256=V2_SHA,sha256=sha,size=len(r),tuning=TUNING,
  labels={'bank2e':{k:hex(v) for k,v in g.labels.items()},'bankF':{k:hex(v) for k,v in f.labels.items()},'bankE':{k:hex(v) for k,v in e.labels.items()}},changes=log),indent=2))
print('Built',out.name,sha,'| 2E',len(code2e),'F',len(codeF),'E',len(codeE))

# Creepy Black Mu v6: Mr. Mu in the Cerulean trade house, the DOME FOSSIL question, PRETA and MACABRE.
# Logged patches on top of verified Mu v5.
from pathlib import Path
import json,hashlib,re
ROOT=Path(__file__).resolve().parent
M5=json.loads((ROOT/'manifest_v5.json').read_text());V5_SHA=M5['sha256']
src=(ROOT/'Creepy_Black_Mu_v5.gb').read_bytes();assert hashlib.sha256(src).hexdigest()==V5_SHA
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

# ---- verified engine addresses (signature-matched against pokered, see ref/sig.py) ----
PRINTTEXT,TEXTSCRIPTEND,HANDLEMENUINPUT,ADDNTIMES,PLAYSOUND=0x3c94,0x2504,0x3af2,0x3abb,0x23de
REMOVEITEMBYID=(5,0x7f51)
PLAYMOVEANIM=0x6fed                                   # bank F
M2=json.loads((ROOT/'manifest_v2.json').read_text())['labels_bank2e']
BLACK_ON,BLACK_OFF=int(M2['black_on'],16),int(M2['black_off'],16)
M3=json.loads((ROOT/'manifest_v3.json').read_text())['labels']
KAB_DATA=int(M3['bankE']['kab_data'],16);OLD_MOVES=int(M3['bankE']['mymoves'],16)
KAB,DOME,MACABRE,SLASH,CUT,SURF,STRENGTH=0xb6,0x29,0xa9,0xa3,0x0f,0x39,0x46
MUSIC_PKMN_HEALED=0xe8
GENTLEMAN=0x10
# New saved RAM (inside v1's NEW GAME clear range D450-D4AD): D460 Cerulean Mu state
# (0 not met, 1 introduced, 2 Preta awakened). D457 = temp party index while adding Preta.
MU2=0xd460

cm={}
for k,v in re.findall(r'^\s*charmap "([^"]+)",\s*\$([0-9A-Fa-f]+)',(ROOT.parent/'pokeblack/charmap.asm').read_text(encoding='utf8'),re.M):cm.setdefault(k,int(v,16))
def enc(s):
    out=bytearray()
    while s:
        k=next(k for k in sorted(cm,key=len,reverse=True) if s.startswith(k));out.append(cm[k]);s=s[len(k):]
    return out
def shown(line):return len(line.replace('#','POKé').replace('<PLAYER>','X'*7))
def txt(paras,end=0x58,maxw=17):
    out=bytearray([0])
    for i,p in enumerate(paras):
        if i:out.append(0x51)
        for j,line in enumerate(p):
            assert shown(line)<=maxw,line
            if j:out.append(0x4f if j==1 else 0x55)
            out+=enc(line)
    out.append(end);return out
DIALOGUE=json.loads((ROOT/'dialogue_v6.json').read_text(encoding='utf8'))

# 1. MACABRE (move A9): never misses (SWIFT effect), typeless 0x1B, Slash animation,
#    and the damage is replaced by "target HP - 1" (it always leaves the enemy at 1 HP).
#    Move data table for A7..A9 is moved to a bigger spot in bank E; the three move-reader helpers are repointed.
old_tbl=bytes(r[fo(0xe,OLD_MOVES):fo(0xe,OLD_MOVES)+12])
NEW_MOVES=0x7d30
put(fo(0xe,NEW_MOVES),old_tbl+bytes([MACABRE,0x11,70,0x1b,0xff,10]),'Bank E: death-move table + MACABRE')
for bank,ptr in ((0xe,int(M3['bankE']['mine'],16)+10),(0xf,int(M3['bankF']['mine'],16)+10),(3,0x7fbd+10)):
    patch(fo(bank,ptr-1),bytes.fromhex('21'+le(NEW_MOVES)),'Move reader helper bank %X -> new move table'%bank,'21'+le(OLD_MOVES))
READER='21 00 40 01 06 00 cd bb 3a'.replace(' ','')
patch(fo(3,0x69d7),bytes.fromhex('cd'+le(0x7fb0))+bytes(6),'GetMaxPP -> death-move table',READER)
patch(fo(3,0x79fa),bytes.fromhex('cd'+le(0x7fb0))+bytes(6),'HealParty PP restore -> death-move table',READER)
patch(fo(0xe,0x70a6),bytes.fromhex('cd'+le(int(M3['bankE']['movehelper'],16)))+bytes(6),'WriteMonMoves reader -> death-move table',READER)
assert r[0xb062e]==0 and r[0xb062d]==0x50
put(0xb062e,enc('MACABRE')+b'\x50','Move name A9 = MACABRE')

f=Code(0xf,0x7de0)
f.label('pdmg');f.emit('fa d2 cf fe %02x'%MACABRE);f.jr('20','pdmgret')
f.emit('fa e6 cf 47 fa e7 cf 4f 78 b1');f.jr('28','store');f.emit('0b')      # bc = enemy HP - 1
f.label('store');f.emit('78 ea d7 d0 79 ea d8 d0 af ea 5e d0')                  # damage = bc, no "critical hit"
f.label('pdmgret');f.emit('21 d7 d0 c9')
f.label('panim');f.emit('fe %02x'%MACABRE);f.jr('20','pago');f.emit('3e %02x'%SLASH)
f.label('pago');f.emit('c3 '+le(PLAYMOVEANIM))
codeF=f.finish();put(fo(0xf,0x7de0),codeF,'Bank F: MACABRE damage + animation hooks')
patch(fo(0xf,0x6218),bytes.fromhex('cd'+le(f.labels['pdmg'])),'ApplyDamageToEnemyPokemon: MACABRE leaves 1 HP','21d7d0')
patch(fo(0xf,0x5804),bytes.fromhex('cd'+le(f.labels['panim'])),'Player move animation: MACABRE uses Slash','cded6f')

# 2. PRETA: a fixed Lv50 party struct (Fossil Kabutops, perfect DVs, MACABRE/CUT/SURF/STRENGTH).
kd=r[fo(0xe,KAB_DATA):fo(0xe,KAB_DATA)+9];base=list(kd[:5]);types=list(kd[5:7])
assert r[fo(0xe,KAB_DATA)+15]==5   # growth rate SLOW
L=50;DV=15
hp=((base[0]+DV)*2*L)//100+L+10;stats=[hp]+[((b+DV)*2*L)//100+5 for b in base[1:]]
exp=5*L**3//4
pp=[10]+[r[fo(0xe,0x4000+(mv-1)*6)+5] for mv in (CUT,SURF,STRENGTH)]
struct=bytes([KAB])+hp.to_bytes(2,'big')+bytes([L,0]+types+[0,MACABRE,CUT,SURF,STRENGTH,0,0])+exp.to_bytes(3,'big')+bytes(10)+b'\xff\xff'+bytes(pp+[L])+b''.join(s.to_bytes(2,'big') for s in stats)
assert len(struct)==44

g=Code(0x2e,0x4600)
g.label('awaken')
g.emit('3e %02x e0 db '%DOME+far(REMOVEITEMBYID[1],REMOVEITEMBYID[0]))              # take the DOME FOSSIL
g.emit('cd '+le(BLACK_ON)+' 3e %02x ea ee c0 cd %s'%(MUSIC_PKMN_HEALED,le(PLAYSOUND)))
g.label('wait');g.emit('fa 26 c0 fe %02x'%MUSIC_PKMN_HEALED);g.jr('28','wait')
g.emit('fa 5b d3 ea ee c0 cd '+le(PLAYSOUND)+' cd '+le(BLACK_OFF))                # map music back, lights on
g.emit('21 63 d1 7e ea 57 d4 34 4f 06 00 21 64 d1 09 36 %02x 23 36 ff'%KAB)        # species list
g.emit('21 6b d1 fa 57 d4 01 2c 00 cd '+le(ADDNTIMES)+' e5');g.ref('11','struct');g.emit('06 2c');g.ref('cd','copy')
g.emit('e1 11 0c 00 19 fa 59 d3 22 fa 5a d3 77')                                    # OT ID = player
g.emit('21 73 d2 fa 57 d4 01 0b 00 cd '+le(ADDNTIMES)+' 11 58 d1 06 0b');g.ref('cd','copy')   # OT name
g.emit('21 b5 d2 fa 57 d4 01 0b 00 cd '+le(ADDNTIMES));g.ref('11','nick');g.emit('06 0b');g.ref('cd','copy')
g.emit('21 08 d3 cb e6 21 1b d3 cb e6 c9')                                          # dex 141 seen + owned
g.label('copy');g.emit('1a 22 13 05');g.jr('20','copy');g.emit('c9')
g.label('struct');g.raw(struct)
g.label('nick');g.raw(enc('PRETA').ljust(11,b'\x50'))
code2e=g.finish();put(fo(0x2e,0x4600),code2e,'Bank 2E: awaken DOME FOSSIL into PRETA')

# 3. Cerulean trade house (map 3F, bank 7): Mr. Mu sits on the left of the table, facing right.
HDR=0x56fa
assert r[fo(7,HDR):fo(7,HDR)+12]==bytes.fromhex('080404de4109570657002057')
OBJ_OLD=0x5720;obj=bytearray(r[fo(7,OBJ_OLD):fo(7,OBJ_OLD)+32]);assert obj[1]==2 and obj[10]==0 and obj[11]==2
c=Code(7,0x7100)
c.label('objects');c.raw(obj[:11]+bytes([3])+obj[12:24]+bytes([GENTLEMAN,4+4,2+4,0xff,0xd3,3])+obj[24:])
c.label('texts');c.raw(r[fo(7,0x5709):fo(7,0x5709)+4]);c.ref('','mu')
c.label('script')                                       # hide Mu unless the player owns Ghost
c.emit('fa 51 d4 a7');c.jr('20','show');c.emit('af ea 30 c1 3e ff ea 34 c2 ea 35 c2')
c.label('show');c.emit('c3 87 3c')
def pt(label):c.ref('21',label);c.emit('cd '+le(PRINTTEXT))
c.label('mu');c.emit('08 fa %s fe 02'%le(MU2));c.ref('ca','hint');c.emit('a7');c.jr('20','met')
pt('t_intro');c.emit('3e 01 ea '+le(MU2));c.jr('18','fossil')
c.label('met');pt('t_again')
c.label('fossil');c.emit('21 1e d3')
c.label('scan');c.emit('2a fe ff');c.jr('28','done');c.emit('fe %02x'%DOME);c.jr('28','have');c.emit('23');c.jr('18','scan')
c.label('have');pt('t_question');pt('t_menu')
c.emit('af ea 26 cc ea 2a cc ea 35 cc ea 37 cc ea 4a cc 3e 0e ea 24 cc 3e 01 ea 25 cc ea 28 cc ea 29 cc f0 f6 cb 8f e0 f6 cd '+le(HANDLEMENUINPUT))
c.emit('fa 26 cc a7');c.jr('20','defy')
pt('t_accept');c.jr('18','done')
c.label('defy');c.emit('fa 63 d1 fe 06');c.jr('38','room')
pt('t_full');c.jr('18','done')
c.label('room');pt('t_defy');c.emit(far(g.labels['awaken'],0x2e));pt('t_got');c.emit('3e 02 ea '+le(MU2))
c.label('done');c.emit('c3 '+le(TEXTSCRIPTEND))
c.label('hint');pt('t_hint');c.jr('18','done')
for k,v in DIALOGUE.items():
    c.label('t_'+k);c.raw(txt(v,0x57 if k=='menu' else 0x58,18 if k=='menu' else 17))
code7=c.finish();put(fo(7,0x7100),code7,'Bank 7: Cerulean trade house Mr. Mu (objects, texts, script)')
patch(fo(7,HDR+5),bytes.fromhex(le(c.labels['texts'])+le(c.labels['script'])),'Trade house text + script pointers','09570657')
patch(fo(7,HDR+10),bytes.fromhex(le(c.labels['objects'])),'Trade house object pointer','2057')

# Header -----------------------------------------------------------------------
patch(0x134,b'CREEPY MU V6'.ljust(16,b'\0'),'Branch identity v6',b'CREEPY MU V5'.ljust(16,b'\0'))
v=0
for x in r[0x134:0x14d]:v=(v-x-1)&255
r[0x14d]=v;r[0x14e:0x150]=((sum(r[:0x14e])+sum(r[0x150:]))&65535).to_bytes(2,'big')
assert len(r)==1048576
out=ROOT/'Creepy_Black_Mu_v6.gb';out.write_bytes(r);sha=hashlib.sha256(r).hexdigest()
(ROOT/'manifest_v6.json').write_text(json.dumps(dict(input='Creepy_Black_Mu_v5.gb',input_sha256=V5_SHA,sha256=sha,size=len(r),
  preta=dict(stats=stats,exp=exp,pp=pp),
  labels={'bank7':{k:hex(v) for k,v in c.labels.items()},'bank2e':{k:hex(v) for k,v in g.labels.items()},'bankF':{k:hex(v) for k,v in f.labels.items()}},changes=log),indent=2))
print('Built',out.name,sha,'| 7',len(code7),'2E',len(code2e),'F',len(codeF),'Preta',stats,exp,pp)

# Creepy Black Mu v12: rival BLUE on the GHOST route - CURSE can't kill him (except as Champion), "died" defeat text,
# shock mode (Tower), Silph Co lines, hero mode (no more encounters, Mewtwo at the League). On top of verified Mu v11.
from pathlib import Path
import json,hashlib,re,io,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'ref'));import pic
M11=json.loads((ROOT/'manifest_v11.json').read_text());V11_SHA=M11['sha256']
src=(ROOT/'Creepy_Black_Mu_v11.gb').read_bytes();assert hashlib.sha256(src).hexdigest()==V11_SHA
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






def shown(line):return len(line.replace('#','POKé').replace('<PLAYER>','X'*7).replace('<RIVAL>','X'*7))
def txt(paras,end=0x58,maxw=17):
    out=bytearray([0])
    for i,p in enumerate(paras):
        if i:out.append(0x51)
        for j,line in enumerate(p):
            assert shown(line)<=maxw,line
            if j:out.append(0x4f if j==1 else 0x55)
            out+=enc(line)
    out.append(end);return out
D=json.loads((ROOT/'dialogue_v12.json').read_text(encoding='utf8'))
PRINTTEXT,TEXTSCRIPTEND,BANKSWITCH=0x3c94,0x2504,0x3618
RIVAL1,RIVAL2,RIVAL3=25,42,43;OPP_RIVAL3=0xc8+RIVAL3
MEWTWO=0x83
MODE=0xd463   # new saved RAM: rival mode 0 normal, 1 shock (cursed before/at the Tower), 2 hero (beat him at Silph Co)
# event flags / map script variables (same as pokered; checked against the scripts in this ROM)
EV_TOWER=(0xd764,7);EV_CERULEAN=(0xd75b,7);EV_R22_WANTS=(0xd7eb,7);SSANNE_SCRIPT=0xd665;SSANNE_NOOP=4
FEAR=0x4032   # v1 frightened-text selector (bank 2E)

# --- bank 6: the in-battle "died" defeat text (same bank as the v2 frightened texts) ---
t6=Code(6,0x6f00);t6.label('died');t6.raw(txt(D['died']))
code6=t6.finish();put(fo(6,0x6f00),code6,'Bank 6: rival "My POKeMON... died!?" defeat text')

g=Code(0x2e,0x4b00)
# 1. After-win CURSE on the trainer himself (base-game "type 3" phase): BLUE (RIVAL1/RIVAL2) can't be killed.
g.label('curse_trainer');g.emit('fa 31 d0 fe %02x'%RIVAL1);g.jr('28','hes');g.emit('fe %02x'%RIVAL2);g.jr('28','hes')
g.emit('3e 01 ea 85 d4 06 03 21 99 4d c3 %s'%le(BANKSWITCH))                       # original: kill + gravestone
g.label('hes');g.ref('21','t_hesitate');g.emit('c3 '+le(PRINTTEXT))
# Scripted trainers (no trainer header, like BLUE) normally get "But, it failed!" here and the menu loops;
# for BLUE report "killable" so the path above shows the hesitation and ends the battle.
g.label('killable');g.emit('cd 5c 36 c0 fa 31 d0 fe %02x'%RIVAL1);g.jr('28','kr');g.emit('fe %02x'%RIVAL2);g.jr('28','kr');g.emit('af c9')
g.label('kr');g.emit('3e 01 a7 c9')
# 2. Defeat text + shock mode
g.label('fear');g.emit('fa 52 d4 a7 c8 fa 31 d0 fe %02x'%RIVAL1);g.jr('28','rival');g.emit('fe %02x c2 %s'%(RIVAL2,le(FEAR)))
g.label('rival');g.emit('3e 06 ea 92 d0 3e %02x ea 8c d0 ea 8e d0 3e %02x ea 8d d0 ea 8f d0'%(t6.labels['died']>>8,t6.labels['died']&0xff))
g.emit('fa 51 d4 a7 c8 fa %s cb %02x c0 fa %s a7 c0'%(le(EV_TOWER[0]),0x47+8*EV_TOWER[1],le(MODE)))   # ghost route, Tower not beaten, no mode yet
g.emit('3e 01 ea '+le(MODE))
g.emit('21 %s cb %02x'%(le(EV_CERULEAN[0]),0xc6+8*EV_CERULEAN[1]))              # skip Cerulean rival
g.emit('fa %s a7'%le(SSANNE_SCRIPT));g.jr('20','ssdone');g.emit('3e %02x ea %s'%(SSANNE_NOOP,le(SSANNE_SCRIPT)))   # skip S.S. Anne rival
g.label('ssdone');g.emit('21 %s cb %02x c9'%(le(EV_R22_WANTS[0]),0x86+8*EV_R22_WANTS[1]))  # skip Route 22 rival
# 3. Pokemon Tower 2F rival text: D457 0 = original, 1 = handled, 2 = printed pre-battle text, continue the battle setup
g.label('tower');g.emit('af ea 57 d4 fa 51 d4 a7 c8 fa %s fe 01 c0 fa %s cb %02x'%(le(MODE),le(EV_TOWER[0]),0x47+8*EV_TOWER[1]));g.jr('28','tpre')
g.ref('21','t_tower_bastard');g.emit('cd %s 3e 01 ea 57 d4 c9'%le(PRINTTEXT))
g.label('tpre');g.ref('21','t_tower_shock');g.emit('cd %s 3e 02 ea 57 d4 c9'%le(PRINTTEXT))
# 4. Silph Co 7F pre-battle text: shock -> avenge, otherwise (GHOST route) -> TEAM ROCKET told me
g.label('silph');g.emit('af ea 57 d4 fa 51 d4 a7 c8');g.ref('21','t_silph_rocket');g.emit('fa %s fe 01'%le(MODE));g.jr('20','sp')
g.ref('21','t_silph_avenge')
g.label('sp');g.emit('cd %s 3e 01 ea 57 d4 c9'%le(PRINTTEXT))
# 5. Silph Co 7F after-battle text (only shown when the player won): hero mode on the GHOST route
g.label('hero');g.emit('fa 51 d4 a7 c8 3e 02 ea %s c9'%le(MODE))
for k in ('hesitate','tower_shock','tower_bastard','silph_avenge','silph_rocket'):g.label('t_'+k);g.raw(txt(D[k]))
code2e=g.finish();put(fo(0x2e,0x4b00),code2e,'Bank 2E: rival BLUE modes (curse, shock, Silph, hero)')

f=Code(0xf,0x7fe8);f.label('ct');f.emit('21 %s 06 2e c3 %s'%(le(g.labels['curse_trainer']),le(BANKSWITCH)))
f.label('kb');f.emit('21 %s 06 2e c3 %s'%(le(g.labels['killable']),le(BANKSWITCH)))
codeF=f.finish();put(fo(0xf,0x7fe8),codeF,'Bank F: trainer-curse hook')
patch(fo(0xf,0x5043),bytes.fromhex('cd'+le(f.labels['ct']))+bytes(10),'Trainer CURSE: BLUE hesitates instead of dying','3e01ea85d40603 21994dcd1836'.replace(' ',''))
patch(fo(0xf,0x5033),bytes.fromhex('cd'+le(f.labels['kb'])),'Trainer CURSE: BLUE counts as cursable (no "But, it failed!" loop)','cd5c36')
patch(fo(0xf,0x7d11),bytes.fromhex('21'+le(g.labels['fear'])),'Defeat text selector -> rival-aware v12',le(0x4032).join(['21','']))

# Pokemon Tower 2F (bank 18): text 1
t18=Code(0x18,0x6600)
t18.label('tower');t18.emit('08 '+far(g.labels['tower'],0x2e)+' fa 57 d4 a7 ca e0 45 3d ca %s c3 f5 45'%le(TEXTSCRIPTEND))
code18=t18.finish();put(fo(0x18,0x6600),code18,'Bank 18: Pokemon Tower 2F rival text wrapper')
assert r[fo(0x18,0x45df):fo(0x18,0x45df)+7]==bytes.fromhex('08fa64d7cb7f28') and r[fo(0x18,0x45f5):fo(0x18,0x45f5)+3]==bytes.fromhex('212dd7')
patch(fo(0x18,0x45db),bytes.fromhex(le(t18.labels['tower'])),'Pokemon Tower 2F text 1 -> wrapper',le(0x45df))

# Silph Co 7F (bank 14): texts 13 (pre-battle) and 15 (after a win); Route 22 map script
t14=Code(0x14,0x6b00)
t14.label('pre');t14.emit('08 '+far(g.labels['silph'],0x2e)+' fa 57 d4 a7');t14.jr('20','pend');t14.emit('21 c3 5e cd '+le(PRINTTEXT))
t14.label('pend');t14.emit('c3 '+le(TEXTSCRIPTEND))
t14.label('after');t14.emit('08 '+far(g.labels['hero'],0x2e)+' 21 d2 5e cd %s c3 %s'%(le(PRINTTEXT),le(TEXTSCRIPTEND)))
t14.label('r22');t14.emit('fa %s a7'%le(MODE));t14.jr('28','r22go');t14.emit('21 %s cb %02x'%(le(EV_R22_WANTS[0]),0x86+8*EV_R22_WANTS[1]))
t14.label('r22go');t14.emit('c3 b2 4e')
code14=t14.finish();put(fo(0x14,0x6b00),code14,'Bank 14: Silph Co 7F rival texts + Route 22 rival gate')
TP=fo(0x14,0x5d3f)
patch(TP+2*12,bytes.fromhex(le(t14.labels['pre'])),'Silph Co 7F text 13 (rival pre-battle) -> wrapper',le(0x5ec3))
patch(TP+2*14,bytes.fromhex(le(t14.labels['after'])),'Silph Co 7F text 15 (rival after win) -> hero mode',le(0x5ed2))
patch(fo(0x14,0x4000+7),bytes.fromhex(le(t14.labels['r22'])),'Route 22 map script -> rival gate (shock/hero: no rival)',le(0x4eb2))

# Champion (RIVAL3): hero mode -> parties 4-6 = parties 1-3 with the Lv65 starter ace replaced by Lv70 MEWTWO
TDP=0x39d79;o=TDP+2*(RIVAL3-1);old_ptr=r[o]|r[o+1]<<8;src=fo(0xe,old_ptr)
parties=[];i=src
for k in range(3):
    j=r.index(b'\x00',i);parties.append(bytes(r[i:j+1]));i=j+1
    assert parties[-1][0]==0xff and parties[-1][-3]==65
hero=[p[:-3]+bytes([70,MEWTWO,0]) for p in parties]
e=Code(0xe,0x7d60)
e.label('parties');e.raw(b''.join(parties+hero))
e.label('rt');e.emit('fa 59 d0 fe %02x'%OPP_RIVAL3);e.jr('20','rtdone');e.emit('fa %s fe 02'%le(MODE));e.jr('20','rtdone')
e.emit('21 5d d0 7e fe 04');e.jr('30','rtdone');e.emit('c6 03 77')
e.label('rtdone');e.emit('fa 2b d1 c9')
codeE=e.finish();put(fo(0xe,0x7d60),codeE,'Bank E: Champion parties (+hero Mewtwo) and trainer-number hook')
patch(o,bytes.fromhex(le(e.labels['parties'])),'RIVAL3 party list -> 6 parties',le(old_ptr))
assert r[fo(0xe,0x5c91):fo(0xe,0x5c91)+3]==bytes.fromhex('fa2bd1')
patch(fo(0xe,0x5c91),bytes.fromhex('cd'+le(e.labels['rt'])),'ReadTrainer: Champion uses hero party in hero mode','fa2bd1')

# Header -----------------------------------------------------------------------
patch(0x134,b'CREEPY MU V12'.ljust(16,b'\0'),'Branch identity v12',b'CREEPY MU V11'.ljust(16,b'\0'))
v=0
for x in r[0x134:0x14d]:v=(v-x-1)&255
r[0x14d]=v;r[0x14e:0x150]=((sum(r[:0x14e])+sum(r[0x150:]))&65535).to_bytes(2,'big')
assert len(r)==1048576
out=ROOT/'Creepy_Black_Mu_v12.gb';out.write_bytes(r);sha=hashlib.sha256(r).hexdigest()
(ROOT/'manifest_v12.json').write_text(json.dumps(dict(input='Creepy_Black_Mu_v11.gb',input_sha256=V11_SHA,sha256=sha,size=len(r),
  labels={'bank2e':{k:hex(v) for k,v in g.labels.items()},'bank14':{k:hex(v) for k,v in t14.labels.items()},'bank18':{k:hex(v) for k,v in t18.labels.items()},
          'bankE':{k:hex(v) for k,v in e.labels.items()},'bank6':{k:hex(v) for k,v in t6.labels.items()}},changes=log),indent=2))
print('Built',out.name,sha,'| 2E',len(code2e),'14',len(code14),'18',len(code18),'E',len(codeE),'parties',[p.hex() for p in hero])

# Creepy Black Mu v2: logged patches applied on top of the verified Mu v1 ROM.
# (The clean base ROM is not in this workspace, so v1 is the input; every patch
# asserts the v1 bytes it replaces.)
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parent
V1_SHA='1bb97ea3f2fbabbca72f29a529983ea11828aed3275623f56bc65a6ae9e73df5'
src=(ROOT/'Creepy_Black_Mu_v1.gb').read_bytes();assert hashlib.sha256(src).hexdigest()==V1_SHA
r=bytearray(src);log=[]
def patch(o,data,name,old):
    data=bytes(data);old=bytes.fromhex(old)
    assert r[o:o+len(old)]==old,(name,hex(o),r[o:o+len(old)].hex())
    log.append(dict(offset=hex(o),before=r[o:o+len(data)].hex(),after=data.hex(),name=name));r[o:o+len(data)]=data
def free(o,n,name):assert not any(r[o:o+n]),('not free',name,hex(o))

class Code:
    def __init__(self,org):self.org=org;self.b=bytearray();self.labels={};self.refs=[];self.rel=[]
    def emit(self,h):self.b+=bytes.fromhex(h)
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

# Engine addresses verified in this ROM (match pokered layout).
BANKSWITCH,PLAYCRY,DELAYFRAMES,PREDEF=0x3618,0x13ff,0x3773,0x3ec1
REMOVEMON,REMOVEMON_BANK=0x7b61,0x01
READPLAYERMON=0x4d6e
GHOST=0x1f
# New saved RAM (unreferenced by the base game, cleared by v1's NEW GAME clear D450-D4AD):
# D455 hunger (255 full .. 0 starving), D456 step counter, D457 temp species, D458-D45A saved palettes.
TUNING=dict(start=160,steps_per_point=6,wild=16,trainer=48,human=160,own=12)
T=TUNING

# 1. Sprites -------------------------------------------------------------------
# Pallet uses sprite set 1 (shared with Viridian, Cinnabar, Routes 1/2/22). None of
# those maps use COOLTRAINER_M (07) or SEEL (3C), so those slots become GENTLEMAN and CHANNELER.
SET1=0x17ab9
patch(SET1+4,[0x10],'Sprite set 1 slot 5: COOLTRAINER_M -> GENTLEMAN (Mr. Mu)','07')
patch(SET1+6,[0x19],'Sprite set 1 slot 7: SEEL -> CHANNELER (shamaness)','3c')
OBJ=0x1ad17  # v1 Pallet object table (bank 6)
patch(OBJ+46,[0x10],'Mr. Mu uses GENTLEMAN sprite','25 0a 0c ff d2 08')
patch(OBJ+52,[0x19,19,12,0xff,0xd2,9],'Shamaness: CHANNELER sprite at x8,y15 by the water, facing water','28 13 0d ff d1 09')

# 2. Ghost hunger -------------------------------------------------------------
B2E=0x2e;g=Code(0x4100);free(0xb8100,0x200,'bank2e')
g.label('hunger_step')
g.emit('fa 51 d4 a7 c8')            # no Ghost yet -> nothing
g.emit('fa 30 d7 cb 7f c0')         # simulated input (cutscene) -> skip
g.emit('21 56 d4 34 7e fe %02x d8 36 00'%T['steps_per_point'])
g.emit('21 55 d4 7e a7');g.jr('28','eat');g.emit('35 c0')   # dec hunger; still >0 -> ret
g.label('eat');g.emit('fa 63 d1 47')
g.label('eat_loop');g.emit('78 a7');g.ref('ca','eat_player');g.emit('05 21 64 d1 58 16 00 19 7e fe %02x'%GHOST);g.jr('28','eat_loop')
g.emit('ea 57 d4 78 ea 92 cf');g.ref('cd','black_on')
g.emit('fa 57 d4 cd '+le(PLAYCRY))                       # victim's cry
g.emit('af ea 95 cf '+far(REMOVEMON,REMOVEMON_BANK))     # remove from party
g.emit('0e 28 cd '+le(DELAYFRAMES));g.ref('cd','black_off')
g.emit('3e %02x ea 55 d4 c9'%T['own'])
g.label('eat_player');g.ref('cd','black_on')
g.emit('3e %02x cd %s 0e 78 cd %s'%(GHOST,le(PLAYCRY),le(DELAYFRAMES)))
g.emit('3e 0a ea 00 00 06 04')                           # enable SRAM, wipe banks 3..0
g.label('wipe_bank');g.emit('05 78 ea 00 40 21 00 a0')
g.label('wipe_fill');g.emit('af 22 7c fe c0');g.jr('20','wipe_fill');g.emit('78 a7');g.jr('20','wipe_bank')
g.emit('af ea 00 00 c3 00 01')                            # disable SRAM, cold restart
g.label('black_on');g.emit('f0 47 ea 58 d4 f0 48 ea 59 d4 f0 49 ea 5a d4 3e ff e0 47 e0 48 e0 49 0e 0a c3 '+le(DELAYFRAMES))
g.label('black_off');g.emit('fa 58 d4 e0 47 fa 59 d4 e0 48 fa 5a d4 e0 49 c9')
g.label('feed');g.emit('21 55 d4 86');g.jr('30','feed_store');g.emit('3e ff');g.label('feed_store');g.emit('77 c9')
g.label('feed_battle');g.emit('fa 51 d4 a7 c8 fa 14 d0 fe %02x c0'%GHOST)   # only Ghost's own kills feed it
g.emit('fa 57 d0 fe 01 3e %02x'%T['wild']);g.jr('28','feed_go');g.emit('3e %02x'%T['trainer']);g.label('feed_go');g.ref('c3','feed')
g.label('feed_human');g.emit('fa 51 d4 a7 c8 3e %02x'%T['human']);g.ref('c3','feed')
g.label('award_ext');g.emit('3e 01 ea 51 d4 3e %02x ea 55 d4 af ea 56 d4 c9'%T['start'])
code2e=g.finish();assert len(code2e)<0x200
patch(0xb8100,code2e,'Ghost hunger engine (step drain, eating, permadeath, feeding)','00'*len(code2e))
patch(0xb802c,bytes.fromhex('c3'+le(g.labels['award_ext'])+'000000'),'Ghost award also fills hunger','3e01ea51d4c9')
# Per-step hook: home padding 0x00E0 stub, then the original poison predef.
free(0xe0,13,'home pad')
patch(0xe0,bytes.fromhex(far(g.labels['hunger_step'],B2E)+' 3e 14 c3 '+le(PREDEF)),'Home stub: hunger step then poison predef','00'*13)
patch(0x62d,bytes.fromhex('cd e0 00 00 00'),'Overworld step hook','3e14cdc13e')
# Enemy faints while Ghost is out: wild / trainer feeding.
free(0x3fd20,16,'bankF')
patch(0x3fd20,bytes.fromhex(far(g.labels['feed_battle'],B2E)+' c3 '+le(READPLAYERMON)),'Feed Ghost on enemy faint','00'*11)
patch(0x3c56d,bytes.fromhex('cd 20 7d'),'FaintEnemyPokemon hook','cd6e4d')
# Human killed (v1 trainer-death hook in bank 3): feed most. Preserve BC/DE for the caller.
patch(0xff8e,bytes.fromhex('3e 01 ea 53 d4 c5 d5 '+far(g.labels['feed_human'],B2E)+' d1 c1 21 a4 d4 c9'),
      'Trainer death: record + feed human','3e01ea53d421a4d4c9'+'00'*12)

# 3. Text fix: the prompt arrow overwrites column 18 of the bottom line, so lines are capped at 17.
import re
cm={}
for k,v in re.findall(r'^\s*charmap "([^"]+)",\s*\$([0-9A-Fa-f]+)',(ROOT.parent/'pokeblack/charmap.asm').read_text(encoding='utf8'),re.M):
    cm.setdefault(k,int(v,16))
def enc(s):
    out=bytearray()
    while s:
        k=next(k for k in sorted(cm,key=len,reverse=True) if s.startswith(k));out.append(cm[k]);s=s[len(k):]
    return out
def shown(line):return len(line.replace('#','POKé').replace('<PLAYER>','X'*7))   # on-screen width
def txt(paras,end,maxw=None):
    out=bytearray([0])
    for i,p in enumerate(paras):
        if i:out.append(0x51)
        for j,line in enumerate(p):
            assert maxw is None or shown(line)<=maxw,line
            if j:out.append(0x4f if j==1 else 0x55)
            out+=enc(line)
    out.append(end);return out
old_src=(ROOT.parent/'edit/build.py').read_text(encoding='utf8')
old=eval(old_src[old_src.index('dialogue={')+9:old_src.index('\n}\n')+2])
new=json.loads((ROOT/'dialogue_v2.json').read_text(encoding='utf8'))
o=0x1a800;tlab={}
for k in old:
    e=0x57 if k in ('menu','briefing') else 0x58
    a=txt(old[k],e);b=txt(new[k],e,None if k.startswith('fear') else 17 if k!='menu' else 18)
    assert r[o:o+len(a)]==a,('v1 text mismatch',k)   # proves this encoder == v1 encoder
    assert len(a)==len(b),k
    if a!=b and not k.startswith('fear'):patch(o,b,'Rewrap '+k+' to 17-col lines',a.hex())
    tlab[k]=0x4000+o%0x4000;o+=len(a)
# Frightened end-battle texts follow "CLASS NAME:" on line 1, so they start on line 2.
# They grew by one byte, so they move to bank 6 free space and the fear table is repointed.
f=0x1ae40;fp=[]
for k in ('fear0','fear1','fear2'):
    b=txt(new['fear_v2'][k],0x58,17);free(f,len(b),k);patch(f,b,'Frightened text '+k+' (starts on line 2)','00'*len(b))
    fp.append(0x4000+f%0x4000);f+=len(b)
patch(0xb805e,b''.join(a.to_bytes(2,'little') for a in fp),'Repoint fear table',
      ''.join(le(tlab[k]) for k in ('fear0','fear1','fear2')))

# 4. Police bulletin: once per map visit after a Curse murder, when a guard speaks
# (sprite text from a GUARD) or script text plays on a map that has a guard (gate scripts).
POLICE_ALERTED=0xd45b
q=Code(0x4200);free(0xb8200,0x80,'bank2e police')
q.label('police');q.emit('fa 3c cc a7 c0 fa 47 cc a7 c0')                 # original skip-wait cases
q.emit('fa 53 d4 a7');q.jr('28','wait');q.emit('fa 5b d4 a7');q.jr('20','wait')
q.emit('fa 13 cf a7');q.jr('28','wait');q.emit('47 fa e1 d4 b8');q.jr('38','script')
q.emit('78 cb 37 6f 26 c1 7e');q.ref('cd','isguard');q.jr('28','alert');q.jr('18','wait')
q.label('script');q.emit('fa e1 d4 a7');q.jr('28','wait');q.emit('4f 21 10 c1')
q.label('scan');q.emit('7e');q.ref('cd','isguard');q.jr('28','alert');q.emit('7d c6 10 6f 0d');q.jr('20','scan');q.jr('18','wait')
q.label('alert');q.emit('3e 01 ea 5b d4 cd 99 38');q.ref('21','police_far');q.emit('cd 94 3c')
q.label('wait');q.emit('c3 99 38')
q.label('isguard');q.emit('fe 31 c8 fe 32 c9')
q.label('police_far');q.emit('17 '+le(tlab['police'])+' 06 50')
q.label('mapload_ext');q.emit('af ea 5b d4 fa 54 d4 c3 03 40')               # clear per-visit flag, resume v1 mapload
pol=q.finish();patch(0xb8200,pol,'Police bulletin v2','00'*len(pol))
patch(0x29fd,bytes.fromhex('21'+le(q.labels['police'])),'Guard hook -> police v2','216440')
patch(0xb8000,bytes.fromhex('c3'+le(q.labels['mapload_ext'])),'Map load clears police flag','fa54d4')

# Header -----------------------------------------------------------------------
patch(0x134,b'CREEPY MU V2'.ljust(16,b'\0'),'Branch identity v2',b'CREEPY MU V1'.hex())
v=0
for x in r[0x134:0x14d]:v=(v-x-1)&255
r[0x14d]=v;r[0x14e:0x150]=((sum(r[:0x14e])+sum(r[0x150:]))&65535).to_bytes(2,'big')
assert len(r)==1048576
out=ROOT/'Creepy_Black_Mu_v2.gb';out.write_bytes(r)
sha=hashlib.sha256(r).hexdigest()
(ROOT/'manifest_v2.json').write_text(json.dumps(dict(input='Creepy_Black_Mu_v1.gb',input_sha256=V1_SHA,sha256=sha,size=len(r),
    tuning=TUNING,labels_bank2e={k:hex(v) for k,v in g.labels.items()},changes=log),indent=2))
print('Built',out.name,sha,'bank2e bytes',len(code2e))

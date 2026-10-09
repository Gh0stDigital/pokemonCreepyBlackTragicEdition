# Creepy Black Mu v23: MR. MU's last talk in the TOWER CHAMBER and the ritual battle.
#  - MR. MU's speech (successor, "I gave birth to you", the LAVENDER clan and the BLACK TAMER, the MIRAGE = his missing
#    half), he hands over the vessel (MASTER BALL, kept by AGATHA), asks "Is there life after death?" (YES/NO, no wrong
#    answer), then the battle starts.
#  - The battle: trainer MR. MU (unused class 27, GENTLEMAN pic). The player's party is put aside (SRAM bank 1) and the
#    player fights alone as YOU (species 79) with STRUGGLE only. PKMN/ITEM/RUN -> "No! You must kill me with your own
#    hands!". MR. MU never attacks. When he dies (gravestone, kill index 33) the MIRAGE ????? (species 7A, RED+GHOST
#    fusion pics) appears: now only ITEM -> MASTER BALL works. The ball turns pure black when it catches ?????.
#  - After the battle the party comes back and ????? joins it (or the PC box if the party is full).
# Logged patches on top of verified Mu v22 (patchlib).
import io,json,sys
from patchlib import *
from patchguard import fo
sys.path.insert(0,str(ROOT.parent/'ref'));import pic
import red_ghost_fusion as FUSION

V22_SHA='d51b965e4587a9dd8799ed227b795466abcef944a8f835023fd84aedfeb67f61'
rom=Rom('Creepy_Black_Mu_v22.gb',V22_SHA)
r=rom.r
w=lambda o:r[o]|r[o+1]<<8
labels={}

# ---- engine addresses (this ROM, checked by disassembly) -------------------------------------------------------
PRINTTEXT,TEXTEND,BANKSWITCH,COPYDATA,ADDNTIMES,DELAYFRAMES=0x3c94,0x2504,0x3618,0x00b5,0x3abb,0x3773
YESNO,GIVEITEM,AUTOTEXT=0x362e,0x3e82,0x3c87
DISPLAYBATTLEMENU,BAGWASSELECTED,MENU_NOT_FIGHT=0x4ede,0x508b,0x5065          # bank F
ENEMYFAINTEDTEXT,TRAINERSENTOUTTEXT=0x4653,0x4aa9                             # bank F text_far records
MOVEANIM=(0x1e,0x4d5e);ASKNAME=0x64c4;ASKNAME_SPECIESNAME=0x64cd               # AskName already skips naming GHOST (1F) there
PREDEFS=fo(0x13,0x7e79)
# ---- RAM ----------------------------------------------------------------------------------------------------------
RIT,TMP,TMP2=0xd467,0xd468,0xd469     # D467 ritual: 0 -, 1 MR. MU battle, 2 MIRAGE phase, 3 done; D468/D469 hook temps
PARTY,PARTY_LEN=0xd163,0x194          # wPartyDataStart..wPartyDataEnd
STASH,CAUGHT=0xb600,0xb800            # SRAM bank 1, unused by the save layout (it ends at B523)
PLAYERNAME,BOXCOUNT=0xd158,0xda80
KILL_IDX=33;KILL_BYTE,KILL_MASK=0xd4a4+(KILL_IDX>>3),1<<(KILL_IDX&7)
# ---- ids ----------------------------------------------------------------------------------------------------------
YOU,MU,MIR=0x79,0x20,0x7a             # 20 / 7A = unused MISSINGNO slots (20 -> pics in bank A, 7A -> bank 2D below)
CLASS=27;OPP=0xc8+CLASS               # unused CHIEF class -> MR. MU
MASTERBALL,STRUGGLE,TOSS_ANIM,CAUGHT_ANIMDATA=0x01,0xa6,0xc2,0x43   # A5 is the base game's CURSE
NIGHTSHADE,CONFUSERAY,HYPNOSIS,DREAMEATER=0x65,0x6d,0x5f,0x8a
CHAMBER=0x69
L22=json.load(open(ROOT/'manifest_v22.json'))['labels']['chamber']
L14=json.load(open(ROOT/'manifest_v14.json'))['labels']['bank2e']

# ================================================================================================================
# 1. Pictures. MR. MU = the GENTLEMAN trainer pic (13:73D0, untouched since v14 repointed the class) copied to bank A.
#    ????? = the RED+GHOST fusion (red_ghost_fusion.py: option A0 front, fuse_back back) in bank 2D.
def tobytes(g):
    H,W=len(g),len(g[0]);out=bytearray()
    for tx in range(W//8):
        for ty in range(H//8):
            for y in range(8):
                lo=hi=0
                for x in range(8):c=g[ty*8+y][tx*8+x];lo=lo<<1|(c&1);hi=hi<<1|(c>>1)
                out+=bytes([lo,hi])
    return bytes(out)
def packed(d):
    c=bytes(pic.compress(d));assert bytes(pic.decompress(io.BytesIO(c)))==d;return c
gent=packed(bytes(pic.decompress(io.BytesIO(bytes(r)),offset=fo(0x13,0x73d0))))
mir_front=packed(tobytes(FUSION.fuse(bytes(r),small='A0')[0]))
mir_back=packed(tobytes(FUSION.fuse_back(bytes(r))))
MU_PIC=0x7efc;assert MU_PIC+len(gent)<=0x8000
rom.put(fo(0xa,MU_PIC),gent,'Bank A: MR. MU battle pic (copy of the GENTLEMAN trainer pic)')
MIR_FRONT=0x41c0;MIR_BACK=MIR_FRONT+len(mir_front)
rom.put(fo(0x2d,MIR_FRONT),mir_front+mir_back,'Bank 2D: ????? front (RED+GHOST fusion) + back pics')

# UncompressMonSprite's bank choice (0:1659-1691), rewritten one case denser (c = bank) to add ????? -> bank 2D.
h=Code(0,0x1659)
h.emit('fa 91 cf')
for bank,cmp,jr in ((0x01,0x15,'28'),(0x2d,0x1f,'28'),(0x2d,MIR,'28'),(0x0b,0xb6,'28'),
                    (0x09,0x1f,'38'),(0x0a,0x4a,'38'),(0x0b,0x74,'38'),(0x0c,0x99,'38')):
    h.emit('0e %02x fe %02x'%(bank,cmp));h.jr(jr,'got')
h.emit('0e 0d');h.label('got');h.emit('79 c3 2a 25')
hb=h.finish();assert len(hb)==0x39
rom.code(0x1659,hb,'UncompressMonSprite: bank by species, + ????? (7A) -> bank 2D',r[0x1659:0x1692],
         reviewed='jumps into 0x1659-0x1691 are this routine\'s own jr\'s (to the shared "jp UncompressSpriteData")')

# ================================================================================================================
# 2. Species headers (GetMonHeader exit hook, bank E) + trainer party
e=Code(0xe,0x7de0)
e.label('hdr');e.emit('fa b5 d0 fe %02x'%MU);e.ref('21','mu_hdr');e.jr('28','copy')
e.emit('fe %02x'%MIR);e.ref('21','mir_hdr');e.jr('28','copy')
e.emit('c3 60 7c')                                                     # older special headers (B6/B7/79/...)
e.label('copy');e.emit('11 b9 d0 06 1b')
e.label('lp');e.emit('2a 12 13 05');e.jr('20','lp');e.emit('fa b5 d0 ea b8 d0 c9')
# hp atk def spd spc | types | catch | exp | dims | front | back | 4 moves | growth | 7 TM bytes | pad
e.label('mu_hdr');e.raw([100,20,20,20,20, 0x00,0x00, 0,0, 0x77]+list(bytes.fromhex(le(MU_PIC)*2))+[0,0,0,0, 0]+[0]*8)
e.label('mir_hdr');e.raw([60,65,60,110,130, 0x08,0x08, 3,200, 0x77]+list(bytes.fromhex(le(MIR_FRONT)+le(MIR_BACK)))
                         +[NIGHTSHADE,CONFUSERAY,HYPNOSIS,DREAMEATER, 5]+[0]*8)
e.label('party');e.raw([0xff, 30,MU, 50,MIR, 0])                         # trainer 1: Lv30 MR. MU, Lv50 ?????
eb=e.finish();assert len(e.labels) and 0x7de0+len(eb)<=0x8000
rom.put(fo(0xe,0x7de0),eb,'Bank E: MR. MU / ????? headers, MR. MU party')
rom.code(0x15c6,bytes.fromhex('cd'+le(e.labels['hdr'])),'GetMonHeader exit -> v23 headers (MR. MU, ?????), then the older ones','cd 60 7c',
         reviewed='same site as v3 (operand-byte hits reviewed in check_hooks)')

# trainer class 27 (CHIEF, no trainers in the game) -> MR. MU
NAMES=0x1c21e;DEX=0x4102e;CRY=0x39484
for sp,nm in ((MU,'MR. MU'),(MIR,'?????')):
    o=NAMES+10*(sp-1);rom.data(o,enc(nm).ljust(10,b'\x50'),'Species name %02x = %s'%(sp,nm),r[o:o+10])
    rom.data(DEX+sp-1,[152],'Species %02x: dex slot 152 (like GHOST; outside the 151 real entries)'%sp,'00')
rom.data(CRY+3*(MIR-1),r[CRY+3*(0x1f-1):CRY+3*0x1f],'????? cry = GHOST cry',r[CRY+3*(MIR-1):CRY+3*MIR])
rom.data(CRY+3*(MU-1),bytes([r[CRY+3*(0x1f-1)],0x10,0x40]),'MR. MU cry = GHOST cry, low and short',r[CRY+3*(MU-1):CRY+3*MU])
PICMONEY=0x39952;o=PICMONEY+5*(CLASS-1)
rom.data(o,bytes.fromhex(le(0x73d0)+'000000'),'Class 27 pic = GENTLEMAN pic, no prize money',r[o:o+5])
TDP=0x39d79;o=TDP+2*(CLASS-1)
rom.data(o,bytes.fromhex(le(e.labels['party'])),'Class 27 party data -> MR. MU + ?????',r[o:o+2])
TN=0x39a3d;names=bytes(r[TN:TN+420]).split(b'\x50')[:47];old=b'\x50'.join(names)+b'\x50'
assert names[CLASS-1]==enc('CHIEF')
names[CLASS-1]=enc('MR. MU');new=b'\x50'.join(names)+b'\x50'
pad=len(old)
while r[TN+pad]==0x50:pad+=1                                                   # spare 50s after the list (v3/v10 renames)
assert len(new)<=pad;rom.data(TN,new.ljust(pad,b'\x50'),'Trainer class names: CHIEF (27) -> MR. MU',r[TN:TN+pad])
# class 27 is used by no map object / trainer header (checked: no OPP byte E3 in any object list)
def objects(o):
    p=o+1;p+=1+4*r[p];p+=1+3*r[p];n=r[p];p+=1;out=[]
    for i in range(n):
        t=r[p+5];size=6+(2 if t&0x40 else 0)+(1 if t&0x80 else 0);out.append((p,t));p+=size
    return out
for mp in range(0xf8):
    bank=r[0xc23d+mp];hp=w(0x1ae+2*mp)
    if hp<0x4000 or bank==0 or mp==0x0b:continue
    hh=fo(bank,hp);n=bin(r[hh+9]&15).count('1');oo=fo(bank,w(hh+10+11*n))
    for p,t in objects(oo):assert not (t&0x40 and r[p+6]==OPP),('class 27 used on map',hex(mp))

# ================================================================================================================
# 3. Bank 2E: party swap, battle hooks (far routines), texts
B={ # battle texts
 'mu_out':  ([["MR. MU stepped","into the circle."]],0x57),
 'mu_idle': ([["MR. MU doesn't","fight back."]],0x58),
 'block1':  ([["MR. MU: No!"],["You must kill me","with your own","hands!"]],0x58),
 'mu_died': ([["MR. MU died with","a smile..."]],0x58),
 'mir_out': ([["The circle","trembles..."],["The MIRAGE","appeared!"]],0x57),
 'mir_idle':([["????? stares","at you..."]],0x58),
 'block2':  ([["It can't be","harmed..."],["Only the MASTER","BALL can hold it!"]],0x58),
}
g=Code(0x2e,0x5820)
def pt(c,label):c.ref('21',label);c.emit('cd '+le(PRINTTEXT))
# ---- before the battle (from MR. MU's text): party -> SRAM, the player alone as YOU with STRUGGLE
g.label('sram_on');g.emit('3e 0a ea 00 00 3e 01 ea 00 40 c9')
g.label('sram_off');g.emit('af ea 00 40 ea 00 00 c9')
g.label('prepare');g.ref('cd','sram_on')
g.emit('21 %s 11 %s 01 %s cd %s'%(le(PARTY),le(STASH),le(PARTY_LEN),le(COPYDATA)));g.ref('cd','sram_off')
g.emit('21 63 d1 3e 01 22 3e %02x 22 36 ff'%YOU)
g.ref('21','you_struct');g.emit('11 6b d1 01 2c 00 cd '+le(COPYDATA))
g.emit('21 58 d1 11 73 d2 01 0b 00 cd '+le(COPYDATA))                             # OT = player
g.emit('fa 59 d3 ea 77 d1 fa 5a d3 ea 78 d1')                                  # OT ID = player's (else YOU disobeys)
g.emit('21 58 d1 11 b5 d2 01 0b 00 cd '+le(COPYDATA))                             # nickname = player
g.emit('3e 01 ea %s 3e %02x ea 59 d0 3e 01 ea 5d d0 c9'%(le(RIT),OPP))             # battle vs MR. MU (trainer 1)
L=50;HP=200;ST=20
you=bytes([YOU])+HP.to_bytes(2,'big')+bytes([L,0,0,0,0, STRUGGLE,0,0,0, 0,0])+(125000).to_bytes(3,'big')+bytes(10)+b'\x88\x88'+bytes([10,0,0,0,L])+HP.to_bytes(2,'big')+ST.to_bytes(2,'big')*4
assert len(you)==44
g.label('you_struct');g.raw(you)
# ---- after the battle (chamber map script): party back, ????? added (party, else current box)
def idx_ptr(c,base,size):                                                         # de = base + [TMP]*size
    c.emit('21 %s 01 %s fa %s cd %s 54 5d'%(le(base),le(size),le(TMP),le(ADDNTIMES)))
g.label('restore');g.ref('cd','sram_on');g.emit('af ea %s fa 63 d1 fe 02'%le(TMP));g.jr('38','nocatch')
g.emit('21 97 d1 11 %s 01 2c 00 cd %s 3e 01 ea %s'%(le(CAUGHT),le(COPYDATA),le(TMP)))  # party slot 2 = the catch
g.label('nocatch');g.emit('fa %s f5'%le(TMP))
g.emit('21 %s 11 %s 01 %s cd %s'%(le(STASH),le(PARTY),le(PARTY_LEN),le(COPYDATA)))
g.emit('f1 a7');g.ref('ca','rdone')
g.emit('fa 63 d1 fe 06');g.ref('ca','tobox')
g.emit('ea %s 3c ea 63 d1'%le(TMP))                                               # TMP = new slot
g.emit('21 64 d1 fa %s 4f 06 00 09 36 %02x 23 36 ff'%(le(TMP),MIR))
idx_ptr(g,0xd16b,44);g.emit('21 %s 01 2c 00 cd %s'%(le(CAUGHT),le(COPYDATA)))
idx_ptr(g,0xd273,11);g.emit('21 58 d1 01 0b 00 cd '+le(COPYDATA))
idx_ptr(g,0xd2b5,11);g.ref('21','mirname');g.emit('01 0b 00 cd '+le(COPYDATA));g.ref('c3','rdone')
g.label('tobox');g.emit('fa 80 da ea %s 3c ea 80 da'%le(TMP))
g.emit('21 81 da fa %s 4f 06 00 09 36 %02x 23 36 ff'%(le(TMP),MIR))
idx_ptr(g,0xda96,33);g.emit('21 %s 01 21 00 cd %s'%(le(CAUGHT),le(COPYDATA)))
idx_ptr(g,0xdd2a,11);g.emit('21 58 d1 01 0b 00 cd '+le(COPYDATA))
idx_ptr(g,0xde06,11);g.ref('21','mirname');g.emit('01 0b 00 cd '+le(COPYDATA))
g.label('rdone');g.ref('cd','sram_off');g.emit('3e 03 ea %s c9'%le(RIT))
g.label('mirname');g.raw(enc('?????').ljust(11,b'\x50'))
# ---- battle hooks. Entered through Bankswitch from the bank F stubs below: [sp+6] = return address into the
#      hooked code (the stubs jump to farcall without a call), so a routine can send the battle elsewhere.
F_RET=0x7e15                                                                      # a "ret" in bank F (farcall's)
g.label('redirect');g.emit('21 06 00 39 73 23 72 c9')                              # [sp+6] = de
g.label('skip3');g.emit('21 06 00 39 7e c6 03 22 d0 34 c9')                         # skip the hooked "call PrintText"
# F:5000 battle menu (TMP = 0 FIGHT, 1 PKMN, 2 ITEM, 3 RUN): MR. MU -> FIGHT only, MIRAGE -> ITEM only
g.label('menu');g.emit('fa %s 3d fe 02'%le(RIT));g.jr('30','menu_ok')
g.emit('87 47 fa %s b8'%le(TMP));g.jr('28','menu_ok')
g.emit('fa %s fe 01'%le(RIT));g.ref('21','t_block1');g.jr('28','menu_pt');g.ref('21','t_block2')
g.label('menu_pt');g.emit('cd '+le(PRINTTEXT));g.emit('11 '+le(DISPLAYBATTLEMENU));g.ref('c3','redirect')
g.label('menu_ok');g.emit('fa %s a7 c8 11 %s'%(le(TMP),le(MENU_NOT_FIGHT)));g.ref('c3','redirect')
# F:5629 SelectEnemyMove: MR. MU / ????? never act (wEnemySelectedMove = FF, return)
g.label('select');g.emit('fa %s 3d fe 02'%le(RIT));g.jr('30','select_n')
g.emit('3e ff ea dd cc 11 '+le(F_RET));g.ref('c3','redirect')
g.label('select_n');g.emit('fa 2b d1 ea %s c9'%le(TMP))
# F:4603 "Enemy X fainted!": MR. MU dies (gravestone bit)
g.label('fainted');g.emit('21 %s fa %s fe 01 c0 fa d8 cf fe %02x c0'%(le(ENEMYFAINTEDTEXT),le(RIT),MU))
g.emit('21 %s cb %02x'%(le(KILL_BYTE),0xc6+8*(KILL_MASK.bit_length()-1)));pt(g,'t_mu_died');g.ref('c3','skip3')
# F:4A65 "<TRAINER> sent out X!": MR. MU steps in / the MIRAGE appears (-> phase 2, the battle counts as wild so
#        the MASTER BALL can be thrown; dex slot 152 marked owned so no dex page / nickname prompt follows)
g.label('sentout');g.emit('21 %s fa %s 3d fe 02 d0 fa d8 cf fe %02x'%(le(TRAINERSENTOUTTEXT),le(RIT),MIR))
g.ref('21','t_mu_out');g.jr('20','so_pt')
g.emit('3e 02 ea %s 3e 01 ea 57 d0 21 09 d3 cb fe'%le(RIT));g.ref('21','t_mir_out')
g.label('so_pt');g.emit('cd '+le(PRINTTEXT));g.ref('c3','skip3')
# F:50DF UseBagItem: MIRAGE phase -> only the MASTER BALL
g.label('usebag');g.emit('fa 5a d0 ea %s fa %s fe 02 c0 fa 91 cf fe %02x c8'%(le(TMP),le(RIT),MASTERBALL))
pt(g,'t_block2');g.emit('11 '+le(BAGWASSELECTED));g.ref('c3','redirect')
# F:6792 ExecuteEnemyMove: "MR. MU doesn't fight back." / "????? stares at you..."
g.label('enemyturn');g.emit('fa dd cc ea %s fa %s 3d fe 02 d0 21 e6 cf 2a b6 c8'%(le(TMP),le(RIT)))
g.emit('fa %s fe 01'%le(RIT));g.ref('21','t_mu_idle');g.jr('28','et_pt');g.ref('21','t_mir_idle')
g.label('et_pt');g.emit('c3 '+le(PRINTTEXT))
for k,(paras,end) in B.items():g.label('t_'+k);g.raw(txt(paras,end=end))
g2=g.finish();assert 0x5820+len(g2)<0x5f00,len(g2)                  # 2E:6000-67FF stays free for the test ROMs' save
rom.put(fo(0x2e,0x5820),g2,'Bank 2E: MR. MU ritual battle (party swap, battle hooks, texts)')
labels['bank2e']={k:hex(v) for k,v in g.labels.items()}

# gravestone list: MR. MU (chamber object 1) gets kill index 33 next to v14's gym leaders
ltab=int(L14['ltab'],16);lt=bytearray()
o=fo(0x2e,ltab)
while r[o]!=0xff:lt+=r[o:o+3];o+=3
lt+=bytes([CHAMBER,1,KILL_IDX,0xff])
LTAB=0x5f00;assert LTAB+len(lt)<0x6000;rom.put(fo(0x2e,LTAB),lt,'Bank 2E: gravestone list + MR. MU (chamber object 1, kill index 33)')
lg=fo(0x2e,int(L14['leader_graves'],16))
rom.data(lg+1,bytes.fromhex(le(LTAB)),'Leader-grave list -> v23 list (+ MR. MU)',le(ltab))

# ================================================================================================================
# 4. Bank F stubs (only small gaps left there): hl = far routine, jump to farcall, which returns a = [TMP]
F={}
c=Code(0xf,0x7e0d)
c.label('farcall');c.emit('06 2e cd %s fa %s c9'%(le(BANKSWITCH),le(TMP)));assert c.org+len(c.b)-1==F_RET
c.label('t_menu');c.emit('ea '+le(TMP));c.emit('21 '+le(g.labels['menu']));c.jr('18','farcall')
fb=c.finish();assert 0x7e0d+len(fb)<=0x7e20;rom.put(fo(0xf,0x7e0d),fb,'Bank F: far-call stub + battle menu stub');F.update(c.labels)
for org,end,names in ((0x7e41,0x7e50,('fainted','sentout','enemyturn')),(0x7e78,0x7e80,('usebag',))):
    c=Code(0xf,org)
    for n in names:c.label('t_'+n);c.emit('21 '+le(g.labels[n]));c.jr('18','farcall')
    fb=c.finish({'farcall':F['farcall']});assert org+len(fb)<=end
    rom.put(fo(0xf,org),fb,'Bank F: battle stubs '+'/'.join(names));F.update(c.labels)
c=Code(0xf,0x7fb2);c.label('t_select');c.emit('21 '+le(g.labels['select'])+' c3 '+le(F['farcall']))
fb=c.finish();rom.put(fo(0xf,0x7fb2),fb,'Bank F: SelectEnemyMove stub');F.update(c.labels)
labels['bankF']={k:hex(v) for k,v in F.items()}
rom.hook(fo(0xf,0x5000),'cd'+le(F['t_menu']),'Battle menu: MR. MU / MIRAGE command limits','a7 20 62',provides=('a','f'))
rom.hook(fo(0xf,0x5629),'cd'+le(F['t_select']),'SelectEnemyMove: MR. MU / ????? never attack','fa 2b d1',provides=('a',))
rom.hook(fo(0xf,0x4603),'cd'+le(F['t_fainted']),'Enemy fainted text: MR. MU dies','21'+le(ENEMYFAINTEDTEXT),provides=('h','l'))
rom.hook(fo(0xf,0x4a65),'cd'+le(F['t_sentout']),'Sent-out text: MR. MU / the MIRAGE','21'+le(TRAINERSENTOUTTEXT),provides=('h','l'))
rom.hook(fo(0xf,0x50df),'cd'+le(F['t_usebag']),'UseBagItem: MIRAGE phase -> MASTER BALL only','fa 5a d0',provides=('a',))
rom.hook(fo(0xf,0x6792),'cd'+le(F['t_enemyturn']),'Enemy turn: MR. MU / ????? stand still','fa dd cc',provides=('a',))

# 5. Bank 15: no EXP from MR. MU (the player alone as YOU)
c=Code(0x15,0x6a70);c.label('noexp');c.emit('fa %s 3d fe 02'%le(RIT));c.jr('38','skip');c.emit('fa 2b d1 c9')
c.label('skip');c.emit('e1 c9')
b15=c.finish();rom.put(fo(0x15,0x6a70),b15,'Bank 15: GainExperience skipped in the MR. MU battle')
rom.hook(fo(0x15,0x524f),'cd'+le(c.labels['noexp']),'GainExperience: none in the MR. MU battle','fa 2b d1',provides=('a',))
labels['bank15']={k:hex(v) for k,v in c.labels.items()}

# 6. Bank 1: predef wrappers. 08 MoveAnimation: the MASTER BALL toss that catches ????? leaves a pure black ball.
#    4F AskName: ????? keeps its name (AskName's own GHOST path).
c=Code(1,0x7d20)
c.label('anim');c.emit('fa 7c d0 ea %s 21 %s 06 %02x cd %s'%(le(TMP2),le(MOVEANIM[1]),MOVEANIM[0],le(BANKSWITCH)))
c.emit('fa %s fe 02 c0 fa %s fe %02x c0 fa 1e d1 fe %02x c0'%(le(RIT),le(TMP2),TOSS_ANIM,CAUGHT_ANIMDATA))
c.emit('3e ff e0 48 e0 49 0e 28 c3 '+le(DELAYFRAMES))                            # OBP0/OBP1 all black
c.label('askname');c.emit('fa 91 cf fe %02x ca %s c3 %s'%(MIR,le(ASKNAME_SPECIESNAME),le(ASKNAME)))
b1=c.finish();rom.put(fo(1,0x7d20),b1,'Bank 1: predef wrappers (black MASTER BALL, ????? not nicknamed)')
labels['bank1']={k:hex(v) for k,v in c.labels.items()}
assert r[PREDEFS+3*8:PREDEFS+3*8+3]==bytes([MOVEANIM[0]])+bytes.fromhex(le(MOVEANIM[1]))
rom.data(PREDEFS+3*8,bytes([1])+bytes.fromhex(le(c.labels['anim'])),'Predef 08 MoveAnimation -> wrapper (black ball)',r[PREDEFS+3*8:PREDEFS+3*8+3])
rom.data(PREDEFS+3*0x4f,bytes([1])+bytes.fromhex(le(c.labels['askname'])),'Predef 4F AskName -> wrapper (?????)','01'+le(ASKNAME))

# ================================================================================================================
# 7. The chamber: MR. MU's talk (text 1) and the after-battle map script
T={
 'speech':[["MR. MU: So...","We meet again."],["...And for the","last time."],
           ["Forgive me,","child. I followed","you and I tested","you."],
           ["But it was no","lie. I have long","sought a","successor."],
           ["I had to be sure","that you were","truly worthy."],
           ["I have watched","you for a long","time, <PLAYER>."],["Longer than you","could ever know."],
           ["...No. It would","be more fitting","to say..."],["...that I gave","birth to you."],
           ["Hm... But no more","of that."],
           ["Long ago, my","people settled","in LAVENDER."],["We sought a way","to carry souls","beyond death."],
           ["In each age, one","was chosen to","become the","BLACK TAMER."],
           ["I was such a","candidate. But I","failed the","transformation."],
           ["I believed I was","unworthy. That I","could not accept","death."],
           ["But you...","You have that","resolve."],
           ["You are the one","who can lead","humanity beyond","death."],
           ["That was never","my destiny. And","now I can accept","my own end..."],
           ["...gladly. For","you will carry","humanity beyond."],
           ["Now listen. The","MIRAGE that has","been stalking","you..."],
           ["It is my missing","half. I have no","hold over it."],
           ["To draw it into","the ritual circle","you must kill me."],
           ["Be warned. When","it comes, it will","be more restless","than ever."],
           ["It will seek a","replacement."],["You will know","what you must do."],
           ["AGATHA kept the","vessel for this","night. Take it."]],
 'question':[["One last thing.","Tell me..."],["Is there life","after death?"]],
 'yes':[["...Is that so?","Then perhaps we","will meet again."]],
 'no':[["...I see. Then","this is truly","goodbye."]],
 'notest':[["Do not worry.","That was no test."],["There is no right","answer. I only","wished to know."],
           ["Now, <PLAYER>...","End me with your","own hands!"]],
 'bagfull':[["MR. MU: ...","Your bag is full,","child."],["Make room, then","come back."]],
 'boxfull':[["MR. MU: ...","Your PC BOX is","full, child."],["Make room, then","come back."]],
 'grave':[["Here lies","MR. MU..."]],
}
c=Code(0x18,0x67e0)
def pt18(label):c.ref('21',label);c.emit('cd '+le(PRINTTEXT))
c.label('mu');c.emit('08 fa %s fe 03'%le(RIT));c.jr('30','grave')   # (his gravestone is silent; fallback only)
c.emit('fa 1d d3 fe 14');c.jr('28','bagfull')                                       # 20 item kinds: no room for the ball
c.emit('fa 63 d1 fe 06');c.jr('20','room');c.emit('fa 80 da fe 14');c.jr('28','boxfull')   # nowhere to put ?????
c.label('room');pt18('t_speech')
c.emit('01 %02x 01 cd %s'%(MASTERBALL,le(GIVEITEM)));pt18('t_ball')
pt18('t_question');c.emit('cd %s fa 26 cc a7'%le(YESNO));c.ref('21','t_yes');c.jr('28','ans');c.ref('21','t_no')
c.label('ans');c.emit('cd '+le(PRINTTEXT));pt18('t_notest')
c.emit(far(g.labels['prepare'],0x2e));c.jr('18','end')
c.label('bagfull');c.ref('21','t_bagfull');c.jr('18','one')
c.label('boxfull');c.ref('21','t_boxfull');c.jr('18','one')
c.label('grave');c.ref('21','t_grave')
c.label('one');c.emit('cd '+le(PRINTTEXT))
c.label('end');c.emit('c3 '+le(TEXTEND))
c.label('script');c.emit('fa %s a7'%le(RIT));c.jr('28','s_end');c.emit('fe 03');c.jr('30','s_end')
c.emit('fa 59 d0 a7');c.jr('20','s_end');c.emit(far(g.labels['restore'],0x2e))
c.label('s_end');c.emit('c3 '+le(AUTOTEXT))
for k,v in T.items():c.label('t_'+k);c.raw(txt(v,end=0x57 if k=='question' else 0x58))
c.label('t_ball');c.raw(txt([["<PLAYER> received","the MASTER BALL!"]],end=0x50)+bytes([0x0b,0x06,0x50]))
b18=c.finish();assert 0x67e0+len(b18)<=0x67e0+3104,len(b18)
rom.put(fo(0x18,0x67e0),b18,'Bank 18: MR. MU last talk + chamber after-battle script')
labels['bank18']={k:hex(v) for k,v in c.labels.items()}
HDR=int(L22['header'],16);TEXTS=int(L22['texts'],16);assert w(0x1ae+2*CHAMBER)==HDR
rom.data(fo(0x18,TEXTS),bytes.fromhex(le(c.labels['mu'])),'Chamber text 1 (MR. MU) -> v23 last talk',r[fo(0x18,TEXTS):fo(0x18,TEXTS)+2])
rom.data(fo(0x18,HDR)+7,bytes.fromhex(le(c.labels['script'])),'Chamber map script -> v23 (party back after the battle)',r[fo(0x18,HDR)+7:fo(0x18,HDR)+9])

rom.finish('Creepy_Black_Mu_v23.gb','manifest_v23.json','CREEPY MU V23',extra=dict(labels=labels,
           pics=dict(mu=len(gent),mirage_front=len(mir_front),mirage_back=len(mir_back))))

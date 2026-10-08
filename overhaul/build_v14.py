# Creepy Black Mu v14: Mirage RNG fix, earlier Ghost hunger, YOU without the Poke Ball, GENTLEMAN -> GAMBLER,
# PRETA/AZHI keep the Kabutops/Aerodactyl dex hidden, killable gym leaders + revenge, killer rumours in towns.
# Logged patches on top of verified Mu v13 (patchlib: every hook is checked by the patch guard).
from patchlib import *
from patchguard import fo

V13_SHA='2fa351de1eca04f63f96abe47469287eccfc3754f6437c0411d5f81ecf7098a4'
rom=Rom('Creepy_Black_Mu_v13.gb',V13_SHA)
r=rom.r
PRINTTEXT,TEXTEND,PREDEF,RANDOM,DISPLAYTEXTID,GIVEITEM,ENGAGE,FARCALL=0x3c94,0x2504,0x3ec1,0x3eb0,0x294d,0x3e82,0x33ac,0x3618
MURDER=0xd453
labels={}

# 1. Mirage roll: mirage_start (2E:4300) compared hRandomAdd with its chance, but the wild-encounter check that leads
#    there had just required hRandomAdd < grass rate. Grass rate <= chance, so every encounter became the Mirage.
#    Now it draws a fresh random number.
g=Code(0x2e,0x4e00)
g.label('mirage_rand');g.emit('47 cd '+le(RANDOM)+' c9')                        # ld b,a ; call Random ; ret
# 0. GHOST award fix (bug since v1): v1 moved the base game's award (AddPartyMon GHOST) from before the rival
#    battle to after it, where wMonDataLocation (CC49) can still be non-zero from the battle (seen: 4). Then
#    AddPartyMon puts GHOST in the ENEMY party and the player never gets it. Now CC49 is cleared first.
g.label('award_add');g.emit('af ea 49 cc c3 5b 39')                             # xor a ; ld [CC49],a ; jp AddPartyMon

# 6b. Map load: gym leaders killed with CURSE join the base game's gravestone list (D486: sprite, 0, kill index).
#     Kill indices 26-32 follow the base game's 0-25 (12 = BROCK, already in the base list).
LEADERS=[  # name, gym map, bank, kill idx, badge, badge bit, pronoun, beat event, TM item, got-TM bit, joy, victory, deactivate, engage
 ('MISTY',   0x41,0x17,26,'CASCADEBADGE',1,'her',(0xd75e,7),0xd3,(0xd75e,6),0x471d,0x474b,(0x4755,'21 5e d7 cb d6 cb de'),0x47bd),
 ('LT.SURGE',0x5c,0x17,27,'THUNDERBADGE',2,'him',(0xd773,7),0xe0,(0xd773,6),0x4aba,0x4ae8,(0x4af2,'fa 73 d7 f6 1c ea 73 d7'),0x4b69),
 ('ERIKA',   0x86,0x12,28,'RAINBOWBADGE',3,'her',(0xd77c,1),0xdd,(0xd77c,0),0x495e,0x498c,(0x4996,'fa 7c d7 f6 fc ea 7c d7 21 7d d7 cb c6'),0x4a48),
 ('KOGA',    0x9d,0x1d,29,'SOULBADGE',   4,'him',(0xd792,1),0xce,(0xd792,0),0x5492,0x54c0,(0x54ca,'fa 92 d7 f6 fc ea 92 d7'),0x556b),
 ('SABRINA', 0xb2,0x17,30,'MARSHBADGE',  5,'her',(0xd7b3,1),0xf6,(0xd7b3,0),0x5078,0x50a6,(0x50b0,'fa b3 d7 f6 fc ea b3 d7 21 b4 d7 cb c6'),0x5164),
 ('BLAINE',  0xa6,0x1d,31,'VOLCANOBADGE',6,'him',(0xd79a,1),0xee,(0xd79a,0),0x5852,0x5880,(0x588a,'fa 9a d7 f6 fc ea 9a d7 21 9b d7 cb c6'),0x58bc),
 ('GIOVANNI',0x2d,0x1d,32,'EARTHBADGE',  7,'him',(0xd751,1),0xe3,(0xd751,0),0x4990,0x49be,(0x49c8,'fa 51 d7 f6 fc ea 51 d7 fa 52 d7 f6 03 ea 52 d7'),0x4abb),
]
BROCK=('BROCK',0x36,0x17,12,'BOULDERBADGE',0,'him')
def killbit(idx):return 0xd4a4+(idx>>3),1<<(idx&7)
g.label('leader_graves');g.ref('21','ltab');g.emit('fa 5e d3 47')
g.label('lg_loop');g.emit('2a fe ff c8 b8');g.jr('28','lg_found');g.emit('23 23');g.jr('18','lg_loop')
g.label('lg_found');g.emit('2a 57 5e 21 86 d4')                                   # d = sprite, e = kill index
g.label('lg_end');g.emit('7e 3c');g.jr('28','lg_put');g.emit('23 23 23');g.jr('18','lg_end')
g.label('lg_put');g.emit('72 23 36 00 23 73 23 36 ff c9')
g.label('ltab')
for L in LEADERS:g.raw([L[1],1,L[3]])                                             # every leader is object 1 of its gym
g.raw([0xff])

# 2. Town rumours: after the first CURSE murder (D453) some flavour NPCs talk about a killer, blamed on TEAM ROCKET.
RUMOURS={  # (map, text id): paragraphs
 (0x00,2):[["Did you hear?","Someone's killing","trainers on the","routes!"],["Mom says it's","TEAM ROCKET.","I'm scared..."]],
 (0x01,1):[["A trainer was","found dead on a","route!"],["His #MON too.","Everybody says","TEAM ROCKET did","it!"]],
 (0x02,1):[["They say a new","ROCKET member","kills trainers","for fun."],["Not even #MON","are spared!"]],
 (0x03,3):[["The POLICE say a","trainer is out","there killing"],["other trainers","and #MON too!"],["Bet it's TEAM","ROCKET's doing!"]],
 (0x03,5):[["A ROCKET grunt","bragged about a","killer trainer."],["He said the BOSS","wants to recruit","him!"]],
 (0x04,2):[["More graves come","every day..."],["Trainers and","their #MON,","killed by a black","shadow, they say."],["Some say it's a","ROCKET assassin."]],
 (0x05,1):[["Lock your doors!","A murderer is","loose in KANTO!"],["They say TEAM","ROCKET pays him","for every kill!"]],
 (0x05,4):[["My workers won't","go on the routes."],["Some ROCKET","killer is picking","off trainers!"]],
 (0x06,1):[["A bad trainer","killed my brother","and his #MON!"],["TEAM ROCKET is","the worst!"]],
 (0x06,4):[["The GAME CORNER","guys say a killer","works for them."],["Trainers keep","turning up dead!"]],
 (0x07,4):[["The WARDEN found","a dead trainer"],["by the SAFARI","ZONE. ROCKETs,","for sure!"]],
 (0x08,1):[["Even out here we","hear about it..."],["A trainer who","kills people and","#MON alike."],["They say he's","TEAM ROCKET's","secret weapon."]],
 (0x0a,3):[["Heh, heard about","the killer?"],["The BOSS wants","him in TEAM","ROCKET!"]],
 (0x0a,10):[["ROCKET is gone,","but the killer"],["is still out","there..."]],
}
def map_header(mp):
    bank=r[0xc23d+mp];h=fo(bank,r[0x1ae+2*mp]|r[0x1af+2*mp]<<8);return bank,h
for (mp,tid),paras in sorted(RUMOURS.items()):
    g.label('rumour_%02x_%d'%(mp,tid));g.raw(txt(paras,end=0x57))

# 7. PRETA/AZHI (species B6/B7) never mark Kabutops/Aerodactyl as seen.
seenF=Code(0xf,0x7d2b)
seenF.label('seen');seenF.emit('f5 fa d8 cf fe b6');seenF.jr('28','seen_skip');seenF.emit('fe b7');seenF.jr('28','seen_skip')
seenF.emit('f1 c3 '+le(PREDEF));seenF.label('seen_skip');seenF.emit('f1 c9')
bS=seenF.finish();assert 0x7d2b+len(bS)<=0x7d40
rom.put(fo(0xf,0x7d2b),bS,'Bank F: PRETA/AZHI (B6/B7) not marked seen')
codeF=Code(0xf,0x7cc0)
# 4. YOU (stand-in species 79) comes out without the Poke Ball: no poof, picture drawn at full size at once
#    (AnimateSendingOutMon's out-of-battle path, the one Pokedex/status screens use).
codeF.label('poof');codeF.emit('f5 fa 14 d0 fe 79');codeF.jr('28','poof_skip');codeF.emit('f1 c3 ed 6f')
codeF.label('poof_skip');codeF.emit('f1 c9')
codeF.label('grow');codeF.emit('f5 fa 14 d0 fe 79');codeF.jr('28','grow_you');codeF.emit('f1 c3 '+le(PREDEF))
codeF.label('grow_you');codeF.emit('fa 57 d0 f5 af ea 57 d0 3e 02 cd '+le(PREDEF)+' f1 ea 57 d0 f1 c9')
bF=codeF.finish();assert codeF.org+len(bF)<=0x7d00
rom.put(fo(0xf,0x7cc0),bF,'Bank F: YOU sent out without the Poke Ball')

g2=g.finish();rom.put(fo(0x2e,0x4e00),g2,'Bank 2E: Mirage random, leader gravestones, town rumours')
labels['bank2e']={k:hex(v) for k,v in g.labels.items()};labels['bankF']={k:hex(v) for k,v in {**codeF.labels,**seenF.labels}.items()}

rom.hook(fo(0x2e,0x4029),'cd'+le(g.labels['award_add']),'GHOST award: AddPartyMon into the PLAYER party (CC49 = 0)','cd 5b 39')
rom.hook(fo(0x2e,0x4326),'cd'+le(g.labels['mirage_rand']),'Mirage roll: fresh random number (was the encounter roll)','47 f0 d3',provides=('a','b'))
# Hunger at the start: 67 points = ~400 steps until GHOST eats (was 160 = ~960 steps).
rom.data(fo(0x2e,0x41ea),bytes.fromhex('3e 43'),'GHOST starts hungrier: 67 (~400 steps to the first meal)','3e a0')
rom.hook(fo(0xf,0x6cfd),'cd'+le(seenF.labels['seen']),'LoadEnemyMonData: PRETA/AZHI not added to the Pokedex','cd c1 3e')
rom.hook(fo(0xf,0x4d0e),'cd'+le(codeF.labels['poof']),'SendOutMon: no Poke Ball poof for YOU','cd ed 6f')
rom.hook(fo(0xf,0x4d16),'cd'+le(codeF.labels['grow']),'SendOutMon: YOU appears at full size','cd c1 3e')

# v6 PRETA award also set Kabutops owned/seen: removed.
AW=bytes.fromhex('21 08 d3 cb e6 21 1b d3 cb e6')
o=r.find(AW,fo(0x2e,0x4600),fo(0x2e,0x4700));assert o>0
rom.code(o,bytes(len(AW)),'PRETA award: Kabutops dex flags no longer set',AW.hex())

# 5. GENTLEMAN (sprite 10) -> GAMBLER (0B) everywhere but Mr. Mu (Pallet, Cerulean trade house, Mansion 1F).
MU_MAPS={0x00,0x3f,0xa5}
def objects(o):
    p=o+1;p+=1+4*r[p];p+=1+3*r[p];n=r[p];p+=1;out=[]
    for i in range(n):
        t=r[p+5];size=6+(2 if t&0x40 else 0)+(1 if t&0x80 else 0);out.append(p);p+=size
    return out
swapped=[]
for mp in range(0xf8):
    if mp in MU_MAPS or mp in (0x0b,):continue               # 0x0B is an unused map id (header points at code)
    bank=r[0xc23d+mp];hp=r[0x1ae+2*mp]|r[0x1af+2*mp]<<8
    if hp<0x4000 or bank==0:continue
    h=fo(bank,hp);n=bin(r[h+9]&15).count('1');oo=fo(bank,r[h+10+11*n]|r[h+11+11*n]<<8)
    for p in objects(oo):
        if r[p]==0x10:rom.data(p,[0x0b],'map %02x object: GENTLEMAN -> GAMBLER sprite'%mp,'10');swapped.append(mp)
assert len(swapped)==24,swapped
SAFFRON_SET=0x17ab9+11*6+4                                   # sprite set 7 (Saffron), slot 5
rom.data(SAFFRON_SET,[0x0b],'Saffron sprite set: GENTLEMAN -> GAMBLER','10')
rom.data(0x39952+5*(41-1),bytes.fromhex('2154'),'GENTLEMAN trainer pic -> GAMBLER pic','d073')

# 6. Gym leaders. CURSE now kills every gym leader like BROCK already could: the leader gets a kill index,
#    turns into a gravestone, the murder counts (D453, police), the badge and TM are taken from the body,
#    and the gym trainers who are left are NOT deactivated: they still fight and swear revenge.
home=Code(0,0xce)            # TalkToTrainer's before-battle text: gym banks get a chance to swap it
home.emit('f0 b8 fe 17');home.jr('28','go');home.emit('fe 12');home.jr('28','go');home.emit('fe 1d c2 '+le(PRINTTEXT))
home.label('go');home.emit('c3 00 7a')
hb=home.finish();assert len(hb)==18;rom.put(0xce,hb,'Home: TalkToTrainer revenge-text dispatch (gym banks 17/12/1D)')

rom.hook(0x3234,'cd'+le(0xce),'TalkToTrainer: gym trainers swear revenge for a killed leader','cd'+le(PRINTTEXT))

def revenge_text(name,pron):
    return txt([[name+' is dead!','You murdered '+pron+'!'],["I'll avenge my","LEADER, murderer!"]])
def map_texts(mp):
    """text table and its length (the trainer headers follow it; the script loads them with ld hl first)"""
    bank,h=map_header(mp);tp=r[h+5]|r[h+6]<<8;sp=r[h+7]|r[h+8]<<8
    seg=r[fo(bank,sp):fo(bank,sp)+40];i=seg.find(bytes.fromhex('cd873c21'))
    end=seg[i+4]|seg[i+5]<<8 if i>=0 else None
    return bank,h,tp,end
banks={}
for L in [BROCK]+LEADERS:banks.setdefault(L[2],[]).append(L)
for bank,Ls in banks.items():
    c=Code(bank,0x7a00)
    # revenge: hl = before-battle text of a gym trainer who hasn't been beaten yet
    c.emit('d5 c5 e5');c.ref('21','tab');c.emit('fa 5e d3 47')
    c.label('lp');c.emit('2a fe ff');c.jr('28','none');c.emit('b8');c.jr('28','found');c.emit('23 23 23 23');c.jr('18','lp')
    c.label('found');c.emit('2a 5f 16 d4 1a a6');c.jr('28','none');c.emit('23 2a 66 6f f1');c.jr('18','out')
    c.label('none');c.emit('e1')
    c.label('out');c.emit('c1 d1 c3 '+le(PRINTTEXT))
    c.label('tab')
    for L in Ls:
        a,mask=killbit(L[3]);c.raw([L[1],a&0xff,mask]);c.ref('','rev_'+L[0])
    c.raw([0xff])
    for L in Ls:c.label('rev_'+L[0]);c.raw(revenge_text(L[0],L[6]))
    for k,L in enumerate(Ls):
        if L[0]=='BROCK':continue
        name,mp,_,idx,badge,bbit,pron,beat,tm,got,joy,vic,(dsite,dold),eng=L
        a,mask=killbit(idx)
        _,_,tp,end=map_texts(mp)
        if name=='BLAINE':end=0x58b7                             # Cinnabar's table ends where its battle-start code begins
        L=Ls[k]=L+((end-tp)//2+1,)                               # new text id = table length + 1
        c.label('eng_'+name)                                     # leader battle: remember the leader's kill index
        if name=='BLAINE':                                       # Cinnabar's battle start is shared with the quiz trainers
            c.emit('f5 fa 13 cf fe 01 3e %02x'%idx);c.jr('28','eng_b');c.emit('af');c.label('eng_b')
        else:c.emit('f5 3e %02x'%idx)
        c.emit('ea af d4 af ea ae d4 f1 c3 '+le(ENGAGE))
        c.label('joy_'+name)                                     # post-battle: killed leader -> badge + TM from the body
        c.emit('f5 fa %s e6 %02x'%(le(a),mask));c.jr('20','killed_'+name);c.emit('f1 3e f0 ea 6b cd c9')
        c.label('killed_'+name);c.emit('f1 e1 3e f0 ea 6b cd')
        c.emit('21 %s cb %02x'%(le(beat[0]),0xc6+8*beat[1]))
        c.emit('3e %02x e0 8c cd %s'%(L[-1],le(DISPLAYTEXTID)))
        c.emit('01 01 %02x cd %s'%(tm,le(GIVEITEM)));c.jr('30','nobag_'+name)
        c.emit('21 %s cb %02x'%(le(got[0]),0xc6+8*got[1]))
        c.label('nobag_'+name);c.emit('c3 '+le(vic))
        c.label('deact_'+name)                                   # gym trainers stay active while their leader is dead
        c.emit('fa %s e6 %02x c0 '%(le(a),mask)+dold+' c9')
        c.label('took_'+name);c.raw(txt([['<PLAYER> took the',badge+' from',name+"'s body."]],end=0x57))
        c.label('ttab_'+name)
        c.raw(r[fo(bank,tp):fo(bank,tp)+2*(L[-1]-1)]);c.ref('','took_'+name)
    if bank==0x17:                                               # Pewter: base game kills BROCK; keep its trainer active
        a,mask=killbit(12);c.label('deact_BROCK');c.emit('fa %s e6 %02x c0 21 55 d7 cb d6 c9'%(le(a),mask))
    code=c.finish();assert 0x7a00+len(code)<=0x8000,(bank,len(code))
    rom.put(fo(bank,0x7a00),code,'Bank %02X: gym leader kill / revenge code'%bank)
    labels['bank%02x'%bank]={k:hex(v) for k,v in c.labels.items()}
    for L in Ls:
        if L[0]=='BROCK':
            rom.hook(fo(bank,0x4437),'cd'+le(c.labels['deact_BROCK'])+'0000','Pewter Gym: trainer stays active if BROCK was killed','21 55 d7 cb d6')
            continue
        name,mp,_,idx,badge,bbit,pron,beat,tm,got,joy,vic,(dsite,dold),eng,newid=L
        _,h,tp,_=map_texts(mp)
        rom.data(h+5,bytes.fromhex(le(c.labels['ttab_'+name])),'%s gym: text table + "took the badge" text (id %d)'%(name,newid),le(tp))
        rom.hook(fo(bank,eng),'cd'+le(c.labels['eng_'+name]),'%s battle: kill index %d'%(name,idx),'cd'+le(ENGAGE))
        rom.hook(fo(bank,joy),'cd'+le(c.labels['joy_'+name])+'0000','%s post-battle: killed -> badge/TM from the body'%name,'3e f0 ea 6b cd')
        n=len(bytes.fromhex(dold))
        rom.hook(fo(bank,dsite),'cd'+le(c.labels['deact_'+name])+'00'*(n-3),'%s victory: trainers stay active if killed'%name,dold,
                 reviewed='17:50fd is trainer-header data (30 b3 d7 = sight range 3, event byte d7b3), not a jr' if name=='SABRINA' else None)

# gravestone list: base map load builds D486 and returns; now it also appends a killed leader
b3=Code(3,0x7fa3);b3.emit('cd 2d 4e '+far(g.labels['leader_graves'],0x2e))
rom.put(fo(3,0x7fa3),b3.finish(),'Bank 3: after the gravestone list, add killed gym leaders')
rom.code(fo(3,0x7f88),bytes.fromhex('21 a2 4e c3 a3 7f'),'Map load: gravestone list -> leader graves','21 a2 4e c3 2d 4e')

# town rumours: TX_ASM wrapper in each map's text bank, rumour text (TX_FAR) in 2E
RUMOUR_SPACE={0x06:0x7400,0x11:0x7400,0x07:0x7800,0x14:0x7000}
cursor=dict(RUMOUR_SPACE)
for (mp,tid),paras in sorted(RUMOURS.items()):
    bank,h=map_header(mp);tp=r[h+5]|r[h+6]<<8;e=fo(bank,tp)+2*(tid-1);orig=r[e]|r[e+1]<<8
    assert r[fo(bank,orig)]==0x17,(hex(mp),tid)                        # plain TX_FAR text: flavour only
    at=cursor[bank];c=Code(bank,at)
    c.emit('08 fa %s a7 21 %s'%(le(MURDER),le(orig)));c.jr('28','print');c.ref('21','far')
    c.label('print');c.emit('cd %s c3 %s'%(le(PRINTTEXT),le(TEXTEND)))
    c.label('far');c.emit('17 %s 2e 50'%le(g.labels['rumour_%02x_%d'%(mp,tid)]))
    code=c.finish();rom.put(fo(bank,at),code,'map %02x text %d: killer rumour after a murder'%(mp,tid));cursor[bank]+=len(code)
    rom.data(e,bytes.fromhex(le(at)),'map %02x text %d -> rumour wrapper'%(mp,tid),le(orig))

sha=rom.finish('Creepy_Black_Mu_v14.gb','manifest_v14.json','CREEPY MU V14',extra=dict(labels=labels))

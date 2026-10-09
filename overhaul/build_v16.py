# Creepy Black Mu v16: AGATHA's quest (GHOST route), part 1: Pokemon Tower hostage, the three relics, the vessel
# (MASTER BALL), GHOST's power, the consort (MISTY / ERIKA / SABRINA + HELIX FOSSIL).
# Logged patches on top of verified Mu v15 (patchlib).
from patchlib import *
from patchguard import fo

V15_SHA='174e9328c2f56f25d39e5a03b30c28659fdeec6eeef515ecffca6c2eb55d77b3'
rom=Rom('Creepy_Black_Mu_v15.gb',V15_SHA)
r=rom.r
PRINTTEXT,TEXTEND,YESNO,GIVEITEM,ADDNTIMES=0x3c94,0x2504,0x362e,0x3e82,0x3abb
REMOVEITEM=(5,0x7f51)                    # RemoveItemByID, item in hItemToRemoveID (FFDB)
GHOST_ROUTE=0xd451;TEMP=0xd457;ARG=0xd458
# new saved RAM (inside D450-D4A3, cleared on NEW GAME)
STAGE=0xd464     # 0 not started, 1 relics asked, 2 vessel asked, 3 GHOST power, 4 consort, 5 consort found
CONSORT=0xd465   # 0 none, 1 MISTY, 2 ERIKA, 3 SABRINA
QFLAGS=0xd466    # bit0 quest failed, bit1 AGATHA gone (left the Tower after the failure), bit2 "Mu woke them" said
EV_RESCUED_FUJI=(0xd769,7)                # set by FUJI's 7F text (with D7E0.7) right before the warp home
EV_GOT_MASTERBALL=(0xd838,5)              # Silph Co. president (18:62DC)
DEX_OWNED_FOSSILS=(0xd308,0x2a)           # owned OMANYTE #138, KABUTO #140, AERODACTYL #142: only from the Cinnabar lab
DOME,HELIX,AMBER,MASTERBALL=0x29,0x2a,0x1f,0x01
PRETA,AZHI,GHOST=0xb6,0xb7,0x1f
GIRLS=[  # n, name, gym map, bank, beat event, kill bit (D4A7), sprite
 (1,'MISTY',  0x41,0x17,(0xd75e,7),0x04,0x1d),
 (2,'ERIKA',  0x86,0x12,(0xd77c,1),0x10,0x1b),
 (3,'SABRINA',0xb2,0x17,(0xd7b3,1),0x40,0x0d),
]
AGATHA_SPRITE=0x39
labels={}

T={
 'hostage':[["AGATHA: Hmph!","These ROCKET","brats tied me up"],["with old FUJI!","Get rid of them,","child!"]],
 'intro':[["AGATHA: You did","it, child."],["Thank you for","saving FUJI and","this old woman."],["..."],["...Wait."],
          ["I can sense it.","Something dark","clings to you."],["You have fallen","to a terrible","fate, haven't","you?"],
          ["Long ago, a tribe","lived in these","lands. My people."],
          ["They knew of the","accursed ones...","evil souls who","bend the souls of","others to their","will."],
          ["There is an old","ritual that may","break the curse."],["I will help you,","child."],
          ["Bring me three","relics of the","ancient world:"],
          ["A shell coiled","like a whirlpool,"],["a dome-shaped","shell from the","deep sea,"],
          ["and a drop of","old sap that","holds the breath","of the sky."]],
 'mu':[["Hm? You have","already woken","some of them..."],["That one's work,","I suppose."],
       ["Don't worry. The","ritual can still","be done."],["Perhaps it is","even better","this way."]],
 'remind1':[["AGATHA: Bring me","the three relics,","child."],["The coiled shell,","the dome shell,","and the old sap."]],
 'labfail':[["AGATHA: ...","No..."],["You let those","scientists wake","an old relic?"],["Its soul is gone","from the stone."],
            ["Then there is","nothing more I","can do for you."]],
 'lament':[["AGATHA: So much","of KANTO's old","ways are lost..."],["My ancestors","must be weeping."]],
 'relics':[["AGATHA: Yes...","These are the","relics."],["I will keep them","safe."],
           ["But the ritual","also needs a","vessel."],["Something strong","enough to hold","any soul."],
           ["I heard those","ROCKETs talk","about SILPH CO."],["A ball that","catches without","fail..."],
           ["Go and see if","SILPH has such","a thing."]],
 'remind2':[["AGATHA: Find the","vessel at SILPH","CO., child."]],
 'balloffer':[["AGATHA: That is","it! The vessel!"],["Let me keep it","safe for you."],["Will you give it","to AGATHA?"]],
 'ballno':[["AGATHA: Bring it","to me when you","are ready."]],
 'ballgiven':[["<PLAYER> handed","over the ball."],["AGATHA: Good."]],
 'ballfail':[["AGATHA: ...You","used the vessel?"],["Then it is gone,","and with it our","chance."],
             ["There is nothing","more I can do for","you."]],
 'weak':[["AGATHA: Your","GHOST is still","too weak."],["In the ritual it","could hide away","where we can't","find it."],
         ["I know it is a","risk, but make it","as strong as it","can be first."],
         ["Feed it only","dangerous #MON","or truly bad","people."]],
 'consort1':[["AGATHA: Its power","is at its peak."],["Now, take back","this shell."]],
 'consort2':[["See the mark on","it? My people","drew it for"],["devotion to the","one you love."],
             ["Find a girl you","truly care for."],["Give her the","shell and ask","for her help."],
             ["Then bring her","here, to","LAVENDER TOWN."]],
 'bagfull':[["AGATHA: Your bag","is full, child.","Make some room."]],
 'alldead':[["AGATHA: ...The","ones you could","have asked..."],["You killed them","all, didn't you?"],
            ["Then the ritual","can never be","finished."],["There is nothing","more I can do for","you."]],
 'remind4':[["AGATHA: Give the","shell to the one","you love, child."]],
 'stage5':[["AGATHA: You have","brought her."],["Good. Rest now."],["We will begin","soon..."]],
 'kept':[["You kept the","HELIX FOSSIL."]],
 'give_MISTY':[["Give MISTY the","HELIX FOSSIL?"]],
 'give_ERIKA':[["Give ERIKA the","HELIX FOSSIL?"]],
 'give_SABRINA':[["Give SABRINA the","HELIX FOSSIL?"]],
 'join_MISTY':[["MISTY: For me?","This mark..."],["...You're asking","me to help you?"],["You're in some","kind of trouble,","aren't you?"],
               ["Fine! I'll go to","LAVENDER TOWN!"],["Don't make me","regret it!"]],
 'join_ERIKA':[["ERIKA: Oh my...","A gift for me?"],["Such an old and","lovely symbol..."],["I understand.","I will help you."],
               ["I shall wait for","you in LAVENDER","TOWN."]],
 'join_SABRINA':[["SABRINA: I knew","you would come."],["I saw this shell","in a vision."],["Your fate is","tied to mine now."],
                 ["I will go to","LAVENDER TOWN."]],
 'tower_MISTY':[["MISTY: This place","gives me chills!"],["Let's get this","over with!"]],
 'tower_ERIKA':[["ERIKA: I am here,","as I promised."]],
 'tower_SABRINA':[["SABRINA: The","spirits here are","restless..."]],
}
def bitop(op,addr_bit):return 'fa %s cb %02x'%(le(addr_bit[0]),op+8*addr_bit[1])   # ld a,[addr]; bit/set n,a

g=Code(0x2e,0x6800)
def pt(k):g.ref('21','t_'+k);g.emit('cd '+le(PRINTTEXT))
# helpers ---------------------------------------------------------------------------------------------------
g.label('has_item');g.emit('21 1e d3')                        # b = item -> nz if in the bag
g.label('hi_l');g.emit('2a fe ff');g.jr('28','no');g.emit('b8');g.jr('28','yes');g.emit('23');g.jr('18','hi_l')
g.label('has_pc_item');g.emit('21 3b d5');g.jr('18','hi_l')    # b = item -> nz if in the PC
g.label('has_species');g.emit('21 64 d1 cd');g.ref('','scan_sp');g.emit('c0 21 81 da')   # party, then current box
g.label('scan_sp');g.emit('2a fe ff');g.jr('28','no');g.emit('b8');g.jr('28','yes');g.jr('18','scan_sp')
g.label('no');g.emit('af c9')
g.label('yes');g.emit('3e 01 a7 c9')
g.label('remove_if');g.emit('47 c5');g.ref('cd','has_item');g.emit('c1 c8 78')     # a = item, removed if in the bag
g.label('remove_item');g.emit('e0 db '+far(REMOVEITEM[1],REMOVEITEM[0])+' c9')
g.label('yesno');g.emit('cd %s fa 26 cc a7 c9'%le(YESNO))     # z = YES
g.label('fail');g.emit('21 %s cb c6 c9'%le(QFLAGS))
# AGATHA's talk -----------------------------------------------------------------------------------------------
g.label('agatha');g.emit('fa %s cb 47'%le(QFLAGS));g.jr('28','nf');pt('lament');g.emit('c9')
g.label('nf');g.emit(bitop(0x47,EV_RESCUED_FUJI));g.jr('20','rescued');pt('hostage');g.emit('c9')
g.label('rescued');g.emit('fa %s a7'%le(STAGE));g.jr('20','dispatch');pt('intro');g.emit('3e 01 ea '+le(STAGE))
g.label('dispatch');g.emit('fa %s fe 01'%le(STAGE));g.ref('ca','stage1');g.emit('fe 02');g.ref('ca','stage2')
g.emit('fe 03');g.ref('ca','stage3');g.emit('fe 04');g.ref('ca','stage4');pt('stage5');g.emit('c9')
# 1. the relics (DOME FOSSIL or PRETA, OLD AMBER or AZHI, HELIX FOSSIL)
g.label('stage1');g.emit('fa %s e6 %02x'%(le(DEX_OWNED_FOSSILS[0]),DEX_OWNED_FOSSILS[1]));g.jr('28','nolab')
pt('labfail');g.ref('c3','fail')
g.label('nolab');g.emit('06 %02x'%PRETA);g.ref('cd','has_species');g.jr('20','mu')
g.emit('06 %02x'%AZHI);g.ref('cd','has_species');g.jr('28','nomu')
g.label('mu');g.emit('21 %s cb 56'%le(QFLAGS));g.jr('20','nomu');g.emit('cb d6');pt('mu')
g.label('nomu');g.emit('06 %02x'%DOME);g.ref('cd','has_item');g.jr('20','d_ok');g.emit('06 %02x'%PRETA);g.ref('cd','has_species');g.jr('28','missing')
g.label('d_ok');g.emit('06 %02x'%AMBER);g.ref('cd','has_item');g.jr('20','a_ok');g.emit('06 %02x'%AZHI);g.ref('cd','has_species');g.jr('28','missing')
g.label('a_ok');g.emit('06 %02x'%HELIX);g.ref('cd','has_item');g.jr('28','missing')
g.emit('3e %02x'%DOME);g.ref('cd','remove_if');g.emit('3e %02x'%AMBER);g.ref('cd','remove_if');g.emit('3e %02x'%HELIX);g.ref('cd','remove_item')
pt('relics');g.emit('3e 02 ea %s c9'%le(STAGE))
g.label('missing');pt('remind1');g.emit('c9')
# 2. the vessel
g.label('stage2');g.emit('06 %02x'%MASTERBALL);g.ref('cd','has_item');g.jr('20','have_ball')
g.emit(bitop(0x47,EV_GOT_MASTERBALL));g.jr('28','noball');g.emit('06 %02x'%MASTERBALL);g.ref('cd','has_pc_item');g.jr('20','noball')
pt('ballfail');g.ref('c3','fail')
g.label('noball');pt('remind2');g.emit('c9')
g.label('have_ball');pt('balloffer');g.ref('cd','yesno');g.jr('28','ball_yes');pt('ballno');g.emit('c9')
g.label('ball_yes');g.emit('3e %02x'%MASTERBALL);g.ref('cd','remove_item');pt('ballgiven');g.emit('3e 03 ea '+le(STAGE))
# 3. GHOST at Lv100
g.label('stage3');g.emit('21 64 d1 0e 00')
g.label('gl');g.emit('2a fe ff');g.jr('28','weak');g.emit('fe %02x'%GHOST);g.jr('28','gf');g.emit('0c');g.jr('18','gl')
g.label('gf');g.emit('21 8c d1 79 01 2c 00 cd %s 7e fe 64'%le(ADDNTIMES));g.jr('30','strong')   # D16B+33 = level
g.label('weak');pt('weak');g.emit('c9')
g.label('strong');g.emit('fa a7 d4 e6 54 fe 54');g.jr('20','alive');pt('alldead');g.ref('c3','fail')
g.label('alive');pt('consort1');g.emit('01 01 %02x cd %s'%(HELIX,le(GIVEITEM)));g.jr('38','gotshell');pt('bagfull');g.emit('c9')
g.label('gotshell');pt('consort2');g.emit('3e 04 ea %s c9'%le(STAGE))
g.label('stage4');pt('remind4');g.emit('c9')
# the girls: talking to MISTY / ERIKA / SABRINA in her gym after beating her, with the shell
for n,name,mp,bank,beat,kb,spr in GIRLS:
    g.label('girl_'+name);g.emit('af ea %s fa %s fe 04 c0'%(le(TEMP),le(STAGE)))
    g.emit('06 %02x'%HELIX);g.ref('cd','has_item');g.emit('c8')
    g.emit(bitop(0x47,beat)+' c8 3e 01 ea '+le(TEMP))
    pt('give_'+name);g.ref('cd','yesno');g.jr('28','join_'+name);pt('kept');g.emit('c9')
    g.label('join_'+name);g.emit('3e %02x'%HELIX);g.ref('cd','remove_item');pt('join_'+name)
    g.emit('3e %02x ea %s 3e 05 ea %s c9'%(n,le(CONSORT),le(STAGE)))
for k,v in T.items():
    if k.startswith('tower_'):continue
    g.label('t_'+k);g.raw(txt(v,end=0x57 if k in ('kept',) else 0x58))
for k,v in T.items():
    if k.startswith('tower_'):g.label('t_'+k);g.raw(txt(v,end=0x57))
# map load: a failed quest -> AGATHA leaves once the player has left the Tower top floor
ML_OLD=r[fo(0x2e,0x4000):fo(0x2e,0x4003)];assert ML_OLD[0]==0xc3;ML_NEXT=ML_OLD[1]|ML_OLD[2]<<8
g.label('mapload');g.emit('fa %s cb 47'%le(QFLAGS));g.jr('28','ml_next');g.emit('fa 5e d3 fe 94');g.jr('28','ml_next')
g.emit('21 %s cb ce'%le(QFLAGS))
g.label('ml_next');g.emit('c3 '+le(ML_NEXT))
code=g.finish();assert 0x6800+len(code)<=0x8000,len(code)
rom.put(fo(0x2e,0x6800),code,'Bank 2E: AGATHA quest logic + texts')
labels['bank2e']={k:hex(v) for k,v in g.labels.items()}
rom.code(fo(0x2e,0x4000),bytes.fromhex('c3'+le(g.labels['mapload'])),'Map load: failed AGATHA quest -> she leaves',ML_OLD)

# Pokemon Tower 7F (map 94, bank 18): AGATHA (obj 5) next to FUJI, MISTY/ERIKA/SABRINA (obj 6-8) beside her
M7=0x94;B7=0x18
bank,h=r[0xc23d+M7],fo(B7,r[0x1ae+2*M7]|r[0x1af+2*M7]<<8);assert bank==B7
TP=r[h+5]|r[h+6]<<8;SP=r[h+7]|r[h+8]<<8;OP=r[h+10]|r[h+11]<<8;assert r[h+9]==0 and (TP,SP,OP)==(0x4e3f,0x4d05,0x4ef6)
o=fo(B7,OP);obj=bytearray(r[o:fo(B7,0x4f1c)+4]);assert obj[1]==1 and obj[6]==0 and obj[7]==4   # border, 1 warp, 0 signs, 4 objects
OBJ_END=0x4f1c-OP                                           # 4 objects end here; the warp-to entry follows
AG_Y,AG_X=3,9;GIRL_Y,GIRL_X=3,11
new_objs=bytes([AGATHA_SPRITE,AG_Y+4,AG_X+4,0xff,0xd0,5])+b''.join(bytes([spr,GIRL_Y+4,GIRL_X+4,0xff,0xd0,6+i]) for i,(n,name,mp,bank_,beat,kb,spr) in enumerate(GIRLS))
c=Code(B7,0x6700)
c.label('objects');c.raw(obj[:7]+bytes([8])+obj[8:OBJ_END]+new_objs+obj[OBJ_END:])
c.label('texts');c.raw(r[fo(B7,TP):fo(B7,TP)+8]);c.ref('','agatha')
for n,name,*_ in GIRLS:c.ref('','girl_'+name)
c.label('script')                                           # hide AGATHA off the GHOST route / once gone; girls unless chosen
c.emit('fa %s a7'%le(GHOST_ROUTE));c.jr('28','hide_a');c.emit('fa %s cb 4f'%le(QFLAGS));c.jr('28','girls')
c.label('hide_a');c.emit('af ea 50 c1 3e ff ea 54 c2 ea 55 c2')
c.label('girls')
for i,(n,name,*_) in enumerate(GIRLS):
    s=6+i;c.emit('fa %s fe %02x'%(le(CONSORT),n));c.jr('28','shown_'+name)
    c.emit('af ea %02x c1 3e ff ea %02x c2 ea %02x c2'%(s*16,s*16+4,s*16+5));c.label('shown_'+name)
c.emit('c3 '+le(SP))
c.label('agatha');c.emit('08 '+far(g.labels['agatha'],0x2e)+' c3 '+le(TEXTEND))
for n,name,*_ in GIRLS:
    c.label('girl_'+name);c.emit('08');c.ref('21','far_'+name);c.emit('cd %s c3 %s'%(le(PRINTTEXT),le(TEXTEND)))
    c.label('far_'+name);c.emit('17 %s 2e 50'%le(g.labels['t_tower_'+name]))
code=c.finish();rom.put(fo(B7,0x6700),code,'Bank 18: Pokemon Tower 7F objects (+AGATHA, girls), texts, script')
rom.data(h+5,bytes.fromhex(le(c.labels['texts'])+le(c.labels['script'])),'Tower 7F text + script pointers',le(TP)+le(SP))
rom.data(h+10,bytes.fromhex(le(c.labels['objects'])),'Tower 7F object data -> v16',le(OP))
labels['bank18']={k:hex(v) for k,v in c.labels.items()}

# the girls' gyms: leader text 1 -> offer the shell; the chosen one leaves her gym
for n,name,mp,bank,beat,kb,spr in GIRLS:
    gh=fo(bank,r[0x1ae+2*mp]|r[0x1af+2*mp]<<8)
    tp=r[gh+5]|r[gh+6]<<8;sp=r[gh+7]|r[gh+8]<<8;e1=fo(bank,tp);orig=r[e1]|r[e1+1]<<8;assert r[fo(bank,orig)]==0x08
    at=0x7000+0x80*n
    c=Code(bank,at)
    c.label('text');c.emit('08 3e %02x ea %s '%(n,le(ARG))+far(g.labels['girl_'+name],0x2e)+' fa %s a7 ca %s c3 %s'%(le(TEMP),le(orig+1),le(TEXTEND)))
    c.label('script');c.emit('fa %s fe %02x'%(le(CONSORT),n));c.jr('20','go')
    c.emit('af ea 10 c1 3e ff ea 14 c2 ea 15 c2')
    c.label('go');c.emit('c3 '+le(sp))
    code=c.finish();rom.put(fo(bank,at),code,'%s gym: shell offer + leaves once chosen'%name)
    rom.data(e1,bytes.fromhex(le(c.labels['text'])),'%s gym text 1 -> v16 wrapper'%name,le(orig))
    rom.data(gh+7,bytes.fromhex(le(c.labels['script'])),'%s gym script -> v16 wrapper'%name,le(sp))
    labels['%s'%name]={k:hex(v) for k,v in c.labels.items()}

rom.finish('Creepy_Black_Mu_v16.gb','manifest_v16.json','CREEPY MU V16',extra=dict(labels=labels))

# Creepy Black Mu v18: Silph Co. on the GHOST route.
#  - Reaching Pokemon Tower 7F (where FUJI is held) clears GIOVANNI out of the Rocket Hideout and opens the Saffron
#    gates (the guards' drink flag), so SILPH CO. can be entered right away.
#  - GIOVANNI at SILPH CO. 11F: new before-battle speech (watching you, wanted to recruit you, will take the weapon),
#    in-battle defeat line cursing "that cult" (also when CURSE was used), no after-win trainer phase (no CURSE on him),
#    new after-battle warning (forces you don't understand are using you); he still leaves as usual.
#  - The PRESIDENT: ROCKET was after the MASTER BALL, his vanished old friend's finest work; then gives it as usual.
# Logged patches on top of verified Mu v17 (patchlib).
from patchlib import *
from patchguard import fo

V17_SHA='eb1805db25d8291f93c64947eda0868a76ecffaf7e235efb616335a164a3152b'
rom=Rom('Creepy_Black_Mu_v17.gb',V17_SHA)
r=rom.r
PRINTTEXT,TEXTEND=0x3c94,0x2504
GHOST_ROUTE=0xd451
GIOVANNI=0x1d;SILPH11=0xeb;TOWER7=0x94
EV_HIDEOUT_GIOVANNI=(0xd81b,7)       # checked by his B4F text (11:553B)
HIDE_FLAGS=0xd5a6                    # toggle n -> D5A6 + n/8, bit n%8 (set = hidden)
T_HIDEOUT_GIOVANNI,T_SILPH_SCOPE=0x83,0x87      # his post-battle script hides 83 and shows 87 (11:54D5)
DRINK=(0xd728,6)                     # Saffron gate guards (7:5FBB): let you through
labels={}

T={
 'gio_pre':[["GIOVANNI: So,","<PLAYER>..."],["I have been","watching you for","some time."],
            ["I thought of","making you one","of us."],["You had talent.","And you had that","weapon."],
            ["But the damage","you have done..."],["No. You can't be","controlled."],
            ["I will simply","take the weapon","for myself!"]],
 'gio_lose':[["GIOVANNI: Damn","that cult...!"]],
 'gio_after':[["GIOVANNI: Hmph."],["You think you're","in control?"],
              ["Fool. There are","forces at work","you can't even","understand."],
              ["They're using","you, <PLAYER>."],["I must go... but","we will meet","again!"]],
 'president':[["PRESIDENT: You","saved us all!"],["Those ROCKETs","were after our","MASTER BALL."],
              ["It was the finest","work of an old","friend of mine."],["He was a genius.","Then one day, he","just vanished..."],
              ["I can't think of","anyone better to","have it. Take it."]],
}
g=Code(0x2e,0x7a00)
for k,v in T.items():g.label('t_'+k);g.raw(txt(v,end=0x58))
# map load: first visit to Tower 7F on the GHOST route -> GIOVANNI leaves the hideout, Saffron opens
ML=r[fo(0x2e,0x4000):fo(0x2e,0x4003)];assert ML[0]==0xc3;ML_NEXT=ML[1]|ML[2]<<8
hb=HIDE_FLAGS+T_HIDEOUT_GIOVANNI//8;assert hb==HIDE_FLAGS+T_SILPH_SCOPE//8
g.label('mapload');g.emit('fa 5e d3 fe %02x'%TOWER7);g.jr('20','next');g.emit('fa %s a7'%le(GHOST_ROUTE));g.jr('28','next')
g.emit('21 %s cb %02x'%(le(DRINK[0]),0xc6+8*DRINK[1]))                                     # gates open
g.emit('21 %s cb %02x'%(le(EV_HIDEOUT_GIOVANNI[0]),0x46+8*EV_HIDEOUT_GIOVANNI[1]));g.jr('20','next')   # hideout not done yet:
g.emit('cb %02x'%(0xc6+8*EV_HIDEOUT_GIOVANNI[1]))                                          #  mark it done,
g.emit('21 %s cb %02x cb %02x'%(le(hb),0xc6+8*(T_HIDEOUT_GIOVANNI%8),0x86+8*(T_SILPH_SCOPE%8)))  #  GIOVANNI gone, SILPH SCOPE ball shown
g.label('next');g.emit('c3 '+le(ML_NEXT))
# in-battle defeat text: keep the cult line for GIOVANNI at SILPH 11F even after CURSE (else the frightened text)
FEAR=0x4032
g.label('fear');g.emit('fe %02x c2 %s fa 5e d3 fe %02x c2 %s c9'%(GIOVANNI,le(FEAR),SILPH11,le(FEAR)))
code=g.finish();assert 0x7a00+len(code)<=0x8000
rom.put(fo(0x2e,0x7a00),code,'Bank 2E: SILPH CO. texts + Tower 7F unlock + GIOVANNI defeat-text exception')
rom.code(fo(0x2e,0x4000),bytes.fromhex('c3'+le(g.labels['mapload'])),'Map load: Tower 7F unlocks SILPH CO. (GHOST route)',ML)
rom.code(fo(0x2e,0x4b41),bytes.fromhex('c2'+le(g.labels['fear'])),'Defeat text after CURSE: GIOVANNI at SILPH keeps his line','c2'+le(FEAR))

# bank 18: SILPH CO. 11F wrappers
c=Code(0x18,0x7400)
def chooser(label,orig,key):
    c.label(label);c.emit('08 fa %s a7 21 %s'%(le(GHOST_ROUTE),le(orig)));c.jr('28',label+'_p');c.ref('21',label+'_far')
    c.label(label+'_p');c.emit('cd %s c3 %s'%(le(PRINTTEXT),le(TEXTEND)))
    c.label(label+'_far');c.emit('17 %s 2e 50'%le(g.labels['t_'+key]))
TP=fo(0x18,0x62b7)
assert r[TP+4:TP+6]==bytes.fromhex(le(0x632b)) and r[TP+10:TP+12]==bytes.fromhex(le(0x6335))
chooser('pre',0x632b,'gio_pre');chooser('after',0x6335,'gio_after')
c.label('lose_far');c.emit('17 %s 2e 50'%le(g.labels['t_gio_lose']))
c.label('lose');c.emit('f5 21 30 63 fa %s a7'%le(GHOST_ROUTE));c.jr('28','lose_d');c.ref('21','lose_far')   # hl = defeat text
c.label('lose_d');c.emit('f1 c9')
c.label('pres_far');c.emit('17 %s 2e 50'%le(g.labels['t_president']))
c.label('pres');c.emit('f5 21 11 63 fa %s a7'%le(GHOST_ROUTE));c.jr('28','pres_d');c.ref('21','pres_far')
c.label('pres_d');c.emit('f1 c9')
code=c.finish();rom.put(fo(0x18,0x7400),code,'Bank 18: SILPH CO. 11F GIOVANNI / PRESIDENT texts (GHOST route)')
rom.data(TP+4,bytes.fromhex(le(c.labels['pre'])),'SILPH 11F text 3 (GIOVANNI before) -> chooser',le(0x632b))
rom.data(TP+10,bytes.fromhex(le(c.labels['after'])),'SILPH 11F text 6 (GIOVANNI after) -> chooser',le(0x6335))
# end-battle texts: ld hl,6330 / ld de,6330 / call SaveEndBattleTextPointers -> hl from the chooser, de = hl
rom.hook(fo(0x18,0x629a),'cd'+le(c.labels['lose'])+'54 5d 00','SILPH 11F GIOVANNI defeat text -> cult line','21 30 63 11 30 63',
         provides=('h','l','d','e'))
rom.hook(fo(0x18,0x62e5),'cd'+le(c.labels['pres']),'PRESIDENT: the MASTER BALL story before he gives it','21 11 63',provides=('h','l'))
labels['bank18']={k:hex(v) for k,v in c.labels.items()};labels['bank2e']={k:hex(v) for k,v in g.labels.items()}

# no after-win trainer phase (CURSE on the trainer) for GIOVANNI at SILPH 11F: it starts when GHOST is out (F:46EC)
f=Code(0xf,0x7dcc)
f.emit('fa 31 d0 fe %02x'%GIOVANNI);f.jr('20','species');f.emit('fa 5e d3 fe %02x'%SILPH11);f.jr('20','species');f.emit('af c9')
f.label('species');f.emit('fa 14 d0 c9')
code=f.finish();assert len(code)<=20;rom.put(fo(0xf,0x7dcc),code,'Bank F: trainer phase check (not for GIOVANNI at SILPH)')
rom.hook(fo(0xf,0x46ec),'cd'+le(0x7dcc),'After a win: no trainer phase against GIOVANNI at SILPH 11F','fa 14 d0',provides=('a','f'))

rom.finish('Creepy_Black_Mu_v18.gb','manifest_v18.json','CREEPY MU V18',extra=dict(labels=labels))

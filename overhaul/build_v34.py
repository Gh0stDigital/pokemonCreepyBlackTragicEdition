# Creepy Black Mu v34: CURSE also kills the scripted grunts, and never marks the wrong trainer.
#   Scripted trainers (battles started by a map script, not by TalkToTrainer) never got a kill index, and D4AE/AF keeps the
#   index of the LAST trainer talked to. So from CERULEAN on (the Rocket thief, the NUGGET BRIDGE Rocket after its five
#   trainers) CURSE either said "But, it failed!" or "killed" an already dead trainer again while the grunt stood there.
#   Now, at the trainer phase (F:46EC -> v18 check, rewritten as a far call), the battle is looked up by (map, opponent,
#   trainer no.) in a table of scripted trainers:
#     - CERULEAN Rocket thief, NUGGET BRIDGE Rocket, MT. MOON Super Nerd, GAME CORNER Rocket: their own kill index
#       ($1FC-$1FF, the last 4 bits of D430-D44F) -> they die and become gravestones;
#     - CINNABAR GYM quiz trainers and GIOVANNI in the hideout: index 0 -> "But, it failed!" (not a stale kill).
#   Every other battle keeps the index TalkToTrainer / the v14 leader engage set, as before. The v18 rule (no trainer
#   phase for GIOVANNI at SILPH 11F) is kept. The map-load gravestone table (kill_chk2) is rebuilt with the 4 grunts.
#   A killed trainer now turns into a gravestone right after the battle (before: only after leaving and re-entering
#   the map, as the base game only checked graves at map load): after every real battle (home stub 0:00C0, carry set)
#   the gravestone pass 3:4E85 runs again and the sprite graphics are reloaded (5:785B).
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm
import killmap as K

V33_SHA='eaeb500c5826969fea6c542a0d76e35ee07ad36e7883e7ace970e2a82e64ece1'
rom=Rom('Creepy_Black_Mu_v33.gb',V33_SHA)
r=rom.r;R=bytes(r)
w=lambda o:R[o]|R[o+1]<<8
BANK=0x2d;CODE=0x6100;TAB=0x7180;TMP=0xd470
POST2=int(json.load(open('manifest_v31.json'))['labels']['bank2d']['post2'],16)
#            map  opponent(class+200) set  sprite  kill index
SCRIPTED=[(0x03,230,5,2,0x1fc),   # CERULEAN: Rocket thief
          (0x23,230,6,1,0x1fd),   # ROUTE 24: NUGGET BRIDGE Rocket
          (0x3d,208,2,1,0x1fe),   # MT. MOON B2F: Super Nerd (fossils)
          (0x87,230,7,11,0x1ff)]  # CELADON GAME CORNER: Rocket
NOKILL=[(0xa6,208,s) for s in (9,10,11,12)]+[(0xa6,211,s) for s in (4,5,6)]+[(0xca,229,1)]   # CINNABAR quiz, hideout GIOVANNI
assert all(0x100<=i<0x200 for *_,i in SCRIPTED)
used=set(w(h+10) for h in K.headers(R));assert not used&{i for *_,i in SCRIPTED},'kill index already taken'

# ---- the trainer phase: v18 check + scripted kill index (2D)
stab=bytearray()
for mp,opp,st,spr,i in SCRIPTED:stab+=bytes([mp,opp,st,i&255,i>>8])
for mp,opp,st in NOKILL:stab+=bytes([mp,opp,st,0,0])
stab.append(0xff)
code,L=asm(f'''
phase2:                          ; F:46EC trainer phase: a = species out (0 = no phase) via {TMP:#x}
    ld a,[$d031]
    cp $1d
    jr nz,.n
    ld a,[$d35e]
    cp $eb
    jr nz,.n
    xor a
    jr .o
.n: ld a,[$d014]
.o: ld [{TMP}],a
    ld hl,stab
.l: ld a,[hl+]
    cp $ff
    ret z
    ld b,a
    ld a,[hl+]
    ld c,a
    ld a,[hl+]
    ld d,a
    ld a,[hl+]
    ld e,a
    ld a,[hl+]
    push af
    ld a,[$d35e]
    cp b
    jr nz,.no
    ld a,[$d059]
    cp c
    jr nz,.no
    ld a,[$d05d]
    cp d
    jr nz,.no
    pop af
    ld [$d4ae],a
    ld a,e
    ld [$d4af],a
    ret
.no:pop af
    jr .l
post3:                           ; after NewBattle (0:00C0): carry = a battle happened
    push af
    call {POST2}
    pop af
    ret nc
    farcall $4e85,3                 ; killed trainers -> gravestone picture
    farcall $785b,5                 ; reload the map sprites' tiles
    ret
stab:
    db {",".join(str(x) for x in stab)}
''',CODE)
assert CODE+len(code)<0x6400,hex(CODE+len(code))
POST=0
rom.put(fo(BANK,CODE),code,'Bank 2D: v34 trainer phase (v18 rule + scripted trainers\' kill index)')
F=fo(0xf,0x7dcc);old=R[F:F+20]
assert old[:3]==bytes.fromhex('fa31d0')
stubF,_=asm(f'''
    ld hl,{L['phase2']}
    ld b,{BANK}
    call $3618
    ld a,[{TMP}]
    ret
''',0x7dcc)
rom.code(F,stubF+bytes(20-len(stubF)),'Bank F: trainer phase check -> phase2 (2D)',old.hex(),
         reviewed='F:7DD1/7DD8 are the old routine\'s own jr\'s (replaced whole); F:7D9C is the 18 operand of call $3618 and 0:03AA the cd operand of ld [$cd6b],a, both misread as jumps')

# ---- map-load gravestone table: rebuilt with the scripted grunts
hs=K.headers(R);hm=K.header_maps(R,hs);lists={}
for h in hs:
    i=w(h+10)
    if not i or h not in hm:continue
    for mp in hm[h]:lists.setdefault(mp,[]).append((R[h],i))
for mp,opp,st,spr,i in SCRIPTED:lists.setdefault(mp,[]).append((spr,i))
ptrs=bytearray();body=bytearray();LISTS=TAB+2*0xf8
for mp in range(0xf8):
    if mp in lists:
        ptrs+=(LISTS+len(body)).to_bytes(2,'little')
        for spr,i in lists[mp]:body+=bytes([spr,i&255,i>>8])
        body.append(0)
    else:ptrs+=b'\0\0'
assert TAB+len(ptrs)+len(body)<0x8000
rom.put(fo(BANK,TAB),bytes(ptrs)+bytes(body),'Bank 2D: v34 map -> (sprite, kill index) gravestone table (+ scripted grunts)')
KC=int(json.load(open('manifest_v29.json'))['labels']['bank2d']['kill_chk2'],16)
assert R[fo(BANK,KC)+0x10:fo(BANK,KC)+0x13]==bytes.fromhex('110065')
rom.data(fo(BANK,KC)+0x11,TAB.to_bytes(2,'little'),'kill_chk2: gravestone table -> v34 table','0065')
assert R[0xc4:0xc9]==bytes([0x21])+POST2.to_bytes(2,'little')+bytes([0x06,BANK])
rom.data(0xc5,L['post3'].to_bytes(2,'little'),'After-battle stub -> post3 (gravestones right after a kill)',POST2.to_bytes(2,'little'))
rom.finish('Creepy_Black_Mu_v34.gb','manifest_v34.json','CREEPY MU V34',extra=dict(labels=dict(bank2d={k:hex(v) for k,v in L.items()}),
    scripted=[dict(map=hex(a),opponent=b,set=c,sprite=d,index=hex(e)) for a,b,c,d,e in SCRIPTED],nokill=[dict(map=hex(a),opponent=b,set=c) for a,b,c in NOKILL]))

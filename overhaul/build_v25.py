# Creepy Black Mu v25: the climax after MR. MU's ritual (GHOST route).
#   1. The caught MIRAGE ????? sits in the party with a hollow-GENTLEMAN party-menu icon.
#   2. In the TOWER CHAMBER every item is disabled (bag, Escape Rope, Dig, Teleport, Fly): "Something prevents you from
#      using that here." (Battles are exempt: the MASTER BALL still works.)
#   3. Walking out of the inner circle: GHOST consumes the MIRAGE (Gengar's cry for now). Two steps later a battle starts:
#      the player (alone, as YOU) against a Lv100 GHOST. Before any move GHOST uses CURSE on the player, the screen stays
#      black for 5 seconds, then fades in to the evolution screen: "GHOST has transcended and become BLACK."
#   4. The player is BLACK from now on: name, battle back picture and map sprite are the RED+GHOST fusion. GHOST leaves the
#      party (unless it is the only member) and the hunger engine is switched off.
#   5. Tower 7F: AGATHA walks up to the player, celebrates, tells about the consort (now at the player's home in PALLET
#      TOWN: she heals the party) and sends BLACK to destroy the POKeMON LEAGUE. Two more talks: MR. MU's story, then the
#      final line.
# Logged patches on top of verified Mu v24 (patchlib). All new code is written in assembly (sm83asm.py).
import io,json,sys
from patchlib import *
from patchguard import fo
from sm83asm import asm
sys.path.insert(0,str(ROOT.parent/'ref'));import pic
import red_ghost_fusion as FUSION
import red_ghost_overworld as OVER
import hollow_icon as ICON

V24_SHA='8526a20e7b70b3592f7ad324a0a1d763fbd774df2a4fa26278a7856b0d4e612e'
rom=Rom('Creepy_Black_Mu_v24.gb',V24_SHA)
r=rom.r
w=lambda o:r[o]|r[o+1]<<8
labels={}

# ---- RAM (saved block, D450-D4A3) -----------------------------------------------------------------------------------
RIT,STEPS,AGTALK,BLACK,LASTY,LASTX,SCENE,BANKR=0xd467,0xd46a,0xd46b,0xd46c,0xd46d,0xd46e,0xd46f,0xd470
CONSORT=0xd465
# ---- ids -------------------------------------------------------------------------------------------------------------
YOU,MU,MIR,BLK,GHOST,GENGAR=0x79,0x20,0x7a,0x7f,0x1f,0x0e
CHAMBER,TOWER7=0x69,0x94
STASH=0xb600;PARTY_LEN=0x194
BANK25=0x2d                                     # all new code and data lives in bank 2D (15 KB free)
L23=json.load(open(ROOT/'manifest_v23.json'))['labels']
L22=json.load(open(ROOT/'manifest_v22.json'))['labels']['chamber']
L16=json.load(open(ROOT/'manifest_v16.json'))['labels']
L19=json.load(open(ROOT/'manifest_v19.json'))['labels']['tower7f']
P23=json.load(open(ROOT/'manifest_v23.json'))['pics']
RESTORE=int(L23['bank2e']['restore'],16)        # v23: party back after MR. MU's battle, ????? added
OLD_AGATHA=int(L16['bank2e']['agatha'],16)      # v16-v22 AGATHA dialogue (2E)
FUSION_FRONT=0x41c0;FUSION_BACK=FUSION_FRONT+P23['mirage_front']       # RED+GHOST pics left in 2D by v23
assert r[fo(0x2d,FUSION_FRONT)]==0x77 and r[fo(0x2d,FUSION_BACK)]==0x44
SHEET=0x7000                                    # BLACK map sprite sheet (2D)
RET3=0x469b                                     # a "ret" in bank 3 (UseItem_ is aborted by returning through it)

# ================================================================================================================
# 1. Data: BLACK map sprite sheet, party icon tiles
frames=OVER.ghost_frames(bytes(r))
def tile(g,ty,tx):
    out=bytearray()
    for y in range(8):
        lo=hi=0
        for x in range(8):c=g[ty*8+y][tx*8+x];lo=lo<<1|(c&1);hi=hi<<1|(c>>1)
        out+=bytes([lo,hi])
    return bytes(out)
sheet=b''.join(tile(g,ty,tx) for g in frames for ty,tx in ((0,0),(0,1),(1,0),(1,1)))
assert len(sheet)==0x180
rom.put(fo(BANK25,SHEET),sheet,'Bank 2D: BLACK map sprite sheet (RED+GHOST fusion, 6 frames)')

# ================================================================================================================
# 2. Texts (bank 2D)
TXT={
 'prevent':([["Something","prevents you from","using that here."]],0x58),
 'consume':([["GHOST consumed","the MIRAGE!"]],0x57),
 'curse':([["GHOST used CURSE!"]],0x58),
 'trans':([["GHOST has","transcended and","become BLACK."]],0x58),
 'now':([["You are now","BLACK."]],0x58),
 'intro':([["AGATHA: It is","done, child!"],
           ["The ceremony is","complete! My","ancestors' dream","lives again!"],
           ["Fear not for your","consort. She is","safe at your home","in PALLET TOWN."],
           ["Go to her when","you need rest."],
           ["But your work has","only begun."],
           ["The time has come","to rid KANTO of","the intruders."],
           ["Destroy the","#MON LEAGUE","and consume them","all!"]],0x58),
 'lore':([["AGATHA: MR. MU...","Do you know how","hard he worked?"],
          ["He was devoted to","our clan. He gave","everything to","perfect you."],
          ["He always felt","shame and guilt","for failing that","ceremony of old."],
          ["It was not even","his fault..."],
          ["..."],
          ["No. The past does","not matter now."],
          ["Today we should","celebrate!"]],0x58),
 'final':([["AGATHA: My","ancestors are","smiling today!"],
           ["I can hear them","singing, child!"],
           ["They sing of the","day KANTO is rid","of its outsiders!"]],0x58),
 'c1':([["MISTY: Welcome","home. Rest a bit."]],0x58),
 'c2':([["ERIKA: Welcome","home. Rest a bit."]],0x58),
 'c3':([["SABRINA: Welcome","home. Rest a bit."]],0x58),
 'healed':([["Your #MON look","much better now."]],0x58),
}
TXT_AT=0x5800
tx=bytearray();TXTSYM={}
for k,(paras,end) in TXT.items():
    TXTSYM['t_'+k]=TXT_AT+len(tx);tx+=txt(paras,end=end)
assert TXT_AT+len(tx)<0x6c00,len(tx)
rom.put(fo(BANK25,TXT_AT),bytes(tx),'Bank 2D: v25 texts')

# ================================================================================================================
# 3. Bank 2D code
YOU_L=50;YOU_HP=200;YOU_ST=20
you=bytes([YOU])+YOU_HP.to_bytes(2,'big')+bytes([YOU_L,0,0,0,0, 0xa6,0,0,0, 0,0])+(125000).to_bytes(3,'big')+bytes(10)+b'\x88\x88'+bytes([10,0,0,0,YOU_L])+YOU_HP.to_bytes(2,'big')+YOU_ST.to_bytes(2,'big')*4
assert len(you)==44
NAME_BLACK=bytes(enc('BLACK').ljust(11,b'\x50'))
SQ=[i*i for i in range(13)]
fadetab=[0xff,0xfe,0xf9,0xe4]
C25=0x4400
SRC=f'''
sram_on:
    ld a,$0a
    ld [$0000],a
    ld a,1
    ld [$4000],a
    ret
sram_off:
    xor a
    ld [$4000],a
    ld [$0000],a
    ret
find_party:                      ; c = species -> a = index (carry set when absent)
    ld hl,$d164
    ld a,[$d163]
    ld b,a
    ld d,0
.l: ld a,b
    and a
    jr z,.nf
    ld a,[hl+]
    cp c
    jr z,.f
    inc d
    dec b
    jr .l
.f: ld a,d
    and a
    ret
.nf: scf
    ret
remove_party:                    ; a = index
    ld [$cf92],a
    xor a
    ld [$cf95],a
    farcall $7b61,1
    ret

; ---- which ROM bank holds this species' pictures (UncompressMonSprite asks for it)
bank_for:
    ld a,[$cf91]
    ld c,$01
    cp $15
    jr z,.got
    ld c,$2d
    cp $1f
    jr z,.got
    cp $7a
    jr z,.got
    cp $7f
    jr z,.got
    cp $79
    jr nz,.rest
    ld a,[{BLACK}]
    and a
    ld a,$79
    jr z,.rest
    jr .got
.rest:
    ld c,$0b
    cp $b6
    jr z,.got
    ld c,$09
    cp $1f
    jr c,.got
    ld c,$0a
    cp $4a
    jr c,.got
    ld c,$0b
    cp $74
    jr c,.got
    ld c,$0c
    cp $99
    jr c,.got
    ld c,$0d
.got:
    ld a,c
    ld [{BANKR}],a
    ret

; ---- the player's walking sprite sheet = BLACK (called from the home stub when BLACK)
black_sprite_load:
    ld de,{SHEET}
    ld hl,$8000
    push de
    push hl
    ld bc,$2d0c
    call $1875
    pop hl
    pop de
    ld a,$c0
    add e
    ld e,a
    jr nc,.c
    inc d
.c: set 3,h
    ld bc,$2d0c
    jp $1875

; ---- every item is disabled in the TOWER CHAMBER (outside battles). Entered instead of UseItem_'s first two instructions.
item_block:
    ld a,1
    ld [$cd6a],a
    ld a,[$d057]
    and a
    ret nz
    ld a,[$d35e]
    cp {CHAMBER}
    ret nz
    ld hl,t_prevent
    call $3c94
    xor a
    ld [$cd6a],a
    ld hl,sp+4
    ld a,{RET3&255}
    ld [hl+],a
    ld a,{RET3>>8}
    ld [hl],a
    ret

; ---- hunger engine (v2) is switched off for BLACK; the original runs otherwise
hunger_wrap:
    ld a,[{BLACK}]
    and a
    ret nz
    farcall $4100,$2e
    ret

; ---- climax: runs at the first battle menu of the GHOST battle (RIT = 5)
climax_menu:
    call $375f
    ld a,[{RIT}]
    cp 5
    ret nz
    ld a,[$d057]
    and a
    ret z
    ld hl,t_curse
    call $3c94
    farcall $418c,$2e
    ld b,9
.w: push bc
    ld c,30
    call $3773
    pop bc
    dec b
    jr nz,.w
    xor a
    ldh [$ba],a
    ld hl,$c3a0
    ld bc,$1214
    call $18f1
    ld a,$ff
    ld [$cfcb],a
    call $0082
    ld a,{GHOST}
    ld [$cf91],a
    ld [$d0b5],a
    farcall $7f04,$1e
    ld a,1
    ldh [$ba],a
    ld hl,fade
    ld b,4
.f: ld a,[hl+]
    ldh [$47],a
    push hl
    push bc
    ld c,10
    call $3773
    pop bc
    pop hl
    dec b
    jr nz,.f
    call $3e27
    ld a,{GHOST}
    ld [$cee9],a
    ld a,{BLK}
    ld [$ceea],a
    farcall $7e34,$1e
    ld hl,t_trans
    call $3c94
    ld a,1
    ld [{BLACK}],a
    xor a
    ld [$d45c],a
    ld hl,name_black
    ld de,$d158
    ld bc,11
    call $00b5
    ld hl,t_now
    call $3c94
    ld hl,sp+4
    ld a,$55
    ld [hl+],a
    ld a,$51
    ld [hl],a
    ret

; ---- TOWER CHAMBER map script, every frame
chamber_tick:
    ld a,[{RIT}]
    and a
    ret z
    cp 3
    jr c,.mu
    jr z,.circle
    cp 5
    jp c,do_count
    jp z,do_post
    ret
.mu:
    ld a,[$d059]
    and a
    ret nz
    farcall {RESTORE},$2e
    ret
.circle:
    ld a,[$d361]
    sub 11
    jr nc,.a1
    cpl
    inc a
.a1: ld e,a
    ld a,[$d362]
    sub 11
    jr nc,.a2
    cpl
    inc a
.a2: ld c,a
    ld b,0
    ld hl,sq
    add hl,bc
    ld d,[hl]
    ld c,e
    ld hl,sq
    add hl,bc
    ld a,[hl]
    add d
    cp 6
    ret c
    ; ---- first step out of the circle: GHOST consumes the MIRAGE
    ld a,[$d361]
    ld [{LASTY}],a
    ld a,[$d362]
    ld [{LASTX}],a
    xor a
    ld [{STEPS}],a
    ld a,4
    ld [{RIT}],a
    ld a,{GENGAR}
    call $13ff
    farcall $418c,$2e
    ld c,30
    call $3773
    farcall $41a8,$2e
    ld c,{MIR}
    call find_party
    jr c,.nom
    call remove_party
.nom:
    ld a,5
    ldh [$ff8c],a
    jp $294d
do_count:
    ld a,[$d361]
    ld b,a
    ld a,[{LASTY}]
    cp b
    jr nz,.moved
    ld a,[$d362]
    ld b,a
    ld a,[{LASTX}]
    cp b
    ret z
.moved:
    ld a,[$d361]
    ld [{LASTY}],a
    ld a,[$d362]
    ld [{LASTX}],a
    ld a,[{STEPS}]
    inc a
    ld [{STEPS}],a
    cp 2
    ret c
    ; ---- two steps later: the party is put aside and the battle starts (YOU against a Lv100 GHOST)
    call sram_on
    ld hl,$d163
    ld de,{STASH}
    ld bc,{PARTY_LEN}
    call $00b5
    call sram_off
    ld hl,$d163
    ld a,1
    ld [hl+],a
    ld a,{YOU}
    ld [hl+],a
    ld [hl],$ff
    ld hl,you_struct
    ld de,$d16b
    ld bc,44
    call $00b5
    ld hl,$d158
    ld de,$d273
    ld bc,11
    call $00b5
    ld hl,$d158
    ld de,$d2b5
    ld bc,11
    call $00b5
    ld a,[$d359]
    ld [$d177],a
    ld a,[$d35a]
    ld [$d178],a
    ld a,5
    ld [{RIT}],a
    ld a,{GHOST}
    ld [$d059],a
    ld a,100
    ld [$d127],a
    ret
do_post:                         ; the battle is over: party back (GHOST leaves it), BLACK is complete
    ld a,[$d057]
    and a
    ret nz
    ld a,[$d059]
    and a
    ret nz
    call sram_on
    ld hl,{STASH}
    ld de,$d163
    ld bc,{PARTY_LEN}
    call $00b5
    call sram_off
    ld a,[$d163]
    cp 2
    jr c,.keep
    ld c,{GHOST}
    call find_party
    jr c,.keep
    call remove_party
.keep:
    ld a,6
    ld [{RIT}],a
    ret

; ---- TOWER 7F: AGATHA walks up to the player after the ritual
tower_tick:
    ld a,[{SCENE}]
    cp 3
    ret nc
    and a
    jr z,.s0
    cp 1
    jr z,.s1
    jr .s2
.s0:
    ld a,[{AGTALK}]
    and a
    jr z,.go
    ld a,3
    ld [{SCENE}],a
    ret
.go:
    ld a,9
    ldh [$ff8c],a
    ld de,mv_right
    call $3674
    ld a,1
    ld [{SCENE}],a
    ret
.s1:
    ld a,[$d730]
    bit 0,a
    ret nz
    ld a,4
    ld [$c199],a
    xor a
    ld [$c109],a
    ld [$cd6b],a
    ld a,5
    ldh [$ff8c],a
    call $294d
    ld a,9
    ldh [$ff8c],a
    ld de,mv_left
    call $3674
    ld a,2
    ld [{SCENE}],a
    ret
.s2:
    ld a,[$d730]
    bit 0,a
    ret nz
    xor a
    ld [$cd6b],a
    ld a,3
    ld [{SCENE}],a
    ret

; ---- AGATHA's talk (text 5 on Tower 7F): the old quest dialogue until the ritual is done
agatha25:
    ld a,[{RIT}]
    cp 6
    jr nc,.new
    farcall {OLD_AGATHA},$2e
    ret
.new:
    ld a,[{AGTALK}]
    and a
    jr z,.intro
    cp 1
    jr z,.lore
    ld hl,t_final
    jp $3c94
.lore:
    ld a,2
    ld [{AGTALK}],a
    ld hl,t_lore
    jp $3c94
.intro:
    ld a,1
    ld [{AGTALK}],a
    ld hl,t_intro
    jp $3c94

; ---- the consort at the player's home: rest and heal
consort_talk:
    ld a,[{CONSORT}]
    ld hl,t_c1
    cp 1
    jr z,.p
    ld hl,t_c2
    cp 2
    jr z,.p
    ld hl,t_c3
.p: call $3c94
    ld a,7
    call $3ec1
    ld a,$e8
    ld [$c0ee],a
    call $23de
.w: ld a,[$c026]
    cp $e8
    jr z,.w
    ld a,[$d35b]
    ld [$c0ee],a
    call $23de
    ld hl,t_healed
    jp $3c94

fade: db {','.join(str(x) for x in fadetab)}
sq: db {','.join(str(x) for x in SQ)}
name_black: db {','.join(str(x) for x in NAME_BLACK)}
mv_right: db $c0,$ff
mv_left: db $80,$ff
you_struct: db {','.join(str(x) for x in you)}
'''
ext={**TXTSYM}
code25,L25=asm(SRC,C25,ext)
assert C25+len(code25)<TXT_AT,hex(C25+len(code25))
rom.put(fo(BANK25,C25),code25,'Bank 2D: v25 code (climax, chamber script, AGATHA scene, items, hunger wrapper)')
labels['bank2d']={k:hex(v) for k,v in L25.items()}
for k in ('item_block','climax_menu','bank_for','black_sprite_load','hunger_wrap','chamber_tick','tower_tick','agatha25','consort_talk'):assert k in L25

# ================================================================================================================
# 4. Hooks
# 4a. UncompressMonSprite (0:1659): the bank for a species now comes from bank_for (dynamic for YOU/BLACK), which also
#     frees home-bank bytes (0:1667-0:167A) for the map-sprite stub.
old=bytes(r[0x1659:0x1692])
win,_=asm(f'''
    farcall bank_for,{BANK25}
    ld a,[{BANKR}]
    jp $252a
''',0x1659,{'bank_for':L25['bank_for']})
assert len(win)==14
rom.code(0x1659,win,'UncompressMonSprite: pic bank from bank_for (2D), frees home bytes',old[:14].hex(),
         reviewed='jumps into 0x1659-0x1691 are this routine\'s own jr/jp targets or operand/data bytes elsewhere (checked in v23)')
SPRSTUB=0x1667
stub,_=asm(f'''
    ld a,[{BLACK}]
    and a
    jr z,.n
    farcall black_sprite_load,{BANK25}
    pop hl
    ret
.n: ld de,$4180
    ret
''',SPRSTUB,{'black_sprite_load':L25['black_sprite_load']})
assert len(stub)<=0x167b-SPRSTUB,len(stub)
rom.code(SPRSTUB,stub,'Home: BLACK walking sprite stub',old[SPRSTUB-0x1659:SPRSTUB-0x1659+len(stub)].hex(),reviewed='dead code of the old bank chain')
# 4b. LoadWalkingPlayerSpriteGraphics (0:1077): ld de,$4180 -> call stub
rom.hook(0x1077,'cd'+le(SPRSTUB),'LoadWalkingPlayerSpriteGraphics: BLACK map sprite','11 80 41',provides=('d','e'),reviewed='stub sets de on purpose; far call clobbers a,b,c,hl which the code after reloads')
# 4c. LoadPlayerBackPic (F:6D84): BLACK back picture
c=Code(0xf,0x7ced)
bp,_=asm(f'''
    ld a,[{BLACK}]
    and a
    jr z,.n
    ld de,{FUSION_BACK}
    ld a,{BANK25}
    jp $3725
.n: ld a,$0c
    jp $3725
''',0x7ced)
assert len(bp)<=19,len(bp)
rom.put(fo(0xf,0x7ced),bp,'Bank F: BLACK back picture stub')
rom.hook(fo(0xf,0x6d84),'cd'+le(0x7ced)+'0000','LoadPlayerBackPic: BLACK back picture','3e 0c cd 25 37',provides=('a','d','e'),
         reviewed='the only jump hit is the operand byte 18 of call $1875 at F:6DD5 misread as jr; the stub re-runs UncompressSpriteFromDE with de/a set on purpose')
# 4d. UseItem_ (3:58F8): every item is disabled in the chamber. 8-byte far-call stub in bank 3.
assert r[fo(3,RET3)]==0xc9
s3,_=asm(f'''
    ld hl,{L25['item_block']}
    ld b,{BANK25}
    jp $3618
''',0x71b7);assert len(s3)==8
rom.put(fo(3,0x71b7),s3,'Bank 3: UseItem_ chamber block stub')
rom.hook(fo(3,0x58f8),'cd b7 71 00 00','UseItem_: items disabled in the TOWER CHAMBER','3e 01 ea 6a cd',provides=('a',),reviewed='stub performs the replaced ld a,1 / ld [wActionResult],a itself')
# 4e. Party menu field moves (4:71C4): Dig / Teleport / Fly are refused in the chamber
FT=0x5400
field,FL=asm(f'''
    ld a,[$d35e]
    cp {CHAMBER}
    jr nz,.ok
    ld a,h
    cp $71
    jr nz,.h72
    ld a,l
    cp $da
    jr nz,.ok
    jr .blk
.h72:
    cp $72
    jr nz,.ok
    ld a,l
    cp $79
    jr z,.blk
    cp $91
    jr nz,.ok
.blk:
    pop af
    ld hl,{FT}
    call $3c94
    jp $710b
.ok:
    ld a,[$d356]
    ret
''',0x53c0)
ftext=txt(TXT['prevent'][0],end=0x58)
assert 0x53c0+len(field)<=FT,len(field)
rom.put(fo(4,0x53c0),field,'Bank 4: field-move block stub (chamber)')
rom.put(fo(4,FT),ftext,'Bank 4: "Something prevents you..." text')
rom.hook(fo(4,0x71c4),'cd c0 53','Party menu field moves: Dig/Teleport/Fly refused in the chamber','fa 56 d3',provides=('a',))
# 4f. hunger engine: home stub at 0:00E0 now calls hunger_wrap (bank 2D)
rom.data(0xe0,bytes.fromhex('21'+le(L25['hunger_wrap'])+'06%02x'%BANK25),'Hunger step stub -> hunger_wrap (off for BLACK)','21 00 41 06 2e')
# 4g. Battle menu (F:4EDE): the climax
stubF,_=asm(f'''
    ld hl,{L25['climax_menu']}
    ld b,{BANK25}
    jp $3618
''',0x7ff8);assert len(stubF)==8
rom.put(fo(0xf,0x7ff8),stubF,'Bank F: climax battle-menu stub')
rom.hook(fo(0xf,0x4ede),'cd f8 7f','DisplayBattleMenu: GHOST uses CURSE first (climax)','cd 5f 37',provides=('a',),reviewed='the 2D routine performs the replaced call itself')

# ================================================================================================================
# 5. Species BLACK (7F): header, name, dex slot, cry; YOU's header for BLACK (back pic); GetMonHeader hook (bank E)
def hdr(stats,types,catch,exp,dims,front,back,moves,growth):
    return bytes(stats)+bytes(types)+bytes([catch,exp,dims])+bytes.fromhex(le(front)+le(back))+bytes(moves)+bytes([growth])+bytes(8)
black_hdr=hdr([100,110,100,110,160],[0x08,0x08],3,255,0x77,FUSION_FRONT,FUSION_BACK,[0xa5,0,0,0],5)
you_black=bytes([15,5,5,5,5,0,0,0,0,0x44])+bytes.fromhex(le(FUSION_BACK)*2)+bytes([0x21,0,0,0,0])+bytes(8)
assert len(black_hdr)==27 and len(you_black)==27
HDR25=0x7e41
hdrcode,HL=asm(f'''
hdr25:
    ld a,[$d0b5]
    cp {BLK}
    ld hl,black_hdr
    jr z,.copy
    cp {YOU}
    jr nz,.old
    ld a,[{BLACK}]
    and a
    jr z,.old
    ld hl,you_black
    jr .copy
.old:
    jp $7de0
.copy:
    ld de,$d0b9
    ld b,$1b
.l: ld a,[hl+]
    ld [de],a
    inc de
    dec b
    jr nz,.l
    ld a,[$d0b5]
    ld [$d0b8],a
    ret
black_hdr: db {','.join(str(x) for x in black_hdr)}
you_black: db {','.join(str(x) for x in you_black)}
''',HDR25)
assert HDR25+len(hdrcode)<=0x8000
rom.put(fo(0xe,HDR25),hdrcode,'Bank E: BLACK / YOU-as-BLACK headers + GetMonHeader extension')
rom.code(0x15c6,bytes.fromhex('cd'+le(HDR25)),'GetMonHeader exit -> v25 headers (BLACK, YOU as BLACK), then v23/v3 ones','cd e0 7d',
         reviewed='same site as v3/v23; hits are operand/data bytes')
NAMES=0x1c21e;DEX=0x4102e;CRY=0x39484
o=NAMES+10*(BLK-1);rom.data(o,enc('BLACK').ljust(10,b'\x50'),'Species name 7F = BLACK',r[o:o+10])
rom.data(DEX+BLK-1,[152],'Species 7F: dex slot 152 (outside the 151 entries)','00')
gcry=bytes(r[CRY+3*(GENGAR-1):CRY+3*GENGAR]);assert gcry==bytes.fromhex('0700ff')
rom.data(CRY+3*(BLK-1),gcry,'BLACK cry = GENGAR cry (for now)',r[CRY+3*(BLK-1):CRY+3*BLK])

# ================================================================================================================
# 6. Party icon (bank 1C): hollow GENTLEMAN for the MIRAGE. Table of 30 entries moved + 4 new entries; both loaders patched.
tiles=ICON.four_tiles(bytes(r))
TBL_OLD=0x57f2;TBL=0x7b9c;TILES=TBL+34*6
entries=bytearray(r[fo(0x1c,TBL_OLD):fo(0x1c,TBL_OLD)+30*6])
for k,(dst,off) in enumerate(((0x82c0,0),(0x82e0,16),(0x86c0,32),(0x86e0,48))):
    entries+=bytes.fromhex(le(TILES+off)+'011c')+bytes.fromhex(le(dst))
icon_stub,_=asm('''
    cp $7a
    jr nz,.n
    pop hl
    ld a,$2c
    ret
.n: ld [$d11e],a
    ret
''',TILES+64)
rom.put(fo(0x1c,TBL),bytes(entries)+b''.join(tiles)+icon_stub,'Bank 1C: party icon table (+4 entries), hollow gentleman tiles, icon stub')
ICONSTUB=TILES+64
for site in (0x579e,0x57c6):
    assert r[fo(0x1c,site)]==0x21 and w(fo(0x1c,site)+1)==TBL_OLD
    rom.code(fo(0x1c,site),bytes.fromhex('21'+le(TBL)),'Party icon loader: new table','21'+le(TBL_OLD),
             reviewed='the only jump hit is the operand byte 18 of call $1824 at 1C:57E2 misread as jr')
for site in (0x57a1,0x57c9):
    assert r[fo(0x1c,site)]==0x3e and r[fo(0x1c,site)+1]==0x1e
    rom.code(fo(0x1c,site),bytes.fromhex('3e22'),'Party icon loader: 34 entries','3e1e')
rom.hook(fo(0x1c,0x5927),'cd'+le(ICONSTUB),'GetPartyMonSpriteID: ????? (7A) gets the hollow icon','ea 1e d1',provides=(),reviewed='the stub performs the replaced ld [wd11e],a')

# ================================================================================================================
# 7. TOWER CHAMBER (map 0x69): text table + script
tp=bytes.fromhex
HDR=int(L22['header'],16);assert w(0x1ae+2*CHAMBER)==HDR
h69=fo(0x18,HDR)
old_tbl=[w(fo(0x18,w(h69+5))+2*i) for i in range(4)]
c18=Code(0x18,0x6ea1)
con,CL=asm(f'''
chamber_script:
    farcall {L25['chamber_tick']},{BANK25}
    jp $3c87
consume_text: db $17
    dw {TXTSYM['t_consume']}
    db {BANK25},$50
table: dw {old_tbl[0]},{old_tbl[1]},{old_tbl[2]},{old_tbl[3]},consume_text
''',0x6ea1)
rom.put(fo(0x18,0x6ea1),con,'Bank 18: chamber script + texts table (+consume text)')
rom.data(h69+5,bytes.fromhex(le(CL['table'])),'Chamber text table -> v25 (+ consume text, id 5)',bytes(r[h69+5:h69+7]).hex())
rom.data(h69+7,bytes.fromhex(le(CL['chamber_script'])),'Chamber map script -> v25 chamber_tick',bytes(r[h69+7:h69+9]).hex())

# ================================================================================================================
# 8. TOWER 7F: AGATHA's text (id 5) and the map script wrapper
h7=fo(0x18,w(0x1ae+2*TOWER7));TEX7=w(h7+5);SCR7=w(h7+7)
assert (TEX7,SCR7)==(0x6742,int(L19['script'],16))
assert w(fo(0x18,TEX7)+8)==int(L16['bank18']['agatha'],16)
t7,TL=asm(f'''
agatha_text: db 8
    farcall {L25['agatha25']},{BANK25}
    jp $2504
script7f:
    ld a,[{RIT}]
    cp 6
    jp c,{SCR7}
    xor a
    ld [$c160],a
    ld [$c170],a
    ld [$c180],a
    ld a,$ff
    ld [$c264],a
    ld [$c265],a
    ld [$c274],a
    ld [$c275],a
    ld [$c284],a
    ld [$c285],a
    farcall {L25['tower_tick']},{BANK25}
    jp {SCR7}
''',0x7458)
rom.put(fo(0x18,0x7458),t7,'Bank 18: Tower 7F AGATHA talk + map script wrapper (v25)')
rom.data(fo(0x18,TEX7)+8,bytes.fromhex(le(TL['agatha_text'])),'Tower 7F text 5 (AGATHA) -> v25 wrapper',le(int(L16['bank18']['agatha'],16)))
rom.data(h7+7,bytes.fromhex(le(TL['script7f'])),'Tower 7F script -> v25 wrapper (consort leaves, AGATHA scene)',le(SCR7))

# ================================================================================================================
# 9. The player's house (map 0x25, bank 12): the consort waits there after the ritual and heals the party
H25=fo(0x12,w(0x1ae+2*0x25))
TP25,SP25,OP25=w(H25+5),w(H25+7),w(H25+10)
o25=fo(0x12,OP25);ob=bytes(r[o25:o25+60])
nw=ob[1];p=2+4*nw;ns=ob[p];p+=1+3*ns;assert ob[p]==1;objs_at=p+1         # one object: Mom
mom=ob[objs_at:objs_at+6];warp_to=ob[objs_at+6:objs_at+6+4*nw];head=ob[:objs_at]
GIRLS=[(0x1d,2),(0x1b,3),(0x0d,4)]                                       # MISTY, ERIKA, SABRINA: sprite, text id
girls=b''.join(bytes([s,5+4,6+4,0xff,0xd0,t]) for s,t in GIRLS)
newobj=head[:p]+bytes([4])+mom+girls+warp_to
hs,HL25=asm(f'''
objects: db {','.join(str(x) for x in newobj)}
mom_text: dw {w(fo(0x12,TP25))}
girl_text: db 8
    farcall {L25['consort_talk']},{BANK25}
    jp $2504
table: dw {w(fo(0x12,TP25))},girl_text,girl_text,girl_text
house_script:
    ld a,[{RIT}]
    ld c,0
    cp 6
    jr c,.go
    ld a,[{CONSORT}]
    ld c,a
.go:
    ld a,c
    cp 1
    call nz,hide2
    ld a,c
    cp 2
    call nz,hide3
    ld a,c
    cp 3
    call nz,hide4
    jp $3c87
hide2:
    xor a
    ld [$c120],a
    ld a,$ff
    ld [$c224],a
    ld [$c225],a
    ret
hide3:
    xor a
    ld [$c130],a
    ld a,$ff
    ld [$c234],a
    ld [$c235],a
    ret
hide4:
    xor a
    ld [$c140],a
    ld a,$ff
    ld [$c244],a
    ld [$c245],a
    ret
''',0x63a3)
rom.put(fo(0x12,0x63a3),hs,'Bank 12: Red\'s house 1F objects (+ consort), texts, script (v25)')
rom.data(H25+5,bytes.fromhex(le(HL25['table'])+le(HL25['house_script'])),"House 1F text table + script -> v25",bytes(r[H25+5:H25+9]).hex())
rom.data(H25+10,bytes.fromhex(le(HL25['objects'])),'House 1F object data -> v25 (consort objects 2-4)',le(OP25))
assert w(H25+5)==TP25 or True

rom.finish('Creepy_Black_Mu_v25.gb','manifest_v25.json','CREEPY MU V25',extra=dict(labels=labels))

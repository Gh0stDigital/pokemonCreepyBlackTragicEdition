# Creepy Black Mu v29: CURSE kills every trainer, and no more RAM corruption.
#
# The bug (base hack, all versions): TalkToTrainer (0:3201) reads a trainer's "kill index" from offset 0xA of its trainer
# header (D4AE/AF). The base hack only wrote real indices into 23 of the 322 headers (the early routes). For the other
# 299 that word is still a text pointer ($4000-$7FFF), so CURSE treated them as killable and the kill set bit
# (pointer/8) above D4A4: a random byte in DCA4-E4A3 (PC box data, the stack, and through echo RAM the sprite tables,
# OAM buffer and screen tile map). And as no gravestone list knew them, the trainer never died either. From NUGGET BRIDGE
# on (the first trainers without an index) CURSE stopped killing and the game slowly broke.
#
# v29:
#   1. every unassigned header gets a unique kill index: 34-79 (free bits of the D4A4 array) and $100-$1FB (new array
#      D430-D44F: 32 bytes of pokered's unused "ds 128" after wDestinationWarpID, inside the saved block, never referenced).
#      The one header no map text uses gets 0 (can't be killed).
#   2. the bit routine (3:4DB9, rewritten in place, same size) maps index >= $100 into D430.
#   3. map load: every killed trainer turns into a gravestone (table of map -> (sprite, index) in bank 2D, checked by the
#      v28 map-load hook after its NPC kill list).
#   4. NEW GAME clears D430-D4AD (was D450-D4AD).
import json,sys
from patchlib import *
from patchguard import fo
from sm83asm import asm
import killmap as K

V28_SHA='e0d0c997b1c1e40f497a0fe9414e850400e6a670289682486727b2d3b30b9f94'
rom=Rom('Creepy_Black_Mu_v28.gb',V28_SHA)
r=rom.r;R=bytes(r)
w=lambda o:R[o]|R[o+1]<<8
BANK=0x2d;CODE=0x6400
OLD_KILL_CHK=int(json.load(open('manifest_v28.json'))['labels']['bank2d']['kill_chk'],16)
HOME_KILL=0x1688

# ---------------------------------------------------------------------------------------------- 1. kill indices
hs=K.headers(R);assert len(hs)==322
hm=K.header_maps(R,hs)
used=sorted(w(h+10) for h in hs if w(h+10)<0x100)
assert max(used)<34,used
todo=[h for h in hs if w(h+10)>=0x100];assert len(todo)==299
assert all(w(h+10)==w(h+8) for h in todo)                    # the duplicated end-battle text pointer = no index
idx={}
free=list(range(34,80))+list(range(0x100,0x200))
for h in todo:
    if h not in hm:idx[h]=0;continue                         # header that no map text uses: not killable
    idx[h]=free.pop(0)
assert max(idx.values())<0x200 and (max(idx.values())-0x100)//8<32
for h,i in idx.items():
    rom.data(h+10,i.to_bytes(2,'little'),'Trainer header %02X:%04X: kill index %d'%(h//0x4000,0x4000+h%0x4000,i),R[h+10:h+12])

# ---------------------------------------------------------------------------------------------- 2. bit routine (3:4DB9)
KB=fo(3,0x4db9)
kb,_=asm('''
    ld a,d
    and a
    jr z,.go
    ld d,0
    ld hl,$d430                  ; index >= $100: the new array
.go:ld a,e
    and 7
    ld c,a
    srl d
    rr e
    srl d
    rr e
    srl d
    rr e
    add hl,de
    ld a,1
    inc c
.m: dec c
    jr z,.k
    add a
    jr .m
.k: ld c,a
    dec b
    jr z,.set
    dec b
    jr z,.test
    ld a,c                       ; b = 0: reset
    cpl
    and [hl]
    ld [hl],a
    ret
.set:
    ld a,[hl]
    or c
    ld [hl],a
    ret
.test:
    ld a,[hl]
    and c
    ld c,a
    ret
''',0x4db9)
assert len(kb)==0x37,len(kb)
assert R[KB+0x36]==0xc9
rom.code(KB,kb,'Kill bit routine: indices >= $100 use D430-D44F',R[KB:KB+0x37].hex(),
         reviewed='all hits are the old routine\'s own internal jr\'s (sources 3:4DCC-4DE1 inside 4DB9-4DEF); the whole routine is replaced')

# ---------------------------------------------------------------------------------------------- 3. gravestones for all
lists={}
for h in hs:
    i=idx.get(h,w(h+10))
    if not i or h not in hm:continue
    for mp in hm[h]:lists.setdefault(mp,[]).append((R[h],i))
tab_ptrs=bytearray();tab_lists=bytearray()
LISTS_AT=CODE+0x100+2*0xf8
for mp in range(0xf8):
    if mp in lists:
        tab_ptrs+=(LISTS_AT+len(tab_lists)).to_bytes(2,'little')
        for spr,i in lists[mp]:tab_lists+=bytes([spr,i&255,i>>8])
        tab_lists.append(0)
    else:tab_ptrs+=b'\0\0'
code,L=asm(f'''
kill_chk2:                       ; map load, sprite offset e: NZ = gravestone. (the v28 NPC list first)
    call {OLD_KILL_CHK}
    ret nz
    ld a,e
    swap a
    ld c,a                       ; c = sprite index
    push de
    ld a,[$d35e]
    ld l,a
    ld h,0
    add hl,hl
    ld de,{CODE+0x100}
    add hl,de
    ld a,[hl+]
    ld h,[hl]
    ld l,a
    or h
    jr z,.no
.l: ld a,[hl+]
    and a
    jr z,.no
    cp c
    jr nz,.skip
    ld e,[hl]
    inc hl
    ld d,[hl]
    push hl
    ld hl,$d4a4
    ld a,d
    and a
    jr z,.lo
    ld hl,$d430
.lo:ld a,e
    and 7
    ld b,a
    srl e
    srl e
    srl e
    ld d,0
    add hl,de
    ld a,[hl]
    inc b
.sh:dec b
    jr z,.bit
    rrca
    jr .sh
.bit:
    pop hl
    and 1
    jr nz,.yes
    dec hl
.skip:
    inc hl
    inc hl
    jr .l
.no:pop de
    xor a
    ret
.yes:
    pop de
    ret
''',CODE,{})
assert len(code)<=0x100,len(code)
blob=code+bytes(0x100-len(code))+bytes(tab_ptrs)+bytes(tab_lists)
rom.put(fo(BANK,CODE),blob,'Bank 2D: v29 trainer gravestone check + map -> (sprite, kill index) table')
old=R[HOME_KILL:HOME_KILL+3]
assert old==bytes([0x21])+OLD_KILL_CHK.to_bytes(2,'little')
rom.data(HOME_KILL+1,L['kill_chk2'].to_bytes(2,'little'),'Map-load gravestone stub -> kill_chk2 (NPC list + all trainers)',old[1:])

# ---------------------------------------------------------------------------------------------- 4. NEW GAME clear
rom.data(fo(3,0x7bc9),bytes.fromhex('2130d4017e00'),'NEW GAME: clear D430-D4AD (new kill bits included)','2150d4015e00')

rom.finish('Creepy_Black_Mu_v29.gb','manifest_v29.json','CREEPY MU V29',extra=dict(
    labels=dict(bank2d={k:hex(v) for k,v in L.items()}),
    kill_index={'%02X:%04X'%(h//0x4000,0x4000+h%0x4000):i for h,i in idx.items()},
    trainer_maps={'%02X:%04X'%(h//0x4000,0x4000+h%0x4000):sorted(hex(x) for x in v) for h,v in hm.items()}))

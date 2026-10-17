# Creepy Black Mu v75: POKeMON TOWER 7F: the channelers stay loaded after a menu / text / battle redraw.
#   ch53 (v53) hides every channeler that is more than two steps away by writing picture 0 (the GB draws ten sprites at most). InitMapSprites (re-run on every
#   redraw: START menu, battle return ...) gives a VRAM tile slot only to pictures that some sprite has RIGHT THEN, and v36 skips picture 0: with all
#   channelers hidden the channeler tiles were not loaded again and every slot read 0, so after the first menu on the floor no channeler was ever drawn
#   (and AGATHA's / the girl's slots shifted). Worse, a redraw does not copy the tiles again, so the slot numbers must be the ones of the map load: sprites drew other pictures
#   (pigtail girls) from the stale VRAM. Now, before InitMapSprites' body runs (v67 im67 chain), objects 4-15 of 7F get the pictures of the object list back
#   (stage 5, ritual not over, long object list), so every load / redraw hands out the same slots; ch53 hides / shows them again next frame.
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V74_SHA='a241a52fd2ea515cf4b1966440df6df0bdf7c4cfff270d29d2bfc2f189ee3d2b'
rom=Rom('Creepy_Black_Mu_v74.gb',V74_SHA)
R=bytes(rom.r)
B31=0x31
L74={k:int(v,16) for k,v in json.load(open('manifest_v74.json'))['labels']['bank31'].items()}
L67={k:int(v,16) for k,v in json.load(open('manifest_v67.json'))['labels']['bank31'].items()}
A=0x4b00
assert not any(R[fo(B31,A):fo(B31,A)+0x40])
code,L=asm(f'''
app75:                           ; (from im67, before InitMapSprites' body) channeler anchor, then the shamanesses (app74)
    ld a,[$d35e]
    cp $94
    jr nz,.o
    ld a,[$d464]
    cp 5
    jr nz,.o
    ld a,[$d467]
    cp 6
    jr nc,.o
    ld a,[$d4e1]
    cp 10
    jr c,.o                      ; the short object list: no channelers
    ld hl,lpic75                 ; objects 4-15 get the pictures of the object list again, exactly as at the map load: the slot numbers the loader hands out then are the
    ld de,$c140                  ; ones the tiles in VRAM were loaded for (a redraw after a menu does not copy the tiles again)
    ld b,12
.l: ld a,[hl+]
    ld [de],a
    ld a,e
    add 16
    ld e,a
    dec b
    jr nz,.l
.o: jp {L74['app66']}
lpic75: db $16,$39,$1d,$1b,$0d,$39,$19,$19,$19,$19,$19,$19
''',A,{})
rom.put(fo(B31,A),code,'Bank 31: v75 app75 (7F object pictures as at the map load before the sprite loader, then app74)')
o=fo(B31,L67['im67']);assert R[o:o+6].hex()=='cd'+le(L74['app66'])+'c3'+le(L67['gymhide']),R[o:o+6].hex()
rom.data(o+1,bytes.fromhex(le(L['app75'])),'im67: call app74 -> app75',le(L74['app66']))
rom.finish('Creepy_Black_Mu_v75.gb','manifest_v75.json','CREEPY MU V75',extra=dict(labels=dict(bank31={k:hex(v) for k,v in L.items()})))

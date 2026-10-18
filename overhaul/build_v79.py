# Creepy Black Mu v79: after the ritual, back on TOWER 7F (BLACK): AGATHA's sprite glitched (black silhouette), the channelers and the player's MOM never showed; and MOM must leave the player's house.
#   1. v75's app75 (7F object pictures as in the object list before the sprite loader) only ran while the ritual was not over (RIT < 6). After the ritual the long list is still loaded
#      (v54: channelers + MOM = object 15, picture 33) but the loader assigned slots only to the pictures that were non-zero at that moment: every redraw (each AGATHA text box!)
#      shifted AGATHA's slot against the tiles loaded at the map load (black silhouette), and the hidden channelers / MOM got no slot at all (image index FF = never drawn).
#      Now app75 runs whenever the long list is loaded (stage 5), and object 15's list picture is MOM's (33), as in the real list (it was the channeler picture in the table).
#   2. The player's house (map 25): once the player is BLACK (RIT 6) MOM is not there any more (hidden by the map script every frame); the consort still waits there.
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V78_SHA='a00dc5797b476adfd862385a36f3ab65dbfbeeee03737911e8102bc744ffe64c'
rom=Rom('Creepy_Black_Mu_v78.gb',V78_SHA)
R=bytes(rom.r)
def lh(a):return a.to_bytes(2,'little').hex()
L75=json.load(open('manifest_v75.json'))['labels']['bank31']
A=int(L75['app75'],16);TAB=int(L75['lpic75'],16)
o=fo(0x31,A)+14;assert R[o:o+7].hex()=='fa67d4fe063018',R[o:o+7].hex()
rom.code(o,bytes(7),'app75: the pictures of the 7F object list also after the ritual (no RIT < 6 test)','fa67d4fe063018',reviewed='nops over a load/compare/jr nc that only skipped the restore')
o=fo(0x31,TAB)+11;assert R[o]==0x19
rom.data(o,bytes([0x33]),'lpic75: object 15 = MOM picture (33), as in the 7F object list','19')
# the house
w=lambda a:R[a]|R[a+1]<<8
H=fo(0x12,w(0x1ae+2*0x25));SCR=w(H+7);assert SCR==0x63f0
B=0x7200
assert not any(R[fo(0x12,B):fo(0x12,B)+0x20])
c,L=asm(f'''
house79:                         ; map script of the player's house: MOM is gone once the player is BLACK, then v25's script
    ld a,[0xd467]
    cp 6
    jr c,.o
    xor a
    ld [$c110],a                ; object 1 (MOM): picture 0, position FF
    ld a,$ff
    ld [$c214],a
    ld [$c215],a
.o: jp {SCR:#x}
''',B,{})
rom.put(fo(0x12,B),c,'Bank 12: v79 house79 (MOM leaves the player\'s house when BLACK)')
rom.data(H+7,bytes.fromhex(lh(L['house79'])),"House 1F map script -> house79",lh(SCR))
rom.finish('Creepy_Black_Mu_v79.gb','manifest_v79.json','CREEPY MU V79',extra=dict(labels=dict(bank12={k:hex(v) for k,v in L.items()})))

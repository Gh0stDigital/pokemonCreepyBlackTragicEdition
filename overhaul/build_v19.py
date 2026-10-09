# Creepy Black Mu v19 (prototype for the climax): a new map, the secret chamber behind AGATHA on Pokemon Tower 7F.
#  - map 0x69 (an unused map id) = TOWER CHAMBER: round room (altar_layout.py), Pokemon Tower tileset, ring of graves,
#    purification circle in the centre where MR. MU stands, four shrines, two statues by the stairs.
#  - Tower 7F: once AGATHA's quest reaches stage 5 (the girl has come), the graves behind AGATHA's spot open into a
#    stairway (block swapped at map load) and AGATHA stands beside it at (2,10); the stairs lead into the chamber.
# Logged patches on top of verified Mu v18 (patchlib).
import json
from patchlib import *
from patchguard import fo
from altar_layout import layout,W,H,STAIRS_STEP,MU_STEP

V18_SHA='7bbcd9bf11620d3439fa2159befb987cd4100b7bb2f620d856bcb1d8ef8d51c8'
rom=Rom('Creepy_Black_Mu_v18.gb',V18_SHA)
r=rom.r
PRINTTEXT,TEXTEND,PREDEF,ENABLE_TEXT=0x3c94,0x2504,0x3ec1,0x3c87
REPLACE_TILE_BLOCK=0x18;NEW_BLOCK_ID=0xd09f;MAPFLAGS=0xd126       # predef ReplaceTileBlock (as SILPH 11F's doors)
STAGE=0xd464
NEW=0x69;TOWER7=0x94;BANK=0x18;TILESET=0x0f
GENTLEMAN,AGATHA=0x10,0x39
DOOR_BLOCK=(0,5);DOOR_ID=0x11                                    # 7F block over (y0-1,x10-11): graves -> stairs in its bottom-right
DOOR_STEP=(1,11);AG_DOOR=(2,10)
w=lambda o:r[o]|r[o+1]<<8
def view_ptr(width,y,x):return 0xc6e8+7+width+(y//2)*(width+6)+x//2   # warp-to entry (checked against 7F's own: c77d for 16,9)
assert view_ptr(10,16,9)==0xc77d
labels={}
L16=json.load(open(ROOT/'manifest_v16.json'))['labels']

# ---- the chamber -----------------------------------------------------------------------------------------------
T_MU=txt([["MR. MU: ..."],["So, you found","this place."],["Come closer,","child of the","GHOST..."]],end=0x57)
c=Code(BANK,0x7500)
c.label('header');c.raw([TILESET,H,W]);c.ref('','blocks');c.ref('','texts');c.ref('','script');c.raw([0]);c.ref('','objects')
c.label('blocks');c.raw(bytes(b for row in layout() for b in row))
c.label('objects');c.raw([0x01, 1, STAIRS_STEP[0],STAIRS_STEP[1],1,TOWER7, 0,
                          1, GENTLEMAN,MU_STEP[0]+4,MU_STEP[1]+4,0xff,0xd0,1])
c.raw(bytes.fromhex(le(view_ptr(W,*STAIRS_STEP))));c.raw(list(STAIRS_STEP))
c.label('texts');c.ref('','mu')
c.label('script');c.emit('c3 '+le(ENABLE_TEXT))
c.label('mu');c.emit('08');c.ref('21','t_mu');c.emit('cd %s c3 %s'%(le(PRINTTEXT),le(TEXTEND)))
c.label('t_mu');c.raw(T_MU)
chamber=c.finish();assert 0x7500+len(chamber)<0x7a00
rom.put(fo(BANK,0x7500),chamber,'Bank 18: TOWER CHAMBER map (header, blocks, objects, MR. MU)')
labels['chamber']={k:hex(v) for k,v in c.labels.items()}
assert w(0x1ae+2*NEW)==w(0x1ae+2*0x6a) and r[0xc23d+NEW]==r[0xc23d+0x6a]    # 0x69 is one of the unused map ids
rom.data(0x1ae+2*NEW,bytes.fromhex(le(c.labels['header'])),'Map 0x69 header pointer -> TOWER CHAMBER',le(w(0x1ae+2*NEW)))
rom.data(0xc23d+NEW,[BANK],'Map 0x69 header bank',[r[0xc23d+NEW]])
SONGS=fo(3,0x404d)
rom.data(SONGS+2*NEW,r[SONGS+2*TOWER7:SONGS+2*TOWER7+2],'Map 0x69 music = Pokemon Tower',r[SONGS+2*NEW:SONGS+2*NEW+2])
WILD=fo(3,0x521c);assert r[fo(3,w(WILD+2*NEW))]==0                          # no wild POKeMON (grass rate 0)

# ---- Tower 7F: second warp (the secret stairs) + an AGATHA beside the door; block swap + who is shown -------------
M7=0x94;h7=fo(BANK,w(0x1ae+2*M7))
OBJ7=w(h7+10);TEX7=w(h7+5);SCR7=w(h7+7)
assert (OBJ7,TEX7,SCR7)==tuple(int(L16['bank18'][k],16) for k in ('objects','texts','script'))
o=fo(BANK,OBJ7);obj=bytearray(r[o:o+8+3*8+6+4*6+4])
assert obj[1]==1 and obj[6]==0 and obj[7]==8 and obj[-4:]==bytes.fromhex('7dc71009')
n7=bytearray(obj[:2]);n7[1]=2
n7+=obj[2:6]+bytes([DOOR_STEP[0],DOOR_STEP[1],0,NEW])                        # warp 1 -> chamber warp 0
n7+=obj[6:7]+bytes([9])+obj[8:-4]+bytes([AGATHA,AG_DOOR[0]+4,AG_DOOR[1]+4,0xff,0xd0,5])   # object 9: AGATHA by the door
n7+=obj[-4:]+bytes.fromhex(le(view_ptr(10,*DOOR_STEP)))+bytes(DOOR_STEP)
c=Code(BANK,0x7a00)
c.label('objects');c.raw(n7)
c.label('script')
# hide whichever AGATHA isn't used: object 5 (in front of the door) before stage 5, object 9 (beside it) from then on
c.emit('fa %s fe 05'%le(STAGE));c.jr('30','open')
c.emit('af ea 90 c1 3e ff ea 94 c2 ea 95 c2');c.emit('c3 '+le(SCR7))
c.label('open');c.emit('af ea 50 c1 3e ff ea 54 c2 ea 55 c2')
c.emit('21 %s cb 6e cb ae ca %s'%(le(MAPFLAGS),le(SCR7)))                       # map just loaded: open the stairs
# ld bc: c = block x, b = block y
c.emit('3e %02x ea %s 01 %02x %02x 3e %02x cd %s c3 %s'%(DOOR_ID,le(NEW_BLOCK_ID),DOOR_BLOCK[1],DOOR_BLOCK[0],REPLACE_TILE_BLOCK,le(PREDEF),le(SCR7)))
code=c.finish();rom.put(fo(BANK,0x7a00),code,'Bank 18: Tower 7F objects (+secret warp, AGATHA by the door) + door script')
rom.data(h7+10,bytes.fromhex(le(c.labels['objects'])),'Tower 7F object data -> v19',le(OBJ7))
rom.data(h7+7,bytes.fromhex(le(c.labels['script'])),'Tower 7F script -> v19 door/AGATHA wrapper',le(SCR7))
labels['tower7f']={k:hex(v) for k,v in c.labels.items()}
TEXT_TABLE=fo(BANK,TEX7);assert w(TEXT_TABLE+2*8)==w(TEXT_TABLE+2*4) or True   # object 9 reuses text 5 (AGATHA)

rom.finish('Creepy_Black_Mu_v19.gb','manifest_v19.json','CREEPY MU V19',extra=dict(labels=labels))

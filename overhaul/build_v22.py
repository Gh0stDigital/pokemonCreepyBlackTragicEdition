# Creepy Black Mu v22: fossils on the stands in front of the three chamber statues (the Mt. Moon fossil sprite 3E, still).
# The chamber keeps v21's blocks, warp, script and MR. MU; it gets a new header/object list/text table with 3 more objects.
# Logged patches on top of verified Mu v21 (patchlib).
import json
from patchlib import *
from patchguard import fo
from altar_layout_v21 import W_BLK,H_BLK,STAIRS_STEP,MU_STEP

V21_SHA='63b8b00c4aba9782a37626819104247b85276ec36fce671a970c55fbcb37b93b'
rom=Rom('Creepy_Black_Mu_v21.gb',V21_SHA)
r=rom.r
w=lambda o:r[o]|r[o+1]<<8
NEW=0x69;BANK=0x18;TOWER7=0x94;GENTLEMAN,FOSSIL=0x10,0x3e
L=json.load(open(ROOT/'manifest_v21.json'))['labels']['chamber']
HDR,BLOCKS,SCRIPT,MU=(int(L[k],16) for k in ('header','blocks','script','mu'))
assert w(0x1ae+2*NEW)==HDR and r[fo(BANK,HDR):fo(BANK,HDR)+3]==bytes([0x0f,H_BLK,W_BLK])
FOSSILS=[((7,11),'OLD AMBER'),((15,6),'DOME FOSSIL'),((15,16),'HELIX FOSSIL')]   # the stands (gravestones) of v21
def view_ptr(width,y,x):return 0xc6e8+7+width+(y//2)*(width+6)+x//2
c=Code(BANK,0x7d40)
c.label('header');c.raw([0x0f,H_BLK,W_BLK]);c.raw(bytes.fromhex(le(BLOCKS)));c.ref('','texts');c.raw(bytes.fromhex(le(SCRIPT)));c.raw([0]);c.ref('','objects')
c.label('objects');c.raw([0x11, 1, STAIRS_STEP[0],STAIRS_STEP[1],1,TOWER7, 0, 1+len(FOSSILS),
                          GENTLEMAN,MU_STEP[0]+4,MU_STEP[1]+4,0xff,0xd0,1])
for i,((y,x),name) in enumerate(FOSSILS):c.raw([FOSSIL,y+4,x+4,0xff,0xff,2+i])
c.raw(bytes.fromhex(le(view_ptr(W_BLK,*STAIRS_STEP))));c.raw(list(STAIRS_STEP))
c.label('texts');c.raw(bytes.fromhex(le(MU)))
for i in range(len(FOSSILS)):c.ref('','f%d'%i)
for i,(pos,name) in enumerate(FOSSILS):
    c.label('f%d'%i);c.emit('08');c.ref('21','t%d'%i);c.emit('cd 94 3c c3 04 25')
    c.label("t%d"%i);c.raw(txt([["The %s"%name,"rests on the","stand."]],end=0x57))
code=c.finish();assert 0x7d40+len(code)<=0x8000,len(code)
rom.put(fo(BANK,0x7d40),code,'Bank 18: TOWER CHAMBER v22 header/objects/texts (+3 fossils)')
rom.data(0x1ae+2*NEW,bytes.fromhex(le(c.labels['header'])),'Map 0x69 header -> v22 (fossils on the stands)',le(HDR))
rom.finish('Creepy_Black_Mu_v22.gb','manifest_v22.json','CREEPY MU V22',extra=dict(labels={'chamber':{k:hex(v) for k,v in c.labels.items()}}))

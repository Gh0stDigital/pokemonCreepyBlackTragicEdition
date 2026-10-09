# Creepy Black Mu v21: TOWER CHAMBER with a ring around the centre tile and a triangle of three POKeMON statues, each with
# a gravestone in front (altar_layout_v21.py). New blocks after v20's (slots 75-AF).

# Logged patches on top of verified Mu v20 (patchlib).
import json
from patchlib import *
from patchguard import fo
from altar_layout_v21 import steps,blocks,W_BLK,H_BLK,STAIRS_STEP,MU_STEP

V20_SHA='9203c4809f4f90014020dc59f95afda5b9d337ca3079a78461456be60b71113c'
rom=Rom('Creepy_Black_Mu_v20.gb',V20_SHA)
r=rom.r
w=lambda o:r[o]|r[o+1]<<8
NEW=0x69;BANK=0x18;TOWER7=0x94;GENTLEMAN=0x10
BLOCKSET=fo(0x1b,0x45c0);FREE_IDS=range(0x75,0xb0)
# blocks: reuse an existing Tower block when the 16 tiles match, else take a free slot
existing={bytes(r[BLOCKSET+16*b:BLOCKSET+16*b+16]):b for b in range(0x75)}
used_by_maps=set()
for m in range(0xf8):
    bank=r[0xc23d+m];hp=w(0x1ae+2*m)
    if hp<0x4000 or bank==0:continue
    h=fo(bank,hp)
    if r[h]==0x0f:used_by_maps|=set(r[fo(bank,w(h+3)):fo(bank,w(h+3))+r[h+1]*r[h+2]])
used_by_maps-=set(range(0x6e,0x75))   # v20's chamber blocks (map 0x69, replaced below)
assert not used_by_maps&set(FREE_IDS),sorted(used_by_maps&set(FREE_IDS))
B=blocks(steps());ids={};nxt=iter(FREE_IDS)
for row in B:
    for b in row:
        if b in existing:ids[b]=existing[b]
        elif b not in ids:
            i=next(nxt);ids[b]=i
            rom.data(BLOCKSET+16*i,b,'Tower blockset slot %02X: chamber block'%i,r[BLOCKSET+16*i:BLOCKSET+16*i+16])
grid=[[ids[b] for b in row] for row in B]
new_ids=sorted(v for v in ids.values() if v>=0x75);print('new blocks',[hex(x) for x in new_ids])

def view_ptr(width,y,x):return 0xc6e8+7+width+(y//2)*(width+6)+x//2
T_MU=txt([["MR. MU: ..."],["So, you found","this place."],["Come closer,","child of the","GHOST..."]],end=0x57)
c=Code(BANK,0x7600)
c.label('header');c.raw([0x0f,H_BLK,W_BLK]);c.ref('','blocks');c.ref('','texts');c.ref('','script');c.raw([0]);c.ref('','objects')
c.label('blocks');c.raw(bytes(b for row in grid for b in row))
c.label('objects');c.raw([0x11, 1, STAIRS_STEP[0],STAIRS_STEP[1],1,TOWER7, 0,
                          1, GENTLEMAN,MU_STEP[0]+4,MU_STEP[1]+4,0xff,0xd0,1])
c.raw(bytes.fromhex(le(view_ptr(W_BLK,*STAIRS_STEP))));c.raw(list(STAIRS_STEP))
c.label('texts');c.ref('','mu')
c.label('script');c.emit('c3 87 3c')
c.label('mu');c.emit('08');c.ref('21','t_mu');c.emit('cd 94 3c c3 04 25')
c.label('t_mu');c.raw(T_MU)
chamber=c.finish();assert 0x7600+len(chamber)<=0x7a00,len(chamber)
rom.put(fo(BANK,0x7600),chamber,'Bank 18: TOWER CHAMBER v21 (centre ring, statue triangle)')
old_hdr=w(0x1ae+2*NEW)
rom.data(0x1ae+2*NEW,bytes.fromhex(le(c.labels['header'])),'Map 0x69 header -> v21 chamber',le(old_hdr))
rom.finish('Creepy_Black_Mu_v21.gb','manifest_v21.json','CREEPY MU V21',
           extra=dict(labels={'chamber':{k:hex(v) for k,v in c.labels.items()}},new_blocks=[hex(x) for x in new_ids]))

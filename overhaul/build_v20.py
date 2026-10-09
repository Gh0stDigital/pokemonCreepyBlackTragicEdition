# Creepy Black Mu v20: the TOWER CHAMBER redrawn per walking tile so the circle has ONE centre tile (MR. MU on it).
# New 4x4-tile blocks go into the Tower blockset's unused slots (6E-AF; no map with tileset 0F uses them).
# Logged patches on top of verified Mu v19 (patchlib).
import json
from patchlib import *
from patchguard import fo
from altar_layout_v20 import steps,blocks,W_BLK,H_BLK,STAIRS_STEP,MU_STEP

V19_SHA='d072bc51443a85ebf0868a560157a99c34d923f6055c4943a6bc45eda354d990'
rom=Rom('Creepy_Black_Mu_v19.gb',V19_SHA)
r=rom.r
w=lambda o:r[o]|r[o+1]<<8
NEW=0x69;BANK=0x18;TOWER7=0x94;GENTLEMAN=0x10
BLOCKSET=fo(0x1b,0x45c0);FREE_IDS=range(0x6e,0xb0)
# blocks: reuse an existing Tower block when the 16 tiles match, else take a free slot
existing={bytes(r[BLOCKSET+16*b:BLOCKSET+16*b+16]):b for b in range(0x6e)}
used_by_maps=set()
for m in range(0xf8):
    bank=r[0xc23d+m];hp=w(0x1ae+2*m)
    if hp<0x4000 or bank==0:continue
    h=fo(bank,hp)
    if r[h]==0x0f:used_by_maps|=set(r[fo(bank,w(h+3)):fo(bank,w(h+3))+r[h+1]*r[h+2]])
assert not used_by_maps&set(FREE_IDS),sorted(used_by_maps&set(FREE_IDS))
B=blocks(steps());ids={};nxt=iter(FREE_IDS)
for row in B:
    for b in row:
        if b in existing:ids[b]=existing[b]
        elif b not in ids:
            i=next(nxt);ids[b]=i
            rom.data(BLOCKSET+16*i,b,'Tower blockset slot %02X: chamber block'%i,r[BLOCKSET+16*i:BLOCKSET+16*i+16])
grid=[[ids[b] for b in row] for row in B]
new_ids=sorted(v for v in ids.values() if v>=0x6e);print('new blocks',[hex(x) for x in new_ids])

def view_ptr(width,y,x):return 0xc6e8+7+width+(y//2)*(width+6)+x//2
T_MU=txt([["MR. MU: ..."],["So, you found","this place."],["Come closer,","child of the","GHOST..."]],end=0x57)
c=Code(BANK,0x7c00)
c.label('header');c.raw([0x0f,H_BLK,W_BLK]);c.ref('','blocks');c.ref('','texts');c.ref('','script');c.raw([0]);c.ref('','objects')
c.label('blocks');c.raw(bytes(b for row in grid for b in row))
c.label('objects');c.raw([0x11, 1, STAIRS_STEP[0],STAIRS_STEP[1],1,TOWER7, 0,
                          1, GENTLEMAN,MU_STEP[0]+4,MU_STEP[1]+4,0xff,0xd0,1])
c.raw(bytes.fromhex(le(view_ptr(W_BLK,*STAIRS_STEP))));c.raw(list(STAIRS_STEP))
c.label('texts');c.ref('','mu')
c.label('script');c.emit('c3 87 3c')
c.label('mu');c.emit('08');c.ref('21','t_mu');c.emit('cd 94 3c c3 04 25')
c.label('t_mu');c.raw(T_MU)
chamber=c.finish();assert 0x7c00+len(chamber)<=0x8000,len(chamber)
rom.put(fo(BANK,0x7c00),chamber,'Bank 18: TOWER CHAMBER v20 (12x12 blocks, one centre tile)')
old_hdr=w(0x1ae+2*NEW)
rom.data(0x1ae+2*NEW,bytes.fromhex(le(c.labels['header'])),'Map 0x69 header -> v20 chamber',le(old_hdr))
rom.finish('Creepy_Black_Mu_v20.gb','manifest_v20.json','CREEPY MU V20',
           extra=dict(labels={'chamber':{k:hex(v) for k,v in c.labels.items()}},new_blocks=[hex(x) for x in new_ids]))

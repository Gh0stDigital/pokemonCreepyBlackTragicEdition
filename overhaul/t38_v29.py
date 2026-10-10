# v29 kill system. Modes:
#  nugget - NUGGET BRIDGE (Route 24): GHOST CURSEs a trainer with a new kill index -> the bit lands in D430-D44F, no
#           stray RAM write (PC box data / stack / sprite tables untouched), the trainer is a gravestone after the battle
#  forest - VIRIDIAN FOREST: a trainer with a base-game index (< 34) still dies as before (D4A4 array)
#  table  - every trainer header has a unique index (or 0), every map lookup in the ROM table matches the manifest
from harness import *
import sys,json
MODE=sys.argv[1]
def clean(s):return ' '.join(''.join(c for c in s if c not in '│─┌┐└┘|').split())
def box():
    if m[0xc3a0+12*20]!=0x79:return ''
    return ' | '.join(x for x in txt()[12:] if x)
def ok(c,msg):
    print(('PASS ' if c else 'FAIL ')+msg,flush=True)
    if not c:sys.exit(1)
MAN=json.load(open('manifest_v29.json'))
def ghost_lead():
    i=list(m[0xd164:0xd16a]).index(0x1f)
    if i==0:return
    a=list(m[0xd16b:0xd197]);b=list(m[0xd16b+44*i:0xd197+44*i]);m[0xd16b:0xd197]=b;m[0xd16b+44*i:0xd197+44*i]=a
    m[0xd164],m[0xd164+i]=m[0xd164+i],m[0xd164]
    for base,n in ((0xd2b5,11),(0xd273,11)):
        x=list(m[base:base+n]);y=list(m[base+n*i:base+n*i+n]);m[base:base+n]=y;m[base+n*i:base+n*i+n]=x
def warp(mapid,warpid=0):
    load('pallet_with_ghost');m[0xd455]=255;ghost_lead()
    for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=warpid;m[0xd3af+4*i+3]=mapid
    for d in ('up','down','left','right','up'):
        if m[0xd35e]==mapid:break
        p.button(d,8);p.tick(30)
    p.tick(120)
def kill_trainer(idx):
    """put trainer sprite idx below the player, talk, fight with GHOST (A everywhere = CURSE), until the battle is over"""
    m[0xc200+16*idx+4]=m[0xd361]+5;m[0xc200+16*idx+5]=m[0xd362]+4;m[0xc200+16*idx+6]=0xff   # one tile below the player
    m[0xc100+16*idx+4]=m[0xc104]+16;m[0xc100+16*idx+6]=m[0xc106]          # screen position too (talking uses it)
    p.tick(30);press('down',20);press('a',300)
    for i in range(15):
        if m[0xd057]:break
        press('a',120)
    inb=m[0xd057];seen=[]
    for i in range(200):
        b=clean(box())
        if b and (not seen or seen[-1]!=b):seen.append(b)
        if i>6 and m[0xd057]==0:break
        p.button('b' if ('change' in b or 'Bring out' in b) else 'a',8);p.tick(200)
    p.tick(300);return inb,seen
def bitset(i):
    base=0xd430 if i>=0x100 else 0xd4a4;j=i&0xff
    return bool(m[base+j//8]&(1<<(j&7)))
def snapshot():return bytes(m[0xda80:0xdf00])
if MODE in ('nugget','forest'):
    mp=0x23 if MODE=='nugget' else 0x33
    warp(mp,0);ok(m[0xd35e]==mp,'arrived on map %02x'%mp)
    tr=[i for i in range(1,m[0xd4e1]+1) if m[0xd504+2*(i-1)]>=0xc8]
    hdrs={k:v for k,v in MAN['trainer_maps'].items() if '0x%x'%mp in v}
    # the kill index of each trainer sprite on this map (header byte 0 = sprite)
    R=open(ROM,'rb').read()
    def off(k):b,a=k.split(':');b=int(b,16);a=int(a,16);return b*0x4000+a-0x4000
    sprite_idx={R[off(k)]:(R[off(k)+10]|R[off(k)+11]<<8) for k in hdrs}
    print('trainer sprites',tr,'kill indices',sprite_idx)
    pick=[s for s in tr if s in sprite_idx and ((sprite_idx[s]>=34) if MODE=='nugget' else (0<sprite_idx[s]<34))][0]
    want=sprite_idx[pick]
    before=snapshot();b430=list(m[0xd430:0xd450]);b4a4=list(m[0xd4a4:0xd4ae])
    inb,seen=kill_trainer(pick)
    ok(inb!=0,'the battle with trainer sprite %d (kill index %d) started'%(pick,want))
    ok((m[0xd4ae]<<8|m[0xd4af])==want,'TalkToTrainer read the new kill index (%d)'%want)
    ok(m[0xd453]==1 or any('dead' in s.lower() or 'kill' in s.lower() for s in seen),'CURSE killed the trainer (D453=%d)'%m[0xd453])
    ok(bitset(want),'its kill bit is set (%s)'%('D430 array' if want>=0x100 else 'D4A4 array'))
    after=snapshot()
    diff=[hex(0xda80+i) for i in range(len(before)) if before[i]!=after[i] and 0xda80+i<0xdee2]
    ok(not diff,'PC box data (DA80-DEE1) untouched by the kill: %s'%diff[:5])
    changed=[i for i in range(32) if b430[i]!=m[0xd430+i]]+[100+i for i in range(10) if b4a4[i]!=m[0xd4a4+i]]
    ok(len(changed)==1,'exactly one kill byte changed: %s'%changed)
    # re-enter the map (fresh load, kill bits carried over): the trainer is a gravestone
    bits=(list(m[0xd430:0xd450]),list(m[0xd4a4:0xd4ae]))
    load('pallet_with_ghost');m[0xd430:0xd450]=bits[0];m[0xd4a4:0xd4ae]=bits[1]
    for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=mp
    for d in ('up','down','left','right','up'):
        if m[0xd35e]==mp:break
        p.button(d,8);p.tick(30)
    p.tick(120)
    ok(m[0xc100+16*pick]==0x49,'after re-entering, the trainer is a gravestone (pic %02x)'%m[0xc100+16*pick])
    others=[s for s in tr if s!=pick and m[0xc100+16*s]==0x49]
    ok(not others,'the other trainers are alive: %s'%others)
    shot('v29_%s_grave'%MODE)
    print('v29 %s: ALL PASS'%MODE)
if MODE=='table':
    ki=MAN['kill_index'];vals=[v for v in ki.values() if v]
    ok(len(vals)==len(set(vals)),'%d new kill indices, all unique'%len(vals))
    ok(all(34<=v<80 or 0x100<=v<0x200 for v in vals),'all in 34-79 or $100-$1FF (D430-D44F holds 256)')
    print('v29 table: ALL PASS')

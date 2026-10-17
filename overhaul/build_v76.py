# Creepy Black Mu v76: (1) no wild encounters on POKeMON TOWER 7F for anybody (v49 only removed them for BLACK); (2) the ritual room (TOWER CHAMBER, map 69):
#   the HELIX FOSSIL stands on the top (middle) stand, the DOME FOSSIL / PRETA on the left one, the OLD AMBER / AZHI on the right one (was: AMBER top, HELIX right).
#   The stands' texts, hiding and the awakened-cry logic follow the objects (text ids 2 AMBER / 3 DOME / 4 HELIX), so only the two objects' positions are swapped.
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V75_SHA='67c62e8ec2b1e23f1dcea1aa36d7ed1c2a8a98c58838b7d49e86d96b2ce8f11b'
rom=Rom('Creepy_Black_Mu_v75.gb',V75_SHA)
R=bytes(rom.r)
L49=json.load(open('manifest_v49.json'))['labels']['bank4']
tow49=int(L49['tow49'],16)
B4=0x7bc0
assert not any(R[fo(4,B4):fo(4,B4)+0x10])
c,L=asm(f'''
tow76:                           ; TryDoWildEncounter (4:78BC): POKeMON TOWER 7F (map 94): never an encounter, else v49's check
    ld a,[$d35e]
    cp $94
    jp nz,{tow49}
    pop af
    ld a,1                       ; "can't encounter" (TryDoWildEncounter's own exit, as tow49)
    and a
    ret
''',B4,{})
rom.put(fo(4,B4),c,'Bank 4: v76 no encounters on POKeMON TOWER 7F')
o=fo(4,0x78bc);assert R[o:o+3].hex()=='cd'+le(tow49)
rom.hook(o,'cd'+le(L['tow76']),'TryDoWildEncounter: 7F has none; else tow49','cd'+le(tow49),provides=('a','f'),reviewed='tow76 repeats tow49\'s exit and otherwise jumps to tow49, which ends in the replaced ld a,[wNPCMovementScriptPointerTableNum]')
# chamber objects (18:7D4C list): object 2 (OLD AMBER, y7 x11) <-> object 4 (HELIX FOSSIL, y15 x16)
o2=fo(0x18,0x7d4c);i=o2+2+4*R[o2+1]+1+0;assert R[o2+1]==1
nobj=R[i];i+=1
objs=[]
for k in range(nobj):
    objs.append(i);i+=6
a,h=objs[1],objs[3]
assert R[a:a+6].hex()=='3e0b0fffff02' and R[h:h+6].hex()=='3e1314ffff04',(R[a:a+6].hex(),R[h:h+6].hex())
rom.data(a+1,bytes([0x13,0x14]),'Chamber: OLD AMBER stand object -> the right stand (y15 x16)','0b0f')
rom.data(h+1,bytes([0x0b,0x0f]),'Chamber: HELIX FOSSIL stand object -> the top stand (y7 x11)','1314')
rom.finish('Creepy_Black_Mu_v76.gb','manifest_v76.json','CREEPY MU V76',extra=dict(labels=dict(bank4={k:hex(v) for k,v in L.items()})))

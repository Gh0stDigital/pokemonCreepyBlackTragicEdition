# v6: Mr. Mu in the Cerulean trade house. Warps from Pallet into map 3F by rewriting the lab door warp.
from harness import *
import sys
MODE=sys.argv[1] if len(sys.argv)>1 else 'main'
def enter_house(ghost=True):
    load('pallet_with_ghost');m[0xd455]=200
    if not ghost:m[0xd451]=0
    for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=0x3f
    seen=[]
    for i in range(6):
        if m[0xd35e]==0x3f:break
        p.button('up',8)
        for _ in range(24):
            p.tick();seen.append(m[0xc130])
    p.tick(90);return seen
def talk(choice=None,n=60):
    lines=[];empty=0
    p.button('a',8);p.tick(60)
    for i in range(n):
        b=box()
        if b and (not lines or lines[-1]!=b):lines.append(b)
        if 'ACCEPT IT' in b and choice:
            if choice=='defy':p.button('down',8);p.tick(20)
            p.button('a',8);p.tick(90);choice=None;continue
        if not b:
            empty+=1
            if empty>2:break
        else:empty=0
        p.button('a',8);p.tick(60)
    return lines
def bag():return [(m[0xd31e+2*i],m[0xd31f+2*i]) for i in range(m[0xd31d])]
def add_item(it,q=1):
    n=m[0xd31d];m[0xd31e+2*n]=it;m[0xd31f+2*n]=q;m[0xd320+2*n]=0xff;m[0xd31d]=n+1

if MODE=='hidden':
    seen=enter_house(ghost=False)
    print('map',pos(),'mu pic per frame after entering',sorted(set(seen[-24:])),'mu y/x',m[0xc234],m[0xc235])
    shot('v6_house_no_ghost')
    walk('up',2);t=talk()
    assert m[0xc130]==0 and m[0xd460]==0,'Mu visible without Ghost';print('PASS Mu hidden without Ghost',t);raise SystemExit
seen=enter_house()
print('map',pos(),'mu pic',hex(m[0xc130]),'sprite slots',[hex(m[0xc100+16*i]) for i in range(4)])
assert m[0xd35e]==0x3f and m[0xc130]!=0;walk('up',2);print('player',pos());shot('v6_house_mu')
t=talk();print('TEXT intro:',t);assert m[0xd460]==1 and any('SILPH' in x for x in t) and any('MT.MOON' in x for x in t);print('PASS intro')
t=talk();print('TEXT again:',t);assert any('still snooping' in x for x in t);print('PASS repeat warning')
add_item(0x29);print('bag',bag())
if MODE=='full':
    for i in range(m[0xd163],6):m[0xd163]+=1;m[0xd164+i]=m[0xd164];m[0xd164+i+1]=0xff
    t=talk('defy');print('TEXT full:',t);assert any('no' in x and 'room' in x for x in t) and (0x29,1) in bag() and m[0xd460]==1
    print('PASS full party keeps fossil');raise SystemExit
t=talk('accept');print('TEXT accept:',t);assert any('died so long ago' in x for x in t) and (0x29,1) in bag() and m[0xd460]==1;print('PASS accept')
shot('v6_question')
before=m[0xd163]
p.button('a',8);p.tick(60);lines=[];snd=set();black=0
for i in range(80):
    b=box()
    if b and (not lines or lines[-1]!=b):lines.append(b)
    if 'ACCEPT IT' in b:p.button('down',8);p.tick(20);p.button('a',8);p.tick(10);continue
    if m[0xd460]==2 and not b:break
    p.button('a',8)
    for _ in range(60):
        p.tick();snd.add(m[0xc026])
        if p.memory[0xff47]==0xff:black+=1
print('TEXT defy:',lines);print('sounds',[hex(x) for x in snd],'black frames',black)
i=m[0xd163]-1;s=0xd16b+44*i
st=list(m[s:s+44]);nick=''.join(cm.get(v,'?') for v in m[0xd2b5+11*i:0xd2b5+11*i+5]);ot=list(m[0xd273+11*i:0xd273+11*i+7])
print('party',list(m[0xd164:0xd16b]),'count',before,'->',m[0xd163],'nick',nick,'struct',st,'OT',ot,'player',list(m[0xd158:0xd15f]),'bag',bag())
assert m[0xd164+i]==0xb6 and nick=='PRETA' and st[33]==50 and st[8:12]==[0xa9,0x0f,0x39,0x46] and st[27:29]==[255,255] and (0x29,1) not in bag()
assert 0xe8 in snd and black>0 and st[12:14]==list(m[0xd359:0xd35b]) and ot==list(m[0xd158:0xd15f]);print('PASS Preta awakened')
t=talk();print('TEXT hint:',t);assert any('valuable' in x for x in t);print('PASS hint')
save('v6_with_preta')

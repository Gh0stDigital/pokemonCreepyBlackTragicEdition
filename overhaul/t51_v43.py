# v43: the black ball on the map looks like the battle-throw POKe BALL, blacked out. Modes:
#  look   - Pallet Town (outdoor sprite set): after the BANE the ball sprite uses a four-tile slot (0B/0C) that no other
#           sprite uses, that slot's VRAM holds the ball tiles; the other NPCs' graphics are unchanged; same after
#           leaving and coming back
#  indoor - a house NPC (BLUE's house, DAISY): the ball gets the ball tiles there too
import sys
MY51=sys.argv[1]
sys.argv=['x','none'];exec(open('t48_v40.py').read().split("if MODE=='bane':")[0]);MODE=MY51
import json
ROMB=open(os.environ['CB_ROM'],'rb').read()
SHEET=int(json.load(open('manifest_v40.json'))['labels']['bank2f']['sheet'],16)
BALL=list(ROMB[0x2f*0x4000+SHEET-0x4000:][:64])
def vram(a,n):return [p.memory[a+k] for k in range(n)]
def slot(i):return m[0xc20e+16*i]
def check_ball(b,where):
    s=slot(b);a={0x0b:0x8780,0x0c:0x87c0}.get(s)
    others=[i for i in range(1,16) if i!=b and m[0xc100+16*i] not in (0,0x47) and slot(i)==s]
    ok(a is not None and vram(a,64)==BALL,'%s: the ball uses four-tile slot %s holding the ball tiles'%(where,hex(s)))
    ok(not others,'%s: no other sprite uses that slot'%where)
if MODE=='look':
    start();ns=[n for n in npcs() if n[1] in (0xd,0x2f) and n[4]==0];b=ns[0][0];a=ns[1][0]
    sa=slot(a);g0=vram(0x8000+(sa-1)*0xc0,0xc0)
    bane(b);T(60)
    check_ball(b,'after the BANE')
    ok(vram(0x8000+(sa-1)*0xc0,0xc0)==g0 and slot(a)==sa,'the spared NPC keeps its graphics')
    go_map(0x25,0);go_map(0,0);T(60)
    check_ball(b,'after coming back')
    ok(vram(0x8000+(slot(a)-1)*0xc0,0xc0)==g0,'the spared NPC still has its graphics after coming back')
elif MODE=='indoor':
    warp(0x27,0,black=True);T(30);freeze()
    ns=[n for n in npcs() if n[4]==0 and m[0xc100+16*n[0]] not in (0,)];print('npcs',ns)
    b=ns[0][0];t=talk(b,answers=['yes']);T(60)
    if pic(b)!=0x47:print(t[-200:])
    ok(pic(b)==0x47 and pending(),'BLUE\'s house: the NPC became a black ball')
    check_ball(b,'indoors')

# v66: town shamaness fixes. Modes:
#  sets   - static: every outdoor map's pictures are in its sprite set(s), also the position-dependent routes (check_sets.py); no new violation vs v62
#  pallet - PALLET without GHOST: the old placeholder is gone, ONE shamaness stands on its old tile (y15 x8), her speech is the story only (no name / title),
#           once talked to she is gone the next time the map loads, nothing of her is left in the sprite table
import sys,subprocess
MODE=sys.argv[1]
def ok(c,msg):print(('PASS ' if c else 'FAIL ')+msg,flush=True)
if MODE=='sets':
    r=subprocess.run([sys.executable,'check_sets.py',__import__('os').environ.get('CB_ROM','Creepy_Black_Mu_v66.gb')],capture_output=True,text=True)
    print(r.stdout)
    ok(r.returncode==0,'no sprite set lost a picture a map needs; the channeler picture is in every shamaness town set');sys.exit(0)
sys.argv=['x','town','0']
src=open('t71_v63.py').read().split("if MY71=='nogh':")[0].replace("MY71=sys.argv[1];TOWN=int(sys.argv[2],0);BLK=len(sys.argv)>3","MY71='x';TOWN=0;BLK=False")
exec(src)
full=open('t71_v63.py').read();exec(full[full.index('from town_map import grid'):full.index('done=False')])
warp(DOOR[0],0,lambda:None);m[0xd365]=0;m[0xd451]=0
for i in range(10):
    if m[0xd35e]==0:break
    p.button('down',8);T(30)
T(120)
sp=sprites();print(sp,'D451',m[0xd451],flush=True)
chan=[x for x in sp if x[1]=='0x19']
ok(len(chan)==1 and chan[0][2:]==(15,8),'exactly one channeler in PALLET (no placeholder), standing on the old tile (y15 x8): %s'%chan)
ok(shaman() is not None,'she is the new shamaness (marker) and needs no GHOST')
ok(sp[4][1]=='0x0' and sp[4][2]==251,'object 5 (the old placeholder) is hidden')
s=shaman();sy,sx=s[2],s[3];done=False
for (dy,dx,face) in ((1,0,'up'),(-1,0,'down'),(0,-1,'right'),(0,1,'left')):
    try:
        if goto(sy+dy,sx+dx):done=True;break
    except AssertionError as e:print('goto',e,flush=True)
ok(done,'walked next to her')
press_(face,20);seen.clear();press_('a',200)
for i in range(30):
    if not box():break
    press_('a',120)
t=allt().replace("'","")
print('text:',t[:300],flush=True)
ok('Long before Kanto' in t and 'hear voices' in t and 'SHAMANESS' not in t and 'Ancient Clan' not in t,'the official lore 1 text, without name or title')
ok(not (m[0xd840]&1)==False,'talked flag set')
f0=m[0xd840]
warp(DOOR[0],0,lambda:None);m[0xd840]=f0;m[0xd451]=0;m[0xd365]=0
for i in range(10):
    if m[0xd35e]==0:break
    p.button('down',8);T(30)
T(120)
sp=sprites();print('after:',sp,flush=True)
ok(shaman() is None and not [x for x in sp if x[1]=='0x19'],'gone the next time PALLET loads')
n=m[0xd4e1]
ok(all(m[0xc100+16*i]==0 and m[0xc200+16*i+4] in (0,0xff) for i in range(n+1,16)) and all(m[0xd4e4+2*(n)+j]==0 for j in (0,1)),'nothing of her is left in the slots after the last sprite')
print('t74 done',flush=True)

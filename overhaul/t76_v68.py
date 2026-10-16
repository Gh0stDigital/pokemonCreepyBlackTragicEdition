# v68: MIRAGE chance grows with the victims (D45C): victims*164/256, capped at 64 (25%) from 100 victims on; none as BLACK (D46C)
import sys,random
sys.argv=['x','none']
src=open('t28_v14.py').read().split("if MODE=='mirage_rate':")[0].replace("MODE=sys.argv[1]","MODE='x'")
exec(src)
def ok(c,msg):print(('PASS ' if c else 'FAIL ')+msg,flush=True)
ent=[];chance=[]
p.hook_register(0x2e,0x4280,lambda c:ent.append(1),None)
p.hook_register(0x2e,0x4326,lambda c:chance.append(p.register_file.A),None)
CASES=[(1,0,0),(2,0,1),(10,0,6),(50,0,32),(99,0,63),(100,0,64),(255,0,64),(0,0,None),(100,1,None)]
for uses,black,want in CASES:
    ent.clear();chance.clear()
    load('pallet_with_ghost');m[0xd455]=255;m[0xd45c]=uses;m[0xd46c]=black;random.seed(uses+black)
    to_route1();assert m[0xd35e]==0xc,pos()
    for step in range(2500):
        if ent:break
        walk(random.choice(['up','down','left','right']),1)
    p.tick(30)
    if want is None:
        # no victims yet / BLACK: m68 returns before the roll
        ok(not chance and bool(ent),'victims %d black %d: no Mirage roll (entered m68: %s)'%(uses,black,bool(ent)))
    else:
        ok(bool(chance) and chance[0]==want,'victims %d: chance %s/256 (wanted %d)'%(uses,chance[:1],want))
print('t76 done',flush=True)

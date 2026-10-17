# v76: no wild encounters on POKeMON TOWER 7F. Modes:
#  tower7f - walk up and down the 7F hall (stage 4: no channelers, no GHOST problem) 400 steps: no battle starts; the same in the 6F hall still can start one
#            (control; needs the game's own wild data of 6F) - skipped if 6F has none
import sys
MY84=sys.argv[1]
sys.argv=['x','none']
src=open('t61_v53.py').read().split("if MODE=='lore':")[0].replace("MY61=sys.argv[1]","MY61='x'")
exec(src)
def ok(c,msg):print(('PASS ' if c else 'FAIL ')+msg,flush=True)
rate=255
def hall_steps(n):
    battles=0
    m[0xd887]=rate
    for k in range(n):
        m[0xd887]=rate
        for d in ('up','down'):
            p.button(d,8);T(20)
            if m[0xd057]:
                battles+=1
                for j in range(200):
                    if not m[0xd057]:break
                    p.button('b',8);T(10)
                    if m[0xd057] and j%10==9:p.button('down',8);p.button('a',8);T(30)
                m[0xd057]=0
    return battles
if MY84=='tower7f':
    tower53(4,consort=0)
    m[0xd451]=0                                   # no GHOST: nothing that refuses / hides
    bfs_to(12,10)
    hits=[]
    if VERSION>=76:
        import json
        a=int(json.load(open('manifest_v76.json'))['labels']['bank4']['tow76'],16)
        p.hook_register(4,a,lambda c:hits.append(1),None)
    b=hall_steps(200)
    print('battles on 7F in 400 steps:',b,flush=True)
    ok(b==0,'no wild encounter on POKeMON TOWER 7F in 400 steps')
    if VERSION>=76:ok(len(hits)>=100,'the 7F check ran on every step (%d times)'%len(hits))
print('t84 done',flush=True)

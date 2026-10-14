# v54: MOM among the channelers after the ritual. Modes:
#  mom    - RIT 6 (BLACK), stage 5: the channelers still stand in the hall, MOM (picture 33) at (9,9); her first talk is the
#           long confession, the second the short one (consort's duty); not after the ritual (RIT 0): no MOM, channelers as v53
import sys
MY62=sys.argv[1]
sys.argv=['x','none'];exec(open('t61_v53.py').read().split("if MODE=='lore':")[0].replace("load('pallet_with_ghost');","load('pallet_with_ghost');m[0xd46f]=3;m[0xd46c]=1 if rit==6 else 0;"));MODE=MY62
def mom_sprites():return {i:v for i,v in sprites().items() if v[0]==0x33}
if MODE=='mom':
    tower53(5,bits=0x18,rit=6)
    ok(len(chs())==0 and not mom_sprites(),'at the entrance nobody is drawn yet')
    bfs_to(9,10);T(40)
    ms=mom_sprites();print('mom',ms,'channelers',len(chs()))
    ok(len(ms)==1 and list(ms.values())[0][1:3]==(9,9),'MOM stands at (9,9) among the channelers')
    ok(len(chs())>=4,'the channelers stand there too (%d drawn)'%len(chs()))
    shot('v54_mom')
    t=talk_at(9,10,'left',n=80);print(t[-120:])
    ok("not really your" in t.replace('  ',' ') or 'Hello, honey' in t,'first talk: the confession')
    for b in range(40):
        if box():press_('a',60)
    T(60)
    ok(m[0xd466]&0x80,'flag set')
    t=talk_at(9,10,'left',n=80);print(t[-120:])
    ok("consort" in t.replace('  ',' ') or 'heal you' in t,'second talk: "that\'s your consort\'s duty now"')
    seen_t=set()
    ok(m[0xc190]!=0x33,'(slot 9 is AGATHA again, not MOM)')
    tower53(5,bits=0x18,rit=0);bfs_to(9,10);T(40)
    ok(not mom_sprites(),'before the ritual: no MOM')

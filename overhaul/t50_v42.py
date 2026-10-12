# v42: a BANEd NPC (black POKe BALL) can't move. Modes (Pallet Town as BLACK; t48's helpers):
#  still  - BANE a wandering NPC, let every NPC walk again (WALK restored): after ~25 s the ball is on the same tile with
#           movement byte STAY, while a spared wandering NPC still walks (normal case)
#  reload - leave the map before picking the ball up and come back: the ball keeps its tile (STAY) for ~25 s, and can
#           still be picked up
import sys
MY50=sys.argv[1]
sys.argv=['x','none'];exec(open('t48_v40.py').read().split("if MODE=='bane':")[0]);MODE=MY50
def tile(i):return (m[0xc204+16*i],m[0xc205+16*i])
def mv(i):return m[0xc206+16*i]
def unfreeze(ids):
    for i in ids:m[0xc206+16*i]=0xfe
def watch(ids,frames=1500):
    seen_t={i:{tile(i)} for i in ids}
    for k in range(frames//10):
        T(10)
        for i in ids:seen_t[i].add(tile(i))
    return seen_t
if MODE=='still':
    load('pallet_with_ghost');m[0xd46c]=1;m[0xd455]=255;T(30)
    walkers=[i for i in range(1,m[0xd4e1]+1) if mv(i)==0xfe];print('wandering NPCs',walkers)
    freeze()
    ns=[n for n in npcs() if n[1] in (0xd,0x2f) and n[4]==0 and n[0] in walkers];b=ns[0][0];a=[i for i in walkers if i!=b][0]
    bane(b);t0=tile(b)
    ok(pic(b)==0x47 and pending(),'NPC %d BANEd: a black ball waits'%b)
    unfreeze(walkers)                                    # as in the real game: nobody was frozen
    st=watch([b])
    print('ball',sorted(st[b]),'mv',hex(mv(b)))
    ok(st[b]=={t0} and mv(b)==0xff and drawn(b),'the black ball stays on its tile (movement STAY) for ~25 s')
    freeze();spot(a);unfreeze([a])                      # normal case: on screen, a spared wandering NPC
    st=watch([a]);print('spared',a,sorted(st[a]))
    ok(len(st[a])>1 and mv(a)==0xfe,'a spared wandering NPC still walks around (%d tiles)'%len(st[a]))
elif MODE=='reload':
    load('pallet_with_ghost');m[0xd46c]=1;m[0xd455]=255;T(30)
    walkers=[i for i in range(1,m[0xd4e1]+1) if mv(i)==0xfe]
    freeze()
    ns=[n for n in npcs() if n[1] in (0xd,0x2f) and n[4]==0 and n[0] in walkers];b=ns[0][0];p0=party()
    bane(b);sp=pending()[0][2]
    go_map(0x25,0);go_map(0,0);T(5);t0=tile(b)
    print('after reload: mv',hex(mv(b)),'tile',t0,'pic',hex(pic(b)))
    st=watch([b])
    ok(st[b]=={t0} and mv(b)==0xff and pic(b)==0x47,'after leaving and coming back the ball stays on its tile (STAY) for ~25 s')
    freeze();t=talk(b);T(60)
    ok(party()==p0+[sp] and not pending(),'and can still be picked up (%s joins)'%hex(sp))

# Party is only Ghost: Ghost goes to the PC, the player is sent out first; escape restores Ghost.
from harness import *
load('mirage_battle_start_only_ghost')
print('party',list(m[0xd164:0xd168]),'count',m[0xd163],'box',m[0xda80],list(m[0xda81:0xda83]))
assert m[0xd163]==1 and m[0xd164]==0x79 and m[0xda81]==0x1f
seen=[]
for i in range(40):
    b=box()
    if b and (not seen or seen[-1]!=b):seen.append(b)
    if 'FIGHT' in b and m[0xd014]==0x79:break
    p.button('a',8);p.tick(160)
shot('only_ghost_player_out')
print([''.join(c for c in s if c not in '│─┌┐└┘|').strip() for s in seen][-3:])
assert m[0xd014]==0x79;print('PASS only-Ghost party: player sent out as himself')
for attempt in range(12):
    st=io=None
    with open(qa/'og.state','wb') as f:p.save_state(f)
    p.tick(attempt*5);p.button('down',8);p.tick(10);p.button('right',8);p.tick(10);p.button('a',8)
    esc=False;black=0
    for i in range(1500):
        p.tick(1)
        if m[0xff47]==0xff:black+=1
        if i%60==30 and box():p.button('a',8)
        if 'Got away' in ''.join(txt()):esc=True
        if m[0xd057]==0 and i>200:break
    if esc:
        for k in range(8):p.button('a',8);p.tick(100)
        walk('up',1);walk('down',1)
        print('escaped; party',list(m[0xd164:0xd167]),'count',m[0xd163],'box',m[0xda80],'flags',m[0xd45d],m[0xd45f])
        assert m[0xd163]==1 and m[0xd164]==0x1f and m[0xda80]==0 and m[0xd45d]==0;print('PASS Ghost restored to party after escape');break
    print('attempt',attempt,'caught (black',black,') - retrying from saved point')
    with open(qa/'og.state','rb') as f:p.load_state(f)

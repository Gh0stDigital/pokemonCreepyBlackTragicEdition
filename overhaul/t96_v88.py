# v88: PROF. OAK's end. Modes: oak (the scene draws the picture with the LCD off and puts it on again; "The MOON STONE shatters!" once through the battle end),
#      lorelei (control: one "shatters" for a normal League battle)
import sys
MY96=sys.argv[1]
sys.argv=['x','none'];exec(open('t52_v44.py').read().split("if MODE=='block':")[0]);MODE=MY96
def setup():
    make_black();lead(CHAR);strong(0)
    b=0xd16b+44;m[b+9]=0x0a;m[b+30]=35
    m[0xd867]|=2;m[0xd876]=6
if MODE=='oak':
    warp(0xe3,0,setup)
    ok(m[0xffd7]==1,'the cave animates its water tile before the scene (hTileAnimations = %d)'%m[0xffd7])
    m[0xd877]=0x10;seen.clear()
    snaps=[]
    for i in range(80):
        T(6)
        if m[0xd877]==0x10 and m[0xcd6b]==255 and m[0xff47] in (0x54,0xa8,0xfc,0xf8,0xf4,0xe4):snaps.append(bytes(p.memory[0x9000:0x9310]))
        if box() and i>20:break
    ok(len(snaps)>5 and all(s==snaps[0] for s in snaps),"OAK's picture tiles in VRAM never change during the scene (%d samples)"%len(snaps))
    ok(m[0xffd7]==0,'tile animations are off during the scene')
    for i in range(400):
        if m[0xd057] or m[0xd877]==0x11:break
        if box():press_('a',80)
        else:T(20)
    for i in range(60):
        if m[0xd057] and m[0xd89c]:break
        press_('a',100)
    T(100);m[0xd89c]=1;wait_menu()
    menu('fight');m[0xcc26]=1;T(4);seen.clear();p.button('a',8)
    for k in range(2500):
        p.tick()
        if k%4==0:T(1)
        if m[0xd05a]==3 and 'FIGHT' in clean(' '.join(txt())):break
        if k%90==0:p.button('a',8)
    seen.clear();use_move(0,300,in_moves=True)
    for i in range(30):
        if m[0xd057]==0:break
        press_('a',100)
    for i in range(10):press_('a',40)
    T(60)
    t=allt()
    print('shatters in the end:',t.count('shatters'),flush=True)
    ok(t.count('shatters')==0,'"The MOON STONE shatters!" is not printed a second time after the kill (%d)'%t.count('shatters'))
    for i in range(80):
        if m[0xd876]==7:break
        press_('a',40)
    ok(m[0xd876]==7,'D876 = 7: the end')
    T(400)
    oam=[(p.memory[0xfe00+4*k],p.memory[0xfe00+4*k+1]) for k in range(40)]
    vis=[o for o in oam if 0<o[0]<160 and 0<o[1]<168]
    ok(not vis,'no sprite over the credits (visible OAM entries: %s)'%vis)
    ok(m[0xff40]&0x80,'the LCD is on during the credits')
elif MODE=='lorelei':
    def setup2():
        make_black();lead(CHAR);strong(0)
        b=0xd16b+44;m[b+9]=0x0a;m[b+30]=35
    to_battle(0xf5,3,5,setup2,one=True)
    menu('fight');m[0xcc26]=1;T(4);seen.clear();p.button('a',8)
    for k in range(2500):
        p.tick()
        if k%4==0:T(1)
        if m[0xd05a]==3 and 'FIGHT' in clean(' '.join(txt())):break
        if k%90==0:p.button('a',8)
    seen.clear();use_move(0,300,in_moves=True)
    for i in range(30):
        if m[0xd057]==0:break
        press_('a',100)
    T(100)
    t=allt()
    ok(t.count('shatters')==0,'no second "shatters" after the BANE kill of LORELEI (%d)'%t.count('shatters'))

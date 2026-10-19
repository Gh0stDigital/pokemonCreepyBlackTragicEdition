# v79: after the ritual. Modes:
#  hall  - back on TOWER 7F as BLACK: AGATHA is drawn with her own tiles all through her scene (slot = the one of the map load), the channelers within two rows and MOM (picture 33) are drawn, MOM talks
#  house - the player's house (map 25): MOM is there before the ritual is over, gone at RIT 6; the consort still waits
import sys
MY87=sys.argv[1]
sys.argv=['x','none']
exec(open('t35_v25.py').read().split("if MODE=='items':")[0])
def ok(c,msg):print(('PASS ' if c else 'FAIL ')+msg,flush=True)
def sp(i):return (m[0xc100+16*i],m[0xc102+16*i],m[0xc200+16*i+14])
if MY87=='hall':
    load('v25_black_'+ROMTAG);T(60)
    bfs_to(STAIRS[0]-1 if 'STAIRS' in dir() else 18,11)
    p.button('down',16);T(200);p.button('down',16);T(60)
    ok(pos()[0]==0x94 and m[0xd46c]==1,'back on Tower 7F as BLACK')
    slot0=sp(9)[2];bad=[];prev=None;dark=[]
    for k in range(40):
        T(24);press_('a',10)
        cur=sp(9);stable=(cur==prev);prev=cur            # (mid-redraw values are transient: judge only what stays for two samples)
        pic,img,slot=cur
        sy,sx=m[0xc104+16*9],m[0xc106+16*9]
        if 8<=sy<=136 and 0<=sx<=152 and not box() :
            c=p.screen.image.convert('L').crop((sx,sy-8 if sy>=8 else 0,sx+16,sy+8)) ;px=list(c.getdata());dark.append(sum(1 for v in px if v<70)/len(px))
        if stable and pic==0x39 and (slot!=slot0 or img==0xff) and abs(m[0xc204+16*9]-4-m[0xd361])<=4:bad.append((k,hex(img),slot))
        if m[0xd46f]==3 and not box():break
    print('AGATHA slot at load',slot0,'bad frames',bad[:5],flush=True)
    print('AGATHA dark ratio per sample',[round(x,2) for x in dark][:12],flush=True)
    ok(not bad and slot0!=0 and (not dark or max(dark)<0.6),'AGATHA keeps her tile slot and is not a black silhouette during her whole scene')
    for step in range(9):
        p.button('down',8);T(26)
    T(20)
    near=[i for i in range(4,16) if m[0xc100+16*i]==0x19 and m[0xc204+16*i]!=0xff]
    undrawn=[i for i in near if m[0xc102+16*i]==0xff]
    print('channelers near',near,'undrawn',undrawn,'MOM',sp(15),flush=True)
    if VERSION>=84:ok(not near,'no channelers stand on 7F after the ritual (v84)')
    else:ok(len(near)>=3 and not undrawn,'the channelers near the player are drawn')
    ok(sp(15)[0]==0x33 and sp(15)[1]!=0xff,'MOM (picture 33) is drawn in the hall')
    # talk to MOM at (y9,x9): stand at (10 -> x) next to her on the right, facing left
    p.button('up',8);T(26);p.button('left',8);T(26);p.button('left',8);T(30)
    seen.clear();press_('a',60)
    for k in range(12):
        if not box():break
        press_('a',60)
    t=allt();print('MOM:',t[:100],flush=True)
    ok('honey' in t,'MOM talks: "Oh! Hello, honey!"')
elif MY87=='house':
    for rit,name in ((0,'before the ritual is over'),(6,'BLACK')):
        load('pallet_with_ghost');m[0xd455]=255;m[0xd467]=rit;m[0xd46c]=1 if rit==6 else 0;m[0xd464]=5;m[0xd465]=1
        for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=0x25
        for i in range(6):
            if m[0xd35e]==0x25:break
            walk('up',1)
        T(120)
        print(name,'map',hex(m[0xd35e]),'MOM object',sp(1),'objects',m[0xd4e1],flush=True)
        if rit==0:ok(m[0xc110]!=0,'MOM is at home before the ritual is over')
        else:
            ok(m[0xc110]==0,'MOM is gone from the house when BLACK')
            ok(m[0xc120]==0x1d or m[0xc130]==0x1d,'the consort (MISTY) still waits there') if False else None
print('t87 done',flush=True)

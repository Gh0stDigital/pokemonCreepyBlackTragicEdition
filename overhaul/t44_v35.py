# v35: a killed trainer vanishes from the map right after the battle (like the early-route trainers always did), then is
# a gravestone when the map is entered again. Mode: vanish MAP  (23 NUGGET BRIDGE, 41 CERULEAN GYM, 33 VIRIDIAN FOREST)
import sys
MY=sys.argv[1];ARG=sys.argv[2] if len(sys.argv)>2 else ''
sys.argv=[sys.argv[0],'none']
exec(open('t38_v29.py').read().split("if MODE in ('nugget','forest'):")[0])
if MY=='vanish':
    mp=int(ARG,16);warp(mp,0);ok(m[0xd35e]==mp,'arrived on map %02x'%mp)
    if mp==0x41:walk('up',3)
    tr=[i for i in range(1,m[0xd4e1]+1) if m[0xd504+2*(i-1)]>=0xc8]
    pick=tr[1] if mp in (0x23,0x41) else tr[0]
    inb,seen=kill_trainer(pick)
    idx=(m[0xd4ae]<<8)|m[0xd4af]
    ok(inb!=0 and bitset(idx),'trainer sprite %d killed (kill index %d)'%(pick,idx))
    p.tick(60);shot('v35_vanish_%02x'%mp)
    ok(m[0xd35e]==mp,'still on the same map')
    ok(m[0xc102+16*pick]==0xff,'the killed trainer vanished right after the battle (image %02x, pic %02x)'%(m[0xc102+16*pick],m[0xc100+16*pick]))
    # a living trainer next to the player is still drawn
    other=[i for i in tr if i!=pick][0]
    m[0xc200+16*other+4]=m[0xd361]+4;m[0xc200+16*other+5]=m[0xd362]+4+1;m[0xc200+16*other+6]=0xff
    m[0xc100+16*other+4]=m[0xc104];m[0xc100+16*other+6]=m[0xc106]+16
    p.tick(30)
    ok(m[0xc102+16*other]!=0xff,'a living trainer standing next to the player is still drawn (image %02x)'%m[0xc102+16*other])
    bits=(list(m[0xd430:0xd450]),list(m[0xd4a4:0xd4ae]))
    load('pallet_with_ghost');m[0xd430:0xd450]=bits[0];m[0xd4a4:0xd4ae]=bits[1]
    for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=mp
    for d in ('up','down','left','right','up'):
        if m[0xd35e]==mp:break
        p.button(d,8);p.tick(30)
    p.tick(120)
    ok(m[0xc100+16*pick]==0x49,'after re-entering it is a gravestone (pic %02x)'%m[0xc100+16*pick])
    print('v35 vanish %02x: ALL PASS'%mp)

# v34. Modes:
#  instant MAP - curse-kill a trainer on MAP (23 = NUGGET BRIDGE, 41 = CERULEAN GYM, 33 = VIRIDIAN FOREST): it is a
#                gravestone right after the battle, without leaving the map; the other trainers are untouched
#  bridge      - the real CERULEAN flow: BLUE north of town, then up NUGGET BRIDGE (trainers spot you), CURSE each:
#                the Rocket at the end gets his own kill index ($1FD) instead of the previous trainer's
#  wild        - a wild battle (no kill) leaves every sprite as it was
import sys
MY=sys.argv[1];ARG=sys.argv[2] if len(sys.argv)>2 else ''
sys.argv=[sys.argv[0],'none']
exec(open('t38_v29.py').read().split("if MODE in ('nugget','forest'):")[0])
if MY=='instant':
    mp=int(ARG,16);warp(mp,0);ok(m[0xd35e]==mp,'arrived on map %02x'%mp)
    tr=[i for i in range(1,m[0xd4e1]+1) if m[0xd504+2*(i-1)]>=0xc8]
    MAN34=json.load(open('manifest_v34.json'));R=open(ROM,'rb').read()
    pick=tr[1] if mp in (0x23,0x41) else tr[0]                 # (Cerulean Gym: sprite 1 is MISTY, take a gym trainer)
    if mp==0x41:walk('up',3)                                  # off the door row: the trainer is put below the player
    before={i:m[0xc100+16*i] for i in tr}
    inb,seen=kill_trainer(pick)
    ok(inb!=0,'battle with trainer sprite %d (kill index %d)'%(pick,(m[0xd4ae]<<8)|m[0xd4af]))
    p.tick(60);shot('v34_instant_%02x'%mp)
    ok(m[0xd35e]==mp,'still on the same map (no re-entry)')
    ok(m[0xc100+16*pick]==0x49,'the killed trainer is a gravestone right after the battle (pic %02x)'%m[0xc100+16*pick])
    others=[i for i in tr if i!=pick and m[0xc100+16*i]!=before[i]]
    ok(not others,'the other trainers are unchanged: %s'%others)
    print('v34 instant %02x: ALL PASS'%mp)

# v75: POKeMON TOWER 7F channelers after a menu redraw. Modes:
#  tower - stage 5: record the channeler tile slot right after the map load; open + close the START menu (twice) at the entrance (no channeler drawn then),
#          walk up the hall: every channeler near the player is drawn (image index <> FF) with the SAME slot as at the load (its tiles are the ones in VRAM),
#          AGATHA and the girl keep their load slots; at stage 4 / ritual done nothing changed
import sys
MY83=sys.argv[1]
sys.argv=['x','none']
src=open('t61_v53.py').read().split("if MODE=='lore':")[0].replace("MY61=sys.argv[1]","MY61='x'")
exec(src)
def ok(c,msg):print(('PASS ' if c else 'FAIL ')+msg,flush=True)
def slot(i):return m[0xc200+16*i+14]
if MY83=='tower':
    tower53(5)
    load_slots={i:slot(i) for i in (4,5,6,9,10,11,15)}
    print('slots at the load',load_slots,flush=True)
    for n in range(2):
        p.button('start',8);T(40);p.button('b',8);T(60)
    ok(slot(10)==load_slots[10] and slot(5)==load_slots[5] and slot(6)==load_slots[6],'after the menu: channeler / AGATHA / girl slots are the load slots')
    bad=[]
    for y in (12,10,8,6):
        bfs_to(y,10);T(40)
        shown=[i for i in range(4,16) if m[0xc100+16*i]==0x19 and m[0xc204+16*i]!=0xff]
        undrawn=[i for i in shown if m[0xc102+16*i]==0xff]
        wrong=[i for i in shown if slot(i)!=load_slots[10]]
        print('y',y,'channelers near',shown,'not drawn',undrawn,'wrong slot',wrong,flush=True)
        ok(len(shown)>=2 and not undrawn and not wrong,'row %d: the channelers within two steps are drawn with the channeler tiles'%y)
        if y==6:ok(m[0xc102+16*5]!=0xff and slot(5)==load_slots[5],'AGATHA drawn with her own slot')
    for st,rit,name in ((4,0,'stage 4'),(5,6,'ritual done')):
        tower53(st,rit=rit);p.button('start',8);T(40);p.button('b',8);T(60)
        ok(not any(m[0xc100+16*i]==0x19 for i in range(4,16)),'%s: no channelers after a menu'%name)
print('t83 done',flush=True)

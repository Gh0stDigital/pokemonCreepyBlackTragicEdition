# v106: TEAM ROCKET route part 1 (PEWTER MUSEUM ROCKET, contract on BROCK). Modes:
#  vis      - no kill yet: no ROCKET in MUSEUM 1F; a trainer killed: he stands at (1,3) facing the exhibit; as BLACK: not there
#  flow     - first talk: annoyed, "eyes of a killer", the joke, the contract (D84A = 1); again: the reminder; BROCK dead: his pay
#             (money +10000, jingle text), the TEAM ROCKET invitation / CERULEAN test (D84A = 2); again: "take the test"; after leaving and
#             coming back he is gone (D84A = 3)
#  already  - BROCK already dead at the first talk: no contract, "already dead", paid at once
#  npcs     - the museum's other people (objects 2-4): their talk, compared between v105 and v106
#  witness  - BROCK killed with CURSE under contract, his gym trainer alive: NOTORIETY +5; control: the trainer was killed first -> +0;
#             control: no contract -> +0
import sys
MY=sys.argv[1]
sys.argv=['x','none'];exec(open('t28_v14.py').read().split("if MODE=='mirage_rate':")[0].replace("MODE=sys.argv[1]","MODE='x'"))
def ok(c,msg):print(('PASS ' if c else 'FAIL ')+msg,flush=True)
CHAR=0xb0;ST=0xd84a
def rk():return (m[0xc160],m[0xc264]-4,m[0xc265]-4)
def to_museum(setup):
    load('pallet_with_ghost');lead(0x1f);m[0xd16b+29]=0x3f;m[0xd455]=255
    setup()
    for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=0x34
    for i in range(6):
        if m[0xd35e]==0x34:break
        walk('up',1)
    T(120);m[0xd887]=0
def talk(n=60):
    y,x=m[0xd361],m[0xd362]
    m[0xc264]=y-1+4;m[0xc265]=x+4;m[0xc266]=0xff
    T(10);p.button('up',8);T(20);seen.clear()
    for k in range(n):
        if not box() and k>10:break
        press_('a',70)
    return allt().replace("'","").replace('  ',' ')
def money():return int(bytes(m[0xd347:0xd34a]).hex())
def killsome():m[0xd430]|=1                      # some trainer of the v29 range is dead
if MY=='vis':
    to_museum(lambda:None);print('no kill:',rk(),flush=True)
    ok(rk()[0]==0,'no trainer killed yet: no ROCKET in the museum')
    to_museum(killsome);print('kill:',rk(),flush=True)
    ok(rk()==(0x18,1,3),'a trainer was killed: the ROCKET stands at the top exhibit (1,3)')
    p.screen.image.resize((480,432),0).save('qa/v106_rocket_museum.png')
    to_museum(lambda:(killsome(),m.__setitem__(0xd46c,1)))
    ok(rk()[0]==0,'as BLACK: no ROCKET')
elif MY=='flow':
    to_museum(killsome);m0=money()
    t=talk();print('1:',t[-300:],flush=True)
    keys=['staring at','good look','eyes of a killer','whispering','killing #MON'.replace('#','POKé'),'Just kidding','real target','PEWTER GYM leader','pay you well','how you do it','witnesses','get caught']
    print([k for k in keys if k not in t])
    ok(all(k in t for k in keys) and m[ST]&15==1,'first talk: annoyed, eyes of a killer, the joke, the contract (state 1)')
    t=talk();print('2:',t[-120:],flush=True)
    ok('still breathing' in t and m[ST]&15==1 and money()==m0,'again: the reminder, no pay')
    m[0xd4a5]|=0x10
    t=talk();print('3:',t[-400:],flush=True)
    keys=['heard the news','Clean work','received','10000','I like you','TEAM ROCKET','CERULEAN','take the test']
    print([k for k in keys if k not in t])
    ok(all(k in t for k in keys),'BROCK dead: the pay, "received ¥10000!", the invitation to the test in CERULEAN')
    ok(money()==m0+10000 and m[ST]&15==2,'money +10000 (%d -> %d), state 2'%(m0,money()))
    t=talk();ok('waiting for' in t and money()==m0+10000,'again: "take the test", no second pay')
    s=m[ST]
    to_museum(lambda:(killsome(),m.__setitem__(0xd4a5,m[0xd4a5]|0x10),m.__setitem__(ST,s)))
    print('state',m[ST],'rk',rk(),flush=True)
    ok(m[ST]&15==3 and rk()[0]==0,'after leaving: he is gone (state 3)')
elif MY=='already':
    to_museum(lambda:(killsome(),m.__setitem__(0xd4a5,m[0xd4a5]|0x10)));m0=money()
    t=talk();print(t[-300:],flush=True)
    ok('eyes of a killer' in t and 'already dead' in t and 'real target' not in t,'BROCK already dead: no contract, "already dead"')
    ok(money()==m0+10000 and m[ST]&15==2 and 'TEAM ROCKET' in t,'paid at once (+10000) and invited (state 2)')
elif MY=='witness':
    def strong(i):
        b=0xd16b+44*i
        m[b+14]=0x10;m[b+15]=0x2c;m[b+16]=0x14;m[b+33]=100;m[b+3]=100;m[b+1]=3;m[b+2]=0xe7;m[b+34]=3;m[b+35]=0xe7
        for j in range(4):m[b+36+2*j]=3;m[b+37+2*j]=0xe7
    for case,pre,want in (('trainer alive',lambda:m.__setitem__(ST,1),5),('trainer already dead',lambda:(m.__setitem__(ST,1),m.__setitem__(0xd4a5,m[0xd4a5]|0x20)),0),
                          ('no contract',lambda:None,0)):
        warp_from_pallet(0x36,0);m[0xd887]=0;pre();n0=m[0xd85c]
        m[0xd755]|=0x04
        walk_to(2,4);p.button('up',8);T(20);seen.clear()
        for i in range(30):
            if m[0xd057]:break
            press_('a',60)
        m[0xd755]&=~0x04
        ok(m[0xd057]==2 and m[0xd031]==34,'%s: BROCK battle'%case)
        fight(spare=False)                                   # t28: GHOST CURSEs, CURSE again in the trainer phase (kill)
        for i in range(40):press_('a',90)
        T(60)
        print(case,'brock dead',bool(m[0xd4a5]&0x10),'notor',n0,'->',m[0xd85c],'state',hex(m[ST]),flush=True)
        ok(m[0xd4a5]&0x10 and m[0xd85c]==n0+want,'%s: BROCK killed, NOTORIETY +%d'%(case,want))
elif MY=='npcs':                                  # control: the museum's own people say what they said before (run on v105 and v106, compare)
    for i in (2,3,4):
        to_museum(killsome)
        y,x=m[0xd361],m[0xd362];m[0xc204+16*i]=y-1+4;m[0xc205+16*i]=x+4;m[0xc206+16*i]=0xff
        T(10);p.button('up',8);T(20);seen.clear()
        for k in range(30):
            if not box() and k>10:break
            press_('a',70)
        print('NPC',i,'|',allt()[-160:],flush=True)
print('t107 done',flush=True)

# v89: ROUTE 22's first rival fight (BLUE, opponent E1). Modes:
#  curse  - GHOST CURSEs: GHOST hesitates, "BLUE ran away!", shock mode (D463 = 1, Cerulean skipped, S.S. ANNE script 4, the 2nd ROUTE 22 fight off), then the SHOCK speech
#  win    - a normal win (CHARMANDER): the original after-battle speech ("... quit dawdling ..."), no shock
import sys,re
MY97=sys.argv[1]
sys.argv=['x','none'];exec(open('t52_v44.py').read().split("if MODE=='block':")[0]);MODE=MY97
def fin(master):
    out=[]
    for i,x in enumerate(master):
        if i+1<len(master) and len(master[i+1])>len(x) and master[i+1].startswith(x.rstrip('▼ ')):continue
        out.append(x)
    return ' | '.join(out)
def setup():
    m[0xd7eb]|=0x81
    if MODE=='curse':lead(GHOST);m[0xd16b+29]=0x3f;m[0xd455]=255
    else:lead(CHAR);strong(0)
import json
L14={k:int(v,16) for k,v in json.load(open('manifest_v89.json'))['labels']['bank14'].items()} if VERSION>=89 else {}
prt=[]
p.hook_register(0,0x3c94,lambda c:prt.append(p.register_file.HL),None)
warp(0x21,0,setup)
print('party after warp',[hex(x) for x in m[0xd164:0xd16a]],flush=True);m[0xd5a6+4]&=~(1<<2)&0xff;T(5)                      # Oak's lab shows the rival; the trigger tile is reached by hand (the walk there is the harness' problem)
m[0xd361]=5;m[0xd362]=29;T(30)
for i in range(40):
    if m[0xd057]:break
    press_('a',90)
ok(m[0xd057]==2 and m[0xd031]==0x19 and m[0xd059]==0xe1,'the first ROUTE 22 rival battle (RIVAL1, opponent E1)')
print('lead in battle',hex(m[0xd014]),flush=True);master=[];seen.clear()
wait_menu()
if MODE=='curse':ci=list(m[0xd16b+8:0xd16b+12]).index(0xa5)
for r in range(14):
    if m[0xd057]==0:break
    if MODE=='win' and m[0xd05a]==3:menu('run');master.extend(seen)
    else:use_move(ci if MODE=='curse' else 0,400);master.extend(seen)
    for k in range(8):
        tt=clean(' '.join(txt()))
        if ('FIGHT' in tt and 'RUN' in tt) or m[0xd057]==0:break
        if 'change' in tt.lower():press_('b',70);master.extend(seen);seen.clear();continue
        press_('a',70);master.extend(seen);seen.clear()
for i in range(70):
    press_('a',60);master.extend(seen);seen.clear()
    if i%10==0:print('dbg',i,'script',m[0xd60a],'d057',m[0xd057],'d05a',m[0xd05a],'box',bool(box()),'cd6b',m[0xcd6b],'d730',hex(m[0xd730]),flush=True)
T_=fin(master);print('TEXT',T_[-1200:],flush=True)
print('D463',m[0xd463],'D452',m[0xd452],'D453',m[0xd453],'cer',m[0xd75a]&1,'ssanne',m[0xd665],'D7EB',hex(m[0xd7eb]),flush=True)
if MODE=='curse':
    print('PrintText pointers',[hex(x) for x in prt[-6:]],flush=True)
    ok('hesitates' in T_ and 'ran away' in T_ and m[0xd453]==0,'GHOST hesitates, BLUE ran away, no murder')
    ok(m[0xd463]==1 and m[0xd75a]&1 and m[0xd665]==4 and not m[0xd7eb]&0x80,'shock mode: D463 = 1, Cerulean skipped, S.S. ANNE skipped, ROUTE 22 flag off')
    ok('What was that' in T_ and 'went limp' in T_ and 'GRAMPS' in T_,'the shock speech after he runs away')
    ok('dawdling' not in T_ and 'LEAGUE has many' not in T_,'not the old speech')
else:
    print('PrintText pointers',[hex(x) for x in prt[-6:]],flush=True)
    ok(0x51b2 in prt,'a normal win: the original after-battle speech (text at 14:51B2)')
    ok(L14.get('shock89') not in prt,'the shock speech is not used')
    ok('What was that' not in T_ and m[0xd463]==0,'no shock text, no shock mode')

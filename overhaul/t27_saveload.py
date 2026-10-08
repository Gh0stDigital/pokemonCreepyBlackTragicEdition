# All overhaul flags (D450-D463) survive SAVE -> power cycle (fresh emulator + the save RAM) -> CONTINUE. Also checks the party/box and a
# few event flags, and that NEW GAME still clears the overhaul range.
from harness import *
def clean(s):return ' '.join(''.join(c for c in s if c not in '│─┌┐└┘|').split())
load('blue_hero');p.tick(60)
# recognizable, harmless values (mode/state bytes kept at real values)
vals={0xd450:1,0xd451:1,0xd453:1,0xd454:3,0xd455:201,0xd456:4,0xd45b:0,0xd45c:77,0xd45d:0,0xd45e:0,0xd45f:0,
      0xd460:3,0xd461:0,0xd462:0,0xd463:2}
for a,v in vals.items():m[a]=v
graves=list(m[0xd4a4:0xd4ae]);party=list(m[0xd163:0xd16b]);ev=list(m[0xd747:0xd747+40])
press('start',90)
for i in range(8):
    if '▲SAVE' in ' '.join(txt()):break
    press('down',30)
press('a',200);print('save prompt:',clean(box()))
p.button('a',8);seen=[]
for i in range(900):
    p.tick();b=clean(box())
    if b and (not seen or seen[-1]!=b):seen.append(b)
    if i%120==60 and 'SAVE' in b and 'Would' not in b and 'saved' not in b.lower():p.button('a',8)
print('save texts:',[x for x in seen if x.endswith('!') or x.endswith('?') or x.endswith('▼')][:6])
assert any('saved' in x.lower() for x in seen)
for i in range(4):press('b',60)
# power cycle: copy the cartridge save RAM into a brand-new emulator (all WRAM starts from scratch)
import harness
from pyboy import PyBoy
sram=[[m[bk,ad] for ad in range(0xa000,0xc000)] for bk in range(4)]
p.stop(save=False)
harness.p=PyBoy(ROM,window='null',sound_emulated=False);harness.p.set_emulation_speed(0);harness.m=harness.p.memory
p=harness.p;m=harness.m
for bk in range(4):
    for i,v in enumerate(sram[bk]):m[bk,0xa000+i]=v
p.tick(300)
for i in range(40):
    t=' '.join(txt())
    if 'CONTINUE' in t or 'PLAYER' in t:break
    press('start' if i%2 else 'a',120)
print('menu:',[x for x in txt() if x][:6])
if 'CONTINUE' in ' '.join(txt()):press('a',200)               # CONTINUE
assert 'PLAYER' in ' '.join(txt())                            # save summary of the file being loaded
press('a',400)
for i in range(10):
    if m[0xd35e]!=0 or pos()!=(0,0,0):break
    press('a',120)
p.tick(200)
got={a:m[a] for a in vals}
print('map',pos())
bad={hex(a):(v,got[a]) for a,v in vals.items() if got[a]!=v}
print('flags after CONTINUE',{hex(a):got[a] for a in vals})
assert not bad,('changed',bad)
assert list(m[0xd4a4:0xd4ae])==graves and list(m[0xd163:0xd16b])==party and list(m[0xd747:0xd747+40])==ev
print('PASS save -> power cycle -> CONTINUE keeps every overhaul flag, gravestones, party and event flags')
# NEW GAME on top of that save must clear the whole overhaul range (no Ghost/hunger/modes carried over)
p.stop(save=False)
harness.p=PyBoy(ROM,window='null',sound_emulated=False);harness.p.set_emulation_speed(0);harness.m=harness.p.memory
p=harness.p;m=harness.m
for bk in range(4):
    for i,v in enumerate(sram[bk]):m[bk,0xa000+i]=v
p.tick(300)
for i in range(40):
    if 'NEW GAME' in ' '.join(txt()):break
    press('start' if i%2 else 'a',120)
press('down',30);press('a',300)
for i in range(6):press('a',120)
print('after NEW GAME: D450-D463',list(m[0xd450:0xd464]),'graves',list(m[0xd4a4:0xd4ae]))
assert not any(m[0xd450:0xd464]) and not any(m[0xd4a4:0xd4ae])
print('PASS NEW GAME over an old save clears every overhaul flag')

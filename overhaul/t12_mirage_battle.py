# Play a Mirage battle: starter FIGHTs (too scared), death move kills it, the player is sent out.
from harness import *
load('mirage_battle_start')
seen=[];black=0;shots=0
def log():
    b=box()
    if b and (not seen or seen[-1]!=b):seen.append(b)
def tick(n):
    global black
    for _ in range(n):
        p.tick(1)
        if m[0xff47]==0xff:black+=1
def clean(s):return ''.join(c for c in s if c not in '│─┌┐└┘|').strip()
print('enemy species',hex(m[0xcfe5]),'lvl',m[0xcff3],'moves',[hex(x) for x in m[0xcfed:0xcff1]],'pp',list(m[0xd002:0xd006]) if False else '',flush=True)
for i in range(120):
    log();b=box()
    if m[0xd057]==0:break
    if m[0xd014]==0x79 and 'FIGHT' in b and 'RUN' in b:
        save('mirage_player_out');print('PLAYER IS OUT: species',hex(m[0xd014]),'name',''.join(cm.get(x,'?') for x in m[0xd009:0xd012]),flush=True);break
    if 'Bring out' in b:p.button('down',8);tick(30);p.button('a',8);tick(200);continue
    p.button('a',8);tick(160)
    if i in (8,14,20):shot('mirage_fight_%02d'%i)
for s in seen:print('  TEXT:',clean(s))
print('black frames',black,'party',list(m[0xd164:0xd16b]),'starter HP',m[0xd16c]*256+m[0xd16d],flush=True)

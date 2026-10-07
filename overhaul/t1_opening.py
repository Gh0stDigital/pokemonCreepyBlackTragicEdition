from harness import *
p.tick(1800);press('start');press('a',400)
names=0
for i in range(160):
    lines=txt()
    if 'NEW NAME' in '\n'.join(lines):names+=1;press('down');press('a');continue
    if names>=2 and m[0xd35e]==0x26 and m[0xd361]==6 and not any('│' in x for x in lines):save('bedroom');break
    press('a')
else:raise SystemExit('FAIL intro')
p.button('right',64);p.tick(100);p.button('up',80);p.tick(200)
p.button('right',40);p.tick(200);p.button('down',80);p.tick(100);p.button('left',56);p.tick(100);p.button('down',40);p.tick(300)
save('mu_start');print('outside',pos(),'mu state',m[0xd454])
for i in range(25):
    if any('THE TRAINER' in x for x in txt()):save('choice');print('PASS choice menu');break
    press('a')
else:raise SystemExit('FAIL no choice')

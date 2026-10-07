# Put a fossil in the lead party slot, start a wild battle, screenshot its back sprite.
from harness import *
import random
from PIL import Image
out=[]
for sp in (0xb6,0xb7):
    random.seed(5);load('pallet_with_ghost')
    m[0xd164]=sp;m[0xd16b]=sp;m[0xd45c]=0;m[0xd455]=255
    for i in range(12):
        if pos()[1]<=10:break
        walk('left',1)
    for i in range(30):
        if m[0xd35e]==0xc and pos()[2]<30:break
        walk('up',1)
    for i in range(1500):
        if m[0xd057]:break
        walk(random.choice(['up','up','down','left','right']),1)
    for i in range(30):
        if 'FIGHT' in box():break
        p.button('a',8);p.tick(150)
    print(hex(sp),'pos',pos(),'battle',m[0xd057],'player mon species',hex(m[0xd014]))
    assert m[0xd014]==sp
    shot('fossil_back_%02x'%sp);out.append(Image.open(qa/('fossil_back_%02x.png'%sp)).convert('RGB'))
W=Image.new('RGB',(340,144),'white');W.paste(out[0],(0,0));W.paste(out[1],(180,0))
W.resize((680,288),Image.NEAREST).save(qa/'v4_fossil_backs.png');print('PASS fossil back sprites rendered in battle')

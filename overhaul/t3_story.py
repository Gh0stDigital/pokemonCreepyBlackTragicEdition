from harness import *
load('trainer_returned')
p.button('right',48);p.tick(80);p.button('up',100);p.tick(100);p.button('right',32);p.tick(80);p.button('up',24);p.tick(400)
for i in range(40):
    if m[0xd35e]==40 and m[0xd5f0]==5:break
    press('a')
else:raise SystemExit('FAIL oak walk '+str(pos()))
save('lab_arrived');print('PASS lab',pos())

from harness import *
load('mu_start');shot('v2_mu_walkup')
load('trainer_returned')
walk('right',4);walk('down',6);walk('left',1);print('pos',pos());shot('v2_shaman_view')
walk('down',2);print('pos',pos());shot('v2_shaman_adjacent')
press('a',60)
lines=[]
for i in range(30):
    b=box()
    if b and (not lines or lines[-1]!=b):lines.append(b)
    press('a',90)
print('\n'.join(lines))

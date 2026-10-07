from harness import *
load('after_curse');p.tick(30)
walk('down',3);walk('up',1);p.tick(120)
m[0xc224]=m[0xd361]+4-1;m[0xc225]=m[0xd362]+4+1   # display-only: bring grave sprite next to player
p.tick(30);shot('grave_closeup');save('forest_after_kill')

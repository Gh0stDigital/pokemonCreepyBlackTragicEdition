from pyboy import PyBoy
from pathlib import Path
import re,json
ROOT=Path(__file__).resolve().parent;qa=ROOT/'qa';qa.mkdir(exist_ok=True)
cm={int(v,16):k for k,v in re.findall(r'^charmap "([^"]+)", \$([0-9A-Fa-f]+)',(ROOT.parent/'pokeblack/charmap.asm').read_text(),re.M) if len(k)==1}
p=PyBoy(str(ROOT/'Creepy_Black_Mu_v1.gb'),window='null',sound_emulated=False);p.set_emulation_speed(0)
def txt():return [''.join(cm.get(v,' ') for v in p.memory[0xc3a0+y*20:0xc3a0+(y+1)*20]).strip() for y in range(18)]
def press(k,n=180):p.button(k,8);p.tick(n)
def save(n):
 p.screen.image.save(qa/(n+'.png'))
 with open(qa/(n+'.state'),'wb') as f:p.save_state(f)
p.tick(1800);press('start');press('a',400)
names=0
for i in range(160):
 lines=txt();print(i,' | '.join(lines),flush=True)
 if 'NEW NAME' in '\n'.join(lines):names+=1;press('down');press('a');continue
 if names>=2 and p.memory[0xd35e]==0x26 and p.memory[0xd361]==6 and not any('│' in x for x in lines):
  save('bedroom');break
 press('a')
else:raise Exception('failed intro')
# move to stairs x7,y1 from x3,y6
p.button('right',64);p.tick(100);p.button('up',80);p.tick(200);save('stairs')
print('coords',p.memory[0xd35e],p.memory[0xd362],p.memory[0xd361],flush=True)
p.stop(save=False)

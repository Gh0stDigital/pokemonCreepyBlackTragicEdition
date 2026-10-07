# Shared PyBoy harness. ROM chosen by CB_ROM env var (default: v2 build).
import os,re,sys
from pathlib import Path
from pyboy import PyBoy
ROOT=Path(__file__).resolve().parent;qa=ROOT/'qa';qa.mkdir(exist_ok=True)
ROM=os.environ.get('CB_ROM',str(ROOT/'Creepy_Black_Mu_v2.gb'))
cm={}
for k,v in re.findall(r'^\s*charmap "([^"]+)",\s*\$([0-9A-Fa-f]+)',(ROOT.parent/'pokeblack/charmap.asm').read_text(encoding='utf8'),re.M):
    if len(k)==1 and ord(k)<0x3000:cm.setdefault(int(v,16),k)
cm[0x54]='#'
p=PyBoy(ROM,window='null',sound_emulated=False);p.set_emulation_speed(0)
m=p.memory
def txt():return [''.join(cm.get(v,' ') for v in m[0xc3a0+y*20:0xc3a0+(y+1)*20]).strip() for y in range(18)]
def box():return ' | '.join(x for x in txt()[12:] if x)
def press(k,n=180):p.button(k,8);p.tick(n)
def shot(n):p.screen.image.save(qa/(n+'.png'))
def save(n):
    shot(n)
    with open(qa/(n+'.state'),'wb') as f:p.save_state(f)
def load(n):
    with open(qa/(n+'.state'),'rb') as f:p.load_state(f)
def pos():return (m[0xd35e],m[0xd362],m[0xd361])  # map, x, y
def walk(d,steps):
    for _ in range(steps):p.button(d,8);p.tick(24)
    p.tick(10)

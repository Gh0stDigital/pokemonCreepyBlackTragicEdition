# v91: the CAVERN tileset graphics are the original ones again (v20-v90 had overwritten tiles 0-14 with TOWER CHAMBER blocks), the TOWER / CHAMBER still draw as before.
import sys,hashlib
sys.argv=['x','none']
exec(open('t52_v44.py').read().split("if MODE=='block':")[0])
def setup():m[0xd455]=255
R1=open('Creepy_Black_Mu_v1.gb','rb').read()
def fo(b,a):return b*0x4000+a-0x4000
CAVE_VRAM='07440dd745418d777570d4a96c143061'          # VRAM $9000-$97FF in the CAVERN tileset (the v19 / original graphics)
for mp,name in ((0x3b,'MT. MOON 1F'),(0x52,'ROCK TUNNEL'),(0xe4,'CERULEAN CAVE 1F'),(0xc5,"DIGLETT'S CAVE")):
    warp(mp,0,setup);T(40)
    h=hashlib.md5(bytes(p.memory[0x9000:0x9800])).hexdigest()
    ok(m[0xd367]==17 and h==CAVE_VRAM,'%s: the cave tile graphics are the original ones'%name)
    ok(bytes(p.memory[0x9000:0x9000+0xf0])==R1[fo(0x1b,0x4ca0):fo(0x1b,0x4ca0)+0xf0],'%s: tiles 0-14 = the base game\'s'%name)
for mp,name,tmh in ((0x8e,'POKeMON TOWER 1F','adda14703c9e07717fbbb06a723e5bd1'),(0x69,'TOWER CHAMBER','eb6fef6f0e4c05cec962d9c265a0beee')):
    warp(mp,0,setup);T(40)
    h=hashlib.md5(bytes(p.memory[0x9000:0x9800])).hexdigest()
    ok(m[0xd367]==15 and h=='4340d229bf5a029aea87ff5fe178962c' and hashlib.md5(bytes(m[0xc3a0:0xc3a0+360])).hexdigest()==tmh,'%s: tiles and blocks draw exactly as before'%name)

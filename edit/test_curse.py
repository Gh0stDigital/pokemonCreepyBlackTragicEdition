exec(open('overhaul/test_opening.py').read().split('p.tick(1800)')[0])
p.load_state(open(qa/'after_rival.state','rb'))
# Harness: swap acquired Ghost to lead; redirect the lab exit to Forest's south entrance.
a=list(p.memory[0xd16b:0xd197]);b=list(p.memory[0xd197:0xd1c3]);p.memory[0xd16b:0xd197]=b;p.memory[0xd197:0xd1c3]=a
p.memory[0xd164],p.memory[0xd165]=p.memory[0xd165],p.memory[0xd164]
p.memory[0xd3b1]=2;p.memory[0xd3b2]=0x33
p.button('down',150);p.tick(150);print('map',p.memory[0xd35e],p.memory[0xd362],p.memory[0xd361],flush=True)
# Put existing trainer 2 immediately above player, retaining original script and roster.
p.memory[0xc224]=p.memory[0xd361]+3;p.memory[0xc225]=p.memory[0xd362]+4
p.tick(60);press('up',20);press('a',300);save('forest_engaged')
black=0
for i in range(95):
 print(i,p.memory[0xd057],p.memory[0xd452],p.memory[0xd453],p.memory[0xd4af],' | '.join(txt()[12:]),flush=True)
 p.screen.image.save(qa/f'curse_{i:02}.png')
 if i>6 and p.memory[0xd057]==0:break
 p.button('a',8)
 for _ in range(220):
  p.tick(1)
  if p.memory[0xff47]==255:black+=1
save('after_curse');print('result',p.memory[0xd452],p.memory[0xd453],'black',black,flush=True)
p.stop(save=False)

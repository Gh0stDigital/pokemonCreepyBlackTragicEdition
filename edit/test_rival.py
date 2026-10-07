exec(open('overhaul/test_opening.py').read().split('p.tick(1800)')[0])
p.load_state(open(qa/'lab_arrived.state','rb'))
for i in range(28):
 print(i,p.memory[0xd5f0],' | '.join(txt()[12:]),flush=True)
 if p.memory[0xd5f0]==6:break
 press('a')
save('lab_ready');press('right',30);press('a',200)
for i in range(30):
 print('pick',i,'count',p.memory[0xd163],p.memory[0xd5f0],' | '.join(txt()[12:]),flush=True)
 if p.memory[0xd5f0]==9:break
 if any('nickname' in x for x in txt()):press('b')
 else:press('a')
save('starter');print('party',list(p.memory[0xd163:0xd169]),flush=True)
p.button('down',48);p.tick(200)
for i in range(120):
 print('fight',i,'count',p.memory[0xd163],p.memory[0xd5f0],p.memory[0xd057],' | '.join(txt()[12:]),flush=True)
 p.screen.image.save(qa/f'rival_{i:03}.png')
 if p.memory[0xd5f0]==10 and p.memory[0xd057]==0:p.button('down',48);p.tick(200)
 if p.memory[0xd5f0]==18 and p.memory[0xd057]==0:break
 press('a',220)
save('after_rival');print('partyafter',list(p.memory[0xd163:0xd169]),'ghostflag',p.memory[0xd451],flush=True)
p.stop(save=False)

exec(open('overhaul/test_opening.py').read().split('p.tick(1800)')[0])
p.load_state(open(qa/'trainer_returned.state','rb'))
print('start',p.memory[0xd362],p.memory[0xd361])
p.button('right',48);p.tick(80);print('right',p.memory[0xd362],p.memory[0xd361]);p.button('up',100);p.tick(100);p.button('right',32);p.tick(80);p.button('up',24);p.tick(400)
for i in range(35):
 print(i,'map',p.memory[0xd35e],'script',p.memory[0xd5f0],' | '.join(txt()[12:]),flush=True)
 p.screen.image.save(qa/f'oak_walk_{i:02}.png')
 if p.memory[0xd35e]==40 and p.memory[0xd5f0]==5:break
 press('a')
save('lab_arrived');print('coords',p.memory[0xd35e],p.memory[0xd362],p.memory[0xd361],p.memory[0xd5f0])
p.stop(save=False)

exec(open('overhaul/test_opening.py').read().split('p.tick(1800)')[0])
p.load_state(open(qa/'stairs.state','rb'))
p.button('right',40);p.tick(200);save('floor1');print('floor',p.memory[0xd35e],p.memory[0xd362],p.memory[0xd361])
p.button('down',80);p.tick(100);p.button('left',56);p.tick(100);p.button('down',40);p.tick(300);save('mu_start');print('outside',p.memory[0xd35e],p.memory[0xd362],p.memory[0xd361],p.memory[0xd454])
for i in range(25):
 print(i,' | '.join(txt()[12:]),'state',p.memory[0xd454],p.memory[0xd450],flush=True);p.screen.image.save(qa/f'mu_{i:02}.png')
 if any('THE TRAINER' in x for x in txt()):save('choice');break
 press('a')
p.stop(save=False)

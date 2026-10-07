exec(open('overhaul/test_opening.py').read().split('p.tick(1800)')[0])
for branch in ['trainer','pokemon']:
 p.load_state(open(qa/'choice.state','rb'));p.tick(120)
 if branch=='pokemon':press('down',30)
 p.screen.image.save(qa/(branch+'_menu.png'));press('a')
 for i in range(8):
  if p.memory[0xd454]==2:break
  press('a')
 print(branch,'answer',p.memory[0xd450],'state',p.memory[0xd454],flush=True);assert p.memory[0xd450]==(1 if branch=='trainer' else 2)
 save(branch+'_pallet');p.button('up',16);p.tick(250);save(branch+'_inside');print('inside',p.memory[0xd35e],p.memory[0xd454],flush=True)
 p.button('down',24);p.tick(200);save(branch+'_returned');print('returned',p.memory[0xd35e],p.memory[0xd454],p.memory[0xc140],flush=True)
 assert p.memory[0xd454]==3 and p.memory[0xc140]==0
p.stop(save=False)

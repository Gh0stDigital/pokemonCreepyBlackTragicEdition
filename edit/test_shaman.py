exec(open('overhaul/test_opening.py').read().split('p.tick(1800)')[0])
p.load_state(open(qa/'trainer_returned.state','rb'))
p.button('right',64);p.tick(80);p.button('down',112);p.tick(100);p.button('left',32);p.tick(80);p.button('down',64);p.tick(80);p.button('right',32);p.tick(80);press('down',30);press('left',24);press('up',24);print('coords',p.memory[0xd362],p.memory[0xd361]);press('a')
for i in range(24):
 print(i,' | '.join(txt()[12:]),flush=True);p.screen.image.save(qa/f'shaman_{i:02}.png');press('a')
save('shaman');p.stop(save=False)

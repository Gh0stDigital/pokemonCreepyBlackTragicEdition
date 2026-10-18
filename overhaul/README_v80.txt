Creepy Black Mu v80 (SHA-256 96b9430d01c31d0588d5e4499e86cfc015aebac222bfd9668f1504aa91182b1f)
As BLACK (D46C), ordinary alive header trainers (not gym trainers, not dead, not scripted fights) talk to you scared:
begging, refusing to fight for their lives/souls, offering their POKeMON. 24 lines before the battle, 16 after it,
picked by the trainer's kill index. The battle itself still happens. Not BLACK, gyms, dead trainers: unchanged (v69 sulk / v67 shock).
Code: bank 31 4C00 rdisp80 (home stub 0:00CE now calls it; it jumps to rdisp69 when it has nothing to say), texts 31:5000.
Test: t88_v80.py black|normal; run_v80.sh.

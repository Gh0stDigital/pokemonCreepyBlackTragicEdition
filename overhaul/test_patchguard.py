# Self-test: the patch guard must catch both bugs this project actually shipped, and pass their fixes.
#   python test_patchguard.py   (from overhaul/)
from patchguard import check_hook,jumps_into,fo
rd=lambda v:open('Creepy_Black_Mu_v%d.gb'%v,'rb').read()
v1,v11,v12,v13=rd(1),rd(11),rd(12),rd(13)
# 1. v1 0x29FD: the original code there had entry points inside the 15 bytes v1 overwrote
v0=bytearray(v1);v0[0x29fd:0x29fd+15]=bytes.fromhex('fa3ccca72009fa47cca72003cd9938')
hits=[t for s,t in jumps_into(bytes(v0),0x29fd,15)]
assert 0x2a03 in hits,hits;print('PASS guard would have refused the v1 0x29FD hook (jumps land at $2A03)')
# 2. v12 F:5033: far call clobbered hl/b before CompareHLWithBC
pr=check_hook(v11,v12,fo(0xf,0x5033),3,provides=('f',))
assert any('365c' in x and 'h' in x for x in pr),pr;print('PASS guard flags the v12 F:5033 hook:',pr[0])
pr=check_hook(v11,v13,fo(0xf,0x5033),3,provides=('f',))
assert not pr,pr;print('PASS guard accepts the v13 fix')

# patchlib smoke test: Rom.hook refuses a v12-style clobbering hook and accepts a register-safe one.
from patchlib import *
import json
sha=json.load(open('manifest_v11.json'))['sha256']
rom=Rom('Creepy_Black_Mu_v11.gb',sha)
site=fo(0xf,0x5033);orig=rom.r[site:site+3].hex();assert orig=='cd5c36'
# bad: far call into a home routine that runs CompareHLWithBC after hl/b were overwritten
rom.put(0xed,bytes.fromhex('cd5c36c9'),'home stub: call CompareHLWithBC')
rom.put(fo(0xf,0x7ff8),bytes.fromhex('21ed000600c31836'),'bad stub: far call (clobbers hl/b)')
try:
    rom.hook(site,bytes.fromhex('cdf87f'),'bad hook',orig,provides=('f',));raise SystemExit('FAIL: bad hook accepted')
except SystemExit as e:
    assert 'REFUSED' in str(e),e;print('PASS bad hook refused:',str(e).splitlines()[1].strip())
rom=Rom('Creepy_Black_Mu_v11.gb',sha)
rom.put(0xed,bytes.fromhex('cd5c36c9'),'home stub: call CompareHLWithBC')
rom.hook(site,bytes.fromhex('cded00'),'good hook',orig,provides=('f',));print('PASS register-safe hook accepted')

# Creepy Black Mu v64: a secret door in the HALL OF FAME (map 76): the top-left corner floor tile (y1, x0) is a warp back to the POKeMON LEAGUE lobby (map AE,
#   its warp 2 = the top door, where you arrive coming back from LORELEI's room). The object data (border, warps, signs, objects) is moved to bank 16:65D6
#   with a third warp (and its warp-to entry); the header's object pointer follows.
from patchlib import *
from patchguard import fo

V63_SHA='0015301cb0e5c92d91631d9f24b2328e7af329d8ed3edb84aee8def5eeabd5f0'
rom=Rom('Creepy_Black_Mu_v63.gb',V63_SHA)
r=rom.r;R=bytes(r)
NEW=0x65d6
OLD=fo(0x16,0x6571)
old=R[OLD:OLD+26];assert old.hex()=='030207040278070503780001030609ffd001'+'17c70704'+'17c70705',old.hex()   # object data, then the warp-to list (view pointer, y, x)
HH=fo(0x16,0x6492);assert R[HH+10:HH+12].hex()=='7165'
data=bytes.fromhex('03'+'03'+'07040278'+'07050378'+'010002ae'+'00'+'01'+'030609ffd001'+'17c70704'+'17c70705'+'f4c60100')   # warp-to (1,0): C6E8+7+5 = C6F4
rom.put(fo(0x16,NEW),data,'Bank 16: v64 HALL OF FAME object data with the secret warp (1,0) -> LEAGUE lobby (map AE, warp 2)')
rom.data(HH+10,bytes.fromhex(le(NEW)),'HALL OF FAME header: object pointer -> v64 data','7165')
rom.finish('Creepy_Black_Mu_v64.gb','manifest_v64.json','CREEPY MU V64')

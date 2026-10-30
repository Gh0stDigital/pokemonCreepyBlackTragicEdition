Creepy Black Mu v92 (on v91): MR. MU in the POKeMON MANSION talks more.
SHA-256: e7a57553bef1ec4f4c8e34225ebaf5fd62fa3d9f15382c3f9bf07e35e3bbd8d0

FIRST TALK: "Oh, RED. I didn't expect to see you here. This place holds many old secrets ... Oh? The key to the GYM? Hmm, I see... Take this, then." He gives the SECRET KEY
("RED received SECRET KEY!" / "This is what you need, right? ... complete your journey, after all."). A SECRET KEY already in the bag is not doubled (he says "You are carrying it already");
a full bag: "Make room" and nothing is marked (he repeats it next time).
THEN he checks the bag for the OLD AMBER: with it "My, RED. You are quite resourceful. You have the AMBER in your possession too now... Could you humor me with an answer to another question?"
and the v52 question (THEY WOULD NOT / THEY WOULD -> AZHI Lv35 as before, party full = make room). Without the AMBER nothing more; if the AMBER comes later he asks at the next talk.
LATER TALKS: a warning about digging too deep in the mansion, the old experiments still linger.  After the AMBER was given to him (AZHI) he adds: "If something is troubling you, don't worry too hard. Just focus on the goal at hand and everything will work out."
GONE: once the AMBER question was answered (either way) he disappears at the next map load (leave and return); giving the AMBER no longer removes him at once.  Without an answer he stays.
(CHANGE: THEY WOULD NOT used to be re-askable at any time; it now ends the question.)

Technical: bank 32:7000 mu92 (hasitem helper, texts); the Mansion text stub 11:752A now points there (bank 32); D885 flags (bit0 key/intro done, bit1 question answered, bit2 AMBER given;
D885 is the last-but-one event-flag byte, unused; NEW GAME clears it); 2E:7700 m92 (first link of the map-load chain at 2E:4000): bit1 set and D460 = 3 -> D460 = 4 (v52's man52 then hides him).
Tests: t100_v92.py talk (20 checks); t60 azhi is skipped from v92 (its old flow changed). run_v92.sh = run_v91.sh + t100.

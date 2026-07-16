#!/usr/bin/env python
"""Author the dense livingpage_full.spec.json for Bronze Serpent from scratch.
Beats are defined with a 'start' phrase (resolved against the word-timed
narration.alignment.json via wordtime.Cursor) plus template/content. t1 of
each beat = t0 of the next beat (frame-exact contiguity); the last beat ends
at the narration's last word end + a short tail.
"""
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from wordtime import Cursor, WORDS

POOL = Path(__file__).resolve().parents[1] / "v1" / "visual_16x9_inked"

c = Cursor()


def full(start, slug, cap, cam=None, punch=False, ramp=False, whip=False,
         inserts=None, takeover=None, sacred=False, fx=None, motion=None):
    cd = {"slug": slug}
    if cam:
        cd["cam"] = cam
    b = {"start": start, "tpl": "full", "clips": [cd], "cap": cap}
    if punch:
        b["punch"] = True
    if ramp:
        b["ramp"] = True
    if whip:
        b["whip"] = True
    if inserts:
        b["inserts"] = inserts
    if takeover:
        b["takeover"] = takeover
    if fx:
        b["fx"] = fx
    return b


def frac3(start, slug, cap, anchors, slides=("left", "up", "right"), sacred=False,
          punch=False, flash=True, cam_hint=None):
    b = {"start": start, "tpl": "hero_frac3",
         "clips": [{"slug": slug}], "cap": cap,
         "anchors": anchors, "_panel_slide": list(slides), "flash": flash}
    if punch:
        b["punch"] = True
    return b


def grid(start, tpl, clips, cap, punch=False, takeover=None, whip=False, ramp=False):
    b = {"start": start, "tpl": tpl, "clips": clips, "cap": cap}
    if punch:
        b["punch"] = True
    if takeover:
        b["takeover"] = takeover
    if whip:
        b["whip"] = True
    if ramp:
        b["ramp"] = True
    return b


def cap_c(text, kw):
    return {"type": "caption", "text": text, "kw": kw}


def cap_r(speaker, ref, text):
    return {"type": "redletter", "speaker": speaker, "ref": ref, "text": text}


R = "reuse_"  # prefix for reused clip_library assets copied into ./clips/

# =====================================================================
# BEATS — in narration order. Each beat's timing is resolved from its
# 'start' phrase; template/content authored by hand against the 27 stills
# (movements M1-M7) + 21 reused inked Cross-cluster clips.
# =====================================================================
beats = []

# ---------------- M1 THE PICTURE (hook) ----------------
beats.append(full("A whole", "01_snakebite", cap_c("A whole camp is dying of snakebite.", "SNAKEBITE"),
                   cam="push", punch=True))
beats.append(full("and God's", "04_venom", cap_c(
    "God's remedy is not to kill the snakes, or heal the wounds, or hand out an antidote.", "REMEDY"),
    inserts=[{"at_frac": 0.55, "slug": "08_raised", "frames": 4}]))
beats.append(full("He tells", "08_raised", cap_c(
    "He tells them to look at a piece of metal on a pole. Look, and live.", "LOOK"), cam="push", ramp=True))
beats.append(full("It is one", "08_raised", cap_c(
    "It is one of the strangest cures in the Bible.", "STRANGEST"), cam="arc"))
# NOTE: beat3/4 both cite still08 but beat4 is folded into beat3 below (see FIX pass) —
# actually keep as one beat; remove duplicate. (placeholder resolved in POSTPROCESS)

beats.append(frac3("It happens", "02_worn_down_they_despise_the_bread_of_heaven", cap_c(
    "It happens near the end of the wilderness years. Israel is worn down by the long road, and the old bitterness boils over.",
    "BOILS OVER"),
    anchors=[[1.0, 0.42, 0.42], [1.9, 0.20, 0.62], [1.9, 0.62, 0.42]]))

beats.append(full("Wherefore have", "03_the_lord_sent_fiery_serpents__and_people_died",
    cap_r("THE PEOPLE", "Numbers 21:5",
          "Wherefore have ye brought us up out of Egypt to die in the wilderness? for there is no bread, neither is there any water; and our soul loatheth this light bread."),
    cam="push", takeover={"panel": 0, "start_frac": 0.75, "zoom": 1.25}))

beats.append(full("And the LORD sent", "03_the_lord_sent_fiery_serpents__and_people_died",
    cap_r("NUMBERS 21", "Numbers 21:6",
          "And the LORD sent fiery serpents among the people, and they bit the people; and much people of Israel died."),
    cam="arc"))
# ^ NOTE: same slug back-to-back — postprocess will merge beats 6+7 into one long beat.

beats.append(frac3("Picture the", "05_they_beg_moses_take_the_serpents_away", cap_r(
    "THE PEOPLE", "Numbers 21:7",
    "We have sinned, for we have spoken against the LORD, and against thee; pray unto the LORD, that he take away the serpents from us."),
    anchors=[[1.0, 0.35, 0.5], [1.8, 0.18, 0.72], [1.8, 0.62, 0.68]]))

beats.append(full("Their confession", "27_outward", cap_c(
    "Their confession is real. They name the sin itself. But look at the cure they ask for: take away the serpents, make the threat go away.",
    "CONFESSION"), cam="push", punch=True))

beats.append(full("Even as they", "27_outward", cap_c(
    "Even as they confess, their request reaches only for the danger outside.", "OUTWARD"), cam="arc"))
# ^ same slug twice adjacent again — postprocess merges beats 10+11.

beats.append(full("Now watch", "06_not", cap_c(
    "Now watch what God actually does, because He does not do what they asked.", "NOT"), cam="arc"))

beats.append(full("Make thee", "07_make_a_fiery_serpent_set_it_on_a_pole", cap_r(
    "THE LORD", "Numbers 21:8",
    "Make thee a fiery serpent, and set it upon a pole: and it shall come to pass, that every one that is bitten, when he looketh upon it, shall live."),
    cam=None))

beats.append(full("Sit with", "22_curse", cap_c(
    "Sit with how strange that is. The cure is shaped like the curse.", "CURSE"), cam="swoop", punch=True))

beats.append(full("The thing lifted", "22_curse", cap_c(
    "The thing lifted up is a serpent, a bronze likeness of the very thing killing them, raised on a pole for all to see.",
    "LIKENESS"), cam="arc"))
# same slug adjacent — postprocess merges.

beats.append(full("And the cure", "08_raised", cap_c(
    "And the cure costs the bitten man nothing he can boast in.", "NOTHING"), cam="arc"))

beats.append(full("Every one", "08_raised", cap_r("THE LORD", "Numbers 21:8b",
    "Every one that is bitten, when he looketh upon it, shall live."), cam=None))
# same slug adjacent — postprocess merges.

beats.append(full("One act", "09_look", cap_c("One act. Look.", "LOOK"), punch=True))

beats.append(frac3("And Moses made", "10_and_moses_made_a_serpent_of_brass_the_camp_looks", cap_r(
    "NUMBERS 21", "Numbers 21:9",
    "And Moses made a serpent of brass, and put it upon a pole, and it came to pass, that if a serpent had bitten any man, when he beheld the serpent of brass, he lived."),
    anchors=[[1.0, 0.5, 0.4], [1.9, 0.2, 0.7], [1.9, 0.78, 0.68]]))

beats.append(grid("Now move", "two_v", [
    {"slug": "01_snakebite", "cam": "swoop"}, {"slug": "03_the_lord_sent_fiery_serpents__and_people_died", "cam": "swoop"}],
    cap_c("Now move forward roughly fourteen hundred years.", "FOURTEEN HUNDRED")))

beats.append(frac3("into a quiet", "11_night", cap_c(
    "Into a quiet night-time conversation. A religious leader named Nicodemus has come to Jesus in the dark, trying to understand who He is.",
    "NICODEMUS"),
    anchors=[[1.0, 0.5, 0.42], [1.9, 0.28, 0.42], [1.9, 0.74, 0.42]]))

beats.append(full("And Jesus reaches", "23_himself", cap_c(
    "And Jesus reaches back, past the temple, past the law, to a snake on a pole in the desert.", "REACHES BACK"),
    cam="push"))

# ---------------- M4 THE CENTURIES-EARLY MATCH ----------------
beats.append(full("And as Moses", "12_even_so_must_the_son_of_man_be_lifted_up", cap_r(
    "JESUS", "John 3:14-15",
    "And as Moses lifted up the serpent in the wilderness, even so must the Son of man be lifted up: That whosoever believeth in him should not perish, but have eternal life."),
    cam=None))

beats.append(grid("Stop on", "two_v", [
    {"slug": R + "jesus_looks_down"}, {"slug": R + "face_on_cross"}],
    cap_c("Stop on that. This is not a preacher centuries later finding a clever picture in the Old Testament.",
          "STOP ON THAT")))

beats.append(full("This is Jesus", "13_lifted_up__signifying_what_death_he_should_die", cap_c(
    "This is Jesus Himself, naming that pole as a portrait of His own cross.", "PORTRAIT"), cam="push", punch=True))

beats.append(full("And He means", "13_lifted_up__signifying_what_death_he_should_die", cap_c(
    "And He means it precisely. Later, John tells us what that phrase pointed to.", "PRECISELY"), cam="arc"))
# same slug adjacent — merge.

beats.append(grid("And I, if", "triptych_v", [
    {"slug": R + "nail_through_hand"}, {"slug": "13_lifted_up__signifying_what_death_he_should_die", "cam": "swoop"},
    {"slug": R + "golgotha_hill_wide"}],
    cap_r("JESUS", "John 12:32", "And I, if I be lifted up from the earth, will draw all men unto me.")))

beats.append(full("This he said", R + "darkness_veil_torn", cap_r(
    "SCRIPTURE", "John 12:33", "This he said, signifying what death he should die."), cam=None))

beats.append(grid("Lifted up", "two_v", [
    {"slug": R + "two_thieves_wide"}, {"slug": R + "cross_at_dawn"}],
    cap_c("Lifted up was the cross. By Jesus' own word, the wilderness pole was a picture of Calvary.", "CALVARY")))

beats.append(full("And the passage", "14_for_god_so_loved_the_world", cap_c(
    "And the passage flows straight on into the verse the whole world knows.", "WHOLE WORLD"), cam="push"))

beats.append(full("For God so loved", "14_for_god_so_loved_the_world", cap_r(
    "SCRIPTURE", "John 3:16",
    "For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have eternal life."),
    cam=None))
# same slug adjacent — merge.

beats.append(grid("The snake on", "big_inset", [
    {"slug": "08_raised", "cam": "arc"}, {"slug": R + "grace_poured_sky"}],
    cap_c("The snake on the pole and God so loved the world sit in the same breath of Scripture.", "SAME BREATH")))

# ---------------- M5 THE HONEST OBJECTION ----------------
beats.append(full("Now, be fair", "24_trust", cap_c(
    "Now, be fair to the doubts, because there are two.", "TWO DOUBTS"), cam="arc"))

beats.append(full("First: doesn't", "24_trust", cap_c(
    "First: doesn't a bronze snake on a pole just become an idol? Scripture itself answers that, bluntly.",
    "IDOL"), cam="swoop"))
# same slug adjacent — merge.

beats.append(full("Centuries later", "15_hezekiah_breaks_the_brazen_serpent", cap_c(
    "Centuries later Israel did begin burning incense to it, and a godly king named Hezekiah", "HEZEKIAH"),
    cam="push"))

beats.append(full("brake in pieces", "15_hezekiah_breaks_the_brazen_serpent", cap_r(
    "2 KINGS 18", "2 Kings 18:4", "brake in pieces the brasen serpent that Moses had made."),
    punch=True))
# same slug adjacent — merge.

beats.append(full("The bronze never", "24_trust", cap_c(
    "The bronze never had power; God did. Looking was never magic, it was trust.", "TRUST"), cam="push"))

beats.append(grid("aimed where", "two_v", [
    {"slug": R + "jesus_looks_down"}, {"slug": R + "hands_of_light_open"}],
    cap_c("Aimed where God told them to aim it. Scripture smashes the relic itself, so you never mistake the sign for the Savior.",
          "NOT THE SIGN")))

beats.append(full("Second, and", "16_the_likeness_of_the_curse_lifted_up", cap_c(
    "Second, and deeper: isn't a serpent a strange picture of Christ?", "STRANGE PICTURE"), cam="push"))

beats.append(full("In the Bible", "16_the_likeness_of_the_curse_lifted_up", cap_c(
    "In the Bible the serpent is the tempter and the curse. Exactly, and that is the point, not the problem.",
    "THE POINT"), cam="arc"))
# same slug adjacent — merge.

beats.append(grid("What hung on", "two_v", [
    {"slug": "16_the_likeness_of_the_curse_lifted_up", "cam": "push"}, {"slug": R + "bowed_head_finished"}],
    cap_c("What hung on that pole was the likeness of the very thing killing them.", "LIKENESS")))

beats.append(full("what hung on the cross", "17_made_a_curse_for_us__on_the_tree", cap_c(
    "What hung on the cross was the One of whom Scripture says God", "OF WHOM SCRIPTURE SAYS"), cam="push"))

beats.append(full("hath made him", "17_made_a_curse_for_us__on_the_tree", cap_r(
    "2 CORINTHIANS 5", "2 Corinthians 5:21", "hath made him to be sin for us, who knew no sin."), cam=None))
# same slug adjacent — merge.

beats.append(grid("being made", "triptych_v", [
    {"slug": R + "nail_through_hand"}, {"slug": "17_made_a_curse_for_us__on_the_tree", "cam": "arc"},
    {"slug": R + "darkness_veil_torn"}],
    cap_r("GALATIANS 3", "Galatians 3:13",
          "being made a curse for us: for it is written, Cursed is every one that hangeth on a tree.")))

beats.append(full("Christ did not", "18_curse", cap_c(
    "Christ did not become a sinner. He was lifted up bearing our curse, in the likeness of the judgment we deserved.",
    "BEARING OUR CURSE"), cam="push", punch=True))

beats.append(full("so the look", "18_curse", cap_c(
    "So the look of faith could find it there and live. This is not a stretch; it is the meaning Jesus put there Himself.",
    "MEANING JESUS PUT THERE"), cam="arc"))
# same slug adjacent — merge.

# ---------------- M6 THE EXCHANGE ----------------
beats.append(grid("So hold the two", "two_v", [
    {"slug": "22_curse", "cam": "swoop"}, {"slug": R + "golgotha_hill_wide"}],
    cap_c("So hold the two scenes together. In the wilderness the cure was never in the dying man.",
          "NEVER IN HIM")))

beats.append(full("he could not", "19_look", cap_c(
    "He could not neutralize the venom or earn his way back to health. It hung entirely outside him, on a pole.",
    "OUTSIDE HIM"), cam="push"))

beats.append(grid("That is the cross", "big_inset", [
    {"slug": "25_we_are_all_bitten__the_cure_outside_us", "cam": "push"}, {"slug": R + "face_on_cross"}],
    cap_c("That is the cross. We are all bitten; the poison of sin is already in us, and no self-improvement reaches it.",
          "ALL BITTEN")))

beats.append(full("So God lifted", "25_we_are_all_bitten__the_cure_outside_us", cap_c(
    "So God lifted up His Son, who", "LIFTED UP HIS SON"), cam="arc"))

beats.append(full("his own self", "16_the_likeness_of_the_curse_lifted_up", cap_r(
    "1 PETER 2", "1 Peter 2:24", "his own self bare our sins in his own body on the tree."), cam="push"))

beats.append(grid("The curse fell", "two_v", [
    {"slug": R + "us_under_cross_shadow"}, {"slug": "18_curse", "cam": "swoop"}],
    cap_c("The curse fell on the lifted One, so that everyone who looks to Him might live.", "FELL ON HIM")))

beats.append(full("It cost the", "26_strong", cap_c(
    "It cost the bitten Israelite nothing but a turn of the eyes. It cost the Son everything.", "COST"),
    cam="push", punch=True))

# ---------------- M7 THE INVITATION ----------------
beats.append(full("There is one", "19_look", cap_c(
    "There is one more detail here, and it may be the kindest of all: the cure was a look.", "THE CURE WAS A LOOK"),
    cam="swoop"))

beats.append(full("God could have", "26_strong", cap_c(
    "God could have asked for a climb, a payment, a proof of strength. He asked for the one thing a dying man can still do.",
    "ONE THING"), cam="arc"))

beats.append(grid("You can be", "two_v", [
    {"slug": R + "man_lifting_face_dawn"}, {"slug": R + "look_up_faces"}],
    cap_c("You can be too weak to stand and still lift your eyes.", "LIFT YOUR EYES")))

beats.append(full("The most poisoned", "20_whosoever", cap_c(
    "The most poisoned person in the camp was no further from healing than the least.", "NO FURTHER"),
    cam="push"))

beats.append(full("both were saved", "20_whosoever", cap_c(
    "Both were saved the same way, by looking away from themselves to the One lifted up.", "SAME WAY"), cam="arc"))
# same slug adjacent — merge.

beats.append(grid("So the invitation", "triptych_v", [
    {"slug": R + "look_up_faces"}, {"slug": "20_whosoever", "cam": "swoop"}, {"slug": R + "hands_of_light_open"}],
    cap_c("So the invitation is as wide as the word Jesus chose: whosoever.", "WHOSOEVER")))

beats.append(full("You do not have", "26_strong", cap_c(
    "You do not have to get the poison out first, or feel strong, or be certain your faith is large enough.",
    "NOT FIRST"), cam="push"))

beats.append(full("Faith is not", "26_strong", cap_c(
    "Faith is not a great work you produce; it is the empty-handed look of someone who has stopped trying to save themselves.",
    "EMPTY-HANDED LOOK"), cam="arc"))
# same slug adjacent — merge.

beats.append(grid("You only have", "two_v", [
    {"slug": R + "man_lifting_face_dawn"}, {"slug": "21_look_to_the_one_lifted_up_hero_close"}],
    cap_c("You only have to stop staring at the bite, and look up.", "LOOK UP"), punch=True))

beats.append(full("The serpent in", "10_and_moses_made_a_serpent_of_brass_the_camp_looks", cap_c(
    "The serpent in the wilderness was God teaching the world one motion that saves.", "ONE MOTION"), cam="swoop"))

beats.append(full("He lifted His Son", "21_look_to_the_one_lifted_up_hero_close", cap_c(
    "He lifted His Son on a cross for exactly that, so that whosoever turns their eyes to Him", "WHOSOEVER TURNS"),
    cam=None))
# same slug adjacent — merge.

beats.append(grid("should not perish", "two_v", [
    {"slug": R + "risen_christ_wounds"}, {"slug": R + "risen_christ_seeking"}],
    cap_r("JOHN 3", "John 3:15b", "should not perish, but have eternal life.")))

beats.append(grid("You have stared", "triptych_v", [
    {"slug": R + "stone_rolled_dawn"}, {"slug": R + "risen_christ_congregation"}, {"slug": R + "first_day_morning"}],
    cap_c("You have stared at the bite long enough. The cure was never inside you.", "NEVER INSIDE YOU")))

beats.append(full("it is lifted up", "21_look_to_the_one_lifted_up_hero_close", cap_c(
    "It is lifted up, outside you, already finished.", "ALREADY FINISHED"), cam=None))
# same slug adjacent — merge.

beats.append(full("Lift your eyes", "21_look_to_the_one_lifted_up_hero_close", cap_c(
    "Lift your eyes from the poison to the Saviour.", "LIFT YOUR EYES"), cam=None))
# same slug adjacent — merge.

beats.append(full("What He has", "21_look_to_the_one_lifted_up_hero_close", cap_c(
    "What He has done on that cross is enough.", "ENOUGH"), cam=None))
# same slug adjacent — merge; final landing hold stays on the hero close throughout.

print(f"authored {len(beats)} pre-merge beat records")
json.dump(beats, open(Path(__file__).resolve().parent / "beats_raw.json", "w"), indent=1)

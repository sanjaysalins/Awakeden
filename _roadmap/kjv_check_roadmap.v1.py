"""$0 KJV check for TWO_DRIVERS_ROADMAP.md quotes. Reuses prophecy/01_bethlehem/fresh_hunt/kjv_check.py."""
import sys
sys.path.insert(0, r"F:\slk\PycharmProjects\JesusInTheBible\prophecy\01_bethlehem\fresh_hunt")
from kjv_check import check
Q = """
2 Samuel 7:13|I will stablish the throne of his kingdom for ever
Luke 1:32|the Lord God shall give unto him the throne of his father David
Luke 1:33|of his kingdom there shall be no end
Hosea 11:1|called my son out of Egypt
Matthew 2:15|Out of Egypt have I called my son
Deuteronomy 8:3|man doth not live by bread only
Matthew 4:4|Man shall not live by bread alone
Isaiah 9:2|The people that walked in darkness have seen a great light
2 Kings 15:29|all the land of Naphtali, and carried them captive to Assyria
Matthew 4:16|The people which sat in darkness saw great light
Deuteronomy 18:15|unto him ye shall hearken
Matthew 17:5|hear ye him
Acts 3:22|A prophet shall the Lord your God raise up unto you
Zechariah 9:9|lowly, and riding upon an ass
John 12:16|These things understood not his disciples at the first
Genesis 49:11|Binding his foal unto the vine
Psalm 118:22|The stone which the builders refused is become the head stone of the corner
Psalm 118:26|Blessed be he that cometh in the name of the LORD
Matthew 21:9|Blessed is he that cometh in the name of the Lord
Matthew 21:42|The stone which the builders rejected
Psalm 110:1|The LORD said unto my Lord, Sit thou at my right hand
Matthew 22:45|If David then call him Lord, how is he his son?
Matthew 22:46|no man was able to answer him a word
Psalm 41:9|mine own familiar friend, in whom I trusted, which did eat of my bread, hath lifted up his heel against me
John 13:18|He that eateth bread with me hath lifted up his heel against me
2 Samuel 15:23|passed over the brook Kidron
2 Samuel 15:30|went up by the ascent of mount Olivet, and wept as he went up
2 Samuel 17:23|hanged himself
John 18:1|over the brook Cedron
Matthew 27:5|went and hanged himself
Daniel 7:13|one like the Son of man came with the clouds of heaven
Matthew 26:64|Hereafter shall ye see the Son of man sitting on the right hand of power, and coming in the clouds of heaven
Exodus 26:31|with cherubims shall it be made
Genesis 3:24|Cherubims, and a flaming sword
Matthew 27:51|the veil of the temple was rent in twain from the top to the bottom
Hebrews 10:20|through the veil, that is to say, his flesh
Psalm 16:10|neither wilt thou suffer thine Holy One to see corruption
Acts 2:29|his sepulchre is with us unto this day
Acts 2:31|spake of the resurrection of Christ
Isaiah 6:1|I saw also the Lord sitting upon a throne, high and lifted up
John 12:41|These things said Esaias, when he saw his glory, and spake of him
Mark 1:11|Thou art my beloved Son, in whom I am well pleased
Psalm 2:7|Thou art my Son
Isaiah 42:1|in whom my soul delighteth
Leviticus 13:46|he shall dwell alone; without the camp shall his habitation be
Mark 1:41|put forth his hand, and touched him
Mark 1:45|could no more openly enter into the city, but was without in desert places
Hebrews 13:12|suffered without the gate
Mark 5:34|Daughter, thy faith hath made thee whole
Leviticus 15:25|she shall be unclean
Luke 8:44|touched the border of his garment
Numbers 15:38|fringes in the borders of their garments
John 20:15|supposing him to be the gardener
John 19:41|in the place where he was crucified there was a garden
Genesis 2:15|put him into the garden of Eden to dress it and to keep it
John 10:3|he calleth his own sheep by name
John 20:16|Jesus saith unto her, Mary
Luke 5:8|Depart from me; for I am a sinful man, O Lord
Isaiah 6:5|Woe is me! for I am undone
Luke 5:10|Fear not; from henceforth thou shalt catch men
Isaiah 6:8|Here am I; send me
John 9:11|A man that is called Jesus
John 9:17|He is a prophet
John 9:38|Lord, I believe. And he worshipped him
John 9:35|and when he had found him
Mark 6:48|would have passed by them
Job 9:8|treadeth upon the waves of the sea
Exodus 33:22|while my glory passeth by
Mark 6:50|Be of good cheer: it is I; be not afraid
Luke 22:32|I have prayed for thee, that thy faith fail not: and when thou art converted, strengthen thy brethren
Luke 22:61|the Lord turned, and looked upon Peter
Mark 5:18|prayed him that he might be with him
Mark 5:19|Go home to thy friends, and tell them how great things the Lord hath done for thee
Mark 5:20|began to publish in Decapolis
Mark 12:40|Which devour widows' houses
Mark 12:43|this poor widow hath cast more in
Mark 12:44|all that she had, even all her living
Luke 24:16|their eyes were holden
Luke 24:31|their eyes were opened, and they knew him
Genesis 3:7|the eyes of them both were opened, and they knew that they were naked
Luke 24:28|he made as though he would have gone further
Luke 24:27|in all the scriptures the things concerning himself
Luke 24:50|he lifted up his hands, and blessed them
Luke 24:51|while he blessed them, he was parted from them
Leviticus 9:22|Aaron lifted up his hand toward the people, and blessed them
Hebrews 7:25|he ever liveth to make intercession for them
"""
ok = bad = 0
for line in Q.strip().splitlines():
    ref, q = line.split("|", 1)
    good, t = check(ref, q)
    ok += good; bad += (not good)
    print(("OK      " if good else "MISMATCH"), ref, "|", q, ("" if good else "\n          REAL: " + t[:400]))
print(f"\nTOTAL {ok+bad}  OK {ok}  MISMATCH {bad}")

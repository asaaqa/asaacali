#ㅌㄹ호우아ㅜ우우웅 asaaqalialtweel
#سورس الامبراطوراليسع #سورس الأمبرو بلاي.
"""
◈ **قائمة النداء والمنشن **

• `{i}ن مميز`
    ❂ : لعمل نداء للاعضاء الأكثر تفاعلا بالجروب .

• `{i}ن المشرفين`
    ❂ : لعمل نداء لمشرفين بالجروب.

• `{i}ناديني`
    نداء باسم المطور

• `{i}ن بوت`
    نداء باسماء البوتات المضافه بالجروب.

• `{i}ننشط`
    وضع علامة على الأعضاء النشطين مؤخرًا.i.

• `{i}نon`
    وضع علامه على الاعضاء الفاتحين

• `{i}نoff`
    وضع علامه على الاعضاء الغير نشيطين
"""

from telethon.tl.types import ChannelParticipantAdmin as admin
from telethon.tl.types import ChannelParticipantCreator as owner
from telethon.tl.types import UserStatusOffline as off
from telethon.tl.types import UserStatusOnline as onn
from telethon.tl.types import UserStatusRecently as rec

from . import inline_mention, kazu_cmd


@kazu_cmd(
    pattern="ن(on|off| مميز| بوت|نشط| المشرفين|اديني)( (.*)|$)",
    groups_only=True,
)
async def _(e):
    okk = e.text
    lll = e.pattern_match.group(2)
    o = 0
    nn = 0
    rece = 0
    xx = f"{lll}" if lll else ""
    lili = await e.client.get_participants(e.chat_id, limit=99)
    for bb in lili:
        x = bb.status
        y = bb.participant
        if isinstance(x, onn):
            o += 1
            if "on" in okk:
                xx += f"\n{inline_mention(bb)}"
        elif isinstance(x, off):
            nn += 1
            if "off" in okk and not bb.bot and not bb.deleted:
                xx += f"\n{inline_mention(bb)}"
        elif isinstance(x, rec):
            rece += 1
            if "نشط" in okk and not bb.bot and not bb.deleted:
                xx += f"\n{inline_mention(bb)}"
        if isinstance(y, owner):
            xx += f"\n◈{inline_mention(bb)}"
        if isinstance(y, admin) and "admin" in okk and not bb.deleted:
            xx += f"\n{inline_mention(bb)}"
        if " مميز" in okk and not bb.bot and not bb.deleted:
            xx += f"\n{inline_mention(bb)}"
        if " بوت" in okk and bb.bot:
            xx += f"\n{inline_mention(bb)}"
    await e.eor(xx)

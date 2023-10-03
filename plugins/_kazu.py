# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.

from telethon.errors import (
    BotMethodInvalidError,
    ChatSendInlineForbiddenError,
    ChatSendMediaForbiddenError,
)

from . import LOG_CHANNEL, LOGS, Button, asst, kazu_cmd, eor, get_string

REPOMSG = """
◈ **𝗦𝗢𝗨𝗥𝗖𝗘 𝗔𝗠𝗕𝗥𝗔 𖠒​** ◈\n
◈ للتنصيب - [أضغط هنا](https://github.com/ionmusic/Kazu-Ubot)
◈ إضافات - [اضغط هنا](https://github.com/ionmusic/addons)
◈ السورس - @Mlze1bot
"""

RP_BUTTONS = [
    [
        Button.url(get_string("bot_3"), "https://github.com/asaaqa/Kazu-Ubot"),
        Button.url("السورس", "https://github.com/asaaq/Addons"),
    ],
    [Button.url("قناة السورس", "t.me/Mlze1bot")],
]

KAZUSTRING = """** شكرًا لنشر 𝗦𝗢𝗨𝗥𝗖𝗘 𝗔𝗠𝗕𝗥𝗔 𖠒!** • إليك بعض الأشياء الأساسية التي يمكنك من خلالها التعرف على كيفية استخدامها.."""


@kazu_cmd(
    pattern="تنصيب$",
    manager=True,
)
async def repify(e):
    try:
        q = await e.client.inline_query(asst.me.username, "")
        await q[0].click(e.chat_id)
        return await e.delete()
    except (
        ChatSendInlineForbiddenError,
        ChatSendMediaForbiddenError,
        BotMethodInvalidError,
    ):
        pass
    except Exception as er:
        LOGS.info(f"Error while repo command : {str(er)}")
    await e.eor(REPOMSG)


@kazu_cmd(pattern="امبرو$")
async def useAyra(rs):
    button = Button.inline("Start >>", "initft_2")
    msg = await asst.send_message(
        LOG_CHANNEL,
        KAZUSTRING,
        file="https://graph.org/file/b23bdfbaa9a7c650f9383.jpg",
        buttons=button,
    )
    if not (rs.chat_id == LOG_CHANNEL and rs.client._bot):
        await eor(rs, f"**[Click Here]({msg.message_link})**")

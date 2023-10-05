# asaaqa   -  asaacali 
# Copyright (C) 2023-2024 senpai80
#
#asaaq ali altweel -   asaaqa  - asaacali 
#sorec ambro 
#The source has been Arabized into Arabic with the rights of Elisha Ishaq 

from datetime import datetime

from pytz import timezone as tz
from telethon import Button, events
from telethon.errors.rpcerrorlist import MessageDeleteForbiddenError
from telethon.utils import get_display_name

from Kazu._misc import SUDO_M, owner_and_sudos
from Kazu.dB.asst_fns import *
from Kazu.fns.helper import inline_mention
from strings import get_string

from . import *

Owner_info_msg = udB.get_key("BOT_INFO_START")
custom_info = True
if Owner_info_msg is None:
    custom_info = False
    Owner_info_msg = f"""
**Owner** - {OWNER_NAME}
**OwnerID** - `{OWNER_ID}`

**Message Forwards** - {udB.get_key("PMBOT")}

**◈ ѕᴏʀᴄᴇ ᴀᴍʙʀᴏ 𓅛​ ◈ [v{kazu_version}](https://github.com/asaaqa/asaacali), powered by @ASAKIOP**
"""


_settings = [
    [
        Button.inline("فارات الأيبي", data="cbs_apiset"),
        Button.inline("اعدادات البوت", data="cbs_chatbot"),
    ],
    [
        Button.inline("اعدادات الفحص", data="cbs_alvcstm"),
        Button.inline("الحماية خاص", data="cbs_ppmset"),
    ],
    [
        Button.inline("الفــارات", data="cbs_otvars"),
        Button.inline("بوت الاغاني", data="cbs_vcb"),
    ],
    [Button.inline("« رجوع", data="mainmenu")],
]

_start = [
    [
        Button.inline("اللغه 🌐", data="lang"),
        Button.inline("ترتيب ⚙️", data="setter"),
    ],
    [
        Button.inline("الأحصائيات ✨", data="stat"),
        Button.inline("إذاعة رساله 📻", data="bcast"),
    ],
    [Button.inline("المنطقة الزمنيه 🌎", data="tz")],
]


@callback("ownerinfo")
async def own(event):
    msg = Owner_info_msg.format(
        mention=event.sender.mention, me=inline_mention(kazu_bot.me)
    )
    if custom_info:
        msg += "\n\n• مشغل بواسطة **@ASAKIOP**"
    await event.edit(
        msg,
        buttons=[Button.inline("إغلاق", data="closeit")],
        link_preview=False,
    )


@callback("closeit")
async def closet(lol):
    try:
        await lol.delete()
    except MessageDeleteForbiddenError:
        await lol.answer("MESSAGE_TOO_OLD", alert=True)


@asst_cmd(pattern="start( (.*)|$)", forwards=False, func=lambda x: not x.is_group)
async def ayra(event):
    args = event.pattern_match.group(1).strip()
    if not is_added(event.sender_id) and event.sender_id not in owner_and_sudos():
        add_user(event.sender_id)
        kak_uiw = udB.get_key("OFF_START_LOG")
        if not kak_uiw or kak_uiw != True:
            msg = f"{inline_mention(event.sender)} `[{event.sender_id}]` started your [Assistant bot](@{asst.me.username})."
            buttons = [[Button.inline("Info", "itkkstyo")]]
            if event.sender.username:
                buttons[0].append(
                    Button.mention(
                        "User", await event.client.get_input_entity(event.sender_id)
                    )
                )
            await event.client.send_message(
                udB.get_key("LOG_CHANNEL"), msg, buttons=buttons
            )
    if event.sender_id not in SUDO_M.fullsudos:
        ok = ""
        me = inline_mention(kazu_bot.me)
        mention = inline_mention(event.sender)
        if args and args != "set":
            await get_stored_file(event, args)
        if not udB.get_key("STARTMSG"):
            if udB.get_key("PMBOT"):
                ok = "❂ : يمكنك التواصل مع مطوري من خلال هاذا البوت!!\n\n❂ : أرسل رسالتك، وسأقوم بتسليمها إلى سيدي ."
            await event.reply(
                f"❂ :**مرحبا عزيزي **{mention}, ❂ :**هاذا هو البوت المساعد الخاص بـ **{me}!\n\n{ok}",
                file=udB.get_key("STARTMEDIA"),
                buttons=[Button.inline("Info.", data="ownerinfo")]
                if Owner_info_msg
                else None,
            )
        else:
            await event.reply(
                udB.get_key("STARTMSG").format(me=me, mention=mention),
                file=udB.get_key("STARTMEDIA"),
                buttons=[Button.inline("Info.", data="ownerinfo")]
                if Owner_info_msg
                else None,
            )
    else:
        name = get_display_name(event.sender)
        if args == "set":
            await event.reply(
                "اختر من الخيارات أدناه -",
                buttons=_settings,
            )
        elif args:
            await get_stored_file(event, args)
        else:
            await event.reply(
                get_string("ast_3").format(name),
                buttons=_start,
            )


@callback("itkkstyo", owner=True)
async def ekekdhdb(e):
    text = f"عندما يزور الزائر الجديد الروبوت المساعد الخاص بك. سوف تحصل على رسالة السجل هذه!\n\nTo Disable : {HNDLR}setdb OFF_START_LOG True"
    await e.answer(text, alert=True)


@callback("mainmenu", owner=True, func=lambda x: not x.is_group)
async def ayra(event):
    await event.edit(
        get_string("ast_3").format(OWNER_NAME),
        buttons=_start,
    )


@callback("stat", owner=True)
async def botstat(event):
    ok = len(get_all_users("BOT_USERS"))
    msg = """Kazu Assistant - Stats
Total Users - {}""".format(
        ok,
    )
    await event.answer(msg, cache_time=0, alert=True)


@callback("bcast", owner=True)
async def bdcast(event):
    ok = get_all_users("BOT_USERS")
    await event.edit(f"• Broadcast to {len(ok)} users.")
    async with event.client.conversation(OWNER_ID) as conv:
        await conv.send_message(
            "أدخل رسالة الاذاعه الخاصة بك.\n او استخدم /cancel لإيقاف  الأذاعه.",
        )
        response = await conv.get_response()
        if response.message == "/cancel":
            return await conv.send_message("تم الإلغاء!!")
        success = 0
        fail = 0
        await conv.send_message(f"تم بدء الاذاعه لـ {len(ok)} users...")
        start = datetime.now()
        for i in ok:
            try:
                await asst.send_message(int(i), response)
                success += 1
            except BaseException:
                fail += 1
        end = datetime.now()
        time_taken = (end - start).seconds
        await conv.send_message(
            f"""
**اكتمل البث خلال {time_taken} ثانية.**
إجمالي المستخدمين في البوت- {len(ok)}
**أرسلت إلى** : `{success} users.`
**فشل لـ** : `{fail} user(s).`""",
        )


@callback("setter", owner=True)
async def setting(event):
    await event.edit(
        "اختر من الخيارات أدناه -",
        buttons=_settings,
    )


@callback("tz", owner=True)
async def timezone_(event):
    await event.delete()
    pru = event.sender_id
    var = "TIMEZONE"
    name = "Timezone"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            "أرسل منطقتك الزمنية من هذه القائمة[Check From Here](http://www.timezoneconverter.com/cgi-bin/findzone.tzc)"
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message(
                "تم الإلغاء!!",
                buttons=get_back_button("mainmenu"),
            )
        try:
            tz(themssg)
            await setit(event, var, themssg)
            await conv.send_message(
                f"{name} تغير إلى {themssg}\n",
                buttons=get_back_button("mainmenu"),
            )
        except BaseException:
            await conv.send_message(
                "المنطقة الزمنية خاطئة، حاول مرة أخرى",
                buttons=get_back_button("mainmenu"),
            )

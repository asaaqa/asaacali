# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.

import asyncio
import os, shutil
import random
import time
from random import randint

try:
    from pytz import timezone
except ImportError:
    timezone = None

from telethon.errors import (
    ChannelsTooMuchError,
    ChatAdminRequiredError,
    MessageIdInvalidError,
    MessageNotModifiedError,
    UserNotParticipantError,
)
from telethon.tl.custom import Button
from telethon.tl.functions.channels import (
    CreateChannelRequest,
    EditAdminRequest,
    EditPhotoRequest,
    InviteToChannelRequest,
)
from telethon.tl.functions.contacts import UnblockRequest
from telethon.tl.types import (
    ChatAdminRights,
    ChatPhotoEmpty,
    InputChatUploadedPhoto,
    InputMessagesFilterDocument,
)
from telethon.utils import get_peer_id

from .. import LOGS, KazuConfig
from ..fns.helper import download_file, inline_mention, updater

db_url = 0


async def autoupdate_local_database():
    from .. import asst, udB, kazu_bot, Var

    global db_url
    if db_url := (
        udB.get_key("TGDB_URL")
        or Var.TGDB_URL
        or kazu_bot._cache.get("TGDB_URL")
    ):
        _split = db_url.split("/")
        _channel = _split[-2]
        _id = _split[-1]
        try:
            await asst.edit_message(
                int(_channel) if _channel.isdigit() else _channel,
                message=_id,
                file="database.json",
                text="**لا تقم بحذف هذا الملف.**",
            )
        except MessageNotModifiedError:
            return
        except MessageIdInvalidError:
            pass
    try:
        LOG_CHANNEL = (
            udB.get_key("LOG_CHANNEL")
            or Var.LOG_CHANNEL
            or asst._cache.get("LOG_CHANNEL")
            or "me"
        )
        msg = await asst.send_message(
            LOG_CHANNEL, "**لا تقم بحذف هذا الملف.**", file="database.json"
        )
        asst._cache["TGDB_URL"] = msg.message_link
        udB.set_key("TGDB_URL", msg.message_link)
    except Exception as ex:
        LOGS.error(f"Error on autoupdate_local_database: {ex}")


def update_envs():
    """تحديث فارات قاعدة بيانات udB"""
    from .. import udB

    for envs in list(os.environ):
        if envs in ["LOG_CHANNEL", "BOT_TOKEN"] or envs in udB.keys():
            udB.set_key(envs, os.environ[envs])


async def startup_stuff():
    from .. import udB

    x = ["resources/auth", "resources/downloads"]
    for x in x:
        if not os.path.isdir(x):
            os.mkdir(x)

    if CT := udB.get_key("CUSTOM_THUMBNAIL"):
        path = "resources/extras/thumbnail.jpg"
        KazuConfig.thumb = path
        try:
            await download_file(CT, path)
        except Exception as er:
            LOGS.exception(er)
    elif CT is False:
        KazuConfig.thumb = None
    if GT := udB.get_key("GDRIVE_AUTH_TOKEN"):
        with open("resources/auth/gdrive_creds.json", "w") as t_file:
            t_file.write(GT)

    if udB.get_key("AUTH_TOKEN"):
        udB.del_key("AUTH_TOKEN")

    MM = udB.get_key("MEGA_MAIL")
    MP = udB.get_key("MEGA_PASS")
    if MM and MP:
        with open(".megarc", "w") as mega:
            mega.write(f"[Login]\nUsername = {MM}\nPassword = {MP}")

    TZ = udB.get_key("TIMEZONE")
    if TZ and timezone:
        try:
            timezone(TZ)
            os.environ["TZ"] = TZ
            time.tzset()
        except AttributeError as er:
            LOGS.debug(er)
        except BaseException:
            LOGS.critical(
                "منطقة زمنية خاطئة"
            )
            os.environ["TZ"] = "UTC"
            time.tzset()


async def autobot():
    from .. import udB, kazu_bot

    if udB.get_key("BOT_TOKEN"):
        return
    await kazu_bot.start()
    LOGS.info("إنشاء روبوت Telegram لك على @BotFather، برجاء الانتظار")
    who = kazu_bot.me
    name = f"{who.first_name}' Bot"
    if who.username:
        username = f"{who.username}_bot"
    else:
        username = f"kazu_{str(who.id)[5:]}_bot"
    bf = "@BotFather"
    await kazu_bot(UnblockRequest(bf))
    await kazu_bot.send_message(bf, "/cancel")
    await asyncio.sleep(1)
    await kazu_bot.send_message(bf, "/newbot")
    await asyncio.sleep(1)
    isdone = (await kazu_bot.get_messages(bf, limit=1))[0].text
    if isdone.startswith("لا أستطيع أن أفعل.") or "20 bots" in isdone:
        LOGS.critical(
            "الرجاء إنشاء روبوت من @BotFather وإضافة الرمز المميز الخاص به في BOT_TOKEN، مثل env var ثم أعد تشغيلي."
        )
        import sys

        sys.exit(1)
    await kazu_bot.send_message(bf, name)
    await asyncio.sleep(1)
    isdone = (await kazu_bot.get_messages(bf, limit=1))[0].text
    if not isdone.startswith("Good."):
        await kazu_bot.send_message(bf, "My Assistant Bot")
        await asyncio.sleep(1)
        isdone = (await kazu_bot.get_messages(bf, limit=1))[0].text
        if not isdone.startswith("Good."):
            LOGS.critical(
                "الرجاء إنشاء روبوت من @BotFather وإضافة الرمز المميز الخاص به في BOT_TOKEN، مثل env var ثم أعد تشغيلي."
            )
            import sys

            sys.exit(1)
    await kazu_bot.send_message(bf, username)
    await asyncio.sleep(1)
    isdone = (await kazu_bot.get_messages(bf, limit=1))[0].text
    await kazu_bot.send_read_acknowledge("botfather")
    if isdone.startswith("Sorry,"):
        ran = randint(1, 100)
        username = f"kazu_{str(who.id)[6:]}{ran}_bot"
        await kazu_bot.send_message(bf, username)
        await asyncio.sleep(1)
        isdone = (await kazu_bot.get_messages(bf, limit=1))[0].text
    if isdone.startswith("Done!"):
        token = isdone.split("`")[1]
        udB.set_key("BOT_TOKEN", token)
        await enable_inline(kazu_bot, username)
        LOGS.info(
            f"انتهى. تم بنجاح إنشاء @{username} لاستخدامه كروبوت مساعد!"
        )
    else:
        LOGS.info(
            "يرجى حذف بعض روبوتات Telegram الخاصة بك فيBotfather أو تعيين Var BOT_TOKEN باستخدام توكن اي بوت خاص بك"
        )

        import sys

        sys.exit(1)


async def autopilot():
    from .. import asst, udB, kazu_bot

    channel = udB.get_key("LOG_CHANNEL")
    new_channel = None
    if channel:
        try:
            chat = await kazu_bot.get_entity(channel)
        except BaseException as err:
            LOGS.exception(err)
            udB.del_key("LOG_CHANNEL")
            channel = None
    if not channel:

        async def _save(exc):
            udB._cache["LOG_CHANNEL"] = kazu_bot.me.id
            await asst.send_message(
                kazu_bot.me.id, f"فشل في إنشاء قناة السجل بسبب {exc}.."
            )

        if kazu_bot._bot:
            msg_ = "'LOG_CHANNEL' tidak ditemukan! Tambahkan untuk digunakan 'BOTMODE'"
            LOGS.error(msg_)
            return await _save(msg_)
        LOGS.info("قم بانشاء قناة السجل الخاصه بك!")
        try:
            r = await kazu_bot(
                CreateChannelRequest(
                    title="سجلات أمبرو بلاك يوزر بوت",
                    about="سجلات أمبرو بلاك يوزر بوت \n\n قناة السورس @ASAAQALIO",
                    megagroup=True,
                ),
            )
        except ChannelsTooMuchError as er:
            LOGS.critical(
                "لديك قنوات او جروبات كثيره جدا احذف بعضها واعد تشغيل السورس "
            )
            return await _save(str(er))
        except BaseException as er:
            LOGS.exception(er)
            LOGS.info(
                "هناك خطأ ما، قم بإنشاء مجموعة وقم بتعيين الايدي في config var LOG_CHANNEL."
            )

            return await _save(str(er))
        new_channel = True
        chat = r.chats[0]
        channel = get_peer_id(chat)
        udB.set_key("LOG_CHANNEL", channel)
    assistant = True
    try:
        await kazu_bot.get_permissions(int(channel), asst.me.username)
    except UserNotParticipantError:
        try:
            await kazu_bot(InviteToChannelRequest(int(channel), [asst.me.username]))
        except BaseException as er:
            LOGS.info("حدث خطأ أثناء إضافة المساعد إلى قناة السجل")
            LOGS.exception(er)
            assistant = False
    except BaseException as er:
        assistant = False
        LOGS.exception(er)
    if assistant and new_channel:
        try:
            achat = await asst.get_entity(int(channel))
        except BaseException as er:
            achat = None
            LOGS.info("حدث خطأ أثناء الحصول على قناة السجل من المساعد")
            LOGS.exception(er)
        if achat and not achat.admin_rights:
            rights = ChatAdminRights(
                add_admins=True,
                invite_users=True,
                change_info=True,
                ban_users=True,
                delete_messages=True,
                pin_messages=True,
                anonymous=False,
                manage_call=True,
            )
            try:
                await kazu_bot(
                    EditAdminRequest(
                        int(channel), asst.me.username, rights, "Assistant"
                    )
                )
            except ChatAdminRequiredError:
                LOGS.info(
                    "Gagal mempromosikan 'Bot Asisten' di 'Log Channel' karena 'Hak Istimewa Admin'"
                )
            except BaseException as er:
                LOGS.info("حدث خطأ أثناء ترقية المساعد في قناة السجل..")
                LOGS.exception(er)
    if isinstance(chat.photo, ChatPhotoEmpty):
        photo = await download_file(
            "https://graph.org/file/a0be504365cce504260c1.jpg",
            "resources/extras/logo.jpg",
        )
        ll = await kazu_bot.upload_file(photo)
        try:
            await kazu_bot(
                EditPhotoRequest(int(channel), InputChatUploadedPhoto(ll))
            )
        except BaseException as er:
            LOGS.exception(er)
        os.remove(photo)


# customize assistant


async def customize():
    from .. import asst, udB, kazu_bot

    rem = None
    try:
        chat_id = udB.get_key("LOG_CHANNEL")
        if asst.me.photo:
            return
        LOGS.info("تخصيص الروبوت المساعد في @BOTFATHER")
        UL = f"@{asst.me.username}"
        if not kazu_bot.me.username:
            sir = kazu_bot.me.first_name
        else:
            sir = f"@{kazu_bot.me.username}"
        file = random.choice(
            [
                "https://graph.org/file/a0be504365cce504260c1.jpg",
                "resources/extras/logo.jpg",
            ]
        )
        if not os.path.exists(file):
            file = await download_file(file, "profile.jpg")
            rem = True
        msg = await asst.send_message(
            chat_id, "**الضبط التلقائي** بدأ @Botfathe"
        )
        await asyncio.sleep(1)
        await kazu_bot.send_message("botfather", "/cancel")
        await asyncio.sleep(1)
        await kazu_bot.send_message("botfather", "/setuserpic")
        await asyncio.sleep(1)
        isdone = (await kazu_bot.get_messages("botfather", limit=1))[0].text
        if isdone.startswith("Invalid bot"):
            LOGS.info("حدث خطأ أثناء محاولة تخصيص المساعد، والتخطي...")
            return
        await kazu_bot.send_message("botfather", UL)
        await asyncio.sleep(1)
        await kazu_bot.send_file("botfather", file)
        await asyncio.sleep(2)
        await kazu_bot.send_message("botfather", "/setabouttext")
        await asyncio.sleep(1)
        await kazu_bot.send_message("botfather", UL)
        await asyncio.sleep(1)
        await kazu_bot.send_message(
            "botfather", f"✨ مرحبا ✨!! انا بوت المساعد الخاص بــ of {sir}"
        )
        await asyncio.sleep(2)
        await kazu_bot.send_message("botfather", "/setdescription")
        await asyncio.sleep(1)
        await kazu_bot.send_message("botfather", UL)
        await asyncio.sleep(1)
        await kazu_bot.send_message(
            "botfather",
            f"✨ ربوت الأمبرو بلاك يوزر بوت ✨\n✨ Master ~ {sir} ✨\n\n✨ الأقوى على الأطلاق  ~ @Mlze1bot ✨",
        )
        await asyncio.sleep(2)
        await msg.edit("تم الانتهاء من **التخصيص التلقائي** في @BotFather.")
        if rem:
            os.remove(file)
        LOGS.info("تم التخصيص")
    except Exception as e:
        LOGS.exception(e)


async def plug(plugin_channels):
    from .. import kazu_bot
    from .utils import load_addons

    if kazu_bot._bot:
        LOGS.info("لا يمكن استخدام قنوات البرنامج المساعد في BOTMODE")
        return
    if os.path.exists("addons") and not os.path.exists("addons/.git"):
        shutil.rmtree("addons")
    if not os.path.exists("addons"):
        os.mkdir("addons")
    if not os.path.exists("addons/__init__.py"):
        with open("addons/__init__.py", "w") as f:
            f.write("from plugins import *\n\nbot = kazu_bot")
    LOGS.info("• Loading Plugins from Plugin Channel(s) •")
    for chat in plugin_channels:
        LOGS.info(f"{'•'*4} {chat}")
        try:
            async for x in kazu_bot.iter_messages(
                chat, search=".py", filter=InputMessagesFilterDocument, wait_time=10
            ):
                plugin = "addons/" + x.file.name.replace("_", "-").replace("|", "-")
                if not os.path.exists(plugin):
                    await asyncio.sleep(0.6)
                    if x.text == "#IGNORE":
                        continue
                    plugin = await x.download_media(plugin)
                try:
                    load_addons(plugin)
                except Exception as e:
                    LOGS.info(f"Kazu - PLUGIN_CHANNEL - ERROR - {plugin}")
                    LOGS.exception(e)
                    os.remove(plugin)
        except Exception as er:
            LOGS.exception(er)


# some stuffs


async def ready():
    from .. import asst, udB, kazu_bot
    from ..fns.tools import async_searcher

    chat_id = udB.get_key("LOG_CHANNEL")
    spam_sent = None
    if not udB.get_key("INIT_DEPLOY"):  # Detailed Message at Initial Deploy
        MSG = """ **شكرا لك لنشر سورس الأمبرو بلاك !**
• فيما يلي بعض الأشياء الأساسية التي يمكنك من خلالها التعرف على كيفية استخدام السورس ."""
        PHOTO = "https://graph.org/file/b23bdfbaa9a7c650f9383.jpg"
        BTTS = Button.inline("• Click to Start •", "initft_2")
        udB.set_key("INIT_DEPLOY", "Done")
    else:
        MSG = f"**تم تنصيب سورس الأمبرو بلاك!**\n➖➖➖➖➖➖➖➖➖➖\n**UserMode**: {inline_mention(kazu_bot.me)}\n**Assistant**: @{asst.me.username}\n➖➖➖➖➖➖➖➖➖➖\n**Support**: @Mlze1bot\n➖➖➖➖➖➖➖➖➖➖"
        BTTS, PHOTO = None, None
        if prev_spam := udB.get_key("LAST_UPDATE_LOG_SPAM"):
            try:
                await kazu_bot.delete_messages(chat_id, int(prev_spam))
            except Exception as E:
                LOGS.info(f"حدث خطأ أثناء حذف رسالة التحديث السابقة :{str(E)}")
        if await updater():
            BTTS = Button.inline("التحديث متاح", "updtavail")

    try:
        spam_sent = await asst.send_message(chat_id, MSG, file=PHOTO, buttons=BTTS)
    except ValueError as e:
        try:
            await (await kazu_bot.send_message(chat_id, str(e))).delete()
            spam_sent = await asst.send_message(chat_id, MSG, file=PHOTO, buttons=BTTS)
        except Exception as g:
            LOGS.info(g)
    except Exception as el:
        LOGS.info(el)
        try:
            spam_sent = await kazu_bot.send_message(chat_id, MSG)
        except Exception as ef:
            LOGS.info(ef)
    if spam_sent and not spam_sent.media:
        udB.set_key("LAST_UPDATE_LOG_SPAM", spam_sent.id)
    get_ = udB.get_key("OLDANN") or []
"""
    try:
        updts = await async_searcher(
            "https://ultroid-api.vercel.app/announcements", post=True, re_json=True
        )
        for upt in updts:
            key = list(upt.keys())[0]
            if key not in get_:
                cont = upt[key]
                if isinstance(cont, str):
                    await asst.send_message(chat_id, cont)
                elif isinstance(cont, dict) and cont.get("chat"):
                    await asst.forward_messages(chat_id, cont["msg_id"], cont["chat"])
                else:
                    LOGS.info(cont)
                    LOGS.info(
                        "تم اكتشاف نوع إعلان غير صالح!\nتأكد من أنك تستخدم الإصدار الأحدث.."
                    )
                get_.append(key)
        udB.set_key("OLDANN", get_)
    except Exception as er:
        LOGS.exception(er)
"""

async def WasItRestart(udb):
    key = udb.get_key("_RESTART")
    if not key:
        return
    from .. import asst, kazu_bot

    try:
        data = key.split("_")
        who = asst if data[0] == "bot" else kazu_bot
        await who.edit_message(
            int(data[1]), int(data[2]), "__تمت اعادة التشغيل بنجاح.__"
        )
    except Exception as er:
        LOGS.exception(er)
    udb.del_key("_RESTART")


def _version_changes(udb):
    for _ in [
        "BOT_USERS",
        "BOT_BLS",
        "VC_SUDOS",
        "SUDOS",
        "CLEANCHAT",
        "LOGUSERS",
        "PLUGIN_CHANNEL",
        "CH_SOURCE",
        "CH_DESTINATION",
        "BROADCAST",
    ]:
        key = udb.get_key(_)
        if key and str(key)[0] != "[":
            key = udb.get(_)
            new_ = [
                int(z) if z.isdigit() or (z.startswith("-") and z[1:].isdigit()) else z
                for z in key.split()
            ]
            udb.set_key(_, new_)


async def enable_inline(kazu_bot, username):
    bf = "BotFather"
    await kazu_bot.send_message(bf, "/setinline")
    await asyncio.sleep(1)
    await kazu_bot.send_message(bf, f"@{username}")
    await asyncio.sleep(1)
    await kazu_bot.send_message(bf, "Search")
    await kazu_bot.send_read_acknowledge(bf)

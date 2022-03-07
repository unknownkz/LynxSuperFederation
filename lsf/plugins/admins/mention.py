import asyncio
import logging
import os

from telethon import Button, TelegramClient, events
from telethon.errors import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator

from ... import lynx_client
from ...handlers.altaraction import commands_functions
from ..disable import DisableAbleCommandHandler

spam_chats = []


@lynx_client.on(events.NewMessage(pattern=r"^[.$!/;@]all ?(.*)"))
@commands_functions
async def all(event):
    chat_id = event.chat_id
    if event.is_private:
        return await event.respond("This command can be use in groups and channels!")

    is_admin = False
    try:
        partici_ = await lynx_client(GetParticipantRequest(event.chat_id, event.sender_id))
    except UserNotParticipantError:
        is_admin = False
    else:
        if isinstance(partici_.participant, (ChannelParticipantAdmin, ChannelParticipantCreator)):
            is_admin = True
    if not is_admin:
        return await event.respond("Only admins can mention all!")

    if event.pattern_match.group(1) and event.is_reply:
        return await event.respond("Give me one argument!")
    elif event.pattern_match.group(1):
        mode = "text_on_cmd"
        msg = event.pattern_match.group(1)
    elif event.is_reply:
        mode = "text_on_reply"
        msg = await event.get_reply_message()
        if msg == None:
            return await event.respond(
                "I can't mention members for older messages! (messages which are sent before I'm added to group)"
            )
    else:
        return await event.respond("Reply to a message or give me some text to mention others!")

    Spam = spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in lynx_client.iter_participants(chat_id):
        if not chat_id in spam_chats:
            break
        usrnum += 1
        usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
        if usrnum == 5:
            if mode == "text_on_cmd":
                txt = f"{usrtxt}\n\n{msg}"
                await lynx_client.send_message(chat_id, txt)
            elif mode == "text_on_reply":
                await msg.reply(usrtxt)
            await asyncio.sleep(2)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@lynx_client.on(events.NewMessage(pattern=r"^[.$!/;@]cancel$"))
@commands_functions
async def cancel(event):
    if not event.chat_id in spam_chats:
        return await event.respond("There is no proccess on going...")
    else:
        try:
            spam_chats.remove(event.chat_id)
        except:
            pass
        return await event.respond("Stopped.")


__help__ = """
*Mention Member*

 • /all <sometext> : mention all member
 • /cancel : canceled ur mention

Variable Pattern : $  !  /  ;  .  @

*Example:*
$all  !all  /all  ;all  .all  @all
 """

__mod_name__ = "Mentions"

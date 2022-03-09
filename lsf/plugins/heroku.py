import asyncio
import html
import math
import os
import subprocess
import heroku3
import requests
from datetime import datetime as wkt
from telegram import ParseMode

from .. import HEROKU_APP_NAME, HEROKU_API_KEY, OWNER_ID, TimeZone, EVENT_LOGS
from ..events import register
from ..handlers.valid import dev_plus
from .commander import Lynxcmd

heroku_api = "https://api.heroku.com"
Heroku = heroku3.from_key(HEROKU_API_KEY)


@dev_plus
@register(pattern=r"^[.$!/;@](set|see|del) env(?: |$)(.*)(?: |$)([\s\S]*)")
async def variable(var):
    if var.fwd_from:
        return
    if var.sender_id == OWNER_ID:
        pass
    else:
        return
    """
    Manage most of ENV setting, set new env var, get current env var,
    or delete env var...
    """
    if HEROKU_APP_NAME is not None:
        app = Heroku.app(HEROKU_APP_NAME)
    else:
        return await var.reply("`[HEROKU]:" "\nPlease setup your` **HEROKU_APP_NAME**")
    exe = var.pattern_match.group(1)
    heroku_var = app.config()
    if exe == "see":
        k = await var.reply("`Getting information...`")
        await asyncio.sleep(1.5)
        try:
            variable = var.pattern_match.group(2).split()[0]
            if variable in heroku_var:
                return await k.edit("**Environments**:" f"\n\n`{variable} = {heroku_var[variable]}`\n")
            else:
                return await k.edit("**Environments**:" f"\n\n`Error:\n-> {variable} don't exists`")
        except IndexError:
            configs = prettyjson(heroku_var.to_dict(), indent=2)
            with open("configs.json", "w") as fp:
                fp.write(configs)
            with open("configs.json", "r") as fp:
                result = fp.read()
                if len(result) >= 4096:
                    await var.client.send_file(
                        var.chat_id,
                        "configs.json",
                        reply_to=var.id,
                        caption="`Output too large, sending it as a file`",
                    )
                else:
                    await k.edit(
                        "`[HEROKU]` ConfigVars:\n\n"
                        "================================"
                        f"\n```{result}```\n"
                        "================================"
                    )
            os.remove("configs.json")
            return
    elif exe == "set":
        s = await var.reply("Setting information...")
        variable = var.pattern_match.group(2)
        if not variable:
            return await s.edit(">`.set env <ENV> <VALUE>`")
        value = var.pattern_match.group(3)
        if not value:
            variable = variable.split()[0]
            try:
                value = var.pattern_match.group(2).split()[1]
            except IndexError:
                return await s.edit(">`/set env <ENV> <VALUE>`")
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await s.edit(f"Environments **{variable}**\n`Successfully changed to`  ->  **{value}**")
        else:
            await s.edit(f"Environments **{variable}**\n`Successfully added to`  ->  **{value}**")
        heroku_var[variable] = value
    elif exe == "del":
        m = await var.reply("`Getting information to deleting env var...`")
        try:
            variable = var.pattern_match.group(2).split()[0]
        except IndexError:
            return await m.edit("`Please Specify ENV Variabel you want to delete`")
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await m.edit(f"`Environments` **{variable}**\n`Successfully deleted`")
            del heroku_var[variable]
        else:
            return await m.edit(f"`Environments` **{variable}** `is not exists`")


@dev_plus
@register(pattern=r"^[.$!/;@]usage(?: |$)")
async def dyno_usage(view):
    if view.fwd_from:
        return
    if view.sender_id == OWNER_ID:
        pass
    else:
        return
    """
    Get your account Dyno Usage
    """
    ur = await view.reply("`Processing...`")
    useragent = (
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/80.0.3987.149 Mobile Safari/537.36"
    )
    user_id = Heroku.account().id
    headers = {
        "User-Agent": useragent,
        "Authorization": f"Bearer {HEROKU_API_KEY}",
        "Accept": "application/vnd.heroku+json; version=3.account-quotas",
    }
    path = "/accounts/" + user_id + "/actions/get-quota"
    kz = requests.get(heroku_api + path, headers=headers)
    if kz.status_code != 200:
        return await ur.edit("`Error: something bad happened`\n\n" f">.`{kz.reason}`\n")
    result = kz.json()
    quota = result["account_quota"]
    quota_used = result["quota_used"]

    """ - Used - """
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)
    day = math.floor(hours / 24)

    """ - Current - """
    App = result["apps"]
    try:
        App[0]["quota_used"]
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]["quota_used"] / 60
        AppPercentage = math.floor(App[0]["quota_used"] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)
    await asyncio.sleep(1.5)

    return await ur.edit(
        "🚦 **Dyno Usage ** 🚦\n\n"
        f" » Dyno usage for **{HEROKU_APP_NAME}**:\n"
        f"      •  `{AppHours}`**h**  `{AppMinutes}`**m**  "
        f"**|**  [`{AppPercentage}`**%**]"
        "\n\n"
        "  » Dyno hours quota remaining this month:\n"
        f"      •  `{hours}`**h**  `{minutes}`**m**  "
        f"**|**  [`{percentage}`**%**]"
        f"\n\n  » Dynos heroku {day} days left"
    )


@dev_plus
@register(pattern=r"^[.$!/;@]logs$")
async def _(view):
    if view.fwd_from:
        return
    if view.sender_id == OWNER_ID:
        pass
    else:
        return
    try:
        Heroku = heroku3.from_key(HEROKU_API_KEY)
        app = Heroku.app(HEROKU_APP_NAME)
    except:
        return await view.reply(
            " Please make sure your Heroku API Key, Your App name are configured correctly in the heroku"
        )
    kz = await view.reply("Getting Logs....")
    with open("logs.txt", "w") as log:
        log.write(app.get_log())
    await kz.edit("Got the logs wait a sec")
    await view.client.send_file(
        view.chat_id,
        "logs.txt",
        reply_to=view.id,
        caption="`LSF Logs`",
    )

    await asyncio.sleep(5)
    await view.client.delete(kz)
    return os.remove("logs.txt")


def prettyjson(obj, indent=2, maxlinelength=80):
    """Renders JSON content with indentation and line splits/concatenations to fit maxlinelength.
    Only dicts, lists and basic types are supported"""

    items, _ = getsubitems(
        obj,
        itemkey="",
        islast=True,
        maxlinelength=maxlinelength - indent,
        indent=indent,
    )
    return indentitems(items, indent, level=0)


@dev_plus
@Lynxcmd("gitpull")
def gitpull(update, context):
    sent_msg = update.effective_message.reply_text("Pulling all changes from remote...")
    subprocess.Popen("git pull", stdout=subprocess.PIPE, shell=True)

    sent_msg_text = sent_msg.text + "\n\nChanges pulled... I guess..\nContinue to restart with /reboot "
    sent_msg.edit_text(sent_msg_text)


@dev_plus
@Lynxcmd("reboot")
def restart(update, context):
    user = update.effective_message.from_user

    update.effective_message.reply_text("Starting a new instance and shutting down this one")

    if EVENT_LOGS:
        ft = "Date : %d/%m/%Y\nTime : %H:%M WIB"
        time_c = wkt.now(TimeZone).strftime(ft)
        message = (
            f"<b>Bot Restarted </b>"
            f"<b>By :</b> <code>{html.escape(user.first_name)}</code>"
            f"<b>\n\nCurrent Time</b>\n<code>{time_c}</code>"
        )
        context.bot.send_message(
            chat_id=EVENT_LOGS,
            text=message,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )

    os.system("bash startapp")

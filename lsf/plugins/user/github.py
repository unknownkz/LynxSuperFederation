import requests

from ...handlers.decorators import Lynxcmd
from telegram import Update, ParseMode
from telegram.ext import CallbackContext


@Lynxcmd("github", pass_args=True)
def github(update: Update, context: CallbackContext):
    bot = context.bot
    message = update.effective_message
    args = message.text.split(" ", 1)

    if len(args) == 1:
        message.reply_text("Provide me Username, Ex - /git unknownkz")
        return
    else:
        pass
    username = args[1]
    URL = f"https://api.github.com/users/{username}"
    with requests.get(URL) as request:
        if request.status_code == 404:
            return message.reply_text("404")

        result = request.json()
        try:
            url = result["html_url"]
            name = result["name"]
            company = result["company"]
            bio = result["bio"]
            created_at = result["created_at"]
            avatar_url = result["avatar_url"]
            blog = result["blog"]
            location = result["location"]
            repositories = result["public_repos"]
            followers = result["followers"]
            following = result["following"]
            caption = f"""**Info Of {name}**
**Username:** `{username}`
**Bio:** `{bio}`
**Profile Link:** [Here]({url})
**Company:** `{company}`
**Created On:** `{created_at}`
**Repositories:** `{repositories}`
**Blog:** `{blog}`
**Location:** `{location}`
**Followers:** `{followers}`
**Following:** `{following}`"""
        except Exception as e:
            print(str(e))
            pass
    message.reply_photo(
        photo=avatar_url, caption=caption, parse_mode=ParseMode.MARKDOWN
    )


__mod_name__ = "Github"

__help__ = """
Get Your Github Profile Information by using this Command

 • /github unknownkz

will send profile of your github account.
"""

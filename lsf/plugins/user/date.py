import calendar
from datetime import datetime as wkt

from telegram import Update, ParseMode
from telegram.ext import CallbackContext

from ... import TimeZone
from ..commander import Lynxcmd


@Lynxcmd("calendar")
def tanggaldanwaktu(update: Update, context: CallbackContext):
    lyn = context.bot
    message = update.effective_message
    m = wkt.now().month
    y = wkt.now().year
    d = wkt.now(TimeZone).strftime("Date : %d/%m/%Y\nTime : %H:%M WIB")
    k = calendar.month(y, m, 2, 1)
    bulan_waktu = (
        f"<strong><i>The calendar for this month is:</i></strong>\n\n" f"<code>{k}</code>\n\n" f"<code>{d}</code>"
    )
    message.reply_text(
        bulan_waktu,
        parse_mode=ParseMode.HTML,
    )


__mod_name__ = "Calendar"

__help__ = """
*Calendar*

Get current date, time and month information.

 • /calendar

Date information is for one month only.

( TimeZone : UTC+07:00 (ICT) )
"""

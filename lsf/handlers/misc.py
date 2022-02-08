from math import ceil
from typing import Dict, List

from telegram import MAX_MESSAGE_LENGTH, Bot, InlineKeyboardButton, ParseMode
from telegram.error import TelegramError

from lsf import NO_LOAD


class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text


def paginate_plugins(page_n: int, plugins_dict: Dict, prefix, chat=None) -> List:
    if not chat:
        plugins = sorted(
            [
                EqInlineKeyboardButton(
                    x.__mod_name__,
                    callback_data="{}_plugins({})".format(
                        prefix, x.__mod_name__.lower()
                    ),
                )
                for x in plugins_dict.values()
            ]
        )
    else:
        plugins = sorted(
            [
                EqInlineKeyboardButton(
                    x.__mod_name__,
                    callback_data="{}_plugins({},{})".format(
                        prefix, chat, x.__mod_name__.lower()
                    ),
                )
                for x in plugins_dict.values()
            ]
        )

    pairs = [plugins[i * 3 : (i + 1) * 3] for i in range((len(plugins) + 3 - 1) // 3)]

    round_num = len(plugins) / 3
    calc = len(plugins) - round(round_num)
    if calc == 1:
        pairs.append((plugins[-1],))
    elif calc == 2:
        pairs.append((plugins[-1],))

    max_num_pages = ceil(len(pairs) / 10)
    plug_page = page_n % max_num_pages

    # can only have a certain amount of buttons side by side
    if len(pairs) > 10:
        pairs = pairs[plug_page * 10 : 10 * (plug_page + 1)] + [
            (
                EqInlineKeyboardButton(
                    "⮜", callback_data="{}_prev({})".format(prefix, plug_page)
                ),
                EqInlineKeyboardButton("Back", callback_data="lynx_back"),
                EqInlineKeyboardButton(
                    "⮞", callback_data="{}_next({})".format(prefix, plug_page)
                ),
            )
        ]

    else:
        pairs += [[EqInlineKeyboardButton("Back", callback_data="lynx_back")]]

    return pairs


def build_keyboard(buttons):
    keyb = []
    for btn in buttons:
        if btn.same_line and keyb:
            keyb[-1].append(InlineKeyboardButton(btn.name, url=btn.url))
        else:
            keyb.append([InlineKeyboardButton(btn.name, url=btn.url)])

    return keyb


def revert_buttons(buttons):
    res = ""
    for btn in buttons:
        if btn.same_line:
            res += f"\n[{btn.name}](buttonurl://{btn.url}:same)"
        else:
            res += f"\n[{btn.name}](buttonurl://{btn.url})"

    return res


def build_keyboard_parser(bot, chat_id, buttons):
    keyb = []
    for btn in buttons:
        if btn.url == "{rules}":
            btn.url = "http://t.me/{}?start={}".format(bot.username, chat_id)
        if btn.same_line and keyb:
            keyb[-1].append(InlineKeyboardButton(btn.name, url=btn.url))
        else:
            keyb.append([InlineKeyboardButton(btn.name, url=btn.url)])

    return keyb


def send_to_list(
    bot: Bot,
    send_to: list,
    message: str,
    markdown=False,
    html=False,
) -> None:
    if html and markdown:
        raise Exception("Can only send with either markdown or HTML!")
    for user_id in set(send_to):
        try:
            if markdown:
                bot.send_message(user_id, message, parse_mode=ParseMode.MARKDOWN)
            elif html:
                bot.send_message(user_id, message, parse_mode=ParseMode.HTML)
            else:
                bot.send_message(user_id, message)
        except TelegramError:
            pass  # ignore users who fail


def split_message(msg: str) -> List[str]:
    if len(msg) < MAX_MESSAGE_LENGTH:
        return [msg]

    lines = msg.splitlines(True)
    small_msg = ""
    result = []
    for line in lines:
        if len(small_msg) + len(line) < MAX_MESSAGE_LENGTH:
            small_msg += line
        else:
            result.append(small_msg)
            small_msg = line
    # Else statement at the end of the for loop, so append the leftover string.
    result.append(small_msg)

    return result


def is_plugins_loaded(name):
    return name not in NO_LOAD

import html2text
from bs4 import BeautifulSoup
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext

from apps.common.utils.generate import generate_content

intro_text = (
    f"Welcome to Pen! 🐧 I'm excited to be your new AI writing assistant."  # noqa F541
    f" With me, you won't have to worry about tedious tasks like writing again. "
    f"I'm here to help you create content faster and more efficiently! 📝⚡️️\n\n️"
    f"Just tell me what you need written and I'll take care of the rest. Let's get started! 🚀"
)


def prettify(htmlstr):
    soup = BeautifulSoup(htmlstr, "html.parser")
    return soup.prettify()


def language(update: Update, context: CallbackContext):
    text = update.message.text
    if text == "🇷🇺Russian":
        buttons = [
            ["Вернуться в главное меню 🏠"],
        ]
        update.message.reply_text(
            f"Напишите тему вашего поста 📱\n\n" f"Максимальное количество символов 100 👇",  # noqa F541
            reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
        )
        lang = "607adc2f6f8fe5000c1e637a"
        context.user_data["lang"] = lang

    elif text == "🇺🇸English":
        buttons = [
            ["Return to main menu 🏠"],
        ]
        update.message.reply_text(
            f"Generate ideas & intro text for your social media posts 📱 \n\n"  # noqa F541
            f"Write the topic of your post, the maximum number of characters is 100 👇",
            reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
        )

        lang = "607adac76f8fe5000c1e636d"
        context.user_data["lang"] = lang

    return "GENERATE"


def generate(update: Update, context: CallbackContext):
    text = update.message.text
    if text == "Вернуться в главное меню 🏠" or text == "Return to main menu 🏠":
        buttons = [
            ["🇷🇺Russian", "🇺🇸English"],
        ]
        update.message.reply_text(
            f"Hello {update.message.from_user.first_name}! 🤗\n\n{intro_text}",
            reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
        )
        return "LANGUAGE"

    if len(text) < 100:
        response = generate_content(context.user_data["lang"], text)
        content = html2text.html2text(prettify(response["data"]["content"]))
        update.message.reply_text(f"{content}", parse_mode="HTML")
        return "START"
    else:
        update.message.reply_text(
            f"Oops, 100 characters is enough for me to create magic! 💫\n\n"
            f"Your text is {len(text)} characters, please try again 🙃\n\n"
            f"/start",
            reply_markup=ReplyKeyboardRemove(),
        )
        return "START"

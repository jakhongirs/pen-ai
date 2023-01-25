import environ
from django.core.management.base import BaseCommand
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, Filters, MessageHandler, Updater

from apps.bot.views import generate, language

env = environ.Env()
env.read_env(".env")

updater = Updater(env.str("tg_token"))

intro_text = (  # noqa F541
    f"Welcome to Pen! 🐧 I'm excited to be your new AI writing assistant."  # noqa F541
    f" With me, you won't have to worry about tedious tasks like writing again. "  # noqa F541
    f"I'm here to help you create content faster and more efficiently! 📝⚡️️\n\n️"  # noqa F541
    f"Just tell me what you need written and I'll take care of the rest. Let's get started! 🚀"  # noqa F541
)  # noqa F541


class Command(BaseCommand):
    help = "Bot"

    def handle(self, *args, **options):
        print("Hello World")

    def start(update: Update, context: CallbackContext):
        language_buttons = [
            ["🇷🇺Russian", "🇺🇸English"],
        ]
        update.message.reply_text(
            f"Hello {update.message.from_user.first_name}! 🤗\n\n{intro_text}",
            parse_mode="HTML",
            reply_markup=ReplyKeyboardMarkup(language_buttons, resize_keyboard=True),
        )
        return "LANGUAGE"

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            "LANGUAGE": [
                MessageHandler(Filters.regex("^(🇷🇺Russian|🇺🇸English)$"), language),
            ],
            "GENERATE": [
                MessageHandler(Filters.text, generate),
            ],
            "START": [
                MessageHandler(Filters.text, start),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    dispatcher = updater.dispatcher
    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

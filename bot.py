import os
from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ChatMemberHandler
from googletrans import Translator

# Redes oficiales permitidas
ALLOWED_LINKS = [
    "instagram.com/sushicoin_worldchain",
    "youtube.com/@sushicoin_worldchain",
    "tiktok.com/@sushicoin_worldchain",
    "facebook.com",
    "threads.net/@sushicoin_worldchain",
    "worldcoin.org/mini-app?app_id=app_189a4201231883859ea837ca1e41cd85"
]

translator = Translator()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 SushiCoin Bot activo.")

async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        welcome = f"👋 Welcome to the official SushiCoin community, {member.mention_html()}!"
        links = """🔗 Stay connected:
• Instagram: https://www.instagram.com/sushicoin_worldchain
• YouTube: https://youtube.com/@sushicoin_worldchain
• TikTok: https://www.tiktok.com/@sushicoin_worldchain
• Facebook: https://www.facebook.com/share/1BrdSxafAz/
• Threads: https://www.threads.net/@sushicoin_worldchain
• App: https://worldcoin.org/mini-app?app_id=app_189a4201231883859ea837ca1e41cd85"""
        translate_info = "🌍 Need translation? Reply any message with: /translate to Spanish (or any language)."
        await update.message.reply_html(welcome)
        await update.message.reply_text(links)
        await update.message.reply_text(translate_info)

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message and len(context.args) >= 2 and context.args[0] == "to":
        lang = context.args[1]
        text = update.message.reply_to_message.text
        if text:
            translated = translator.translate(text, dest=lang).text
            await update.message.reply_text(f"🔁 Translation ({lang}):{translated}")
        else:
            await update.message.reply_text("❗ Please reply to a text message.")
    else:
        await update.message.reply_text("Usage: /translate to <language> (reply to a message)")

async def filter_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    if "http" in text:
        if not any(link in text for link in ALLOWED_LINKS):
            try:
                await update.message.delete()
                await context.bot.send_message(chat_id=update.effective_chat.id, text="🚫 Only official SushiCoin links are allowed.")
            except:
                pass

def main():
    TOKEN = os.environ.get("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("translate", translate))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), filter_links))
    app.run_polling()

if __name__ == "__main__":
    main()

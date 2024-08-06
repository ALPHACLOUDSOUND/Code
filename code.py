from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler
from telegram.helpers import mention_html
from telegram.constants import ParseMode
from telegram.ext import filters

# Replace with your bot's token
TOKEN = '6375148626:AAHjSpQYzMam6dz5v_IFJdpjnZOcGJamgCI'

# Mock balance
BALANCE = 3000000  # 3 crore USDT
PENDING_WITHDRAWAL = False

async def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    username = user.username if user.username else user.first_name
    mention = mention_html(user.id, username)
    avatar_url = f"https://t.me/i/userpic/320/{user.id}.jpg"  # Placeholder URL
    
    text = (
        f"Hello {mention},\n"
        f"Your wallet balance is: {BALANCE} USDT\n"
        f"Pending withdrawal: Please ask Alan Walker to provide the confirmation code to access the server and withdraw."
    )

    keyboard = [
        [InlineKeyboardButton("Show Balance", callback_data='balance')],
        [InlineKeyboardButton("Withdraw", callback_data='withdraw')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_photo(photo=avatar_url, caption=text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'balance':
        await query.edit_message_text(text=f"Your wallet balance is: {BALANCE} USDT")
    elif query.data == 'withdraw':
        await query.edit_message_text(text="Please ask Alan Walker to confirm the code to withdraw.")
        global PENDING_WITHDRAWAL
        PENDING_WITHDRAWAL = True

async def confirm_withdraw(update: Update, context: CallbackContext) -> None:
    global PENDING_WITHDRAWAL
    if PENDING_WITHDRAWAL:
        if update.message.text == "CONFIRM_CODE":
            await update.message.reply_text("Withdrawal Successful: Transferring all funds.")
            # Reset balance after withdrawal
            global BALANCE
            BALANCE = 0
        else:
            await update.message.reply_text("Invalid confirmation code. Withdrawal failed.")
        PENDING_WITHDRAWAL = False
    else:
        await update.message.reply_text("No pending withdrawal request.")

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_withdraw))

    application.run_polling()

if __name__ == '__main__':
    main()

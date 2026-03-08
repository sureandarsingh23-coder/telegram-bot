from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

TOKEN = "8629090609:AAGm0ZNTQAr94Gmb8FiIpuwylwdxQMrBTdo"
CHANNEL = "@Fuckscammrs"
ADMIN_ID = 6283442463

order_counter = 1000


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("Join Channel", url="https://t.me/Fuckscammrs")],
        [InlineKeyboardButton("✅ Verify", callback_data="verify")]
    ]

    await update.message.reply_text(
        "❌ Bot use karne se pehle channel join karo",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    member = await context.bot.get_chat_member(CHANNEL, user_id)

    if member.status in ["member", "administrator", "creator"]:

        keyboard = [
            [InlineKeyboardButton("5 Members – ₹10", callback_data="5")],
            [InlineKeyboardButton("10 Members – ₹20", callback_data="10")],
            [InlineKeyboardButton("20 Members – ₹35", callback_data="20")],
            [InlineKeyboardButton("50 Members – ₹80", callback_data="50")],
            [InlineKeyboardButton("100 Members – ₹150", callback_data="100")]
        ]

        await query.message.reply_text(
            "Select Members",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    else:
        await query.message.reply_text("❌ Pehle channel join karo.")


async def plan(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    plan = query.data

    keyboard = [
        [InlineKeyboardButton("Payment Done ✅", callback_data="paid")]
    ]

    await query.message.reply_photo(
        photo=open("qr.png", "rb"),
        caption=f"{plan} Members plan selected\n\nQR scan karke payment karo.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    context.user_data["plan"] = plan


async def payment_done(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "Payment screenshot bhejo."
    )


async def screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global order_counter

    if update.message.photo:

        order_counter += 1

        plan = context.user_data.get("plan", "Unknown")

        caption = f"""
New Order

Order ID: #{order_counter}
Plan: {plan} Members
User ID: {update.message.chat_id}
Username: @{update.message.from_user.username}
"""

        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=update.message.photo[-1].file_id,
            caption=caption
        )

        await update.message.reply_text(
            f"Order submitted ✅\nOrder ID: #{order_counter}\nAdmin verify karega."
        )


async def admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.reply_to_message:

        text = update.message.reply_to_message.caption

        if text and "User ID:" in text:

            user_id = int(text.split("User ID: ")[1].split("\n")[0])

            await context.bot.send_message(
                chat_id=user_id,
                text=update.message.text
            )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(verify, pattern="verify"))
app.add_handler(CallbackQueryHandler(plan, pattern="5|10|20|50|100"))
app.add_handler(CallbackQueryHandler(payment_done, pattern="paid"))
app.add_handler(MessageHandler(filters.PHOTO, screenshot))
app.add_handler(MessageHandler(filters.TEXT & filters.User(ADMIN_ID), admin_reply))

print("Bot started...")

app.run_polling()
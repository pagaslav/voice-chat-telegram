from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from gtts import gTTS
import os
import random

# Load the API token from environment variable
API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')

# List of jokes in Ukrainian and English
jokes = [
    # Ukrainian jokes
    "Чому комп'ютер пішов на побачення? Бо в нього був гарний профіль!",
    "Як називається ліс без дерев? Поляна!",
    "Що робить програміст, коли голодний? Пише кодек з куркою.",
    "Чому курка перейшла дорогу? Щоб завантажити оновлення!",
    "Ти як Windows: працюєш, але кожного дня оновлюєшся.",
    "Я такий голодний, що можу з'їсти кілобайт їжі.",
    "Інтернет - як кохання: коли він зникає, життя стає безглуздим.",
    "Якщо ти відчуваєш себе непомітним, згадай, що є Wi-Fi мережі без пароля.",
    "Чому комп'ютер не любить каву? Бо він боїться перегрітися.",
    "Твоя посмішка яскрава, як екран смартфона на повній яскравості вночі.",
    
    # English jokes
    "I told my wife she should embrace her mistakes. She hugged me.",
    "Why don't skeletons fight each other? They don't have the guts.",
    "I would tell you a construction joke, but I'm still working on it.",
    "Why do cows have hooves instead of feet? Because they lactose.",
    "I used to play piano by ear, but now I use my hands.",
    "What do you call fake spaghetti? An impasta.",
    "I have a fear of speed bumps, but I'm slowly getting over it.",
    "Why don’t eggs tell jokes? They’d crack each other up.",
    "Parallel lines have so much in common. It’s a shame they’ll never meet.",
    "I was wondering why the ball kept getting bigger, then it hit me."
]

# List of quotes in Ukrainian and English
quotes = [
    # Ukrainian quotes
    "Життя - це те, що з тобою трапляється, поки ти будуєш інші плани.",
    "У кожного своя дорога, і вона починається з першого кроку.",
    "Завжди мрій, навіть якщо мрії здаються недосяжними.",
    "Ті, хто думають, що можуть, і ті, хто думають, що не можуть - обидва праві.",
    "Вчорашній день - це історія, завтрашній - загадка, сьогодні - дарунок.",
    "Справжня свобода - це здатність вибирати своє майбутнє.",
    "Роби те, що любиш, і не працюй жодного дня у своєму житті.",
    "Мудрість приходить з досвідом, а не з роками.",
    "Кожен новий день - це ще один шанс зробити все краще.",
    "Ти сильніший, ніж здається. Мудріший, ніж думаєш.",
    
    # English quotes
    "The only limit to our realization of tomorrow is our doubts of today.",
    "Success is not final, failure is not fatal: It is the courage to continue that counts.",
    "Believe you can and you're halfway there.",
    "Do not go where the path may lead, go instead where there is no path and leave a trail.",
    "In the end, we only regret the chances we didn't take.",
    "Life is 10% what happens to us and 90% how we react to it.",
    "It is never too late to be what you might have been.",
    "The best way to predict the future is to create it.",
    "Don’t watch the clock; do what it does. Keep going.",
    "Act as if what you do makes a difference. It does."
]

# List of funny and cheeky horoscopes in Ukrainian and English
horoscopes_uk = [
    "Сьогодні зірки підкажуть, що краще залишити штани застебнутими. Ну, принаймні до вечора.",
    "У тебе сьогодні той день, коли твої фантазії стануть реальністю... тільки спробуй не заснути до цього.",
    "Ти такий гарячий, що сьогодні точно зіпсуєш чиюсь дієту. Слідкуй за тими, хто дивиться на тебе довше трьох секунд.",
    "Сьогодні твій день настільки гарячий, що навіть холодильник позаздрить.",
    "Зірки кажуть, що ти занадто сексуальний, щоб весь день сидіти вдома. Виходь і подаруй світу свій шарм!",
]

horoscopes_en = [
    "Today the stars suggest you keep your pants on... at least until the evening.",
    "It's one of those days where your fantasies might come true... just try not to fall asleep before it happens.",
    "You're so hot today, you're bound to ruin someone's diet. Watch out for those who stare longer than three seconds.",
    "Your day is so sizzling, even the fridge will envy you.",
    "The stars say you're too sexy to stay home all day. Go out and give the world a taste of your charm!"
]

# Function to convert text to speech and save as an audio file
def synthesize_speech(text, lang='uk', output_file="output.mp3"):
    tts = gTTS(text, lang=lang)
    tts.save(output_file)

# Function to handle /voice command that converts quoted message to audio
async def handle_voice_command(update: Update, context: CallbackContext):
    if update.message.reply_to_message and update.message.reply_to_message.text:
        text_to_convert = update.message.reply_to_message.text
        print(f"Converting to audio: {text_to_convert}")
        synthesize_speech(text_to_convert, lang='uk')
        await update.message.reply_voice(voice=open("output.mp3", "rb"))
    else:
        await update.message.reply_text("Please use this command as a reply to the message you want to convert to audio.")

# Function to send a random joke
async def send_joke(update: Update, context: CallbackContext):
    joke = random.choice(jokes)
    await update.message.reply_text(joke)

# Function to send a random quote
async def send_quote(update: Update, context: CallbackContext):
    quote = random.choice(quotes)
    await update.message.reply_text(quote)

# Function to send a random horoscope
async def send_horoscope(update: Update, context: CallbackContext):
    if random.choice([True, False]):
        horoscope = random.choice(horoscopes_uk)
    else:
        horoscope = random.choice(horoscopes_en)
    await update.message.reply_text(horoscope)

# Function to provide help information
async def send_help(update: Update, context: CallbackContext):
    help_text = (
        "/joke - Get a random joke (either in Ukrainian or English).\n"
        "/quote - Receive a random inspirational quote.\n"
        "/horoscope - Get a cheeky and funny horoscope prediction.\n"
        "/voice - Convert a quoted message to an audio file. Use this command by replying to a message you want to convert.\n"
        "/help - Show this help message."
    )
    await update.message.reply_text(help_text)

# Main function to set up the bot
def main():
    app = Application.builder().token(API_TOKEN).build()
    
    # Add command handlers for jokes, quotes, horoscopes, voice conversion, and help
    app.add_handler(CommandHandler("joke", send_joke))
    app.add_handler(CommandHandler("quote", send_quote))
    app.add_handler(CommandHandler("horoscope", send_horoscope))
    app.add_handler(CommandHandler("voice", handle_voice_command))
    app.add_handler(CommandHandler("help", send_help))
    
    # Start the bot
    app.run_polling()

# Entry point of the script
if __name__ == '__main__':
    main()
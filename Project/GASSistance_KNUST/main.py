import telebot
from telebot import types
import config

bot = telebot.TeleBot(config.API_TOKEN, parse_mode=None)

intro_message = (
    "Hey there! 📊 I'm your GASS Library buddy. "
    "Need help with course materials? Just let me know, and I'll get everything ready for you! 🚀"
)

help_message = (
    "🌟 Here's how to use GASS Library:\n\n"
    "1. Tap on the 📚 'Choose Year' button to get started.\n"
    "2. Select your academic year from the list.\n"
    "3. Receive links for Semester 1 and Semester 2 based on your selection.\n"
    "4. Explore your course materials and ace your studies! 🎓💪"
)

years = ["1st Year", "2nd Year", "3rd Year", "4th Year"]

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item1 = types.KeyboardButton("📚 Choose Year")
    item2 = types.KeyboardButton("❓ Help")

    markup.add(item1, item2)

    bot.reply_to(message, intro_message, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "📚 Choose Year")
def choose_year(message):
    markup = create_preference_markup(years)
    bot.send_message(message.chat.id, "🎓 Select your year:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "❓ Help")
def show_help(message):
    bot.send_message(message.chat.id, help_message)

def create_preference_markup(options):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(*[types.KeyboardButton(option) for option in options + ["🔙 Go Back"]])
    return markup

@bot.message_handler(func=lambda message: message.text in years + ["🔙 Go Back"])
def process_year_selection(message):
    user_selection = message.text
    if user_selection == "🔙 Go Back":
        bot.send_message(message.chat.id, "Sure! Let's go back to the previous step.", reply_markup=create_preference_markup(["📚 Choose Year", "❓ Help"]))
    else:
        # Generate links for Semester 1 and Semester 2 based on the user's selection
        links = generate_links(user_selection)
        response_message = (
            f"📚 Here are the links for {user_selection}:\n\n"
            f"Semester 1: {links['Semester 1']}\n"
            f"Semester 2: {links['Semester 2']}"
        )
        bot.send_message(message.chat.id, response_message)

def generate_links(year):
    link_mapping = {
        "1st Year": {"Semester 1": "www.html.com", "Semester 2": "www.html.com"},
        "2nd Year": {"Semester 1": "www.html.com", "Semester 2": "www.html.com"},
        "3rd Year": {"Semester 1": "www.html.com", "Semester 2": "www.html.com"},
        "4th Year": {"Semester 1": "www.html.com", "Semester 2": "www.html.com"},
    }
    return link_mapping.get(year, {"Semester 1": "default_link_semester_1", "Semester 2": "default_link_semester_2"})

# Start the bot
bot.polling()
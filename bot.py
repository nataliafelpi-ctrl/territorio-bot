import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import json

TOKEN = "8778203220:AAEIElSVb5rlRtm31jpXTERIqcAn7cpCqwg"
bot = telebot.TeleBot(TOKEN)

SERVICOS = [
    "Corte de Cabelo",
    "Barba",
    "Corte + Barba"
]

HORARIOS = [
    "09:00", "10:00", "11:00",
    "14:00", "15:00", "16:00", "17:00"
]

user_data = {}

def salvar_agendamento(dados):
    try:
        with open("agendamentos.json", "r") as f:
            lista = json.load(f)
    except:
        lista = []

    lista.append(dados)

    with open("agendamentos.json", "w") as f:
        json.dump(lista, f, indent=4)

@bot.message_handler(commands=['start'])
def start(msg):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("📅 Agendar Horário"))

    bot.send_message(
        msg.chat.id,
        "✂️ Bem-vindo à Barbearia Território!\nClique abaixo para agendar:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.text == "📅 Agendar Horário")
def escolher_servico(msg):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    for s in SERVICOS:
        markup.add(KeyboardButton(s))

    bot.send_message(msg.chat.id, "Escolha o serviço:", reply_markup=markup)
    user_data[msg.chat.id] = {}

@bot.message_handler(func=lambda m: m.text in SERVICOS)
def escolher_data(msg):
    user_data[msg.chat.id]["servico"] = msg.text
    bot.send_message(msg.chat.id, "Digite a data (DD/MM):")

@bot.message_handler(func=lambda m: "/" in m.text and len(m.text) == 5)
def escolher_horario(msg):
    user_data[msg.chat.id]["data"] = msg.text

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for h in HORARIOS:
        markup.add(KeyboardButton(h))

    bot.send_message(msg.chat.id, "Escolha o horário:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in HORARIOS)
def confirmar(msg):
    user_data[msg.chat.id]["horario"] = msg.text
    user_data[msg.chat.id]["cliente"] = msg.from_user.first_name

    salvar_agendamento(user_data[msg.chat.id])

    bot.send_message(
        msg.chat.id,
        "✅ Agendamento confirmado!\n\n"
        f"👤 Cliente: {msg.from_user.first_name}\n"
        f"✂️ Serviço: {user_data[msg.chat.id]['servico']}\n"
        f"📅 Data: {user_data[msg.chat.id]['data']}\n"
        f"⏰ Horário: {user_data[msg.chat.id]['horario']}"
    )

print("Bot Território rodando...")
bot.infinity_polling()
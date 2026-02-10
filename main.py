import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from flask import Flask
from threading import Thread
from groq import Groq  # Importam creierul

# --- Configurare Jurnal ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- Partea 1: Server Web (Keep-Alive) ---
app = Flask('')

@app.route('/')
def home():
    return "Botul AI este TREAZ si GANDESTE!"

def run_http():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

def keep_alive():
    t = Thread(target=run_http)
    t.start()

# --- Partea 2: Inteligenta Artificiala ---
# Initializam clientul Groq cu cheia din Render
client_ai = None
api_key = os.environ.get("GROQ_API_KEY")
if api_key:
    client_ai = Groq(api_key=api_key)
else:
    logging.error("ATENTIE: Nu am gasit GROQ_API_KEY!")

async def ask_ai(text):
    if not client_ai:
        return "Nu am creier! (Lipseste cheia API Groq)"
    
    try:
        completion = client_ai.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Esti un asistent util si prietenos. Raspunzi scurt si la obiect in limba romana."
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            model="llama3-8b-8192", # Model gratuit si rapid
        )
        return completion.choices[0].message.content
    except Exception as e:
        logging.error(f"Eroare AI: {e}")
        return "Am obosit (Eroare la conectarea cu creierul)."

# --- Partea 3: Logica Botului Telegram ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salut! Acum sunt inteligent. Intreaba-me orice!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mesaj_utilizator = update.message.text
    
    # Trimitem mesajul "Se scrie..." ca sa stie userul ca gandim
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    
    # Intrebam AI-ul
    raspuns_ai = await ask_ai(mesaj_utilizator)
    
    # Trimitem raspunsul inapoi
    await update.message.reply_text(raspuns_ai)

if __name__ == '__main__':
    keep_alive()
    
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        print("Eroare: Lipseste TELEGRAM_TOKEN!")
    else:
        application = ApplicationBuilder().token(token).build()
        
        application.add_handler(CommandHandler('start', start))
        application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
        
        application.run_polling()

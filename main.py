import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from flask import Flask
from threading import Thread

# --- Partea 1: Server Web (ca să țină Render fericit) ---
app = Flask('')

@app.route('/')
def home():
    return "Botul e treaz! (Alive)"

def run_http():
    # Render ne dă un port prin variabila PORT, sau folosim 8080
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

def keep_alive():
    t = Thread(target=run_http)
    t.start()

# --- Partea 2: Logica Botului ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salut! Sunt online pe Render. Scrie-mi ceva!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Aici vom conecta ulterior "creierul" AI.
    # Momentan, doar repetă ce zici (Echo).
    text_primit = update.message.text
    await update.message.reply_text(f"Ai zis: {text_primit}")

if __name__ == '__main__':
    # Pornim serverul web în fundal
    keep_alive()
    
    # Pornim botul de Telegram
    # TOKEN-ul va fi luat din setările Render (Environment Variables)
    token = os.environ.get("TELEGRAM_TOKEN")
    
    if not token:
        print("Eroare: Nu am găsit TELEGRAM_TOKEN!")
    else:
        application = ApplicationBuilder().token(token).build()
        
        start_handler = CommandHandler('start', start)
        echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
        
        application.add_handler(start_handler)
        application.add_handler(echo_handler)
        
        application.run_polling()

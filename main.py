import os
import telebot
import requests

# Configurações
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Limite de segurança: 20MB
MAX_SIZE = 20 * 1024 * 1024 

@bot.message_handler(content_types=['video', 'document', 'audio', 'voice'])
def handle_video(message):
    # 1. Checagem de tamanho (Filtro)
    file_size = 0
    if message.video: file_size = message.video.file_size
    elif message.document: file_size = message.document.file_size
    
    if file_size > MAX_SIZE:
        bot.reply_to(message, "⚠️ Arquivo muito grande! (Máx 20MB). Por favor, use um bot conversor para transformar em áudio (MP3) antes de me enviar.")
        return

    bot.reply_to(message, "Recebi! Iniciando processamento...")
    try:
        # Baixa e processa
        file_id = message.video.file_id if message.video else message.document.file_id
        file_info = bot.get_file(file_id)
        file_url = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_info.file_path}"
        
        response = requests.get(file_url)
        with open("temp.mp4", "wb") as f: f.write(response.content)
            
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
        with open("temp.mp4", "rb") as f:
            files = {"file": ("temp.mp4", f, "video/mp4"), "model": (None, "whisper-large-v3"), "language": (None, "pt")}
            res = requests.post("https://api.groq.com/openai/v1/audio/transcriptions", headers=headers, files=files)
        
        texto = res.json().get("text", "Erro na transcrição.")
        bot.reply_to(message, f"**Transcrição:**\n\n{texto}", parse_mode="Markdown")
        os.remove("temp.mp4")
    except Exception as e:
        bot.reply_to(message, f"Erro: {str(e)}")

bot.infinity_polling()

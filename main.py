import os
import telebot
import requests

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(content_types=['video', 'document', 'audio', 'voice'])
def handle_video(message):
    bot.reply_to(message, "Recebi! Iniciando processamento...")
    try:
        # Identifica o arquivo
        file_id = message.video.file_id if message.video else message.document.file_id
        file_info = bot.get_file(file_id)
        file_url = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_info.file_path}"
        
        # Baixa o arquivo
        response = requests.get(file_url)
        with open("temp.mp4", "wb") as f: f.write(response.content)
            
        # Envia para a Groq
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
        with open("temp.mp4", "rb") as f:
            files = {"file": ("temp.mp4", f, "video/mp4"), "model": (None, "whisper-large-v3"), "language": (None, "pt")}
            res = requests.post("https://api.groq.com/openai/v1/audio/transcriptions", headers=headers, files=files)
        
        # Envia a transcrição de volta
        texto = res.json().get("text", "Erro na transcrição.")
        bot.reply_to(message, f"**Transcrição:**\n\n{texto}", parse_mode="Markdown")
        os.remove("temp.mp4")
    except Exception as e:
        bot.reply_to(message, f"Erro: {str(e)}")

bot.infinity_polling()
@bot.message_handler(content_types=['video', 'document', 'audio', 'voice'])
def handle_video(message):
    # --- FILTRO DE SEGURANÇA ---
    # Pegar tamanho em bytes (25MB é um limite seguro para o Render gratuito)
    file_size = 0
    if message.video: file_size = message.video.file_size
    elif message.document: file_size = message.document.file_size
    
    if file_size > 25 * 1024 * 1024:  # Se > 25MB
        bot.reply_to(message, "⚠️ Arquivo muito grande! (Máx 25MB para processamento direto). \n\nDica: Encaminhe este vídeo para um bot de 'Converter para MP3' no Telegram, pegue o áudio gerado e encaminhe para mim!")
        return
    # ---------------------------

    bot.reply_to(message, "Recebi! Iniciando processamento...")
    # ... (o resto do seu código continua aqui)
@bot.message_handler(content_types=['video', 'document', 'audio', 'voice'])
def handle_video(message):
    # --- FILTRO DE SEGURANÇA ---
    # Pegar tamanho em bytes (25MB é um limite seguro para o Render gratuito)
    file_size = 0
    if message.video: file_size = message.video.file_size
    elif message.document: file_size = message.document.file_size
    
    if file_size > 25 * 1024 * 1024:  # Se > 25MB
        bot.reply_to(message, "⚠️ Arquivo muito grande! (Máx 25MB para processamento direto). \n\nDica: Encaminhe este vídeo para um bot de 'Converter para MP3' no Telegram, pegue o áudio gerado e encaminhe para mim!")
        return
    # ---------------------------

    bot.reply_to(message, "Recebi! Iniciando processamento...")
    # ... (o resto do seu código continua aqui)

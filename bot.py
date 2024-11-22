import discord
from discord.ext import commands
from googletrans import Translator
import requests  # Untuk API konversi mata uang

# Setup bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Tentukan bahasa default (misalnya, bahasa Inggris)
default_lang = "en"

# Daftar kode bahasa yang didukung
language_codes = {
    "en": "English",
    "id": "Indonesian",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "ru": "Russian",
    "ja": "Japanese",
    "ko": "Korean",
    "zh": "Chinese (Simplified)",
    "ar": "Arabic",
    "tr": "Turkish",
    "pl": "Polish",
    "hi": "Hindi",
    "tl": "Tagalog",  
    "th": "Thai"      
}


API_KEY = "00a1d56bafcd1e104d06bb8d"  # Ganti dengan API key Anda dari ExchangeRate-API
EXCHANGE_API_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"

@bot.event
async def on_ready():
    print(f"Bot {bot.user.name} Online Now !")

@bot.event
async def on_message(message):
    if message.author.bot:
        return  # Abaikan pesan dari bot lain

    # Jika pesan diawali dengan "!translate"
    if message.content.startswith("!translate"):
        try:
            # Ambil teks setelah "!translate "
            text_to_translate = message.content[len("!translate "):]

            # Tentukan bahasa tujuan jika ada
            if " to:" in text_to_translate:
                parts = text_to_translate.split(" to:")
                text_to_translate = parts[0]
                lang_code = parts[1]
            else:
                lang_code = default_lang  # Default ke bahasa Inggris

            # Inisialisasi translator dengan bahasa tujuan menggunakan googletrans
            translator = Translator()

            # Terjemahkan teks
            translated = translator.translate(text_to_translate, dest=lang_code)
            
            # Kirim hasil terjemahan
            await message.channel.send(f"Terjemahan: {translated.text}")
        except Exception as e:
            await message.channel.send(f"Error: {e}")

    # Jika pesan diawali dengan "!convert"
    if message.content.startswith("!convert"):
        try:
            # Format: !convert <jumlah> <dari_kode_mata_uang> to <ke_kode_mata_uang>
            parts = message.content.split(" ")
            amount = float(parts[1])
            from_currency = parts[2].upper()
            to_currency = parts[4].upper()

            # Dapatkan data konversi dari ExchangeRate-API
            response = requests.get(EXCHANGE_API_URL)
            data = response.json()

            if data['result'] == 'success':
                # Ambil nilai tukar dari mata uang sumber ke USD
                from_rate = data['conversion_rates'].get(from_currency, None)
                to_rate = data['conversion_rates'].get(to_currency, None)

                if from_rate and to_rate:
                    # Hitung nilai tukar
                    usd_amount = amount / from_rate
                    converted_amount = usd_amount * to_rate

                    # Kirim hasil konversi
                    await message.channel.send(
                        f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}"
                    )
                else:
                    await message.channel.send("The requested currency is invalid.")
            else:
                await message.channel.send("An error occurred while retrieving currency data.")
        except Exception as e:
            await message.channel.send(f"Error: {e}")

    # Jika pesan diawali dengan "!help"
    if message.content.startswith("!help"):
        help_message = "You can use the command `!translate <text> to:<language code>` to translate.\n\n"
        help_message += "Here are some language codes that can be used.:\n"
        
        for code, language in language_codes.items():
            help_message += f"- `{code}`: {language}\n"

        help_message += "\nExample Used:\n"
        help_message += "`!translate Hello to:en` => Translates 'Hello' to English\n"
        help_message += "`!translate Hello to:id` => Translate 'Hello' to Indonesian\n"
        help_message += "\nFor currency conversion, use the command `!convert <amount> <currency_code> to <currency_code>\n"
        help_message += "Example: `!convert 100 USD to EUR` to convert 100 USD to EUR"
        
        # Kirim pesan bantuan
        await message.channel.send(help_message)

# Jalankan bot (masukkan token dari Discord Developer Portal)
TOKEN = "DISCORD_TOKEN_KEY"
bot.run(TOKEN)

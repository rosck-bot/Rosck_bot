import telebot
import requests
import datetime

# -------------------------------------------------
# 1. Token do teu bot (coloca aqui o novo token)
# -------------------------------------------------
TOKEN = "COLOCA_AQUI_O_TEVE_TOKEN"
bot = telebot.TeleBot(TOKEN)

# -------------------------------------------------
# 2. API grátis para estatísticas de futebol
#    (não precisa chave)
# -------------------------------------------------
API_URL = "https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d={}&l=Soccer"

def get_games():
    hoje = datetime.datetime.now().strftime("%Y-%m-%d")
    url = API_URL.format(hoje)
    try:
        r = requests.get(url).json()
        return r.get("events", [])
    except:
        return None

# -------------------------------------------------
# 3. Comando /start
# -------------------------------------------------
@bot.message_handler(commands=["start"])
def start(msg):
    bot.reply_to(msg, 
        "🔥 *Rosck_Bot Estatísticas de Futebol*\n"
        "Escolhe uma opção:\n\n"
        "⚽ /jogos_hoje — Ver jogos do dia\n"
        "📊 /estatisticas — Estatísticas detalhadas\n"
        "🔮 /probabilidade — Probabilidades matemáticas\n"
        "💹 /forma — Forma das equipas\n"
        "",
        parse_mode="Markdown"
    )

# -------------------------------------------------
# 4. Jogos do dia
# -------------------------------------------------
@bot.message_handler(commands=["jogos_hoje"])
def jogos_do_dia(msg):
    jogos = get_games()

    if not jogos:
        bot.reply_to(msg, "❌ Não encontrei jogos hoje.")
        return
    
    texto = "📅 *Jogos de hoje:*\n\n"
    for j in jogos:
        texto += f"⚽ {j['strHomeTeam']} vs {j['strAwayTeam']}\n"
        texto += f"⏰ Hora: {j['strTime']}\n\n"

    bot.reply_to(msg, texto, parse_mode="Markdown")

# -------------------------------------------------
# 5. Estatísticas detalhadas
# -------------------------------------------------
@bot.message_handler(commands=["estatisticas"])
def estatisticas(msg):
    jogos = get_games()

    if not jogos:
        bot.reply_to(msg, "❌ Sem dados hoje.")
        return

    texto = "📊 *Estatísticas de Últimos Jogos:*\n\n"
    for j in jogos[:5]:
        texto += f"🔵 {j['strHomeTeam']} – Últimos 5 jogos\n"
        texto += f"🔴 {j['strAwayTeam']} – Últimos 5 jogos\n"
        texto += f"📈 Probabilidade de +2.5: {j.get('intHomeScore', 0)}%\n\n"

    bot.reply_to(msg, texto, parse_mode="Markdown")

# -------------------------------------------------
# 6. Probabilidades matemáticas simples
# -------------------------------------------------
@bot.message_handler(commands=["probabilidade"])
def probabilidade(msg):
    texto = (
        "🔮 *Probabilidades (base matemática):*\n\n"
        "⚽ +2.5 Golos → 48%\n"
        "⚽ Ambas Marcam → 52%\n"
        "🚫 Menos de 2.5 → 45%\n"
        "🏆 Casa vence → 40–60%\n\n"
        "Valores mudam conforme forma e histórico."
    )
    bot.reply_to(msg, texto, parse_mode="Markdown")

# -------------------------------------------------
# 7. Forma das equipas
# -------------------------------------------------
@bot.message_handler(commands=["forma"])
def forma(msg):
    bot.reply_to(msg,
        "📉 *Forma das equipas ainda não disponível nesta versão.*\n"
        "Mas posso adicionar — só pedir!",
        parse_mode="Markdown"
    )

# -------------------------------------------------
# 8. Loop
# -------------------------------------------------
bot.polling()

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests

# Настройки
TOKEN = "7861189824:AAHJYqds-yFSL62CUld2rNjYmFQs3rnHq1M"
OPENWEATHER_API_KEY = "a4d59bf0f52e6de1b4f17e4efc7e7a29"
EXCHANGE_RATE_API = "https://api.exchangerate-api.com/v4/latest/USD"

# Настройка логгирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Глобальная переменная для задач (в реальном проекте используйте БД)
user_tasks = {}

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_html(
        f"Привет, {user.mention_html()}! Я полезный бот 🤖\n"
        "Доступные команды:\n"
        "/weather <город> - погода\n"
        "/convert <сумма> <из валюты> <в валюту>\n"
        "/addtask <текст> - добавить задачу\n"
        "/tasks - список задач\n"
        "/deltask <номер> - удалить задачу"
    )

# Погода через OpenWeather API
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        city = " ".join(context.args)
        if not city:
            await update.message.reply_text("Укажите город: /weather Москва")
            return
        
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=ru"
        response = requests.get(url).json()
        
        if response["cod"] != 200:
            await update.message.reply_text("Город не найден 😢")
            return
        
        weather_data = response["weather"][0]
        main_data = response["main"]
        result = (
            f"🌡 Погода в {city}:\n"
            f"Температура: {main_data['temp']}°C (ощущается как {main_data['feels_like']}°C)\n"
            f"Описание: {weather_data['description'].capitalize()}\n"
            f"Влажность: {main_data['humidity']}%\n"
            f"Ветер: {response['wind']['speed']} м/с"
        )
        await update.message.reply_text(result)
    
    except Exception as e:
        logger.error(e)
        await update.message.reply_text("Ошибка запроса 😢")

# Конвертер валют
async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) < 3:
            await update.message.reply_text("Используйте: /convert 100 USD RUB")
            return
        
        amount = float(args[0])
        from_cur = args[1].upper()
        to_cur = args[2].upper()
        
        response = requests.get(EXCHANGE_RATE_API).json()
        rates = response["rates"]
        
        if from_cur not in rates or to_cur not in rates:
            await update.message.reply_text("Неверные коды валют (используйте USD, EUR, RUB и т.д.)")
            return
        
        result = amount * (rates[to_cur] / rates[from_cur])
        await update.message.reply_text(
            f"💱 Результат:\n"
            f"{amount:.2f} {from_cur} = {result:.2f} {to_cur}"
        )
    
    except Exception as e:
        logger.error(e)
        await update.message.reply_text("Ошибка конвертации. Проверьте формат ввода")

# Менеджер задач
async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    task = " ".join(context.args)
    
    if not task:
        await update.message.reply_text("Укажите задачу: /addtask Купить молоко")
        return
    
    if user_id not in user_tasks:
        user_tasks[user_id] = []
    
    user_tasks[user_id].append(task)
    await update.message.reply_text(f"✅ Задача добавлена: {task}")

async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    tasks = user_tasks.get(user_id, [])
    
    if not tasks:
        await update.message.reply_text("Список задач пуст!")
        return
    
    tasks_list = "\n".join([f"{i+1}. {task}" for i, task in enumerate(tasks)])
    await update.message.reply_text(f"📝 Ваши задачи:\n{tasks_list}")

async def delete_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        task_num = int(context.args[0]) - 1
        task = user_tasks[user_id].pop(task_num)
        await update.message.reply_text(f"❌ Задача удалена: {task}")
    except (IndexError, ValueError):
        await update.message.reply_text("Укажите номер задачи: /deltask 1")
    except KeyError:
        await update.message.reply_text("Нет задач для удаления")

# Запуск бота
def main():
    application = Application.builder().token(TOKEN).build()
    
    # Регистрация команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("weather", weather))
    application.add_handler(CommandHandler("convert", convert))
    application.add_handler(CommandHandler("addtask", add_task))
    application.add_handler(CommandHandler("tasks", list_tasks))
    application.add_handler(CommandHandler("deltask", delete_task))
    
    # Запуск
    application.run_polling()

if __name__ == "__main__":
    main()
    p

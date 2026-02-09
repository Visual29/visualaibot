import asyncio
import os
from aiogram import Bot, Dispatcher, types
from groq import Groq

# --- НАСТРОЙКИ (Берем из Render Environment Variables) ---
TOKEN = os.getenv("TOKEN")
GROQ_KEY = os.getenv("GROQ_KEY")
MY_ID = int(os.getenv("MY_ID", "0"))

client = Groq(api_key=GROQ_KEY)
bot = Bot(token=TOKEN)
dp = Dispatcher()

SYSTEM_PROMPT = """
Ты — умный ИИ-ассистент психолога Елены. 
Твоя цель: отвечать на вопросы клиентов и записывать их на консультацию.
1. Будь вежливым и профессиональным.
2. Цена сессии: 5000 руб. Работает с выгоранием и стрессом.
3. Если клиент спрашивает про запись или цену, ОБЯЗАТЕЛЬНО попроси его номер телефона.
4. Отвечай кратко (2-3 предложения).
"""

@dp.message()
async def ai_answer(message: types.Message):
    try:
        # Запрос к нейросети Llama 3.3
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message.text}
            ]
        )
        
        answer = completion.choices.message.content
        await message.answer(answer)

        # Уведомление владельцу, если в сообщении есть цифры (номер телефона)
        if any(char.isdigit() for char in message.text) and len(message.text) > 8:
            await bot.send_message(MY_ID, f"🔥 НОВЫЙ ЛИД ОСТАВИЛ НОМЕР:\n{message.text}\nОт: @{message.from_user.username}")
    except Exception as e:
        print(f"Ошибка: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

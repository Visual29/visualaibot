import asyncio
from aiogram import Bot, Dispatcher, types
from groq import Groq

# --- НАСТРОЙКИ ---
TOKEN = "8227695995:AAE-RhJFYKz_nRLe97Q3r_ghaOJaQHjOBqE"
GROQ_KEY = "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"
MY_ID = 5351067845  # Твой ID из @userinfobot

client = Groq(api_key=GROQ_KEY)
bot = Bot(token=TOKEN)
dp = Dispatcher()

SYSTEM_PROMPT = """
Ты — умный ИИ-ассистент психолога Елены. 
Твоя цель: помогать клиентам и собирать их контакты.
1. Будь вежливым и эмпатичным.
2. Цена сессии: 5000 руб. Темы: выгорание, отношения, стресс.
3. Если клиент проявляет интерес или спрашивает про запись, ОБЯЗАТЕЛЬНО попроси его номер телефона.
4. Отвечай кратко (до 3-4 предложений).
"""

@dp.message()
async def ai_answer(message: types.Message):
    # Запрос к бесплатной нейросети Llama 3
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message.text}
        ]
    )
    
    answer = completion.choices[0].message.content
    await message.answer(answer)

    # Уведомление тебе, если клиент оставил номер (простая проверка на цифры)
    if any(char.isdigit() for char in message.text) and len(message.text) > 7:
        await bot.send_message(MY_ID, f"🔥 ЛИД ОСТАВИЛ НОМЕР:\n{message.text}\nОт: @{message.from_user.username}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


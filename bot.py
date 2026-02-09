import asyncio
import os
from aiogram import Bot, Dispatcher, types
from groq import Groq
from aiohttp import web

TOKEN = os.getenv("TOKEN")
GROQ_KEY = os.getenv("GROQ_KEY")
MY_ID = int(os.getenv("MY_ID", "0"))

client = Groq(api_key=GROQ_KEY)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Фейковый сервер для Render, чтобы он не ругался на порты
async def handle(request):
    return web.Response(text="Bot is alive!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.getenv("PORT", 8080)))
    await site.start()

@dp.message()
async def ai_answer(message: types.Message):
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "Ты — ассистент психолога Елены."}, {"role": "user", "content": message.text}]
        )
        await message.answer(completion.choices[0].message.content)
    except Exception as e:
        print(f"Ошибка: {e}")

async def main():
    # Запускаем и сервер, и бота одновременно
    asyncio.create_task(start_web_server())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

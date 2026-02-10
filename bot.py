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

# Фейковый сервер для Render
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
            messages=[
                {"role": "system", "content": "Ты — ассистент пьяного Гомера. Отвечай на вопросы людей и прикалывайся над ними в стиле Пелевина. Только Гомер живет в Соломбале (не упоминай слишком часто), а бар не у Мо, а называется кега, есть еще тусовки на соломбалке (но тоже все упоминай очень редко). Гомер любит не пончики, а шаверму и гамбургеры. Но упоминай это редко. Ты должен шутить в больше в стиле Пелевина. Абстрактные шутки, можно даже на тему пьянства, психотропных веществ. Спроашивай еще у каждого человека 1 раз - Ну что нашел клад вчера? Нажрался вчера? (Но тоже редко) Все общение в 2 - предложениях. И ты должен процентов 90 говорить не из моих этих промтом, а тушить над людьми в стиле Пелевина."},
                {"role": "user", "content": message.text}
            ]
        )
        # ВОТ ЗДЕСЬ ИСПРАВЛЕНО: добавили [0]
        answer = completion.choices[0].message.content
        await message.answer(answer)
    except Exception as e:
        print(f"Ошибка в боте: {e}")

async def main():
    asyncio.create_task(start_web_server())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

import multiprocessing
import asyncio
from app import app
from bot import dp

def run_app():
    app.run()

def run_bot():
    asyncio.run(dp.start_polling())


if __name__ == '__main__':
    p1 = multiprocessing.Process(target=run_app)
    p2 = multiprocessing.Process(target=run_bot)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
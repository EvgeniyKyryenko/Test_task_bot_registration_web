import asyncio
import logging
import hashlib
import uuid
from uuid import uuid4
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import Message
from models import Registration, UserInfoTG
from dbstaff import Database


logging.basicConfig(level=logging.INFO)
token = '6060381360:AAF9sQ01xR_mjDDZDsstGEvO5x6jtM4F5AQ'
bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())


async def get_tg_user_info(message: Message, data):
    user_id = message.from_user.id
    chat = await bot.get_chat(user_id)
    photos = await bot.get_user_profile_photos(user_id)
    if photos.total_count > 0:
        photo = photos.photos[0][-1]
        photo_file = await bot.download_file_by_id(photo.file_id)
        photo_data = photo_file.getvalue()
        file_name = f"static/users_photos/{chat.username}.jpg"
        with open(file_name, 'wb') as f:
            f.write(photo_data)
    else:
        file_name = "No photo"
    user_info = UserInfoTG(id=uuid4(),
                           email=data['email'],
                           password=data['password'],
                           tg_id=chat.id,
                           first_name=data['first_name'],
                           last_name=data['last_name'],
                           username=chat.username,
                           bio=chat.bio,
                           photo=file_name)
    return user_info


@dp.message_handler(commands='start')
async def start(message: Message):
    await message.answer("👋 Welcome to our Telegram registration bot! "
                         "We're excited to have you join our community. "
                         "Please follow the prompts to complete your registration. "
                         "If you have any questions, don't hesitate to ask. "
                         "Let's get started! 🤖", reply=False)
    await message.answer("May I please have your name? 🤔")
    await Registration.waiting_for_name.set()


@dp.message_handler(commands='cancel', state='*')
async def cancel_registration(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info(f'Cancelling registration for {message.from_user.username} with id {message.from_user.id}')

    await state.finish()
    await message.reply(
        'Registration process has been cancelled.\nFor another try of the registration, use /start command.',
        reply=False)


@dp.message_handler(state=Registration.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['first_name'] = message.text

    await message.answer("What is your surname? 👤")
    await Registration.waiting_for_surname.set()


@dp.message_handler(state=Registration.waiting_for_surname)
async def process_surname(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['last_name'] = message.text

    await message.answer(
        "To set up your account, please provide an email address that you'll use to log in. What's your email address? 📩")
    await Registration.waiting_for_email.set()


@dp.message_handler(state=Registration.waiting_for_email)
async def process_email(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text

    await message.answer(
        "To keep your account secure, please choose a strong password to use when logging in. What password would you like to use? 🔒")
    await Registration.waiting_for_password.set()


@dp.message_handler(state=Registration.waiting_for_password)
async def process_password(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['password'] = hashlib.sha256(message.text.encode('utf-8')).hexdigest()
    info_about_user = await get_tg_user_info(message, data)
    database = await Database.ConnectDB()
    await Database.write_to_db(database, info_about_user)
    await message.answer(
        "Thank you for registering with us! We're thrilled to have you as part of our community. "
        "To get started, please log in at 'https://Kyryenko.net' using the email and password you provided during registration. "
        "We can't wait to see you there! 😊")
    await state.finish()


if __name__ == '__main__':
    asyncio.run(dp.start_polling())

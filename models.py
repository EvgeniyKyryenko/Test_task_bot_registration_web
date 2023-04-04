from aiogram.dispatcher.filters.state import State, StatesGroup
from dataclasses import dataclass
from uuid import uuid4

class Registration(StatesGroup):
    waiting_for_name = State()
    waiting_for_surname = State()
    waiting_for_email = State()
    waiting_for_password = State()

@dataclass
class UserInfoTG:
    id:uuid4
    email:str
    password:str
    tg_id:int
    first_name:str
    last_name:str
    username:str
    bio:str
    photo:str
import os
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import DB_URL

from band import BandMember, Band

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
print(TOKEN)

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)
session = Session()


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    user = message.from_user
    band_member = session.query(BandMember).filter(BandMember.id == user.id)
    if band_member.first():
        await message.reply(f'Вы уже регистрировались!')

    else:
        us_name = ''
        us_lastname = ''
        if user.first_name:
            us_name = user.first_name
        if user.last_name:
            us_lastname = user.last_name
        member = BandMember(id=user.id, name=us_name + ' ' + us_lastname)
        session.add(member)
        session.commit()
        await message.reply(
            f'Привет!\nМне написал {user.first_name + " " + user.last_name}\nТы занесён в базу джемеров. Поздравляю! ')


@dp.message_handler(commands=['set_instruments'])
async def process_start_command(message: types.Message):
    user = message.from_user
    band_member = session.query(BandMember).filter(BandMember.id == user.id).first()
    arguments = message.get_args()
    if band_member:
        band_member.instruments = arguments
        session.commit()
        await message.reply(f'Выставляем инструменты для {band_member.name}\n'
                            f'Ваши инстурменты: {arguments}')
    else:
        await message.reply(f'Похоже вы еще не зарегестрировались')


@dp.message_handler(commands=['get_instruments'])
async def process_start_command(message: types.Message):
    user = message.from_user
    band_member = session.query(BandMember).filter(BandMember.id == user.id).first()
    if band_member:
        await message.reply(f'Ваши инстурменты: {band_member.instruments}')
    else:
        await message.reply(f'Похоже вы еще не зарегестрировались')


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")


@dp.message_handler(commands=['jam'])
async def process_jam_command(message: types.Message):
    ses_members = session.query(BandMember).all()
    session.flush()
    mem_count = int(message.get_args())
    if mem_count > len(ses_members):
        await message.reply("Выхотите в джем больше участников чем есть!")
    else:

        band = Band(ses_members)

        band = band.create_band(mem_count)
        band.det_instrument()
        repl = ""
        for mem in band.members:
            repl += mem.name + " " + mem.chosen_instrument + "\n"
        await message.reply("А теперь играют:\n" + repl)

@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)


if __name__ == '__main__':
    executor.start_polling(dp)

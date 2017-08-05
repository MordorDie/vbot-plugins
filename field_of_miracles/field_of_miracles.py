import random

from database import *
from plugin_system import Plugin

plugin = Plugin('Поле чудес',
                usage=['поле чудес - чтобы начать игру',
                       'поле чудес очки - чтобы показать ваши текущие очки за игры',
                       'поле чудес сдаюсь - чтобы закончить игру'])


class FOMData(BaseModel):
    user_id = peewee.BigIntegerField(unique=True)

    lives = peewee.IntegerField(null=True)
    answer = peewee.TextField(null=True)
    description = peewee.TextField(null=True)

    cheating = peewee.BooleanField(default=False)

    open = peewee.TextField(null=True)

    score = peewee.IntegerField(default=0)


FOMData.create_table(True)


@plugin.on_message(status=1)
async def letter1(msg, args):
    if not await plugin.is_mine(msg.user):
        return

    cl = msg.text.strip().lower()

    d = await get_or_none(FOMData, user_id=msg.user_id)

    if not d:
        await plugin.clear_user(msg.user)

        return await msg.answer("Произошла ошибка!")

    if cl == d.answer:
        score = max(len(set(d.answer)) - len(d.open), 1)

        d.score += score
        await db.update(d)

        await plugin.clear_user(msg.user)

        return await msg.answer(f"👍 Вы угадали! Ответ: \"{d.answer}\"!\n"
                                f"👏 Ваши заработанные очки: {score}.\n"
                                f"🎉 Всего очков: {d.score}")

    if len(cl) != 1:
        if d.cheating:
            d.lives -= 1
            await db.update(d)

            return await msg.answer("💬 Назовите одну букву или ответ!\n"
                                    f"Жизни: {'<3 ' * d.lives}\n"
                                    f"👉 \"{d.description}\"")

        else:
            d.cheating = True
            await db.update(d)

        return await msg.answer("💬 Назовите одну букву или ответ!\n"
                                f"👉 \"{d.description}\"")

    if cl in d.open:
        return await msg.answer("🗿 Вы уже называли эту букву!\n"
                                "💬 Назовите букву или ответ!")

    d.open += cl

    current = ""
    done = True
    for l in d.answer:
        if l == " ":
            current += "_"
            continue

        if l in d.open:
            current += l

        else:
            current += "*"
            done = False

    if done:
        d.score += 1
        await db.update(d)

        await plugin.clear_user(msg.user)

        return await msg.answer(f"👍 Вы ответили верно! Слово: \"{d.answer}\"!\n"
                                f"👏 Ваши заработанные очки: 1.\n"
                                f"🎉 Всего очков: {d.score}")

    if cl not in d.answer:
        d.lives -= 1
        d.cheating = False
        await db.update(d)

        if d.lives < 1:
            await plugin.clear_user(msg.user)

            return await msg.answer(f"👋 Вы проиграли! Ответ: \"{d.answer}\"!\n")

        return await msg.answer(f"👋 Такой буквы нет!\n"
                                f"{' '.join(current)}\n"
                                f"Жизни: {'<3 ' * d.lives}\n\n"
                                f"💬 Назовите букву или ответ!\n"
                                f"👉 \"{d.description}\"")

    d.cheating = False
    await db.update(d)

    return await msg.answer(f"👋 Буква есть в слове!\n"
                            f"{' '.join(current)}\n"
                            f"Жизни: {'<3 ' * d.lives}\n\n"
                            f"💬 Назовите букву или ответ!\n"
                            f"👉 \"{d.description}\"")


@plugin.on_command('поле чудес')
async def main(msg, args):
    r, m = await plugin.lock(msg.user)

    if not r:
        return await msg.answer(m)

    v = random.choice(variants)

    u, c = await db.get_or_create(FOMData, user_id=msg.user_id)
    u.answer = v[1]
    u.description = v[0]
    u.open = ""
    u.lives = max(3, int(len(u.answer) * 0.7))
    await db.update(u)

    parts = [" *" * len(p) for p in u.answer.split()]

    result = " _".join(parts)[1:]

    await msg.answer(f"💭 Загадка:\n"
                     f"👉 {u.description}\n"
                     f"{result}\n"
                     f"💬 Назовите букву или ответ!")

    await plugin.set_user_status(msg.user, 1)


@plugin.on_command('поле чудес сдаюсь', 'поле чудес сдаться')
async def give_up(msg, args):
    if plugin.is_mine(msg.user):
        await plugin.clear_user(msg.user)

        d = await get_or_none(FOMData, user_id=msg.user_id)
        if d:
            await msg.answer(f"Ваше слово: \"{d.answer}\"")

    await plugin.set_user_status(msg.user, 1)


@plugin.on_command('поле чудес очки', 'поле чудес счёт')
async def show_score(msg, args):
    d = await get_or_none(FOMData, user_id=msg.user_id)

    if d:
        return await msg.answer(f"Ваши очки: \"{d.score}\"")

    await msg.answer(f"Вы не играли!")


variants = [
    ("Город в Бразилии, столица штата Баия", "салвадор"),
    ("Файловый менеджер с закрытым исходным кодом, работающий на платформе Microsoft Windows.", "диско командир"),
    ("Немецкая синти-поп и поп-рок группа, образованная в 2001 году в Магдебурге.", "tokio hotel"),
    ("Программа, подготавливающая код программы на языке C++ к компиляции.", "препроцессор"),
    ("Фильм ужасов 1975 года режиссёра Марио Сичильяно.", "дьявольский глаз"),
    ("Кухня казаков.", "казачья кухня"),
    ("Бинарное неорганическое соединение платины и алюминия с формулой AlPt, кристаллы.", "платинаалюминий"),
    ("Закрытый шахматный дебют, начинающийся ходами:1. d2-d4 d7-d52. c2-c4 c7-c6.Относится к закрытым началам.",
     "славянская защита"),
    ("Развитая племенная негосударственная организация древлян до подчинения Киеву.", "деревская земля"),
    ("Вымершая птица семейства попугаевых.", "виргинский ара"),
    ("Одна из крепостных башен Старого замка города Каменец-Подольский. Построена в конце XIV—XV вв.",
     "лянцкоронская башня"),
    ("Кинокомедия 2004 года, ремейк американского фильма «День сурка».", "уже вчера"),
    ("Бабочка семейства Коконопряды.", "коконопряд золотистый"),
    ("Рыба семейства вьюновые.", "обыкновенный вьюн"),
    ("Это явление, при котором ребёнок владеет двумя языками, причём использование языков не мешает друг другу.",
     "детский билингвизм"),
    ("Пятый эпизод девятнадцатого сезона мультсериала «Южный парк».", "безопасное пространство"),
    ("Пьеса Александра Островского. Написана в 1850 году.", "неожиданный случай"),
    ("Произведение Фридриха Ницше.", "весёлая наука"),
    ("Станица в Отрадненском районе Краснодарского края. Входит в состав Подгорно-Синюхинского сельского поселения.",
     "спокойная синюха"),
    ("Община в провинции Южная Голландия (Нидерланды).", "кромстрейен"),
]

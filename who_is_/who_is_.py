from random import choice

from plugin_system import Plugin

plugin = Plugin('Кто ... ?', usage=['кто <текст> - размышляет кто это может быть'])


@plugin.on_command('кто')
async def is_search(msg, args):
    if not args:
        return await msg.answer("Используй кто <текст>")

    try:
        users = await msg.vk.method('messages.getChatUsers', {'chat_id': msg.cid, 'fields': 'name'})
        user = choice(users)

        await msg.answer(f"{msg.text}? Я думаю, это {user['first_name']} {user['last_name']} 🙈")

    except TypeError:
        await msg.answer("Эту команду надо использовать только в беседе.")

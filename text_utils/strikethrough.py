from plugin_system import Plugin

plugin = Plugin('Перечеркиватель',
                usage=['перечеркнуть - перечеркивает строку'])

helptext = '''перечеркни <строка>'''


def get_sttext(text):
    sttext = '&#0822;'.join(text) + '&#0822;'
    return sttext


@plugin.on_command('зачеркни', 'перечеркни', "перечеркнуть")
async def strikethroughtext(msg, args):
    # Если нет аргументов
    if not args:
        return await msg.answer(helptext)

    text = ' '.join(args)

    await msg.answer('Готово:\n' + get_sttext(text))

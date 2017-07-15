from plugin_system import Plugin
from vbot import VERSION

plugin = Plugin("Информация о боте",
                usage=["о боте - вывод информации о боте"])


@plugin.on_command('about', "о боте")
async def command(msg, args):
    message = "🌍 VBot 🌍\n" \
              "🌲 VBot - бот, написанный на языке программирования Python, способный выполнять различные " \
              "команды, которые он может получать от пользователей. Бот может работать как пользователь или как " \
              "группа. Этот бот может развлекать и поддерживать конференции, группы и просто быть приятным " \
              "времяпровождением.\n" \
              "🌲 Версия: " + VERSION + "\n" \
              "🌲 https://github.com/VKBots/VBot"

    return await msg.answer(message)

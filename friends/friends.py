from plugin_system import Plugin
from utils import schedule_coroutine, load_settings

plugin = Plugin("Автоматическое добавление друзей(каждые 10 секунд)")


@plugin.on_init()
async def get_vk(vk):
    plugin.temp_data['s'] = load_settings(plugin)

    if not vk.tokens and plugin.temp_data['s']['accept']:
        schedule_coroutine(add_friends(vk))


# Функция, если её запустить(см. get_vk для примера с выполнением в фоне),
# будет выполняться каждые 10 секунд, до тех пор, пока stopper.stop == False

# Функция обязана принимать 1 обязательны параметр - stopper, но может
# принимать и больше
@plugin.schedule(10)
async def add_friends(stopper, vk):
    stopper.sleep = int(plugin.temp_data['s']['time'])

    result = await vk.method("friends.getRequests")

    if not result or not result["count"]:
        return

    users = result["items"]

    for user in users:
        await vk.method("friends.add", {"user_id": user})

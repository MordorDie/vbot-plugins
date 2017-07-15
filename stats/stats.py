import datetime

import hues

from plugin_system import Plugin
from settings import GROUP_ID
from utils import schedule_coroutine, load_settings

plugin = Plugin('Счётчики',
                usage=['обновляет статус бота каждые 5 секунд'])


@plugin.on_init()
async def setup_counter(vk):
    plugin.temp_data['s'] = load_settings(plugin)

    if plugin.temp_data['s']['set_status']:
        schedule_coroutine(update_counters(vk))


@plugin.schedule(5)
async def update_counters(stopper, vk):
    stopper.sleep = int(plugin.temp_data['s']['time'])

    STATISTICS = vk.bot.STATISTICS

    if datetime.datetime.now() - STATISTICS['new_time'] >= datetime.timedelta(days=1):
        STATISTICS["amount"] = 0
        STATISTICS['new_time'] = datetime.datetime.now()

    uptime = (datetime.datetime.now() - STATISTICS['time']).total_seconds()

    hours, remainder = divmod(uptime, 3600)
    minutes, seconds = divmod(remainder, 60)

    message = f"uptime: {'%02d:%02d:%02d' % (hours, minutes, seconds)} | всего сообщений: {STATISTICS['amount']} | " \
              f"сообщений за 24 часа: {STATISTICS['all_amount']}"

    v = {"text": message}
    if GROUP_ID:
        v["group_id"] = GROUP_ID
    elif vk.tokens:
        return hues.error("Невозможно установить статус! Вы не указала ID группы!")

    result = await vk.method("status.set", v)

    if result == 0:
        hues.error("Не удалось установить статус! Для изменения статуса необходи аккаунт администратора группы!")

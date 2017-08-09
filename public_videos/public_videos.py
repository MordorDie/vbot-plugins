import random

from plugin_system import Plugin
from utils import load_settings
from database import *

plugin = Plugin('Видео группы', usage=['Для получения в ЛС видео введите: видео'])


class UserVideos(BaseModel):
    user_id = peewee.BigIntegerField(unique=True)
    video_list = peewee.TextField(default='')

UserVideos.create_table(True)


@plugin.on_init()
async def check_group_videos(vk):
    # await send_videos(vk)
    plugin.temp_data['s'] = load_settings(plugin)
    # Получаем количество видео в группе
    values = {
        'owner_id': -int(plugin.temp_data['s']['public_id']),
        'count': 0
    }
    resp = await vk.method('video.get', values)
    if resp:
        plugin.temp_data['public_video_count'] = resp.get('count')


@plugin.on_command('случайное видео')
async def send_videos(msg, args):
    """Отправляет пользователю видео из группы, записывает в базу уже отправленные"""
    if not plugin.temp_data.get('public_video_count'):
        return await msg.answer('Группа закрыта или в ней нет видеозаписей')
    user, create = await db.get_or_create(UserVideos, user_id=msg.user_id)
    videos = await get_videos(msg.vk)
    video_list = []
    for vid in videos:
        attach_link = f"video{vid['owner_id']}_{vid['id']}"
        if attach_link not in user.video_list:
            video_list.append(attach_link)
        if len(video_list) == int(plugin.temp_data['s']['total_videos']):
            break

    if not video_list:
        return await msg.answer('Все видео группы были отправлены вам в лс.\n'
                                'Для сброса счетчика напишите "сбросить счетчик"')
    attachment = ','.join(video_list)
    user.video_list += attachment + ','
    user.save()
    print(user.video_list)
    await msg.answer('Приятного просмотра!', attachment=attachment)


@plugin.on_command('сбросить счетчик', 'сбросить счётчик')
async def reset_counter(msg, args):
    """Сбрасывает отправленные пользователю видео"""
    user = await get_or_none(UserVideos, user_id=msg.user_id)
    user.video_list = ''
    user.save()
    await msg.answer('Счетчик просмотров успешно сброшен')


async def get_videos(vk):
    """Возвращает 200 видео из группы по случайному срезу"""
    public_video_count = plugin.temp_data['public_video_count']
    offset = 0
    if public_video_count > 200:
        offset = random.randint(0, public_video_count-200)
    values = {'owner_id': -int(plugin.temp_data['s']['public_id']),
              'count': 200,
              'offset': offset,
              }
    resp = await vk.method('video.get', values)
    videos = resp.get('items')
    return videos


import os
import logging
from random import randint

from vk_api import bot_longpoll, VkApi

# Подтягиваем чувствительные данные из переменных окружения
assert 'VK_TEST_BOT_TOKEN' in os.environ, 'Environment variable VK_TEST_BOT_TOKEN is not exist'
assert 'VK_TEST_BOT_GROUP_ID' in os.environ, 'Environment variable VK_TEST_BOT_TOKEN is not exist'
DEV_VK_TOKEN = os.environ.get('VK_TEST_BOT_TOKEN')
DEV_GROUP_ID = os.environ.get('VK_TEST_BOT_GROUP_ID')

# Настраиваем логгер
bot_logger = logging.Logger(__name__, logging.DEBUG)
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
console_handler.setFormatter(console_formatter)
bot_logger.addHandler(console_handler)


class Bot:
    max_random_id = int('1'*63, 2)      # Int64

    def __init__(self, token, group_id):
        self.session = VkApi(token=token)
        self.vk_bot = bot_longpoll.VkBotLongPoll(self.session, group_id)
        self.api = self.session.get_api()
        bot_logger.info('Bot: Initialized')

    def start(self):
        bot_logger.info('Bot: Start listening')
        for event in self.vk_bot.listen():
            try:
                self._on_event(event)
            except Exception as exc:
                bot_logger.error(exc)

    def _on_event(self, event):
        if event.type == bot_longpoll.VkBotEventType.MESSAGE_NEW:
            self._on_message(event)
        else:
            bot_logger.debug(f'Bot: Unknown event type {event.type}')

    def _on_message(self, event):
        bot_logger.info(f'Bot: Message received. Peer ID: {event.message.peer_id}. Message: {event.message.text}')
        self.send_message(event.message.peer_id,event.message.text.upper())

    def send_message(self, peer_id, message):
        self.api.messages.send(user_id=peer_id, message=message, random_id=randint(0, self.max_random_id))
        bot_logger.info(f'Bot: Message sent. Peer ID: {peer_id}. Message: {message}')


echo_bot = Bot(DEV_VK_TOKEN, DEV_GROUP_ID)
echo_bot.start()


#!/usr/bin/env python3.7

import os
import logging
from random import randint

from vk_api import bot_longpoll, VkApi


bot_logger = logging.Logger('vk_bot', logging.DEBUG)


def logging_config():
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    console_handler.setFormatter(console_formatter)
    bot_logger.addHandler(console_handler)

    file_handler = logging.FileHandler('bot.log', mode='a', delay=True)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%d-%m-%Y %H:%M')
    file_handler.setFormatter(file_formatter)
    bot_logger.addHandler(file_handler)


class Bot:
    """
    Echo bot для vk.com

    use python3.7
    """
    max_random_id = int('1'*63, 2)      # Int64

    def __init__(self, token, group_id):
        """

        Parameters
        ----------
        token: str
            Ключ доступа к сообществу
        group_id: str
            ID сообщества

        """
        self.session = VkApi(token=token)
        self.vk_bot = bot_longpoll.VkBotLongPoll(self.session, group_id)
        self.api = self.session.get_api()
        bot_logger.info('Bot: Initialized')

    def start(self):
        """ Запуск бота """
        bot_logger.info('Bot: Start listening')
        for event in self.vk_bot.listen():
            try:
                self._on_event(event)
            except Exception:
                bot_logger.exception('Event handling error')

    def _on_event(self, event):
        """
        Основной обработчик прилетевших из вк событий

        Parameters
        ----------
        event: VkBotEvent

        """
        if event.type == bot_longpoll.VkBotEventType.MESSAGE_NEW:
            self._on_message(event)
        else:
            bot_logger.debug(f'Bot: Unknown event type {event.type}')

    def _on_message(self, event):
        """
        Обработчик прилетевших из вк событий сообщений. Отвечает отправителю капсом его же сообщением

        Parameters
        ----------
        event: VkBotMessageEvent

        """
        bot_logger.info(f'Bot: Message received. Peer ID: {event.message.peer_id}. Message: {event.message.text}')
        if 'отключ' in event.message.text.lower():
            self.send_message(event.message.peer_id, 'Ну ладно тебе. Нормально ж общались(')
        else:
            self.send_message(event.message.peer_id, event.message.text.upper())

    def send_message(self, peer_id, message):
        """
        Метод для отправки текстовых сообщений

        Parameters
        ----------
        peer_id: str or int
            ID получателя
        message: str
            Текст сообщения

        """
        self.api.messages.send(user_id=peer_id, message=message, random_id=randint(0, self.max_random_id))
        bot_logger.info(f'Bot: Message sent. Peer ID: {peer_id}. Message: {message}')


if __name__ == '__main__':
    # Подтягиваем чувствительные данные из переменных окружения
    assert 'VK_TEST_BOT_TOKEN' in os.environ, 'Environment variable VK_TEST_BOT_TOKEN is not exist'
    assert 'VK_TEST_BOT_GROUP_ID' in os.environ, 'Environment variable VK_TEST_BOT_TOKEN is not exist'
    DEV_VK_TOKEN = os.environ.get('VK_TEST_BOT_TOKEN')
    DEV_GROUP_ID = os.environ.get('VK_TEST_BOT_GROUP_ID')

    logging_config()

    echo_bot = Bot(DEV_VK_TOKEN, DEV_GROUP_ID)
    echo_bot.start()

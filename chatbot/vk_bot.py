#!/usr/bin/env python3.7

import os
import logging
from random import randint

from vk_api import bot_longpoll, VkApi

import scenarios
import handlers


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


class UserState:
    """
    Состояние пользователя внутри сценария
    """
    def __init__(self, scenario_name, step_name, context=None):
        """

        Parameters
        ----------
        scenario_name: str
            имя сценария
        step_name: str
            имя шага
        context: dict
            контекст - накопленные данные пользователя
        """
        self.scenario_name = scenario_name
        self.step_name = step_name
        self.context = context or {}


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
        self.user_states = dict()       # peer_id -> UserState

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
        message_text = event.message.text
        peer_id = event.message.peer_id
        bot_logger.info(f'Bot: Message received. Peer ID: {peer_id}. Message: {message_text}')

        if peer_id in self.user_states:
            # continue scenario
            text_to_send = self.continue_scenario(message_text, peer_id)

        else:
            # search intent
            for intent in scenarios.INTENTS:
                if any(token in message_text for token in intent['tokens']):
                    # run intent
                    if intent['answer']:
                        text_to_send = intent['answer']
                    else:
                        # launch new scenario
                        text_to_send = self.start_scenario(peer_id, intent['scenario'])
                    break
                else:
                    text_to_send = scenarios.DEFAULT_ANSWER

        self.send_message(peer_id, text_to_send)


    def start_scenario(self, peer_id, scenario_name):
        scenario = scenarios.SCENARIOS[scenario_name]
        first_step = scenario['first_step']
        step = scenario['steps'][first_step]
        text_to_send = step['text']
        self.user_states[peer_id] = UserState(scenario_name, first_step)
        return text_to_send

    def continue_scenario(self, message_text, peer_id):
        state = self.user_states[peer_id]
        steps = scenarios.SCENARIOS[state.scenario_name]['steps']
        step = steps[state.step_name]
        handler = getattr(handlers, step['handler'])
        if handler(message_text, state.context):
            # next step
            next_step = steps[step['next_step']]
            text_to_send = next_step['text'].format(**state.context)
            if next_step['next_step']:
                # switch to next step
                state.step_name = step['next_step']
            else:
                # finish scenario
                self.user_states.pop(peer_id)
        else:
            # retry current step
            text_to_send = step['failure'].format(**state.context)
        return text_to_send

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

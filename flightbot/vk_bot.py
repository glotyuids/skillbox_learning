#!/usr/bin/env python3.7

"""
Вк-бот, работающий по заданным сценариям
"""

import os
import logging
from random import randint
from dataclasses import dataclass, field

from vk_api import bot_longpoll, VkApi

import scenarios
import handlers


bot_logger = logging.Logger('vk_bot', logging.DEBUG)


def logging_config():
    """
    Настраиваем логгер. Пишем и в файл (дополняем существующий), и на консоль
    """
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s [%(levelname)s] [%(name)s] %(message)s')
    console_handler.setFormatter(console_formatter)
    bot_logger.addHandler(console_handler)

    file_handler = logging.FileHandler('bot.log', mode='a', delay=True)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s',
                                       datefmt='%d-%m-%Y %H:%M')
    file_handler.setFormatter(file_formatter)
    bot_logger.addHandler(file_handler)


@dataclass
class UserState:
    """
    Состояние пользователя внутри сценария
    """
    scenario_name: str
    step_name: str
    context: dict = field(default_factory=dict)


class ScenarioResultError(ValueError):
    """
    Исключение для отлова невалидных шагов с результатами вида (None, None)
    """
    def __init__(self, user_state, result_name):
        """

        Parameters
        ----------
        user_state: UserState
        result_name: str
            Строка вида 'result_0'
        """
        self.scenario = user_state.scenario_name
        self.step = user_state.step_name
        self.result_name = result_name
        self.result_value = scenarios.SCENARIOS[self.scenario]['steps'][self.step][result_name]
        self.message = 'Both values in result tuple is None: ' + \
                       '/'.join(['SCENARIOS', self.scenario, 'steps', self.step, self.result_name]) + \
                       ': ' + repr(self.result_value)
        super().__init__(self.message)

    def __str__(self):
        return self.message


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
        bot_logger.info('Initialized')
        self.user_states = dict()       # peer_id -> UserState

    def start(self):
        """ Запуск бота """
        bot_logger.info('Start listening')
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
            bot_logger.debug('Unknown event type %s', event.type)

    def _on_message(self, event):
        """
        Обработчик прилетевших из вк событий сообщений

        Parameters
        ----------
        event: VkBotMessageEvent

        """
        message_text = event.message.text
        peer_id = event.message.peer_id
        bot_logger.info('Message received. Peer ID: %s. Message: %s', peer_id, repr(message_text))
        text_to_send = self.commands_handler(peer_id, message_text)

        if not text_to_send:
            if peer_id in self.user_states:
                # continue scenario
                text_to_send = self.continue_scenario(peer_id, message_text)
            else:
                # search intent
                for intent in scenarios.INTENTS:
                    if any(token in message_text.lower() for token in intent['tokens']):
                        # run intent
                        bot_logger.info('User %s gets intent %s', peer_id, intent['name'])
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
        """
        Запускает выбранный сценарий для пользователя
        Parameters
        ----------
        peer_id: str
            Vk ID пользователя
        scenario_name: str
            Имя сценария, который нужно запустить

        Returns
        -------
        str
            Текст сообщения, который берётся из первого шага сценария
        """
        bot_logger.info('User %s started scenario intent %s', peer_id, scenario_name)
        scenario = scenarios.SCENARIOS[scenario_name]
        first_step = scenario['first_step']
        step = scenario['steps'][first_step]
        text_to_send = step['text']
        self.user_states[peer_id] = UserState(scenario_name=scenario_name, step_name=first_step)
        return text_to_send

    def continue_scenario(self, peer_id, message_text):
        """
        Пропускает сообщение через хендлер шага,
        дёргает соответсвующее сообщение из сценария и переключает шаги.
        Если хендлер шага возвращает False, то возвращаем сообщение failure из текущего шага.
        Если True - то переключаем пользователя на следубщий шаг и возвращаем из него сообщение text
        Parameters
        ----------
        message_text: str
            Текст сообщения, присланного пользователем
        peer_id: str
            Vk ID пользователя

        Returns
        -------
        str
            Текст сообщения, который берётся из сценария.
        """
        state = self.user_states[peer_id]
        steps = scenarios.SCENARIOS[state.scenario_name]['steps']
        step = steps[state.step_name]
        handler = getattr(handlers, step['handler'])
        ret_code = handler(message_text, state.context)
        if ret_code == 0:
            # next step
            next_step = steps[step['next_step']]
            text_to_send = next_step['text'].format(**state.context)
            if next_step['next_step']:
                # switch to next step
                state.step_name = step['next_step']
            else:
                # finish scenario
                bot_logger.info('User %s finished scenario %s. Context: %s',
                                peer_id, state.scenario_name, state.context)
                self.user_states.pop(peer_id)
        else:
            # retry current step
            text_to_send = step['failure_' + str(ret_code)].format(**state.context)
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
        self.api.messages.send(user_id=peer_id,
                               message=message,
                               random_id=randint(0, self.max_random_id))
        bot_logger.info('Message sent. Peer ID: %s. Message: %s', peer_id, repr(message))

    def commands_handler(self, peer_id, message_text):
        if message_text == '/exit':
            if peer_id in self.user_states:
                state = self.user_states[peer_id]
                bot_logger.info('User %s cancelled scenario %s. Context: %s',
                                peer_id, state.scenario_name, state.context)
                self.user_states.pop(peer_id)
            return scenarios.HELP_ANSWER
        if message_text == '/help':
            return scenarios.HELP_ANSWER
        return None


if __name__ == '__main__':
    # Подтягиваем чувствительные данные из переменных окружения
    assert 'VK_BOT_TOKEN' in os.environ, 'Environment variable VK_BOT_TOKEN is not exist'
    assert 'VK_BOT_GROUP_ID' in os.environ, 'Environment variable VK_BOT_TOKEN is not exist'
    DEV_VK_TOKEN = os.environ['VK_BOT_TOKEN']
    DEV_GROUP_ID = os.environ['VK_BOT_GROUP_ID']

    logging_config()

    echo_bot = Bot(DEV_VK_TOKEN, DEV_GROUP_ID)
    echo_bot.start()

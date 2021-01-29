import unittest
from copy import deepcopy
from datetime import datetime
from unittest.mock import Mock, patch, call

patch.dict('os.environ', {'RAPIDAPI_KEY': 'AAA'}, clear=True).start()
import skyscanner_api as skyapi
from vk_api.bot_longpoll import VkBotMessageEvent
import scenarios
import vk_bot


class VKBotTestCase(unittest.TestCase):
    RAW_EVENT = {
        'type': 'message_new',
        'object': {
            'message': {
                'date': 1602440563, 'from_id': 25833442, 'id': 86, 'out': 0,
                'peer_id': 25833442, 'text': 'Hello', 'conversation_message_id': 84,
                'fwd_messages': [], 'important': False, 'random_id': 0, 'attachments': [],
                'is_hidden': False
            },
            'client_info': {
                'button_actions': ['text', 'vkpay', 'open_app', 'location', 'open_link'],
                'keyboard': True, 'inline_keyboard': True, 'carousel': False,
                'lang_id': 0
            }
        },
        'group_id': 197090073,
        'event_id': 'cda2978fe40bb257ba476407ad8ca57c5d3c6b08'}
    ORIGIN = skyapi.Place('Москва', 'MOW', 'Россия')
    DEST = skyapi.Place('Белгород', 'EGO', 'Россия')
    FLIGHT = skyapi.Flight(
        price=500,
        direct=True,
        origin=ORIGIN,
        dest=DEST,
        arrival=datetime(2021, 2, 12),
        carrier='S7'
    )
    SEATS = '2'
    COMMENT = 'Это коммент'
    TEST_CONTEXT = {
        'origin': ORIGIN,
        'dest': DEST,
        'flight': FLIGHT,
        'seats': SEATS,
        'comment': COMMENT
    }
    STEPS = scenarios.SCENARIOS['find_flights']['steps']
    TD_INTENTS = [
        ('Привет', scenarios.INTENTS[1]['answer']),
        ('/помощь', scenarios.INTENTS[0]['answer']),
        ('вапвапв', scenarios.DEFAULT_ANSWER),
        ('/билет', STEPS['enter_arrival']['text']),
        ('/выход', scenarios.WELCOME_ANSWER),
        ]
    TD_TICKET = [
        ('/билет', STEPS['enter_arrival']['text']),
        ('/помощь', scenarios.SCENARIOS['find_flights']['help']),
        ('sdfsdfsfd', STEPS['enter_arrival']['result_1'][0]),
        ('Москва', STEPS['enter_dest']['text'].format(**TEST_CONTEXT)),
        ('sdfsdfsfd', STEPS['enter_dest']['result_1'][0]),
        ('Белгород', STEPS['enter_date']['text'].format(**TEST_CONTEXT)),
        ('sdfsdfsfd', STEPS['enter_date']['result_1'][0]),
        ('12-02-2021', STEPS['enter_seats']['text'].format(**TEST_CONTEXT)),
        ('sdfsdfsfd', STEPS['enter_seats']['result_1'][0]),
        ('100000', STEPS['enter_seats']['result_2'][0]),
        ('0', STEPS['enter_seats']['result_3'][0]),
        (SEATS, STEPS['enter_comment']['text']),
        (COMMENT, STEPS['verify_data']['text'].format(**TEST_CONTEXT)),
        ('далее', STEPS['enter_phone']['text']),
        ('sdfsdfsfd', STEPS['enter_phone']['result_1'][0]),
        ('+7 999 123 45 67', STEPS['finish']['text']),
        ('Привет', scenarios.INTENTS[1]['answer']),
    ]

    def test_run(self):
        count = 5
        obj = {'1': 1}
        events = [obj] * count
        listen_mock = Mock(return_value=events)
        longpoller_mock = Mock()
        longpoller_mock.listen = listen_mock

        with patch('vk_bot.VkApi'):
            with patch('vk_bot.bot_longpoll.VkBotLongPoll', return_value=longpoller_mock):
                bot = vk_bot.Bot('', '')
                bot._on_event = Mock()
                bot.start()

                self.assertEqual(True, bot._on_event.called)
                self.assertEqual(count, bot._on_event.call_count)
                bot._on_event.assert_called_with(obj)

                # Проверяем, что отлавливается исключение
                with patch('vk_bot.bot_logger.exception') as exc_logger_mock:
                    bot._on_event = Mock(side_effect=ValueError())
                    bot.start()
                    self.assertEqual(True, exc_logger_mock.called)
                    exc_logger_mock.assert_called_with('Event handling error')

    def test_on_event(self):
        event = VkBotMessageEvent(raw=self.RAW_EVENT)

        with patch('vk_bot.VkApi'):
            with patch('vk_bot.bot_longpoll.VkBotLongPoll'):
                with patch('vk_bot.Bot._on_message') as on_message_mock:
                    bot = vk_bot.Bot('', '')
                    bot._on_event(event=event)

                    self.assertEqual(True, on_message_mock.called)
                    on_message_mock.assert_called_with(event)

                    # Проверяем обработку незнакомого ивента
                    event.type = 'bad_event_for_test'
                    with patch('vk_bot.bot_logger.debug') as logger_mock:
                        bot._on_event(event=event)
                        self.assertEqual(True, logger_mock.called)
                        logger_mock.assert_called_with('Unknown event type %s', event.type)

    def test_intents(self):
        send_message_mock = Mock()
        msg_event = deepcopy(self.RAW_EVENT)

        with patch('vk_bot.VkApi'), \
             patch('vk_bot.bot_longpoll.VkBotLongPoll'):
            bot = vk_bot.Bot('', '')
            bot.send_message = send_message_mock

            for message_text, _ in self.TD_INTENTS:
                msg_event['object']['message']['text'] = message_text
                bot._on_message(event=VkBotMessageEvent(raw=msg_event))

            self.assertEqual(True, send_message_mock.called)
            self.assertEqual(len(self.TD_INTENTS), send_message_mock.call_count)
            expected_calls = [call(msg_event['object']['message']['peer_id'], response)
                              for _, response in self.TD_INTENTS]
            send_message_mock.assert_has_calls(expected_calls, any_order=False)

    def test_scenario_ticket(self):
        send_message_mock = Mock()
        msg_event = deepcopy(self.RAW_EVENT)

        with patch('vk_bot.VkApi'), \
             patch('vk_bot.bot_longpoll.VkBotLongPoll'), \
             patch('skyscanner_api.get_flight', return_value=self.FLIGHT), \
             patch('skyscanner_api.get_dates', return_value=['2021-02-12']), \
             patch('skyscanner_api.get_city', side_effect=[None, self.ORIGIN, None, self.DEST], return_value=None):
            bot = vk_bot.Bot('', '')
            bot.send_message = send_message_mock

            for message_text, _ in self.TD_INTENTS:
                msg_event['object']['message']['text'] = message_text
                bot._on_message(event=VkBotMessageEvent(raw=msg_event))

            self.assertEqual(True, send_message_mock.called)
            self.assertEqual(len(self.TD_INTENTS), send_message_mock.call_count)
            expected_calls = [call(msg_event['object']['message']['peer_id'], response)
                              for _, response in self.TD_INTENTS]
            send_message_mock.assert_has_calls(expected_calls, any_order=False)

    def test_send_message(self):
        peer_id, message = 5001, 'Hello'
        send_message_mock = Mock()
        with patch('vk_bot.VkApi'):
            with patch('vk_bot.bot_longpoll.VkBotLongPoll'):
                bot = vk_bot.Bot('', '')
                bot.api = Mock()
                bot.api.messages.send = send_message_mock
                bot.send_message(peer_id=peer_id, message=message)

                self.assertEqual(True, send_message_mock.called)
                # Можно было бы просто замокать рандинт, либо использовать ANY,
                # но в данном случае мне важно, чтобы на сторонний сервис уходили корректные данные.
                # Конечно, остаётся неопределённость с тем, будет ли корректно передаваться random_id каждый раз,
                # но можно хотя бы убедиться, что random_id входит в диапазон, требуемый сервисом
                send_kwargs = send_message_mock.call_args_list[0][1]
                self.assertEqual((peer_id, message, True),
                                 (send_kwargs['user_id'], send_kwargs['message'],
                                  send_kwargs['random_id'] in range(0, vk_bot.Bot.max_random_id + 1)))


if __name__ == '__main__':
    unittest.main()

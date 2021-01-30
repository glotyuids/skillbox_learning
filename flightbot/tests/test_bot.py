import unittest
from copy import deepcopy
from unittest.mock import Mock, patch, call

from vk_api.bot_longpoll import VkBotMessageEvent
import vk_bot

import test_data as td


class VKBotTestCase(unittest.TestCase):
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
        event = VkBotMessageEvent(raw=td.RAW_EVENT)

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
        msg_event = deepcopy(td.RAW_EVENT)

        with patch('vk_bot.VkApi'), \
             patch('vk_bot.bot_longpoll.VkBotLongPoll'):
            bot = vk_bot.Bot('', '')
            bot.send_message = send_message_mock

            for message_text, _ in td.INTENTS:
                msg_event['object']['message']['text'] = message_text
                bot._on_message(event=VkBotMessageEvent(raw=msg_event))

            self.assertEqual(True, send_message_mock.called)
            self.assertEqual(len(td.INTENTS), send_message_mock.call_count)
            expected_calls = [call(msg_event['object']['message']['peer_id'], response)
                              for _, response in td.INTENTS]
            send_message_mock.assert_has_calls(expected_calls, any_order=False)

    def test_scenario_ticket(self):
        send_message_mock = Mock()
        msg_event = deepcopy(td.RAW_EVENT)

        with patch('vk_bot.VkApi'), \
             patch('vk_bot.bot_longpoll.VkBotLongPoll'), \
             patch('skyscanner_api.get_flight', return_value=td.FLIGHT), \
             patch('skyscanner_api.get_dates', return_value=['2021-02-12']), \
             patch('skyscanner_api.get_city', side_effect=[None, td.ORIGIN, None, td.DEST], return_value=None):
            bot = vk_bot.Bot('', '')
            bot.send_message = send_message_mock

            for message_text, _ in td.INTENTS:
                msg_event['object']['message']['text'] = message_text
                bot._on_message(event=VkBotMessageEvent(raw=msg_event))

            self.assertEqual(True, send_message_mock.called)
            self.assertEqual(len(td.INTENTS), send_message_mock.call_count)
            expected_calls = [call(msg_event['object']['message']['peer_id'], response)
                              for _, response in td.INTENTS]
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

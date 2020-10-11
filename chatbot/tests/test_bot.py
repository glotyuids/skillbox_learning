import unittest
from unittest.mock import Mock, patch

from vk_api.bot_longpoll import VkBotMessageEvent

import vk_bot


class VKBotTestCase(unittest.TestCase):
    RAW_EVENT = {'type': 'message_new',
                 'object': {'message': {'date': 1602440563, 'from_id': 25833442, 'id': 86, 'out': 0,
                                        'peer_id': 25833442, 'text': 'Hello', 'conversation_message_id': 84,
                                        'fwd_messages': [], 'important': False, 'random_id': 0, 'attachments': [],
                                        'is_hidden': False},
                            'client_info': {'button_actions': ['text', 'vkpay', 'open_app', 'location', 'open_link'],
                                            'keyboard': True, 'inline_keyboard': True, 'carousel': False, 'lang_id': 0}},
                 'group_id': 197090073,
                 'event_id': 'cda2978fe40bb257ba476407ad8ca57c5d3c6b08'}

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

    def test_on_event(self):
        event = VkBotMessageEvent(raw=self.RAW_EVENT)
        on_message_mock = Mock()
        vk_bot.Bot._on_message = on_message_mock

        with patch('vk_bot.VkApi'):
            with patch('vk_bot.bot_longpoll.VkBotLongPoll'):
                bot = vk_bot.Bot('', '')
                bot._on_event(event=event)

        self.assertEqual(True, on_message_mock.called)
        on_message_mock.assert_called_with(event)

    def test_on_message(self):
        message_event = VkBotMessageEvent(raw=self.RAW_EVENT)
        send_message_mock = Mock()
        vk_bot.Bot.send_message = send_message_mock

        with patch('vk_bot.VkApi'):
            with patch('vk_bot.bot_longpoll.VkBotLongPoll'):
                bot = vk_bot.Bot('', '')
                bot._on_message(event=message_event)

                self.assertEqual(True, send_message_mock.called)
                send_message_mock.assert_called_with(message_event.message.peer_id, message_event.message.text.upper())

                message_event.message.text = 'отключу'
                bot._on_message(event=message_event)

                send_message_mock.assert_called_with(message_event.message.peer_id,
                                                     'Ну ладно тебе. Нормально ж общались(')





if __name__ == '__main__':
    unittest.main()

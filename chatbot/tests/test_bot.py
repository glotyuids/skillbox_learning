import unittest
from unittest.mock import Mock, patch

import vk_bot


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


if __name__ == '__main__':
    unittest.main()

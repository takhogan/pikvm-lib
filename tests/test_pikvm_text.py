import string
import unittest
from unittest.mock import patch, MagicMock

from pikvm_lib.keymaps import TEXT_KEYMAP, TYPEABLE_CHARACTERS, find_untypeable, text_to_keys
from pikvm_lib.pikvm import PiKVM
from pikvm_lib.pikvm_websocket import PiKVMWebsocket
import mock_pikvm_response


# Typing text either types exactly what it was given or refuses it before any
# key is sent: a VDI_WriteFile that types the wrong bytes writes a wrong file
# without a word. "\r" used to be typed as Space and a character with no key
# (an accented letter, say) was dropped.


def sent_keys(create_event):
    """The (key code, state) of each event, in the order sent."""
    return [c[0] for c in create_event.call_args_list]


class TestTypeableCharacters(unittest.TestCase):
    def test_printable_ascii_tab_and_line_breaks(self):
        self.assertEqual(TYPEABLE_CHARACTERS, frozenset(string.printable) - {'\x0b', '\x0c'})

    def test_every_typeable_character_has_one_key(self):
        for char in string.ascii_lowercase:
            self.assertEqual(TEXT_KEYMAP[char], (f"Key{char.upper()}", False))
            self.assertEqual(TEXT_KEYMAP[char.upper()], (f"Key{char.upper()}", True))
        self.assertEqual(TEXT_KEYMAP['7'], ("Digit7", False))
        self.assertEqual(TEXT_KEYMAP['&'], ("Digit7", True))
        self.assertEqual(TEXT_KEYMAP[' '], ("Space", False))
        self.assertEqual(TEXT_KEYMAP['\t'], ("Tab", False))
        self.assertEqual(TEXT_KEYMAP['\n'], ("Enter", False))
        self.assertEqual(TEXT_KEYMAP['"'], ("Quote", True))
        self.assertEqual(TEXT_KEYMAP["'"], ("Quote", False))
        self.assertEqual(TEXT_KEYMAP[':'], ("Semicolon", True))
        self.assertEqual(TEXT_KEYMAP['\\'], ("Backslash", False))

    def test_find_untypeable(self):
        self.assertIsNone(find_untypeable('C:\\Users\\x\\a:b.txt\r\n\tdone'))
        self.assertEqual(find_untypeable('café'), (3, 'é'))
        self.assertEqual(find_untypeable('a\x0bb'), (1, '\x0b'))
        self.assertEqual(find_untypeable('a\u00a0b'), (1, '\u00a0'))

    def test_line_breaks_are_one_enter_each(self):
        self.assertEqual(text_to_keys('a\r\nb'), ['a', '\n', 'b'])
        self.assertEqual(text_to_keys('a\nb'), ['a', '\n', 'b'])
        self.assertEqual(text_to_keys('a\rb'), ['a', '\n', 'b'])
        self.assertEqual(text_to_keys('a\r\n\r\nb'), ['a', '\n', '\n', 'b'])
        self.assertEqual(text_to_keys('a\n\rb'), ['a', '\n', '\n', 'b'])
        self.assertEqual(text_to_keys('end\r'), ['e', 'n', 'd', '\n'])

    def test_untypeable_text_raises_naming_the_character_and_position(self):
        with self.assertRaises(ValueError) as raised:
            text_to_keys('naïve')
        self.assertIn("'ï'", str(raised.exception))
        self.assertIn('U+00EF', str(raised.exception))
        self.assertIn('position 2', str(raised.exception))


class TestKeyboardWrite(unittest.TestCase):
    def setUp(self):
        patch('pikvm_lib.pikvm.PiKVM.get_system_info',
              return_value=mock_pikvm_response.pikvm_mock_info).start()
        self.addCleanup(patch.stopall)
        self.keyboard = PiKVM("example.com", "user", "password", schema="https", ws_client=MagicMock())
        self.keyboard.ws_client = MagicMock()
        self.sleep = patch('time.sleep').start()

    def test_write_types_exactly(self):
        self.keyboard.write('A:\r\n\tb')
        self.assertEqual(sent_keys(self.keyboard.ws_client._create_event), [
            ('ShiftLeft', 'true'), ('KeyA', 'true'), ('KeyA', 'false'), ('ShiftLeft', 'false'),
            ('ShiftLeft', 'true'), ('Semicolon', 'true'), ('Semicolon', 'false'), ('ShiftLeft', 'false'),
            ('Enter', 'true'), ('Enter', 'false'),
            ('Tab', 'true'), ('Tab', 'false'),
            ('KeyB', 'true'), ('KeyB', 'false'),
        ])

    def test_lone_carriage_return_is_enter_not_space(self):
        self.keyboard.write('a\rb')
        self.assertIn(('Enter', 'true'), sent_keys(self.keyboard.ws_client._create_event))
        self.assertNotIn(('Space', 'true'), sent_keys(self.keyboard.ws_client._create_event))

    def test_write_refuses_untypeable_text_before_typing_anything(self):
        with self.assertRaises(ValueError) as raised:
            self.keyboard.write('abc é')
        self.assertIn('position 4', str(raised.exception))
        self.keyboard.ws_client._send_with_retry.assert_not_called()

    def test_typewrite_is_write(self):
        self.keyboard.typewrite('x')
        self.assertEqual(sent_keys(self.keyboard.ws_client._create_event), [('KeyX', 'true'), ('KeyX', 'false')])

    def test_press_refuses_a_character_with_no_key(self):
        for char in ('é', '٣', '\u00a0', '\x0c'):
            with self.assertRaises(ValueError):
                self.keyboard.press(char)
        self.keyboard.ws_client._send_with_retry.assert_not_called()

    def test_press_still_takes_named_keys(self):
        self.keyboard.press('enter')
        self.keyboard.ws_client._create_event.assert_any_call('Enter', 'true')


class TestWebsocketSendInput(unittest.TestCase):
    def setUp(self):
        with patch("websocket.WebSocket") as mock_websocket:
            mock_websocket.return_value = MagicMock()
            self.ws = PiKVMWebsocket("example.com", "user", "password")
        self.ws.send_key = MagicMock()
        self.ws._send_with_retry = MagicMock()
        patch('time.sleep').start()
        self.addCleanup(patch.stopall)

    def test_line_breaks_and_tab(self):
        self.ws.send_input('a\r\nb\rc\nd\te')
        keys = [c[0][0] for c in self.ws.send_key.call_args_list]
        self.assertEqual(keys, ['KeyA', 'Enter', 'KeyB', 'Enter', 'KeyC', 'Enter', 'KeyD', 'Tab', 'KeyE'])

    def test_double_quote_is_typed_once(self):
        self.ws.send_input('"')
        keys = [c[0][0] for c in self.ws.send_key.call_args_list]
        self.assertEqual(keys, ['Quote'])

    def test_refuses_untypeable_text_before_sending(self):
        with self.assertRaises(ValueError) as raised:
            self.ws.send_input('ok<Enter>ü')
        self.assertIn('position 9', str(raised.exception))
        self.ws.send_key.assert_not_called()
        self.ws._send_with_retry.assert_not_called()

    def test_special_keys_still_sent(self):
        self.ws.send_input('a<Enter>')
        keys = [c[0][0] for c in self.ws.send_key.call_args_list]
        self.assertEqual(keys, ['KeyA', 'Enter'])


if __name__ == '__main__':
    unittest.main()

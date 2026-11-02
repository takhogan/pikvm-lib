import string
from typing import Final, Mapping, List, Optional, Tuple

KEYMAP_PYAUTOGUI: Final[Mapping[str, str]] = {
    "\t": "Tab",
    "\n": "Enter",
    "\r": "Enter",
    "'": "Quote",
    ",": "Comma",
    "-": "Minus",
    ".": "Period",
    "/": "Slash",
    ";": "Semicolon",
    "=": "Equal",
    "[": "BracketLeft",
    "\\": "Backslash",
    "]": "BracketRight",
    "`": "Backquote",
    # "accept": ",
    "add": "NumpadAdd",
    "alt": "AltLeft",
    "altleft": "AltLeft",
    "altright": "AltRight",
    # "apps": ",
    "backspace": "Backspace",
    # "browserback": ",
    # "browserfavorites": ",
    # "browserforward": ",
    # "browserhome": ",
    # "browserrefresh": ",
    # "browsersearch": ",
    # "browserstop": ",
    "capslock": "CapsLock",
    # "clear": ",
    "convert": "Convert",
    "ctrl": "ControlLeft",
    "ctrlleft": "ControlLeft",
    "ctrlright": "ControlRight",
    "decimal": "NumpadDecimal",
    "del": "Delete",
    "delete": "Delete",
    "divide": "NumpadDivide",
    "down": "ArrowDown",
    "end": "End",
    "enter": "Enter",
    "esc": "Escape",
    "escape": "Escape",
    # "execute": ",
    "f1": "F1",
    "f10": "F10",
    "f11": "F11",
    "f12": "F12",
    "f13": "F13",
    "f14": "F14",
    "f15": "F15",
    "f16": "F16",
    "f17": "F17",
    "f18": "F18",
    "f19": "F19",
    "f2": "F2",
    "f20": "F20",
    "f21": "F21",
    "f22": "F22",
    "f23": "F23",
    "f24": "F24",
    "f3": "F3",
    "f4": "F4",
    "f5": "F5",
    "f6": "F6",
    "f7": "F7",
    "f8": "F8",
    "f9": "F9",
    # "final": ",
    # "fn": ",
    # "hanguel": ",
    # "hangul": ",
    # "hanja": ",
    # "help": ",
    "home": "Home",
    "insert": "Insert",
    # "junja": ",
    "kana": "KanaMode",
    # "kanji": ",
    # "launchapp1": ",
    # "launchapp2": ",
    # "launchmail": ",
    # "launchmediaselect": ",
    "left": "ArrowLeft",
    # "modechange": ",
    "multiply": "NumpadMultiply",
    # "nexttrack": ",
    "nonconvert": "NonConvert",
    "num0": "Numpad0",
    "num1": "Numpad1",
    "num2": "Numpad2",
    "num3": "Numpad3",
    "num4": "Numpad4",
    "num5": "Numpad5",
    "num6": "Numpad6",
    "num7": "Numpad7",
    "num8": "Numpad8",
    "num9": "Numpad9",
    "numlock": "NumLock",
    "pagedown": "PageDown",
    "pageup": "PageUp",
    "pause": "Pause",
    "pgdn": "PageDown",
    "pgup": "PageUp",
    # "playpause": ",
    # "prevtrack": ",
    "print": "PrintScreen",
    "printscreen": "PrintScreen",
    "prntscrn": "PrintScreen",
    "prtsc": "PrintScreen",
    "prtscr": "PrintScreen",
    "return": "Enter",
    "right": "ArrowRight",
    "scrolllock": "ScrollLock",
    # "select": ",
    # "separator": ",
    "shift": "ShiftLeft",
    "shiftleft": "ShiftLeft",
    "shiftright": "ShiftRight",
    # "sleep": ",
    "space": "Space",
    # "stop": ",
    "subtract": "NumpadSubtract",
    "tab": "Tab",
    "up": "ArrowUp",
    # "volumedown": ",
    # "volumemute": ",
    # "volumeup": ",
    "win": "MetaLeft",
    "winleft": "MetaLeft",
    "winright": "MetaRight",
    "yen": "IntlYen",
    "command": "MetaLeft",
    "option": "AltLeft",
    "optionleft": "AltLeft",
    "optionright": "AltRight"
}

KEYMAP_SHIFT: Final[Mapping[str, str]] = {
    "_":"Minus",
    "+":"Equal",
    "{":"BracketLeft",
    "}":"BracketRight",
    "|":"Backslash",
    ":":"Semicolon",
    "\"":"Quote",
    "~":"Backquote",
    "<":"Comma",
    ">":"Period",
    "?":"Slash",
    "!":"Digit1",
    "@":"Digit2",
    "#":"Digit3",
    "$":"Digit4",
    "%":"Digit5",
    "^":"Digit6",
    "&":"Digit7",
    "*":"Digit8",
    "(":"Digit9",
    ")":"Digit0"
}

KEYMAP_BASE: Final[Mapping[str, str]] = {
    "\n":"Enter",
    "\b":"Backspace",
    "\t":"Tab",
    "\\s":"Space",
    "-":"Minus",
    "=":"Equal",
    "[":"BracketLeft",
    "]":"BracketRight",
    "\\":"Backslash",
    ";":"Semicolon",
    "'":"Quote",
    "`":"Backquote",
    ",":"Comma",
    ".":"Period",
    "/":"Slash",
    "<Esc>":"Escape",
    "<Enter>":"Enter",
    "<CapsLock>":"CapsLock",
    "<F1>":"F1",
    "<F2>":"F2",
    "<F3>":"F3",
    "<F4>":"F4",
    "<F5>":"F5",
    "<F6>":"F6",
    "<F7>":"F7",
    "<F8>":"F8",
    "<F9>":"F9",
    "<F10>":"F10",
    "<F11>":"F11",
    "<F12>":"F12",
    "<PrintScreen>":"PrintScreen",
    "<Insert>":"Insert",
    "<Home>":"Home",
    "<PageUp>":"PageUp",
    "<Delete>":"Delete",
    "<End>":"End",
    "<PageDown>":"PageDown",
    "<ArrowRight>":"ArrowRight",
    "<ArrowLeft>":"ArrowLeft",
    "<ArrowDown>":"ArrowDown",
    "<ArrowUp>":"ArrowUp",
    "<ControlLeft>":"ControlLeft",
    "<ShiftLeft>":"ShiftLeft",
    "<AltLeft>":"AltLeft",
    "<MetaLeft>":"MetaLeft",
    "<ControlRight>":"ControlRight",
    "<ShiftRight>":"ShiftRight",
    "<AltRight>":"AltRight",
    "<MetaRight>":"MetaRight",
    "<Pause>":"Pause",
    "<Power>":"Power"
}


def _build_text_keymap():
    """Every character that typing text can reproduce exactly, as
    (key code, whether Shift is held), on the US layout the key codes above
    assume. Anything else (a non-ASCII letter, a control character other than
    tab and the line breaks) has no key, so text holding it is refused rather
    than typed as something else."""
    keys = {}
    for char in string.ascii_lowercase:
        keys[char] = (f"Key{char.upper()}", False)
    for char in string.ascii_uppercase:
        keys[char] = (f"Key{char}", True)
    for char in string.digits:
        keys[char] = (f"Digit{char}", False)
    keys[" "] = ("Space", False)
    keys["\t"] = ("Tab", False)
    # A line break is one Enter whichever way it is written: "\r\n" is
    # collapsed to a single "\n" by text_to_keys, and a lone "\r" is Enter too.
    keys["\n"] = ("Enter", False)
    keys["\r"] = ("Enter", False)
    for char, code in KEYMAP_PYAUTOGUI.items():
        if len(char) == 1 and char.isprintable():
            keys[char] = (code, False)
    for char, code in KEYMAP_SHIFT.items():
        keys[char] = (code, True)
    return keys


# char -> (key code, shift)
TEXT_KEYMAP: Final[Mapping[str, Tuple[str, bool]]] = _build_text_keymap()

# The characters text may hold: printable ASCII, tab, "\n" and "\r".
TYPEABLE_CHARACTERS: Final[frozenset] = frozenset(TEXT_KEYMAP)


def describe_untypeable(char: str, position: Optional[int] = None) -> str:
    """The error for a character there is no key for."""
    where = f" at position {position}" if position is not None else ""
    return (f"cannot type {char!r} (U+{ord(char):04X}){where}: the PiKVM keyboard "
            f"has no key for it, so nothing was typed")


def find_untypeable(text: str) -> Optional[Tuple[int, str]]:
    """The position and character of the first character of text there is no
    key for, or None when all of it can be typed."""
    for position, char in enumerate(text):
        if char not in TYPEABLE_CHARACTERS:
            return position, char
    return None


def text_to_keys(text: str) -> List[str]:
    """The characters to press, one per key, to type text exactly: "\r\n" and
    a lone "\r" become one "\n" (Enter), since a CRLF is one line break in a
    Windows editor and typing both would make two. Raises ValueError naming
    the first character there is no key for, before anything is typed."""
    untypeable = find_untypeable(text)
    if untypeable is not None:
        position, char = untypeable
        raise ValueError(describe_untypeable(char, position))
    keys = []
    position = 0
    while position < len(text):
        char = text[position]
        if char == "\r":
            keys.append("\n")
            if position + 1 < len(text) and text[position + 1] == "\n":
                position += 1
        else:
            keys.append(char)
        position += 1
    return keys

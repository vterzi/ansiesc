"""ASCII control codes and ANSI escape sequences."""

__all__ = ("C0", "C1", "ANSIControl", "ANSIText", "ANSIColor")


class _Const:
    def __new__(cls, value, name):
        self = super().__new__(cls, value)
        self._value = value
        self._name = name
        return self

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return self._name


class _StrConst(_Const, str):
    pass


class _IntConst(_Const, int):
    pass


class _Consts:
    def __init__(self, func, items, doc=None):
        for key, value in items.items():
            setattr(self, key, func(key, value))
        self.__doc__ = doc

    def __repr__(self):
        return (
            "("
            + ", ".join(key for key in dir(self) if not key.startswith("_"))
            + ")"
        )


C0 = _Consts(
    lambda key, value: _StrConst(value[0], value[1]),
    {
        "NUL": ("\0", "Null"),
        "SOH": ("\x01", "Start of Heading"),
        "STX": ("\x02", "Start of Text"),
        "ETX": ("\x03", "End of Text"),
        "EOT": ("\x04", "End of Transmission"),
        "ENQ": ("\x05", "Enquiry"),
        "ACK": ("\x06", "Acknowledge"),
        "BEL": ("\a", "Bell"),
        "BS": ("\b", "Backspace"),
        "TAB": ("\t", "Horizontal Tab"),
        "LF": ("\n", "Line Feed"),
        "VT": ("\v", "Vertical Tab"),
        "FF": ("\f", "Form Feed"),
        "CR": ("\r", "Carriage Return"),
        "SO": ("\x0e", "Shift Out"),
        "SI": ("\x0f", "Shift In"),
        "DLE": ("\x10", "Data Link Escape"),
        "DC1": ("\x11", "Device Control 1"),
        "DC2": ("\x12", "Device Control 2"),
        "DC3": ("\x13", "Device Control 3"),
        "DC4": ("\x14", "Device Control 4"),
        "NAK": ("\x15", "Negative Acknowledge"),
        "SYN": ("\x16", "Synchronous Idle"),
        "ETB": ("\x17", "End of Transmission Block"),
        "CAN": ("\x18", "Cancel"),
        "EM": ("\x19", "End of Medium"),
        "SUB": ("\x1a", "Substitute"),
        "ESC": ("\x1b", "Escape"),
        "FS": ("\x1c", "File Separator"),
        "GS": ("\x1d", "Group Separator"),
        "RS": ("\x1e", "Record Separator"),
        "US": ("\x1f", "Unit Separator"),
        "SP": (" ", "Space"),
        "DEL": ("\x7f", "Delete"),
    },
    """
    Contains the active C0 control character set (the standard ASCII control
    codes).
    """,
)

C1 = _Consts(
    lambda key, value: _StrConst(C0.ESC + value[0], value[1]),
    {
        "PAD": ("@", "Padding Character"),
        "HOP": ("A", "High Octet Preset"),
        "BPH": ("B", "Break Permitted Here"),
        "NBH": ("C", "No Break Here"),
        "IND": ("D", "Index"),
        "NEL": ("E", "Next Line"),
        "SSA": ("F", "Start of Selected Area"),
        "ESA": ("G", "End of Selected Area"),
        "HTS": ("H", "Character Tabulation Set (Horizontal Tabulation Set)"),
        "HTJ": (
            "I",
            "Character Tabulation with Justification (Horizontal"
            " Tabulation with Justification)",
        ),
        "VTS": ("J", "Line Tabulation Set (Vertical Tabulation Set)"),
        "PLD": ("K", "Partial Line Forward (Partial Line Down)"),
        "PLU": ("L", "Partial Line Backward (Partial Line Up)"),
        "RI": ("M", "Reverse Line Feed (Reverse Index)"),
        "SS2": ("N", "Single-Shift 2"),
        "SS3": ("O", "Single-Shift 3"),
        "DCS": ("P", "Device Control String"),
        "PU1": ("Q", "Private Use 1"),
        "PU2": ("R", "Private Use 2"),
        "STS": ("S", "Set Transmit State"),
        "CCH": ("T", "Cancel Character"),
        "MW": ("U", "Message Waiting"),
        "SPA": ("V", "Start of Protected Area"),
        "EPA": ("W", "End of Protected Area"),
        "SOS": ("X", "Start of String"),
        "SGC": ("Y", "Single Graphic Character Introducer"),
        "SGCI": ("Y", "Single Graphic Character Introducer"),
        "SCI": ("Z", "Single Character Introducer"),
        "CSI": ("[", "Control Sequence Introducer"),
        "ST": ("\\", "String Terminator"),
        "OSC": ("]", "Operating System Command"),
        "PM": ("^", "Privacy Message"),
        "APC": ("_", "Application Program Command"),
    },
    """
    Contains the active C1 control character set (the standard ASCII control
    codes).
    """,
)

ANSIControl = _Consts(
    lambda key, value: _StrConst(C1.CSI + value[0], value[1]),
    {
        "CUU": ("{}A", "Cursor Up"),
        "CUD": ("{}B", "Cursor Down"),
        "CUF": ("{}C", "Cursor Forward"),
        "CUB": ("{}D", "Cursor Back"),
        "HVP": ("{};{}f", "Horizontal and Vertical Position"),
        "CUP": ("{};{}H", "Cursor Position"),
        "ED": ("{}J", "Erase Display"),
        "EL": ("{}K", "Erase in Line"),
        "SGR": ("{}m", "Select Graphic Rendition"),
        "DSR": ("6n", "Device Status Report"),
        "SCP": ("s", "Save Cursor Position"),
        "RCP": ("u", "Restore Cursor Position"),
    },
    """
    Contains the standard (DOS ANSI.SYS) ANSI escape sequences with blanks `{}`
    for parameters to be filled with `format`.
    """,
)

ANSIText = _Consts(
    lambda key, value: _IntConst(value, key),
    {
        "RESET": 0,
        "BOLD": 1,
        "HIGH_INTENSITY": 1,
        "FAINT": 2,
        "LOW_INTENSITY": 2,
        "CURSIVE": 3,
        "UNDERLINE": 4,
        "BLINK": 5,
        "FAST_BLINK": 6,
        "INVERT": 7,
        "HIDE": 8,
        "STRIKETHROUGH": 9,
        "DEFAULT_FONT": 10,
        "BLACKLETTER": 20,
        "NOT_BOLD": 21,
        "DOUBLE_UNDERLINE": 21,
        "NOT_FAINT": 22,
        "NORMAL_INTENSITY": 22,
        "NOT_CURSIVE": 23,
        "NOT_UNDERLINE": 24,
        "NOT_BLINK": 25,
        "PROPORTIONAL_SPACE": 26,
        "NOT_INVERT": 27,
        "NOT_HIDE": 28,
        "NOT_STRIKETHROUGH": 29,
        "NOT_PROPORTIONAL_SPACE": 50,
        "FRAME": 51,
        "ENCIRCLE": 52,
        "OVERLINE": 53,
        "NOT_FRAME": 54,
        "NOT_ENCIRCLE": 54,
        "NOT_OVERLINE": 55,
        "RIGHT_LINE": 60,
        "DOUBLE_RIGHT_LINE": 61,
        "LEFT_LINE": 62,
        "DOUBLE_LEFT_LINE": 63,
        "STRESS_MARK": 64,
        "NOT_IDEOGRAM": 65,
        "SUPERSCRIPT": 73,
        "SUBSCRIPT": 74,
        "NOT_SCRIPT": 75,
    },
    """
    Contains parameter values for changing text attributes by selecting graphic
    rendition with ANSI escape sequences.

    `ANSIControl.SGR.format(';'.join(str(attrib) for attrib in attribs))` with
    an array of selected attributes `attribs` returns the escape sequence to
    apply selected changes.
    """,
)

ANSIColor = _Consts(
    lambda key, value: _IntConst(value, key),
    {
        "BLACK": 0,
        "RED": 1,
        "GREEN": 2,
        "YELLOW": 3,
        "BLUE": 4,
        "MAGENTA": 5,
        "CYAN": 6,
        "WHITE": 7,
        "SET": 8,
        "COLOR8": 5,
        "COLOR24": 2,
        "DEFAULT": 9,
        "FORE": 30,
        "BACK": 40,
        "UNDERLINE": 50,
        "BRIGHT": 60,
    },
    """
    Contains parameter values for changing color by selecting graphic rendition
    with ANSI escape sequences.

    `ANSIControl.SGR.format(';'.join(str(attrib) for attrib in attribs))` with
    an array of selected attributes `attribs` returns the escape sequence to
    apply selected changes.

    Adding `ANSIColor.FORE`, `ANSIColor.BACK`, or `ANSIColor.UNDERLINE` to the
    selected color value targets the color of foreground, background, or
    underline, respectively.  Adding `ANSIColor.BRIGHT` selects brighter
    colors.

    `(ANSIColor.SET, ANSIColor.COLOR8, value)` with a non-negative integer
    `value` less than 256 are attributes to select an 8-bit color.

    `(ANSIColor.SET, ANSIColor.COLOR24, r, g, b)` with non-negative integers
    `r`, `g`, and `b` less than 256 each are attributes to select a 24-bit
    color.
    """,
)

"""Function for formatting strings with ANSI escape sequences."""

__all__ = ('TEXT_ATTRIBS', 'BASIC_COLORS', 'EXTENDED_COLORS', 'ansifmt')

from functools import reduce
from string import hexdigits
from typing import Union, Sequence, Optional

from .codes import ANSIControl, ANSIText, ANSIColor

TEXT_ATTRIBS = {
    '*': ANSIText.BOLD,
    '.': ANSIText.FAINT,
    '/': ANSIText.CURSIVE,
    '_': ANSIText.UNDERLINE,
    '%': ANSIText.BLINK,
    '!': ANSIText.INVERT,
    '?': ANSIText.HIDE,
    '-': ANSIText.STRIKETHROUGH,
    '&': ANSIText.BLACKLETTER,
    '=': ANSIText.DOUBLE_UNDERLINE,
    '^': ANSIText.OVERLINE,
}

BASIC_COLORS = {
    'k': ANSIColor.BLACK,
    'r': ANSIColor.RED,
    'g': ANSIColor.GREEN,
    'y': ANSIColor.YELLOW,
    'b': ANSIColor.BLUE,
    'm': ANSIColor.MAGENTA,
    'c': ANSIColor.CYAN,
    'w': ANSIColor.WHITE,
}

EXTENDED_COLORS = {
    'aliceblue': (240, 248, 255),
    'antiquewhite': (250, 235, 215),
    'aqua': (0, 255, 255),
    'aquamarine': (127, 255, 212),
    'azure': (240, 255, 255),
    'beige': (245, 245, 220),
    'bisque': (255, 228, 196),
    'black': (0, 0, 0),
    'blanchedalmond': (255, 235, 205),
    'blue': (0, 0, 255),
    'blueviolet': (138, 43, 226),
    'brown': (165, 42, 42),
    'burlywood': (222, 184, 135),
    'cadetblue': (95, 158, 160),
    'chartreuse': (127, 255, 0),
    'chocolate': (210, 105, 30),
    'coral': (255, 127, 80),
    'cornflowerblue': (100, 149, 237),
    'cornsilk': (255, 248, 220),
    'crimson': (220, 20, 60),
    'cyan': (0, 255, 255),
    'darkblue': (0, 0, 139),
    'darkcyan': (0, 139, 139),
    'darkgoldenrod': (184, 134, 11),
    'darkgray': (169, 169, 169),
    'darkgreen': (0, 100, 0),
    'darkgrey': (169, 169, 169),
    'darkkhaki': (189, 183, 107),
    'darkmagenta': (139, 0, 139),
    'darkolivegreen': (85, 107, 47),
    'darkorange': (255, 140, 0),
    'darkorchid': (153, 50, 204),
    'darkred': (139, 0, 0),
    'darksalmon': (233, 150, 122),
    'darkseagreen': (143, 188, 143),
    'darkslateblue': (72, 61, 139),
    'darkslategray': (47, 79, 79),
    'darkslategrey': (47, 79, 79),
    'darkturquoise': (0, 206, 209),
    'darkviolet': (148, 0, 211),
    'deeppink': (255, 20, 147),
    'deepskyblue': (0, 191, 255),
    'dimgray': (105, 105, 105),
    'dimgrey': (105, 105, 105),
    'dodgerblue': (30, 144, 255),
    'firebrick': (178, 34, 34),
    'floralwhite': (255, 250, 240),
    'forestgreen': (34, 139, 34),
    'fuchsia': (255, 0, 255),
    'gainsboro': (220, 220, 220),
    'ghostwhite': (248, 248, 255),
    'gold': (255, 215, 0),
    'goldenrod': (218, 165, 32),
    'gray': (128, 128, 128),
    'green': (0, 128, 0),
    'greenyellow': (173, 255, 47),
    'grey': (128, 128, 128),
    'honeydew': (240, 255, 240),
    'hotpink': (255, 105, 180),
    'indianred': (205, 92, 92),
    'indigo': (75, 0, 130),
    'ivory': (255, 255, 240),
    'khaki': (240, 230, 140),
    'lavender': (230, 230, 250),
    'lavenderblush': (255, 240, 245),
    'lawngreen': (124, 252, 0),
    'lemonchiffon': (255, 250, 205),
    'lightblue': (173, 216, 230),
    'lightcoral': (240, 128, 128),
    'lightcyan': (224, 255, 255),
    'lightgoldenrodyellow': (250, 250, 210),
    'lightgray': (211, 211, 211),
    'lightgreen': (144, 238, 144),
    'lightgrey': (211, 211, 211),
    'lightpink': (255, 182, 193),
    'lightsalmon': (255, 160, 122),
    'lightseagreen': (32, 178, 170),
    'lightskyblue': (135, 206, 250),
    'lightslategray': (119, 136, 153),
    'lightslategrey': (119, 136, 153),
    'lightsteelblue': (176, 196, 222),
    'lightyellow': (255, 255, 224),
    'lime': (0, 255, 0),
    'limegreen': (50, 205, 50),
    'linen': (250, 240, 230),
    'magenta': (255, 0, 255),
    'maroon': (128, 0, 0),
    'mediumaquamarine': (102, 205, 170),
    'mediumblue': (0, 0, 205),
    'mediumorchid': (186, 85, 211),
    'mediumpurple': (147, 112, 219),
    'mediumseagreen': (60, 179, 113),
    'mediumslateblue': (123, 104, 238),
    'mediumspringgreen': (0, 250, 154),
    'mediumturquoise': (72, 209, 204),
    'mediumvioletred': (199, 21, 133),
    'midnightblue': (25, 25, 112),
    'mintcream': (245, 255, 250),
    'mistyrose': (255, 228, 225),
    'moccasin': (255, 228, 181),
    'navajowhite': (255, 222, 173),
    'navy': (0, 0, 128),
    'oldlace': (253, 245, 230),
    'olive': (128, 128, 0),
    'olivedrab': (107, 142, 35),
    'orange': (255, 165, 0),
    'orangered': (255, 69, 0),
    'orchid': (218, 112, 214),
    'palegoldenrod': (238, 232, 170),
    'palegreen': (152, 251, 152),
    'paleturquoise': (175, 238, 238),
    'palevioletred': (219, 112, 147),
    'papayawhip': (255, 239, 213),
    'peachpuff': (255, 218, 185),
    'peru': (205, 133, 63),
    'pink': (255, 192, 203),
    'plum': (221, 160, 221),
    'powderblue': (176, 224, 230),
    'purple': (128, 0, 128),
    'red': (255, 0, 0),
    'rosybrown': (188, 143, 143),
    'royalblue': (65, 105, 225),
    'saddlebrown': (139, 69, 19),
    'salmon': (250, 128, 114),
    'sandybrown': (244, 164, 96),
    'seagreen': (46, 139, 87),
    'seashell': (255, 245, 238),
    'sienna': (160, 82, 45),
    'silver': (192, 192, 192),
    'skyblue': (135, 206, 235),
    'slateblue': (106, 90, 205),
    'slategray': (112, 128, 144),
    'slategrey': (112, 128, 144),
    'snow': (255, 250, 250),
    'springgreen': (0, 255, 127),
    'steelblue': (70, 130, 180),
    'tan': (210, 180, 140),
    'teal': (0, 128, 128),
    'thistle': (216, 191, 216),
    'tomato': (255, 99, 71),
    'turquoise': (64, 224, 208),
    'violet': (238, 130, 238),
    'wheat': (245, 222, 179),
    'white': (255, 255, 255),
    'whitesmoke': (245, 245, 245),
    'yellow': (255, 255, 0),
    'yellowgreen': (154, 205, 50),
}

_COLOR8 = 1 << 8
_COLOR24 = 1 << 24
_Color = Optional[Union[int, float, str, Sequence[int], Sequence[float]]]


def ansifmt(string: str,
            attribs: str = '',
            fore: _Color = None,
            back: _Color = None,
            underline: _Color = None,
            extra_attribs: Optional[Sequence[int]] = None) -> str:
    """
    Format a string by adding ANSI escape codes that change its graphics mode
    to it.

    Accepted colors are a character from `BASIC_COLORS` (uppercase for a bright
    color), a string from `EXTENDED_COLORS`, a non-negative hexadecimal integer
    less than 2^24 (24-bit color), a floating point number (gray color), an
    array of one decimal integer (8-bit color), or an array of three decimal
    integers or floating point numbers (24-bit color, RGB).  All decimal
    integers should be non-negative and less than 2^8, and all floating point
    numbers should be non-negative and not greater than 1.

    :param string: a string to format
    :param attribs: string of characters contained in `TEXT_ATTRIBS`
    :param fore: the foreground color
    :param back: the background color
    :param underline: the underline color
    :param extra_attribs: additional attributes
    :return: `string` surrounded by the selected ANSI escape codes
    :raise ValueError:
    """
    def check_int(arg, max_arg):
        return isinstance(arg, int) and 0 <= arg < max_arg

    def check_float(arg):
        return isinstance(arg, float) and 0 <= arg <= 1

    def decompose_color(arg):
        arr = []
        for _ in range(3):
            arr.insert(0, arg % _COLOR8)
            arg >>= 8
        return arr

    def add_color8(offset, arg):
        fmt.append(offset + ANSIColor.SET)
        fmt.append(ANSIColor.COLOR8)
        fmt.append(arg)

    def add_color24(offset, arg):
        fmt.append(offset + ANSIColor.SET)
        fmt.append(ANSIColor.COLOR24)
        fmt.append(arg[0])
        fmt.append(arg[1])
        fmt.append(arg[2])

    fmt = []
    for c in attribs:
        if c in TEXT_ATTRIBS:
            if TEXT_ATTRIBS[c] not in fmt:
                fmt.append(TEXT_ATTRIBS[c])
        else:
            raise ValueError(f"unexpected character in text attributes: '{c}'")
    for color, target, name in zip(
                (fore, back, underline),
                (ANSIColor.FORE, ANSIColor.BACK, ANSIColor.UNDERLINE),
                ('foreground', 'background', 'underline')
            ):
        if color:
            if isinstance(color, str):
                if color.lower() in BASIC_COLORS:
                    if color.isupper():
                        target += ANSIColor.BRIGHT
                    fmt.append(target + BASIC_COLORS[color.lower()])
                elif color.lower() in EXTENDED_COLORS:
                    add_color24(target, EXTENDED_COLORS[color.lower()])
                else:
                    color = color.replace('#', '0x')
                    if color.startswith('0x'):
                        color = color[2:]
                    if all(c in hexdigits for c in color):
                        len_color = len(color)
                        color = int(color, 16)
                        if len_color == 6:
                            add_color24(target, decompose_color(color))
                        elif len_color == 2:
                            add_color8(target, color)
                        else:
                            raise ValueError(f'unexpected length of the string'
                                             f' containing a hexadecimal'
                                             f' integer in the {name} color')
                    else:
                        raise ValueError(f'a color name or a string containing'
                                         f' a hexadecimal integer in the'
                                         f' {name} color expected')
            elif check_int(color, _COLOR24):
                add_color24(target, decompose_color(color))
            elif check_float(color):
                add_color24(target, 3 * [int(color * (_COLOR8 - 1))])
            elif hasattr(color, '__len__') and hasattr(color, '__getitem__'):
                len_color = len(color)
                if len_color == 3:
                    if reduce(lambda res, elem: res and check_int(elem,
                                                                  _COLOR8),
                              color, True):
                        add_color24(target, color)
                    elif reduce(lambda res, elem: res and check_float(elem),
                                color, True):
                        add_color24(target, [int(f * (_COLOR8 - 1))
                                             for f in color])
                    else:
                        raise ValueError(f'an array of 3 ints (0<=i<{_COLOR8})'
                                         f' or floats (0<=f<=1) in the {name}'
                                         f' color expected')
                elif len_color == 1 and check_int(color[0], _COLOR8):
                    add_color8(target, color[0])
                else:
                    raise ValueError(f'an array of 3 numbers or 1 int'
                                     f' (0<=i<{_COLOR8}) in the {name} color'
                                     f' expected')
            else:
                raise ValueError(f'unexpected value of the {name} color:'
                                 f' {color}')
    if extra_attribs is not None:
        fmt += extra_attribs
    return (ANSIControl.SGR.format(';'.join(str(f) for f in fmt)) + string
            + ANSIControl.SGR.format(''))

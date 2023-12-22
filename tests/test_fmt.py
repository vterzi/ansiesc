import random
import string
import unittest

from ansiesc import *


class TestFmt(unittest.TestCase):
    def test_Ansifmt(self):
        color8 = 2**8
        color24 = 2**24
        text = "lorem ipsum"
        attribs = "".join(
            set(random.choice(tuple(TEXT_ATTRIBS)) for _ in range(3))
        )
        fore, back, underline = [
            random.choice(tuple(BASIC_COLORS)) for _ in range(3)
        ]

        def fmt_string(colors):
            return (
                f'\x1b[{";".join(str(f) for f in [TEXT_ATTRIBS[attrib] for attrib in attribs] + colors)}m'
                f"{text}"
                f"\x1b[m"
            )

        def decompose_color(arg):
            arr = []
            for _ in range(3):
                arr.insert(0, arg % color8)
                arg >>= 8
            return arr

        self.assertEqual(
            fmt_string(
                [
                    30 + BASIC_COLORS[fore],
                    40 + BASIC_COLORS[back],
                    50 + BASIC_COLORS[underline],
                ]
            ),
            ansifmt(text, attribs, fore, back, underline),
        )

        self.assertEqual(
            fmt_string(
                [
                    90 + BASIC_COLORS[fore],
                    100 + BASIC_COLORS[back],
                    110 + BASIC_COLORS[underline],
                ]
            ),
            ansifmt(
                text, attribs, fore.upper(), back.upper(), underline.upper()
            ),
        )

        fore, back, underline = [
            random.choice(tuple(EXTENDED_COLORS)) for _ in range(3)
        ]
        self.assertEqual(
            fmt_string(
                [
                    38,
                    2,
                    *EXTENDED_COLORS[fore],
                    48,
                    2,
                    *EXTENDED_COLORS[back],
                    58,
                    2,
                    *EXTENDED_COLORS[underline],
                ]
            ),
            ansifmt(text, attribs, fore, back, underline),
        )

        fore, back, underline = [
            "".join(random.choice(string.hexdigits) for _ in range(6))
            for _ in range(3)
        ]

        def convert(color):
            return decompose_color(int(color, 16))

        self.assertEqual(
            fmt_string(
                [
                    38,
                    2,
                    *convert(fore),
                    48,
                    2,
                    *convert(back),
                    58,
                    2,
                    *convert(underline),
                ]
            ),
            ansifmt(text, attribs, fore, back, underline),
        )

        fore, back, underline = [
            "0x" + "".join(random.choice(string.hexdigits) for _ in range(6))
            for _ in range(3)
        ]

        def convert(color):
            return decompose_color(int(color, 16))

        self.assertEqual(
            fmt_string(
                [
                    38,
                    2,
                    *convert(fore),
                    48,
                    2,
                    *convert(back),
                    58,
                    2,
                    *convert(underline),
                ]
            ),
            ansifmt(text, attribs, fore, back, underline),
        )

        fore, back, underline = [
            "#" + "".join(random.choice(string.hexdigits) for _ in range(6))
            for _ in range(3)
        ]

        def convert(color):
            return decompose_color(int(color.replace("#", "0x"), 16))

        self.assertEqual(
            fmt_string(
                [
                    38,
                    2,
                    *convert(fore),
                    48,
                    2,
                    *convert(back),
                    58,
                    2,
                    *convert(underline),
                ]
            ),
            ansifmt(text, attribs, fore, back, underline),
        )

        fore, back, underline = [
            "".join(random.choice(string.hexdigits) for _ in range(2))
            for _ in range(3)
        ]

        def convert(color):
            return [int(color, 16)]

        self.assertEqual(
            fmt_string(
                [
                    38,
                    5,
                    *convert(fore),
                    48,
                    5,
                    *convert(back),
                    58,
                    5,
                    *convert(underline),
                ]
            ),
            ansifmt(text, attribs, fore, back, underline),
        )

        fore, back, underline = [random.randrange(color24) for _ in range(3)]
        convert = decompose_color
        self.assertEqual(
            fmt_string(
                [
                    38,
                    2,
                    *convert(fore),
                    48,
                    2,
                    *convert(back),
                    58,
                    2,
                    *convert(underline),
                ]
            ),
            ansifmt(text, attribs, fore, back, underline),
        )

        fore, back, underline = [random.random() for _ in range(3)]

        def convert(color):
            return 3 * [int(color * (color8 - 1))]

        self.assertEqual(
            fmt_string(
                [
                    38,
                    2,
                    *convert(fore),
                    48,
                    2,
                    *convert(back),
                    58,
                    2,
                    *convert(underline),
                ]
            ),
            ansifmt(text, attribs, fore, back, underline),
        )

        fore, back, underline = [
            [random.randrange(color8) for _ in range(3)] for _ in range(3)
        ]
        self.assertEqual(
            fmt_string([38, 2, *fore, 48, 2, *back, 58, 2, *underline]),
            ansifmt(text, attribs, fore, back, underline),
        )

        fore, back, underline = [
            [random.random() for _ in range(3)] for _ in range(3)
        ]

        def convert(color):
            return [int(f * (color8 - 1)) for f in color]

        self.assertEqual(
            fmt_string(
                [
                    38,
                    2,
                    *convert(fore),
                    48,
                    2,
                    *convert(back),
                    58,
                    2,
                    *convert(underline),
                ]
            ),
            ansifmt(text, attribs, fore, back, underline),
        )

        fore, back, underline = [
            [random.randrange(color8) for _ in range(1)] for _ in range(3)
        ]
        self.assertEqual(
            fmt_string([38, 5, *fore, 48, 5, *back, 58, 5, *underline]),
            ansifmt(text, attribs, fore, back, underline),
        )


if __name__ == "__main__":
    unittest.main()

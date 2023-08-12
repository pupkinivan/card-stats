from enum import Enum


class Colors(Enum):
    BLACK = "black"
    BLUE = "blue"
    GREEN = "green"
    RED = "red"
    WHITE = "white"
    NONLAND = "nonland"

    @classmethod
    def of(cls, value: str) -> "Colors":
        value_to_enum = {
            "black": cls.BLACK,
            "blue": cls.BLUE,
            "green": cls.GREEN,
            "red": cls.RED,
            "white": cls.WHITE,
            "nonland": cls.NONLAND,
        }

        try:
            return value_to_enum[value.lower()]
        except KeyError as error:
            raise ValueError("Not a valid color")

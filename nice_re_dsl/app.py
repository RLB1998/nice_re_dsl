from typing import Union


class Elem:
    class Char(str):
        REGEX_META_CHARS = {'.', '^', '$', '*', '+', '?', '{', '}', '[', ']', '(', ')', '|', '\\'}

        def __new__(cls, char: str):
            if char in cls.REGEX_META_CHARS:
                char = '\\' + char

            return super().__new__(cls, char)

    def __init__(self, chars: str):
        self._chars = ''.join((self.Char(char) for char in chars))

    def __str__(self):
        return self._chars

    def __add__(self, other: 'Elem'):
        return ProcessedElem(self._chars + other._chars)

    def __len__(self):
        return len(self._chars)

    def zero_or_once(self, elem: 'Union[Elem, str]'):
        return ProcessedElem(self._chars + str(Op.zero_or_once(elem)))

    def zero_or_more(self, elem: 'Union[Elem, str]'):
        return ProcessedElem(self._chars + str(Op.zero_or_more(elem)))

    def once_or_more(self, elem: 'Union[Elem, str]'):
        return ProcessedElem(self._chars + str(Op.once_or_more(elem)))

    def repeat_n(self, elem: 'Union[Elem, str]', n: int):
        return ProcessedElem(self._chars + str(Op.repeat_n(elem, n)))

    def repeat_at_least(self, elem: 'Union[Elem, str]', n: int):
        return ProcessedElem(self._chars + str(Op.repeat_at_least(elem, n)))

    def repeat_n2m(self, elem: 'Union[Elem, str]', n: int, m: int):
        return ProcessedElem(self._chars + str(Op.repeat_n2m(elem, n, m)))

    def then(self, elem: 'Union[Elem, str]'):
        return ProcessedElem(self._chars + str(Op.then(elem)))


class ProcessedElem(Elem):
    def __init__(self, chars: str):
        super().__init__("")
        self._chars = chars


class Group(Elem):
    def __init__(self, elems_tuple: tuple[Union[str, Elem], ...], is_catch, is_alternative):
        super().__init__("")
        result_list = []

        for elem in elems_tuple:
            if isinstance(elem, str):
                result_list.append(str(Elem(elem)))
            elif isinstance(elem, Elem):
                result_list.append(str(elem))

        if is_alternative:
            self._chars = "|".join(result_list)
        else:
            self._chars = "".join(result_list)

        if is_catch:
            self._chars = f"({self._chars})"
        else:
            self._chars = f"(?:{self._chars})"


class CharSetChar:
    REGEX_META_CHARS = {']', '\\', '^', '-'}

    def __init__(self, char: str):
        self._char = '\\' + char if char in self.REGEX_META_CHARS else char

    def __str__(self):
        return self._char

    def __add__(self, other: 'CharSetChar'):
        new_csc = CharSetChar("")
        new_csc._char = self._char + other._char
        return new_csc


class CharSet(Elem):

    def __init__(self, chars_list: list[Union[str, CharSetChar]], is_exclude=False):
        super().__init__("")
        self._chars = "[^" if is_exclude else "["

        for chars in chars_list:
            if isinstance(chars, CharSetChar):
                self._chars += str(chars)
            elif isinstance(chars, str):
                self._chars += "".join((str(CharSetChar(char)) for char in chars))
            else:
                pass

        self._chars += "]"


class CSRange(CharSetChar):

    def __init__(self, start_char: str, end_char: str):
        super().__init__("")

        if len(start_char) != 1 or len(end_char) != 1:
            pass
        if start_char > end_char:
            pass

        self._char = f"{start_char}-{end_char}"


class WordBoundary(Elem):
    def __init__(self, word: Union[str, Elem], left_on: bool = True, right_on: bool = True):
        super().__init__("")
        if isinstance(word, str):
            self._chars = ''.join((self.Char(char) for char in word))
        elif isinstance(word, Elem):
            self._chars = str(word)
        else:
            pass

        if left_on:
            self._chars = r"\b" + self._chars
        if right_on:
            self._chars += r"\b"


class NonWordBoundary(Elem):
    def __init__(self, word: str, left_on: bool = True, right_on: bool = True):
        super().__init__("")
        if isinstance(word, str):
            self._chars = ''.join((self.Char(char) for char in word))
        elif isinstance(word, Elem):
            self._chars = str(word)
        else:
            pass

        if left_on:
            self._chars = r"\B" + self._chars
        if right_on:
            self._chars += r"\B"


class Op:
    __REGEX_ESCAPE_COMMON = {
        r"\.", r"\^", r"\$", r"\*", r"\+", r"\?", r"\{", r"\}", r"\[", r"\]", r"\(", r"\)", r"\|", r"\\",
        r"\d", r"\D", r"\w", r"\W", r"\s", r"\S", r"\b", r"\B", r"\n", r"\r", r"\t",
    }

    @classmethod
    def __if_group(cls, elem: Elem):
        return (not isinstance(elem, Group) and not isinstance(elem, CharSet)
                and len(elem) != 1 and str(elem) not in Op.__REGEX_ESCAPE_COMMON)

    @staticmethod
    def __check_and_process_elem(elem: Union[Elem, str]):
        if isinstance(elem, str):
            return Elem(elem)
        elif isinstance(elem, Elem):
            return elem
        else:
            return None

    @classmethod
    def zero_or_once(cls, elem: Union[Elem, str]):
        elem = cls.__check_and_process_elem(elem)
        return ProcessedElem(f"(?:{elem})?") if cls.__if_group(elem) else ProcessedElem(f"{elem}?")

    @classmethod
    def once_or_more(cls, elem: Union[Elem, str]):
        elem = cls.__check_and_process_elem(elem)
        return ProcessedElem(f"(?:{elem})+") if cls.__if_group(elem) else ProcessedElem(f"{elem}+")

    @classmethod
    def zero_or_more(cls, elem: Union[Elem, str]):
        elem = cls.__check_and_process_elem(elem)
        return ProcessedElem(f"(?:{elem})*") if cls.__if_group(elem) else ProcessedElem(f"{elem}*")

    @classmethod
    def repeat_n(cls, elem: Union[Elem, str], n: int):
        elem = cls.__check_and_process_elem(elem)
        return ProcessedElem(f"(?:{elem}){{{n}}}") if cls.__if_group(elem) else ProcessedElem(f"{elem}{{{n}}}")

    @classmethod
    def repeat_at_least(cls, elem: Union[Elem, str], n: int):
        elem = cls.__check_and_process_elem(elem)
        return ProcessedElem(f"(?:{elem}){{{n},}}") if cls.__if_group(elem) else ProcessedElem(f"{elem}{{{n},}}")

    @classmethod
    def repeat_n2m(cls, elem: Union[Elem, str], n: int, m: int):
        elem = cls.__check_and_process_elem(elem)
        return ProcessedElem(f"(?:{elem}){{{n},{m}}}") if cls.__if_group(elem) else ProcessedElem(f"{elem}{{{n},{m}}}")

    @classmethod
    def then(cls, elem: Union[Elem, str]):
        return cls.__check_and_process_elem(elem)


class Regexp:
    def __init__(self):
        self.__regexp = ""

    def start_with(self):
        self.__regexp = "^" + self.__regexp
        return self

    def end_with(self):
        self.__regexp += "$"
        return self.__regexp

    def ignore_case_from_here(self):
        self.__regexp += "(?i)"
        return self

    def notice_case_from_here(self):
        self.__regexp += "(?-i)"
        return self

    def zero_or_once(self, elem: 'Union[Elem, str]'):
        self.__regexp += str(Op.zero_or_once(elem))
        return self

    def once_or_more(self, elem: 'Union[Elem, str]'):
        self.__regexp += str(Op.once_or_more(elem))
        return self

    def zero_or_more(self, elem: 'Union[Elem, str]'):
        self.__regexp += str(Op.zero_or_more(elem))
        return self

    def repeat_n(self, elem: 'Union[Elem, str]', n: int):
        self.__regexp += str(Op.repeat_n(elem, n))
        return self

    def repeat_at_least(self, elem: 'Union[Elem, str]', n: int):
        self.__regexp += str(Op.repeat_at_least(elem, n))
        return self

    def repeat_n2m(self, elem: 'Union[Elem, str]', n: int, m: int):
        self.__regexp += str(Op.repeat_n2m(elem, n, m))
        return self

    def then(self, elem: 'Union[Elem, str]'):
        self.__regexp += str(Op.then(elem))
        return self

    def done(self):
        return self.__regexp

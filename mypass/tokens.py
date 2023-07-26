import abc
import re
import copy
from typing import AnyStr


class Token(abc.ABC):
    pattern = None

    __slots__ = 'value', 'line_no', 'start', 'end'

    def __init__(self, value: AnyStr = None, start: int = None, end: int = None, line_no: int = None):
        self.value = value
        self.start = start
        self.end = end
        self.line_no = line_no

    def type_aware_value(self, remove_quotes=True):
        if self.value.lower() == 'true':
            return True
        elif self.value.lower() == 'false':
            return False
        try:
            return int(self.value)
        except ValueError:
            try:
                return float(self.value)
            except ValueError:
                if remove_quotes:
                    if ((self.value.startswith("'") and self.value.endswith("'"))
                            or (self.value.startswith('"') and self.value.endswith('"'))):
                        return self.value[1:-1]

                return self.value

    def __eq__(self, other):
        return isinstance(other, Token) \
            and other.name == self.name \
            and other.span() == self.span() \
            and other.value == self.value

    def copy(self):
        """
        Returns a shallow copy, by using copy function from copy module on self
        """
        new = copy.copy(self)
        return new

    def span(self):
        return self.start, self.end

    @property
    def name(self):
        return type(self).__name__

    def __repr__(self):
        return f"Token(class={self.name!r}, pattern=r'{self.pattern.pattern}', span={self.span()!r}, value={self.value!r})"


class Insert(Token):
    pattern = re.compile(r'\bINSERT\s+INTO\b|\bINSERT\b', re.I)


class Delete(Token):
    pattern = re.compile(r'\bDELETE\s+FROM\b|\bDELETE\b', re.I)


class Truncate(Token):
    pattern = re.compile(r'TRUNCATE\s+TABLE\b|\bTRUNCATE\b', re.I)


class OrderBy(Token):
    pattern = re.compile(r'\bORDER\s+BY\b', re.I)


class Ascending(Token):
    pattern = re.compile(r'\bASCENDING\b|\bASC\b|\b↑\b', re.I)


class Descending(Token):
    pattern = re.compile(r'\bDESCENDING\b|\bDESC\b|\b↓\b', re.I)


class Select(Token):
    pattern = re.compile(r'\bSELECT\b', re.I)


class From(Token):
    pattern = re.compile(r'\bFROM\b', re.I)


class Values(Token):
    pattern = re.compile(r'\bVALUES\b', re.I)


class Update(Token):
    pattern = re.compile(r'\bUPDATE\b', re.I)


class Set(Token):
    pattern = re.compile(r'\bSET\b', re.I)


class Where(Token):
    pattern = re.compile(r'\bWHERE\b', re.I)


class And(Token):
    pattern = re.compile(r'\bAND\b|\b&\b', re.I)


class Or(Token):
    pattern = re.compile(r'\bOR\b|\b\|\b', re.I)


class NotEquals(Token):
    pattern = re.compile(r'!=|<>')


class GreaterEquals(Token):
    pattern = re.compile(r'>=')


class LessEquals(Token):
    pattern = re.compile(r'<=')


class Greater(Token):
    pattern = re.compile(r'>')


class Less(Token):
    pattern = re.compile(r'<')


class Times(Token):
    pattern = re.compile(r'\*')


class Divide(Token):
    pattern = re.compile(r'/')


class Plus(Token):
    pattern = re.compile(r'\+')


class Minus(Token):
    pattern = re.compile(r'-')


class Backslash(Token):
    pattern = re.compile(r'\\')


class Dot(Token):
    pattern = re.compile(r'\.')


class Caret(Token):
    pattern = re.compile(r'\^')


class Dollar(Token):
    pattern = re.compile(r'\$')


class Comma(Token):
    pattern = re.compile(r',')


class Equals(Token):
    pattern = re.compile(r'=')


class Hashtag(Token):
    pattern = re.compile(r'#')


class NewLine(Token):
    pattern = re.compile(r'\n')


class Semicolon(Token):
    pattern = re.compile(r';')


class ExclamationMark(Token):
    pattern = re.compile(r'!')


class QuestionMark(Token):
    pattern = re.compile(r'\?')


class Percentage(Token):
    pattern = re.compile(r'%')


class LeftBracket(Token):
    pattern = re.compile(r'\[')


class RightBracket(Token):
    pattern = re.compile(r']')


class LeftParenthesis(Token):
    pattern = re.compile(r'\(')


class RightParenthesis(Token):
    pattern = re.compile(r'\)')


class LeftCurlyBracket(Token):
    pattern = re.compile(r'\{')


class RightCurlyBracket(Token):
    pattern = re.compile(r'}')


class Identifier(Token):
    pattern = re.compile(r'(?<![\'"])\b(?:\d*[A-Za-z_]+\d*|[A-Za-z_]\w*)\b(?![\'"])', re.I)


class Literal(Token):
    pattern = re.compile(r'\d*\.\d+|\d+\.\d*|\d+|"[^"]*"|\'[^\']*\'|True|False', re.I)


class Unknown(Token):
    pattern = re.compile(r'[^\t ]+')


sql_tokens = (
    Insert, Delete, Truncate, OrderBy, Ascending, Descending,
    Select, From, Values, Update, Set,
    Where, And, Or,
    NotEquals, GreaterEquals, LessEquals, Greater, Less, Equals,
    Times, Divide, Plus, Minus,
    Backslash, Dot, Caret, Dollar, Comma, Hashtag, Semicolon, ExclamationMark, QuestionMark, Percentage,
    LeftBracket, RightBracket, LeftParenthesis, RightParenthesis, LeftCurlyBracket, RightCurlyBracket,
    Identifier, Literal, Unknown,
)

# -*- encoding: utf8 -*-
# ------------------------------------------------------------------------------
# core.py
# Created on 11/04/2022
#
# The MIT License
#
#
# Copyright 2022 Jorge A. Gomes
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ------------------------------------------------------------------------------

# region IMPORTS

import os

from minilang.utillities.jsom import JSOM
from minilang.utillities.code import Source, SourceLocation
from typing import Optional, Any, Callable, TypeVar, Union, Tuple, List

# endregion (imports)
# ---------------------------------------------------------
# region EXPORTS


__all__ = [
    'Token',
    'Lexer',
    'export_constants'
]


# endregion (exports)
# ---------------------------------------------------------
# region CONSTANTS & ENUMS

T = TypeVar('T')
F = Callable[[...], "Token"]

TEMPLATE = """# -*- encoding: utf8 -*-

# region EXPORTS

__all__ = [
{}
]

# endregion (exports)

# region CONSTANTS


{}

# endregion (constants)
"""

# endregion (constants)
# ---------------------------------------------------------
# region CLASSES


class Error:

    def __init__(self, message: str, *args, **kwargs):
        self.message: str = message
        self.args: Any = args
        self.kwargs: Any = kwargs


class UnexpectedCharError(Error):
    pass


class Token:

    def __init__(self, location: SourceLocation, kind: str, value_slice: slice, **kwargs):
        self._source: Source = location.source
        self._location: SourceLocation = location
        self._kind: str = kind
        self._slice: Union[str, slice] = value_slice
        self._subkind: str = kwargs.get('subkind', '')
        self._base: int = kwargs.get('base', 10)
        self._suffix: str = kwargs.get('suffix', '')

    def __str__(self) -> str:
        return f"[ {self._kind} {self._subkind} {self.value} {self._location} ]"

    @property
    def source(self):
        return self._source

    @property
    def location(self):
        return self._location

    @property
    def kind(self):
        return self._kind

    @property
    def subkind(self):
        return self._subkind

    @property
    def value(self):
        return self._source[self._slice]

    @property
    def base(self):
        return self._base

    @property
    def suffix(self):
        return self._suffix


class Lexer:

    def __init__(self, config: JSOM, source: Source, **kwargs):
        self._config: JSOM = config
        self._source: Source = source
        self._pos: SourceLocation = SourceLocation(source, slice(0, -1), -1, 1, 1)
        self._char: str = ''
        self._on_unexpected: Optional[Callable[[SourceLocation, str, Optional[str]], Any]] = kwargs.get('on_unexpected',
                                                                                                        on_unexpected)
        if kwargs.get('export', False):
            export_constants(config)

    @property
    def source(self) -> Source:
        return self._source

    def _kind_subkind(self, kind: str, subkind: Union[str, None]) -> Union[str, None]:
        delim = self._config.get('subkind_delimiter')
        if isinstance(delim, str) and subkind is not None and kind != subkind:
            return delim.join((kind, subkind))
        return kind

    def _advance(self):
        """Advances the lexer to the next character

        :return: None
        :raises RuntimeError: if character _index is out of bounds
        """
        self._pos.advance(self._char)
        if self._pos.index >= len(self._source.code):
            self._char = None
        else:
            self._char = self._source[self._pos.index]

    def _scan_string(self) -> Token:
        """Scans and returns a STRING type of token

        :return: The token
        """
        quote: str = self._char
        conf = self._config
        subkind: str = conf.string[quote].subkind
        start: SourceLocation = self._pos.copy()
        end: SourceLocation = start
        self._advance()

        while self._char is not None:
            if self._char == conf.string.escape.mark:
                self._advance()
                self._advance()
            elif self._char == quote:
                self._advance()
                end = self._pos.copy()
                break
            else:
                self._advance()

        return Token(start, conf.kinds.string, slice(start.index, end.index), subkind=subkind)

    def _scan_number(self) -> Tuple[Union[Token, None], Union[Error, None]]:
        """Scans and returns a NUMBER type of token

        :return: The token or an error
        """
        conf = self._config
        start = self._pos.copy()
        base = 10
        subkind = conf.number.subkind
        digits: str = '0123456789'
        has_decimal: bool = False
        has_other_base: bool = False
        idx: int = 0
        number: str = ''
        suffix: str = ''

        while self._char is not None:
            if idx == 0 and self._char == '0':
                idx += 1
                number += self._char
                self._advance()
                if self._char.lower() in conf.number.integer.base_chars.lower():
                    digits = conf.number.integer.base[self._char].digits
                    subkind = conf.number.integer.base[self._char].subkind
                    base = len(digits)
                    has_other_base = True
                    idx += 1
                    number += self._char
                    self._advance()
                    continue

            if self._char.lower() in digits.lower():
                idx += 1
                number += self._char
                self._advance()

            elif self._char == conf.number.separator:
                idx += 1
                self._advance()

            elif self._char == '.':
                if has_other_base or has_decimal:
                    return None, self._on_unexpected(self._pos.copy(), self._char)
                has_decimal = True
                subkind = "FLOAT"
                idx += 1
                number += self._char
                self._advance()

            elif self._char.isalpha() and not has_other_base:
                if has_other_base:
                    return None, self._on_unexpected(self._pos.copy(), self._char, "Not base 10")
                idx += 1
                suffix += self._char
                self._advance()

            elif self._char in conf.whitespace.chars:
                break

            elif self._char in conf.delimiter.chars:
                break

            elif self._char in conf.operator.chars:
                break

            else:
                return None, self._on_unexpected(self._pos.copy(), self._char)

        end = self._pos.index
        token = Token(start, conf.kinds.number, slice(start.index, end), base=base, suffix=suffix, subkind=subkind)
        return token, None

    def _scan_operator(self) -> Tuple[Union[Token, None], Union[Error, None]]:
        """Scans and returns a OPERATOR type of token

        :return: The token
        """
        conf = self._config
        start = self._pos.copy()
        operator: str = ''
        kind: str = conf.kinds.operator
        subkind: Union[str, None]

        while self._char is not None:
            if self._char in conf.operator.chars:

                operator += self._char
                self._advance()

                if len(operator) > conf.operator.max_length:
                    return None, self._on_unexpected(self._pos.copy(), self._char)

            else:
                break

        if operator == conf.document.line:
            end = self._scan_comment().index
            kind = conf.kinds.documentation
            subkind = conf.document.subkind
            include = conf.document.include

        elif operator == conf.document.block.begin:
            end = self._scan_comment(conf.document.block.end).index
            kind = conf.kinds.documentation
            subkind = conf.document.block.subkind
            include = conf.document.include

        elif operator == conf.comment.line:
            end = self._scan_comment().index
            kind = conf.kinds.comment
            subkind = conf.comment.subkind
            include = conf.comment.include

        elif operator == conf.comment.block.begin:
            end = self._scan_comment(conf.comment.block.end).index
            kind = conf.kinds.comment
            subkind = conf.comment.block.subkind
            include = conf.comment.include
        else:
            subkind = conf.tokens.get(operator, '')
            end = self._pos.index
            include = True

        token = Token(start, kind, slice(start.index, end), subkind=subkind)
        if not include:
            token = None
        return token, None

    def _scan_comment(self, end: Union[str, None] = None) -> SourceLocation:
        """Scans a COMMENT type of token

        :param end: An optional ending marker to match for block comments or None for _line comments
        :return: The position in the _source code where the comment ends
        """
        comment: str = ''
        while self._char is not None:
            if self._char == '\n' and end is None:
                break

            comment += self._char
            self._advance()

            if end is not None:
                if comment.endswith(end):
                    break

        return self._pos.copy()

    def _scan_word(self) -> Tuple[Union[Token, None], Union[Error, None]]:
        """Scans and returns a WORD type of token

        :return: The token returned after `fn` gets called or an error
        """
        conf = self._config
        start = self._pos.copy()
        word: str = ''
        subkind: str

        while self._char is not None:
            if not self._char.isalnum() or self._char == '_':
                break
            word += self._char
            self._advance()

            if len(word) > conf.word.max_length:
                return None, self._on_unexpected(self._pos.copy(), self._char, "Identifier is too long")

        kind = conf.kinds.word
        subkind = conf.word.subkind
        if word in conf.keyword.reserved:
            kind = conf.kinds.keyword
            subkind = conf.keyword.subkind
        else:
            for key_kind in conf.keyword.subkinds:
                if key_kind in conf.keyword and word in conf.keyword[key_kind]:
                    kind = conf.kinds.keyword
                    subkind = key_kind

        token = Token(start, kind, slice(start.index, self._pos.index), subkind=subkind.upper())
        return token, None

    def gen_tokens(self) -> Tuple[List[Token], Optional[Error]]:
        """Scans the _source code and returns a list of tokens

        :return: The list of tokens or an error
        """
        tokens: List[Token] = []
        token: Token
        conf = self._config

        while self._char is not None:
            if self._char in conf.whitespace.chars:
                start = self._pos.copy()
                while self._char is not None and self._char in conf.whitespace.chars:
                    self._advance()
                if conf.whitespace.include:
                    token = Token(start, conf.kinds.whitespace, slice(start.index, self._pos.index))
                    tokens.append(token)
                continue

            if self._char in conf.string.delimiters:
                tokens.append(self._scan_string())

            elif self._char in "0123456789":
                token, error = self._scan_number()
                if error:
                    return [], error
                tokens.append(token)

            elif self._char in conf.delimiter.chars:
                kind = conf.kinds.delimiter
                subkind = conf.tokens.get(self._char, '')
                token = Token(self._pos.copy(), kind, slice(self._pos.index, self._pos.index + 1), subkind=subkind)
                tokens.append(token)
                self._advance()

            elif self._char in conf.operator.chars:
                token, error = self._scan_operator()
                if error:
                    return [], error
                if token:
                    tokens.append(token)

            elif self._char.isalpha():
                token, error = self._scan_word()
                if error:
                    return [], error
                tokens.append(token)

            else:
                error = on_unexpected(self._pos.copy(), self._char)
                return [], error

        token = Token(self._pos.copy(), conf.kinds.eof, slice(-1, -1))
        tokens.append(token)
        return tokens, None

# endregion (classes)
# ---------------------------------------------------------
# region FUNCTIONS


def export_constants(conf: JSOM):
    path = os.path.split(__file__)[0]
    src_file: str = os.path.join(path, 'tokens.py')
    exports: list[str] = []
    consts: list[str] = []

    for k, v in conf.kinds.items():
        exports.append(f"    'TK_{k.upper()}',")
        consts.append(f"TK_{k.upper()} = '{v}'")

    for k, v in conf.tokens.items():
        exports.append(f"    '{v}',")
        consts.append(f"{v.upper()} = '{k}'")

    for k in conf.string.delimiters:
        v = conf.string[k].subkind
        exports.append(f"    'SK_{v.upper()}',")
        consts.append(f"SK_{v.upper()} = '{v.upper()}'")

    exports.append(f"    'SK_{conf.keyword.subkind.upper()}',")
    consts.append(f"SK_{conf.keyword.subkind.upper()} = '{conf.keyword.subkind.upper()}'")
    for v in conf.keyword[conf.keyword.subkind.lower()]:
        exports.append(f"    'KW_{v.upper()}',")
        consts.append(f"KW_{v.upper()} = '{v}'")

    for k in conf.keyword.subkinds:
        exports.append(f"    'SK_{k.upper()}',")
        consts.append(f"SK_{k.upper()} = '{k.upper()}'")
        for v in conf.keyword[k]:
            exports.append(f"    'KW_{v.upper()}',")
            consts.append(f"KW_{v.upper()} = '{v}'")

    exports.append(f"    'SK_{conf.word.subkind.upper()}',")
    consts.append(f"SK_{conf.word.subkind.upper()} = '{conf.word.subkind.upper()}'")

    exports.append(f"    'SK_{conf.number.subkind.upper()}',")
    consts.append(f"SK_{conf.number.subkind.upper()} = '{conf.number.subkind.upper()}'")

    exports.append(f"    'SK_{conf.number.float.subkind.upper()}',")
    consts.append(f"SK_{conf.number.float.subkind.upper()} = '{conf.number.float.subkind.upper()}'")

    code = TEMPLATE.format('\n'.join(exports), '\n'.join(consts))

    with open(src_file, 'w', encoding='utf8') as source:
        source.write(code)


def on_unexpected(location: SourceLocation, char: str, message: str = '') -> UnexpectedCharError:
    msg = f"\n\t{message}" if message else ''
    return UnexpectedCharError(f"UnexpectedCharError: '{char}' at {location}{msg}")

# endregion (functions)

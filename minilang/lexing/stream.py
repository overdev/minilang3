# -*- encoding: utf8 -*-
# ------------------------------------------------------------------------------
# stream.py
# Created on 12/04/2022
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

import sys

from typing import Union, List, Callable, Any, Sized

from minilang.utillities.code import Source, SourceLocation
from minilang.lexing.core import Token, Lexer
from minilang.utillities.jsom import JSOM

# endregion (imports)
# ---------------------------------------------------------
# region EXPORTS


__all__ = [
    'TokenStream',
]


# endregion (exports)
# ---------------------------------------------------------
# region CLASSES


class TokenStream(Sized):

    __slots__ = '_tokens', '_source', '_idx', '_on_unexpected', '_on_end_of_tokens', '_kind_delimiter'

    def __init__(self, source: Source, tokens: List[Token], **kwargs):
        self._tokens: List[Token] = tokens
        self._source: Source = source
        self._idx: int = 0
        self._on_unexpected: Union[Callable[[Any, ...], None], None] = kwargs.get('on_unexpected')
        self._on_end_of_tokens: Union[Callable[[Source], Any], None] = kwargs.get('on_end_of_tokens')
        self._kind_delimiter: Union[str, None] = kwargs.get('kind_delimiter')

    def __len__(self) -> int:
        return self._tokens.__len__()

    @property
    def eot(self) -> bool:
        return self._idx >= self.__len__()

    @property
    def token(self) -> Token:
        if 0 <= self._idx < self.__len__():
            return self._tokens[self._idx]

        elif self._on_end_of_tokens:
            return self._on_end_of_tokens(self._source)

        else:
            print("TokenStreamError: Unexpected end of tokens", file=sys.stderr)
            sys.exit(1)

    @property
    def location(self) -> SourceLocation:
        return self.token.location

    @property
    def value(self) -> str:
        return self.token.value

    @property
    def source(self) -> Source:
        return self._source

    def advance(self) -> bool:
        self._idx += 1
        return True

    def get(self) -> token:
        token: Token = self.token
        self.advance()
        return token

    def is_token(self, *values: str) -> bool:
        return self._tokens[self._idx].value in values

    def match_token(self, *values: str) -> bool:
        if self.is_token(*values):
            return self.advance()
        return False

    def expect_token(self, *values):
        if self.is_token(*values):
            return self.advance()
        elif self._on_unexpected:
            self._on_unexpected(self._source, self._tokens[self._idx], values, 'value', self.token.value)
        else:
            print(f"TokenStreamError: Unexpected token value {self.token}", file=sys.stderr)
            sys.exit(1)

    def is_kind(self, *kinds: str) -> bool:
        if self._tokens[self._idx].kind in kinds:
            return True
        return False

    def match_kind(self, *kinds: str) -> bool:
        if self.is_kind(*kinds):
            return self.advance()
        return False

    def expect_kind(self, *kinds):
        if self.is_kind(*kinds):
            return self.advance()
        elif self._on_unexpected:
            self._on_unexpected(self._source, self._tokens[self._idx], kinds, 'kind', self.token.kind)
        else:
            print(f"TokenStreamError: Unexpected token kind {self.token}", file=sys.stderr)
            sys.exit(1)

    def is_subkind(self, *subkinds: str) -> bool:
        if self._tokens[self._idx].subkind in subkinds:
            return True
        return False

    def match_subkind(self, *subkinds: str) -> bool:
        if self.is_subkind(*subkinds):
            return self.advance()
        return False

    def expect_subkind(self, *subkinds):
        if self.is_subkind(*subkinds):
            return self.advance()
        elif self._on_unexpected:
            self._on_unexpected(self._source, self._tokens[self._idx], subkinds, 'subkind', self.token.subkind)
        else:
            print(f"TokenStreamError: Unexpected token subkind {self.token}", file=sys.stderr)
            sys.exit(1)


# endregion (classes)
# ---------------------------------------------------------
# region FUNCTIONS


def main() -> int:

    conf: JSOM = JSOM.parse_file('./lexconf.json')
    source: Source = Source.load('../../examples/testproj/src/main.txt')
    lex: Lexer = Lexer(conf, source, export=True)
    tokens, error = lex.gen_tokens()
    if error:
        return 1
    stream: TokenStream = TokenStream(source, tokens)

    while not stream.eot:
        print(stream.token)
        stream.advance()

    return 0


# endregion (functions)
# ---------------------------------------------------------
# region ENTRYPOINT


if __name__ == '__main__':
    sys.exit(main())

# endregion (entrypoint)

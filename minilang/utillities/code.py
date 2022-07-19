# -*- encoding: utf8 -*-
# ------------------------------------------------------------------------------
# code.py
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


from typing import Optional

# endregion (imports)
# ---------------------------------------------------------
# region EXPORTS


__all__ = [
    'Source',
    'SourceLocation',
]


# endregion (exports)
# ---------------------------------------------------------
# region CLASSES

class Source:

    # region CLASSMETHODS

    @classmethod
    def load(cls, filename: str) -> "Source":
        with open(filename, 'r', encoding='utf-8') as code:
            return cls(filename, code.read())

    # endregion

    # region SPECIAL

    def __init__(self, filename: str, code: Optional[str] = None):
        self.filename: str = filename
        self.code: Optional[str] = code

    def __len__(self) -> int:
        return self.code.__len__()

    def __getitem__(self, key) -> Optional[str]:
        if self.loaded:
            return self.code.__getitem__(key)
        return None

    def __str__(self) -> str:
        return f"[ '{self.filename}' | { 0 if not self.loaded else len(self.code)} characters ]"

    # endregion

    # region PROPERTIES

    @property
    def loaded(self) -> bool:
        return self.code is not None

    # endregion


class SourceLocation:

    # region SPECIAL

    __slots__ = '_index', '_line_slice', '_line', '_column', '_source'

    def __init__(self, source: Source, line_slice: slice, index: int = 0, line: int = 0, column: int = 0):
        self._index: int = index
        self._line_slice: slice = line_slice
        self._line: int = line
        self._column: int = column
        self._source: Source = source

    def __str__(self):
        return f"{self._line}:{self._column}"

    # endregion

    # region PROPERTIES

    @property
    def index(self):
        """Gets this location's character index in the source code string"""
        return self._index

    @property
    def line_slice(self):
        """Gets this location's line start and stop indices in the source code string"""
        return self._line_slice

    @property
    def line(self):
        """Gets this location line"""
        return self._line

    @property
    def column(self):
        """Gets this location column"""
        return self._column

    @property
    def source(self):
        """Gets the source code that contains this location"""
        return self._source

    @property
    def source_line(self) -> str:
        return self._source[self.line_slice]

    # endregion (properties)

    # region METHODS

    def advance(self, char: str) -> "SourceLocation":
        self._index += 1
        if char == '\n':
            stop = self.source.code.find(char, self._index + 1)
            self._line_slice = slice(self._index, stop)
            self._line += 1
            self._column = 1
        else:
            self._column += 1

        return self

    def copy(self) -> "SourceLocation":
        return SourceLocation(
            self._source, slice(self._line_slice.start, self._line_slice.stop), self._index, self._line, self._column)

    # endregion (methods)

# endregion (classes)

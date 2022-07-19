# -*- encoding: utf8 -*-
# ------------------------------------------------------------------------------
# jsom.py
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

import sys
import json

from typing import Any, Mapping, Union

# endregion (imports)
# ---------------------------------------------------------
# region EXPORTS


__all__ = [
    'JSOM',
]


# endregion (exports)
# ---------------------------------------------------------
# region CLASSES


class JSOM(dict):
    """JSOM (Java Script Object Mapping) class

    A JSOM object behaves to a certain point similarly to a JSON object. You can
    manipulate it as the built-in dict, but also access its keys as instance attributes.
    """

    @classmethod
    def stringify(cls, jsom: 'JSOM') -> str:
        return json.dumps(jsom)

    @classmethod
    def parse(cls, jsom_s: str) -> Union['JSOM', list]:
        return json.loads(jsom_s, object_pairs_hook=_hook)

    @classmethod
    def parse_file(cls, filename: str) -> Union['JSOM', list]:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file, object_pairs_hook=_hook)

    def __init__(self, *m: Mapping, **kwargs):
        super().__init__(**kwargs)
        for _m in m:
            super().update(_m)

    def __getattr__(self, key: Any) -> Any:
        if key in self:
            return dict.__getitem__(self, key)
        raise AttributeError(f"JSOM object has no attribute '{key}'")

    def __setattr__(self, key: Any, value: Any) -> None:
        dict.__setitem__(self, key, value)


# endregion (classes)
# ---------------------------------------------------------
# region FUNCTIONS


def _hook(pairs):
    obj: JSOM = JSOM()
    for (key, value) in pairs:
        obj[key] = value
    return obj

# endregion (functions)

"""
MIT License

Copyright (c) 2022 Ramon Hagenaars

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from typing import Any, Tuple

from nptyping.error import InvalidArgumentsError
from nptyping.ndarray import NDArray, NDArrayMeta
from nptyping.structure import Structure
from nptyping.typing_ import DType


class RecArrayMeta(NDArrayMeta, implementation="RecArray"):
    """
    Metaclass that is coupled to nptyping.RecArray. It takes most of its logic
    from NDArrayMeta.
    """

    def _get_item(cls, item: Any) -> Tuple[Any, ...]:
        cls._check_item(item)
        shape, dtype = cls._get_from_tuple(item)
        return shape, dtype

    def _get_dtype(cls, dtype_candidate: Any) -> DType:
        if not issubclass(dtype_candidate, Structure) and dtype_candidate is not Any:
            raise InvalidArgumentsError(
                f"Unexpected argument {dtype_candidate}. Expecting a Structure."
            )
        return dtype_candidate


class RecArray(NDArray, metaclass=RecArrayMeta):
    """
    An nptyping equivalent of numpy recarray.

    ## RecArrays can take a Shape and must take a Structure
    >>> from nptyping import Shape, Structure
    >>> RecArray[Shape["2, 2"], Structure["x: Float, y: Float"]]
    RecArray[Shape['2, 2'], Structure['[x, y]: Float']]

    ## Or Any
    >>> from typing import Any
    >>> RecArray[Shape["2, 2"], Any]
    RecArray[Shape['2, 2'], Any]
    """

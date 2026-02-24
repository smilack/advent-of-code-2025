from typing import Protocol, TypeVar, Literal
from collections.abc import Iterable, Sequence, Callable
from enum import Enum


def zip_sum(*args: Iterable[SummableT]) -> Iterable[SummableT] | Iterable[Literal[0]]:
    """Sum the columns of a matrix.

    zip_sum(a, b, ...) = [sum(a[0], b[0], ...), sum(a[1], b[1], ...), ...]
    """
    return map(sum, zip(*args))


def scale(
    k: MullableT1, xs: Iterable[MullableT2]
) -> Iterable[MullableT1] | Iterable[MullableT2]:
    """Scale a list of items by a given factor.

    scale(2, [1, 2, 3]) = [2, 4, 6]
    """
    return [k * x for x in xs]


class Matrix(Enum):
    TL = "𜸖"
    TR = "𜸘"
    BL = "𜸗"
    BR = "𜸙"
    V = "│"


T = TypeVar("T")


def print_matrix(
    matrix: Sequence[Sequence[T]],
    /,
    to_str: Callable[[T], str] | None = None,
    to_str_rc: Callable[[T, int, int], str] | None = None,
) -> None:
    """Print a matrix to stdout, padding and aligning columns, and optionally transforming the value with a custom string function.

    print_matrix([[1, 2], [3, 4]]) →
        𜸖 1 2 𜸘
        𜸗 3 4 𜸙

    print_matrix([[1, 2, 3, 4]]) →
        [ 1 2 3 4 ]

    print_matrix([[65, 66], [67, 68], [69, 70]], to_str=chr) →
        𜸖 A B 𜸘
        │ C D │
        𜸗 E F 𜸙

    print_matrix([[0,0,0],[0,0,0],[0,0,0]], to_str_rc=lambda v, r, c: (r+c+1) * "#") →
        𜸖   #   ##   ### 𜸘
        │  ##  ###  #### │
        𜸗 ### #### ##### 𜸙
    """
    if to_str_rc:
        str_matrix = [
            [to_str_rc(val, r, c) for c, val in enumerate(row)]
            for r, row in enumerate(matrix)
        ]
    else:
        if not to_str:
            to_str = str

        str_matrix = [[to_str(val) for val in row] for row in matrix]

    cell_widths = [max(len(cell) for cell in col) for col in transpose(str_matrix)]

    if len(str_matrix) == 1:
        _print_row(str_matrix[0], prefix="[", suffix="]")
    else:
        _print_row(
            str_matrix[0],
            widths=cell_widths,
            prefix=Matrix.TL.value,
            suffix=Matrix.TR.value,
        )

        for i in range(1, len(str_matrix) - 1):
            _print_row(
                str_matrix[i],
                widths=cell_widths,
                prefix=Matrix.V.value,
                suffix=Matrix.V.value,
            )

        _print_row(
            str_matrix[-1],
            widths=cell_widths,
            prefix=Matrix.BL.value,
            suffix=Matrix.BR.value,
        )


def _print_row(
    values: Iterable[str],
    /,
    widths: Sequence[int] = [],
    prefix: str = "",
    suffix: str = "",
):
    if widths:
        values = [v.rjust(width, " ") for v, width in zip(values, widths)]
    print(prefix, " ".join(values), suffix)


def transpose(matrix: Sequence[Sequence]) -> Sequence[Sequence]:
    """Exchange rows and columns of a matrix.

    transpose([[1, 2], [3, 4]]) == [[1, 3], [2, 4]]
    """
    return [[row[c] for row in matrix] for c in range(len(matrix[0]))]


# I was looking for a way to type something like ruby's `respond_to?` for `+`
# and `*`. SupportsInt is the easiest in the typing library and it covers ints,
# floats, and bools. It excludes complex, which is unfortunate, and strings and
# sequences, which is probably good.
#
# typeshed does something like this, making protocols that have __add__ and
# __radd__ methods and then creating a typevar out of them:
#
# Summable, Mullable based on https://github.com/python/typeshed/blob/main/stdlib/_typeshed/__init__.pyi#L111-L115
# SummableT, MullableT based on https://github.com/python/typeshed/blob/main/stdlib/builtins.pyi#L1926-L1940

_T_co = TypeVar("_T_co", covariant=True)
_T_contra = TypeVar("_T_contra", contravariant=True)


class Summable(Protocol[_T_contra, _T_co]):
    def __add__(self, x: _T_contra, /) -> _T_co: ...
    def __radd__(self, x: _T_contra, /) -> _T_co: ...


SummableT = TypeVar("SummableT", bound=Summable)


class Mullable(Protocol[_T_contra, _T_co]):
    def __mul__(self, x: _T_contra, /) -> _T_co: ...
    def __rmul__(self, x: _T_contra, /) -> _T_co: ...


MullableT1 = TypeVar("MullableT1", bound=Mullable)
MullableT2 = TypeVar("MullableT2", bound=Mullable)

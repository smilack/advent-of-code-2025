from typing import Iterable, Protocol, TypeVar, Literal


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

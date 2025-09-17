#!/usr/bin/env python3
from __future__ import annotations

"""
Working with Just Intonation intervals.
Based on The Just Intotation Primer by David B. Doty.
Page numbers refer to that book.

TODOS
* add page numbers
* Special relationships
* Difference tones (3 varieties)
* Periodicity pitches
* Something something harmonics
* convert list of intervals to harmonic/subharmonic scale degrees

"""



from fractions import Fraction
from typing import ClassVar, Self, List, Iterable
import math
import itertools, operator

from sympy import factorint
import scamp_extensions.pitch.utilities as pitchutils


import itertools, operator
from fractions import Fraction
from typing import Iterable

def steps_to_sequence(steps: Iterable, base: float = 264.0,
                   include_root: bool = True,
                   include_octave: bool = True) -> list[float]:
    """
    steps: iterable of Interval objects whose product is the target interval (e.g., 2/1).
           Each Interval should expose .numerator and .denominator OR .as_fraction() -> Fraction.
    """
    def as_frac(s):
        m = getattr(s, "as_fraction", None)
        if callable(m):
            return m()
        return Fraction(s.numerator, s.denominator)

    fracs = [as_frac(s) for s in steps]
    cum = list(itertools.accumulate(fracs, operator.mul))  # cumulative ratios
    freqs = [base * float(r) for r in cum]
    if include_root:
        freqs = [base] + freqs
    if not include_octave and freqs:
        freqs = freqs[:-1]
    return freqs

# usage:
# steps = Interval.octave.divide(7)
# freqs = steps_to_sequence(steps, base=264.0)



def _is_P_smooth(k: int, P: int | None) -> bool:
    if P is None:
        return True
    if P < 2:
        return k == 1  # only 1 is "P-smooth" when no primes allowed
    return max(factorint(k).keys(), default=1) <= P

def _max_rungs_2limit(p: int, q: int) -> int:
    # number of powers of two you can ever fit in any scaled window [Mq, Mp]
    # width in log2-space is constant: W = log2(p/q)
    W = math.log2(p / q)
    return max(0, math.floor(W) + 1)


def minimal_multiplier_M(p: int, q: int, parts: int, prime_limit: int | None = None) -> int:
    """
    Smallest M such that the integer ladder [Mq..Mp] has at least (parts+1)
    integers whose prime factors are all <= prime_limit. If prime_limit is None,
    no restriction is applied (so M = ceil(parts / (p - q))).
    """
    if prime_limit == 2:
        max_rungs = _max_rungs_2limit(p, q)
        max_parts = max(0, max_rungs - 1)
        if parts > max_parts:
            raise ValueError(
                f"Impossible in 2-limit: interval {p}:{q} can yield at most "
                f"{max_parts} parts (needs {parts})."
            )
    if not (isinstance(p, int) and isinstance(q, int) and p > 0 and q > 0 and p > q):
        raise ValueError("Require positive integers with p > q.")
    if parts < 1:
        raise ValueError("parts must be >= 1.")

    # exact lower bound when no prime limit
    M = max(1, math.ceil(parts / (p - q)))
    if prime_limit is None:
        return M

    while True:
        lo, hi = M * q, M * p
        survivors = sum(1 for k in range(hi, lo - 1, -1) if _is_P_smooth(k, prime_limit))
        if survivors >= parts + 1:
            return M
        M += 1



class Interval(Fraction):

    octave: ClassVar["Interval"]

    def is_superparticular(self) -> bool:
        return self.numerator == self.denominator + 1

    def to_hz(self, base_frequency: int = 264) -> int:
        """
        Converts the interval to a frequency in Hz.

        Args:
            base_frequency (int): The base frequency in Hz.
              The default is 264Hz, the C below A440.

        Returns:
            int: The frequency in Hz.
        """

        return int(base_frequency * self)


    def to_midi(self, base_frequency: int = 264) -> float:
        """
        Converts the interval to a (floating-point) MIDI note number.

        Args:
            base_frequency (int): The base frequency in Hz.
              The default is 264Hz, the C below A440.

        Returns:
            float: The MIDI note number.
        """

        return pitchutils.hertz_to_midi(self.to_hz(base_frequency)) # type: ignore




    def to_cents(self) -> float:
        theta = 1200 / math.log10(2)
        return math.log10(self) * theta



    def above_1_1(self) -> bool:
        "is the interval above 1/1?"
        return self > 1

    def reverse(self) -> Self:
        "reverse the interval"
        return type(self)(self.denominator, self.numerator)

    def __sub__(self, other: Self) -> Self: # type: ignore[override]
        """
        Reverse ratio of subtrahend, then multiply
        """
        if self >= 2/1:
            raise ValueError("Can't subtract intervals larger than an octave")
        if self.numerator < self.denominator:
            raise ValueError("Can't subtract intervals where denominator is greater than numerator")
        other = Fraction(other.denominator, other.numerator) # type: ignore[override]
        result = Fraction.__mul__(self, other) # type: ignore[override]
        # TODO handle it if result < 1/1
        return type(self)(result.numerator, result.denominator) # otherwise result will be a Fraction

    def __add__(self, other: Self) -> Self:  # type: ignore[override]
        """
        To add two Just intervals, you actually multiply them.
        """
        # use Fraction's mul directly
        result = Fraction.__mul__(self, other) # type: ignore[override]
        # TODO handle it if result > 2/1
        # Convert to Interval:
        return type(self)(result.numerator, result.denominator) # otherwise result will be a Fraction


    def __mul__(self, other: Self) -> Self: # type: ignore[override]
        """
        To multiply two Just intervals, you actually multiply them.
        """
        # use Fraction's mul directly
        # I guess that means we don't need this method?
        result = Fraction.__mul__(self, other) # type: ignore[override]
        # TODO handle it if result > 2/1
        return type(self)(result.numerator, result.denominator) # otherwise result will be a Fraction

    def complement(self) -> Self:
        if self >= 2/1:
            raise ValueError("Can't complement intervals larger than an octave")
        if self.numerator < self.denominator:
            raise ValueError("Can't complement intervals where denominator is greater than numerator")
        result = type(self).octave  - self
        return type(self)(result.numerator, result.denominator) # otherwise result will be a Fraction


    # TODO refactor this to divide any interval - make it an instance method
    # @classmethod
    def divide(self, pieces: int, prime_limit: int|None = None) -> List[Self]:
        """
        Divide an interval into a given number of pieces, optionally limiting the prime factors of the resulting intervals.
        Page 26.
        """

        if prime_limit:
            multiplier = minimal_multiplier_M(self.numerator, self.denominator, pieces, prime_limit)
        else:
            multiplier = pieces
        # start with the simplest case
        hi = self.numerator * multiplier
        lo = self.denominator * multiplier
        seq = []
        for i in range(hi, lo - 1, -1):
            seq.append(i)

        if prime_limit:
            seq = [x for x in seq if _is_P_smooth(x, prime_limit)]
            # this may be redundant in most cases, but not in others:
            seq = seq[:pieces + 1]

        ret = []
        while True:
            ret.append(type(self)(seq[0], seq[1]))
            seq.pop(0)
            if len(seq) == 1:
                break


        return ret

Interval.octave = Interval(2, 1)

def special_relationships():
    """
    Arthur Benade's "special relationships".
    Page 22.
    """
    return [
        Interval(2, 1), # Octave
        Interval(3, 2), # Perfect Fifth
        Interval(4, 3), # Perfect Fourth
        Interval(5, 3), # Major Sixth
        Interval(5, 4), # Major Third
        Interval(6, 5), # Minor Third
        Interval(7, 4), # Harmonic or Septimal Major Seventh
        Interval(7, 5), # Septimal Tritone
        Interval(8, 5), # Minor Sixth
        Interval(7, 6), # Subminor or Septimal Major Third
        # above an octave:
        Interval(7, 3), # Septimal or Subminor Tenth
        Interval(8, 3), # Octave Extension of Perfect Fourth
        Interval(3, 1), # Perfect Twelfth
        Interval(7, 2), # Octave Extension of Harmonic Seventh
        Interval(4, 1), # Double Octave
        Interval(5, 1), # Two octaves plus a perfect fifth
        Interval(7, 1), # Two octaves plus a harmonic seventh
        Interval(8, 1), # Triple octave
        Interval(9, 4), # Major Ninth
    ]


def difftone1(f1: Interval, f2: Interval) -> Interval:
    "page 16"
    return f1 - f2

def difftone2(f1: Interval, f2: Interval) -> Interval:
    return (2 * f1) - f2

def difftone3(f1: Interval, f2: Interval) -> Interval:
    return (3 * f1) - (2 * f2)



if __name__ == "__main__":
    # print(Interval(8, 7).is_superparticular())
    print(Interval.octave.divide(4))
    print(Interval.octave.divide(4, 5))
    print(Interval(3,2).divide(4))
    print(Interval(3,2).divide(4, 7))
    print(Interval(3,2).divide(4, 5))
    print(Interval(3,2).divide(4, 3))
    # print(Interval(5,4).divide(5, 2)) # impossible

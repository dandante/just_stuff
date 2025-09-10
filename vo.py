#!/usr/bin/env python3

"""
Convert between Hertz and volt per octave
"""

import math
from typing import Iterable, Union

Number = Union[int, float]

# VCV rack uses C4 as the baseline voltage
C4_HZ = 261.6256


def hz_to_vpo(f: Union[Number, Iterable[Number]],
              f_ref: float = C4_HZ, # was 440.0
              v_ref: float = 0.0):
    """
    Convert frequency (Hz) -> volts (1 V/oct).

    V = v_ref + log2(f / f_ref)

    Parameters
    ----------
    f : float | iterable of floats
        Frequency (Hz). Must be > 0.
    f_ref : float
        Reference frequency (Hz) that corresponds to v_ref volts.
    v_ref : float
        Reference voltage (V).

    Returns
    -------
    float or list[float]
    """
    def one(x):
        if x <= 0:
            raise ValueError("Frequency must be > 0")
        return v_ref + math.log2(x / f_ref)

    if isinstance(f, (list, tuple)):
        return [one(x) for x in f]
    return one(f)


def vpo_to_hz(v: Union[Number, Iterable[Number]],
              f_ref: float = C4_HZ,
              v_ref: float = 0.0):
    """
    Convert volts (1 V/oct) -> frequency (Hz).

    f = f_ref * 2**(V - v_ref)
    """
    def one(x):
        return f_ref * (2 ** (x - v_ref))

    if isinstance(v, (list, tuple)):
        return [one(x) for x in v]
    return one(v)

# Convenience: 0 V at C0 (≈16.3516 Hz)
C0_HZ = 16.351597831287414
# VCV rack uses C4 as the baseline voltage
C4_HZ = 261.6256
# Example: map 440 Hz with 0 V at C0
print(hz_to_vpo(440.0, v_ref=0.0))  # ~4.0 V
# Example: if 0 V is A4=440 Hz, then:
print(hz_to_vpo(880.0, v_ref=0.0))  # 1.0 V
print(vpo_to_hz(1.0, v_ref=0.0))    # 880.0 Hz


"""Deterministic generation of PRV operating schedules."""

import itertools
import math
from typing import Sequence


def generate_prv_schedules(
    settings: Sequence[float],
    periods: int = 4,
) -> list[tuple[float, ...]]:
    """Generate every combination of PRV settings across time periods.

    Each schedule contains one setting per operating period.
    The order of settings in the input is preserved.

    Example:
        2 settings across 3 periods produce 2**3 = 8 schedules.
    """
    if isinstance(periods, bool) or not isinstance(periods, int):
        raise TypeError("periods must be an integer.")

    if periods < 1:
        raise ValueError("periods must be at least 1.")

    if not settings:
        raise ValueError("At least one PRV setting is required.")

    validated_settings = []

    for setting in settings:
        if isinstance(setting, bool) or not isinstance(setting, (int, float)):
            raise TypeError("Every PRV setting must be a number.")

        if not math.isfinite(setting):
            raise ValueError("Every PRV setting must be finite.")

        if setting <= 0:
            raise ValueError("Every PRV setting must be greater than zero.")

        validated_settings.append(float(setting))

    if len(set(validated_settings)) != len(validated_settings):
        raise ValueError("PRV settings must be unique.")

    return list(itertools.product(validated_settings, repeat=periods))

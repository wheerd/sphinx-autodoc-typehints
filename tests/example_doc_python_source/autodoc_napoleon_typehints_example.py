#!/usr/bin/env python

"""Small module to provide sourcecode for testing if everything works as needed

"""

from typing import Union, Optional, Iterable


def format_unit(value: Union[float, int], unit: str) -> str:
    """Formats the given value as a human readable string using the given units.

    :param value: A numeric value.
    :param unit: The unit for the value (kg, m, etc.).

    :returns: This function returns something.

    """
    return '{} {}'.format(value, unit)


def format_unit_google(value: Union[float, int], unit: str) -> str:
    """Formats the given value as a human readable string using the given units.

    Args:
        value: A numeric value.
        unit: The unit for the value (kg, m, etc.).

    Returns:
        This function returns something.

    """
    return '{} {}'.format(value, unit)


def format_unit_numpy(value: Union[float, int], unit: str) -> str:
    """Formats the given value as a human readable string using the given units.

    Parameters
    ----------
    value:
        A numeric value.
    unit:
        The unit for the value (kg, m, etc.).

    Returns
    -------
    This function returns something.

    """
    return '{} {}'.format(value, unit)

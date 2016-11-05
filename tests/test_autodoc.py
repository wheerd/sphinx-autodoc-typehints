#!/usr/bin/env python

"""
Testing.
"""

import inspect
import os
import pytest
from sphinx_testing import with_app
import sys
from typing import (Any, Callable, Dict, Generic, Mapping, Optional, Pattern,
                    Tuple, Type, TypeVar, Union)

sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), 'example_doc_python_source'))

from sphinx_autodoc_napoleon_typehints import process_docstring, format_annotation
from autodoc_napoleon_typehints_example import format_unit, format_unit_google, format_unit_numpy


T = TypeVar('T')
U = TypeVar('U', covariant=True)
V = TypeVar('V', contravariant=True)


class A:
    def get_type(self) -> Type['A']:
        return type(self)


class B(Generic[T]):
    pass


class C(Dict[T, int]):
    pass


@pytest.mark.parametrize('annotation, expected_result', [
    (str,                           ':class:`str`'),
    (int,                           ':class:`int`'),
    (type(None),                    '``None``'),
    (Any,                           ':class:`~typing.Any`'),
    (Generic[T],                    ':class:`~typing.Generic`\\[\\~T]'),
    (Mapping,                       ':class:`~typing.Mapping`\\[\\~KT, \\+VT_co]'),
    (Mapping[T, int],               ':class:`~typing.Mapping`\\[\\~T, :class:`int`]'),
    (Mapping[str, V],               ':class:`~typing.Mapping`\\[:class:`str`, \\-V]'),
    (Mapping[T, U],                 ':class:`~typing.Mapping`\\[\\~T, \\+U]'),
    (Mapping[str, bool],            ':class:`~typing.Mapping`\\[:class:`str`, :class:`bool`]'),
    (Dict,                          ':class:`~typing.Dict`\\[\\~KT, \\~VT]'),
    (Dict[T, int],                  ':class:`~typing.Dict`\\[\\~T, :class:`int`]'),
    (Dict[str, V],                  ':class:`~typing.Dict`\\[:class:`str`, \\-V]'),
    (Dict[T, U],                    ':class:`~typing.Dict`\\[\\~T, \\+U]'),
    (Dict[str, bool],               ':class:`~typing.Dict`\\[:class:`str`, :class:`bool`]'),
    (Tuple,                         ':class:`~typing.Tuple`'),
    (Tuple[str, bool],              ':class:`~typing.Tuple`\\[:class:`str`, :class:`bool`]'),
    (Tuple[int, int, int],          ':class:`~typing.Tuple`\\[:class:`int`, :class:`int`, '
                                    ':class:`int`]'),
    (Tuple[str, ...],               ':class:`~typing.Tuple`\\[:class:`str`, ...]'),
    (Union,                         ':class:`~typing.Union`'),
    (Union[str, bool],              ':class:`~typing.Union`\\[:class:`str`, :class:`bool`]'),
    (Optional[str],                 ':class:`~typing.Optional`\\[:class:`str`]'),
    (Optional[Union[int, str]],     ':class:`~typing.Optional`\\[:class:`~typing.Union`'
                                    '\\[:class:`int`, :class:`str`]]'),
    (Union[Optional[int], str],     ':class:`~typing.Optional`\\[:class:`~typing.Union`'
                                    '\\[:class:`int`, :class:`str`]]'),
    (Union[int, Optional[str]],     ':class:`~typing.Optional`\\[:class:`~typing.Union`'
                                    '\\[:class:`int`, :class:`str`]]'),
    (Callable,                      ':class:`~typing.Callable`'),
    (Callable[..., int],            ':class:`~typing.Callable`\\[..., :class:`int`]'),
    (Callable[[int], int],          ':class:`~typing.Callable`\\[\\[:class:`int`], :class:`int`]'),
    (Callable[[int, str], bool],    ':class:`~typing.Callable`\\[\\[:class:`int`, :class:`str`], '
                                    ':class:`bool`]'),
    (Callable[[int, str], None],    ':class:`~typing.Callable`\\[\\[:class:`int`, :class:`str`], '
                                    '``None``]'),
    (Callable[[T], T],              ':class:`~typing.Callable`\\[\\[\\~T], \\~T]'),
    (Pattern,                       ':class:`~typing.Pattern`\\[\\~AnyStr]'),
    (Pattern[str],                  ':class:`~typing.Pattern`\\[:class:`str`]'),
    (A,                             ':class:`~%s.A`' % __name__),
    (B,                             ':class:`~%s.B`\\[\\~T]' % __name__),
    (C,                             ':class:`~%s.C`\\[\\~T]' % __name__),
    (Type,                          ':class:`~typing.Type`\\[\\+CT]'),
    (Type[A],                       ':class:`~typing.Type`\\[:class:`~%s.A`]' % __name__),
    (Type['A'],                     ':class:`~typing.Type`\\[A]'),
    (Type['str'],                   ':class:`~typing.Type`\\[:class:`str`]'),
])
def test_format_annotation(annotation, expected_result):
    result = format_annotation(annotation, None)
    assert result == expected_result


def test_format_annotation_with_obj():
    result = format_annotation(Type['A'], A.get_type)
    assert result == ':class:`~typing.Type`\\[:class:`~%s.A`]' % __name__

    result = format_annotation(Type['A'], A)
    assert result == ':class:`~typing.Type`\\[A]'


@pytest.mark.parametrize('function, expected_docstr', [
    (format_unit, """:rtype: :class:`str`
    Formats the given value as a human readable string using the given units.

    :type value: :class:`~typing.Union`\\[:class:`float`, :class:`int`]
    :param value: A numeric value.
    :type unit: :class:`str`
    :param unit: The unit for the value (kg, m, etc.).

    :returns: This function returns something.

    """),
    (format_unit_google, """:rtype: :class:`str`
    Formats the given value as a human readable string using the given units.

    Args:
        value (:class:`~typing.Union`\\[:class:`float`, :class:`int`]): A numeric value.
        unit (:class:`str`): The unit for the value (kg, m, etc.).

    Returns:
        This function returns something.

    """),
    (format_unit_numpy, """:rtype: :class:`str`
    Formats the given value as a human readable string using the given units.

    Parameters
    ----------
    value : :class:`~typing.Union`\\[:class:`float`, :class:`int`]
        A numeric value.
    unit : :class:`str`
        The unit for the value (kg, m, etc.).

    Returns
    -------
    This function returns something.

    """)
])
def test_process_napoleon_docstrings(function, expected_docstr):
    """Test that the annotation transformations work as expected for numpy and
    google docstring as well.

    """
    lines = inspect.cleandoc(function.__doc__).splitlines()
    expected_lines = inspect.cleandoc(expected_docstr).splitlines()

    process_docstring(None, 'function', function.__name__, format_unit, {}, lines)

    assert lines == expected_lines


@pytest.fixture
def html():
    """Test if plugin actually works
    """

    html_str = ''

    @with_app(buildername='html',
              srcdir=os.path.join(os.path.dirname(__file__), 'example_docs'),
              copy_srcdir_to_tmpdir=True)
    def build(app, status, warning):
        app.build()
        html = (app.outdir / 'index.html').read_text()
        nonlocal html_str
        html_str = html

    build()
    return html_str


def test_autodoc(html):
    # with open('html_output.html', 'w') as f:
    #     f.write(html)
    start = "<p>This is test documentation</p>"
    start_ix = html.find(start)
    assert start_ix > -1, 'Start of actual code documentation is not where it should be... it wasn\'t found at all.'
    end = '</dd></dl>\n'
    end_ix = html.rfind(end) + len(end)
    assert end_ix > -1, 'End of actual code documentation is not where it should be... it wasn\'t found at all.'
    actual = html[start_ix:end_ix]
    assert actual

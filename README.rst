|Build Status| |Coverage Status| |PyPi Status|


sphinx-autodoc-napoleon-typehints
=================================

This extension allows you to use Python 3 annotations for documenting acceptable argument types
and return value types of functions. This allows you to use type hints in a very natural fashion,
allowing you to migrate from this:

.. code-block:: python

    def format_unit(value, unit):
        """
        Formats the given value as a human readable string using the given units.

        :param float|int value: a numeric value
        :param str unit: the unit for the value (kg, m, etc.)
        :rtype: str
        """
        return '{} {}'.format(value, unit)

to this:

.. code-block:: python

    from typing import Union

    def format_unit(value: Union[float, int], unit: str) -> str:
        """
        Formats the given value as a human readable string using the given units.

        :param value: a numeric value
        :param unit: the unit for the value (kg, m, etc.)
        """
        return '{} {}'.format(value, unit)


There is also support for google docstrings or numpy docstrings with help of the napoleon
`napoleon sphinx extention <http://sphinxcontrib-napoleon.readthedocs.io/en/latest/>`_.
This means that even docstrings like this:

.. code-block:: python

    def format_unit_google(self, value: Union[float, int], unit: str, test: Optional[Union[Iterable, str]]) -> str:
        """
        Formats the given value as a human readable string using the given units.

        Args:
            value: a numeric value
            unit: the unit for the value (kg, m, etc.)
            test: bla bla blathe unit for the value (kg, m, etc.)

        Returns:
           This function returns something of
           value: and does not overwrite this part.
        """
        return '{} {}'.format(value, unit)

    def format_unit_numpy(self, value: Union[float, int], unit: str, test: Optional[Union[Iterable, str]]) -> str:
        """
        Formats the given value as a human readable string using the given units.

        Parameters
        ----------
        value: a numeric value
        unit: the unit for the value (kg, m, etc.)
        test: bla bla blathe unit for the value (kg, m, etc.)

        Returns
        -------
        This function returns something of
        value: and does not overwrite this part.
        """
        return '{} {}'.format(value, unit)


the result for which is the same as above


Installation and setup
----------------------

First, use pip to download and install the extension::

    $ pip install sphinx-autodoc-napoleon-typehints

Then, add the extension to your ``conf.py``:

.. code-block:: python

    extensions = [
        'sphinx.ext.autodoc',
        'sphinx_autodoc_napoleon_typehints'
    ]


How it works
------------

The extension listens to the ``autodoc-process-signature`` and ``autodoc-process-docstring``
Sphinx events. In the former, it strips the annotations from the function signature. In the latter,
it injects the appropriate ``:type argname:`` and ``:rtype:`` directives into the docstring.

Only arguments that have an existing ``:param:`` directive in the docstring get their respective
``:type:`` directives added. The ``:rtype:`` directive is added if and only if no existing
``:rtype:`` is found.

This extension does not currently have any configuration options.


Project links
-------------

* `Source repository <https://github.com/daviskirk/sphinx-autodoc-napoleon-typehints>`_
* `Issue tracker <https://github.com/daviskirk/sphinx-autodoc-napoleon-typehints/issues>`_
* The project was originally forked from `here <https://github.com/agronholm/sphinx-autodoc-typehints>`_


.. |Build Status| image:: https://travis-ci.org/daviskirk/sphinx-autodoc-napoleon-typehints.svg?branch=master
   :target: https://travis-ci.org/daviskirk/sphinx-autodoc-napoleon-typehints
.. |Coverage Status| image:: https://coveralls.io/repos/github/daviskirk/sphinx-autodoc-napoleon-typehints/badge.svg?branch=master
   :target: https://coveralls.io/github/daviskirk/sphinx-autodoc-napoleon-typehints?branch=master
.. |PyPi Status| image:: https://badge.fury.io/py/sphinx-autodoc-napoleon-typehints.svg
   :target: https://badge.fury.io/py/sphinx-autodoc-napoleon-typehints

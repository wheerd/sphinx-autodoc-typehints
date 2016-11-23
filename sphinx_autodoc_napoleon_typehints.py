import inspect
import logging
import re
import sys

from sphinx.ext.autodoc import (ClassDocumenter, Documenter, add_documenter,
                                formatargspec)
from sphinx.locale import _
from sphinx.util.inspect import getargspec

try:
    from backports.typing import (Any, Callable, Generic, GenericMeta, Tuple, TypeVar, TypingMeta,
                                  Union, _ForwardRef, _TypeAlias, get_type_hints)
except ImportError:
    from typing import (Any, Callable, Generic, GenericMeta, Tuple, TypeVar, TypingMeta,
                        Union, _ForwardRef, _TypeAlias, get_type_hints, Iterable, Iterator, Generator)


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class mutable_list_iter:
    def __init__(self, list):
        self._list = list
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            value = self._list[self._index]
        except IndexError:
            raise StopIteration
        self._index += 1
        return value

    def peek(self):
        return self._list[self._index]

    def undo(self):
        self._index -= 1

    def replace_last(self, new_value):
        self._list[self._index - 1] = new_value


def format_annotation(annotation, obj=None):
    if inspect.isclass(annotation):
        # builtin types don't need to be qualified with a module name
        if annotation.__module__ == 'builtins':
            if annotation.__qualname__ == 'NoneType':
                return '``None``'
            else:
                return ':class:`{}`'.format(annotation.__qualname__)

        role = 'class'
        params = None
        # Check first if we have an TypingMeta instance, because when mixing in another meta class,
        # some information might get lost.
        # For example, a class inheriting from both tuple and Enum ends up not having the
        # TypingMeta metaclass and hence none of the Tuple typing information.
        if isinstance(annotation, TypingMeta):
            # Since Any is a superclass of everything, make sure it gets handled normally.
            if annotation is Any:
                role = 'data'
            # Generic classes have type arguments
            elif isinstance(annotation, GenericMeta):
                params = annotation.__args__
                # Make sure to format Generic[T, U, ...] correctly, because it only
                # has parameters but nor argument values for them
                if not params and issubclass(annotation, Generic):
                    params = annotation.__parameters__
            # Tuples are not Generics, so handle their type parameters separately.
            elif issubclass(annotation, Tuple):
                role = 'data'
                if annotation.__tuple_params__:
                    params = list(annotation.__tuple_params__)
                # Tuples can have variable size with a fixed type, indicated by an Ellipsis:
                # e.g. Tuple[T, ...]
                if annotation.__tuple_use_ellipsis__:
                    params.append(Ellipsis)
            # Unions are not Generics, so handle their type parameters separately.
            elif issubclass(annotation, Union):
                role = 'data'
                if annotation.__union_params__:
                    params = list(annotation.__union_params__)
                    # If the Union contains None, wrap it in an Optional, i.e.
                    # Union[T,None]   => Optional[T]
                    # Union[T,U,None] => Optional[Union[T, U]]
                    if type(None) in annotation.__union_set_params__:
                        annotation.__qualname__ = 'Optional'
                        params.remove(type(None))
                        if len(params) > 1:
                            params = [Union[tuple(params)]]
            # Callables are not Generics, so handle their type parameters separately.
            # They have the format Callable[arg_types, return_type].
            # arg_types is either a list of types or an Ellipsis for Callables with
            # variable arguments.
            elif issubclass(annotation, Callable):
                role = 'data'
                if annotation.__args__ is not None or annotation.__result__ is not None:
                    if annotation.__args__ is Ellipsis:
                        args_r = Ellipsis
                    else:
                        args_r = '\\[{}]'.format(', '.join(format_annotation(a, obj) for a in annotation.__args__))
                    params = [args_r, annotation.__result__]
            # Type variables are formatted with a prefix character (~, +, -)
            # which have to be escaped.
            elif isinstance(annotation, TypeVar):
                return '\\' + repr(annotation)
            # Strings inside of type annotations are converted to _ForwardRef internally
            elif isinstance(annotation, _ForwardRef):
                try:
                    try:
                        global_vars = obj is not None and obj.__globals__ or dict()
                    except AttributeError:
                        global_vars = dict()
                    # Evaluate the type annotation string and then format it
                    actual_type = eval(annotation.__forward_arg__, global_vars)
                    return format_annotation(actual_type, obj)
                except Exception:
                    return annotation.__forward_arg__

        generic = params and '\\[{}]'.format(', '.join(format_annotation(p, obj) for p in params)) or ''
        return ':{}:`~{}.{}`{}'.format(role, annotation.__module__, annotation.__qualname__, generic)
    # _TypeAlias is an internal class used for the Pattern/Match types
    # It represents an alias for another type, e.g. Pattern is an alias for any string type
    elif isinstance(annotation, _TypeAlias):
        actual_type = format_annotation(annotation.type_var, obj)
        return ':class:`~typing.{}`\\[{}]'.format(annotation.name, actual_type)
    # Ellipsis is used in Callable/Tuple
    elif annotation is Ellipsis:
        return '...'

    return str(annotation)


def process_signature(app, what: str, name: str, obj, options, signature, return_annotation):
    if callable(obj):
        if what in ('class', 'exception'):
            obj = getattr(obj, '__init__')

        try:
            argspec = getargspec(obj)
        except TypeError:
            return

        if inspect.ismethod(obj) and argspec.args:
            del argspec.args[0]

        return formatargspec(obj, *argspec[:-1]), None


ARGUMENT_HEADINGS = (
    'Args:',
    'Arguments:',
    'Parameters:',
    'Other Parameters:',
    'Keyword Args:',
    'Keyword Arguments:',
    'Attributes:'
)
RETURN_HEADINGS = (
    'Return:',
    'Returns:',
    'Yield:',
    'Yields:'
)

_google_args_regex = r'^{}(\*?\*?\s*)(\w+)(?:\s+\((.*?)\))?\s*:\s*(.*)$'
_google_return_regex = r'^(\s+)(?:(.*?)\s*:\s*)?(.*)$'


def _process_google_docstrings(app, type_hints, lines, obj):
    """Process google docstrings parameters."""
    lines = mutable_list_iter(lines)
    found_arguments = set()
    for line in lines:
        if line.strip() in ARGUMENT_HEADINGS:
            found_arguments.update(_process_google_args(app, lines, type_hints, obj))
        elif line.strip() in RETURN_HEADINGS:
            if _process_google_return(app, lines, type_hints, obj, line.startswith('Yield')):
                found_arguments.add('return')

    return found_arguments

def _process_google_args(app, lines, type_hints, obj):
    """Process the argument section of a google docstring."""
    indent = None
    found_arguments = set()
    for line in lines:
        if not line.strip():
            continue
        match = re.match(r'^\s+', line)
        if not match:
            lines.undo()
            break
        new_indent = match.group(0)
        is_unindent = indent is not None and (
            not new_indent.startswith(indent)
            or len(indent) >= len(new_indent))
        if is_unindent:
            indent = None
        if indent is None:
            indent = match.group(0)
            match = re.match(_google_args_regex.format(indent), line)
            if match:
                arg_prefix, arg_name, arg_type, rest = match.groups()

                type_hint = None
                if arg_type:
                    if not '`' in arg_type:
                        try:
                            module = sys.modules[obj.__module__]
                            type_hint = eval(arg_type, module.__dict__)

                        except Exception as e:
                            app.warn("Failed to parse type of argument {} for {}: {}."
                                     .format(arg_name, obj.__name__, e))
                elif arg_name in type_hints:
                    type_hint = type_hints[arg_name]

                if type_hint is not None:
                    if rest:
                        rest = ' ' + rest
                    arg_type = format_annotation(type_hint, obj)
                    lines.replace_last('{}{}{} ({}):{}'.format(indent, arg_prefix, arg_name, arg_type, rest))
                elif not arg_type:
                    app.warn("Found argument {} for {} in the docstring, but got no type "
                             "hint for it.".format(arg_name, obj.__name__))
                found_arguments.add(arg_name)
        else:
            indent = None
    return found_arguments

def _process_google_return(app, lines, type_hints, obj, is_yield):
    line = next(lines)
    match = re.match(_google_return_regex, line)
    found = False
    if match:
        indent, return_type, rest = match.groups()

        if return_type:
            app.debug("Skipping return section of {} because it already has a type "
                      "defined in the docstring.".format(obj.__name__))
        elif 'return' in type_hints:
            if rest:
                rest = ' ' + rest
            return_type = type_hints['return']
            if is_yield:
                if isinstance(return_type, type) and issubclass(return_type, (Iterable, Iterator, Generator)):
                    return_type = return_type.__args__[0]
                else:
                    app.warn("{} has a yield section in the docstring, but the return "
                             "type hint is not an iterable type ({}).".format(obj.__name__, return_type))
            return_type = format_annotation(return_type, obj)
            lines.replace_last('{}{}:{}'.format(indent, return_type, rest))
        else:
            app.warn("Found return/yield section for {} in the docstring, but got no "
                     "type hint for it.".format(obj.__name__))
        found = True

        for line in lines:
            if line.strip() and not line.startswith(indent):
                lines.undo()
                break
    else:
        lines.undo()

    return found


def _check_numpy_section_start(lines, i, section=None):
    """Check if numpy section starts at line `i`"""
    return (
        i > 0 and
        i < len(lines) - 1 and
        lines[i + 1].startswith('---') and
        (section is None or lines[i] == section)
    )


def _process_numpy_docstrings(type_hints, lines, obj):
    """Process numpy docstrings parameters."""
    for argname, annotation in type_hints.items():
        formatted_annotation = format_annotation(annotation, obj)

        if argname == 'return':
            pass
        else:
            logger.debug('Searching for %s', argname)
            in_args_section = False
            for i, line in enumerate(lines):
                if _check_numpy_section_start(lines, i - 1, 'Parameters'):
                    logger.debug('Numpy parameters section ended on line %i', i)
                    in_args_section = True
                elif in_args_section:
                    if _check_numpy_section_start(lines, i):
                        in_args_section = False
                        logger.debug('Numpy parameters section ended on line %i', i)
                        break
                    match = re.match('{}( ?: ?)?'.format(argname), line)
                    if match:
                        lines[i] = argname + ' : ' + formatted_annotation
                        logger.debug('line replaced: %s', lines[i])


def _process_sphinx_docstrings(type_hints, lines, obj):
    for arg_name, annotation in type_hints.items():
        if arg_name == 'return':
            if annotation is None:
                continue
            insert_index = None # len(lines)
            for i, line in enumerate(lines):
                if line.startswith(':rtype:'):
                    insert_index = None
                    break
                elif line.startswith(':return:') or line.startswith(':returns:'):
                    insert_index = i

            if insert_index is not None:
                lines.insert(insert_index, ':rtype: {}'.format(format_annotation(annotation, obj)))
        else:
            searchfor = ':param {}:'.format(arg_name)
            for i, line in enumerate(lines):
                if line.startswith(searchfor):
                    lines.insert(i, ':type {}: {}'.format(arg_name, format_annotation(annotation, obj)))
                    break


def process_docstring(app, what, name, obj, options, lines):
    if callable(obj):
        if what in ('class', 'exception'):
            obj = getattr(obj, '__init__')

        # Unwrap until we get to the original definition
        while hasattr(obj, '__wrapped__'):
            obj = obj.__wrapped__

        try:
            type_hints = get_type_hints(obj)
        except AttributeError:
            return

        _process_sphinx_docstrings(type_hints, lines, obj)
        _process_google_docstrings(app, type_hints, lines, obj)
        _process_numpy_docstrings(type_hints, lines, obj)

class CustomClassDocumenter(ClassDocumenter):
    def add_directive_header(self, sig):
        # type: (unicode) -> None
        if self.doc_as_attr:
            self.directivetype = 'attribute'
        Documenter.add_directive_header(self, sig)

        # add inheritance info, if wanted
        if not self.doc_as_attr and self.options.show_inheritance:
            sourcename = self.get_sourcename()
            self.add_line(u'', sourcename)
            if hasattr(self.object, '__bases__') and len(self.object.__bases__):
                bases = [format_annotation(b, self.object)
                         for b in self.object.__bases__
                         if b != object]
                if bases:
                    self.add_line(u'   ' + _(u'Bases: %s') % ', '.join(bases),
                                  sourcename)

def setup(app):
    app.connect('autodoc-process-signature', process_signature)
    app.connect('autodoc-process-docstring', process_docstring)
    add_documenter(CustomClassDocumenter)

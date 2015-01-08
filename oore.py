# encoding: utf-8
"""
    oore
    ~~~~

    :copyright: 2014 by Daniel Neuhäuser
    :license: BSD, see LICENSE.rst for details
"""
import re


class r(object):
    """
    A wrapper for :class:`re.RegexObject`, that provides several useful ways to
    create new regular expressions.

    Concatenation::

        r('foo') + r('bar') == r('foobar')

    Or::
        r('foo') + r('bar') == r('foo|bar')

    Repetition::

        r('foo')[n] == r('foo{n}')

    Zero/One/N or more::

        r('foo')[0, ...] == r('(foo)*')
        r('foo')[1, ...] == r('(foo)+')
        r('foo')[n, ...] == r('(foo){n}foo*')

    In addition to that all attributes/methods provided by
    :class:`re.RegexObject` instances are supported as well.

    Combining patterns using different string types e.g.
    ``r(u'foo') + r(b'bar')`` will raise a :exc:`TypeError`.
    """
    def __init__(self, pattern):
        self.pattern = pattern
        self._compiled = re.compile(self.pattern)

    @property
    def flags(self):
        return self._compiled.flags

    @property
    def groups(self):
        return self._compiled.groups

    @property
    def groupindex(self):
        return self._compiled.groupindex

    def __add__(self, other):
        if isinstance(other, r):
            if self.pattern.__class__ != other.pattern.__class__:
                raise TypeError(
                    'incompatible pattern types: {} and {}'.format(
                        self.pattern.__class__, other.pattern.__class__
                    )
                )
            elif isinstance(self.pattern, bytes):
                return r(
                    '(?:{})(?:{})'.format(
                        self.pattern.decode('latin1'),
                        other.pattern.decode('latin1')
                    ).encode('latin1')
                )
            else:
                return r('(?:{})(?:{})'.format(self.pattern, other.pattern))
        return NotImplemented

    def __or__(self, other):
        if isinstance(other, r):
            if self.pattern.__class__ != other.pattern.__class__:
                raise TypeError(
                    'incompatible pattern types: {} and {}'.format(
                        self.pattern.__class__,
                        other.pattern.__class__
                    )
                )
            elif isinstance(self.pattern, bytes):
                return r(
                    '(?:{})|(?:{})'.format(
                        self.pattern.decode('latin1'),
                        other.pattern.decode('latin1')
                    ).encode('latin1')
                )
            else:
                return r('(?:{})|(?:{})'.format(self.pattern, other.pattern))
        return NotImplemented

    def __getitem__(self, index):
        if isinstance(index, int) and index > 0:
            if isinstance(self.pattern, bytes):
                return r(
                    '(?:{}){{{}}}'.format(
                        self.pattern.decode('latin1'),
                        index
                    ).encode('latin1')
                )
            else:
                return r('(?:{}){{{}}}'.format(self.pattern, index))
        elif isinstance(index, tuple) and len(index) == 2:
            if (
                isinstance(index[0], int) and isinstance(index[1], int) and
                index[0] < index[1]
            ):
                if isinstance(self.pattern, bytes):
                    return r(
                        '(?:{}){{{},{}}}'.format(
                            self.pattern.decode('latin1'),
                            *index
                        ).encode('latin1')
                    )
                else:
                    return r('(?:{}){{{},{}}}'.format(self.pattern, *index))
            elif (
                isinstance(index[0], int) and index[1] is Ellipsis
            ):
                if index[0] == 0:
                    if isinstance(self.pattern, bytes):
                        return r(
                            '(?:{})*'.format(
                                self.pattern.decode('latin1')
                            ).encode('latin1')
                        )
                    else:
                        return r('(?:{})*'.format(self.pattern))
                elif index[0] == 1:
                    if isinstance(self.pattern, bytes):
                        return r(
                            '(?:{})+'.format(
                                self.pattern.decode('latin1')
                            ).encode('latin1')
                        )
                    else:
                        return r('(?:{})+'.format(self.pattern))
                else:
                    if isinstance(self.pattern, bytes):
                        return r(
                            '(?:{pattern}){{{n}}}(?:{pattern})*'.format(
                                pattern=self.pattern.decode('latin1'),
                                n=index[0]
                            ).encode('latin1')
                        )
                    else:
                        return r(
                            '(?:{pattern}){{{n}}}(?:{pattern})*'.format(
                                pattern=self.pattern, n=index[0]
                            )
                        )
        return NotImplemented

    def search(self, string, *args):
        return self._compiled.search(string, *args)

    def match(self, string, *args):
        return self._compiled.match(string, *args)

    def split(self, string, maxsplit=0):
        return self._compiled.split(string, maxsplit=maxsplit)

    def findall(self, string, *args):
        return self._compiled.findall(string, *args)

    def finditer(self, string, *args):
        return self._compiled.finditer(string, *args)

    def sub(self, repl, string, count=0):
        return self._compiled.sub(repl, string, count=count)

    def subn(self, repl, string, count=0):
        return self._compiled.subn(repl, string, count=count)

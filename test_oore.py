# encoding: utf-8
"""
    test_oore
    ~~~~~~~~~

    :copyright: 2014 by Daniel Neuhäuser
    :license: BSD, see LICENSE.rst for details
"""
import re
import sys

from oore import r

from pytest import raises


if sys.version_info[0] == 2:
    text_type = unicode
else:
    text_type = str


def test_add_text():
    foo = r(u'foo')
    bar = r(u'bar')
    foobar = foo + bar
    assert isinstance(foobar.pattern, text_type)
    assert foobar.match(u'foobar')


def test_add_bytes():
    foo = r(b'foo')
    bar = r(b'bar')
    foobar = foo + bar
    assert isinstance(foobar.pattern, bytes)
    assert foobar.match(b'foobar')


def test_add_mixed():
    foo = r(u'foo')
    bar = r(b'bar')
    with raises(TypeError):
        foo + bar


def test_or_text():
    a = r(u'foo|bar')
    b = r(u'foo') | r(u'bar')
    for expr in [a, b]:
        assert expr.match(u'foo')
        assert expr.match(u'bar')


def test_or_bytes():
    a = r(b'foo|bar')
    b = r(b'foo') | r(b'bar')
    for expr in [a, b]:
        assert expr.match(b'foo')
        assert expr.match(b'bar')


def test_or_mixed():
    foo = r(u'foo')
    bar = r(b'bar')
    with raises(TypeError):
        foo | bar


def test_repeat_text():
    foo = r(u'foo')
    foo_3 = foo[3]
    assert isinstance(foo_3.pattern, text_type)
    assert foo_3.match(u'foo' * 3)


def test_repeat_bytes():
    foo = r(b'foo')
    foo_3 = foo[3]
    assert isinstance(foo_3.pattern, bytes)
    assert foo_3.match(b'foo' * 3)


def test_repeat_from_to_text():
    foo = r(u'foo')
    foo_2_to_4 = foo[2, 4]
    assert isinstance(foo_2_to_4.pattern, text_type)
    for i in range(2, 5):
        assert foo_2_to_4.match(u'foo' * i)


def test_repeat_from_to_bytes():
    foo = r(b'foo')
    foo_2_to_4 = foo[2, 4]
    assert isinstance(foo_2_to_4.pattern, bytes)
    for i in range(2, 5):
        assert foo_2_to_4.match(b'foo' * i)


def test_repeat_zero_or_more_text():
    foo = r(u'foo')
    foo_zero_or_more = foo[0, ...]
    assert isinstance(foo_zero_or_more.pattern, text_type)
    for i in range(10):
        assert foo_zero_or_more.match(u'foo' * i)


def test_repeat_zero_or_more_bytes():
    foo = r(b'foo')
    foo_zero_or_more = foo[0, ...]
    assert isinstance(foo_zero_or_more.pattern, bytes)
    for i in range(10):
        assert foo_zero_or_more.match(b'foo' * i)


def test_repeat_one_or_more_text():
    foo = r(u'foo')
    foo_one_or_more = foo[1, ...]
    assert isinstance(foo_one_or_more.pattern, text_type)
    for i in range(1, 10):
        assert foo_one_or_more.match(u'foo' * i)


def test_repeat_one_or_more_bytes():
    foo = r(b'foo')
    foo_one_or_more = foo[1, ...]
    assert isinstance(foo_one_or_more.pattern, bytes)
    for i in range(1, 10):
        assert foo_one_or_more.match(b'foo' * i)


def test_repeat_n_or_more_text():
    foo = r(u'foo')
    for n in range(2, 5):
        foo_n_or_more = foo[n, ...]
        assert isinstance(foo_n_or_more.pattern, text_type)
        for i in range(n, 10):
            assert foo_n_or_more.match(u'foo' * i)


def test_repeat_n_or_more_bytes():
    foo = r(b'foo')
    for n in range(2, 5):
        foo_n_or_more = foo[n, ...]
        assert isinstance(foo_n_or_more.pattern, bytes)
        for i in range(n, 10):
            assert foo_n_or_more.match(b'foo' * i)


def test_check_r_argument_is_valid_regexp():
    with raises(re.error):
        r('(')


def test_numbered_groups_text():
    foo = r(u'foo').grouped()
    assert isinstance(foo.pattern, text_type)
    bar = r(u'bar')
    foobar = foo + bar
    match = foobar.match(u'foobar')
    assert match.group(1) == u'foo'


def test_numbered_groups_bytes():
    foo = r(b'foo').grouped()
    assert isinstance(foo.pattern, bytes)
    bar = r(b'bar')
    foobar = foo + bar
    match = foobar.match(b'foobar')
    assert match.group(1) == b'foo'


def test_named_groups_text():
    foo = r(u'foo').grouped('group')
    assert isinstance(foo.pattern, text_type)
    bar = r(u'bar')
    foobar = foo + bar
    match = foobar.match(u'foobar')
    assert match.group('group') == u'foo'


def test_named_groups_bytes():
    foo = r(b'foo').grouped('group')
    assert isinstance(foo.pattern, bytes)
    bar = r(b'bar')
    foobar = foo + bar
    match = foobar.match(b'foobar')
    assert match.group('group') == b'foo'

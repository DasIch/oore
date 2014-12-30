# encoding: utf-8
"""
    test_oore
    ~~~~~~~~~

    :copyright: 2014 by Daniel Neuhäuser
    :license: BSD, see LICENSE.rst for details
"""
from oore import cached_property, r

from pytest import raises


class TestCachedProperty(object):
    def test_getter(self):
        calls = [0]

        class Foo(object):
            @cached_property
            def attribute(self):
                calls[0] += 1
                return 'attribute'

        foo = Foo()
        assert foo.attribute == 'attribute'
        assert foo.attribute == 'attribute'
        assert calls == [1]

    def test_setter(self):
        calls = [0]

        class Foo(object):
            @cached_property
            def attribute(self):
                calls[0] += 1
                return 'attribute'

        foo = Foo()
        foo.attribute = 'overwritten'
        assert foo.attribute == 'overwritten'
        assert calls == [0]


def test_add_text():
    foo = r(u'foo')
    bar = r(u'bar')
    foobar = foo + bar
    assert foobar.match(u'foobar')


def test_add_bytes():
    foo = r(b'foo')
    bar = r(b'bar')
    foobar = foo + bar
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
    assert foo_3.match(u'foo' * 3)


def test_repeat_bytes():
    foo = r(b'foo')
    foo_3 = foo[3]
    assert foo_3.match(b'foo' * 3)


def test_repeat_from_to_text():
    foo = r(u'foo')
    foo_2_to_4 = foo[2, 4]
    for i in range(2, 5):
        assert foo_2_to_4.match(u'foo' * i)


def test_repeat_from_to_bytes():
    foo = r(b'foo')
    foo_2_to_4 = foo[2, 4]
    for i in range(2, 5):
        assert foo_2_to_4.match(b'foo' * i)


def test_repeat_zero_or_more_text():
    foo = r(u'foo')
    foo_zero_or_more = foo[0, ...]
    for i in range(10):
        assert foo_zero_or_more.match(u'foo' * i)


def test_repeat_zero_or_more_bytes():
    foo = r(b'foo')
    foo_zero_or_more = foo[0, ...]
    for i in range(10):
        assert foo_zero_or_more.match(b'foo' * i)


def test_repeat_one_or_more_text():
    foo = r(u'foo')
    foo_one_or_more = foo[1, ...]
    for i in range(1, 10):
        assert foo_one_or_more.match(u'foo' * i)


def test_repeat_one_or_more_bytes():
    foo = r(b'foo')
    foo_one_or_more = foo[1, ...]
    for i in range(1, 10):
        assert foo_one_or_more.match(b'foo' * i)


def test_repeat_n_or_more_text():
    foo = r(u'foo')
    for n in range(2, 5):
        foo_n_or_more = foo[n, ...]
        for i in range(n, 10):
            assert foo_n_or_more.match(u'foo' * i)


def test_repeat_n_or_more_bytes():
    foo = r(b'foo')
    for n in range(2, 5):
        foo_n_or_more = foo[n, ...]
        for i in range(n, 10):
            assert foo_n_or_more.match(b'foo' * i)

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import textwrap

import pytest

from pre_commit_hooks.string_fixer import main

TESTS = (
    # Base cases
    ("''", "''", 0),
    ('""', "''", 1),
    (r'"\'"', r'"\'"', 0),
    (r'"\""', r'"\""', 0),
    (r"'\"\"'", r"'\"\"'", 0),
    # String somewhere in the line
    ('x = "foo"', "x = 'foo'", 1),
    # Test escaped characters
    (r'"\'"', r'"\'"', 0),
    # Docstring
    ('""" Foo """', '""" Foo """', 0),
    (
        textwrap.dedent("""
        x = " \\
        foo \\
        "\n
        """),
        textwrap.dedent("""
        x = ' \\
        foo \\
        '\n
        """),
        1,
    ),
    ('"foo""bar"', "'foo''bar'", 1),
)


@pytest.mark.parametrize(('input_s', 'output', 'expected_retval'), TESTS)
def test_rewrite(input_s, output, expected_retval, tmpdir):
    path = tmpdir.join('file.txt')
    path.write(input_s)
    retval = main([path.strpath])
    assert path.read() == output
    assert retval == expected_retval

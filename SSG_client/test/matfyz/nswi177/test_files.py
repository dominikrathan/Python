#!/usr/bin/env python
# pylint: disable=missing-docstring

from nose.tools import eq_

from matfyz.nswi177.files import relative_paths_walk


def test_relative_paths_walk_with_filter():
    result = [
        (a, b, c)
        for (a, b, c) in relative_paths_walk('test/', '*.py')
        if a == 'test/matfyz/nswi177/test_files.py'
    ]
    eq_(len(result), 1)
    eq_(result[0][0], 'test/matfyz/nswi177/test_files.py')
    eq_(result[0][1], 'matfyz/nswi177/test_files.py')
    eq_(result[0][2], 'matfyz/nswi177')

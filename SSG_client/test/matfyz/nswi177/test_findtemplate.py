#!/usr/bin/env python
# pylint: disable=missing-docstring

from nose.tools import eq_

import pathlib
import matfyz.nswi177.my_ssg as my_ssg


def test_template_found():
    current_dir = pathlib.Path(__file__).parent.absolute()
    filename_result = my_ssg.get_template_filename(current_dir)
    filename_expected = "main.j2"
    eq_(filename_result, filename_expected)

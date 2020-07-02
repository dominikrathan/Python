#!/usr/bin/env python
# pylint: disable=missing-docstring

from nose.tools import eq_

import os
import pathlib
import markdown
import matfyz.nswi177.my_ssg as my_ssg


def test_markdownify_template():
    current_dir = pathlib.Path(__file__).parent.absolute()

    template = my_ssg.get_markdownify_template(current_dir)
    markdown_content = open(os.path.join(current_dir,"content.md"), "r").read()
    rendered = template.render(content=markdown_content)

    from markdown import markdown
    expected = markdown(markdown_content)

    eq_(rendered,expected)

#!/usr/bin/env python
# pylint: disable=missing-docstring

from nose.tools import eq_

import os
import shutil
import pathlib
import matfyz.nswi177.my_ssg as my_ssg

def remove_whitespace(s):
    return "".join(s.split())

def test_whole_output():
    current_dir = pathlib.Path(__file__).parent.absolute()

    output_folder = os.path.join(current_dir,"input_test_extension","out")
    if (os.path.exists(output_folder)):
        shutil.rmtree(output_folder)

    import subprocess
    subprocess.call([os.path.join(current_dir,"input_test_extension","run.sh")])

#!/usr/bin/env python
# pylint: disable=missing-docstring

from nose.tools import eq_

import os
import shutil
import pathlib
import matfyz.nswi177.my_ssg as my_ssg
from nose.tools import nottest

def remove_whitespace(s):
    return "".join(s.split())

@nottest
def compare_files(file_name1, file_name2):
    file1 = open(file_name1, 'r').read()
    file2 = open(file_name2, 'r').read()

    eq_(file1, file2)

@nottest
def test_case(input_directory, expected_directory):
    current_dir = pathlib.Path(__file__).parent.absolute()

    output_folder = os.path.join(current_dir,input_directory,"out")
    if (os.path.exists(output_folder)):
        shutil.rmtree(output_folder)

    import subprocess
    subprocess.call([os.path.join(current_dir,input_directory,"run.sh")])

    compare_files(
        os.path.join(output_folder,"index.html"),
        os.path.join(current_dir, expected_directory, "index.html")
        )

    compare_files(
        os.path.join(output_folder,"labs/index.html"),
        os.path.join(current_dir, expected_directory, "labs/index.html")
        )

    compare_files(
        os.path.join(output_folder,"tasks/index.html"),
        os.path.join(current_dir, expected_directory, "tasks/index.html")
        )

def test_whole_output():
    test_case("input_test", "output_expected")

def test_whole_output_extension():
    test_case("input_test_extension", "output_expected_extension")

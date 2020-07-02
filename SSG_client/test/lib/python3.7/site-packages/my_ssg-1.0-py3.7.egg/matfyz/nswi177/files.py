#!/usr/bin/env python3

"""
File-related utilities.
"""

import fnmatch
import os


def relative_paths_walk(base_dir, filename_filter='*'):
    """
    Wrapper for os.walk that computes relative paths along the way.

    Parameters
    ----------
    base_dir: str
        Where to start the (recursive) walk.
    filename_filter: str
        Optional fnmach-style filter (i.e. shell wildcards).

    Returns
    -------
    Tuple of full filename (including `base_dir), relative filename
    (i.e. to `base_dir`) and relative directory name (also to `base_dir`).
    """

    for (directory_name, _, filenames) in os.walk(base_dir):
        relative_directory_name = os.path.relpath(directory_name, base_dir)
        for filename in fnmatch.filter(filenames, filename_filter):
            full_filename = os.path.join(directory_name, filename)
            relative_filename = os.path.join(relative_directory_name, filename)
            yield (full_filename, relative_filename, relative_directory_name)
